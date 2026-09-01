#!/usr/bin/env python3
"""TOP-001 S1M: exact modular-basis equivalence audit for a flat T^3.

LABEL: mathematical-template-only
GATE:  TOP-001 Stage S1.7 / S1M (fixed-boundary basis identity)
CLAIM: exact lattice-basis identity only; physics_pass is always false
STATUS: OPEN_SCAFFOLD_ONLY

For a direct-lattice basis B and M in SL(3,Z), B' = B M generates the
same lattice. Direct labels transform as n' = M^{-1} n, while reciprocal
mode and winding labels transform as m' = M^T m. This audit checks those
relations exactly and separates them from a genuine ambient shape
deformation F B.

Does NOT: select a preferred shear, derive a modulus action, compute Casimir
stress, establish stability/backreaction, or produce cosmological constants.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import sympy as sp


PASS_STATUS = "PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE"
FAIL_STATUS = "FAIL_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def matrix_rows(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def vector_entries(vector: sp.Matrix) -> list[str]:
    return [str(vector[i, 0]) for i in range(vector.rows)]


def require_basis(B: sp.Matrix) -> None:
    if B.shape != (3, 3):
        raise ValueError("B must be a 3x3 matrix")
    if any(not value.is_finite for value in B):
        raise ValueError("B entries must be finite")
    if sp.simplify(B.det()) == 0:
        raise ValueError("B must be nonsingular")


def require_sl3z(M: sp.Matrix) -> None:
    if M.shape != (3, 3):
        raise ValueError("M must be a 3x3 matrix")
    if any(value.is_integer is not True for value in M):
        raise ValueError("M entries must be exact integers")
    if M.det() != 1:
        raise ValueError("M must have determinant +1 (SL(3,Z))")


def reciprocal_mode(B: sp.Matrix, label: sp.Matrix) -> sp.Matrix:
    require_basis(B)
    if label.shape != (3, 1):
        raise ValueError("mode label must be a three-vector")
    return sp.simplify(2 * sp.pi * B.inv().T * label)


def winding_covector(B: sp.Matrix, winding: sp.Matrix) -> sp.Matrix:
    require_basis(B)
    if winding.shape != (3, 1):
        raise ValueError("winding label must be a three-vector")
    return sp.simplify(2 * sp.pi * B.inv().T * winding)


def expect_value_error(action: Callable[[], None]) -> bool:
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

    # Rational, non-orthogonal chart keeps every identity exact while avoiding
    # a special cubic basis.
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
    direct_labels = [
        sp.Matrix([1, 0, 0]),
        sp.Matrix([2, -1, 3]),
        sp.Matrix([-2, 2, 1]),
    ]
    reciprocal_labels = [
        sp.Matrix([0, 1, 0]),
        sp.Matrix([1, -2, 3]),
        sp.Matrix([-3, 1, 2]),
    ]
    winding_labels = [sp.Matrix([1, 0, -1]), sp.Matrix([2, -1, 1])]
    checks: list[dict[str, Any]] = []
    map_rows: list[dict[str, Any]] = []

    require_basis(B)
    G = sp.simplify(B.T * B)
    base_volume = abs(B.det())

    for name, M in modular_maps.items():
        require_sl3z(M)
        transformed_basis = sp.simplify(B * M)
        direct_ok = all(
            sp.simplify(transformed_basis * (M.inv() * n) - B * n) == sp.zeros(3, 1)
            and all(value.is_integer is True for value in M.inv() * n)
            for n in direct_labels
        )
        reciprocal_ok = all(
            sp.simplify(
                reciprocal_mode(transformed_basis, M.T * m) - reciprocal_mode(B, m)
            )
            == sp.zeros(3, 1)
            for m in reciprocal_labels
        )
        winding_ok = all(
            sp.simplify(
                winding_covector(transformed_basis, M.T * w) - winding_covector(B, w)
            )
            == sp.zeros(3, 1)
            for w in winding_labels
        )
        transformed_gram = sp.simplify(transformed_basis.T * transformed_basis)
        gram_ok = sp.simplify(transformed_gram - M.T * G * M) == sp.zeros(3, 3)
        volume_ok = abs(transformed_basis.det()) == base_volume

        map_rows.append(
            {
                "name": name,
                "M": matrix_rows(M),
                "det_M": str(M.det()),
                "direct_reindexing_exact": direct_ok,
                "reciprocal_reindexing_exact": reciprocal_ok,
                "winding_reindexing_exact": winding_ok,
                "gram_covariance_exact": gram_ok,
                "volume_invariant_exact": volume_ok,
            }
        )

    add_check(
        checks,
        "declared_maps_are_SL3Z",
        all(M.det() == 1 and all(v.is_integer is True for v in M) for M in modular_maps.values()),
        n_maps=len(modular_maps),
    )
    add_check(
        checks,
        "direct_lattice_reindexing_is_exact",
        all(row["direct_reindexing_exact"] for row in map_rows),
        rule="B_prime=B*M; n_prime=M^-1*n",
    )
    add_check(
        checks,
        "reciprocal_mode_reindexing_is_exact",
        all(row["reciprocal_reindexing_exact"] for row in map_rows),
        rule="m_prime=M^T*m",
    )
    add_check(
        checks,
        "winding_covector_reindexing_is_exact",
        all(row["winding_reindexing_exact"] for row in map_rows),
        rule="w_prime=M^T*w",
    )
    add_check(
        checks,
        "gram_matrix_transforms_covariantly",
        all(row["gram_covariance_exact"] for row in map_rows),
        rule="G_prime=M^T*G*M",
    )
    add_check(
        checks,
        "fundamental_volume_is_invariant",
        all(row["volume_invariant_exact"] for row in map_rows),
        base_volume=str(base_volume),
    )

    # Paired labels test equality of exact reciprocal eigenvalues without
    # incorrectly imposing the same cubical coordinate cutoff in both bases.
    paired_spectrum_ok = True
    for M in modular_maps.values():
        B_prime = B * M
        for m in reciprocal_labels:
            k = reciprocal_mode(B, m)
            k_prime = reciprocal_mode(B_prime, M.T * m)
            paired_spectrum_ok &= sp.simplify((k.T * k)[0] - (k_prime.T * k_prime)[0]) == 0
    add_check(
        checks,
        "paired_laplacian_eigenvalues_are_exactly_invariant",
        paired_spectrum_ok,
        cutoff_warning="Coordinate-box cutoffs must be reindexed with labels; identical raw label boxes are not basis invariant.",
    )

    shear = modular_maps["elementary_shear_12"]
    sample_mode = reciprocal_labels[1]
    mismatched_mode_changes = sp.simplify(
        reciprocal_mode(B * shear, sample_mode) - reciprocal_mode(B, sample_mode)
    ) != sp.zeros(3, 1)
    add_check(
        checks,
        "negative_control_untransformed_label_is_not_claimed_invariant",
        mismatched_mode_changes,
        purpose="Prevents comparing coordinate labels without the required M^T reindexing.",
    )

    # A left-acting, volume-preserving ambient deformation is not an integer
    # basis relabelling. Its reciprocal norm changes for this explicit mode.
    F = sp.diag(sp.Rational(2), sp.Rational(1), sp.Rational(1, 2))
    deformed_basis = sp.simplify(F * B)
    k_before = reciprocal_mode(B, sp.Matrix([1, 0, 0]))
    k_after = reciprocal_mode(deformed_basis, sp.Matrix([1, 0, 0]))
    deformation_changes_norm = sp.simplify(
        (k_before.T * k_before)[0] - (k_after.T * k_after)[0]
    ) != 0
    add_check(
        checks,
        "physical_shape_deformation_is_separate_from_basis_identity",
        F.det() == 1 and deformation_changes_norm,
        deformation="B_physical=F*B",
        F=matrix_rows(F),
        volume_preserved=True,
        sampled_reciprocal_norm_changed=deformation_changes_norm,
    )

    malformed = {
        "singular_basis": expect_value_error(lambda: require_basis(sp.diag(1, 1, 0))),
        "wrong_shape_basis": expect_value_error(lambda: require_basis(sp.eye(2))),
        "non_integer_map": expect_value_error(
            lambda: require_sl3z(sp.diag(sp.Rational(1, 2), 2, 1))
        ),
        "determinant_two_map": expect_value_error(lambda: require_sl3z(sp.diag(2, 1, 1))),
        "orientation_reversing_map": expect_value_error(lambda: require_sl3z(sp.diag(-1, 1, 1))),
    }
    add_check(checks, "malformed_and_out_of_domain_maps_rejected", all(malformed.values()), cases=malformed)

    packaging_flags = {
        "claims_preferred_shear": False,
        "claims_modulus_action": False,
        "claims_casimir_tensor": False,
        "claims_backreaction_or_stability": False,
        "claims_twisted_E2_E3_preference": False,
        "claims_147_significance": False,
        "claims_13_12_attractor": False,
        "claims_H0_or_a0_or_Cobs": False,
        "claims_cosmology": False,
    }
    add_check(
        checks,
        "claim_firewall_packaging_flags_false",
        all(value is False for value in packaging_flags.values()),
        flags=packaging_flags,
    )

    all_ok = all(check["ok"] for check in checks)
    status = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "stage": "S1.7_S1M_FIXED_BOUNDARY_MODULAR_BASIS_IDENTITY",
        "label": "mathematical-template-only",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": status,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "basis_convention": {
            "direct_lattice": "Lambda(B)={B*n | n in Z^3}; columns of B are basis vectors",
            "same_lattice_map": "B_prime=B*M with M in SL(3,Z)",
            "direct_label_map": "n_prime=M^-1*n",
            "reciprocal_and_winding_label_map": "m_prime=M^T*m; w_prime=M^T*w",
            "reciprocal_vector": "k(B,m)=2*pi*B^-T*m",
            "gram_map": "G_prime=M^T*G*M",
        },
        "base_basis": matrix_rows(B),
        "base_gram": matrix_rows(G),
        "base_volume": str(base_volume),
        "modular_map_results": map_rows,
        "checks": checks,
        "n_checks": len(checks),
        "scientific_boundary": (
            "Exact fixed-boundary lattice-basis equivalence under declared SL(3,Z) maps only. "
            "This identifies coordinate descriptions of the same flat T^3 and separates them "
            "from an explicit ambient shape deformation. It does not select a shear, construct "
            "modulus dynamics, compare Casimir energies, or establish physical preference."
        ),
        "cutoff_caution": (
            "A coordinate-label box is not invariant under a general modular map. Spectral "
            "comparisons must transform labels or use a physical eigenvalue cutoff."
        ),
        "forbidden_packaging_not_used": list(packaging_flags.keys()),
        "next_research_step": (
            "Use this identity as a quotient/redundancy guardrail before any dynamical-modulus "
            "or twisted-boundary comparison; no such calculation is performed here."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "top001_s1m_modular_basis_equivalence_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    sidecar = args.output_dir / "top001_s1m_modular_basis_equivalence_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("TOP-001 S1M modular-basis equivalence audit")
    print("  physics_pass:", summary["physics_pass"])
    print("  research_gate_status:", summary["research_gate_status"])
    print("  n_checks:", len(checks))
    for check in checks:
        print(f"  [{'OK' if check['ok'] else 'FAIL'}] {check['name']}")
    print("STATUS:", status)
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
