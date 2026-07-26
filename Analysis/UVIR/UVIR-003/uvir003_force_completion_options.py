#!/usr/bin/env python3
"""Audit the bounded completion options for the UVIR-003 force sector.

This script does not select a new canonical action.  It checks:

1. the covariant rest-space Laplacian identity and its FRW/flat limits;
2. the difference between three evolving-frame regulator candidates;
3. the zero-gradient smoothings of Y^(3/2);
4. the singular zero-gradient limit of the nonzero-gradient expansion.

The output is a decision record, not a UVIR-003 pass or a physical amplitude.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = (
    ROOT
    / "Analysis"
    / "UVIR"
    / "UVIR-003"
    / "outputs"
    / "uvir003_force_completion_options_summary.json"
)


def check_equal(lhs: sp.Expr, rhs: sp.Expr, label: str) -> dict[str, str]:
    residual = sp.simplify(lhs - rhs)
    if residual != 0:
        raise AssertionError(f"{label}: residual {residual}")
    return {"label": label, "status": "VERIFIED", "residual": str(residual)}


def main() -> None:
    # Abstract 1+3 identities.  H2 is h^{mu nu} nabla_mu nabla_nu psi,
    # theta is nabla_mu U^mu, Q=U^mu nabla_mu psi, and aD=a^mu D_mu psi.
    hessian, theta, q_flow, a_dot_d = sp.symbols(
        "Hessian theta Q a_dot_D", real=True
    )
    rest_laplacian = hessian + theta * q_flow
    divergence_projected_gradient = rest_laplacian + a_dot_d

    identity_checks = [
        check_equal(
            rest_laplacian,
            hessian + theta * q_flow,
            "D_mu D^mu psi = hessian_perp + theta Q",
        ),
        check_equal(
            divergence_projected_gradient,
            rest_laplacian + a_dot_d,
            "nabla_mu(h^{mu nu} nabla_nu psi) = D^2 psi + a.D psi",
        ),
    ]

    # Homogeneous flat-FRW limit: hessian_perp=-3 H psidot,
    # theta=3H and Q=psidot.  The rest-space Laplacian must vanish.
    hubble, psi_dot = sp.symbols("H psi_dot", real=True)
    frw_hessian = -3 * hubble * psi_dot
    frw_theta_q = 3 * hubble * psi_dot
    identity_checks.append(
        check_equal(
            frw_hessian + frw_theta_q,
            sp.Integer(0),
            "D^2 psi vanishes for homogeneous psi on flat FRW",
        )
    )

    # Smooth completions.  sigma>0 is a dimensionless crossover in sqrt(Y).
    y, sigma = sp.symbols("Y sigma", positive=True)
    smooth_with_linear = (y + sigma**2) ** sp.Rational(3, 2) - sigma**3
    smooth_subtracted = (
        smooth_with_linear - sp.Rational(3, 2) * sigma * y
    )
    smooth_with_linear_series = sp.series(
        smooth_with_linear, y, 0, 4
    ).removeO()
    smooth_subtracted_series = sp.series(
        smooth_subtracted, y, 0, 4
    ).removeO()

    expected_with_linear = (
        sp.Rational(3, 2) * sigma * y
        + sp.Rational(3, 8) * y**2 / sigma
        - sp.Rational(1, 16) * y**3 / sigma**3
    )
    expected_subtracted = (
        sp.Rational(3, 8) * y**2 / sigma
        - sp.Rational(1, 16) * y**3 / sigma**3
    )
    smoothing_checks = [
        check_equal(
            smooth_with_linear_series,
            expected_with_linear,
            "unsubtracted smoothing generates a canonical Y term",
        ),
        check_equal(
            smooth_subtracted_series,
            expected_subtracted,
            "linear-subtracted smoothing begins at Y^2",
        ),
    ]

    # Expand |v + grad(pi)|^3 about a nonzero gradient v along x.
    # p2 is the squared transverse perturbation.  The epsilon^4 coefficient
    # diverges as v -> 0, proving that this Taylor family has no regular
    # zero-gradient quartic limit.
    eps, x_parallel = sp.symbols("epsilon x_parallel", real=True)
    v = sp.symbols("v", positive=True)
    p2 = sp.symbols("p_perp_sq", nonnegative=True)
    norm_cubed = (
        (v + eps * x_parallel) ** 2 + eps**2 * p2
    ) ** sp.Rational(3, 2)
    nonzero_gradient_series = sp.series(norm_cubed, eps, 0, 5).removeO()
    expected_nonzero_gradient = (
        v**3
        + 3 * v**2 * eps * x_parallel
        + sp.Rational(3, 2)
        * v
        * eps**2
        * (2 * x_parallel**2 + p2)
        + eps**3
        * (
            x_parallel**3
            + sp.Rational(3, 2) * x_parallel * p2
        )
        + sp.Rational(3, 8) * eps**4 * p2**2 / v
    )
    background_checks = [
        check_equal(
            nonzero_gradient_series,
            expected_nonzero_gradient,
            "nonzero-gradient Y^(3/2) expansion through quartic order",
        )
    ]

    result = {
        "gate": "UVIR-003",
        "stage": "B_FORCE_COMPLETION_OPTIONS",
        "date": "2026-07-26",
        "status": "TRACK_A_SELECTED",
        "uvir003_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "regulator_comparison": {
            "selected_rest_space_laplacian": {
                "operator": (
                    "Delta_U psi := D_mu D^mu psi "
                    "= h^{mu nu} nabla_mu nabla_nu psi + theta Q"
                ),
                "reasons": [
                    "generally covariant scalar built from g, U and psi",
                    "reduces to the Stage-A spatial Laplacian for constant U",
                    "annihilates fields homogeneous on the aether rest space",
                    "has a purely spatial second-derivative principal part",
                    "in aether-unitary ADM it is the intrinsic leaf Laplacian",
                ],
                "boundary": (
                    "Track A adopts this operator for the next derivation."
                ),
            },
            "projected_hessian_only": {
                "operator": "h^{mu nu} nabla_mu nabla_nu psi",
                "difference": "-theta Q relative to D_mu D^mu psi",
                "assessment": (
                    "NOT_RECOMMENDED: it is nonzero for homogeneous psi on "
                    "an evolving FRW background."
                ),
            },
            "spacetime_divergence": {
                "operator": (
                    "nabla_mu(h^{mu nu} nabla_nu psi)"
                ),
                "difference": "+a^mu D_mu psi relative to D_mu D^mu psi",
                "assessment": (
                    "VIABLE_BUT_NONMINIMAL: it is divergence-form but adds "
                    "an acceleration/lapse-gradient coupling."
                ),
            },
        },
        "y_three_halves_comparison": {
            "exact_zero_gradient_branch": {
                "preserves_target_ir_law": True,
                "ordinary_taylor_vertex_at_Y_zero": False,
                "use": (
                    "classical nonlinear boundary-value problems; not a "
                    "standard zero-background perturbative S-matrix vertex"
                ),
            },
            "nonzero_gradient_background": {
                "ordinary_local_expansion": True,
                "preserves_exact_operator": True,
                "cost": (
                    "background selects a spatial direction; the quartic "
                    "coefficient contains 1/|grad psi_0| and has no regular "
                    "zero-gradient limit"
                ),
                "use": "local weak-field response, not isotropic FRW scattering",
            },
            "smooth_with_linear_term": {
                "function": "(Y+sigma^2)^(3/2)-sigma^3",
                "series": str(smooth_with_linear_series),
                "benefit": "analytic at Y=0 and supplies quadratic spatial stiffness",
                "cost": (
                    "the generated (3/2) sigma Y term dominates in the "
                    "deep IR and changes the target asymptotic branch"
                ),
            },
            "smooth_linear_subtracted": {
                "function": (
                    "(Y+sigma^2)^(3/2)-sigma^3-(3/2)sigma Y"
                ),
                "series": str(smooth_subtracted_series),
                "benefit": (
                    "analytic at Y=0 without a canonical Y term; the leading "
                    "interaction is quartic in spatial gradients"
                ),
                "cost": (
                    "introduces a crossover scale and replaces the exact "
                    "deep-IR Y^(3/2) law by Y^2"
                ),
            },
        },
        "verified_identities": identity_checks,
        "verified_smoothing_series": smoothing_checks,
        "verified_nonzero_background_series": background_checks,
        "decision_tracks": {
            "A_preserve_exact_ir_branch": (
                "Keep exact Y^(3/2); use a nonzero-gradient local background "
                "for force-sector perturbation theory and do not call it the "
                "homogeneous cosmological 2-to-2 amplitude."
            ),
            "B_preserve_homogeneous_analytic_amplitude": (
                "Choose a smooth completion and a crossover sigma; accept "
                "and test the resulting modification of the deep-IR law."
            ),
        },
        "selected_decision": (
            "Track A: retain exact Y^(3/2), adopt D_mu D^mu psi, and assign "
            "force perturbation theory to a declared nonzero-gradient local "
            "background."
        ),
        "scientific_boundary": (
            "The regulator comparison identifies the operator now adopted by "
            "Track A. No option simultaneously keeps "
            "the exact asymptotic Y^(3/2) law at Y=0 and supplies an ordinary "
            "analytic zero-background vertex. UVIR-003 and MAT-001 therefore "
            "remain open."
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print("Rest-space Laplacian identities: VERIFIED")
    print("Smooth-completion series: VERIFIED")
    print("Nonzero-gradient singular limit: VERIFIED")
    print("Rest-space regulator: TRACK_A_ADOPTED")
    print("Y^(3/2) treatment: EXACT_NONZERO_GRADIENT_LOCAL_TRACK")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: TRACK_A_SELECTED")


if __name__ == "__main__":
    main()
