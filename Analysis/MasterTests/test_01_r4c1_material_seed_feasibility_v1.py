"""First material seed compatibility controls; no evolving-background clearance."""
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
PARENT = 'Analysis/MasterTests/test_01_r4c1_canonical_seed_admission_v1.py'
PSHA = '4f123be20aab9b1cd39a1fc27da8f01fd0fb66b13e1e0f7eedab4bfc6fcfb8b7'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_MATERIAL_SEED_FEASIBILITY_V1_CONTRACT_2026-10-21.md'
CSHA = '08e7acde553e54086b177ebc0c63a4b5db3ef39bb3ea9b6db75039705fb449c1'
SHA = lambda value: hashlib.sha256(value).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
TIMES = (('1e-10', '1e-12'), ('1e-14', '1e-20'))
EPS = '1e-26'

if SHA((ROOT/PARENT).read_bytes()) != PSHA:
    raise ValueError('canonical seed source changed')
spec = importlib.util.spec_from_file_location('material_seed_parent', ROOT/PARENT)
seed = importlib.util.module_from_spec(spec); spec.loader.exec_module(seed)
descriptor, body, base = seed.descriptor, seed.body, seed.base
number, small, Checks = seed.number, seed.small, seed.Checks


def sources():
    meta = seed.sources()
    pins = {PARENT: PSHA, CONTRACT: CSHA, SELF: SHA((ROOT/SELF).read_bytes()),
        'Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SEED_ADMISSION_V1_REPORT_2026-10-21.md':
        'b75fea87b5aa089b893bb8c1587e5877e7cae23186a000627aa1cb0b6e09cbc3',
        'Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SEED_ADMISSION_V1_ANALYTIC_DERIVATION_2026-10-21.md':
        '6fb146d509df555ea3d30bf3413f450634f44e29e37a18fa84b6582daec099ef',
        'Theory/Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_REPORT_2026-10-18.md':
        '7237b9649f08fe16746660415f418dd93b0268b81edb0871e6105abdca7c47ef',
        'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CONSTRAINT_V1_REPORT_2026-10-18.md':
        '44113ba26531526435206a520495e56e5d57cae3c8e6843595a0dc871d9dd305'}
    for name, want in pins.items():
        path = ROOT/name; side = Path(str(path)+'.sha256')
        if SHA(path.read_bytes()) != want or side.read_text().split()[0].lower() != want:
            raise ValueError('source/sidecar drift: '+name)
        meta['pins'][name] = want
        for f in (path, side):
            meta['records'][f.relative_to(ROOT).as_posix()] = base.metadata(f)
    return meta


