"""Actual canonical source-rate and normalized momentum-lift bounds."""

import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_trace_momentum_drift_v2 import first_differentials_only
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_FREE_MOMENTUM_SOURCE_RATE_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_rate_input_multipliers_v1_20261114/receipt.json'
LIFT=OUT+'rtau_strong_constraint_lift_v4_20261104/receipt.json'
CLOCK=OUT+'r4c1_rtau_clock_density_v3_attempt_01/summary.json'
LABELS=['q_free_H1','p_free_L2','q_free_rate_L2','ordinary_p_free_rate_Hminus1',
        'clock_p_rate_Hminus2','momentum_mean','momentum_mean_rate']


def exact_controls():
    x,t=sp.symbols('x t')
    def modes(f):
        return [(term.as_powers_dict().get(x,0),term) for term in sp.Add.make_args(sp.expand(f))]
    def dz(f):return sp.expand(sum(sp.I*n*term for n,term in modes(f)))
    def mean(f):return sum(term for n,term in modes(f) if n==0)
    def primitive(f):return sp.expand(sum(term/(sp.I*n) for n,term in modes(f) if n))
    at=lambda f:sp.expand(f.subs(t,0))
    rate=lambda f:at(sp.diff(f,t))
    B,pf,qf,p,q,u,w=[i+2+x/(i+3)+1/(x*(i+4))+t*(i+1+x**2/(i+5)) for i in range(7)]
    source=-dz(B*pf+qf*p)+pf*dz(q)+p*dz(qf)
    source_rate=-dz(sp.diff(B,t)*pf+B*sp.diff(pf,t)+sp.diff(qf,t)*p+qf*sp.diff(p,t))
    source_rate+=sp.diff(pf,t)*dz(q)+pf*dz(sp.diff(q,t))+sp.diff(p,t)*dz(qf)+p*dz(sp.diff(qf,t))
    eta=2+3*t
    y=u*primitive(w*source)
    output=y+u*(eta-mean(y))/mean(u)
    yt=sp.diff(u,t)*primitive(w*source)+u*primitive(sp.diff(w,t)*source+w*source_rate)
    normal=(eta-mean(y))/mean(u)
    split=yt+sp.diff(u,t)*normal+u*(sp.diff(eta,t)-mean(yt)-mean(sp.diff(u,t))*normal)/mean(u)
    return dict(actual_source_product_rate=rate(source)==at(source_rate),
                actual_normalized_lift_rate=rate(output)==at(split),
                prescribed_mean_rate_retained=sp.simplify(mean(rate(output))-3)==0,
                normalization_drift_omission_detected=at(sp.diff(u,t)*normal)!=0,
                integrating_factor_rate_omission_detected=at(u*primitive(sp.diff(w,t)*source))!=0,
                total_clock_momentum_scalar_term_required=at(pf*dz(q))!=0)


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
        path=ROOT/rel
        h=Path(str(path)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        path=ROOT/rel
        assert digest(path)==h,rel
        for p in (path,Path(str(path)+'.sha256')):
            if p.exists():snap[p]=(digest(p),p.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks'])
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J,D=ctx['J'],ctx['D']
    first_differentials_only(D)
    grad=ctx['gradient']
    checks=exact_controls()
    def Bmatrix(q):
        h=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
        B=[[J(0) for _ in range(3)] for _ in range(13)]
        for k,(a,b) in enumerate(ctx['hm']):
            for i in range(3):B[k][i]=(h[a][i] if b==2 else J(0))+(h[b][i] if a==2 else J(0))
        for i in range(3):B[6+i][i]=-q[8]
        return B
    def norm(values,order=0):
        def row(j):return iv.sqrt(sum((iv.mpf(ab(v.c[j]*(2 if j==2 else 1)))**2 for v in values),iv.mpf(0)))
        return row(0)+(row(1) if order>=1 else 0)+(row(1)+row(2) if order==2 else 0)
    third_bound=hi(decode(read(CLOCK)['whole_circle_third_shift_bound']))
    third=iv.mpf([-third_bound,third_bound])
    records=[]
    for cell in read(LIFT)['cells']:
        y,_=ctx['state'](J.variable(decode(cell['z'])),True,[third]*3)
        action=ctx['evaluate'](y)
        assert not action.h
        q,v,g=y[:14],y[14:28],y[28:42]
        p=[grad(action,14+i) for i in range(13)]
        pt=[grad(action,i).c[0]-grad(action,28+i).c[1] for i in range(13)]
        B,Bt=Bmatrix(q),Bmatrix(v)
        a=q[0]**mp.mpf('.5')
        L=v[0]/(2*q[0])
        dp_norm=iv.sqrt(sum((iv.mpf(ab(x))**2 for x in pt),iv.mpf(0)))
        per_axis=[]
        for i,j in enumerate((2,2,1)):
            jac=[]
            jac_t=[]
            for k in range(13):
                basis=Bmatrix([J(int(k==m)) for m in range(14)])
                jac.append(sum((basis[n][i]*p[n] for n in range(13)),J(0)))
                jac_t.append(sum((basis[n][i]*J(pt[n]) for n in range(13)),J(0)))
            Bi=[row[i] for row in B]
            Bti=[row[i] for row in Bt]
            assert all(Bi[12].c[n]==0 for n in range(3))
            s=[norm(jac),norm(Bi),iv.mpf(0),iv.mpf(0),iv.mpf(0)]
            st=[norm(jac_t),norm(Bti),norm(jac),norm(Bi[:12],1),iv.mpf(0)]
            if i==2:
                s[0]+=norm(p)
                s[1]+=norm(g[:13])
                st[0]+=dp_norm
                st[1]+=iv.sqrt(sum((iv.mpf(ab(z.c[1]))**2 for z in v[:13]),iv.mpf(0)))
                st[2]+=norm(p,1)
                st[3]+=norm(g[:12],1)
                st[4]+=norm([g[12]],2)
            u=a**(-j)
            ut=-j*u*L
            w=1/(2*a) if i==2 else J(1)
            wt=-w*L if i==2 else J(0)
            per_axis.append(dict(source=s,source_rate=st,u=u,ut=ut,w=w,wt=wt))
        records.append(dict(cell=cell['cell'],L=L.c[0],axes=per_axis))
    spanL=iv.mpf(max(hi(r['L']) for r in records))-iv.mpf(min(lo(r['L']) for r in records))
    rows=[]
    source_rows=[]
    rate_rows=[]
    for i,j in enumerate((2,2,1)):
        axis=[r['axes'][i] for r in records]
        u0=iv.mpf(max(ab(a['u'].c[0]) for a in axis))
        u1=iv.mpf(max(hi(norm([a['u']],1)) for a in axis))
        umin=iv.mpf(min(lo(a['u'].c[0]) for a in axis))
        assert lo(umin)>0
        ut0=iv.mpf(max(ab(a['ut'].c[0]) for a in axis))
        w1=iv.mpf(max(hi(norm([a['w']],1)) for a in axis))
        w2=iv.mpf(max(hi(norm([a['w']],2)) for a in axis))
        wt1=iv.mpf(max(hi(norm([a['wt']],1)) for a in axis))
        n0=u0/umin
        ndot=j*spanL*n0
        projected=1+n0
        initial=2*u0*w1
        source_factor=projected*2*(ut0*w1+u0*wt1)+ndot*initial
        rate_factor=projected*2*u1*w2
        s=[iv.mpf(max(hi(a['source'][k]) for a in axis)) for k in range(5)]
        st=[iv.mpf(max(hi(a['source_rate'][k]) for a in axis)) for k in range(5)]
        source_rows.append(s)
        rate_rows.append(st)
        rows.append([source_factor*ss+rate_factor*rr for ss,rr in zip(s,st)]+[ndot,n0])
    bdot_flux=[]
    for k in range(7):
        bound=iv.mpf(0)
        for i,slot in enumerate((2,4,5)):
            coeff=parent['column_bounds_binary']['U'][slot]
            U1=decode(coeff[0])+decode(coeff[1])
            bound+=U1*rows[i][k]
        bdot_flux.append(bound)
    checks.update(all_sixteen_cells_and_three_axes_retained=len(records)==16 and len(rows)==3,
                  all_clock_rate_transverse_columns_zero=all(lo(rate_rows[i][4])==hi(rate_rows[i][4])==0 for i in (0,1)),
                  longitudinal_clock_rate_coefficient_positive=lo(rate_rows[2][4])>0,
                  finite_nonnegative_coefficients=all(lo(v)>=0 and mp.isfinite(hi(v)) for row in rows for v in row),
                  original_sources_and_sidecars_preserved=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_FREE_MOMENTUM_SOURCE_RATE_V1',source_sha256=digest(Path(__file__)),source_pins=pins,pinned_sources=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],input_order=LABELS,
                source_Hminus1_binary=[[binary(v) for v in r] for r in source_rows],
                source_rate_Hminus2_binary=[[binary(v) for v in r] for r in rate_rows],
                normalized_momentum_rate_Hminus1_binary=[[binary(v) for v in r] for r in rows],
                ordinary_current_of_moving_lift_Hminus1_binary=[binary(v) for v in bdot_flux],
                upper_display=[[mp.nstr(hi(v),25) for v in r] for r in rows],
                scope='CONDITIONAL_INITIAL_ACTUAL_FREE_SOURCE_AND_NORMALIZATION_RATE',full_source_composition='OPEN',
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
        print('Moving free-momentum source controls complete')


if __name__=='__main__':main()
