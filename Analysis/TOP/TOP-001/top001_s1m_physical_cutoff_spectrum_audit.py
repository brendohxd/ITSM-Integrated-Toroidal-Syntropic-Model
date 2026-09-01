#!/usr/bin/env python3
"""TOP-001 S1M robustness: modular spectrum under a physical cutoff.

The dimensionless reciprocal eigenvalue is ell=m^T(B^-1 B^-T)m, with
physical |k|^2=(2*pi)^2 ell. This audit independently enumerates every mode
below a declared ell cutoff in several SL(3,Z)-related bases, proves the
enumeration boxes are complete, and compares exact rational spectra including
degeneracies. It also reproduces the false discrepancy from raw label boxes.

This is a mathematical fixed-boundary audit. physics_pass is always false.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import sympy as sp


PASS_STATUS = "PASS_TOP001_S1M_PHYSICAL_CUTOFF_SPECTRUM_INVARIANCE"
FAIL_STATUS = "FAIL_TOP001_S1M_PHYSICAL_CUTOFF_SPECTRUM_INVARIANCE"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--basis-summary",
        type=Path,
        default=base / "outputs" / "top001_s1m_modular_basis_equivalence_summary.json",
    )
    parser.add_argument(
        "--cutoff",
        default="2",
        help="positive rational cutoff on ell=k^2/(2*pi)^2 (for example 2 or 3/2)",
    )
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--raw-box-n", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def parse_positive_fraction(text: str) -> Fraction:
    try:
        value = Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("cutoff must be a finite positive rational") from exc
    if value <= 0:
        raise ValueError("cutoff must be positive")
    return value


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}"
    if not isinstance(data, dict):
        return None, "top_level_not_object"
    return data, None


def basis_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE"
        and data.get("calculation_status") == "PASS"
        and data.get("research_gate_status") == "OPEN_SCAFFOLD_ONLY"
        and data.get("physics_pass") is False
        and data.get("derived_claims") == []
    )


def require_basis(B: sp.Matrix) -> None:
    if B.shape != (3, 3) or B.det() == 0:
        raise ValueError("B must be an invertible 3x3 basis")
    if any(value.is_finite is not True for value in B):
        raise ValueError("B entries must be finite")


def require_sl3z(M: sp.Matrix) -> None:
    if M.shape != (3, 3):
        raise ValueError("M must be 3x3")
    if any(value.is_integer is not True for value in M):
        raise ValueError("M entries must be exact integers")
    if M.det() != 1:
        raise ValueError("M must have determinant +1")


def rational_matrix(matrix: sp.Matrix) -> list[list[Fraction]]:
    output: list[list[Fraction]] = []
    for i in range(matrix.rows):
        row = []
        for j in range(matrix.cols):
            value = sp.Rational(matrix[i, j])
            row.append(Fraction(int(value.p), int(value.q)))
        output.append(row)
    return output


def scaled_quadratic(matrix: sp.Matrix) -> tuple[list[list[int]], int]:
    rational = rational_matrix(matrix)
    denominator = 1
    for row in rational:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    scaled = [
        [int(value * denominator) for value in row]
        for row in rational
    ]
    return scaled, denominator


def quadratic_numerator(Q: list[list[int]], label: tuple[int, int, int]) -> int:
    i, j, k = label
    return (
        Q[0][0] * i * i
        + Q[1][1] * j * j
        + Q[2][2] * k * k
        + 2 * Q[0][1] * i * j
        + 2 * Q[0][2] * i * k
        + 2 * Q[1][2] * j * k
    )


def enumerate_spectrum(
    Q_matrix: sp.Matrix,
    n_max: int,
    cutoff: Fraction | None,
) -> tuple[Counter[Fraction], dict[tuple[int, int, int], Fraction]]:
    if n_max < 1:
        raise ValueError("n_max must be at least 1")
    Q, denominator = scaled_quadratic(Q_matrix)
    counter: Counter[Fraction] = Counter()
    labels: dict[tuple[int, int, int], Fraction] = {}
    cutoff_scaled = None if cutoff is None else cutoff * denominator
    for i in range(-n_max, n_max + 1):
        for j in range(-n_max, n_max + 1):
            for k in range(-n_max, n_max + 1):
                if i == 0 and j == 0 and k == 0:
                    continue
                label = (i, j, k)
                numerator = quadratic_numerator(Q, label)
                if cutoff_scaled is not None and numerator > cutoff_scaled:
                    continue
                value = Fraction(numerator, denominator)
                counter[value] += 1
                labels[label] = value
    return counter, labels


def spectrum_digest(counter: Counter[Fraction]) -> str:
    canonical = "\n".join(
        f"{value.numerator}/{value.denominator}:{counter[value]}"
        for value in sorted(counter)
    )
    return hashlib.sha256((canonical + "\n").encode("ascii")).hexdigest().upper()


def completeness_certificate(
    Q_matrix: sp.Matrix,
    n_max: int,
    cutoff: Fraction,
) -> dict[str, Any]:
    # For symmetric positive-definite Q, lambda_min(Q)=1/lambda_max(Q^-1)
    # and lambda_max(Q^-1) <= ||Q^-1||_infinity. This gives an exact rational
    # lower bound with no floating eigenvalue or error-margin assumption.
    Q_inverse = Q_matrix.inv()
    inverse_infinity_norm = max(
        sum(abs(Q_inverse[i, j]) for j in range(Q_inverse.cols))
        for i in range(Q_inverse.rows)
    )
    minimum_eigenvalue_lower_bound = sp.simplify(1 / inverse_infinity_norm)
    outside_box_lower_bound = sp.simplify(
        minimum_eigenvalue_lower_bound * (n_max + 1) ** 2
    )
    cutoff_exact = sp.Rational(cutoff.numerator, cutoff.denominator)
    return {
        "proof": "lambda_min(Q) >= 1/||Q^-1||_infinity",
        "inverse_infinity_norm": str(inverse_infinity_norm),
        "minimum_eigenvalue_lower_bound": str(minimum_eigenvalue_lower_bound),
        "outside_box_lower_bound": str(outside_box_lower_bound),
        "outside_box_lower_bound_numeric": float(outside_box_lower_bound),
        "cutoff": str(cutoff),
        "complete": bool(
            minimum_eigenvalue_lower_bound > 0
            and outside_box_lower_bound > cutoff_exact
        ),
    }


def transform_label(M: sp.Matrix, label: tuple[int, int, int]) -> tuple[int, int, int]:
    transformed = M.T * sp.Matrix(label)
    return tuple(int(transformed[i, 0]) for i in range(3))


def expect_value_error(action: Callable[[], Any]) -> bool:
    try:
        action()
    except ValueError:
        return True
    except Exception:
        return False
    return False


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    args = parse_args()
    cutoff = parse_positive_fraction(args.cutoff)
    if args.raw_box_n < 1:
        raise ValueError("raw_box_n must be at least 1")

    basis_summary, basis_error = load_json(args.basis_summary)
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "upstream_modular_basis_contract",
        basis_contract(basis_summary),
        source=args.basis_summary.name,
        parse_error=basis_error,
    )

    B = sp.Matrix(
        [
            [sp.Rational(2), sp.Rational(1, 3), sp.Rational(1, 5)],
            [sp.Rational(0), sp.Rational(3), sp.Rational(2, 7)],
            [sp.Rational(0), sp.Rational(0), sp.Rational(5)],
        ]
    )
    modular_maps = {
        "identity": sp.eye(3),
        "elementary_shear_12": sp.Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]]),
        "compound_shear": sp.Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]]),
        "orientation_preserving_cycle": sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
    }
    require_basis(B)
    for M in modular_maps.values():
        require_sl3z(M)
    add_check(
        checks,
        "declared_maps_are_SL3Z",
        all(M.det() == 1 and all(value.is_integer is True for value in M) for M in modular_maps.values()),
        n_maps=len(modular_maps),
    )

    spectra: dict[str, Counter[Fraction]] = {}
    label_maps: dict[str, dict[tuple[int, int, int], Fraction]] = {}
    map_rows: list[dict[str, Any]] = []
    for name, M in modular_maps.items():
        B_prime = sp.simplify(B * M)
        Q_prime = sp.simplify(B_prime.inv() * B_prime.inv().T)
        spectrum, labels = enumerate_spectrum(Q_prime, args.n_max, cutoff)
        certificate = completeness_certificate(Q_prime, args.n_max, cutoff)
        spectra[name] = spectrum
        label_maps[name] = labels
        values = sorted(spectrum)
        map_rows.append(
            {
                "name": name,
                "n_modes_below_cutoff": sum(spectrum.values()),
                "n_distinct_eigenvalues": len(spectrum),
                "minimum_ell": str(values[0]) if values else None,
                "maximum_ell": str(values[-1]) if values else None,
                "spectrum_sha256": spectrum_digest(spectrum),
                "maximum_degeneracy": max(spectrum.values()) if spectrum else 0,
                "completeness_certificate": certificate,
            }
        )

    add_check(
        checks,
        "physical_cutoff_enumerations_are_complete",
        all(row["completeness_certificate"]["complete"] for row in map_rows),
        certificates={row["name"]: row["completeness_certificate"] for row in map_rows},
    )
    base_spectrum = spectra["identity"]
    add_check(
        checks,
        "exact_spectrum_multisets_are_modular_invariant",
        all(spectrum == base_spectrum for spectrum in spectra.values()),
        spectrum_sha256=spectrum_digest(base_spectrum),
        map_digests={row["name"]: row["spectrum_sha256"] for row in map_rows},
    )
    add_check(
        checks,
        "degeneracy_profiles_are_modular_invariant",
        all(
            sorted(spectrum.values()) == sorted(base_spectrum.values())
            for spectrum in spectra.values()
        ),
        n_distinct_eigenvalues=len(base_spectrum),
        maximum_degeneracy=max(base_spectrum.values()),
    )

    base_labels = label_maps["identity"]
    bijection_rows = []
    for name, M in modular_maps.items():
        transformed_labels = label_maps[name]
        exact = True
        for label, eigenvalue in base_labels.items():
            mapped = transform_label(M, label)
            if transformed_labels.get(mapped) != eigenvalue:
                exact = False
                break
        exact = exact and len(transformed_labels) == len(base_labels)
        bijection_rows.append({"name": name, "exact": exact})
    add_check(
        checks,
        "physical_cutoff_label_bijection_is_exact",
        all(row["exact"] for row in bijection_rows),
        rule="m_prime=M^T*m",
        results=bijection_rows,
    )

    refined_ok = True
    for name, M in modular_maps.items():
        B_prime = B * M
        Q_prime = sp.simplify(B_prime.inv() * B_prime.inv().T)
        refined, _ = enumerate_spectrum(Q_prime, args.n_max + 2, cutoff)
        refined_ok &= refined == spectra[name]
    add_check(
        checks,
        "physical_cutoff_spectrum_is_box_refinement_stable",
        refined_ok,
        n_max=args.n_max,
        n_max_refined=args.n_max + 2,
    )

    Q_base = sp.simplify(B.inv() * B.inv().T)
    shear = modular_maps["elementary_shear_12"]
    B_shear = B * shear
    Q_shear = sp.simplify(B_shear.inv() * B_shear.inv().T)
    raw_base, raw_base_labels = enumerate_spectrum(Q_base, args.raw_box_n, None)
    raw_shear, _ = enumerate_spectrum(Q_shear, args.raw_box_n, None)
    mapped_labels_leave_box = any(
        max(abs(value) for value in transform_label(shear, label)) > args.raw_box_n
        for label in raw_base_labels
    )
    add_check(
        checks,
        "negative_control_raw_label_box_creates_false_difference",
        raw_base != raw_shear and mapped_labels_leave_box,
        raw_box_n=args.raw_box_n,
        raw_base_digest=spectrum_digest(raw_base),
        raw_shear_digest=spectrum_digest(raw_shear),
        mapped_labels_leave_box=mapped_labels_leave_box,
    )

    F = sp.diag(sp.Rational(2), sp.Rational(1), sp.Rational(1, 2))
    B_physical = F * B
    Q_physical = sp.simplify(B_physical.inv() * B_physical.inv().T)
    physical_spectrum, _ = enumerate_spectrum(Q_physical, args.n_max, cutoff)
    physical_certificate = completeness_certificate(Q_physical, args.n_max, cutoff)
    add_check(
        checks,
        "volume_preserving_physical_deformation_changes_spectrum",
        F.det() == 1
        and physical_certificate["complete"]
        and physical_spectrum != base_spectrum,
        deformation="B_physical=F*B",
        det_F=str(F.det()),
        physical_spectrum_sha256=spectrum_digest(physical_spectrum),
        base_spectrum_sha256=spectrum_digest(base_spectrum),
        completeness_certificate=physical_certificate,
    )

    malformed = {
        "zero_cutoff": expect_value_error(lambda: parse_positive_fraction("0")),
        "negative_cutoff": expect_value_error(lambda: parse_positive_fraction("-1")),
        "non_rational_cutoff": expect_value_error(lambda: parse_positive_fraction("nan")),
        "zero_n_max": expect_value_error(lambda: enumerate_spectrum(Q_base, 0, cutoff)),
        "singular_basis": expect_value_error(lambda: require_basis(sp.diag(1, 1, 0))),
        "non_integer_map": expect_value_error(
            lambda: require_sl3z(sp.diag(sp.Rational(1, 2), 2, 1))
        ),
        "determinant_two_map": expect_value_error(lambda: require_sl3z(sp.diag(2, 1, 1))),
    }
    add_check(
        checks,
        "malformed_cutoff_basis_and_maps_rejected",
        all(malformed.values()),
        cases=malformed,
    )

    packaging_flags = {
        "claims_preferred_shear": False,
        "claims_modulus_action": False,
        "claims_casimir_energy": False,
        "claims_physical_stability": False,
        "claims_twisted_boundary_preference": False,
        "claims_147_significance": False,
        "claims_13_12_or_H0_or_a0_or_Cobs": False,
        "claims_cosmology": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "claim_firewall_packaging_flags_false",
        all(value is False for value in packaging_flags.values()),
        flags=packaging_flags,
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "stage": "S1M_PHYSICAL_CUTOFF_SPECTRUM_ROBUSTNESS",
        "label": "mathematical-template-only",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "cutoff_convention": {
            "dimensionless_eigenvalue": "ell=m^T*(B^-1*B^-T)*m",
            "physical_relation": "|k|^2=(2*pi)^2*ell",
            "cutoff_ell": str(cutoff),
            "n_max": args.n_max,
            "completeness_rule": "(n_max+1)^2/||Q^-1||_infinity > cutoff",
        },
        "modular_map_results": map_rows,
        "reference_spectrum": {
            "n_modes": sum(base_spectrum.values()),
            "n_distinct_eigenvalues": len(base_spectrum),
            "maximum_degeneracy": max(base_spectrum.values()),
            "spectrum_sha256": spectrum_digest(base_spectrum),
        },
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": packaging_flags,
        "scientific_boundary": (
            "A PASS proves exact equality of the enumerated reciprocal spectrum and "
            "degeneracies under declared SL(3,Z) basis changes for a certified-complete "
            "physical eigenvalue cutoff. It also demonstrates why identical raw coordinate "
            "label boxes are invalid comparisons. It does not compute Casimir energy, select "
            "a shear or topology, supply modulus dynamics, or establish a physics preference."
        ),
        "serial_next": (
            "Treat modularly equivalent bases as one fixed-boundary geometry before any "
            "inequivalent modulus or twisted-boundary energy comparison."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "top001_s1m_physical_cutoff_spectrum_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "top001_s1m_physical_cutoff_spectrum_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("TOP-001 S1M physical-cutoff spectrum audit")
    print("  cutoff ell:", cutoff, "| n_max:", args.n_max)
    print("  physics_pass: False | research_gate: OPEN_SCAFFOLD_ONLY")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
