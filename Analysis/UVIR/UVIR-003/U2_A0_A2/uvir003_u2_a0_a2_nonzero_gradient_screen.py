#!/usr/bin/env python3
"""UVIR-003 U2 exact nonzero-gradient A0-A2 fail-closed screen.

Re-derives the local Y^(3/2) expansion and then tests whether the repository
contains the action-domain and constrained-DOF evidence required to advance
U2 beyond A0-A2.  Script PASS means the audit executed, not a physics PASS.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(rows: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "local_exact": ROOT / "Analysis/UVIR/UVIR-003/outputs/uvir003_nonzero_gradient_force_local_summary.json",
        "closure_audit": ROOT / "Analysis/UVIR/UVIR-003/outputs/uvir003_full_gate_closure_audit_summary.json",
        "stage_a": ROOT / "Theory/Gates/UVIR-003/UVIR-003_STAGE_A_REPORT.md",
        "core_architecture": ROOT / "Theory/Core/ITSM_Core_Architecture.md",
        "tier1_programme": ROOT / "Theory/Core/ITSM_Tier1_Route_Test_Programme.md",
    }
    local = load_json(inputs["local_exact"])
    closure = load_json(inputs["closure_audit"])
    stage_a = inputs["stage_a"].read_text(encoding="utf-8")
    core = inputs["core_architecture"].read_text(encoding="utf-8")
    programme = inputs["tier1_programme"].read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    # Independent exact expansion around grad(psi_bar)=v e_x, v>0.
    eps = sp.symbols("epsilon", real=True)
    v, A = sp.symbols("v A_IR", positive=True)
    x, y, z = sp.symbols("x y z", real=True)
    f = ((v + eps * x) ** 2 + eps**2 * (y**2 + z**2)) ** sp.Rational(3, 2)
    series = sp.series(f, eps, 0, 5).removeO().expand()
    coeff = [sp.simplify(series.coeff(eps, i)) for i in range(5)]
    expected = [
        v**3,
        3 * v**2 * x,
        sp.Rational(3, 2) * v * (2 * x**2 + y**2 + z**2),
        sp.Rational(1, 2) * x * (2 * x**2 + 3 * y**2 + 3 * z**2),
        sp.Rational(3, 8) * (y**2 + z**2) ** 2 / v,
    ]
    add_check(checks, "exact_nonzero_gradient_series", all(sp.simplify(a - b) == 0 for a, b in zip(coeff, expected)), coefficients=[str(c) for c in coeff])

    g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
    potential = A * (g1**2 + g2**2 + g3**2) ** sp.Rational(3, 2)
    hessian = sp.hessian(potential, (g1, g2, g3)).subs({g1: v, g2: 0, g3: 0})
    eigenvalues = sorted([str(sp.simplify(ev)) for ev in hessian.eigenvals()], reverse=True)
    add_check(
        checks,
        "anisotropic_spatial_hessian",
        hessian == sp.diag(6 * A * v, 3 * A * v, 3 * A * v),
        matrix=str(hessian),
        longitudinal=str(6 * A * v),
        transverse=str(3 * A * v),
        distinct_eigenvalues=eigenvalues,
    )
    quartic = expected[4]
    add_check(checks, "zero_gradient_boundary_is_singular", sp.limit(quartic.subs({y: 1, z: 0}), v, 0, dir="+") == sp.oo, quartic=str(quartic))
    add_check(
        checks,
        "independent_reproduction_matches_prior_local_artifact",
        local.get("subgate_status") == "PASS_NONZERO_GRADIENT_FORCE_LOCAL"
        and local.get("analytic", {}).get("quartic_singular_as_v_to_0") is True
        and local.get("full_gate_status") == "IN_PROGRESS",
    )

    # Evidence tests for A0-A2. These are deliberately fail-closed.
    a0_ok = (
        "finite-density" in core
        and "separate force field `psi`" in core
        and "Y^(3/2)" in core
        and "U2 | Exact nonzero-gradient `Y^(3/2)`" in programme
    )
    add_check(checks, "A0_identity_fidelity_is_declared", a0_ok)

    restricted_completion_open = (
        "generally covariant completion" in stage_a
        and "is not yet fixed" in stage_a
        and "K_Q" in stage_a
        and "M_*" in stage_a
    )
    add_check(checks, "A1_restricted_action_limitation_is_explicit", restricted_completion_open)

    blockers = set(closure.get("blocking_for_full_pass", []))
    required_blockers = {
        "M2_stability_declared_domain",
        "M3_causality_declared_domain",
        "M6_physical_cutoff",
        "M7_matter_ready_for_MAT",
    }
    add_check(checks, "A2_and_domain_blockers_remain_live", required_blockers.issubset(blockers), blockers=sorted(blockers))
    add_check(
        checks,
        "gate_firewall_preserved",
        closure.get("full_gate_status") == "IN_PROGRESS"
        and closure.get("mat001_status") == "BLOCKED_PASS_TAG_FORBIDDEN",
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "UVIR003_U2_A0_A2_EXACT_NONZERO_GRADIENT_SCREEN",
        "calculation_status": "PASS_AUDIT_PIPELINE" if all_ok else "FAIL_AUDIT_PIPELINE",
        "route_disposition": "FREEZE_U2_AT_A0_A2_INCOMPLETE_ACTION_DOMAIN_AND_DOF" if all_ok else "HOLD_PIPELINE_FAILURE",
        "A0_identity": {
            "status": "PASS_BOUNDED_IDENTITY_FIDELITY",
            "note": "The exact nonanalytic force operator remains a separate conditional force-sector route inside the declared finite-density/toroidal/open-system identity; it is not substituted for the condensate parent.",
        },
        "A1_action": {
            "status": "HOLD_RESTRICTED_BACKGROUND_ACTION_NOT_FULL_DOMAIN",
            "note": "The local operator is exact for v>0, but the regulator's generally covariant completion and the v=0 interface are not fixed; K_Q and the physical cutoff are unmatched.",
        },
        "A2_symmetry_DOF": {
            "status": "HOLD_LOCAL_HESSIAN_ONLY_FULL_CONSTRAINT_DOF_UNRESOLVED",
            "note": "Positive spatial Hessian eigenvalues establish a local gradient-sector result only. They are not a constrained Hamiltonian/ghost count for the coupled condensate-frame-force action.",
        },
        "local_exact_result": {
            "background": "grad(psi_bar)=v e_x, v>0",
            "hessian_longitudinal": str(6 * A * v),
            "hessian_transverse": str(3 * A * v),
            "quartic": str(quartic),
            "zero_gradient_join": "SINGULAR_NOT_DEFINED_BY_THIS_PATCH",
        },
        "force_regime_overlap_below_cutoff": "NOT_ESTABLISHED",
        "ghost_or_double_count_result": "NO_LOCAL_SPATIAL_HESSIAN_GHOST_FOUND; FULL_COUPLED_DOF_TEST_NOT_DONE",
        "UVIR_003_status": "IN_PROGRESS",
        "MAT_001_status": "BLOCKED",
        "K_Q_status": "NOT_DERIVED",
        "physics_pass": False,
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "This screen exactly verifies the local nonzero-gradient Y^(3/2) patch and its positive anisotropic spatial Hessian. It does not establish a full covariant action domain, the coupled constrained DOF count, a physical cutoff, causality, the v=0 join, or overlap with the galaxy force regime.",
    }

    json_path = OUT / "uvir003_u2_a0_a2_nonzero_gradient_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# UVIR-003 U2 exact nonzero-gradient A0-A2 screen

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**UVIR-003:** `IN_PROGRESS` · **MAT-001:** `BLOCKED` · **physics pass:** `false`

## Exact result

For `grad(psi_bar)=v e_x`, `v>0`, the exact `Y^(3/2)` expansion independently
reproduces the prior local result. The spatial potential Hessian is

- longitudinal: `{6 * A * v}`;
- transverse: `{3 * A * v}` (twice).

Both are positive for `A_IR>0` and `v>0`. The quartic coefficient is
`{quartic}` and diverges at the zero-gradient boundary.

## A0-A2 disposition

- **A0 — `PASS_BOUNDED_IDENTITY_FIDELITY`:** the route preserves the declared
  separate force sector and does not replace the finite-density condensate.
- **A1 — `HOLD_RESTRICTED_BACKGROUND_ACTION_NOT_FULL_DOMAIN`:** the exact local
  patch exists, but the regulator's general covariant completion, zero-gradient
  join, matched `K_Q`, and physical cutoff do not.
- **A2 — `HOLD_LOCAL_HESSIAN_ONLY_FULL_CONSTRAINT_DOF_UNRESOLVED`:** a positive
  spatial Hessian is not the full coupled constraint/Hamiltonian count.

U2 therefore freezes at A0-A2. The repository has not established that this
patch overlaps the galaxy-force regime below the physical cutoff, and no
parent-gate promotion follows.
"""
    report_path = OUT / "UVIR-003_U2_A0_A2_NONZERO_GRADIENT.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "uvir003_u2_a0_a2_nonzero_gradient.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
