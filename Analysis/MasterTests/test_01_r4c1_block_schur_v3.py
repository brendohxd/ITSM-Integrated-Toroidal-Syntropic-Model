"""Complete retained-block multiprecision pilot; no physical admission."""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import heapq
import importlib.util
import json
import multiprocessing as multiprocessing
from pathlib import Path
import time
import traceback

import mpmath as mp
from mpmath.matrices import eigen as me
import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_BLOCK_SCHUR_V3_CONTRACT_2026-10-20.md'
CSHA = 'd3c80312debdf42555bc354f719bc0751bc4531f07d501119f6fb491594b5728'
PARENT = 'Analysis/MasterTests/test_01_r4c1_mp_schur_pilot_v1.py'
PSHA = '6ed31d6064e96a1564d572cd4027e118d93e9a42de6acfc2b99acc4e53e4dece'
BLOCK_PARENT = 'Analysis/MasterTests/test_01_r4c1_exact_canonical_blocks_v1.py'
BSHA = '82a0037f74cf67345ead1cba5f6c7a0de7aae7ab2b6dd09a12067d4c773ddced'
BLOCK_BASE = 'Analysis/MasterTests/outputs/r4c1_exact_canonical_blocks_v1_attempt_01/'
BLOCK_INDEX = BLOCK_BASE + 'independent.json'
ISHA = '2e09e35739ee28d8264f22622cbef663831d8eda34bf9da40a1b07f666afb689'
BRANCHES = ((35, False), (50, False), (50, True))
BUDGET = 600
MAX_WORKERS = 6
_PROGRESS = None


def load_module(name, path, want):
    if SHA((ROOT / path).read_bytes()) != want:
        raise ValueError('frozen parent drift: ' + path)
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load_module('sealed_mp_pilot_v1', PARENT, PSHA)
blocks = load_module('sealed_exact_blocks_v1', BLOCK_PARENT, BSHA)
num = pilot.old.old.num
Checks = pilot.pv.base.Checks
merge = pilot.pv.nodal.reg.joint.merge_checks
ENTRY = next(r for r in json.loads((ROOT / BLOCK_INDEX).read_bytes()) if r['key'] == [4, 17, 0])
BLOCK_FILE = BLOCK_BASE + ENTRY['file']


def sources():
    pins, _ = blocks.sources()
    pins.update({'Analysis/MasterTests/test_01_r4c1_block_schur_v1.py': '30130a8a46405a4e4070c6761a0bab6a6ee860983fca5e752eecf0623429d38c',
                 'Theory/Gates/RES-001/RES001_R4C1_BLOCK_SCHUR_V1_CONTRACT_2026-10-20.md': '3a426ca7f84025ef81e81b9bda4d5bdb8bd78e8e2a43e992ef8fdc8702260909',
                 'Analysis/MasterTests/outputs/r4c1_block_schur_v1_smoke_attempt_01/summary.json': '8277c6e3e5e7dd1dc4943c4ead108e02ccaf401c3749c06b7a8b22b218471244',
                 'Analysis/MasterTests/test_01_r4c1_block_schur_v2.py': '6e204bd698c8caafb4fb7862c427653fd7940e09d9afb38b25d4762361bd7a0c',
                 'Theory/Gates/RES-001/RES001_R4C1_BLOCK_SCHUR_V2_CONTRACT_2026-10-20.md': '91eae56349bdf7de7d6153cc354e6e389751a06c255917702a8bec10c846297d',
                 'Analysis/MasterTests/outputs/r4c1_block_schur_v2_smoke_attempt_01/summary.json': '80a63717e1886cbe4e861d9b7ddac820795c5cbf97c3811679c9ad4e79501d1c',
                 PARENT: PSHA, BLOCK_PARENT: BSHA, CONTRACT: CSHA,
                 BLOCK_INDEX: ISHA, BLOCK_FILE: ENTRY['sha256'],
                 SELF: SHA((ROOT / SELF).read_bytes())})
    meta = {}
    for name, want in pins.items():
        path = ROOT / name
        sidecar = Path(str(path) + '.sha256')
        if SHA(path.read_bytes()) != want or sidecar.read_text().split()[0] != want:
            raise ValueError('source/sidecar drift: ' + name)
        for f in (path, sidecar):
            meta[f.relative_to(ROOT).as_posix()] = num.file_metadata(f)
    lib = Path(me.__file__)
    if mp.__version__ != '1.3.0' or SHA(lib.read_bytes()) != pilot.LIBSHA:
        raise ValueError('installed multiprecision algorithm drift')
    meta['installed-mpmath/eigen.py'] = num.file_metadata(lib)
    return pins, meta


