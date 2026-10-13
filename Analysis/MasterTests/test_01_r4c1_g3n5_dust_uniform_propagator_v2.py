"""Uniform propagator on the actual rotating B1 background; remainder open."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PARENT=BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_01/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_dust_remainder_v6.py'
ENGINE_SHA='efef4d8cc501fbbf7f62f2c9e60d12a5dceab8c24f0caaa73b3136e952eba913'
CONTROL='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_V2_CONTROLS_2026-10-11.md'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!=ENGINE_SHA:raise RuntimeError('Frozen source drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_remainder_v6 as old
common=old.common

def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()})
    pins[PARENT+'summary.json']='0d280bcdd436535e62dd56d509c23bda1de44536b178ecfa130d096a47e6b039'
    pins[CONTROL]=common.sha((ROOT/CONTROL).read_bytes());pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks()
    failed=[row for row in ps['checks'] if not row['passed']]
    checks.add('failed_v1_retained_not_accepted',ps['validation']=='FAIL_LOCAL_CHECKS' and len(failed)==5 and all(row['name'].startswith('background_box_sanity_') for row in failed),failed)
    bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell
    on=lambda m:m.applyfunc(s.cancel)
    exact=lambda name,m:old.parent.exact(checks,name,on(m) if isinstance(m,s.MatrixBase) else s.cancel(m))
    wire=common.read_json(PARENT+'formulas.json')
    maps={k:old.parent.import_matrix(val,bg.sy) for k,val in wire['matrices'].items()}
    c,uf,tw,ti,q,fw,lw,drift=[maps[k] for k in ('longitudinal_velocity_scaling_C','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi','positive_evolution_Q','dispersive_principal_F','ordinary_wave_principal_L','wave_drift')]
    vs=[maps['residual_numerator_'+str(k)] for k in range(6)]
    ci=s.eye(20);ci[13,13]=a/ell
    raw=common.read_json(old.PARENT+'matrices.json');az=old.parent.import_matrix(raw['balanced_generator'],bg.sy)
    ac=on((bg.dt(c)+c*az)*ci);tf=s.eye(20)+uf/ell;g=-22*a*a/375
    invnum=(1-g/ell**2)*s.eye(20)-uf/ell+uf**2/ell**2
    exact('mixed_scaling_inverse',c*ci-s.eye(20))
    exact('wave_inverse',tw*ti-s.eye(20));exact('fast_cubic_identity',uf**3-g*uf)
    exact('fast_inverse',tf*invnum-(1-g/ell**2)*s.eye(20))
    # Revalidate the complete unspecialized generator, independent of v1 counts.
    lhs=tw*invnum*(ac*tf-bg.dt(tf))*ti
    rhs=(1-g/ell**2)*(ell**2*fw+ell*lw)+sum((vs[k]/ell**k for k in range(6)),s.zeros(20))
    exact('complete_transformed_generator_unspecialized',lhs-rhs)
    exact('wave_coordinate_drift',drift*tw-bg.dt(tw))
    exact('dispersive_Q_skew',q*fw+fw.conjugate().T*q)
    exact('wave_Q_skew',q*lw+lw.conjugate().T*q)
    d=s.eye(20);d[0,0]=s.Rational(1,3);d[4,4]=d[5,5]=s.Rational(4,5);d[9,9]=s.Rational(5,33)
    rank=s.zeros(20);rank[6:8,6:8]=s.Matrix([v,-u])*s.Matrix([[v,-u]])/13
    exact('Q_fixed_positive_lower_metric',q-d-rank)
    checks.add('lower_metric_positive',min(d.diagonal())==s.Rational(5,33))
    exact('angular_charge_preserved',bg.dt(s.Matrix([a**3*(u*vd-v*ud)])))
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    initial={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    for ix,sym in enumerate(bg.bg):
        saved=s.Rational(coeff['background_coefficients'][ix][0][0]);target=initial[sym]
        checks.add('registered_initial_'+str(sym),bool(abs(s.N(saved-target,75))<s.Rational(1,10)**60))
    exact('initial_energy',bg.energy.subs(initial)-s.Rational(3469,1400));exact('initial_Friedmann',bg.constraint.subs(initial))
    exact('initial_angular_charge_one',(a**3*(u*vd-v*ud)).subs(initial)-1)
    T=s.Rational(1,20);rmax=1+T/4;smax=1+T*T
    force=1+smax/6+smax*smax/80+3*rmax*rmax/14
    fr=rmax*(2+rmax*rmax/7+3*smax/14)
    vmin=1-(3+T*force)*T;rmin=s.Rational(1,4)-(s.Rational(3,4)+fr)*T
    checks.add('positive_velocity_bootstrap',vmin>0 and rmin>0 and 1-force*T*T/2>0,{'v_dot_min':str(vmin),'r_dot_min':str(rmin)})
    exact('u_force_identity',-bg.rates[3]-3*H*ud-u*(1+(u*u+v*v)/6+(u*u+v*v)**2/80+3*r*r/14))
    exact('v_force_identity',-bg.rates[5]-3*H*vd-v*(1+(u*u+v*v)/6+(u*u+v*v)**2/80+3*r*r/14))
    exact('r_force_identity',-bg.rates[7]-3*H*rd-r*(2+r*r/7+3*(u*u+v*v)/14))
    boxes={a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(3,4),s.Integer(1)),u:(1-force*T*T/2,s.Integer(1)),v:(s.Integer(0),T),r:(s.Integer(1),rmax),ud:(-force*T,s.Integer(0)),vd:(vmin,s.Integer(1)),rd:(rmin,s.Rational(1,4)),pd:(s.Rational(1,6),s.Rational(1,5)),rho:(s.Rational(17,100),s.Rational(1,5)),C:(s.Integer(1),s.Rational(250,249))}
    bx=old.RationalBox(boxes)
    scale=lambda m:s.Matrix(20,20,lambda i,j:s.cancel(m[i,j]/s.sqrt(d[i,i]*d[j,j])))
    sd=scale(bg.dt(q)+q*drift+drift.conjugate().T*q)
    hjs=[scale(q*m+m.conjugate().T*q) for m in vs]
    rows=[]
    for i in range(20):
        upper=bx.evaluate(sd[i,i])[1]+sum(bx.absolute(sd[i,j]) for j in range(20) if j!=i)
        upper+=sum(sum(bx.absolute(h[i,j]) for j in range(20))/s.Integer(4)**k for k,h in enumerate(hjs))
        rows.append(s.cancel(upper))
    mu=max(s.Integer(0),max(rows));checks.add('all_energy_rows_exact_rational',all(x.is_Rational for x in rows))
    print('Certified rotating-background energy derivative display',float(mu),flush=True)
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']]);ar=common.read_json(old.PARENT+'trajectories.json')
    fn=s.lambdify([bg.bg,ell],(c,ci,bg.dt(c),az,uf,bg.dt(uf),tw,ti,bg.dt(tw),q,fw,lw,drift,*vs),'numpy',cse=True)
    qraw=old.parent.import_matrix(raw['full_field_reconstruction'],bg.sy);biraw=old.parent.import_matrix(raw['balancing_map_inverse'],bg.sy)
    fieldfn=s.lambdify([bg.bg,ell],qraw*biraw,'numpy',cse=True);modes=[]
    for item in ar['modes']:
        kval=item['ell'];maxamp=maxinverse=maxgen=maxbox=maxfield=maxconj=0.;energy0=None
        for ix,t in enumerate(ar['time']):
            bval=np.polynomial.polynomial.polyval(t,bc.T);vals=[np.asarray(m,complex) for m in fn(bval,kval)]
            cn,cin,cd,azn,un,udn,twn,tin,twd,qn,fwn,lwn,dn=vals[:13];nn=vals[13:]
            den=1+22*bval[0]**2/(375*kval**2);tfn=np.eye(20)+un/kval;tfin=np.eye(20)-un/(kval*den)+un@un/(kval*kval*den)
            rawz=np.array(item['balanced'][ix]);z=rawz[...,0]+1j*rawz[...,1];w=twn@tfin@cn@z
            energy=np.real(np.sum(w.conjugate()*(qn@w),axis=0))
            if energy0 is None:energy0=energy
            maxamp=max(maxamp,float(np.max(np.sqrt(energy/energy0)/np.exp(float(mu)*t/2))))
            maxinverse=max(maxinverse,float(np.linalg.norm(cin@tfn@tin@w-z,np.inf)/max(1.,np.linalg.norm(z,np.inf))))
            cw=w.conjugate();eneg=np.real(np.sum(cw.conjugate()*(qn.conjugate()@cw),axis=0))
            maxconj=max(maxconj,float(np.max(abs(energy-eneg))/max(1.,np.max(abs(energy)))))
            af=np.array(item['full_fields'][ix]);af=af[...,0]+1j*af[...,1]
            maxfield=max(maxfield,float(np.linalg.norm(np.asarray(fieldfn(bval,kval),complex)@z-af,np.inf)/max(1.,np.linalg.norm(af,np.inf))))
            for sym,value in zip(bg.bg,bval):
                lo,hi=boxes[sym];maxbox=max(maxbox,max(float(lo)-value,value-float(hi),0.))
            if ix in (0,len(ar['time'])//2,len(ar['time'])-1):
                acn=(cd+cn@azn)@cin;afast=tfin@(acn@tfn-udn/kval);direct=(twd+twn@afast)@tin
                factored=kval*kval*fwn+kval*lwn+dn+sum((nn[k]/kval**k for k in range(6)),np.zeros((20,20),complex))/den
                maxgen=max(maxgen,float(np.linalg.norm(direct-factored,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
        for name,value,limit in (('archive_Q_bound',maxamp,1+1e-9),('inverse_reconstruction',maxinverse,1e-9),('numeric_generator_identity',maxgen,1e-9),('background_box_sanity',maxbox,1e-10),('all_22_fields_unchanged',maxfield,1e-10),('negative_conjugate_norm',maxconj,1e-9)):
            checks.add(name+'_'+str(kval),bool(value<=limit),value,'<='+str(limit))
        modes.append(dict(ell=kval,normalized_Q_bound_ratio=maxamp,inverse_residual=maxinverse,generator_residual=maxgen,field_residual=maxfield,box_violation=maxbox))
    checks.add('five_modes_four_columns_retained',sorted(m['ell'] for m in modes)==list(old.MODES) and all(np.array(m['initial_balanced']).shape==(20,4,2) for m in ar['modes']))
    checks.add('all_complex_directions_retained',az.shape==(20,20) and qraw.shape==(22,20) and q[6,7]!=0)
    checks.add('coordinate_and_momentum_drifts_retained',bg.dt(c)[13,13]!=0 and any(x!=0 for x in bg.dt(uf)) and any(x!=0 for x in bg.dt(tw)))
    checks.add('all_input_pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    formulas=dict(general_exact_maps_source=PARENT+'formulas.json',general_exact_maps_sha256=ps['artifacts']['formulas.json'],full_generator_revalidated=True,coordinate_definition='w=Tw (I+U/ell)^(-1) C z, z=B x',domain='ell>=4; 0<=s<=t<=1/20; registered rotating B1 background J=1, positive a,C,rho; all 20 complex first-order states and 22 reconstructed fields',norm='sqrt(w^dagger Q(t) w)',inequality='||w(t)||_Q(t)<=exp(mu*(t-s)/2)||w(s)||_Q(s)',proof='Exact principal Q-skew identities; Q>=D>0. Rational interval/Gershgorin bounds on D^(-1/2)(Q_dot+Q residual+residual^dagger Q)D^(-1/2) give E_dot<=mu*||w||_D^2<=mu*E for mu>=0.',lower_metric_diagonal=[str(x) for x in d.diagonal()],background_boxes={str(k):[str(x) for x in val] for k,val in boxes.items()},force_bounds={'u_v_coefficient':str(force),'r_force':str(fr)},energy_row_constants=[str(x) for x in rows],mu_exact=str(mu),mu_display=float(mu),endpoint_amplification_display=float(s.exp(mu*T/2)),rejected_v1_bound_display=2.798753391173326)
    proof_ok=all(row['passed'] for row in checks.rows)
    diag=dict(modes=modes,uniform_full_linear_propagator_proved=proof_ok,full_prepared_high_p_remainder_proved=False,full_dust_convergence_order='NOT_PROVED',failed_v1_checks=failed,remaining='Control the actual dust observable error, retained fast forcing and initial mismatch; uniform full-state evolution alone does not prove its order.',precision='Exact algebra/rational outward intervals; binary64 archive controls; no new high-precision IVP or physical EFT statement')
    payloads={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag)};passed=sum(row['passed'] for row in checks.rows)
    summary=dict(schema='r4c1-g3n5-dust-uniform-propagator-v2',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='ROTATING_B1_UNIFORM_PROPAGATOR_CHECKED_PREPARED_REMAINDER_OPEN',uniform_full_linear_propagator_proved=True,full_prepared_high_p_remainder_proved=False,full_dust_convergence_order='NOT_PROVED',analytic_dust_milestone='OPEN_PREPARED_REMAINDER',rejected_v1='FAILED 67/72; invalid zero-v_dot/zero-r_dot enclosure; affirmative proof flag not valid for registered trajectory; original files retained.',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',original_slow_time_coefficient='-11/6',ordinary_wave_Jordan_defect_removed=False,complete_density_Hamiltonian_positive=False,physical_EFT_cutoff_derived=False,healthy_continuous_GR_verified=False,source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(b) for k,b in payloads.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),review_dependencies=['R9-MT1-G3N5-DUST-REMAINDER','G3N5 finite-mode/weighted/nonzero and B1G'])
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED','uniform_full_linear_propagator_proved':proof_ok})
    if not proof_ok:summary['status']='ROTATING_B1_UNIFORM_PROPAGATOR_NOT_VERIFIED'
    payloads['summary.json']=common.encode(summary)
    return payloads,summary

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02');ap.add_argument('--replay');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination missing')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing receipt directory')
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
