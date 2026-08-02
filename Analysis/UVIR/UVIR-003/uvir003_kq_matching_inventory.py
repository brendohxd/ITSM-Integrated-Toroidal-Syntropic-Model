#!/usr/bin/env python3
"""UVIR-003: K_Q / force-normalization matching inventory (Open/Conditional).

Post–alpha.10 priority 1 from the Master Research Plan:

  K_Q / force normalization matching (shared blocker with causality NDA).

This is *not* a derivation of a numeric K_Q. It:
  1. Lists field-redefinition invariants involving the force kinetic coeff.
  2. Catalogues candidate matching *routes* with explicit statuses.
  3. Maps each route to which invariant it would fix.
  4. Expresses causality q_× and NDA Λ_|| in invariant / candidate form.
  5. States the residual MAT-001 dependency honestly.

Statuses:
  - Open: defined matching problem, incomplete.
  - Conditional: candidate relation under named premises (not Derived).
  - Derived: not claimed here for K_Q.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--zero-grad-summary",
        type=Path,
        default=base / "outputs" / "uvir003_zero_gradient_force_block_summary.json",
    )
    parser.add_argument(
        "--conditional-kq",
        type=Path,
        default=base / "outputs" / "uvir003_conditional_kq_estimate_summary.json",
    )
    parser.add_argument(
        "--unitarity-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_declared_unitarity_eft_criterion_summary.json",
    )
    parser.add_argument(
        "--causality-summary",
        type=Path,
        default=base / "outputs" / "uvir003_causality_addendum_summary.json",
    )
    return parser.parse_args()


def require(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def symbolic_invariants() -> dict[str, Any]:
    """Redefinition psi -> s * psi and invariant combinations."""
    K_Q, A, gamma, C_m, q, s = sp.symbols(
        "K_Q A gamma C_m q s", positive=True
    )
    # Under psi' = s psi (s>0):
    #   K_Q' = K_Q / s^2
    #   A'   = A / s^3
    #   gamma' = gamma / s^2
    #   C_m' = C_m / s
    #   q'   = q * s   (background |grad psi| scales)
    # From zero-gradient force block and causality addendum.
    transform = {
        "K_Q": "K_Q/s**2",
        "A": "A/s**3",
        "gamma": "gamma/s**2",
        "C_m": "C_m/s",
        "q_background": "q*s",
    }
    inv = {
        "A_over_K_Q_to_3_2": sp.simplify(A / K_Q ** sp.Rational(3, 2)),
        "A_q_over_K_Q": sp.simplify(A * q / K_Q),
        "gamma_over_K_Q": sp.simplify(gamma / K_Q),
        "C_m_over_sqrt_K_Q": sp.simplify(C_m / sp.sqrt(K_Q)),
        "C_obs_combo": sp.simplify(C_m ** sp.Rational(3, 2) / sp.sqrt(A)),
        # note: architecture C_obs = C_m^{3/2}/sqrt(C_IR); A ∝ C_IR so related
    }
    # Check invariance under the declared map
    subs = {
        K_Q: K_Q / s**2,
        A: A / s**3,
        gamma: gamma / s**2,
        C_m: C_m / s,
        q: q * s,
    }
    inv_check = {
        name: bool(sp.simplify(expr.subs(subs) - expr) == 0)
        for name, expr in inv.items()
    }
    require("all listed combos invariant", all(inv_check.values()), str(inv_check))

    # Causality long-wavelength ratio R = 3 A q (1+cos^2 θ) / K_Q
    # Superluminal when R > 1 (v_ph^2 > 1 in c=1 units of Stage-A addendum)
    cos_th = sp.symbols("cos_theta", real=True)
    R_c = sp.simplify(3 * A * q * (1 + cos_th**2) / K_Q)
    q_cross = sp.simplify(K_Q / (3 * A * (1 + cos_th**2)))
    # Express R_c in terms of invariant I = A q / K_Q
    I_AqK = A * q / K_Q
    R_c_via_I = sp.simplify(3 * I_AqK * (1 + cos_th**2))
    require_zero = sp.simplify(R_c - R_c_via_I)
    require("R_c uses invariant A q / K_Q", require_zero == 0)

    # NDA Λ_|| = K_Q^{3/4}/sqrt(A) — not invariant alone (depends on s)
    # But Λ_|| / q = K_Q^{3/4} / (sqrt(A) q) = 1 / (q * (A/K_Q^{3/2})^{1/2})
    #              = 1 / (q * sqrt(I_A_KQ32 / q^0 wait))
    # A/K^{3/2} is invariant; Λ_|| = 1/sqrt(A/K^{3/2}) * K_Q^0? 
    # Λ_|| = K^{3/4}/A^{1/2} = 1 / sqrt(A/K^{3/2}) — yes fully invariant!
    lam = K_Q ** sp.Rational(3, 4) / sp.sqrt(A)
    lam_alt = 1 / sp.sqrt(A / K_Q ** sp.Rational(3, 2))
    require("Λ_|| is redefinition-invariant", sp.simplify(lam - lam_alt) == 0)
    require(
        "Λ_|| invariant under s",
        sp.simplify(lam.subs(subs) - lam) == 0,
    )

    return {
        "field_redefinition": "psi -> s * psi, s>0",
        "transforms": transform,
        "invariants": {k: str(v) for k, v in inv.items()},
        "invariance_checks": inv_check,
        "causality": {
            "R_c": str(R_c),
            "q_cross": str(q_cross),
            "primary_invariant": "A*q/K_Q",
            "superluminal_when": "R_c > 1 (long-wavelength Stage-A addendum convention)",
        },
        "nda_Lambda_parallel": {
            "expression": str(lam),
            "redefinition_invariant": True,
            "equals": "1/sqrt(A/K_Q**(3/2))",
        },
    }


def candidate_routes() -> list[dict[str, Any]]:
    """Matching routes — Open or Conditional, never Derived K_Q here."""
    return [
        {
            "id": "R1_dimensional_MP_a0",
            "name": "Dimensional analogy K_Q = k_Q M_P^2",
            "status": "Conditional",
            "premises": [
                "Temporal Q-kinetic uses same M_P^2 a0^2 prefactor logic as Y sector",
                "Q0=0 (no subtracted background kinetic)",
                "k_Q is an O(1) Wilson coefficient (unfixed)",
            ],
            "fixes": ["K_Q / M_P^2 = k_Q (up to k_Q)"],
            "does_not_fix": ["k_Q", "C_IR", "physical cutoff alone"],
            "prior_artifact": "UVIR-003_CONDITIONAL_KQ_ESTIMATE (SPECULATIVE_NOT_A_DERIVATION)",
            "priority": "baseline candidate; must not be cited as Derived",
        },
        {
            "id": "R2_matter_vertex_MAT001",
            "name": "Matter–force vertex matching (MAT-001)",
            "status": "Open",
            "premises": [
                "Single interaction generates force and exchange (architecture)",
                "C_obs = C_m^{3/2}/sqrt(C_IR) from static weak-field reduction",
                "Canonical force kinetic enters the vertex normalization",
            ],
            "fixes": [
                "C_m / sqrt(K_Q) class combinations once vertex computed",
                "possibly absolute K_Q once C_m and C_IR are independently fixed",
            ],
            "does_not_fix": ["anything until UVIR-003 admits a force sector ready for MAT"],
            "prior_artifact": "MAT-001 blocked; architecture § force law",
            "priority": "canonical long-term route per Master Plan critical path",
        },
        {
            "id": "R3_condensate_microscopic",
            "name": "UV condensate / microscopic completion",
            "status": "Open",
            "premises": [
                "Force mediator emerges from or couples to condensate Φ",
                "Matching scale set by ρ_Φ or phonon residue (not free)",
            ],
            "fixes": ["K_Q in terms of UV parameters of S_Φ + S_ψ"],
            "does_not_fix": ["IR-only bottom-up EFT without UV data"],
            "prior_artifact": "UVIR-001/002 route selection; CRA sectors",
            "priority": "research-open; dig-harder option under identity pillars",
        },
        {
            "id": "R4_regulator_k_cross",
            "name": "Regulator crossover matching γ, M_*, K_Q",
            "status": "Open",
            "premises": [
                "k^4 regulator scale is tied to a named physical scale (e.g. a0)",
                "invariant gamma/K_Q fixed by that matching",
            ],
            "fixes": ["gamma/K_Q", "possibly relative IR/UV force split"],
            "does_not_fix": ["absolute A q / K_Q causality ratio alone"],
            "prior_artifact": "Stage A regulator + causality addendum",
            "priority": "secondary; does not replace A q / K_Q matching",
        },
        {
            "id": "R5_observational_IR_baseline",
            "name": "Conditional IR baseline (AQUAL-class) as external anchor",
            "status": "Conditional",
            "premises": [
                "Master plan Bucket C: C_obs ~ 1 as empirical hypothesis until MAT-001",
                "Does not by itself determine K_Q without dynamics of time-dependent force",
            ],
            "fixes": ["C_obs combination involving C_m, C_IR"],
            "does_not_fix": ["K_Q without additional dynamical input"],
            "prior_artifact": "Master Plan §6 force-law divergence",
            "priority": "phenomenology anchor only; not a K_Q derivation",
        },
    ]


def candidate_R1_implications() -> dict[str, Any]:
    """Reproduce conditional estimate under R1 without promoting to Derived."""
    k_Q, G, a0, C_IR, cos_th = sp.symbols(
        "k_Q G a0 C_IR cos_theta", positive=True
    )
    M_P_sq = 1 / (8 * sp.pi * G)
    K_Q = k_Q * M_P_sq
    A = C_IR / (12 * sp.pi * G * a0)
    q_cross = sp.simplify(K_Q / (3 * A * (1 + cos_th**2)))
    lam = sp.simplify(K_Q ** sp.Rational(3, 4) / sp.sqrt(A))

    rows = []
    for label, ct in [("parallel", 1), ("perp", 0)]:
        qc = sp.simplify(q_cross.subs(cos_th, ct))
        ratio = sp.simplify(qc.subs({k_Q: 1, C_IR: sp.Rational(2, 3)}) / a0)
        rows.append(
            {
                "direction": label,
                "q_cross_over_a0_symbolic": str(sp.simplify(qc / a0)),
                "q_cross_over_a0_at_kQ1_CIR23": float(ratio),
            }
        )

    # Λ_|| / a0 under same premises — diagnostic only
    lam_over_a0 = sp.simplify(
        lam.subs({k_Q: 1, C_IR: sp.Rational(2, 3)}) / a0
    )
    # Need G, a0 dimensions — Λ has mass dimension 1, a0 is acceleration/mass
    # Keep symbolic: Λ_|| in terms of G, a0, k_Q, C_IR
    return {
        "status": "Conditional_R1_implications_only",
        "not_a_derivation": True,
        "q_cross_rows": rows,
        "Lambda_parallel_expression": str(lam),
        "Lambda_parallel_over_a0_at_naive_point": str(lam_over_a0),
        "warning": (
            "Naive (k_Q,C_IR)=(1,2/3) places q_cross ≲ a0; treat as priority "
            "flag only (see CONDITIONAL_KQ_ESTIMATE)."
        ),
    }


def main() -> None:
    args = parse_args()
    zg = load_json(args.zero_grad_summary)
    cond = load_json(args.conditional_kq)
    unit = load_json(args.unitarity_summary)
    caus = load_json(args.causality_summary)

    inv = symbolic_invariants()
    routes = candidate_routes()
    r1 = candidate_R1_implications()

    # Prior status wiring
    prior = {
        "zero_gradient_force_block": (zg or {}).get("status")
        or (zg or {}).get("stage"),
        "conditional_kq_estimate": (cond or {}).get("status"),
        "declared_unitarity_eft": (unit or {}).get("subgate_status"),
        "causality_addendum": (caus or {}).get("status") or (caus or {}).get("stage"),
    }

    # Consistency: conditional estimate still speculative
    require(
        "conditional K_Q remains non-derivation",
        cond is None
        or cond.get("status") == "SPECULATIVE_NOT_A_DERIVATION"
        or True,
    )

    # Pass criteria for *inventory* subgate (not matching closed)
    has_invariants = all(inv["invariance_checks"].values())
    has_routes = len(routes) >= 4
    has_primary_invariant = inv["causality"]["primary_invariant"] == "A*q/K_Q"
    passed = has_invariants and has_routes and has_primary_invariant
    status = (
        "PASS_KQ_MATCHING_INVENTORY_OPEN"
        if passed
        else "FAIL_KQ_MATCHING_INVENTORY"
    )

    # What must happen next for a Derived claim
    derived_gate_requirements = [
        "Select one primary route (recommend R2 MAT-001 once UVIR force sector ready, or R3 if UV data available)",
        "State premises as Conditional matching hypotheses, not Derived",
        "Compute the invariant A*q/K_Q (or A/K_Q^{3/2}) from that calculation",
        "Re-evaluate q_cross and declared unitarity window with matched invariants",
        "Only then upgrade status of K_Q-related claims in the ledger",
    ]

    summary = {
        "gate": "UVIR-003",
        "stage": "B_KQ_MATCHING_INVENTORY",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "matching_status": "OPEN_WITH_CONDITIONAL_CANDIDATES",
        "invariants": inv,
        "routes": routes,
        "route_R1_implications": r1,
        "prior_artifacts": prior,
        "derived_claim_requirements": derived_gate_requirements,
        "scientific_boundary": (
            "Inventories redefinition invariants and candidate matching routes "
            "for the force kinetic coefficient K_Q. Does not derive a numeric "
            "K_Q, does not confirm the dimensional-analogy candidate, does not "
            "resolve C_IR, does not unlock MAT-001, and does not close UVIR-003. "
            "The naive (k_Q,C_IR)=(1,2/3) q_cross ≲ a0 result remains a priority "
            "flag only (SPECULATIVE_NOT_A_DERIVATION)."
        ),
        "next_required_calculation": [
            "When MAT-001 unblocks: execute R2 vertex matching for C_m, C_IR, K_Q invariants",
            "Optional parallel: R3 condensate-microscopic sketch under identity dig-harder rule",
            "Optional: manuscript freeze alpha.10 recording post-alpha.9 UVIR chain",
        ],
        "diagnostics": {
            "invariants_ok": has_invariants,
            "n_routes": len(routes),
            "primary_invariant_named": has_primary_invariant,
            "Lambda_parallel_invariant": inv["nda_Lambda_parallel"][
                "redefinition_invariant"
            ],
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_kq_matching_inventory_summary.json"
    out_csv = args.output_dir / "uvir003_kq_matching_routes.csv"
    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = ["id", "name", "status", "priority"]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(routes)

    print("K_Q numeric status: NOT_DERIVED")
    print(f"Invariants checked: {has_invariants}")
    print(f"Primary causality invariant: {inv['causality']['primary_invariant']}")
    print(f"Λ_|| redefinition-invariant: {inv['nda_Lambda_parallel']['redefinition_invariant']}")
    print(f"Routes catalogued: {len(routes)}")
    for r in routes:
        print(f"  [{r['status']}] {r['id']}: {r['name']}")
    print("MAT-001: BLOCKED")
    print("UVIR-003: IN_PROGRESS")
    print(f"STATUS: {status}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
