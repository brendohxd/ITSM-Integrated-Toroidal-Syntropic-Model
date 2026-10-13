"""Prepared-data dust error bound; sharp order and physical gates remain open."""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2];BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_g3n5_dust_fast_transfer_attempt_01/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_dust_fast_transfer_v1.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='7a982ff1c100b35aee057030f818efd7024af491cd537fc0baf88cf486eac2cf':raise RuntimeError('Engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_fast_transfer_v1 as parent
old=parent.old;common=old.common
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_PREPARED_DUST_ERROR_CONTRACT_2026-10-11.md'
CONTROL='Theory/Gates/RES-001/RES001_R4C1_G3N5_PREPARED_ERROR_CONTROLS_2026-10-11.md'
PROGRESS=None

def progress(message):
    print(message,flush=True)
    if PROGRESS is not None:PROGRESS.write(message+'\n');PROGRESS.flush()

def wire(mat):return {'shape':list(mat.shape),'entries':[{'row':i,'column':j,'terms':[str(mat[i,j])]} for i in range(mat.rows) for j in range(mat.cols) if mat[i,j]!=0]}
def complex_array(obj):
    z=np.array(obj);return z[...,0]+1j*z[...,1]

def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()});pins[PARENT+'summary.json']='c05d0237a34a4ac35771dc24da9ad961df3ed8c1fd947c10c1ca24c9d6c0d5d9'
    for rel in (CONTRACT,CONTROL,SELF):pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;eps=s.Symbol('eps',positive=True)
    on=lambda mat:mat.applyfunc(s.cancel)
    shell=lambda mat:mat.applyfunc(lambda z:bg.constraint_reduce_scalar(z) if z!=0 else s.Integer(0))
    exact=lambda name,mat:old.parent.exact(checks,name,on(mat) if isinstance(mat,s.MatrixBase) else s.cancel(mat))
    checks.add('parent_component_lemma_not_full_error',ps['passed']==ps['total']==33 and ps['fast_component_transfer_proved'] and not ps['full_prepared_high_p_remainder_proved'])
    exact('Friedmann_shell_preserved',bg.dt(s.Matrix([bg.constraint])))
    raw=common.read_json(old.PARENT+'matrices.json')
    az,bo,bi,obs,graph,mm,qfields=[old.parent.import_matrix(raw[k],bg.sy) for k in ('balanced_generator','balancing_map','balancing_map_inverse','actual_dust_observable','formal_slow_lift','leading_dust_generator','full_field_reconstruction')]
    uniform=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    original=common.read_json(uniform['general_exact_maps_source'])['matrices']
    cm,um,tw,twi=[old.parent.import_matrix(original[k],bg.sy) for k in ('longitudinal_velocity_scaling_C','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi')]
    ci=s.eye(20);ci[13,13]=a/ell;ac=on((bg.dt(cm)+cm*az)*ci);oc=on(obs*bi*ci)
    blocks={}
    for i in range(20):
        for j in range(20):
            for term in s.Add.make_args(s.expand(ac[i,j])):
                power=term.as_powers_dict().get(ell,s.Integer(0));val=s.cancel(term/ell**power)
                if not power.is_Integer or ell in val.free_symbols:raise ValueError('Not Laurent')
                blocks.setdefault(int(power),s.zeros(20))[i,j]+=val
    exact('complete_generator_Laurent_identity',ac-sum((mat*ell**d for d,mat in blocks.items()),s.zeros(20)))
    fi=s.zeros(20);fi[9,19]=-33*a*a/5;fi[19,9]=a*a
    lift={j:s.zeros(20,2) for j in range(4)}
    lift[0][0,:]=s.Matrix([[12*s.sqrt(2)*s.I*rho/11,2*s.sqrt(2)*s.I*H]]);lift[0][3,1]=1
    for pos,vel in ((6,ud),(7,vd),(8,rd)):lift[0][pos,1]=s.I*vel
    lift[0][13,:]=s.Matrix([[6*rho/11,-H-2*pd/5]])
    flow=on(bg.dt(lift[0])+lift[0]*mm)
    for pos,vel in ((0,10),(1,11),(2,12),(4,14),(5,15),(6,16),(7,17),(8,18)):lift[1][vel,:]=a*flow[pos,:]
    forced=on(-fi*blocks[1]*lift[0]);lift[1]+=forced
    dots={}
    def dtlift(j):
        if j not in dots:dots[j]=bg.dt(lift[j])
        return dots[j]
    def rawres(power):
        z=sum((mat*lift[d-power] for d,mat in blocks.items() if d-power in lift),s.zeros(20,2))
        if -power in lift:z-=dtlift(-power)+lift[-power]*mm
        return z
    def reduced_res(power):return shell(on(rawres(power)))
    progress('Leading lift and action-derived forced fast coefficient constructed')
    rr=reduced_res(0);lift[2]+=on(-fi*rr);dots.pop(2,None)
    for power in (2,1,0):exact('leading_residual_power_'+str(power),reduced_res(power))
    rw=shell(on(tw*reduced_res(-1)))
    exact('order_minus_one_slow_compatibility',rw[[3,13],:])
    wavefix=s.zeros(20,2)
    for pos,vel,speed2 in ((0,10,s.Rational(1,3)),(1,11,1),(2,12,1),(4,14,s.Rational(4,5)),(5,15,s.Rational(4,5)),(8,18,1)):
        wavefix[pos,:]=a*rw[vel,:]/speed2;wavefix[vel,:]=-a*rw[pos,:]
    pp=s.eye(2)+s.Matrix([v,-u])*s.Matrix([[v,-u]])/13
    wavefix[6:8,:]=on(a*pp.inv()*rw[16:18,:]);wavefix[16:18,:]=-a*rw[6:8,:]
    lift[2]+=on(twi*wavefix);dots.pop(2,None)
    rr=reduced_res(-1);exact('remaining_source_only_in_fast_block',rr[[i for i in range(20) if i not in (9,19)],:])
    lift[3]+=on(-fi*rr);dots.pop(3,None)
    for power in (2,1,0,-1):exact('corrected_lift_residual_power_'+str(power),reduced_res(power))
    checks.add('forced_fast_coefficient_nonzero',any(z!=0 for z in forced))
    progress('All positive, constant and inverse-ell residual coefficients verified')
    boxes={bg.sy[k]:(s.sympify(val[0]),s.sympify(val[1])) for k,val in uniform['background_boxes'].items()};bx=old.RationalBox(boxes)
    n2=lambda mat:max(bx.norm(mat),bx.norm(mat.T))
    fastcert=common.read_json(PARENT+'formulas.json');vf=old.parent.import_matrix(fastcert['matrices']['second_fast_map_V'],bg.sy)
    emin=ps['ell_min'];vb=s.sympify(fastcert['constants']['V_norm']);kap=s.sympify(fastcert['constants']['kappa']);gamma=s.sympify(fastcert['constants']['gamma_diagonal'])
    an={d:n2(mat) for d,mat in blocks.items()};hn={j:n2(mat) for j,mat in lift.items()}
    dn={j:n2(dtlift(j)) for j in (2,3)}
    checks.add('leading_transfer_21_over_10_norm_bound',n2(mm)<=s.Rational(21,10))
    rn={}
    for j in range(2,6):
        rn[j]=sum(an[d]*hn[d+j] for d in blocks if d+j in lift)
        if j in lift:rn[j]+=dn[j]+hn[j]*s.Rational(21,10)
    def source_bound(k):return sum(rn[j]/s.Integer(k)**(j-2) for j in rn)
    kr=source_bound(emin);kr4=source_bound(4)
    progress('Whole-interval residual-source constants obtained without sampled maxima')
    hc=sum((lift[j]*eps**j for j in lift),s.zeros(20,2));oce=oc.subs(ell,1/eps)
    observe=on(oce*hc-s.eye(2));maxdeg=max((s.Poly(x,eps).degree() for x in observe if x!=0),default=0)
    ocoef={j:s.Matrix(2,2,lambda i,k:s.Poly(observe[i,k],eps).nth(j)) for j in range(int(maxdeg)+1)}
    for j in (0,1):exact('observable_normalization_power_'+str(j),shell(ocoef.get(j,s.zeros(2))))
    def observable_ref_bound(k):return sum(n2(mat)/s.Integer(k)**(j-2) for j,mat in ocoef.items() if j>=2)
    kho=observable_ref_bound(emin);kho4=observable_ref_bound(4)
    progress('Actual-observable comparison-lift normalization bounds obtained')
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    init={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    for i,z in enumerate(bg.bg):checks.add('original_initial_'+str(z),bool(abs(s.N(s.Rational(coeff['background_coefficients'][i][0][0])-init[z],75))<s.Rational(1,10)**60))
    op0=on(obs.subs(init));g0=on(graph.subs(init));bc0=on((cm*bo).subs(init));og0=on(op0*g0)
    oldinitial=on(bc0*g0*og0.inv()).subs(ell,1/eps);hi=hc.subs(init)
    delta1=on(-forced.subs(init));delta2=on((oldinitial-hi-eps*delta1)/eps**2)
    checks.add('initial_mismatch_fast_only_at_first_order',all(delta1[i,k]==0 for i in range(20) if i not in (9,19) for k in range(2)))
    exact('initial_mismatch_recomposition',oldinitial-hi-eps*delta1-eps**2*delta2)
    for mat in (delta2,):
        for val in mat:
            _,den=s.cancel(val).as_numer_denom()
            if den.subs(eps,0)==0:raise ValueError('Initial remainder not analytic at inverse ell zero')
    def constant_n2(mat,k):
        point=old.RationalBox({eps:(s.Integer(0),s.Rational(1,k))})
        return max(point.norm(mat),point.norm(mat.T))
    kd2=constant_n2(delta2,emin);kd1=constant_n2(delta1,emin)
    ub=n2(um);u2b=n2(on(um*um));twb=n2(tw)
    kw=s.cancel(s.Rational(3,2)*twb*(1+ub/emin+u2b/s.Integer(emin)**2))
    kw4=s.cancel(s.Rational(3,2)*twb*(1+ub/4+u2b/16))
    co=s.cancel(kw*kd2+s.Rational(3,2)*twb*(ub+u2b/emin)*kd1+2*(3*vb)*kw*(kd1/emin+kd2/s.Integer(emin)**2))
    cf=s.cancel(2*kw*(kd1+kd2/emin))
    oy=on(oce*(s.eye(20)+um*eps)*twi*(s.eye(20)+vf*eps**2))
    fullbox=old.RationalBox({**boxes,eps:(s.Integer(0),s.Rational(1,emin))})
    fulln=lambda mat:max(fullbox.norm(mat),fullbox.norm(mat.T))
    ko=3*fulln(oy);of=oy[:,[9,19]]
    exact('actual_fast_observable_zero_leading',of.subs(eps,0))
    kof=3*fulln(on(of/eps))
    T=s.Rational(1,20)
    # Full solution retained. Split the ORIGINAL mismatch into orthogonal
    # components only for the inequality; no new prepared initial data.
    def high_bound(t):
        return s.Rational(3,2)*(ko*(3*s.exp(30*t)*(co+2*kw*kr*t)+9*kap*t*s.exp(gamma*t)*cf)+3*kof*s.exp(30*t)*cf+kho*s.exp(s.Rational(21,10)*t))
    c2=high_bound(T)
    ow=on(oce*(s.eye(20)+um*eps)*twi);low={}
    for kval in (4,8):
        kdl=constant_n2(delta2,kval);lowbox=old.RationalBox({**boxes,eps:(s.Rational(1,kval),s.Rational(1,kval))})
        kow=3*max(lowbox.norm(ow),lowbox.norm(ow.T))
        low[kval]={'delta2':kdl,'observable':kow}
    progress('Original-data mismatch, fast transfer and complete error constants combined')
    payload_mats={f'comparison_lift_H{j}':mat for j,mat in lift.items()};payload_mats.update(forced_fast_coefficient=forced,initial_fast_mismatch=delta1,initial_remainder=delta2)
    exported={k:wire(mat) for k,mat in payload_mats.items()}
    for name,val in exported.items():exact('roundtrip_'+name,old.parent.import_matrix(val,{**bg.sy,'eps':eps})-payload_mats[name])
    ar=common.read_json(old.PARENT+'trajectories.json');bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']]);phi=np.asarray(ar['leading_Phi'],complex)
    checks.add('leading_Phi_real_matrix_wire_shape',phi.shape==(len(ar['time']),2,2))
    fn=s.lambdify([bg.bg,ell],(oc,ci,hc.subs(eps,1/ell),bg.dt(hc).subs(eps,1/ell),ac,qfields*bi),'numpy',cse=True)
    residual_fn=s.lambdify([bg.bg,ell],sum((rawres(-j)/ell**j for j in range(2,6)),s.zeros(20,2)),'numpy',cse=True)
    modes=[]
    for item in ar['modes']:
        kval=item['ell'];maxfields=maxobs=maxres=maxerror=maxidentity=0.;maxviolation=0.
        for ix,t in enumerate(ar['time']):
            bval=np.polynomial.polynomial.polyval(t,bc.T);oo,cin,hh,hd,aa,qq=[np.asarray(x,complex) for x in fn(bval,kval)]
            z=complex_array(item['balanced'][ix]);w=oo@np.linalg.inv(cin)@z;oldw=complex_array(item['dust_observables'][ix]);oldfields=complex_array(item['full_fields'][ix])
            maxobs=max(maxobs,float(np.linalg.norm(w-oldw,np.inf)/max(1.,np.linalg.norm(oldw,np.inf))))
            maxfields=max(maxfields,float(np.linalg.norm(qq@z-oldfields,np.inf)/max(1.,np.linalg.norm(oldfields,np.inf))))
            err=float(np.linalg.norm(w[:,:2]-phi[ix],np.inf));maxerror=max(maxerror,err)
            if kval>=emin:
                bound=float(high_bound(s.Rational(str(t)))/kval**2)
            else:
                kow=low[kval]['observable'];kdl=low[kval]['delta2'];tt=s.Rational(str(t))
                bound=float(s.Rational(3,2)*(kow*kw4*s.exp(30*tt)*(kd1/kval+(kdl+kr4*tt)/kval**2)+kho4*s.exp(s.Rational(21,10)*tt)/kval**2))
            maxviolation=max(maxviolation,err-bound-1e-9*(1+abs(bound)))
            if ix in (0,len(ar['time'])//2,len(ar['time'])-1):
                mn=np.asarray(s.lambdify([bg.bg],mm,'numpy')(bval),complex)
                direct=aa@hh-hd-hh@mn
                recomposed=np.asarray(residual_fn(bval,kval),complex)
                maxidentity=max(maxidentity,float(np.linalg.norm(direct-recomposed,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
                # This numerical check uses the source majorant, while exact
                # low-power cancellations and complete source terms above
                # provide the proof, not a sampled residual fit.
                allowed=float(source_bound(kval)/kval**2)
                maxres=max(maxres,float(np.linalg.norm(direct,2)/max(1.,allowed)))
        checks.add('prepared_actual_error_bound_'+str(kval),maxviolation<=0,maxviolation,'<=0 after predeclared binary64 allowance')
        checks.add('actual_observable_unchanged_'+str(kval),maxobs<=1e-10,maxobs,'<=1e-10')
        checks.add('all_22_fields_unchanged_'+str(kval),maxfields<=1e-10,maxfields,'<=1e-10')
        checks.add('retained_source_majorant_numeric_'+str(kval),maxres<=1+1e-9,maxres,'<=1 with predeclared roundoff only')
        checks.add('direct_Laurent_residual_identity_'+str(kval),maxidentity<=1e-9,maxidentity,'<=1e-9')
        modes.append(dict(ell=kval,domain='IN_HIGH_MODE_THEOREM' if kval>=emin else 'SEPARATE_FINITE_MODE_BOUND',max_actual_error=maxerror,upper_bound_endpoint_display=float(c2/kval**2) if kval>=emin else None,source_majorant_ratio=maxres,field_residual=maxfields,observable_residual=maxobs,residual_identity=maxidentity))
    checks.add('five_modes_four_original_columns',sorted(x['ell'] for x in modes)==list(old.MODES) and all(np.array(x['initial_balanced']).shape==(20,4,2) for x in ar['modes']))
    checks.add('positive_exact_interval_constants',all(x.is_Rational and x>=0 for x in (ko,kof,kw,kw4,kd1,kd2,co,cf,kr,kr4,kho,kho4)))
    checks.add('all_input_pins_after',common.inspect_pins(pins)==absent);checks.add('source_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(x['passed'] for x in checks.rows);ok=passed==len(checks.rows)
    constants={k:str(val) for k,val in dict(K_O=ko,K_Of=kof,K_W=kw,K_W_low=kw4,K_initial_fast=kd1,K_initial_remainder=kd2,C_other=co,C_fast=cf,K_source=kr,K_source_low=kr4,K_observation=kho,K_observation_low=kho4,kappa=kap,gamma=gamma).items()}
    formulas=dict(matrices=exported,domain=f'ell>={emin} high-mode theorem, with separate ell=4,8 bounds; rotating B1 J=1, 0<=t<=1/20',constants=constants,source_coefficient_bounds={str(j):str(val) for j,val in rn.items()},error_coefficient_exact=str(c2),error_coefficient_endpoint_display=float(c2),high_mode_inequality='||W_full(t)-Phi(t) W0||_infinity<=C2(t)*||W0||_infinity/ell^2',coefficient_definition='C2(t)=(3/2)[K_O{3 exp(30t)(C_other+2 K_W K_source t)+9 kappa t exp(gamma t) C_fast}+3 K_Of exp(30t) C_fast+K_observation exp(21t/10)]',proof='Use whole-interval residual/observable bounds and original mismatch decomposition. Parent uniform propagator bounds arbitrary retained response; parent fast-transfer lemma bounds the leading fast mismatch into other states. Actual fast observation is O(1/ell), and all remaining initial/forcing/normalization errors are O(1/ell^2). Convert 2-norm prepared-observable operator to infinity norm by sqrt(2)<=3/2.',sharp_order_proved=False,physical_window_proved=False)
    diagnostics=dict(modes=modes,upper_order=2,sharp_order='NOT_PROVED',finite_accuracy_usefulness='NOT_CLAIMED',initial_data_not_reprepared=True,complementary_probes_retained=True,precision='Exact SymPy and rational interval constants; binary64 archive controls, no new high-precision IVP')
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diagnostics)}
    summary=dict(schema='r4c1-g3n5-prepared-dust-error-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='PREPARED_DUST_UNIFORM_UPPER_BOUND_CHECKED_SHARPNESS_OPEN' if ok else 'PREPARED_DUST_UPPER_BOUND_NOT_VERIFIED',prepared_error_upper_bound_proved=ok,convergence_upper_order=2 if ok else 'NOT_PROVED',full_dust_convergence_order='SHARP_ORDER_NOT_PROVED',full_prepared_high_p_remainder_proved=False,analytic_dust_milestone='OPEN_SHARPNESS_AND_USEFULNESS',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',ordinary_wave_Jordan_defect_removed=False,complete_density_Hamiltonian_positive=False,physical_EFT_cutoff_derived=False,healthy_continuous_GR_verified=False,source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(val) for k,val in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'});bodies['summary.json']=common.encode(summary);return bodies,summary

def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_prepared_dust_error_attempt_01');ap.add_argument('--replay');ap.add_argument('--progress-file');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination missing')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing receipt directory')
    if args.progress_file and not args.replay:
        p=(ROOT/args.progress_file).resolve();p.relative_to((ROOT/'.local/itsm-context').resolve());PROGRESS=p.open('x',encoding='utf-8')
    try:bodies,summary=calculate()
    except BaseException:
        if PROGRESS is not None:traceback.print_exc(file=PROGRESS);PROGRESS.flush()
        raise
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'status':summary['status'],'physics_pass':False}))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    if PROGRESS is not None:PROGRESS.close()
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
