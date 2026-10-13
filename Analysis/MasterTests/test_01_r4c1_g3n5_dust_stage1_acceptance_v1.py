"""Original-scope Stage-1 consolidation and exact prepared-data bridge."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,sys
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_STAGE1_ACCEPTANCE_V1_CONTRACT_2026-10-12.md'
PARENT=BASE+'r4c1_g3n5_dust_seed_enclosure_attempt_01/'
EXPECTED='85ed17c65f0c53c6b01762ec224188be67c85d3ba3e8e725057d233c4d6526ff'
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_certified_numerical_v1 as numerical
old=numerical.old;common=numerical.common


def calculate():
    if common.sha((ROOT/(PARENT+'summary.json')).read_bytes())!=EXPECTED:raise RuntimeError('Frozen final seed receipt drift')
    ps=common.read_json(PARENT+'summary.json')
    pins=dict(ps['source_sha256']);pins[PARENT+'summary.json']=EXPECTED
    pins.update({PARENT+name:value for name,value in ps['artifacts'].items()})
    for rel in (SELF,CONTRACT,'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_REMAINDER_REPORT_2026-10-11.md',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_REFERENCE_REMAINDER_REPORT_2026-10-12.md',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_CERTIFIED_NUMERICAL_REPORT_2026-10-12.md'):
        pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/rel for rel in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks()
    packs={}
    for label,name,count in (
        ('split','r4c1_g3n5_dust_remainder_attempt_01',78),
        ('correction','r4c1_g3n5_corrected_dust_remainder_attempt_04',100),
        ('order','r4c1_g3n5_dust_actual_order_attempt_03',72),
        ('energy','r4c1_g3n5_dust_finite_energy_attempt_04',89),
        ('numerical','r4c1_g3n5_dust_certified_numerical_attempt_01',85),
        ('independent','r4c1_g3n5_dust_certificate_controls_attempt_01',97),
        ('stored','r4c1_g3n5_dust_seed_enclosure_attempt_01',34)):
        q=common.read_json(BASE+name+'/summary.json');packs[label]=q
        checks.add('all_'+label+'_checks_inspected',q['passed']==q['total']==len(q['checks'])==count and all(row['passed'] is True for row in q['checks']))
        checks.add('unpromoted_'+label,q['physics_pass'] is False and q['gate_effect']=='NONE' and q['Rule9_cleared'] is False and q['review_status']=='DEFERRED')
    names=lambda key:{row['name'] for row in packs[key]['checks'] if row['passed'] is True}
    checks.add('moving_basis_and_momentum_not_omitted',{'physical_momentum_drift','omitting_physical_momentum_drift_rejected'}<=names('split') and 'omitted_correction_drift_rejected' in names('correction') and 'omitted_transform_drift_rejected' in names('order'))
    checks.add('positive_forcing_full_initial_response',packs['correction']['corrected_reference_forced_remainder_proved'] and packs['correction']['retained_original_response'] and packs['correction']['controlled_remainder_upper_order']==3 and 'positive_forcing_matrix_decomposition' in names('correction'))
    checks.add('derived_sharp_order_not_sampled_slope',packs['order']['complete_original_error_expansion_proved'] and packs['order']['full_retained_response_bound_proved'] and packs['order']['mathematical_asymptotic_order']==2 and {'total_cubic_order_rejected_by_nonzero_second_coefficient','explicit_total_order_two_lower_domain'}<=names('order'))
    checks.add('complete_finite_energy_budget_retained',packs['energy']['finite_mode_error_bounds_proved'] and not packs['energy']['useful_finite_mode_accuracy_proved'])
    checks.add('useful_continuous_band_and_stored_inputs',packs['numerical']['continuous_finite_mode_numerical_accuracy_proved'] and packs['numerical']['useful_finite_mode_accuracy_proved'] and packs['stored']['original_stored_seed_accuracy_proved'])
    # Exact bridge between independently exported preparations. Constants are
    # substituted BEFORE the small adjugate/inverse, avoiding a new dense general
    # background calculation. Positive ell remains symbolic.
    bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell
    initial={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    mats={name:old.parent.import_matrix(obj,bg.sy).subs(initial) for name,obj in common.read_json(old.PARENT+'matrices.json').items()}
    prep=common.read_json(BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json')
    eps=s.Symbol('eps',positive=True);sy={**bg.sy,'eps':eps}
    hs={j:old.parent.import_matrix(prep['matrices']['comparison_lift_H'+str(j)],sy).subs(initial) for j in range(4)}
    d1=old.parent.import_matrix(prep['matrices']['initial_fast_mismatch'],sy).subs(initial)
    d2=old.parent.import_matrix(prep['matrices']['initial_remainder'],sy).subs(initial).subs(eps,1/ell)
    eorig=sum((mat/ell**j for j,mat in hs.items()),s.zeros(20,2))+d1/ell+d2/ell**2
    normalization=(mats['actual_dust_observable']*mats['formal_slow_lift']).applyfunc(s.cancel)
    cm=s.eye(20);cm[13,13]=ell
    raw=cm*mats['balancing_map']*mats['formal_slow_lift']*normalization.inv()
    bridge=(eorig-raw).applyfunc(s.cancel)
    for col in range(2):checks.add('exact_original_prepared_bridge_'+str(col),all(value==0 for value in bridge[:,col]),dict(nonzero_entries=sum(value!=0 for value in bridge[:,col])), 'ALL 20 entries; symbolic positive ell, same exact initial background')
    cert=common.read_json(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json')
    seed=common.read_json(PARENT+'seed_enclosures.json')
    checks.add('same_registered_domain_and_complete_columns',len(cert['modes'])==5 and [r['ell'] for r in cert['modes']]==[4,8,16,32,64] and sum(r['steps'] for r in cert['modes'])==416 and cert['no_projection_during_evolution'] is True and all(len(r['final_state'])==20 and all(len(x)==4 for x in r['final_state']) for r in cert['modes']))
    for row in seed['modes']:
        checks.add('both_original_seed_representations_'+str(row['ell']),[r['representation'] for r in row['representations']]==['exact_JSON_decimal','original_binary64'] and all(max(F(r['dust_numerical_error_upper']),F(r['field_numerical_error_upper']))<=F(1,10**8) and F(r['prepared_model_error_upper'])<=F(1,100) for r in row['representations']))
    archive=common.read_json(old.PARENT+'trajectories.json')
    checks.add('nonmonotonic_original_probes_not_replaced',len(archive['modes'])==5 and all(len(row['initial_balanced'])==20 and all(len(x)==4 for x in row['initial_balanced']) for row in archive['modes']) and old.PARENT+'trajectories.json' in pins)
    checks.add('source_pins_after',common.inspect_pins(pins)==absent)
    checks.add('source_size_mtime_hash_preserved',old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    coverage=dict(exact_moving_split='split',finite_k_correction_and_positive_retained_forcing='correction',controlled_asymptotic_remainder_and_sharp_order='order',complete_finite_mode_budget='energy',continuous_useful_band_error='numerical',independent_stepper_rational_controls='independent',both_original_stored_seed_representations='stored',exact_initial_data_bridge='new symbolic identity')
    bodies={'acceptance.json':common.encode(dict(requirements=coverage,domain='REGISTERED LINEAR B1 bounded research only; ell=4,8,16,32,64 for numerical band; [0,1/20]; original prepared two-column span, preserved complementary probes/22 fields; separate sufficient large-ell asymptotic domain',prepared_bridge_symbolically_zero=all(value==0 for value in bridge),full_programme_complete=False,physical_dust_closure=False,physics_pass=False))}
    summary=dict(schema='r4c1-g3n5-dust-stage1-acceptance-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='STAGE1_BOUNDED_RESEARCH_ACCEPTANCE_MET' if ok else 'STAGE1_ACCEPTANCE_OPEN',bounded_stage1_research_acceptance_met=ok,full_programme_complete=False,physical_dust_closure=False,
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
                 source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={name:common.sha(body) for name,body in bodies.items()})
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED','Stage2':'STOP_AND_ASSESS_DOMAIN_UNRESOLVED','Stage3':'NOT_ENTERED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',default=BASE+'r4c1_g3n5_dust_stage1_acceptance_attempt_01');p.add_argument('--replay');args=p.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay missing')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Read-only replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=summary['validation'],passed=summary['passed'],total=summary['total'],bounded_stage1_research_acceptance_met=summary['bounded_stage1_research_acceptance_met'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
