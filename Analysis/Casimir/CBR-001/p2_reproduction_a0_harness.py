#!/usr/bin/env python3
"""Isolated two-run reproduction harness for the P2/CBR-001 baseline.

This is an execution and provenance control, not a physics-gate test.  It
copies the four frozen science scripts into two clean OS-temporary run roots,
uses explicit paths between every stage, and compares fresh and tracked
artifacts without overwriting the repository.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import csv
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any


EXPECTED_PYTHON = Path(r"C:\Users\brend\anaconda3\envs\itsm_env\python.exe")
SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIR.parents[2]
SCIENCE_SCRIPTS = (
    "casimir_t3_lattice.py",
    "cbr001_stage2_standalone.py",
    "cbr001_stage3_backreaction.py",
    "cbr001_stage3b_ratio_test.py",
)
EXPECTED_OUTPUTS = (
    Path("cbr001_stage1.csv"),
    Path("stage2_outputs/cbr001_stage2_scan.csv"),
    Path("stage2_outputs/cbr001_stage2_stress.png"),
    Path("stage2_outputs/cbr001_stage2_anisotropy.png"),
    Path("stage3_outputs/cbr001_stage3_runs.csv"),
    Path("stage3_outputs/cbr001_stage3_summary.json"),
    Path("stage3_outputs/cbr001_stage3_shape.png"),
    Path("stage3_outputs/cbr001_stage3_shear.png"),
    Path("stage3_outputs/cbr001_stage3_hubble_ratio.png"),
    Path("stage3b_outputs/cbr001_stage3b_runs.csv"),
    Path("stage3b_outputs/cbr001_stage3b_thresholds.csv"),
    Path("stage3b_outputs/cbr001_stage3b_summary.json"),
    Path("stage3b_outputs/cbr001_stage3b_ratio.png"),
    Path("stage3b_outputs/cbr001_stage3b_phase_space.png"),
    Path("stage3b_outputs/cbr001_stage3b_threshold_epsilon.png"),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def replace_root(value: Any, root: Path) -> Any:
    """Replace one known absolute root in JSON strings; change no numbers."""

    if isinstance(value, dict):
        return {key: replace_root(item, root) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_root(item, root) for item in value]
    if isinstance(value, str):
        candidates = {
            str(root),
            root.as_posix(),
            str(root.resolve()),
            root.resolve().as_posix(),
        }
        normalized = value
        for candidate in sorted(candidates, key=len, reverse=True):
            normalized = normalized.replace(candidate, "<CBR_ROOT>")
        return normalized
    return value


def scientific_payload_hash(path: Path, root: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        normalized = replace_root(value, root)
        return hashlib.sha256(canonical_json_bytes(normalized)).hexdigest()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
        return hashlib.sha256(canonical_json_bytes(rows)).hexdigest()
    return sha256_file(path)


def scientific_payload_method(path: Path) -> str:
    if path.suffix.lower() == ".json":
        return "canonical_json_with_known_root_replaced"
    if path.suffix.lower() == ".csv":
        return "canonical_csv_cells_newline_independent"
    return "raw_bytes"


def output_inventory(root: Path) -> dict[str, dict[str, Any]]:
    inventory: dict[str, dict[str, Any]] = {}
    for relative in EXPECTED_OUTPUTS:
        path = root / relative
        if path.is_file():
            inventory[relative.as_posix()] = {
                "size": path.stat().st_size,
                "sha256": sha256_file(path),
                "scientific_payload_sha256": scientific_payload_hash(path, root),
                "scientific_payload_method": scientific_payload_method(path),
            }
    return inventory


def compare_inventories(
    left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]], field: str
) -> dict[str, Any]:
    left_keys = set(left)
    right_keys = set(right)
    shared = sorted(left_keys & right_keys)
    mismatches = [key for key in shared if left[key][field] != right[key][field]]
    return {
        "field": field,
        "identical": not mismatches and left_keys == right_keys,
        "left_only": sorted(left_keys - right_keys),
        "right_only": sorted(right_keys - left_keys),
        "mismatches": mismatches,
    }


def command_record(
    command: list[str], cwd: Path, log_dir: Path, label: str, environment: dict[str, str]
) -> dict[str, Any]:
    started = time.time()
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    ended = time.time()
    stdout_path = log_dir / f"{label}.stdout.txt"
    stderr_path = log_dir / f"{label}.stderr.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    return {
        "label": label,
        "command": command,
        "cwd": str(cwd),
        "started_unix": started,
        "ended_unix": ended,
        "duration_seconds": ended - started,
        "exit_code": completed.returncode,
        "stdout_path": str(stdout_path),
        "stdout_sha256": sha256_file(stdout_path),
        "stdout_tail": completed.stdout.splitlines()[-12:],
        "stderr_path": str(stderr_path),
        "stderr_sha256": sha256_file(stderr_path),
        "stderr_tail": completed.stderr.splitlines()[-12:],
    }


def run_once(run_root: Path, source_hashes: dict[str, str]) -> dict[str, Any]:
    source_dir = run_root / "source"
    log_dir = run_root / "logs"
    source_dir.mkdir(parents=True)
    log_dir.mkdir(parents=True)
    copied_hashes: dict[str, str] = {}
    for name in SCIENCE_SCRIPTS:
        source = SCRIPT_DIR / name
        target = source_dir / name
        shutil.copy2(source, target)
        copied_hashes[name] = sha256_file(target)

    copy_match = copied_hashes == source_hashes
    python = str(EXPECTED_PYTHON)
    stage2_dir = run_root / "stage2_outputs"
    stage3_dir = run_root / "stage3_outputs"
    stage3b_dir = run_root / "stage3b_outputs"
    environment = os.environ.copy()
    environment.update(
        {
            "MPLBACKEND": "Agg",
            "MPLCONFIGDIR": str(run_root / "mplconfig"),
            "PYTHONHASHSEED": "0",
        }
    )
    commands = (
        (
            "stage1",
            [python, str(source_dir / SCIENCE_SCRIPTS[0]), "--csv", str(run_root / "cbr001_stage1.csv")],
        ),
        (
            "stage2",
            [python, str(source_dir / SCIENCE_SCRIPTS[1]), "--output-dir", str(stage2_dir)],
        ),
        (
            "stage3a",
            [
                python,
                str(source_dir / SCIENCE_SCRIPTS[2]),
                "--stage2-csv",
                str(stage2_dir / "cbr001_stage2_scan.csv"),
                "--output-dir",
                str(stage3_dir),
            ],
        ),
        (
            "stage3b",
            [
                python,
                str(source_dir / SCIENCE_SCRIPTS[3]),
                "--stage2-csv",
                str(stage2_dir / "cbr001_stage2_scan.csv"),
                "--output-dir",
                str(stage3b_dir),
            ],
        ),
    )
    records: list[dict[str, Any]] = []
    if copy_match:
        for label, command in commands:
            record = command_record(command, source_dir, log_dir, label, environment)
            records.append(record)
            if record["exit_code"] != 0:
                break
    inventory = output_inventory(run_root)
    return {
        "run_root": str(run_root),
        "source_copy_sha256": copied_hashes,
        "source_copy_byte_equal": copy_match,
        "commands": records,
        "all_commands_succeeded": len(records) == len(commands)
        and all(item["exit_code"] == 0 for item in records),
        "expected_output_count": len(EXPECTED_OUTPUTS),
        "actual_output_count": len(inventory),
        "missing_outputs": sorted(
            relative.as_posix()
            for relative in EXPECTED_OUTPUTS
            if relative.as_posix() not in inventory
        ),
        "output_inventory": inventory,
    }


def tracked_comparison(run_inventory: dict[str, dict[str, Any]]) -> dict[str, Any]:
    tracked = output_inventory(SCRIPT_DIR)
    return {
        "tracked_output_count": len(tracked),
        "raw_bytes": compare_inventories(run_inventory, tracked, "sha256"),
        "normalized_scientific_payload": compare_inventories(
            run_inventory, tracked, "scientific_payload_sha256"
        ),
        "tracked_inventory": tracked,
    }


def package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in ("numpy", "scipy", "matplotlib"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "NOT_INSTALLED"
    return versions


def main() -> int:
    actual_python = Path(sys.executable).resolve()
    expected_python = EXPECTED_PYTHON.resolve()
    if os.path.normcase(str(actual_python)) != os.path.normcase(str(expected_python)):
        raise RuntimeError(
            f"wrong interpreter: {actual_python}; expected {expected_python}"
        )

    source_hashes = {
        name: sha256_file(SCRIPT_DIR / name) for name in SCIENCE_SCRIPTS
    }
    temporary_root = Path(tempfile.mkdtemp(prefix="itsm_p2_a0_507d8b_"))
    resolved_repository = REPOSITORY_ROOT.resolve()
    resolved_temporary = temporary_root.resolve()
    if resolved_temporary == resolved_repository or resolved_repository in resolved_temporary.parents:
        raise RuntimeError(f"temporary root is inside repository: {resolved_temporary}")

    run1 = run_once(temporary_root / "run1", source_hashes)
    run2 = run_once(temporary_root / "run2", source_hashes)
    raw_comparison = compare_inventories(
        run1["output_inventory"], run2["output_inventory"], "sha256"
    )
    scientific_comparison = compare_inventories(
        run1["output_inventory"],
        run2["output_inventory"],
        "scientific_payload_sha256",
    )
    tracked = tracked_comparison(run1["output_inventory"])
    success = all(
        (
            run1["source_copy_byte_equal"],
            run2["source_copy_byte_equal"],
            run1["all_commands_succeeded"],
            run2["all_commands_succeeded"],
            not run1["missing_outputs"],
            not run2["missing_outputs"],
            scientific_comparison["identical"],
        )
    )
    tracked_scientific_match = tracked["normalized_scientific_payload"]["identical"]
    manifest = {
        "schema_version": "p2-a0-reproduction-v1",
        "primary_classification": (
            "LOCAL_BASELINE_REPRODUCTION_SCIENTIFICALLY_MATCHES_TRACKED_UNADJUDICATED"
            if success and tracked_scientific_match
            else "LOCAL_CODE_REPRODUCES_BUT_TRACKED_SCIENTIFIC_PAYLOAD_DIVERGES"
            if success
            else "LOCAL_BASELINE_REPRODUCTION_FAILED"
        ),
        "scope": "mechanical execution and provenance only",
        "environment": {
            "python_executable": str(actual_python),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "packages": package_versions(),
        },
        "repository_root": str(resolved_repository),
        "temporary_root": str(resolved_temporary),
        "harness_sha256": sha256_file(Path(__file__).resolve()),
        "science_source_sha256": source_hashes,
        "run1": run1,
        "run2": run2,
        "run1_run2_raw_bytes": raw_comparison,
        "run1_run2_normalized_scientific_payload": scientific_comparison,
        "fresh_run1_vs_tracked": tracked,
        "documentation_hazard": {
            "present": True,
            "statement": (
                "Stage-2 defaults write to the current directory, whereas Stage-3A/3B "
                "defaults read stage2_outputs/cbr001_stage2_scan.csv. This harness uses "
                "explicit paths so a fresh Stage-2 file cannot be bypassed silently."
            ),
        },
        "gate_boundary": {
            "TOP-001 / CBR-002": "SCOPED_NEGATIVE_FREE_DILUTION",
            "MAT-001": "BLOCKED",
            "UVIR-003": "IN_PROGRESS",
            "K_Q": "NOT_DERIVED",
            "V": "NOT_COMPUTED",
            "gate_effect": "NONE",
        },
        "explicit_non_claims": [
            "No physics gate is passed.",
            "No independent analytic validation is supplied.",
            "No publication or release decision is made.",
            "Raw-byte inequality caused only by line endings or path-bearing JSON is not scientific inequality.",
        ],
    }
    manifest_path = temporary_root / "p2_a0_reproduction_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_hash = sha256_file(manifest_path)
    print(manifest["primary_classification"])
    print(f"temporary_root={resolved_temporary}")
    print(f"run1_success={run1['all_commands_succeeded']}")
    print(f"run2_success={run2['all_commands_succeeded']}")
    print(f"raw_output_trees_identical={raw_comparison['identical']}")
    print(f"normalized_scientific_payload_identical={scientific_comparison['identical']}")
    print(
        "fresh_vs_tracked_normalized_identical="
        f"{tracked['normalized_scientific_payload']['identical']}"
    )
    print(f"manifest={manifest_path}")
    print(f"manifest_sha256={manifest_hash}")
    print("gate_effect=NONE")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
