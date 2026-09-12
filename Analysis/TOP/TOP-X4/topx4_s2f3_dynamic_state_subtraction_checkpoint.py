#!/usr/bin/env python3
"""Bounded dynamic scalar-state checkpoint for TOP-X4 candidate X4-S2F3.

Constructs the exact evolving charged-scalar mode system on the registered A1
background and tests finite-order scalar adiabatic UV diagnostics. It does not
compute a covariantly renormalized five-dimensional stress tensor, a Dirac
adiabatic state, the parity-odd determinant phase, or a physical Hessian.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

from topx4_a1_background_control import parameters, rhs, stress_components


STATUS = "PASS_DYNAMIC_SCALAR_ADIABATIC_UV_HOLD_FULL_STATE_STRESS_AND_HESSIAN"
FAIL_STATUS = "FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)
K_OBS_GRID = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
KK_GRID = (0, 1, 2, 4)
UV_K_MIN = 16.0
INTERIOR_FRACTION = 0.05


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


def initial_state(p: dict[str, float]) -> np.ndarray:
    provisional = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    energy, _, _ = stress_components(provisional, p)
    hubble = math.sqrt(energy / (6.0 * p["M5_cubed"]))
    provisional[7] = hubble
    provisional[8] = hubble
    return provisional


def integrate_background(points: int, p: dict[str, float]) -> Any:
    times = np.linspace(0.0, 1.0, points)
    return solve_ivp(
        fun=lambda time, state: rhs(time, state, p),
        t_span=(0.0, 1.0),
        y0=initial_state(p),
        method="DOP853",
        t_eval=times,
        rtol=1.0e-11,
        atol=1.0e-13,
    )


def background_fields(solution: Any, p: dict[str, float]) -> dict[str, np.ndarray]:
    states = solution.y.T
    derivatives = np.vstack(
        [rhs(float(time), state, p) for time, state in zip(solution.t, states)]
    )
    a = states[:, 0]
    b = states[:, 1]
    rho = states[:, 2]
    rho_dot = states[:, 3]
    chi = states[:, 4]
    mu = states[:, 6]
    h_a = states[:, 7]
    h_b = states[:, 8]
    rho_ddot = derivatives[:, 3]
    mu_dot = derivatives[:, 6]
    h_a_dot = derivatives[:, 7]
    h_b_dot = derivatives[:, 8]
    expansion = 3.0 * h_a + h_b
    gamma = 0.5 * expansion
    gamma_dot = 0.5 * (3.0 * h_a_dot + h_b_dot)
    h = rho_dot / rho
    h_dot = rho_ddot / rho - h * h
    u_rr = (
        p["m_phi_squared"]
        + 1.5 * p["lambda_phi5"] * rho * rho
        + 0.5 * p["g5"] * chi * chi
    )
    m_sigma2 = u_rr - mu * mu
    m_chi_eff2 = (
        p["m_chi_squared"]
        + 0.5 * p["lambda_chi5"] * chi * chi
        + 0.5 * p["g5"] * rho * rho
    )
    return {
        "a": a,
        "b": b,
        "rho": rho,
        "mu": mu,
        "mu_dot": mu_dot,
        "h": h,
        "h_dot": h_dot,
        "gamma": gamma,
        "gamma_dot": gamma_dot,
        "m_sigma2": m_sigma2,
        "m_chi_eff2": m_chi_eff2,
        "charge": a**3 * b * rho**2 * mu,
    }


def wkb_iterate(
    times: np.ndarray, omega: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    spline0 = CubicSpline(times, omega)
    omega_dot = spline0(times, 1)
    omega_ddot = spline0(times, 2)
    w2_squared = omega * omega - 0.5 * omega_ddot / omega + 0.75 * (omega_dot / omega) ** 2
    details: dict[str, Any] = {
        "min_W2_squared": float(np.min(w2_squared)),
        "min_W2_squared_time": float(times[int(np.argmin(w2_squared))]),
    }
    if np.min(w2_squared) <= 0.0:
        details["failed_stage"] = "W2"
        return np.full_like(omega, np.nan), np.full_like(omega, np.nan), details
    w2 = np.sqrt(w2_squared)
    spline2 = CubicSpline(times, w2)
    w2_dot = spline2(times, 1)
    w2_ddot = spline2(times, 2)
    w4_squared = omega * omega - 0.5 * w2_ddot / w2 + 0.75 * (w2_dot / w2) ** 2
    details["min_W4_squared"] = float(np.min(w4_squared))
    details["min_W4_squared_time"] = float(times[int(np.argmin(w4_squared))])
    if np.min(w4_squared) <= 0.0:
        details["failed_stage"] = "W4"
        return w2, np.full_like(omega, np.nan), details
    details["failed_stage"] = None
    return w2, np.sqrt(w4_squared), details


def branch_frequencies(fields: dict[str, np.ndarray], k_obs: float, n_kk: int) -> dict[str, np.ndarray]:
    k2 = k_obs * k_obs / fields["a"] ** 2 + n_kk * n_kk / fields["b"] ** 2
    mu = fields["mu"]
    m2 = fields["m_sigma2"]
    coefficient = m2 + 4.0 * mu * mu
    discriminant = coefficient * coefficient + 16.0 * mu * mu * k2
    root = np.sqrt(discriminant)
    omega_minus2 = 0.5 * (2.0 * k2 + coefficient - root)
    omega_plus2 = 0.5 * (2.0 * k2 + coefficient + root)
    omega_chi2 = k2 + fields["m_chi_eff2"] - fields["gamma_dot"] - fields["gamma"] ** 2
    return {
        "charged_minus": np.sqrt(omega_minus2),
        "charged_plus": np.sqrt(omega_plus2),
        "chi": np.sqrt(omega_chi2),
    }


def mode_diagnostics(solution: Any, p: dict[str, float]) -> dict[str, Any]:
    fields = background_fields(solution, p)
    cut = max(2, int(INTERIOR_FRACTION * solution.t.size))
    interior = slice(cut, -cut)
    modes: list[dict[str, Any]] = []
    all_positive = True
    scalar_w_positive = True
    wronskian_residuals: list[float] = []
    for k_obs in K_OBS_GRID:
        for n_kk in KK_GRID:
            frequencies = branch_frequencies(fields, k_obs, n_kk)
            branch_results: dict[str, Any] = {}
            for branch, omega in frequencies.items():
                w2, w4, iteration_details = wkb_iterate(solution.t, omega)
                positive = bool(
                    np.all(np.isfinite(omega))
                    and np.min(omega) > 0.0
                    and np.all(np.isfinite(w2))
                    and np.min(w2) > 0.0
                    and np.all(np.isfinite(w4))
                    and np.min(w4) > 0.0
                )
                all_positive = all_positive and bool(np.min(omega) > 0.0)
                scalar_w_positive = scalar_w_positive and positive
                if positive:
                    rel20 = np.abs(w2[interior] - omega[interior]) / omega[interior]
                    rel42 = np.abs(w4[interior] - w2[interior]) / w2[interior]
                    w4_spline = CubicSpline(solution.t, w4)
                    w = float(w4[0])
                    w_dot = float(w4_spline(solution.t[0], 1))
                    u = complex(1.0 / math.sqrt(2.0 * w), 0.0)
                    u_dot = complex(-w_dot / (2.0 * w), -w) * u
                    wronskian = u * u_dot.conjugate() - u.conjugate() * u_dot
                    wronskian_residual = abs(wronskian - 1j)
                    wronskian_residuals.append(float(wronskian_residual))
                    branch_results[branch] = {
                        "positive": True,
                        "min_omega": float(np.min(omega)),
                        "min_W2": float(np.min(w2)),
                        "min_W4": float(np.min(w4)),
                        "max_relative_W2_minus_W0_interior": float(np.max(rel20)),
                        "max_relative_W4_minus_W2_interior": float(np.max(rel42)),
                        "wronskian_residual_at_t0": float(wronskian_residual),
                        "iteration_extrema": iteration_details,
                    }
                else:
                    branch_results[branch] = {
                        "positive": False,
                        "min_omega": float(np.nanmin(omega)),
                        "iteration_extrema": iteration_details,
                    }
            modes.append(
                {
                    "k_obs": k_obs,
                    "n": n_kk,
                    "uv_subset": k_obs >= UV_K_MIN,
                    "branches": branch_results,
                }
            )
    uv_entries = [mode for mode in modes if mode["uv_subset"]]
    uv_rel20 = [
        branch["max_relative_W2_minus_W0_interior"]
        for mode in uv_entries
        for branch in mode["branches"].values()
        if branch["positive"]
    ]
    uv_rel42 = [
        branch["max_relative_W4_minus_W2_interior"]
        for mode in uv_entries
        for branch in mode["branches"].values()
        if branch["positive"]
    ]
    uv_hierarchy = all(
        branch["max_relative_W4_minus_W2_interior"]
        < branch["max_relative_W2_minus_W0_interior"]
        for mode in uv_entries
        for branch in mode["branches"].values()
        if branch["positive"]
    )
    return {
        "points": int(solution.t.size),
        "solver_success": bool(solution.success),
        "finite_positive_background": bool(
            np.all(np.isfinite(solution.y))
            and np.min(fields["a"]) > 0.0
            and np.min(fields["b"]) > 0.0
            and np.min(fields["rho"]) > 0.0
        ),
        "max_charge_relative_error": float(
            np.max(np.abs(fields["charge"] / fields["charge"][0] - 1.0))
        ),
        "all_scalar_frequencies_positive": all_positive,
        "all_iterated_scalar_frequencies_positive": scalar_w_positive,
        "max_wronskian_residual": max(wronskian_residuals, default=float("inf")),
        "uv_hierarchy_all_modes": uv_hierarchy,
        "uv_max_relative_W2_minus_W0": max(uv_rel20, default=float("inf")),
        "uv_max_relative_W4_minus_W2": max(uv_rel42, default=float("inf")),
        "modes": modes,
    }


def symbolic_checks() -> dict[str, Any]:
    vs, vp, vs_dot, vp_dot = sp.symbols("v_s v_p v_s_dot v_p_dot", real=True)
    gamma, gamma_dot, h, h_dot, mu, mu_dot = sp.symbols(
        "gamma gamma_dot h h_dot mu mu_dot", real=True
    )
    k2, m2 = sp.symbols("k2 M_sigma2", real=True)
    transformed = (
        ((vs_dot - gamma * vs) ** 2 + (vp_dot - gamma * vp) ** 2) / 2
        - h * vp * (vp_dot - gamma * vp)
        + h**2 * vp**2 / 2
        + 2 * mu * vs * (vp_dot - gamma * vp)
        - (k2 + m2) * vs**2 / 2
        - k2 * vp**2 / 2
    )
    k_ss = k2 + m2 - gamma**2 - gamma_dot
    k_pp = k2 - gamma**2 - gamma_dot - 2 * h * gamma - h**2 - h_dot
    k_sp = mu_dot + 2 * mu * gamma
    canonical = (
        (vs_dot**2 + vp_dot**2) / 2
        + mu * (vs * vp_dot - vp * vs_dot)
        - (k_ss * vs**2 + 2 * k_sp * vs * vp + k_pp * vp**2) / 2
    )
    total_derivative = (
        -gamma_dot * (vs**2 + vp**2) / 2
        - gamma * (vs * vs_dot + vp * vp_dot)
        - h_dot * vp**2 / 2
        - h * vp * vp_dot
        + mu_dot * vs * vp
        + mu * (vs_dot * vp + vs * vp_dot)
    )
    transform_residual = sp.simplify(sp.expand(transformed - canonical - total_derivative))

    omega2 = sp.symbols("omega2", nonnegative=True)
    static_determinant = sp.expand((omega2 - k2 - m2) * (omega2 - k2) - 4 * mu**2 * omega2)
    expected = sp.expand(omega2**2 - omega2 * (2 * k2 + m2 + 4 * mu**2) + k2 * (k2 + m2))
    omitted = sp.expand((omega2 - k2 - m2) * (omega2 - k2))
    charge_law = -(2 * gamma + 2 * h) * mu
    k_sp_on_charge = sp.simplify(k_sp.subs(mu_dot, charge_law))
    wrong_charge_law = -(2 * gamma + h) * mu
    wrong_k_sp = sp.simplify(k_sp.subs(mu_dot, wrong_charge_law))
    return {
        "canonical_transform_exact": transform_residual == 0,
        "canonical_transform_residual": str(transform_residual),
        "constant_background_determinant_exact": sp.simplify(static_determinant - expected) == 0,
        "determinant": str(expected),
        "charge_reduced_K_sp_exact": sp.simplify(k_sp_on_charge + 2 * mu * h) == 0,
        "charge_reduced_K_sp": str(k_sp_on_charge),
        "omitted_mixing_rejected": sp.simplify(static_determinant - omitted) != 0,
        "wrong_charge_law_rejected": sp.simplify(wrong_k_sp + 2 * mu * h) != 0,
        "wrong_charge_K_sp": str(wrong_k_sp),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    base = root / "Analysis" / "TOP" / "TOP-X4"
    output_dir = base / "outputs"
    authority_paths = [
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_DYNAMIC_STATE_SUBTRACTION_CONTRACT_2026-09-12.md",
        base / "TOPX4_S2F3_PLAN11_FINITE_CHARGE_OPERATOR_CHECKPOINT_2026-09-12.md",
        output_dir / "topx4_a1_background_summary.json",
        output_dir / "topx4_s2f3_finite_charge_operator_summary.json",
    ]
    receipts = [sidecar_check(path, root) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(checks, "frozen_authority_sidecars_match", all(item["matches"] for item in receipts), receipts=receipts)

    symbolic = symbolic_checks()
    add_check(
        checks,
        "canonical_volume_rescaling_is_exact_up_to_declared_boundary_term",
        symbolic["canonical_transform_exact"],
        residual=symbolic["canonical_transform_residual"],
    )
    add_check(
        checks,
        "canonical_equation_and_charge_reduction_are_exact",
        symbolic["charge_reduced_K_sp_exact"],
        equation="v_ddot+2*mu*J*v_dot+(K+mu_dot*J)*v=0",
        K_sp_after_charge_law=symbolic["charge_reduced_K_sp"],
    )
    add_check(
        checks,
        "constant_background_determinant_regression",
        symbolic["constant_background_determinant_exact"],
        determinant=symbolic["determinant"],
    )
    add_check(
        checks,
        "mixing_and_charge_law_mutations_are_rejected",
        symbolic["omitted_mixing_rejected"] and symbolic["wrong_charge_law_rejected"],
        wrong_charge_K_sp=symbolic["wrong_charge_K_sp"],
    )

    p = parameters()
    primary = mode_diagnostics(integrate_background(1601, p), p)
    witness = mode_diagnostics(integrate_background(801, p), p)
    add_check(
        checks,
        "registered_background_integrations_complete_and_conserve_charge",
        primary["solver_success"]
        and witness["solver_success"]
        and primary["finite_positive_background"]
        and witness["finite_positive_background"]
        and primary["max_charge_relative_error"] < 1.0e-9
        and witness["max_charge_relative_error"] < 1.0e-9,
        primary_max_charge_relative_error=primary["max_charge_relative_error"],
        witness_max_charge_relative_error=witness["max_charge_relative_error"],
        threshold=1.0e-9,
    )
    add_check(
        checks,
        "registered_scalar_frequencies_and_WKB_iterates_are_positive",
        primary["all_scalar_frequencies_positive"]
        and primary["all_iterated_scalar_frequencies_positive"]
        and witness["all_scalar_frequencies_positive"]
        and witness["all_iterated_scalar_frequencies_positive"],
    )
    add_check(
        checks,
        "preregistered_UV_adiabatic_order_hierarchy",
        primary["uv_hierarchy_all_modes"] and witness["uv_hierarchy_all_modes"],
        condition="max|W4-W2|/W2 < max|W2-W0|/W0 for every k_obs>=16 scalar branch",
    )
    add_check(
        checks,
        "UV_fourth_order_correction_below_registered_bound",
        primary["uv_max_relative_W4_minus_W2"] < 1.0e-3,
        measured=primary["uv_max_relative_W4_minus_W2"],
        threshold=1.0e-3,
    )
    resolution_difference = max(
        abs(primary["uv_max_relative_W2_minus_W0"] - witness["uv_max_relative_W2_minus_W0"]),
        abs(primary["uv_max_relative_W4_minus_W2"] - witness["uv_max_relative_W4_minus_W2"]),
    )
    add_check(
        checks,
        "primary_witness_UV_envelopes_agree",
        resolution_difference < 2.0e-4,
        maximum_absolute_difference=resolution_difference,
        threshold=2.0e-4,
    )
    add_check(
        checks,
        "candidate_scalar_data_have_canonical_Wronskian",
        primary["max_wronskian_residual"] < 1.0e-12,
        maximum_absolute_residual=primary["max_wronskian_residual"],
        threshold=1.0e-12,
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    static_import = ("from " + "topx4_s2f3_static_determinant_checkpoint") in source_text
    add_check(
        checks,
        "dynamic_static_and_observational_firewalls",
        not forbidden_hits and not static_import,
        forbidden_source_tokens=forbidden_hits,
        static_solver_imported=static_import,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_DYNAMIC_STATE_SUBTRACTION_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_renormalized_stress": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "registered_grid": {
            "time_interval": [0.0, 1.0],
            "primary_points": 1601,
            "witness_points": 801,
            "k_obs": list(K_OBS_GRID),
            "n": list(KK_GRID),
            "UV_subset": "k_obs>=16",
            "interior_fraction_excluded_at_each_endpoint": INTERIOR_FRACTION,
        },
        "exact_mode_system": {
            "unscaled_lagrangian": "1/2 sigma_dot^2+1/2(pi_dot-h*pi)^2+2mu*sigma(pi_dot-h*pi)-1/2 k_n^2(sigma^2+pi^2)-1/2 M_sigma^2 sigma^2",
            "canonical_equation": "v_ddot+2*mu*J*v_dot+(K+mu_dot*J)*v=0",
            "J": [[0, -1], [1, 0]],
            "K_ss": "k_n^2+M_sigma^2-gamma^2-gamma_dot",
            "K_pp": "k_n^2-gamma^2-gamma_dot-2h*gamma-h^2-h_dot",
            "K_sp": "mu_dot+2mu*gamma=-2mu*h",
        },
        "state_declaration": {
            "claimed_scope": "finite-order scalar branchwise UV candidate data only",
            "target_for_future_full_state": "infinite-order adiabatic/Hadamard coupled scalar-spinor state",
            "orders_tested": [0, 2, 4],
            "candidate_data": "u=1/sqrt(2W); u_dot=(-iW-W_dot/(2W))*u",
            "coupled_eigenvector_transport": "NOT_CONSTRUCTED",
            "dirac_spinor_state": "NOT_CONSTRUCTED",
            "full_Hadamard_claim": False,
        },
        "subtraction_declaration": {
            "scalar_branchwise_ingredients": [
                "|u|^2_ad=1/(2W)",
                "|u_dot|^2_ad=W/2+W_dot^2/(8W^3)",
            ],
            "orders": [0, 2, 4],
            "decompactified_reference": "Delta_KK[F]=sum_n F(n/b)-b*integral dp_y F(p_y)",
            "covariant_5D_stress_subtraction": "NOT_DERIVED",
            "counterterm_map": "NOT_DERIVED",
            "stress_integral_or_KK_sum_performed": False,
        },
        "symbolic_checks": symbolic,
        "primary_diagnostics": primary,
        "resolution_witness": witness,
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "hold_reasons": [
            "finite fourth-order scalar branch data are not a proved Hadamard state for the coupled five-dimensional system",
            "charged-branch eigenvector transport and coupled normalization are not constructed",
            "neutral Dirac spinor adiabatic states and the parity-odd determinant phase remain unaudited",
            "the covariant five-dimensional stress subtraction and counterterm map are not derived",
            "no renormalized stress, semiclassical background solution, or physical constrained Hessian is computed",
        ],
        "next_required_calculation": (
            "construct normalized coupled charged-scalar transport and the neutral Dirac adiabatic state, "
            "then derive the covariant five-dimensional subtraction/counterterm map before any stress integral"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this dynamic scalar-state checkpoint",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "derived_claims": [],
        "explicit_nonclaims": [
            "no full Hadamard state",
            "no Dirac adiabatic state",
            "no renormalized quantum stress tensor",
            "no stabilized finite-charge background",
            "no physical radion mass or Hessian",
            "no parity or anomaly clearance",
            "no architecture, A4, Ultra, or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_dynamic_state_subtraction_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"checks={result['calculation_checks_passed']}/{result['calculation_checks_total']}")
    print(f"uv_max_W2_minus_W0={primary['uv_max_relative_W2_minus_W0']:.17g}")
    print(f"uv_max_W4_minus_W2={primary['uv_max_relative_W4_minus_W2']:.17g}")
    print(f"resolution_difference={resolution_difference:.17g}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print("advance_to_renormalized_stress=false")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
