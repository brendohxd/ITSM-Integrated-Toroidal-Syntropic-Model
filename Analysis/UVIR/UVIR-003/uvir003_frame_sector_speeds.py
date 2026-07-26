#!/usr/bin/env python3
"""UVIR-003 Stage B (frame sector only): coupled aether-metric mode speeds.

Verifies the sign/convention map between the UVIR-003 Stage-A frame action
(signature -+++, U^mu U_mu=-1) and the Eling-Jacobson-Mattingly Einstein-aether
review (arXiv:gr-qc/0410001; signature +---, u^a u_a=+1), then substitutes
that verified map into their published Table 1 mode-speed formulas and checks
that they reduce to Stage A's decoupled-limit speeds (c1/c14, c123/c14) in the
weak-metric-coupling limit already used there.

This is a literature-substitution check, not an independent re-derivation of
the full linearized Einstein-aether field equations. The substitution itself
(not just the final formulas) is verified symbolically below.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the frame-sector JSON summary.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Verify the c_i sign/convention map between EJM (+---) and Stage-A
    #    (-+++) by tracking explicit metric factors through all four terms
    #    of K^{ab}_{mn} nabla_a u^m nabla_b u^n, using an arbitrary
    #    symbolic 'nabla_a u^m' object (Christoffel symbols, and hence
    #    covariant derivatives of matching index type, are invariant under
    #    a global g -> -g rescaling, since Gamma ~ g^{-1} d(g) picks up two
    #    sign flips that cancel).
    # ------------------------------------------------------------------
    eta_ejm = sp.diag(1, -1, -1, -1)
    eta_itsm = sp.diag(-1, 1, 1, 1)
    require("signature is a global sign flip", eta_itsm == -eta_ejm)

    ubar = sp.Matrix([1, 0, 0, 0])
    nabla_u = sp.Matrix(4, 4, lambda a, m: sp.Symbol(f"M_{a}{m}"))  # nabla_a u^m

    def c1_term(eta: sp.Matrix) -> sp.Expr:
        eta_inv = eta.inv()
        return sp.expand(
            sum(
                eta_inv[a, b] * eta[m, n] * nabla_u[a, m] * nabla_u[b, n]
                for a in range(4)
                for b in range(4)
                for m in range(4)
                for n in range(4)
            )
        )

    def c2_term(eta: sp.Matrix) -> sp.Expr:
        eta_inv = eta.inv()
        divergence = sum(
            eta_inv[a, b] * eta[b, m] * nabla_u[a, m]
            for a in range(4)
            for b in range(4)
            for m in range(4)
        )
        return sp.expand(divergence**2)

    def c3_term(eta: sp.Matrix) -> sp.Expr:
        delta = eta.inv() * eta
        return sp.expand(
            sum(
                delta[a, n]
                * delta[b, m]
                * nabla_u[a, m]
                * nabla_u[b, n]
                for a in range(4)
                for b in range(4)
                for m in range(4)
                for n in range(4)
            )
        )

    def c4_term(eta: sp.Matrix) -> sp.Expr:
        return sp.expand(
            sum(
                ubar[a] * ubar[b] * eta[m, n] * nabla_u[a, m] * nabla_u[b, n]
                for a in range(4)
                for b in range(4)
                for m in range(4)
                for n in range(4)
            )
        )

    c1_ejm, c1_itsm = c1_term(eta_ejm), c1_term(eta_itsm)
    c2_ejm, c2_itsm = c2_term(eta_ejm), c2_term(eta_itsm)
    c3_ejm, c3_itsm = c3_term(eta_ejm), c3_term(eta_itsm)
    c4_ejm, c4_itsm = c4_term(eta_ejm), c4_term(eta_itsm)
    require("c1 term is convention-invariant", sp.simplify(c1_ejm - c1_itsm) == 0)
    require("c2 term is convention-invariant", sp.simplify(c2_ejm - c2_itsm) == 0)
    require("c3 term is convention-invariant", sp.simplify(c3_ejm - c3_itsm) == 0)
    require("c4 term flips sign under signature flip", sp.simplify(c4_ejm + c4_itsm) == 0)

    # Stage-A's declared bracket carries an explicit extra minus sign on its
    # c4 term ("-c4 a_mu a^mu"), which cancels the sign flip just verified.
    # Net result: c1, c2, c3, c4 all map identically (no relabeling) between
    # the Stage-A action and EJM's Table 1.
    convention_map = (
        "IDENTITY OPERATOR LABELS AND SIGNS; "
        "alpha_i(EJM)=(M_U^2/M_P^2)*c_i(Stage A)"
    )

    # ------------------------------------------------------------------
    # 2. EJM Table 1 mode speeds (quoted, using the verified identity map).
    # ------------------------------------------------------------------
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    c13 = c1 + c3
    c14 = c1 + c4
    c123 = c1 + c2 + c3
    r_u = sp.symbols("r_U", positive=True)
    alpha1, alpha2, alpha3, alpha4 = (
        r_u * c1,
        r_u * c2,
        r_u * c3,
        r_u * c4,
    )
    alpha13 = sp.simplify(alpha1 + alpha3)
    alpha14 = sp.simplify(alpha1 + alpha4)
    alpha123 = sp.simplify(alpha1 + alpha2 + alpha3)

    s_tensor_sq = sp.simplify(1 / (1 - alpha13))
    s_vector_sq = sp.simplify(
        (alpha1 - alpha1**2 / 2 + alpha3**2 / 2)
        / (alpha14 * (1 - alpha13))
    )
    s_scalar_sq = sp.simplify(
        alpha123
        * (2 - alpha14)
        / (alpha14 * (1 - alpha13) * (2 + alpha13 + 3 * alpha2))
    )

    # ------------------------------------------------------------------
    # 3. Weak-metric-coupling limit: EJM state the stability conditions
    #    reduce to the simple ratios "for c_i small compared to unity" —
    #    i.e. all four c_i scaled together, not c1,c3 alone. Scale
    #    c1,c2,c3,c4 -> eps*c1,eps*c2,eps*c3,eps*c4 and take the leading
    #    eps->0 behavior of each ratio.
    # ------------------------------------------------------------------
    vector_leading = sp.limit(s_vector_sq, r_u, 0, dir="+")
    scalar_leading = sp.limit(s_scalar_sq, r_u, 0, dir="+")

    expected_vector_decoupled = sp.simplify(c1 / c14)
    expected_scalar_decoupled = sp.simplify(c123 / c14)

    require(
        "vector speed reduces to Stage-A decoupled c1/c14 for r_U -> 0",
        sp.simplify(vector_leading - expected_vector_decoupled) == 0,
    )
    require(
        "scalar speed reduces to Stage-A decoupled c123/c14 for r_U -> 0",
        sp.simplify(scalar_leading - expected_scalar_decoupled) == 0,
    )
    vector_leading_coeff = vector_leading
    scalar_leading_coeff = scalar_leading

    # ------------------------------------------------------------------
    # 4. No-ghost / positivity conditions (EJM Table 1 discussion, quoted).
    # ------------------------------------------------------------------
    stability_conditions_small_alpha = [
        "alpha1/alpha14 >= 0",
        "alpha123/alpha14 >= 0",
    ]
    energy_positivity_exact = [
        "(2*alpha1 - alpha1**2 + alpha3**2)/(1 - alpha13) > 0  # vector mode",
        "alpha14*(2 - alpha14) > 0  # trace/scalar mode",
    ]
    light_cone_condition = (
        "alpha4=0, alpha3=-alpha1, "
        "alpha2=alpha1/(1-2*alpha1)"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_FRAME_SECTOR_PARTIAL",
        "method": "literature_substitution_verified",
        "source": "Eling, Jacobson, Mattingly, arXiv:gr-qc/0410001, Table 1",
        "convention_map": convention_map,
        "normalization_map": {
            "ratio": "r_U=M_U^2/M_P^2",
            "published_coefficients": "alpha_i=r_U*c_i",
            "bare_identity_valid_only_if": "M_U=M_P",
        },
        "convention_checks": {
            "c1": "PASS: invariant under global signature flip",
            "c2": "PASS: invariant under global signature flip",
            "c3": "PASS: invariant under global signature flip",
            "c4": "PASS: contraction flips; Stage-A explicit minus sign restores the identity coefficient map",
        },
        "mode_speeds_squared": {
            "spin_2_tensor": str(s_tensor_sq),
            "spin_1_vector": str(s_vector_sq),
            "spin_0_scalar": str(s_scalar_sq),
        },
        "consistency_with_stage_a_decoupled_limit": {
            "scaling": "r_U=M_U^2/M_P^2 -> 0+ with fixed c_i ratios",
            "vector_leading": str(vector_leading_coeff),
            "expected_vector": str(expected_vector_decoupled),
            "scalar_leading": str(scalar_leading_coeff),
            "expected_scalar": str(expected_scalar_decoupled),
            "verdict": "CONSISTENT",
        },
        "stability_conditions_small_alpha": stability_conditions_small_alpha,
        "energy_positivity_exact": energy_positivity_exact,
        "light_cone_condition": light_cone_condition,
        "not_yet_done": [
            "force-sector (psi) coupling to the frame sector in this SVT decomposition",
            "condensate (Phi) coupling to the frame sector",
            "full nonzero-background (accelerating/vortical U) generalization",
            "independent from-scratch re-derivation (this result relies on a verified literature substitution, not a first-principles ITSM-side linearized Einstein equation calculation)",
        ],
        "status": "PARTIAL_PROGRESS_FRAME_SECTOR_ONLY",
    }
    json_path = args.output_dir / "uvir003_frame_sector_speeds_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 Stage B frame-sector mode speeds: literature substitution VERIFIED")
    print("Aether normalization: alpha_i=(M_U^2/M_P^2)*c_i")
    print("Consistency with Stage-A decoupled limit: CONSISTENT")
    print("STATUS: PARTIAL_PROGRESS_FRAME_SECTOR_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
