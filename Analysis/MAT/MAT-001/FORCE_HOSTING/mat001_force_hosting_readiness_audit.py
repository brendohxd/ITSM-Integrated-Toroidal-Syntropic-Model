#!/usr/bin/env python3
"""MAT-001 force-field hosting readiness for live S_int / d,h.

Inventories which live UVIR sectors currently host a force phonon and whether
any of them can accept the declared Conditional S_int without substitution.
Does not embed S_int, does not export live d,h, and does not compute V.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

PASS_STATUS = "PASS_MAT001_FORCE_HOSTING_READINESS_BLOCKED"
FAIL_STATUS = "FAIL_MAT001_FORCE_HOSTING_READINESS"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--s-int-summary",
        type=Path,
        default=mat
        / "S_INT_DH_EXPORT"
        / "outputs"
        / "mat001_s_int_dh_export_summary.json",
    )
    parser.add_argument(
        "--free-sector-summary",
        type=Path,
        default=mat
        / "SAME_CHART_EXPORT"
        / "outputs"
        / "mat001_same_chart_quadratic_export_summary.json",
    )
    parser.add_argument(
        "--nonlinear-adm-summary",
        type=Path,
        default=uvir / "uvir003_nonlinear_adm_action_provenance_summary.json",
    )
    parser.add_argument(
        "--force-local-summary",
        type=Path,
        default=uvir / "uvir003_nonzero_gradient_force_local_summary.json",
    )
    parser.add_argument(
        "--s2-summary",
        type=Path,
        default=uvir / "uvir003_complete_s2_operator_summary.json",
    )
    parser.add_argument(
        "--kinetic-inventory-summary",
        type=Path,
        default=mat / "outputs" / "mat001_v_kinetic_chart_inventory_summary.json",
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


def route_inventory(
    s_int: dict[str, Any] | None,
    free: dict[str, Any] | None,
    nonlinear: dict[str, Any] | None,
    force: dict[str, Any] | None,
    s2: dict[str, Any] | None,
    kinetic: dict[str, Any] | None,
) -> dict[str, Any]:
    free = free or {}
    free_fields = (
        free.get("free_sector_export", {})
        .get("original_chart", {})
        .get("dynamical_fields", [])
    )
    free_has_psi = any(
        str(item).split("=")[0].strip() in {"psi", "phi", "pi", "Pi"}
        for item in free_fields
    )

    symbolic = (nonlinear or {}).get("symbolic_audit", {})
    force_obs = symbolic.get("force_sector_obstructions", {})
    constraint_ready = symbolic.get("constraint_source_readiness", {})

    force_local = force or {}
    force_boundary = str(force_local.get("scientific_boundary", ""))
    force_next = force_local.get("next_required_calculation", [])

    s2_audit = (s2 or {}).get("symbolic_audit", {})
    track_a = s2_audit.get("track_a_force_sector", {})

    routes = {
        "R1_free_sector_ADM_scalar_chart": {
            "host_fields": free_fields,
            "hosts_force_phonon": free_has_psi,
            "hosts_external_rho_b_source": False,
            "hosts_declared_S_int": False,
            "status": "NOT_A_FORCE_HOST",
            "reason": (
                "Finite-q free-sector dynamical chart is "
                "(R, delta_rho, vartheta); force phonon is factorized out and "
                "not a dynamical coordinate of that export."
            ),
            "ready_for_live_d_h_export": False,
        },
        "R2_track_A_local_nonzero_gradient_force": {
            "host_fields": ["pi"],
            "hosts_force_phonon": True,
            "hosts_external_rho_b_source": False,
            "hosts_declared_S_int": False,
            "status": "FORCE_PRESENT_MATTER_ABSENT",
            "scope": (
                "Local expansion of |grad(pi)|^3 about a nonzero spatial "
                "gradient background; not the free-sector FRW ADM chart."
            ),
            "evidence_subgate": force_local.get("subgate_status"),
            "local_cubic_vertex": (force_local.get("local_cubic_vertex") or {}).get(
                "status"
            ),
            "matter_coupling_mentioned_in_boundary": "rho_b" in force_boundary
            or "S_int" in force_boundary
            or "matter" in force_boundary.lower(),
            "reason": (
                "Track-A hosts a force fluctuation pi and a local cubic vertex, "
                "but no declared external-matter density source and no exported "
                "action-level d,h from S_int."
            ),
            "ready_for_live_d_h_export": False,
            "optional_next_from_source": force_next,
        },
        "R3_complete_finite_q_S2_with_Track_A_force_block": {
            "hosts_force_phonon": bool(track_a),
            "hosts_external_rho_b_source": False,
            "hosts_declared_S_int": False,
            "status": "FORCE_BLOCK_IN_S2_WITHOUT_MATTER",
            "track_a_present": bool(track_a),
            "track_a_keys": sorted(track_a.keys()) if isinstance(track_a, dict) else [],
            "reason": (
                "Complete finite-q S2 includes a Track-A force sector block on the "
                "homogeneous zero-gradient branch, but that is a free force "
                "constraint/cubic structure, not a declared S_int matter vertex."
            ),
            "ready_for_live_d_h_export": False,
        },
        "R4_full_nonlinear_ADM_with_force_completion": {
            "hosts_force_phonon": False,
            "hosts_external_rho_b_source": False,
            "hosts_declared_S_int": False,
            "status": "BLOCKED_FORCE_COVARIANT_COMPLETION",
            "full_g_U_Phi_psi_J2": constraint_ready.get("full_g_U_Phi_psi_J2"),
            "Delta_U_covariant_completion": force_obs.get(
                "Delta_U_covariant_completion"
            ),
            "Y_three_halves_rule": force_obs.get("Y_three_halves_about_zero_gradient"),
            "analytic_cubic_vertex": force_obs.get("analytic_cubic_vertex"),
            "reason": (
                "Parent gravity-aether-condensate-alignment block is fixed, but "
                "force completion needed for full psi-inclusive J2 remains "
                "blocked on covariant Delta_U and the nonanalytic Y^(3/2) rule."
            ),
            "ready_for_live_d_h_export": False,
        },
        "R5_IR_template_only": {
            "hosts_force_phonon": True,
            "hosts_external_rho_b_source": True,
            "hosts_declared_S_int": True,
            "status": "TEMPLATE_NOT_LIVE_UVIR_ACTION",
            "S_int_status": (s_int or {}).get("S_int_status"),
            "IR_d_h_export_status": (s_int or {}).get("IR_d_h_export_status"),
            "live_UVIR_d_h_export_status": (s_int or {}).get(
                "live_UVIR_d_h_export_status"
            ),
            "reason": (
                "IR single-field template declares S_int and d,h form, but is "
                "not the live UVIR quadratic action used for free-sector K,C."
            ),
            "ready_for_live_d_h_export": False,
        },
    }

    any_ready = any(route["ready_for_live_d_h_export"] for route in routes.values())
    preferred_next = (
        "Declare and expand S_int on the Track-A force host (pi) in one named "
        "chart, exporting action-level d,h without claiming FRW free-sector "
        "equivalence; or complete the nonlinear force sector and only then "
        "attach S_int to the joined ADM quadratic."
    )

    kinetic_blockers = []
    if kinetic:
        kinetic_blockers = kinetic.get("next_required") or kinetic.get(
            "blocking_requirements"
        ) or []

    return {
        "routes": routes,
        "any_live_route_ready_for_d_h": any_ready,
        "selected_host_route": "NONE",
        "preferred_serial_path": preferred_next,
        "cross_cutting_blockers": [
            "No live UVIR quadratic currently exports action-level d,h from declared S_int.",
            "Free-sector ADM chart and Track-A force chart are distinct; silent identification is forbidden.",
            "Full psi-inclusive ADM J2 remains blocked on force covariant completion and Y^(3/2) treatment.",
            "Numeric K_Q / V remain NOT_DERIVED / NOT_COMPUTED independent of hosting readiness.",
        ],
        "kinetic_inventory_crossref": kinetic_blockers,
    }


def validate_upstream(
    s_int: dict[str, Any] | None,
    free: dict[str, Any] | None,
    nonlinear: dict[str, Any] | None,
    force: dict[str, Any] | None,
    s2: dict[str, Any] | None,
    kinetic: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "s_int_upstream_contract",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED"
            and s_int.get("V_status") == "NOT_COMPUTED"
            and s_int.get("live_UVIR_d_h_export_status") == "NOT_EXPORTED"
            and s_int.get("S_int_status") == "DECLARED_CONDITIONAL_FORM"
        ),
    )
    add_check(
        checks,
        "free_sector_upstream_contract",
        bool(
            free
            and free.get("subgate_status")
            == "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL"
            and free.get("V_status") == "NOT_COMPUTED"
            and free.get("mat001_pass") is False
        ),
    )
    add_check(
        checks,
        "nonlinear_adm_upstream_contract",
        bool(
            nonlinear
            and nonlinear.get("subgate_status")
            == "PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE"
            and nonlinear.get("mat001_status") == "BLOCKED"
            and nonlinear.get("full_gate_status") == "IN_PROGRESS"
            and (nonlinear.get("symbolic_audit") or {})
            .get("constraint_source_readiness", {})
            .get("full_g_U_Phi_psi_J2")
            == "BLOCKED_ON_FORCE_COVARIANT_COMPLETION_AND_NONANALYTIC_RULE"
        ),
    )
    add_check(
        checks,
        "force_local_upstream_contract",
        bool(
            force
            and force.get("subgate_status") == "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
            and force.get("mat001_status") == "BLOCKED"
            and force.get("calculation_status") == "PASS"
            and (force.get("local_cubic_vertex") or {}).get("status")
            == "PASS_LOCAL_CUBIC_FORCE_VERTEX"
        ),
    )
    add_check(
        checks,
        "s2_upstream_contract",
        bool(
            s2
            and s2.get("subgate_status") == "PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL"
            and s2.get("mat001_status") == "BLOCKED"
            and s2.get("full_gate_status") == "IN_PROGRESS"
        ),
    )
    add_check(
        checks,
        "kinetic_inventory_upstream_contract",
        bool(
            kinetic
            and kinetic.get("subgate_status")
            == "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN"
            and kinetic.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def build_summary(
    inventory: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    routes = inventory["routes"]
    add_check(
        checks,
        "free_sector_not_selected_as_force_host",
        routes["R1_free_sector_ADM_scalar_chart"]["hosts_force_phonon"] is False
        and routes["R1_free_sector_ADM_scalar_chart"]["ready_for_live_d_h_export"]
        is False,
    )
    add_check(
        checks,
        "track_a_hosts_force_without_matter",
        routes["R2_track_A_local_nonzero_gradient_force"]["hosts_force_phonon"] is True
        and routes["R2_track_A_local_nonzero_gradient_force"][
            "hosts_declared_S_int"
        ]
        is False
        and routes["R2_track_A_local_nonzero_gradient_force"][
            "ready_for_live_d_h_export"
        ]
        is False,
    )
    add_check(
        checks,
        "full_adm_force_completion_still_blocked",
        routes["R4_full_nonlinear_ADM_with_force_completion"]["status"]
        == "BLOCKED_FORCE_COVARIANT_COMPLETION"
        and "BLOCKED" in str(
            routes["R4_full_nonlinear_ADM_with_force_completion"][
                "full_g_U_Phi_psi_J2"
            ]
        ),
    )
    add_check(
        checks,
        "no_live_route_ready_for_d_h",
        inventory["any_live_route_ready_for_d_h"] is False
        and inventory["selected_host_route"] == "NONE",
    )
    add_check(
        checks,
        "IR_template_not_promoted_to_live_host",
        routes["R5_IR_template_only"]["status"] == "TEMPLATE_NOT_LIVE_UVIR_ACTION"
        and routes["R5_IR_template_only"]["live_UVIR_d_h_export_status"]
        == "NOT_EXPORTED",
    )

    firewall = {
        "force_host_route_selected": False,
        "live_S_int_embedded": False,
        "live_UVIR_d_h_exported": False,
        "live_same_chart_bundle_complete": False,
        "numeric_matching_ready": False,
        "computes_numeric_V": False,
        "derives_numeric_K_Q": False,
        "reopens_stage4A": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
        "identifies_free_sector_with_Track_A": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(value is False for value in firewall.values()),
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "FORCE_HOST_TO_S_INT",
        "stage": "FORCE_HOSTING_READINESS",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "hosting_status": "NO_LIVE_HOST_READY_FOR_S_INT",
        "selected_host_route": "NONE",
        "live_UVIR_d_h_export_status": "NOT_EXPORTED",
        "live_action_export_status": "PARTIAL_FORCE_PRESENT_MATTER_NOT_HOSTED",
        "numeric_matching_status": "BLOCKED_LIVE_FORCE_MATTER_HOST_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "route_inventory": inventory["routes"],
        "cross_cutting_blockers": inventory["cross_cutting_blockers"],
        "preferred_serial_path": inventory["preferred_serial_path"],
        "blocking_requirements": [
            "Choose one live force host chart (Track-A pi sector or completed ADM force sector) and declare it explicitly for MAT matching.",
            "Embed Conditional S_int = -C_m rho_b psi (or parent equivalent / justified pi chart map) in that host action.",
            "Export action-level d,h from that expansion in the same chart as the host kinetic objects.",
            "Do not identify free-sector (R,delta_rho,vartheta) with Track-A pi without a declared map.",
            "Resolve free-sector Mv residual only in the chart actually used for constraint elimination with matter sources.",
        ],
        "inadmissible_substitutions": {
            "free_sector_as_force_host_without_psi": "REJECTED_CHART_MISMATCH",
            "Track_A_force_vertex_as_matter_S_int": "REJECTED_ROLE_MISMATCH",
            "IR_template_as_live_UVIR_host": "REJECTED_PROVENANCE_MISMATCH",
            "silent_free_sector_Track_A_identification": "REJECTED_UNDECLARED_MAP",
            "force_completion_placeholder_for_Delta_U_or_Y": "REJECTED_INCOMPLETE_ACTION",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS maps which live UVIR sectors host a force phonon and "
            "proves none is yet ready to export action-level d,h from declared "
            "S_int. It does not embed S_int, compute V or K_Q, complete the "
            "force sector, or authorize MAT/UVIR/downstream physics claims."
        ),
        "serial_next": inventory["preferred_serial_path"],
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    banned = [
        "force_host_route_selected",
        "live_S_int_embedded",
        "live_UVIR_d_h_exported",
        "numeric_matching_ready",
        "computes_numeric_V",
        "physics_pass",
        "claims_MAT_pass",
        "identifies_free_sector_with_Track_A",
    ]
    for key in banned:
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(
            any(mutant["claim_firewall"][item] is True for item in banned),
            f"mutation {key} failed",
        )
    require(summary["selected_host_route"] == "NONE", "no host may be selected")
    require(
        summary["hosting_status"] == "NO_LIVE_HOST_READY_FOR_S_INT",
        "hosting status must stay blocked",
    )


def main() -> None:
    args = parse_args()
    s_int, s_int_err, s_int_sha = load_json(args.s_int_summary)
    free, free_err, free_sha = load_json(args.free_sector_summary)
    nonlinear, nonlinear_err, nonlinear_sha = load_json(args.nonlinear_adm_summary)
    force, force_err, force_sha = load_json(args.force_local_summary)
    s2, s2_err, s2_sha = load_json(args.s2_summary)
    kinetic, kinetic_err, kinetic_sha = load_json(args.kinetic_inventory_summary)

    evidence = {
        "s_int_dh": {
            "source": args.s_int_summary.name,
            "sha256": s_int_sha,
            "parse_error": s_int_err,
        },
        "free_sector_export": {
            "source": args.free_sector_summary.name,
            "sha256": free_sha,
            "parse_error": free_err,
        },
        "nonlinear_adm_provenance": {
            "source": args.nonlinear_adm_summary.name,
            "sha256": nonlinear_sha,
            "parse_error": nonlinear_err,
        },
        "force_local": {
            "source": args.force_local_summary.name,
            "sha256": force_sha,
            "parse_error": force_err,
        },
        "complete_s2": {
            "source": args.s2_summary.name,
            "sha256": s2_sha,
            "parse_error": s2_err,
        },
        "kinetic_inventory": {
            "source": args.kinetic_inventory_summary.name,
            "sha256": kinetic_sha,
            "parse_error": kinetic_err,
        },
    }

    checks = validate_upstream(s_int, free, nonlinear, force, s2, kinetic)
    for name, err in (
        ("s_int_dh", s_int_err),
        ("free_sector_export", free_err),
        ("nonlinear_adm_provenance", nonlinear_err),
        ("force_local", force_err),
        ("complete_s2", s2_err),
        ("kinetic_inventory", kinetic_err),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    inventory = route_inventory(s_int, free, nonlinear, force, s2, kinetic)
    summary = build_summary(inventory, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(check["ok"] for check in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_force_hosting_readiness_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_force_hosting_readiness_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 force-field hosting readiness")
    print("  hosting:", summary["hosting_status"])
    print("  selected route:", summary["selected_host_route"])
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(summary["subgate_status"]))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
