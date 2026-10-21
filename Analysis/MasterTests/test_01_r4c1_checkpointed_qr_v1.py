"""Resumable complete QR, same R4C1 matrices and pinned mpmath iteration rules."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import re
import shutil
import sys
import time
import traceback
import zlib

import mpmath as mp
from mpmath.matrices import eigen as me

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
PARENT = 'Analysis/MasterTests/test_01_r4c1_block_schur_v3.py'
PSHA = '3b02e4e127542a1f7544db7d1fa2efff68fa39cf86607421e4189b31fb3b4b56'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_CHECKPOINTED_QR_V1_CONTRACT_2026-10-21.md'
CSHA = '82ec3ebb3eb3eeb2e3c99be54751f703528749bb1ee2b7db6fdafd0fa0482525'
REPORT = 'Theory/Gates/RES-001/RES001_R4C1_BLOCK_SCHUR_V3_REPORT_2026-10-21.md'
RSHA = '36d7f109cd5c40a03910b83c1430e6ebe2d256a60885d6751a9f98532128bac6'
BASE = 'Analysis/MasterTests/outputs/r4c1_block_schur_v3_attempt_01/'
INPUT_HASHES = {
    'formulas.json': 'c907560c8174664fff9d487544392e19309f143bc37614b8257de1ef8ea936c1',
    'hessenberg_b00_c000_d35_s0.json': '7d98e3c9652f8d44f4829124c2d958e2fe28db66fb9a52d4f5e8076748e2881e',
    'hessenberg_b00_c000_d50_s0.json': 'af6b989de412e0e3686911c850c127945eb1624a3b384dc27b54ffd5c4b9a078',
    'hessenberg_b00_c000_d50_s1.json': 'f145587ff75597009b02ba3933b043dc5d18568eff917aa045dc0039bb66f0c5',
    'hessenberg_b01_c000_d35_s0.json': '5f1e653be7630d9016428ce5fdf5d9f0ed6062619363505614e5f5321de9fb14',
    'hessenberg_b01_c000_d50_s0.json': 'e5f16ff069b485b00c19d769ae3b367b24371fc2ac61a4bd34bd778380223204',
    'hessenberg_b01_c000_d50_s1.json': 'eb5ba79f08ffc731528266031da77c43ec0dfef3d7934720a132f9c2e0120325',
    'independent.json': '8229a9085382248293110d25e64f100257b3d0dd732125f4a5b8030253e54f39',
    'run_inputs.json': 'd965f78df99eb556eb20340fbd57da8c7afcd02a5d63012f3b6fb4341d86466a',
    'schur_b01_c000_d35_s0.json': '95930bc0ec1cebf3dff86beafcb1cf1a1ee3e3c6fc2b95c4a94ec5a92e72b7d7',
    'schur_b01_c000_d50_s0.json': '311db03667d2336145a5c6697c6388ead1f56a195fb5f33acba436b0a09cd7e0',
    'schur_b01_c000_d50_s1.json': '78a600ca44314cbd520d4c3f15024e3d367e32d3d4b7e17cdbb6296d3866ab31',
    'structure.json': '185cea8d9ae312b9c1c55b79dd2d16e28289dd8322d254af7ec7f17fd5b0b502',
    'summary.json': '3b7a3bb92b386f42708bf4bc1650020f69e6efb1069793c9e79356adac8adb2a',
}
if SHA((ROOT / PARENT).read_bytes()) != PSHA:
    raise ValueError('parent drift')
spec = importlib.util.spec_from_file_location('frozen_block_schur_v3', ROOT / PARENT)
v3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v3)
num, Checks, merge = v3.num, v3.Checks, v3.merge
BRANCHES = v3.BRANCHES
QUANTUM = 4
TRANCHE = 12
CHILD_BUDGET = 180
OUTPUT_CAP = 2 * 1024 ** 3
FREE_FLOOR = 3 * 1024 ** 3
_PROGRESS = None
STATE_FIELDS = {'n0', 'n1', 'its', 'totalits', 'outer_steps', 'norm', 'eps',
                'maxits', 'precision_bits', 'done'}


def sources():
    pins, _ = v3.sources()
    pins.update({PARENT: PSHA, CONTRACT: CSHA, REPORT: RSHA,
                 SELF: SHA((ROOT / SELF).read_bytes()), **{BASE + k: v for k, v in INPUT_HASHES.items()}})
    meta = {}
    for name, want in pins.items():
        path = ROOT / name
        if SHA(path.read_bytes()) != want or Path(str(path) + '.sha256').read_text().split()[0] != want:
            raise ValueError('source drift: ' + name)
        for item in (path, Path(str(path) + '.sha256')):
            meta[item.relative_to(ROOT).as_posix()] = num.file_metadata(item)
    for label, path in [('mpmath/eigen.py', Path(me.__file__)),
                        ('python/gzip.py', Path(gzip.__file__)), ('python/zlib', Path(zlib.__file__))]:
        meta['installed/' + label] = num.file_metadata(path)
    if mp.__version__ != '1.3.0' or SHA(Path(me.__file__).read_bytes()) != v3.pilot.LIBSHA:
        raise ValueError('pinned QR algorithm drift')
    return pins, meta


def emit(stage, **kw):
    line = json.dumps(dict(stage=stage, **kw), sort_keys=True)
    print(line, flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a', encoding='utf-8') as f:
            f.write(line + '\n')


def encstate(state):
    return {k: mp.nstr(value, mp.mp.dps + 12) if k in ('norm', 'eps') else value
            for k, value in state.items()}


def decstate(state):
    if set(state) != STATE_FIELDS:
        raise ValueError('missing or foreign QR resume state')
    answer = {k: mp.mpf(value) if k in ('norm', 'eps') else value for k, value in state.items()}
    if answer['precision_bits'] != mp.mp.prec or answer['maxits'] != 4 * mp.mp.dps:
        raise ValueError('QR resume precision/convergence-limit mismatch')
    return answer


# The local outer-loop driver below follows mpmath1.3.0 eigen.py:hessenberg_qr.
# Only checkpoint boundaries/state handling are added; installed qr_step is used.
# Copyright (c) 2005-2021 Fredrik Johansson and mpmath contributors
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# a. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# b. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# c. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
def initial_state(A):
    n = A.rows
    if n < 1 or A.cols != n:
        raise ValueError('invalid QR input')
    norm = 0
    for x in range(n):
        for y in range(min(x + 2, n)):
            norm += mp.re(A[y, x]) ** 2 + mp.im(A[y, x]) ** 2
    norm = mp.sqrt(norm) / n
    return dict(n0=0, n1=n, its=0, totalits=0, outer_steps=0, norm=norm,
                eps=mp.mp.eps / (100 * n), maxits=mp.mp.dps * 4,
                precision_bits=mp.mp.prec, done=bool(norm == 0 or n == 1))


def qr_quantum(A, Q, state, count=QUANTUM):
    state = decstate(encstate(state))
    n = A.rows
    if state['eps'] != mp.mp.eps / (100 * n):
        raise ValueError('QR epsilon changed')
    if not (0 <= state['n0'] < state['n1'] <= n):
        raise ValueError('invalid QR active domain')
    if state['done']:
        return state
    n0, n1, its, totalits = (state[k] for k in ('n0', 'n1', 'its', 'totalits'))
    norm, eps, maxits = (state[k] for k in ('norm', 'eps', 'maxits'))
    for _ in range(count):
        k = n0
        while k + 1 < n1:
            s = abs(mp.re(A[k, k])) + abs(mp.im(A[k, k])) + abs(mp.re(A[k + 1, k + 1])) + abs(mp.im(A[k + 1, k + 1]))
            if s < eps * norm:
                s = norm
            if abs(A[k + 1, k]) < eps * s:
                break
            k += 1
        state['outer_steps'] += 1
        if k + 1 < n1:
            A[k + 1, k] = 0
            n0, its = k + 1, 0
            if n0 + 1 >= n1:
                n0, n1 = 0, k + 1
                if n1 < 2:
                    state.update(n0=n0, n1=n1, its=its, totalits=totalits, done=True)
                    return state
        else:
            if its % 30 == 10:
                shift = A[n1 - 1, n1 - 2]
            elif its % 30 == 20:
                shift = abs(A[n1 - 1, n1 - 2])
            elif its % 30 == 29:
                shift = norm
            else:
                t = A[n1 - 2, n1 - 2] + A[n1 - 1, n1 - 1]
                s = (A[n1 - 1, n1 - 1] - A[n1 - 2, n1 - 2]) ** 2 + 4 * A[n1 - 1, n1 - 2] * A[n1 - 2, n1 - 1]
                s = mp.sqrt(s) if mp.re(s) > 0 else mp.sqrt(-s) * 1j
                a, b = (t + s) / 2, (t - s) / 2
                shift = b if abs(A[n1 - 1, n1 - 1] - a) > abs(A[n1 - 1, n1 - 1] - b) else a
            its += 1
            totalits += 1
            me.qr_step(mp.mp, n0, n1, A, Q, shift)
            if its > maxits:
                raise RuntimeError('qr: failed to converge after %d steps' % its)
        state.update(n0=n0, n1=n1, its=its, totalits=totalits)
    return state


def input_name(branch):
    dps, scaled = BRANCHES[branch]
    return 'hessenberg_b00_c000_d%d_s%d.json' % (dps, scaled)


def validate_reference_state(state, expected):
    if state['norm'] != expected['norm'] or state['eps'] != expected['eps']:
        raise ValueError('initial norm/epsilon not retained')


def predecessor(dest, branch, index):
    if index == 1:
        name = input_name(branch)
        return BASE + name, INPUT_HASHES[name]
    name = checkpoint_name(branch, index - 1)
    payload = num.check_pair(dest, name)
    return (dest / name).relative_to(ROOT).as_posix(), SHA(payload)


def read_state(path, want, branch):
    payload = (ROOT / path).read_bytes()
    if SHA(payload) != want or Path(str(ROOT / path) + '.sha256').read_text().split()[0] != want:
        raise ValueError('QR checkpoint predecessor drift')
    obj = json.loads(gzip.decompress(payload) if path.endswith('.gz') else payload)
    data = obj['data']
    Q, H = v3.pilot.decm(data['Q']), v3.pilot.decm(data['form'])
    state = decstate(data['state']) if 'state' in data else initial_state(H)
    original = json.loads((ROOT / (BASE + input_name(branch))).read_bytes())['data']
    expected = initial_state(v3.pilot.decm(original['form']))
    validate_reference_state(state, expected)
    return Q, H, state


def worker(conn, branch, path, want, timeout_control=False):
    try:
        if timeout_control:
            time.sleep(10)
            result = dict(status='UNEXPECTED_CONTROL_COMPLETION')
        else:
            dps, _ = BRANCHES[branch]
            mp.mp.dps = dps
            Q, H, state = read_state(path, want, branch)
            state = qr_quantum(H, Q, state)
            data = dict(Q=v3.pilot.encm(Q, dps), form=v3.pilot.encm(H, dps),
                        state=encstate(state), dimension=H.rows)
            if state['done']:
                data['eigenvalues'] = [v3.pilot.encz(H[i, i], dps) for i in range(H.rows)]
            result = dict(status='COMPLETED', data=data)
        conn.send(result)
    except BaseException:
        conn.send(dict(status='EXECUTION_ERROR', error=traceback.format_exc()))
    finally:
        conn.close()


def bounded_round(tasks, control=False):
    ctx = multiprocessing.get_context('spawn')
    active, results, failure = {}, {}, None
    heartbeat = time.monotonic()
    try:
        for branch, path, want in tasks:
            recv, send = ctx.Pipe(duplex=False)
            process = ctx.Process(target=worker, args=(send, branch, path, want, control))
            process.start()
            send.close()
            active[branch] = process, recv, time.monotonic()
            emit('quantum_started', branch=branch, pid=process.pid)
        while active:
            for branch, (process, recv, started) in list(active.items()):
                if recv.poll(.1):
                    try:
                        result = recv.recv()
                    except EOFError:
                        result = dict(status='EXECUTION_ERROR', error='owned result pipe closed')
                    process.join(5)
                    if process.is_alive():
                        result = dict(status='EXECUTION_ERROR', error='owned child did not exit')
                    else:
                        recv.close()
                        del active[branch]
                    if result['status'] != 'COMPLETED':
                        failure = dict(branch=branch, **result)
                        break
                    results[branch] = result['data']
                elif not process.is_alive():
                    failure = dict(branch=branch, status='EXECUTION_ERROR', error='owned child exited without result')
                    break
                elif time.monotonic() - started >= (3 if control else CHILD_BUDGET):
                    failure = dict(branch=branch, status='TIME_BUDGET_REACHED')
                    break
            if failure:
                break
            now = time.monotonic()
            if now - heartbeat >= 15:
                emit('verified_quantum_wait', children=[dict(branch=b, pid=p.pid, alive=p.is_alive())
                     for b, (p, _, _) in active.items()])
                heartbeat = now
    finally:
        for process, recv, _ in active.values():
            if process.is_alive():
                process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join(5)
            recv.close()
    return results, failure


def smoke():
    ch = Checks()
    for dps in (35, 50):
        mp.mp.dps = dps
        hadamard = mp.matrix([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]) / 2
        triangular = mp.matrix([[-3, mp.mpf(1) / 7, 0, 1], [0, -1, 1, 0], [0, 0, 2, 1], [0, 0, 0, 5]])
        examples = [hadamard * triangular * hadamard.T,
                    mp.matrix([[0, 1], [0, 0]]), mp.matrix([[0, -1], [1, 0]]),
                    mp.zeros(3), mp.matrix([[mp.j, 2, 1], [3, -mp.j, 4], [1, 2, -2]]),
                    mp.matrix([[1, mp.mpf('1e12'), 0], [mp.mpf('1e-12'), 1, 1], [0, 1, 2]])]
        for i, matrix in enumerate(examples):
            Q0, H0 = mp.hessenberg(matrix)
            Qref, Rref = Q0.copy(), H0.copy()
            me.hessenberg_qr(mp.mp, Rref, Qref)
            Q, H, state = Q0.copy(), H0.copy(), initial_state(H0)
            for count in range(1000):
                if state['done']:
                    break
                state = qr_quantum(H, Q, state, count=1)
                package = ENC(dict(Q=v3.pilot.encm(Q, dps), H=v3.pilot.encm(H, dps), state=encstate(state)))
                decoded = json.loads(gzip.decompress(gzip.compress(package, compresslevel=1, mtime=0)))
                Q, H, state = v3.pilot.decm(decoded['Q']), v3.pilot.decm(decoded['H']), decstate(decoded['state'])
            ch.add('serialized_stop_resume_complete_%d_%d' % (dps, i), bool(state['done']))
            ch.add('identical_installed_QR_arrays_%d_%d' % (dps, i),
                   v3.pilot.encm(Q, dps) == v3.pilot.encm(Qref, dps) and v3.pilot.encm(H, dps) == v3.pilot.encm(Rref, dps))
            data = dict(Q=v3.pilot.encm(Q, dps), form=v3.pilot.encm(H, dps), dimension=H.rows,
                        eigenvalues=[v3.pilot.encz(H[j, j], dps) for j in range(H.rows)])
            rows, _ = v3.verify_factor(matrix, data, 'schur', dps)
            merge(ch, rows, 'small_%d_%d_' % (dps, i))
        bad = encstate(initial_state(mp.eye(2)))
        del bad['norm']
        try:
            decstate(bad)
        except ValueError:
            rejected = True
        else:
            rejected = False
        ch.add('omitted_resume_field_rejected_%d' % dps, rejected)
        bad = encstate(initial_state(mp.eye(2)))
        bad['precision_bits'] += 1
        try:
            decstate(bad)
        except ValueError:
            rejected = True
        else:
            rejected = False
        ch.add('wrong_resume_precision_rejected_%d' % dps, rejected)
        reference = initial_state(mp.eye(2))
        bad = dict(reference)
        bad['norm'] += 1
        try:
            validate_reference_state(bad, reference)
        except ValueError:
            rejected = True
        else:
            rejected = False
        ch.add('changed_original_norm_rejected_%d' % dps, rejected)
    _, failure = bounded_round([(0, '', '')], control=True)
    ch.add('owned_timeout_and_cleanup', failure is not None and failure['status'] == 'TIME_BUDGET_REACHED')
    return ch.rows


def checkpoint_name(branch, index):
    return 'checkpoint_b%d_q%05d.json.gz' % (branch, index)


def checkpoints(dest):
    result = {b: [] for b in range(3)}
    for path in sorted(dest.glob('checkpoint_*.json.gz')):
        match = re.fullmatch(r'checkpoint_b([0-2])_q([0-9]{5})\.json\.gz', path.name)
        if not match:
            raise ValueError('foreign checkpoint name')
        b, index = map(int, match.groups())
        if index != len(result[b]) + 1:
            raise ValueError('missing or out-of-order quantum')
        result[b].append(path.name)
    return result


def read_checkpoint(dest, name):
    return json.loads(gzip.decompress(num.check_pair(dest, name)))


def latest(dest, branch, names):
    return read_checkpoint(dest, names[-1])['data']['state'] if names else None


def verify_checkpoint(branch, data, previous, structure):
    dps, scaled = BRANCHES[branch]
    mp.mp.dps = dps
    state = decstate(data['state'])
    if previous is None:
        previous = initial_state(v3.pilot.decm(json.loads((ROOT / (BASE + input_name(branch))).read_bytes())['data']['form']))
    else:
        previous = decstate(previous)
    ch = Checks()
    ch.add('monotone_bounded_outer_iteration_progress',
           previous['outer_steps'] < state['outer_steps'] <= previous['outer_steps'] + QUANTUM)
    ch.add('iteration_and_active_domain_retained',
           state['totalits'] >= previous['totalits'] and state['n1'] <= previous['n1'] and
           state['norm'] == previous['norm'] and state['eps'] == previous['eps'])
    A = v3.block_matrix(0, dps, scaled, structure)
    rows, metrics = v3.verify_factor(A, data, 'schur' if state['done'] else 'hessenberg', dps)
    merge(ch, rows, 'full302_')
    if not state['done']:
        H = v3.pilot.decm(data['form'])
        atrace = sum(A[i, i] for i in range(A.rows))
        htrace = sum(H[i, i] for i in range(H.rows))
        ch.small('full_trace_retained', abs(atrace - htrace) / (1 + abs(atrace) + abs(htrace)), '1e-8')
        a2 = sum(A[i, j] * A[j, i] for i in range(A.rows) for j in range(A.rows))
        h2 = sum(H[i, j] * H[j, i] for i in range(H.rows) for j in range(H.rows))
        ch.small('full_trace_square_retained', abs(a2 - h2) / (1 + abs(a2) + abs(h2)), '1e-8')
    return ch.rows, metrics


def create_checkpoint(dest, branch, index, data, runsha, previous, structure, replay=False):
    path, want = predecessor(dest, branch, index)
    rows, metrics = verify_checkpoint(branch, data, previous, structure)
    obj = dict(run_input_sha256=runsha, branch=branch, quantum=index,
               predecessor=dict(path=path, sha256=want), data=data, checks=rows, metrics=metrics)
    payload = gzip.compress(ENC(obj), compresslevel=1, mtime=0)
    name = checkpoint_name(branch, index)
    if replay:
        num.check_pair(dest, name, payload)
    else:
        if sum(p.stat().st_size for p in dest.iterdir()) + len(payload) > OUTPUT_CAP:
            raise ValueError('retained-output storage cap reached; delete nothing')
        num.write_pair(dest, name, payload)
    emit('quantum_sealed', branch=branch, quantum=index, outer_steps=data['state']['outer_steps'],
         qr_steps=data['state']['totalits'], active_end=data['state']['n1'], done=data['state']['done'],
         passed=sum(row['passed'] for row in rows), total=len(rows))
    return obj


def complete_comparisons(dest, names, structure, ch):
    spectra = []
    for branch, (dps, scaled) in enumerate(BRANCHES):
        large = read_checkpoint(dest, names[branch][-1])['data']
        small_name = 'schur_b01_c000_d%d_s%d.json' % (dps, scaled)
        small = json.loads((ROOT / (BASE + small_name)).read_bytes())['data']
        rows, _ = v3.verify_factor(v3.block_matrix(1, dps, scaled, structure), small, 'schur', dps)
        merge(ch, rows, 'retained70_b%d_' % branch)
        values = large['eigenvalues'] + small['eigenvalues']
        ch.add('all372_modes_b%d' % branch, len(values) == 372)
        spectra.append(values)
    mp.mp.dps = 65
    ch.small('complete372_35_50_precision_agreement', v3.pilot.spectral_distance(spectra[0], spectra[1]), '1e-6')
    ch.small('complete372_fixed_canonical_rescaling', v3.pilot.spectral_distance(spectra[1], spectra[2]), '1e-6')
    return spectra


def tranche_summary(dest, names, source_unchanged, structure, stop, failure=None):
    ch = Checks()
    for branch in range(3):
        for name in names[branch]:
            merge(ch, read_checkpoint(dest, name)['checks'], name + '_')
    ch.add('source_sidecar_metadata_unchanged', source_unchanged)
    completed = all(names[b] and latest(dest, b, names[b])['done'] for b in range(3))
    spectra = complete_comparisons(dest, names, structure, ch) if completed else []
    return dict(validation='PASS_ONE_COMPLETE_CASE_PRECISION_ONLY' if completed and all(r['passed'] for r in ch.rows)
                else 'CHECKPOINTED_INCOMPLETE' if failure is None and all(r['passed'] for r in ch.rows)
                else 'UNRESOLVED_OR_EXECUTION_ERROR', passed=sum(r['passed'] for r in ch.rows), total=len(ch.rows),
                checks=ch.rows, checkpoint_names=names, latest_state={b: latest(dest, b, names[b]) for b in range(3)},
                stop_reason=stop, execution_failure=failure, full372_precision_completed=completed,
                complete_spectra=spectra, all_family_coverage=False, physical_modes_normalized=False,
                certified_eigenvalue_enclosures=False, stage2_complete=False, stage3_entered=False,
                physics_pass=False, gate_effect='NONE', Rule9_cleared=False, review_status='DEFERRED')


def execute(args, dest):
    pins, before = sources()
    manifest = ENC(dict(source_sha256=pins, source_metadata=before, branches=BRANCHES,
                        quantum=QUANTUM, tranche=TRANCHE, child_budget=CHILD_BUDGET,
                        output_cap=OUTPUT_CAP, free_floor=FREE_FLOOR, python=sys.version,
                        zlib_version=zlib.ZLIB_VERSION, zlib_runtime_version=zlib.ZLIB_RUNTIME_VERSION))
    runsha = SHA(manifest)
    structure = v3.layout()
    if args.output:
        num.write_pair(dest, 'run_inputs.json', manifest)
    else:
        num.check_pair(dest, 'run_inputs.json', manifest)
    if args.replay:
        existing = checkpoints(dest)
        for index in range(1, max(map(len, existing.values()), default=0) + 1):
            tasks = [(b, *predecessor(dest, b, index)) for b in range(3) if len(existing[b]) >= index]
            results, failure = bounded_round(tasks)
            if failure:
                raise ValueError('replay execution failure: ' + str(failure))
            for b in sorted(results):
                previous = read_checkpoint(dest, existing[b][index - 2])['data']['state'] if index > 1 else None
                create_checkpoint(dest, b, index, results[b], runsha, previous, structure, replay=True)
        for path in sorted(dest.glob('tranche_*_summary.json')):
            expected = json.loads(num.check_pair(dest, path.name))
            names = {int(b): v for b, v in expected['checkpoint_names'].items()}
            _, after = sources()
            actual = tranche_summary(dest, names, before == after, structure, expected['stop_reason'], expected['execution_failure'])
            num.check_pair(dest, path.name, ENC(actual))
        return 0
    if (dest / 'summary.json').exists():
        raise ValueError('terminal attempt cannot advance')
    if shutil.disk_usage(dest).free < FREE_FLOOR:
        raise ValueError('less than3GiB free; advance stopped without deletion')
    failure = None
    for _ in range(TRANCHE):
        names = checkpoints(dest)
        tasks = [(b, *predecessor(dest, b, len(names[b]) + 1)) for b in range(3)
                 if not names[b] or not latest(dest, b, names[b])['done']]
        if not tasks:
            break
        results, failure = bounded_round(tasks)
        for b in sorted(results):
            previous = latest(dest, b, names[b])
            obj = create_checkpoint(dest, b, len(names[b]) + 1, results[b], runsha, previous, structure)
            if any(not row['passed'] for row in obj['checks']):
                failure = dict(status='NUMERICAL_CHECK_FAILED', branch=b)
        if failure:
            break
    names = checkpoints(dest)
    _, after = sources()
    stop = 'EXECUTION_FAILURE' if failure else 'TRANCHE_CHECKPOINTED'
    summary = tranche_summary(dest, names, before == after, structure, stop, failure)
    index = len(list(dest.glob('tranche_*_summary.json'))) + 1
    num.write_pair(dest, 'tranche_%04d_summary.json' % index, ENC(summary))
    if failure or summary['full372_precision_completed']:
        num.write_pair(dest, 'summary.json', ENC(summary))
    emit('tranche_sealed', tranche=index, **{k: summary[k] for k in
         ('validation', 'passed', 'total', 'full372_precision_completed', 'execution_failure')})
    return 0 if failure is None and summary['passed'] == summary['total'] else 1


def main():
    global _PROGRESS
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ('output', 'advance', 'replay', 'progress-log'):
        parser.add_argument('--' + option)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.smoke:
        if any((args.output, args.advance, args.replay)):
            parser.error('smoke is execution/algebra only')
        rows = smoke()
        emit('EXECUTION_ALGEBRA_ONLY', passed=sum(r['passed'] for r in rows), total=len(rows),
             failed=[r for r in rows if not r['passed']])
        return 0 if all(r['passed'] for r in rows) else 1
    if sum(bool(x) for x in (args.output, args.advance, args.replay)) != 1:
        parser.error('choose fresh output, saved advance or read-only replay')
    dest = (ROOT / (args.output or args.advance or args.replay)).resolve()
    if not dest.is_relative_to(ROOT / 'Analysis/MasterTests/outputs'):
        raise ValueError('outside research output root')
    if args.output:
        dest.mkdir(parents=True, exist_ok=False)
    if args.progress_log:
        _PROGRESS = (ROOT / args.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT / '.local/itsm-context'):
            raise ValueError('outside ignored progress root')
        with _PROGRESS.open('x', encoding='utf-8'):
            pass
    before = {p.name: num.file_metadata(p) for p in dest.iterdir()} if args.replay else None
    result = execute(args, dest)
    if args.replay:
        if before != {p.name: num.file_metadata(p) for p in dest.iterdir()}:
            raise ValueError('read-only replay changed bytes/metadata/file set')
        print('READ_ONLY_REPLAY_EXACT', flush=True)
    return result


if __name__ == '__main__':
    raise SystemExit(main())
