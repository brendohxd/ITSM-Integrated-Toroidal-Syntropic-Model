"""Independent Fraction controls for the frozen continuous dust certificate."""
from fractions import Fraction as F
from hashlib import sha256
from math import factorial
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_CERTIFICATE_CONTROLS_V1_CONTRACT_2026-10-12.md'
PARENT=BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/'
EXPECTED='df6dff025f24f82afaf26ac699d419037d65546f6da7f823b50dbb54b12569e1'
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_certified_numerical_v1 as target
k=target.k;common=target.common


def exp_rational_upper(q):
    q=F(q)
    if not 0<=q<201:raise ValueError('Positive exponential series domain')
    term=total=F(1)
    for n in range(1,201):term=term*q/n;total+=term
    following=term*q/201
    return total+following/(1-q/202)


def bounds(interval):return F(interval.lo,k.SCALE),F(interval.hi,k.SCALE)


def value_between(interval,q):
    a,b=bounds(interval)
    return a<=q<=b


def interval_controls(checks):
    intervals=[(F(-5,7),F(13,11)),(F(-8,3),F(-1,19)),(F(1,17),F(19,4)),(F(0),F(0)),(F(-1,10**60),F(1,10**60))]
    iv=lambda a,b:k.IV(k.IV.fraction(a).lo,k.IV.fraction(b).hi)
    for i,(a,b) in enumerate(intervals):
        aa=iv(a,b)
        for j,(c,d) in enumerate(intervals):
            bb=iv(c,d)
            corner=[(x,y) for x in (a,b) for y in (c,d)]
            ok=all(value_between(aa+bb,x+y) and value_between(aa-bb,x-y) and value_between(aa*bb,x*y) for x,y in corner)
            if c>0 or d<0:ok=ok and all(value_between(aa/bb,x/y) for x,y in corner)
            checks.add(f'wide_interval_Fraction_{i}_{j}',ok)
    for i,(a,b) in enumerate(((F(0),F(2)),(F(1,19),F(7,3)),(F(3469,4620),F(3469,4620)))):
        root=iv(a,b).sqrt();lo,hi=bounds(root)
        checks.add('wide_square_root_'+str(i),lo*lo<=a<=b<=hi*hi)
    for i,(a,b) in enumerate(intervals):
        if a<=0<=b:
            try:iv(a,b).inverse()
            except ZeroDivisionError:ok=True
            else:ok=False
            checks.add('wide_zero_inverse_rejected_'+str(i),ok)
    p=k.TM([k.IV.fraction(F(3,4)),k.IV.fraction(F(1,8)),k.IV.fraction(F(-1,32)),k.ZERO])
    q=p.inverse().restrict(3,8,2)
    checks.add('inverse_and_restriction_tail_present',q.radius>0)
    for i in range(17):
        t=F(3,8)+F(i,128)
        actual=1/(F(3,4)+t/8-t*t/32)
        checks.add('independent_rational_Taylor_inverse_'+str(i),value_between(q.at(i,16),actual))


def actual_stepper_controls(checks):
    degree=target.DEGREE
    zero=k.TM.constant(k.ZERO,degree)
    omega=k.TM.constant(k.IV.rational(8192),degree)
    entries=[(0,1,-omega,zero),(1,0,omega,zero)]
    initial=[[(k.ONE if i==c else k.ZERO,k.ZERO) for c in range(4)] for i in range(20)]
    models,end,defect,amplitude=target.state_polynomial(entries,initial,F(1,16384))
    x=F(1,2)
    cosine=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(31)),F(0))
    sine=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range(31)),F(0))
    ctail=x**62/factorial(62);stail=x**63/factorial(63)
    # Two active defect components imply ||r||_2 <= sqrt(2) d < 2d.
    propagated=2*F(defect,k.SCALE)/16384
    errors=[]
    for i,c,actual,tail in ((0,0,cosine,ctail),(1,0,sine,stail),(0,1,-sine,stail),(1,1,cosine,ctail)):
        approximation=F(end[i][c][0].lo,k.SCALE)
        errors.append(abs(approximation-actual)+tail)
    checks.add('actual_skew_stepper_independent_analytic_enclosure',max(errors)<=propagated,
               dict(actual_error_upper=str(max(errors)),continuous_defect_error_upper=str(propagated)), 'exact Fraction Taylor series and unit Euclidean propagation')
    checks.add('actual_skew_all_four_columns_20_states',len(end)==20 and all(len(row)==4 for row in end))
    _,unchanged,d0,_=target.state_polynomial([],initial,F(1,16384))
    checks.add('actual_zero_generator_no_jump',d0==0 and all(unchanged[i][c][q].lo==initial[i][c][q].lo==unchanged[i][c][q].hi for i in range(20) for c in range(4) for q in range(2)))


def verify_tiles(row,tiles):
    if len(tiles)!=row['steps'] or [t['tile'] for t in tiles]!=list(range(row['steps'])):raise ValueError('Omitted/reordered tile')
    chain=sha256()
    for tile in tiles:chain.update(bytes.fromhex(tile['polynomial_sha256']))
    if chain.hexdigest()!=row['tile_chain_sha256']:raise ValueError('Tile polynomial chain mismatch')
    for name,key in (('defect_upper','state_defect_upper'),('state_amplitude_upper','state_amplitude_upper'),('prepared_difference_upper','prepared_approximant_difference_upper')):
        if max(F(int(t[name]),k.SCALE) for t in tiles)!=F(row[key]):raise ValueError('Tile aggregate mismatch')


