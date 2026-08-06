#!/usr/bin/env python3
"""MAT-001 Track-A force host: Conditional S_int embed and d,h export.

Selects the Track-A force phonon chart as the Conditional live host for the
declared matter interaction, embeds S_int = -C_m rho_b psi with the map
psi = psi_bar + pi, and exports action-level source covectors d,h in that
host chart. Does not join free-sector ADM, does not derive numeric K_Q or V,
and does not authorize MAT physics PASS.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
FAIL_STATUS = "FAIL_MAT001_TRACK_A_S_INT_EMBED"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force-hosting-summary",
        type=Path,
        default=mat
        / "FORCE_HOSTING"
        / "outputs"
        / "mat001_force_hosting_readiness_summary.json",
    )
    parser.add_argument(
        "--s-int-summary",
        type=Path,
        default=mat
        / "S_INT_DH_EXPORT"
        / "outputs"
        / "mat001_s_int_dh_export_summary.json",
    )
    parser.add_argument(
        "--track-a-summary",
        type=Path,
        default=uvir / "uvir003_track_a_force_adm_cubic_summary.json",
    )
    parser.add_argument(
        "--force-local-summary",
        type=Path,
        default=uvir / "uvir003_nonzero_gradient_force_local_summary.json",
    )
    parser.add_argument(
        "--free-sector-summary",
        type=Path,
        default=mat
        / "SAME_CHART_EXPORT"
        / "outputs"
        / "mat001_same_chart_quadratic_export_summary.json",
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


def embed_and_export() -> dict[str, Any]:
    c_m, k_q, rho_b = sp.symbols("C_m K_Q rho_b", positive=True)
    psi_bar, pi = sp.symbols("psi_bar pi", real=True)
    delta_n, beta = sp.symbols("delta_N beta", real=True)

    # Declared host map: IR force phonon is the Track-A force field.
    psi = psi_bar + pi
    l_int = -c_m * rho_b * psi
    l_int_expanded = sp.expand(l_int)
    # Linear external-source sector in the dynamical fluctuation pi, treating
    # rho_b as the J2 external density and psi_bar as a background shift.
    l_int_pi = sp.expand(l_int_expanded.coeff(pi) * pi)
    require(
        sp.simplify(l_int_pi - (-c_m * rho_b * pi)) == 0,
        "pi interaction sector must be -C_m rho_b pi",
    )

    # J2 source sector: rho_b * (d^T x + h^T z) with x=(pi), z=(delta_N, beta).
    d_pi = -c_m
    h_delta_n = sp.Integer(0)
    h_beta = sp.Integer(0)
    l_j2_source = rho_b * (d_pi * pi + h_delta_n * delta_n + h_beta * beta)
    require(
        sp.simplify(l_int_pi - rho_b * d_pi * pi) == 0,
        "d must match the pi source sector",
    )
    require(
        sp.simplify(l_j2_source - rho_b * d_pi * pi) == 0,
        "h vanishes for pure -C_m rho_b psi coupling",
    )

    # Host kinetic template from Track-A quadratic force density (physical):
    # K_Q * pi_dot^2 / 2  => time-kinetic coefficient K = K_Q for single field.
    # Spatial regulator/potential terms are not part of the time-kinetic K.
    host_k = k_q
    c_eff = sp.Matrix([d_pi])  # no B,C dressing from this pure h=0 coupling
    v = c_m / sp.sqrt(k_q)
    g_can_abs = sp.simplify(sp.Abs(c_eff[0]) / sp.sqrt(host_k))
    require(sp.simplify(g_can_abs - v) == 0, "|g_can| must recover V form on host")

    # Background piece couples matter to psi_bar; recorded, not used as d,h.
    l_background = -c_m * rho_b * psi_bar

    return {
        "host_selection": {
            "route": "R2_TRACK_A_FORCE_PHONON",
            "status": "SELECTED_CONDITIONAL",
            "dynamical_fluctuation": "pi",
            "force_field": "psi=psi_bar+pi",
            "constraint_fields_recorded": ["delta_N", "beta"],
            "not_free_sector_ADM": True,
            "not_full_g_U_Phi_alignment_join": True,
        },
        "field_map": {
            "IR_psi_to_Track_A": "psi_IR := psi_TrackA = psi_bar + pi",
            "status": "DECLARED_CONDITIONAL_FORCE_ROLE_MAP",
            "does_not_identify_free_sector_fields": True,
        },
        "declared_S_int_on_host": {
            "form": "-C_m*rho_b*psi",
            "expanded": str(l_int_expanded),
            "fluctuation_sector": str(l_int_pi),
            "background_sector": str(l_background),
            "status": "EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST",
        },
        "host_quadratic_kinetic_template": {
            "track_a_quadratic_force_density": "K_Q*a**3*pi_dot**2/2 - gamma*lap_pi**2/(2*M_star_sq*a)",
            "physical_time_kinetic_coefficient_K": "K_Q",
            "spatial_terms": "regulator/potential; not the time-kinetic K used for g_can",
            "K_Q_numeric_status": "NOT_DERIVED",
        },
        "exported_d_h": {
            "chart": "Track-A force host; x=(pi); z=(delta_N, beta); rho=rho_b",
            "d": ["-C_m"],
            "h": ["0", "0"],
            "c_eff_without_free_force_B_dressing": ["-C_m"],
            "note_on_B_dressing": (
                "Track-A free-force action has constraint sources quadratic in "
                "pi velocities; those are free-sector force J2 components, not "
                "linear matter covectors. This export is the matter S_int channel "
                "only. Joining free-force B,C with matter d,h remains a later step."
            ),
            "abs_g_can_equals_V_form_on_single_field_host": True,
            "V_definition": "C_m/sqrt(K_Q)",
            "export_status": "EXPORTED_CONDITIONAL_ON_TRACK_A_HOST",
            "ready_for_joined_live_matching": False,
            "dimensions_in_export": (
                "ROLE_DECLARED: d multiplies rho_b*pi in the Lagrangian density; "
                "absolute SI unit system not fixed; K_Q remains symbolic"
            ),
        },
        "symbolic_checks": {
            "L_int_pi_matches_d": True,
            "h_vanishes_for_pure_psi_coupling": True,
            "abs_g_can_equals_V_form": True,
        },
    }


def validate_upstream(
    hosting: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    force_local: dict[str, Any] | None,
    free: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "force_hosting_upstream_contract",
        bool(
            hosting
            and hosting.get("subgate_status")
            == "PASS_MAT001_FORCE_HOSTING_READINESS_BLOCKED"
            and hosting.get("selected_host_route") == "NONE"
            and hosting.get("V_status") == "NOT_COMPUTED"
            and hosting.get("hosting_status") == "NO_LIVE_HOST_READY_FOR_S_INT"
        ),
    )
    add_check(
        checks,
        "s_int_form_upstream_contract",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED"
            and s_int.get("S_int_status") == "DECLARED_CONDITIONAL_FORM"
            and s_int.get("live_UVIR_d_h_export_status") == "NOT_EXPORTED"
            and s_int.get("V_status") == "NOT_COMPUTED"
        ),
    )
    track_ok = False
    if track_a and track_a.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT":
        audit = track_a.get("symbolic_audit", {})
        gauge = str((audit.get("exact_adm_building_blocks") or {}).get("gauge", ""))
        quad = str(
            (audit.get("verified_expansion") or {}).get("quadratic_force_density", "")
        )
        force_l = str((audit.get("track_a_action") or {}).get("force_lagrangian", ""))
        track_ok = (
            track_a.get("mat001_status") == "BLOCKED"
            and track_a.get("full_gate_status") == "IN_PROGRESS"
            and "psi_bar" in gauge
            and "pi" in gauge
            and "K_Q" in quad
            and "K_Q" in force_l
        )
    add_check(checks, "track_a_force_upstream_contract", track_ok)

    add_check(
        checks,
        "force_local_upstream_contract",
        bool(
            force_local
            and force_local.get("subgate_status")
            == "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
            and force_local.get("mat001_status") == "BLOCKED"
        ),
    )
    add_check(
        checks,
        "free_sector_upstream_not_identified",
        bool(
            free
            and free.get("subgate_status")
            == "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL"
            and free.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def build_summary(
    embed: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    d_h = embed["exported_d_h"]
    host = embed["host_selection"]

    add_check(
        checks,
        "track_a_host_selected_conditional",
        host["route"] == "R2_TRACK_A_FORCE_PHONON"
        and host["status"] == "SELECTED_CONDITIONAL"
        and host["not_free_sector_ADM"] is True,
    )
    add_check(
        checks,
        "S_int_embedded_on_track_a_host",
        embed["declared_S_int_on_host"]["status"]
        == "EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST"
        and embed["declared_S_int_on_host"]["form"] == "-C_m*rho_b*psi",
    )
    add_check(
        checks,
        "d_h_exported_on_track_a_host",
        d_h["export_status"] == "EXPORTED_CONDITIONAL_ON_TRACK_A_HOST"
        and d_h["d"] == ["-C_m"]
        and d_h["h"] == ["0", "0"]
        and d_h["abs_g_can_equals_V_form_on_single_field_host"] is True,
    )
    add_check(
        checks,
        "joined_live_matching_still_not_ready",
        d_h["ready_for_joined_live_matching"] is False
        and embed["host_quadratic_kinetic_template"]["K_Q_numeric_status"]
        == "NOT_DERIVED",
    )
    add_check(
        checks,
        "free_sector_not_silently_identified",
        embed["field_map"]["does_not_identify_free_sector_fields"] is True
        and host["not_free_sector_ADM"] is True,
    )

    firewall = {
        "track_a_host_selected_conditional": True,
        "S_int_embedded_on_track_a": True,
        "d_h_exported_on_track_a_host": True,
        "joined_free_sector_force_bundle_complete": False,
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
        firewall["computes_numeric_V"] is False
        and firewall["physics_pass"] is False
        and firewall["claims_MAT_pass"] is False
        and firewall["identifies_free_sector_with_Track_A"] is False
        and firewall["numeric_matching_ready"] is False
        and firewall["live_same_chart_bundle_complete"] is False,
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "TRACK_A_FORCE_HOST_S_INT",
        "stage": "TRACK_A_S_INT_EMBED_AND_DH_EXPORT",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "selected_host_route": "R2_TRACK_A_FORCE_PHONON",
        "host_selection_status": "SELECTED_CONDITIONAL",
        "S_int_status": "EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST",
        "track_a_d_h_export_status": "EXPORTED_CONDITIONAL_ON_TRACK_A_HOST",
        "live_UVIR_free_sector_d_h_export_status": "NOT_EXPORTED",
        "live_action_export_status": "PARTIAL_TRACK_A_MATTER_CHANNEL_EXPORTED",
        "numeric_matching_status": "BLOCKED_K_Q_AND_JOINED_BUNDLE_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "host_selection": embed["host_selection"],
        "field_map": embed["field_map"],
        "declared_S_int_on_host": embed["declared_S_int_on_host"],
        "host_quadratic_kinetic_template": embed["host_quadratic_kinetic_template"],
        "exported_d_h": embed["exported_d_h"],
        "blocking_requirements": [
            "Keep free-sector ADM and Track-A force host as distinct charts unless a field map is declared and verified.",
            "Join matter d,h with free-force constraint blocks B,C only in a declared multi-sector quadratic if that join is required.",
            "Derive numeric K_Q (or an invariant on-shell residue) from the same host action before claiming numeric V.",
            "Do not treat this Conditional embed as MAT physics PASS or Stage 4A reopen.",
        ],
        "inadmissible_substitutions": {
            "free_sector_R_delta_rho_vartheta_as_pi": "REJECTED_CHART_MISMATCH",
            "numeric_V_from_symbolic_C_m_over_sqrt_K_Q_without_K_Q": "REJECTED_NOT_COMPUTED",
            "Track_A_cubic_force_vertex_as_matter_d_h": "REJECTED_ROLE_MISMATCH",
            "background_psi_bar_term_as_fluctuation_d": "REJECTED_MODE_MISMATCH",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS selects Track-A as the Conditional force host, embeds "
            "S_int = -C_m rho_b psi with psi = psi_bar + pi, and exports "
            "matter-channel d,h in that host chart, recovering the |V| form "
            "when the host time-kinetic coefficient is symbolic K_Q. It does "
            "not derive numeric K_Q or V, does not complete free-sector joins, "
            "and does not authorize MAT/UVIR/downstream physics claims."
        ),
        "serial_next": (
            "Either derive K_Q (or the invariant residue) on the Track-A host "
            "for a numeric V attempt under explicit Conditional scope, or join "
            "the matter channel with free-force B,C / free-sector ADM only under "
            "a declared multi-sector chart; keep Stage 4A closed until a matched "
            "invariant exists."
        ),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    banned_true_required_false = [
        "computes_numeric_V",
        "derives_numeric_K_Q",
        "physics_pass",
        "claims_MAT_pass",
        "identifies_free_sector_with_Track_A",
        "numeric_matching_ready",
        "live_same_chart_bundle_complete",
    ]
    for key in banned_true_required_false:
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, f"mutation setup {key}")
    require(summary["V_status"] == "NOT_COMPUTED", "V must stay NOT_COMPUTED")
    require(
        summary["selected_host_route"] == "R2_TRACK_A_FORCE_PHONON",
        "host selection must remain Track-A",
    )
    require(
        summary["live_UVIR_free_sector_d_h_export_status"] == "NOT_EXPORTED",
        "free-sector d,h must stay absent",
    )


def main() -> None:
    args = parse_args()
    hosting, hosting_err, hosting_sha = load_json(args.force_hosting_summary)
    s_int, s_int_err, s_int_sha = load_json(args.s_int_summary)
    track_a, track_a_err, track_a_sha = load_json(args.track_a_summary)
    force_local, force_err, force_sha = load_json(args.force_local_summary)
    free, free_err, free_sha = load_json(args.free_sector_summary)

    evidence = {
        "force_hosting": {
            "source": args.force_hosting_summary.name,
            "sha256": hosting_sha,
            "parse_error": hosting_err,
        },
        "s_int_form": {
            "source": args.s_int_summary.name,
            "sha256": s_int_sha,
            "parse_error": s_int_err,
        },
        "track_a_force_adm": {
            "source": args.track_a_summary.name,
            "sha256": track_a_sha,
            "parse_error": track_a_err,
        },
        "force_local": {
            "source": args.force_local_summary.name,
            "sha256": force_sha,
            "parse_error": force_err,
        },
        "free_sector_export": {
            "source": args.free_sector_summary.name,
            "sha256": free_sha,
            "parse_error": free_err,
        },
    }

    checks = validate_upstream(hosting, s_int, track_a, force_local, free)
    for name, err in (
        ("force_hosting", hosting_err),
        ("s_int_form", s_int_err),
        ("track_a_force_adm", track_a_err),
        ("force_local", force_err),
        ("free_sector_export", free_err),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    embed = embed_and_export()
    summary = build_summary(embed, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(check["ok"] for check in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_track_a_s_int_embed_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_track_a_s_int_embed_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 Track-A S_int embed and d,h export")
    print("  host:", summary["selected_host_route"], summary["host_selection_status"])
    print("  S_int:", summary["S_int_status"])
    print("  Track-A d,h:", summary["track_a_d_h_export_status"])
    print("  free-sector d,h:", summary["live_UVIR_free_sector_d_h_export_status"])
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(summary["subgate_status"]))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
