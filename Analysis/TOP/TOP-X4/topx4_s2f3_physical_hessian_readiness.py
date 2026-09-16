#!/usr/bin/env python3
"""Audit readiness for the physical constrained X4-S2F3 Hessian.

This is deliberately a readiness checkpoint, not a Hessian calculation.  It
checks the registered upstream receipts and records the missing action,
stress, state, constraint and normalization inputs without setting any of
them to zero or inferring them from a fixed-metric operator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


STATUS = "HOLD_PHYSICAL_HESSIAN_INPUTS_NOT_CLOSED"
PHYSICAL_HESSIAN = "NOT_CONSTRUCTED"
RADION_MASS = "NOT_COMPUTED"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "galaxy" + "_target",
    "hubble" + "_target",
    "desired" + "_coupling",
)

REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_physical_hessian_readiness_summary.json"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_PHYSICAL_HESSIAN_READINESS_CONTRACT_2026-09-16.md"
)
PLAN_PATH = (
    REPO_ROOT
    / "Theory"
    / "Core"
    / "Reasoning_Mode_Plans"
    / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
    / "PLAN.md"
)
PARENT_FREEZE_PATH = (
    REPO_ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def root_has_any(data: dict[str, Any], names: tuple[str, ...]) -> list[str]:
    return sorted(name for name in names if name in data)


def main() -> int:
    args = parse_args()
    outputs = BASE / "outputs"
    paths = [
        CONTRACT_PATH,
        PLAN_PATH,
        PARENT_FREEZE_PATH,
        outputs / "topx4_a1_background_summary.json",
        outputs / "topx4_s2f3_dynamic_state_subtraction_summary.json",
        outputs / "topx4_s2f3_exact_transport_retry_summary.json",
        outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json",
        outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json",
        outputs / "topx4_s2f3_global_state_construction_summary.json",
    ]
    receipts = [sidecar_check(path) for path in paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_readiness_authority_and_input_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    dynamic = load_json(outputs / "topx4_s2f3_dynamic_state_subtraction_summary.json")
    exact = load_json(outputs / "topx4_s2f3_exact_transport_retry_summary.json")
    covariant = load_json(outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json")
    parametrix = load_json(outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json")
    global_state = load_json(outputs / "topx4_s2f3_global_state_construction_summary.json")

    add_check(
        checks,
        "fixed_metric_scalar_operator_is_not_called_physical_hessian",
        covariant.get("scalar_matrix_operator") == "DERIVED_FIXED_METRIC_OFF_SHELL"
        and covariant.get("physics_pass") is False
        and covariant.get("gate_effect") == "NONE",
        scalar_matrix_operator=covariant.get("scalar_matrix_operator"),
        physical_hessian=PHYSICAL_HESSIAN,
    )
    add_check(
        checks,
        "global_scalar_state_does_not_supply_stress",
        global_state.get("construction_status", {}).get("global_scalar_matrix_hadamard_state")
        == "THEOREM_BACKED_CONSTRUCTED"
        and global_state.get("physics_pass") is False
        and global_state.get("gate_effect") == "NONE"
        and covariant.get("renormalized_stress") == "NOT_COMPUTED",
        global_state_status=global_state.get("construction_status", {}).get(
            "global_scalar_matrix_hadamard_state"
        ),
        renormalized_stress=covariant.get("renormalized_stress"),
    )
    add_check(
        checks,
        "finite_charge_semiclassical_background_is_not_closed",
        dynamic.get("advance_to_renormalized_stress") is False
        and exact.get("advance_to_semiclassical_background") is False
        and dynamic.get("physics_pass") is False
        and exact.get("physics_pass") is False,
        dynamic_status=dynamic.get("status"),
        exact_status=exact.get("status"),
    )
    add_check(
        checks,
        "determinant_and_stress_inputs_are_explicitly_uncomputed",
        covariant.get("determinant") == "NOT_COMPUTED"
        and covariant.get("renormalized_stress") == "NOT_COMPUTED"
        and parametrix.get("determinant") == "NOT_COMPUTED"
        and parametrix.get("renormalized_stress") == "NOT_COMPUTED",
        determinant=covariant.get("determinant"),
        renormalized_stress=covariant.get("renormalized_stress"),
    )

    constraint_names = (
        "preconstraint_kinetic_block",
        "constraint_hessian",
        "dynamic_constraint_mixing",
        "reduced_hessian",
        "physical_hessian",
        "radion_mass",
    )
    present_constraint_keys = sorted(
        set(root_has_any(dynamic, constraint_names))
        | set(root_has_any(exact, constraint_names))
        | set(root_has_any(covariant, constraint_names))
        | set(root_has_any(global_state, constraint_names))
    )
    add_check(
        checks,
        "constraint_and_reduced_hessian_blocks_are_not_exported",
        not present_constraint_keys,
        present_root_keys=present_constraint_keys,
        required_missing=list(constraint_names),
    )

    required_inputs = {
        "complete_varied_semiclassical_action": "NOT_AVAILABLE",
        "finite_charge_on_shell_background": "NOT_AVAILABLE",
        "state_dependent_renormalized_stress": "NOT_AVAILABLE",
        "gravity_ghost_and_parity_sectors": "NOT_AVAILABLE",
        "counterterm_normalizations": "NOT_AVAILABLE",
        "constraint_blocks_and_singular_domain": "NOT_AVAILABLE",
        "canonical_fixed_charge_reduction": "NOT_AVAILABLE",
        "robustness_domain_for_reduced_hessian": "NOT_AVAILABLE",
    }
    add_check(
        checks,
        "all_required_physical_hessian_inputs_remain_unavailable",
        all(value == "NOT_AVAILABLE" for value in required_inputs.values()),
        required_inputs=required_inputs,
    )

    source_text = Path(__file__).read_text(encoding="utf-8")
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result: dict[str, Any] = {
        "schema": "ITSM_TOPX4_S2F3_PHYSICAL_HESSIAN_READINESS_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "status": STATUS if all_ok else "ERROR_PHYSICAL_HESSIAN_READINESS_AUDIT",
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "readiness_checks_passed": sum(check["ok"] for check in checks),
        "readiness_checks_total": len(checks),
        "physical_hessian": PHYSICAL_HESSIAN,
        "radion_mass": RADION_MASS,
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_x4_d2": False,
        "checks": checks,
        "required_inputs": required_inputs,
        "nonclaims": [
            "no physical constrained Hessian",
            "no canonical radion mass",
            "no determinant or renormalized stress",
            "no finite-charge self-consistent background",
            "no parity/anomaly clearance",
            "no A4 or Ultra entry",
            "no MAT, UVIR, cosmology, BBN or publication promotion",
        ],
        "scientific_boundary": (
            "The registered fixed-metric scalar operator and theorem-backed scalar state "
            "are prerequisites only. A physical Hessian requires the complete varied "
            "semiclassical action, state-dependent stress and an explicit metric/radion "
            "constraint reduction. No missing block is inferred or set to zero."
        ),
        "source_sha256": sha256_file(Path(__file__)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    args.output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"readiness_checks={result['readiness_checks_passed']}/{result['readiness_checks_total']}")
    print(f"physical_hessian={PHYSICAL_HESSIAN}")
    print(f"radion_mass={RADION_MASS}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
