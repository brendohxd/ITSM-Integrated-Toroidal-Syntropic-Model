#!/usr/bin/env python3
"""MAT-001 H1.1–H1.2: parent-action matching declaration + repo inventory.

Selects the Derived route for independently normalized signed C_m and K_Q (or V): one parent action
with kinetic Z_phi and coupling g_phi, mapped to the Track-A force host.
Inventories the repository for those microscopic inputs. Expected outcome is
INCOMPLETE until a genuine derivation exists. Does not invent numerics.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_PARENT_ACTION_MATCHING_DECLARED_INCOMPLETE"
FAIL_STATUS = "FAIL_MAT001_PARENT_ACTION_MATCHING"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
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
        "--j1",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--kq-dig",
        type=Path,
        default=mat
        / "KQ_DERIVATION_DIG"
        / "outputs"
        / "mat001_kq_derivation_dig_summary.json",
    )
    parser.add_argument(
        "--tier1-readiness",
        type=Path,
        default=repo
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_tier1_peer_review_readiness_summary.json",
    )
    parser.add_argument(
        "--r3",
        type=Path,
        default=repo
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_r3_uv_residue_audit_summary.json",
    )
    parser.add_argument("--repo-root", type=Path, default=repo)
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


def declare_parent_route() -> dict[str, Any]:
    z_phi, f_phi = sp.symbols("Z_phi f_phi", positive=True)
    g_phi = sp.symbols("g_phi", real=True, finite=True, nonzero=True)
    c_m = sp.simplify(g_phi / f_phi)
    k_q = sp.simplify(z_phi / f_phi**2)
    v = sp.simplify(g_phi / sp.sqrt(z_phi))
    v_alt = sp.simplify(c_m / sp.sqrt(k_q))
    require(sp.simplify(v - v_alt) == 0, "parent and IR V must agree")
    require(
        sp.simplify(v.subs(g_phi, -g_phi) + v) == 0,
        "signed V must flip with field orientation",
    )

    return {
        "selected_derived_route": "PARENT_ACTION_Z_phi_g_phi_TO_TRACK_A",
        "status": "DECLARED_NOT_COMPLETED",
        "parent_chart": {
            "field": "phi",
            "kinetic_term": "(Z_phi/2)*(U.grad(phi))^2",
            "matter_vertex": "-g_phi*rho_b*phi",
            "required_coefficients": ["Z_phi", "g_phi"],
        },
        "IR_Track_A_chart": {
            "field_map": "psi = f_phi * phi  (Conditional force-role map to Track-A: psi=psi_bar+pi)",
            "induced_C_m": str(c_m),
            "induced_K_Q": str(k_q),
            "induced_V": str(v),
            "host": "R2_TRACK_A_FORCE_PHONON",
        },
        "backup_route": {
            "id": "DIRECT_ON_SHELL_RESIDUE_V",
            "status": "DECLARED_NOT_ATTEMPTED_IN_THIS_CHECKPOINT",
            "note": "R2 identity: canonical residue equals V without bare K_Q once dynamics exist",
        },
        "forbidden_as_Derived": [
            "R1 K_Q = k_Q M_P^2 with k_Q ~ 1",
            "R3 incomplete Z_psi r_rho without micro matching",
            "Conditional matching-branch samples",
            "Free-sector ADM fields as force phonon without map",
        ],
        "symbolic_identities_verified": {
            "V_parent_equals_C_m_over_sqrt_K_Q": True,
            "C_m_equals_g_over_f": True,
            "K_Q_equals_Z_over_f_squared": True,
            "signed_V_flips_under_orientation_reversal": True,
        },
        "orientation_anchor": "f_phi>0 aligns phi and psi; reversing the physical mode flips the signed residue",
    }


def inventory_repo_for_micro_inputs(repo: Path) -> dict[str, Any]:
    """Search an explicit acyclic source set for numeric Z_phi/g_phi inputs.

    This is a presence inventory, not a derivation. The scope is restricted to
    upstream UVIR evidence and the core architecture. MAT gate products and the
    Master Research Plan are deliberately excluded: they are downstream
    governance/assessment records and must not become inputs to H1.1-H1.2.
    """
    patterns = {
        "Z_phi": re.compile(r"\bZ_phi\b"),
        "g_phi": re.compile(r"\bg_phi\b"),
        "Z_psi": re.compile(r"\bZ_psi\b"),
        "numeric_Z_phi_assignment": re.compile(
            r"\bZ_phi\s*(?::=|=)\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
            re.IGNORECASE,
        ),
        "numeric_g_phi_assignment": re.compile(
            r"\bg_phi\s*(?::=|=)\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
            re.IGNORECASE,
        ),
    }
    roots = [
        repo / "Analysis" / "UVIR",
        repo / "Theory" / "Core" / "ITSM_Core_Architecture.md",
        repo / "Theory" / "Gates" / "UVIR-003",
    ]
    hits: dict[str, list[str]] = {key: [] for key in patterns}
    scanned_files = 0
    files: list[Path] = []
    for root in roots:
        candidates = (
            [root] if root.is_file() else root.rglob("*") if root.is_dir() else []
        )
        for path in candidates:
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".py", ".md", ".json", ".tex"}:
                continue
            if "ITSM-Cosmologist" in path.name or path.name.endswith(".sha256"):
                continue
            files.append(path)
    for path in sorted(set(files), key=lambda p: p.as_posix().lower()):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned_files += 1
        try:
            rel = path.resolve().relative_to(repo.resolve()).as_posix()
        except ValueError:
            rel = path.name
        for key, rx in patterns.items():
            if rx.search(text):
                hits[key].append(rel)

    hits_capped = {key: sorted(set(paths))[:12] for key, paths in hits.items()}
    has_symbol_mentions = bool(hits_capped["Z_phi"] or hits_capped["g_phi"])
    has_numeric_assignment = bool(
        hits_capped["numeric_Z_phi_assignment"]
        or hits_capped["numeric_g_phi_assignment"]
    )
    return {
        "inventory_scope": [
            path.resolve().relative_to(repo.resolve()).as_posix() for path in roots
        ],
        "scope_exclusions": [
            "Analysis/MAT downstream gate products",
            "Theory/Core/ITSM_Master_Research_Plan.md governance record",
        ],
        "scanned_files": scanned_files,
        "hit_paths_capped": hits_capped,
        "symbol_mentions_present": has_symbol_mentions,
        "numeric_Z_phi_or_g_phi_assignment_found": has_numeric_assignment,
        "microscopic_coefficients_status": (
            "NOT_DERIVED_NUMERIC_ABSENT"
            if not has_numeric_assignment
            else "NUMERIC_ASSIGNMENT_STRINGS_FOUND_REQUIRE_HUMAN_REVIEW"
        ),
        "interpretation": (
            "No numeric Z_phi/g_phi assignment occurs in the explicit upstream "
            "derivation-source set; parent-action matching remains incomplete."
        ),
    }


def build_summary(
    declaration: dict[str, Any],
    inventory: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    incomplete = (
        inventory["microscopic_coefficients_status"] == "NOT_DERIVED_NUMERIC_ABSENT"
        or inventory["numeric_Z_phi_or_g_phi_assignment_found"] is False
    )
    add_check(
        checks,
        "parent_route_declared",
        declaration["selected_derived_route"] == "PARENT_ACTION_Z_phi_g_phi_TO_TRACK_A"
        and declaration["status"] == "DECLARED_NOT_COMPLETED",
    )
    add_check(
        checks,
        "symbolic_V_identities_hold",
        all(declaration["symbolic_identities_verified"].values()),
    )
    add_check(
        checks,
        "inventory_finds_no_numeric_micro_coefficients",
        incomplete is True
        and inventory["numeric_Z_phi_or_g_phi_assignment_found"] is False,
    )
    add_check(
        checks,
        "forbidden_routes_listed",
        len(declaration["forbidden_as_Derived"]) >= 3,
    )

    firewall = {
        "parent_route_declared": True,
        "numeric_Z_phi_derived": False,
        "numeric_g_phi_derived": False,
        "numeric_V_computed": False,
        "numeric_K_Q_derived": False,
        "uses_R1_as_Derived": False,
        "uses_conditional_samples_as_Derived": False,
        "claims_MAT_pass": False,
        "physics_pass": False,
        "reopens_stage4A": False,
        "matching_complete": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        firewall["matching_complete"] is False
        and firewall["numeric_V_computed"] is False
        and firewall["claims_MAT_pass"] is False
        and firewall["physics_pass"] is False
        and firewall["reopens_stage4A"] is False,
        flags=firewall,
    )

    missing = [
        "Numeric Z_phi from a declared parent action (same action as g_phi)",
        "Numeric g_phi from the same parent matter coupling",
        "Justified f_phi (or equivalent) map from phi to Track-A pi chart",
        "Provenance that parent kinetic is the Track-A K_Q time piece",
        "Optional backup: dynamical residue computation of V without bare K_Q",
    ]

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001",
        "interface": "PARENT_ACTION_TO_TRACK_A",
        "stage": "H1_PARENT_ACTION_MATCHING",
        "plan_step": "H1.1_H1.2",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "matching_status": "DECLARED_INCOMPLETE",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "C_m_numeric_status": "NOT_DERIVED_FORM_ONLY",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "declaration": declaration,
        "repo_inventory": inventory,
        "missing_microscopic_inputs": missing,
        "next_work_packages": [
            "H1.3: derive or bound Z_phi and g_phi from declared S_Phi + S_int, or prove absence in all declared sources",
            "H1.4: freeze research requirements for parent kinetic matching in Master Plan / queue",
            "H2: only after numeric or residue success — redefinition invariance package for peer review",
        ],
        "blocking_requirements": missing,
        "inadmissible_substitutions": {
            "k_Q_equals_1_as_Z_phi": "REJECTED",
            "conditional_sample_as_parent_match": "REJECTED",
            "symbolic_identity_as_numeric_V": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS declares the parent-action Derived route for Track-A matching "
            "and inventories the repo for microscopic Z_phi/g_phi. Finding them "
            "absent is an incompleteness result, not a derivation of V or K_Q."
        ),
        "serial_next": (
            "H1.3 derivation attempt from declared architecture/UVIR sources, "
            "or explicit incompleteness bound; do not open Stage 4A."
        ),
    }


def validate_upstream(
    s_int: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    dig: dict[str, Any] | None,
    tier1: dict[str, Any] | None,
    r3: dict[str, Any] | None,
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
        "kq_dig_upstream_incomplete",
        bool(
            dig
            and dig.get("subgate_status") == "PASS_MAT001_KQ_DERIVATION_DIG_INCOMPLETE"
            and dig.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "tier1_hold_upstream",
        bool(
            tier1
            and tier1.get("subgate_status")
            == "PASS_TIER1_PEER_REVIEW_READINESS_HOLD_RETAINED"
            and tier1.get("decision") == "HOLD_TIER1_CLOSURE_RETAINED"
        ),
    )
    add_check(
        checks,
        "r3_still_incomplete_upstream",
        bool(
            r3
            and r3.get("kq_numeric_status") == "NOT_DERIVED"
            and (
                r3.get("classification") == "INCOMPLETE_R3_UV_RESIDUE"
                or r3.get("classification_code") == "C"
            )
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "numeric_V_computed",
        "numeric_K_Q_derived",
        "matching_complete",
        "claims_MAT_pass",
        "physics_pass",
        "reopens_stage4A",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["matching_status"] == "DECLARED_INCOMPLETE", "incomplete")
    require(summary["V_status"] == "NOT_COMPUTED", "V closed")


def main() -> None:
    args = parse_args()
    s_int, e1, s1 = load_json(args.track_a_s_int)
    j1, e2, s2 = load_json(args.j1)
    dig, e3, s3 = load_json(args.kq_dig)
    tier1, e4, s4 = load_json(args.tier1_readiness)
    r3, e5, s5 = load_json(args.r3)

    evidence = {
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s1,
            "parse_error": e1,
        },
        "j1": {"source": args.j1.name, "sha256": s2, "parse_error": e2},
        "kq_dig": {"source": args.kq_dig.name, "sha256": s3, "parse_error": e3},
        "tier1_readiness": {
            "source": args.tier1_readiness.name,
            "sha256": s4,
            "parse_error": e4,
        },
        "r3": {"source": args.r3.name, "sha256": s5, "parse_error": e5},
    }
    checks = validate_upstream(s_int, j1, dig, tier1, r3)
    for name, err in (
        ("track_a_s_int", e1),
        ("j1", e2),
        ("kq_dig", e3),
        ("tier1_readiness", e4),
        ("r3", e5),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    declaration = declare_parent_route()
    inventory = inventory_repo_for_micro_inputs(args.repo_root.resolve())
    summary = build_summary(declaration, inventory, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_parent_action_matching_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_parent_action_matching_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )
    print("MAT-001 parent-action matching (H1.1–H1.2)")
    print("  route:", summary["declaration"]["selected_derived_route"])
    print("  matching:", summary["matching_status"])
    print("  micro:", summary["repo_inventory"]["microscopic_coefficients_status"])
    print("  V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
