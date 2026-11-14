"""Bound the moving local compensated trace row in its weak divergence form."""

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import r4c1_canonical_density_factory_v1 as factory
from test_rtau_nonlocal_trace_drift_v1 import ROOT, GATE, OUT, digest, read

CONTRACT = GATE+'RES001_RTAU_LOCAL_TRACE_DRIFT_V1_CONTRACT_2026-11-13.md'
PARENT = OUT+'rtau_nonlocal_trace_drift_v1_20261113/receipt.json'
LIFT = OUT+'rtau_strong_constraint_lift_v4_20261104/receipt.json'
ACCEL = OUT+'r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
TIME = 200


def mixed_time_engine(dual):
    def product(self, other):
        other = self.cast(other)
        zero = self.scalar(0)
        keys = self.g.keys() | other.g.keys()
        g = {i: self.g.get(i, zero)*other.c+other.g.get(i, zero)*self.c for i in keys}
        h = {k: self.h.get(k, zero)*other.c+other.h.get(k, zero)*self.c
             for k in self.h.keys() | other.h.keys()}
        for i in keys:
            if i != TIME:
                k = (min(i, TIME), max(i, TIME))
                h[k] = h.get(k, zero)+self.g.get(i, zero)*other.g.get(TIME, zero)
                h[k] += self.g.get(TIME, zero)*other.g.get(i, zero)
        return type(self)(self.c*other.c, {i:v for i,v in g.items() if v != 0},
                          {k:v for k,v in h.items() if v != 0})

    def unary(self, value, first, second):
        zero = self.scalar(0)
        h = {k:first*v for k,v in self.h.items()}
        for i in self.g:
            if i != TIME:
                k = (min(i, TIME), max(i, TIME))
                h[k] = h.get(k, zero)+second*self.g[i]*self.g.get(TIME, zero)
        return type(self)(value, {i:first*v for i,v in self.g.items()},
                          {k:v for k,v in h.items() if v != 0})

    dual.__mul__ = dual.__rmul__ = product
    dual.unary = unary


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    decode = lambda x: iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary = lambda x: [list(v) for v in iv.mpf(x)._mpi_]
    parent = read(PARENT)
    pins = dict(parent['source_pins'])
    for rel in (CONTRACT, PARENT, 'Analysis/MasterTests/test_rtau_nonlocal_trace_drift_v1.py'):
        path = ROOT/rel
        expected = Path(str(path)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel] == expected, rel
        pins[rel] = expected
    snap = {}
    for rel, expected in pins.items():
        p = ROOT/rel
        assert digest(p) == expected, rel
        for f in (p, Path(str(p)+'.sha256')):
            if f.exists():
                snap[f] = (digest(f), f.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks'])
    ctx = factory.prepare()
    mp.mp.dps, mp.iv.dps = 100, 60
    J, D = ctx['J'], ctx['D']
    mixed_time_engine(D)
    deriv = lambda x: J(coefficients=[x.c[1], 2*x.c[2], iv.mpf(0)])
    grad = lambda x,i: x.g.get(i,J(0))
    mixed = lambda x,i: x.h.get((min(i,TIME),max(i,TIME)),J(0))
    checks = {}
    x, t = sp.symbols('x t')
    exact = sp.exp(x*t)/(2+x)+sp.sqrt(3+x*x)
    X = D(J(iv.mpf(2)/5), {0:J(1)})
    T = D(J(iv.mpf(1)/3), {TIME:J(1)})
    test = (X*T).exp()/(2+X)+(3+X*X)**mp.mpf('.5')
    target = iv.mpf(str(sp.N(sp.diff(exact,x,t).subs({x:sp.Rational(2,5),t:sp.Rational(1,3)}),85)))
    checks['mixed_time_engine_matches_independent_symbolic_derivative'] = ab(mixed(test,0).c[0]-target) < mp.mpf('1e-50')
    acceleration = read(ACCEL)
    bound = {k:decode(v) for k,v in acceleration['bounds'].items()}
    symmetric = lambda value: iv.mpf([-hi(value),hi(value)])
    box = lambda value: J(symmetric(value))
    total_acc = bound['original_final_acceleration']
    particular = bound['particular_acceleration']
    shift_rate = [box(bound['xi_transverse'])]*2+[box(bound['original_shift_rate_z'])]
    shift_gradient_rate = [box(bound['original_shift_rate_derivative_xy'])]*2+[box(bound['original_shift_rate_derivative_z'])]
    records = []
    for cell in read(LIFT)['cells']:
        y,_ = ctx['state'](J.variable(decode(cell['z'])), True, [0,0,0])
        q,v,g,S,Sz = y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
        vz = [deriv(a) for a in v]
        yt = v+[box(total_acc)]*13+[J(0)]+vz+shift_rate+shift_gradient_rate
        variables = [D(a,{i:J(1),TIME:r}) for i,(a,r) in enumerate(zip(y,yt))]
        total = ctx['env']['density'](ctx['env']['lifted'](variables))[0]
        Q,V,G,SS = variables[:14],variables[14:28],variables[28:42],variables[42:45]
        N,mu,gamma,H,_ = ctx['geometry'](Q,G)
        proper = (V[12]-SS[2]*G[12])/N
        rest = [H[i][2]*G[12]+Q[6+i]*(proper+Q[8]*G[12]/(gamma+1)) for i in range(3)]
        h = [[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        Y = sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))+2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0]) > 0
        pars = ctx['env']['env']['exact']
        rat = lambda a: iv.mpf(int(a.p))/int(a.q)
        b,beta = iv.mpf(5)/11,iv.mpf(2)/5
        force = (gamma*proper+Q[8]*G[12])**2*(rat(pars['K_Q'])/2)-Y**mp.mpf('1.5')*rat(pars['A'])
        reg = N*mu*Q[13]**2*(b/2)-N*mu*H[2][2]*G[13]*G[12]*b+N*mu*Q[13]*H[2][2]*G[12]**2*(b*beta)
        ordinary = total-N*mu*force-reg
        # Ordinary clock/auxiliary momenta vanish by the inherited exact dependency proof.
        p = [grad(total,14+i) for i in range(12)]+[J(0),J(0)]
        pt = [grad(total,i)-deriv(grad(total,28+i)) for i in range(12)]+[J(0),J(0)]
        U = [a-c for a,c in zip(v,ctx['lie'](q,g,S,Sz))]
        lie_v = ctx['lie'](v,vz,S,Sz)
        Ut = [box(particular)-a for a in lie_v]
        # Canonical ordinary flux, with independent momentum coordinates.
        qshape, dshape = [J(0)]*14,[J(0)]*14
        qshape_t,dshape_t = [J(0)]*14,[J(0)]*14
        for i in (0,3):
            qshape[i],dshape[i] = q[0],g[0]
            qshape_t[i],dshape_t[i] = v[0],vz[0]
        QQ = [D(a,{0:s,TIME:r},{(0,TIME):sr}) for a,s,r,sr in zip(q,qshape,v,qshape_t)]
        GG = [D(a,{0:s,1:ss,TIME:r},{(0,TIME):sr,(1,TIME):ssr})
              for a,s,ss,r,sr,ssr in zip(g,dshape,qshape,vz,dshape_t,qshape_t)]
        PP = [D(a,{TIME:r}) for a,r in zip(p,pt)]
        n,vol,frame,inv,curvature = ctx['geometry'](QQ,GG)
        flux = sum((n*frame*inv[i][2]*PP[6+i] for i in range(3)),D(0))-n*curvature/2
        Io = ordinary.c-sum((a*c for a,c in zip(p,U)),J(0))-deriv(flux.c)
        Iot = grad(ordinary,TIME)-sum((a*c+aa*cc for a,c,aa,cc in zip(pt,U,p,Ut)),J(0))-deriv(grad(flux,TIME))
        # Index variation of Lie_S q at fixed gradient, including its moving shape.
        index = ctx['lie'](qshape,[J(0)]*14,[J(0)]*3,Sz)
        index_t = [a+c for a,c in zip(ctx['lie'](qshape_t,[J(0)]*14,[J(0)]*3,Sz),ctx['lie'](qshape,[J(0)]*14,[J(0)]*3,shift_gradient_rate))]
        B = sum((grad(ordinary,28+i)+S[2]*p[i] for i in (0,3)),J(0))
        Bt = sum((mixed(ordinary,28+i)+shift_rate[2]*p[i]+S[2]*pt[i] for i in (0,3)),J(0))
        At = (v[0]*(grad(ordinary,0)+grad(ordinary,3))
              +q[0]*(mixed(ordinary,0)+mixed(ordinary,3))
              +vz[0]*B+g[0]*Bt
              +sum((a*c+aa*cc for a,c,aa,cc in zip(pt,index,p,index_t)),J(0))-Iot)
        B_t = v[0]*B+q[0]*Bt
        records.append({ 'cell':cell['cell'], 'A_t':At.c[0], 'B_t':B_t.c[0],
                         'C_t':mixed(flux,0).c[0], 'E_t':mixed(flux,1).c[0] })
    sup = lambda key: iv.mpf(max(ab(r[key]) for r in records))
    bounds = {key:sup(key) for key in ('A_t','B_t','C_t','E_t')}
    bounds['local_H1_to_Hminus1'] = sum(bounds.values(),iv.mpf(0))
    nonlocal_bound = decode(parent['bounds_binary']['Kdot_L2_to_L2'])
    bounds['combined_H1_to_Hminus1'] = bounds['local_H1_to_Hminus1']+nonlocal_bound
    checks.update(all_sixteen_cells_retained=len(records)==16,
                  all_coefficient_bounds_finite=all(mp.isfinite(hi(a)) for a in bounds.values()),
                  mixed_engine_discards_unneeded_second_time_derivatives=(TIME,TIME) not in test.h,
                  source_bytes_and_timestamps_preserved=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items()))
    assert all(checks.values()), checks
    return dict(kind='RTAU_LOCAL_TRACE_DRIFT_V2',source_sha256=digest(Path(__file__)),
                source_pins=pins,pinned_sources=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                bounds_binary={k:binary(v) for k,v in bounds.items()},
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                cells=[{k:binary(v) if k!='cell' else v for k,v in r.items()} for r in records],
                scope='CONDITIONAL_INITIAL_MOVING_TRACE_LOCAL_ROW',
                moving_free_source='OPEN',full_coupled_energy='OPEN',review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path)
    group.add_argument('--replay',type=Path)
    args=parser.parse_args()
    payload=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if args.replay:
        assert args.replay.read_bytes()==payload
        print('Byte-identical read-only replay')
    else:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as stream:
            stream.write(payload)
        print('Local trace drift controls complete')


if __name__=='__main__':
    main()
