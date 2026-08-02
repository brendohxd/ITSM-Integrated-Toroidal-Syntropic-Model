#!/usr/bin/env python3
"""DISK-001 Stage 0: spherical Plummer + Conditional AQUAL benchmarks.

Validates deep-MOND and interpolating-function radial response for a sphere
(no free-form halo). Curl is identically zero by construction in 1D radial
reduction; reported for hygiene.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from disk001_ir_law import aqual_g_magnitude, deep_mond_speed, default_conditional_ir


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--mass", type=float, default=1.0e10, help="M_sun")
    p.add_argument("--scale-kpc", type=float, default=1.0)
    p.add_argument("--n-radial", type=int, default=64)
    return p.parse_args()


def plummer_gN(r: np.ndarray, mass: float, b: float, G: float = 4.30091e-6) -> np.ndarray:
    """Newtonian |g_N| for Plummer sphere (km/s)^2/kpc if G in SPARC units."""
    return G * mass * r / (r * r + b * b) ** 1.5


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    r = np.geomspace(0.05 * args.scale_kpc, 30.0 * args.scale_kpc, args.n_radial)
    gN = plummer_gN(r, args.mass, args.scale_kpc)
    g_deep = deep_mond_speed(gN, ir)
    g_aqual = aqual_g_magnitude(gN, ir)

    # Deep-MOND analytic: g = C_obs sqrt(a0 gN)
    rel_deep = np.max(np.abs(g_deep - ir.C_obs * np.sqrt(ir.a0 * gN)) / np.maximum(g_deep, 1e-30))
    # Outer radii should approach deep-MOND (gN << a0)
    outer = gN < 0.05 * ir.a0
    if np.any(outer):
        rel_outer = np.max(
            np.abs(g_aqual[outer] - g_deep[outer]) / np.maximum(g_deep[outer], 1e-30)
        )
    else:
        rel_outer = float("nan")

    # Inner Newtonian: gN >> a0 ⇒ g ~ gN
    inner = gN > 20.0 * ir.a0
    if np.any(inner):
        rel_inner = np.max(np.abs(g_aqual[inner] - gN[inner]) / np.maximum(gN[inner], 1e-30))
    else:
        rel_inner = float("nan")

    curl_radial = 0.0  # spherical reduction
    passed = rel_deep < 1e-12 and (
        not np.isfinite(rel_outer) or rel_outer < 0.05
    ) and (not np.isfinite(rel_inner) or rel_inner < 0.05)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE0_SPHERE_BENCHMARK",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_SPHERE_PLUMMER_AQUAL"
            if passed
            else "FAIL_DISK001_SPHERE"
        ),
        "ir": ir.to_dict(),
        "model": {
            "profile": "Plummer",
            "mass_Msun": args.mass,
            "scale_kpc": args.scale_kpc,
            "n_radial": args.n_radial,
        },
        "diagnostics": {
            "deep_mond_identity_max_rel": float(rel_deep),
            "outer_aqual_vs_deep_max_rel": float(rel_outer),
            "inner_aqual_vs_newton_max_rel": float(rel_inner),
            "curl_radial_reduction": curl_radial,
        },
        "scientific_boundary": (
            "Spherical Conditional AQUAL/deep-MOND benchmark only. "
            "Not a SPARC fit, not Derived C_obs, not DISK-001 full PASS."
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "disk001_sphere_benchmark_summary.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    # sample curve
    np.savetxt(
        args.output_dir / "disk001_sphere_benchmark_curve.csv",
        np.column_stack([r, gN, g_deep, g_aqual]),
        delimiter=",",
        header="r_kpc,gN,g_deep,g_aqual",
        comments="",
    )

    print(f"IR: a0={ir.a0:.4g}  C_obs={ir.C_obs}  ({ir.label})")
    print(f"deep-MOND identity max rel err: {rel_deep:.3e}")
    print(f"outer AQUAL↔deep max rel: {rel_outer:.3e}")
    print(f"inner AQUAL↔Newton max rel: {rel_inner:.3e}")
    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
