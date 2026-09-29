"""R4C1-S4D: bounded exact recursive leading-span diagnostic.

Conditional fixed-action calculation. A valid receipt is not IVP/stability closure.
Prior receipt-producing entrypoints are imported but never called.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_frame_dust_principal as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
ROWS = previous.ROWS
H = base.H
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_RECURSIVE_LEADING_SPAN_CONTRACT_2026-09-26.md':
        '3cd2ad808053862ca1d947bae4ae0d69b46e8fdae415706b3f332cf3867aede1',
    'Theory/Gates/RES-001/RES001_R4C1_FRAME_DUST_PRINCIPAL_REPORT_2026-09-26.md':
        '65a0a4238673ec757493cc1f398bddc50c8e07a47226603e9dd50e70bb0441ec',
    'Analysis/MasterTests/test_01_r4c1_frame_dust_principal.py':
        '8732ca4b991a60ce99eb32cf5de85a147435ae075f07dbf8495f661c22af6f82',
    'Analysis/MasterTests/outputs/test_01_r4c1_frame_dust_principal_summary.json':
        'ddccc444ac7e9191a1d19d6e61aaf009932e6394b700dcfe29af4d0bb361107b',
    'Analysis/MasterTests/outputs/test_01_r4c1_frame_dust_principal_detail.json':
        'b4cd27382b516c7fec994c926829db60cc3c1bc295abd4074324c7a7c6ec24bc',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        audit.test('S4D_pin:' + name, actual == expected, actual)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4D_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    summary = prior.read_raw('test_01_r4c1_frame_dust_principal_summary.json')
    audit.test('S4C_scoped_result',
               summary['validation'] == 'PASS' and
               summary['passed'] == summary['total'] == 117 and
               summary['status'] == 'LEADING_FRAME_DUST_BLOCK_LEAKS_FULL_IVP_OPEN' and
               summary['physics_pass'] is False and
               summary['Rule9_cleared'] is False)
    audit.test('S4C_transitive_detail', all(base.sha(ROOT/name) == digest
               for name, digest in summary['artifacts'].items()))
    return inputs


def parse_saved(matrix, name, p):
    locals_ = dict(prior.SYMBOLS)
    locals_['p'] = p
    return s.Matrix([[s.sympify(value, locals=locals_) for value in row]
                     for row in matrix[name]])


def classify_vector(vector, p):
    return [previous.leading(vector[i], p) for i in range(vector.rows)]


def max_degree(items):
    return max((item['degree'] for item in items
                if item['degree'] is not None), default=None)


def exact_zero(audit, name, vector):
    audit.exact(name, vector.applyfunc(s.cancel))


def derive(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    saved = prior.read_raw('test_01_r4c1_mixed_regularity_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    detail = prior.read_raw('test_01_r4c1_frame_dust_principal_detail.json')
    Fq = prior.parse_matrix(old, 'original_graph_map')
    F, Fdot = [prior.parse_matrix(saved, name) for name in
               ('full_graph_map', 'full_graph_map_derivative')]
    R, G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in
                       ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Rdot = up.dtime(R)
    pphysical = base.k / base.a
    Fq1 = Fq.col_join(pphysical * Fq[14, :])
    audit.test('S4D_shapes', Fq1.shape == F.shape == Fdot.shape == (16, 12)
               and R.shape == (6, 6) and A.shape == (12, 12))
    audit.test('S4D_chart_rows', tuple(ROWS) ==
               (0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 15))
    audit.exact('S4D_pdot', up.dtime(pphysical) + H * pphysical)
    audit.exact('S4D_Mcdot', W - Vc - up.dtime(Mc))
    audit.exact('S4D_new_dust_row', F[15, :] - pphysical * F[14, :])

    p = s.Symbol('p', positive=True)
    fixed = {base.a: 1, base.C: 1, base.u: 1, base.ud: 0,
             base.v: 0, base.vd: 1, base.r: 1, base.rd: s.Rational(1, 4),
             base.pd: s.Rational(1, 5), base.rho: s.Rational(1, 5),
             base.k: p}
    Fq1s, Fs, Fds, As, Rs, Rds = [m.subs(fixed)
                                   for m in (Fq1, F, Fdot, A, R, Rdot)]
    Tq = Fq1s.extract(ROWS, range(12))
    audit.test('S4D_full_chart_rank_from_pin',
               detail['selected_minor'] ==
               '-sqrt(66)*p**5*(79200*H**2 + 200*p**2 + 1419)/15840')
    print('S4D exact chart inverse...', flush=True)
    Tinv = Tq.inv(method='DM')
    exact_zero(audit, 'S4D_chart_inverse', Tq * Tinv - s.eye(12))
    Ri = Rs.inv()

    def column(i):
        y = Tinv[:, i]
        x = Ri * y[:6, 0]
        z = s.Matrix.vstack(x, Ri * (y[6:, 0] - Rds * x))
        graph = (Fs * z).applyfunc(s.cancel)
        evolution = (Fds * z + Fs * (As * z)).applyfunc(s.cancel)
        e = s.zeros(12, 1)
        e[i] = 1
        exact_zero(audit, 'S4D_chart_unit_' + str(i), Tq * y - e)
        exact_zero(audit, 'S4D_graph_reconstruction_' + str(i),
                   graph - Fq1s * y)
        return dict(index=i, graph=graph, evolution=evolution,
                    graph_asymptotics=classify_vector(graph, p),
                    evolution_asymptotics=classify_vector(evolution, p))

    columns = {}
    queue = [previous.FRAME, previous.DUST]
    source_growth = []
    faster_than_p = []
    unselected_order_p = []
    stopped_at = None
    while queue:
        i = queue.pop(0)
        if i in columns:
            continue
        print('S4D full column:', i, flush=True)
        item = column(i)
        columns[i] = item
        if i in (previous.FRAME, previous.DUST):
            label = 'frame' if i == previous.FRAME else 'dust'
            exact_zero(audit, 'S4D_recover_S4C_graph_' + label,
                       item['graph'] - parse_saved(detail, label + '_graph', p))
            exact_zero(audit, 'S4D_recover_S4C_evolution_' + label,
                       item['evolution'] - parse_saved(detail, label + '_evolution', p))
        growth = max_degree(item['graph_asymptotics'])
        if growth is not None and growth > 0:
            source_growth.append(dict(index=i, degree=growth,
                rows=[j for j, x in enumerate(item['graph_asymptotics'])
                      if x['degree'] == growth]))
        for row, datum in enumerate(item['evolution_asymptotics']):
            degree = datum['degree']
            if degree is not None and degree > 1:
                faster_than_p.append(dict(input=i, row=row, **datum))
                coefficient = s.sympify(datum['coefficient'],
                                        locals={**prior.SYMBOLS, 'p': p})
                audit.exact('S4D_independent_leading_limit_' + str(i) + '_' + str(row),
                            s.limit(item['evolution'][row] / p**degree, p, s.oo)
                            - coefficient)
            if row not in ROWS and degree is not None and degree >= 1:
                unselected_order_p.append(dict(input=i, row=row, **datum))
        if source_growth or faster_than_p:
            stopped_at = i
            break
        for j, row in enumerate(ROWS):
            degree = item['evolution_asymptotics'][row]['degree']
            if degree is not None and degree >= 1 and j not in columns and j not in queue:
                queue.append(j)

    audit.test('S4D_S4C_pair_seen', previous.FRAME in columns and
               previous.DUST in columns)
    if previous.FRAME in columns:
        f = columns[previous.FRAME]['evolution_asymptotics']
        audit.test('S4D_S4C_leakage_10_12', f[10]['degree'] == f[12]['degree'] == 1
                   and f[10]['coefficient'] == 'sqrt(330)/55'
                   and f[12]['coefficient'] == 'sqrt(10)/5')
    status = 'CHART_REWEIGHT_REQUIRED' if source_growth or faster_than_p else None
    residuals = []
    leading_block = None
    if status is None:
        Q = (Fq1s * Tinv).applyfunc(s.cancel)
        for i, item in columns.items():
            selected = s.Matrix([item['evolution'][row] for row in ROWS])
            residual = (item['evolution'] - Q * selected).applyfunc(s.cancel)
            asymptotics = classify_vector(residual, p)
            hits = [dict(input=i, row=row, **entry)
                    for row, entry in enumerate(asymptotics)
                    if entry['degree'] is not None and entry['degree'] >= 1]
            residuals.extend(hits)
        if residuals:
            status = 'FULL_GRAPH_LEAKAGE'
        else:
            order = sorted(columns)
            leading_block = [[columns[i]['evolution_asymptotics'][ROWS[j]]
                              if columns[i]['evolution_asymptotics'][ROWS[j]]['degree'] == 1
                              else {'degree': None, 'coefficient': '0'}
                              for i in order] for j in order]
            status = 'LEADING_SPAN_CLOSED_ONLY'
    audit.test('S4D_bounded_classification', status is not None and
               len(columns) <= 12)
    return dict(status=status, columns=columns, source_growth=source_growth,
                faster_than_p=faster_than_p, unselected_order_p=unselected_order_p,
                full_graph_residuals=residuals, leading_block=leading_block,
                chart_rows=list(ROWS), selected_indices=sorted(columns),
                pending_indices=list(queue), stopped_at=stopped_at)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4d_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[c for c in audit.checks if not c['passed']])))
        return 1
    result = derive(audit)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(schema='r4c1-s4d-leading-span-detail-v1',
        status=result['status'], chart_rows=result['chart_rows'],
        selected_indices=result['selected_indices'],
        pending_indices=result['pending_indices'], stopped_at=result['stopped_at'],
        columns={str(i): dict(graph=base.matrix_strings(item['graph']),
            evolution=base.matrix_strings(item['evolution']),
            graph_asymptotics=item['graph_asymptotics'],
            evolution_asymptotics=item['evolution_asymptotics'])
            for i, item in result['columns'].items()},
        source_growth=result['source_growth'],
        faster_than_p=result['faster_than_p'],
        unselected_order_p=result['unselected_order_p'],
        full_graph_residuals=result['full_graph_residuals'],
        leading_block=result['leading_block']))
    summary = dict(schema='r4c1-s4d-leading-span-summary-v1',
        validation='PASS' if valid else 'FAIL',
        passed=sum(check['passed'] for check in audit.checks), total=len(audit.checks),
        status=result['status'] if valid else 'UNVALIDATED',
        physics_pass=False, gate_effect='NONE', review_status='DEFERRED',
        Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=['R9-MT1-S4C','R9-MT1-S4B','R9-MT1-S4A',
            'R9-MT1-S3','R9-MT1-S2','R9-MT1-S1','R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix():base.sha(detailpath)},
        decision=dict(selected_indices=result['selected_indices'],
            pending_indices=result['pending_indices'], stopped_at=result['stopped_at'],
            source_growth=result['source_growth'], faster_than_p=result['faster_than_p'],
            unselected_order_p=result['unselected_order_p'],
            full_graph_residuals=result['full_graph_residuals'],
            leading_span_closed=result['status'] == 'LEADING_SPAN_CLOSED_ONLY',
            full_constrained_IVP='NOT_PROVED', symmetrizer='NOT_TESTED'),
        canonical=dict(MAT_001='BLOCKED', UVIR_003='IN_PROGRESS',
                       K_Q='NOT_DERIVED', V='NOT_COMPUTED', Stage4A='CLOSED'),
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')} |
                     {'selected_indices': result['selected_indices'],
                      'pending_indices': result['pending_indices'],
                      'source_growth': result['source_growth'],
                      'faster_than_p': result['faster_than_p']}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
