"""R4C1-S4E: exact phase-pair and diagonal graph-equivalence screen.

Conditional B1 calculation only. Never calls a prior receipt-writing main().
The no-go is restricted to graph-equivalent diagonal chart reweightings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_recursive_leading_span as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
ROWS = previous.ROWS
H = base.H
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_PHASE_PAIR_REWEIGHT_CONTRACT_2026-09-29.md':
        '24c61003b25964933c96a9362756555de5e0f2f0ff1891ef2edb6666fbdbe73a',
    'Theory/Gates/RES-001/RES001_R4C1_RECURSIVE_LEADING_SPAN_REPORT_2026-09-26.md':
        '9479d990e612658d08c68c8a7e2521c1f4a11461a49946e5be6ff73d240f4a2e',
    'Theory/Gates/RES-001/RES001_R4C1_RECURSIVE_LEADING_SPAN_CONTRACT_2026-09-26.md':
        '3cd2ad808053862ca1d947bae4ae0d69b46e8fdae415706b3f332cf3867aede1',
    'Analysis/MasterTests/test_01_r4c1_recursive_leading_span.py':
        'e11b15b7b8cd8d7a1c513fec5fd611b7a83269b409097dfba9a394a0577f32c1',
    'Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/summary.json':
        '319ce57136468f51eb4040c4362d12efa0da08106dc68ed3e5a0c1d354b60097',
    'Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/detail.json':
        '719d011083ae8c7f5a80b00c210d58e138aa49b07dbbbf3b1cc666c954f2e9f0',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        audit.test('S4E_pin:' + name, actual == expected, actual)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4E_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    first_name, first_expected = next(iter(PINS.items()))
    mutated = ('0' if first_expected[0] != '0' else '1') + first_expected[1:]
    audit.test('S4E_deliberately_bad_digest_rejected',
               base.sha(ROOT / first_name) == first_expected
               and base.sha(ROOT / first_name) != mutated)
    s4d = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/summary.json').read_text())
    audit.test('S4E_S4D_scoped_result',
               s4d['validation'] == 'PASS' and s4d['passed'] == s4d['total'] == 125
               and s4d['status'] == 'CHART_REWEIGHT_REQUIRED'
               and s4d['physics_pass'] is False
               and s4d['Rule9_cleared'] is False)
    audit.test('S4E_S4D_artifacts',
               all(base.sha(ROOT / name) == digest
                   for name, digest in s4d['artifacts'].items()))
    return inputs


def derive(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    s4d = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/detail.json').read_text())
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in
                       ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Rdot = up.dtime(R)
    pphysical = base.k / base.a
    Fq1 = Fq.col_join(pphysical * Fq[14, :])
    audit.test('S4E_shapes', Fq1.shape == F.shape == Fdot.shape == (16, 12)
               and R.shape == (6, 6) and A.shape == (12, 12))
    audit.test('S4E_chart_rows', tuple(ROWS) ==
               (0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15))
    audit.exact('S4E_pdot', up.dtime(pphysical) + H * pphysical)
    audit.exact('S4E_Mcdot', W - Vc - up.dtime(Mc))
    audit.exact('S4E_added_dust_row', F[15, :] - pphysical * F[14, :])
    audit.test('S4E_Rdot_present', any(z != 0 for z in Rdot))
    audit.test('S4E_Fdot_present', any(z != 0 for z in Fdot))

    p = s.Symbol('p', positive=True)
    fixed = {base.a: 1, base.C: 1, base.u: 1, base.ud: 0,
             base.v: 0, base.vd: 1, base.r: 1, base.rd: s.Rational(1, 4),
             base.pd: s.Rational(1, 5), base.rho: s.Rational(1, 5),
             base.k: p}
    Fq1s, Fs, Fds, As, Rs, Rds = [matrix.subs(fixed) for matrix in
                                  (Fq1, F, Fdot, A, R, Rdot)]
    Tq = Fq1s.extract(ROWS, range(12))
    audit.test('S4E_pinned_minor',
               s4d['status'] == 'CHART_REWEIGHT_REQUIRED'
               and s4d['chart_rows'] == list(ROWS)
               and s4d['selected_indices'] == [7, 8, 11])
    print('S4E exact chart inverse...', flush=True)
    Tinv = Tq.inv(method='DM')
    audit.exact('S4E_chart_inverse', Tq * Tinv - s.eye(12))
    Ri = Rs.inv()

    def column(i):
        y = Tinv[:, i]
        x = Ri * y[:6, 0]
        z = s.Matrix.vstack(x, Ri * (y[6:, 0] - Rds * x))
        graph = (Fs * z).applyfunc(s.cancel)
        evolution = (Fds * z + Fs * (As * z)).applyfunc(s.cancel)
        unit = s.zeros(12, 1)
        unit[i] = 1
        audit.exact('S4E_chart_unit_' + str(i), Tq * y - unit)
        audit.exact('S4E_full_graph_reconstruction_' + str(i),
                    graph - Fq1s * y)
        audit.exact('S4E_selected_graph_unit_' + str(i),
                    graph.extract(ROWS, [0]) - unit)
        asymptotics = previous.classify_vector(evolution, p)
        audit.test('S4E_full_16row_scan_' + str(i),
                   len(asymptotics) == len(graph) == len(evolution) == 16)
        return dict(graph=graph, evolution=evolution,
                    graph_asymptotics=previous.classify_vector(graph, p),
                    evolution_asymptotics=asymptotics)

    columns = {}
    for i in (6, 7, 9):
        print('S4E full column:', i, flush=True)
        columns[i] = column(i)
    graph7, evolution7 = columns[7]['graph'], columns[7]['evolution']
    saved7 = s4d['columns']['7']
    audit.exact('S4E_replay_S4D_g7',
                graph7 - previous.parse_saved(
                    {'graph': saved7['graph']}, 'graph', p))
    audit.exact('S4E_replay_S4D_ell7',
                evolution7 - previous.parse_saved(
                    {'evolution': saved7['evolution']}, 'evolution', p))
    audit.exact('S4E_g7_exact_unit',
                graph7 - s.eye(16)[:, 10])
    audit.exact('S4E_g6_selected_phase_kinetic',
                columns[6]['graph'][9] - 1)
    b67 = s.cancel(evolution7[ROWS[6]])
    leading = previous.classify_vector(s.Matrix([b67]), p)[0]
    audit.test('S4E_B67_polynomial_leading',
               leading == {'degree': 2, 'coefficient': 'sqrt(165)/33'},
               leading)
    audit.exact('S4E_B67_independent_limit',
                s.limit(b67 / p**2, p, s.oo) - s.sqrt(165) / 33)
    audit.test('S4E_mutated_leading_coefficient_rejected',
               leading['coefficient'] != str(s.sqrt(165) / 34))

    hits = {}
    for i in (6, 9):
        hits[str(i)] = [
            dict(row=row, selected_index=ROWS.index(row) if row in ROWS else None,
                 **entry)
            for row, entry in enumerate(columns[i]['evolution_asymptotics'])
            if entry['degree'] is not None and entry['degree'] >= 1
        ]
    pair_reverse = previous.classify_vector(
        s.Matrix([columns[6]['evolution'][ROWS[7]]]), p)[0]
    return dict(columns=columns, b67=b67, b67_leading=leading,
                reverse_leading=pair_reverse, new_hits=hits,
                source_norm_facts=dict(g7_norm_squared='1',
                                       g6_norm_squared_lower_bound='1'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4e_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[c for c in audit.checks
                                      if not c['passed']])))
        return 1
    result = derive(audit)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-s4e-phase-pair-detail-v1',
        status='DIAGONAL_GRAPH_EQUIVALENT_ORDER_P_REJECTED'
               if valid else 'INCOMPLETE_VALIDATION',
        chart_rows=list(ROWS),
        columns={str(i): dict(
            graph=base.matrix_strings(item['graph']),
            evolution=base.matrix_strings(item['evolution']),
            graph_asymptotics=item['graph_asymptotics'],
            evolution_asymptotics=item['evolution_asymptotics'])
            for i, item in result['columns'].items()},
        B_6_7_exact=str(result['b67']),
        B_6_7_leading=result['b67_leading'],
        B_7_6_leading=result['reverse_leading'],
        further_order_p_hits=result['new_hits'],
        source_norm_facts=result['source_norm_facts']))
    summary = dict(
        schema='r4c1-s4e-phase-pair-summary-v1',
        validation='PASS' if valid else 'FAIL',
        passed=sum(c['passed'] for c in audit.checks),
        total=len(audit.checks),
        status='DIAGONAL_GRAPH_EQUIVALENT_ORDER_P_REJECTED'
               if valid else 'INCOMPLETE_VALIDATION',
        physics_pass=False, gate_effect='NONE',
        review_status='DEFERRED', Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY'
                           if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=[
            'R9-MT1-S4D', 'R9-MT1-S4C', 'R9-MT1-S4B', 'R9-MT1-S4A',
            'R9-MT1-S3', 'R9-MT1-S2', 'R9-MT1-S1', 'R9-MT1-B1',
            'R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        decision=dict(
            exact_B_6_7_leading=result['b67_leading'],
            reverse_B_7_6_leading=result['reverse_leading'],
            further_order_p_hits=result['new_hits'],
            diagonal_graph_equivalent_order_p_bound='REJECTED' if valid else 'UNPROVEN',
            full_constrained_IVP='NOT_PROVED',
            non_diagonal_symmetrizer='NOT_TESTED',
            physical_EFT_cutoff='NOT_DERIVED'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key]
                      for key in ('validation', 'passed', 'total', 'status')} |
                     {'B_6_7_leading': result['b67_leading'],
                      'B_7_6_leading': result['reverse_leading'],
                      'further_order_p_hits': result['new_hits']}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
