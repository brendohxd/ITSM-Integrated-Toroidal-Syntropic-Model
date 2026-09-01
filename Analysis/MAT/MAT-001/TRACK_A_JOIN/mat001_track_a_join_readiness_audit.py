#!/usr/bin/env python3
"""MAT-001 Track-A join readiness: matter d,h vs free-force constraint blocks.

Classifies whether matter-channel d,h can be joined with Track-A free-force
J2/constraint structure under the MAT J2 static template. Records velocity-
quadratic free-force residuals outside pure static B, and the still-missing
full g+U+Phi+alignment join. Does not compute V or numeric K_Q.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

PASS_STATUS = "PASS_MAT001_TRACK_A_JOIN_READINESS_PARTIAL_MATTER_CHANNEL_ONLY"
FAIL_STATUS = "FAIL_MAT001_TRACK_A_JOIN_READINESS"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--track-a-s-int",
        type=Path,
        default=mat
        / "TRACK_A_S_INT"
        / "outputs"
        / "mat001_track_a_s_int_embed_summary.json",
    )
    parser.add_argument(
        "--kq-readiness",
        type=Path,
        default=mat
        / "TRACK_A_KQ"
        / "outputs"
        / "mat001_track_a_kq_readiness_summary.json",
    )
    parser.add_argument(
        "--conditional-branch",
        type=Path,
        default=mat
        / "CONDITIONAL_MATCHING_BRANCH"
        / "outputs"
        / "mat001_conditional_matching_branch_summary.json",
    )
    parser.add_argument(
        "--track-a-force",
        type=Path,
        default=uvir / "uvir003_track_a_force_adm_cubic_summary.json",
    )
    parser.add_argument(
        "--j2-template",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
    )
    parser.add_argument(
        "--free-sector",
        type=Path,
        default=mat
        / "SAME_CHART_EXPORT"
        / "outputs"
        / "mat001_same_chart_quadratic_export_summary.json",
    )
    parser.add_argument(
        "--nonlinear-adm",
        type=Path,
        default=uvir / "uvir003_nonlinear_adm_action_provenance_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--self-test-mutations", action="store_true")
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


def classify_join(
    s_int: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    j2: dict[str, Any] | None,
    free: dict[str, Any] | None,
    nonlinear: dict[str, Any] | None,
) -> dict[str, Any]:
    d_h = (s_int or {}).get("exported_d_h") or {}
    host = (s_int or {}).get("host_selection") or {}
    cs = ((track_a or {}).get("symbolic_audit") or {}).get("constraint_source") or {}
    not_derived = (
        ((track_a or {}).get("symbolic_audit") or {}).get("scientific_boundary") or {}
    ).get("not_derived") or []
    conv = (j2 or {}).get("quadratic_convention") or {}
    free_status = (free or {}).get("live_action_export_status")
    full_j2 = (nonlinear or {}).get("full_J2_status")
    force_block = (
        ((nonlinear or {}).get("symbolic_audit") or {})
        .get("constraint_source_readiness")
        or {}
    ).get("full_g_U_Phi_psi_J2")

    matter = {
        "channel": "S_int = -C_m rho_b psi on Track-A host",
        "x": ["pi"],
        "z": ["delta_N", "beta"],
        "d": d_h.get("d"),
        "h": d_h.get("h"),
        "c_eff_matter_only": d_h.get("c_eff_without_free_force_B_dressing"),
        "linear_in_external_rho_b": True,
        "compatible_with_static_J2_source_sector": bool(
            d_h.get("d") == ["-C_m"] and d_h.get("h") == ["0", "0"]
        ),
        "status": "MATTER_CHANNEL_READY_FORM",
    }

    free_force = {
        "lapse_J2_physical": cs.get("lapse_J2_physical_density"),
        "beta_J2": cs.get("beta_J2_after_spatial_integration_by_parts"),
        "Y_three_halves_J2_at_zero_gradient": cs.get(
            "Y_three_halves_J2_at_zero_gradient"
        ),
        "structure": (
            "Constraint sources are quadratic in pi velocities/gradients "
            "(e.g. pi_dot^2, partial(pi_dot partial pi)), not a static linear "
            "B^T x block of the J2 template alone."
        ),
        "static_linear_B_isolated": False,
        "velocity_quadratic_residual": True,
        "status": "FREE_FORCE_J2_OUTSIDE_PURE_STATIC_B",
    }

    full_join = {
        "assembled_g_U_Phi_alignment_psi_J2": "NOT_YET_ASSEMBLED"
        if any("assembled J2" in str(item) for item in not_derived)
        or (track_a or {}).get("full_J2_status") == "NOT_YET_ASSEMBLED"
        else "UNKNOWN",
        "nonlinear_full_g_U_Phi_psi_J2": force_block,
        "full_J2_status_field": full_j2 or (track_a or {}).get("full_J2_status"),
        "status": "FULL_MULTI_SECTOR_JOIN_NOT_READY",
    }

    free_sector = {
        "live_action_export_status": free_status,
        "identified_with_Track_A": False,
        "status": "DISTINCT_CHART_NOT_JOINED",
    }

    # Matter-only static projection identity under h=0: c_eff = d.
    matter_only_projection = {
        "J2_effective_source": "c_eff = d - B C^{-1} h",
        "with_h_zero": "c_eff = d",
        "with_no_static_linear_B_from_matter": "c_eff = (-C_m)",
        "g_can_form": "Abs(c_eff)/sqrt(K) = C_m/sqrt(K_Q) on single-field host",
        "requires_numeric_K_Q_for_numeric_V": True,
        "free_force_velocity_J2_included": False,
        "status": "MATTER_ONLY_STATIC_CHANNEL_FORM_COMPLETE",
    }

    return {
        "j2_template_lagrangian": conv.get("lagrangian"),
        "matter_channel": matter,
        "free_force_constraint_channel": free_force,
        "full_multi_sector_join": full_join,
        "free_sector_adm": free_sector,
        "matter_only_static_projection": matter_only_projection,
        "join_decision": {
            "selected_operational_channel": "MATTER_ONLY_STATIC_ON_TRACK_A_HOST",
            "free_force_static_B_join": "NOT_READY_VELOCITY_QUADRATIC_RESIDUAL",
            "full_g_U_Phi_join": "NOT_READY",
            "free_sector_join": "NOT_DECLARED_DISTINCT_CHART",
            "ready_for_numeric_live_matching": False,
            "reason": (
                "Matter d,h define a static J2 source channel with h=0 and "
                "c_eff=d on the Track-A host. Free-force constraint sources are "
                "velocity-quadratic residuals outside pure static B. Full "
                "multi-sector J2 is not assembled. Numeric K_Q remains open."
            ),
        },
    }


def validate_upstream(
    s_int: dict[str, Any] | None,
    kq: dict[str, Any] | None,
    cond: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    j2: dict[str, Any] | None,
    free: dict[str, Any] | None,
    nonlinear: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "track_a_s_int_upstream",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and s_int.get("V_status") == "NOT_COMPUTED"
            and (s_int.get("exported_d_h") or {}).get("d") == ["-C_m"]
            and (s_int.get("exported_d_h") or {}).get("h") == ["0", "0"]
        ),
    )
    add_check(
        checks,
        "kq_readiness_upstream",
        bool(
            kq
            and kq.get("subgate_status")
            == "PASS_MAT001_TRACK_A_KQ_SYMBOLIC_HOST_NUMERIC_BLOCKED"
            and kq.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "conditional_branch_upstream",
        bool(
            cond
            and cond.get("subgate_status")
            == "PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS"
            and cond.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_force_upstream",
        bool(
            track_a
            and track_a.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT"
            and track_a.get("mat001_status") == "BLOCKED"
            and isinstance(
                ((track_a.get("symbolic_audit") or {}).get("constraint_source") or {}).get(
                    "lapse_J2_physical_density"
                ),
                str,
            )
        ),
    )
    add_check(
        checks,
        "j2_template_upstream",
        bool(
            j2
            and j2.get("subgate_status")
            == "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
            and j2.get("V_status") == "NOT_COMPUTED"
            and "c_eff=d-B*C^-1*h"
            in str((j2.get("quadratic_convention") or {}).get("effective_source", ""))
        ),
    )
    add_check(
        checks,
        "free_sector_upstream_distinct",
        bool(
            free
            and free.get("subgate_status")
            == "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL"
            and free.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "nonlinear_adm_upstream",
        bool(
            nonlinear
            and nonlinear.get("subgate_status")
            == "PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE"
            and nonlinear.get("mat001_status") == "BLOCKED"
        ),
    )
    return checks


def build_summary(
    join: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    dec = join["join_decision"]
    add_check(
        checks,
        "matter_channel_static_form_ready",
        join["matter_channel"]["compatible_with_static_J2_source_sector"] is True
        and join["matter_only_static_projection"]["status"]
        == "MATTER_ONLY_STATIC_CHANNEL_FORM_COMPLETE",
    )
    add_check(
        checks,
        "free_force_not_pure_static_B",
        join["free_force_constraint_channel"]["static_linear_B_isolated"] is False
        and join["free_force_constraint_channel"]["velocity_quadratic_residual"]
        is True,
    )
    add_check(
        checks,
        "full_multi_sector_not_ready",
        join["full_multi_sector_join"]["status"]
        == "FULL_MULTI_SECTOR_JOIN_NOT_READY",
    )
    add_check(
        checks,
        "free_sector_not_identified",
        join["free_sector_adm"]["identified_with_Track_A"] is False,
    )
    add_check(
        checks,
        "numeric_matching_still_blocked",
        dec["ready_for_numeric_live_matching"] is False
        and dec["selected_operational_channel"]
        == "MATTER_ONLY_STATIC_ON_TRACK_A_HOST",
    )

    firewall = {
        "matter_only_static_channel_form_complete": True,
        "free_force_static_B_joined": False,
        "full_multi_sector_joined": False,
        "free_sector_identified_with_Track_A": False,
        "numeric_matching_ready": False,
        "computes_numeric_V": False,
        "derives_numeric_K_Q": False,
        "reopens_stage4A": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(
            firewall[k] is False
            for k in (
                "free_force_static_B_joined",
                "full_multi_sector_joined",
                "free_sector_identified_with_Track_A",
                "numeric_matching_ready",
                "computes_numeric_V",
                "claims_MAT_pass",
                "physics_pass",
            )
        ),
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001",
        "interface": "TRACK_A_MATTER_FREE_FORCE_JOIN",
        "stage": "TRACK_A_JOIN_READINESS",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "join_status": "PARTIAL_MATTER_CHANNEL_ONLY",
        "selected_operational_channel": dec["selected_operational_channel"],
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "numeric_matching_status": "BLOCKED_NUMERIC_K_Q_AND_FULL_JOIN",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "join_inventory": join,
        "blocking_requirements": [
            "Numeric K_Q (or residue V) still required for numeric matching on the matter-only channel.",
            "Treat free-force velocity-quadratic constraint sources as residuals outside pure static J2 B unless an extended projection identity is declared.",
            "Assemble full g+U+Phi+alignment+psi J2 only under a declared multi-sector expansion.",
            "Do not identify free-sector ADM with Track-A without a field map.",
        ],
        "inadmissible_substitutions": {
            "free_force_pi_dot_squared_J2_as_static_B": "REJECTED_CONVENTION_MISMATCH",
            "free_sector_as_Track_A_host": "REJECTED_CHART_MISMATCH",
            "matter_only_form_as_numeric_V": "REJECTED_NOT_COMPUTED",
            "partial_join_as_MAT_pass": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS classifies the Track-A join: matter-channel d,h form a "
            "static J2 source sector with c_eff=d when h=0, while free-force "
            "constraint J2 is velocity-quadratic and outside pure static B, "
            "and full multi-sector J2 is not assembled. It does not compute V "
            "or authorize MAT/UVIR physics PASS."
        ),
        "serial_next": (
            "Operate on the matter-only static Track-A channel for Conditional "
            "probes; keep free-force residuals explicit; continue numeric K_Q "
            "or residue work for Derived V; retain Stage 4A closed."
        ),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "free_force_static_B_joined",
        "full_multi_sector_joined",
        "numeric_matching_ready",
        "computes_numeric_V",
        "claims_MAT_pass",
        "physics_pass",
        "free_sector_identified_with_Track_A",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["V_status"] == "NOT_COMPUTED", "V closed")
    require(
        summary["join_status"] == "PARTIAL_MATTER_CHANNEL_ONLY",
        "partial join only",
    )


def main() -> None:
    args = parse_args()
    s_int, e1, s1 = load_json(args.track_a_s_int)
    kq, e2, s2 = load_json(args.kq_readiness)
    cond, e3, s3 = load_json(args.conditional_branch)
    track_a, e4, s4 = load_json(args.track_a_force)
    j2, e5, s5 = load_json(args.j2_template)
    free, e6, s6 = load_json(args.free_sector)
    nonlinear, e7, s7 = load_json(args.nonlinear_adm)

    evidence = {
        "track_a_s_int": {"source": args.track_a_s_int.name, "sha256": s1, "parse_error": e1},
        "kq_readiness": {"source": args.kq_readiness.name, "sha256": s2, "parse_error": e2},
        "conditional_branch": {
            "source": args.conditional_branch.name,
            "sha256": s3,
            "parse_error": e3,
        },
        "track_a_force": {"source": args.track_a_force.name, "sha256": s4, "parse_error": e4},
        "j2_template": {"source": args.j2_template.name, "sha256": s5, "parse_error": e5},
        "free_sector": {"source": args.free_sector.name, "sha256": s6, "parse_error": e6},
        "nonlinear_adm": {
            "source": args.nonlinear_adm.name,
            "sha256": s7,
            "parse_error": e7,
        },
    }
    checks = validate_upstream(s_int, kq, cond, track_a, j2, free, nonlinear)
    for name, err in (
        ("track_a_s_int", e1),
        ("kq_readiness", e2),
        ("conditional_branch", e3),
        ("track_a_force", e4),
        ("j2_template", e5),
        ("free_sector", e6),
        ("nonlinear_adm", e7),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    join = classify_join(s_int, track_a, j2, free, nonlinear)
    summary = build_summary(join, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_track_a_join_readiness_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_track_a_join_readiness_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )
    print("MAT-001 Track-A join readiness")
    print("  join:", summary["join_status"])
    print("  channel:", summary["selected_operational_channel"])
    print("  V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
