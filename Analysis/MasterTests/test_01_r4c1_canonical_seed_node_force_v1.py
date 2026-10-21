"""Read-only independent analytic node-force control of frozen seed receipts."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/test_01_r4c1_canonical_seed_admission_v1.py'
PSHA = '4f123be20aab9b1cd39a1fc27da8f01fd0fb66b13e1e0f7eedab4bfc6fcfb8b7'
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SEED_NODE_FORCE_V1_ADDENDUM_2026-10-21.md'
ASHA = 'd423a5e3674a34eee954085393e906c4ab2a5272f701cfea8f2be0cf445050b1'
PRIMARY = 'Analysis/MasterTests/outputs/r4c1_canonical_seed_admission_v1_attempt_01'
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()

if SHA((ROOT/PARENT).read_bytes()) != PSHA:
    raise ValueError('frozen primary source drift')
spec = importlib.util.spec_from_file_location('node_force_seed_parent', ROOT/PARENT)
seed = importlib.util.module_from_spec(spec); spec.loader.exec_module(seed)


def sources():
    meta = seed.sources()
    pins = {PARENT: PSHA, ADDENDUM: ASHA, SELF: SHA((ROOT/SELF).read_bytes())}
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in (ROOT/PRIMARY).iterdir()} != expected:
        raise ValueError('primary receipt set changed')
    for name in ('summary.json', 'independent.json', 'formulas.json'):
        path = ROOT/PRIMARY/name; pins[path.relative_to(ROOT).as_posix()] = SHA(path.read_bytes())
    for name, digest in pins.items():
        path = ROOT/name; side = Path(str(path)+'.sha256')
        if SHA(path.read_bytes()) != digest or side.read_text().split()[0].lower() != digest:
            raise ValueError('node-force source/sidecar drift: '+name)
        meta['pins'][name] = digest
        for f in (path, side):
            meta['records'][f.relative_to(ROOT).as_posix()] = seed.base.metadata(f)
    return meta


def calculate():
    mp.mp.dps = 100
    before = sources(); ch = seed.Checks()
    primary = json.loads((ROOT/PRIMARY/'summary.json').read_bytes())
    payload = json.loads((ROOT/PRIMARY/'independent.json').read_bytes())
    ch.add('primary_actual_K_controls_passed', primary['validation'] == 'CANONICAL_SEED_IDENTITIES_VERIFIED' and not primary['failed_checks'])
    x = sy.Symbol('x', positive=True)
    majorant = sy.factor(3*x-((1-x)**-2-1))
    ch.add('exact_phase_normalization_remainder_bound', sy.cancel(majorant-x*(1-5*x+3*x*x)/(1-x)**2) == 0)
    ch.add('phase_remainder_positive_on_registered_domain', sy.Rational(1, 6500000) < sy.Rational(1, 10) and 1-5*sy.Rational(1, 10) > 0)
    ch.add('positive_radial_force_all_eta', sy.Rational(127, 560)-sy.Rational(3, 6500000) > 0)
    records = []; seen = set()
    for case in payload['cases']:
        key = (case['family'], case['eta'], case['grid'], case['node_orientation'])
        ch.add(str(key)+'_unique_case', key not in seen); seen.add(key)
        if case.get('incomplete'):
            ch.add(str(key)+'_complete', False); continue
        eta = mp.mpf(case['eta'].split('/')[0])/mp.mpf(case['eta'].split('/')[1]) if '/' in case['eta'] else mp.mpf(case['eta'])
        p = eta/5; rho = mp.sqrt(eta)
        par = seed.body.canonical.parameters(case['family'], case['eta'], 'mp')
        expected = {'m2': mp.mpf(1), 'lambda4': mp.mpf(1)/3, 'lambda6': mp.mpf(1)/5,
                    'Lambda': mp.mpf(2), 'g_r': 3*eta/7, 'zeta': eta/13}
        seed.small(ch, str(key)+'_original_scalar_parameter_map', max(abs(par[k]-v) for k, v in expected.items()), '1e-80')
        phase_x = par['zeta']*eta/(2*500**2)
        jnode = eta/(1-phase_x)
        Vprime = par['m2']*rho+par['lambda4']*rho**3/2+par['lambda6']*rho**5/(4*par['Lambda']**2)+par['g_r']*rho**3/2
        force = Vprime-jnode*jnode/rho**3
        alternate = rho*(eta/6+mp.mpf(127)*eta**2/560-((1-eta**2/6500000)**-2-1))
        seed.small(ch, str(key)+'_independent_force_simplification', abs(force-alternate)/(1+abs(force)), '1e-80')
        ch.add(str(key)+'_force_strictly_positive', bool(force > 0), seed.number(force))
        steps = []
        for profile in case['radial_seeds']:
            fnode = mp.mpf(1) if profile['profile'] == 'constant' or case['node_orientation'] == 0 else mp.mpf(-1)
            predicted = -force*fnode/p**3
            for step in profile['steps']:
                actual, actual_Z = map(mp.mpf, step['next_auxiliary']['values'])
                error = abs(actual-predicted)/(1+abs(actual)+abs(predicted))
                label = str(key)+'_'+profile['profile']+'_'+step['step']
                seed.small(ch, label+'_full_K_node_s_force', error)
                seed.small(ch, label+'_full_K_node_Z_zero', abs(actual_Z))
                steps.append(dict(profile=profile['profile'], step=step['step'],
                    predicted_s=seed.number(predicted), actual_s=seed.number(actual),
                    normalized_s_error=seed.number(error), actual_Z=seed.number(actual_Z)))
        records.append(dict(key=key, local_phase_density=seed.number(jnode), mean_phase_density=seed.number(eta),
            positive_radial_force=seed.number(force), checks=steps))
    ch.add('all36_cases_all144_node_pairs_checked', len(records) == 36 and len(seen) == 36 and sum(len(r['checks']) for r in records) == 144)
    if sources() != before:
        raise ValueError('primary or source metadata changed during independent read')
    failures = [r for r in ch.rows if not r['passed']]
    summary = dict(validation='CANONICAL_SEED_NODE_FORCE_VERIFIED' if not failures else 'CANONICAL_SEED_NODE_FORCE_UNRESOLVED',
        passed=len(ch.rows)-len(failures), total=len(ch.rows), checks=ch.rows, failed_checks=failures, unknown_checks=[],
        source_metadata=before, physical_persistence_proved=False, frozen_A_squared_is_not_material_persistence=True,
        primary_receipts_read_only=True, physics_pass=False, gate_effect='NONE', stage2_complete=False,
        stage3_entered=False, review_status='DEFERRED', Rule9_cleared=False)
    formulas = dict(local_phase='j_node=eta/(1-eta^2/6500000), not mean eta',
        radial_force='sqrt(eta)*(eta/6+127*eta^2/560-((1-eta^2/6500000)^(-2)-1))>0',
        next_node_s='-F_rho*f(node)/p^3', next_node_Z='0',
        conclusion='If full seed identity and analytic structural hypotheses hold: u_f in frozen D(A), Au_f not in frozen D(A); no physical instability or persistence verdict')
    return summary, dict(cases=records), formulas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--replay', type=Path)
    args = parser.parse_args()
    dest = (args.output or args.replay).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):
        raise ValueError('outside declared output root')
    if args.output and dest.exists():
        raise FileExistsError('never overwrite a result')
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('missing replay destination')
    summary, independent, formulas = calculate()
    if args.output:
        dest.mkdir(parents=False, exist_ok=False)
    for name, value in [('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)]:
        seed.base.pair(dest, name, ENC(value), bool(args.replay))
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in dest.iterdir()} != expected:
        raise ValueError('node-force receipt set changed')
    seed.weak.progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
        passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    raise SystemExit(bool(summary['failed_checks']))


if __name__ == '__main__':
    main()
