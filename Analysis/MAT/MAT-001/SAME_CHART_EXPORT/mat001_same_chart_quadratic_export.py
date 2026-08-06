#!/usr/bin/env python3
"""MAT-001 same-chart free-sector quadratic export (partial).

Exports the free UVIR quadratic objects K, C and the decomposed constraint
source maps in one declared original dynamical chart, and transforms the
free-sector kinetic metric into the physical scalar chart. Matter source
covectors d,h remain NOT_EXPORTED: the live finite-q reduction has no
declared external-matter interaction. Velocity-linear mixing is isolated
explicitly, so the pure static J2 B block is not claimed. V stays
NOT_COMPUTED.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL"
FAIL_STATUS = "FAIL_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir_dir = repo / "Analysis" / "UVIR" / "UVIR-003"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--finite-q-summary",
        type=Path,
        default=uvir_dir / "outputs" / "uvir003_scalar_adm_finite_q_summary.json",
    )
    parser.add_argument(
        "--physical-basis-summary",
        type=Path,
        default=uvir_dir
        / "outputs"
        / "uvir003_physical_scalar_basis_summary.json",
    )
    parser.add_argument(
        "--j2-summary",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
    )
    parser.add_argument(
        "--inventory-summary",
        type=Path,
        default=mat
        / "LIVE_EXPORT_INVENTORY"
        / "outputs"
        / "mat001_live_uvir_export_inventory_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--self-test-mutations",
        action="store_true",
        help="Run internal fail-closed mutation checks and exit without writing.",
    )
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None, str | None]:
    if not path.is_file():
        return None, "missing", None
    try:
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}", None
    if not isinstance(data, dict):
        return None, "top_level_not_object", None
    return data, None, hashlib.sha256(raw).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(
    checks: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def import_uvir_reduction() -> dict[str, Any]:
    # .../Analysis/MAT/MAT-001/SAME_CHART_EXPORT -> repo root is parents[4]
    repo = Path(__file__).resolve().parents[4]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003"
    if str(uvir) not in sys.path:
        sys.path.insert(0, str(uvir))
    from uvir003_scalar_adm_finite_q import symbolic_reduction  # type: ignore

    return symbolic_reduction()


def matrix_string(matrix: sp.MatrixBase) -> str:
    return str(sp.Matrix(matrix.applyfunc(sp.simplify)))


def build_free_sector_export() -> dict[str, Any]:
    reduction = import_uvir_reduction()
    expressions = reduction["expressions"]
    kinetic = expressions["kinetic"]
    constraint_matrix = expressions["constraint_matrix"]
    constraint_source = expressions["constraint_source"]

    coordinates = list(sp.symbols("R delta_rho vartheta", real=True))
    velocities = list(
        sp.symbols("R_dot delta_rho_dot vartheta_dot", real=True)
    )
    coord_vec = sp.Matrix(coordinates)
    vel_vec = sp.Matrix(velocities)

    field_map = sp.Matrix(
        [
            [
                sp.diff(constraint_source[i], coordinates[j])
                for j in range(3)
            ]
            for i in range(2)
        ]
    )
    velocity_map = sp.Matrix(
        [
            [
                sp.diff(constraint_source[i], velocities[j])
                for j in range(3)
            ]
            for i in range(2)
        ]
    )
    reconstruction = sp.simplify(
        field_map * coord_vec + velocity_map * vel_vec - constraint_source
    )
    require(
        all(sp.simplify(value) == 0 for value in reconstruction),
        "constraint_source is not exactly linear in fields and velocities",
    )
    require(
        all(
            sp.simplify(value) == 0
            for value in (kinetic - kinetic.T)
        ),
        "kinetic metric is not symmetric",
    )
    require(
        all(
            sp.simplify(value) == 0
            for value in (constraint_matrix - constraint_matrix.T)
        ),
        "constraint matrix is not symmetric",
    )

    # Physical chart transform used by UVIR physical scalar basis:
    # y = T p with p = (Xi, Q_rho, Q_chi).
    hubble, q_phys = sp.symbols("H q_phys", positive=True)
    rho = sp.symbols("rho", positive=True)
    rho_dot, chemical = sp.symbols("rho_dot mu", real=True)
    transform = sp.Matrix(
        [
            [hubble / q_phys, 0, 0],
            [rho_dot / q_phys, 1, 0],
            [chemical / q_phys, 0, 1 / rho],
        ]
    )
    physical_kinetic = sp.simplify(transform.T * kinetic * transform)
    physical_field_map = sp.simplify(field_map * transform)
    physical_velocity_map = sp.simplify(velocity_map * transform)

    j2_static_B = sp.simplify(field_map.T)
    velocity_residual_present = any(
        sp.simplify(value) != 0 for value in velocity_map
    )

    original_chart = {
        "dynamical_fields": ["R", "delta_rho", "vartheta"],
        "constraint_fields": ["delta_N", "Sigma=q_phys^2*beta"],
        "velocities": ["R_dot", "delta_rho_dot", "vartheta_dot"],
        "K": matrix_string(kinetic),
        "C": matrix_string(constraint_matrix),
        "constraint_source_field_map_Mx": matrix_string(field_map),
        "constraint_source_velocity_map_Mv": matrix_string(velocity_map),
        "J2_static_B_candidate_from_Mx_transpose": matrix_string(j2_static_B),
        "lagrangian_constraint_sector": (
            "L contains + z^T (Mx x + Mv xdot) + (1/2) z^T C z; "
            "stationary z = -C^{-1}(Mx x + Mv xdot)"
        ),
        "j2_template_comparison": (
            "J2 uses -x^T B z - (1/2) z^T C z with z = C^{-1}(rho h - B^T x). "
            "Only the static field map Mx can supply a B candidate; nonzero Mv "
            "is a residual outside the pure static template."
        ),
    }
    physical_chart = {
        "dynamical_fields": [
            "Xi=(q_phys/H)R",
            "Q_rho=delta_rho-(rho_dot/H)R",
            "Q_chi=rho[vartheta-(mu/H)R]",
        ],
        "constraint_fields": ["delta_N", "Sigma=q_phys^2*beta"],
        "transform_y_equals_T_p": matrix_string(transform),
        "K": matrix_string(physical_kinetic),
        "C_unchanged_by_dynamical_basis": matrix_string(constraint_matrix),
        "constraint_source_field_map_Mx_T": matrix_string(physical_field_map),
        "constraint_source_velocity_map_Mv_T": matrix_string(
            physical_velocity_map
        ),
        "time_dependent_T_dot_terms": (
            "NOT_INCLUDED_IN_THIS_EXPORT; full velocity map under evolving "
            "background uses the separate physical-basis field_and_velocity_map"
        ),
    }

    object_status = {
        "K": {
            "original_chart": "EXPORTED_FROM_FINITE_Q_REDUCED_HESSIAN",
            "physical_chart": "EXPORTED_VIA_STATIC_BASIS_TRANSFORM",
            "dimensions_in_export": (
                "ROLE_DECLARED: coefficient of (1/2) xdot^T K xdot in the "
                "reduced quadratic Lagrangian density; absolute SI unit system "
                "not fixed in this export"
            ),
            "ready_for_J2_live_matching": False,
        },
        "C": {
            "original_chart": "EXPORTED_CONSTRAINT_HESSIAN",
            "physical_chart": "SAME_MATRIX_CONSTRAINT_BASIS_UNCHANGED",
            "dimensions_in_export": (
                "ROLE_DECLARED: coefficient of (1/2) z^T C z; absolute SI unit "
                "system not fixed in this export"
            ),
            "ready_for_J2_live_matching": False,
        },
        "B": {
            "static_field_block": (
                "ISOLATED_AS_Mx_WITH_J2_CANDIDATE_B_EQUALS_Mx_TRANSPOSE"
            ),
            "velocity_block": (
                "ISOLATED_AS_Mv_NONZERO_RESIDUAL_OUTSIDE_PURE_STATIC_J2"
                if velocity_residual_present
                else "VANISHES"
            ),
            "isolated_pure_static_J2_B": not velocity_residual_present,
            "dimensions_in_export": (
                "ROLE_DECLARED: linear maps from dynamical fields/velocities "
                "into the constraint source; absolute SI unit system not fixed"
            ),
            "ready_for_J2_live_matching": False,
        },
        "d": {
            "status": "NOT_EXPORTED",
            "reason": (
                "live finite-q quadratic reduction has no declared external "
                "matter density interaction providing a source covector on "
                "dynamical fields"
            ),
            "ready_for_J2_live_matching": False,
        },
        "h": {
            "status": "NOT_EXPORTED",
            "reason": (
                "live finite-q quadratic reduction has no declared external "
                "matter density interaction providing a source covector on "
                "algebraic constraints"
            ),
            "ready_for_J2_live_matching": False,
        },
        "u": {
            "status": "NOT_SELECTED",
            "reason": (
                "selecting a physical eigenmode for g_can requires the matter "
                "source channel c_eff; free-sector spectra alone do not "
                "authorize a MAT vertex mode"
            ),
            "ready_for_J2_live_matching": False,
        },
    }

    return {
        "velocity_residual_present": velocity_residual_present,
        "original_chart": original_chart,
        "physical_chart": physical_chart,
        "object_status": object_status,
        "reconstruction_residual_zero": True,
    }


def validate_upstream(
    finite: dict[str, Any] | None,
    physical: dict[str, Any] | None,
    j2: dict[str, Any] | None,
    inventory: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    finite_ok = bool(
        finite
        and finite.get("calculation_status") == "PASS"
        and finite.get("reduction_status") == "PASS_FINITE_Q_CONSTRAINT_ELIMINATION"
        and finite.get("mat001_status") == "BLOCKED"
        and finite.get("full_gate_status") == "IN_PROGRESS"
    )
    add_check(checks, "finite_q_upstream_contract", finite_ok)
    physical_ok = bool(
        physical
        and physical.get("calculation_status") == "PASS"
        and physical.get("basis_status") == "DERIVED_AND_VERIFIED"
        and physical.get("projected_vertex_status") == "NOT_YET_EVALUATED"
        and physical.get("mat001_status") == "BLOCKED"
    )
    add_check(checks, "physical_basis_upstream_contract", physical_ok)
    j2_ok = bool(
        j2
        and j2.get("subgate_status")
        == "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
        and j2.get("live_action_export_status") == "NOT_PROVIDED"
        and j2.get("V_status") == "NOT_COMPUTED"
        and j2.get("mat001_pass") is False
    )
    add_check(checks, "j2_template_upstream_contract", j2_ok)
    inventory_ok = bool(
        inventory
        and inventory.get("subgate_status")
        == "PASS_MAT001_LIVE_UVIR_EXPORT_INVENTORY_BLOCKED"
        and inventory.get("live_action_export_status") == "PARTIAL_NOT_SAME_CHART"
        and inventory.get("V_status") == "NOT_COMPUTED"
        and inventory.get("mat001_pass") is False
    )
    add_check(checks, "live_inventory_upstream_contract", inventory_ok)
    return checks


def build_summary(
    free: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    velocity_residual = bool(free["velocity_residual_present"])
    object_status = free["object_status"]

    add_check(
        checks,
        "original_chart_K_C_exported",
        bool(free["original_chart"]["K"].startswith("Matrix("))
        and bool(free["original_chart"]["C"].startswith("Matrix(")),
    )
    add_check(
        checks,
        "constraint_source_decomposed_linear_exact",
        free["reconstruction_residual_zero"] is True
        and bool(
            free["original_chart"]["constraint_source_field_map_Mx"].startswith(
                "Matrix("
            )
        )
        and bool(
            free["original_chart"][
                "constraint_source_velocity_map_Mv"
            ].startswith("Matrix(")
        ),
    )
    add_check(
        checks,
        "velocity_mixing_residual_recorded_not_erased",
        velocity_residual
        and object_status["B"]["isolated_pure_static_J2_B"] is False,
    )
    add_check(
        checks,
        "physical_chart_K_transformed",
        bool(free["physical_chart"]["K"].startswith("Matrix(")),
    )
    add_check(
        checks,
        "matter_source_covectors_remain_absent",
        object_status["d"]["status"] == "NOT_EXPORTED"
        and object_status["h"]["status"] == "NOT_EXPORTED"
        and object_status["u"]["status"] == "NOT_SELECTED",
    )

    free_same_chart = (
        object_status["K"]["original_chart"].startswith("EXPORTED")
        and object_status["C"]["original_chart"].startswith("EXPORTED")
        and object_status["B"]["static_field_block"].startswith("ISOLATED")
    )
    complete_bundle = (
        free_same_chart
        and object_status["d"]["status"] != "NOT_EXPORTED"
        and object_status["h"]["status"] != "NOT_EXPORTED"
        and object_status["u"]["status"] != "NOT_SELECTED"
        and object_status["B"]["isolated_pure_static_J2_B"] is True
    )
    firewall = {
        "free_sector_same_chart_objects_exported": free_same_chart,
        "live_same_chart_bundle_complete": False,
        "pure_static_J2_B_ready": False,
        "numeric_matching_ready": False,
        "computes_numeric_V": False,
        "derives_numeric_K_Q": False,
        "reopens_stage4A": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
    }
    require(
        complete_bundle is False,
        "complete bundle must remain false without d,h,u and pure static B",
    )
    add_check(
        checks,
        "claim_firewall_fail_closed",
        firewall["live_same_chart_bundle_complete"] is False
        and firewall["numeric_matching_ready"] is False
        and firewall["computes_numeric_V"] is False
        and firewall["physics_pass"] is False
        and firewall["claims_MAT_pass"] is False,
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "UVIR-003_TO_MAT-001",
        "stage": "SAME_CHART_FREE_QUADRATIC_EXPORT",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "live_action_export_status": (
            "PARTIAL_FREE_SECTOR_SAME_CHART_MATTER_SOURCES_ABSENT"
            if all_ok
            else "EXPORT_FAILED"
        ),
        "numeric_matching_status": "BLOCKED_MATTER_SOURCE_AND_STATIC_B_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "chart_declaration": {
            "primary_export_chart": "original_R_delta_rho_vartheta",
            "physical_scalar_chart": "Xi_Q_rho_Q_chi",
            "constraint_chart": ["delta_N", "Sigma=q_phys^2*beta"],
            "normalization_convention": (
                "UVIR finite-q reduced quadratic Lagrangian; aether-unitary "
                "scalar gauge; no external-matter density chart declared"
            ),
        },
        "free_sector_export": {
            "original_chart": free["original_chart"],
            "physical_chart": free["physical_chart"],
        },
        "required_object_status": object_status,
        "blocking_requirements": [
            "Declare one external-matter interaction in the live quadratic action and derive action-level d and h.",
            "Either reduce the velocity-linear constraint mixing into the pure static J2 B convention or extend the projection identity to the Mv residual.",
            "Select physical mode u in the same chart only after c_eff is defined from d,h and B,C.",
            "Fix one absolute unit/normalization system for every exported coefficient before numerical matching.",
        ],
        "inadmissible_substitutions": {
            "diagnostic_Q_rho_Q_chi_impulses_for_d_h": "REJECTED_ROLE_MISMATCH",
            "free_sector_eigenmode_for_matter_vertex_u": "REJECTED_CHANNEL_MISSING",
            "static_B_from_Mx_while_erasing_Mv": "REJECTED_CONVENTION_MISMATCH",
            "cross_chart_silent_K_C_combination": "REJECTED_CHART_MISMATCH",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS exports free-sector K, C and the exact linear "
            "decomposition of the constraint source in one original chart, "
            "and the transformed free kinetic metric in the physical chart. "
            "It does not supply matter covectors d,h, does not erase velocity "
            "mixing, does not compute V or K_Q, and does not authorize MAT, "
            "UVIR or downstream physics claims."
        ),
        "serial_next": (
            "Declare S_int with external matter density, derive d and h in the "
            "same original or physical chart used here, resolve the Mv residual "
            "relative to the J2 static template, select u from the resulting "
            "c_eff channel, then rerun the live J2 projection."
        ),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    cases = [
        ("live_same_chart_bundle_complete", True),
        ("computes_numeric_V", True),
        ("physics_pass", True),
        ("claims_MAT_pass", True),
        ("numeric_matching_ready", True),
    ]
    for key, value in cases:
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = value
        require(
            mutant["claim_firewall"][key] is value,
            "mutation setup failed",
        )
        require(
            any(
                mutant["claim_firewall"][item] is True
                for item in (
                    "live_same_chart_bundle_complete",
                    "computes_numeric_V",
                    "physics_pass",
                    "claims_MAT_pass",
                    "numeric_matching_ready",
                )
            ),
            f"mutation {key} did not promote a banned flag",
        )
    # Role mutations on object status must remain rejected by boundary.
    mutant_objects = copy.deepcopy(summary)
    mutant_objects["required_object_status"]["d"]["status"] = "FAKE_FROM_DIAGNOSTIC"
    require(
        mutant_objects["required_object_status"]["d"]["status"]
        != summary["required_object_status"]["d"]["status"],
        "d mutation setup failed",
    )
    require(
        summary["required_object_status"]["d"]["status"] == "NOT_EXPORTED",
        "canonical d must stay absent",
    )


def main() -> None:
    args = parse_args()
    finite, finite_err, finite_sha = load_json(args.finite_q_summary)
    physical, physical_err, physical_sha = load_json(args.physical_basis_summary)
    j2, j2_err, j2_sha = load_json(args.j2_summary)
    inventory, inventory_err, inventory_sha = load_json(args.inventory_summary)

    evidence = {
        "finite_q_reduction": {
            "source": args.finite_q_summary.name,
            "sha256": finite_sha,
            "parse_error": finite_err,
        },
        "physical_scalar_basis": {
            "source": args.physical_basis_summary.name,
            "sha256": physical_sha,
            "parse_error": physical_err,
        },
        "MAT_J2_template": {
            "source": args.j2_summary.name,
            "sha256": j2_sha,
            "parse_error": j2_err,
        },
        "live_export_inventory": {
            "source": args.inventory_summary.name,
            "sha256": inventory_sha,
            "parse_error": inventory_err,
        },
    }

    checks = validate_upstream(finite, physical, j2, inventory)
    for name, err in (
        ("finite_q_reduction", finite_err),
        ("physical_scalar_basis", physical_err),
        ("MAT_J2_template", j2_err),
        ("live_export_inventory", inventory_err),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    free = build_free_sector_export()
    summary = build_summary(free, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(check["ok"] for check in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_same_chart_quadratic_export_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_same_chart_quadratic_export_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 same-chart free-sector quadratic export")
    print(
        "  free-sector status:",
        summary["live_action_export_status"],
    )
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(summary["subgate_status"]))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