def exact(ch):
    t, s, Z = sy.symbols('t s Z', real=True)
    p = sy.Symbol('p', positive=True)
    f, force, pdot, sdot, zdot = sy.symbols('f F Pdot sdot zdot', real=True)
    P, J, gr = [sy.Function(x)(t) for x in ('P', 'J', 'rho_z')]
    W = sy.Function('W')(s, Z, t)
    radial_rate = P/(J*s)+W*gr
    dt = lambda expression: sy.diff(expression, t)+sdot*sy.diff(expression, s)+zdot*sy.diff(expression, Z)
    initial = {P: 0, gr: 0, sy.diff(gr, t): 0, sy.diff(P, t): pdot, J: 1, s: p}
    ds = sy.simplify(dt(sy.diff(radial_rate, s)).subs(initial, simultaneous=True))
    dz = sy.simplify(dt(sy.diff(radial_rate, Z)).subs(initial, simultaneous=True))
    ch.add('full_shift_kept_material_s_identity', sy.simplify(ds+pdot/p**2) == 0)
    ch.add('full_shift_kept_material_Z_identity', dz == 0)
    ch.add('actual_radial_rate_initially_zero', radial_rate.subs({P: 0, gr: 0}, simultaneous=True) == 0)
    material = (ds*f-force*f/p**3).subs(pdot, -force/p)
    ch.add('first_material_s_cancellation', sy.simplify(material) == 0)
    ch.add('frozen_term_alone_is_not_zero', -force*f/p**3 != 0)
    ch.add('background_derivative_cannot_be_omitted', sy.simplify((ds*f).subs(pdot, -force/p)-force*f/p**3) == 0)
    rho, j, w, zeta, m2, l4, l6, cutoff, gc, rr = sy.symbols('rho j w zeta m2 l4 l6 cutoff gr rres', nonzero=True, real=True)
    V = m2*rho**2/2+l4*rho**4/8+l6*rho**6/(24*cutoff**2)+gc*rho**2*rr**2/4
    phase_energy = j*j/(2*rho*rho*(1-zeta*rho*rho*w*w))
    F = sy.diff(V+phase_energy, rho)
    expected = m2*rho+l4*rho**3/2+l6*rho**5/(4*cutoff**2)+gc*rho*rr**2/2-j*j*(1-2*zeta*rho*rho*w*w)/(rho**3*(1-zeta*rho*rho*w*w)**2)
    ch.add('bulk_force_derived_before_fixing_rho_or_eta', sy.cancel(F-expected) == 0)
    ch.add('local_phase_density_retained', sy.diff(F, j) != 0)
    # Three-point exact fixed-charge projection, independent of field sampling.
    dd = sy.symbols('d0:3'); residual = sy.symbols('r0:3')
    av = lambda seq: sum(seq)/len(seq)
    projected = [x-av(dd) for x in dd]
    clock = sy.Symbol('exp_beta_tau', positive=True)
    ch.add('dust_contrast_exactly_preserves_charge', sy.simplify(av(projected)) == 0)
    changed = [r+clock*d/p**2 for r, d in zip(residual, projected)]
    ch.add('dust_contrast_cannot_change_mean_defect', sy.simplify(av(changed)-av(residual)) == 0)
    correction = [-p*p*(r-av(residual))/clock for r in residual]
    ch.add('zero_mean_defect_lift_leaves_mean_equation', all(sy.simplify(r+clock*d/p**2-av(residual)) == 0 for r, d in zip(residual, correction)))
    uniform = sy.Symbol('constant_contrast')
    ch.add('uniform_contrast_is_chart_null', all(x.subs({d: uniform for d in dd}) == 0 for x in projected))
    # Node movement acts on Phi[u], which vanishes identically for this seed;
    # it is not a general assumption of stationary nodes or zero background drift.
    z, speed = sy.symbols('z speed', real=True)
    zero = sy.Integer(0)
    ch.add('seed_node_transport_term_accounted', speed*sy.diff(zero, z) == 0)
    ch.add('seed_node_first_jet_transport_accounted', speed*sy.diff(zero, z, 2) == 0)
    return dict(
        radial_velocity='delta H/dP_rho=P_rho/(J*s)+W*D rho, full restored W retained',
        initial_structure='P_rho=D rho=T_rho=D T_rho=0; action parameters held fixed',
        force='V_rho-j(z)^2*(1-2*zeta*rho^2*w^2)/(rho^3*(1-zeta*rho^2*w^2)^2)',
        momentum_rate='T_P_rho=-F_rho/p', material_partial_s='-T_P_rho*f/p^2',
        frozen_next_s='-F_rho*f/p^3', material_sum_s='0', material_sum_cross_corrected_Z='0',
        node_jets='Phi[u] identically zero; moving-node terms vanish specifically for this initial seed',
        clock='Explicit global force-clock tangent tau_dot=1 included; perturbation tau stays fixed',
        dust_defect='Delta R_s=exp(beta*tau)*Delta P_dust/p^2 for mean-zero contrast; mean residual unchanged',
        known_initial_construction='Inherited from certified INITIAL-ADMISSION-V1, not rerun or newly completed',
        scope='FIRST_DIRECTIONAL_MATERIAL_COMPATIBILITY_ONLY; no evolution or complete higher hierarchy',
        physics_pass=False)


def maximum(values):
    return max((abs(x) for x in values), default=mp.mpf(0))


