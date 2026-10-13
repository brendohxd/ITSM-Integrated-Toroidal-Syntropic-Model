"""Normalized-reference error component; full finite-mode dust bound pending."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_NORMALIZED_REFERENCE_CONTRACT_2026-10-12.md'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_dust_actual_order_v3.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='7d7da3e67e5a24736baea8956c6ca717a3d52ebcb50b521d50543c8a50cad5ab':
    raise RuntimeError('Frozen V3 drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_actual_order_v3 as library
old,prior,common,engine=library.old,library.prior,library.common,library.engine
PROGRESS=None


def progress(message):
    print(message,flush=True)
    if PROGRESS is not None:
        PROGRESS.write(message+'\n');PROGRESS.flush()


def calculate():
    parent=BASE+'r4c1_g3n5_dust_actual_order_attempt_03/'
    expected='7f0888a9096145c42257bcccf84b8e7fdc3d98a1f10e05bbfd4f68a00dcf5c60'
    if common.sha((ROOT/(parent+'summary.json')).read_bytes())!=expected:
        raise RuntimeError('V3 receipt drift')
    ps=common.read_json(parent+'summary.json')
    pins=dict(ps['source_sha256'])
    pins.update({parent+name:digest for name,digest in ps['artifacts'].items()})
    pins[parent+'summary.json']=expected
    for rel in (SELF,CONTRACT,ENGINE,
                'Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_energy_v1.py',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_ENERGY_CONTRACT_2026-10-12.md'):
        pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/name for name in pins]
    paths.extend(Path(str(path)+'.sha256') for path in list(paths) if Path(str(path)+'.sha256').exists())
    before=old.parent.snapshot(paths)
    checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell
    eps=s.Symbol('eps',positive=True)
    on=lambda mat:mat.applyfunc(s.cancel)
    shell=lambda mat:mat.applyfunc(lambda value:bg.constraint_reduce_scalar(value) if value!=0 else s.Integer(0))
    exact=lambda name,mat:old.parent.exact(checks,name,on(mat))
    progress('Pinned inputs inspected; starting independent reference-component algebra')
    checks.add('V3_is_scoped_not_full_dust_closure',ps['passed']==ps['total']==72 and not ps['physics_pass'] and not ps['full_dust_milestone_complete'])
    generic=lambda label:s.Matrix(2,2,lambda i,j:s.Symbol(f'{label}_{i}_{j}'))
    gj,gjd,gm,gmc,gphi=[generic(label) for label in ('J','Jdot','M','Mc','Phi')]
    gs=gjd+gj*gmc-gm*gj
    exact('generic_positive_normalized_forcing_identity',(gjd+gj*gmc)*gphi-gm*gj*gphi-gs*gphi)
    checks.add('generic_Jdot_omission_rejected',any(value!=0 for value in gjd*gphi))
    raw=common.read_json(old.PARENT+'matrices.json')
    obs,bi,M=[old.parent.import_matrix(raw[name],bg.sy) for name in ('actual_dust_observable','balancing_map_inverse','leading_dust_generator')]
    Ci=s.eye(20);Ci[13,13]=a/ell
    Oc=on(obs*bi*Ci)
    prep=common.read_json(BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json')
    corrected=common.read_json(BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_04/formulas.json')
    hs={power:old.parent.import_matrix(prep['matrices']['comparison_lift_H'+str(power)],bg.sy) for power in range(4)}
    q3,h4,N2=[old.parent.import_matrix(corrected['matrices'][name],bg.sy) for name in ('wave_addition_q3','fast_addition_H4','lift_generator_N2')]
    hc={**hs,3:hs[3]+q3,4:h4}
    Hc=sum((mat/ell**power for power,mat in hc.items()),s.zeros(20,2))
    Mc=M+N2/ell**2
    J=on(Oc*Hc)
    Jdot=bg.dt(J)
    Sref=on(Jdot+J*Mc-M*J)
    exact('actual_product_rule_drift',Jdot-bg.dt(Oc)*Hc-Oc*bg.dt(Hc))
    checks.add('actual_Jdot_omission_rejected',any(value!=0 for value in Jdot))
    formal=common.read_json(BASE+'r4c1_g3n5_observable_correction_attempt_01/formulas.json')
    Nobs=old.parent.import_matrix(formal['matrices']['observable_correction_N2'],bg.sy)
    se=Sref.subs(ell,1/eps)
    for power in (0,1):
        coefficient=se.applyfunc(lambda value:s.Poly(value,eps).nth(power))
        exact('no_reference_source_order_'+str(power),shell(coefficient))
    coefficient2=se.applyfunc(lambda value:s.Poly(value,eps).nth(2))
    exact('same_complete_observable_N2',shell(coefficient2-Nobs))
    progress('Exact normalized-reference identity, drift and observable N2 verified')
    un=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    boxes={bg.sy[name]:tuple(s.Rational(value) for value in bounds) for name,bounds in un['background_boxes'].items()}
    box=engine.EnclosureBox(boxes);constbox=engine.EnclosureBox({})
    mu=s.Rational(21,10);T=s.Rational(1,20)
    norm=lambda mat:max(box.norm(mat),box.norm(mat.T))
    checks.add('leading_reference_rate',norm(M)<=mu)
    nn=norm(on(N2))
    init={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    numeric=s.lambdify([bg.bg,ell],(Oc,bg.dt(Oc),Hc,bg.dt(Hc),M,Mc,Sref),'mpmath',cse=True)
    energy_numeric=s.lambdify([bg.bg],bg.energy,'mpmath',cse=True)
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    rows,controls=[],[]
    for kval in old.MODES:
        j0=on(J.subs(init).subs(ell,kval))
        checks.add('reference_initial_inverse_'+str(kval),j0.det()!=0)
        if j0.det()==0:raise RuntimeError('Singular reference initial chart')
        ji=on(j0.inv())
        exact('reference_initial_identity_'+str(kval),j0*ji-s.eye(2))
        inverse_bound=constbox.norm(ji)
        ks=box.norm(on(Sref.subs(ell,kval)))
        rate=mu+nn/kval**2
        bound=ks*inverse_bound*T*s.exp(max(mu,rate)*T)
        checks.add('exact_positive_component_constants_'+str(kval),all(value.is_Rational and value>=0 for value in (inverse_bound,ks,rate)))
        with mp.workdps(70):
            nrm=lambda mat:max(sum(abs(mat[i,j]) for j in range(mat.cols)) for i in range(mat.rows))
            for t in (0.,.025,.05):
                point=[mp.mpf(str(value)) for value in np.polynomial.polynomial.polyval(t,bc.T)]
                point[1]=mp.sqrt(mp.mpf(10)*energy_numeric(point)/33)
                oc,ocd,hh,hd,mm,mc,src=numeric(point,kval)
                direct=ocd*hh+oc*hd+(oc*hh)*mc-mm*(oc*hh)
                residual=float(nrm(direct-src)/max(mp.mpf(1),nrm(src)))
                checks.add('independent_reference_chain_rule_'+str(kval)+'_'+str(t),residual<=1e-30,residual,'<=1e-30; 70-digit algebraic shell')
                controls.append(dict(ell=kval,time=t,residual=residual,precision=70))
        rows.append(dict(ell=kval,K_source=str(ks),K_J0_inverse=str(inverse_bound),leading_rate=str(mu),reference_rate=str(rate),endpoint_bound=str(bound),endpoint_display=float(bound)))
        progress('Normalized-reference component completed for original ell='+str(kval))
    archive=common.read_json(old.PARENT+'trajectories.json')
    checks.add('all_five_original_modes_four_columns_preserved',sorted(item['ell'] for item in archive['modes'])==list(old.MODES) and all(np.array(item['initial_balanced']).shape==(20,4,2) for item in archive['modes']))
    checks.add('input_pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    formulas=dict(matrices={'complete_normalized_reference_source':prior.wire(Sref)},modes=rows,domain='Registered rotating linear B1 prepared family; original ell=4,8,16,32,64; 0<=t<=1/20; full corrected lift/normalization on the preserved background shell',inequality='||W_ref-Phi_M W0||_infinity<=K_source K_J0_inverse t exp(max(mu,lambda)t)||W0||_infinity',proof='Exact normalized positive-forcing identity and initial W_ref(0)=W0; whole-background interval source/rate constants; variation of constants. No inverse of J(t), omitted drift or state projection.',scope='REFERENCE COMPONENT ONLY; full retained-response/forcing error, useful finite-band accuracy and physical domain are not proved here',full_finite_mode_bound_proved=False,physical_window_proved=False)
    diagnostics=dict(independent_reference_controls=controls,raw_maximum_residual=max(item['residual'] for item in controls),new_trajectory_runs=0,original_archive_preserved=True,pending_full_state_calculation='finite_energy_v1; component does not depend on its unfinished output')
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diagnostics)}
    summary=dict(schema='r4c1-g3n5-normalized-reference-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='REFERENCE_COMPONENT_CHECKED_FULL_ERROR_PENDING' if ok else 'REFERENCE_COMPONENT_NOT_VERIFIED',normalized_reference_bound_proved=ok,full_finite_mode_bound_proved=False,full_dust_milestone_complete=False,useful_finite_mode_accuracy_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={name:common.sha(body) for name,body in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,mpmath=mp.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_normalized_reference_attempt_01')
    ap.add_argument('--replay');ap.add_argument('--progress-file')
    args=ap.parse_args();dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.progress_file and not args.replay:
        path=(ROOT/args.progress_file).resolve();path.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS=path.open('x',encoding='utf-8')
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
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=summary['validation'],passed=summary['passed'],total=summary['total'],status=summary['status'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    if PROGRESS is not None:PROGRESS.close()
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
