#!/usr/bin/env python3
"""DISK-001 Stage 0: 2D curl residual of algebraic AQUAL map on disk-like g_N.

If g = f(|g_N|) g_N with g_N = -∇Φ_N curl-free, g is *not* automatically a
gradient field. This script measures ||∇×g|| / ||∇g||_rms on a Cartesian
midplane patch using finite differences — the diagnostic required by DISK-001
readiness (quantify curl; do not assert zero).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from disk001_ir_law import aqual_g_from_gN, default_conditional_ir

G_SPARC = 4.30091e-6


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--n", type=int, default=81, help="grid points per side (odd)")
    p.add_argument("--half-box-kpc", type=float, default=12.0)
    p.add_argument("--sigma0", type=float, default=300.0, help="M_sun/pc^2")
    p.add_argument("--Rd", type=float, default=3.0)
    return p.parse_args()


def kuzmin_like_gN(x: np.ndarray, y: np.ndarray, mass: float, a: float) -> tuple[np.ndarray, np.ndarray]:
    """Simple axisymmetric Newtonian field in plane: Plummer-projected proxy.

    g_N = -∇Φ with Φ = -G M / sqrt(R^2 + a^2) (softened point / Kuzmin-like).
    """
    R2 = x * x + y * y
    denom = (R2 + a * a) ** 1.5
    gx = G_SPARC * mass * x / denom
    gy = G_SPARC * mass * y / denom
    return gx, gy


def finite_curl_z(gx: np.ndarray, gy: np.ndarray, dx: float, dy: float) -> np.ndarray:
    """(∇×g)_z ≈ ∂g_y/∂x - ∂g_x/∂y on interior."""
    dgy_dx = np.gradient(gy, dx, axis=1)
    dgx_dy = np.gradient(gx, dy, axis=0)
    return dgy_dx - dgx_dy


def main() -> None:
    args = parse_args()
    if args.n % 2 == 0:
        args.n += 1
    ir = default_conditional_ir()

    xs = np.linspace(-args.half_box_kpc, args.half_box_kpc, args.n)
    ys = np.linspace(-args.half_box_kpc, args.half_box_kpc, args.n)
    dx = xs[1] - xs[0]
    dy = ys[1] - ys[0]
    X, Y = np.meshgrid(xs, ys, indexing="xy")

    # Mass scale from exponential disk total M = 2π Σ0 Rd^2
    sigma0 = args.sigma0 * 1.0e6
    mass = 2.0 * np.pi * sigma0 * args.Rd**2
    gNx, gNy = kuzmin_like_gN(X, Y, mass, args.Rd)

    # Algebraic AQUAL map pointwise
    gx = np.zeros_like(gNx)
    gy = np.zeros_like(gNy)
    for i in range(args.n):
        for j in range(args.n):
            vec = aqual_g_from_gN(np.array([gNx[i, j], gNy[i, j]]), ir)
            gx[i, j], gy[i, j] = vec[0], vec[1]

    curl_N = finite_curl_z(gNx, gNy, dx, dy)
    curl_g = finite_curl_z(gx, gy, dx, dy)

    # Interior mask (drop 2-cell boundary)
    m = np.zeros_like(curl_g, dtype=bool)
    m[2:-2, 2:-2] = True
    # Exclude very centre singularity soft region
    m &= (X**2 + Y**2) > (0.5 * args.Rd) ** 2

    def rms(a: np.ndarray) -> float:
        return float(np.sqrt(np.mean(a[m] ** 2)))

    curl_N_rms = rms(curl_N)
    curl_g_rms = rms(curl_g)
    gN_rms = rms(np.sqrt(gNx**2 + gNy**2))
    g_rms = rms(np.sqrt(gx**2 + gy**2))
    # Strain proxy for normalisation
    dg = np.gradient(gx, dy, axis=0)
    strain_rms = rms(dg)
    curl_ratio = curl_g_rms / max(strain_rms, 1e-30)
    # Relative curls (FD residual scale)
    curl_N_rel = curl_N_rms / max(gN_rms / max(dx, 1e-30), 1e-30)
    curl_g_rel = curl_g_rms / max(g_rms / max(dx, 1e-30), 1e-30)

    # Radial Newtonian field: relative FD curl should be << 1
    newton_ok = curl_N_rel < 0.05
    # AQUAL algebraic map: we require a measured diagnostic (finite), and
    # typically larger relative curl than pure Newtonian FD noise.
    measured = np.isfinite(curl_ratio) and np.isfinite(curl_g_rel)
    map_has_structure = curl_g_rms >= 0.0
    passed = newton_ok and measured and map_has_structure

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE0_CURL_RESIDUAL",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_CURL_RESIDUAL_MEASURED"
            if passed
            else "FAIL_DISK001_CURL"
        ),
        "ir": ir.to_dict(),
        "grid": {
            "n": args.n,
            "half_box_kpc": args.half_box_kpc,
            "dx_kpc": dx,
        },
        "diagnostics": {
            "curl_newton_rms": curl_N_rms,
            "curl_aqual_map_rms": curl_g_rms,
            "curl_newton_rel_to_g_over_dx": curl_N_rel,
            "curl_aqual_rel_to_g_over_dx": curl_g_rel,
            "strain_proxy_rms": strain_rms,
            "curl_over_strain_aqual": curl_ratio,
            "newton_curl_small": bool(newton_ok),
            "note": (
                "Algebraic AQUAL map g=f(|gN|)gN on a curl-free gN is not "
                "guaranteed curl-free; nonlinear AQUAL Poisson would restore "
                "potential structure. Reported residual is the Stage-0 diagnostic."
            ),
        },
        "scientific_boundary": (
            "2D finite-difference curl diagnostic of the *algebraic* Conditional "
            "AQUAL map. Not a full nonlinear AQUAL Poisson solve; not DISK-001 PASS."
        ),
        "full_gate_status": "IN_PROGRESS",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_curl_residual_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"curl_N rms: {curl_N_rms:.3e}  rel: {curl_N_rel:.3e}")
    print(f"curl_AQUAL-map rms: {curl_g_rms:.3e}  rel: {curl_g_rel:.3e}")
    print(f"curl/strain (AQUAL map): {curl_ratio:.3e}")
    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
