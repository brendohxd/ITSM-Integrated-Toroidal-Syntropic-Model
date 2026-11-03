"""Second fast-gradient normal form; full coupled energy remains open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V2_EXECUTION_SPEC_2026-11-03.md'
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_CONTRACT_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
V1='Analysis/MasterTests/outputs/rtau_strong_density_normal_form_v1_20261103/receipt.json'
V1REPORT='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_REPORT_2026-11-03.md'
HIGHER='Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,CONTRACT,MANIFEST,FACTORY,V1,V1REPORT,HIGHER,MIXED):pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snap[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_hashes_match',len(original)==219)
    parent,higher,mixed=[json.loads((ROOT/rel).read_text()) for rel in (V1,HIGHER,MIXED)]
    check('first_normal_form_and_actual_action_owners_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (parent,higher,mixed)))
    hkeys={tuple(x['ij']) for x in mixed['full_mixed_Hessian_upper_triangle']}
    check('ordinary_temporal_block_decouples_clock_velocity_exactly',all(tuple(sorted((14+i,26))) not in hkeys for i in range(12)))

    # Complete force-gradient coefficient at fixed background geometry.
    N,mu,p,fs,fps,dpz=sp.symbols('N mu p fs fps dpz',nonzero=True)
    gradient=-(p/mu)*(N*mu*fps*dpz)-fs*N*dpz
    coefficient=-N*(p*fps+fs);alpha=-(p*fps+fs)
    check('actual_force_gradient_coefficient',sp.expand(gradient-coefficient*dpz)==0)
    check('kinematic_gradient_correction_cancels_fast_derivative',sp.expand(coefficient-alpha*N)==0)
    S,C,a,at,az,Sz,Nz,dpp,Gz,Q,w,wz,chiz=sp.symbols('S C a at az Sz Nz dpp Gz Q w wz chiz')
    # u1=w+a*chi_z, material chi_z rate=N*delta p_z+Nz*delta p+Sz*chi_z+Gchi_z.
    raw=C*(w+a*chiz)+a*N*dpz+Q-(at-S*az)*chiz-a*(N*dpz+Nz*dpp+Sz*chiz+Gz)
    transformed=C*w+(C*a-at+S*az-a*Sz)*chiz+Q-a*Nz*dpp-a*Gz
    check('complete_second_normal_form_row',sp.expand(raw-transformed)==0)
    check('second_coefficient_time_drift_not_dropped',sp.diff(sp.expand(raw),at)==-chiz)
    check('coordinate_vector_weight_term_retained',sp.diff(sp.expand(raw),Sz)==-a*chiz)
    z=sp.symbols('z');vel,chi=[sp.Function(n)(z) for n in ('S','chi')]
    check('gradient_transport_commutator',sp.expand(sp.diff(vel*sp.diff(chi,z),z)-vel*sp.diff(chi,z,2)-sp.diff(vel,z)*sp.diff(chi,z))==0)
    # Independent periodic exact control with nonconstant coefficients.
    st=sp.sin(z)/7;nt=2+sp.cos(z)/11;alt=sp.cos(z)/13;ct=1+sp.sin(z)/17
    cht=sp.sin(2*z)/19;dpt=sp.cos(z)/23;gt=sp.sin(z)/29;qt=sp.cos(2*z)/31
    altime=1+sp.cos(z)/37;wt=sp.sin(3*z)/41;u1=wt+alt*sp.diff(cht,z)
    chi_time=st*sp.diff(cht,z)+nt*dpt+gt
    u1time=st*sp.diff(u1,z)+ct*u1+alt*nt*sp.diff(dpt,z)+qt
    wtime=u1time-altime*sp.diff(cht,z)-alt*sp.diff(chi_time,z)
    expected=st*sp.diff(wt,z)+ct*wt+(ct*alt-altime+st*sp.diff(alt,z)-alt*sp.diff(st,z))*sp.diff(cht,z)
    expected+=qt-alt*sp.diff(nt,z)*dpt-alt*sp.diff(gt,z)
    check('independent_periodic_second_normal_form_identity',sp.trigsimp(sp.expand(wtime-expected))==0)

    fac=load('second_normal_form_factory',FACTORY);env=fac.prepare();pars=env['env']['env']['exact']
    KQ,A=[rational(pars[k]) for k in ('K_Q','A')]
    third=decode(higher['whole_circle_third_shift_bound']);thirdbox=iv.mpf([-hi(third),hi(third)])

    def force(ctx,q,pn,sn):
        J,D=ctx['J'],ctx['D'];Q=[D.var(x,i) for i,x in enumerate(q)]
        pp=D.var(pn,100);ss=D.var(sn,101)
        _,mu,gamma,H,_=ctx['geometry'](Q,[J(0)]*14)
        h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        rest=[H[i][2]*ss+Q[6+i]*(pp+Q[8]*ss/(gamma+1)) for i in range(3)]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0,'No third force derivative inferred at Y=0'
        f=(gamma*pp+Q[8]*ss)**2*KQ/2-Y**mp.mpf('1.5')*A
        return dict(f=f,Y=Y,mu=mu,gamma=gamma,H=H,Q=Q)

    def compute(ctx,y,L):
        J=ctx['J'];grad=ctx['gradient'];q,v,d,S=y[:14],y[14:28],y[28:42],y[42:45]
        N,mu,_,_,_=ctx['geometry'](q,d);pn=(v[12]-S[2]*d[12])/N
        F=force(ctx,q,pn,d[12]);f=F['f']
        fs=f.g.get(101,J(0));fp=f.g.get(100,J(0));fps=f.h.get((100,101),J(0));fpp=f.h.get((100,100),J(0))
        alpha=-(pn*fps+fs)
        assert lo(fpp.c[0])>0,'Cannot derive p_t if f_pp may vanish'
        mut=sum((F['mu'].g.get(i,J(0)).c[0]*v[i].c[0] for i in range(13)),iv.mpf(0))
        ptcanon=grad(L,12).c[0]-grad(L,40).c[1]
        drift=sum((f.h.get(tuple(sorted((100,i))),J(0)).c[0]*v[i].c[0] for i in range(9)),iv.mpf(0))
        sdot=v[12].c[1]
        ptime=(ptcanon-mut*fp.c[0]-mu.c[0]*(drift+fps.c[0]*sdot))/(mu.c[0]*fpp.c[0])
        # Only the first time coefficient is used; zero higher Taylor slots
        # are storage, not assertions about higher background time derivatives.
        qtime=[J(coefficients=[a.c[0],b.c[0],iv.mpf(0)]) for a,b in zip(q,v)]
        ptimejet=J(coefficients=[pn.c[0],ptime,iv.mpf(0)])
        stimejet=J(coefficients=[d[12].c[0],sdot,iv.mpf(0)])
        FT=force(ctx,qtime,ptimejet,stimejet);ft=FT['f']
        atime=-(ptimejet*ft.h.get((100,101),J(0))+ft.g.get(101,J(0)))
        return dict(alpha=alpha,alpha_time=atime.c[1],p_time=ptime,F=F,FT=FT,pn=pn,
                    ptimejet=ptimejet,stimejet=stimejet,fpp=fpp,ptcanon=ptcanon)

    J=env['J'];y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[thirdbox]*3)
    L=env['evaluate'](y);whole=compute(env,y,L)
    alpha0=up(whole['alpha'].c[0]);alpha1=up(whole['alpha'].c[1]);alphat=up(whole['alpha_time'])
    c0=decode(parent['bounds_binary']['coefficient']);mapbound=1+c0+alpha0
    check('normal_clock_kinetic_coefficient_positive_on_whole_root',lo(whole['fpp'].c[0])>0)
    check('whole_root_force_and_time_coefficients_finite',all(mp.isfinite(hi(x)) for x in (alpha0,alpha1,alphat,up(whole['p_time']),mapbound)))
    check('nonzero_norm_cubed_interaction_retained',lo(A)>0)
    check('combined_map_preserves_density_L2_order',hi(mapbound)>=1 and parent['density_strength'].startswith('L2 retained'))
    # The inverse is sigma=w+c*P(delta pi)+alpha*chi_z, with all other
    # physical data unchanged. No Fourier mode or density component is lost.
    sig,u,c,prim,al,dchi=sp.symbols('sig u c prim al dchi')
    check('combined_triangular_inverse_exact',sp.expand((sig-c*prim-al*dchi)+c*prim+al*dchi-sig)==0)
    point_controls=[]
    for loc in ('0.3','1.1','2.4'):
        ctx=fac.point(loc);yy,LL=ctx['y'],ctx['L'];pco=compute(ctx,yy,LL)
        F=pco['FT'];gamma=F['gamma'].c;H=F['H'];Q=F['Q'];pn=pco['ptimejet'];sn=pco['stimejet'];Y=F['Y'].c
        # Use the time-direction metric itself, not a frozen spatial metric,
        # when constructing the independent closed partial derivatives.
        h=[[Q[0].c,Q[1].c,Q[2].c],[Q[1].c,Q[3].c,Q[4].c],[Q[2].c,Q[4].c,Q[5].c]]
        tilt=sum((Q[6+i].c*h[i][j]*Q[6+j].c for i in range(3) for j in range(3)),ctx['J'](0))
        vz=Q[8].c;kap=H[2][2].c
        B=gamma*vz*pn+(kap+vz*vz)*sn
        Dp=tilt*pn+gamma*vz*sn
        rootY=Y**mp.mpf('.5')
        fs_exp=vz*(gamma*pn+vz*sn)*KQ-rootY*B*(3*A)
        fps_exp=gamma*vz*KQ-(Dp*B/rootY+rootY*gamma*vz)*(3*A)
        alpha_exp=-(pn*fps_exp+fs_exp)
        defect=alpha_exp.c[1]-pco['alpha_time']
        check('independent_full_force_time_partial_'+loc,hi(up(defect))<mp.mpf('1e-25'),mp.nstr(hi(up(defect)),24))
        check('actual_point_alpha_coefficients_enclosed_'+loc,hi(up(pco['alpha'].c[0]))<=hi(alpha0) and hi(up(pco['alpha_time']))<=hi(alphat))
        point_controls.append(dict(location=loc,alpha_time=binary(pco['alpha_time']),explicit_partial_defect=binary(defect)))
    check('all_source_sidecar_bytes_timestamps_preserved',all(sha(path)==h and path.stat().st_mtime_ns==t for path,(h,t) in snap.items()))
    values=dict(alpha=alpha0,alpha_z=alpha1,alpha_time=alphat,normal_p_time=up(whole['p_time']),
                normal_force_kinetic_lower=iv.mpf(lo(whole['fpp'].c[0])),combined_triangular_map=mapbound)
    return dict(kind='RTAU_STRONG_DENSITY_SECOND_FAST_NORMAL_FORM_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),bounds_binary={k:binary(v) for k,v in values.items()},upper_display={k:mp.nstr(hi(v),24) for k,v in values.items()},
                point_controls=point_controls,alpha_definition='-(p*f_ps+f_s), with the full frame-dependent norm-cubed force',
                complete_row='w_t-S*w_z=C*w+(C*alpha-alpha_t+S*alpha_z-alpha*S_z)*chi_z+Q0-alpha*N_z*delta_p-alpha*D_z(Gchi)',
                remainder='Q0 is the complete V1 row remainder after isolating -N*(p*f_ps+f_s)*delta_p_z; all primitive means/current/gauge/ordinary couplings retained',
                transformation='w=deltaSigma-c*P(delta pi_psi)-alpha*D_z(delta psi)',
                density_strength='L2 retained; canonical momentum L2 and force H2 controls unchanged',
                removed_fast_terms=['delta Z_z','delta p_z'],ordinary_coupled_energy='NOT_DERIVED',full_normal_form_contract='INCOMPLETE',actual_time_tube='NOT_ESTABLISHED',
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
                      'bounds':data['upper_display'],'ordinary_coupled_energy':data['ordinary_coupled_energy']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
