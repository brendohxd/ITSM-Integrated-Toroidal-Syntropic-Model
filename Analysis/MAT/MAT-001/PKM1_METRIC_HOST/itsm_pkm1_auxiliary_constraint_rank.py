#!/usr/bin/env python3
"""PKM1 non-affine auxiliary constraint-rank audit.

This is a local deep-regime Dirac sub-block, not the full metric-khronon-
condensate Hamiltonian. It tests whether the deliberately constructed
susceptibility variable is genuinely auxiliary for Y>0 and identifies its
zero-gradient rank-loss boundary.
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
        "pkm1_screen": OUT / "itsm_pkm1_metric_hosted_khronon_summary.json",
        "pkm1_obstruction": OUT / "itsm_pkm1_a2_a6_obstruction_summary.json",
        "core_identity": ROOT / "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md",
        "tier1_programme": ROOT / "Theory/Core/ITSM_Tier1_Route_Test_Programme.md",
    }
    screen = load(inputs["pkm1_screen"])
    obstruction = load(inputs["pkm1_obstruction"])
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "route_enters_as_new_fail_closed_action_class",
        screen.get("route_disposition")
        == "SELECT_PKM1_FOR_A2_A6_DERIVATION_NOT_GATE_PROMOTION"
        and obstruction.get("route_disposition")
        == "ADVANCE_PKM1_TO_FULL_PARENT_HAMILTONIAN_ONLY",
    )

    Y, a0, s = sp.symbols("Y a0 s", positive=True)
    F = Y**2 / (2 * a0**2 * s) + a0**2 * s**3 / 6
    constraint_s = sp.diff(F, s)
    hessian_s = sp.diff(constraint_s, s)
    s_star = sp.sqrt(Y) / a0
    effective_energy = sp.simplify(F.subs(s, s_star))
    hessian_on_shell = sp.simplify(hessian_s.subs(s, s_star))
    add_check(
        checks,
        "exact_nonaffine_elimination_identity",
        sp.simplify(constraint_s.subs(s, s_star)) == 0
        and effective_energy
        == sp.Rational(2, 3) * Y ** sp.Rational(3, 2) / a0
        and hessian_on_shell == 2 * a0 * sp.sqrt(Y),
        static_energy=str(F),
        secondary_constraint=str(constraint_s),
        stationary_point=str(s_star),
        on_shell_hessian=str(hessian_on_shell),
        effective_energy=str(effective_energy),
    )

    # Since no dot(s) occurs, p_s=0 is primary. Preservation produces
    # C_s=dF/ds=0. Their local Poisson bracket is -dC_s/ds.
    p_s, dot_s = sp.symbols("p_s dot_s", real=True)
    primary_momentum = sp.Integer(0)
    constraint_bracket_on_shell = sp.simplify(-hessian_on_shell)
    add_check(
        checks,
        "local_second_class_auxiliary_pair_for_positive_Y",
        primary_momentum == 0
        and dot_s not in F.free_symbols
        and constraint_bracket_on_shell == -2 * a0 * sp.sqrt(Y),
        primary_constraint="p_s=0",
        secondary_constraint="C_s=dF/ds=0",
        poisson_bracket=str(constraint_bracket_on_shell),
        phase_space_variables=2,
        second_class_constraints=2,
        local_propagating_auxiliary_DOF=0,
        scope="strictly Y>0 only; metric, phase and amplitude constraints are not counted here",
    )

    bracket_zero_limit = sp.limit(constraint_bracket_on_shell, Y, 0, dir="+")
    stiffness_zero_limit = sp.limit(hessian_on_shell, Y, 0, dir="+")
    add_check(
        checks,
        "zero_gradient_constraint_rank_loss",
        bracket_zero_limit == 0
        and stiffness_zero_limit == 0
        and sp.limit(s_star, Y, 0, dir="+") == 0,
        s_star_limit="0 from the positive-s branch",
        bracket_limit=str(bracket_zero_limit),
        stiffness_limit=str(stiffness_zero_limit),
        consequence="the second-class test degenerates and the strict s>0 chart ends at Y=0",
    )

    # A gapped analytic control produces only integer powers of Y. This is a
    # concrete check illustrating the implicit-function-theorem obstruction.
    chi, coupling = sp.symbols("chi g", real=True)
    mass_sq = sp.symbols("m_sq", positive=True)
    analytic_parent = mass_sq * chi**2 / 2 + coupling * chi * Y
    chi_star = sp.solve(sp.diff(analytic_parent, chi), chi)[0]
    analytic_effective = sp.factor(analytic_parent.subs(chi, chi_star))
    add_check(
        checks,
        "gapped_analytic_parent_control_has_integer_power_series",
        chi_star == -Y * coupling / mass_sq
        and analytic_effective == -Y**2 * coupling**2 / (2 * mass_sq),
        stationary_point=str(chi_star),
        effective_energy=str(analytic_effective),
        implication="with a nonsingular heavy Hessian, the implicit function theorem gives an analytic integer-power effective action near Y=0; an exact Y^(3/2) term requires a critical, singular, gapless, nonlocal, or explicitly nonanalytic ingredient",
    )

    deep_to_high_ratio = sp.simplify(effective_energy / Y)
    add_check(
        checks,
        "constructed_parent_is_deep_regime_only",
        sp.limit(deep_to_high_ratio, Y, sp.oo) == sp.oo,
        F_over_Y=str(deep_to_high_ratio),
        high_Y_limit="infinity",
        consequence="this auxiliary block cannot supply the high-acceleration GR join; it must not be advertised as a global J(Y)",
    )

    dimensions = {"Y": 2, "a0": 1, "s": 0, "F": 2}
    add_check(
        checks,
        "mass_dimensions_close",
        2 * dimensions["Y"] - 2 * dimensions["a0"] - dimensions["s"]
        == dimensions["F"]
        and 2 * dimensions["a0"] + 3 * dimensions["s"] == dimensions["F"],
        dimensions=dimensions,
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "PKM1_NONAFFINE_AUXILIARY_CONSTRAINT_RANK",
        "calculation_status": "PASS_LOCAL_DIRAC_SUBBLOCK" if all_ok else "FAIL_PIPELINE",
        "route_disposition": (
            "HOLD_PKM1_GLOBAL_PARENT_LOCAL_AUXILIARY_SECOND_CLASS_FOR_Y_GT_0"
            if all_ok
            else "HOLD_PIPELINE_FAILURE"
        ),
        "constructed_parent": {
            "weak_static_total_energy": "F(Y,s)=Y^2/(2*a0^2*s)+(a0^2/6)*s^3, s>0",
            "corresponding_deep_J": "J_deep(Y,s)=-Y+F(Y,s)",
            "classification": "ENGINEERED_NONAFFINE_DEEP_IR_CONTROL_NOT_MICROSCOPIC_DERIVATION",
        },
        "local_constraint_result": {
            "domain": "Y>0",
            "primary": "p_s=0",
            "secondary": "dF/ds=0",
            "bracket": "-2*a0*sqrt(Y)",
            "auxiliary_DOF": 0,
        },
        "hard_boundary": {
            "domain": "Y=0",
            "result": "CONSTRAINT_RANK_LOSS_AND_END_OF_STRICT_POSITIVE_S_CHART",
            "interpretation": "criticality is not optional for this exact fractional-power representation",
        },
        "next_calculation": "Embed this block in one covariant finite-density rho-Theta-metric parent, specify a global high-acceleration join, and perform the complete ADM/Dirac and characteristic analysis across Y>0 and Y=0.",
        "gate_firewall": {
            "MAT_001": "BLOCKED",
            "UVIR_003": "IN_PROGRESS",
            "physics_pass": False,
            "canonical_action_replaced": False,
            "downstream_opened": False,
        },
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "The calculation establishes only the local constraint class of one deliberately engineered deep-static auxiliary block. It neither derives that block from condensate microphysics nor counts the metric, phase, amplitude, topology, reservoir, or matter degrees of freedom.",
    }
    json_path = OUT / "itsm_pkm1_auxiliary_constraint_rank_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# PKM1 non-affine auxiliary constraint-rank audit

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**Physics pass:** `false`

## Exact local result

For the deliberately constructed deep-static block

`F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3`, with `s>0`,

the stationary point is `s_star=sqrt(Y)/a0`. Eliminating `s` gives exactly

`F_eff=(2/3)Y^(3/2)/a0`.

Because the action contains no `dot(s)`, `p_s=0` is a primary constraint and
`dF/ds=0` is secondary. Their on-shell Poisson bracket is

`{{p_s,C_s}}=-2 a0 sqrt(Y)`.

It is nonzero for `Y>0`, so the pair is locally second class and removes the
two-dimensional `(s,p_s)` phase space: this susceptibility adds zero local
propagating degrees of freedom in that restricted patch.

## Hard zero-gradient boundary

As `Y -> 0+`, `s_star`, the stationary curvature, and the constraint bracket
all vanish. The strict `s>0` chart ends and the constraint rank changes. This
is not a technical nuisance: a gapped analytic heavy sector with an invertible
Hessian would generate an analytic integer-power series near `Y=0`, not an
exact fractional `Y^(3/2)` term. Exact deep behaviour therefore requires a
critical, singular, gapless, nonlocal, or explicitly nonanalytic ingredient.

## Scope and decision

The block is an engineered representation of the desired operator, not an
ITSM microscopic derivation. It also grows relative to `Y` at high
acceleration and therefore supplies no GR join. It is useful because it turns
the broad question into one sharp calculation: embed this block in a
finite-density `rho-Theta-metric` parent and test whether the complete
constraint algebra and characteristics remain healthy through `Y=0`.

MAT-001 remains `BLOCKED`; UVIR-003 remains `IN_PROGRESS`; no downstream gate
is opened.
"""
    report_path = OUT / "ITSM_PKM1_AUXILIARY_CONSTRAINT_RANK.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "itsm_pkm1_auxiliary_constraint_rank.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
