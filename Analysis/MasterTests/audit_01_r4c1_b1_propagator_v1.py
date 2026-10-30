"""Independent exact-Fraction aggregation audit, not a new propagator or peer review.

Checks the recorded certificate inequalities without using its IV/TM arithmetic.
The main recomputing replay still has to verify the generated local defects.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_b1_propagator_v1_attempt_01/summary.json'
PSHA='93c5d85618d4546b61b6a74961d04d93da35e2ad95dc20d3b57b4ce4e38dce10'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda v:(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def exact_exp_upper(x):
    """Rational Taylor/geometric-tail bound, with exact scaling/squaring."""
    x=F(x);assert x>=0;count=0
    while x>1:x/=2;count+=1
    term=total=F(1)
    for n in range(1,81):term*=x/n;total+=term
    nxt=term*x/81;ratio=x/82
    answer=total+nxt/(1-ratio)
    for _ in range(count):answer*=answer
    return answer


def calculate():
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    d=json.loads((ROOT/PARENT).read_bytes());checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    pins=dict(d['source_sha256']);pins[PARENT]=PSHA;pins[SELF]=SHA((ROOT/SELF).read_bytes())
    snapshots={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        assert SHA(p.read_bytes())==want and sc.read_text().split()[0]==want,name
        for file in (p,sc):snapshots[file.relative_to(ROOT).as_posix()]=(SHA(file.read_bytes()),file.stat().st_mtime_ns)
    check('main_all_checks_and_acceptance',d['accepted'] and d['passed']==d['total']==62)
    check('scope_keeps_all_parent_holds',not any(d[z] for z in ('physics_pass','all_frequency_estimate','nonlinear_admission','nodal_G1_admitted','physical_window_demonstrated')))
    b=d['background'];T=F(1,20);bg_error=F(b['accumulated_error'])
    bg_required=(F(b['initial_error'])+T*F(b['residual']))*exact_exp_upper(T*F(b['Lipschitz']))
    check('background_accumulation_with_independent_exponential',bg_error>=bg_required)
    check('background_strict_tube_margins',len(b['strict_margins'])==11 and all(F(z)>0 for z in b['strict_margins']))
    check('kinetic_volume_conversion',F(6,5)**2>F(11,10)**3)
    check('all_frozen_modes_present',[m['k'] for m in d['modes']]==[1,7,40])
    for m in d['modes']:
        tag=str(m['k']);rows=m['tile_certificates'];h=T/64
        check('complete_time_cover_'+tag,len(rows)==64 and [x['tile'] for x in rows]==list(range(64)))
        check('nonnegative_defects_and_nonzero_tails_'+tag,all(
            all(F(row[z])>=0 for z in ('low_defect','high_tail','coefficient_remainder','background_forcing','interface_jump'))
            and F(row['high_tail'])>0 for row in rows))
        check('all_defect_components_included_'+tag,all(F(row['total_defect'])>=sum(F(row[z]) for z in
            ('low_defect','high_tail','coefficient_remainder','background_forcing')) for row in rows))
        check('all_polynomial_hashes_present_'+tag,all(len(row['polynomial_sha256'])==64 and
              set(row['polynomial_sha256'])<=set('0123456789abcdef') for row in rows))
        check('background_generator_error_'+tag,F(m['background_coefficient_error'])>=F(m['coefficient_Lipschitz'])*bg_error)
        check('continuous_defect_integral_'+tag,F(m['integrated_defect'])>=h*sum(F(row['total_defect']) for row in rows))
        check('all_interfaces_included_'+tag,F(m['interface_jumps'])>=sum(F(row['interface_jump']) for row in rows))
        mu=F(m['logarithmic_norm']);growth=F(m['growth'])
        check('logarithmic_norm_maximum_'+tag,mu>=max(F(row['mu']) for row in rows))
        check('growth_with_independent_exponential_'+tag,growth>=exact_exp_upper(mu*T))
        error=F(m['continuous_transformed_error'])
        check('full_accumulated_state_error_'+tag,error>=growth*(F(m['integrated_defect'])+F(m['interface_jumps'])))
        maxW=max(F(z) for z in m['norm']['W']);factor=F(6,5)*maxW
        check('physical_norm_conversion_'+tag,F(m['norm']['physical_conversion'])==factor and
              F(m['continuous_physical_relative_error'])>=factor*error)
        check('frozen_accuracy_met_'+tag,F(m['continuous_physical_relative_error'])<=F(1,10**8))
        reconstruction=F(m['reconstruction_norm'])*error+F(m['reconstruction_Lipschitz'])*bg_error*F(m['approximate_propagator_sup'])
        check('all_reconstruction_error_terms_'+tag,F(m['reconstruction_error_per_unit_transformed_input'])>=reconstruction)
        rho_min=F(int(b['tube'][-1][0]),2**256)
        check('linear_density_amplitude_safe_'+tag,0<F(m['linear_density_amplitude_limit'])<=
              rho_min/(2*F(m['linear_density_gain_per_unit_initial_kinetic_norm'])))
    for name,(digest,mtime) in snapshots.items():
        p=ROOT/name;assert SHA(p.read_bytes())==digest and p.stat().st_mtime_ns==mtime,name
    check('all_inputs_and_sidecars_unchanged',True)
    return dict(kind='B1_PROPAGATOR_EXACT_FRACTION_AGGREGATION_AUDIT_V1',
        passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,source_sha256=pins,
        scope='Independent rational arithmetic for recorded aggregation inequalities; local Taylor proof still requires main replay',
        external_peer_review=False,physics_pass=False,gate_effect='NONE',review='DEFERRED')


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--out');g.add_argument('--replay');args=p.parse_args()
    if args.out and (ROOT/args.out).exists():raise FileExistsError(args.out)
    d=calculate();raw=ENC(d)
    if args.replay:
        f=ROOT/args.replay;assert f.read_bytes()==raw and Path(str(f)+'.sha256').read_text().split()[0]==SHA(raw)
        print('IMMUTABLE_REPLAY_EXACT')
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);f=out/'summary.json';f.write_bytes(raw)
        Path(str(f)+'.sha256').write_text(SHA(raw)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:d[k] for k in ('passed','total','physics_pass')}));raise SystemExit(0 if d['passed']==d['total'] else 2)


if __name__=='__main__':main()
