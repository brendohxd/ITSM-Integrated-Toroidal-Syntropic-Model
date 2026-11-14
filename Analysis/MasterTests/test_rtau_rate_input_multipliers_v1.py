"""Initial ordinary source maps on L2 field and Hminus1 momentum rates."""

import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_trace_momentum_drift_v2 import first_differentials_only
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_RATE_INPUT_MULTIPLIERS_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_source_weight_rates_v1_20261113/receipt.json'
LIFT=OUT+'rtau_strong_constraint_lift_v4_20261104/receipt.json'
CLOCK=OUT+'r4c1_rtau_clock_density_v3_attempt_01/summary.json'


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    ab=lambda x:max(abs(lo(x)),abs(hi(x)))
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    parent=read(PARENT)
    pins=dict(parent['source_pins'])
    for rel in (CONTRACT,PARENT,'Analysis/MasterTests/test_rtau_trace_momentum_drift_v2.py'):
        p=ROOT/rel
        expected=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==expected,rel
        pins[rel]=expected
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel
        assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks'])
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J,D=ctx['J'],ctx['D']
    first_differentials_only(D)
    grad=lambda f,i:f.g.get(i,J(0))
    deriv=lambda f:J(coefficients=[f.c[1],2*f.c[2],iv.mpf(0)])
    thirdbound=hi(decode(read(CLOCK)['whole_circle_third_shift_bound']))
    third=iv.mpf([-thirdbound,thirdbound])
    checks={}
    records=[]
    for cell in read(LIFT)['cells']:
        y,_=ctx['state'](J.variable(decode(cell['z'])),True,[third]*3)
        variables=[D.var(a,i) for i,a in enumerate(y)]
        total=ctx['env']['density'](ctx['env']['lifted'](variables))[0]
        assert not total.h
        Q,V,G,SS=variables[:14],variables[14:28],variables[28:42],variables[42:45]
        N,mu,gamma,H,_=ctx['geometry'](Q,G)
        proper=(V[12]-SS[2]*G[12])/N
        rest=[H[i][2]*G[12]+Q[6+i]*(proper+Q[8]*G[12]/(gamma+1)) for i in range(3)]
        h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))+2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0
        pars=ctx['env']['env']['exact']
        rat=lambda a:iv.mpf(int(a.p))/int(a.q)
        b,beta=iv.mpf(5)/11,iv.mpf(2)/5
        force=(gamma*proper+Q[8]*G[12])**2*(rat(pars['K_Q'])/2)-Y**mp.mpf('1.5')*rat(pars['A'])
        reg=N*mu*Q[13]**2*(b/2)-N*mu*H[2][2]*G[13]*G[12]*b+N*mu*Q[13]*H[2][2]*G[12]**2*(b*beta)
        ordinary=total-N*mu*force-reg
        q,v,g,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
        p=[grad(total,14+i) for i in range(12)]+[J(0),J(0)]
        U=[a-c for a,c in zip(v,ctx['lie'](q,g,S,Sz))]
        QQ=[D.var(a,i) for i,a in enumerate(q)]
        GG=[D.var(a,28+i) for i,a in enumerate(g)]
        PP=[D.var(a,100+i) for i,a in enumerate(p)]
        n,vol,frame,inv,curvature=ctx['geometry'](QQ,GG)
        flux=sum((n*frame*inv[i][2]*PP[6+i] for i in range(3)),D(0))-n*curvature/2
        Io=ordinary.c-sum((a*c for a,c in zip(p,U)),J(0))-deriv(flux.c)
        measure=N*mu
        rows={k:[] for k in ('a','b','Fq','Fd','U','Fp')}
        for i in range(14):
            basis=[J(int(i==j)) for j in range(14)]
            index=ctx['lie'](basis,[J(0)]*14,[J(0)]*3,Sz)
            A=grad(ordinary,i)+sum((a*c for a,c in zip(p,index)),J(0))-Io*grad(measure,i)/measure.c
            B=grad(ordinary,28+i)+S[2]*p[i]
            values=dict(a=A,b=B,Fq=grad(flux,i),Fd=grad(flux,28+i),
                        U=U[i] if i<12 else J(0),Fp=grad(flux,100+i))
            if i==13:
                checks['auxiliary_absence_consistency_cell_'+str(cell['cell'])]=all(lo(values[k].c[0])<=0<=hi(values[k].c[0]) for k in ('a','b','Fq','Fd'))
                for k in ('a','b','Fq','Fd'):values[k]=J(0)
            for k,f in values.items():
                rows[k].append([f.c[0],f.c[1]])
        records.append(dict(cell=cell['cell'],**rows))
    bounds={}
    columns={}
    for key in rows:
        col=[[iv.mpf(max(ab(r[key][i][j]) for r in records)) for j in range(2)] for i in range(14)]
        # One vector norm for each spatial order bounds the pointwise row.
        order_norm=[iv.sqrt(sum((c[j]*c[j] for c in col),iv.mpf(0))) for j in range(2)]
        bounds[key+'_sup']=order_norm[0]
        if key in ('b','Fd','U','Fp'):
            bounds[key+'_multiplier_Hminus1']=sum(order_norm,iv.mpf(0))
        columns[key]=[[binary(x) for x in c] for c in col]
    bounds['configuration_L2_to_Hminus2']=bounds['a_sup']+bounds['b_multiplier_Hminus1']+bounds['Fq_sup']+bounds['Fd_multiplier_Hminus1']
    bounds['momentum_Hminus1_to_Hminus2']=bounds['U_multiplier_Hminus1']+bounds['Fp_multiplier_Hminus1']
    z=sp.symbols('z',real=True)
    multiplier=2+sp.sin(z)/3
    u,w=sp.cos(2*z),sp.sin(3*z)
    checks.update(exact_periodic_derivative_pairing=sp.simplify(sp.integrate(multiplier*sp.diff(u,z)*w+u*sp.diff(multiplier*w,z),(z,0,2*sp.pi)))==0,
                  multiplier_duality_retains_derivative=sp.expand(sp.diff(multiplier*w,z)-multiplier*sp.diff(w,z)-sp.diff(multiplier,z)*w)==0,
                  all_fourteen_columns_and_sixteen_cells_retained=len(records)==16 and all(len(r[k])==14 for r in records for k in rows),
                  finite_positive_operator_bounds=all(lo(bounds[k])>0 and mp.isfinite(hi(bounds[k])) for k in ('configuration_L2_to_Hminus2','momentum_Hminus1_to_Hminus2')),
                  source_bytes_and_sidecars_preserved=all((digest(p),p.stat().st_mtime_ns)==s for p,s in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_RATE_INPUT_MULTIPLIERS_V1',source_sha256=digest(Path(__file__)),source_pins=pins,pinned_sources=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                bounds_binary={k:binary(v) for k,v in bounds.items()},column_bounds_binary=columns,
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                scope='CONDITIONAL_INITIAL_ORDINARY_RATE_INPUT_MAPS',moving_momentum_source='OPEN',full_source_composition='OPEN',
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


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
        with args.output.open('xb') as f:f.write(payload)
        print('Ordinary rate-input multiplier controls complete')


if __name__=='__main__':main()
