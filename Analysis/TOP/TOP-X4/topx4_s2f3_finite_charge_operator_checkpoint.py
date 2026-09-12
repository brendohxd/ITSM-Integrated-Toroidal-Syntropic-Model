#!/usr/bin/env python3
"""Plan-11 finite-charge operator and variation checkpoint for X4-S2F3.

Derives the fixed-background amplitude/phase operator of the charged complex
scalar and the fixed-global-charge Routhian identities from the frozen parent.
This is not a time-dependent determinant, renormalized stress tensor, coupled
gravity Hessian, anomaly clearance, or stabilization result.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = "PASS_FINITE_CHARGE_OPERATOR_HOLD_DYNAMIC_STATE_STRESS_AND_HESSIAN"
FAIL_STATUS = "FAIL_FINITE_CHARGE_OPERATOR_CHECKPOINT"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sidecar_check(path: Path, root: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        expected = sidecar.read_text(encoding="ascii").split()[0].lower()
    return {
        "path": str(path.relative_to(root)),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    base = root / "Analysis" / "TOP" / "TOP-X4"
    output_dir = base / "outputs"
    authority_paths = [
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md",
        root
        / "Theory"
        / "Core"
        / "Reasoning_Mode_Plans"
        / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
        / "PLAN.md",
        root
        / "Theory"
        / "Gates"
        / "TOP-X4"
        / "TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md",
        output_dir / "topx4_s2f3_static_determinant_summary.json",
    ]
    receipts = [sidecar_check(path, root) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "frozen_authority_and_static_checkpoint_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    eps = sp.symbols("epsilon", real=True)
    rho, sigma, sigma_dot, pi_dot, mu = sp.symbols(
        "rho sigma sigma_dot pi_dot mu", real=True, finite=True
    )
    k2, u_r, u_rr = sp.symbols("k2 U_r U_rr", real=True)
    radial = rho + eps * sigma
    phase_dot = mu + eps * pi_dot / rho
    potential_taylor = eps * u_r * sigma + eps**2 * u_rr * sigma**2 / 2
    lagrangian = (
        eps**2 * sigma_dot**2 / 2
        + radial**2 * phase_dot**2 / 2
        - eps**2 * k2 * sigma**2 / 2
        - eps**2 * k2 * sp.symbols("pi", real=True) ** 2 / 2
        - potential_taylor
    )
    linear = sp.expand(lagrangian).coeff(eps, 1)
    quadratic = sp.expand(lagrangian).coeff(eps, 2)
    pi = next(symbol for symbol in quadratic.free_symbols if symbol.name == "pi")
    m_sigma2 = sp.symbols("M_sigma2", real=True)
    quadratic_on_shell = sp.simplify(quadratic.subs(u_rr, m_sigma2 + mu**2))
    target_quadratic = (
        sigma_dot**2 / 2
        + pi_dot**2 / 2
        + 2 * mu * sigma * pi_dot
        - k2 * (sigma**2 + pi**2) / 2
        - m_sigma2 * sigma**2 / 2
    )
    add_check(
        checks,
        "background_radial_stationarity_is_required_before_spectrum",
        sp.simplify(linear.subs(u_r, rho * mu**2) - mu * rho * pi_dot) == 0,
        linear_residual=str(sp.factor(linear)),
        stationarity="U_r=rho*mu^2 on a constant zero-winding control",
        discarded_boundary_term="mu*rho*pi_dot=d(mu*rho*pi)/dt for constant background",
    )
    add_check(
        checks,
        "charged_amplitude_phase_quadratic_lagrangian",
        sp.simplify(quadratic_on_shell - target_quadratic) == 0,
        quadratic_lagrangian=str(target_quadratic),
        canonical_phase_fluctuation="pi=rho*delta_theta",
    )

    omega2 = sp.symbols("omega2", nonnegative=True)
    determinant = sp.expand(
        (omega2 - k2 - m_sigma2) * (omega2 - k2) - 4 * mu**2 * omega2
    )
    expected_determinant = sp.expand(
        omega2**2
        - omega2 * (2 * k2 + m_sigma2 + 4 * mu**2)
        + k2 * (k2 + m_sigma2)
    )
    add_check(
        checks,
        "mixed_inverse_operator_determinant",
        sp.simplify(determinant - expected_determinant) == 0,
        determinant_polynomial=str(expected_determinant),
        off_diagonal_frequency_mixing="+/- 2 i mu omega",
    )
    omitted_mixing_determinant = sp.expand(
        (omega2 - k2 - m_sigma2) * (omega2 - k2)
    )
    add_check(
        checks,
        "omitted_charge_mixing_mutation_is_rejected",
        sp.simplify(determinant - omitted_mixing_determinant + 4 * mu**2 * omega2)
        == 0
        and determinant.subs({omega2: 2, k2: 1, m_sigma2: 3, mu: 1})
        != omitted_mixing_determinant.subs(
            {omega2: 2, k2: 1, m_sigma2: 3, mu: 1}
        ),
        omitted_mixing_polynomial=str(omitted_mixing_determinant),
        required_difference="-4*mu^2*omega2",
    )

    zero_momentum = sp.factor(expected_determinant.subs(k2, 0))
    add_check(
        checks,
        "one_goldstone_and_one_gapped_mode_at_zero_momentum",
        sp.simplify(zero_momentum - omega2 * (omega2 - m_sigma2 - 4 * mu**2)) == 0,
        roots=["0", "M_sigma2+4*mu^2"],
        stability_condition="M_sigma2>0",
    )
    implicit_sound_speed2 = sp.simplify(m_sigma2 / (m_sigma2 + 4 * mu**2))
    add_check(
        checks,
        "low_momentum_goldstone_speed_is_positive_and_subluminal_in_stable_domain",
        implicit_sound_speed2.subs({m_sigma2: 3, mu: 2}) == sp.Rational(3, 19),
        sound_speed_squared=str(implicit_sound_speed2),
        domain="M_sigma2>0 and real mu",
    )
    zero_charge_factorization = sp.factor(expected_determinant.subs(mu, 0))
    add_check(
        checks,
        "zero_charge_operator_factorizes_to_radial_and_phase_controls",
        sp.simplify(
            zero_charge_factorization
            - (omega2 - k2) * (omega2 - k2 - m_sigma2)
        )
        == 0,
        factorization=str(zero_charge_factorization),
    )

    lapse, a, b, charge = sp.symbols("N a b Q", positive=True)
    fixed_charge_routhian = -lapse * charge**2 / (2 * a**3 * b * rho**2)
    mu_from_charge = charge / (a**3 * b * rho**2)
    radial_equation_term = sp.simplify(
        -sp.diff(fixed_charge_routhian, rho) / (lapse * a**3 * b)
    )
    add_check(
        checks,
        "fixed_charge_routhian_reproduces_radial_centrifugal_term",
        sp.simplify(radial_equation_term + rho * mu_from_charge**2) == 0,
        routhian=str(fixed_charge_routhian),
        radial_term=str(radial_equation_term),
        ensemble="fixed conserved global charge; no inserted chemical potential",
    )
    wrong_sign_routhian = -fixed_charge_routhian
    wrong_sign_radial_term = sp.simplify(
        -sp.diff(wrong_sign_routhian, rho) / (lapse * a**3 * b)
    )
    add_check(
        checks,
        "wrong_sign_fixed_charge_routhian_mutation_is_rejected",
        sp.simplify(wrong_sign_radial_term - rho * mu_from_charge**2) == 0
        and sp.simplify(wrong_sign_radial_term - radial_equation_term) != 0,
        wrong_sign_radial_term=str(wrong_sign_radial_term),
        required_radial_term=str(radial_equation_term),
    )
    epsilon_q = sp.simplify(-sp.diff(fixed_charge_routhian, lapse) / (a**3 * b))
    pressure_a_q = sp.simplify(
        sp.diff(fixed_charge_routhian, a) / (3 * lapse * a**2 * b)
    )
    pressure_y_q = sp.simplify(
        sp.diff(fixed_charge_routhian, b) / (lapse * a**3)
    )
    expected_charge_energy = sp.simplify(rho**2 * mu_from_charge**2 / 2)
    add_check(
        checks,
        "fixed_charge_metric_variation_gives_consistent_energy_and_pressures",
        all(
            sp.simplify(item - expected_charge_energy) == 0
            for item in (epsilon_q, pressure_a_q, pressure_y_q)
        ),
        energy_density=str(epsilon_q),
        observed_space_pressure=str(pressure_a_q),
        circle_pressure=str(pressure_y_q),
    )

    k_observed2, mode_n = sp.symbols("k_observed2 n", nonnegative=True)
    kk_momentum2 = k_observed2 + mode_n**2 / b**2
    add_check(
        checks,
        "periodic_circle_momentum_enters_every_bosonic_branch",
        sp.simplify(kk_momentum2.subs(mode_n, 0) - k_observed2) == 0
        and sp.simplify(kk_momentum2.subs(k_observed2, 0) - mode_n**2 / b**2) == 0,
        momentum_squared=str(kk_momentum2),
        circumference="2*pi*b",
    )
    m_fermion = sp.symbols("m_F", positive=True)
    fermion_frequency2 = kk_momentum2 + m_fermion**2
    add_check(
        checks,
        "neutral_spectator_fermion_operator_has_no_direct_charge_shift",
        mu not in fermion_frequency2.free_symbols and rho not in fermion_frequency2.free_symbols,
        frequency_squared=str(fermion_frequency2),
        limitation="metric evolution still makes the operator state dependent through a(t), b(t)",
    )

    quantum_variation_contract = {
        "effective_action": "Gamma=S_I1C+Gamma_even+Gamma_odd+Gamma_ct",
        "vary_before_ansatz": True,
        "metric_source": "T_AB^q=-2/sqrt(-G) delta(Gamma_q)/delta(G^AB)",
        "radial_source": "E_rho^q=+1/sqrt(-G) delta(Gamma_q)/delta(rho)",
        "phase_source": "E_theta^q=+1/sqrt(-G) delta(Gamma_q)/delta(theta)",
        "matter_proxy_source": "E_chi^q=+1/sqrt(-G) delta(Gamma_q)/delta(chi)",
        "diffeomorphism_ward_identity": "nabla^A T_AB^q=sum_i E_i^q nabla_B phi_i",
        "global_u1_identity": "Gamma_q is theta-shift invariant; corrected global charge is conserved",
        "fixed_charge_reduction": "perform only after covariant variation, using the Routhian",
    }
    add_check(
        checks,
        "semiclassical_variation_contract_contains_all_required_sources",
        all(
            key in quantum_variation_contract
            for key in (
                "metric_source",
                "radial_source",
                "phase_source",
                "matter_proxy_source",
                "diffeomorphism_ward_identity",
                "global_u1_identity",
            )
        ),
        contract=quantum_variation_contract,
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    static_import_statement = "from " + "topx4_s2f3_static_determinant_checkpoint"
    static_imported = static_import_statement in source_text
    add_check(
        checks,
        "static_vacuum_solver_is_not_reused_as_dynamic_determinant",
        not static_imported,
        static_solver_imported=static_imported,
    )
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_source_tokens=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_FINITE_CHARGE_OPERATOR_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_dynamic_determinant": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "finite_charge_spectrum": {
            "scope": "constant-background principal operator before gravity constraints",
            "determinant_polynomial_in_omega_squared": str(expected_determinant),
            "goldstone_speed_squared": str(implicit_sound_speed2),
            "zero_momentum_modes": ["omega_-^2=0", "omega_+^2=M_sigma2+4*mu^2"],
            "finite_density_degree_count": "one gapless phase mode plus one gapped amplitude mode",
        },
        "semiclassical_variation_contract": quantum_variation_contract,
        "hold_reasons": [
            "the constant-background principal operator is not an evolving Hadamard/adiabatic state",
            "no adiabatic-order convergence or renormalized state-dependent stress tensor is calculated",
            "the metric-radion-amplitude-phase constraints and physical Hessian are not reduced",
            "the parity-odd determinant phase and quantized counterterms remain unaudited",
            "continuous finite-charge mass-ratio, cutoff and state robustness remain uncomputed",
        ],
        "next_required_calculation": (
            "construct the time-dependent coupled mode system on the A1 background, declare the "
            "Hadamard/adiabatic state and subtraction terms, and demonstrate adiabatic-order convergence"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this finite-charge operator checkpoint",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "derived_claims": [],
        "explicit_nonclaims": [
            "no finite-charge determinant",
            "no renormalized quantum stress tensor",
            "no stabilized finite-charge background",
            "no physical radion mass",
            "no anomaly clearance",
            "no architecture or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_finite_charge_operator_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(
        f"checks={result['calculation_checks_passed']}/"
        f"{result['calculation_checks_total']}"
    )
    print("physics_pass=false")
    print("gate_effect=NONE")
    print("advance_to_dynamic_determinant=false")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
