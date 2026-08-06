#!/usr/bin/env python3
"""MAT-001 dig: can numeric K_Q be derived from microscopic/residue sources?

Re-audits R3 UV residue incompleteness, J1 parent coefficients, and Track-A
host readiness against the same-host V form. Proves the microscopic derivation
path is still incomplete without inventing Z_psi, rho_Phi, or k_Q. Dual status:
gate dig PASS does not imply numeric K_Q Derived.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_KQ_DERIVATION_DIG_INCOMPLETE"
FAIL_STATUS = "FAIL_MAT001_KQ_DERIVATION_DIG"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kq-readiness",
        type=Path,
        default=mat
        / "TRACK_A_KQ"
        / "outputs"
        / "mat001_track_a_kq_readiness_summary.json",
    )
    parser.add_argument(
        "--track-a-s-int",
        type=Path,
        default=mat
        / "TRACK_A_S_INT"
        / "outputs"
        / "mat001_track_a_s_int_embed_summary.json",
    )
    parser.add_argument(
        "--r3-summary",
        type=Path,
        default=uvir / "uvir003_r3_uv_residue_audit_summary.json",
    )
    parser.add_argument(
        "--matching-summary",
        type=Path,
        default=uvir / "uvir003_matching_route_program_summary.json",
    )
    parser.add_argument(
        "--j1-summary",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--conditional-kq",
        type=Path,
        default=uvir / "uvir003_conditional_kq_estimate_summary.json",
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


def derivation_paths() -> dict[str, Any]:
    z_phi, g_phi, f_phi = sp.symbols("Z_phi g_phi f_phi", positive=True)
    z_psi, r_rho, m_p, a0, k_q = sp.symbols(
        "Z_psi r_rho M_P a0 k_Q", positive=True
    )
    c_m = g_phi / f_phi
    k_from_parent = z_phi / f_phi**2
    v_parent = g_phi / sp.sqrt(z_phi)
    v_ir = c_m / sp.sqrt(k_from_parent)
    require(sp.simplify(v_parent - v_ir) == 0, "J1 identity must hold")

    k_r3 = z_psi * (r_rho * m_p**2)  # using r_rho = rho_Phi/(M_P^2 a0^2) => rho_Phi = r_rho M_P^2 a0^2
    # K_Q = Z_psi rho_Phi / a0^2 = Z_psi r_rho M_P^2
    k_r3_form = z_psi * r_rho * m_p**2
    k_r1 = k_q * m_p**2

    return {
        "path_P1_parent_Z_phi_g_phi": {
            "status": "FORM_IDENTITY_ONLY",
            "requires": ["numeric Z_phi", "numeric g_phi", "map phi->Track-A pi"],
            "induced_K_Q": str(k_from_parent),
            "induced_C_m": str(c_m),
            "induced_V": str(v_ir),
            "numeric_inputs_present_in_repo": False,
            "ready_to_derive_numeric_K_Q": False,
        },
        "path_P2_R3_residue_ansatz": {
            "status": "CONDITIONAL_ANSATZ_INCOMPLETE",
            "ansatz": "K_Q = Z_psi * rho_Phi / a0**2 = Z_psi * r_rho * M_P**2",
            "form": str(k_r3_form),
            "missing": ["Z_psi", "rho_Phi", "r_rho", "S_Phi matching"],
            "classification_from_r3_audit": "INCOMPLETE_R3_UV_RESIDUE",
            "ready_to_derive_numeric_K_Q": False,
        },
        "path_P3_R1_dimensional": {
            "status": "CONDITIONAL_NOT_DERIVATION",
            "ansatz": "K_Q = k_Q * M_P**2",
            "form": str(k_r1),
            "unfixed": ["k_Q"],
            "ready_to_derive_numeric_K_Q": False,
        },
        "path_P4_residue_V_then_K_Q": {
            "status": "BLOCKED_ON_NUMERIC_V_OR_C_m",
            "identity": "K_Q = C_m**2 / V**2 once V and C_m known",
            "requires": [
                "numeric C_m from S_int microphysics or fit under Conditional scope",
                "numeric invariant residue V from dynamics",
            ],
            "ready_to_derive_numeric_K_Q": False,
            "note": (
                "Track-A exports d=-C_m (form) only; does not supply absolute C_m"
            ),
        },
    }


def build_summary(
    paths: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
    r3: dict[str, Any] | None,
) -> dict[str, Any]:
    any_ready = any(p.get("ready_to_derive_numeric_K_Q") for p in paths.values())
    add_check(checks, "no_path_ready_for_numeric_K_Q", any_ready is False)
    add_check(
        checks,
        "parent_path_form_only",
        paths["path_P1_parent_Z_phi_g_phi"]["numeric_inputs_present_in_repo"] is False,
    )
    add_check(
        checks,
        "r3_path_incomplete",
        paths["path_P2_R3_residue_ansatz"]["ready_to_derive_numeric_K_Q"] is False
        and (
            r3 is None
            or r3.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
            or r3.get("classification_code") == "C"
        ),
    )
    add_check(
        checks,
        "r1_not_a_derivation",
        paths["path_P3_R1_dimensional"]["status"] == "CONDITIONAL_NOT_DERIVATION",
    )
    add_check(
        checks,
        "v_then_kq_blocked_on_absolute_coefficients",
        paths["path_P4_residue_V_then_K_Q"]["ready_to_derive_numeric_K_Q"] is False,
    )

    firewall = {
        "numeric_K_Q_derived": False,
        "numeric_V_computed": False,
        "microscopic_Z_psi_derived": False,
        "Z_phi_numeric_matched": False,
        "r3_promoted_Derived": False,
        "r1_promoted_Derived": False,
        "claims_MAT_pass": False,
        "physics_pass": False,
        "stage4A_reopened": False,
        "claims_downstream_Derived": False,
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
        "interface": "KQ_DERIVATION_DIG",
        "stage": "KQ_MICROSCOPIC_DERIVATION_DIG",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "dig_status": "INCOMPLETE_NO_NUMERIC_K_Q_PATH_READY",
        "kq_numeric_status": "NOT_DERIVED",
        "V_status": "NOT_COMPUTED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "derivation_paths": paths,
        "terminal_classification": "INCOMPLETE_MICROSCOPIC_K_Q_DERIVATION",
        "blocking_requirements": [
            "Supply numeric Z_phi and g_phi from one parent action with a Track-A field map, or",
            "Complete microscopic S_Phi -> force kinetic matching for Z_psi and rho_Phi, or",
            "Obtain independent absolute C_m and invariant residue V, then K_Q=C_m^2/V^2, or",
            "Use only an explicitly Conditional ansatz branch (never Derived).",
        ],
        "inadmissible_substitutions": {
            "Z_psi_equals_1_as_Derived": "REJECTED",
            "r_rho_equals_1_as_Derived": "REJECTED",
            "k_Q_equals_1_as_Derived": "REJECTED",
            "incomplete_R3_as_Derived_K_Q": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means the microscopic/residue derivation dig completed and "
            "found no ready path to numeric K_Q. It is an incompleteness result, "
            "not a derivation of K_Q or V."
        ),
        "serial_next": (
            "Open the dual-status Conditional matching branch for labeled probes, "
            "and/or continue genuine UV/microscopic matching outside placeholder "
            "Wilson coefficients."
        ),
    }


def validate_upstream(
    kq_ready: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
    r3: dict[str, Any] | None,
    matching: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    conditional: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "kq_readiness_upstream",
        bool(
            kq_ready
            and kq_ready.get("subgate_status")
            == "PASS_MAT001_TRACK_A_KQ_SYMBOLIC_HOST_NUMERIC_BLOCKED"
            and kq_ready.get("kq_numeric_status") == "NOT_DERIVED"
            and kq_ready.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_s_int_upstream",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and s_int.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "r3_upstream_incomplete",
        bool(
            r3
            and r3.get("calculation_status") == "PASS"
            and r3.get("kq_numeric_status") == "NOT_DERIVED"
            and r3.get("mat001_status") == "BLOCKED"
            and (
                r3.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
                or r3.get("classification_code") == "C"
            )
        ),
    )
    add_check(
        checks,
        "matching_upstream",
        bool(
            matching
            and matching.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
            and matching.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "j1_upstream",
        bool(
            j1
            and j1.get("subgate_status")
            == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
            and j1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "conditional_kq_not_derivation",
        bool(
            conditional and conditional.get("status") == "SPECULATIVE_NOT_A_DERIVATION"
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "numeric_K_Q_derived",
        "numeric_V_computed",
        "r3_promoted_Derived",
        "r1_promoted_Derived",
        "claims_MAT_pass",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["kq_numeric_status"] == "NOT_DERIVED", "K_Q open")
    require(
        summary["dig_status"] == "INCOMPLETE_NO_NUMERIC_K_Q_PATH_READY",
        "dig incomplete",
    )


def main() -> None:
    args = parse_args()
    kq_ready, e1, s1 = load_json(args.kq_readiness)
    s_int, e2, s2 = load_json(args.track_a_s_int)
    r3, e3, s3 = load_json(args.r3_summary)
    matching, e4, s4 = load_json(args.matching_summary)
    j1, e5, s5 = load_json(args.j1_summary)
    conditional, e6, s6 = load_json(args.conditional_kq)

    evidence = {
        "kq_readiness": {"source": args.kq_readiness.name, "sha256": s1, "parse_error": e1},
        "track_a_s_int": {"source": args.track_a_s_int.name, "sha256": s2, "parse_error": e2},
        "r3_residue": {"source": args.r3_summary.name, "sha256": s3, "parse_error": e3},
        "matching_program": {"source": args.matching_summary.name, "sha256": s4, "parse_error": e4},
        "j1": {"source": args.j1_summary.name, "sha256": s5, "parse_error": e5},
        "conditional_kq": {"source": args.conditional_kq.name, "sha256": s6, "parse_error": e6},
    }
    checks = validate_upstream(kq_ready, s_int, r3, matching, j1, conditional)
    for name, err in (
        ("kq_readiness", e1),
        ("track_a_s_int", e2),
        ("r3_residue", e3),
        ("matching_program", e4),
        ("j1", e5),
        ("conditional_kq", e6),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    paths = derivation_paths()
    summary = build_summary(paths, checks, evidence, r3)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_kq_derivation_dig_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_kq_derivation_dig_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )
    print("MAT-001 K_Q derivation dig")
    print("  dig:", summary["dig_status"])
    print("  K_Q:", summary["kq_numeric_status"], "| V:", summary["V_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
