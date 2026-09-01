#!/usr/bin/env python3
"""DISK-001 Stage 1 suite: spherical identity + 2D nonlinear AQUAL Poisson."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
SCRIPTS = [
    "disk001_sphere_nonlinear_aqual.py",
    "disk001_poisson_2d_aqual.py",
]


def main() -> None:
    results = []
    for name in SCRIPTS:
        print(f"\n=== {name} ===")
        proc = subprocess.run(
            [sys.executable, str(BASE / name)],
            cwd=str(BASE),
            capture_output=True,
            text=True,
        )
        print(proc.stdout)
        if proc.returncode != 0:
            print(proc.stderr)
            raise SystemExit(proc.returncode)
        results.append({"script": name, "returncode": 0})

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE1_NONLINEAR_AQUAL",
        "calculation_status": "PASS",
        "subgate_status": "PASS_DISK001_STAGE1_NONLINEAR_AQUAL",
        "full_gate_status": "IN_PROGRESS",
        "scripts": results,
        "scientific_boundary": (
            "Stage-1 methods package under Conditional IR: spherical AQUAL "
            "identity theorem + residual/convergence; 2D Picard FD nonlinear "
            "AQUAL Poisson with PDE residual and curl diagnostics. Not full "
            "DISK-001 PASS (no 3D/R–z, no SPARC, no Derived C_obs)."
        ),
        "next_required_calculation": [
            "Tighten residual targets and BC (free multipole / larger box)",
            "Axisymmetric R–z or 3D thin-disk solver",
            "Resolution study table for manuscript methods",
            "Then DISK-001_GATE_REPORT when criteria met",
        ],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "disk001_stage1_suite_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    print("STATUS: PASS_DISK001_STAGE1_NONLINEAR_AQUAL")


if __name__ == "__main__":
    main()
