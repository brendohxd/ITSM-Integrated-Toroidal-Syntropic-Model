"""V3 mean-control/composite acceptance; reuse immutable V2 trajectories."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import scipy
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PARENT=BASE+'r4c1_three_family_time_response_attempt_02/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V3_MEAN_CONTROL_CONTRACT_2026-10-12.md'
PINNED={CONTRACT:'21123d8d2ad9e1c4390e2b23c6a1d8f5c63d18d25bc3bae06470c8af873ab6c0',
        PARENT+'summary.json':'32e55c59882515d00a604dc0eed5dae79b89961f7d8aee32846301c99dc4ab4d',
        PARENT+'trajectories.json':'8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d'}
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda v:(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
read=lambda n:json.loads((ROOT/n).read_bytes())


def calculate():
    for n,h in PINNED.items():
        if sha((ROOT/n).read_bytes())!=h:raise RuntimeError('Direct input drift: '+n)
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_three_family_time_response_v2 as original
    prior,entry,generic,pins,_,_=original.import_and_pin()
    old=read(PARENT+'summary.json');pins.update(PINNED);pins[SELF]=sha((ROOT/SELF).read_bytes())
    pins.update({PARENT+n:h for n,h in old['artifacts'].items()})
    paths=[];missing=[]
    for n,h in pins.items():
        p=ROOT/n
        if sha(p.read_bytes())!=h:raise RuntimeError('Inherited drift: '+n)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0]!=h:raise RuntimeError('Sidecar drift: '+n)
            paths.append(side)
        else:missing.append(n)
    before=entry.snapshot(paths);checks=prior.Checks()
    runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__)
    checks.add('actual_runtime_matches_original_trajectory_runtime',runtime==old['runtime'],runtime)
    bad=[r for r in old['checks'] if r['passed'] is not True]
    badnames={r['name'] for r in bad}
    checks.add('V2_failed_status_and_counts_preserved',old['validation']=='FAIL_LOCAL_CHECKS' and (old['passed'],old['total'])==(10395,10449))
    checks.add('exact_expected54_old_failure_classification',len(bad)==54 and all(r['passed'] is False and r['name'].endswith('_reject_omitted_mean_metric_coordinates') and r['evidence']<1e-12 for r in bad))
    checks.add('all_other10395_inherited_checks_remain_PASS',sum(r['passed'] is True for r in old['checks'])==10395 and all(r['passed'] is True for r in old['checks'] if r['name'] not in badnames))
    src=original.TimeSources(prior,generic,checks);red=original.EvolvingReduction(prior,generic)
    runs=read(PARENT+'trajectories.json')['runs'];rows=[];nullrows=[];replaced=set()
    idx=generic.IDX;columns=[idx[f] for f in ('Mxx','Mxy','Mxz','Myy','Myz','Mzz')];omitted=[idx[f] for f in ('Mxz','Myz','Mzz')]
    for run in runs:
        name,k,method=run['family'],run['k'],run['method'];p,_=entry.initial_conditions(generic,name,original.ETA)
        for ti,t in enumerate(original.TIMES):
            b=np.asarray(run['first_order_states'][ti]);context=src.context(name,b[:12],p,b[12],b[13],k)
            so=src.fourier(name,context)[0];d=red.at(b[:12],p,0,so[:22],so[22:])
            null=float(np.linalg.norm(d['EA'][:,columns],np.inf)/(1+np.linalg.norm(d['EA'],np.inf)))
            label=name+'_k'+str(k)+'_'+method+'_t'+str(ti)
            checks.add(label+'_all6_mean_position_null_columns_ON_SHELL',null<=1e-10,null)
            nullrows.append(dict(family=name,k=k,method=method,time=float(t),normalized_position_column_norm=null))
            if ti not in (0,10,20):continue
            n=len(d['dyn']);state=(np.arange(2*n)+1)*1e-4*(1+.37j)
            out=red.reconstruct(d,state,p,checks,label+'_unchanged_full_mean_trial')
            q,qd,qdd=(out[f].copy() for f in ('q','qd','qdd'))
            q[omitted]=0
            position_only=float(np.linalg.norm(d['EA']@q+d['EB']@qd+d['ED']@qdd+d['S'],np.inf)/out['scale'])
            oldname=label+'_reject_omitted_mean_metric_coordinates';replaced.add(oldname)
            oldrow=next(r for r in bad if r['name']==oldname)
            checks.add(label+'_original_position_only_failure_reproduced',position_only<1e-12 and abs(position_only-oldrow['evidence'])<=1e-12,dict(original=oldrow['evidence'],recomputed=position_only))
            qd[omitted]=0;qdd[omitted]=0
            proper=float(np.linalg.norm(d['EA']@q+d['EB']@qd+d['ED']@qdd+d['S'],np.inf)/out['scale'])
            checks.add(label+'_reject_ACTUAL_mean_field_truncation',proper>1e-12,proper)
            rows.append(dict(family=name,k=k,method=method,time=float(t),omitted_fields=['Mxz','Myz','Mzz'],
                             original_position_only_residual=position_only,proper_q_qdot_qddot_truncation_residual=proper,
                             full22_trial_residual=out['error'],original_normalization=out['scale'],negative_mean_kinetic_eigenvalues=np.linalg.eigvalsh(d['K']).tolist()))
    checks.add('every54_failed_control_addressed_EXACTLY_once',replaced==badnames and len(rows)==54)
    checks.add('all378_registered_mean_position_checks_retained',len(nullrows)==378)
    checks.add('original_sources_hash_size_mtime_preserved',entry.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(r['passed'] for r in checks.rows)
    scope=dict(numerical_trajectory_source=PARENT+'trajectories.json',original_trajectory_sha256=PINNED[PARENT+'trajectories.json'],
               numerical_values_changed=False,new_ODE_integrations=0,inherited_V2_validation='FAIL_LOCAL_CHECKS',inherited_passed=10395,inherited_total=10449,
               inherited54_failed_controls=bad,scope='composite finite-time perturbative acceptance; not a new trajectory, physical window, or continuous error certificate',
               homogeneous_metric_lemma='Constant positive spatial B in g_ij=a^2 B_ij gives another homogeneous local on-shell solution. Mean position-null columns do not remove velocity/acceleration dynamics; no global gauge/fixed-charge/physical-energy claim.')
    bodies={'mean_controls.json':encode(dict(corrected_omission_controls=rows,all_mean_position_null_controls=nullrows)), 'scope.json':encode(scope)}
    j=dict(schema='r4c1-three-family-time-response-acceptance-v3',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
           passed=passed,total=len(checks.rows),checks=checks.rows,
           status='CONDITIONAL_FINITE_TIME_RESPONSE_CHECKED_FULL_DOMAIN_OPEN' if passed==len(checks.rows) else 'MEAN_CONTROL_FAILURE_REQUIRES_DISPOSITION',
           inherited_V2_validation='FAIL_LOCAL_CHECKS',inherited_passed=10395,inherited_total=10449,
           preserved_original_trajectory_sha256=PINNED[PARENT+'trajectories.json'],new_ODE_integrations=0,
           physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',physical_go=False,
           stage2_complete=False,stage3_entered=False,physical_decision='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',
           full_second_order_response_solved=False,full_coupled_interactions_computed=False,certified_continuous_error=False,
           nonlinear_remainder_controlled=False,physical_EFT_cutoff_derived=False,
           canonical_tests_1_to_3='HOLD_SUBSTANTIVE',**{'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'},K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
           source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,
           substantive_unknowns=old['substantive_unknowns'],review_dependencies=['THREE-FAMILY-TIME-RESPONSE-V2/V3','all inherited deferred review'],
           artifacts={n:sha(b) for n,b in bodies.items()},runtime=runtime)
    bodies['summary.json']=encode(j)
    return bodies,j


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default=BASE+'r4c1_three_family_time_response_attempt_03');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay missing')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output')
    bodies,j=calculate()
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(sha(b)+'  '+n+'\n').encode():raise RuntimeError('Immutable replay mismatch: '+n)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for n,b in bodies.items():
            with (dest/n).open('xb') as stream:stream.write(b)
            with (dest/(n+'.sha256')).open('xb') as stream:stream.write((sha(b)+'  '+n+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=j['validation'],passed=j['passed'],total=j['total'],physics_pass=False,status=j['status'])))
    for r in j['checks']:
        if not r['passed']:print(json.dumps(r))
    return int(j['passed']!=j['total'])


if __name__=='__main__':raise SystemExit(main())
