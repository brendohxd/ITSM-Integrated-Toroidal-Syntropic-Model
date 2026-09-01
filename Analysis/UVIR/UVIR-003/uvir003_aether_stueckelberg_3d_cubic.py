#!/usr/bin/env python3
"""UVIR-003 Stage B: three-dimensional khronon cubic and NDA audit.

Expands the normalized hypersurface-orthogonal Einstein-aether field in three
spatial dimensions through cubic order on a flat decoupling background.  It
also proves the perturbative constraint-elimination identity relevant to a
future cosmological cubic reduction and audits what interaction scale can, and
cannot, be inferred from the resulting canonical operator basis.

The operator-by-operator NDA values are basis-dependent diagnostics, not a
physical unitarity cutoff.  A physical scale requires the complete constrained
cosmological vertex and an on-shell 2-to-2 amplitude (including exchange and
quartic contact terms).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Verified representative FRW summary.",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
        help="Verified representative FRW trajectory.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.factor(sp.expand(expression))
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def symbolic_three_dimensional_vertex() -> dict[str, object]:
    epsilon = sp.symbols("epsilon", real=True)
    c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4", real=True)
    pi_t, pi_tt = sp.symbols("pi_t pi_tt", real=True)
    p = sp.Matrix(sp.symbols("p_1:4", real=True))
    v = sp.Matrix(sp.symbols("v_1:4", real=True))
    h11, h22, h33, h12, h13, h23 = sp.symbols(
        "H_11 H_22 H_33 H_12 H_13 H_23",
        real=True,
    )
    hessian = sp.Matrix(
        [
            [h11, h12, h13],
            [h12, h22, h23],
            [h13, h23, h33],
        ]
    )
    metric = sp.diag(-1, 1, 1, 1)

    p_squared = (p.T * p)[0]
    u_contravariant = sp.Matrix(
        [1 + epsilon**2 * p_squared / 2]
        + [
            -epsilon * p[index] + epsilon**2 * pi_t * p[index]
            for index in range(3)
        ]
    )

    d_u = sp.zeros(4, 4)
    d_u[0, 0] = epsilon**2 * (p.T * v)[0]
    for spatial_derivative in range(3):
        d_u[spatial_derivative + 1, 0] = epsilon**2 * (
            p.T * hessian.row(spatial_derivative).T
        )[0]
    for component in range(3):
        d_u[0, component + 1] = (
            -epsilon * v[component]
            + epsilon**2
            * (pi_tt * p[component] + pi_t * v[component])
        )
        for spatial_derivative in range(3):
            d_u[spatial_derivative + 1, component + 1] = (
                -epsilon * hessian[spatial_derivative, component]
                + epsilon**2
                * (
                    v[spatial_derivative] * p[component]
                    + pi_t * hessian[spatial_derivative, component]
                )
            )

    invariant_1 = sp.expand(
        sum(
            metric[a, a] * metric[m, m] * d_u[a, m] ** 2
            for a in range(4)
            for m in range(4)
        )
    )
    divergence = sum(d_u[index, index] for index in range(4))
    invariant_2 = sp.expand(divergence**2)
    invariant_3 = sp.expand(
        sum(d_u[a, b] * d_u[b, a] for a in range(4) for b in range(4))
    )
    invariant_4 = sp.expand(
        sum(
            u_contravariant[a]
            * u_contravariant[b]
            * metric[m, m]
            * d_u[a, m]
            * d_u[b, m]
            for a in range(4)
            for b in range(4)
            for m in range(4)
        )
    )
    lagrangian = sp.expand(
        -sp.Rational(1, 2)
        * (
            c1 * invariant_1
            + c2 * invariant_2
            + c3 * invariant_3
            - c4 * invariant_4
        )
    )
    quadratic = sp.expand(lagrangian).coeff(epsilon, 2)
    cubic = sp.expand(lagrangian).coeff(epsilon, 3)

    v_squared = (v.T * v)[0]
    hessian_squared = sp.trace(hessian.T * hessian)
    hessian_trace = sp.trace(hessian)
    p_dot_v = (p.T * v)[0]
    p_hessian_v = (p.T * hessian * v)[0]
    c14 = c1 + c4

    expected_quadratic = sp.expand(
        (
            c14 * v_squared
            - (c1 + c3) * hessian_squared
            - c2 * hessian_trace**2
        )
        / 2
    )
    expected_cubic = sp.expand(
        -c14 * (pi_tt * p_dot_v + pi_t * v_squared)
        + (c1 + 2 * c3 - c4) * p_hessian_v
        + 2 * c2 * hessian_trace * p_dot_v
        + (c1 + c3) * pi_t * hessian_squared
        + c2 * pi_t * hessian_trace**2
    )
    require_zero("three-dimensional quadratic vertex", quadratic - expected_quadratic)
    require_zero("three-dimensional cubic vertex", cubic - expected_cubic)

    # Collinear reduction must reproduce the independently derived 1D basis.
    replacements = {
        p[1]: 0,
        p[2]: 0,
        v[1]: 0,
        v[2]: 0,
        h22: 0,
        h33: 0,
        h12: 0,
        h13: 0,
        h23: 0,
    }
    collinear = sp.factor(cubic.subs(replacements))
    c123 = c1 + c2 + c3
    expected_collinear = sp.expand(
        -c14 * pi_t * v[0] ** 2
        + c123 * pi_t * h11**2
        - c14 * pi_tt * v[0] * p[0]
        + (2 * c123 - c14) * v[0] * p[0] * h11
    )
    require_zero("one-dimensional reduction", collinear - expected_collinear)

    return {
        "quadratic": expected_quadratic,
        "cubic": expected_cubic,
        "collinear_cubic": expected_collinear,
        "compact_notation": {
            "p_i": "partial_i pi",
            "v_i": "partial_i dot(pi)",
            "H_ij": "partial_i partial_j pi",
            "H": "trace(H_ij)=Delta pi",
        },
    }


def constraint_elimination_identity() -> dict[str, str]:
    c, j, z1, z2, l3 = sp.symbols("C J z_1 z_2 L_3", nonzero=True)
    quadratic_at_shifted_constraint = sp.expand(
        c * (z1 + z2) ** 2 / 2 + j * (z1 + z2)
    )
    stationary = sp.expand(quadratic_at_shifted_constraint.subs(z1, -j / c))
    expected = sp.expand(-j**2 / (2 * c) + c * z2**2 / 2)
    require_zero(
        "second-order constraint cancellation",
        stationary - expected,
    )
    require(
        "second-order correction starts quartic",
        sp.Poly(expected, z2).coeff_monomial(z2) == 0,
    )
    return {
        "identity": (
            "L2[z1+z2]=L2[z1]+(C*z1+J)*z2+C*z2^2/2"
        ),
        "stationary_solution": "z1=-C^{-1}J",
        "cubic_consequence": (
            "L_reduced^(3)=L3[x,z1]; explicit z2 is unnecessary"
        ),
        "scope": (
            "algebraic constraints with an invertible quadratic constraint matrix"
        ),
        "placeholder": str(l3),
    }


def representative_inputs(
    summary_path: Path,
    trajectory_path: Path,
) -> tuple[dict[str, float], list[float]]:
    with summary_path.open(encoding="utf-8") as handle:
        frw = json.load(handle)
    require("verified FRW status", frw["calculation_status"] == "PASS")
    branch = frw["representative_branch"]
    parameters = branch["parameters"]
    derived = branch["derived_parameters"]
    values = {
        "M_U": float(parameters["M_U"]),
        "c1": float(parameters["c1"]),
        "c2": float(parameters["c2"]),
        "c3": float(parameters["c3"]),
        "c4": float(parameters["c4"]),
        "c14": float(derived["c14"]),
        "c123": float(derived["c123"]),
    }
    with trajectory_path.open(newline="", encoding="utf-8") as handle:
        hubble_values = [float(row["H"]) for row in csv.DictReader(handle)]
    require("nonempty FRW trajectory", bool(hubble_values))
    require("positive c14", values["c14"] > 0)
    require("positive c123", values["c123"] > 0)
    return values, hubble_values


def nda_diagnostics(
    values: dict[str, float],
    hubble_values: list[float],
) -> dict[str, object]:
    c1 = values["c1"]
    c2 = values["c2"]
    c3 = values["c3"]
    c4 = values["c4"]
    c14 = values["c14"]
    c123 = values["c123"]
    m_u = values["M_U"]
    sound_speed = math.sqrt(c123 / c14)
    canonical_denominator = m_u * c14 ** 1.5

    coefficient_bounds = {
        "pi_tt_p_dot_v": abs(c14) * sound_speed**3,
        "pi_t_v_squared": abs(c14) * sound_speed**3,
        "p_H_v": abs(c1 + 2 * c3 - c4) * sound_speed,
        "traceH_p_dot_v": abs(2 * c2) * sound_speed,
        "pi_t_Hij_squared": abs(c1 + c3) * sound_speed,
        "pi_t_traceH_squared": abs(c2) * sound_speed,
    }
    require(
        "nonzero cubic coefficient",
        max(coefficient_bounds.values()) > 0,
    )
    momentum_scales = {
        name: canonical_denominator / coefficient
        for name, coefficient in coefficient_bounds.items()
        if coefficient > 0
    }
    basis_nda_momentum = min(momentum_scales.values())
    basis_nda_energy = sound_speed * basis_nda_momentum
    minimum_hubble = min(hubble_values)
    maximum_hubble = max(hubble_values)

    return {
        "canonical_mode": "chi_k=M_U*sqrt(c14)*abs(k)*pi_k",
        "sound_speed": sound_speed,
        "canonical_cubic_denominator": canonical_denominator,
        "derivative_counting": (
            "abs(omega)~c_s*abs(k); each canonical cubic operator scales "
            "as coefficient*k^2*chi^3/[M_U*c14^(3/2)]"
        ),
        "operator_coefficient_bounds": coefficient_bounds,
        "operator_momentum_scales": momentum_scales,
        "basis_dependent_nda_momentum": basis_nda_momentum,
        "basis_dependent_nda_energy": basis_nda_energy,
        "representative_hubble_range": {
            "minimum": minimum_hubble,
            "maximum": maximum_hubble,
        },
        "basis_nda_momentum_over_H": {
            "minimum": basis_nda_momentum / maximum_hubble,
            "maximum": basis_nda_momentum / minimum_hubble,
        },
        "status": "DIAGNOSTIC_ONLY_NOT_PHYSICAL_CUTOFF",
        "limitations": [
            "OPERATOR_BASIS_DEPENDENT_UNDER_FIELD_REDEFINITIONS",
            "NO_METRIC_OR_CONDENSATE_MIXING",
            "NO_EXCHANGE_OR_QUARTIC_CONTACT_AMPLITUDE",
            "REPRESENTATIVE_PARAMETERS_ARE_DIMENSIONLESS_AND_UNSELECTED",
        ],
    }


def build_summary(
    symbolic: dict[str, object],
    constraint_identity: dict[str, str],
    values: dict[str, float],
    nda: dict[str, object],
) -> dict[str, object]:
    return {
        "stage": "B_AETHER_STUECKELBERG_3D_CUBIC",
        "calculation_status": "PASS_3D_CUBIC_AND_CONSTRAINT_IDENTITY",
        "scope": {
            "geometry": "FLAT_METRIC_DECOUPLING_LIMIT",
            "spatial_dimension": 3,
            "aether": "HYPERSURFACE_ORTHOGONAL",
            "order": "CUBIC_IN_PI",
        },
        "symbolic_result": {
            "overall_factor": "M_U^2",
            "quadratic_lagrangian": str(symbolic["quadratic"]),
            "cubic_lagrangian": str(symbolic["cubic"]),
            "collinear_reduction": str(symbolic["collinear_cubic"]),
            "compact_notation": symbolic["compact_notation"],
        },
        "constraint_elimination": constraint_identity,
        "three_point_kinematics": {
            "linear_dispersion": "abs(omega)=c_s*abs(k)",
            "momentum_conservation": "k1+k2+k3=0",
            "on_shell_noncollinear_three_point": "KINEMATICALLY_FORBIDDEN",
            "reason": (
                "Energy conservation requires one momentum magnitude to equal "
                "the sum of the other two; equality in the triangle inequality "
                "forces collinearity."
            ),
            "physical_scale_consequence": (
                "A noncollinear on-shell cubic amplitude cannot define the "
                "cutoff. Use the complete 2-to-2 amplitude."
            ),
        },
        "representative_branch": {
            "parameters": values,
            "nda_diagnostic": nda,
        },
        "interpretation": {
            "three_dimensional_vertex_status": "DERIVED_AND_VERIFIED",
            "second_order_constraint_solution_status": (
                "NOT_REQUIRED_EXPLICITLY_FOR_REDUCED_CUBIC_ACTION"
            ),
            "basis_nda_status": "COMPUTED_DIAGNOSTIC_ONLY",
            "physical_strong_coupling_scale_status": "NOT_YET_DERIVED",
            "next_required_calculation": [
                "FULL_COSMOLOGICAL_CUBIC_VERTEX_WITH_FIRST_ORDER_CONSTRAINTS",
                "COMPLETE_PHYSICAL_SCALAR_EIGENMODE_PROJECTION",
                "FULL_COSMOLOGICAL_QUARTIC_WITH_SECOND_ORDER_CONSTRAINT_SCHUR_COMPLEMENT",
                "GAUGE_REGULAR_ON_SHELL_2_TO_2_AMPLITUDE",
            ],
        },
        "gate_status": {
            "UVIR-003": "IN_PROGRESS",
            "MAT-001": "BLOCKED",
        },
    }


def main() -> None:
    args = parse_args()
    symbolic = symbolic_three_dimensional_vertex()
    constraint_identity = constraint_elimination_identity()
    values, hubble_values = representative_inputs(
        args.frw_summary,
        args.frw_trajectory,
    )
    nda = nda_diagnostics(values, hubble_values)
    summary = build_summary(symbolic, constraint_identity, values, nda)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (
        args.output_dir / "uvir003_aether_stueckelberg_3d_cubic_summary.json"
    )
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 three-dimensional khronon cubic vertex: VERIFIED")
    print("Reduced cubic second-order constraint correction: CANCELS")
    print("Noncollinear on-shell three-point amplitude: KINEMATICALLY_FORBIDDEN")
    print(
        "Representative basis-dependent NDA momentum: "
        f"{nda['basis_dependent_nda_momentum']:.12g}"
    )
    print("Physical strong-coupling scale: NOT_YET_DERIVED")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_3D_CUBIC_AND_CONSTRAINT_IDENTITY")


if __name__ == "__main__":
    main()
