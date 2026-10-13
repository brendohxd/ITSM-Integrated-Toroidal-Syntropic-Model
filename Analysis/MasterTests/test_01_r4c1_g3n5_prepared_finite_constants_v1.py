"""Export exact low-mode constants omitted from the unchanged parent receipt."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import sympy as s

ROOT=Path(__file__).resolve().parents[2];BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix();PARENT=BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_error_v1.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='1a9e162f5985c8f2a7ee00ffc6eea227106bcf49afb238fd7dbaa55202096748':raise RuntimeError('Engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_prepared_dust_error_v1 as engine
old=engine.old;common=engine.common

def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()});pins[PARENT+'summary.json']='a637c7291ba1f3e1c1b3719f4c640de3b690c40bb0e9c6b38e7d9e37ab9f0e40';pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists());before=old.parent.snapshot(paths)
    checks=common.Checks();checks.add('parent_upper_bound_checked_not_sharp',ps['passed']==ps['total']==67 and ps['prepared_error_upper_bound_proved'] and not ps['full_prepared_high_p_remainder_proved'])
    bg=old.Background();ell=bg.ell;eps=s.Symbol('eps',positive=True);on=lambda m:m.applyfunc(s.cancel)
    data=common.read_json(PARENT+'formulas.json');diag=common.read_json(PARENT+'diagnostics.json');cc={k:s.sympify(v) for k,v in data['constants'].items()}
    delta2=old.parent.import_matrix(data['matrices']['initial_remainder'],{**bg.sy,'eps':eps})
    uniform=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json');maps=common.read_json(uniform['general_exact_maps_source'])['matrices']
    um,twi=[old.parent.import_matrix(maps[k],bg.sy) for k in ('fast_cross_map_U','wave_inverse_Twi')]
    raw=common.read_json(old.PARENT+'matrices.json');oo=old.parent.import_matrix(raw['actual_dust_observable'],bg.sy);bi=old.parent.import_matrix(raw['balancing_map_inverse'],bg.sy)
    ci=s.eye(20);ci[13,13]=bg.bg[0]/ell
    ow=on((oo*bi*ci).subs(ell,1/eps)*(s.eye(20)+um*eps)*twi)
    boxes={bg.sy[k]:(s.sympify(v[0]),s.sympify(v[1])) for k,v in uniform['background_boxes'].items()};t=s.Symbol('t',nonnegative=True);rows=[]
    for kval in (4,8):
        initialbox=old.RationalBox({eps:(s.Integer(0),s.Rational(1,kval))});kd=max(initialbox.norm(delta2),initialbox.norm(delta2.T))
        obsbox=old.RationalBox({**boxes,eps:(s.Rational(1,kval),s.Rational(1,kval))});ko=3*max(obsbox.norm(ow),obsbox.norm(ow.T))
        bound=s.Rational(3,2)*(ko*cc['K_W_low']*s.exp(30*t)*(cc['K_initial_fast']/kval+(kd+cc['K_source_low']*t)/kval**2)+cc['K_observation_low']*s.exp(s.Rational(21,10)*t)/kval**2)
        endpoint=s.simplify(bound.subs(t,s.Rational(1,20)));actual=next(x['max_actual_error'] for x in diag['modes'] if x['ell']==kval)
        checks.add('exact_rational_low_constants_'+str(kval),kd.is_Rational and ko.is_Rational and kd>=0 and ko>=0)
        checks.add('endpoint_control_'+str(kval),actual<=float(endpoint),actual,'<=derived endpoint display; parent already checked all 257 times')
        rows.append(dict(ell=kval,initial_remainder_constant=str(kd),observation_constant=str(ko),bound_exact=str(bound),endpoint_exact=str(endpoint),endpoint_display=float(endpoint),actual_max_error=actual,scope='Original prepared data, rotating B1, t in [0,1/20]; no new evolution or parent overwrite'))
    checks.add('pins_after',common.inspect_pins(pins)==absent);checks.add('source_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    body=common.encode(dict(parent_certificate=PARENT+'summary.json',parent_high_C2_endpoint_display=data['error_coefficient_endpoint_display'],common_exact_constants={k:str(cc[k]) for k in ('K_W_low','K_initial_fast','K_source_low','K_observation_low')},finite_mode_bounds=rows,sharpness_proved=False,physical_window_proved=False))
    passed=sum(x['passed'] for x in checks.rows);summary=dict(schema='r4c1-g3n5-prepared-finite-constants-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='EXACT_FINITE_CONSTANTS_EXPORTED_PARENT_UNCHANGED',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={'finite_bounds.json':common.sha(body)},prepared_upper_bound_parent_checked=True,sharp_order='NOT_PROVED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'});return {'finite_bounds.json':body,'summary.json':common.encode(summary)},summary

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_prepared_finite_constants_attempt_01');ap.add_argument('--replay');args=ap.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
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
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'physics_pass':False}))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
