"""Read-only local SPARC input audit; no fitting or source-data modification."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'Data/SPARC_data'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    files = sorted(p for p in DATA.iterdir() if p.is_file())
    pins = {p.relative_to(ROOT).as_posix(): sha(p) for p in files}
    metadata, issues = {}, []
    for p in files:
        if p.suffix != '.csv':
            continue
        with p.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            rows = list(reader)
            columns = reader.fieldnames
        names = [r.get('Name') for r in rows]
        if len(names) != len(set(names)) or not all(names):
            issues.append({'file': p.name, 'issue': 'missing_or_duplicate_metadata_names'})
        metadata[p.name] = {'columns': columns, 'rows': len(rows), 'by_name': {r['Name']: r for r in rows}}
    tables = {}
    for p in files:
        if p.suffix != '.dat':
            continue
        suffix = '_rotmod.dat'
        alternate = '_rotmod-ITSM-Cosmologist.dat'
        if p.name.endswith(suffix):
            name, kind = p.name[:-len(suffix)], 'standard'
        elif p.name.endswith(alternate):
            name, kind = p.name[:-len(alternate)], 'alternate'
        else:
            issues.append({'file': p.name, 'issue': 'unrecognized_dat_filename'})
            continue
        rows, malformed = [], []
        for number, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1):
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            try:
                row = list(map(float, line.split()))
                if len(row) != 8 or not all(math.isfinite(v) for v in row):
                    raise ValueError('expected eight finite columns')
                rows.append(row)
            except ValueError:
                malformed.append(number)
        problems = []
        if malformed:
            problems.append({'malformed_lines': malformed})
        if not rows:
            problems.append('empty_table')
        if any(r[0] <= 0 or r[2] <= 0 for r in rows):
            problems.append('nonpositive_radius_or_velocity_error')
        if any(a[0] >= b[0] for a, b in zip(rows, rows[1:])):
            problems.append('radii_not_strictly_increasing')
        if problems:
            issues.append({'file': p.name, 'issues': problems})
        tables.setdefault(name, {})[kind] = {
            'file': p.name, 'sha256': sha(p), 'rows': len(rows),
            'negative_gas_rows': sum(r[3] < 0 for r in rows),
            'errors_below_1_kms': sum(r[2] < 1 for r in rows),
            'parsed_rows_sha256': hashlib.sha256(json.dumps(rows, allow_nan=False).encode()).hexdigest(),
        }
    selected = {n: t.get('standard', t.get('alternate')) for n, t in sorted(tables.items())}
    pairs = {n: {'byte_identical': t['standard']['sha256'] == t['alternate']['sha256'],
                 'numeric_identical': t['standard']['parsed_rows_sha256'] == t['alternate']['parsed_rows_sha256']}
             for n, t in sorted(tables.items()) if len(t) == 2}
    joins = {n: {'metadata_without_radial_table': sorted(set(t['by_name']) - set(selected)),
                 'radial_table_without_metadata': sorted(set(selected) - set(t['by_name']))}
             for n, t in metadata.items()}
    return {
        'schema': 'SPARC_LOCAL_INPUT_AUDIT_V1', 'source_sha256': sha(Path(__file__)),
        'scope': 'Local inventory and structural validation only; origin-site provenance not verified.',
        'physics_pass': False, 'gate_effect': 'NONE', 'rule9': 'DEFERRED',
        'status': 'INPUT_ISSUES_FOUND' if issues else 'LOCAL_STRUCTURE_CHECKED',
        'counts': {'dat_files': sum(p.suffix == '.dat' for p in files),
                   'galaxies': len(selected), 'paired_copies': len(pairs),
                   'selected_rows': sum(t['rows'] for t in selected.values()),
                   'negative_gas_rows': sum(t['negative_gas_rows'] for t in selected.values()),
                   'errors_below_1_kms': sum(t['errors_below_1_kms'] for t in selected.values())},
        'issues': issues, 'metadata': metadata, 'joins': joins,
        'alternate_pairs': pairs, 'selected_tables': selected, 'input_sha256': pins,
        'limits': ['No uncertainty floor, clipping, exclusion, fit or acceleration coefficient is applied.',
                   'Standard filenames take precedence; differing alternates are reported, not discarded from disk.',
                   'No identification of the new 147-galaxy lensing sample or lensing covariance is supplied.',
                   'Full inference requires nuisance uncertainties/covariances and independent physical predictions.'],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify', type=Path)
    args = parser.parse_args()
    if bool(args.output) == bool(args.verify):
        parser.error('choose exactly one of --output (new file) or --verify (read-only replay)')
    result = audit()
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as stream:
            stream.write(payload)
    else:
        if args.verify.read_bytes() != payload:
            raise SystemExit('REPLAY_MISMATCH')
    print(json.dumps({'status': result['status'], 'counts': result['counts'],
                      'issues': result['issues'], 'joins': result['joins'],
                      'different_alternates': [n for n, p in result['alternate_pairs'].items() if not p['numeric_identical']],
                      'replay': 'EXACT' if args.verify else 'NOT_YET_RUN',
                      'physics_pass': False}, indent=2))
