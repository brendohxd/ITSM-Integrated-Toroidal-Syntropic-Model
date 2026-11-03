"""Initial forward current/physical density rows in weak spaces, not energy."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_WEAK_DENSITY_ROW_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
RATE='Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json'
GAUGE='Analysis/MasterTests/outputs/rtau_initial_gauge_composition_v2_20261103/receipt.json'
MAP='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
DIRECT='Analysis/MasterTests/outputs/r4c1_rtau_density_time_transport_v1_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
DT='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
LIE='Analysis/MasterTests/r4c1_gauge_velocity_v1.py'
COEFF='Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def module(name, rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    binary=lambda x:[list(t) for t in x._mpi_]
    zero=lambda:[iv.mpf(0) for _ in range(4)]
    basis=lambda i:[iv.mpf(int(i==k)) for k in range(4)]
    add=lambda *rows:[sum(xs,iv.mpf(0)) for xs in zip(*rows)]
    scale=lambda c,row:[c*x for x in row]
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,RATE,GAUGE,MAP,DIRECT,FACTORY,DT,LIE,COEFF,
                'Theory/Gates/RES-001/RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V2_REPORT_2026-11-03.md'):
        pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snap[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_source_hashes_match',len(original)==219)
    rates=json.loads((ROOT/RATE).read_text());gauge=json.loads((ROOT/GAUGE).read_text())
    direct=json.loads((ROOT/DIRECT).read_text())
    check('inherited_rate_gauge_and_current_controls_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (rates,gauge,direct)))
    vv=[decode(x) for x in rates['coefficients_binary']['field_rate_L2']]
    zz=[decode(x) for x in rates['coefficients_binary']['auxiliary_L2']]
    factory=module('density_row_actual_factory',FACTORY);env=factory.prepare()
    J,D=env['J'],env['D'];grad=env['gradient']
    y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    L=env['evaluate'](y);q=y[:14];v=y[14:28];d=y[28:42];S=y[42:45];Sz=y[45:48]
    density=module('density_row_existing_direct',DT);lie=module('density_row_existing_lie',LIE)
    RG=density.regulator(env,[D.var(x,i) for i,x in enumerate(q)],[D.var(x,28+i) for i,x in enumerate(d)])
    L0=L-RG
    pj=[grad(L,14+i) for i in range(13)]+[J(0)]
    p=[x.c[0] for x in pj]
    rv=[x-t for x,t in zip(v,env['lie'](q,d,S,Sz))]
    N,vol,gam,hinv,curv=env['geometry'](q,d)
    B0=density.improvement(env,q,d,pj)
    beta=iv.mpf(2)/5;b=iv.mpf(5)/11
    I=(L0.c-sum((pj[i]*rv[i] for i in range(13)),J(0))-b*N*vol*q[13]*q[13]/2).c[0]-B0.c[1]
    I0=up(I)
    check('actual_background_current_density_bound_finite',mp.isfinite(hi(I0)),mp.nstr(hi(I0),20))

    r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000
    e2=iv.exp(2*r);kap=e2
    psi0=eps*(iv.mpf(1)/29+iv.mpf(1)/31)
    ps1=eps*(iv.mpf(1)/29+iv.mpf(2)/31)
    ps2=eps*(iv.mpf(1)/29+iv.mpf(4)/31)
    ps3=eps*(iv.mpf(1)/29+iv.mpf(8)/31)
    vel0=iv.mpf(1)/5+eps/47;vel1=3*eps/47
    H=decode(json.loads((ROOT/COEFF).read_text())['H_interval'])
    M=up(H)+eps/31;B=2*eps/31
    s0=up(S[2].c[0]);s1=up(Sz[2].c[0]);svec1=norm([x.c[0] for x in Sz])
    ni=iv.exp(beta*psi0);n0=ni
    Z0=e2*(ps2+r*ps1)
    Z1=e2*(ps3+r*ps1+r*ps2+2*r*r*ps1)
    p0=ni*(vel0+s0*ps1)
    p1=ni*(vel1+s1*ps1+s0*ps2)+beta*ps1*p0
    K0=ni*e2*(iv.sqrt(3)*(M+r*s0)+svec1)
    trace0=ni*(3*(M+r*s0)+s1)
    T0=kap*ni*(M+r*s0+s1)
    A0=b*n0*n0*iv.exp(3*r);alog1=2*beta*ps1+3*r
    E0=iv.sqrt(3)*kap/2
    kdelta=scale(ni/iv.sqrt(2),vv)
    kdelta=add(kdelta,scale(ni/iv.sqrt(2)*(s0+2*svec1)+beta*K0,basis(1)),
               scale(ni*e2*(1+iv.sqrt(3)*r),basis(3)))
    tdelta=add(scale((iv.sqrt(3)+2)*kap*kap,kdelta),
               scale(iv.sqrt(2)*(5*kap**3*K0+trace0*kap*kap),basis(1)))
    pdelta=add(scale(ni,vv),scale(ni*s0+beta*p0,basis(1)),scale(ni*ps1,basis(3)))
    kappa_delta=scale(iv.sqrt(2)*kap*kap,basis(1))
    bracket=Z0*kap*p1+Z0*T0*ps1+p0*kap*Z1
    F0=A0*bracket
    derZ=A0*kap*((1+alog1+2*r)*p0+p1)
    derp=A0*kap*((1+alog1+2*r)*Z0+Z1)
    flux=add(scale(A0*(2*beta+iv.sqrt(2)*E0)*bracket+A0*Z0*T0,basis(1)),
             scale(A0*(kap*p1+T0*ps1)+derZ,zz),
             scale(A0*kap*Z1+derp,pdelta),
             scale(A0*(Z0*p1+p0*Z1),kappa_delta),scale(A0*Z0*ps1,tdelta))

    # Static canonical density: Legendre/shift cancellations are exact before
    # bounding, and the regulator is already on its secondary surface.
    tq=[]
    for k in range(13):
        e=[J(int(i==k)) for i in range(14)]
        tx=lie.lie_fields(e,[J(0)]*14,[J(0)]*3,Sz)
        tq.append(sum((p[i]*tx[i].c[0] for i in range(13)),iv.mpf(0)))
    hatq=norm([grad(L0,i).c[0]+tq[i] for i in range(13)])
    hatd=norm([grad(L0,28+i).c[0]+S[2].c[0]*p[i] for i in range(13)])
    hatp=norm([x.c[0] for x in rv[:13]])
    qD=[D.var(x,i) for i,x in enumerate(q)];dD=[D.var(x,28+i) for i,x in enumerate(d)]
    nD,_,_,_,curvD=env['geometry'](qD,dD)
    curvature=-nD*curvD/2
    curvbound=norm([grad(curvature,i).c[0] for i in range(13)])+norm([grad(curvature,28+i).c[0] for i in range(13)])
    V0=norm([q[i].c[0] for i in (6,7,8)])
    gamma0=iv.sqrt(1+e2*V0*V0)
    dgamma=V0*V0/iv.sqrt(2)+e2*V0
    avec0=n0*gamma0*kap
    davec=n0*(gamma0*kap*beta+kap*dgamma+iv.sqrt(2)*gamma0*kap*kap)
    Bq=norm(p[6:9])*davec+curvbound
    staticI=add(scale(hatp+avec0,basis(0)),
                scale(hatq+hatd+Bq+b*n0*iv.exp(3*r)*Z0*Z0*(beta+iv.sqrt(2)*E0)/2,basis(1)),
                scale(b*n0*iv.exp(3*r)*Z0,zz))
    oldIrate=add(scale(s0+s1,staticI),scale(I0,basis(3)),flux)

    # Physical rho quotient in the original coordinate. Background I_t is
    # controlled in H^-1 via its divergence law, without a third root jet.
    m0=iv.exp(beta*psi0+3*r)
    mlog1=beta*ps1+3*r
    m1=m0*mlog1
    m2=m0*(mlog1*mlog1+beta*ps2+3*r)
    mult1=m0+m1;mult2=m0+iv.sqrt(2)*m1+m2
    rho0=I0*m0
    logcoef=beta+iv.sqrt(2)*E0*(1+2*r)
    alpha0=3*M+beta*vel0;alpha1=3*B+beta*vel1
    deltaalpha=add(scale(beta+iv.sqrt(3/2)*kap,vv),scale(iv.sqrt(6)*M*kap,basis(1)))
    staticrho=add(scale(mult1,staticI),scale(rho0*logcoef,basis(1)))
    Itweak=s0*I0+F0
    algebra=3*iv.sqrt(5)
    oldrhorate=add(scale(mult2,oldIrate),scale(mult1*algebra*logcoef*Itweak,basis(1)),
                   scale(alpha0+alpha1,staticrho),scale(rho0,deltaalpha))
    mb=json.loads((ROOT/MAP).read_text())['bounds']
    j=iv.mpf(lo(decode(mb['J_lower_binary'])));u=iv.mpf(hi(decode(mb['J_upper_binary'])))
    W=iv.mpf(hi(decode(mb['drift_upper_binary'])));P=iv.mpf(hi(decode(mb['drift_derivative_upper_binary'])))
    W2=B+r*W+r*P
    den1=iv.mpf(max(mp.mpf(1),hi(u)))/iv.sqrt(j)
    scalar1=u*(iv.mpf(max(mp.mpf(1),hi(u)))+r)/iv.sqrt(j)
    den2=decode(gauge['pullback_binary']['force_momentum_Hminus2'])
    scalar2=decode(gauge['pullback_binary']['auxiliary_time_Hminus2'])
    outputs=dict(current_density_Hminus1=scale(den1,staticI),
                 current_density_rate_Hminus2=scale(den2,add(oldIrate,scale(W+P,staticI))),
                 physical_density_Hminus1=scale(scalar1,staticrho),
                 physical_density_rate_Hminus2=scale(scalar2,add(oldrhorate,scale(W+2*P+W2,staticrho))),
                 original_current_flux_Hminus1=flux)
    sigma=[decode(x) for x in gauge['canonical_input_constants_binary']['corrective_shift_H1_original']]
    def close(row):return [row[i]+row[3]*sigma[i] if i<3 else row[3]*sigma[3] for i in range(4)]
    closed={key:close(row) for key,row in outputs.items()}
    qlift=decode(gauge['graph_lift_binary']['Q1_per_Dminus']);plift=decode(gauge['graph_lift_binary']['P0_per_Dminus'])
    lifted={key:[row[0]*plift+row[1]*qlift,row[1],row[0],row[2],row[3]] for key,row in closed.items()}
    check('all_static_flux_and_time_constants_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in lifted.values() for x in row))

    # Independent rational full-six-entry variation of the actual flux.
    z,e=s.symbols('z e',real=True);bb=s.Rational(5,11);be=s.Rational(2,5)
    h=s.Matrix([[2,s.Rational(1,7),s.Rational(1,11)],[s.Rational(1,7),3,s.Rational(1,13)],[s.Rational(1,11),s.Rational(1,13),4]])
    hz=s.Matrix([[1,2,3],[2,4,5],[3,5,6]])/37
    vv0=s.Matrix([[3,-2,1],[-2,5,2],[1,2,4]])/17
    kk=s.Matrix([[1,2,3],[2,-1,4],[3,4,2]])/19
    kz=s.Matrix([[2,-1,3],[-1,4,2],[3,2,-2]])/23
    ll=s.Matrix([[4,2,-1],[2,3,1],[-1,1,5]])/29
    shift=s.Matrix([1,-2,3])/31;shiftz=s.Matrix([2,1,-1])/41
    ds=s.Matrix([-1,3,2])/43;dsz=s.Matrix([3,-2,1])/47
    nn=s.Rational(7,9);chi=s.Rational(2,13);cz=s.Rational(3,17);czz=s.Rational(4,19)
    ps=s.Rational(1,11);pss=s.Rational(2,23);vel=s.Rational(1,5);velz=s.Rational(3,29)
    eta=s.Rational(2,31);etaz=s.Rational(1,37);Z=s.Rational(-2,41);Zz=s.Rational(1,43)
    dzeta=s.Rational(3,47);dzeta_z=s.Rational(-2,53)
    ez=s.Matrix([0,0,1])
    def lieh(a,az,S,Sz):return S[2]*az+(a*Sz)*ez.T+ez*(a*Sz).T
    def fl(a,az,V,S,Sz,N,ps,pss,vel,velz,Z,Zz):
        H=a.inv();kap=H[2,2];K=(V-lieh(a,az,S,Sz))/(2*N)
        pn=(vel-S[2]*ps)/N
        pnz=(velz-Sz[2]*ps-S[2]*pss)/N+be*ps*pn
        T=s.trace(H*K)*kap-2*(H*K*H)[2,2]
        return bb*N*N*s.sqrt(a.det())*(Z*kap*pnz+Z*T*ps-pn*kap*Zz)
    raw=fl(h+e*kk,hz+e*kz,vv0+e*ll,shift+e*ds,shiftz+e*dsz,nn*s.exp(-be*e*chi),
           ps+e*cz,pss+e*czz,vel+e*eta,velz+e*etaz,Z+e*dzeta,Zz+e*dzeta_z)
    Hh=h.inv();kap0=Hh[2,2];dH=-Hh*kk*Hh
    K=(vv0-lieh(h,hz,shift,shiftz))/(2*nn)
    dK=(ll-lieh(kk,kz,shift,shiftz)-lieh(h,hz,ds,dsz))/(2*nn)+be*chi*K
    T=s.trace(Hh*K)*kap0-2*(Hh*K*Hh)[2,2]
    dT=(s.trace(dH*K+Hh*dK)*kap0+s.trace(Hh*K)*dH[2,2]
        -2*(dH*K*Hh+Hh*dK*Hh+Hh*K*dH)[2,2])
    pn=(vel-shift[2]*ps)/nn
    pnz=(velz-shiftz[2]*ps-shift[2]*pss)/nn+be*ps*pn
    dpn=(eta-ds[2]*ps-shift[2]*cz)/nn+be*pn*chi
    dpnz=(etaz-dsz[2]*ps-ds[2]*pss-shiftz[2]*cz-shift[2]*czz)/nn
    dpnz+=be*chi*(velz-shiftz[2]*ps-shift[2]*pss)/nn+be*cz*pn+be*ps*dpn
    pref=bb*nn*nn*s.sqrt(h.det());dlog=-2*be*chi+s.trace(Hh*kk)/2
    expanded=pref*(dlog*(Z*kap0*pnz+Z*T*ps-pn*kap0*Zz)
        +(dzeta*kap0+Z*dH[2,2])*pnz+Z*kap0*dpnz
        +dzeta*T*ps+Z*dT*ps+Z*T*cz
        -dpn*kap0*Zz-pn*dH[2,2]*Zz-pn*kap0*dzeta_z)
    check('independent_full_six_metric_current_variation',s.simplify(s.diff(raw,e).subs(e,0)-expanded)==0)
    check('omitted_auxiliary_gradient_flux_rejected',s.simplify(pref*pn*kap0*dzeta_z)!=0)
    gg,ff=s.Function('g')(z),s.Function('f')(z)
    check('weak_derivative_product_identity',s.expand(gg*s.diff(ff,z)-s.diff(gg*ff,z)+s.diff(gg,z)*ff)==0)
    tt=s.symbols('t');II,MM=s.Function('I')(tt),s.Function('M')(tt)
    dI,dM=s.Function('dI')(tt),s.Function('dM')(tt)
    rho=II/MM;drho=dI/MM-rho*dM/MM
    al=s.diff(MM,tt)/MM;dal=s.diff(dM,tt)/MM-al*dM/MM
    formula=s.diff(dI,tt)/MM-s.diff(II,tt)*dM/MM**2-al*drho-rho*dal
    check('physical_density_time_quotient_identity',s.simplify(s.diff(drho,tt)-formula)==0)
    check('omitted_measure_variation_rejected',s.diff(rho,MM)!=0)
    n=s.symbols('n',integer=True,positive=True)
    check('periodic_H1_embedding_tail_bound',s.simplify(1/(n*(n+1))-1/(n+1)**2)==1/(n*(n+1)**2))
    wa=s.Function('w')(z);la=s.Function('lam')(z);LL=s.Function('L')(z);mean=s.symbols('mean')
    derivative=s.diff(LL-mean-s.diff(la,z)*wa,z)
    check('background_drift_second_derivative_identity',s.expand(derivative-(s.diff(LL,z)-s.diff(la,z,2)*wa-s.diff(la,z)*s.diff(wa,z)))==0)
    check('current_and_physical_density_not_identified',lo(m0)>0 and logcoef!=0)
    check('all_original_inputs_and_sidecars_preserved',all(sha(path)==h and path.stat().st_mtime_ns==stamp for path,(h,stamp) in snap.items()))
    return dict(kind='RTAU_INITIAL_WEAK_DENSITY_ROW_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,
                input_order=['Dminus','Qfree_H1_original','Pfree_L2_original','force_configuration_H2_original','harmonic_coordinate_velocity_adapted'],
                constants_binary={key:[binary(x) for x in row] for key,row in lifted.items()},
                upper_display={key:[mp.nstr(hi(x),18) for x in row] for key,row in lifted.items()},
                canonical_input_constants_binary={key:[binary(x) for x in row] for key,row in closed.items()},
                background_binary={key:binary(val) for key,val in dict(current_density=I,current_density_abs=I0,current_flux_abs=F0,
                    current_time_Hminus1=Itweak,physical_density_abs=rho0,coordinate_drift_second_abs=W2,H1_algebra_constant=algebra).items()},
                background_upper_display={key:mp.nstr(hi(val),18) for key,val in dict(current_density_abs=I0,current_flux_abs=F0,current_time_Hminus1=Itweak,
                    physical_density_abs=rho0,coordinate_drift_second_abs=W2).items()},
                source_sha256=pins,inherited_source_count=len(original),
                Ward_defect='D_z(N^2*h^iz*delta C_i+delta(N^2*h^iz)*C_i); retained, zero only on exact constrained background/tangent',
                scope='INITIAL_FORWARD_DENSITY_GAUGE_WEAK_ROW_ON_EXACT_COMPATIBLE_GRAPH',
                evolving_Green_inverse='NOT_DERIVED',physical_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    try:receipt=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            with (args.output.parent/'failure.json').open('x') as handle:json.dump(dict(status='FAILED_ATTEMPT',error=repr(error),source_sha256=sha(Path(__file__)),physics_pass=False),handle,indent=2)
        raise
    raw=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as handle:handle.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as handle:handle.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps(dict(passed=receipt['passed'],total=receipt['total'],failed=[x for x in receipt['checks'] if not x['passed']],
                         bounds=receipt['upper_display'],background=receipt['background_upper_display']),indent=2))
    return 0 if receipt['passed']==receipt['total'] else 1


if __name__=='__main__':raise SystemExit(main())
