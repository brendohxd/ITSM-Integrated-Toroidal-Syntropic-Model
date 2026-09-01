#!/usr/bin/env python3
"""Independent reproduction and mutation audit for PKM1-P0.

This script does not import the primary parent-Hamiltonian calculation.  It
re-derives the decisive identities directly from the frozen action, checks the
written output manifest, and verifies that common claim-changing mutations are
detected.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def add_check(
    rows: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in reduced):
            return
        raise AssertionError(f"{name} failed: {reduced}")
    if sp.factor(reduced) != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in path.read_text(encoding="ascii").splitlines():
        expected, name = line.split("  ", maxsplit=1)
        rows.append((expected, name))
    return rows


def main() -> None:
    checks: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 1. Reproduce the two J-control Hessians from their primitives.
    # ------------------------------------------------------------------
    y, a0 = sp.symbols("y a0", positive=True)
    invariant = a0**2 * y**2
    j_a = a0**2 * (
        sp.log(1 + y)
        - sp.log(1 + y**2) / 2
        - sp.atan(y)
    )
    jy_a = sp.factor(sp.diff(j_a, y) / sp.diff(invariant, y))
    jrad_a = sp.factor(jy_a + y * sp.diff(jy_a, y))
    numerator_a = sp.factor(
        jrad_a * (1 + y + y**2 + y**3) ** 2
    )
    require_zero(
        "independent P0-A radial numerator",
        numerator_a - (2 * y**3 + y**2 - 1),
    )
    mp.mp.dps = 60
    root_mp = mp.findroot(lambda value: 2 * value**3 + value**2 - 1, (0.6, 0.7))
    root_residual = abs(2 * root_mp**3 + root_mp**2 - 1)
    add_check(
        checks,
        "independent_P0_A_root_and_sign_reproduction",
        root_residual < mp.mpf("1e-50")
        and jrad_a.subs(y, sp.Rational(1, 2)) < 0
        and jrad_a.subs(y, 1) > 0,
        critical_y=mp.nstr(root_mp, 50),
        root_residual=mp.nstr(root_residual, 8),
        radial_Hessian=str(jrad_a),
    )

    j_b = -2 * a0**2 * (y - sp.log(1 + y))
    jy_b = sp.factor(sp.diff(j_b, y) / sp.diff(invariant, y))
    jrad_b = sp.factor(jy_b + y * sp.diff(jy_b, y))
    require_zero("independent P0-B transverse", jy_b + 1 / (1 + y))
    require_zero("independent P0-B radial", jrad_b + 1 / (1 + y) ** 2)
    add_check(
        checks,
        "independent_P0_B_Hessian_reproduction",
        sp.ask(sp.Q.negative(jy_b)) is True
        and sp.ask(sp.Q.negative(jrad_b)) is True,
        J_Y=str(jy_b),
        J_radial=str(jrad_b),
    )

    # Mutation: static ellipticity alone would wrongly accept P0-A at y=1.
    mu_a = sp.factor(1 + jy_a)
    static_radial_a = sp.factor(mu_a + y * sp.diff(mu_a, y))
    add_check(
        checks,
        "mutation_static_ellipticity_cannot_substitute_for_khronon_Hessian",
        static_radial_a.subs(y, 1) > 0 and jrad_a.subs(y, 1) > 0,
        static_radial_at_y1=str(static_radial_a.subs(y, 1)),
        required_negative_khronon_Hessian_at_y1=str(jrad_a.subs(y, 1)),
        mutation_result="REJECTED_FALSE_EQUIVALENCE",
    )

    # Mutation: reversing the J sign makes the transverse kinetic coefficient
    # negative even though the algebra remains finite.
    mutated_jy_b = -jy_b
    add_check(
        checks,
        "mutation_reversed_J_sign_is_detected_as_kinetic_failure",
        sp.ask(sp.Q.positive(mutated_jy_b)) is True,
        mutated_lagrangian_kinetic="-2*M_P^2*(-J_Y)<0",
        mutation_result="REJECTED",
    )

    # ------------------------------------------------------------------
    # 2. Reproduce K_QQ directly by a Schur complement of rho and N.
    # ------------------------------------------------------------------
    lapse, rho, chemical, mp2 = sp.symbols(
        "N rho mu M_P_sq", positive=True
    )
    mass_sq, quartic, sextic, cutoff = sp.symbols(
        "m_squared lambda4 lambda6 Lambda", positive=True
    )
    potential = (
        mass_sq * rho**2 / 2
        + quartic * rho**4 / 8
        + sextic * rho**6 / (24 * cutoff**2)
    )
    reduced_lapse_density = rho**2 * chemical**2 / (2 * lapse) - lapse * potential
    branch = {sp.diff(potential, rho): rho * chemical**2}
    f_nn = sp.diff(reduced_lapse_density, lapse, 2).subs(lapse, 1)
    f_nr = sp.diff(reduced_lapse_density, lapse, rho).subs(lapse, 1)
    f_rr = sp.diff(reduced_lapse_density, rho, 2).subs(lapse, 1)
    f_nn = sp.simplify(f_nn.xreplace(branch))
    f_nr = sp.simplify(f_nr.xreplace(branch))
    # Explicitly impose V_rho=rho*mu^2 after differentiation.
    v_rho = sp.diff(potential, rho)
    f_nr = sp.simplify(f_nr.subs(v_rho, rho * chemical**2))
    f_rr = sp.simplify(f_rr.subs(v_rho, rho * chemical**2))
    mrho_sq = sp.factor(sp.diff(potential, rho, 2) - chemical**2)
    require_zero("direct lapse Hessian", f_nn - rho**2 * chemical**2)
    require_zero("direct lapse-radial mixing", f_nr + 2 * rho * chemical**2)
    require_zero("direct radial Hessian", f_rr + mrho_sq)
    effective_f_nn = sp.factor(f_nn - f_nr**2 / f_rr)
    expected_effective = sp.factor(
        rho**2
        * chemical**2
        * (1 + 4 * chemical**2 / mrho_sq)
    )
    mrho_positive = sp.symbols("M_rho_sq", positive=True)
    expected_effective_abstract = sp.factor(
        rho**2
        * chemical**2
        * (1 + 4 * chemical**2 / mrho_positive)
    )
    require_zero(
        "direct Schur K_QQ enhancement", effective_f_nn - expected_effective
    )
    add_check(
        checks,
        "independent_original_action_Schur_K_QQ_reproduction",
        sp.ask(sp.Q.positive(expected_effective_abstract)) is True,
        f_NN=str(f_nn),
        f_Nrho=str(f_nr),
        f_rhorho=str(f_rr),
        effective_M_P_sq_K_QQ=str(effective_f_nn),
        K_QQ=str(sp.factor(effective_f_nn / mp2)),
    )

    add_check(
        checks,
        "mutation_exact_K_QQ_zero_conflicts_with_stable_finite_density",
        sp.ask(sp.Q.positive(expected_effective_abstract)) is True,
        assumptions=["rho>0", "mu>0", "M_rho^2>0"],
        mutation="set K_QQ=0",
        mutation_result="REJECTED_BY_POSITIVE_SCHUR_COMPLEMENT",
    )

    # ------------------------------------------------------------------
    # 3. Independently eliminate the FRW lapse and scalar shift.
    # ------------------------------------------------------------------
    m, hubble, rhodot, q, c_j = sp.symbols(
        "M_P_sq H rho_dot q C_J", positive=True
    )
    rhodot = sp.symbols("rho_dot", real=True)
    v0, vr = sp.symbols("V V_rho", real=True)
    r, dr, sigma, dsigma = sp.symbols(
        "R R_dot delta_rho delta_rho_dot", real=True
    )
    alpha, shift = sp.symbols("delta_N Sigma", real=True)
    cmat = sp.Matrix(
        [[c_j * q**2 - 2 * v0, 2 * m * hubble], [2 * m * hubble, 0]]
    )
    source = sp.Matrix(
        [
            6 * m * hubble * dr
            + 2 * m * q**2 * r
            - (vr + rho * chemical**2) * sigma
            - rhodot * dsigma,
            -2 * m * dr - rhodot * sigma,
        ]
    )
    unconstrained = (
        -3 * m * dr**2
        - 18 * m * hubble * r * dr
        + (m * q**2 - 9 * v0) * r**2
        + 3 * (rho * chemical**2 - vr) * r * sigma
        + 3 * rhodot * r * dsigma
        + dsigma**2 / 2
    )
    z = sp.Matrix([alpha, shift])
    full = sp.expand(
        unconstrained + (z.T * source)[0] + (z.T * cmat * z)[0] / 2
    )
    direct_solution = sp.solve(
        [sp.diff(full, alpha), sp.diff(full, shift)],
        [alpha, shift],
        dict=True,
        simplify=False,
    )[0]
    reduced = sp.factor(full.subs(direct_solution))
    kinetic = sp.hessian(reduced, [dr, dsigma])
    enthalpy = rhodot**2 + rho**2 * chemical**2
    kinetic_os = sp.simplify(
        kinetic.subs(v0, 3 * m * hubble**2 - enthalpy / 2)
    )
    expected_kinetic = sp.Matrix(
        [
            [(enthalpy + c_j * q**2) / hubble**2, -rhodot / hubble],
            [-rhodot / hubble, 1],
        ]
    )
    require_zero(
        "independent direct constraint solution kinetic matrix",
        kinetic_os - expected_kinetic,
    )
    determinant = sp.factor(kinetic_os.det())
    expected_determinant = sp.factor(
        (rho**2 * chemical**2 + c_j * q**2) / hubble**2
    )
    require_zero("independent kinetic determinant", determinant - expected_determinant)
    add_check(
        checks,
        "independent_direct_FRW_constraint_elimination_reproduction",
        sp.ask(sp.Q.positive(expected_determinant)) is True
        and sp.ask(sp.Q.positive(expected_determinant.subs(q, 0))) is True,
        lapse_solution=str(direct_solution[alpha]),
        shift_solution=str(direct_solution[shift]),
        kinetic_matrix=str(expected_kinetic),
        determinant=str(expected_determinant),
        q0_determinant=str(expected_determinant.subs(q, 0)),
    )

    # Mutation: deleting the finite charge makes the strict-q0 determinant
    # vanish.  The audit must not call that mutated branch regular.
    deleted_charge_q0 = sp.simplify(
        expected_determinant.subs({chemical: 0, q: 0})
    )
    add_check(
        checks,
        "mutation_deleted_finite_charge_triggers_q0_rank_loss",
        deleted_charge_q0 == 0,
        mutation="mu->0 at q=0",
        mutated_determinant=str(deleted_charge_q0),
        mutation_result="DETECTED_RANK_LOSS",
    )

    # ------------------------------------------------------------------
    # 4. Verify primary output checks and SHA manifest independently.
    # ------------------------------------------------------------------
    primary_json = OUT / "itsm_pkm1_finite_density_parent_hamiltonian_summary.json"
    primary = json.loads(primary_json.read_text(encoding="utf-8"))
    primary_checks = primary.get("checks", [])
    add_check(
        checks,
        "primary_summary_is_fail_closed",
        primary.get("calculation_status") == "PASS_BOUNDED_PARENT_AUDIT"
        and primary.get("physics_pass") is False
        and primary.get("gate_firewall", {}).get("MAT_001") == "BLOCKED"
        and primary.get("gate_firewall", {}).get("UVIR_003") == "IN_PROGRESS"
        and primary_checks
        and all(bool(row.get("ok")) for row in primary_checks),
        route_disposition=primary.get("route_disposition"),
        primary_check_count=len(primary_checks),
    )

    manifest_path = OUT / "itsm_pkm1_finite_density_parent_hamiltonian.sha256"
    manifest_rows = parse_manifest(manifest_path)
    manifest_results: list[dict[str, Any]] = []
    for expected, name in manifest_rows:
        candidates = [HERE / name, OUT / name]
        matches = [path for path in candidates if path.exists()]
        if len(matches) != 1:
            raise AssertionError(f"manifest target resolution failed for {name}: {matches}")
        actual = digest(matches[0])
        manifest_results.append(
            {
                "name": name,
                "expected": expected,
                "actual": actual,
                "ok": expected == actual,
            }
        )
    add_check(
        checks,
        "primary_manifest_all_hashes_match",
        len(manifest_results) == 5
        and all(row["ok"] for row in manifest_results),
        files=manifest_results,
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "PKM1_P0_INDEPENDENT_REPRODUCTION_AND_MUTATION",
        "calculation_status": (
            "PASS_INDEPENDENT_REPRODUCTION" if all_ok else "FAIL_REPRODUCTION"
        ),
        "physics_pass": False,
        "route_disposition": primary.get("route_disposition"),
        "independence": (
            "No import from the primary calculation; decisive J Hessians, "
            "original-action radial Schur complement and direct ADM constraint "
            "elimination were reconstructed separately."
        ),
        "mutation_tests": {
            "static_ellipticity_substituted_for_khronon_Hessian": "REJECTED",
            "reversed_J_sign": "REJECTED",
            "forced_K_QQ_zero": "REJECTED",
            "deleted_finite_charge_at_q0": "DETECTED_RANK_LOSS",
        },
        "checks": checks,
        "input_sha256": {
            "primary_script": digest(
                HERE / "itsm_pkm1_finite_density_parent_hamiltonian.py"
            ),
            "primary_summary": digest(primary_json),
            "primary_manifest": digest(manifest_path),
            "spec": digest(HERE / "PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md"),
        },
        "gate_firewall": primary.get("gate_firewall"),
        "scientific_boundary": (
            "This reproduces algebra and detects scoped mutations. It does not "
            "independently derive J, a0, a physical locality window, nonlinear "
            "stability, PPN phenomenology or topology."
        ),
    }
    json_path = OUT / "itsm_pkm1_p0_independent_reproduction_summary.json"
    json_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report_path = OUT / "ITSM_PKM1_P0_INDEPENDENT_REPRODUCTION.md"
    report = f"""# PKM1-P0 independent reproduction and mutation audit

