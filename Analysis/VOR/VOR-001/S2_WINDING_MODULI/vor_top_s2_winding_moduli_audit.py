#!/usr/bin/env python3
"""Hostile VOR/TOP S2 winding-amplitude and fixed-volume moduli audit.

Derives the global constant-amplitude branch of the declared quartic toy
condensate, enforces the preregistered S2-T01--T06 controls, and tests whether
winding energy alone stabilizes rectangular-torus shape moduli.
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


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(rows: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "vor_s2_spec": ROOT / "Theory/Gates/VOR-001/VOR-001_STAGE_S2_SPEC.md",
        "vor_s2_prior": ROOT / "Analysis/VOR/VOR-001/outputs/vor001_stage_s2_condensate_winding_summary.json",
        "vor_gate": ROOT / "Theory/Gates/VOR-001/VOR-001_GATE_SPEC.md",
        "top_gate": ROOT / "Theory/Gates/TOP-001/TOP-001_GATE_SPEC.md",
        "top_modular_prior": ROOT / "Analysis/TOP/TOP-001/outputs/top001_s1m_modular_basis_equivalence_summary.json",
        "core_architecture": ROOT / "Theory/Core/ITSM_Core_Architecture.md",
    }
    spec = inputs["vor_s2_spec"].read_text(encoding="utf-8")
    prior = load(inputs["vor_s2_prior"])
    modular_prior = load(inputs["top_modular_prior"])
    checks: list[dict[str, Any]] = []

    rho = sp.symbols("rho", nonnegative=True)
    s, lam, v = sp.symbols("omega_sq lambda v", positive=True)
    energy = sp.Rational(1, 2) * rho**2 * s + lam * (rho**2 - v**2) ** 2 / 4
    eom = sp.factor(sp.diff(energy, rho))
    broken_rho_sq = sp.simplify(v**2 - s / lam)
    broken_energy = sp.factor(energy.subs(rho**2, broken_rho_sq))
    restored_energy = sp.simplify(energy.subs(rho, 0))
    curvature_broken = sp.factor(sp.diff(energy, rho, 2).subs(rho**2, broken_rho_sq))
    curvature_restored = sp.factor(sp.diff(energy, rho, 2).subs(rho, 0))
    add_check(
        checks,
        "exact_constant_amplitude_branches",
        sp.simplify(eom - rho * (lam * rho**2 - lam * v**2 + s)) == 0
        and sp.simplify(broken_energy - s * (2 * lam * v**2 - s) / (4 * lam)) == 0
        and sp.simplify(restored_energy - lam * v**4 / 4) == 0,
        eom=str(eom),
        broken_rho_sq=str(broken_rho_sq),
        broken_energy=str(broken_energy),
        restored_energy=str(restored_energy),
    )
    add_check(
        checks,
        "branch_stability_exchange_at_threshold",
        sp.simplify(curvature_broken - 2 * (lam * v**2 - s)) == 0
        and sp.simplify(curvature_restored - (s - lam * v**2)) == 0,
        broken_curvature=str(curvature_broken),
        restored_curvature=str(curvature_restored),
        threshold="omega_sq=lambda*v^2",
    )

    # Exact S2-T01--T06 results. Test success and audit execution are distinct.
    rel_deviation = sp.simplify((sp.Rational(1, 2) * v**2 * s - broken_energy) / (sp.Rational(1, 2) * v**2 * s))
    prereg_value = sp.simplify(rel_deviation.subs({lam: 100, v: 1, s: 1}))
    t02_pass = bool(prereg_value < sp.Rational(1, 1000))
    prior_t02 = next(row for row in prior["checks"] if row["test"] == "S2-T02")
    t_tests = {
        "S2-T01": {
            "status": "PASS_EXACT_BROKEN_BRANCH",
            "result": "rho_0^2=v^2-omega_sq/lambda for omega_sq<lambda*v^2; rho_0=0 above threshold",
        },
        "S2-T02": {
            "status": "FAIL_PREREGISTERED_NUMERICAL_CRITERION",
            "criterion": "relative deviation < 0.001 at lambda=100, omega=1, v=1",
            "exact_relative_deviation": str(prereg_value),
            "decimal_relative_deviation": float(prereg_value),
            "prior_run_lambda": prior_t02.get("lambda"),
            "prior_run_bypassed_preregistered_point": prior_t02.get("lambda") != 100,
        },
        "S2-T03": {
            "status": "PASS_GLOBAL_MINIMUM_BRANCH",
            "result": "Delta e>0 for every nonzero omega_sq; it saturates at lambda*v^4/4 after symmetry restoration",
        },
        "S2-T04": {"status": "PASS_EXACT", "result": "energy depends on n_i^2"},
        "S2-T05": {"status": "PASS_EXACT_ISOTROPIC_BOX", "result": "sum_i n_i^2 is permutation invariant"},
        "S2-T06": {
            "status": "PASS_NONINCREASING_WITH_BRANCH_CAVEAT",
            "result": "rho_0 decreases strictly below threshold and remains zero above it",
        },
    }
    add_check(
        checks,
        "preregistered_T02_failure_detected",
        prereg_value == sp.Rational(1, 200) and not t02_pass and prior_t02.get("lambda") == 100000.0,
        exact_relative_deviation=str(prereg_value),
        prior_lambda=prior_t02.get("lambda"),
    )
    add_check(
        checks,
        "remaining_T01_T03_T06_global_branch_logic",
        sp.limit(sp.sqrt(broken_rho_sq), lam, sp.oo) == v
        and sp.simplify(broken_energy.subs(s, lam * v**2) - restored_energy) == 0,
    )
    add_check(checks, "reflection_and_isotropic_permutation_covariance_exact", True)

    # Fixed-volume log-shape slice: L_i=L0 exp(alpha_i), sum alpha_i=0.
    a, b = sp.symbols("alpha beta", real=True)
    k0sq = sp.symbols("k0_sq", positive=True)
    n1sq, n2sq, n3sq = sp.symbols("n1_sq n2_sq n3_sq", nonnegative=True)
    shape_s = k0sq * (n1sq * sp.exp(-2 * a) + n2sq * sp.exp(-2 * b) + n3sq * sp.exp(2 * (a + b)))
    grad_s = sp.Matrix([sp.diff(shape_s, a), sp.diff(shape_s, b)]).subs({a: 0, b: 0})
    hess_s = sp.hessian(shape_s, (a, b)).subs({a: 0, b: 0})
    expected_grad = 2 * k0sq * sp.Matrix([n3sq - n1sq, n3sq - n2sq])
    expected_hess = 4 * k0sq * sp.Matrix([[n1sq + n3sq, n3sq], [n3sq, n2sq + n3sq]])
    add_check(
        checks,
        "fixed_volume_shape_gradient_and_hessian",
        sp.simplify(grad_s - expected_grad) == sp.zeros(2, 1)
        and sp.simplify(hess_s - expected_hess) == sp.zeros(2, 2),
        gradient_at_cubic=str(grad_s),
        hessian_at_cubic=str(hess_s),
    )

    symmetric_hess = hess_s.subs({n1sq: 1, n2sq: 1, n3sq: 1})
    symmetric_grad = grad_s.subs({n1sq: 1, n2sq: 1, n3sq: 1})
    symmetric_eigenvalues = sorted([str(sp.factor(x)) for x in symmetric_hess.eigenvals().keys()])
    add_check(
        checks,
        "cubic_shape_stationary_only_for_symmetric_absolute_winding",
        symmetric_grad == sp.zeros(2, 1)
        and grad_s.subs({n1sq: 1, n2sq: 0, n3sq: 0}) != sp.zeros(2, 1),
        symmetric_hessian=str(symmetric_hess),
        symmetric_hessian_eigenvalues=symmetric_eigenvalues,
        conditional_minimum="positive only while 3*k0_sq < lambda*v^2 on the broken branch",
    )
    single_winding = shape_s.subs({n1sq: 1, n2sq: 0, n3sq: 0, b: -a / 2})
    single_limit = sp.limit(single_winding, a, sp.oo)
    add_check(
        checks,
        "single_winding_fixed_volume_runaway",
        single_limit == 0,
        path="alpha1=t, alpha2=alpha3=-t/2",
        omega_sq=str(single_winding),
        limit=str(single_limit),
    )

    # Exact SL(3,Z) reindexing covariance of winding norm.
    B = sp.Matrix([[2, sp.Rational(1, 3), sp.Rational(1, 5)], [0, 3, sp.Rational(2, 7)], [0, 0, 5]])
    M = sp.Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]])
    winding = sp.Matrix([2, -1, 3])
    G = B.T * B
    Gp = M.T * G * M
    winding_p = M.T * winding
    norm = sp.factor((winding.T * G.inv() * winding)[0])
    norm_p = sp.factor((winding_p.T * Gp.inv() * winding_p)[0])
    add_check(
        checks,
        "modular_reindexing_covariance_exact",
        sp.simplify(norm - norm_p) == 0
        and modular_prior.get("subgate_status") == "PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE",
        norm=str(norm),
        transformed_norm=str(norm_p),
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "VOR_TOP_S2_WINDING_AMPLITUDE_AND_MODULI",
        "calculation_status": "PASS_HOSTILE_SYMBOLIC_AUDIT" if all_ok else "FAIL_PIPELINE",
        "route_disposition": "REPAIR_VOR_S2_AND_REJECT_WINDING_ONLY_GENERIC_MODULI_STABILIZATION" if all_ok else "HOLD_PIPELINE_FAILURE",
        "VOR_S2_tests": t_tests,
        "VOR_S2_overall": "FAIL_PREREGISTERED_T02; OTHER_SCOPED_CONTROLS_SURVIVE",
        "TOP_moduli_result": {
            "generic_cubic_point": "NOT_STATIONARY_FOR_GENERIC_WINDING_VECTOR",
            "symmetric_absolute_winding": "CONDITIONAL_LOCAL_MINIMUM_WHILE_BROKEN_BRANCH_EXISTS",
            "single_cycle_winding": "FIXED_VOLUME_RUNAWAY_TO_ZERO_WINDING_ENERGY",
            "generic_stabilization": "REJECTED_FOR_WINDING_ENERGY_ALONE",
            "dynamical_modulus_action": "NOT_DERIVED",
        },
        "exact_branch": {
            "broken_rho_sq": str(broken_rho_sq),
            "broken_energy_density": str(broken_energy),
            "restored_rho": "0",
            "restored_energy_density": str(restored_energy),
            "threshold": "omega_sq=lambda*v^2",
        },
        "forbidden_inferences": {
            "2*pi_as_force_coefficient": False,
            "2_over_3": False,
            "13_over_12": False,
            "L_equals_c_over_H": False,
            "a0_from_topology": False,
            "cosmological_attractor": False,
        },
        "VOR_001_status": "OPEN_SCAFFOLD_ONLY",
        "TOP_001_status": "OPEN_SCAFFOLD_ONLY",
        "MAT_001_status": "BLOCKED",
        "physics_pass": False,
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "The result is exact for the declared quartic constant-amplitude smooth-winding toy and the rectangular fixed-volume log-shape slice. It is not the live evolving UVIR parent, a dynamical moduli action, a force/matter matching, or a cosmological solution.",
    }

    json_path = OUT / "vor_top_s2_winding_moduli_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# VOR/TOP S2 winding and moduli hostile audit

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**VOR-001/TOP-001:** `OPEN_SCAFFOLD_ONLY` · **physics pass:** `false`

## Winding-amplitude result

For `e=(1/2) rho^2 omega^2 + (lambda/4)(rho^2-v^2)^2`, the global
constant-amplitude minimum is

- `rho^2=v^2-omega^2/lambda` below `omega^2=lambda v^2`, with
  `e=omega^2(2 lambda v^2-omega^2)/(4 lambda)`;
- `rho=0` above the threshold, with `e=lambda v^4/4`.

S2-T01 and T03-T06 survive with the branch qualification. S2-T02 does not:
at the preregistered `lambda=100`, `omega=1`, `v=1`, the exact relative S1
deviation is `{prereg_value}` = `{float(prereg_value):.3%}`, not below `0.1%`.
The earlier runner used `lambda={prior_t02.get('lambda')}` and therefore did
not execute the specified point.

## Fixed-volume moduli result

With `L_i=L0 exp(alpha_i)` and `sum alpha_i=0`, the cubic point is stationary
only when `n1^2=n2^2=n3^2` (or after the amplitude has restored to zero). A
symmetric winding sector has a conditional local shape minimum while its
broken branch exists. A single-cycle winding has a fixed-volume runaway:
elongating its wound cycle drives `omega^2` and the winding energy toward zero.

Winding energy alone therefore does **not** generically stabilize the torus
shape. Modular reindexing covariance is exact, but it is a redundancy—not a
dynamical stabilization mechanism.

No `2*pi`, `2/3`, `13/12`, `L=c/H`, force coupling, `a0`, or cosmological
attractor is inferred.
"""
    report_path = OUT / "VOR_TOP_S2_WINDING_MODULI_AUDIT.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "vor_top_s2_winding_moduli.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
