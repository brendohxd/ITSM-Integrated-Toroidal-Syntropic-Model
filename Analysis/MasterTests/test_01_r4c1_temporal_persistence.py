"""R4C1-S4H: moving B1 chart and symbol reconstruction, not an IVP pass.

The frozen contract requires more than this finite diagnostic. Prior modules
are imported for their read-only formulas/verifiers; no prior main is called.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s

import test_01_r4c1_order_p_symmetrizer as s4g

s4f = s4g.previous
prior, up, base = s4g.prior, s4g.up, s4g.base
ROOT, OUT, ROWS = base.ROOT, base.OUT, s4f.ROWS

PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_TEMPORAL_PERSISTENCE_CONTRACT_2026-09-29.md':
        '3bb4fa5ec045715f4667ce1260fce2a146238e45079c683ef9862260857eb26e',
    'Theory/Gates/RES-001/RES001_R4C1_ORDER_P_SYMMETRIZER_REPORT_2026-09-29.md':
        '361e3f2b2c3583e52c83164318cc511462b4e42474b3363b2ae1840f6a849bfe',
    'Analysis/MasterTests/test_01_r4c1_order_p_symmetrizer.py':
        '1e5d7c517ef1249119ed9de0bc7a94b363dcf22b0e8482ff7fe6b57ea7ae54c3',
    'Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/summary.json':
        '37530650e1f75ea22caef79b0ead1621b9866e595f89a055572a447f162d174f',
    'Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/detail.json':
        'a778e9d25e5cc4c9b9789aa55f2b2ed30242c3e213da89d6510eefc7c07b037c',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv':
        '0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa',
    'Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md':
        '48b49fddd9066d6df783eb336e00d49374f3845ec38414ee53fe0fad812348d8',
}
TIMES = (0.0, 0.5, 1.0, 2.0, 3.0, 4.0)
MODES = (1, 8, 64, 256)
REPLAY_TOLERANCE = 1e-7


def verify(audit):
    inputs = s4g.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        audit.test('S4H_pin:' + name, actual == expected, actual)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4H_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/summary.json').read_text())
    audit.test('S4H_parent_status',
               parent['validation'] == 'PASS'
               and parent['passed'] == parent['total'] == 194
               and parent['status'] == 'B1_FORMAL_BOUNDED_ENERGY_RATE_CANDIDATE'
               and parent['physics_pass'] is False
               and parent['Rule9_cleared'] is False)
    audit.test('S4H_parent_artifacts', all(
        base.sha(ROOT / name) == digest
        for name, digest in parent['artifacts'].items()))
    name, digest = next(iter(PINS.items()))
    altered = ('0' if digest[0] != '0' else '1') + digest[1:]
    audit.test('S4H_bad_pin_rejected_in_memory',
               base.sha(ROOT / name) == digest
               and base.sha(ROOT / name) != altered)
    return inputs


def exact_chart(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in
                       ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    a, H, k = base.a, base.H, base.k
    physical_p = k / a
    Fq1 = Fq.col_join(physical_p * Fq[14, :])
    Tq = Fq1.extract(ROWS, range(12))
    old_rows = tuple(old['selected_minor_rows'])
    audit.test('S4H_rows_match_S4F',
               tuple(ROWS) == (0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15)
               and old_rows == ROWS[:-1] + (14,))
    audit.exact('S4H_added_row', Fq1[15, :] - physical_p * Fq[14, :])
    audit.exact('S4H_selected_rows_replay',
                Tq[:11, :] - Fq.extract(ROWS[:-1], range(12)))
    audit.exact('S4H_selected_last_row', Tq[11, :] - physical_p * Fq[14, :])

    old_minor = s.sympify(old['original_chart_minor'], locals=prior.SYMBOLS)
    old_canonical = s.sympify(old['full_canonical_minor'],
                              locals=prior.SYMBOLS)
    sum_squares = (396*H**2*a**2 + 18*a**2*base.pd**2
                   + 6*a**2*(base.rd**2 + base.ud**2 + base.vd**2)
                   + k**2)
    explicit = (-s.sqrt(66)*k**4*sum_squares /
                (396*base.C**2*a**6*base.rho))
    audit.exact('S4H_original_minor_formula', old_minor - explicit)
    audit.exact('S4H_canonical_minor_from_R',
                old_canonical - old_minor * R.det()**2)
    audit.test('S4H_regular_domain_nonzero',
               all(coefficient > 0 for coefficient in (396, 18, 6, 1))
               and tuple(ROWS[:-1]) == old_rows[:-1],
               'On finite real fields, a,C,rho_m,H,k>0 gives '
               'p*old_minor != 0 and p*old_canonical != 0; '
               'sum_squares >= k**2>0')
    audit.exact('S4H_fixed_comoving_k_pdot',
                up.dtime(physical_p) + H * physical_p)
    audit.exact('S4H_Mcdot_retained', W - Vc - up.dtime(Mc))
    audit.test('S4H_Rdot_nonzero', any(z != 0 for z in up.dtime(R)))
    audit.test('S4H_Fdot_nonzero', any(z != 0 for z in Fdot))
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    return dict(F=F, Fdot=Fdot, A=A, old_minor=str(old_minor),
                old_canonical=str(old_canonical),
                moving_original_minor=str(s.factor(physical_p * old_minor)),
                moving_canonical_minor=str(s.factor(physical_p * old_canonical)))


def csv_rows():
    path = ROOT / 'Analysis/MasterTests/outputs/' \
           'test_01_r4c1_interacting_background_trajectory.csv'
    with path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    return rows


def matrix_at(lambdas, row, n):
    k = 2 * mp.pi * n
    C = mp.exp(mp.mpf(2) * mp.mpf(row['psi']) / 5)
    args = [mp.mpf(row[key]) for key in
            ('a', 'H', 'u', 'ud', 'v', 'vd', 'r', 'rd', 'psid', 'rho_m')]
    args.extend((C, k))
    Fm, Fdm, Am = [mp.matrix(fun(*args)) for fun in lambdas]
    p = k / args[0]
    T = mp.matrix([[Fm[r, j] for j in range(12)] for r in ROWS])
    full_L = Fdm + Fm * Am
    L = mp.matrix([[full_L[r, j] for j in range(12)] for r in ROWS])
    Ti = T**-1
    B = L * Ti
    weights = [p if j in (0, 2, 4) else mp.mpf(1) for j in range(12)]
    moving = mp.matrix([[weights[j] * B[j, i] / weights[i]
                         for i in range(12)] for j in range(12)])
    for j in (0, 2, 4):
        moving[j, j] -= args[1]
    graph = Fm * Ti
    as_numpy = lambda mat: np.asarray(
        [[float(mat[j, i]) for i in range(mat.cols)]
         for j in range(mat.rows)], dtype=float)
    return dict(C=as_numpy(moving), graph=as_numpy(graph),
                p=float(p), condition=float(np.linalg.cond(as_numpy(T))))


def relative_max(observed, reference):
    return float(np.max(np.abs(observed-reference)/(1+np.abs(reference))))


def sampled_reconstruction(audit, symbolic):
    print('S4H compiling moving graph/generator evaluators...', flush=True)
    mp.mp.dps = 70
    lambdas = [s.lambdify(up.ARGS, symbolic[name], 'mpmath', cse=True)
               for name in ('F', 'Fdot', 'A')]
    detail, p_sym, frozen = s4g.load_c()
    frozen_fun = s.lambdify((p_sym, base.H), frozen, 'numpy', cse=True)
    rows = csv_rows()
    audit.test('S4H_B1_sample_count', len(rows) == 801, len(rows))
    expected_graph = np.zeros((16, 12))
    for column, index in enumerate(ROWS):
        expected_graph[index, column] = 1
    samples = []
    for t in TIMES:
        index = round(t / 0.005)
        row = rows[index]
        audit.test('S4H_csv_time_' + str(t),
                   abs(float(row['t']) - t) < 1e-12, row['t'])
        for n in MODES:
            print(f'S4H sampled moving chart: t={t}, n={n}', flush=True)
            item = matrix_at(lambdas, row, n)
            p = item['p']
            graph_target = expected_graph.copy()
            for target, source in ((1, 0), (4, 2), (7, 4)):
                graph_target[target, source] = p
            graph_target[14, 11] = 1/p
            graph_error = relative_max(item['graph'], graph_target)
            result = dict(t=t, n=n, p=p, chart_condition=item['condition'],
                          graph_reconstruction_error=graph_error,
                          max_real_generator_eigenvalue=float(np.max(
                              np.linalg.eigvals(item['C']).real)),
                          phase_p2_skew_residual=float(
                              (item['C'][6, 7]+item['C'][7, 6])/p**2),
                          phase_p2_antisymmetric_coefficient=float(
                              (item['C'][6, 7]-item['C'][7, 6])/(2*p**2)))
            if t == 0:
                reference = np.asarray(frozen_fun(p, float(row['H'])), dtype=float)
                result['initial_event_replay_error'] = relative_max(
                    item['C'], reference)
                if n == 1:
                    no_fdot = matrix_at((lambdas[0],
                        lambda *args: mp.zeros(16, 12), lambdas[2]), row, n)
                    no_pdot = item['C'].copy()
                    no_pdot[[0, 2, 4], [0, 2, 4]] += float(row['H'])
                    result['omit_Fdot_error'] = relative_max(no_fdot['C'], reference)
                    result['omit_pdot_error'] = relative_max(no_pdot, reference)
            samples.append(result)
    max_replay = max(x['initial_event_replay_error'] for x in samples if x['t']==0)
    max_graph = max(x['graph_reconstruction_error'] for x in samples)
    audit.test('S4H_initial_event_numeric_replay',
               max_replay < REPLAY_TOLERANCE, max_replay,
               f'<{REPLAY_TOLERANCE}')
    audit.test('S4H_sampled_graph_identity',
               max_graph < REPLAY_TOLERANCE, max_graph,
               f'<{REPLAY_TOLERANCE}; diagnostic, not exact interval proof')
    audit.test('S4H_omit_Fdot_rejected',
               samples[0]['omit_Fdot_error'] > REPLAY_TOLERANCE,
               samples[0]['omit_Fdot_error'])
    audit.test('S4H_omit_pdot_rejected',
               samples[0]['omit_pdot_error'] > REPLAY_TOLERANCE,
               samples[0]['omit_pdot_error'])
    audit.test('S4H_sample_domain',
               all(x['p'] >= 1 and math.isfinite(x['chart_condition'])
                   for x in samples))
    return samples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(x['passed'] for x in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[x for x in audit.checks if not x['passed']])))
        return 1
    chart = exact_chart(audit)
    samples = sampled_reconstruction(audit, chart)
    valid = all(x['passed'] for x in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-s4h-temporal-persistence-detail-v1',
        status='INCOMPLETE_TEMPORAL_PERSISTENCE',
        domain=dict(t='registered_B1_0_to_4_sampled',
                    torus_modes=list(MODES), sample_times=list(TIMES),
                    p='k/a>=1', physical_EFT_cutoff='NOT_DERIVED'),
        original_chart_minor=chart['old_minor'],
        original_canonical_minor=chart['old_canonical'],
        moving_chart_minor=chart['moving_original_minor'],
        moving_canonical_minor=chart['moving_canonical_minor'],
        samples=samples))
    summary = dict(
        schema='r4c1-s4h-temporal-persistence-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(x['passed'] for x in audit.checks), total=len(audit.checks),
        status='INCOMPLETE_TEMPORAL_PERSISTENCE',
        physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False,
        research_execution='HOLD_SUBSTANTIVE_FOR_FINITE_TIME_CLAIM',
        direct_unreviewed_input='R9-MT1-S4G',
        inherited_unreviewed_inputs=[
            'R9-MT1-S4F', 'R9-MT1-S4E', 'R9-MT1-S4D', 'R9-MT1-S4C',
            'R9-MT1-S4B', 'R9-MT1-S4A', 'R9-MT1-S3', 'R9-MT1-S2',
            'R9-MT1-S1', 'R9-MT1-B1', 'R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        decision=dict(exact_moving_chart_minor='p * pinned_S4A_minor',
                      moving_C2_C1_144='NOT_DERIVED',
                      smooth_metric='NOT_CONSTRUCTED',
                      uniform_interval_energy_constant='NOT_PROVED',
                      full_constrained_IVP='NOT_PROVED',
                      physical_EFT_cutoff='NOT_DERIVED'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
