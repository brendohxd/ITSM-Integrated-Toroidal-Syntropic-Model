#!/usr/bin/env python3
"""DISK-001 Stage 0: run sphere + disk midplane + curl residual suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
SCRIPTS = [
    "disk001_sphere_benchmark.py",
    "disk001_disk_midplane.py",
    "disk001_curl_residual.py",
]


def main() -> None:
    results = []
    for name in SCRIPTS:
        path = BASE / name
        print(f"\n=== {name} ===")
        proc = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(BASE),
            capture_output=True,
            text=True,
        )
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr)
            raise SystemExit(proc.returncode)
        results.append({"script": name, "returncode": proc.returncode})

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE0_SCAFFOLD_SUITE",
        "calculation_status": "PASS",
        "subgate_status": "PASS_DISK001_STAGE0_SCAFFOLD",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "scripts": results,
        "ir_policy": "Conditional AQUAL-class with declared C_obs~1, phenomenological a0",
        "scientific_boundary": (
            "Stage-0 tooling only under Conditional IR. No SPARC validation, "
            "no Derived C_obs, no morphology-independent coupling claim, "
            "no DISK-001 full-gate PASS."
        ),
        "next_required_calculation": [
            "Nonlinear AQUAL/Poisson (or equivalent) 2D/3D solver for potential structure",
            "Resolution/box convergence study",
            "Optional SPARC single-galaxy *diagnostic* curves under declared inputs (not STAT-001)",
            "DISK-001_GATE_REPORT.md only after sphere+disk+curl+convergence PASS criteria",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "disk001_stage0_suite_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    print("STATUS: PASS_DISK001_STAGE0_SCAFFOLD")


if __name__ == "__main__":
    main()
