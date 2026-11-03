"""Local other-sector lapse pullback with full canonical linearization."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_CONTRACT_2026-11-03.md'
SPEC='Theory/Gates/RES-001/RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_EXECUTION_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
DENSITY='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
BODY='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
WEAK='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
LIFT='Analysis/MasterTests/test_01_r4c1_rtau_clock_density_v3.py'
V2='Analysis/MasterTests/outputs/rtau_strong_density_normal_form_v2_20261103/receipt.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),CONTRACT,SPEC,MANIFEST,FACTORY,DENSITY,BODY,WEAK,LIFT,V2):pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel in pins:
        for p in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if p.exists():snapshot[p]=(sha(p),p.stat().st_mtime_ns)
    check('all_219_original_source_hashes_match',len(original)==219)
    parent=json.loads((ROOT/V2).read_text())
    check('two_stage_normal_form_owner_passes',parent['passed']==parent['total'] and all(c['passed'] for c in parent['checks']))

    # Source dependency audit of the original normalized local body after
    # removing the declared force/regulator sectors. Geometry's q/dq use is
    # separately documented: metric slots 0..5 and frame slots 6..8 only.
    bodytree=ast.parse((ROOT/BODY).read_text(encoding='utf-8-sig'))
    body=next(n for n in bodytree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
    ret=copy.deepcopy(next(n.value for n in body.body if isinstance(n,ast.Return)))
    class Remove(ast.NodeTransformer):
        def visit_Name(self,node):return ast.copy_location(ast.Constant(0),node) if node.id in ('force','reg') else node
    ret=Remove().visit(ret)
    assignments={}
    for node in ast.walk(body):
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name):targets=[target.id]
                elif isinstance(target,(ast.Tuple,ast.List)):
                    targets=[n.id for n in ast.walk(target) if isinstance(n,ast.Name)]
                elif isinstance(target,ast.Subscript):
                    base=target
                    while isinstance(base,ast.Subscript):base=base.value
                    targets=[base.id] if isinstance(base,ast.Name) else []
                else:targets=[]
                deps={n.id for n in ast.walk(node.value) if isinstance(n,ast.Name)}
                for name in targets:assignments.setdefault(name,set()).update(deps)
    need={n.id for n in ast.walk(ret) if isinstance(n,ast.Name)};reached=set()
    while need-reached:
        name=next(iter(need-reached));reached.add(name)
        if name in assignments:need|=assignments[name]
    check('pruned_local_body_has_no_clock_gradient_or_velocity_dependency',not ({'gp','gz','Y','force','reg','s'} & reached))
    check('all_other_physical_sectors_retained',{'adm','frame','align','can','pot'}<=reached)
    lifttree=ast.parse((ROOT/LIFT).read_text());calc=next(n for n in lifttree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    lifted=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='lifted')
    liftret=next(n.value for n in lifted.body if isinstance(n,ast.Return))
    def segments(n):return segments(n.left)+segments(n.right) if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add) else [n]
    seg=segments(liftret)
    check('actual_clock_lift_sets_dust_multiplier_to_zero',ast.unparse(seg[0])=='y[:14]' and isinstance(seg[1],ast.List) and [n.value for n in seg[1].elts]==[0,0])
    check('weak_curvature_retains_both_lapse_and_gradient',"A[54]*gg-A[55]*flux" in (ROOT/WEAK).read_text().replace(' ',''))

    # Generic exact proof for arbitrary proper-velocity dependence and weak
    # curvature flux. No field equation or homogeneous constraint is used.
    N,Nz,w1,w2,g,flux=sp.symbols('N Nz w1 w2 g flux',nonzero=True)
    F=sp.Function('F');L=N*F(w1/N,w2/N,Nz/N)+N*g-Nz*flux
    hom=sp.simplify(L-N*sp.diff(L,N)-Nz*sp.diff(L,Nz)-w1*sp.diff(L,w1)-w2*sp.diff(L,w2))
    check('generic_proper_velocity_lapse_homogeneity',hom==0)
    z=sp.symbols('z');beta=sp.symbols('beta',nonzero=True)
    n,ln,lnz,pr=[sp.Function(k)(z) for k in ('n','LN','LNz','piRV')]
    lnclock=-beta*n*ln-beta*sp.diff(n,z)*lnz
    ldzclock=-beta*n*lnz
    eclock=lnclock-sp.diff(ldzclock,z)
    ihat=n*ln+sp.diff(n,z)*lnz
    improved=ihat-sp.diff(n*lnz,z)
    check('generic_local_clock_lapse_Euler_chain',sp.expand(eclock+beta*n*(ln-sp.diff(lnz,z)))==0)
    check('generic_improved_canonical_lapse_density',sp.expand(improved-n*(ln-sp.diff(lnz,z)))==0)
    check('generic_other_sector_identity_off_shell',sp.expand(eclock+beta*improved)==0)
    eps=sp.symbols('eps');dn,dln,dlnz=[sp.Function(k)(z) for k in ('dn','dLN','dLNz')]
    variation={n:n+eps*dn,ln:ln+eps*dln,lnz:lnz+eps*dlnz}
    check('generic_full_first_variation_identity',sp.expand(sp.diff((eclock+beta*improved).subs(variation,simultaneous=True).doit(),eps).subs(eps,0))==0)
    nt=1+sp.cos(z)/5;lt=sp.sin(z)/7
    check('omitting_local_improvement_rejected_generically',sp.simplify(sp.diff(nt*lt,z))!=0)

    fac=load('other_lapse_factory',FACTORY);env=fac.prepare();transport=load('other_lapse_improvement',DENSITY)
    pars=env['env']['env']['exact'];b,bet,KQ,A=[rational(pars[k]) for k in ('b','beta','K_Q','A')]
    def sector(ctx,y,Lraw,raw):
        J,D=ctx['J'],ctx['D'];q,v,d,S=y[:14],y[14:28],y[28:42],y[42:45]
        Q=[D.var(x,i) for i,x in enumerate(q)];V=[D.var(x,14+i) for i,x in enumerate(v)]
        DX=[D.var(x,28+i) for i,x in enumerate(d)];SS=[D.var(x,42+i) for i,x in enumerate(S)]
        nc,mu,gamma,H,_=ctx['geometry'](Q,DX)
        n0=ctx['geometry'](q,d)[0];nz0=n0*d[12]*(-bet)
        N=D.var(n0,48) if raw else nc
        NZ=D.var(nz0,49) if raw else N*DX[12]*(-bet)
        pp=(V[12]-SS[2]*DX[12])/N
        h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        rest=[H[i][2]*DX[12]+Q[6+i]*(pp+Q[8]*DX[12]/(gamma+1)) for i in range(3)]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0
        force=(gamma*pp+Q[8]*DX[12])**2*KQ/2-Y**mp.mpf('1.5')*A
        M=N*mu
        regulator=M*Q[13]**2*(b/2)-M*H[2][2]*DX[13]*DX[12]*b-mu*Q[13]*H[2][2]*NZ*DX[12]*b
        return dict(L=Lraw-M*force-regulator,N=N,Nz=NZ,M=M,Q=Q,DX=DX,Y=Y)

    controls=[];omit_improvement=False;omit_measure=False;omit_lapse_gradient=False
    for location in ('0.3','1.1','2.4'):
        ctx=fac.point(location);y,Lc,LR=ctx['y'],ctx['L'],ctx['LR']
        clock=sector(ctx,y,Lc,False);raw=sector(ctx,y,LR,True)
        J,D,grad,hj=ctx['J'],ctx['D'],ctx['gradient'],ctx['hj'];oc,orr=clock['L'],raw['L']
        q,v,d,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
        rv=[a-c for a,c in zip(v,ctx['lie'](q,d,S,Sz))]
        po=[grad(oc,14+i) for i in range(13)]+[J(0)]
        hat=oc.c-sum((po[i]*rv[i] for i in range(12)),J(0))
        B0=transport.improvement(ctx,q,d,po)
        Ican=hat.c[0]-B0.c[1]
        LN,LNz=grad(orr,48),grad(orr,49);n0=raw['N'].c;nz0=raw['Nz'].c
        Iraw=n0.c[0]*(LN.c[0]-LNz.c[1])
        E=grad(oc,12).c[0]-grad(oc,40).c[1]
        homog=orr.c-sum((grad(orr,14+i)*rv[i] for i in range(12)),J(0))-n0*LN-nz0*LNz
        defects=[up(homog.c[k]) for k in (0,1)]
        check('actual_raw_lapse_homogeneity_'+location,all(hi(x)<mp.mpf('1e-26') for x in defects))
        check('actual_raw_clock_sector_values_match_'+location,hi(up(oc.c.c[0]-orr.c.c[0]))<mp.mpf('1e-26'))
        check('actual_raw_canonical_improvement_match_'+location,all(hi(up((n0*LNz-B0).c[k]))<mp.mpf('1e-26') for k in (0,1)))
        check('actual_local_lapse_and_clock_identity_'+location,hi(up(Ican-Iraw))<mp.mpf('1e-26') and hi(up(E+bet*Ican))<mp.mpf('1e-26'))
        # These numerical near-zero differences are controls; the exact
        # absence follows from the audited sector/source construction.
        check('raw_other_sector_clock_partials_near_zero_'+location,all(hi(up(grad(orr,i).c[k]))<mp.mpf('1e-26') for i in (12,26,40) for k in (0,1)))
        omit_improvement|=hi(up(E+bet*hat.c[0]))>mp.mpf('1e-16')
        omit_lapse_gradient|=hi(up(bet*nz0.c[0]*LNz.c[0]))>mp.mpf('1e-16')
        for label in ('all_fields_canonical_momenta_shift','clock_sector'):
            x=[J(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(14)]
            dx=[J(coefficients=[v.c[1],2*v.c[2],iv.mpf(0)]) for v in x]
            pi=[J(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,iv.mpf(0)]) for i in range(13)]+[J(0)]
            w=[J(coefficients=[iv.mpf(i+1)/113,-iv.mpf(i+2)/127,iv.mpf(0)]) for i in range(3)]
            wz=[J(coefficients=[v.c[1],iv.mpf(0),iv.mpf(0)]) for v in w]
            if label=='clock_sector':
                x=[J(0)]*14;x[12]=J(coefficients=[iv.mpf(1)/3,iv.mpf(1)/5,iv.mpf(1)/7])
                dx=[J(coefficients=[v.c[1],2*v.c[2],iv.mpf(0)]) for v in x]
                pi=[J(0)]*14;pi[12]=J(coefficients=[iv.mpf(1)/11,iv.mpf(1)/13,iv.mpf(0)]);w=[J(0)]*3;wz=[J(0)]*3
            dy0=x+[J(0)]*14+dx+w+wz
            rhs=[pi[i]-sum((ctx['hj'](Lc,14+i,k)*dy0[k] for k in range(48)),J(0)) for i in range(13)]
            dv0,e0=ctx['solve']([v.c[0] for v in rhs])
            dv1,e1=ctx['solve']([rhs[i].c[1]-sum((ctx['Mz'][i][j]*dv0[j] for j in range(13)),iv.mpf(0)) for i in range(13)])
            dv=[J(coefficients=[a,b,iv.mpf(0)]) for a,b in zip(dv0,dv1)]+[J(0)];dy=x+dv+dx+w+wz
            dpo=[sum((hj(oc,14+i,k)*dy[k] for k in range(48)),J(0)) for i in range(13)]+[J(0)]
            check('complete_canonical_inverse_'+location+'_'+label,hi(e0)<mp.mpf('1e-30') and hi(e1)<mp.mpf('1e-30') and all(hi(up((dpo[i]-pi[i]).c[k]))<mp.mpf('1e-25') for i in range(12) for k in (0,1)))
            QQ=[D(t,{0:e}) for t,e in zip(q,x)];DD=[D(t,{0:e}) for t,e in zip(d,dx)];PP=[D(t,{0:e}) for t,e in zip(po,dpo)]
            dB=transport.improvement(ctx,QQ,DD,PP).g.get(0,J(0))
            lvar=ctx['lie'](x,dx,S,Sz);lw=ctx['lie'](q,d,w,wz)
            dhat=sum((grad(oc,k)*dy[k] for k in range(48)),J(0))
            dhat-=sum((dpo[i]*rv[i]+po[i]*(dv[i]-lvar[i]-lw[i]) for i in range(12)),J(0))
            dIcan=dhat.c[0]-dB.c[1]
            dE=sum((hj(oc,12,k)*dy[k] for k in range(48)),J(0)).c[0]-sum((hj(oc,40,k)*dy[k] for k in range(48)),J(0)).c[1]
            dn=n0*x[12]*(-bet);dnz=(n0*dx[12]+nz0*x[12])*(-bet)
            dry=dy+[dn,dnz]
            dLN=sum((hj(orr,48,k)*dry[k] for k in range(50)),J(0))
            dLNz=sum((hj(orr,49,k)*dry[k] for k in range(50)),J(0))
            dIraw=dn.c[0]*(LN.c[0]-LNz.c[1])+n0.c[0]*(dLN.c[0]-dLNz.c[1])
            error1=dE+bet*dIcan;error2=dIraw-dIcan
            check('full_linearized_other_Euler_identity_'+location+'_'+label,hi(up(error1))<mp.mpf('1e-25'),mp.nstr(hi(up(error1)),24))
            check('full_raw_lapse_linearization_'+location+'_'+label,hi(up(error2))<mp.mpf('1e-25'),mp.nstr(hi(up(error2)),24))
            nn,mm,_,_,_=ctx['geometry'](QQ,DD);M=(nn*mm).c;dM=(nn*mm).g.get(0,J(0))
            Sigma=Ican/M.c[0];dSigma=(dIcan-Sigma*dM.c[0])/M.c[0]
            check('linearized_physical_measure_retained_'+location+'_'+label,hi(up(dE+bet*(M.c[0]*dSigma+Sigma*dM.c[0])))<mp.mpf('1e-25'))
            omit_measure|=hi(up(dE+bet*M.c[0]*dSigma))>mp.mpf('1e-16')
            controls.append(dict(location=location,label=label,Euler_defect=binary(error1),raw_lapse_defect=binary(error2)))
    check('omitted_local_improvement_rejected_on_actual_data',omit_improvement)
    check('omitted_lapse_gradient_chain_term_rejected_on_actual_data',omit_lapse_gradient)
    check('omitted_physical_measure_variation_rejected_on_actual_data',omit_measure)
    check('all_source_sidecar_bytes_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snapshot.items()))
    return dict(kind='RTAU_OTHER_SECTOR_LOCAL_LAPSE_IDENTITY_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),source_reachable_names=sorted(reached),point_controls=controls,
                exact_identity='E_other=-beta*N*E_N,other=-beta*I_other=-beta*M*Sigma',
                exact_linearization='delta E_other=-beta*(M*delta Sigma+Sigma*delta M)',
                proof_scope='Off-shell local identity of the declared nonmatter force/regulator-free clock sector, including N_z improvement; no Euler equation assumed in its proof',
                reorganized_density_reaction='-N*trK*Sigma replaces N*(beta*p-trK)*Sigma+(p/mu)*E_other',
                reorganized_scalar_current='pi_t=D(S*pi-M*f_s+d*Z_z-2*beta*d*Z*s)+beta*M*(e_force-Sigma)-beta*L_reg',
                normal_form_remainder='V1/V2 identities retained with the reorganized reaction and complete new current/local sources; no modes or means removed',
                strong_density_L2_source_bound='NOT_YET_QUANTIFIED',full_coupled_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

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
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],
                      'identity':data['exact_identity'],'full_coupled_energy':data['full_coupled_energy']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
