"""R4C1-S4G: exact, conditional B1 order-p symmetrizer screen.

Imports parent verifiers without running their receipt-writing main functions.
An initial-event formal high-p result is not a full constrained IVP or EFT pass.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_full_symbol as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT, H = base.ROOT, base.OUT, base.H
K = tuple(i for i in range(12) if i not in (6, 7))
P = (6, 7)
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_ORDER_P_SYMMETRIZER_CONTRACT_2026-09-29.md':
        '74ec49a2e51ff3f27fcfb960b0f6ce7d04ba33d5a82b2122677a67438bbdbb80',
    'Theory/Gates/RES-001/RES001_R4C1_FULL_SYMBOL_CONTRACT_2026-09-29.md':
        '5cd9ed377cb640b50ded531e41ef44a81588fa560a835c8e7df6f6d4bb79168d',
    'Theory/Gates/RES-001/RES001_R4C1_FULL_SYMBOL_REPORT_2026-09-29.md':
        'eb05942b22b2e2b736e9614b3db3510d2acab4ba047a8df3bacc7915ad22ce4b',
    'Analysis/MasterTests/test_01_r4c1_full_symbol.py':
        'd2a34c1855ef0260e6609ff906fd22ea1a11ec051e820e2bb48af29c25d08546',
    'Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/summary.json':
        'c1b47d62d1e6da23269867420be774d114b77d3a33e40e95284e327dfce08604',
    'Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/detail.json':
        '6336924b22b91f5c3c91d835c498c81e8e3880227215ab117c8ccac19dcd8273',
}


def zero(mat):
    return all(s.cancel(value) == 0 for value in mat)


def exact_matrix(audit, name, mat):
    reduced = mat.applyfunc(s.cancel)
    is_zero = all(value == 0 for value in reduced)
    audit.test(name, is_zero,
               'zero_matrix' if is_zero else
               [(j, i, str(reduced[j, i])) for j in range(reduced.rows)
                for i in range(reduced.cols) if reduced[j, i] != 0])


def evaluate_polynomial(poly, mat):
    eye = s.eye(mat.rows)
    value = s.zeros(mat.rows)
    for coefficient in s.Poly(poly).all_coeffs():
        value = (value * mat + coefficient * eye).applyfunc(s.cancel)
    return value


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        audit.test('S4G_pin:' + name, actual == expected, actual)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4G_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    name, digest = next(iter(PINS.items()))
    altered = ('0' if digest[0] != '0' else '1') + digest[1:]
    audit.test('S4G_bad_pin_rejected_in_memory',
               base.sha(ROOT / name) == digest
               and base.sha(ROOT / name) != altered)
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/summary.json').read_text())
    audit.test('S4G_parent_scoped_status',
               parent['validation'] == 'PASS'
               and parent['passed'] == parent['total'] == 208
               and parent['status'] ==
                   'FULL_P2_SYMBOL_SKEW_IN_GRAPH_EQUIVALENT_NORM'
               and parent['physics_pass'] is False
               and parent['Rule9_cleared'] is False)
    audit.test('S4G_parent_artifact_hashes',
               all(base.sha(ROOT / name) == digest
                   for name, digest in parent['artifacts'].items()))
    return inputs


def load_c():
    detail = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/detail.json').read_text())
    p = s.Symbol('p', positive=True)
    local = dict(prior.SYMBOLS)
    local['p'] = p
    C = s.Matrix([[s.sympify(value, locals=local) for value in row]
                  for row in detail['C']])
    return detail, p, C


def principal_matrices(audit, detail, p, C):
    print('S4G exact C2/C1 limits...', flush=True)
    C2 = s.zeros(12)
    C1 = s.zeros(12)
    remainder = s.zeros(12)
    degrees = []
    for j in range(12):
        row = []
        for i in range(12):
            if C[j, i] == 0:
                row.append({'degree': None, 'coefficient': '0'})
                continue
            C2[j, i] = s.cancel(s.limit(C[j, i] / p**2, p, s.oo))
            C1[j, i] = s.cancel(s.limit(
                (C[j, i] - p**2 * C2[j, i]) / p, p, s.oo))
            remainder[j, i] = s.cancel(C[j, i] - p**2 * C2[j, i]
                                       - p * C1[j, i])
            row.append(previous.classify(remainder[j, i], p))
        degrees.append(row)
    saved = s.Matrix([[s.sympify(value, locals={**prior.SYMBOLS, 'p': p})
                       for value in row] for row in detail['C2']])
    exact_matrix(audit, 'S4G_replay_full_C2', C2 - saved)
    exact_matrix(audit, 'S4G_C2_skew', C2 + C2.T)
    audit.test('S4G_C2_only_phase_pair',
               all(C2[j, i] == 0 for j in range(12) for i in range(12)
                   if (j, i) not in ((6, 7), (7, 6)))
               and C2[6, 7] == s.sqrt(165) / 33
               and C2[7, 6] == -s.sqrt(165) / 33)
    audit.exact('S4G_replay_order_p_symmetric_witness',
                (C1[2, 3] + C1[3, 2]) / 2 + s.Rational(1, 26))
    audit.test('S4G_144_bounded_remainders',
               len(degrees) == 12 and all(len(row) == 12 for row in degrees)
               and all(x['degree'] is None or x['degree'] <= 0
                       for row in degrees for x in row))
    local = {**prior.SYMBOLS, 'p': p}
    gram = s.Matrix([[s.sympify(value, locals=local) for value in row]
                     for row in detail['graph_gram']])
    weight = s.Matrix([[s.sympify(value, locals=local) for value in row]
                       for row in detail['D']])
    exact_matrix(audit, 'S4G_graph_Gram_replay',
                 gram - s.diag(1+p**2, 1, 1+p**2, 1, 1+p**2, 1,
                               1, 1, 1, 1, 1, 1+p**-2))
    exact_matrix(audit, 'S4G_graph_D_replay',
                 weight - s.diag(p, 1, p, 1, p, 1, 1, 1, 1, 1, 1, 1))
    return C2, C1, remainder, degrees


def projected_spectrum(audit, A):
    print('S4G projected characteristic/minimal polynomial...', flush=True)
    lam = s.Symbol('lambda')
    char = s.Poly(s.factor(A.charpoly(lam).as_expr()), lam).monic()
    candidate = char.sqf_part().monic()
    candidate_at_A = evaluate_polynomial(candidate, A)
    semisimple = zero(candidate_at_A)
    audit.test('S4G_squarefree_characteristic_part_annihilates_A',
               semisimple,
               'yes' if semisimple else
               [(j, i, str(candidate_at_A[j, i]))
                for j in range(A.rows) for i in range(A.cols)
                if candidate_at_A[j, i] != 0])
    if not semisimple:
        return dict(status='ORDER_P_KERNEL_JORDAN_OBSTRUCTION',
                    char=char.as_expr(), minimal=None,
                    factors=[], frequencies=[], zero_nullity=None)

    factors = s.factor_list(candidate.as_expr(), lam)[1]
    for factor, power in factors:
        quotient = s.div(candidate, s.Poly(factor, lam))[0]
        audit.test('S4G_minimal_factor_necessary:' + str(factor),
                   not zero(evaluate_polynomial(quotient, A)))
    zero_power = 0
    for factor, power in s.factor_list(char.as_expr(), lam)[1]:
        if (s.Poly(factor, lam).degree() == 1
                and s.Poly(factor, lam).eval(0) == 0):
            zero_power = power
    zero_nullity = A.rows - A.rank()
    audit.test('S4G_zero_branch_semisimple', zero_nullity == zero_power,
               {'nullity': zero_nullity, 'algebraic_multiplicity': zero_power})

    frequencies = []
    admissible = True
    has_zero = False
    for factor, power in factors:
        poly = s.Poly(factor, lam).monic()
        if poly.degree() == 1 and poly.eval(0) == 0:
            has_zero = True
        elif poly.degree() == 2 and poly.nth(1) == 0:
            omega2 = s.cancel(poly.nth(0))
            if omega2.is_positive is not True:
                admissible = False
            frequencies.append(omega2)
        else:
            admissible = False
    audit.test('S4G_pure_imaginary_semisimple_factorization',
               admissible and has_zero and zero_nullity == zero_power,
               {'factors': [str(x) for x, _ in factors],
                'frequencies_squared': [str(x) for x in frequencies]})
    return dict(status='SPECTRUM_ADMISSIBLE' if admissible else
                'ORDER_P_KERNEL_SPECTRAL_OBSTRUCTION',
                char=char.as_expr(), minimal=candidate.as_expr(),
                factors=factors, frequencies=frequencies,
                zero_nullity=zero_nullity)


def construct_projector_metric(audit, A, frequencies):
    print('S4G exact spectral projectors and positive metric...', flush=True)
    eye = s.eye(A.rows)
    square = (A * A).applyfunc(s.cancel)
    eigenvalues = [s.Integer(0)] + [-x for x in frequencies]
    projectors = []
    for value in eigenvalues:
        proj = eye
        for other in eigenvalues:
            if value != other:
                proj = (proj * (square - other * eye) /
                        (value - other)).applyfunc(s.cancel)
        projectors.append(proj)
    exact_matrix(audit, 'S4G_projector_resolution',
                 sum(projectors, s.zeros(A.rows)) - eye)
    for j, proj in enumerate(projectors):
        exact_matrix(audit, f'S4G_projector_idempotent_{j}', proj * proj - proj)
        exact_matrix(audit, f'S4G_projector_eigenvalue_{j}',
                     (square - eigenvalues[j] * eye) * proj)
        for i in range(j):
            exact_matrix(audit, f'S4G_projector_orthogonal_{i}_{j}',
                         projectors[i] * proj)
    exact_matrix(audit, 'S4G_zero_projector_kernel', A * projectors[0])
    G = projectors[0].T * projectors[0]
    for omega2, proj in zip(frequencies, projectors[1:]):
        Ap = (A * proj).applyfunc(s.cancel)
        G += proj.T * proj + Ap.T * Ap / omega2
    G = G.applyfunc(s.cancel)
    exact_matrix(audit, 'S4G_positive_metric_symmetric', G - G.T)
    exact_matrix(audit, 'S4G_projected_skew_identity', A.T * G + G * A)
    audit.test('S4G_sum_of_squares_positive_certificate',
               len(projectors) == 1 + len(frequencies)
               and all(x.is_positive is True for x in frequencies)
               and len(projectors) > 1,
               'G=sum(P_j.T P_j)+sum((A P_j).T(A P_j)/omega_j**2); '
               'sum(P_j)=I implies G>=I/N for N projectors')
    return projectors, G


def construct_full_metric(audit, p, C2, C1, remainder, G, projectors):
    print('S4G cross-block correction and full remainder...', flush=True)
    M0 = s.zeros(12)
    for j, row in enumerate(K):
        for i, col in enumerate(K):
            M0[row, col] = G[j, i]
    for index in P:
        M0[index, index] = 1
    exact_matrix(audit, 'S4G_M0_C2_skew', M0 * C2 + C2.T * M0)
    S1 = (M0 * C1 + C1.T * M0).applyfunc(s.cancel)
    exact_matrix(audit, 'S4G_order_p_KK_cancel', S1.extract(K, K))
    exact_matrix(audit, 'S4G_order_p_PP_cancel', S1.extract(P, P))
    J = C2.extract(P, P)
    audit.test('S4G_phase_block_invertible', s.factor(J.det()) != 0,
               str(s.factor(J.det())))
    cross = (-S1.extract(K, P) * J.inv()).applyfunc(s.cancel)
    M1 = s.zeros(12)
    for j, row in enumerate(K):
        for i, col in enumerate(P):
            M1[row, col] = cross[j, i]
            M1[col, row] = cross[j, i]
    exact_matrix(audit, 'S4G_M1_symmetric', M1 - M1.T)
    exact_matrix(audit, 'S4G_full_order_p_cancellation',
                 S1 + M1 * C2 + C2.T * M1)
    audit.test('S4G_no_M1_control_has_order_p_defect', not zero(S1),
               [(j, i, str(S1[j, i])) for j in range(12)
                for i in range(12) if S1[j, i] != 0][:12])

    fixed = {base.ud: 0, base.vd: 1, base.rd: s.Rational(1, 4),
             base.pd: s.Rational(1, 5), base.rho: s.Rational(1, 5)}
    Hdot = s.cancel(up.FLOW[H].subs(fixed))
    audit.exact('S4G_B1_Hdot', Hdot + s.Rational(553, 880))
    M0dot = M0.diff(H) * Hdot
    M1dot_over_p = (M1.diff(H) * Hdot + H * M1) / p
    E = (M0 * remainder + remainder.T * M0 + M1 * C1 + C1.T * M1
         + (M1 * remainder + remainder.T * M1) / p
         + M0dot + M1dot_over_p).applyfunc(s.cancel)
    C = p**2 * C2 + p * C1 + remainder
    direct = ((M0 + M1/p) * C + C.T * (M0 + M1/p)
              + M0dot + M1dot_over_p).applyfunc(s.cancel)
    exact_matrix(audit, 'S4G_full_energy_derivative_identity', E - direct)
    E_asym = [[previous.classify(E[j, i], p) for i in range(12)]
              for j in range(12)]
    positive = [(j, i, E_asym[j][i]) for j in range(12) for i in range(12)
                if E_asym[j][i]['degree'] is not None
                and E_asym[j][i]['degree'] > 0]
    audit.test('S4G_144_energy_remainder_scan',
               len(E_asym) == 12 and all(len(row) == 12 for row in E_asym))
    audit.test('S4G_M1_finite_at_fixed_H',
               all(entry.free_symbols <= {H} for entry in M1))
    count = len(projectors)
    positivity_bound = (
        f'M0 >= I/{count} by projector resolution and Cauchy-Schwarz; '
        f'p >= max(1,{2*count}*sqrt(trace(M1.T*M1))) implies '
        f'M0+M1/p >= I/{2*count}, for each fixed H>0')
    status = ('B1_FORMAL_BOUNDED_ENERGY_RATE_CANDIDATE'
              if not positive else 'B1_ORDER_P_ENERGY_DEFECT_REMAINS')
    return dict(status=status, M0=M0, M1=M1, E=E, E_asym=E_asym,
                positive_remainder_hits=positive, Hdot=Hdot,
                positivity_bound=positivity_bound, S1=S1)


def derive(audit):
    detail, p, C = load_c()
    audit.test('S4G_input_shapes', C.shape == (12, 12)
               and len(detail['Q']) == len(detail['L']) == 16)
    C2, C1, remainder, residual_degrees = principal_matrices(audit, detail, p, C)
    A = C1.extract(K, K)
    spectrum = projected_spectrum(audit, A)
    result = dict(status=spectrum['status'], C2=C2, C1=C1,
                  remainder=remainder, residual_degrees=residual_degrees,
                  A=A, spectrum=spectrum, G=None, projectors=None,
                  full=None)
    if spectrum['status'] != 'SPECTRUM_ADMISSIBLE':
        return result
    projectors, G = construct_projector_metric(
        audit, A, spectrum['frequencies'])
    result['G'], result['projectors'] = G, projectors
    result['full'] = construct_full_metric(
        audit, p, C2, C1, remainder, G, projectors)
    result['status'] = result['full']['status']
    return result


def matrix_or_none(mat):
    return base.matrix_strings(mat) if mat is not None else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4g_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[x for x in audit.checks if not x['passed']])))
        return 1
    result = derive(audit)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    spectrum = result['spectrum']
    full = result['full']
    base.write_json(detailpath, dict(
        schema='r4c1-s4g-order-p-symmetrizer-detail-v1',
        status=result['status'] if valid else 'INCOMPLETE_VALIDATION',
        domain=dict(H='positive_fixed_B1_event', p='k/a>=1',
                    formal_limit='p_to_positive_infinity'),
        phase_indices=list(P), kernel_indices=list(K),
        C2=matrix_or_none(result['C2']), C1=matrix_or_none(result['C1']),
        bounded_C_remainder=matrix_or_none(result['remainder']),
        bounded_C_remainder_degrees=result['residual_degrees'],
        projected_order_p_matrix=matrix_or_none(result['A']),
        characteristic_polynomial=str(s.factor(spectrum['char'])),
        minimal_polynomial=str(s.factor(spectrum['minimal']))
            if spectrum['minimal'] is not None else None,
        zero_nullity=spectrum['zero_nullity'],
        squared_frequencies=[str(x) for x in spectrum['frequencies']],
        spectral_projectors=[matrix_or_none(x)
                             for x in result['projectors']]
            if result['projectors'] is not None else None,
        projected_metric=matrix_or_none(result['G']),
        M0=matrix_or_none(full['M0']) if full else None,
        M1=matrix_or_none(full['M1']) if full else None,
        uncorrected_order_p_defect=matrix_or_none(full['S1']) if full else None,
        energy_remainder=matrix_or_none(full['E']) if full else None,
        energy_remainder_degrees=full['E_asym'] if full else None,
        positive_remainder_hits=full['positive_remainder_hits'] if full else None,
        B1_Hdot=str(full['Hdot']) if full else None,
        positivity_bound=full['positivity_bound'] if full else None))
    summary = dict(
        schema='r4c1-s4g-order-p-symmetrizer-summary-v1',
        validation='PASS' if valid else 'FAIL',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status=result['status'] if valid else 'INCOMPLETE_VALIDATION',
        physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY'
            if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=[
            'R9-MT1-S4F', 'R9-MT1-S4E', 'R9-MT1-S4D', 'R9-MT1-S4C',
            'R9-MT1-S4B', 'R9-MT1-S4A', 'R9-MT1-S3', 'R9-MT1-S2',
            'R9-MT1-S1', 'R9-MT1-B1', 'R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        decision=dict(
            projected_characteristic=str(s.factor(spectrum['char'])),
            projected_minimal=str(s.factor(spectrum['minimal']))
                if spectrum['minimal'] is not None else None,
            squared_frequencies=[str(x) for x in spectrum['frequencies']],
            zero_nullity=spectrum['zero_nullity'],
            positive_energy_remainder_hits=full['positive_remainder_hits']
                if full else None,
            graph_equivalence='FIXED_H_LARGE_P_ONLY' if full else 'UNPROVEN',
            full_constrained_IVP='NOT_PROVED',
            physical_EFT_cutoff='NOT_DERIVED',
            all_sector_stability='NOT_PROVED'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    # Audit evidence may contain exact SymPy Integer values; preserve them as
    # decimal strings without weakening or dropping any check.
    summary = json.loads(json.dumps(summary, default=str))
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key]
                      for key in ('validation', 'passed', 'total', 'status')} |
                     {'projected_characteristic': summary['decision']['projected_characteristic'],
                      'projected_minimal': summary['decision']['projected_minimal'],
                      'positive_energy_remainder_hits':
                          summary['decision']['positive_energy_remainder_hits']}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
