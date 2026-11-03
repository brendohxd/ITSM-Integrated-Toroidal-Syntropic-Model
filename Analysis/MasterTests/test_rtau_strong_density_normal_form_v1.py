"""Strong-density normal-form identity and initial coefficients; energy open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_CONTRACT_2026-11-03.md'
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_EXECUTION_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
DENSITY='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
HIGHER='Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json'
HIGHER_REPORT='Theory/Gates/RES-001/RES001_R4C1_RTAU_CLOCK_DENSITY_V3_REPORT_2026-11-01.md'
INITIAL='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
IDENTITY='Analysis/MasterTests/outputs/rtau_compensated_density_v1_20261103/receipt.json'
SCREEN='Analysis/MasterTests/outputs/rtau_weak_density_energy_screen_v1_20261103/receipt.json'
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),CONTRACT,SPEC,MANIFEST,FACTORY,DENSITY,HIGHER,HIGHER_REPORT,INITIAL,IDENTITY,SCREEN):pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snap[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_source_hashes_match',len(original)==219)
    higher,initial,identity,screen=[json.loads((ROOT/rel).read_text()) for rel in (HIGHER,INITIAL,IDENTITY,SCREEN)]
    check('all_immediate_owners_pass_in_their_scopes',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (higher,initial,identity,screen)))
    check('higher_root_bound_is_ODE_derived_not_Fourier_tail',higher['root_third_jet']=='derived from differentiated momentum ODE; not Fourier truncation')

    # Generic complete primitive transformation, retaining independent means.
    S,C,c,ct,cz,P,pi,mpi,mspi,d,zz,mdzz,J,mJ,r,Z,mrZ,PrzZ,PR,F0,U,Uz=sp.symbols('S C c ct cz P pi mpi mspi d zz mdzz J mJ r Z mrZ PrzZ PR F0 U Uz')
    sigma=U+c*P;sigmaz=Uz+cz*P+c*(pi-mpi)
    sigmat=S*sigmaz+C*sigma+c*d*zz+F0
    Pt=S*pi-mspi+d*zz-mdzz+J-mJ+r*Z-mrZ-PrzZ+PR
    direct=sp.expand(sigmat-ct*P-c*Pt)
    transformed=S*Uz+C*U+(C*c-ct+S*cz)*P+F0+c*(mspi-S*mpi)+c*mdzz-c*(J-mJ)-c*(r*Z-mrZ)+c*PrzZ-c*PR
    check('complete_normal_form_algebra_and_fast_cancellation',sp.expand(direct-transformed)==0 and sp.diff(sp.expand(direct),zz)==0)
    check('dropping_coefficient_time_drift_rejected',sp.diff(sp.expand(direct),ct)==-P)
    check('weighted_fast_mean_not_deleted',sp.diff(sp.expand(direct),mdzz)==c)
    aa,dd=sp.symbols('a d',nonzero=True)
    check('current_derived_ratio_cancels_only_with_correct_coefficient',sp.simplify(aa-(aa/dd)*dd)==0)

    x=sp.symbols('x');bb,bet=sp.symbols('b beta')
    mf,kf,zf,sf,sh,pf,fsf,loq,lod,ef=[sp.Function(n)(x) for n in ('M','kap','Z','s','S','pi','fs','Loq','Lod','e')]
    df=bb*mf*kf
    lr=bb*mf*zf*zf/2-df*sf*sp.diff(zf,x)+bet*df*zf*sf*sf
    er=-bet*lr-sp.diff(df*(-sp.diff(zf,x)+2*bet*zf*sf),x)
    original_current=sp.diff(sh*pf,x)-sp.diff(mf*fsf,x)+bet*mf*ef+loq-sp.diff(lod,x)+er
    full_flux=sh*pf-mf*fsf-lod+df*sp.diff(zf,x)-2*bet*df*zf*sf
    local_source=loq+bet*mf*ef-bet*lr
    check('complete_scalar_current_flux_and_local_split',sp.expand(original_current-sp.diff(full_flux,x)-local_source)==0)
    jet=sp.Symbol('Zzjet')
    check('local_regulator_fast_derivative_coefficient',sp.diff(local_source.xreplace({sp.diff(zf,x):jet}),jet)==bet*df*sf)

    # Independent exact periodic profiles. Nonzero scalar-momentum mean is
    # deliberate and is not identified with the fixed total clock charge.
    z=sp.symbols('z',real=True)
    simplify=lambda x:sp.trigsimp(sp.expand_trig(sp.expand(x)))
    mean=lambda f:sp.simplify(sp.integrate(sp.expand_trig(f),(z,0,2*sp.pi))/(2*sp.pi))
    def primitive(f):
        raw=sp.integrate(sp.expand_trig(f-mean(f)),z)
        return simplify(raw-mean(raw))
    st=sp.sin(z)/13;cot=2+sp.cos(z)/5;dt=3+sp.sin(z)/7;rt=1+sp.cos(z)/11
    pit=1+sp.cos(z)/17;zt=sp.cos(z)/19;sg=sp.sin(z)/23
    jt=sp.cos(2*z)/29;r0=1+sp.sin(2*z)/31;react=2+sp.cos(z)/37
    f0=sp.cos(2*z)/41;ctt=1+sp.sin(z)/43
    prim=primitive(pit);ut=sg-cot*prim
    sigma_time=st*sp.diff(sg,z)+react*sg+cot*dt*sp.diff(zt,z)+f0
    pi_time=sp.diff(st*pit+dt*sp.diff(zt,z)+jt,z)+rt*sp.diff(zt,z)+r0
    sharp_time=sigma_time-ctt*prim-cot*primitive(pi_time)
    rhs=st*sp.diff(ut,z)+react*ut+(react*cot-ctt+st*sp.diff(cot,z))*prim+f0
    rhs+=cot*(mean(st*pit)-st*mean(pit))-cot*mean(sp.diff(dt,z)*zt)
    rhs-=cot*(jt-mean(jt))+cot*(rt*zt-mean(rt*zt))
    rhs+=cot*primitive(sp.diff(rt,z)*zt)-cot*primitive(r0)
    check('independent_periodic_complete_normal_form_identity',simplify(sharp_time-rhs)==0)
    check('nonzero_momentum_mean_is_retained',mean(pit)==1)
    check('weighted_fast_mean_is_nonzero_control',mean(dt*sp.diff(zt,z))==-sp.Rational(1,266))
    check('weighted_mean_integration_by_parts',sp.simplify(mean(dt*sp.diff(zt,z))+mean(sp.diff(dt,z)*zt))==0)
    w=sp.cos(z)/47
    comm=primitive(sp.diff(w*pit,z))-w*sp.diff(primitive(pit),z)
    check('density_primitive_coordinate_commutator',simplify(comm-w*mean(pit)+mean(w*pit))==0)
    check('primitive_coordinate_commutator_nonzero',simplify(comm)!=0)
    check('triangular_transformation_exact_inverse',simplify(ut+cot*prim-sg)==0)

    fac=load('strong_density_normal_form_factory',FACTORY);env=fac.prepare()
    transport=load('strong_density_normal_form_improvement',DENSITY)
    pars=env['env']['env']['exact'];b,beta,KQ,A=[rational(pars[k]) for k in ('b','beta','K_Q','A')]
    third=decode(higher['whole_circle_third_shift_bound']);thirdbox=iv.mpf([-hi(third),hi(third)])
    J2=env['J'];y,_=env['state'](J2.variable(iv.mpf([0,hi(2*iv.pi)])),True,[thirdbox]*3)
    L=env['evaluate'](y)
    check('certified_third_root_jet_inserted_with_factorial',all(lo(2*y[45+i].c[2])<=-hi(third) and hi(2*y[45+i].c[2])>=hi(third) for i in range(3)))

    def coefficient(ctx,yy):
        J,D=ctx['J'],ctx['D'];q,v,d,S,Sz=yy[:14],yy[14:28],yy[28:42],yy[42:45],yy[45:48]
        Q=[D.var(x,i) for i,x in enumerate(q)];V=[D.var(x,14+i) for i,x in enumerate(v)]
        DX=[D.var(x,28+i) for i,x in enumerate(d)];SS=[D.var(x,42+i) for i,x in enumerate(S)];SZ=[D.var(x,45+i) for i,x in enumerate(Sz)]
        N,mu,_,H,_=ctx['geometry'](Q,DX);rv=[a-c for a,c in zip(V,ctx['lie'](Q,DX,SS,SZ))]
        kv=[rv[i]/(2*N) for i in range(6)]
        K=[[kv[0],kv[1],kv[2]],[kv[1],kv[3],kv[4]],[kv[2],kv[4],kv[5]]]
        trace=sum((H[i][k]*K[k][i] for i in range(3) for k in range(3)),D(0))
        kup=sum((H[2][i]*K[i][k]*H[k][2] for i in range(3) for k in range(3)),D(0))
        T=H[2][2]*trace-2*kup
        a=T*DX[12]*N*b;dcoef=N*mu*H[2][2]*b
        ccoef=T*DX[12]/(mu*H[2][2])
        return dict(c=ccoef,a=a,d=dcoef,N=N,mu=mu,Q=Q,V=V,DX=DX,S=SS,Sz=SZ,H=H)

    co=coefficient(env,y);cc=co['c'];grad=env['gradient'];hj=env['hj'];D=env['D'];JJ=env['J']
    check('fast_current_coefficient_strictly_positive',lo(co['d'].c.c[0])>0)
    defect=co['a'].c.c[0]-cc.c.c[0]*co['d'].c.c[0]
    check('actual_fast_ratio_enclosures_consistent',lo(defect)<=0<=hi(defect))
    check('coefficient_has_no_auxiliary_or_clock_velocity_dependency',all(i not in cc.g for i in (13,26,27,41)))
    velocity=[v.c[0] for v in y[14:27]];velocityz=[v.c[1] for v in y[14:27]]
    pt=[grad(L,i).c[0]-grad(L,28+i).c[1] for i in range(13)]
    rhsacc=[pt[i]-sum((hj(L,14+i,k).c[0]*velocity[k]+hj(L,14+i,28+k).c[0]*velocityz[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
    Minv=decode(initial['bounds']['original_temporal_inverse'])
    cq=[cc.g.get(i,JJ(0)).c[0] for i in range(13)]
    cd=[cc.g.get(28+i,JJ(0)).c[0] for i in range(13)]
    cv=[cc.g.get(14+i,JJ(0)).c[0] for i in range(13)]
    ct_bound=norm(cq)*norm(velocity)+norm(cd)*norm(velocityz)+norm(cv)*Minv*norm(rhsacc)
    cabs,czabs=up(cc.c.c[0]),up(cc.c.c[1]);transform_bound=1+cabs
    check('coefficient_and_initial_canonical_time_bound_finite',all(mp.isfinite(hi(x)) and lo(x)>=0 for x in (cabs,czabs,ct_bound,transform_bound)))

    # Complete background Sigma and its derivative, now with certified C3 S.
    N,mu,gamma,H=co['N'],co['mu'],None,co['H'];Q,V,DX=co['Q'],co['V'],co['DX']
    _,_,gamma,_,_=env['geometry'](Q,DX)
    normalp=(V[12]-co['S'][2]*DX[12])/N
    h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
    rest=[H[i][2]*DX[12]+Q[6+i]*(normalp+Q[8]*DX[12]/(gamma+1)) for i in range(3)]
    Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
    Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
    check('positive_force_branch_retained',lo(Y.c.c[0])>0)
    force=(gamma*normalp+Q[8]*DX[12])**2*KQ/2-Y**mp.mpf('1.5')*A
    M=N*mu;other=L-M*force-transport.regulator(env,Q,DX)
    mom=[grad(L,14+i) for i in range(13)]+[JJ(0)]
    rv=[a-c for a,c in zip(y[14:28],env['lie'](y[:14],y[28:42],y[42:45],y[45:48]))]
    hat=other.c-sum((mom[i]*rv[i] for i in range(12)),JJ(0))
    B0=transport.improvement(env,y[:14],y[28:42],mom)
    sig=(hat.c[0]-B0.c[1])/M.c.c[0]
    sigz=(hat.c[1]-2*B0.c[2]-sig*M.c.c[1])/M.c.c[0]
    sigabs,sigzabs=up(sig),up(sigz)
    check('strong_background_density_gradient_bound_finite',mp.isfinite(hi(sigzabs)))

    # Structural shift covariance: L depends on v,S,S_z through RV;
    # c is linear in the metric components of RV. The canonical derivative
    # therefore cancels all S_t and S_tz coefficients, without setting them.
    ell,mm,qz,Bgen,Tg,Tzg=sp.symbols('ell M qz B T Tz')
    lvS=-mm*qz;lvSz=-mm*Bgen;cvS=-ell*qz;cvSz=-ell*Bgen
    check('structural_canonical_shift_time_cancellation',sp.expand(cvS*Tg+cvSz*Tzg+ell*(-lvS*Tg-lvSz*Tzg)/mm)==0)
    point_controls=[]
    for loc in ('0.3','1.1','2.4'):
        ctx=fac.point(loc);yy,LL=ctx['y'],ctx['L'];pc=coefficient(ctx,yy)['c'];Jp=ctx['J']
        hp=ctx['hj'];gp=ctx['gradient'];q=yy[:13];qzv=yy[28:41]
        hh=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
        BM=[[Jp(0) for _ in range(3)] for _ in range(13)]
        for i,(a0,b0) in enumerate(HM):
            for j0 in range(3):BM[i][j0]=(hh[a0][j0] if b0==2 else Jp(0))+(hh[b0][j0] if a0==2 else Jp(0))
        for j0 in range(3):BM[6+j0][j0]=-q[8]
        errors=[];coef_errors=[]
        for k in range(3):
            gs=[qzv[i] if k==2 else Jp(0) for i in range(13)]
            gz=[BM[i][k] for i in range(13)]
            for gen,slot in ((gs,42+k),(gz,45+k)):
                for i in range(13):
                    e=hp(LL,14+i,slot)+sum((hp(LL,14+i,14+j)*gen[j] for j in range(13)),Jp(0));errors.append(up(e.c[0]))
                e=pc.g.get(slot,Jp(0))+sum((pc.g.get(14+j,Jp(0))*gen[j] for j in range(13)),Jp(0));coef_errors.append(up(e.c[0]))
        check('actual_Legendre_shift_covariance_'+loc,hi(max(errors,key=hi))<mp.mpf('1e-28'))
        check('actual_coefficient_shift_covariance_'+loc,hi(max(coef_errors,key=hi))<mp.mpf('1e-28'))
        v0=[x.c[0] for x in yy[14:27]];v1=[x.c[1] for x in yy[14:27]]
        pp=[gp(LL,i).c[0]-gp(LL,28+i).c[1] for i in range(13)]
        ra=[pp[i]-sum((hp(LL,14+i,k).c[0]*v0[k]+hp(LL,14+i,28+k).c[0]*v1[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
        acc,err=ctx['solve'](ra)
        ctd=sum((pc.g.get(i,Jp(0)).c[0]*v0[i]+pc.g.get(28+i,Jp(0)).c[0]*v1[i]+pc.g.get(14+i,Jp(0)).c[0]*acc[i] for i in range(13)),iv.mpf(0))
        check('actual_point_time_coefficient_enclosed_'+loc,hi(up(ctd))<=hi(ct_bound) and hi(err)<mp.mpf('1e-30'))
        point_controls.append(dict(location=loc,coefficient_time=binary(ctd),inverse_error=binary(err)))
    check('all_source_and_sidecar_bytes_timestamps_preserved',all(sha(path)==h and path.stat().st_mtime_ns==t for path,(h,t) in snap.items()))
    values=dict(coefficient=cabs,coefficient_z=czabs,coefficient_time=ct_bound,triangular_map=transform_bound,
                background_Sigma=sigabs,background_Sigma_z=sigzabs,fast_current_lower=iv.mpf(lo(co['d'].c.c[0])),reused_shift_third=third)
    return dict(kind='RTAU_STRONG_DENSITY_NORMAL_FORM_IDENTITY_AND_INITIAL_COEFFICIENTS_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),bounds_binary={k:binary(x) for k,x in values.items()},upper_display={k:mp.nstr(hi(x),24) for k,x in values.items()},
                point_controls=point_controls,transformed_operator='u_t-S*u_z=C*u+(C*c-c_t+S*c_z)*P(pi)+F0+c*(mean(S*pi)-S*mean(pi))-c*mean(d_z*Z)-c*P0(J0)-c*P0(r*Z)+c*P(r_z*Z)-c*P(R0)',
                source_definitions='P=Dinv P0; r=beta*d*psi_z; J0=delta J-S*delta pi-d*delta Z_z; R0=delta R-r*delta Z_z; F0 retains complete original density linearization except S*deltaSigma_z,C*deltaSigma,a*delta Z_z',
                exact_force_Zz_cancellation=True,density_strength='L2 retained by bounded triangular map with scalar momentum L2',
                coefficient_time_shift_assumption='No physical S_t=0; canonical shift-time coefficients cancel structurally and are controlled at actual points',
                root_C3='Reused immutable momentum-ODE certificate; no differentiated C2 error radius',
                remaining_ordinary_derivatives='Retained in F0 for full coupled principal energy; not assumed L2 forcing',
                full_coupled_energy='NOT_DERIVED',normal_form_contract='INCOMPLETE',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps({'status':'FAILED_ATTEMPT','error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n')
        raise
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],
                      'bounds':data['upper_display'],'full_coupled_energy':data['full_coupled_energy']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
