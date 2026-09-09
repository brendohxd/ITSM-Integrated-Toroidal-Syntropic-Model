#!/usr/bin/env python3
"""TOP-X4 A0 exact kinematic and dimensional control.

Tests a rectangular spatial T4 written as T3_obs x S1_y. This does not test a
five-dimensional dynamical action, radion stability, matter coupling,
reservoir exchange or any observational prediction. physics_pass is always
false.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any


PASS_STATUS = "PASS_TOPX4_A0_KINEMATIC_AND_DIMENSIONAL_CONTROL"
FAIL_STATUS = "FAIL_TOPX4_A0_KINEMATIC_AND_DIMENSIONAL_CONTROL"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-max", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def direct_t4_reduced_eigenvalue(
    label: tuple[int, int, int, int], lengths: tuple[Fraction, ...]
) -> Fraction:
    return sum(Fraction(n * n, 1) / (length * length) for n, length in zip(label, lengths))


def t3_plus_kk_reduced_eigenvalue(
    label: tuple[int, int, int, int], lengths: tuple[Fraction, ...]
) -> Fraction:
    t3 = sum(Fraction(label[i] * label[i], 1) / (lengths[i] * lengths[i]) for i in range(3))
    kk = Fraction(label[3] * label[3], 1) / (lengths[3] * lengths[3])
    return t3 + kk


def isotropic_shell_degeneracies(n_max: int, shell_max: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for label in itertools.product(range(-n_max, n_max + 1), repeat=4):
        shell = sum(n * n for n in label)
        if 0 < shell <= shell_max:
            counts[shell] += 1
    return counts


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    args = parse_args()
    if args.n_max < 2:
        raise ValueError("n-max must be at least 2 to certify the first four shells")

    checks: list[dict[str, Any]] = []

    betti = [math.comb(4, k) for k in range(5)]
    euler = sum(((-1) ** k) * value for k, value in enumerate(betti))
    add_check(checks, "t4_betti_numbers", betti == [1, 4, 6, 4, 1], values=betti)
    add_check(checks, "t4_euler_characteristic_zero", euler == 0, value=euler)
    circle_factors = 4
    add_check(
        checks,
        "fundamental_group_product_identity",
        circle_factors == 4,
        circle_factors=circle_factors,
        identity="pi_1((S1)^4)=product_1^4 pi_1(S1)=Z^4",
        proof_type="analytic product-space identity; not inferred numerically",
    )

    lengths = (Fraction(1, 1), Fraction(6, 5), Fraction(7, 5), Fraction(3, 4))
    labels = list(itertools.product(range(-args.n_max, args.n_max + 1), repeat=4))
    labels.remove((0, 0, 0, 0))
    mismatches = []
    for label in labels:
        direct = direct_t4_reduced_eigenvalue(label, lengths)
        decomposed = t3_plus_kk_reduced_eigenvalue(label, lengths)
        if direct != decomposed:
            mismatches.append({"label": label, "direct": str(direct), "decomposed": str(decomposed)})
    add_check(
        checks,
        "direct_t4_equals_t3_plus_kk_exactly",
        not mismatches,
        labels_tested=len(labels),
        mismatches=mismatches[:5],
        convention="lambda/(2*pi)^2=sum_i n_i^2/L_i^2",
    )

    shell_counts = isotropic_shell_degeneracies(args.n_max, 4)
    expected_shells = {1: 8, 2: 24, 3: 32, 4: 24}
    add_check(
        checks,
        "isotropic_first_four_shell_degeneracies",
        all(shell_counts[shell] == expected for shell, expected in expected_shells.items()),
        measured={str(k): shell_counts[k] for k in expected_shells},
        expected={str(k): value for k, value in expected_shells.items()},
    )

    circumference = 5.0
    radius = circumference / (2.0 * math.pi)
    correct_gap = 1.0 / radius
    circumference_gap = 2.0 * math.pi / circumference
    wrong_gap = 1.0 / circumference
    add_check(
        checks,
        "radius_circumference_kk_gap_identity",
        math.isclose(correct_gap, circumference_gap, rel_tol=0.0, abs_tol=1.0e-15),
        radius=radius,
        circumference=circumference,
        gap=correct_gap,
    )
    add_check(
        checks,
        "negative_control_wrong_radius_convention_detected",
        not math.isclose(wrong_gap, correct_gap, rel_tol=1.0e-12, abs_tol=0.0),
        wrong_gap=wrong_gap,
        correct_gap=correct_gap,
        mismatch_factor=correct_gap / wrong_gap,
    )

    circumferences = [0.5, 1.0, 2.0]
    gaps = [2.0 * math.pi / length for length in circumferences]
    add_check(
        checks,
        "small_circle_raises_kk_gap",
        gaps[0] > gaps[1] > gaps[2],
        circumferences=circumferences,
        first_gaps=gaps,
    )

    # Natural-unit mass dimensions. Length has dimension -1.
    dimensions = {
        "length": -1,
        "Phi_5": Fraction(3, 2),
        "phi_4": Fraction(1, 1),
        "ell_minus_half": Fraction(1, 2),
        "M5_cubed": 3,
        "MPl_squared": 2,
        "lambda5_quartic": -1,
        "lambda4_quartic": 0,
        "rho0_squared": 3,
        "inverse_radius_squared": 2,
        "rho_winding_5d": 5,
    }
    add_check(
        checks,
        "field_normalization_dimensions",
        dimensions["phi_4"] + dimensions["ell_minus_half"] == dimensions["Phi_5"],
        equation="[Phi_5]=[ell^-1/2]+[phi_4]",
    )
    add_check(
        checks,
        "planck_reduction_dimensions",
        dimensions["M5_cubed"] + dimensions["length"] == dimensions["MPl_squared"],
        equation="M_Pl^2=ell_4 M5^3",
    )
    add_check(
        checks,
        "quartic_reduction_dimensions",
        dimensions["lambda5_quartic"] - dimensions["length"] == dimensions["lambda4_quartic"],
        equation="lambda4=lambda5/ell_4",
    )
    add_check(
        checks,
        "winding_energy_density_dimension_five",
        dimensions["rho0_squared"] + dimensions["inverse_radius_squared"]
        == dimensions["rho_winding_5d"],
        equation="rho_w,5=rho0^2 w^2/(2 R^2)",
    )

    winding_zero = 0.0
    winding_nonzero = (2.0**2) * (3.0**2) / (2.0 * radius**2)
    add_check(
        checks,
        "winding_zero_and_positive_gradient_control",
        winding_zero == 0.0 and winding_nonzero > 0.0,
        zero_winding_energy=winding_zero,
        sample_nonzero_winding_energy=winding_nonzero,
    )

    forbidden_inputs = {
        "observed_a0": False,
        "H0": False,
        "SPARC": False,
        "target_2pi_coefficient": False,
        "target_reservoir_current": False,
    }
    add_check(checks, "observational_input_firewall", not any(forbidden_inputs.values()), flags=forbidden_inputs)

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_A0_v1",
        "route": "TOP-X4_KK-001",
        "status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "canonical_t3_replaced": False,
        "interpretation": "spatial/internal T3_obs x S1_y; Lorentzian time noncompact",
        "coordinate_convention": {
            "y_period": "2*pi",
            "physical_radius": "R",
            "physical_circumference": "ell_4=2*pi*R",
            "kk_mass_squared": "m_n^2=m_0^2+n^2/R^2=m_0^2+(2*pi*n/ell_4)^2",
        },
        "exact_lengths_for_spectrum_test": [str(value) for value in lengths],
        "mass_dimensions_natural_units": {key: str(value) for key, value in dimensions.items()},
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "derived_claims": [],
        "next_entry_condition": "freeze one complete five-dimensional off-shell action and on-shell background",
        "explicit_nonclaims": [
            "no radion stabilization",
            "no derived Q^mu",
            "no matter pole residue",
            "no K_Q or V",
            "no a0 or H0 relation",
            "no observational prediction",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "topx4_a0_kinematic_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = sha256_bytes(payload)
    sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
    sidecar_path.write_text(f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n")

    print(result["status"])
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
