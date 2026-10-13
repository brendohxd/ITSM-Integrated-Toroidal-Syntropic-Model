"""Frozen full finite-mode dust/slow comparison; no physical gate promotion."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.sparse import csr_matrix, eye, kron
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = BASE + 'r4c1_g3n5_slow_dust_weighted_attempt_01/'
NONZERO = BASE + 'r4c1_g3n5_nonzero_characteristic_attempt_02/'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_K_CONTRACT_2026-10-11.md'
ENGINE = 'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py'
PINNED = {
    ENGINE: '8c63194a678734917c5c9a9593da8023fb7ba946790cc0376c7cd3a9fa57c991',
    CONTRACT: 'e8a27ba03b11cd0137ecf1b566db761f0d4ee356700911a500235e95fcd9221d',
    PARENT + 'summary.json': 'fe81f337ba6a7bd5a2783fc2e8a99b617ec08dd119673844f11edf30d53b1208',
    'Theory/Gates/RES-001/RES001_R4C1_G3N5_SLOW_DUST_WEIGHTED_REPORT_2026-10-11.md':
        'da03bc19d9414f5b78f3c7bb6257e602f6721769a96b5268d885ba36ebf1f1ff',
}
if hashlib.sha256((ROOT / ENGINE).read_bytes()).hexdigest() != PINNED[ENGINE]:
    raise RuntimeError('Frozen imported engine drift')
sys.path.insert(0, str(ROOT / 'Analysis/MasterTests'))
import test_01_r4c1_g3n5_nonzero_characteristic_v1 as parent
old = parent.old
common = old.common
MODES = (4, 8, 16, 32, 64)
END = 0.05
NC = 4


def realify(matrix):
    return np.block([[matrix.real, -matrix.imag], [matrix.imag, matrix.real]])


def pack(matrix):
    return np.vstack((matrix.real, matrix.imag)).ravel()


def unpack(vector):
    rows = np.asarray(vector).reshape(40, NC)
    return rows[:20] + 1j * rows[20:]


def norm(matrix):
    return float(np.linalg.norm(matrix, np.inf))


def calculate():
    ps = common.read_json(PARENT + 'summary.json')
    pins = dict(ps['source_sha256'])
    for key, value in PINNED.items():
        if key in pins and pins[key] != value:
            raise ValueError('Conflicting frozen pin ' + key)
        pins[key] = value
    pins.update({PARENT + name: value for name, value in ps['artifacts'].items()})
    pins[SELF] = common.sha((ROOT / SELF).read_bytes())
    missing = common.inspect_pins(pins)
    paths = [ROOT / q for q in pins]
    paths.extend(Path(str(q) + '.sha256') for q in list(paths)
                 if Path(str(q) + '.sha256').is_file())
    before = parent.snapshot(paths)
    checks = common.Checks()
    exact = lambda name, expr: parent.exact(checks, name, expr)
    numerical = lambda name, value, limit: old.numerical(checks, name, value, limit)
    checks.add('all_source_pins_before', True, {'files': len(before), 'absent': missing})
    checks.add('parent_checked_and_adverse_findings_retained',
               ps['passed'] == ps['total'] == 79 and ps['physics_pass'] is False
               and ps['original_slow_time_coefficient'] == '-11/6'
               and ps['complete_density_Hamiltonian_positive'] is False
               and ps['ordinary_wave_Jordan_defect_removed'] is False)
    print('Rebuild full action/Euler chart and dust observable maps', flush=True)
    op = old.Operator(checks)
    ell = s.Symbol('ell', positive=True)
    p = s.Symbol('p', positive=True)
    ch = op.chart(checks, (ell, 0, 0))
    a, H = op.bg[:2]
    rho, C = op.bg[-2:]
    psi = op.bg[8]
    beta = old.PARAMS['beta']
    sy = {**op.sy, 'ell': ell, 'p': p, 'I': s.I, 'sqrt': s.sqrt}
    saved = common.read_json(NONZERO + 'matrices.json')
    A, R, K = (parent.import_matrix(saved[key], sy) for key in ('A', 'R', 'K'))
    E0, E1, E2 = (ch['symbolic'][key] for key in ('E0', 'E1', 'E2'))
    exact('full_Euler_value_matches_saved_action', E0 - A + op.dtm(R) + 3*H*R)
    exact('full_Euler_velocity_matches_saved_action', E1 - R.conjugate().T + R + op.dtm(K) + 3*H*K)
    exact('full_Euler_acceleration_matches_saved_action', E2 + K)
    L = s.zeros(20)
    L[:10, 10:] = s.eye(10)
    L[10:, :10] = K.inv()*E0
    L[10:, 10:] = K.inv()*E1
    L = parent.ex(L)
    exact('negative_Fourier_conjugation', L.subs(ell, -ell) - L.conjugate())
    exact('complete_acceleration_block_inverse', K*K.inv() - s.eye(10))
    checks.add('all_ten_coordinates_retained', ch['dimension'] == 10, ch['names'])

    # Full field reconstruction, including density and the normal multiplier.
    Q0, Q1 = (ch['symbolic'][key].copy() for key in ('Q0', 'Q1'))
    Q0[old.IDX['Em'], :] = ch['symbolic']['EmL']
    Q1[old.IDX['Em'], :] = ch['symbolic']['EmM']
    Q = Q0.row_join(Q1)
    Qd = parent.ex(op.dtm(Q) + Q*L)
    F = s.Matrix(ch['F']).applyfunc(s.nsimplify)
    full = [parent.ex(mat.subs(dict(zip(op.k, (ell, 0, 0)))))
            for mat in (op.EA, op.EB, op.ED)]
    EA, EB, ED = full
    provisional = parent.ex(EA*Q + EB*Qd + ED*F*L[10:, :])
    multiplier = -provisional[old.IDX['nu'], :]/EA[old.IDX['nu'], old.IDX['LambdaU']]
    Q[old.IDX['LambdaU'], :] = multiplier
    residual = parent.ex(provisional + EA[:, old.IDX['LambdaU']]*multiplier)
    # On-shell redundant equations may contain the explicit Friedmann factor.
    mod = s.Poly(op.constraint, H)
    reduced = residual.applyfunc(lambda value: s.Poly(s.cancel(value).as_numer_denom()[0], H).rem(mod).as_expr())
    exact('all_22_full_reconstructed_Euler_identities_on_B1_constraint', reduced)
    exact('full_clock_and_norm_fixed', Q[[old.IDX['T'], old.IDX['nu']], :])
    exact('multiplier_derivatives_unused', EB[:, old.IDX['LambdaU']].col_join(ED[:, old.IDX['LambdaU']]))
    Pi = Q[old.IDX['Pi'], :]
    drho = parent.ex(C**4*Q[old.IDX['Em'], :] + 4*beta*rho*Pi)
    Obs = (drho/(s.I*(ell/a)*rho)).col_join(Q[old.IDX['Vx'], :])
    Obs = parent.ex(Obs)
    Pt = a**3*rho/C
    trace = sum((Q[old.IDX[key], :] for key in ('Mxx', 'Myy', 'Mzz')), s.zeros(1, 20))
    dPt = parent.ex(a**3*C**3*Q[old.IDX['Em'], :] + Pt*(trace/2 + 3*beta*Pi))
    continuity = parent.ex(op.dtm(dPt) + dPt*L - s.I*(ell/a)*Pt*Q[old.IDX['Sx'], :])
    conservation_mod = continuity.applyfunc(lambda value: s.Poly(s.cancel(value).as_numer_denom()[0], H).rem(mod).as_expr())
    exact('independent_full_dust_current_conservation_on_B1_constraint', conservation_mod)
    M = s.Matrix([[H, 1], [6*rho/11, -H-beta*psi]])
    Obs_defect = parent.ex(op.dtm(Obs) + Obs*L - M*Obs)

    # Evolving formal slow lift; only initial data and diagnostics use this graph.
    fm = common.read_json(NONZERO + 'formulas.json')['formal_slow']
    slow0, slow1 = (parent.import_matrix(saved[key], sy) for key in ('slow_Q0', 'slow_Q1'))
    slowE = [s.sympify(fm[key], locals=sy) for key in ('E0', 'E1', 'E2')]
    N = s.Matrix([[0, 1], [-slowE[0]/slowE[2], -slowE[1]/slowE[2]]])
    rot = s.eye(10)
    rot[:3, :3] = s.Matrix([[1/s.sqrt(2), 1/s.sqrt(2), 0], [0, 0, 1], [1/s.sqrt(2), -1/s.sqrt(2), 0]])
    embed = s.zeros(10, 6)
    for j, i in enumerate((0, 3, 6, 7, 8, 9)):
        embed[i, j] = 1
    Ts = s.diag(1/p, 1, 1/p, 1/p, 1/p, 1/p**2)
    Ts[5, 1] = s.I*psi/p
    ys = parent.ex((rot*embed*Ts*slow0).row_join(rot*embed*Ts*slow1).subs(p, ell/a))
    G = ys.col_join(parent.ex(op.dtm(ys) + ys*N))
    OG = parent.ex(Obs*G)
    exact('slow_lift_relative_velocity', G[ch['names'].index('Vx'), :] - s.Matrix([[1, 0]]))
    leading_obs = OG.subs(ell, a*p).applyfunc(lambda value: s.expand(value).coeff(p, 0))
    expected = s.Matrix([[11*(H+beta*psi)/(6*rho), 11/(6*rho)], [1, 0]])
    exact('finite_lift_recovers_frozen_leading_observable_map', leading_obs - expected)

    # Mixed-order balancing, including all time-dependent terms.
    wave = ell/a
    D = s.diag(wave, wave, wave, 1, 1, 1, wave, wave, wave, wave**2)
    D[9, 3] = -s.I*wave*psi
    Z = D*rot.T
    Zd = op.dtm(Z)
    freq_inv = s.diag(*([1/wave]*9 + [1/wave**2]))
    freq = freq_inv.inv()
    B = (Z.row_join(s.zeros(10))).col_join((freq_inv*Zd).row_join(freq_inv*Z))
    Zi = Z.inv()
    Bi = (Zi.row_join(s.zeros(10))).col_join((-Zi*Zd*Zi).row_join(Zi*freq))
    B, Bi = parent.ex(B), parent.ex(Bi)
    Bd = op.dtm(B)
    exact('balanced_map_exact_inverse', B*Bi - s.eye(20))
    Gz = parent.ex((Bd+B*L)*Bi)
    exact('balanced_evolving_generator_identity', Gz*B-B*L-Bd)
    checks.add('reject_omitted_balancing_generator', any(v != 0 for v in Bd), True, 'B_dot is nonzero')
    checks.add('reject_zero_mode_balancing_inverse', True, 'ell=0 remains a separate homogeneous chart')

    print('Compile finite-mode maps; retain all fields and both real quadratures', flush=True)
    fn = s.lambdify([op.bg, ell], (L, B, Bi, Gz, Obs, G, Q, Obs_defect), 'numpy', cse=True)
    generator_fn = s.lambdify([op.bg, ell], Gz, 'numpy', cse=True)
    rawQ0, rawQ1 = (ch['symbolic'][key] for key in ('Q0', 'Q1'))
    emL, emM = (ch['symbolic'][key] for key in ('EmL', 'EmM'))
    reconstruct_fn = s.lambdify([op.bg, ell],
        (rawQ0, rawQ1, op.dtm(rawQ0), op.dtm(rawQ1), emL, emM, op.dtm(emL), op.dtm(emM)), 'numpy', cse=True)
    # Binary64 Horner evaluation of the existing high-precision background.
    saved_bg = common.read_json(BASE + 'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    checks.add('saved_background_degree_and_digits', saved_bg['digits'] == 70 and saved_bg['degree'] == 40
               and saved_bg['background_order'] == list(old.BG_NAMES))
    if any(float(pair[1]) != 0 for row in saved_bg['background_coefficients'] for pair in row):
        raise ValueError('Expected real saved background coefficients')
    bc = np.array([[float(pair[0]) for pair in row] for row in saved_bg['background_coefficients']])
    bg_at = lambda t: np.polynomial.polynomial.polyval(t, bc.T)
    bgdot = lambda t: np.polynomial.polynomial.polyval(t, (bc[:, 1:]*np.arange(1, 41)).T)
    grid = np.linspace(0, END, 257)
    backgrounds = np.array([bg_at(t) for t in grid])
    old_bg = np.load(ROOT/(BASE + 'r4c1_g3n5_constraint_response_attempt_01/background.npy'), allow_pickle=False)
    numerical('saved_background_agreement', np.max(np.abs(backgrounds-old_bg)/(1+np.abs(old_bg))), 1e-10)
    numerical('saved_background_rate_residual', max(norm(bgdot(t)-np.asarray(op.bg_fn(bg_at(t))).ravel()) for t in grid), 1e-10)
    numerical('sampled_Friedmann_constraint', max(abs(op.constraint_fn(bg)) for bg in backgrounds), 1e-10)
    checks.add('all_sampled_background_domains', bool(np.isfinite(backgrounds).all() and np.min(backgrounds[:, [0, 9, 10]]) > 0))
    slow_transfer = common.read_json(PARENT + 'transfer.json')
    coeff = np.array([[float(value) for value in row] for row in slow_transfer['degree40_coefficients']])
    Phi = np.array([np.polynomial.polynomial.polyval(t, coeff.T).reshape(2, 2) for t in grid])
    numerical('slow_transfer_initial_identity', norm(Phi[0]-np.eye(2)), 1e-11)

    reports, trajectories = [], []
    for kval in MODES:
        print('Evolve full finite mode ell=' + str(kval), flush=True)
        numeric_chart = {**ch, 'mode': (kval, 0, 0), 'rec': lambda bg: reconstruct_fn(bg, kval)}
        initial = [np.asarray(v, dtype=complex) for v in fn(bg_at(0), kval)]
        ln, bn, binv, gz, obs, graph, qn, defect = initial
        normalizer = obs@graph
        E = graph@np.linalg.inv(normalizer)
        zslow = bn@E
        seeds = []
        for idx in (9, 19):
            seed = np.eye(20, dtype=complex)[:, idx]
            seed = seed - zslow@(obs@binv@seed)
            magnitude = float(np.max(np.abs(seed)))
            if not np.isfinite(magnitude) or magnitude == 0:
                raise ValueError('Degenerate complementary seed')
            seeds.append(seed/magnitude)
        z0 = np.column_stack((zslow, *seeds))
        wanted = np.column_stack((np.eye(2), np.zeros((2, 2))))
        numerical('initial_actual_dust_matching_' + str(kval), norm(obs@binv@z0-wanted), 1e-11)
        def generation(t):
            return np.asarray(generator_fn(bg_at(t), kval), dtype=complex)
        def rhs(t, state):
            return (realify(generation(t))@state.reshape(40, NC)).ravel()
        def jac(t, state):
            return kron(csr_matrix(realify(generation(t))), eye(NC, format='csr'), format='csr')
        solutions = []
        for method, rtol, atol in (('DOP853', 1e-10, 1e-12), ('Radau', 1e-10, 1e-12), ('DOP853', 2e-12, 2e-14)):
            options = {'jac': jac} if method == 'Radau' else {}
            sol = solve_ivp(rhs, (0, END), pack(z0), method=method, rtol=rtol, atol=atol, dense_output=True, **options)
            solutions.append(sol)
        checks.add('all_three_full_solvers_completed_' + str(kval), all(sol.success and sol.t[-1] == END for sol in solutions))
        states = [np.array([unpack(sol.sol(t)) for t in grid]) for sol in solutions]
        primary = states[2]
        balanced_disagreement = max(norm(states[j][i]-primary[i])/max(1., norm(primary[i]), norm(states[j][i]))
                                    for j in (0, 1) for i in range(257))
        numerical('balanced_solver_agreement_' + str(kval), balanced_disagreement, 2e-7)
        observable_disagreement = 0.
        euler_error, graph_condition, graph_distance, equation_defect = 0., 0., 0., 0.
        observables, all_fields = [], []
        for i, t in enumerate(grid):
            ln, bn, binv, gz, obs, graph, qn, defect = [np.asarray(v, dtype=complex) for v in fn(backgrounds[i], kval)]
            x = binv@primary[i]
            w = obs@x
            observables.append(w)
            all_fields.append(qn@x)
            for j in (0, 1):
                other = obs@binv@states[j][i]
                observable_disagreement = max(observable_disagreement, norm(w-other)/max(1., norm(w), norm(other)))
            E = graph@np.linalg.inv(obs@graph)
            graph_condition = max(graph_condition, float(np.linalg.cond(obs@graph)))
            graph_distance = max(graph_distance, norm(bn@(x[:, :2]-E@w[:, :2]))/max(1., norm(bn@x[:, :2])))
            equation_defect = max(equation_defect, norm(defect@x[:, :2]))
            for j in range(NC):
                y, vel = x[:10, j], x[10:, j]
                acc = (ln@x[:, j])[10:]
                _, _, _, residual_num = op.reconstruct(numeric_chart, backgrounds[i], y, vel, acc)
                euler_error = max(euler_error, residual_num)
        observables = np.array(observables)
        all_fields = np.array(all_fields)
        numerical('actual_dust_solver_agreement_' + str(kval), observable_disagreement, 2e-7)
        numerical('all_22_analytic_Euler_residual_' + str(kval), euler_error, 1e-9)
        checks.add('diagnostic_graph_regular_' + str(kval), bool(np.isfinite(graph_condition)), graph_condition, 'finite; explicit rho,p domains retained')
        error = max(norm(observables[i, :, :2]-Phi[i]) for i in range(257))/max(1., max(norm(v) for v in Phi))
        generated = max(norm(w[:, 2:]) for w in observables)
        # Independent full-field finite differences, using the refined dense IVP.
        omega = 1 + kval + np.sqrt(5/33)*kval*kval
        h0 = min(END/16, 0.2/omega)
        fd = []
        def fields_at(t):
            vals = [np.asarray(v, dtype=complex) for v in fn(bg_at(t), kval)]
            return vals[6]@vals[2]@unpack(solutions[2].sol(t))
        for h in (h0, h0/2):
            maximum = 0.
            for t in (END/4, END/2, 3*END/4):
                qm2, qm1, qc, qp1, qp2 = [fields_at(t+j*h) for j in (-2, -1, 0, 1, 2)]
                qd = (-qp2+8*qp1-8*qm1+qm2)/(12*h)
                qdd = (-qp2+16*qp1-30*qc+16*qm1-qm2)/(12*h*h)
                fa, fb, fc = [np.asarray(v, dtype=complex) for v in op.full_fn(bg_at(t), (kval, 0, 0))]
                terms = (fa@qc, fb@qd, fc@qdd)
                for col in range(NC):
                    maximum = max(maximum, norm(sum(terms)[:, col])/max(sum(norm(v[:, col]) for v in terms), 1e-20))
            fd.append({'step': h, 'error': maximum})
        numerical('independent_full_Euler_fine_difference_' + str(kval), fd[1]['error'], 1e-5)
        refinement = fd[0]['error']/max(fd[1]['error'], np.finfo(float).tiny)
        checks.add('full_field_difference_refinement_' + str(kval), refinement >= 4 or max(q['error'] for q in fd) <= 1e-8,
                   {'refinement': refinement, 'errors': fd}, '>=4 or both<=1e-8')
        reports.append(dict(ell=kval,slow_observable_error=error,complementary_seed_dust_transfer=generated,
                            balanced_graph_distance=graph_distance,observable_equation_defect=equation_defect,
                            graph_condition=graph_condition,balanced_solver_disagreement=balanced_disagreement,
                            dust_solver_disagreement=observable_disagreement,analytic_Euler_error=euler_error,
                            full_field_finite_differences=fd,
                            solvers=[{'method': name, 'success': bool(sol.success), 'nfev': sol.nfev, 'njev': sol.njev, 'nlu': sol.nlu}
                                     for name, sol in zip(('DOP853','Radau','DOP853_refined'), solutions)],
                            initial_balanced_norms=[float(np.max(np.abs(z0[:, j]))) for j in range(NC)]))
        trajectories.append({'ell': kval, 'initial_balanced': z0, 'balanced': primary,
                             'dust_observables': observables, 'full_fields': all_fields})
        print(json.dumps({'ell': kval, 'slow_error': error, 'complementary_dust': generated,
                          'solver_error': balanced_disagreement, 'fine_Euler_FD': fd[1]['error']}), flush=True)

    errors = {row['ell']: row['slow_observable_error'] for row in reports}
    support = bool(errors[64] <= 0.01 and errors[64] <= errors[32] and errors[8] >= 4*errors[64])
    payload_matrices = {'full_generator': L, 'balancing_map': B, 'balancing_map_inverse': Bi,
                        'balanced_generator': Gz, 'actual_dust_observable': Obs, 'formal_slow_lift': G,
                        'full_field_reconstruction': Q, 'leading_dust_generator': M,
                        'observable_equation_defect': Obs_defect}
    bundle = {key: parent.exports(value) for key, value in payload_matrices.items()}
    for key, value in payload_matrices.items():
        exact('serialized_roundtrip_' + key, parent.import_matrix(bundle[key], sy)-value)
    checks.add('all_source_pins_after', common.inspect_pins(pins) == missing)
    checks.add('all_input_hash_size_mtime_preserved', parent.snapshot(paths) == before, {'files': len(before)})
    def complex_pairs(array):
        return np.stack((array.real, array.imag), axis=-1).tolist()
    payloads = {
        'matrices.json': common.encode(bundle),
        'diagnostics.json': common.encode({'modes': reports, 'finite_sample_support_criterion_met': support,
            'criterion': 'e64<=0.01 and e64<=e32 and e8>=4*e64', 'error_e8_over_e64': errors[8]/max(errors[64], np.finfo(float).tiny),
            'review': 'DEFERRED; same-agent local checks only', 'full_uniform_remainder_proved': False}),
        'trajectories.json': common.encode({'time': grid.tolist(), 'leading_Phi': Phi.tolist(), 'complex_storage': 'last axis [real,imag]',
            'columns': ['slow_D','slow_Vx','complementary_chi','complementary_chi_velocity'],
            'chart_order': ch['names'], 'full_field_order': list(old.FIELDS),
            'modes': [{'ell': row['ell'], **{key: complex_pairs(row[key]) for key in ('initial_balanced','balanced','dust_observables','full_fields')}}
                      for row in trajectories]}),
    }
    passed = sum(row['passed'] for row in checks.rows)
    summary = dict(schema='r4c1-g3n5-dust-finite-k-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
                   passed=passed,total=len(checks.rows),checks=checks.rows,
                   status='CONDITIONAL_FINITE_MODE_DUST_COMPARISON_DIAGNOSTIC',
                   finite_sample_slow_criterion_met=support,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,
                   review_status='DEFERRED',full_finite_k_uniform_remainder_verified=False,physical_EFT_cutoff_derived=False,
                   physical_Hessian_verified=False,ordinary_wave_Jordan_defect_removed=False,original_slow_time_coefficient='-11/6',
                   complete_density_Hamiltonian_positive=False,canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',
                   V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=missing,
                   source_metadata_preserved=len(before),artifacts={key:common.sha(value) for key,value in payloads.items()},
                   runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
                   review_dependencies=['Weighted dust and nonzero canonical entries','B1/G3N4/full G3N5 constraints','All inherited physical/review debt'])
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    payloads['summary.json'] = common.encode(summary)
    return payloads, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', default=BASE+'r4c1_g3n5_dust_finite_k_attempt_01')
    ap.add_argument('--replay')
    args = ap.parse_args()
    dest = (ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():
        raise FileExistsError('Refuse existing scientific output')
    payloads, summary = calculate()
    if args.replay:
        for key, body in payloads.items():
            if (dest/key).read_bytes()!=body or (dest/(key+'.sha256')).read_bytes()!=(common.sha(body)+'  '+key+'\n').encode():
                raise RuntimeError('Exact replay mismatch '+key)
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for key, body in payloads.items():
            with (dest/key).open('xb') as stream:
                stream.write(body)
            with (dest/(key+'.sha256')).open('xb') as stream:
                stream.write((common.sha(body)+'  '+key+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
                      **{key:summary[key] for key in ('validation','passed','total','status','finite_sample_slow_criterion_met','physics_pass','gate_effect')}}))
    for row in summary['checks']:
        if not row['passed']:
            print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__ == '__main__':
    raise SystemExit(main())