def calculate():
    if sha256((ROOT/(PARENT+'summary.json')).read_bytes()).hexdigest()!=EXPECTED:raise ValueError('Original summary drift')
    ps=common.read_json(PARENT+'summary.json');cert=common.read_json(PARENT+'certificate.json');tiles=common.read_json(PARENT+'tile_certificates.json')
    pins=dict(ps['source_sha256']);pins[PARENT+'summary.json']=EXPECTED
    pins.update({PARENT+name:value for name,value in ps['artifacts'].items()})
    for rel in (SELF,CONTRACT):pins[rel]=common.sha((ROOT/rel).read_bytes())
    missing=common.inspect_pins(pins)
    paths=[ROOT/rel for rel in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=target.old.parent.snapshot(paths)
    checks=common.Checks()
    checks.add('every_original_check_inspected',ps['passed']==ps['total']==85 and len(ps['checks'])==85 and all(q['passed'] is True for q in ps['checks']))
    checks.add('original_scope_unpromoted',ps['physics_pass'] is False and ps['gate_effect']=='NONE' and ps['Rule9_cleared'] is False and ps['review_status']=='DEFERRED' and not ps['full_dust_milestone_complete'])
    for name,value in {**ps['artifacts'],'summary.json':EXPECTED}.items():
        body=(ROOT/(PARENT+name)).read_bytes()
        checks.add('artifact_sidecar_'+name,sha256(body).hexdigest()==value and (ROOT/(PARENT+name+'.sha256')).read_text().split()[0]==value)
    interval_controls(checks);actual_stepper_controls(checks)
    bg=cert['background'];lead=cert['leading'];T=F(1,20)
    eb=F(bg['error'])
    eb_min=exp_rational_upper(F(bg['Lipschitz'])*T)*(F(bg['initial_error'])+T*F(bg['defect']))
    checks.add('Fraction_background_majorant',eb>=eb_min and eb<F(bg['continuation_margin']))
    ep=F(lead['error'])
    ep_min=exp_rational_upper(F(21,10)*T)*T*(F(lead['defect'])+F(lead['Lipschitz'])*eb*F(lead['amplitude']))
    checks.add('Fraction_leading_majorant',ep>=ep_min)
    observations=[]
    for row in cert['modes']:
        mode=row['ell'];const={name:F(value) for name,value in row['constants'].items()}
        verify_tiles(row,tiles[str(mode)])
        checks.add('all_continuous_tiles_'+str(mode),True,dict(tiles=row['steps']))
        try:verify_tiles(row,tiles[str(mode)][:-1])
        except ValueError:reject=True
        else:reject=False
        checks.add('omitted_tile_rejected_'+str(mode),reject)
        forcing=F(row['state_defect_upper'])+const['L_Az']*eb*F(row['state_amplitude_upper'])
        ew_min=exp_rational_upper(F(3,2))*const['K_T_infinity_to_Q']*(F(row['initial_error_upper'])+T*forcing)
        ew=F(row['Q_state_error_upper'])
        checks.add('Fraction_full_Q_error_'+str(mode),ew>=ew_min)
        ow_min=const['K_observation_Q']*ew+const['L_Oz']*eb*F(row['state_amplitude_upper'])
        fw_min=const['K_fields_Q']*ew+const['L_Fz']*eb*F(row['state_amplitude_upper'])
        ow,fw=F(row['dust_numerical_error_upper']),F(row['field_numerical_error_upper'])
        checks.add('Fraction_all_observed_errors_'+str(mode),ow>=ow_min and fw>=fw_min and max(ow,fw)<=F(1,10**8))
        model_min=F(row['prepared_approximant_difference_upper'])+2*ow+ep
        model=F(row['prepared_true_model_error_upper'])
        checks.add('Fraction_prepared_model_error_'+str(mode),model>=model_min and model<=F(1,100))
        checks.add('declared_step_choice_'+str(mode),row['steps']>=32 and row['steps']<=32768 and row['steps']&(row['steps']-1)==0 and F(row['Az_infinity_majorant'])*T/row['steps']<=1)
        comparisons=row['archive_comparisons']
        checks.add('original_all_four_columns_archive_'+str(mode),len(comparisons)==257 and [r['index'] for r in comparisons]==list(range(257)) and max(r['dust_difference'] for r in comparisons)<=1e-8 and max(r['field_difference'] for r in comparisons)<=1e-8 and len(row['final_state'])==20 and all(len(q)==4 for q in row['final_state']))
        observations.append(dict(ell=mode,tiles=row['steps'],model_error_upper=str(model),dust_error_upper=str(ow),fields_error_upper=str(fw)))
    checks.add('five_modes_not_convenient_subset',[q['ell'] for q in cert['modes']]==[4,8,16,32,64])
    checks.add('source_pins_after',common.inspect_pins(pins)==missing)
    checks.add('source_size_mtime_hash_preserved',target.old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(q['passed'] for q in checks.rows);ok=passed==len(checks.rows)
    bodies={'controls.json':common.encode(dict(modes=observations,original_checks_inspected=85,actual_stepper_rotation_and_zero_controls=True,independent_arithmetic='fractions.Fraction',input_preservation=len(before),physics_pass=False))}
    summary=dict(schema='r4c1-g3n5-dust-certificate-controls-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='INDEPENDENT_CERTIFICATE_CONTROLS_CHECKED' if ok else 'INDEPENDENT_CERTIFICATE_CONTROLS_FAILED',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                 full_dust_milestone_complete=False,canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
                 source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,artifacts={name:common.sha(body) for name,body in bodies.items()})
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED','Stage2':'STOP_AND_ASSESS_DOMAIN_UNRESOLVED','Stage3':'NOT_ENTERED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',default=BASE+'r4c1_g3n5_dust_certificate_controls_attempt_01')
    p.add_argument('--replay');args=p.parse_args()
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
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',passed=summary['passed'],total=summary['total'],validation=summary['validation'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
