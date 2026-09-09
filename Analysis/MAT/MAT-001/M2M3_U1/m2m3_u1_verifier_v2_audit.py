#!/usr/bin/env python3
"""Isolated deterministic and mutation audit for the M2/M3-U1 v2 verifier."""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mpmath
import sympy


DECLARED_MUTATIONS = (
    "MUT_01_KINETIC_MIXING",
    "MUT_02_DELETE_SQRT2_SOURCE",
    "MUT_03_DIMENSION_R_POWER",
    "MUT_04_REVERSE_GRADIENT_SIGN",
    "MUT_05_SPHERE_NUMERATOR",
    "MUT_06_SIDECAR_BYTE_MUTATION",
    "MUT_07_EXTRA_RUN2_FILE",
    "MUT_08_MARKDOWN_FORMULA",
    "MUT_09_REVERSE_K4_SIGN",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_tree(root: Path) -> dict[str, dict[str, Any]]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): {
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def compare_trees(
    left: dict[str, dict[str, Any]], right: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    left_paths = set(left)
    right_paths = set(right)
    common = left_paths & right_paths
    mismatched = sorted(path for path in common if left[path] != right[path])
    return {
        "left_only": sorted(left_paths - right_paths),
        "right_only": sorted(right_paths - left_paths),
        "content_mismatches": mismatched,
        "identical": not (left_paths ^ right_paths) and not mismatched,
    }


def normalized_command(root: Path, script_relpath: str, arguments: list[str]) -> str:
    args = " ".join(arguments)
    suffix = f" {args}" if args else ""
    return f"<ITSM_PYTHON> <TEMP_ROOT>/{root.name}/{script_relpath}{suffix}"


def execute(
    python_executable: Path,
    root: Path,
    script_relpath: str,
    arguments: list[str] | None = None,
) -> dict[str, Any]:
    arguments = arguments or []
    script = root / script_relpath
    started = datetime.now(timezone.utc)
    process = subprocess.run(
        [str(python_executable), str(script), *arguments],
        cwd=script.parent,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    ended = datetime.now(timezone.utc)
    return {
        "command": normalized_command(root, script_relpath, arguments),
        "working_directory": (
            f"<TEMP_ROOT>/{root.name}/Analysis/MAT/MAT-001/M2M3_U1"
        ),
        "started_utc": started.isoformat(),
        "ended_utc": ended.isoformat(),
        "duration_seconds": (ended - started).total_seconds(),
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def prepare_tree(source_root: Path, destination: Path, relpaths: tuple[str, ...]) -> None:
    for relpath in relpaths:
        source = source_root / relpath
        target = destination / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> dict[str, Any]:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[4]
    python_executable = Path(sys.executable).resolve()
    expected_python = Path(
        r"C:\Users\brend\anaconda3\envs\itsm_env\python.exe"
    ).resolve()
    if python_executable != expected_python:
        raise RuntimeError(
            f"wrong interpreter: {python_executable}; expected {expected_python}"
        )

    baseline_script = (
        "Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks.py"
    )
    candidate_script = (
        "Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks_v2.py"
    )
    output_relpath = "Analysis/MAT/MAT-001/M2M3_U1/outputs"
    source_relpaths = (
        "GEMINI.md",
        "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md",
        "active_research.md",
        "Theory/Core/Reasoning_Mode_Plans/README.md",
        "Theory/Core/Reasoning_Mode_Plans/03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md",
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/HANDOFF_SHA256.md",
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/ANTIGRAVITY_HANDOFF_A-B4_VERIFIER_REPAIR.md",
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/ANTIGRAVITY_HANDOFF_A-B4_VERIFIER_REPAIR.md.sha256",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_HIGH_HANDOFF_2026-09-05.md",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md.sha256",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md.sha256",
        "Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md",
        "Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md.sha256",
        baseline_script,
        f"{baseline_script}.sha256",
        candidate_script,
        f"{output_relpath}/m2m3_u1_fixed_background_summary.json",
        f"{output_relpath}/m2m3_u1_fixed_background_summary.sha256",
    )
    missing = [relpath for relpath in source_relpaths if not (repo_root / relpath).is_file()]
    if missing:
        raise FileNotFoundError(f"mandatory inputs missing: {missing}")

    source_inventory = {
        relpath: {
            "size": (repo_root / relpath).stat().st_size,
            "sha256": sha256_file(repo_root / relpath),
        }
        for relpath in source_relpaths
    }

    with tempfile.TemporaryDirectory(prefix="itsm_ab4r_") as temp_name:
        temp_root = Path(temp_name)

        def new_tree(name: str) -> Path:
            root = temp_root / name
            prepare_tree(repo_root, root, source_relpaths)
            return root

        baseline_roots = [new_tree("baseline_run1"), new_tree("baseline_run2")]
        baseline_records = [
            execute(python_executable, root, baseline_script) for root in baseline_roots
        ]
        baseline_trees = [file_tree(root / output_relpath) for root in baseline_roots]
        baseline_comparison = compare_trees(*baseline_trees)

        candidate_roots = [new_tree("candidate_run1"), new_tree("candidate_run2")]
        candidate_records = [
            execute(python_executable, root, candidate_script) for root in candidate_roots
        ]
        candidate_trees = [file_tree(root / output_relpath) for root in candidate_roots]
        candidate_comparison = compare_trees(*candidate_trees)

        source_copy_equality: dict[str, bool] = {}
        for relpath, source_data in source_inventory.items():
            source_copy_equality[relpath] = all(
                sha256_file(root / relpath) == source_data["sha256"]
                for root in baseline_roots + candidate_roots
            )

        mutation_results: dict[str, dict[str, Any]] = {}
        cli_mutations = (
            "MUT_01_KINETIC_MIXING",
            "MUT_02_DELETE_SQRT2_SOURCE",
            "MUT_03_DIMENSION_R_POWER",
            "MUT_04_REVERSE_GRADIENT_SIGN",
            "MUT_05_SPHERE_NUMERATOR",
            "MUT_09_REVERSE_K4_SIGN",
        )
        for mutation in cli_mutations:
            root = new_tree(mutation.lower())
            record = execute(
                python_executable, root, candidate_script, ["--mutation", mutation]
            )
            mutation_results[mutation] = {
                "detected": record["exit_code"] != 0,
                "execution": record,
            }

        sidecar_root = new_tree("mut_06_sidecar_byte_mutation")
        corrupted = sidecar_root / output_relpath / "m2m3_u1_fixed_background_summary.json"
        data = bytearray(corrupted.read_bytes())
        data[0] ^= 1
        corrupted.write_bytes(data)
        sidecar_record = execute(python_executable, sidecar_root, candidate_script)
        mutation_results["MUT_06_SIDECAR_BYTE_MUTATION"] = {
            "detected": sidecar_record["exit_code"] != 0,
            "mutated_target": (
                "Analysis/MAT/MAT-001/M2M3_U1/outputs/"
                "m2m3_u1_fixed_background_summary.json"
            ),
            "execution": sidecar_record,
        }

        markdown_root = new_tree("mut_08_markdown_formula")
        reduction_relpath = (
            "Theory/Gates/MAT-001/M2M3_U1/"
            "M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md"
        )
        reduction_path = markdown_root / reduction_relpath
        original_text = reduction_path.read_text(encoding="utf-8")
        altered_text = original_text.replace(
            r"=2\lambda_4v^2,\\", r"=3\lambda_4v^2,\\", 1
        )
        replacement_count = int(altered_text != original_text)
        reduction_path.write_text(altered_text, encoding="utf-8", newline="\n")
        markdown_record = execute(python_executable, markdown_root, candidate_script)
        mutation_results["MUT_08_MARKDOWN_FORMULA"] = {
            "detected": replacement_count == 1 and markdown_record["exit_code"] != 0,
            "replacement_count": replacement_count,
            "execution": markdown_record,
        }

        # Required real asymmetric output-tree mutation.
        extra_path = candidate_roots[1] / output_relpath / "extra_unsolicited_artifact.txt"
        extra_path.write_text("mutation-07\n", encoding="ascii", newline="\n")
        candidate_run2_mutated_tree = file_tree(candidate_roots[1] / output_relpath)
        extra_file_comparison = compare_trees(
            candidate_trees[0], candidate_run2_mutated_tree
        )
        mutation_results["MUT_07_EXTRA_RUN2_FILE"] = {
            "detected": "extra_unsolicited_artifact.txt"
            in extra_file_comparison["right_only"],
            "tree_comparison": extra_file_comparison,
        }

        all_mutations_detected = all(
            mutation_results[name]["detected"] for name in DECLARED_MUTATIONS
        )
        baseline_success = (
            all(record["exit_code"] == 0 for record in baseline_records)
            and baseline_comparison["identical"]
        )
        candidate_success = (
            all(record["exit_code"] == 0 for record in candidate_records)
            and candidate_comparison["identical"]
        )

        candidate_summary_hashes = [
            sha256_file(
                root / output_relpath / "m2m3_u1_fixed_background_summary_v2.json"
            )
            for root in candidate_roots
        ]
        baseline_summary_hashes = [
            sha256_file(root / output_relpath / "m2m3_u1_fixed_background_summary.json")
            for root in baseline_roots
        ]

        classification = (
            "VERIFIER_V2_CANDIDATE_COMPLETE_ALL_PREDECLARED_MUTATIONS_DETECTED"
            if baseline_success and candidate_success and all_mutations_detected
            else "VERIFIER_REPAIR_INCOMPLETE"
        )
        manifest: dict[str, Any] = {
            "schema_version": "1.0",
            "package": "A-B4R_CODEX_PARENT_REPAIR_AND_AUDIT",
            "mutation_declaration_before_execution": list(DECLARED_MUTATIONS),
            "environment": {
                "platform": platform.platform(),
                "python_executable": str(python_executable),
                "python_version": sys.version,
                "sympy_version": sympy.__version__,
                "mpmath_version": mpmath.__version__,
            },
            "temporary_execution": {
                "root": "OS-managed unique directory; normalized as <TEMP_ROOT>",
                "retained_after_audit": False,
            },
            "source_inventory": source_inventory,
            "source_copy_byte_equality": source_copy_equality,
            "baseline_runs": baseline_records,
            "baseline_output_trees": baseline_trees,
            "baseline_tree_comparison": baseline_comparison,
            "baseline_summary_sha256": baseline_summary_hashes,
            "candidate_script_sha256": sha256_file(repo_root / candidate_script),
            "candidate_runs": candidate_records,
            "candidate_output_trees": candidate_trees,
            "candidate_tree_comparison": candidate_comparison,
            "candidate_summary_sha256": candidate_summary_hashes,
            "mutation_results": mutation_results,
            "all_mutations_detected": all_mutations_detected,
            "primary_classification": classification,
            "gate_boundary": {
                "gate_effect": "NONE",
                "MAT-001": "BLOCKED",
                "UVIR-003": "IN_PROGRESS",
                "K_Q": "NOT_DERIVED",
                "V": "NOT_COMPUTED",
            },
            "code_to_claim_limits": [
                "The v2 result verifies fixed-background scalar identities only.",
                "The independent matrix comparison verifies eigenfrequencies, not a metric-reduced physical residue.",
                "No force normalization, K_Q, V, screening, PPN, lensing or a_0 is derived.",
                "A calculation pass is not a physics-gate pass.",
            ],
        }

    output_dir = repo_root / output_relpath
    output_path = output_dir / "m2m3_u1_verifier_v2_audit_manifest.json"
    serialized = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    output_path.write_text(serialized, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    output_path.with_suffix(".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(manifest["primary_classification"])
    print(f"baseline_success={baseline_success}")
    print(f"candidate_success={candidate_success}")
    print(f"mutations={len(DECLARED_MUTATIONS)} detected={sum(result['detected'] for result in mutation_results.values())}")
    print(f"audit_manifest_sha256={digest}")
    print("MAT-001=BLOCKED K_Q=NOT_DERIVED V=NOT_COMPUTED gate_effect=NONE")
    return manifest


if __name__ == "__main__":
    audit = main()
    if audit["primary_classification"] != (
        "VERIFIER_V2_CANDIDATE_COMPLETE_ALL_PREDECLARED_MUTATIONS_DETECTED"
    ):
        raise SystemExit(1)
