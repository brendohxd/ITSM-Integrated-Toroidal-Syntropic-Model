"""R4C1-S4H step 4: conditional pointwise moving formal metric.

The metric identities here are exact on the regular B1 flow, but no uniform
finite-time energy estimate, cutoff, or constrained-IVP pass is claimed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_moving_spectrum as previous


prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
K, P = previous.K, previous.P
PINS = {
    'Analysis/MasterTests/test_01_r4c1_moving_spectrum.py':
        '369677a86adf1856e00e30f61f8e3256dd2d54034e172b653dfa7474e6d10aab',
    'Analysis/MasterTests/outputs/r4c1_s4h_spectrum_attempt_01/summary.json':
        'a5abe1959655e4b278ffbd6282dfa3d8ef9e455297a485d49a10445292f78cca',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4H5_pin:' + name, actual == expected, actual)
        audit.test('S4H5_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_spectrum_attempt_01/summary.json').read_text())
    audit.test('S4H5_parent_scope',
               parent['validation'] == 'PASS_LOCAL_CHECKS'
               and parent['status'] == 'PRINCIPAL_SPECTRUM_CONDITIONAL_REGULAR_B1'
               and parent['physics_pass'] is False
               and parent['Rule9_cleared'] is False)
    return inputs


def exact_zero(audit, name, matrix):
    reduced = matrix.applyfunc(s.cancel)
    failures = [(i, j, str(reduced[i, j])) for i in range(reduced.rows)
                for j in range(reduced.cols) if reduced[i, j] != 0]
    audit.test(name, not failures, failures[:8] if failures else 'zero_matrix')


def derive(audit):
    detail = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_principal_attempt_01/detail.json').read_text())
    symbols = prior.SYMBOLS
    C2 = s.Matrix([[s.sympify(x, locals=symbols) for x in row]
                   for row in detail['C2']])
    C1 = s.Matrix([[s.sympify(x, locals=symbols) for x in row]
                   for row in detail['C1']])
    A = C1.extract(K, K)
    radius2 = base.u**2 + base.v**2
    frequencies = [s.Integer(1), s.Rational(1, 3),
                   1 + radius2 / 13]
    eigenvalues = [s.Integer(0)] + [-value for value in frequencies]
    eye = s.eye(A.rows)
    square = (A * A).applyfunc(s.cancel)
    projectors = []
    for index, value in enumerate(eigenvalues):
        print(f'S4H5 exact projector {index}/3', flush=True)
        projector = eye
        for other in eigenvalues:
            if value != other:
                projector = (projector * (square - other * eye)
                             / (value - other)).applyfunc(s.cancel)
        projectors.append(projector)
        exact_zero(audit, f'S4H5_projector_idempotent_{index}',
                   projector * projector - projector)
        exact_zero(audit, f'S4H5_projector_eigenvalue_{index}',
                   (square - value * eye) * projector)
    exact_zero(audit, 'S4H5_projector_resolution',
               sum(projectors, s.zeros(A.rows)) - eye)
    for i in range(4):
        for j in range(i):
            exact_zero(audit, f'S4H5_projector_disjoint_{j}_{i}',
                       projectors[j] * projectors[i])
    exact_zero(audit, 'S4H5_zero_projector_kernel', A * projectors[0])

    G = projectors[0].T * projectors[0]
    for omega2, projector in zip(frequencies, projectors[1:]):
        Ap = (A * projector).applyfunc(s.cancel)
        G += projector.T * projector + Ap.T * Ap / omega2
    G = G.applyfunc(s.cancel)
    exact_zero(audit, 'S4H5_G_symmetric', G - G.T)
    exact_zero(audit, 'S4H5_G_skew_identity', A.T * G + G * A)
    audit.test('S4H5_positive_sum_of_squares_certificate',
               len(projectors) == 4
               and all(s.cancel(x) != 0 for x in frequencies),
               'For real u,v and angular charge J=1, radius2>0; '
               'omega2={1,1/3,1+radius2/13}>0 and sum(P_j)=I '
               'implies G>=I/4 by Cauchy-Schwarz.')

    M0 = s.zeros(12)
    for i, row in enumerate(K):
        for j, col in enumerate(K):
            M0[row, col] = G[i, j]
    for index in P:
        M0[index, index] = 1
    exact_zero(audit, 'S4H5_M0_C2_skew', M0*C2 + C2.T*M0)
    S1 = (M0*C1 + C1.T*M0).applyfunc(s.cancel)
    exact_zero(audit, 'S4H5_order_p_KK_cancel', S1.extract(K, K))
    exact_zero(audit, 'S4H5_order_p_PP_cancel', S1.extract(P, P))
    J = C2.extract(P, P)
    audit.test('S4H5_phase_J_invertible', s.cancel(J.det()) != 0,
               str(s.cancel(J.det())))
    cross = (-S1.extract(K, P) * J.inv()).applyfunc(s.cancel)
    M1 = s.zeros(12)
    for i, row in enumerate(K):
        for j, col in enumerate(P):
            M1[row, col] = cross[i, j]
            M1[col, row] = cross[i, j]
    exact_zero(audit, 'S4H5_M1_symmetric', M1-M1.T)
    exact_zero(audit, 'S4H5_full_order_p_cancellation',
               S1 + M1*C2 + C2.T*M1)
    audit.test('S4H5_M1_depends_only_on_background',
               all(x.free_symbols <= set(up.FLOW) for x in M1))
    audit.test('S4H5_M0_depends_only_on_background',
               all(x.free_symbols <= set(up.FLOW) for x in M0))
    return dict(G=G, M0=M0, M1=M1,
                threshold='p>=max(1,8*sqrt(trace(M1.T*M1))) '
                          'implies M0+M1/p >= I/8 at each regular state')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_metric_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[check for check in audit.checks
                                      if not check['passed']])))
        return 1
    result = derive(audit)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-s4h-moving-metric-detail-v1',
        status='MOVING_FORMAL_METRIC_POINTWISE_ONLY' if valid else
               'MOVING_METRIC_FAILED_OR_UNKNOWN',
        domain='conditional regular finite B1 state; a,H,rho_m,radius2>0; '
               'p>=1; physical cutoff and exact [0,4] regularity unproved',
        projected_metric=base.matrix_strings(result['G']),
        M0=base.matrix_strings(result['M0']),
        M1=base.matrix_strings(result['M1']),
        pointwise_lower_bound=result['threshold']))
    summary = dict(
        schema='r4c1-s4h-moving-metric-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status='MOVING_FORMAL_METRIC_POINTWISE_ONLY' if valid else
               'MOVING_METRIC_FAILED_OR_UNKNOWN',
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
        review_status='DEFERRED',
        decision=dict(moving_C2_C1_144='EXACT_FORMULAS',
                      moving_slow_spectrum='CONDITIONAL_REGULAR_B1',
                      moving_metric='POINTWISE_FORMAL' if valid else 'NOT_PROVED',
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
