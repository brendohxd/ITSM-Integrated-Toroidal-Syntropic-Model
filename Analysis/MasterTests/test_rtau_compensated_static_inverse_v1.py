"""Initial compensated scalar chart on its compatible range; no evolution claim."""
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_STATIC_INVERSE_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
PARENT_SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_coupled_periodic_inverse_v1.py'
PARENT_RECEIPT='Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
DENSITY='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
RATE='Analysis/MasterTests/outputs/rtau_compensated_rate_v1_20261103/receipt.json'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,FACTORY,
                PARENT_SOURCE,PARENT_RECEIPT,DENSITY,RATE):pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for p in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if p.exists():snap[p]=(sha(p),p.stat().st_mtime_ns)
    check('all_219_original_hashes_match',len(original)==219)
    parent=json.loads((ROOT/PARENT_RECEIPT).read_text());rate=json.loads((ROOT/RATE).read_text())
    check('owning_inverse_and_full_rate_controls_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (parent,rate)))
    fac=load('compensated_static_factory',FACTORY);env=fac.prepare()
    density=load('compensated_static_density',DENSITY)
    # Extract only the immutable same-action coefficient construction, not its
    # old experiment or a specialized homogeneous matrix.
    tree=ast.parse((ROOT/PARENT_SOURCE).read_text())
    outer=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    fn=copy.deepcopy(next(n for n in outer.body if isinstance(n,ast.FunctionDef) and n.name=='coefficients'))
    namespace={'mp':mp,'iv':iv}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<preserved-same-action-trace-coefficients>','exec'),namespace)
    old_coefficients=namespace['coefficients']
    params=env['env']['env']['exact'];KQ,A,b=[rational(params[k]) for k in ('K_Q','A','b')]

    # Exact canonical force-energy differential. The normal scalar velocity
    # changes when the metric/volume changes at fixed canonical momentum.
    p,s,q,a,mu,dmu,dq,ds,dpi=sp.symbols('p s q a mu dmu dq ds dpi',nonzero=True)
    force=(1+q)*p**2/2-a*((1+q*q)*p*p+2*q*p*s+(1+q)*s*s)**sp.Rational(3,2)
    fp=sp.diff(force,p);energy=p*fp-force
    dp=(dpi-fp*dmu-mu*sp.diff(fp,q)*dq-mu*sp.diff(fp,s)*ds)/(mu*sp.diff(fp,p))
    actual=sp.diff(energy,p)*dp+sp.diff(energy,q)*dq+sp.diff(energy,s)*ds
    expected=p*dpi/mu-p*fp*dmu/mu-sp.diff(force,q)*dq-sp.diff(force,s)*ds
    check('nonquadratic_frame_dependent_canonical_energy_differential',sp.simplify(actual-expected)==0)
    z=sp.symbols('z');ff,cc,ss,mm=[sp.Function(n)(z) for n in ('f','c','s','mu')]
    Z=-sp.diff(cc*ss,z)/mm
    deltaZ=-ff*Z-sp.diff(cc*ss*ff,z)/mm
    check('secondary_trace_variation_keeps_gradient_term',sp.expand(deltaZ+cc*ss*sp.diff(ff,z)/mm)==0)

    H2=sp.Rational(3469,4620);H=sp.sqrt(H2);pi=-sp.Rational(11,10)*H
    fvar=sp.symbols('fvar');vol=1+fvar
    ts=(1+sp.Rational(1,16)+params['K_Q']/25)/2
    force_ts=params['K_Q']/50
    pot=params['m2']/2+params['lambda4']/8+params['lambda6']/(24*params['Lambda']**2)+params['mr2']/2+params['lambda_r']/4+params['g_r']/4+params['rho_Lambda']
    def ham(pzz):
        ps=[pi*(1+fvar),pi*(1+fvar),pzz]
        kinetic=2*(sum(x*x for x in ps)-sp.Rational(16,33)*sum(ps)**2)/vol
        return -kinetic-ts/vol-vol*pot
    sigref=sp.simplify((ham(pi)+force_ts/vol).subs(fvar,0))
    cn=sp.simplify(sp.diff((ham(pi*(1+fvar))+force_ts/vol)/vol,fvar).subs(fvar,0))
    cm=sp.simplify(sp.diff((ham(pi)+force_ts/vol)/vol,fvar).subs(fvar,0))
    check('same_action_reference_physical_compensator',sigref==sp.Rational(13,50),str(sigref))
    check('reference_nonzero_mass_from_action',cn==sp.Rational(17,16),str(cn))
    check('reference_negative_mean_retained',cm==-sp.Rational(4951,8400),str(cm))
    check('longitudinal_nonlocal_reference_retained',sp.simplify(cn-cm+2*H*pi)==0)
    densitized_cn=sp.simplify(sp.diff(ham(pi*(1+fvar))+force_ts/vol,fvar).subs(fvar,0))
    check('omitting_physical_volume_changes_operator',sp.simplify(densitized_cn-cn)==sigref and sigref!=0)
    n=sp.symbols('n',integer=True,positive=True)
    check('reference_inverse_all_nonzero_fourier_modes',cn>1 and sp.simplify((n*n+cn)-(1+n*n))==cn-1)

    def coefficients(ctx,y,L):
        J,D,grad=ctx['J'],ctx['D'],ctx['gradient']
        co=old_coefficients(ctx,y,L)
        qq,v,dd,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
        N,mu0,_,hinv,_=ctx['geometry'](qq,dd);M=N*mu0
        normalp=(v[12]-S[2]*dd[12])/N
        qn=[D.var(x,i) for i,x in enumerate(qq)]
        _,_,gamma,Hinv,_=ctx['geometry'](qn,[J(0)]*14)
        pp=D.var(normalp,100);sc=D.var(dd[12],101)
        h=[[qn[0],qn[1],qn[2]],[qn[1],qn[3],qn[4]],[qn[2],qn[4],qn[5]]]
        rest=[Hinv[i][2]*sc+qn[6+i]*(pp+qn[8]*sc/(gamma+1)) for i in range(3)]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0
        F=(gamma*pp+qn[8]*sc)**2*KQ/2-Y**mp.mpf('1.5')*A
        # Compute background Sigma directly by its other-action definition.
        RG=density.regulator(ctx,qn,[D.var(x,28+i) for i,x in enumerate(dd)])
        other=L-D(N*mu0)*F-RG
        pj=[grad(L,14+i) for i in range(13)]+[J(0)]
        rv=[a-c for a,c in zip(v,ctx['lie'](qq,dd,S,Sz))]
        B0=density.improvement(ctx,qq,dd,pj)
        sig=((other.c-sum((pj[i]*rv[i] for i in range(12)),J(0))).c[0]-B0.c[1])/M.c[0]
        trace_force=qq[0]*(F.g.get(0,J(0))+F.g.get(3,J(0)))
        zeroth=co['A0']/M.c[0]-F.c.c[0]-trace_force.c[0]+b*qq[13].c[0]**2/2-sig
        first=co['A1']/M.c[0]-b*qq[13].c[0]*hinv[2][2].c[0]*dd[12].c[0]
        second=co['A2']/M.c[0]
        return dict(A0=zeroth,A1=first,A2=second,rv=[x.c[0]/M.c[0] for x in rv],
                    sigma=sig,old=co,F=F,normalp=normalp,M=M,Y=Y)

    J=env['J'];y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    L=env['evaluate'](y);co=coefficients(env,y,L)
    r=iv.mpf(1)/13000;p0=-iv.mpf(11)/10*iv.sqrt(iv.mpf(3469)/4620)
    rref=2*iv.sqrt(iv.mpf(3469)/4620)
    tx,ty,Terr=[decode(parent['bounds'][k]) for k in ('transverse_x','transverse_y','longitudinal_difference')]
    d2=up(co['A2']+1);d1=up(co['A1']);d0=up(co['A0']-rational(cm))
    rv=co['rv'];nonlocal_error=up(rv[2])*tx+up(rv[4])*ty+up(rv[5])*Terr+up(rv[5]-rref)*up(p0)
    strong_error=d2+d1/2+d0+nonlocal_error
    # A2=-a^-2 exactly. Weak integration by parts keeps its derivative.
    leading_drift=2*r*iv.exp(2*r)
    weak_error=d2+d1+d0+nonlocal_error+leading_drift
    R0=rational(1/abs(cm));ks=R0*strong_error;kw=R0*weak_error
    strong=R0/(1-ks) if hi(ks)<1 else None
    weak=R0/(1-kw) if hi(kw)<1 else None
    check('whole_root_principal_scalar_enclosure_consistency',lo(co['A2']+1/y[0].c[0])<=0<=hi(co['A2']+1/y[0].c[0]))
    check('strong_projected_inverse_contraction',hi(ks)<1,mp.nstr(hi(ks),24))
    check('weak_projected_inverse_contraction_with_leading_drift',hi(kw)<1,mp.nstr(hi(kw),24))
    controls=[]
    for location in ('0.3','1.1','2.4'):
        ctx=fac.point(location);yy,LL=ctx['y'],ctx['L'];cc0=coefficients(ctx,yy,LL)
        JJ,DD=ctx['J'],ctx['D'];grad=ctx['gradient'];pc=[iv.mpf(1)/37,-iv.mpf(1)/41,iv.mpf(1)/43]
        for basis in range(3):
            fj=[iv.mpf(int(i==basis)) for i in range(3)]
            fjet=JJ(coefficients=[fj[0],fj[1],fj[2]/2]);qvar=yy[0]*fjet
            dq0=[JJ(0) for _ in range(14)];dd0=[JJ(0) for _ in range(14)]
            for slot in (0,3):dq0[slot]=qvar;dd0[slot]=JJ(coefficients=[qvar.c[1],2*qvar.c[2],iv.mpf(0)])
            pt=cc0['old']['PT'];lz=yy[0].c[1]/(2*yy[0].c[0])
            px,py=cc0['old']['p'][2],cc0['old']['p'][4]
            slopes=[-2*lz*pc[0]-px.c[1]*fj[0]-px.c[0]*fj[1]-2*lz*px.c[0]*fj[0],
                    -2*lz*pc[1]-py.c[1]*fj[0]-py.c[0]*fj[1]-2*lz*py.c[0]*fj[0],
                    -lz*pc[2]+pt.c[0]*fj[1]/2+lz*pt.c[0]*fj[0]]
            dp0=[JJ(0) for _ in range(14)]
            for slot,value,slope in zip((2,4,5),pc,slopes):dp0[slot]=JJ(coefficients=[value,slope,iv.mpf(0)])
            result=ctx['run_probe']('compensated_trace_'+str(basis),dq0,dd0,dp0,[JJ(0)]*3,[JJ(0)]*3)
            # Independent direct other-action variation: solve the full
            # temporal matrix, then differentiate its defining density.
            rhs=[dp0[i].c[0]-sum((ctx['hj'](LL,14+i,k)*dq0[k]+ctx['hj'](LL,14+i,28+k)*dd0[k] for k in range(14)),JJ(0)).c[0] for i in range(13)]
            dv0,err=ctx['solve'](rhs);dv=[JJ(t) for t in dv0]+[JJ(0)]
            dy=dq0+dv+dd0+[JJ(0)]*6
            qv,vv,ddv=yy[:14],yy[14:28],yy[28:42]
            sv,szv=yy[42:45],yy[45:48]
            n0,mu0,_,_,_=ctx['geometry'](qv,ddv)
            pn=cc0['normalp'];ppdelta=(dv[12]-sv[2]*dd0[12])/n0
            # These trace probes have delta psi=delta psi_z=0.
            dforce=sum((cc0['F'].g.get(i,JJ(0))*dq0[i] for i in range(9)),JJ(0))+cc0['F'].g.get(100,JJ(0))*ppdelta
            M=cc0['M'];dM=M*fjet
            dlother=sum((grad(LL,k)*dy[k] for k in range(48)),JJ(0))-dM*cc0['F'].c-M*dforce
            # Regulator variation is evaluated independently in raw q/d variables.
            Q=[DD(t,{0:e}) for t,e in zip(qv,dq0)];DX=[DD(t,{0:e}) for t,e in zip(ddv,dd0)]
            dlother-=density.regulator(ctx,Q,DX).g.get(0,JJ(0))
            pi0=ctx['pi'];rv0=ctx['rv'];lv=ctx['lie'](dq0,dd0,sv,szv)
            dn=dlother-sum((dp0[i]*rv0[i]+pi0[i]*(dv[i]-lv[i]) for i in range(12)),JJ(0))
            PP=[DD(t,{0:e}) for t,e in zip(pi0,dp0)]
            dB=density.improvement(ctx,Q,DX,PP).g.get(0,JJ(0))
            direct=(dn.c[0]-dB.c[1])/M.c[0]-cc0['sigma']*fj[0]
            predicted=cc0['A0']*fj[0]+cc0['A1']*fj[1]+cc0['A2']*fj[2]-sum((cc0['rv'][i]*v for i,v in zip((2,4,5),pc)),iv.mpf(0))
            defect=direct-predicted
            check('direct_other_action_scalar_trace_'+location+'_'+str(basis),hi(up(defect))<mp.mpf('1e-26'),mp.nstr(hi(up(defect)),24))
            check('direct_temporal_inverse_'+location+'_'+str(basis),hi(err)<mp.mpf('1e-30'))
            controls.append(dict(location=location,basis=basis,defect=binary(defect)))
        check('full_raw_current_momentum_controls_'+location,all(c['passed'] for c in ctx['checks']))
    check('all_sources_and_sidecar_bytes_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snap.items()))
    bounds={k:binary(v) for k,v in dict(trace_second=d2,trace_first=d1,trace_zeroth=d0,nonlocal_error=nonlocal_error,
             leading_drift=leading_drift,strong_error=strong_error,weak_error=weak_error,strong_contraction=ks,weak_contraction=kw).items()}
    return dict(kind='RTAU_COMPENSATED_STATIC_COUPLED_INVERSE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),reference_nonzero_mass=str(cn),reference_mean_mass=str(cm),
                reference_background_Sigma=str(sigref),reference_inverse=str(1/abs(cm)),bounds_binary=bounds,
                coefficients_binary={k:binary(co[k]) for k in ('A0','A1','A2','sigma')},
                inverse_L2_H2_binary=binary(strong) if strong is not None else None,
                inverse_Hminus1_H1_binary=binary(weak) if weak is not None else None,
                upper_display={k:mp.nstr(hi(v),24) for k,v in [('strong_contraction',ks),('weak_contraction',kw)]+([('inverse_L2_H2',strong)] if strong is not None else [])+([('inverse_Hminus1_H1',weak)] if weak is not None else [])},
                point_controls=controls,range='Projected inverse only; transverse zero-mean sources, weighted longitudinal compatibility and original fixed-I/U1 charge tangents retained; no fixed Sigma mean',
                scope='INITIAL_LINEAR_PLANAR_COMPENSATED_SCALAR_TRACE_OPERATOR',physical_energy='NOT_DERIVED',evolving_inverse='NOT_DERIVED',
                actual_time_tube='NOT_ESTABLISHED',Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=parser.parse_args()
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
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],'bounds':data['upper_display']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