def relative_vectors(a, b):
    return maximum([x-y for x, y in zip(a, b)])/(1+maximum(a)+maximum(b))


def fresh_temporal(X, raw):
    """Rebuild the UNSPECIALIZED temporal matrix at the changed point."""
    restored = body.restore(X, raw); matrices = []; ys = []; error = mp.mpf(0)
    for i, (q, p, dq) in enumerate(zip(restored['q'], restored['p'], restored['dq'])):
        s = X['Q'][i][11]; zero = [mp.mpf(0)]*12
        _, ell = body.local_derivatives(q, dq, zero, s, raw['par'])
        columns = []
        for j in range(12):
            unit = zero.copy(); unit[j] = mp.mpf(1)
            _, derivative = body.local_derivatives(q, dq, unit, s, raw['par'])
            columns.append([derivative[k]-ell[k] for k in range(12)])
        matrix = body.trans(columns); matrices.append(matrix)
        volume = body.geometry(q, dq)[3]
        P = [2*x for x in p[:6]]+p[6:12]
        velocity = list(mp.lu_solve(mp.matrix(matrix), mp.matrix([a/volume-b for a, b in zip(P, ell[:12])])))
        ys.append(velocity)
        _, got = body.local_derivatives(q, dq, velocity, s, raw['par'])
        error = max(error, relative_vectors(got[:12], [v/volume for v in P]))
    changed = dict(raw, Rs=matrices)
    return changed, ys, descriptor.functional(X, changed, ys), error


def phi(X, raw, covector):
    """Full state-dependent cross correction, not the flat-background B."""
    n = raw['n']; vel = descriptor.zeros(n)
    for i in range(n):
        vel['Q'][i][:10] = [n*x for x in covector['P'][i]]
    vel['M'] = covector['PM'].copy(); vel = descriptor.project(vel, raw)
    q = body.coordinates(X, raw); corrected = []; gvals = []
    for i, qi in enumerate(q):
        h = body.tensor(qi); hi = body.inv3(h); V = qi[6:9]
        volume = body.sqrt(body.det3(h)); hv = body.mv(h, V); c = body.dot(V, hv)
        vi = vel['Q'][i]
        dh = body.tensor([vi[0], vi[1], vel['M'][0], vi[2], vel['M'][1], vel['M'][2]])
        dg = raw['par']['b']*volume*(c*body.tr(body.mm(hi, dh))/2+2*body.dot(vi[3:6], hv)+body.dot(V, body.mv(dh, V)))
        corrected.append(n*covector['Q'][i][10]-X['Q'][i][11]*dg)
        gvals.append(raw['par']['b']*volume*c)
    return [[n*r[11] for r in covector['Q']], corrected], gvals


def force_profile(raw, out):
    par = raw['par']; result = []
    for q, mom in zip(out['q'], out['p']):
        rho = mp.sqrt(q[9]**2+q[10]**2); j = q[9]*mom[10]-q[10]*mom[9]; w = q[7]
        Vp = par['m2']*rho+par['lambda4']*rho**3/2+par['lambda6']*rho**5/(4*par['Lambda']**2)+par['g_r']*rho*q[11]**2/2
        den = 1-par['zeta']*rho*rho*w*w
        result.append(Vp-j*j*(1-2*par['zeta']*rho*rho*w*w)/(rho**3*den*den))
    return result


