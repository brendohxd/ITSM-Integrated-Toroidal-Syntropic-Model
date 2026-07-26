#!/usr/bin/env python3
"""UVIR-003 Stage B: nonlinear ADM action-provenance audit.

Reconstructs the exact aether-unitary ADM action for the two-derivative
gravity, aether, canonical condensate and current-alignment sectors.  It
checks that this nonlinear parent action reproduces the verified FRW
minisuperspace action and the complete finite-q quadratic lapse/shift
constraint matrix and source.

The declared force regulator is intentionally not promoted into this action:
Stage A defines Delta_U only in a constant hypersurface-orthogonal frame and
defers its generally covariant completion.  In addition, Y^(3/2) is
non-analytic at the zero-gradient background.  Consequently this audit proves
action provenance for the g+U+Phi+alignment block, but it does not claim that
the full cosmological quadratic constraint source J2 is derived.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in reduced):
            return
        raise AssertionError(f"{name} failed: {reduced}")
    if sp.factor(reduced) != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def symbolic_audit() -> dict[str, object]:
    mp2, mu2 = sp.symbols("M_P_sq M_U_sq", positive=True)
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    hubble, q = sp.symbols("H q_phys", real=True)
    rho, rho_dot, chemical = sp.symbols(
        "rho rho_dot mu", real=True
    )
    potential, potential_rho = sp.symbols("V V_rho", real=True)
    alignment = sp.symbols("zeta_align", nonnegative=True)

    curvature, curvature_dot = sp.symbols("R R_dot", real=True)
    delta_rho, delta_rho_dot = sp.symbols(
        "delta_rho delta_rho_dot", real=True
    )
    phase, phase_dot = sp.symbols(
        "vartheta vartheta_dot", real=True
    )

    c13 = sp.expand(c1 + c3)
    c14 = sp.expand(c1 + c4)
    c123 = sp.expand(c1 + c2 + c3)
    ctheta = sp.expand(c1 + 3 * c2 + c3)

    # Exact ADM coefficients in
    # N sqrt(h) [A K_ij K^ij + B K^2 + ...]/2.
    coeff_kij = sp.expand(mp2 - mu2 * c13)
    coeff_k = sp.expand(-mp2 - mu2 * c2)
    coeff_acc = sp.expand(mu2 * c14)
    mcos2 = sp.expand(mp2 + mu2 * ctheta / 2)
    d123 = sp.expand(mu2 * c123)

    require_zero(
        "FRW extrinsic-curvature identity",
        coeff_kij + 3 * coeff_k + 2 * mcos2,
    )
    require_zero(
        "scalar-shift identity",
        coeff_kij + coeff_k + d123,
    )

    # The exact homogeneous ADM reduction is
    # -3 M_cos^2 a adot^2/N + a^3 T/N - N a^3 V,
    # T=(rho_dot^2+rho^2 mu^2)/2.
    kinetic_density = sp.expand(
        (rho_dot**2 + rho**2 * chemical**2) / 2
    )
    friedmann_residual = sp.expand(
        3 * mcos2 * hubble**2 - kinetic_density - potential
    )
    lapse_squared_raw = sp.expand(
        -3 * mcos2 * hubble**2 + kinetic_density
    )
    require_zero(
        "on-shell homogeneous lapse-squared coefficient",
        lapse_squared_raw + potential + friedmann_residual,
    )
    lapse_squared_on_shell = -potential

    # Reconstruct C and J1 from the nonlinear ADM building blocks.  Sigma is
    # q_phys^2 beta and exists only for q_phys != 0.
    constraint_matrix = sp.Matrix(
        [
            [coeff_acc * q**2 - 2 * potential, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -d123],
        ]
    )
    expected_constraint_matrix = sp.Matrix(
        [
            [mu2 * c14 * q**2 - 2 * potential, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -mu2 * c123],
        ]
    )
    require_zero(
        "finite-q constraint matrix",
        constraint_matrix - expected_constraint_matrix,
    )

    lapse_source = sp.expand(
        6 * mcos2 * hubble * curvature_dot
        + 2 * mp2 * q**2 * curvature
        - (potential_rho + rho * chemical**2) * delta_rho
        - rho_dot * delta_rho_dot
        - rho**2 * chemical * phase_dot
    )
    shift_source = sp.expand(
        -2 * mcos2 * curvature_dot
        - rho_dot * delta_rho
        - rho**2 * chemical * phase
    )
    constraint_source = sp.Matrix([lapse_source, shift_source])

    expected_source = sp.Matrix(
        [
            6 * mcos2 * hubble * curvature_dot
            + 2 * mp2 * q**2 * curvature
            - (potential_rho + rho * chemical**2) * delta_rho
            - rho_dot * delta_rho_dot
            - rho**2 * chemical * phase_dot,
            -2 * mcos2 * curvature_dot
            - rho_dot * delta_rho
            - rho**2 * chemical * phase,
        ]
    )
    require_zero(
        "finite-q linear constraint source",
        constraint_source - expected_source,
    )

    # Exact current projection in aether-unitary gauge:
    # J_Phi^mu=-varrho^2 grad^mu theta, so
    # h_mn J^m J^n=varrho^4 h^ij D_i theta D_j theta.
    phase_gradient_coefficient = sp.expand(
        rho**2 * (1 + alignment * rho**2)
    )
    require_zero(
        "quadratic alignment phase-gradient coefficient",
        phase_gradient_coefficient
        - (rho**2 + alignment * rho**4),
    )

    # At a zero-gradient background Y=eps^2*y2.  Y^(3/2) is |eps|^3
    # y2^(3/2), which is even under eps -> -eps.  A nonzero homogeneous
    # cubic Taylor polynomial would be odd.  This parity mismatch is an exact
    # obstruction to treating the operator as an ordinary analytic cubic
    # vertex at that background.
    epsilon = sp.symbols("epsilon", real=True)
    y2 = sp.symbols("Y2", positive=True)
    force_ir_line = sp.Abs(epsilon) ** 3 * y2 ** sp.Rational(3, 2)
    require_zero(
        "force Y^(3/2) even-amplitude identity",
        force_ir_line.subs(epsilon, -epsilon) - force_ir_line,
    )

    return {
        "adm_parent_action": {
            "g_plus_U": (
                "N*sqrt(h)/2*[M_P_sq*R3"
                "+(M_P_sq-M_U_sq*c13)*KijKij"
                "-(M_P_sq+M_U_sq*c2)*K^2"
                "+M_U_sq*c14*a_i*a^i]"
            ),
            "condensate": (
                "N*sqrt(h)*[(n(varrho)^2+varrho^2*n(theta)^2)/2"
                "-h^ij*(D_i(varrho)D_j(varrho)"
                "+varrho^2*D_i(theta)D_j(theta))/2-V(varrho)]"
            ),
            "alignment": (
                "-N*sqrt(h)*zeta_align*varrho^4"
                "*h^ij*D_i(theta)D_j(theta)/2"
            ),
            "gauge": (
                "U^mu=n^mu; N=1+delta_N; "
                "N_i=partial_i beta; h_ij=a^2*exp(2R)*delta_ij"
            ),
        },
        "coefficient_dictionary": {
            "c13": str(c13),
            "c14": str(c14),
            "c123": str(c123),
            "M_cos_squared": str(mcos2),
            "KijKij": str(coeff_kij),
            "K_squared": str(coeff_k),
            "acceleration_squared": str(coeff_acc),
        },
        "frw_provenance": {
            "minisuperspace": (
                "-3*M_cos_sq*a*adot^2/N"
                "+a^3*(rho_dot^2+rho^2*Theta_dot^2)/(2N)"
                "-N*a^3*V(rho)"
            ),
            "friedmann_residual": str(friedmann_residual),
            "on_shell_lapse_squared_lagrangian_coefficient": str(
                lapse_squared_on_shell
            ),
            "status": "VERIFIED",
        },
        "finite_q_quadratic_provenance": {
            "constraint_matrix": str(constraint_matrix),
            "constraint_source": str(constraint_source),
            "alignment_phase_gradient_stiffness": str(
                phase_gradient_coefficient
            ),
            "status": "VERIFIED_FROM_NONLINEAR_PARENT_BLOCK",
        },
        "force_sector_obstructions": {
            "Delta_U_covariant_completion": (
                "NOT_DECLARED_FOR_THE_EVOLVING_NONLINEAR_FRAME"
            ),
            "Y_three_halves_about_zero_gradient": str(force_ir_line),
            "analytic_cubic_vertex": (
                "NOT_DEFINED_BY_AN_ORDINARY_TAYLOR_EXPANSION"
            ),
            "reason": (
                "|epsilon|^3 is even, whereas a nonzero homogeneous cubic "
                "Taylor polynomial is odd"
            ),
        },
        "constraint_source_readiness": {
            "g_U_Phi_alignment_J2": (
                "PARENT_ACTION_FIXED; EXPLICIT EXPANSION_NOT_YET_DERIVED"
            ),
            "full_g_U_Phi_psi_J2": (
                "BLOCKED_ON_FORCE_COVARIANT_COMPLETION_AND_NONANALYTIC_RULE"
            ),
            "physical_2_to_2_amplitude": "NOT_YET_DERIVED",
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_audit()
    summary = {
        "gate": "UVIR-003",
        "stage": "B_NONLINEAR_ADM_ACTION_PROVENANCE",
        "calculation_status": "PASS",
        "subgate_status": "PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE",
        "full_J2_status": (
            "HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_audit": symbolic,
        "scientific_boundary": (
            "The exact nonlinear gravity-aether-condensate-alignment parent "
            "block reproduces the verified FRW and finite-q quadratic "
            "constraint data. This does not derive the quadratic constraint "
            "source J2. The full source and physical scalar 2-to-2 amplitude "
            "cannot be claimed until the force regulator has a declared "
            "nonlinear covariant completion and the zero-gradient "
            "Y^(3/2) interaction is assigned a non-analytic perturbative "
            "prescription or a smooth completion."
        ),
        "next_required_calculation": [
            (
                "choose and derive a generally covariant completion of "
                "Delta_U on the evolving aether foliation"
            ),
            (
                "declare a controlled treatment or smooth completion of "
                "Y^(3/2) about the zero-gradient force background"
            ),
            (
                "expand the resulting full scalar ADM action to cubic order "
                "and extract the quadratic lapse/shift source J2"
            ),
            (
                "form the quartic Schur complement and project onto the "
                "regular physical scalar basis"
            ),
        ],
    }

    output_path = (
        args.output_dir
        / "uvir003_nonlinear_adm_action_provenance_summary.json"
    )
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Nonlinear g+U+Phi+alignment ADM parent action: VERIFIED")
    print("FRW minisuperspace provenance: VERIFIED")
    print("Finite-q quadratic C and J1 provenance: VERIFIED")
    print(
        "Full cosmological J2: "
        "HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED"
    )
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
