"""R4C1-S4F: complete B1 chart and graph-normalized leading symbol.

Conditional fixed-action calculation. Prior modules are imported but their
receipt-writing entrypoints are not called. No full-IVP or EFT claim follows.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_phase_pair_reweight as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
ROWS, H = previous.ROWS, base.H
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_FULL_SYMBOL_CONTRACT_2026-09-29.md':
        '5cd9ed377cb640b50ded531e41ef44a81588fa560a835c8e7df6f6d4bb79168d',
    'Theory/Gates/RES-001/RES001_R4C1_PHASE_PAIR_REWEIGHT_CONTRACT_2026-09-29.md':
        '24c61003b25964933c96a9362756555de5e0f2f0ff1891ef2edb6666fbdbe73a',
    'Theory/Gates/RES-001/RES001_R4C1_PHASE_PAIR_REWEIGHT_REPORT_2026-09-29.md':
        '90ae5ad23518f311214b152f198014262d4b4b058e2cedbb84d7a6340d12ad8f',
    'Analysis/MasterTests/test_01_r4c1_phase_pair_reweight.py':
        'cf5d2c96c4f61529b89cdeac84b7243f22c176760a9682d1fcc0089e1dc1bc01',
    'Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/summary.json':
        '597535a08264a038a225b68ef8f13b62d3e47ba3d83a882d1b8e6a8e615b5c4b',
    'Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/detail.json':
        'c82d6076df21f9b89b8b2e6fe0d739f1381cc3a8efd974be32431f6376f9b472',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        audit.test('S4F_pin:' + name, actual == expected, actual)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4F_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    name, digest = next(iter(PINS.items()))
    mutated = ('0' if digest[0] != '0' else '1') + digest[1:]
    audit.test('S4F_bad_pin_rejected_in_memory',
               base.sha(ROOT / name) == digest
               and base.sha(ROOT / name) != mutated)
    prior_receipt = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/summary.json').read_text())
    audit.test('S4F_S4E_scoped_status',
               prior_receipt['validation'] == 'PASS'
               and prior_receipt['passed'] == prior_receipt['total'] == 147
               and prior_receipt['status'] ==
                   'DIAGONAL_GRAPH_EQUIVALENT_ORDER_P_REJECTED'
               and prior_receipt['physics_pass'] is False
               and prior_receipt['Rule9_cleared'] is False)
    audit.test('S4F_S4E_artifact_hashes',
               all(base.sha(ROOT / path) == digest
                   for path, digest in prior_receipt['artifacts'].items()))
    return inputs


def classify(expr, p):
    return previous.previous.classify_vector(s.Matrix([expr]), p)[0]


def derive(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    s4e = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/detail.json').read_text())
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in
                       ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Rdot = up.dtime(R)
    pphysical = base.k / base.a
    Fq1 = Fq.col_join(pphysical * Fq[14, :])
    audit.test('S4F_shapes', Fq1.shape == F.shape == Fdot.shape == (16, 12)
               and R.shape == (6, 6) and A.shape == (12, 12))
    audit.test('S4F_chart_rows', tuple(ROWS) ==
               (0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15))
    audit.exact('S4F_pdot', up.dtime(pphysical) + H * pphysical)
    audit.exact('S4F_Mcdot', W - Vc - up.dtime(Mc))
    audit.exact('S4F_added_dust_row', F[15, :] - pphysical * F[14, :])
    audit.test('S4F_Rdot_present', any(z != 0 for z in Rdot))
    audit.test('S4F_Fdot_present', any(z != 0 for z in Fdot))

    p = s.Symbol('p', positive=True)
    fixed = {base.a: 1, base.C: 1, base.u: 1, base.ud: 0,
             base.v: 0, base.vd: 1, base.r: 1, base.rd: s.Rational(1, 4),
             base.pd: s.Rational(1, 5), base.rho: s.Rational(1, 5),
             base.k: p}
    Fq1s, Fs, Fds, As, Rs, Rds = [matrix.subs(fixed) for matrix in
                                  (Fq1, F, Fdot, A, R, Rdot)]
    Tq = Fq1s.extract(ROWS, range(12))
    print('S4F exact chart inverse...', flush=True)
    Tinv = Tq.inv(method='DM')
    audit.exact('S4F_chart_inverse', Tq * Tinv - s.eye(12))
    Ri = Rs.inv()

    qcols, lcols = [], []
    qasy, lasy = [], []
    for i in range(12):
        print('S4F full column:', i, flush=True)
        y = Tinv[:, i]
        x = Ri * y[:6, 0]
        z = s.Matrix.vstack(x, Ri * (y[6:, 0] - Rds * x))
        q = (Fs * z).applyfunc(s.cancel)
        ell = (Fds * z + Fs * (As * z)).applyfunc(s.cancel)
        unit = s.zeros(12, 1)
        unit[i] = 1
        audit.exact('S4F_chart_unit_' + str(i), Tq * y - unit)
        audit.exact('S4F_graph_reconstruction_' + str(i),
                    q - Fq1s * y)
        audit.exact('S4F_selected_graph_unit_' + str(i),
                    q.extract(ROWS, [0]) - unit)
        qcols.append(q)
        lcols.append(ell)
        qasy.append(previous.previous.classify_vector(q, p))
        lasy.append(previous.previous.classify_vector(ell, p))
        audit.test('S4F_complete_16row_scan_' + str(i),
                   len(qasy[-1]) == len(lasy[-1]) == 16)
        if str(i) in s4e['columns']:
            savedcol = s4e['columns'][str(i)]
            audit.exact('S4F_replay_S4E_graph_' + str(i),
                        q - previous.previous.parse_saved(
                            {'graph': savedcol['graph']}, 'graph', p))
            audit.exact('S4F_replay_S4E_evolution_' + str(i),
                        ell - previous.previous.parse_saved(
                            {'evolution': savedcol['evolution']}, 'evolution', p))

    Q = s.Matrix.hstack(*qcols)
    L = s.Matrix.hstack(*lcols)
    expected_Q = s.zeros(16, 12)
    for i, row in enumerate(ROWS):
        expected_Q[row, i] = 1
    for row, column in ((1, 0), (4, 2), (7, 4)):
        expected_Q[row, column] = p
    expected_Q[14, 11] = 1 / p
    audit.exact('S4F_full_graph_Q_identity', Q - expected_Q)
    expected_S = s.diag(1+p**2, 1, 1+p**2, 1, 1+p**2, 1,
                        1, 1, 1, 1, 1, 1+p**-2)
    audit.exact('S4F_full_graph_Gram', Q.T * Q - expected_S)
    weights = [p if i in (0, 2, 4) else s.Integer(1) for i in range(12)]
    D = s.diag(*weights)
    D2 = D.T * D
    audit.exact('S4F_lower_equivalence_identity',
                expected_S - D2 - s.diag(1, 0, 1, 0, 1, 0,
                                         0, 0, 0, 0, 0, p**-2))
    audit.exact('S4F_upper_equivalence_identity',
                2 * D2 - expected_S -
                s.diag(p**2-1, 1, p**2-1, 1, p**2-1, 1,
                       1, 1, 1, 1, 1, 1-p**-2))
    wrong_D2 = D2.copy()
    wrong_D2[0, 0] = 1
    audit.test('S4F_wrong_D_weight_rejected',
               s.limit(expected_S[0, 0] / wrong_D2[0, 0], p, s.oo)
               == s.oo)

    B = L.extract(ROWS, range(12))
    audit.test('S4F_selected_generator_shape', B.shape == (12, 12))
    Cdot = s.diag(*[-H if i in (0, 2, 4) else 0 for i in range(12)])
    pdot_over_p = s.cancel(up.dtime(pphysical) / pphysical)
    audit.exact('S4F_Ddot_from_pdot',
                Cdot - s.diag(*[pdot_over_p if i in (0, 2, 4) else 0
                                   for i in range(12)]))
    C = s.Matrix(12, 12, lambda j, i: s.cancel(
        weights[j] * B[j, i] / weights[i] + Cdot[j, i]))
    casy = [[classify(C[j, i], p) for i in range(12)]
            for j in range(12)]
    degree_hits = [
        dict(row=j, column=i, **casy[j][i])
        for j in range(12) for i in range(12)
        if casy[j][i]['degree'] is not None
        and casy[j][i]['degree'] >= 1
    ]
    high_hits = [item for item in degree_hits if item['degree'] >= 2]
    for item in high_hits:
        j, i, degree = item['row'], item['column'], item['degree']
        coeff = s.sympify(item['coefficient'],
                          locals={**prior.SYMBOLS, 'p': p})
        audit.exact('S4F_independent_limit_' + str(j) + '_' + str(i),
                    s.limit(C[j, i] / p**degree, p, s.oo) - coeff)
    audit.test('S4F_144_entry_scan',
               len(casy) == 12 and all(len(row) == 12 for row in casy)
               and len(qasy) == len(lasy) == 12)
    audit.test('S4F_phase_pair_recovered',
               casy[6][7] ==
                   {'degree': 2, 'coefficient': 'sqrt(165)/33'}
               and casy[7][6] ==
                   {'degree': 2, 'coefficient': '-sqrt(165)/33'})
    max_degree = max((item['degree'] for item in degree_hits), default=None)
    C2 = None
    skew_residual = None
    if max_degree is not None and max_degree > 2:
        status = 'HIGHER_ORDER_FULL_SYMBOL_COUPLING'
    else:
        C2 = s.Matrix(12, 12, lambda j, i:
            s.sympify(casy[j][i]['coefficient'],
                      locals={**prior.SYMBOLS, 'p': p})
            if casy[j][i]['degree'] == 2 else s.Integer(0))
        skew_residual = (C2 + C2.T).applyfunc(s.factor)
        skew = all(x == 0 for x in skew_residual)
        status = ('FULL_P2_SYMBOL_SKEW_IN_GRAPH_EQUIVALENT_NORM'
                  if skew else 'FULL_P2_SYMBOL_NOT_SKEW_IN_CANDIDATE_NORM')
        audit.test('S4F_p2_skew_classification',
                   skew == (status ==
                            'FULL_P2_SYMBOL_SKEW_IN_GRAPH_EQUIVALENT_NORM'))
    symmetric = ((C + C.T) / 2).applyfunc(s.cancel)
    sasy = [[classify(symmetric[j, i], p) for i in range(12)]
            for j in range(12)]
    symmetric_max_degree = max(
        (entry['degree'] for row in sasy for entry in row
         if entry['degree'] is not None), default=None)
    full_graph_hits = [
        dict(input=i, row=row, **lasy[i][row])
        for i in range(12) for row in range(16)
        if lasy[i][row]['degree'] is not None
        and lasy[i][row]['degree'] >= 1
    ]
    return dict(status=status, Q=Q, L=L, B=B, C=C, C2=C2,
                skew_residual=skew_residual,
                qasy=qasy, lasy=lasy, casy=casy, sasy=sasy,
                max_degree=max_degree, symmetric_max_degree=symmetric_max_degree,
                degree_hits=degree_hits, high_hits=high_hits,
                full_graph_hits=full_graph_hits, graph_gram=expected_S,
                D=D)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4f_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(c['passed'] for c in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[c for c in audit.checks if not c['passed']])))
        return 1
    result = derive(audit)
    valid = all(c['passed'] for c in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-s4f-full-symbol-detail-v1',
        status=result['status'] if valid else 'INCOMPLETE_VALIDATION',
        domain=dict(H='positive_fixed_B1_event', p='k/a>=1',
                    formal_limit='p_to_positive_infinity'),
        chart_rows=list(ROWS),
        Q=base.matrix_strings(result['Q']),
        L=base.matrix_strings(result['L']),
        B=base.matrix_strings(result['B']),
        D=base.matrix_strings(result['D']),
        graph_gram=base.matrix_strings(result['graph_gram']),
        C=base.matrix_strings(result['C']),
        C2=base.matrix_strings(result['C2'])
           if result['C2'] is not None else None,
        C2_skew_residual=base.matrix_strings(result['skew_residual'])
           if result['skew_residual'] is not None else None,
        Q_asymptotics=result['qasy'],
        L_asymptotics=result['lasy'],
        C_asymptotics=result['casy'],
        symmetric_C_asymptotics=result['sasy'],
        degree_hits=result['degree_hits'],
        full_graph_order_p_hits=result['full_graph_hits']))
    summary = dict(
        schema='r4c1-s4f-full-symbol-summary-v1',
        validation='PASS' if valid else 'FAIL',
        passed=sum(c['passed'] for c in audit.checks),
        total=len(audit.checks),
        status=result['status'] if valid else 'INCOMPLETE_VALIDATION',
        physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY'
                           if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=[
            'R9-MT1-S4E', 'R9-MT1-S4D', 'R9-MT1-S4C', 'R9-MT1-S4B',
            'R9-MT1-S4A', 'R9-MT1-S3', 'R9-MT1-S2', 'R9-MT1-S1',
            'R9-MT1-B1', 'R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        decision=dict(
            max_generator_degree=result['max_degree'],
            max_symmetric_degree=result['symmetric_max_degree'],
            degree_2_or_faster_hits=result['high_hits'],
            p2_skew_residual=base.matrix_strings(result['skew_residual'])
                if result['skew_residual'] is not None else None,
            graph_equivalent_D='VERIFIED_FOR_P_GE_1' if valid else 'UNPROVEN',
            full_constrained_IVP='NOT_PROVED',
            physical_EFT_cutoff='NOT_DERIVED',
            all_sector_stability='NOT_PROVED'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key]
                      for key in ('validation', 'passed', 'total', 'status')} |
                     {'max_generator_degree': result['max_degree'],
                      'max_symmetric_degree': result['symmetric_max_degree'],
                      'degree_2_or_faster_hits': result['high_hits']}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
