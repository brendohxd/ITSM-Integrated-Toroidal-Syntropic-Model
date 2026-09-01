#!/usr/bin/env python3
"""UVIR-003 Stage B: bounded Einstein-aether Stueckelberg cubic audit.

Derives the longitudinal, one-dimensional, flat-metric decoupling-limit
quadratic and cubic Lagrangians for a hypersurface-orthogonal aether,

    U_mu = -d_mu(t + pi) / sqrt[-d(t + pi)^2].

This is a controlled vertex-basis calculation.  It is not the full
cosmological cubic ADM reduction: non-collinear momentum triads, metric
constraints, background evolution and matter mixing are deliberately absent.
Consequently the script reports canonical quadratic normalization and cubic
coefficients, but refuses to assign a physical strong-coupling scale.
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
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Verified representative FRW summary used for numerical values.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def symbolic_vertex_basis() -> dict[str, object]:
    c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4", real=True)
    pi_t, pi_x = sp.symbols("pi_t pi_x", real=True)
    pi_tt, pi_tx, pi_xx = sp.symbols("pi_tt pi_tx pi_xx", real=True)
    epsilon = sp.symbols("epsilon", real=True)

    c14 = sp.expand(c1 + c4)
    c123 = sp.expand(c1 + c2 + c3)

    # Expand the normalized contravariant aether to second field order.
    # That is sufficient because each invariant is quadratic in d_mu U^nu.
    metric = sp.diag(-1, 1)
    u_contravariant = sp.Matrix(
        [
            1 + epsilon**2 * pi_x**2 / 2,
            -epsilon * pi_x + epsilon**2 * pi_t * pi_x,
        ]
    )
    d_u = sp.Matrix(
        [
            [
                epsilon**2 * pi_x * pi_tx,
                -epsilon * pi_tx
                + epsilon**2 * (pi_tt * pi_x + pi_t * pi_tx),
            ],
            [
                epsilon**2 * pi_x * pi_xx,
                -epsilon * pi_xx
                + epsilon**2 * (pi_tx * pi_x + pi_t * pi_xx),
            ],
        ]
    )

    invariant_1 = sp.expand(
        sum(
            metric[a, a] * metric[m, m] * d_u[a, m] ** 2
            for a in range(2)
            for m in range(2)
        )
    )
    divergence = d_u[0, 0] + d_u[1, 1]
    invariant_2 = sp.expand(divergence**2)
    invariant_3 = sp.expand(
        sum(d_u[a, b] * d_u[b, a] for a in range(2) for b in range(2))
    )
    invariant_4 = sp.expand(
        sum(
            u_contravariant[a]
            * u_contravariant[b]
            * metric[m, m]
            * d_u[a, m]
            * d_u[b, m]
            for a in range(2)
            for b in range(2)
            for m in range(2)
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

    expected_quadratic = sp.expand(
        sp.Rational(1, 2) * (c14 * pi_tx**2 - c123 * pi_xx**2)
    )
    expected_cubic = sp.expand(
        -c14 * pi_t * pi_tx**2
        + c123 * pi_t * pi_xx**2
        - c14 * pi_tt * pi_tx * pi_x
        + (2 * c123 - c14) * pi_tx * pi_x * pi_xx
    )
    require(
        "derived quadratic Lagrangian",
        sp.simplify(quadratic - expected_quadratic) == 0,
    )
    require(
        "derived cubic Lagrangian",
        sp.simplify(cubic - expected_cubic) == 0,
    )

    require(
        "quadratic temporal coefficient",
        sp.expand(quadratic).coeff(pi_tx, 2) == c14 / 2,
    )
    require(
        "quadratic spatial coefficient",
        sp.expand(quadratic).coeff(pi_xx, 2) == -c123 / 2,
    )
    require(
        "cubic pi_t pi_tx^2 coefficient",
        sp.expand(cubic).coeff(pi_t, 1).coeff(pi_tx, 2) == -c14,
    )
    require(
        "cubic pi_t pi_xx^2 coefficient",
        sp.expand(cubic).coeff(pi_t, 1).coeff(pi_xx, 2) == c123,
    )
    require(
        "cubic pi_tt pi_tx pi_x coefficient",
        sp.expand(cubic).coeff(pi_tt, 1).coeff(pi_tx, 1).coeff(pi_x, 1)
        == -c14,
    )
    require(
        "cubic pi_tx pi_x pi_xx coefficient",
        sp.expand(cubic).coeff(pi_tx, 1).coeff(pi_x, 1).coeff(pi_xx, 1)
        == 2 * c123 - c14,
    )

    return {
        "quadratic": quadratic,
        "cubic": cubic,
        "c14": c14,
        "c123": c123,
        "aether_invariant_convention": (
            "-(M_U^2/2)*(c1*I1+c2*I2+c3*I3-c4*I4)"
        ),
        "symbols": {
            "c1": c1,
            "c2": c2,
            "c3": c3,
            "c4": c4,
        },
    }
def representative_values(path: Path) -> dict[str, float]:
    with path.open(encoding="utf-8") as handle:
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
    require("positive c14", values["c14"] > 0)
    require("positive c123", values["c123"] > 0)
    return values


def build_summary(
    symbolic: dict[str, object],
    values: dict[str, float],
) -> dict[str, object]:
    c14 = values["c14"]
    c123 = values["c123"]
    m_u = values["M_U"]
    coefficients = {
        "pi_t_pi_tx_squared": -c14,
        "pi_t_pi_xx_squared": c123,
        "pi_tt_pi_tx_pi_x": -c14,
        "pi_tx_pi_x_pi_xx": 2 * c123 - c14,
    }

    # chi_k = M_U*sqrt(c14)*|k|*pi_k canonically normalizes the
    # longitudinal quadratic kinetic term for each nonzero Fourier mode.
    canonical_prefactor = m_u * c14**0.5
    speed_squared = c123 / c14

    return {
        "stage": "B_AETHER_STUECKELBERG_CUBIC_BOUNDED",
        "calculation_status": "PASS_BOUNDED_VERTEX_BASIS",
        "scope": {
            "geometry": "FLAT_METRIC_DECOUPLING_LIMIT",
            "aether": "HYPERSURFACE_ORTHOGONAL",
            "profile": "ONE_DIMENSIONAL_LONGITUDINAL",
            "order": "CUBIC_IN_PI",
        },
        "symbolic_result": {
            "overall_factor": "M_U^2",
            "invariant_convention": symbolic["aether_invariant_convention"],
            "quadratic_lagrangian": str(symbolic["quadratic"]),
            "cubic_lagrangian": str(symbolic["cubic"]),
            "surviving_combinations": ["c14=c1+c4", "c123=c1+c2+c3"],
        },
        "representative_branch": {
            "parameters": values,
            "scalar_speed_squared": speed_squared,
            "canonical_fourier_mode": (
                "chi_k=M_U*sqrt(c14)*abs(k)*pi_k, for k!=0"
            ),
            "canonical_prefactor": canonical_prefactor,
            "dimensionless_cubic_coefficients_before_canonicalization": (
                coefficients
            ),
        },
        "interpretation": {
            "vertex_basis_status": (
                "DERIVED_IN_ONE_DIMENSIONAL_FLAT_DECOUPLING_LIMIT"
            ),
            "quadratic_canonical_mode_status": "IDENTIFIED_FOR_NONZERO_K",
            "physical_strong_coupling_scale_status": "NOT_YET_DERIVED",
            "naive_low_q_cutoff_status": "REJECTED_AS_GAUGE_NORMALIZATION",
            "missing_for_physical_scale": [
                "FULL_COSMOLOGICAL_CUBIC_VERTEX_ON_FIRST_ORDER_CONSTRAINTS",
                "EVOLVING_FRW_BACKGROUND_TERMS",
                "CONDENSATE_AND_METRIC_MODE_MIXING",
                "PHYSICAL_EIGENMODE_PROJECTION",
                "QUARTIC_CONTACT_AND_2_TO_2_AMPLITUDE",
            ],
        },
        "gate_status": {
            "UVIR-003": "IN_PROGRESS",
            "MAT-001": "BLOCKED",
        },
    }


def main() -> None:
    args = parse_args()
    symbolic = symbolic_vertex_basis()
    values = representative_values(args.frw_summary)
    summary = build_summary(symbolic, values)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (
        args.output_dir / "uvir003_aether_stueckelberg_cubic_summary.json"
    )
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 bounded Stueckelberg cubic vertex basis: VERIFIED")
    print(
        "Longitudinal scalar speed squared: "
        f"{summary['representative_branch']['scalar_speed_squared']:.12g}"
    )
    print("Physical strong-coupling scale: NOT_YET_DERIVED")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_BOUNDED_VERTEX_BASIS")


if __name__ == "__main__":
    main()
