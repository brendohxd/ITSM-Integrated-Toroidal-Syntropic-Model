"""Enclose original stored seeds as well as the exact-recipe dust certificate."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_SEED_ENCLOSURE_V1_CONTRACT_2026-10-12.md'
PARENT=BASE+'r4c1_g3n5_dust_certificate_controls_attempt_01/'
EXPECTED='c7f7f8354ca5a4cbc7c78aa6d7a5adb37f95a7b23f08f2ff9644eda23741b5aa'
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_certificate_controls_v1 as control
target=control.target;k=control.k;common=control.common


def calculate():
    if sha256((ROOT/(PARENT+'summary.json')).read_bytes()).hexdigest()!=EXPECTED:raise RuntimeError('Control receipt drift')
    ps=common.read_json(PARENT+'summary.json')
    pins=dict(ps['source_sha256']);pins[PARENT+'summary.json']=EXPECTED
    pins.update({PARENT+name:value for name,value in ps['artifacts'].items()})
    for rel in (SELF,CONTRACT):pins[rel]=common.sha((ROOT/rel).read_bytes())
    missing=common.inspect_pins(pins)
    paths=[ROOT/rel for rel in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=target.old.parent.snapshot(paths)
    checks=common.Checks()
    checks.add('all_parent_controls_inspected',ps['passed']==ps['total']==97 and len(ps['checks'])==97 and all(r['passed'] is True for r in ps['checks']))
    cert=common.read_json(control.PARENT+'certificate.json')
    archive=json.loads((ROOT/(target.old.PARENT+'trajectories.json')).read_text(),parse_float=F)
    bg=target.old.Background()
    mats={name:target.old.parent.import_matrix(obj,bg.sy) for name,obj in common.read_json(target.old.PARENT+'matrices.json').items()}
    exponential=control.exp_rational_upper(F(3,2))
    rows=[]
    for row in cert['modes']:
        mode=row['ell'];nominal,radius,_=target.exact_initial(bg,mats,mode)
        checks.add('same_frozen_initial_enclosure_'+str(mode),F(radius,k.SCALE)==F(row['initial_error_upper']))
        stored=next(item['initial_balanced'] for item in archive['modes'] if item['ell']==mode)
        checks.add('original_seed_shapes_'+str(mode),len(stored)==20 and all(len(x)==4 for x in stored))
        const={name:F(value) for name,value in row['constants'].items()}
        representations=[]
        for label,cast in (('exact_JSON_decimal',lambda x:F(x)),('original_binary64',lambda x:F(float(x)))):
            delta=F(0)
            for i in range(20):
                for c in range(4):
                    difference=sum(abs(F(nominal[i][c][q].lo,k.SCALE)-cast(stored[i][c][q])) for q in range(2))
                    delta=max(delta,difference)
            # The center-to-exact-recipe radius is independently verified above.
            against_recipe=delta+F(radius,k.SCALE)
            homogeneous=exponential*const['K_T_infinity_to_Q']*against_recipe
            observer=F(row['dust_numerical_error_upper'])+const['K_observation_Q']*homogeneous
            fields=F(row['field_numerical_error_upper'])+const['K_fields_Q']*homogeneous
            model=F(row['prepared_true_model_error_upper'])+2*const['K_observation_Q']*homogeneous
            checks.add('original_stored_numerical_accuracy_'+str(mode)+'_'+label,max(observer,fields)<=F(1,10**8),dict(dust=float(observer),fields=float(fields)),'<=1e-8 full interval/all columns/all fields')
            checks.add('original_stored_model_accuracy_'+str(mode)+'_'+label,model<=F(1,100),float(model),'<=1/100 original prepared input-coefficient span')
            representations.append(dict(representation=label,center_difference=str(delta),against_exact_recipe=str(against_recipe),homogeneous_Q_radius=str(homogeneous),dust_numerical_error_upper=str(observer),field_numerical_error_upper=str(fields),prepared_model_error_upper=str(model),display=dict(dust=float(observer),fields=float(fields),prepared_model=float(model))))
        rows.append(dict(ell=mode,representations=representations))
    checks.add('five_modes_two_representations',[row['ell'] for row in rows]==[4,8,16,32,64] and all(len(row['representations'])==2 for row in rows))
    checks.add('source_pins_after',common.inspect_pins(pins)==missing)
    checks.add('source_size_mtime_hash_preserved',target.old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(r['passed'] for r in checks.rows);ok=passed==len(checks.rows)
    bodies={'seed_enclosures.json':common.encode(dict(modes=rows,domain='Original 20-state/four-column seeds, exact recipe plus immutable JSON-decimal and binary64 representations; same background/action; 0<=t<=1/20',proof='Homogeneous full Q propagator plus existing continuous defect/background/leading certificate',original_inputs_edited=False,physics_pass=False))}
    summary=dict(schema='r4c1-g3n5-dust-seed-enclosure-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='ORIGINAL_STORED_INPUTS_ENCLOSED' if ok else 'ORIGINAL_STORED_INPUT_ACCEPTANCE_UNMET',original_stored_seed_accuracy_proved=ok,
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',full_dust_milestone_complete=False,
                 canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
                 source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,artifacts={name:common.sha(body) for name,body in bodies.items()})
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED','Stage2':'STOP_AND_ASSESS_DOMAIN_UNRESOLVED','Stage3':'NOT_ENTERED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',default=BASE+'r4c1_g3n5_dust_seed_enclosure_attempt_01');p.add_argument('--replay');args=p.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Read-only replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',passed=summary['passed'],total=summary['total'],validation=summary['validation'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