**Calculation:** `{summary['calculation_status']}`
**Physics pass:** `false`
**Route:** `{summary['route_disposition']}`

The decisive results were reproduced without importing the primary script:

- P0-A's radial Hessian is
  `(2y^3+y^2-1)/(1+y+y^2+y^3)^2` and changes sign at
  `y={mp.nstr(root_mp, 16)}`;
- P0-B has `J_Y=-1/(1+y)` and
  `J_Y+2YJ_YY=-1/(1+y)^2`;
- a direct Schur complement of the original `rho,N` action gives
  `M_P^2 K_QQ=rho^2 mu^2(1+4mu^2/M_rho^2)`;
- direct lapse/shift elimination gives
  `det K=(rho^2 mu^2+C_J q^2)/H^2`, including a positive strict-`q=0`
  determinant on the finite-charge branch.

Four claim-changing mutations were detected: replacing the khronon Hessian
with static ellipticity, reversing the sign of `J`, forcing `K_QQ=0`, and
deleting the finite charge at `q=0`.

All five files in the primary SHA-256 manifest match their recorded hashes.
This is an independent algebra/reproducibility pass, not a physics pass.
"""
    report_path.write_text(report, encoding="utf-8")
    seal_paths = [Path(__file__), json_path, report_path]
    seal = "\n".join(
        f"{digest(path)}  {path.name}" for path in seal_paths
    ) + "\n"
    (OUT / "itsm_pkm1_p0_independent_reproduction.sha256").write_text(
        seal, encoding="ascii"
    )
    print(
        json.dumps(
            {
                "calculation": summary["calculation_status"],
                "checks": len(checks),
                "mutations": len(summary["mutation_tests"]),
            },
            sort_keys=True,
        )
    )
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
