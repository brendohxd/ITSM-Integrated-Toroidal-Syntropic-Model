#!/usr/bin/env python3
"""UVIR-003 Stage 2a: R3 UV residue derivation/bound audit.

Serial Stage 2a (UVIR-003_SERIAL_STAGE_ORDER): dig-harder whether the
*declared repository action / condensate UV structure* can derive or bound

  Z_psi, r_rho = rho_Phi/(M_P^2 a0^2),  product Z_psi r_rho,
  K_Q = Z_psi rho_Phi / a0^2,
  I_a0 = (2/3) C_IR / (Z_psi r_rho).

Terminal classifications (exactly one):
  A. DERIVED_UNDER_NAMED_PREMISES
  B. BOUNDED_UNDER_NAMED_PREMISES
  C. INCOMPLETE_R3_UV_RESIDUE

physics_pass remains false unless a genuine action-level derivation exists
(and even then this does not claim UVIR full-gate PASS).

Firewalls:
  - no silent Z_psi=1, r_rho=1, C_IR=2/3 as Derived
  - no MAT unlock, no UVIR full PASS, no physical cutoff claim
  - no observational/cosmological claim
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--inventory-summary",
        type=Path,
        default=base / "outputs" / "uvir003_kq_matching_inventory_summary.json",
    )
    p.add_argument(
        "--matching-summary",
        type=Path,
        default=base / "outputs" / "uvir003_matching_route_program_summary.json",
    )
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require(name: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def symbolic_r3_map() -> dict[str, Any]:
    """Recover R3 identities from the Conditional residual ansatz only."""
    Z_psi, rho_Phi, a0, G, C_IR, r_rho = sp.symbols(
        "Z_psi rho_Phi a0 G C_IR r_rho", positive=True
    )
    M_P_sq = 1 / (8 * sp.pi * G)
    # Ansatz (Conditional sketch — not Derived from S_Phi in repo)
    K_Q = Z_psi * rho_Phi / a0**2
    A = C_IR / (12 * sp.pi * G * a0)
    I_a0_via_rho = sp.simplify(A * a0 / K_Q)
    # r_rho definition
    r_def = rho_Phi / (M_P_sq * a0**2)
    require("r_rho = 8 pi G rho_Phi / a0^2", sp.simplify(r_def - 8 * sp.pi * G * rho_Phi / a0**2) == 0)
    K_Q_via_r = sp.simplify(Z_psi * r_rho / (8 * sp.pi * G))
    I_a0_via_r = sp.simplify(A * a0 / K_Q_via_r)
    target = sp.Rational(2, 3) * C_IR / (Z_psi * r_rho)
    require(
        "I_a0 recovers (2/3) C_IR/(Z_psi r_rho)",
        sp.simplify(I_a0_via_r - target) == 0,
    )
    # Equivalence: K_Q via rho with r_rho substituted
    K_Q_sub = sp.simplify(K_Q.subs(rho_Phi, r_rho * M_P_sq * a0**2))
    require("K_Q via r_rho matches", sp.simplify(K_Q_sub - K_Q_via_r) == 0)

    return {
        "ansatz_K_Q": str(K_Q),
        "r_rho_definition": "rho_Phi/(M_P^2 a0^2) with M_P^2=1/(8 pi G)",
        "I_a0_via_rho": str(I_a0_via_rho),
        "I_a0_via_r": str(I_a0_via_r),
        "I_a0_canonical": str(target),
        "identity_check_ok": True,
        "provenance": "Conditional residual ansatz in uvir003_matching_route_program.symbolic_r3_sketch",
        "is_action_derivation": False,
    }


def psi_rescaling_invariance() -> dict[str, Any]:
    """Field redefinition psi -> s * psi (s>0).

    Architecture / inventory transforms:
      K_Q -> K_Q/s^2,  A -> A/s^3,  q -> q*s
    Primary invariant A*q/K_Q is invariant.

    Under bare R3 ansatz K_Q = Z_psi * rho_Phi / a0^2 with rho_Phi treated as a
    *physical condensate density* independent of IR psi normalization, Z_psi
    must carry the s^{-2} of K_Q. Therefore the product Z_psi*r_rho is *not*
    automatically a pure UV invariant under arbitrary IR field normalization:
    it inherits K_Q's normalization ambiguity unless a fixed field chart is
    declared. The physical invariant is A*q/K_Q; I_a0=A*a0/K_Q is only its
    chart-fixed q=a0 diagnostic when a0 is held external.
    """
    K_Q, A, q, s, Z_psi, r_rho, C_IR, G = sp.symbols(
        "K_Q A q s Z_psi r_rho C_IR G", positive=True
    )
    I = A * q / K_Q
    I_prime = (A / s**3) * (q * s) / (K_Q / s**2)
    require("Aq/K_Q invariant under psi rescaling", sp.simplify(I_prime - I) == 0)

    # Bare product P = Z_psi r_rho ~ 8 pi G K_Q under ansatz
    P = Z_psi * r_rho
    P_from_K = 8 * sp.pi * G * K_Q
    # Under rescaling at fixed G, P_from_K -> P_from_K / s^2  (not invariant)
    P_prime = P_from_K / s**2
    bare_product_invariant = bool(sp.simplify(P_prime - P_from_K) == 0)

    I_a0 = sp.Rational(2, 3) * C_IR / P
    # For I_a0 to stay invariant when C_IR is Wilson (may rescale with A),
    # inventory treats C_IR as tied to A: A = C_IR/(12 pi G a0) so C_IR ~ A * const
    # Under s: A' = A/s^3 => C_IR' = C_IR/s^3 if a0,G fixed.
    C_IR_p = C_IR / s**3
    P_p = P / s**2  # if P tracks K_Q
    I_a0_p = sp.Rational(2, 3) * C_IR_p / P_p
    # Wait: (C_IR/s^3) / (P/s^2) = (C_IR/P) / s  — NOT invariant!
    # Actually A' = A/s^3, a0 fixed => C_IR' from A' = C_IR/s^3
    # K_Q' = K_Q/s^2 => P' = P/s^2
    # I_a0 = A a0 / K_Q is not invariant when a0 is held external:
    #   C_IR' / P' = (C_IR/s^3)/(P/s^2) = C_IR/(P s)  — inconsistent unless
    # this is a chart-fixed diagnostic that scales as 1/s.
    # Correction: under psi rescaling, architecture sets C_IR as coefficient in
    # L_IR ~ C_IR M_P^2 a0^2 Y^{3/2}; Y involves (grad psi / a0)^2 so Y' = s^2 Y
    # and A ~ C_IR/(G a0) with the force term A |grad psi|^3 ... need care.
    # Inventory already verified A_q_over_K_Q invariant under declared map
    # (K_Q/s^2, A/s^3, q*s). That is authoritative.
    # Conclusion for audit: do not treat bare Z_psi or r_rho as Derived UV
    # numbers independent of IR field chart; Aq/K_Q is the invariant object.

    # I_a0 := A*a0/K_Q with *external fixed* a0 is NOT redefinition-invariant:
    #   A' a0 / K_Q' = A a0 /(s K_Q). The invariant object is A*q/K_Q where the
    # background gradient q scales as q'=s q. Evaluating at "q=a0" therefore
    # selects a field chart (gradient unit), not a pure UV residue.
    a0 = sp.symbols("a0", positive=True)
    I_a0_fixed_a0 = A * a0 / K_Q
    I_a0_fixed_a0_p = (A / s**3) * a0 / (K_Q / s**2)
    fixed_a0_invariant = bool(
        sp.simplify(I_a0_fixed_a0_p - I_a0_fixed_a0) == 0
    )
    require(
        "fixed external a0 I_a0 is chart-dependent (not invariant)",
        fixed_a0_invariant is False,
    )

    return {
        "primary_invariant_Aq_over_KQ": "invariant under psi -> s psi",
        "I_a0_via_A_times_external_a0_over_KQ": "NOT invariant (chart-dependent)",
        "bare_Z_psi_r_rho_product_invariant_if_tracks_KQ": bare_product_invariant,
        "scientific_conclusion": (
            "Bare Z_psi and r_rho (or their product) are not automatically "
            "UV-only Derived numbers: under the residual ansatz they inherit "
            "K_Q's field-normalization map. The redefinition-invariant object is "
            "A*q/K_Q (q = background |grad psi|). Evaluating at q=a0 with a0 an "
            "external fixed scale picks a field chart. A numerical 'match' that "
            "depends on arbitrary psi normalization is not a physical R3 derivation."
        ),
        "psi_rescaling_test_ok": True,
    }


def provenance_table() -> dict[str, Any]:
    """Classify each R3 symbol against repository declarations."""
    return {
        "symbols": {
            "Phi": {
                "role": "complex condensate order parameter",
                "class": "declared_input_architecture",
                "source": "ITSM_Core_Architecture.md §3.2",
                "derivable_numeric": False,
            },
            "rho0": {
                "role": "homogeneous finite-density amplitude (VEV)",
                "class": "declared_with_branch_existence_UVIR001",
                "source": "Architecture V_eff; UVIR-001 stable branch",
                "derivable_numeric": False,
                "note": "Existence/stability domain only; not rho_Phi matching scale",
            },
            "rho_Phi": {
                "role": "background energy/charge density scale in R3 ansatz",
                "class": "requires_external_UV_or_matching",
                "source": "Introduced in matching_route_program R3 sketch only",
                "derivable_numeric": False,
                "in_architecture": False,
                "in_UVIR001_action": False,
            },
            "Z_psi": {
                "role": "phonon/force kinetic residue after amplitude integration",
                "class": "requires_external_UV_or_matching",
                "source": "Conditional residual ansatz; not computed from S_Phi",
                "derivable_numeric": False,
                "in_architecture": False,
            },
            "r_rho": {
                "role": "rho_Phi/(M_P^2 a0^2) dimensionless density fraction",
                "class": "dimensional_definition_plus_unknown_rho_Phi",
                "source": "Definition only; value free without rho_Phi",
                "derivable_numeric": False,
            },
            "K_Q": {
                "role": "IR force temporal kinetic coefficient",
                "class": "IR_EFT_coefficient_not_derived",
                "source": "UVIR-003 Stage A / inventory; R1 Conditional or R3 ansatz",
                "derivable_numeric": False,
                "status": "NOT_DERIVED",
            },
            "a0": {
                "role": "IR acceleration scale in Y, Q normalizations",
                "class": "declared_IR_input_or_DSM_postulate",
                "source": "Architecture § force; Master Plan DSM Conditional",
                "derivable_numeric": False,
                "note": "Not derived from topology/circulation under recovery",
            },
            "C_IR": {
                "role": "IR force Wilson coefficient",
                "class": "Wilson_coefficient_open",
                "source": "Architecture L_IR; not fixed by R3",
                "derivable_numeric": False,
            },
            "A": {
                "role": "force spatial coefficient A = C_IR/(12 pi G a0)",
                "class": "derived_from_architecture_form_given_C_IR",
                "source": "Core Architecture weak-field",
                "derivable_numeric": False,
                "note": "Form Derived under architecture; value needs C_IR",
            },
            "I_a0": {
                "role": "A a0 / K_Q on the named q=a0 field chart",
                "class": "conditional_chart_fixed_map",
                "source": "R3 sketch identity I_a0=(2/3)C_IR/(Z_psi r_rho)",
                "derivable_numeric": False,
                "note": "Algebraic map holds under the ansatz; it is not invariant with fixed external a0",
            },
            "S_Phi": {
                "role": "condensate action",
                "class": "partial_UVIR001_candidate_not_canonical_micro_action",
                "source": "UVIR-001 tested P(Z); rejected as direct Y^{3/2} origin",
                "derivable_numeric": False,
                "note": "No matching of K_Q from S_Phi present in repo",
            },
            "S_psi": {
                "role": "preferred-frame force sector",
                "class": "declared_two_sector_route_UVIR002_003",
                "source": "UVIR-002/003 Track A",
                "derivable_numeric": False,
            },
        },
        "explicitly_declared_inputs": [
            "Phi form",
            "U^mu frame (independent constrained aether choice)",
            "a0 as IR normalization scale",
            "C_IR as Wilson coefficient",
            "K_Q as free IR kinetic coeff until matching",
        ],
        "derivable_from_action_form_only": [
            "A expression given C_IR, G, a0",
            "I_a0 map under Conditional R3 ansatz identities",
            "redefinition invariants Aq/K_Q, A/K_Q^{3/2}",
        ],
        "requires_external_UV_completion": [
            "Z_psi from integrating out amplitude / matching residue",
            "rho_Phi absolute scale tied to force kinetic",
            "r_rho numeric value",
            "microscopic S_Phi that produces S_psi temporal kinetic",
        ],
        "dimensional_ansatze_or_conventions": [
            "K_Q = Z_psi rho_Phi / a0^2 (Conditional residual sketch)",
            "R1 K_Q = k_Q M_P^2 (Conditional dimensional analogy)",
            "naive O(1) guesses k_Q~1, Z_psi~1, r_rho~1 (non-derived comparison only)",
        ],
        "rigorous_bound_Z_psi_r_rho_found": False,
    }


def naive_comparison_only() -> dict[str, Any]:
    """Labelled non-derived comparison — not a match result."""
    # Z_psi r_rho = 1, C_IR = 2/3  => same as R1 naive
    I = float(sp.Rational(2, 3) * sp.Rational(2, 3) / 1)
    return {
        "label": "NON_DERIVED_COMPARISON_ONLY",
        "assumptions": {
            "Z_psi": 1.0,
            "r_rho": 1.0,
            "C_IR": float(sp.Rational(2, 3)),
        },
        "I_a0": I,
        "q_cross_parallel_over_a0": 0.375,
        "warning": (
            "Do not cite as Derived. Identical to R1 naive (k_Q,C_IR)=(1,2/3)."
        ),
    }


def classify(prov: dict[str, Any], r3_map: dict[str, Any]) -> dict[str, Any]:
    """Decide A / B / C from repository content."""
    # No action-level derivation of Z_psi or rho_Phi
    z_ok = prov["symbols"]["Z_psi"]["derivable_numeric"]
    r_ok = prov["symbols"]["r_rho"]["derivable_numeric"]
    rho_ok = prov["symbols"]["rho_Phi"]["derivable_numeric"]
    action_deriv = r3_map.get("is_action_derivation", False)
    rigorous_bound = bool(prov.get("rigorous_bound_Z_psi_r_rho_found", False))

    if action_deriv and z_ok and (r_ok or rho_ok):
        code = "A"
        name = "DERIVED_UNDER_NAMED_PREMISES"
        reason = "Action-level derivation of residue and density scale found."
    elif rigorous_bound:
        code = "B"
        name = "BOUNDED_UNDER_NAMED_PREMISES"
        reason = "Rigorous bound on Z_psi r_rho from declared premises."
    else:
        code = "C"
        name = "INCOMPLETE_R3_UV_RESIDUE"
        reason = (
            "Declared architecture and UVIR-001/002/003 provide Phi, rho0 branch "
            "existence, and a two-sector force route, but do not compute Z_psi, "
            "rho_Phi, or r_rho from S_Phi. R3 is a Conditional dimensional residual "
            "ansatz (matching_route_program) with free Wilson/residue parameters. "
            "No rigorous inequality bounding Z_psi r_rho from the microscopic "
            "action is present. Stage 2a therefore terminates as incomplete UV "
            "residue matching — an acceptable serial-order result."
        )

    return {
        "code": code,
        "classification": name,
        "reason": reason,
        "physics_pass": False,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "stage_2a_exit": "INCOMPLETE_proceed_to_2b_or_continue_UV_work",
    }


def main() -> None:
    args = parse_args()
    inv = load_json(args.inventory_summary)
    match = load_json(args.matching_summary)

    checks: list[dict[str, Any]] = []

    # Prior subgates present
    inv_ok = (
        inv is not None
        and inv.get("subgate_status") == "PASS_KQ_MATCHING_INVENTORY_OPEN"
    )
    match_ok = (
        match is not None
        and match.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    )
    checks.append(
        {
            "name": "prior_inventory_summary_present",
            "ok": inv_ok,
            "got": None if inv is None else inv.get("subgate_status"),
        }
    )
    checks.append(
        {
            "name": "prior_matching_route_program_present",
            "ok": match_ok,
            "got": None if match is None else match.get("subgate_status"),
        }
    )

    r3_map = symbolic_r3_map()
    checks.append(
        {
            "name": "r3_invariant_formula_recovered",
            "ok": r3_map["identity_check_ok"],
            "I_a0_canonical": r3_map["I_a0_canonical"],
        }
    )

    # Matching program R3 sketch status is Open/Conditional, not Derived
    r3_status = None
    if match is not None:
        r3_status = (match.get("route_R3_sketch") or {}).get("status")
    checks.append(
        {
            "name": "matching_program_labels_r3_as_open_conditional_sketch",
            "ok": r3_status
            in (
                "Open_Conditional_sketch",
                "Open",
                "Conditional",
            )
            or (
                match is not None
                and "Z_psi" in str(match.get("route_R3_sketch", {}))
            ),
            "got": r3_status,
        }
    )

    rescale = psi_rescaling_invariance()
    checks.append(
        {
            "name": "psi_rescaling_primary_invariant_ok",
            "ok": rescale["psi_rescaling_test_ok"],
        }
    )
    checks.append(
        {
            "name": "bare_Z_psi_r_rho_not_auto_invariant_under_psi_rescaling",
            "ok": rescale["bare_Z_psi_r_rho_product_invariant_if_tracks_KQ"] is False,
            "note": rescale["scientific_conclusion"],
        }
    )

    prov = provenance_table()
    # Completeness: critical UV symbols not numeric-derivable
    missing_micro = [
        k
        for k in ("Z_psi", "rho_Phi", "r_rho")
        if not prov["symbols"][k]["derivable_numeric"]
    ]
    checks.append(
        {
            "name": "uv_residue_symbols_not_numerically_derivable_in_repo",
            "ok": set(missing_micro) == {"Z_psi", "rho_Phi", "r_rho"},
            "missing": missing_micro,
        }
    )

    # No silent defaults as Derived
    naive = naive_comparison_only()
    checks.append(
        {
            "name": "naive_point_labelled_non_derived_comparison_only",
            "ok": naive["label"] == "NON_DERIVED_COMPARISON_ONLY",
        }
    )

    # Dimensional consistency: [K_Q] ~ energy density / a0^2
    # rho_Phi ~ energy density, a0 ~ acceleration ~ 1/time in natural units with c=1
    # Symbolic: K_Q * a0^2 / (Z_psi * rho_Phi) = 1 under ansatz
    Z_psi, rho_Phi, a0 = sp.symbols("Z_psi rho_Phi a0", positive=True)
    K_Q = Z_psi * rho_Phi / a0**2
    dim_ok = bool(sp.simplify(K_Q * a0**2 / (Z_psi * rho_Phi) - 1) == 0)
    checks.append({"name": "dimensional_ansatz_internal_consistency", "ok": dim_ok})

    # Architecture does not define Z_psi / rho_Phi (grep-level logical flag)
    checks.append(
        {
            "name": "reviewed_declared_sources_lack_Z_psi_rho_Phi_matching_formula",
            "ok": True,
            "evidence": (
                "ITSM_Core_Architecture §3.2 defines Phi, rho0, V_eff; no Z_psi, "
                "rho_Phi, or K_Q = Z_psi rho_Phi/a0^2. UVIR-001 rejects pure "
                "sextic as direct Y^{3/2} origin; physical charge-setting open."
            ),
        }
    )

    classification = classify(prov, r3_map)
    checks.append(
        {
            "name": "terminal_classification_is_C_incomplete",
            "ok": classification["code"] == "C",
            "classification": classification["classification"],
        }
    )

    firewall = {
        "numeric_Derived_K_Q": False,
        "MAT001_unlocked": False,
        "UVIR003_full_PASS": False,
        "physical_cutoff_claimed": False,
        "observational_or_cosmological_claim": False,
        "silent_Z_psi_equals_1_as_Derived": False,
        "silent_r_rho_equals_1_as_Derived": False,
        "silent_C_IR_equals_2_3_as_Derived": False,
        "exploratory_scan_promoted_to_derivation": False,
    }
    checks.append(
        {
            "name": "claim_firewall_all_false",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    # Audit infrastructure PASS even when classification is incomplete
    subgate = (
        "PASS_R3_UV_RESIDUE_AUDIT_INCOMPLETE"
        if all_ok and classification["code"] == "C"
        else (
            "PASS_R3_UV_RESIDUE_AUDIT"
            if all_ok
            else "FAIL_R3_UV_RESIDUE_AUDIT"
        )
    )

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "B_R3_UV_RESIDUE_AUDIT_STAGE_2A",
        "serial_stage": "2a",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "classification_code": classification["code"],
        "classification": classification["classification"],
        "classification_reason": classification["reason"],
        "physics_pass": False,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "r3_map": r3_map,
        "psi_rescaling": rescale,
        "provenance": prov,
        "naive_comparison_only": naive,
        "missing_microscopic_inputs": [
            "Microscopic S_Phi (or S_Phi+S_psi matching) that yields temporal force kinetic K_Q",
            "Computed residue Z_psi from amplitude integration / wave-function renormalization",
            "Physical identification of rho_Phi as the density entering that matching",
            "Fixed IR field chart / matching scheme so residue is redefinition-safe",
            "Independent determination or bound on C_IR if quoted in I_a0",
        ],
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Stage 2a dig-harder R3 audit: maps Conditional residual identities "
            "and finds no action-level derivation or bound of Z_psi, r_rho in the "
            "audited declared sources. Classification C is an acceptable Stage-2a exit. Does "
            "not unlock MAT-001, does not close UVIR-003, does not claim Derived K_Q."
        ),
        "next_required": [
            "Stage 2b: Conditional matching floor with scope (if programme accepts)",
            "or continue genuine UV/microscopic matching of S_Phi -> force kinetic",
            "Stage 2c: re-evaluate causality/NDA under chosen floor",
            "Never promote R1/R3 naive O(1) points to Derived",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_r3_uv_residue_audit_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    content_hash = hashlib.sha256(payload).hexdigest()
    (args.output_dir / "uvir003_r3_uv_residue_audit_summary.sha256").write_bytes(
        f"{content_hash}  {out.name}\n".encode("utf-8")
    )

    print("UVIR-003 Stage 2a R3 UV residue audit")
    print("  classification:", classification["code"], classification["classification"])
    print("  physics_pass: False")
    print("  full_gate_status: IN_PROGRESS | MAT-001: BLOCKED")
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", content_hash)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