def dust_control(ch, X, raw, y0, out, T, gradient):
    n, p = raw['n'], raw['rate']
    delta = [mp.mpf('1e-9')*(mp.cos(2*t)+mp.sin(t)/7) for t in raw['theta']]
    average = body.mean(delta); delta = [v-average for v in delta]
    Y = descriptor.combine(X, descriptor.zeros(n))
    for row, value in zip(Y['P'], delta): row[9] += value
    rr, yy, oo, err = fresh_temporal(Y, raw)
    small(ch, 'dust_control_fresh_stationarity', err)
    TY = descriptor.background(Y, rr, yy, oo)
    gy = descriptor.gradient(Y, rr, yy)
    old = descriptor.combine(descriptor.omega(X, raw, T), gradient, -1)
    new = descriptor.combine(descriptor.omega(Y, rr, TY), gy, -1)
    actual = [n*(a[11]-b[11]) for a, b in zip(new['Q'], old['Q'])]
    predicted = [v/p**2 for v in delta]
    small(ch, 'full_functional_mean_zero_dust_defect_identity', relative_vectors(actual, predicted), '1e-40')
    small(ch, 'dust_control_mean_defect_unchanged', abs(body.mean(actual)), '1e-40')
    small(ch, 'dust_control_Z_defect_unchanged', maximum([n*(a[10]-b[10]) for a, b in zip(new['Q'], old['Q'])]), '1e-40')
    U = descriptor.combine(X, descriptor.zeros(n))
    for row in U['P']: row[9] += mp.mpf('1e-9')
    constant = body.restore(U, raw)
    small(ch, 'constant_dust_contrast_chart_null', maximum([a[14]-b[14] for a, b in zip(constant['p'], out['p'])]), '1e-70')
    return dict(delta=[number(v) for v in delta], measured_change=[number(v) for v in actual],
        predicted_change=[number(v) for v in predicted], mean_change=number(body.mean(actual)),
        temporary_algebra_control_only=True, original_state_unchanged=True, physical_candidate_adopted=False)


