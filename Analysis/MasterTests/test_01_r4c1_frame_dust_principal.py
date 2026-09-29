"""R4C1-S4C: exact frame/dust leading-coupling and leakage audit.

Conditional fixed-action diagnostic only. A passed script is not IVP closure.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as s

import test_01_r4c1_mixed_regularity as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
STEM = 'test_01_r4c1_frame_dust_principal'
H = base.H
ROWS = (0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15)
FRAME, DUST = 8, 11
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_FRAME_DUST_PRINCIPAL_CONTRACT_2026-09-26.md':
        'd961553f9e2c26d617d8324fbcb0a78169c4bcc2f716aa5fa267725443adffa6',
    'Theory/Gates/RES-001/RES001_R4C1_MIXED_REGULARITY_REPORT_2026-09-26.md':
        '437e82f0faf3d8053763d253e102ac732eb39a34c598d7aad8efc0abc3d2131f',
    'Analysis/MasterTests/test_01_r4c1_mixed_regularity.py':
        'ee9bd6fe894e8595a52d97f02bebc3827c6a70dee473e4cff41dfa6cfb2c7552',
    'Analysis/MasterTests/outputs/test_01_r4c1_mixed_regularity_summary.json':
        'e98be1809f48d6aaf2316dc3109473cd2b5b4c4a362d173f0f633be5c9498a73',
    'Analysis/MasterTests/outputs/test_01_r4c1_mixed_regularity_matrices.json':
        '503e58fdc2f95951107f9702daca36ae63acd45df83eb9395a00b0fe9c7e69db',
    'Analysis/MasterTests/outputs/test_01_r4c1_mixed_regularity_samples.json':
        '63ca5e2e542ff3f6212556fa3fa8d45bb121971550c2fb6315b0bd48b46d8b54',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT/name
        actual = base.sha(path)
        audit.test('S4C_pin:'+name, actual == expected, actual)
        sidecar = path.with_name(path.name+'.sha256')
        audit.test('S4C_sidecar:'+name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    receipt = prior.read_raw('test_01_r4c1_mixed_regularity_summary.json')
    audit.test('S4B_scope', receipt['validation'] == 'PASS' and
               receipt['passed'] == receipt['total'] == 169 and
               receipt['status'] == 'ONE_EXTRA_DUST_DERIVATIVE_FIXED_GRAPH_BOUND_REJECTED_FULL_IVP_OPEN' and
               receipt['physics_pass'] is False and receipt['Rule9_cleared'] is False)
    audit.test('S4B_transitive_artifacts', all(base.sha(ROOT/name) == digest
               for name, digest in receipt['artifacts'].items()))
    return inputs


def leading(expr, p):
    expr = s.cancel(expr)
    if expr == 0:
        return {'degree': None, 'coefficient': '0'}
    numerator, denominator = expr.as_numer_denom()
    num, den = s.Poly(numerator, p), s.Poly(denominator, p)
    degree = int(num.degree()-den.degree())
    coefficient = s.factor(s.cancel(num.LC()/den.LC()))
    return {'degree': degree, 'coefficient': str(coefficient)}


def derive(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in
                       ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Rdot = up.dtime(R)
    pphysical = base.k/base.a
    Fq1 = Fq.col_join(pphysical*Fq[14, :])
    audit.test('full_source_shapes', Fq.shape == (15, 12) and F.shape == (16, 12)
               and Fdot.shape == (16, 12) and R.shape == (6, 6))
    audit.exact('new_dust_row_unchanged', F[15, :]-pphysical*F[14, :])
    audit.exact('physical_pdot', up.dtime(pphysical)+H*pphysical)
    audit.exact('corrected_Mcdot', W-Vc-up.dtime(Mc))
    audit.test('reject_missing_Rdot', any(z != 0 for z in Rdot))
    audit.test('reject_missing_F1dot', any(s.cancel(z) != 0 for z in Fdot[15, :]))
    oldrows = tuple(old['selected_minor_rows'])
    audit.test('selected_chart_is_row_replacement',
               oldrows[:-1] == ROWS[:-1] and oldrows[-1] == 14 and ROWS[-1] == 15)

    p = s.Symbol('p', positive=True)
    fixed = {base.a: 1, base.C: 1, base.u: 1, base.ud: 0,
             base.v: 0, base.vd: 1, base.r: 1, base.rd: s.Rational(1, 4),
             base.pd: s.Rational(1, 5), base.rho: s.Rational(1, 5), base.k: p}
    samples = prior.read_raw('test_01_r4c1_mixed_regularity_samples.json')
    initial = samples['b1_initial_state']
    expected = [1., None, 1., 0., 0., 1., 1., .25, 0., .2, .2, 0.]
    audit.test('B1_initial_coefficients', len(initial) == 12 and initial[1] > 0
               and all(abs(initial[i]-value) < 1e-15
                       for i, value in enumerate(expected) if value is not None), initial)
    Fq1s, Fs, Fds, As, Rs, Rds = [matrix.subs(fixed)
                                   for matrix in (Fq1, F, Fdot, A, R, Rdot)]
    Tq = Fq1s.extract(ROWS, range(12))
    original_minor = s.sympify(old['original_chart_minor'], locals=prior.SYMBOLS)
    expected_minor = s.factor(p*original_minor.subs(fixed))
    audit.exact('selected_minor_row_scaling', Tq[11, :]-p*Fq1s[14, :])
    print('S4C determinant...', flush=True)
    actual_minor = s.factor(Tq.det(method='domain-ge'))
    audit.exact('selected_minor_exact', actual_minor-expected_minor)
    audit.test('selected_minor_regular_domain', actual_minor != 0 and
               not s.cancel(actual_minor).as_numer_denom()[1].equals(0))
    density_coefficient = (79200*H**2+200*p**2+1419)/240
    audit.exact('regular_density_velocity_coefficient',
                Fq1s[13, 10]-density_coefficient)

    yf, yd = s.zeros(12, 1), s.zeros(12, 1)
    yf[11] = s.sqrt(6)
    yf[10] = -s.cancel(Fq1s[13, 11]*yf[11]/Fq1s[13, 10])
    yd[4] = 1/p**2
    yd[10] = -s.cancel(Fq1s[13, 4]*yd[4]/Fq1s[13, 10])
    ef, ed = s.zeros(12, 1), s.zeros(12, 1)
    ef[FRAME], ed[DUST] = 1, 1
    audit.exact('unit_frame_chart_data', Tq*yf-ef)
    audit.exact('unit_dust_chart_data', Tq*yd-ed)
    gf, gd = (Fq1s*yf).applyfunc(s.cancel), (Fq1s*yd).applyfunc(s.cancel)
    expected_gf, expected_gd = s.zeros(16, 1), s.zeros(16, 1)
    expected_gf[11] = 1
    expected_gd[14], expected_gd[15] = 1/p, 1
    audit.exact('full_frame_graph_support', gf-expected_gf)
    audit.exact('full_dust_graph_support', gd-expected_gd)
    Ri = Rs.inv()
    def canonical(y):
        x = Ri*y[:6, 0]
        return s.Matrix.vstack(x, Ri*(y[6:, 0]-Rds*x))
    zf, zd = canonical(yf), canonical(yd)
    audit.exact('frame_canonical_graph_reconstruction', Fs*zf-gf)
    audit.exact('dust_canonical_graph_reconstruction', Fs*zd-gd)
    wrong_dust_z = s.Matrix.vstack(Ri*yd[:6, 0], Ri*yd[6:, 0])
    audit.test('reject_omitted_Rdot_on_dust',
               any(s.cancel(value) != 0 for value in Fs*wrong_dust_z-gd))
    print('S4C full two-column evolution...', flush=True)
    lf = (Fds*zf+Fs*(As*zf)).applyfunc(s.cancel)
    ld = (Fds*zd+Fs*(As*zd)).applyfunc(s.cancel)
    audit.test('reject_frozen_graph_evolution',
               any(s.cancel(x) != 0 for x in Fds*zf) or
               any(s.cancel(x) != 0 for x in Fds*zd))
    graph = gf+gd
    norm2 = s.cancel((graph.T*graph)[0])
    audit.exact('S4B_witness_norm', norm2-(2*p**2+1)/p**2)
    rate = s.cancel((graph.T*(lf+ld))[0]/norm2)
    rate_limit = s.factor(s.limit(rate/p, p, s.oo))
    audit.exact('S4B_witness_limit_recovered', rate_limit-s.sqrt(6)/2)
    return dict(p=p, frame_graph=gf, dust_graph=gd, frame_z=zf, dust_z=zd,
                frame_evolution=lf, dust_evolution=ld,
                selected_minor=str(actual_minor), rate_limit=str(rate_limit))


def classify(audit, result):
    p = result['p']
    columns = {}
    for label, vector in (('frame', result['frame_evolution']),
                          ('dust', result['dust_evolution'])):
        print('S4C exact asymptotics:', label, flush=True)
        columns[label] = [leading(vector[i], p) for i in range(16)]
        audit.test(label+'_all_degrees_recorded', len(columns[label]) == 16)
    leakage = []
    faster = []
    for label, rows in columns.items():
        for i, item in enumerate(rows):
            degree = item['degree']
            if degree is not None and degree > 1:
                faster.append(dict(input=label, row=i, **item))
            if i not in (11, 15) and degree is not None and degree >= 1:
                leakage.append(dict(input=label, row=i, **item))
    closed = not leakage and not faster
    block = None
    symmetrizer = 'NOT_TESTED_NONCLOSED_LEADING_BLOCK'
    if closed:
        def coefficient(label, row):
            item = columns[label][row]
            return (s.sympify(item['coefficient'], locals=prior.SYMBOLS)
                    if item['degree'] == 1 else s.S.Zero)
        B = s.Matrix([[coefficient('frame', 11), coefficient('dust', 11)],
                      [coefficient('frame', 15), coefficient('dust', 15)]])
        block = base.matrix_strings(B)
        q, r = s.symbols('q r', real=True)
        P = s.Matrix([[1, q], [q, r]])
        equations = list(P*B+B.T*P)
        solutions = s.solve(equations, (q, r), dict=True)
        symmetrizer = dict(equations=[str(s.factor(x)) for x in equations],
                           solutions=[{str(k): str(v) for k, v in d.items()}
                                      for d in solutions],
                           positivity='Requires r>q**2; no full-system claim')
    audit.test('classification_complete', len(columns) == 2 and
               all(len(v) == 16 for v in columns.values()))
    return dict(columns=columns, leakage=leakage, faster_than_p=faster,
                leading_two_variable_closed=closed, leading_block=block,
                conditional_symmetrizer=symmetrizer)


def main():
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[c for c in audit.checks if not c['passed']])))
        return 1
    result = derive(audit)
    diagnostic = classify(audit, result)
    valid = all(check['passed'] for check in audit.checks)
    status = ('LEADING_FRAME_DUST_BLOCK_CLOSED_ONLY' if diagnostic['leading_two_variable_closed']
              else 'LEADING_FRAME_DUST_BLOCK_LEAKS_FULL_IVP_OPEN') if valid else 'UNVALIDATED'
    detailpath = OUT/(STEM+'_detail.json')
    base.write_json(detailpath, dict(schema='r4c1-frame-dust-principal-detail-v1',
        chart_rows=list(ROWS), frame_chart_index=FRAME, dust_chart_index=DUST,
        selected_minor=result['selected_minor'],
        frame_graph=base.matrix_strings(result['frame_graph']),
        dust_graph=base.matrix_strings(result['dust_graph']),
        frame_canonical=base.matrix_strings(result['frame_z']),
        dust_canonical=base.matrix_strings(result['dust_z']),
        frame_evolution=base.matrix_strings(result['frame_evolution']),
        dust_evolution=base.matrix_strings(result['dust_evolution']),
        S4B_rate_over_p_limit=result['rate_limit'], diagnostic=diagnostic))
    summary = dict(schema='r4c1-frame-dust-principal-summary-v1',
        validation='PASS' if valid else 'FAIL',
        passed=sum(c['passed'] for c in audit.checks), total=len(audit.checks),
        status=status, physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=['R9-MT1-S4B','R9-MT1-S4A','R9-MT1-S3',
            'R9-MT1-S2','R9-MT1-S1','R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix():base.sha(detailpath)},
        decision=dict(leading_two_variable_closed=diagnostic['leading_two_variable_closed'],
                      leakage=diagnostic['leakage'],
                      faster_than_p=diagnostic['faster_than_p'],
                      isolated_symmetrizer=diagnostic['conditional_symmetrizer'],
                      full_constrained_IVP='NOT_PROVED',
                      fixed_S4B_metric_bound='REJECTED_BY_PRIOR_EXACT_WITNESS'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    base.write_json(OUT/(STEM+'_summary.json'), summary)
    print(json.dumps({key: summary[key] for key in ('validation','passed','total','status')}
                     | {'leakage': diagnostic['leakage'],
                        'faster_than_p': diagnostic['faster_than_p']}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
