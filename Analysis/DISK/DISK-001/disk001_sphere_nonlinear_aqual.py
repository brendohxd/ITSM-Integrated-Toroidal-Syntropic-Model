#!/usr/bin/env python3
"""DISK-001 Stage 1: spherical AQUAL identity + high-resolution residual audit.

Peer-review content
-------------------
Under spherical symmetry the AQUAL equation

  (1/r²) d/dr [ r² μ(|g|/a0) |g| ] = 4π G ρ

integrates exactly to the algebraic map

  |g| μ(|g|/a0) = |g_N| = G M(<r)/r².

Therefore a 1D "nonlinear PDE" is not an independent dynamical problem: it is a
**theorem + numerical residual check** of the discrete integration of enclosed
mass against the algebraic AQUAL root. This script documents that identity
(so Stage 1 does not overclaim a 1D nonlinear breakthrough) and verifies
high-resolution consistency for a Plummer sphere under declared Conditional IR.

Outputs machine-readable residuals suitable for a methods appendix.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from disk001_ir_law import (
    a0_effective,
    aqual_g_magnitude,
    default_conditional_ir,
    simple_mu_interpolating,
)

G_SPARC = 4.30091e-6


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--mass", type=float, default=1.0e10)
    p.add_argument("--b-kpc", type=float, default=1.0)
    p.add_argument(
        "--n-list",
        type=int,
        nargs="+",
        default=[64, 128, 256, 512],
        help="Radial resolutions for convergence of enclosed-mass integral.",
    )
    return p.parse_args()


def plummer_rho(r: np.ndarray, mass: float, b: float) -> np.ndarray:
    """Plummer density M_sun/kpc^3."""
    return (3.0 * mass / (4.0 * np.pi * b**3)) * (1.0 + (r / b) ** 2) ** (-2.5)


def plummer_mass_enclosed_exact(r: np.ndarray, mass: float, b: float) -> np.ndarray:
    return mass * r**3 / (r * r + b * b) ** 1.5


def plummer_gN_exact(r: np.ndarray, mass: float, b: float) -> np.ndarray:
    return G_SPARC * plummer_mass_enclosed_exact(r, mass, b) / np.maximum(r * r, 1e-30)


def trap_mass_enclosed(r: np.ndarray, rho: np.ndarray) -> np.ndarray:
    """M(<r) by cumulative trapezoid of 4π r² ρ."""
    m = np.zeros_like(r)
    integrand = 4.0 * np.pi * r * r * rho
    for i in range(1, len(r)):
        m[i] = m[i - 1] + 0.5 * (integrand[i] + integrand[i - 1]) * (r[i] - r[i - 1])
    return m


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    a0_eff = a0_effective(ir)

    rows = []
    for n in args.n_list:
        r = np.geomspace(1e-3 * args.b_kpc, 40.0 * args.b_kpc, n)
        rho = plummer_rho(r, args.mass, args.b_kpc)
        m_num = trap_mass_enclosed(r, rho)
        m_ex = plummer_mass_enclosed_exact(r, args.mass, args.b_kpc)
        # avoid r=0 end
        mask = r > 0.05 * args.b_kpc
        mass_rel = float(
            np.max(np.abs(m_num[mask] - m_ex[mask]) / np.maximum(m_ex[mask], 1e-30))
        )

        gN_ex = plummer_gN_exact(r, args.mass, args.b_kpc)
        gN_num = G_SPARC * m_num / np.maximum(r * r, 1e-30)
        g_alg = aqual_g_magnitude(gN_ex, ir)

        # Discrete spherical AQUAL residual of the *identity*:
        # flux F = r² μ(g/a0) g should equal G M_num (in consistent units)
        # g from algebraic map on gN_num; residual relative to G M_num
        g = aqual_g_magnitude(gN_num, ir)
        mu = simple_mu_interpolating(g / a0_eff)
        flux = (r * r) * mu * g
        rhs = G_SPARC * m_num
        # identity residual (should be ~0 if algebraic map exact)
        id_rel = float(
            np.max(np.abs(flux[mask] - rhs[mask]) / np.maximum(np.abs(rhs[mask]), 1e-30))
        )
        # gN numerical vs exact
        gN_rel = float(
            np.max(np.abs(gN_num[mask] - gN_ex[mask]) / np.maximum(gN_ex[mask], 1e-30))
        )

        rows.append(
            {
                "n": int(n),
                "mass_enclosed_max_rel_err": mass_rel,
                "gN_num_vs_exact_max_rel_err": gN_rel,
                "spherical_aqual_identity_max_rel_err": id_rel,
                "outer_g_aqual": float(g_alg[-1]),
                "outer_gN": float(gN_ex[-1]),
            }
        )

    # Convergence: mass integral error should decrease with n (monotone in max)
    mass_errs = [row["mass_enclosed_max_rel_err"] for row in rows]
    conv_ok = all(mass_errs[i] >= mass_errs[i + 1] * 0.5 for i in range(len(mass_errs) - 1)) or (
        mass_errs[-1] < mass_errs[0]
    )
    id_ok = all(row["spherical_aqual_identity_max_rel_err"] < 1e-10 for row in rows)
    mass_ok = mass_errs[-1] < 5e-3
    passed = bool(id_ok and mass_ok and conv_ok)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE1_SPHERE_NONLINEAR_IDENTITY",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_SPHERE_AQUAL_IDENTITY_CONVERGENCE"
            if passed
            else "FAIL_DISK001_SPHERE_STAGE1"
        ),
        "theorem": (
            "Spherical AQUAL integrates to |g| μ(|g|/a0)=|g_N|; 1D nonlinear "
            "solve is not independent of the algebraic map."
        ),
        "ir": ir.to_dict(),
        "a0_eff": a0_eff,
        "model": {"profile": "Plummer", "mass_Msun": args.mass, "b_kpc": args.b_kpc},
        "convergence": rows,
        "diagnostics": {
            "finest_mass_rel_err": mass_errs[-1],
            "identity_ok": id_ok,
            "mass_ok": mass_ok,
            "error_improves_with_n": conv_ok,
        },
        "scientific_boundary": (
            "Documents spherical AQUAL≡algebraic map and numerical mass-integral "
            "convergence. Does not constitute a non-spherical nonlinear PDE solve; "
            "see disk001_poisson_2d_aqual.py for that. Conditional IR only; not "
            "Derived C_obs; not full DISK-001 PASS."
        ),
        "full_gate_status": "IN_PROGRESS",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_sphere_nonlinear_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print("Theorem: spherical AQUAL ⇔ algebraic map (identity residual checks)")
    for row in rows:
        print(
            f"  n={row['n']:4d}  mass_err={row['mass_enclosed_max_rel_err']:.3e}  "
            f"id_err={row['spherical_aqual_identity_max_rel_err']:.3e}"
        )
    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
