#!/usr/bin/env python3
"""WAK-001 W2.5 finite-q scalar mode-inventory pre-screen.

The audit classifies direct-sum, mixed and identified-W alternatives. It does
not establish a microscopic wake degree of freedom or close WAK-001 Stage 2.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import sympy as sp


EXISTING_FINITE_Q_MODES = ("Xi", "Q_rho", "Q_chi", "Pi")


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def inertia(matrix: sp.Matrix) -> tuple[int, int, int]:
    eigenvalues = matrix.eigenvals()
    positive = 0
    zero = 0
    negative = 0
    for value, multiplicity in eigenvalues.items():
        sign = sp.sign(sp.simplify(value))
        if sign == 1:
            positive += multiplicity
        elif sign == 0:
            zero += multiplicity
        elif sign == -1:
            negative += multiplicity
        else:
            raise ValueError(f"undetermined eigenvalue sign: {value}")
    return positive, zero, negative


def main() -> None:
    args = parse_args()

    k_xi, k_rho, k_chi, k_pi, Z = sp.symbols(
        "k_Xi k_Qrho k_Qchi k_Pi Z_W", positive=True, finite=True
    )
    existing_kinetic = sp.diag(k_xi, k_rho, k_chi, k_pi)
    direct_sum = sp.diag(k_xi, k_rho, k_chi, k_pi, Z)
    determinant_factorization = sp.simplify(
        direct_sum.det() - existing_kinetic.det() * Z
    )

    sample_existing = sp.eye(4)
    sample_Z = sp.Rational(1, 1)
    decoupled = sp.diag(1, 1, 1, 1, sample_Z)

    small_mixing = sp.Matrix(
        [sp.Rational(1, 5), sp.Rational(-1, 10), 0, sp.Rational(1, 10)]
    )
    healthy_mixed = sample_existing.row_join(small_mixing).col_join(
        small_mixing.T.row_join(sp.Matrix([[sample_Z]]))
    )
    healthy_schur = sp.simplify(
        sample_Z - (small_mixing.T * sample_existing.inv() * small_mixing)[0]
    )

    rank_loss_mixing = sp.Matrix([1, 0, 0, 0])
    rank_loss_matrix = sample_existing.row_join(rank_loss_mixing).col_join(
        rank_loss_mixing.T.row_join(sp.Matrix([[sample_Z]]))
    )
    rank_loss_schur = sp.simplify(
        sample_Z
        - (rank_loss_mixing.T * sample_existing.inv() * rank_loss_mixing)[0]
    )

    ghost_mixing = sp.Matrix([2, 0, 0, 0])
    ghost_matrix = sample_existing.row_join(ghost_mixing).col_join(
        ghost_mixing.T.row_join(sp.Matrix([[sample_Z]]))
    )
    ghost_schur = sp.simplify(
        sample_Z - (ghost_mixing.T * sample_existing.inv() * ghost_mixing)[0]
    )

    # If W=a_i q_i is an identification rather than a new coordinate, the map
    # q -> (q, W(q)) has rank four and cannot add a canonical pair.
    a_xi, a_rho, a_chi, a_pi = sp.symbols(
        "a_Xi a_Qrho a_Qchi a_Pi", real=True, finite=True
    )
    identification_jacobian = sp.eye(4).col_join(
        sp.Matrix([[a_xi, a_rho, a_chi, a_pi]])
    )

    zero_kinetic_control = sp.diag(1, 1, 1, 1, 0)
    checks = {
        "declared_existing_finite_q_mode_labels_are_unique": (
            len(set(EXISTING_FINITE_Q_MODES)) == 4
        ),
        "direct_sum_determinant_factorizes": determinant_factorization == 0,
        "positive_decoupled_W_adds_one_kinetic_rank": (
            decoupled.rank() == sample_existing.rank() + 1
        ),
        "decoupled_finite_q_inertia_is_five_positive": (
            inertia(decoupled) == (5, 0, 0)
        ),
        "negative_control_zero_W_kinetic_adds_no_rank": (
            zero_kinetic_control.rank() == sample_existing.rank()
        ),
        "small_declared_mixing_has_positive_schur_complement": healthy_schur > 0,
        "small_declared_mixing_remains_positive_definite": (
            inertia(healthy_mixed) == (5, 0, 0)
        ),
        "negative_control_unit_mixing_causes_rank_loss": (
            rank_loss_schur == 0
            and rank_loss_matrix.rank() == 4
            and inertia(rank_loss_matrix) == (4, 1, 0)
        ),
        "negative_control_large_mixing_creates_ghost": (
            ghost_schur < 0 and inertia(ghost_matrix) == (4, 0, 1)
        ),
        "identified_W_map_adds_no_independent_coordinate": (
            identification_jacobian.rank() == 4
        ),
    }
    checks = {name: bool(passed) for name, passed in checks.items()}
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_W2_5_MODE_COUNTING_PRESCREEN"
        if all_ok
        else "FAIL_WAK001_W2_5_MODE_COUNTING_PRESCREEN"
    )

    summary: dict[str, Any] = {
        "gate": "WAK-001",
        "stage": "W2.5 finite-q scalar mode-inventory pre-screen",
        "label": "symbolic-mode-counting-template-only",
        "status": status,
        "calculation_pass": all_ok,
        "stage2_status": "IN_PROGRESS",
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "domain": (
            "finite nonzero q; the exactly homogeneous Xi mode is excluded as gauge"
        ),
        "existing_declared_modes": [
            {
                "label": "Xi",
                "role": "finite-q gauge-regular metric/frame continuation",
            },
            {"label": "Q_rho", "role": "retained condensate-density scalar"},
            {"label": "Q_chi", "role": "retained condensate-phase scalar"},
            {"label": "Pi", "role": "quadratically factorized Track-A force mode"},
        ],
        "classification": {
            "decoupled_independent_W": (
                "adds one positive canonical pair by construction when Z_W>0"
            ),
            "mixed_independent_W": (
                "requires positive kinetic Schur complement "
                "Z_W-b^T K_existing^-1 b"
            ),
            "identified_W": (
                "adds no independent coordinate; assigning a second T_W would double count"
            ),
        },
        "sample_exact": {
            "healthy_mixing_schur_complement": str(healthy_schur),
            "rank_loss_schur_complement": str(rank_loss_schur),
            "ghost_mixing_schur_complement": str(ghost_schur),
            "decoupled_inertia": list(inertia(decoupled)),
            "healthy_mixed_inertia": list(inertia(healthy_mixed)),
            "rank_loss_inertia": list(inertia(rank_loss_matrix)),
            "ghost_inertia": list(inertia(ghost_matrix)),
        },
        "checks": checks,
        "mode_independence_status": "NOT_YET_ESTABLISHED",
        "hold": "HOLD_MICROSCOPIC_MODE_IDENTITY_AND_COUPLED_MIXING",
        "scientific_boundary": (
            "The pre-screen classifies kinetic-rank outcomes. With no mixing or "
            "identification map declared, the trial action adds W as a new mode by "
            "construction, not by derivation. The actual coupled Hessian, microscopic "
            "identity and constraint ownership remain unmatched."
        ),
        "forbidden_inferences": {
            "independent_physical_wake_exists": False,
            "wake_is_distinct_from_Phi_U_psi": False,
            "interaction_source_is_derived": False,
            "exchange_current_is_derived": False,
            "dissipation_is_derived": False,
            "static_AQUAL_correction_is_derived": False,
        },
        "next": [
            "supply one parent quadratic S_UV+S_psi+S_W action with declared mixing",
            "compute its constrained finite-q Hessian before and after adding W",
            "reject Route II if W is an identified combination or produces rank loss/ghost",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_route2_mode_inventory_prescreen_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 W2.5 finite-q scalar mode-inventory pre-screen")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("MODE INDEPENDENCE: NOT_YET_ESTABLISHED")
    print("HOLD: HOLD_MICROSCOPIC_MODE_IDENTITY_AND_COUPLED_MIXING")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
