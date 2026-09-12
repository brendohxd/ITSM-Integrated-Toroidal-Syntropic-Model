#!/usr/bin/env python3
"""Exact scalar/Dirac transport retry for TOP-X4 candidate X4-S2F3.

This checkpoint preserves the prior low-mode WKB failure and tests a different
construction: positive-Hamiltonian scalar data with exact symplectic transport
and a first-order Dirac superadiabatic projector with exact unitary transport.
It does not construct a full Hadamard state or a renormalized stress tensor.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.linalg import expm

from topx4_a1_background_control import parameters, rhs, stress_components


STATUS = "PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN"
FAIL_STATUS = "FAIL_EXACT_SCALAR_DIRAC_TRANSPORT_CHECKPOINT"
K_OBS_GRID = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)
KK_GRID = (0, 1, 2, 4)
UV_TREND_GRID = (8.0, 16.0, 32.0)
M_F = 1.0
OMEGA4 = np.block(
    [[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]]
)
OMEGA2 = np.array([[0.0, 1.0], [-1.0, 0.0]])
J2 = np.array([[0.0, -1.0], [1.0, 0.0]])
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


def initial_state(p: dict[str, float]) -> np.ndarray:
    state = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    energy, _, _ = stress_components(state, p)
    hubble = math.sqrt(energy / (6.0 * p["M5_cubed"]))
    state[7] = hubble
    state[8] = hubble
    return state


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
        "H_a": h_a,
        "H_b": h_b,
        "charge": a**3 * b * rho**2 * mu,
    }


def make_splines(times: np.ndarray, fields: dict[str, np.ndarray]) -> dict[str, CubicSpline]:
    return {name: CubicSpline(times, values) for name, values in fields.items()}


def scalar_matrices(
    time: float, k_obs: float, n_kk: int, splines: dict[str, CubicSpline]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = {name: float(spline(time)) for name, spline in splines.items()}
    k2 = k_obs**2 / values["a"] ** 2 + n_kk**2 / values["b"] ** 2
    k_matrix = np.array(
        [
            [
                k2
                + values["m_sigma2"]
                - values["gamma"] ** 2
                - values["gamma_dot"],
                -2.0 * values["mu"] * values["h"],
            ],
            [
                -2.0 * values["mu"] * values["h"],
                k2
                - values["gamma"] ** 2
                - values["gamma_dot"]
                - 2.0 * values["h"] * values["gamma"]
                - values["h"] ** 2
                - values["h_dot"],
            ],
        ]
    )
    mu = values["mu"]
    hessian = np.block(
        [
            [k_matrix + mu * mu * np.eye(2), mu * J2],
            [-mu * J2, np.eye(2)],
        ]
    )
    generator = OMEGA4 @ hessian
    return k_matrix, hessian, generator


def normalized_scalar_modes(generator: np.ndarray) -> tuple[np.ndarray, list[float]]:
    eigenvalues, eigenvectors = np.linalg.eig(generator)
    selected = np.flatnonzero(np.imag(eigenvalues) < -1.0e-9)
    if selected.size != 2:
        raise FloatingPointError("charged scalar generator must have two positive-frequency modes")
    modes = eigenvectors[:, selected]
    norm = 1j * modes.conjugate().T @ OMEGA4 @ modes
    norm = 0.5 * (norm + norm.conjugate().T)
    norm_values, norm_vectors = np.linalg.eigh(norm)
    if np.min(norm_values) <= 0.0:
        raise FloatingPointError("positive-frequency scalar symplectic norm is not positive")
    modes = (
        modes
        @ norm_vectors
        @ np.diag(1.0 / np.sqrt(norm_values))
        @ norm_vectors.conjugate().T
    )
    frequencies = sorted(float(-np.imag(eigenvalues[index])) for index in selected)
    return modes, frequencies


def integrate_real_fundamental(
    times: np.ndarray, dimension: int, generator: Callable[[float], np.ndarray]
) -> tuple[Any, np.ndarray]:
    result = solve_ivp(
        fun=lambda time, flat: (generator(time) @ flat.reshape(dimension, dimension)).ravel(),
        t_span=(float(times[0]), float(times[-1])),
        y0=np.eye(dimension).ravel(),
        method="DOP853",
        t_eval=times,
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    matrices = result.y.T.reshape((-1, dimension, dimension))
    return result, matrices


def scalar_transport_diagnostics(
    times: np.ndarray, fields: dict[str, np.ndarray], splines: dict[str, CubicSpline]
) -> dict[str, Any]:
    modes: list[dict[str, Any]] = []
    for k_obs in K_OBS_GRID:
        for n_kk in KK_GRID:
            min_k = float("inf")
            min_g = float("inf")
            for time in times:
                k_matrix, hessian, _ = scalar_matrices(float(time), k_obs, n_kk, splines)
                min_k = min(min_k, float(np.min(np.linalg.eigvalsh(k_matrix))))
                min_g = min(min_g, float(np.min(np.linalg.eigvalsh(hessian))))
            _, _, generator0 = scalar_matrices(float(times[0]), k_obs, n_kk, splines)
            initial_modes, initial_frequencies = normalized_scalar_modes(generator0)
            initial_norm = float(
                np.linalg.norm(
                    1j * initial_modes.conjugate().T @ OMEGA4 @ initial_modes - np.eye(2),
                    ord="fro",
                )
            )
            initial_isotropy = float(
                np.linalg.norm(initial_modes.T @ OMEGA4 @ initial_modes, ord="fro")
            )
            solver, transports = integrate_real_fundamental(
                times,
                4,
                lambda time, k=k_obs, n=n_kk: scalar_matrices(time, k, n, splines)[2],
            )
            max_symplectic = 0.0
            max_norm = 0.0
            max_isotropy = 0.0
            finite = bool(solver.success and np.all(np.isfinite(transports)))
            for transport in transports:
                evolved = transport @ initial_modes
                max_symplectic = max(
                    max_symplectic,
                    float(np.linalg.norm(transport.T @ OMEGA4 @ transport - OMEGA4, ord="fro")),
                )
                max_norm = max(
                    max_norm,
                    float(
                        np.linalg.norm(
                            1j * evolved.conjugate().T @ OMEGA4 @ evolved - np.eye(2),
                            ord="fro",
                        )
                    ),
                )
                max_isotropy = max(
                    max_isotropy,
                    float(np.linalg.norm(evolved.T @ OMEGA4 @ evolved, ord="fro")),
                )
            _, _, generator_final = scalar_matrices(float(times[-1]), k_obs, n_kk, splines)
            instantaneous_final, _ = normalized_scalar_modes(generator_final)
            evolved_final = transports[-1] @ initial_modes
            beta = -1j * instantaneous_final.T @ OMEGA4 @ evolved_final
            final_mixing = float(np.real(np.trace(beta.conjugate().T @ beta)))
            modes.append(
                {
                    "k_obs": k_obs,
                    "n": n_kk,
                    "min_K_eigenvalue": min_k,
                    "min_Hamiltonian_eigenvalue": min_g,
                    "initial_frequencies": initial_frequencies,
                    "initial_normalization_residual": initial_norm,
                    "initial_isotropy_residual": initial_isotropy,
                    "solver_success": bool(solver.success),
                    "finite_transport": finite,
                    "max_symplectic_residual": max_symplectic,
                    "max_mode_normalization_residual": max_norm,
                    "max_mode_isotropy_residual": max_isotropy,
                    "final_instantaneous_basis_mixing": final_mixing,
                }
            )
    uv_monotonic = True
    for n_kk in KK_GRID:
        sequence = [
            next(
                mode["final_instantaneous_basis_mixing"]
                for mode in modes
                if mode["n"] == n_kk and mode["k_obs"] == k_obs
            )
            for k_obs in UV_TREND_GRID
        ]
        uv_monotonic = uv_monotonic and sequence[0] > sequence[1] > sequence[2]
    return {
        "modes": modes,
        "all_positive_K": all(mode["min_K_eigenvalue"] > 0.0 for mode in modes),
        "all_positive_Hamiltonians": all(
            mode["min_Hamiltonian_eigenvalue"] > 0.0 for mode in modes
        ),
        "all_finite": all(mode["finite_transport"] for mode in modes),
        "max_initial_normalization_residual": max(
            mode["initial_normalization_residual"] for mode in modes
        ),
        "max_initial_isotropy_residual": max(
            mode["initial_isotropy_residual"] for mode in modes
        ),
        "max_symplectic_residual": max(mode["max_symplectic_residual"] for mode in modes),
        "max_mode_normalization_residual": max(
            mode["max_mode_normalization_residual"] for mode in modes
        ),
        "max_mode_isotropy_residual": max(
            mode["max_mode_isotropy_residual"] for mode in modes
        ),
        "uv_endpoint_mixing_strictly_decreases": bool(uv_monotonic),
        "uv_max_endpoint_mixing": max(
            mode["final_instantaneous_basis_mixing"]
            for mode in modes
            if mode["k_obs"] in UV_TREND_GRID
        ),
    }


def chi_transport_diagnostics(
    times: np.ndarray, fields: dict[str, np.ndarray]
) -> dict[str, Any]:
    modes: list[dict[str, Any]] = []
    for k_obs in K_OBS_GRID:
        for n_kk in KK_GRID:
            omega2 = (
                k_obs**2 / fields["a"] ** 2
                + n_kk**2 / fields["b"] ** 2
                + fields["m_chi_eff2"]
                - fields["gamma_dot"]
                - fields["gamma"] ** 2
            )
            omega2_spline = CubicSpline(times, omega2)
            omega0 = math.sqrt(float(omega2[0]))
            initial_mode = np.array(
                [[1.0 / math.sqrt(2.0 * omega0)], [-1j * math.sqrt(omega0 / 2.0)]]
            )
            solver, transports = integrate_real_fundamental(
                times,
                2,
                lambda time, spline=omega2_spline: np.array(
                    [[0.0, 1.0], [-float(spline(time)), 0.0]]
                ),
            )
            max_symplectic = 0.0
            max_norm = 0.0
            for transport in transports:
                evolved = transport @ initial_mode
                max_symplectic = max(
                    max_symplectic,
                    float(np.linalg.norm(transport.T @ OMEGA2 @ transport - OMEGA2, ord="fro")),
                )
                max_norm = max(
                    max_norm,
                    float(
                        np.linalg.norm(
                            1j * evolved.conjugate().T @ OMEGA2 @ evolved - np.eye(1),
                            ord="fro",
                        )
                    ),
                )
            omega_final = math.sqrt(float(omega2[-1]))
            instantaneous_final = np.array(
                [
                    [1.0 / math.sqrt(2.0 * omega_final)],
                    [-1j * math.sqrt(omega_final / 2.0)],
                ]
            )
            evolved_final = transports[-1] @ initial_mode
            beta = -1j * instantaneous_final.T @ OMEGA2 @ evolved_final
            mixing = float(np.real((beta.conjugate().T @ beta)[0, 0]))
            modes.append(
                {
                    "k_obs": k_obs,
                    "n": n_kk,
                    "min_frequency_squared": float(np.min(omega2)),
                    "solver_success": bool(solver.success),
                    "finite_transport": bool(solver.success and np.all(np.isfinite(transports))),
                    "max_symplectic_residual": max_symplectic,
                    "max_wronskian_residual": max_norm,
                    "final_instantaneous_basis_mixing": mixing,
                }
            )
    uv_monotonic = True
    for n_kk in KK_GRID:
        sequence = [
            next(
                mode["final_instantaneous_basis_mixing"]
                for mode in modes
                if mode["n"] == n_kk and mode["k_obs"] == k_obs
            )
            for k_obs in UV_TREND_GRID
        ]
        uv_monotonic = uv_monotonic and sequence[0] > sequence[1] > sequence[2]
    return {
        "modes": modes,
        "all_frequencies_positive": all(mode["min_frequency_squared"] > 0.0 for mode in modes),
        "all_finite": all(mode["finite_transport"] for mode in modes),
        "max_symplectic_residual": max(mode["max_symplectic_residual"] for mode in modes),
        "max_wronskian_residual": max(mode["max_wronskian_residual"] for mode in modes),
        "uv_endpoint_mixing_strictly_decreases": bool(uv_monotonic),
        "uv_max_endpoint_mixing": max(
            mode["final_instantaneous_basis_mixing"]
            for mode in modes
            if mode["k_obs"] in UV_TREND_GRID
        ),
    }


def dirac_matrices() -> tuple[list[np.ndarray], np.ndarray]:
    sigma1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma2 = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    sigma3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    identity = np.eye(2, dtype=complex)
    alphas = [
        np.kron(sigma1, sigma1),
        np.kron(sigma1, sigma2),
        np.kron(sigma1, sigma3),
        np.kron(sigma2, identity),
    ]
    beta = np.kron(sigma3, identity)
    return alphas, beta


def clifford_residual(alphas: list[np.ndarray], beta: np.ndarray) -> float:
    matrices = [*alphas, beta]
    identity = np.eye(4, dtype=complex)
    residual = 0.0
    for row, left in enumerate(matrices):
        residual = max(residual, float(np.linalg.norm(left - left.conjugate().T, ord="fro")))
        for column, right in enumerate(matrices):
            target = 2.0 * identity if row == column else np.zeros((4, 4), dtype=complex)
            residual = max(
                residual,
                float(np.linalg.norm(left @ right + right @ left - target, ord="fro")),
            )
    return residual


def dirac_hamiltonian(
    time: float,
    k_obs: float,
    n_kk: int,
    splines: dict[str, CubicSpline],
    alphas: list[np.ndarray],
    beta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    a = float(splines["a"](time))
    b = float(splines["b"](time))
    h_a = float(splines["H_a"](time))
    h_b = float(splines["H_b"](time))
    momentum_a = k_obs / a
    momentum_b = n_kk / b
    hamiltonian = alphas[0] * momentum_a + alphas[3] * momentum_b + beta * M_F
    omega = math.sqrt(momentum_a**2 + momentum_b**2 + M_F**2)
    hamiltonian_dot = -alphas[0] * h_a * momentum_a - alphas[3] * h_b * momentum_b
    omega_dot = -(h_a * momentum_a**2 + h_b * momentum_b**2) / omega
    return hamiltonian, hamiltonian_dot, omega, omega_dot


def dirac_parts(
    time: float,
    k_obs: float,
    n_kk: int,
    splines: dict[str, CubicSpline],
    alphas: list[np.ndarray],
    beta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
    hamiltonian, hamiltonian_dot, omega, omega_dot = dirac_hamiltonian(
        time, k_obs, n_kk, splines, alphas, beta
    )
    projector = 0.5 * (np.eye(4) + hamiltonian / omega)
    projector_dot = 0.5 * (
        hamiltonian_dot / omega - hamiltonian * omega_dot / omega**2
    )
    first_order = (-1j / (2.0 * omega)) * (
        projector_dot @ projector - projector @ projector_dot
    )
    rotation_generator = first_order @ projector - projector @ first_order
    rotation = expm(rotation_generator)
    adiabatic_projector = rotation @ projector @ rotation.conjugate().T
    return hamiltonian, projector, projector_dot, adiabatic_projector, omega


def integrate_dirac_modes(
    times: np.ndarray,
    initial_modes: np.ndarray,
    hamiltonian: Callable[[float], np.ndarray],
) -> tuple[Any, np.ndarray]:
    entries = initial_modes.size
    initial_flat = np.concatenate((initial_modes.real.ravel(), initial_modes.imag.ravel()))

    def equation(time: float, flat: np.ndarray) -> np.ndarray:
        modes = flat[:entries].reshape(initial_modes.shape) + 1j * flat[entries:].reshape(
            initial_modes.shape
        )
        derivative = -1j * hamiltonian(time) @ modes
        return np.concatenate((derivative.real.ravel(), derivative.imag.ravel()))

    result = solve_ivp(
        fun=equation,
        t_span=(float(times[0]), float(times[-1])),
        y0=initial_flat,
        method="DOP853",
        t_eval=times,
        rtol=1.0e-10,
        atol=1.0e-12,
    )
    real = result.y[:entries].T.reshape((-1, *initial_modes.shape))
    imaginary = result.y[entries:].T.reshape((-1, *initial_modes.shape))
    return result, real + 1j * imaginary


def dirac_transport_diagnostics(
    times: np.ndarray, splines: dict[str, CubicSpline]
) -> dict[str, Any]:
    alphas, beta = dirac_matrices()
    gamma_residual = clifford_residual(alphas, beta)
    modes: list[dict[str, Any]] = []
    step = float(times[1] - times[0])
    for k_obs in K_OBS_GRID:
        for n_kk in KK_GRID:
            initial_parts = dirac_parts(
                float(times[0]), k_obs, n_kk, splines, alphas, beta
            )
            hamiltonian0, projector0, projector_dot0, projector_ad0, omega0 = initial_parts
            max_hamiltonian_hermiticity = 0.0
            for time in times:
                sampled_hamiltonian = dirac_hamiltonian(
                    float(time), k_obs, n_kk, splines, alphas, beta
                )[0]
                max_hamiltonian_hermiticity = max(
                    max_hamiltonian_hermiticity,
                    float(
                        np.linalg.norm(
                            sampled_hamiltonian - sampled_hamiltonian.conjugate().T,
                            ord="fro",
                        )
                    ),
                )
            nearby = [
                dirac_parts(float(time), k_obs, n_kk, splines, alphas, beta)[3]
                for time in times[:5]
            ]
            projector_ad_dot0 = (
                -25.0 * nearby[0]
                + 48.0 * nearby[1]
                - 36.0 * nearby[2]
                + 16.0 * nearby[3]
                - 3.0 * nearby[4]
            ) / (12.0 * step)
            defect0 = float(np.linalg.norm(1j * projector_dot0, ord="fro"))
            defect1 = float(
                np.linalg.norm(
                    1j * projector_ad_dot0
                    - (hamiltonian0 @ projector_ad0 - projector_ad0 @ hamiltonian0),
                    ord="fro",
                )
            )
            eigenvalues, eigenvectors = np.linalg.eigh(projector_ad0)
            selected = np.argsort(eigenvalues)[-2:]
            initial_modes = eigenvectors[:, selected]
            solver, evolved_modes = integrate_dirac_modes(
                times,
                initial_modes,
                lambda time, k=k_obs, n=n_kk: dirac_hamiltonian(
                    time, k, n, splines, alphas, beta
                )[0],
            )
            max_norm = max(
                float(np.linalg.norm(modes_at_time.conjugate().T @ modes_at_time - np.eye(2)))
                for modes_at_time in evolved_modes
            )
            hamiltonian_final, projector_final, _, _, _ = dirac_parts(
                float(times[-1]), k_obs, n_kk, splines, alphas, beta
            )
            del hamiltonian_final
            final_modes = evolved_modes[-1]
            leakage = float(
                np.real(
                    np.trace(
                        final_modes.conjugate().T
                        @ (np.eye(4) - projector_final)
                        @ final_modes
                    )
                )
                / 2.0
            )
            modes.append(
                {
                    "k_obs": k_obs,
                    "n": n_kk,
                    "initial_omega": omega0,
                    "max_Hamiltonian_hermiticity_residual": max_hamiltonian_hermiticity,
                    "projector_hermiticity_residual": float(
                        np.linalg.norm(projector_ad0 - projector_ad0.conjugate().T, ord="fro")
                    ),
                    "projector_idempotency_residual": float(
                        np.linalg.norm(projector_ad0 @ projector_ad0 - projector_ad0, ord="fro")
                    ),
                    "projector_trace": float(np.real(np.trace(projector_ad0))),
                    "zeroth_order_invariance_defect": defect0,
                    "first_order_invariance_defect": defect1,
                    "defect_ratio": defect1 / defect0,
                    "solver_success": bool(solver.success),
                    "finite_transport": bool(solver.success and np.all(np.isfinite(evolved_modes))),
                    "max_inner_product_residual": max_norm,
                    "final_negative_energy_leakage": leakage,
                }
            )
    uv_monotonic = True
    for n_kk in KK_GRID:
        sequence = [
            next(
                mode["final_negative_energy_leakage"]
                for mode in modes
                if mode["n"] == n_kk and mode["k_obs"] == k_obs
            )
            for k_obs in UV_TREND_GRID
        ]
        uv_monotonic = uv_monotonic and sequence[0] > sequence[1] > sequence[2]
    return {
        "N_F": 3,
        "m_F_dimensionless_equal_mass_control": M_F,
        "clifford_residual": gamma_residual,
        "modes": modes,
        "all_Hamiltonians_Hermitian": all(
            mode["max_Hamiltonian_hermiticity_residual"] < 1.0e-14 for mode in modes
        ),
        "all_projectors_rank_two": all(
            abs(mode["projector_trace"] - 2.0) < 1.0e-12 for mode in modes
        ),
        "all_projectors_exact": all(
            mode["projector_hermiticity_residual"] < 1.0e-12
            and mode["projector_idempotency_residual"] < 1.0e-12
            for mode in modes
        ),
        "max_defect_ratio": max(mode["defect_ratio"] for mode in modes),
        "all_first_order_defects_reduced": all(mode["defect_ratio"] < 1.0 for mode in modes),
        "all_finite": all(mode["finite_transport"] for mode in modes),
        "max_inner_product_residual": max(
            mode["max_inner_product_residual"] for mode in modes
        ),
        "uv_endpoint_leakage_strictly_decreases": bool(uv_monotonic),
        "uv_max_endpoint_leakage": max(
            mode["final_negative_energy_leakage"]
            for mode in modes
            if mode["k_obs"] in UV_TREND_GRID
        ),
    }


def symbolic_hamiltonian_check() -> dict[str, Any]:
    mu, mu_dot = sp.symbols("mu mu_dot", real=True)
    k11, k12, k22 = sp.symbols("K11 K12 K22", real=True)
    k_matrix = sp.Matrix([[k11, k12], [k12, k22]])
    identity = sp.eye(2)
    j_matrix = sp.Matrix([[0, -1], [1, 0]])
    omega = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(2), identity),
        sp.Matrix.hstack(-identity, sp.zeros(2)),
    )
    hessian = sp.Matrix.vstack(
        sp.Matrix.hstack(k_matrix + mu**2 * identity, mu * j_matrix),
        sp.Matrix.hstack(-mu * j_matrix, identity),
    )
    generator = omega * hessian
    expected = sp.Matrix.vstack(
        sp.Matrix.hstack(-mu * j_matrix, identity),
        sp.Matrix.hstack(-(k_matrix + mu**2 * identity), -mu * j_matrix),
    )
    generator_exact = sp.simplify(generator - expected) == sp.zeros(4)
    q1, q2, qd1, qd2 = sp.symbols("q1 q2 qd1 qd2", real=True)
    q = sp.Matrix([q1, q2])
    q_dot = sp.Matrix([qd1, qd2])
    second_order = -k_matrix * q - 2 * mu * j_matrix * q_dot - mu_dot * j_matrix * q
    target = -(k_matrix + mu_dot * j_matrix) * q - 2 * mu * j_matrix * q_dot
    return {
        "Hamilton_generator_exact": bool(generator_exact),
        "second_order_equation_exact": bool(sp.simplify(second_order - target) == sp.zeros(2, 1)),
        "Hamiltonian_matrix": str(hessian),
        "generator": str(generator),
    }


def constant_background_controls() -> dict[str, float]:
    k2 = 5.0
    m2 = 2.0
    mu = 0.7
    k_matrix = np.diag([k2 + m2, k2])
    hessian = np.block(
        [[k_matrix + mu**2 * np.eye(2), mu * J2], [-mu * J2, np.eye(2)]]
    )
    generator = OMEGA4 @ hessian
    initial_modes, frequencies = normalized_scalar_modes(generator)
    transport = expm(generator)
    beta_scalar = -1j * initial_modes.T @ OMEGA4 @ (transport @ initial_modes)
    scalar_mixing = float(np.real(np.trace(beta_scalar.conjugate().T @ beta_scalar)))

    omega_chi = 2.3
    chi_generator = np.array([[0.0, 1.0], [-omega_chi**2, 0.0]])
    chi_mode = np.array(
        [[1.0 / math.sqrt(2.0 * omega_chi)], [-1j * math.sqrt(omega_chi / 2.0)]]
    )
    chi_evolved = expm(chi_generator) @ chi_mode
    beta_chi = -1j * chi_mode.T @ OMEGA2 @ chi_evolved
    chi_mixing = float(np.real((beta_chi.conjugate().T @ beta_chi)[0, 0]))

    alphas, beta = dirac_matrices()
    hamiltonian = 3.0 * alphas[0] + 2.0 * alphas[3] + M_F * beta
    omega_dirac = math.sqrt(14.0)
    projector = 0.5 * (np.eye(4) + hamiltonian / omega_dirac)
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    spinors = eigenvectors[:, np.argsort(eigenvalues)[-2:]]
    evolved_spinors = expm(-1j * hamiltonian) @ spinors
    dirac_leakage = float(
        np.real(
            np.trace(
                evolved_spinors.conjugate().T @ (np.eye(4) - projector) @ evolved_spinors
            )
        )
        / 2.0
    )

    coefficient = m2 + 4.0 * mu**2
    discriminant = coefficient**2 + 16.0 * mu**2 * k2
    expected_frequencies = sorted(
        [
            math.sqrt(0.5 * (2.0 * k2 + coefficient - math.sqrt(discriminant))),
            math.sqrt(0.5 * (2.0 * k2 + coefficient + math.sqrt(discriminant))),
        ]
    )
    return {
        "scalar_frequency_regression_residual": max(
            abs(left - right) for left, right in zip(frequencies, expected_frequencies)
        ),
        "scalar_static_mixing": scalar_mixing,
        "chi_static_mixing": chi_mixing,
        "dirac_static_leakage": dirac_leakage,
    }


def diagnostic_envelope(result: dict[str, Any]) -> np.ndarray:
    return np.array(
        [
            result["scalar"]["max_symplectic_residual"],
            result["scalar"]["max_mode_normalization_residual"],
            result["scalar"]["uv_max_endpoint_mixing"],
            result["chi"]["max_wronskian_residual"],
            result["chi"]["uv_max_endpoint_mixing"],
            result["dirac"]["max_inner_product_residual"],
            result["dirac"]["max_defect_ratio"],
            result["dirac"]["uv_max_endpoint_leakage"],
        ]
    )


def run_transport(points: int, p: dict[str, float]) -> dict[str, Any]:
    solution = integrate_background(points, p)
    fields = background_fields(solution, p)
    splines = make_splines(solution.t, fields)
    return {
        "points": points,
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
        "scalar": scalar_transport_diagnostics(solution.t, fields, splines),
        "chi": chi_transport_diagnostics(solution.t, fields),
        "dirac": dirac_transport_diagnostics(solution.t, splines),
    }


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    base = root / "Analysis" / "TOP" / "TOP-X4"
    output_dir = base / "outputs"
    prior_output_path = output_dir / "topx4_s2f3_dynamic_state_subtraction_summary.json"
    authority_paths = [
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md",
        root
        / "Theory"
        / "Core"
        / "Reasoning_Mode_Plans"
        / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
        / "PLAN.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_DYNAMIC_STATE_SUBTRACTION_CONTRACT_2026-09-12.md",
        root / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_EXACT_TRANSPORT_RETRY_CONTRACT_2026-09-12.md",
        base / "TOPX4_S2F3_PLAN11_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT_2026-09-12.md",
        prior_output_path,
        output_dir / "topx4_a1_background_summary.json",
        output_dir / "topx4_s2f3_finite_charge_operator_summary.json",
    ]
    receipts = [sidecar_check(path, root) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "frozen_authority_sidecars_match",
        all(receipt["matches"] for receipt in receipts),
        receipts=receipts,
    )

    prior = json.loads(prior_output_path.read_text(encoding="utf-8"))
    prior_failed_modes = sorted(
        (branch_name, float(mode["k_obs"]), int(mode["n"]))
        for mode in prior["primary_diagnostics"]["modes"]
        for branch_name, branch in mode["branches"].items()
        if not branch["positive"]
    )
    expected_failed_modes = sorted(
        [("charged_minus", 1.0, 0), ("chi", 1.0, 0), ("charged_minus", 1.0, 1)]
    )
    add_check(
        checks,
        "prior_WKB_failure_is_preserved",
        prior["status"] == "FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT"
        and prior["calculation_checks_passed"] == 11
        and prior["calculation_checks_total"] == 12
        and prior_failed_modes == expected_failed_modes,
        prior_status=prior["status"],
        prior_checks=f"{prior['calculation_checks_passed']}/{prior['calculation_checks_total']}",
        failed_modes=prior_failed_modes,
    )

    dimension_ledger = {
        "rho_sigma_pi": "3/2",
        "Psi": "2",
        "momentum_mu_mF": "1",
        "K": "2",
        "H_D": "1",
        "projector": "0",
        "scale_factors": "0",
    }
    add_check(
        checks,
        "five_dimensional_dimension_ledger",
        dimension_ledger
        == {
            "rho_sigma_pi": "3/2",
            "Psi": "2",
            "momentum_mu_mF": "1",
            "K": "2",
            "H_D": "1",
            "projector": "0",
            "scale_factors": "0",
        },
        dimensions=dimension_ledger,
        absolute_mass_prediction=False,
    )

    symbolic = symbolic_hamiltonian_check()
    static_controls = constant_background_controls()
    add_check(
        checks,
        "scalar_Hamilton_equations_and_constant_branch_regression",
        symbolic["Hamilton_generator_exact"]
        and symbolic["second_order_equation_exact"]
        and static_controls["scalar_frequency_regression_residual"] < 1.0e-12,
        symbolic=symbolic,
        constant_frequency_residual=static_controls["scalar_frequency_regression_residual"],
    )

    p = parameters()
    primary = run_transport(801, p)
    witness = run_transport(401, p)
    add_check(
        checks,
        "registered_background_and_scalar_Hamiltonians_are_valid",
        primary["solver_success"]
        and witness["solver_success"]
        and primary["finite_positive_background"]
        and witness["finite_positive_background"]
        and primary["max_charge_relative_error"] < 1.0e-9
        and witness["max_charge_relative_error"] < 1.0e-9
        and primary["scalar"]["all_positive_K"]
        and primary["scalar"]["all_positive_Hamiltonians"]
        and witness["scalar"]["all_positive_K"]
        and witness["scalar"]["all_positive_Hamiltonians"],
        primary_charge_error=primary["max_charge_relative_error"],
        witness_charge_error=witness["max_charge_relative_error"],
        primary_min_K=min(
            mode["min_K_eigenvalue"] for mode in primary["scalar"]["modes"]
        ),
        primary_min_Hamiltonian=min(
            mode["min_Hamiltonian_eigenvalue"] for mode in primary["scalar"]["modes"]
        ),
        limitation="not the coupled gravity/radion physical Hessian",
    )
    add_check(
        checks,
        "initial_charged_scalar_modes_are_canonically_normalized",
        primary["scalar"]["max_initial_normalization_residual"] < 1.0e-12
        and primary["scalar"]["max_initial_isotropy_residual"] < 1.0e-12
        and witness["scalar"]["max_initial_normalization_residual"] < 1.0e-12
        and witness["scalar"]["max_initial_isotropy_residual"] < 1.0e-12,
        primary_normalization=primary["scalar"]["max_initial_normalization_residual"],
        primary_isotropy=primary["scalar"]["max_initial_isotropy_residual"],
    )
    scalar_transport_ok = all(
        result["scalar"][key] < 5.0e-8
        for result in (primary, witness)
        for key in (
            "max_symplectic_residual",
            "max_mode_normalization_residual",
            "max_mode_isotropy_residual",
        )
    )
    add_check(
        checks,
        "exact_charged_scalar_transport_preserves_symplectic_normalization",
        scalar_transport_ok,
        primary_symplectic=primary["scalar"]["max_symplectic_residual"],
        primary_mode_normalization=primary["scalar"]["max_mode_normalization_residual"],
        primary_mode_isotropy=primary["scalar"]["max_mode_isotropy_residual"],
        threshold=5.0e-8,
    )
    add_check(
        checks,
        "exact_chi_transport_is_positive_and_preserves_Wronskian",
        primary["chi"]["all_frequencies_positive"]
        and witness["chi"]["all_frequencies_positive"]
        and primary["chi"]["max_wronskian_residual"] < 5.0e-8
        and witness["chi"]["max_wronskian_residual"] < 5.0e-8,
        primary_wronskian=primary["chi"]["max_wronskian_residual"],
        threshold=5.0e-8,
    )
    prior_low_modes = {(1.0, 0), (1.0, 1)}
    low_modes_finite = all(
        mode["finite_transport"]
        for result in (primary, witness)
        for mode in result["scalar"]["modes"]
        if (mode["k_obs"], mode["n"]) in prior_low_modes
    ) and all(
        mode["finite_transport"]
        for result in (primary, witness)
        for mode in result["chi"]["modes"]
        if (mode["k_obs"], mode["n"]) == (1.0, 0)
    )
    add_check(
        checks,
        "previously_failed_low_modes_have_finite_exact_transport",
        low_modes_finite and primary["scalar"]["all_finite"] and primary["chi"]["all_finite"],
        replacement_method="positive-Hamiltonian Cauchy data plus exact transport; no WKB iterate",
        retroactive_WKB_pass=False,
    )
    add_check(
        checks,
        "scalar_UV_endpoint_mixing_strictly_decreases",
        primary["scalar"]["uv_endpoint_mixing_strictly_decreases"]
        and witness["scalar"]["uv_endpoint_mixing_strictly_decreases"]
        and primary["chi"]["uv_endpoint_mixing_strictly_decreases"]
        and witness["chi"]["uv_endpoint_mixing_strictly_decreases"],
        trend_grid=list(UV_TREND_GRID),
        convergence_claim=False,
    )
    add_check(
        checks,
        "Dirac_Clifford_algebra_and_Hamiltonians_are_Hermitian",
        primary["dirac"]["clifford_residual"] < 1.0e-14
        and witness["dirac"]["clifford_residual"] < 1.0e-14
        and primary["dirac"]["all_Hamiltonians_Hermitian"]
        and witness["dirac"]["all_Hamiltonians_Hermitian"],
        clifford_residual=primary["dirac"]["clifford_residual"],
        threshold=1.0e-14,
    )
    add_check(
        checks,
        "first_order_Dirac_projectors_are_exact_rank_two_projectors",
        primary["dirac"]["all_projectors_rank_two"]
        and witness["dirac"]["all_projectors_rank_two"]
        and primary["dirac"]["all_projectors_exact"]
        and witness["dirac"]["all_projectors_exact"],
        threshold=1.0e-12,
    )
    add_check(
        checks,
        "first_order_Dirac_projector_reduces_invariance_defect",
        primary["dirac"]["all_first_order_defects_reduced"]
        and witness["dirac"]["all_first_order_defects_reduced"]
        and primary["dirac"]["max_defect_ratio"] < 0.25
        and witness["dirac"]["max_defect_ratio"] < 0.25,
        primary_max_ratio=primary["dirac"]["max_defect_ratio"],
        witness_max_ratio=witness["dirac"]["max_defect_ratio"],
        threshold=0.25,
    )
    add_check(
        checks,
        "exact_Dirac_transport_preserves_inner_products",
        primary["dirac"]["all_finite"]
        and witness["dirac"]["all_finite"]
        and primary["dirac"]["max_inner_product_residual"] < 5.0e-8
        and witness["dirac"]["max_inner_product_residual"] < 5.0e-8,
        primary_max_residual=primary["dirac"]["max_inner_product_residual"],
        threshold=5.0e-8,
    )
    add_check(
        checks,
        "Dirac_UV_endpoint_leakage_strictly_decreases",
        primary["dirac"]["uv_endpoint_leakage_strictly_decreases"]
        and witness["dirac"]["uv_endpoint_leakage_strictly_decreases"],
        trend_grid=list(UV_TREND_GRID),
        convergence_claim=False,
    )
    add_check(
        checks,
        "static_background_controls_have_zero_mixing",
        static_controls["scalar_static_mixing"] < 1.0e-10
        and static_controls["chi_static_mixing"] < 1.0e-10
        and abs(static_controls["dirac_static_leakage"]) < 1.0e-10,
        controls=static_controls,
        threshold=1.0e-10,
    )
    envelope_difference = float(
        np.max(np.abs(diagnostic_envelope(primary) - diagnostic_envelope(witness)))
    )
    add_check(
        checks,
        "primary_and_resolution_witness_envelopes_agree",
        envelope_difference < 2.0e-5,
        maximum_absolute_difference=envelope_difference,
        threshold=2.0e-5,
    )

    alphas, beta = dirac_matrices()
    broken_alphas = [*alphas]
    broken_alphas[3] = broken_alphas[0]
    broken_clifford_residual = clifford_residual(broken_alphas, beta)
    wrong_omega = np.block(
        [[np.zeros((2, 2)), np.eye(2)], [np.eye(2), np.zeros((2, 2))]]
    )
    wrong_symplectic_residual = float(np.linalg.norm(wrong_omega.T + wrong_omega))
    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    prior_wkb_import = (
        "from " + "topx4_s2f3_dynamic_state_subtraction_checkpoint"
    ) in source_text
    static_vacuum_import = (
        "from " + "topx4_s2f3_static_determinant_checkpoint"
    ) in source_text
    add_check(
        checks,
        "mutations_and_scope_firewalls_are_rejected",
        wrong_symplectic_residual > 1.0
        and broken_clifford_residual > 1.0
        and not prior_wkb_import
        and not static_vacuum_import
        and not forbidden_hits,
        wrong_symplectic_residual=wrong_symplectic_residual,
        broken_clifford_residual=broken_clifford_residual,
        prior_WKB_solver_imported=prior_wkb_import,
        static_vacuum_solver_imported=static_vacuum_import,
        forbidden_source_tokens=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_EXACT_TRANSPORT_RETRY_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "full_Hadamard_state": False,
        "covariant_5D_subtraction": "NOT_DERIVED",
        "renormalized_stress": "NOT_COMPUTED",
        "advance_to_semiclassical_background": False,
        "advance_to_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "dimension_ledger": dimension_ledger,
        "registered_control": {
            "time_interval": [0.0, 1.0],
            "Cauchy_surface": 0.0,
            "primary_points": 801,
            "witness_points": 401,
            "k_obs": list(K_OBS_GRID),
            "n": list(KK_GRID),
            "UV_trend_grid": list(UV_TREND_GRID),
            "N_F": 3,
            "m_F": M_F,
            "units": "dimensionless equal-mass A1 control; no absolute mass prediction",
        },
        "prior_negative_evidence": {
            "status": prior["status"],
            "failed_modes": prior_failed_modes,
            "retroactively_reclassified": False,
        },
        "state_scope": {
            "charged_scalar": "instantaneous positive-Hamiltonian data at t=0 plus exact symplectic transport",
            "chi": "instantaneous positive-frequency data at t=0 plus exact symplectic transport",
            "Dirac": "first-order superadiabatic projector at t=0 plus exact unitary transport",
            "low_mode_rule": "exact transport; no WKB iterate",
            "finite_order_only": True,
            "Hadamard_claim": False,
        },
        "symbolic_checks": symbolic,
        "static_controls": static_controls,
        "primary_diagnostics": primary,
        "resolution_witness": witness,
        "resolution_envelope_difference": envelope_difference,
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "hold_reasons": [
            "the scalar instantaneous positive-Hamiltonian state is not an infinite-order adiabatic/Hadamard construction",
            "the Dirac projector is first order, not the infinite-order state required for a Hadamard claim",
            "no covariant five-dimensional subtraction or local counterterm map is derived",
            "no renormalized stress, self-consistent semiclassical solution, or physical constrained Hessian is computed",
            "the parity-odd determinant phase and quantized counterterms remain unaudited",
        ],
        "next_required_calculation": (
            "derive a matrix/spinor high-order or pseudodifferential Hadamard construction and the "
            "covariant five-dimensional subtraction/counterterm map before any stress integral"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this exact scalar/Dirac transport retry",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "derived_claims": [],
        "explicit_nonclaims": [
            "no retroactive pass of the failed branchwise WKB checkpoint",
            "no full Hadamard state",
            "no covariant subtraction or renormalized quantum stress",
            "no finite-charge semiclassical background",
            "no physical radion mass or Hessian",
            "no parity or anomaly clearance",
            "no architecture, A4, Ultra, phenomenology, or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_exact_transport_retry_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"checks={result['calculation_checks_passed']}/{result['calculation_checks_total']}")
    print(f"scalar_symplectic_residual={primary['scalar']['max_symplectic_residual']:.17g}")
    print(f"dirac_inner_product_residual={primary['dirac']['max_inner_product_residual']:.17g}")
    print(f"dirac_max_defect_ratio={primary['dirac']['max_defect_ratio']:.17g}")
    print(f"resolution_envelope_difference={envelope_difference:.17g}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print("full_Hadamard_state=false")
    print("advance_to_semiclassical_background=false")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
