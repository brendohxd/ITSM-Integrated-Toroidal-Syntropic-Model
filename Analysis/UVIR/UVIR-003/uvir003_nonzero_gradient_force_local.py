#!/usr/bin/env python3
"""UVIR-003 Track A: local nonzero-gradient expansion of exact |grad(pi)|^3.

Master-plan remaining alpha.10 item after
PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN:

  Nonzero-gradient |grad(pi)|^3 sector on a declared background.

Context
-------
Exact Track-A IR force density contains

    - A_IR |grad(pi)|^3

which is nonanalytic at the homogeneous zero-gradient origin and therefore has
no ordinary trilinear Taylor kernel on the FRW freeze used for the local
four-leg assembly.  Force-completion Track A (see UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS)
preserves the exact Y^(3/2) law by expanding around a *declared local*
nonzero spatial gradient background.

What this script does
---------------------
1. Declares a local background with |grad(pi_bar)| = v > 0 along e_x.
2. Expands |v e_x + epsilon * grad(delta pi)|^3 through O(epsilon^4).
3. Verifies coefficients against the documented Track-A expansion.
4. Builds the local force Lagrangian contributions from -A_IR |grad pi|^3
   (quadratic / cubic / quartic in fluctuations).
5. Checks the spatial Hessian of the quadratic force term is positive for
   A_IR > 0 (parallel + transverse eigenvalues).
6. Constructs the local momentum-space cubic force vertex for three plane-wave
   legs on this anisotropic background (parallel/transverse projectors).
7. Records that this is *not* a homogeneous FRW 2-to-2 amplitude.

What this does *not* do
-----------------------
- Unlock MAT-001.
- Claim an isotropic cosmological S-matrix involving the exact Y^(3/2) vertex.
- Evaluate nested in-in integrals.
- Declare unitarity / strong-coupling scale (next alpha.10 item).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--v-samples",
        type=float,
        nargs="+",
        default=[0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
        help="Background gradient magnitudes v = |grad pi_bar|.",
    )
    parser.add_argument(
        "--A-IR",
        type=float,
        default=1.0,
        help="Force amplitude A_IR > 0 used in numerical samples.",
    )
    return parser.parse_args()


def require(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        msg = name if not detail else f"{name}: {detail}"
        raise AssertionError(msg)


def require_zero(name: str, expression: sp.Expr) -> None:
    residual = sp.simplify(sp.expand(expression))
    if residual != 0:
        raise AssertionError(f"{name} failed: {residual}")


def analytic_track_a_expansion() -> dict[str, Any]:
    """Expand |v e_x + eps * g|^3 with g = (x, y, z)."""
    eps = sp.symbols("epsilon", positive=True)
    v = sp.symbols("v", positive=True)
    x, y, z = sp.symbols("x y z", real=True)
    # Spatial gradient fluctuation components in the local orthonormal frame
    # with e_parallel = e_x.
    g = sp.Matrix([v + eps * x, eps * y, eps * z])
    mag = sp.sqrt(sp.expand(g.dot(g)))
    # |g|^3 = (g·g)^{3/2}
    y3 = sp.expand(mag**3)

    # Series in epsilon through O(eps^4) — expand fully before coeff extraction
    series = sp.expand(y3.series(eps, 0, 5).removeO())
    coeffs = {n: sp.simplify(sp.expand(series.coeff(eps, n))) for n in range(0, 5)}

    # Documented Track A expansion (FORCE_COMPLETION_OPTIONS §4):
    # |v + eps grad|^3
    #   = v^3
    #   + 3 v^2 eps x
    #   + (3/2) v eps^2 (2 x^2 + p_perp^2)
    #   + eps^3 (x^3 + (3/2) x p_perp^2)
    #   + (3/8) eps^4 p_perp^4 / v
    #   + O(eps^5)
    # with p_perp^2 = y^2 + z^2.
    p_perp_sq = y**2 + z**2
    expected = {
        0: v**3,
        1: 3 * v**2 * x,
        2: sp.Rational(3, 2) * v * (2 * x**2 + p_perp_sq),
        3: x**3 + sp.Rational(3, 2) * x * p_perp_sq,
        4: sp.Rational(3, 8) * p_perp_sq**2 / v,
    }
    for n, target in expected.items():
        require_zero(f"Track-A coeff eps^{n}", coeffs[n] - sp.expand(target))

    # Lagrangian density contribution L = -A_IR |grad pi|^3
    A = sp.symbols("A_IR", positive=True)
    L2 = sp.simplify(-A * coeffs[2])
    L3 = sp.simplify(-A * coeffs[3])
    L4 = sp.simplify(-A * coeffs[4])

    # Quadratic form: L2 = -A * (3/2) v * (2 x^2 + y^2 + z^2)
    # Hessian w.r.t. (x,y,z): diag(-3 A v, - (3/2) A v, - (3/2) A v)
    # For positive A,v the *energy density* from -L (if L is Lagrangian density
    # with positive kinetic elsewhere) needs care: the spatial gradient term
    # enters the potential. Stage A: cubic force Hessian positive at nonzero
    # gradient for A>0 means the second variation of +A |grad|^3 potential
    # (i.e. -L_force) is positive.
    potential2 = sp.simplify(-L2)  # = A * (3/2) v * (2 x^2 + p_perp^2)
    hess = sp.hessian(potential2, (x, y, z))
    eigs = [sp.simplify(e) for e in hess.eigenvals().keys()]
    # Expected eigenvalues: 3 A v (parallel, multiplicity 1 from 2x^2 term
    #   d2/dx2 of A*(3/2)*v*2 x^2 = d2/dx2 of 3 A v x^2 = 6 A v? Wait.
    # potential2 = A*(3/2)*v*(2 x^2 + y^2 + z^2) = 3 A v x^2 + (3/2) A v (y^2+z^2)
    # Hessian diag(6 A v, 3 A v, 3 A v)
    expected_eigs = {6 * A * v, 3 * A * v}
    require(
        "Hessian eigenvalues match",
        set(eigs) == expected_eigs,
        detail=str(eigs),
    )
    # Positivity for A>0, v>0
    pos = all(sp.ask(sp.Q.positive(e.subs({A: 1, v: 1}))) for e in eigs)
    require("Hessian positive at A=v=1", bool(pos))

    return {
        "background": "grad(pi_bar) = v e_x with v>0",
        "expansion_variable": "epsilon * (x,y,z) fluctuation gradient",
        "coefficients": {str(n): str(coeffs[n]) for n in range(5)},
        "expected_match": "PASS_TRACK_A_SERIES_MATCH",
        "L2_force": str(L2),
        "L3_force": str(L3),
        "L4_force": str(L4),
        "potential_quadratic": str(potential2),
        "hessian_eigenvalues": [str(e) for e in eigs],
        "hessian_positive_for_A_v_positive": True,
        "quartic_singular_as_v_to_0": True,
        "isotropic_zero_gradient_limit": "NONANALYTIC_NOT_TAKEN",
    }


def local_cubic_vertex_momentum() -> dict[str, Any]:
    """Cubic force vertex on the anisotropic background in Fourier space.

    From L3 = -A * (x^3 + (3/2) x p_perp^2)
            = -A * (x^3 + (3/2) x (y^2 + z^2))

    With x = i k_parallel delta_pi etc. for each leg... more carefully:
    the cubic density is a local product of three first spatial derivatives.
    For three plane waves with wavevectors k1,k2,k3 and polarization amplitudes
    of delta pi, the vertex factor is the symmetrized contraction of
    derivatives into the cubic polynomial.

    Write fluctuation gradient g = ∇ δπ. Then
      L3/(-A) = g_∥^3 + (3/2) g_∥ |g_⊥|^2
    In Fourier space each g_i -> i k_i π_i, and the vertex multiplies three
    amplitudes π1 π2 π3 with all permutations of the cubic monomials.
    """
    A, v = sp.symbols("A_IR v", positive=True)
    # Not needed for vertex polynomial itself (v enters L2/L4, not L3)
    _ = v

    def mono_vertex(k1, k2, k3):
        """Contribution of g_x^3 + (3/2) g_x (g_y^2 + g_z^2) symmetrized.

        For product of derivatives, Fourier: g_a(kj) ~ i (k_j)_a.
        Vertex for π1 π2 π3 from cubic form C_abc g^a g^b g^c is
        sum_perms C_abc (ik1)_a (ik2)_b (ik3)_c.
        Since each g brings one i, overall factor is i^3 = -i.
        """
        # Fully symmetrized cubic form associated to
        # f = g_x^3 + (3/2) g_x (g_y^2 + g_z^2)
        # = g_x^3 + (3/2) g_x g_y^2 + (3/2) g_x g_z^2
        # Multilinearization of (1/6) d3 f:
        # For pure g_x^3: coefficient 1 -> multilin  g_x1 g_x2 g_x3 * 6 / 6 = product
        # Standard: for f = (1/6) λ_abc g^a g^b g^c with λ fully symmetric,
        # multilin is λ_abc g1^a g2^b g3^c.
        # For g_x^3: λ_xxx = 6, multilin = 6 g_x1 g_x2 g_x3 / something?
        # Easier: f(g) = g_x^3 + (3/2) g_x g_y^2 + (3/2) g_x g_z^2
        # Polarization: (1/6) d^3/de1 de2 de3 f(e1 g1 + e2 g2 + e3 g3) at 0
        e1, e2, e3 = sp.symbols("e1 e2 e3")
        gx = e1 * k1[0] + e2 * k2[0] + e3 * k3[0]
        gy = e1 * k1[1] + e2 * k2[1] + e3 * k3[1]
        gz = e1 * k1[2] + e2 * k2[2] + e3 * k3[2]
        f = gx**3 + sp.Rational(3, 2) * gx * (gy**2 + gz**2)
        # Each Fourier gradient contributes a factor of i, so (i)^3 = -i
        # times this polarization of the real polynomial in k-components.
        pol = sp.diff(sp.diff(sp.diff(f, e1), e2), e3).subs({e1: 0, e2: 0, e3: 0})
        return sp.simplify(-sp.I * pol)  # include i^3 = -i

    # Symbolic wavevector components
    k1 = sp.symbols("k1x k1y k1z", real=True)
    k2 = sp.symbols("k2x k2y k2z", real=True)
    k3 = sp.symbols("k3x k3y k3z", real=True)
    vertex_poly = mono_vertex(k1, k2, k3)
    # Full vertex multiplies by -A_IR (from L = -A |...|)
    vertex = sp.simplify(-A * vertex_poly)

    # Consistency: pure parallel waves k = (q,0,0)
    q = sp.symbols("q", positive=True)
    v_par = sp.simplify(
        vertex.subs(
            {
                k1[0]: q,
                k1[1]: 0,
                k1[2]: 0,
                k2[0]: q,
                k2[1]: 0,
                k2[2]: 0,
                k3[0]: q,
                k3[1]: 0,
                k3[2]: 0,
            }
        )
    )
    # f = 3 g_x1 g_x2 g_x3 * 2?  d3/de of (e1+e2+e3)^3 q^3 at 0
    # (sum ei)^3 -> 6 e1 e2 e3, so pol = 6 q^3, * (-i) * (-A) = 6 i A q^3
    # Wait: vertex = -A * (-i * pol) = A i pol; pol for g_x^3:
    # f=(e1 k1x+...)^3 with ki x = q => (q(e1+e2+e3))^3, d3 = 6 q^3
    # vertex = -A * (-I) * 6 q^3 = 6 I A q^3
    require_zero("parallel cubic vertex", v_par - 6 * sp.I * A * q**3)

    return {
        "vertex_expression": str(vertex),
        "fourier_convention": "g_a(k) = i k_a π(k); overall i^3 = -i in polynomial map",
        "parallel_check": "6*I*A_IR*q**3 for three parallel legs k=(q,0,0)",
        "status": "PASS_LOCAL_CUBIC_FORCE_VERTEX",
        "not_isotropic_frw_amplitude": True,
    }


def numerical_samples(v_values: list[float], a_ir: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for v in v_values:
        # Quadratic potential eigenvalues (from Hessian of A*(3/2)v*(2x^2+y^2+z^2))
        # diag(6 A v, 3 A v, 3 A v)
        e_par = 6.0 * a_ir * v
        e_perp = 3.0 * a_ir * v
        # Quartic coefficient singularity ~ 1/v
        quartic_coeff = (3.0 / 8.0) * a_ir / v  # from -L4 with L4 = -A*(3/8) p^4/v
        # => potential4 = A*(3/8) p_perp^4 / v
        rows.append(
            {
                "v": v,
                "A_IR": a_ir,
                "hessian_parallel": e_par,
                "hessian_transverse": e_perp,
                "hessian_min": min(e_par, e_perp),
                "positive_hessian": bool(e_par > 0 and e_perp > 0),
                "quartic_p_perp_coeff": quartic_coeff,
                "quartic_blows_up_as_v_to_0": True,
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    require("A_IR positive", args.A_IR > 0)
    require("v samples positive", all(v > 0 for v in args.v_samples))

    analytic = analytic_track_a_expansion()
    vertex = local_cubic_vertex_momentum()
    samples = numerical_samples(list(args.v_samples), float(args.A_IR))

    all_pos = all(s["positive_hessian"] for s in samples)
    require("all sample Hessians positive", all_pos)

    # v -> 0 singularity of quartic
    qs = [s["quartic_p_perp_coeff"] for s in samples]
    require(
        "quartic coefficient decreases with v",
        qs == sorted(qs, reverse=True),
        detail=str(qs),
    )

    passed = (
        analytic["expected_match"] == "PASS_TRACK_A_SERIES_MATCH"
        and analytic["hessian_positive_for_A_v_positive"]
        and vertex["status"] == "PASS_LOCAL_CUBIC_FORCE_VERTEX"
        and all_pos
    )
    status = (
        "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
        if passed
        else "FAIL_NONZERO_GRADIENT_FORCE_LOCAL"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_NONZERO_GRADIENT_FORCE_LOCAL",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "track": "A_exact_Y_3_over_2_on_declared_nonzero_gradient_background",
        "physical_2_to_2_status": (
            "LOCAL_FORCE_VERTEX_ON_ANISOTROPIC_BACKGROUND_NOT_HOMOGENEOUS_S_MATRIX"
        ),
        "analytic": analytic,
        "local_cubic_vertex": vertex,
        "numerical_samples": samples,
        "scientific_boundary": (
            "Declares and verifies the Track-A local expansion of exact "
            "|grad(pi)|^3 about a nonzero spatial-gradient background, including "
            "positive Hessian for A_IR>0 and a local cubic force vertex. This is "
            "not an isotropic FRW 2-to-2 amplitude, does not evaluate nested "
            "in-in integrals, does not establish unitarity or a strong-coupling "
            "scale, and does not unlock MAT-001. The quartic coefficient is "
            "singular as v->0, so the zero-gradient homogeneous limit is not "
            "taken."
        ),
        "next_required_calculation": [
            "declared perturbative-unitarity / EFT-validity criterion on the "
            "combined high-q Green proxy + local nonzero-gradient force sector "
            "(scope-limited; not 'theory closed')",
            "optional: couple local force vertex into the multi-slice FRW Green "
            "proxy as an anisotropic source term",
        ],
        "diagnostics": {
            "series_match": analytic["expected_match"],
            "hessian_positive": analytic["hessian_positive_for_A_v_positive"],
            "vertex_status": vertex["status"],
            "all_samples_positive": all_pos,
            "n_v_samples": len(samples),
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_nonzero_gradient_force_local_summary.json"
    out_csv = args.output_dir / "uvir003_nonzero_gradient_force_local_samples.csv"
    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = list(samples[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(samples)

    print(f"Track A series match: {analytic['expected_match']}")
    print(f"Hessian eigenvalues: {analytic['hessian_eigenvalues']}")
    print(f"Local cubic vertex: {vertex['status']}")
    print(f"v samples: {args.v_samples}  all Hessian positive: {all_pos}")
    print("Homogeneous FRW S-matrix from exact Y^(3/2): NOT_CLAIMED")
    print("Full in-in: NOT_COMPUTED")
    print("Unitarity: NOT_ESTABLISHED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
