"""Restartable local exact replay of the frozen source-aware V1 computation."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys

import numpy as np
import sympy
import test_01_r4c1_cusp3_source_aware_window_v1 as frozen

ROOT = frozen.ROOT
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_SOURCE_AWARE_WINDOW_V1_REPLAY_ADDENDUM_2026-10-17.md'
SOURCE_SHA = '994f26566358ddaa01032f3608bddb8ce3f570fc23429d5a423c3289104c38a1'
SUMMARY_SHA = '35cd15dbedcb2ef6be3acfc41a1e43d9a1392100db1b05c7989c5a4f0e21bc90'
ORIGINAL = ROOT / frozen.BASE / 'r4c1_cusp3_source_aware_window_attempt_01'
DEFAULT = frozen.BASE + 'r4c1_cusp3_source_aware_replay_attempt_01'


def sha(body):
    return hashlib.sha256(body).hexdigest()


def exclusive(path, body):
    with path.open('xb') as stream:
        stream.write(body)


def write_checked(path, body):
    exclusive(path, body)
    exclusive(Path(str(path) + '.sha256'), (sha(body) + '  ' + path.name + '\n').encode())


def checked(path):
    body = path.read_bytes()
    expected = (sha(body) + '  ' + path.name + '\n').encode()
    if Path(str(path) + '.sha256').read_bytes() != expected:
        raise ValueError('Checkpoint sidecar drift: ' + str(path))
    return body


def compare_original(name, body):
    if checked(ORIGINAL / name) != body:
        raise ValueError('Immutable replay differs: ' + name)


def snapshot(paths):
    return [(p.relative_to(ROOT).as_posix(), sha(p.read_bytes()),
             p.stat().st_size, p.stat().st_mtime_ns) for p in sorted(set(paths))]


def fresh_case(index):
    # No original receipt is substituted for a calculation here.
    ch = frozen.Checks()
    with contextlib.redirect_stdout(io.StringIO()):
        red = frozen.parent.evolving.EvolvingReduction(frozen.parent.prior, frozen.parent.generic)
        record = frozen.Case(index, ch).run(red)
    record['accepted'] = all(row['passed'] for row in ch.rows)
    body = frozen.ENCODE(record)
    compare_original(f'case_{index:02d}.json', body)
    if not record['accepted']:
        raise ValueError(f'Fresh case {index} failed')
    return index, body


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', default=DEFAULT)
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--workers', type=int, default=min(4, os.cpu_count() or 1))
    args = ap.parse_args()
    if not 1 <= args.workers <= min(9, os.cpu_count() or 1):
        raise ValueError('Worker count outside local CPU/case bounds')
    dest = (ROOT / args.output).resolve()
    dest.relative_to((ROOT / frozen.BASE).resolve())
    if dest == ORIGINAL or ORIGINAL in dest.parents:
        raise ValueError('Replay checkpoints must not enter original evidence')
    if sha((ROOT / frozen.SELF).read_bytes()) != SOURCE_SHA:
        raise ValueError('Frozen executable drift')
    if sha((ORIGINAL / 'summary.json').read_bytes()) != SUMMARY_SHA:
        raise ValueError('Frozen summary drift')
    pins, absent, source_snapshot = frozen.inputs()
    extra = [ROOT / SELF, ROOT / ADDENDUM]
    for path in list(extra):
        checked(path)
        extra.append(Path(str(path) + '.sha256'))
    original_paths = sorted(ORIGINAL.iterdir())
    if any(not p.is_file() for p in original_paths):
        raise ValueError('Unexpected non-file original evidence')
    initial = dict(schema='source-aware-replay-manifest-v1',
        source_metadata=source_snapshot(), original_metadata=snapshot(original_paths),
        replay_metadata=snapshot(extra), runtime=dict(python=platform.python_version(),
            numpy=np.__version__, sympy=sympy.__version__),
        original_summary_sha256=SUMMARY_SHA, frozen_source_sha256=SOURCE_SHA)
    initial_body = frozen.ENCODE(initial)
    if args.resume:
        if checked(dest / 'manifest.json') != initial_body:
            raise ValueError('Resume manifest/source/runtime/original metadata drift')
        if (dest / 'receipt.json').exists():
            raise ValueError('Replay already complete; preserve its receipt')
    else:
        dest.mkdir(parents=False, exist_ok=False)
        write_checked(dest / 'manifest.json', initial_body)
    pending = []
    for i in range(9):
        name = f'case_{i:02d}.json'
        path = dest / name
        if path.exists():
            body = checked(path)
            compare_original(name, body)
            print(json.dumps(dict(stage='REUSE_VERIFIED_CHECKPOINT', index=i)), flush=True)
        else:
            if Path(str(path) + '.sha256').exists():
                raise ValueError('Orphan checkpoint sidecar; preserve and investigate')
            pending.append(i)
    print(json.dumps(dict(stage='FRESH_PARALLEL_REPLAY', pending=pending,
                         workers=args.workers)), flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        jobs = {pool.submit(fresh_case, i): i for i in pending}
        for job in as_completed(jobs):
            index, body = job.result()
            write_checked(dest / f'case_{index:02d}.json', body)
            print(json.dumps(dict(stage='CASE_EXACT_CHECKPOINTED', index=index)), flush=True)
    fresh_records = [json.loads(checked(dest / f'case_{i:02d}.json')) for i in range(9)]

    class CompletedFreshCase:
        def __init__(self, index, ch):
            self.record = fresh_records[index]
            ch.rows.extend(self.record['checks'])

        def run(self, red):
            return self.record

    artifacts = {}

    def emit(name, body):
        compare_original(name, body)
        artifacts[name] = sha(body)

    original_case = frozen.Case
    try:
        frozen.Case = CompletedFreshCase
        out = frozen.calculate(emit)
        out['artifacts'] = dict(artifacts)
        emit('summary.json', frozen.ENCODE(out))
    finally:
        frozen.Case = original_case
    if initial['source_metadata'] != source_snapshot():
        raise ValueError('Source hash/size/mtime changed during replay')
    if initial['original_metadata'] != snapshot(original_paths):
        raise ValueError('Original evidence hash/size/mtime changed during replay')
    if initial['replay_metadata'] != snapshot(extra):
        raise ValueError('Replay source/addendum changed during execution')
    if out['passed'] != out['total'] or out['total'] != 336:
        raise ValueError('Original full validation not reproduced')
    receipt = dict(schema='r4c1-source-aware-parallel-exact-replay-v1',
        validation='PASS_READ_ONLY_PARALLEL_REPLAY_EXACT', passed=out['passed'], total=out['total'],
        original_payloads_exact=len(artifacts), fresh_cases=9, workers=args.workers,
        source_metadata_preserved=len(initial['source_metadata']),
        original_metadata_preserved=len(initial['original_metadata']),
        original_summary_sha256=SUMMARY_SHA, frozen_source_sha256=SOURCE_SHA,
        replay_source_sha256=sha((ROOT / SELF).read_bytes()),
        addendum_sha256=sha((ROOT / ADDENDUM).read_bytes()),
        inherited_sidecars_absent=absent, serial_cli_completed=False,
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False, review_status='DEFERRED',
        full_nonlinear_remainder=False, physical_window_admitted=False, healthy_GR_verified=False)
    write_checked(dest / 'receipt.json', frozen.ENCODE(receipt))
    print('READ_ONLY_PARALLEL_REPLAY_EXACT', flush=True)
    print(json.dumps(receipt, sort_keys=True), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