def emit(stage, **kw):
    line = json.dumps(dict(stage=stage, **kw), sort_keys=True)
    print(line, flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a', encoding='utf-8') as stream:
            stream.write(line + '\n')


def directed_components(raw):
    """Exact generator SCCs; row->column edges, ordered for upper triangularity."""
    n = len(raw)
    if not n or any(len(row) != n for row in raw):
        raise ValueError('invalid generator dimension')
    adjacency = []
    for row in raw:
        values = [Decimal(str(x)) for x in row]
        if any(not x.is_finite() for x in values):
            raise ValueError('nonfinite graph input')
        adjacency.append([j for j, x in enumerate(values) if not x.is_zero()])
    counter = 0
    indices, low = {}, {}
    stack, active, groups = [], set(), []

    def visit(v):
        nonlocal counter
        indices[v] = low[v] = counter
        counter += 1
        stack.append(v)
        active.add(v)
        for w in adjacency[v]:
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            group = []
            while True:
                w = stack.pop()
                active.remove(w)
                group.append(w)
                if w == v:
                    break
            groups.append(sorted(group))

    for v in range(n):
        if v not in indices:
            visit(v)
    owner = {v: c for c, g in enumerate(groups) for v in g}
    edges = {c: set() for c in range(len(groups))}
    degree = [0] * len(groups)
    for i in range(n):
        for j in adjacency[i]:
            a, b = owner[i], owner[j]
            if a != b and b not in edges[a]:
                edges[a].add(b)
                degree[b] += 1
    ready = [(min(groups[c]), c) for c, k in enumerate(degree) if not k]
    heapq.heapify(ready)
    ordered = []
    while ready:
        _, c = heapq.heappop(ready)
        ordered.append(groups[c])
        for target in sorted(edges[c], key=lambda z: min(groups[z])):
            degree[target] -= 1
            if not degree[target]:
                heapq.heappush(ready, (min(groups[target]), target))
    if len(ordered) != len(groups):
        raise ValueError('component condensation is not a DAG')
    order = {i: c for c, group in enumerate(ordered) for i in group}
    if sorted(order) != list(range(n)) or any(order[i] > order[j] for i in range(n) for j in adjacency[i]):
        raise ValueError('incomplete or non-upper-triangular component order')
    return ordered


def generator_strings(raw):
    n, d = len(raw), len(raw) // 2
    if n % 2:
        raise ValueError('odd canonical dimension')
    return [[str(Decimal(raw[(i + d) % n][j]).copy_negate()) if i >= d
             else raw[i + d][j] for j in range(n)] for i in range(n)]


def layout():
    source = json.loads(num.check_pair(ROOT / BLOCK_BASE, ENTRY['file']))['data']
    original = json.loads((ROOT / pilot.INPUT).read_bytes())['data']['transformed_forms']['100']
    n = len(original)
    rebuild = [row.copy() for row in original]
    supports = [b['indices'] for b in source['blocks']]
    if sorted(i for support in supports for i in support) != list(range(n)):
        raise ValueError('missing/duplicate original coordinates')
    owner = {i: c for c, support in enumerate(supports) for i in support}
    for i in range(n):
        for j in range(n):
            if owner[i] != owner[j] and not Decimal(original[i][j]).is_zero():
                raise ValueError('canonical offblock entry is nonzero')
    result = []
    for b in source['blocks']:
        support, raw = b['indices'], b['quadratic_form']
        for i, gi in enumerate(support):
            for j, gj in enumerate(support):
                rebuild[gi][gj] = raw[i][j]
        result.append(dict(indices=support, components=directed_components(generator_strings(raw)),
                           dimension=len(support)))
    if rebuild != original or SHA(ENC(rebuild)) != source['serialized_matrix_payload_sha256']:
        raise ValueError('original decimal token reconstruction failed')
    return dict(dimension=n, canonical_blocks=result,
                original_payload_sha256=source['serialized_matrix_payload_sha256'],
                every_coordinate_retained=True, numerical_factors_completed=False)


def block_matrix(block, dps, scaled, structure):
    whole = pilot.prepare(dps, scaled)
    support = structure['canonical_blocks'][block]['indices']
    return mp.matrix([[whole[i, j] for j in support] for i in support])


def component_matrix(task, structure):
    block, component, dps, scaled, _ = task
    matrix = block_matrix(block, dps, scaled, structure)
    support = structure['canonical_blocks'][block]['components'][component]
    return mp.matrix([[matrix[i, j] for j in support] for i in support])


def phase_name(task):
    block, component, dps, scaled, phase = task
    return '%s_b%02d_c%03d_d%d_s%d.json' % (phase, block, component, dps, scaled)


def worker(conn, task, structure, dependency):
    try:
        block, component, dps, scaled, phase = task
        mp.mp.dps = dps
        if phase == 'timeout_control':
            time.sleep(10)
            data = {}
        elif phase == 'hessenberg':
            matrix = component_matrix(task, structure)
            Q, form = (mp.eye(1), matrix.copy()) if matrix.rows == 1 else mp.hessenberg(matrix)
            data = dict(Q=pilot.encm(Q, dps), form=pilot.encm(form, dps), dimension=matrix.rows)
        elif phase == 'schur':
            path, want = dependency
            payload = (ROOT / path).read_bytes()
            if SHA(payload) != want or Path(str(ROOT / path) + '.sha256').read_text().split()[0] != want:
                raise ValueError('phase checkpoint drift')
            data0 = json.loads(payload)['data']
            Q, form = pilot.decm(data0['Q']), pilot.decm(data0['form'])
            if form.rows > 1:
                me.hessenberg_qr(mp.mp, form, Q)
            data = dict(Q=pilot.encm(Q, dps), form=pilot.encm(form, dps), dimension=form.rows,
                        eigenvalues=[pilot.encz(form[i, i], dps) for i in range(form.rows)])
        else:
            raise ValueError('unknown phase')
        conn.send(dict(status='COMPLETED', data=data))
    except BaseException:
        conn.send(dict(status='EXECUTION_ERROR', error=traceback.format_exc()))
    finally:
        conn.close()


def matrix_product_probe(A, Q, form, dps):
    mp.mp.dps = dps
    worst = mp.mpf(0)
    for seed in (1, 3):
        x = mp.matrix([mp.mpf((i * seed + 2) % 11 - 5) for i in range(A.rows)])
        lhs, rhs = A * (Q * x), Q * (form * x)
        scale = 1 + mp.norm(lhs) + mp.norm(rhs)
        worst = max(worst, mp.norm(lhs - rhs) / scale)
    return worst


def verify_factor(matrix, data, phase, dps):
    ch = Checks()
    metrics = pilot.verify(ch, matrix, data, phase, dps)
    probe = matrix_product_probe(matrix, pilot.decm(data['Q']), pilot.decm(data['form']), dps)
    ch.small('independent_complete_coordinate_mp_factor_probes', probe, '1e-8')
    metrics['multiprecision_matvec_probe_not_a_bound'] = mp.nstr(probe, dps)
    return ch.rows, metrics


def owned_timeout_control():
    ctx = multiprocessing.get_context('spawn')
    recv, send = ctx.Pipe(duplex=False)
    process = ctx.Process(target=worker, args=(send, (0, 0, 35, False, 'timeout_control'), {}, None))
    process.start()
    send.close()
    try:
        if recv.poll(3):
            return recv.recv()
        return dict(status='TIME_BUDGET_REACHED')
    finally:
        if process.is_alive():
            process.terminate()
        process.join(5)
        if process.is_alive():
            process.kill()
            process.join(5)
        recv.close()


def smoke():
    ch = Checks()
    mp.mp.dps = 50
    examples = [mp.matrix([[2, 7, 0], [0, -3, 11], [0, 0, 0]]),
                mp.matrix([[0, 1], [0, 0]]), mp.matrix([[0, -1], [1, 0]])]
    for k, matrix in enumerate(examples):
        raw = [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]
        groups = directed_components(raw)
        symbol = blocks.sy.Symbol('lambda')
        exact = blocks.sy.Matrix(raw)
        polynomial = blocks.sy.Integer(1)
        for group in groups:
            subexact = exact.extract(group, group)
            polynomial *= (symbol * blocks.sy.eye(len(group)) - subexact).det()
        ch.add('exact_characteristic_polynomial_%d' % k,
               blocks.sy.expand((symbol * blocks.sy.eye(matrix.rows) - exact).det() - polynomial) == 0)
        order = [i for g in groups for i in g]
        P = mp.matrix([[int(i == j) for j in order] for i in range(matrix.rows)])
        B = P.T * matrix * P
        W, R = mp.eye(matrix.rows), mp.matrix(matrix.rows)
        offset = 0
        for g in groups:
            sub = mp.matrix([[matrix[i, j] for j in g] for i in g])
            Q, H = (mp.eye(1), sub.copy()) if sub.rows == 1 else mp.hessenberg(sub)
            if H.rows > 1:
                me.hessenberg_qr(mp.mp, H, Q)
            for i in range(len(g)):
                for j in range(len(g)):
                    W[offset + i, offset + j] = Q[i, j]
            offset += len(g)
        R = W.H * B * W
        Q = P * W
        data = dict(Q=pilot.encm(Q, 50), form=pilot.encm(R, 50),
                    eigenvalues=[pilot.encz(R[i, i], 50) for i in range(matrix.rows)])
        rows, _ = verify_factor(matrix, data, 'schur', 50)
        merge(ch, rows, 'exact_small_%d_' % k)
        expected = [2, -3, 0] if k == 0 else [0, 0] if k == 1 else [mp.j, -mp.j]
        ch.small('known_spectrum_%d' % k, pilot.spectral_distance(data['eigenvalues'],
                 [pilot.encz(x, 50) for x in expected]), '1e-6')
        if k == 1:
            ch.add('Jordan_coupling_retained', abs(R[0, 1]) > 0)
    ch.add('one_way_coupling_retained_in_separate_components',
           directed_components([['1', '9'], ['0', '2']]) == [[0], [1]])
    ch.add('tiny_return_coupling_merges_components',
           directed_components([['1', '9'], ['1e-300', '2']]) == [[0, 1]])
    ch.add('distinct_zero_spellings_not_nonzero',
           directed_components([['0', '-0.0'], ['0E-80', '0']]) == [[0], [1]])
    # Fixed rescaling must use global indices, not local component order.
    global_support = [2, 5, 8, 11]
    d = 6
    extra = [mp.mpf(2) ** ((i % 3) - 1) for i in range(d)]
    extra += [1 / x for x in extra]
    ch.add('global_configuration_momentum_rescaling_pairs',
           all(extra[i] * extra[i + d] == 1 for i in range(d)) and
           [extra[i] for i in global_support] != [extra[i] for i in range(4)])
    stop = owned_timeout_control()
    ch.add('owned_child_timeout_terminated_joined', stop['status'] == 'TIME_BUDGET_REACHED')
    return ch.rows


def tasks(structure):
    return [(b, c, dps, scaled, phase)
            for dps, scaled in BRANCHES
            for b, block in enumerate(structure['canonical_blocks'])
            for c in range(len(block['components']))
            for phase in ('hessenberg', 'schur')]


def dependency(dest, task):
    if task[-1] != 'schur':
        return None
    name = phase_name((*task[:-1], 'hessenberg'))
    return ((dest / name).relative_to(ROOT).as_posix(), SHA((dest / name).read_bytes()))


def run_phases(dest, structure, runsha, replay):
    all_tasks = tasks(structure)
    pending = list(all_tasks)
    complete, running = {}, {}
    ctx = multiprocessing.get_context('spawn')
    outcome = None
    try:
        while pending or running:
            for task in pending.copy():
                name = phase_name(task)
                if (dest / name).exists() and not replay:
                    obj = json.loads(num.check_pair(dest, name))
                    if obj['run_input_sha256'] != runsha:
                        raise ValueError('foreign factor checkpoint')
                    complete[name] = obj
                    pending.remove(task)
                    continue
                if len(running) >= MAX_WORKERS:
                    break
                if task[-1] == 'schur' and phase_name((*task[:-1], 'hessenberg')) not in complete:
                    continue
                recv, send = ctx.Pipe(duplex=False)
                process = ctx.Process(target=worker, args=(send, task, structure, dependency(dest, task)))
                process.start()
                send.close()
                running[name] = (process, recv, time.monotonic(), task)
                pending.remove(task)
                emit('phase_started', phase=name, pid=process.pid)
            if not running and pending:
                raise ValueError('phase dependency deadlock')
            for name, (process, recv, started, task) in list(running.items()):
                if recv.poll(.1):
                    try:
                        result = recv.recv()
                    except EOFError:
                        result = dict(status='EXECUTION_ERROR', error='owned result pipe closed')
                    process.join(5)
                    if process.is_alive():
                        process.terminate()
                        process.join(5)
                        result = dict(status='EXECUTION_ERROR', error='owned child did not exit after result')
                    recv.close()
                    del running[name]
                    if result['status'] != 'COMPLETED':
                        outcome = dict(phase=name, **result)
                        break
                    matrix = component_matrix(task, structure)
                    rows, metrics = verify_factor(matrix, result['data'], task[-1], task[2])
                    obj = dict(run_input_sha256=runsha, task=list(task), data=result['data'],
                               checks=rows, metrics=metrics)
                    if replay:
                        num.check_pair(dest, name, ENC(obj))
                    else:
                        num.write_pair(dest, name, ENC(obj))
                    complete[name] = obj
                    emit('phase_sealed', phase=name, dimension=matrix.rows,
                         passed=sum(x['passed'] for x in rows), total=len(rows))
                    if any(not row['passed'] for row in rows):
                        outcome = dict(status='NUMERICAL_CHECK_FAILED', phase=name,
                                       failures=[row for row in rows if not row['passed']])
                        break
                elif not process.is_alive():
                    outcome = dict(status='EXECUTION_ERROR', phase=name,
                                   error='owned child exited without result')
                    break
                elif time.monotonic() - started >= BUDGET:
                    outcome = dict(status='TIME_BUDGET_REACHED', phase=name, budget_seconds=BUDGET)
                    break
            if outcome:
                break
            now = time.monotonic()
            if now - run_phases.last_heartbeat >= 15:
                emit('verified_wait', owned_children=[dict(phase=n, pid=p.pid, alive=p.is_alive())
                     for n, (p, _, _, _) in running.items()], sealed=len(complete), pending=len(pending))
                run_phases.last_heartbeat = now
    finally:
        for process, recv, _, _ in running.values():
            if process.is_alive():
                process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join(5)
            recv.close()
    return complete, outcome


run_phases.last_heartbeat = 0


def assemble(dest, structure, complete, runsha, replay):
    ch, spectra, index = Checks(), {}, []
    for dps, scaled in BRANCHES:
        mp.mp.dps = dps
        eigenvalues = []
        for b, block in enumerate(structure['canonical_blocks']):
            A = block_matrix(b, dps, scaled, structure)
            groups = block['components']
            order = [i for g in groups for i in g]
            n = A.rows
            Q = mp.matrix(n)
            for c, group in enumerate(groups):
                obj = complete[phase_name((b, c, dps, scaled, 'schur'))]['data']
                part = pilot.decm(obj['Q'])
                start = sum(len(g) for g in groups[:c])
                for i, original in enumerate(group):
                    for j in range(len(group)):
                        Q[original, start + j] = part[i, j]
            # The multiplication retains all upper-component couplings. If the
            # graph has a single component, reuse its sealed complete Schur form.
            if len(groups) == 1:
                R = pilot.decm(complete[phase_name((b, 0, dps, scaled, 'schur'))]['data']['form'])
            else:
                R = Q.H * A * Q
            data = dict(Q=pilot.encm(Q, dps), form=pilot.encm(R, dps), dimension=n,
                        eigenvalues=[pilot.encz(R[i, i], dps) for i in range(n)],
                        original_coordinate_support=block['indices'], component_order=order)
            rows, metrics = verify_factor(A, data, 'schur', dps)
            merge(ch, rows, 'assembled_b%d_d%d_s%d_' % (b, dps, scaled))
            name = 'complete_b%d_d%d_s%d.json' % (b, dps, scaled)
            obj = dict(run_input_sha256=runsha, data=data, metrics=metrics, checks=rows)
            if replay:
                num.check_pair(dest, name, ENC(obj))
            else:
                num.write_pair(dest, name, ENC(obj))
            index.append(dict(file=name, sha256=SHA(ENC(obj))))
            eigenvalues += data['eigenvalues']
        ch.add('all372_eigenvalues_d%d_s%d' % (dps, scaled), len(eigenvalues) == structure['dimension'] == 372)
        spectra['d%d_s%d' % (dps, scaled)] = eigenvalues
    mp.mp.dps = 65
    ch.small('full372_35_50_spectrum_agreement',
             pilot.spectral_distance(spectra['d35_s0'], spectra['d50_s0']), '1e-6')
    ch.small('full372_independent_canonical_rescaling',
             pilot.spectral_distance(spectra['d50_s0'], spectra['d50_s1']), '1e-6')
    return ch.rows, spectra, index


def execute(args, dest):
    pins, before = sources()
    structure = layout()
    manifest = ENC(dict(source_sha256=pins, source_metadata=before, key=[4, 17, 0],
                        branches=BRANCHES, phase_budget_seconds=BUDGET, max_workers=MAX_WORKERS,
                        mpmath=mp.__version__, backend=pilot.old.old.backend_identity()))
    runsha = SHA(manifest)
    if args.output:
        num.write_pair(dest, 'run_inputs.json', manifest)
        num.write_pair(dest, 'structure.json', ENC(structure))
    else:
        num.check_pair(dest, 'run_inputs.json', manifest)
        num.check_pair(dest, 'structure.json', ENC(structure))
    emit('complete_layout', blocks=[dict(dimension=b['dimension'],
         component_dimensions=[len(g) for g in b['components']]) for b in structure['canonical_blocks']])
    if args.prepare:
        emit('PREPARED_NO_FACTORIZATION', coordinates=structure['dimension'])
        return 0
    control_rows = smoke()
    if any(not row['passed'] for row in control_rows):
        raise ValueError('execution/algebra controls failed: ' + str([r for r in control_rows if not r['passed']]))
    complete, outcome = run_phases(dest, structure, runsha, bool(args.replay))
    ch = Checks()
    merge(ch, control_rows, 'control_')
    for name, obj in sorted(complete.items()):
        merge(ch, obj['checks'], name + '_')
    full = len(complete) == len(tasks(structure)) and outcome is None
    spectra, index = {}, []
    if full:
        rows, spectra, index = assemble(dest, structure, complete, runsha, bool(args.replay))
        merge(ch, rows, 'assembled_')
    else:
        ch.add('complete_precision_pilot', False, str(outcome))
    _, after = sources()
    ch.add('source_sidecar_metadata_unchanged', before == after)
    passed = sum(row['passed'] for row in ch.rows)
    summary = dict(validation='PASS_ONE_COMPLETE_CASE_SCHUR_ONLY' if full and passed == len(ch.rows)
                   else 'UNRESOLVED_OR_EXECUTION_LIMIT_BLOCK_SCHUR', passed=passed, total=len(ch.rows),
                   checks=ch.rows, source_sha256=pins, source_metadata=before,
                   execution_status=outcome or 'COMPLETED', completed_phases=sorted(complete),
                   full372_precision_pilot_completed=full, complete_family_coverage=False,
                   left_right_physical_modes_normalized=False, certified_eigenvalue_enclosures=False,
                   stage2_complete=False, stage3_entered=False, physics_pass=False, gate_effect='NONE',
                   review_status='DEFERRED', Rule9_cleared=False)
    independent = dict(full_factor_index=index, complete_spectra=spectra,
                       retained_negative_action_and_nonoscillatory_evidence=True)
    formulas = dict(scope='Complete372 coordinate pilot, exact canonical/SCC organization, all couplings retained',
                    holds='Physical modes/energy/clock, other cases, continuum/node, nonlinear interactions/cutoff, healthy GR, identifying matching inputs')
    for name, obj in (('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)):
        if args.replay:
            num.check_pair(dest, name, ENC(obj))
        else:
            num.write_pair(dest, name, ENC(obj))
    emit('terminal', **{k: summary[k] for k in ('validation', 'passed', 'total', 'execution_status', 'full372_precision_pilot_completed')})
    return 0 if full and passed == len(ch.rows) else 1


def main():
    global _PROGRESS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--resume')
    parser.add_argument('--replay')
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--progress-log')
    args = parser.parse_args()
    if args.smoke:
        if any((args.output, args.resume, args.replay, args.prepare)):
            parser.error('smoke is execution/algebra only')
        _, before = sources()
        rows = smoke()
        _, after = sources()
        if before != after:
            raise ValueError('smoke source mutation')
        emit('EXECUTION_ALGEBRA_ONLY', passed=sum(r['passed'] for r in rows), total=len(rows),
             failed=[r for r in rows if not r['passed']])
        return 0 if all(r['passed'] for r in rows) else 1
    if sum(bool(x) for x in (args.output, args.resume, args.replay)) != 1:
        parser.error('choose fresh output, unfinished resume, or exact read-only replay')
    if args.prepare and not args.output:
        parser.error('prepare is only valid for a fresh output')
    dest = (ROOT / (args.output or args.resume or args.replay)).resolve()
    if not dest.is_relative_to(ROOT / 'Analysis/MasterTests/outputs'):
        raise ValueError('outside research output root')
    if args.output:
        dest.mkdir(parents=True, exist_ok=False)
    if args.resume and (dest / 'summary.json').exists():
        raise ValueError('terminal attempt cannot resume')
    if args.progress_log:
        _PROGRESS = (ROOT / args.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT / '.local/itsm-context'):
            raise ValueError('private progress outside ignored root')
        with _PROGRESS.open('x', encoding='utf-8'):
            pass
    before = {p.name: num.file_metadata(p) for p in dest.iterdir()} if args.replay else None
    rc = execute(args, dest)
    if args.replay:
        if before != {p.name: num.file_metadata(p) for p in dest.iterdir()}:
            raise ValueError('read-only replay changed output bytes/metadata/file set')
        print('READ_ONLY_REPLAY_EXACT', flush=True)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
