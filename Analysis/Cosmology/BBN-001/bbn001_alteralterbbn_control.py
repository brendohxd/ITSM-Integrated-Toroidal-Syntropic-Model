#!/usr/bin/env python3
"""Run an isolated AlterAlterBBN network as a bounded BBN control.

This adapter is deliberately not an ITSM cosmology implementation.  It
validates the six-column external cosmology contract, runs a caller-supplied
AlterAlterBBN executable, records hashes and parses the final abundance file.
The result remains ``CONTROL_ONLY`` unless the upstream ITSM background,
transfer current, effective gravity and perturbation contracts are separately
derived and reviewed.

The adapter does not vendor AlterAlterBBN or assume that its ``H`` column is
used.  For the pinned source audit, the network evolves using ``dTdt``,
``Tnu`` and the baryon-density column; the ``H`` value is retained in the
input contract but is not independently consumed by ``bbn.c``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = Path(__file__).parent / "outputs" / "bbn001_alteralterbbn_control_summary.json"
COSMO_COLUMNS = (
    ("t", "s"),
    ("T", "MeV"),
    ("dTdt", "MeV^2"),
    ("Tnu", "MeV"),
    ("H", "MeV"),
    ("nb_etaf", "MeV^3"),
)
ABUNDANCE_NAMES = ("n", "p", "H2", "H3", "He3", "He4", "Li6", "Li7", "Be7")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fail(message: str) -> None:
    raise ValueError(message)


def _source_commit(source_root: Path | None) -> str:
    if source_root is None:
        return "NOT_SUPPLIED"
    if not source_root.is_dir():
        _fail(f"source root does not exist: {source_root}")
    try:
        result = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        _fail(f"could not resolve source commit for {source_root}: {exc}")
    commit = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        _fail("source commit is not a 40-character Git SHA-1")
    return commit


def _load_eta(param_path: Path) -> float:
    if not param_path.is_file():
        _fail(f"missing parameter file: {param_path}")
    text = param_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^\s*eta\s*=\s*([0-9.eE+-]+)\s*$", text)
    if match is None:
        _fail("param_file.dat must contain one plain eta=<value> line")
    eta = float(match.group(1))
    if not math.isfinite(eta) or eta <= 0.0:
        _fail("eta must be finite and positive")
    return eta


def _load_cosmology(cosmo_path: Path) -> list[list[float]]:
    if not cosmo_path.is_file():
        _fail(f"missing cosmology file: {cosmo_path}")
    rows: list[list[float]] = []
    for line_number, raw_line in enumerate(cosmo_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        fields = raw_line.split()
        if len(fields) != len(COSMO_COLUMNS):
            _fail(f"cosmo_file.dat line {line_number} has {len(fields)} columns; expected 6")
        try:
            row = [float(field) for field in fields]
        except ValueError as exc:
            _fail(f"cosmo_file.dat line {line_number} is not numeric: {exc}")
        if not all(math.isfinite(value) for value in row):
            _fail(f"cosmo_file.dat line {line_number} contains a non-finite value")
        rows.append(row)

    if len(rows) < 2:
        _fail("cosmo_file.dat must contain at least two data rows")

    def strictly_increasing(index: int) -> bool:
        return all(rows[i + 1][index] > rows[i][index] for i in range(len(rows) - 1))

    def strictly_decreasing(index: int) -> bool:
        return all(rows[i + 1][index] < rows[i][index] for i in range(len(rows) - 1))

    if not strictly_increasing(0):
        _fail("cosmo_file.dat time column must be strictly increasing")
    if not strictly_decreasing(1):
        _fail("cosmo_file.dat photon temperature must be strictly decreasing")
    if any(row[2] >= 0.0 for row in rows):
        _fail("cosmo_file.dat dTdt column must be negative")
    if any(row[3] <= 0.0 or row[4] <= 0.0 or row[5] <= 0.0 for row in rows):
        _fail("cosmo_file.dat Tnu, H and nb_etaf columns must be positive")
    return rows


def _load_abundances(path: Path) -> dict[str, dict[str, float]]:
    if not path.is_file():
        _fail(f"network did not produce abundance_file.dat: {path}")
    rows: list[list[float]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        fields = raw_line.split()
        if len(fields) != 3:
            _fail(f"abundance_file.dat line {line_number} has {len(fields)} columns; expected 3")
        try:
            row = [float(field) for field in fields]
        except ValueError as exc:
            _fail(f"abundance_file.dat line {line_number} is not numeric: {exc}")
        if not all(math.isfinite(value) for value in row):
            _fail(f"abundance_file.dat line {line_number} contains a non-finite value")
        rows.append(row)
    if len(rows) != len(ABUNDANCE_NAMES):
        _fail(f"abundance_file.dat has {len(rows)} rows; expected {len(ABUNDANCE_NAMES)}")
    return {
        name: {column: value for column, value in zip(("mean", "high", "low"), row)}
        for name, row in zip(ABUNDANCE_NAMES, rows)
    }


def run_control(
    executable: Path,
    input_dir: Path,
    output_path: Path,
    label: str,
    source_root: Path | None,
) -> dict:
    executable = executable.resolve()
    input_dir = input_dir.resolve()
    if not executable.is_file():
        _fail(f"executable does not exist: {executable}")
    if not input_dir.is_dir():
        _fail(f"input directory does not exist: {input_dir}")

    param_path = input_dir / "param_file.dat"
    cosmo_path = input_dir / "cosmo_file.dat"
    abundance_path = input_dir / "abundance_file.dat"
    eta = _load_eta(param_path)
    rows = _load_cosmology(cosmo_path)
    source_commit = _source_commit(source_root.resolve() if source_root else None)

    completed = subprocess.run(
        [str(executable), str(input_dir)],
        cwd=executable.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        _fail(
            "AlterAlterBBN returned nonzero "
            f"({completed.returncode}); stdout={completed.stdout[-1000:]!r}; "
            f"stderr={completed.stderr[-1000:]!r}"
        )

    abundances = _load_abundances(abundance_path)
    p = abundances["p"]["mean"]
    h2 = abundances["H2"]["mean"]
    he4 = abundances["He4"]["mean"]
    if p <= 0.0 or h2 <= 0.0 or he4 <= 0.0:
        _fail("network control requires positive p, H2 and He4 mean abundances")

    result = {
        "record_type": "ALTERALTERBBN_EXTERNAL_NETWORK_CONTROL",
        "gate": "BBN-001",
        "label": label,
        "status": "CONTROL_ONLY",
        "physics_pass": False,
        "gate_effect": "NONE",
        "publication_status": "NOT_A_PHYSICS_CLAIM",
        "network": {
            "name": "AlterAlterBBN",
            "reported_version": "v2.0",
            "license": "GPL-3.0",
            "source_commit": source_commit,
            "executable_sha256": _sha256(executable),
            "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
        },
        "input": {
            "param_file": "param_file.dat",
            "cosmo_file": "cosmo_file.dat",
            "abundance_file": "abundance_file.dat",
            "eta": eta,
            "cosmo_rows": len(rows),
            "columns": [{"name": name, "unit": unit} for name, unit in COSMO_COLUMNS],
            "param_file_sha256": _sha256(param_path),
            "cosmo_file_sha256": _sha256(cosmo_path),
        },
        "outputs": {
            "abundances": abundances,
            "Y_He_mass_fraction": 4.0 * he4,
            "D_over_H": h2 / p,
            "conversion_contract": {
                "Y_He_mass_fraction": "4 * n_He4 / n_b",
                "D_over_H": "n_H2 / n_H",
            },
        },
        "network_input_audit": {
            "H_column": "retained_in_input_contract",
            "H_column_consumed_by_pinned_source": (
                "NOT_USED_BY_PINNED_SOURCE" if source_commit != "NOT_SUPPLIED" else "UNVERIFIED"
            ),
            "basis": (
                "For the supplied source audit, bbn.c calls dTdt, neutrino_temperature "
                "and nb_eta_final_ratio; it does not call an H interpolation accessor."
                if source_commit != "NOT_SUPPLIED"
                else "A pinned source root was not supplied, so H-column usage is not verified."
            ),
        },
        "review_state": {
            "independent_reproduction": "NOT_COMPLETED",
            "three_way_consensus": "NOT_MET",
            "external_BBN_likelihood": "NOT_IMPLEMENTED",
            "ITSM_mapping": "NOT_DERIVED",
        },
        "limitations": [
            "The input history is an external standard/control history, not an ITSM action-derived background.",
            "No early-plenum density, Q^mu, G_eff(z), perturbation matching or Planck/DESI likelihood is supplied.",
            "The network result is a reproducibility and sensitivity control only; it is not an ITSM prediction.",
        ],
    }
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    digest = _sha256(output_path)
    output_path.with_name(output_path.name + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="utf-8"
    )
    return result | {"summary_sha256": digest}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", required=True, type=Path)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument("--label", default="external_network_control")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args(argv)
    try:
        result = run_control(
            executable=args.executable,
            input_dir=args.input_dir,
            output_path=args.output,
            label=args.label,
            source_root=args.source_root,
        )
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"BBN-001 external network control failed closed: {exc}", file=sys.stderr)
        return 2
    print("BBN-001 external network control complete")
    print(f"Status: {result['status']}")
    print(f"Label: {result['label']}")
    print(f"Y_He: {result['outputs']['Y_He_mass_fraction']:.16g}")
    print(f"D/H: {result['outputs']['D_over_H']:.16g}")
    print(f"SHA-256: {result['summary_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
