"""Formal dust-observable correction; full forcing/remainder/order still open."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2];BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_OBSERVABLE_CORRECTION_CONTRACT_2026-10-11.md'
PARENT=BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_error_v1.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='1a9e162f5985c8f2a7ee00ffc6eea227106bcf49afb238fd7dbaa55202096748':raise RuntimeError('Frozen engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_prepared_dust_error_v1 as prior
old=prior.old;common=prior.common

def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()})
    pins[PARENT+'summary.json']='a637c7291ba1f3e1c1b3719f4c640de3b690c40bb0e9c6b38e7d9e37ab9f0e40'
    for rel in (CONTRACT,SELF):pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;eps=s.Symbol('eps',positive=True)
    on=lambda mat:mat.applyfunc(s.cancel)
    shell=lambda mat:mat.applyfunc(lambda val:bg.constraint_reduce_scalar(val) if val!=0 else s.Integer(0))
    exact=lambda name,mat:old.parent.exact(checks,name,on(mat) if isinstance(mat,s.MatrixBase) else s.cancel(mat))
    checks.add('parent_upper_not_sharp',ps['passed']==ps['total']==67 and ps['prepared_error_upper_bound_proved'] and not ps['full_prepared_high_p_remainder_proved'])
    raw=common.read_json(old.PARENT+'matrices.json')
    az,bi,obs,mm=[old.parent.import_matrix(raw[k],bg.sy) for k in ('balanced_generator','balancing_map_inverse','actual_dust_observable','leading_dust_generator')]
    uniform=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    maps=common.read_json(uniform['general_exact_maps_source'])['matrices']
    cm,tw,fw,lw=[old.parent.import_matrix(maps[k],bg.sy) for k in ('longitudinal_velocity_scaling_C','wave_map_Tw','dispersive_principal_F','ordinary_wave_principal_L')]
    ci=s.eye(20);ci[13,13]=a/ell
    ac=on((bg.dt(cm)+cm*az)*ci)
    blocks={}
    for i in range(20):
        for j in range(20):
            for term in s.Add.make_args(s.expand(ac[i,j])):
                power=term.as_powers_dict().get(ell,s.Integer(0));val=s.cancel(term/ell**power)
                if not power.is_Integer or ell in val.free_symbols:raise ValueError('Not Laurent')
                blocks.setdefault(int(power),s.zeros(20))[i,j]+=val
    exact('full_generator_Laurent_identity',ac-sum((mat*ell**d for d,mat in blocks.items()),s.zeros(20)))
    prepared=common.read_json(PARENT+'formulas.json')
    hs={j:old.parent.import_matrix(prepared['matrices']['comparison_lift_H'+str(j)],bg.sy) for j in range(4)}
    select=s.zeros(2,20);select[0,3]=select[1,13]=1
    left=select*tw;gslow=on(left*hs[0])
    exact('kernel_rows_F',select*fw);exact('kernel_rows_L',select*lw)
    exact('leading_lift_principal_F',fw*tw*hs[0]);exact('leading_lift_principal_L',lw*tw*hs[0])
    exact('slow_chart_determinant',gslow.det()-6*rho)
    boxes={bg.sy[k]:(s.sympify(val[0]),s.sympify(val[1])) for k,val in uniform['background_boxes'].items()}
    checks.add('rho_inverse_domain',boxes[rho][0]>0 and gslow.det()==6*rho)
    r2=on(sum((left*mat*hs[d+2] for d,mat in blocks.items() if d+2 in hs),s.zeros(2))-left*bg.dt(hs[2])-left*hs[2]*mm)
    n2=shell(on(gslow.inv()*r2))
    exact('projected_order_two_solvability',shell(r2-gslow*n2))
    oc=on(on(obs*bi*ci).subs(ell,1/eps))
    oco={j:oc.applyfunc(lambda val:s.diff(val,eps,j).subs(eps,0)/s.factorial(j)) for j in range(3)}
    exact('observation_order_zero',shell(oco[0]*hs[0]-s.eye(2)))
    exact('observation_order_one',shell(oco[0]*hs[1]+oco[1]*hs[0]))
    j2=shell(on(sum((oco[j]*hs[2-j] for j in range(3)),s.zeros(2))))
    jd=on(bg.dt(j2));neff=shell(on(n2+jd+j2*mm-mm*j2))
    exact('normalized_observation_order_two',shell(oco[0]*(hs[2]-hs[0]*j2)+oco[1]*hs[1]+oco[2]*hs[0]))
    exact('normalized_projected_solvability',shell(r2+gslow*(-mm*j2+j2*mm+jd-neff)))
    z=s.Matrix(2,2,lambda i,j:s.Symbol(f'Z{i}{j}',real=True))
    zd=s.Matrix(2,2,lambda i,j:s.Symbol(f'Zdot{i}{j}',real=True))
    nchange=n2+mm*z-z*mm-zd;jchange=j2+z
    exact('auxiliary_chart_invariant_observable',shell(on(nchange+jd+zd+jchange*mm-mm*jchange-neff)))
    checks.add('omitted_normalization_drift_rejected',any(val!=0 for val in jd))
    checks.add('omitted_normalization_changes_coefficient',any(val!=0 for val in on(neff-n2)))
    initial={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    exact('registered_Friedmann_shell',bg.constraint.subs(initial))
    exact('registered_angular_charge',(a**3*(u*vd-v*ud)).subs(initial)-1)
    checks.add('formal_coefficient_nonzero',any(val!=0 for val in neff))
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    fn=s.lambdify([bg.bg],(j2,n2,mm,neff),'numpy',cse=True)
    def at(t):return [np.asarray(val,complex) for val in fn(np.polynomial.polynomial.polyval(t,bc.T))]
    step=1e-5;controls=[]
    for t in (0.,.025,.05):
        jj,nn,mn,nobs=at(t)
        if t==0:drift=(-3*jj+4*at(t+step)[0]-at(t+2*step)[0])/(2*step)
        elif t==.05:drift=(3*jj-4*at(t-step)[0]+at(t-2*step)[0])/(2*step)
        else:drift=(at(t+step)[0]-at(t-step)[0])/(2*step)
        direct=nn+drift+jj@mn-mn@jj
        error=float(np.linalg.norm(direct-nobs,np.inf));limit=1e-7+1e-6*max(1.,float(np.linalg.norm(nobs,np.inf)))
        checks.add('independent_time_derivative_'+str(t),error<=limit,error,'1e-6 relative plus 1e-7 absolute')
        controls.append(dict(t=t,error=error,allowance=limit))
    exported={name:prior.wire(mat) for name,mat in dict(slow_chart_G=gslow,lift_correction_N2=n2,observation_J2=j2,observable_correction_N2=neff,observable_N2_initial=on(neff.subs(initial))).items()}
    for name,obj in exported.items():exact('roundtrip_'+name,old.parent.import_matrix(obj,bg.sy)-dict(slow_chart_G=gslow,lift_correction_N2=n2,observation_J2=j2,observable_correction_N2=neff,observable_N2_initial=on(neff.subs(initial)))[name])
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    formulas=dict(matrices=exported,definition='N_obs=N2+J2_dot+[J2,M], multiplying coordinate ell^-2, not physical p^-2 without a^2 conversion',domain='Formal high-ell coefficient on rotating B1 J=1, preserved Friedmann shell, a,C,rho_m>0; frozen short-time background [0,1/20]',rho_inverse_lower=str(boxes[rho][0]),source_terms='R2 retains complete Laurent generator, evolving H2, M and H3; only principal-kernel compatibility projected for coefficient derivation',auxiliary_chart_invariance='H->H(I+ell^-2 Z): N2->N2+[M,Z]-Zdot, J2->J2+Z, N_obs unchanged',nonclaims=['No closed projected dust evolution','Full retained fast/wave forcing and original mismatch remain','No controlled corrected-system remainder or sharp-order theorem','No physical window, healthy GR, microscopic matching or numerical acceleration prediction'])
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(dict(time_derivative_controls=controls,original_data_not_changed=True,formal_only=True))}
    summary=dict(schema='r4c1-g3n5-observable-correction-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='FORMAL_OBSERVABLE_CORRECTION_CHECKED_REMAINDER_OPEN' if ok else 'FORMAL_OBSERVABLE_CORRECTION_NOT_VERIFIED',formal_observable_correction_checked=ok,corrected_system_remainder_proved=False,full_dust_convergence_order='SHARP_ORDER_NOT_PROVED',full_prepared_high_p_remainder_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(val) for k,val in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'});bodies['summary.json']=common.encode(summary)
    return bodies,summary

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_observable_correction_attempt_01');ap.add_argument('--replay');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    bodies,summary=calculate()
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
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
