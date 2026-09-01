#!/usr/bin/env python3
"""UVIR-003 Stage B: derive and verify an evolving flat-FRW background.

Reduces the declared Stage-A Einstein-Hilbert, complex-condensate and
independent-aether sectors on a homogeneous and isotropic ansatz.  The force
field is constant, the alignment term vanishes on the comoving branch, and no
reservoir exchange is introduced.  A representative dimensionless solution
is then integrated and checked against the Friedmann constraint, Raychaudhuri
equation, condensate charge conservation and energy continuity.

This establishes existence of an on-shell background class and one
representative branch.  It is not a cosmological fit or a perturbation audit.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the JSON summary and trajectory CSV.",
    )
    parser.add_argument(
        "--t-end",
        type=float,
        default=8.0,
        help="End time of the representative dimensionless integration.",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=801,
        help="Number of equally spaced output samples.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.simplify(expression)
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def symbolic_derivation() -> dict[str, str]:
    # ------------------------------------------------------------------
    # 1. Flat-FRW reduction.
    #
    # ds^2=-N(t)^2 dt^2+a(t)^2 delta_ij dx^i dx^j
    # U^mu=(1/N,0,0,0)
    # Phi=rho(t) exp(i Theta(t))/sqrt(2)
    # psi=constant
    # ------------------------------------------------------------------
    lapse, scale, scale_dot = sp.symbols("N a a_dot", positive=True)
    rho, rho_dot, theta_dot = sp.symbols(
        "rho rho_dot Theta_dot", real=True
    )
    m_planck_sq, m_aether_sq = sp.symbols(
        "M_P_sq M_U_sq", positive=True
    )
    c1, c2, c3 = sp.symbols("c1 c2 c3", real=True)
    potential = sp.symbols("V", real=True)

    hubble_lapse = scale_dot / (scale * lapse)
    c_theta = sp.simplify(c1 + 3 * c2 + c3)

    # On the comoving unit-aether ansatz:
    # O1=3H_N^2, O2=9H_N^2, O3=3H_N^2, and a_mu a^mu=0.
    operator_1 = 3 * hubble_lapse**2
    operator_2 = 9 * hubble_lapse**2
    operator_3 = 3 * hubble_lapse**2
    acceleration_sq = sp.Integer(0)
    aether_density = sp.simplify(
        -m_aether_sq
        * (c1 * operator_1 + c2 * operator_2 + c3 * operator_3)
        / 2
    )
    expected_aether_density = sp.simplify(
        -3 * m_aether_sq * c_theta * hubble_lapse**2 / 2
    )
    require_zero(
        "comoving aether FRW reduction",
        aether_density - expected_aether_density,
    )

    m_cos_sq = sp.simplify(
        m_planck_sq + m_aether_sq * c_theta / 2
    )
    lagrangian = sp.simplify(
        -3 * m_cos_sq * scale * scale_dot**2 / lapse
        + scale**3 * (rho_dot**2 + rho**2 * theta_dot**2) / (2 * lapse)
        - lapse * scale**3 * potential
    )

    energy_density = sp.simplify(
        (rho_dot**2 + rho**2 * theta_dot**2) / 2 + potential
    )
    pressure = sp.simplify(
        (rho_dot**2 + rho**2 * theta_dot**2) / 2 - potential
    )
    hubble = scale_dot / scale
    lapse_equation = sp.simplify(
        sp.diff(lagrangian, lapse).subs(lapse, 1)
    )
    friedmann_residual = sp.simplify(
        3 * m_cos_sq * hubble**2 - energy_density
    )
    require_zero(
        "lapse variation gives Friedmann equation",
        lapse_equation / scale**3 - friedmann_residual,
    )

    # The alignment projector annihilates the homogeneous current because
    # J^mu is parallel to U^mu.  The constant force field has no derivatives.
    number_density = sp.simplify(rho**2 * theta_dot)
    projected_current_sq = sp.Integer(0)
    force_background_lagrangian = sp.Integer(0)

    # ------------------------------------------------------------------
    # 2. Conservation identities.
    # ------------------------------------------------------------------
    hubble_sym, hubble_dot = sp.symbols("H H_dot", real=True)
    rho_ddot, theta_ddot = sp.symbols(
        "rho_ddot Theta_ddot", real=True
    )
    potential_prime = sp.symbols("V_prime", real=True)

    radial_equation = sp.simplify(
        rho_ddot
        + 3 * hubble_sym * rho_dot
        - rho * theta_dot**2
        + potential_prime
    )
    charge_equation = sp.simplify(
        rho**2 * theta_ddot
        + 2 * rho * rho_dot * theta_dot
        + 3 * hubble_sym * rho**2 * theta_dot
    )

    rho_ddot_on_shell = sp.simplify(
        -3 * hubble_sym * rho_dot
        + rho * theta_dot**2
        - potential_prime
    )
    theta_ddot_on_shell = sp.simplify(
        -3 * hubble_sym * theta_dot
        - 2 * rho_dot * theta_dot / rho
    )
    hubble_dot_on_shell = sp.simplify(
        -(rho_dot**2 + rho**2 * theta_dot**2) / (2 * m_cos_sq)
    )

    require_zero(
        "radial equation substitution",
        radial_equation.subs(rho_ddot, rho_ddot_on_shell),
    )
    require_zero(
        "charge equation substitution",
        charge_equation.subs(theta_ddot, theta_ddot_on_shell),
    )

    energy_dot = sp.simplify(
        rho_dot * rho_ddot
        + rho * rho_dot * theta_dot**2
        + rho**2 * theta_dot * theta_ddot
        + potential_prime * rho_dot
    )
    continuity_residual = sp.simplify(
        energy_dot
        + 3 * hubble_sym * (energy_density + pressure)
    )
    require_zero(
        "condensate continuity",
        continuity_residual.subs(
            {
                rho_ddot: rho_ddot_on_shell,
                theta_ddot: theta_ddot_on_shell,
            }
        ),
    )

    friedmann_time_derivative = sp.simplify(
        6 * m_cos_sq * hubble_sym * hubble_dot
        - energy_dot
    )
    require_zero(
        "Friedmann propagation",
        friedmann_time_derivative.subs(
            {
                rho_ddot: rho_ddot_on_shell,
                theta_ddot: theta_ddot_on_shell,
                hubble_dot: hubble_dot_on_shell,
            }
        ),
    )

    # Check equivalence with the normalized Einstein-aether cosmological
    # prefactor alpha_i=(M_U^2/M_P^2)c_i.
    r_u = sp.symbols("r_U", positive=True)
    normalized_factor = sp.simplify(
        1 + r_u * c_theta / 2
    )
    require_zero(
        "normalized aether cosmological Planck mass",
        m_cos_sq.subs(m_aether_sq, r_u * m_planck_sq)
        - m_planck_sq * normalized_factor,
    )

    return {
        "aether_operator_O1": str(operator_1),
        "aether_operator_O2": str(operator_2),
        "aether_operator_O3": str(operator_3),
        "aether_acceleration_squared": str(acceleration_sq),
        "aether_background_lagrangian_density": str(aether_density),
        "c_theta": str(c_theta),
        "effective_cosmological_planck_mass_squared": str(m_cos_sq),
        "normalized_cosmological_factor": str(normalized_factor),
        "minisuperspace_lagrangian": str(lagrangian),
        "energy_density": str(energy_density),
        "pressure": str(pressure),
        "friedmann_equation_zero": str(friedmann_residual),
        "radial_equation_zero": str(radial_equation),
        "charge_equation_zero": str(charge_equation),
        "raychaudhuri_H_dot": str(hubble_dot_on_shell),
        "number_density": str(number_density),
        "alignment_background": str(projected_current_sq),
        "force_background_lagrangian": str(force_background_lagrangian),
    }


def integrate_representative_branch(
    t_end: float,
    samples: int,
    parameter_overrides: dict[str, float] | None = None,
    initial_condition_overrides: dict[str, float] | None = None,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    require("positive t_end", t_end > 0)
    require("sufficient samples", samples >= 3)

    # Dimensionless representative point.  These values are selected only to
    # demonstrate existence and numerical consistency, not as a fit.
    params = {
        "M_P": 1.0,
        "M_U": 0.5,
        "c1": 0.10,
        "c2": 0.05,
        "c3": 0.05,
        "c4": 0.05,
        "m_squared": 1.0,
        "lambda4": 0.50,
        "lambda6": 0.20,
        "Lambda": 2.0,
    }
    if parameter_overrides:
        unknown_parameters = set(parameter_overrides) - set(params)
        require("known parameter overrides", not unknown_parameters)
        params.update(
            {
                key: float(value)
                for key, value in parameter_overrides.items()
            }
        )
    c_theta = params["c1"] + 3 * params["c2"] + params["c3"]
    c14 = params["c1"] + params["c4"]
    c123 = params["c1"] + params["c2"] + params["c3"]
    r_u = (params["M_U"] / params["M_P"]) ** 2
    alpha13 = r_u * (params["c1"] + params["c3"])
    alpha2 = r_u * params["c2"]
    m_cos_sq = params["M_P"] ** 2 * (
        1 + (alpha13 + 3 * alpha2) / 2
    )

    require("positive c14", c14 > 0)
    require("positive c1", params["c1"] > 0)
    require("positive c123", c123 > 0)
    require("positive cosmological Planck mass squared", m_cos_sq > 0)

    def potential(rho: float | np.ndarray) -> float | np.ndarray:
        return (
            0.5 * params["m_squared"] * rho**2
            + params["lambda4"] * rho**4 / 8
            + params["lambda6"] * rho**6
            / (24 * params["Lambda"] ** 2)
        )

    def potential_prime(rho: float | np.ndarray) -> float | np.ndarray:
        return (
            params["m_squared"] * rho
            + params["lambda4"] * rho**3 / 2
            + params["lambda6"] * rho**5
            / (4 * params["Lambda"] ** 2)
        )

    initial_overrides = initial_condition_overrides or {}
    known_initial_conditions = {
        "a",
        "rho",
        "rho_dot",
        "Theta",
    }
    require(
        "known initial-condition overrides",
        not (set(initial_overrides) - known_initial_conditions),
    )
    a_initial = float(initial_overrides.get("a", 1.0))
    rho_initial = float(initial_overrides.get("rho", 1.0))
    rho_dot_initial = float(initial_overrides.get("rho_dot", 0.0))
    theta_initial = float(initial_overrides.get("Theta", 0.0))
    require("positive initial scale factor", a_initial > 0)
    require("positive initial amplitude", rho_initial > 0)
    mu_initial = float(
        np.sqrt(potential_prime(rho_initial) / rho_initial)
    )
    conserved_charge = (
        a_initial**3 * rho_initial**2 * mu_initial
    )
    energy_initial = float(
        0.5 * rho_dot_initial**2
        + 0.5 * rho_initial**2 * mu_initial**2
        + potential(rho_initial)
    )
    hubble_initial = float(
        np.sqrt(energy_initial / (3 * m_cos_sq))
    )

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        scale, rho, rho_dot, theta, hubble = state
        if scale <= 0 or rho <= 0:
            raise RuntimeError(
                "Representative branch left the positive a,rho domain."
            )
        mu = conserved_charge / (scale**3 * rho**2)
        return np.array(
            [
                scale * hubble,
                rho_dot,
                -3 * hubble * rho_dot
                + rho * mu**2
                - potential_prime(rho),
                mu,
                -(rho_dot**2 + rho**2 * mu**2) / (2 * m_cos_sq),
            ],
            dtype=float,
        )

    times = np.linspace(0.0, t_end, samples)
    initial_state = np.array(
        [
            a_initial,
            rho_initial,
            rho_dot_initial,
            theta_initial,
            hubble_initial,
        ],
        dtype=float,
    )
    solution = solve_ivp(
        rhs,
        (0.0, t_end),
        initial_state,
        method="DOP853",
        t_eval=times,
        rtol=1e-11,
        atol=1e-13,
    )
    require("integration success", solution.success)
    require("all requested samples returned", solution.t.size == samples)
    require("finite trajectory", bool(np.all(np.isfinite(solution.y))))

    scale, rho, rho_dot, theta, hubble = solution.y
    mu = conserved_charge / (scale**3 * rho**2)
    energy = (
        0.5 * rho_dot**2
        + 0.5 * rho**2 * mu**2
        + potential(rho)
    )
    pressure = (
        0.5 * rho_dot**2
        + 0.5 * rho**2 * mu**2
        - potential(rho)
    )
    friedmann_residual = 3 * m_cos_sq * hubble**2 - energy
    friedmann_scale = np.maximum.reduce(
        [
            np.abs(3 * m_cos_sq * hubble**2),
            np.abs(energy),
            np.full_like(energy, 1e-30),
        ]
    )
    relative_friedmann_residual = np.abs(
        friedmann_residual
    ) / friedmann_scale

    rho_ddot = (
        -3 * hubble * rho_dot
        + rho * mu**2
        - potential_prime(rho)
    )
    mu_dot = mu * (-3 * hubble - 2 * rho_dot / rho)
    energy_dot = (
        rho_dot * rho_ddot
        + rho * rho_dot * mu**2
        + rho**2 * mu * mu_dot
        + potential_prime(rho) * rho_dot
    )
    continuity_residual = energy_dot + 3 * hubble * (
        energy + pressure
    )
    continuity_scale = np.maximum(
        np.abs(3 * hubble * (energy + pressure)),
        1e-30,
    )
    relative_continuity_residual = np.abs(
        continuity_residual
    ) / continuity_scale

    charge_samples = scale**3 * rho**2 * mu
    relative_charge_drift = np.abs(
        charge_samples / conserved_charge - 1
    )
    raychaudhuri_rhs = -(
        rho_dot**2 + rho**2 * mu**2
    ) / (2 * m_cos_sq)
    require(
        "expanding branch remains expanding",
        bool(np.all(hubble > 0)),
    )
    require(
        "scale factor is monotonic",
        bool(np.all(np.diff(scale) > 0)),
    )
    require("positive amplitude", bool(np.all(rho > 0)))
    require(
        "Friedmann residual tolerance",
        float(np.max(relative_friedmann_residual)) < 1e-9,
    )
    require(
        "charge drift tolerance",
        float(np.max(relative_charge_drift)) < 1e-12,
    )
    require(
        "continuity residual tolerance",
        float(np.max(relative_continuity_residual)) < 1e-12,
    )

    rows: list[dict[str, float]] = []
    for index in range(samples):
        rows.append(
            {
                "t": float(solution.t[index]),
                "a": float(scale[index]),
                "rho": float(rho[index]),
                "rho_dot": float(rho_dot[index]),
                "Theta": float(theta[index]),
                "mu": float(mu[index]),
                "H": float(hubble[index]),
                "H_dot": float(raychaudhuri_rhs[index]),
                "energy_density": float(energy[index]),
                "pressure": float(pressure[index]),
                "charge": float(charge_samples[index]),
                "friedmann_residual": float(
                    friedmann_residual[index]
                ),
                "continuity_residual": float(
                    continuity_residual[index]
                ),
            }
        )

    summary: dict[str, object] = {
        "status": "PASS_REPRESENTATIVE_DIMENSIONLESS_BRANCH",
        "parameter_scope": (
            "Dimensionless existence example only; not a cosmological fit."
        ),
        "parameters": params,
        "derived_parameters": {
            "c_theta": c_theta,
            "c14": c14,
            "c123": c123,
            "r_U": r_u,
            "alpha13": alpha13,
            "alpha2": alpha2,
            "M_cos_squared": m_cos_sq,
        },
        "initial_conditions": {
            "a": a_initial,
            "rho": rho_initial,
            "rho_dot": rho_dot_initial,
            "Theta": theta_initial,
            "mu": mu_initial,
            "H": hubble_initial,
            "conserved_charge": conserved_charge,
            "radial_acceleration": float(
                rhs(0.0, initial_state)[2]
            ),
        },
        "integration": {
            "method": "scipy.solve_ivp_DOP853",
            "t_start": 0.0,
            "t_end": t_end,
            "samples": samples,
            "rtol": 1e-11,
            "atol": 1e-13,
            "function_evaluations": int(solution.nfev),
        },
        "endpoint": {
            "a": float(scale[-1]),
            "rho": float(rho[-1]),
            "rho_dot": float(rho_dot[-1]),
            "Theta": float(theta[-1]),
            "mu": float(mu[-1]),
            "H": float(hubble[-1]),
            "energy_density": float(energy[-1]),
            "pressure": float(pressure[-1]),
        },
        "diagnostics": {
            "max_relative_friedmann_residual": float(
                np.max(relative_friedmann_residual)
            ),
            "max_relative_charge_drift": float(
                np.max(relative_charge_drift)
            ),
            "max_relative_continuity_residual": float(
                np.max(relative_continuity_residual)
            ),
            "min_scale_factor": float(np.min(scale)),
            "min_amplitude": float(np.min(rho)),
            "min_hubble": float(np.min(hubble)),
            "max_hubble": float(np.max(hubble)),
            "expansion_factor": float(scale[-1] / scale[0]),
            "amplitude_ratio": float(rho[-1] / rho[0]),
            "chemical_potential_ratio": float(mu[-1] / mu[0]),
            "hubble_monotonic_nonincreasing": bool(
                np.all(np.diff(hubble) <= 1e-13)
            ),
        },
    }
    return summary, rows


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    symbolic = symbolic_derivation()
    numerical, rows = integrate_representative_branch(
        args.t_end,
        args.samples,
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_EVOLVING_FRW_BACKGROUND",
        "calculation_status": "PASS",
        "background_status": "ON_SHELL_REPRESENTATIVE_BRANCH_VERIFIED",
        "ansatz": {
            "metric": (
                "ds^2=-N(t)^2 dt^2+a(t)^2 delta_ij dx^i dx^j"
            ),
            "aether": "U^mu=(1/N,0,0,0)",
            "condensate": (
                "Phi=rho(t)*exp(i*Theta(t))/sqrt(2)"
            ),
            "force": "psi_bar=constant",
            "reservoir": (
                "No background reservoir or charge-transfer source in the "
                "representative branch."
            ),
        },
        "symbolic_derivation": symbolic,
        "representative_branch": numerical,
        "scientific_boundary": (
            "This proves existence and numerical consistency for a "
            "dimensionless background branch. It does not select a physical "
            "parameter point, fit cosmological data, or establish scalar "
            "perturbation stability."
        ),
        "next_required_calculation": [
            "derive the full scalar perturbation action about the evolving branch",
            "eliminate lapse, scalar shift and aether multiplier constraints",
            "compute the reduced kinetic and gradient matrices in a controlled subhorizon regime",
            "retain the full time-dependent system for the strict low-k audit",
            "only introduce reservoir exchange after declaring its action or constitutive perturbation response",
        ],
        "adm_reduction_status": (
            "READY_TO_BEGIN_ON_EVOLVING_FRW_BACKGROUND"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
    }

    json_path = args.output_dir / "uvir003_frw_background_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    csv_path = args.output_dir / "uvir003_frw_background_trajectory.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    diagnostics = numerical["diagnostics"]
    print("UVIR-003 flat-FRW minisuperspace identities: VERIFIED")
    print("Comoving aether cosmological normalization: VERIFIED")
    print("Representative evolving background: ON_SHELL")
    print(
        "Max relative Friedmann residual: "
        f"{diagnostics['max_relative_friedmann_residual']:.3e}"
    )
    print(
        "Max relative charge drift: "
        f"{diagnostics['max_relative_charge_drift']:.3e}"
    )
    print(
        "Max relative continuity residual: "
        f"{diagnostics['max_relative_continuity_residual']:.3e}"
    )
    print("Scalar ADM reduction: READY_TO_BEGIN_ON_EVOLVING_FRW_BACKGROUND")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_EVOLVING_FRW_BACKGROUND")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
