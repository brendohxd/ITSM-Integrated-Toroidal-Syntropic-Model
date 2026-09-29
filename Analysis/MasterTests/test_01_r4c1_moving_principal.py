"""R4C1-S4H step 3: exact moving high-p coefficients on the B1 flow.

This is a conditional principal-symbol screen. It neither proves temporal
spectral persistence nor a finite-time constrained-IVP/physical EFT result.
Earlier receipt-writing entrypoints are imported but never called.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_temporal_persistence as previous


prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT, ROWS = base.ROOT, base.OUT, previous.ROWS
K = tuple(i for i in range(12) if i not in (6, 7))
P = (6, 7)
PINS = {
    'Analysis/MasterTests/test_01_r4c1_temporal_persistence.py':
        '1d966f7d3f6d973f855b46ef67295cbd811ae3e69bc4b919a0cc1f3320b79c20',
    'Theory/Gates/RES-001/RES001_R4C1_TEMPORAL_PERSISTENCE_REPORT_2026-09-29.md':
        'aa740eb2419dcfebfc1532230823be7b5df4c3dc31d156701649c5572cf4037b',
    'Analysis/MasterTests/outputs/r4c1_s4h_attempt_02/summary.json':
        '20eaa579780061a8f839a586f3c08725d5098a0e2527857a3c54032c55bc69d7',
    'Analysis/MasterTests/outputs/r4c1_s4h_attempt_02/detail.json':
        '37068a4e93c919194a1d28608e2bab086dd0f36df1583b0d6b9fd589b3e32007',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4H3_pin:' + name, actual == expected, actual)
        audit.test('S4H3_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_attempt_02/summary.json').read_text())
    audit.test('S4H3_parent_scope',
               parent['validation'] == 'PASS_LOCAL_CHECKS'
               and parent['status'] == 'INCOMPLETE_TEMPORAL_PERSISTENCE'
               and parent['physics_pass'] is False
               and parent['Rule9_cleared'] is False)
    return inputs


def exact_zero(audit, name, matrix):
    reduced = matrix.applyfunc(s.cancel)
    failures = [(i, j, str(reduced[i, j])) for i in range(reduced.rows)
                for j in range(reduced.cols) if reduced[i, j] != 0]
    audit.test(name, not failures, failures[:8] if failures else 'zero_matrix')


def moving_matrices(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W = [prior.parse_matrix(s2, name) for name in
               ('q_from_x', 'G', 'W')]
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Rdot = up.dtime(R)
    p = s.Symbol('p', positive=True)
    subs = {base.k: base.a * p}
    Fq1 = Fq.col_join(base.k / base.a * Fq[14, :]).subs(subs)
    Tq = Fq1.extract(ROWS, range(12))
    print('S4H3 exact original chart inverse...', flush=True)
    Tinv = Tq.inv(method='DM')
    exact_zero(audit, 'S4H3_chart_inverse', Tq * Tinv - s.eye(12))
    Ri = R.inv(method='DM')
    transform = s.BlockMatrix([
        [Ri, s.zeros(6)], [-Ri * Rdot * Ri, Ri],
    ]).as_explicit().subs(subs)
    Z = transform * Tinv
    Q = F.subs(subs) * Z
    expected = s.zeros(16, 12)
    for col, row in enumerate(ROWS):
        expected[row, col] = 1
    for row, col in ((1, 0), (4, 2), (7, 4)):
        expected[row, col] = p
    expected[14, 11] = 1 / p
    exact_zero(audit, 'S4H3_full_graph_identity', Q - expected)
    print('S4H3 exact moving evolution matrix...', flush=True)
    L = (Fdot.subs(subs) + F.subs(subs) * A.subs(subs)) * Z
    B = L.extract(ROWS, range(12))
    weights = [p if i in (0, 2, 4) else s.Integer(1) for i in range(12)]
    C = s.Matrix(12, 12, lambda j, i: s.cancel(
        weights[j] * B[j, i] / weights[i]
        + (-base.H if i == j and j in (0, 2, 4) else 0)))
    audit.test('S4H3_matrix_shapes', C.shape == (12, 12)
               and Q.shape == (16, 12) and B.shape == (12, 12))
    return p, C


def coefficients(audit, p, C):
    C2, C1 = s.zeros(12), s.zeros(12)
    bounded = []
    for j in range(12):
        print(f'S4H3 exact principal row {j}/11', flush=True)
        for i in range(12):
            entry = C[j, i]
            if entry == 0:
                bounded.append((j, i))
                continue
            leading = s.cancel(s.limit(entry / p**2, p, s.oo))
            if leading.has(s.oo, -s.oo, s.zoo, s.nan):
                audit.test(f'S4H3_degree_at_most_two_{j}_{i}', False,
                           str(leading))
                continue
            subleading = s.cancel(s.limit(
                (entry - p**2 * leading) / p, p, s.oo))
            if subleading.has(s.oo, -s.oo, s.zoo, s.nan):
                audit.test(f'S4H3_degree_at_most_one_after_{j}_{i}', False,
                           str(subleading))
                continue
            remainder = s.cancel(entry - p**2 * leading - p * subleading)
            tail = s.cancel(s.limit(remainder / p, p, s.oo))
            audit.test(f'S4H3_bounded_remainder_{j}_{i}', tail == 0,
                       str(tail))
            if tail == 0:
                bounded.append((j, i))
            C2[j, i], C1[j, i] = leading, subleading
    audit.test('S4H3_all_144_coefficients', len(bounded) == 144, len(bounded))
    return C2, C1


def replay_initial_event(audit, C2, C1):
    detail = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/detail.json').read_text())
    fixed = {base.a: 1, base.C: 1, base.u: 1, base.ud: 0,
             base.v: 0, base.vd: 1, base.r: 1,
             base.rd: s.Rational(1, 4), base.pd: s.Rational(1, 5),
             base.rho: s.Rational(1, 5)}
    symbols = prior.SYMBOLS
    for name, matrix in (('C2', C2), ('C1', C1)):
        saved = s.Matrix([[s.sympify(value, locals=symbols) for value in row]
                          for row in detail[name]])
        exact_zero(audit, 'S4H3_initial_event_' + name,
                   matrix.subs(fixed) - saved)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_principal_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[check for check in audit.checks
                                      if not check['passed']])))
        return 1
    p, C = moving_matrices(audit)
    C2, C1 = coefficients(audit, p, C)
    replay_initial_event(audit, C2, C1)
    exact_zero(audit, 'S4H3_moving_C2_skew', C2 + C2.T)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-s4h-moving-principal-detail-v1',
        status='PRINCIPAL_COEFFICIENTS_ONLY' if valid else
               'PRINCIPAL_SCREEN_FAILED_OR_UNKNOWN',
        background='R4C1-v1 classical B1 flow; no interval proof',
        domain='formal p=k/a to infinity; physical EFT cutoff unknown',
        chart_rows=list(ROWS),
        variables=[str(x) for x in up.ARGS],
        C2=base.matrix_strings(C2), C1=base.matrix_strings(C1),
        projected_C1=base.matrix_strings(C1.extract(K, K))))
    summary = dict(
        schema='r4c1-s4h-moving-principal-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status='PRINCIPAL_COEFFICIENTS_ONLY' if valid else
               'PRINCIPAL_SCREEN_FAILED_OR_UNKNOWN',
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
        review_status='DEFERRED',
        decision=dict(moving_C2_C1_144='EXACT_FORMULAS' if valid else 'INCOMPLETE',
                      projected_order_p_spectrum='NOT_PROVED',
                      smooth_metric='NOT_CONSTRUCTED',
                      uniform_interval_energy_constant='NOT_PROVED',
                      full_constrained_IVP='NOT_PROVED',
                      physical_EFT_cutoff='NOT_DERIVED'),
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
