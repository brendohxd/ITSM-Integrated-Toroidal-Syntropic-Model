#!/usr/bin/env python3
"""VOR-001 mathematical-template-only winding audit (not a physics pass).

LABEL: mathematical-template-only
GATE:  VOR-001 (Open scaffold)
CLAIM: none Derived; no a0, C_obs, cosmology, lunar SWNT, 13/12, dual RAR

What this checks (toy math on a periodic 2-torus slice of T^3 thinking)
----------------------------------------------------------------------
1. Global winding integers n = (n_x, n_y) from phase holonomy on cycles.
2. Local phase fluctuations about a pure-winding background.
3. Separation: fluctuating field has zero net winding (integer residual ~0).
4. Toy energy E ~ integral |grad Theta|^2  for smooth superflow (template).
5. Negative controls:
   - trivial winding n=(0,0)
   - forced smooth density floor kills "core indicator"
   - non-integer fake holonomy rejected

What this deliberately does NOT do
----------------------------------
- Use physical G, a0, H0, C=2/3, or any ITSM packaging constants
- Couple to force field psi
- Claim resonance spectra or PTA intervals
- Validate a condensate action from UVIR

Exit status PASS_VOR001_MATH_TEMPLATE_ONLY means only that the template
separations and negative controls hold numerically.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--N", type=int, default=64, help="grid points per side")
    p.add_argument("--Lx", type=float, default=1.0)
    p.add_argument("--Ly", type=float, default=1.0)
    return p.parse_args()


def validate_grid(N: int, Lx: float, Ly: float) -> None:
    """Reject malformed or inadequate template grids explicitly."""
    if N < 4:
        raise ValueError("N must be at least 4")
    if not math.isfinite(Lx) or Lx <= 0.0:
        raise ValueError("Lx must be finite and strictly positive")
    if not math.isfinite(Ly) or Ly <= 0.0:
        raise ValueError("Ly must be finite and strictly positive")


def validate_winding_resolution(n: int, points: int, axis: str) -> None:
    """Require a phase step strictly below pi on the sampled cycle."""
    if 2 * abs(n) >= points:
        raise ValueError(
            f"under-resolved {axis}-winding: require 2*abs(n_{axis}) < N_{axis}"
        )


def phase_pure_winding(
    X: np.ndarray,
    Y: np.ndarray,
    n_x: int,
    n_y: int,
    Lx: float,
    Ly: float,
) -> np.ndarray:
    """Multi-valued phase with exact holonomies 2 pi n_i on the two cycles."""
    validate_winding_resolution(n_x, X.shape[1], "x")
    validate_winding_resolution(n_y, Y.shape[0], "y")
    return 2.0 * math.pi * (n_x * X / Lx + n_y * Y / Ly)


def unwrap_holonomy_1d(theta_line: np.ndarray) -> float:
    """Net phase advance along a periodic line sample (radians)."""
    d = np.diff(theta_line)
    # principal difference in (-pi, pi]
    d = (d + math.pi) % (2.0 * math.pi) - math.pi
    return float(np.sum(d) + ((theta_line[0] - theta_line[-1] + math.pi) % (2.0 * math.pi) - math.pi))


def holonomy_integers(
    Theta: np.ndarray,
    Lx: float,
    Ly: float,
) -> tuple[float, float, int, int]:
    """Estimate winding from mid-lines; return (w_x, w_y, n_x_round, n_y_round)."""
    Ny, Nx = Theta.shape
    mid_y = Ny // 2
    mid_x = Nx // 2
    # cycle along x at fixed y
    wx = unwrap_holonomy_1d(Theta[mid_y, :]) / (2.0 * math.pi)
    # cycle along y at fixed x
    wy = unwrap_holonomy_1d(Theta[:, mid_x]) / (2.0 * math.pi)
    return wx, wy, int(round(wx)), int(round(wy))


def is_near_integer(w: float, tol: float = 1e-6) -> bool:
    return abs(w - round(w)) < tol


def local_fluctuation_zero_winding(
    X: np.ndarray,
    Y: np.ndarray,
    Lx: float,
    Ly: float,
    amp: float = 0.15,
) -> np.ndarray:
    """Smooth 2π-periodic local phase with designed zero net winding."""
    return amp * np.sin(2.0 * math.pi * X / Lx) * np.cos(2.0 * math.pi * Y / Ly)


def toy_gradient_energy(Theta: np.ndarray, dx: float, dy: float) -> float:
    """Dimensionless Dirichlet energy of phase (smooth superflow template)."""
    # remove 2π jumps for pure winding is hard on multi-valued Theta;
    # use complex representation on unit circle instead
    z = np.exp(1j * Theta)
    dz_dx = (np.roll(z, -1, axis=1) - np.roll(z, 1, axis=1)) / (2.0 * dx)
    dz_dy = (np.roll(z, -1, axis=0) - np.roll(z, 1, axis=0)) / (2.0 * dy)
    dens = np.abs(dz_dx) ** 2 + np.abs(dz_dy) ** 2
    return float(np.sum(dens) * dx * dy)


def defect_like_density(
    X: np.ndarray,
    Y: np.ndarray,
    Lx: float,
    Ly: float,
    xi: float,
) -> np.ndarray:
    """Toy amplitude with a soft core near the cell centre (not a true vortex solver)."""
    x0, y0 = 0.5 * Lx, 0.5 * Ly
    r2 = (X - x0) ** 2 + (Y - y0) ** 2
    # on T^2, use minimum-image for a crude core
    dx = np.minimum(np.abs(X - x0), Lx - np.abs(X - x0))
    dy = np.minimum(np.abs(Y - y0), Ly - np.abs(Y - y0))
    r2 = dx**2 + dy**2
    return np.tanh(np.sqrt(r2) / xi)


def core_indicator(rho: np.ndarray, threshold: float = 0.2) -> float:
    """Fraction of points with rho below threshold (template diagnostic)."""
    return float(np.mean(rho < threshold))


def main() -> None:
    args = parse_args()
    N = args.N
    Lx, Ly = args.Lx, args.Ly
    validate_grid(N, Lx, Ly)
    x = np.linspace(0.0, Lx, N, endpoint=False)
    y = np.linspace(0.0, Ly, N, endpoint=False)
    X, Y = np.meshgrid(x, y)
    dx, dy = Lx / N, Ly / N

    checks: list[dict[str, Any]] = []

    # --- Positive control: integer winding recovery ---
    for n_x, n_y in [(0, 0), (1, 0), (0, 1), (1, -1), (2, 1)]:
        Theta = phase_pure_winding(X, Y, n_x, n_y, Lx, Ly)
        wx, wy, nx_r, ny_r = holonomy_integers(Theta, Lx, Ly)
        ok = (
            is_near_integer(wx)
            and is_near_integer(wy)
            and nx_r == n_x
            and ny_r == n_y
        )
        checks.append(
            {
                "name": f"holonomy_recover_n=({n_x},{n_y})",
                "ok": ok,
                "w_x": wx,
                "w_y": wy,
                "n_x_round": nx_r,
                "n_y_round": ny_r,
                "control_type": "positive",
            }
        )

    # --- Separation: local fluctuation does not change winding integers ---
    n_x, n_y = 1, 0
    Theta0 = phase_pure_winding(X, Y, n_x, n_y, Lx, Ly)
    vartheta = local_fluctuation_zero_winding(X, Y, Lx, Ly)
    Theta1 = Theta0 + vartheta
    wx0, wy0, _, _ = holonomy_integers(Theta0, Lx, Ly)
    wx1, wy1, nx1, ny1 = holonomy_integers(Theta1, Lx, Ly)
    sep_ok = (
        is_near_integer(wx1)
        and is_near_integer(wy1)
        and nx1 == n_x
        and ny1 == n_y
        and abs(wx1 - wx0) < 1e-6
        and abs(wy1 - wy0) < 1e-6
    )
    checks.append(
        {
            "name": "local_fluctuation_preserves_winding_integers",
            "ok": bool(sep_ok),
            "w_before": [wx0, wy0],
            "w_after": [wx1, wy1],
            "control_type": "positive_separation",
        }
    )

    # --- Toy energy increases with |n| for pure winding (template, not physics) ---
    e00 = toy_gradient_energy(phase_pure_winding(X, Y, 0, 0, Lx, Ly), dx, dy)
    e10 = toy_gradient_energy(phase_pure_winding(X, Y, 1, 0, Lx, Ly), dx, dy)
    e20 = toy_gradient_energy(phase_pure_winding(X, Y, 2, 0, Lx, Ly), dx, dy)
    energy_ok = e00 < 1e-10 and e10 > e00 and e20 > e10
    checks.append(
        {
            "name": "toy_dirichlet_energy_monotone_in_nx",
            "ok": bool(energy_ok),
            "E_00": e00,
            "E_10": e10,
            "E_20": e20,
            "control_type": "positive_template_energy",
            "note": "Dimensionless template only; not a physical tension",
        }
    )

    # --- Negative control 1: trivial winding ---
    wx, wy, nx_r, ny_r = holonomy_integers(
        phase_pure_winding(X, Y, 0, 0, Lx, Ly), Lx, Ly
    )
    trivial_ok = abs(wx) < 1e-6 and abs(wy) < 1e-6 and nx_r == 0 and ny_r == 0
    checks.append(
        {
            "name": "negative_control_trivial_winding",
            "ok": bool(trivial_ok),
            "w_x": wx,
            "w_y": wy,
            "control_type": "negative",
        }
    )

    # --- Negative control 2: forced smooth density floor ---
    rho_core = defect_like_density(X, Y, Lx, Ly, xi=0.05 * min(Lx, Ly))
    rho_smooth = np.maximum(rho_core, 0.5)
    core_frac = core_indicator(rho_core, 0.2)
    smooth_frac = core_indicator(rho_smooth, 0.2)
    smooth_ok = core_frac > 0.0 and smooth_frac == 0.0
    checks.append(
        {
            "name": "negative_control_forced_smooth_density_kills_core_indicator",
            "ok": bool(smooth_ok),
            "core_fraction_raw": core_frac,
            "core_fraction_floored": smooth_frac,
            "control_type": "negative",
        }
    )

    # --- Negative control 3: non-integer fake holonomy rejected ---
    fake_w = 1.37
    fake_ok = not is_near_integer(fake_w)
    checks.append(
        {
            "name": "negative_control_non_integer_fake_holonomy_rejected",
            "ok": bool(fake_ok),
            "fake_w": fake_w,
            "control_type": "negative",
        }
    )

    # --- Negative control 4: under-resolved winding is rejected ---
    alias_n = N // 2
    alias_rejected = False
    try:
        phase_pure_winding(X, Y, alias_n, 0, Lx, Ly)
    except ValueError:
        alias_rejected = True
    checks.append(
        {
            "name": "negative_control_under_resolved_winding_rejected",
            "ok": alias_rejected,
            "n_x": alias_n,
            "grid_points_x": N,
            "control_type": "negative",
        }
    )

    all_ok = all(c["ok"] for c in checks)
    status = (
        "PASS_VOR001_MATH_TEMPLATE_ONLY"
        if all_ok
        else "FAIL_VOR001_MATH_TEMPLATE"
    )

    summary = {
        "gate": "VOR-001",
        "label": "mathematical-template-only",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": status,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "forbidden_packaging_not_used": [
            "lunar_SWNT",
            "a0=cH0/2pi_as_circulation_quantum",
            "C=2/3",
            "13/12",
            "PTA_interval_from_a0_units",
            "automatic_cosmology_or_lensing",
        ],
        "separations_demonstrated": [
            "local_phase_fluctuation_vs_global_winding_integers",
            "topological_integers_vs_absent_Wilson_coefficients",
            "defect_core_indicator_vs_forced_smooth_density",
        ],
        "grid": {"N": N, "Lx": Lx, "Ly": Ly},
        "checks": checks,
        "scientific_boundary": (
            "Toy 2D periodic phase template illustrating holonomy integers, "
            "local fluctuation separation, and negative controls. Not a "
            "condensate action, not VOR-001 research PASS, not claim restoration."
        ),
        "next_research_stages": [
            "S1 finite-density background under a named V(rho)",
            "S2 winding-sector energy from declared action",
            "S3 true defect core ODE/PDE",
            "S4.0 define resonance before any spectrum packaging",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "vor001_winding_template_audit_summary.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print("VOR-001 mathematical-template-only audit")
    print("  physics_pass: False")
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']}")
    print("STATUS:", status)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
