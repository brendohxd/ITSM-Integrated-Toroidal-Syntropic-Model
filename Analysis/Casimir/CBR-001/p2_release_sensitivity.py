#!/usr/bin/env python3
"""Registered Paper-2 release sensitivity aggregator.

This script does not alter the canonical CBR-001 outputs. It checks frozen
Stage-1 and Stage-3B evidence against the 2026-10-01 sensitivity contract and
writes a deterministic JSON receipt plus SHA-256 sidecar.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]

STAGE1 = SCRIPT_DIR / "cbr001_stage1.csv"
BASELINE = SCRIPT_DIR / "stage3b_outputs" / "cbr001_stage3b_summary.json"
HEAT_KERNEL_RHO = -0.837536910696079

EXPECTED_HASHES = {
    STAGE1: "57847f382bafa562827413f19f416dbc3da004c95996413d05e0cb7fde0bb47c",
    BASELINE: "9a5e80d2f713f01b02b7ea14c2460a344bcb2fcfdf814ea6696677d465c2ce3b",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fit_limit(cutoffs: np.ndarray, values: np.ndarray, order: int) -> float:
    design = np.column_stack(
        [np.ones_like(cutoffs)]
        + [(1.0 / cutoffs) ** power for power in range(1, order + 1)]
    )
    coefficients, *_ = np.linalg.lstsq(design, values, rcond=None)
    return float(coefficients[0])


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(right), np.finfo(float).tiny)


def threshold(summary: dict[str, Any], r0: float) -> dict[str, Any]:
    for item in summary["thresholds"]:
        if abs(float(item["r0"]) - r0) < 1.0e-12:
            return item
    raise KeyError(f"No threshold row for r0={r0}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tight-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    input_hashes: dict[str, str] = {}
    for path, expected in EXPECTED_HASHES.items():
        actual = sha256(path)
        input_hashes[str(path.relative_to(REPO_ROOT))] = actual
        checks.append(
            {
                "name": f"frozen_hash:{path.name}",
                "passed": actual == expected,
                "actual": actual,
                "expected": expected,
            }
        )

    with STAGE1.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    cutoffs = np.asarray([float(row["cutoff"]) for row in rows], dtype=float)
    rho = np.asarray([float(row["rho"]) for row in rows], dtype=float)

    variants = {
        "full_order_1": fit_limit(cutoffs, rho, 1),
        "full_order_2": fit_limit(cutoffs, rho, 2),
        "full_order_3": fit_limit(cutoffs, rho, 3),
        "tail_order_1": fit_limit(cutoffs[1:], rho[1:], 1),
        "tail_order_2": fit_limit(cutoffs[1:], rho[1:], 2),
    }
    rel_errors = {
        name: relative_difference(value, HEAT_KERNEL_RHO)
        for name, value in variants.items()
    }
    static_specs = (
        ("full_order_2_vs_heat_kernel", rel_errors["full_order_2"], 2.0e-6),
        ("tail_order_2_vs_heat_kernel", rel_errors["tail_order_2"], 1.0e-6),
        ("full_order_3_vs_heat_kernel", rel_errors["full_order_3"], 1.0e-7),
        (
            "order_2_window_stability",
            relative_difference(variants["full_order_2"], variants["tail_order_2"]),
            1.0e-6,
        ),
    )
    for name, actual, maximum in static_specs:
        checks.append(
            {"name": name, "passed": actual < maximum, "actual": actual, "maximum": maximum}
        )

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    tight_path = args.tight_summary.resolve()
    tight = json.loads(tight_path.read_text(encoding="utf-8"))
    input_hashes[str(tight_path.relative_to(REPO_ROOT))] = sha256(tight_path)

    dynamic_rows: list[dict[str, Any]] = []
    for r0 in (1.1, 1.5, 3.0):
        base_row = threshold(baseline, r0)
        tight_row = threshold(tight, r0)
        epsilon_relative = relative_difference(
            float(tight_row["epsilon_threshold"]),
            float(base_row["epsilon_threshold"]),
        )
        dwell_absolute = abs(
            float(tight_row["dwell_time_within_1_percent"])
            - float(base_row["dwell_time_within_1_percent"])
        )
        row = {
            "r0": r0,
            "baseline_classification": base_row["classification"],
            "tight_classification": tight_row["classification"],
            "baseline_attractor": bool(base_row["attractor"]),
            "tight_attractor": bool(tight_row["attractor"]),
            "baseline_epsilon": float(base_row["epsilon_threshold"]),
            "tight_epsilon": float(tight_row["epsilon_threshold"]),
            "epsilon_relative_difference": epsilon_relative,
            "dwell_absolute_difference": dwell_absolute,
        }
        dynamic_rows.append(row)
        checks.extend(
            [
                {
                    "name": f"r0={r0}:classification_stable",
                    "passed": base_row["classification"] == "TRANSIENT_CROSSING"
                    and tight_row["classification"] == "TRANSIENT_CROSSING",
                },
                {
                    "name": f"r0={r0}:no_attractor",
                    "passed": not base_row["attractor"] and not tight_row["attractor"],
                },
                {
                    "name": f"r0={r0}:threshold_stable",
                    "passed": epsilon_relative < 1.0e-8,
                    "actual": epsilon_relative,
                    "maximum": 1.0e-8,
                },
                {
                    "name": f"r0={r0}:dwell_stable",
                    "passed": dwell_absolute <= 0.011,
                    "actual": dwell_absolute,
                    "maximum": 0.011,
                },
            ]
        )

    tight_validations = tight.get("validations", {})
    validation_values = [bool(value) for value in tight_validations.values()]
    checks.append(
        {
            "name": "tight_internal_validation",
            "passed": bool(validation_values) and all(validation_values),
            "details": tight_validations,
        }
    )

    passed = all(bool(check["passed"]) for check in checks)
    receipt = {
        "programme": "P2 release sensitivity",
        "contract": "Theory/Verification/P2_RELEASE_SENSITIVITY_CONTRACT_2026-10-01.md",
        "status": "PASS_CONTROL_ONLY" if passed else "FAIL",
        "validation_pass": passed,
        "physics_pass": False,
        "publication_ready": False,
        "publication_hold": (
            "Dynamic renormalized-state/backreaction inputs and deferred independent review remain open."
        ),
        "input_sha256": input_hashes,
        "static_extrapolation": {
            "heat_kernel_rho": HEAT_KERNEL_RHO,
            "fit_values": variants,
            "relative_errors": rel_errors,
        },
        "dynamic_solver": dynamic_rows,
        "checks": checks,
        "passed": sum(bool(check["passed"]) for check in checks),
        "total": len(checks),
    }

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    output.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="ascii", newline="\n"
    )

    print(json.dumps({
        "status": receipt["status"],
        "passed": receipt["passed"],
        "total": receipt["total"],
        "physics_pass": receipt["physics_pass"],
        "publication_ready": receipt["publication_ready"],
        "output": str(output),
        "output_sha256": digest,
    }, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