def grid_job(task):
    index, point, initial, offset = task; ch = Checks()
    try:
        raw, X = body.build_data(point, initial, 17, offset, 100)
        y0, error = body.baseline(raw, X); out = descriptor.functional(X, raw, y0)
        small(ch, 'original_stationarity', error)
        T = descriptor.background(X, raw, y0, out)
        # Original temporal formulation has explicit force clock tau_dot=1.
        # This tangent is not integrated and does not modify the frozen module.
        T['tau'] = mp.mpf(1)
        gradient = descriptor.gradient(X, raw, y0)
        force = force_profile(raw, out); p = raw['rate']; n = raw['n']
        small(ch, 'original_functional_full_radial_force', relative_vectors([r[6] for r in T['P']], [-F/p for F in force]))
        small(ch, 'structural_amplitude_rate_zero', maximum([r[6] for r in T['Q']]))
        small(ch, 'structural_amplitude_rate_spatial_derivative_zero', maximum(body.Dmul(raw['D'], [r[6] for r in T['Q']])) )
        speed = -T['Q'][0][4]/out['dq'][0][7]
        shift, C = seed.effective_shift(raw, out, y0)
        profiles = []
        for name in ('constant', 'sin'):
            u, f = seed.seed(raw, name); expected_seed, image = seed.expected_seed(raw, shift, f)
            K, _, drift = seed.full_action(X, raw, y0, out, T, u, mp.mpf(EPS))
            Ka, _, image_drift = seed.full_action(X, raw, y0, out, T, image, mp.mpf(EPS))
            small(ch, name+'_original_entire_seed_identity', descriptor.relative(K, expected_seed))
            small(ch, name+'_seed_drift_verified_zero', descriptor.norm(drift))
            small(ch, name+'_image_drift_verified_zero', descriptor.norm(image_drift))
            Phi, _ = phi(X, raw, K); nextPhi, _ = phi(X, raw, Ka)
            predicted_dt = [[-r[6]*v/p**2 for r, v in zip(T['P'], f)], [mp.mpf(0)]*n]
            predicted_next = [[-F*v/p**3 for F, v in zip(force, f)], [mp.mpf(0)]*n]
            for j in range(2):
                small(ch, name+'_bulk_next_auxiliary_'+str(j), relative_vectors(nextPhi[j], predicted_next[j]))
                small(ch, name+'_seed_entire_auxiliary_zero_'+str(j), maximum(Phi[j]))
            ch.add(name+'_frozen_next_s_cannot_be_erased', bool(abs(nextPhi[0][0]) > 1), number(nextPhi[0][0]))
            steps = []
            for hs, tolerance in TIMES:
                h = mp.mpf(hs); varied = []
                for sign in (-1, 1):
                    Y = descriptor.combine(X, T, sign*h)
                    rr, yy, oo, stationarity = fresh_temporal(Y, raw)
                    small(ch, name+'_'+hs+'_'+str(sign)+'_changed_original_stationarity', stationarity)
                    HY = descriptor.hvp(Y, rr, yy, oo, u, mp.mpf(EPS))
                    fields, gg = phi(Y, rr, HY); varied.append(fields)
                    method = seed.weak.directions(rr)[0]
                    test, _ = phi(Y, rr, descriptor.omega(Y, rr, method))
                    projected = descriptor.project(method, rr)
                    expected = [[-g*r[10] for g, r in zip(gg, projected['Q'])], [g*r[11] for g, r in zip(gg, projected['Q'])]]
                    for j in range(2): small(ch, name+'_'+hs+'_'+str(sign)+'_general_B_identity_'+str(j), relative_vectors(test[j], expected[j]))
                dt = [[(a-b)/(2*h) for a, b in zip(plus, minus)] for plus, minus in zip(varied[1], varied[0])]
                material = [[a+b for a, b in zip(d, nxt)] for d, nxt in zip(dt, nextPhi)]
                errors = []; slope_errors = []; node_values = []; node_slopes = []
                for j in range(2):
                    small(ch, name+'_'+hs+'_independent_time_derivative_'+str(j), relative_vectors(dt[j], predicted_dt[j]), tolerance)
                    relative = maximum(material[j])/(1+maximum(dt[j])+maximum(nextPhi[j]))
                    small(ch, name+'_'+hs+'_material_value_'+str(j), relative, tolerance); errors.append(number(relative))
                    d_dt, d_next = body.Dmul(raw['D'], dt[j]), body.Dmul(raw['D'], nextPhi[j])
                    slope = [a+b for a, b in zip(d_dt, d_next)]
                    relative_slope = maximum(slope)/(1+maximum(d_dt)+maximum(d_next))
                    small(ch, name+'_'+hs+'_material_spatial_jet_'+str(j), relative_slope, tolerance); slope_errors.append(number(relative_slope))
                    DPhi = body.Dmul(raw['D'], Phi[j]); DDPhi = body.Dmul(raw['D'], DPhi)
                    node_values.append(number(material[j][0]+speed*DPhi[0]))
                    node_slopes.append(number(slope[0]+speed*DDPhi[0]))
                steps.append(dict(time_step=hs, frozen_tolerance=tolerance, material_value_errors=errors,
                    material_first_jet_errors=slope_errors, material_values=[list(map(number, a)) for a in material],
                    actual_partial_time=[list(map(number, a)) for a in dt], node_material_values=node_values,
                    node_material_first_jets=node_slopes, background_curve='X+/-h*T directional control ONLY, NOT an evolving solution'))
            profiles.append(dict(profile=name, force=[number(x) for x in force],
                predicted_partial_time=[list(map(number, a)) for a in predicted_dt],
                actual_frozen_next=[list(map(number, a)) for a in nextPhi], steps=steps))
        defect = descriptor.combine(descriptor.omega(X, raw, T), gradient, -1)
        dust = dust_control(ch, X, raw, y0, out, T, gradient)
        result = dict(family=point['family'], eta=point['eta'], grid=17, node_orientation=offset,
            profiles=profiles, dust_control=dust, node_speed=number(speed),
            transverse_node_rates=[number(T['Q'][0][j]) for j in (3, 5)],
            background_s_defect=[number(n*r[11]) for r in defect['Q']],
            background_Z_defect=[number(n*r[10]) for r in defect['Q']], global_clock_row_separate=number(defect['tau']),
            exact_implicit_initial_construction='INHERITED_NOT_RERUN', exported_background_admission_certified=False,
            physical_state_adopted_or_evolved=False, full_material_hierarchy_closed=False)
    except Exception:
        ch.add('unexpected_case_exception', False, traceback.format_exc())
        result = dict(family=point['family'], eta=point['eta'], node_orientation=offset, incomplete=True)
    return (index, offset), result, ch.rows


