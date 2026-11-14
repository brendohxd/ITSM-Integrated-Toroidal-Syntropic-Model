"""Initial measure/clock source-weight rates in the declared weak spaces."""

import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_SOURCE_WEIGHT_RATES_V1_CONTRACT_2026-11-13.md'
PARENT=OUT+'rtau_free_coefficient_drift_v1_20261113/receipt.json'
NORMAL1=OUT+'rtau_strong_density_normal_form_v1_20261103/receipt.json'
NORMAL2=OUT+'rtau_strong_density_normal_form_v2_20261103/receipt.json'


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
    for rel in (CONTRACT,PARENT,NORMAL1,NORMAL2):
        path=ROOT/rel
        expected=Path(str(path)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==expected,rel
        pins[rel]=expected
    snap={}
    for rel,h in pins.items():
        path=ROOT/rel
        assert digest(path)==h,rel
        for f in (path,Path(str(path)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for p in (parent,read(NORMAL1),read(NORMAL2)) for c in p['checks'])
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J=ctx['J']
    y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q,v,g=y[:14],y[14:28],y[28:42]
    N,mu,_,_,_=ctx['geometry'](q,g)
    M=N*mu
    L=v[0]/(2*q[0])
    Mt=M*(-v[12]*(iv.mpf(2)/5)+3*L)
    M0,Mz,Mtime=[iv.mpf(ab(z)) for z in (M.c[0],M.c[1],Mt.c[0])]
    cdata=read(NORMAL1)['bounds_binary']
    adata=read(NORMAL2)['bounds_binary']
    c,ct,cz=[decode(cdata[k]) for k in ('coefficient','coefficient_time','coefficient_z')]
    alpha,at,az=[decode(adata[k]) for k in ('alpha','alpha_time','alpha_z')]
    bounds=dict(measure_sup=M0,measure_spatial_rate_sup=Mz,measure_time_rate_sup=Mtime,
                Mc_time_sup=Mtime*c+M0*ct,
                Malpha_time_sup=Mtime*alpha+M0*at,
                measure_multiplier_Hminus1=M0+Mz,
                Malpha_D_chi_rate_L2_to_Hminus1=(M0+Mz)*alpha+M0*az,
                Mc_P_xi_rate_Hminus2_to_Hminus1=2*((M0+Mz)*c+M0*cz))
    t,z=sp.symbols('t z',real=True)
    m,f=sp.Function('m')(t),sp.Function('f')(t)
    k=sp.symbols('k',integer=True,nonzero=True)
    coefficient=2+sp.sin(z)/3
    u,vtest=sp.cos(2*z),sp.sin(3*z)
    product=sp.integrate(coefficient*sp.diff(u,z)*vtest+u*sp.diff(coefficient*vtest,z),(z,0,2*sp.pi))
    scale,psi=sp.Function('a')(t),sp.Function('psi')(t)
    exact_measure=sp.exp(-sp.Rational(2,5)*psi)*scale**3
    checks=dict(
        exact_source_weight_product_rate=sp.diff(m*f,t)==sp.diff(m,t)*f+m*sp.diff(f,t),
        exact_periodic_weak_derivative_pairing=sp.simplify(product)==0,
        primitive_multiplier_ratio_exact=sp.simplify((1+k*k)/k**2-(1+1/k**2))==0,
        exact_prepared_measure_logarithmic_rate=sp.simplify(sp.diff(exact_measure,t)-exact_measure*(-sp.Rational(2,5)*sp.diff(psi,t)+3*sp.diff(scale,t)/scale))==0,
        all_weight_bounds_finite_positive=all(lo(x)>0 and mp.isfinite(hi(x)) for x in bounds.values()),
        pinned_sources_preserved=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_SOURCE_WEIGHT_RATES_V1',source_sha256=digest(Path(__file__)),
                source_pins=pins,pinned_sources=len(pins),checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                bounds_binary={k:binary(v) for k,v in bounds.items()},
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                scope='CONDITIONAL_INITIAL_SOURCE_WEIGHT_RATES',moving_free_source='OPEN',
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
        print('Source-weight controls complete')


if __name__=='__main__':main()
