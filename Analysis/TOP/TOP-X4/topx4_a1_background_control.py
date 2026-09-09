#!/usr/bin/env python3
"""TOP-X4 A1 finite-charge on-shell background control.

Integrates a preregistered dimensionless background of the frozen X4-I1C
five-dimensional Einstein + complex scalar + bulk real-scalar proxy action.
This is an action/background consistency test, not a perturbative, radion,
matter-universality, source-current, screening or phenomenology pass.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp


PASS_STATUS = "PASS_TOPX4_A1_CONTROL_BACKGROUND_ONLY"
FAIL_STATUS = "FAIL_TOPX4_A1_CONTROL_BACKGROUND"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_a0",
    "target" + "_a0",
    "H" + "0_target",
    "S" + "PARC_target",
    "desired" + "_Q",
)


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--t-final", type=float, default=1.0)
    return parser.parse_args()


def parameters() -> dict[str, float]:
    """Registered dimensionless control parameters, not observational fits."""
    return {
        "M5_cubed": 1.0,
        "U0": 0.0,
        "m_phi_squared": 1.0,
        "lambda_phi5": 1.0,
        "m_chi_squared": 1.0,
        "lambda_chi5": 1.0,
        "g5": 0.1,
        "winding_integer": 0.0,
    }


def stress_components(state: np.ndarray, p: dict[str, float]) -> tuple[float, float, float]:
    a, b, rho, rho_dot, chi, chi_dot, mu, _, _ = state
    del a
    s = 0.5 * rho * rho
    u_phi = p["U0"] + p["m_phi_squared"] * s + 0.5 * p["lambda_phi5"] * s * s
    w_chi = 0.5 * p["m_chi_squared"] * chi * chi + p["lambda_chi5"] * chi**4 / 24.0
    interaction = 0.25 * p["g5"] * rho * rho * chi * chi
    kinetic_time = 0.5 * (rho_dot * rho_dot + rho * rho * mu * mu + chi_dot * chi_dot)
    kinetic_winding = 0.5 * rho * rho * p["winding_integer"] ** 2 / (b * b)
    potential = u_phi + w_chi + interaction
    energy = kinetic_time + kinetic_winding + potential
    pressure_a = kinetic_time - kinetic_winding - potential
    pressure_y = kinetic_time + kinetic_winding - potential
    return energy, pressure_a, pressure_y


def rhs(_: float, state: np.ndarray, p: dict[str, float]) -> np.ndarray:
    a, b, rho, rho_dot, chi, chi_dot, mu, h_a, h_b = state
    if a <= 0.0 or b <= 0.0 or rho <= 0.0:
        raise FloatingPointError("positive scale factors and rho are required")

    _, pressure_a, pressure_y = stress_components(state, p)
    expansion = 3.0 * h_a + h_b
    winding_term = p["winding_integer"] ** 2 / (b * b)

    rho_ddot = -(
        expansion * rho_dot
        - rho * mu * mu
        + winding_term * rho
        + p["m_phi_squared"] * rho
        + 0.5 * p["lambda_phi5"] * rho**3
        + 0.5 * p["g5"] * rho * chi * chi
    )
    chi_ddot = -(
        expansion * chi_dot
        + p["m_chi_squared"] * chi
        + p["lambda_chi5"] * chi**3 / 6.0
        + 0.5 * p["g5"] * rho * rho * chi
    )
    mu_dot = -(expansion + 2.0 * rho_dot / rho) * mu

    h_a_dot = -2.0 * h_a * h_a - pressure_y / (3.0 * p["M5_cubed"])
    h_b_dot = (
        -2.0 * h_a_dot
        - 3.0 * h_a * h_a
        - 2.0 * h_a * h_b
        - h_b * h_b
        - pressure_a / p["M5_cubed"]
    )

    return np.array(
        [a * h_a, b * h_b, rho_dot, rho_ddot, chi_dot, chi_ddot, mu_dot, h_a_dot, h_b_dot],
        dtype=float,
    )


def continuity_residual(state: np.ndarray, state_dot: np.ndarray, p: dict[str, float]) -> float:
    _, b, rho, rho_dot, chi, chi_dot, mu, h_a, h_b = state
    _, b_dot, _, rho_ddot, _, chi_ddot, mu_dot, _, _ = state_dot
    energy, pressure_a, pressure_y = stress_components(state, p)

    energy_dot = (
        rho_dot * rho_ddot
        + rho * rho_dot * mu * mu
        + rho * rho * mu * mu_dot
        + chi_dot * chi_ddot
        + p["m_phi_squared"] * rho * rho_dot
        + 0.5 * p["lambda_phi5"] * rho**3 * rho_dot
        + p["m_chi_squared"] * chi * chi_dot
        + p["lambda_chi5"] * chi**3 * chi_dot / 6.0
        + 0.5 * p["g5"] * rho * rho_dot * chi * chi
        + 0.5 * p["g5"] * rho * rho * chi * chi_dot
        + rho * rho_dot * p["winding_integer"] ** 2 / (b * b)
        - rho * rho * p["winding_integer"] ** 2 * b_dot / (b**3)
    )
    return energy_dot + 3.0 * h_a * (energy + pressure_a) + h_b * (energy + pressure_y)


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    args = parse_args()
    if not math.isfinite(args.t_final) or args.t_final <= 0.0:
        raise ValueError("t-final must be finite and positive")

    p = parameters()
    # Registered dimensionless initial state. chi=0 is on shell by the Z2
    # symmetry. h_a=h_b is used only at t=0 to solve the Hamiltonian constraint.
    provisional = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], dtype=float)
    initial_energy, _, _ = stress_components(provisional, p)
    initial_hubble = math.sqrt(initial_energy / (6.0 * p["M5_cubed"]))
    y0 = provisional.copy()
    y0[7] = initial_hubble
    y0[8] = initial_hubble

    sample_times = np.linspace(0.0, args.t_final, 401)
    solution = solve_ivp(
        fun=lambda time, state: rhs(time, state, p),
        t_span=(0.0, args.t_final),
        y0=y0,
        method="DOP853",
        t_eval=sample_times,
        rtol=1.0e-11,
        atol=1.0e-13,
    )

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "solver_completed_registered_interval",
        bool(solution.success and solution.t.size == sample_times.size),
        solver_message=solution.message,
        points=int(solution.t.size),
        t_final_reached=float(solution.t[-1]),
    )

    finite = bool(np.all(np.isfinite(solution.y)))
    positive_domain = bool(
        np.min(solution.y[0]) > 0.0
        and np.min(solution.y[1]) > 0.0
        and np.min(solution.y[2]) > 0.0
    )
    add_check(
        checks,
        "finite_positive_background_domain",
        finite and positive_domain,
        min_a=float(np.min(solution.y[0])),
        min_b=float(np.min(solution.y[1])),
        min_rho=float(np.min(solution.y[2])),
    )

    constraint_residuals: list[float] = []
    continuity_residuals: list[float] = []
    charges: list[float] = []
    for column in range(solution.t.size):
        state = solution.y[:, column]
        state_dot = rhs(float(solution.t[column]), state, p)
        energy, _, _ = stress_components(state, p)
        hamiltonian = 3.0 * state[7] * (state[7] + state[8]) - energy / p["M5_cubed"]
        constraint_residuals.append(abs(float(hamiltonian)))
        continuity_residuals.append(abs(float(continuity_residual(state, state_dot, p))))
        charges.append(float(state[0] ** 3 * state[1] * state[2] ** 2 * state[6]))

    max_constraint = max(constraint_residuals)
    max_continuity = max(continuity_residuals)
    initial_charge = charges[0]
    max_charge_relative_error = max(abs(charge / initial_charge - 1.0) for charge in charges)
    add_check(
        checks,
        "hamiltonian_constraint_propagated",
        max_constraint < 1.0e-8,
        max_absolute_residual=max_constraint,
        threshold=1.0e-8,
    )
    add_check(
        checks,
        "global_u1_charge_conserved",
        max_charge_relative_error < 1.0e-9,
        initial_charge=initial_charge,
        final_charge=charges[-1],
        max_relative_error=max_charge_relative_error,
        threshold=1.0e-9,
    )
    add_check(
        checks,
        "analytic_stress_continuity",
        max_continuity < 1.0e-10,
        max_absolute_residual=max_continuity,
        threshold=1.0e-10,
    )

    zero_portal = dict(p)
    zero_portal["g5"] = 0.0
    add_check(
        checks,
        "literal_nested_zero_portal_limit",
        zero_portal["g5"] == 0.0 and all(zero_portal[key] == p[key] for key in p if key != "g5"),
        changed_parameter="g5",
        zero_value=zero_portal["g5"],
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    state_names = ["a", "b", "rho", "rho_dot", "chi", "chi_dot", "mu", "H_a", "H_b"]
    result = {
        "schema": "ITSM_TOPX4_A1_v1",
        "route": "TOP-X4_KK-001",
        "parent": "X4-I1C_bulk_scalar_control",
        "status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "canonical_t3_replaced": False,
        "units": "dimensionless control units with M5^3=m_phi^2=lambda_phi5=1",
        "parameters": p,
        "initial_state": dict(zip(state_names, (float(value) for value in y0))),
        "final_state": dict(zip(state_names, (float(value) for value in solution.y[:, -1]))),
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "derived_claims": [],
        "explicit_nonclaims": [
            "no perturbative health result",
            "no radion stabilization",
            "no Standard Model or equivalence-principle matter result",
            "no derived nonzero Q^mu",
            "no K_Q or V",
            "no screening or observational prediction",
        ],
        "next_entry_condition": "independent equation audit, then Max fixed-action KK/radion reduction",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "topx4_a1_background_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = sha256_bytes(payload)
    sidecar_path = output_path.with_suffix(output_path.suffix + ".sha256")
    sidecar_path.write_text(f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n")

    print(result["status"])
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print(f"max_constraint_residual={max_constraint:.17g}")
    print(f"max_charge_relative_error={max_charge_relative_error:.17g}")
    print(f"max_continuity_residual={max_continuity:.17g}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