def calculate(workers):
    mp.mp.dps = 100
    before = sources(); ch = Checks(); formulas = exact(ch)
    points = body.lift.READ(body.nodal.reg.JOINT+'independent.json'); initial = body.lift.READ(body.lift.cop.CERTS)
    if len(points) != 9 or len(initial) != 9 or any(a['family'] != b['family'] or a['eta'] != b['eta'] for a, b in zip(points, initial)):
        raise ValueError('original input order changed')
    selected = [(i, a, b) for i, (a, b) in enumerate(zip(points, initial)) if a['eta'] == '1/4']
    if len(selected) != 3:
        raise ValueError('representative cases not found')
    tasks = [(i, a, b, o) for i, a, b in selected for o in (0, 1)]
    seed.weak.progress('MATERIAL_SEED_FEASIBILITY_TASKS', tasks=len(tasks), workers=workers)
    results = {}
    if workers == 1:
        for task in tasks:
            key, record, rows = grid_job(task); results[key] = record, rows
            seed.weak.progress('CASE_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    else:
        with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
            for future in as_completed([pool.submit(grid_job, task) for task in tasks]):
                key, record, rows = future.result()
                if key in results: raise ValueError('duplicate case')
                results[key] = record, rows
                seed.weak.progress('CASE_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    records = []
    for key in sorted(results):
        record, rows = results[key]; records.append(record)
        for row in rows: ch.add(str(key)+'_'+row['name'], row['passed'], row.get('value'), row.get('criterion'))
    ch.add('all6_cases_and_two_profiles_complete', len(records) == 6 and all(not r.get('incomplete') and len(r['profiles']) == 2 for r in records))
    if sources() != before: raise ValueError('source/native metadata changed')
    failed = [r for r in ch.rows if not r['passed']]
    summary = dict(validation='FIRST_MATERIAL_SEED_IDENTITIES_VERIFIED' if not failed else 'MATERIAL_SEED_FEASIBILITY_UNRESOLVED',
        passed=len(ch.rows)-len(failed), total=len(ch.rows), failed_checks=failed, unknown_checks=[], checks=ch.rows,
        source_metadata=before, scope='Initial first directional material seed balance; analytic proof in owning report; representative controls only',
        full_initial_data_admission_proved=False, physical_evolving_background_admitted=False, domain_persistence_proved=False,
        higher_auxiliary_hierarchy_closed=False, physical_energy_or_window_derived=False, physical_state_adopted_or_evolved=False,
        stage2_complete=False, stage3_entered=False, physics_pass=False, gate_effect='NONE', review_status='DEFERRED', Rule9_cleared=False,
        MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED', UVIR_003='IN_PROGRESS', Stage4A='CLOSED', TOP_X4='UNCHANGED')
    return summary, dict(cases=records), formulas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--output', type=Path)
    group.add_argument('--replay', type=Path)
    parser.add_argument('--workers', type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 6: parser.error('--workers must be1..6')
    if args.preflight:
        mp.mp.dps = 100; ch = Checks(); exact(ch)
        failed = [r for r in ch.rows if not r['passed']]
        seed.weak.progress('MATERIAL_METHOD_PREFLIGHT', passed=len(ch.rows)-len(failed), total=len(ch.rows), failures=failed)
        raise SystemExit(bool(failed))
    dest = (args.output or args.replay).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'): raise ValueError('outside declared output root')
    if args.output and dest.exists(): raise FileExistsError('never overwrite an attempt')
    if args.replay and not dest.is_dir(): raise FileNotFoundError('missing replay directory')
    summary, independent, formulas = calculate(args.workers)
    if args.output: dest.mkdir(parents=False, exist_ok=False)
    for name, value in [('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)]:
        base.pair(dest, name, ENC(value), bool(args.replay))
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in dest.iterdir()} != expected: raise ValueError('receipt set changed')
    seed.weak.progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
        passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    raise SystemExit(bool(summary['failed_checks']))


if __name__ == '__main__':
    multiprocessing.freeze_support(); main()
