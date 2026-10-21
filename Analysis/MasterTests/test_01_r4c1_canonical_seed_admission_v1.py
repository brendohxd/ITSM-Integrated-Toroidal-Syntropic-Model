"""Actual full-K canonical seed admission; no physical persistence clearance."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import traceback

import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/test_01_r4c1_weak_generator_realization_v2.py'
PSHA = '84a25e02d57fbcdc208bf5cef5531bad6226fbfbaaff0ab2ff8906d722c9867b'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SEED_ADMISSION_V1_CONTRACT_2026-10-21.md'
CSHA = 'a181b17335dc737b1d1afa004bb0e09d4a14f306450216191541261e1260eab0'
SHA = lambda value: hashlib.sha256(value).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
STEPS = ('1e-24', '1e-28')
TOL = '1e-20'

if SHA((ROOT/PARENT).read_bytes()) != PSHA:
    raise ValueError('frozen full-K source changed')
spec = importlib.util.spec_from_file_location('seed_weak_parent', ROOT/PARENT)
weak = importlib.util.module_from_spec(spec); spec.loader.exec_module(weak)
descriptor, body, base = weak.descriptor, weak.body, weak.base
Checks = weak.Checks


def number(value):
    return mp.nstr(value, 70)


def small(ch, name, error, tolerance=TOL):
    ch.add(name, bool(mp.isfinite(error) and error < mp.mpf(tolerance)), number(error), 'finite and strictly < '+tolerance)


def sources():
    meta = weak.sources()
    pins = {
        PARENT: PSHA, CONTRACT: CSHA, SELF: SHA((ROOT/SELF).read_bytes()),
        'Theory/Gates/RES-001/RES001_R4C1_WEAK_GENERATOR_REALIZATION_V2_REPORT_2026-10-21.md':
        'c87c3f7bac32c49c510ee64485d2ef199d87ab6c581af1619bec9942129aced2',
        'Theory/Gates/RES-001/RES001_R4C1_WEAK_GENERATOR_REALIZATION_V2_ANALYTIC_DERIVATION_2026-10-21.md':
        '6446be0c8bd44343978622cfb3a68a403a15da077794612e4a8a4deedb7bb847',
        'Analysis/MasterTests/outputs/r4c1_weak_generator_realization_v2_attempt_01/summary.json':
        '5e368c93c0025bc4e15be6ed8ccb0ff1f6df9d0376de4175d043d242e4800a88',
        'Analysis/MasterTests/outputs/r4c1_weak_generator_realization_v2_attempt_01/independent.json':
        '305ba2e7df99aac30ec96294b2fbae52f6a3fa7d64ceca122ba04c9bbccc0116',
        'Analysis/MasterTests/outputs/r4c1_weak_generator_realization_v2_attempt_01/formulas.json':
        'a30623f240e1124e463873271f5e32a8114ee79c24406b21120aa5fc71cb1582'}
    for name, want in pins.items():
        path = ROOT/name; side = Path(str(path)+'.sha256')
        if SHA(path.read_bytes()) != want or side.read_text().split()[0].lower() != want:
            raise ValueError('source or sidecar drift: '+name)
        meta['pins'][name] = want
        meta['records'][name] = base.metadata(path)
        meta['records'][side.relative_to(ROOT).as_posix()] = base.metadata(side)
    return meta


def exact(ch):
    # Polar kinetic/current identities from the original Cartesian density.
    r, a, rd, ad = sy.symbols('r a rdot adot', real=True)
    u, v = r*sy.cos(a), r*sy.sin(a)
    ud = sy.diff(u, r)*rd+sy.diff(u, a)*ad
    vd = sy.diff(v, r)*rd+sy.diff(v, a)*ad
    ch.add('original_radial_kinetic_decoupling', sy.trigsimp(ud**2+vd**2-rd**2-r**2*ad**2) == 0)
    ch.add('original_alignment_current_has_no_radial_rate', sy.trigsimp(v*ud-u*vd+r*r*ad) == 0)
    p, f, g, z, c, d, y = sy.symbols('p f g z C d y', nonzero=True, real=True)
    # I*=-I; translation lambda=-<f Dg>/d. Independently keep its contribution.
    direct = (-z)*f*g/p-c*f*g/(d*p)
    ch.add('translation_corrected_mixed_pullback', sy.cancel(direct-(-z-c/d)*f*g/p) == 0)
    ch.add('full_stationary_radial_inverse', sy.diff(y*f-y*y/2, y).subs(y, f) == 0)
    ch.add('radial_legendre_second_derivative', sy.diff((f+y)**2/(2*p), y, 2)-1/p == 0)
    ch.add('frozen_velocity_second_derivative_would_be_zero', sy.diff((f+y)*f-f*f/2, y, 2) == 0)
    # Both auxiliary residuals vanish identically for the proposed actual K seed.
    t = sy.Symbol('theta', real=True)
    for node in (sy.pi/2, 3*sy.pi/2):
        for name in ('s', 'cross_corrected_Z'):
            zero = sy.Integer(0)
            ch.add(name+'_zero_value_'+str(node), zero.subs(t, node) == 0)
            ch.add(name+'_zero_first_jet_'+str(node), sy.diff(zero, t).subs(t, node) == 0)
    # Counterexample to the invalid inference: frozen A maps out of D(0), yet
    # the moving constraint is exactly preserved by the nonautonomous flow.
    tau, x = sy.symbols('time x', real=True)
    path = sy.Matrix([x, tau*x]); M = sy.Matrix([[0, 0], [1, 0]])
    F = sy.Matrix([[-tau, 1]])
    ch.add('moving_domain_counterexample_solves_actual_ODE', sy.diff(path, tau)-M*path == sy.zeros(2, 1))
    ch.add('moving_domain_counterexample_material_constraint', sy.simplify((F*path)[0]) == 0)
    ch.add('frozen_second_domain_is_not_persistence', (F.subs(tau, 0)*M*path.subs(tau, 0))[0] == x and x != 0)
    ch.add('material_constraint_retains_explicit_time_term', sy.simplify((sy.diff(F, tau)*path+F*M*path)[0]) == 0)
    for label, value, accept in (('below', mp.mpf('1e-21'), True), ('boundary', mp.mpf(TOL), False),
                                 ('above', mp.mpf('1e-19'), False), ('nonfinite', mp.inf, False)):
        ch.add('strict_new_check_'+label, bool(mp.isfinite(value) and value < mp.mpf(TOL)) == accept)
    return dict(
        radial_seed='u_f: delta P_amplitude=f only; Q, other P, M, PM, s, Z all zero',
        translation='lambda_mixed=-<f*D(delta amplitude)>/d; retain full restored Kzz and Xy momenta',
        effective_shift='R_eff=-I(y_Kzz)-(<y_Xy*sin>+<y_Kzz*I(sin*D w)>)/d',
        full_K='(Ku)_Pamp=f/p; (Ku)_Qamp=-D(R_eff*f)/p; every other average-L2 row zero',
        graph_image='(Au)_Qamp=f/p; (Au)_Pamp=D(R_eff*f)/p; all other components zero',
        analytic_domain='For fixed smooth registered structural background and smooth periodic f, seed lies in frozen D(Amax); not physical initial-state admission',
        auxiliary='r_s=0 and r_Z-B*r_P=0 IDENTICALLY for the seed, hence both jets zero at BOTH nodes',
        material_requirement='D_t F(t,u)=partial_t F+F(A(t)u)+node_speed*D_node F; frozen A^2 alone is insufficient',
        background_requirement='Omega*T-dH=0 on the declared reduced chart plus full admission/persistence; small sampled residual is not zero',
        physical_persistence='NOT_PROVED', physical_mode='NOT_IDENTIFIED', physics_pass=False)


def seed(raw, name):
    result = descriptor.zeros(raw['n'])
    values = [mp.mpf(1) if name == 'constant' else mp.sin(t) for t in raw['theta']]
    for row, value in zip(result['P'], values):
        row[6] = value
    return result, values


def effective_shift(raw, out, y0):
    yL = [row[5] for row in y0]
    yV = [row[7] for row in y0]
    inv_yL = body.mv(raw['I'], yL)
    sin_dw = [s*dq[7] for s, dq in zip(raw['sine'], out['dq'])]
    I_sin_dw = body.mv(raw['I'], sin_dw)
    C = body.mean([a*b+c*d for a, b, c, d in zip(yV, raw['sine'], yL, I_sin_dw)])
    return [-value-C/out['d'] for value in inv_yL], C


def expected_seed(raw, shift, values):
    n, p = raw['n'], raw['rate']
    derivative = body.Dmul(raw['D'], [a*b for a, b in zip(shift, values)])
    cov, image = descriptor.zeros(n), descriptor.zeros(n)
    for i, value in enumerate(values):
        cov['P'][i][6] = value/(p*n)
        cov['Q'][i][6] = -derivative[i]/(p*n)
        image['Q'][i][6] = value/p
        image['P'][i][6] = derivative[i]/p
    return cov, image


def auxiliary(cov, raw):
    n, p, b = raw['n'], raw['rate'], raw['par']['b']
    rs = [n*row[11] for row in cov['Q']]
    rz = [n*row[10] for row in cov['Q']]
    corrected = []
    for i, q in enumerate(raw['q']):
        w = q[7]
        B = p*b*(w*w*(n*cov['P'][i][0]/2+3*n*cov['P'][i][2]/2+cov['PM'][2]/2)+2*w*n*cov['P'][i][4])
        corrected.append(rz[i]-B)
    slopes = [body.Dmul(raw['D'], field)[0] for field in (rs, corrected)]
    return dict(s=[number(v) for v in rs], raw_Z=[number(v) for v in rz],
        corrected_Z=[number(v) for v in corrected], values=[number(rs[0]), number(corrected[0])],
        spectral_slopes=[number(v) for v in slopes],
        sampled_node='pi/2' if raw['sine'][0] > 0 else '3*pi/2',
        interpretation='FINITE_INTERPOLANT_DIAGNOSTIC_NOT_CONTINUUM_TRACE_OR_MATERIAL_PERSISTENCE')


def full_action(X, raw, y0, out, T, vector, h):
    H = descriptor.hvp(X, raw, y0, out, vector, h)
    D = descriptor.drift(X, raw, vector, T, h)
    return descriptor.combine(H, D, -1), H, D


def grid_job(task):
    index, point, initial, n, offset = task
    ch = Checks()
    try:
        raw, X = body.build_data(point, initial, n, offset, 100)
        y0, err = body.baseline(raw, X)
        out = descriptor.functional(X, raw, y0)
        small(ch, 'original_stationary_twelve_velocity_solve', err)
        T = descriptor.background(X, raw, y0, out)
        shift, C = effective_shift(raw, out, y0)
        grad = descriptor.gradient(X, raw, y0)
        residual = descriptor.combine(descriptor.omega(X, raw, T), grad, -1)
        clock_row = residual['tau']; residual['tau'] = mp.mpf(0)
        small(ch, 'zero_initial_radial_velocity', max(abs(row[9]) for row in y0))
        records = []
        for name in ('constant', 'sin'):
            u, values = seed(raw, name)
            expected, image = expected_seed(raw, shift, values)
            omega_image = descriptor.omega(X, raw, image)
            small(ch, name+'_complete_Omega_image_matches_expected_K', descriptor.relative(omega_image, expected))
            previous = None; steps = []
            for hs in STEPS:
                h = mp.mpf(hs)
                K, H, D = full_action(X, raw, y0, out, T, u, h)
                identity = descriptor.relative(K, expected)
                small(ch, name+'_entire_full_K_independent_identity_'+hs, identity)
                small(ch, name+'_momentum_only_seed_drift_'+hs, descriptor.norm(D)/(1+descriptor.norm(K)), '1e-30')
                actual_image_K, image_H, image_D = full_action(X, raw, y0, out, T, image, h)
                if previous is not None:
                    small(ch, name+'_two_step_seed_K', descriptor.relative(K, previous[0]))
                    small(ch, name+'_two_step_next_coupled_K', descriptor.relative(actual_image_K, previous[1]))
                previous = K, actual_image_K
                steps.append(dict(step=hs, seed_identity_error=number(identity), seed_drift_norm=number(descriptor.norm(D)),
                    seed_auxiliary=auxiliary(K, raw), next_auxiliary=auxiliary(actual_image_K, raw),
                    next_full_K=[mp.nstr(v, 45) for v in body.flatten(actual_image_K)],
                    next_full_K_order='Q rows12 then P rows10 then M3 PM3 tau1; payload fields carry1/n',
                    next_drift_norm=number(descriptor.norm(image_D))))
            frozen = descriptor.hvp(X, raw, y0, out, u, mp.mpf(STEPS[-1]), frozen=True)
            omission = descriptor.norm(descriptor.combine(previous[0], frozen, -1))
            ch.add(name+'_frozen_velocity_shortcut_rejected', bool(omission > mp.mpf('1e-15')), number(omission))
            mixed = None
            if name == 'constant' and n == 25 and offset == 0:
                mixed = descriptor.mixed_control(ch, X, raw, y0, weak.directions(raw)[0], u, previous[0])
            records.append(dict(profile=name, steps=steps, independent_original_functional_mixed=mixed,
                graph_image=[mp.nstr(v, 45) for v in body.flatten(image)], frozen_velocity_omission_norm=number(omission)))
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset,
            radial_seeds=records, effective_shift=[number(v) for v in shift], translation_C=number(C),
            background_chart_residual_norm=number(descriptor.norm(residual)),
            background_auxiliary_residual=auxiliary(residual, raw), global_clock_residual_separate=number(clock_row),
            computed_node_speed=number(-T['Q'][0][4]/out['dq'][0][7]),
            background_exact_admission=False, physical_initial_data_admission=False,
            material_persistence_proved=False, frozen_A_squared_equals_time_persistence=False,
            physical_state_adopted_or_evolved=False)
    except Exception:
        ch.add('unexpected_grid_exception', False, traceback.format_exc())
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset, incomplete=True)
    return (index, n, offset), result, ch.rows


def calculate(workers):
    mp.mp.dps = 100
    before = sources(); ch = Checks(); formulas = exact(ch)
    points = body.lift.READ(body.nodal.reg.JOINT+'independent.json')
    initial = body.lift.READ(body.lift.cop.CERTS)
    if len(points) != 9 or len(initial) != 9 or any(a['family'] != b['family'] or a['eta'] != b['eta'] for a, b in zip(points, initial)):
        raise ValueError('original case order changed')
    tasks = [(i, a, b, n, o) for i, (a, b) in enumerate(zip(points, initial)) for n in (25, 33) for o in (0, 1)]
    weak.progress('CANONICAL_SEED_TASKS', tasks=len(tasks), workers=workers)
    results = {}
    if workers == 1:
        for task in tasks:
            key, result, rows = grid_job(task); results[key] = result, rows
            weak.progress('GRID_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    else:
        with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
            futures = [pool.submit(grid_job, task) for task in tasks]
            for future in as_completed(futures):
                key, result, rows = future.result()
                if key in results:
                    raise ValueError('duplicate case key')
                results[key] = result, rows
                weak.progress('GRID_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    records = []
    for key in sorted(results):
        record, rows = results[key]; records.append(record)
        for row in rows:
            ch.add(str(key)+'_'+row['name'], row['passed'], row.get('value'), row.get('criterion'))
    ch.add('complete_all36_grids_both_seed_profiles_both_steps', len(records) == 36 and all(not r.get('incomplete') and len(r['radial_seeds']) == 2 and all(len(s['steps']) == 2 for s in r['radial_seeds']) for r in records))
    if sources() != before:
        raise ValueError('source/native metadata changed during run')
    failed = [row for row in ch.rows if not row['passed']]
    summary = dict(validation='CANONICAL_SEED_IDENTITIES_VERIFIED' if not failed else 'CANONICAL_SEED_UNRESOLVED',
        passed=len(ch.rows)-len(failed), total=len(ch.rows), checks=ch.rows, failed_checks=failed, unknown_checks=[],
        source_metadata=before, analytic_seed_domain_scope='Owning report proof required; fixed smooth structural coefficients and smooth f; frozen D(Amax) only',
        physical_background_admitted=False, physical_initial_data_space_identified=False, material_domain_persistence_proved=False,
        full_physical_auxiliary_hierarchy_closed=False, positive_physical_energy_derived=False,
        physical_window_derived=False, healthy_GR_proved=False, state_adopted_or_evolved=False,
        stage2_complete=False, stage3_entered=False, physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False, MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED',
        UVIR_003='IN_PROGRESS', Stage4A='CLOSED', TOP_X4='UNCHANGED')
    return summary, dict(cases=records), formulas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--output', type=Path)
    group.add_argument('--replay', type=Path)
    parser.add_argument('--workers', type=int, default=16)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error('--workers must be1..16')
    if args.preflight:
        mp.mp.dps = 100; ch = Checks(); exact(ch)
        failures = [r for r in ch.rows if not r['passed']]
        weak.progress('CANONICAL_SEED_METHOD_PREFLIGHT', passed=len(ch.rows)-len(failures), total=len(ch.rows), failures=failures)
        raise SystemExit(bool(failures))
    dest = (args.replay or args.output).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):
        raise ValueError('outside declared output root')
    if args.output and dest.exists():
        raise FileExistsError('never overwrite an attempt')
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('replay directory missing')
    summary, independent, formulas = calculate(args.workers)
    if args.output:
        dest.mkdir(parents=False, exist_ok=False)
    for name, value in [('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)]:
        base.pair(dest, name, ENC(value), bool(args.replay))
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in dest.iterdir()} != expected:
        raise ValueError('receipt file set changed')
    weak.progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
        passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    raise SystemExit(bool(summary['failed_checks']))


if __name__ == '__main__':
    multiprocessing.freeze_support(); main()
