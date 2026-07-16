#!/usr/bin/env python3
"""UVIR-003 Stage-A action and decoupling-limit stability checks.

The calculation validates necessary conditions for the independently dynamical
preferred-frame and regulated force sectors.  It does not perform the full
metric/aether/condensate constraint reduction required to close UVIR-003.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the Stage-A JSON and parameter-check CSV.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    simplified = sp.simplify(expression)
    if isinstance(simplified, sp.MatrixBase):
        is_zero = simplified == sp.zeros(*simplified.shape)
    else:
        is_zero = simplified == 0
    if not is_zero:
        raise AssertionError(f"{name} failed: {simplified}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 1. Independent unit vector aligned, but not identified, with the
    #    condensate current.  Expand h_{mu nu} J^mu J^nu to second order.
    # ------------------------------------------------------------------
    eps, density = sp.symbols("epsilon n", positive=True)
    ux, uy, uz, jx, jy, jz = sp.symbols(
        "u_x u_y u_z j_x j_y j_z", real=True
    )
    u_sq = ux**2 + uy**2 + uz**2
    j_sq = jx**2 + jy**2 + jz**2
    u_dot_j = ux * jx + uy * jy + uz * jz
    u0 = sp.sqrt(1 + eps**2 * u_sq)
    current_sq = -density**2 + eps**2 * j_sq
    u_dot_current = -density * u0 + eps**2 * u_dot_j
    projected_current_sq = sp.expand(current_sq + u_dot_current**2)
    alignment_quadratic = sp.expand(
        sp.diff(projected_current_sq, eps, 2).subs(eps, 0) / 2
    )
    expected_alignment = (
        (jx - density * ux) ** 2
        + (jy - density * uy) ** 2
        + (jz - density * uz) ** 2
    )
    require_zero("alignment quadratic", alignment_quadratic - expected_alignment)

    # ------------------------------------------------------------------
    # 2. Frozen-metric Einstein-aether decoupling limit.  With the action
    #    convention in the report, the necessary coefficients are c14 for
    #    time derivatives, c1 for transverse gradients and c123 for the
    #    longitudinal gradient.
    # ------------------------------------------------------------------
    c1, c2, c3, c4, m_u, k = sp.symbols(
        "c1 c2 c3 c4 M_U k", positive=True
    )
    # Re-declare unrestricted couplings for algebraic expressions: individual
    # c_i need not all be positive even when the combinations are healthy.
    c1r, c2r, c3r, c4r = sp.symbols("c1r c2r c3r c4r", real=True)
    c14 = sp.simplify(c1r + c4r)
    c123 = sp.simplify(c1r + c2r + c3r)
    frame_kinetic = sp.simplify(m_u**2 * c14)
    frame_gradient_transverse = sp.simplify(m_u**2 * c1r)
    frame_gradient_longitudinal = sp.simplify(m_u**2 * c123)
    frame_speed_transverse_sq = sp.simplify(c1r / c14)
    frame_speed_longitudinal_sq = sp.simplify(c123 / c14)
    require_zero(
        "frame transverse dispersion",
        frame_kinetic * frame_speed_transverse_sq * k**2
        - frame_gradient_transverse * k**2,
    )
    require_zero(
        "frame longitudinal dispersion",
        frame_kinetic * frame_speed_longitudinal_sq * k**2
        - frame_gradient_longitudinal * k**2,
    )

    # ------------------------------------------------------------------
    # 3. Regulated force scalar.  E=A|v+grad(pi)|^3 around v=(q,0,0).
    # ------------------------------------------------------------------
    amplitude, k_q, gamma, m_star, q = sp.symbols(
        "A K_Q gamma M_star q", positive=True
    )
    dx, dy, dz = sp.symbols("d_x d_y d_z", real=True)
    spatial_energy = amplitude * (
        (q + dx) ** 2 + dy**2 + dz**2
    ) ** sp.Rational(3, 2)
    fluctuations = (dx, dy, dz)
    spatial_hessian = sp.Matrix(
        [
            [sp.diff(spatial_energy, a, b) for b in fluctuations]
            for a in fluctuations
        ]
    ).subs({dx: 0, dy: 0, dz: 0})
    spatial_hessian = sp.simplify(spatial_hessian)
    expected_hessian = sp.diag(
        6 * amplitude * q, 3 * amplitude * q, 3 * amplitude * q
    )
    require_zero("force spatial Hessian", spatial_hessian - expected_hessian)

    cosine = sp.symbols("cos_theta", real=True)
    omega_nonzero_sq = sp.simplify(
        (
            3 * amplitude * q * (1 + cosine**2) * k**2
            + gamma * k**4 / m_star**2
        )
        / k_q
    )
    omega_zero_sq = sp.simplify(sp.limit(omega_nonzero_sq, q, 0))
    expected_zero = gamma * k**4 / (k_q * m_star**2)
    require_zero("zero-gradient k4 dispersion", omega_zero_sq - expected_zero)
    crossover_k_sq = sp.simplify(
        3 * amplitude * q * (1 + cosine**2) * m_star**2 / gamma
    )
    require_zero(
        "force crossover",
        omega_nonzero_sq.subs(k**2, crossover_k_sq)
        - 2
        * (
            3
            * amplitude
            * q
            * (1 + cosine**2)
            * crossover_k_sq
            / k_q
        ),
    )

    # ------------------------------------------------------------------
    # 4. Numerical sign checks.  These are illustrative points, not a scan of
    #    the observationally allowed Einstein-aether parameter region.
    # ------------------------------------------------------------------
    aether_samples = [
        ("aether_healthy_decoupling", 0.20, 0.10, 0.05, 0.10),
        ("aether_bad_time_kinetic", 0.20, 0.10, 0.05, -0.30),
        ("aether_bad_transverse_gradient", -0.10, 0.30, 0.10, 0.30),
        ("aether_bad_longitudinal_gradient", 0.20, -0.30, 0.05, 0.10),
    ]
    rows: list[dict[str, str | float | bool]] = []
    for name, vc1, vc2, vc3, vc4 in aether_samples:
        vc14 = vc1 + vc4
        vc123 = vc1 + vc2 + vc3
        passed = vc14 > 0 and vc1 > 0 and vc123 > 0
        rows.append(
            {
                "case": name,
                "sector": "aether_decoupling",
                "c1": vc1,
                "c2": vc2,
                "c3": vc3,
                "c4": vc4,
                "c14": vc14,
                "c123": vc123,
                "K_Q": "",
                "A": "",
                "gamma": "",
                "q": "",
                "cos_theta": "",
                "k": "",
                "omega_squared": "",
                "necessary_conditions_pass": passed,
            }
        )

    force_samples = [
        ("force_zero_gradient_regulated", 1.0, 1.0, 0.5, 0.0, 0.4, 1.0),
        ("force_nonzero_parallel", 1.0, 1.0, 0.5, 0.2, 1.0, 1.0),
        ("force_nonzero_perpendicular", 1.0, 1.0, 0.5, 0.2, 0.0, 1.0),
        ("force_bad_regulator", 1.0, 1.0, -0.5, 0.0, 0.4, 1.0),
    ]
    for name, vkq, va, vgamma, vq, vcos, vk in force_samples:
        value = (
            3.0 * va * vq * (1.0 + vcos**2) * vk**2
            + vgamma * vk**4
        ) / vkq
        passed = vkq > 0 and va > 0 and vgamma > 0 and value >= 0
        rows.append(
            {
                "case": name,
                "sector": "force_decoupling",
                "c1": "",
                "c2": "",
                "c3": "",
                "c4": "",
                "c14": "",
                "c123": "",
                "K_Q": vkq,
                "A": va,
                "gamma": vgamma,
                "q": vq,
                "cos_theta": vcos,
                "k": vk,
                "omega_squared": value,
                "necessary_conditions_pass": passed,
            }
        )

    csv_path = args.output_dir / "uvir003_stage_a_checks.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "gate": "UVIR-003",
        "stage": "A_ACTION_AND_DECOUPLING",
        "stage_validation": "PASS",
        "full_gate_status": "IN_PROGRESS",
        "architecture_decision": "INDEPENDENT_DYNAMICAL_U_WITH_CURRENT_ALIGNMENT",
        "double_counting_rule": "U is varied independently; it is not set algebraically equal to the normalized condensate current.",
        "alignment": {
            "quadratic_projected_current": str(alignment_quadratic),
            "interpretation": "Positive alignment coefficient penalizes relative spatial current j_i-n u_i.",
        },
        "aether_decoupling": {
            "necessary_conditions": ["c14 > 0", "c1 > 0", "c123 > 0"],
            "transverse_speed_squared": str(frame_speed_transverse_sq),
            "longitudinal_speed_squared": str(frame_speed_longitudinal_sq),
            "scope": "Necessary frozen-metric conditions only; not the full Einstein-aether stability region.",
        },
        "force_decoupling": {
            "nonzero_gradient_hessian": [
                [str(value) for value in row] for row in spatial_hessian.tolist()
            ],
            "dispersion_nonzero_gradient": str(omega_nonzero_sq),
            "dispersion_zero_gradient": str(omega_zero_sq),
            "crossover_k_squared": str(crossover_k_sq),
            "necessary_conditions": ["K_Q > 0", "A > 0", "gamma > 0"],
            "regulator_verdict": "CONDITIONAL_PASS_IN_FLAT_DECOUPLING_LIMIT",
        },
        "not_yet_done": [
            "complete symmetry-allowed Phi-U-psi mixing census",
            "full metric-lapse-shift-aether-condensate constraint elimination",
            "coupled nonzero-gradient mode matrix",
            "strong-coupling scale",
            "radiative and technical naturalness",
            "covariant regulator completion on general aether backgrounds",
            "matter coupling and lensing",
        ],
        "mat001_status": "BLOCKED",
        "interpretation": "PASS validates necessary Stage-A identities; it does not close UVIR-003.",
    }
    json_path = args.output_dir / "uvir003_stage_a_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 Stage-A validation: PASS")
    print("Architecture: INDEPENDENT_DYNAMICAL_U_WITH_CURRENT_ALIGNMENT")
    print("k4 regulator: CONDITIONAL_PASS_IN_FLAT_DECOUPLING_LIMIT")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
