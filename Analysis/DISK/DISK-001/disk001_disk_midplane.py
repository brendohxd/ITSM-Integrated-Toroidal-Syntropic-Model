#!/usr/bin/env python3
"""DISK-001 Stage 0: razor-thin exponential disk midplane Newtonian + AQUAL g.

Baryonic surface density Σ(R)=Σ0 exp(-R/Rd). Newtonian midplane g_N uses the
standard thin-disk Bessel combination (Toomre). AQUAL applies the Conditional
interpolating map along the radial direction only (1D midplane reduction).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.special import iv, kn

from disk001_ir_law import aqual_g_magnitude, default_conditional_ir

G_SPARC = 4.30091e-6  # kpc (km/s)^2 / M_sun


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--sigma0", type=float, default=300.0, help="M_sun/pc^2")
    p.add_argument("--Rd", type=float, default=3.0, help="kpc")
    p.add_argument("--n-radial", type=int, default=48)
    return p.parse_args()


def exponential_disk_gN_midplane(R: np.ndarray, sigma0_msun_pc2: float, Rd: float) -> np.ndarray:
    """|g_N| radial (inward) for thin exp disk; SPARC units (km/s)^2/kpc.

    Σ0 input in M_sun/pc^2 → convert to M_sun/kpc^2 (*1e6).
    V_c^2 = 4π G Σ0 Rd y^2 [I0(y)K0(y)-I1(y)K1(y)], y=R/(2 Rd)
    g_N = V_c^2 / R
    """
    R = np.asarray(R, dtype=float)
    sigma0 = sigma0_msun_pc2 * 1.0e6  # M_sun / kpc^2
    y = R / (2.0 * Rd)
    # Avoid y=0 singularity: g_N → 0 at centre for soft core behaviour of formula
    y_safe = np.maximum(y, 1e-8)
    i0, i1 = iv(0, y_safe), iv(1, y_safe)
    k0, k1 = kn(0, y_safe), kn(1, y_safe)
    bracket = i0 * k0 - i1 * k1
    v2 = 4.0 * np.pi * G_SPARC * sigma0 * Rd * (y_safe**2) * bracket
    gN = v2 / np.maximum(R, 1e-8)
    gN = np.where(R < 1e-6 * Rd, 0.0, gN)
    return np.abs(gN)


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    R = np.linspace(0.2 * args.Rd, 8.0 * args.Rd, args.n_radial)
    gN = exponential_disk_gN_midplane(R, args.sigma0, args.Rd)
    g = aqual_g_magnitude(gN, ir)
    v_N = np.sqrt(np.maximum(gN * R, 0.0))
    v = np.sqrt(np.maximum(g * R, 0.0))

    # Sanity: outer v should exceed Newtonian for same baryons (MOND boost)
    outer = R > 4.0 * args.Rd
    boost = float(np.mean(v[outer] / np.maximum(v_N[outer], 1e-30)))
    finite = bool(np.all(np.isfinite(g)) and np.all(g >= 0))
    passed = finite and boost > 1.05

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE0_DISK_MIDPLANE",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_EXP_DISK_MIDPLANE_AQUAL"
            if passed
            else "FAIL_DISK001_DISK_MIDPLANE"
        ),
        "ir": ir.to_dict(),
        "model": {
            "profile": "razor_thin_exponential",
            "sigma0_Msun_pc2": args.sigma0,
            "Rd_kpc": args.Rd,
            "n_radial": args.n_radial,
        },
        "diagnostics": {
            "outer_mean_v_over_vN": boost,
            "all_finite_nonneg": finite,
            "v_flat_proxy_kms": float(np.median(v[-5:])),
            "vN_flat_proxy_kms": float(np.median(v_N[-5:])),
        },
        "scientific_boundary": (
            "1D midplane Conditional AQUAL on thin exponential disk. "
            "Not a SPARC fit; not morphology-complete DISK-001 PASS; "
            "curl not measured in this reduction."
        ),
        "full_gate_status": "IN_PROGRESS",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_disk_midplane_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    np.savetxt(
        args.output_dir / "disk001_disk_midplane_curve.csv",
        np.column_stack([R, gN, g, v_N, v]),
        delimiter=",",
        header="R_kpc,gN,g_aqual,vN_kms,v_aqual_kms",
        comments="",
    )
    print(f"outer mean v/v_N boost: {boost:.3f}")
    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
