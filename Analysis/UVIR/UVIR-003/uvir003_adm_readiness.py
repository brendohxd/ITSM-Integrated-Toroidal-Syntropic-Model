#!/usr/bin/env python3
"""UVIR-003 Stage B: readiness audit for the scalar ADM reduction.

Checks whether the declared Minkowski, finite-density condensate, constant
aether and constant-force background is an on-shell background of the
declared action.  It also derives the coefficient map required when the
Einstein-Hilbert and aether terms carry independent mass scales.

This is a prerequisite audit.  It does not eliminate the scalar constraints.
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
        help="Directory for the machine-readable readiness summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.simplify(expression)
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Homogeneous finite-density condensate background.
    # ------------------------------------------------------------------
    s, mu, m2, lam4, lam6, cutoff = sp.symbols(
        "s mu m2 lambda4 lambda6 Lambda", positive=True
    )
    potential = (
        sp.Rational(1, 2) * m2 * s
        + sp.Rational(1, 8) * lam4 * s**2
        + lam6 * s**3 / (24 * cutoff**2)
    )
    pressure = sp.simplify(sp.Rational(1, 2) * s * mu**2 - potential)
    energy_density = sp.simplify(sp.Rational(1, 2) * s * mu**2 + potential)
    enthalpy = sp.simplify(energy_density + pressure)
    require_zero("finite-density enthalpy", enthalpy - s * mu**2)

    branch_equation = sp.simplify(
        mu**2 - m2 - lam4 * s / 2 - lam6 * s**2 / (4 * cutoff**2)
    )
    pressure_on_shell = sp.simplify(
        pressure.subs(mu**2, m2 + lam4 * s / 2 + lam6 * s**2 / (4 * cutoff**2))
    )
    expected_pressure_on_shell = (
        lam4 * s**2 / 8 + lam6 * s**3 / (12 * cutoff**2)
    )
    require_zero(
        "on-shell condensate pressure",
        pressure_on_shell - expected_pressure_on_shell,
    )

    # A constant vacuum-energy counterterm shifts rho and p oppositely.  It
    # cannot cancel their sum, so flat space with nonzero s and mu remains
    # off shell even after arbitrary constant subtraction.
    vacuum_energy = sp.symbols("Lambda_vac", real=True)
    total_energy_with_constant = energy_density + vacuum_energy
    total_pressure_with_constant = pressure - vacuum_energy
    require_zero(
        "constant counterterm leaves enthalpy unchanged",
        total_energy_with_constant
        + total_pressure_with_constant
        - s * mu**2,
    )

    # Any support sector that makes Minkowski an exact solution must cancel
    # both rho and p.  It therefore has non-vacuum enthalpy and cannot be
    # omitted from the scalar lapse/shift constraints without an explicit
    # rigid/external approximation.
    support_rho = -energy_density
    support_pressure = -pressure
    support_enthalpy = sp.simplify(support_rho + support_pressure)
    require_zero(
        "required support-sector enthalpy",
        support_enthalpy + s * mu**2,
    )

    # ------------------------------------------------------------------
    # 2. Aether normalization map.
    #
    # EJM factor the aether operators with the same 1/(16 pi G)=M_P^2/2
    # prefactor as R.  The ITSM action instead writes M_U^2/2.  Therefore
    # the dimensionless coefficients entering EJM's exact speeds are
    # alpha_i=(M_U^2/M_P^2)c_i, not bare c_i unless M_U=M_P.
    # ------------------------------------------------------------------
    ratio = sp.symbols("r_U", positive=True)
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    a1, a2, a3, a4 = [sp.simplify(ratio * c) for c in (c1, c2, c3, c4)]
    a13 = sp.simplify(a1 + a3)
    a14 = sp.simplify(a1 + a4)
    a123 = sp.simplify(a1 + a2 + a3)

    tensor_speed_sq = sp.simplify(1 / (1 - a13))
    vector_speed_sq = sp.simplify(
        (a1 - a1**2 / 2 + a3**2 / 2) / (a14 * (1 - a13))
    )
    scalar_speed_sq = sp.simplify(
        a123
        * (2 - a14)
        / (a14 * (1 - a13) * (2 + a13 + 3 * a2))
    )

    expected_vector_decoupled = sp.simplify(c1 / (c1 + c4))
    expected_scalar_decoupled = sp.simplify(
        (c1 + c2 + c3) / (c1 + c4)
    )
    vector_weak_gravity = sp.simplify(
        sp.limit(vector_speed_sq, ratio, 0, dir="+")
    )
    scalar_weak_gravity = sp.simplify(
        sp.limit(scalar_speed_sq, ratio, 0, dir="+")
    )
    require_zero(
        "normalized vector weak-coupling limit",
        vector_weak_gravity - expected_vector_decoupled,
    )
    require_zero(
        "normalized scalar weak-coupling limit",
        scalar_weak_gravity - expected_scalar_decoupled,
    )
    require_zero(
        "tensor weak-coupling limit",
        sp.limit(tensor_speed_sq, ratio, 0, dir="+") - 1,
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_SCALAR_ADM_READINESS",
        "calculation_status": "PASS",
        "adm_reduction_status": (
            "BLOCKED_PENDING_ON_SHELL_BACKGROUND_COMPLETION"
        ),
        "declared_background": {
            "metric": "Minkowski",
            "condensate": "Phi=(rho0/sqrt(2))*exp(i*mu*t), s=rho0^2>0",
            "aether": "U^mu=(1,0,0,0)",
            "force": "psi_bar=constant",
        },
        "condensate": {
            "branch_equation_zero": str(branch_equation),
            "pressure": str(pressure),
            "energy_density": str(energy_density),
            "enthalpy": str(enthalpy),
            "on_shell_pressure": str(pressure_on_shell),
            "minkowski_obstruction": (
                "rho_phi+p_phi=s*mu**2>0, so no constant vacuum-energy "
                "counterterm can set both rho_total and p_total to zero."
            ),
        },
        "required_background_completion": {
            "support_energy_density": str(support_rho),
            "support_pressure": str(support_pressure),
            "support_enthalpy": str(support_enthalpy),
            "constraint_requirement": (
                "Declare the reservoir/driver action or a controlled rigid "
                "support approximation and include its scalar perturbations "
                "in the lapse and shift constraints."
            ),
        },
        "aether_normalization": {
            "ratio": "r_U=M_U**2/M_P**2",
            "published_coefficients": "alpha_i=r_U*c_i",
            "bare_identity_valid_only_if": "M_U=M_P",
            "spin_2_speed_squared": str(tensor_speed_sq),
            "spin_1_speed_squared": str(vector_speed_sq),
            "spin_0_speed_squared": str(scalar_speed_sq),
            "weak_coupling_vector": str(vector_weak_gravity),
            "weak_coupling_scalar": str(scalar_weak_gravity),
        },
        "safe_existing_result": (
            "The zero-gradient force block still factorizes at quadratic "
            "order; this readiness obstruction concerns the remaining "
            "metric-aether-condensate block."
        ),
        "next_required_inputs": [
            "an on-shell background completion including support-sector stress",
            "the support sector's quadratic scalar response or an explicit controlled rigidity limit",
            "a declared value or retained symbolic ratio r_U=M_U^2/M_P^2",
            "a declared cosmological or subhorizon background for the low-k audit",
        ],
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
    }

    output_path = args.output_dir / "uvir003_adm_readiness_summary.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 scalar ADM readiness identities: VERIFIED")
    print("Declared Minkowski finite-density background: OFF_SHELL")
    print("Aether normalization: alpha_i=(M_U^2/M_P^2)*c_i")
    print("Scalar ADM reduction: BLOCKED_PENDING_ON_SHELL_BACKGROUND_COMPLETION")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_READINESS_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
