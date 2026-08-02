#!/usr/bin/env python3
"""DISK-001: declared IR force-law helpers (Conditional AQUAL-class baseline).

Master Plan §6 / DISK-001 readiness: solver development may use Conditional
AQUAL-class IR with *declared* (a0, C_obs). This module never claims topology
derivation of a0 or C_obs=2/3 packaging (Selective Publishing B1/B9).

Default Conditional baseline (Master Plan):
  C_obs ~ 1 under C_m = C_IR matching hypothesis for fits,
  a0 as phenomenological input (optional present-epoch DSM label only).

Deep-MOND limit used for analytic benchmarks:
  |g| = C_obs * sqrt(a0 * |g_N|)
  direction parallel to g_N (curl residual measured separately when applied
  to non-spherical sources).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

# km^2 s^-2 kpc^-1 if a0 in those units; keep dimensionless ratios internal.
# SI: a0 ~ 1.2e-10 m/s^2 is ~ 3700 (km/s)^2 / kpc
A0_EMP_KMSKPC = 3700.0  # ~1.2e-10 m s^-2 in SPARC-ish units


@dataclass(frozen=True)
class DeclaredIR:
    """Explicit inputs — must appear in every DISK-001 report table."""

    a0: float
    C_obs: float
    label: str = "Conditional_AQUAL_baseline"
    a0_origin: str = "phenomenological_input"
    C_obs_origin: str = "Conditional_default_Cobs_sim_1_MasterPlan_sec6"
    ban_B9_dual_rar: bool = True

    def __post_init__(self) -> None:
        if self.a0 <= 0 or self.C_obs <= 0:
            raise ValueError("a0 and C_obs must be positive")
        # Hard reject dual RAR packaging combination as default
        # (a0 = c H0 / 2π with C_obs = 2/3). We only check the C_obs side
        # against 2/3 when a0 is labelled geometric DSM.
        if self.ban_B9_dual_rar and abs(self.C_obs - 2.0 / 3.0) < 1e-9:
            if "cH0" in self.a0_origin.lower() or "geometric" in self.a0_origin.lower():
                raise ValueError(
                    "B9: refuse dual packaging C_obs=2/3 with geometric a0=cH0/2π label"
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_conditional_ir(
    a0: float = A0_EMP_KMSKPC,
    C_obs: float = 1.0,
) -> DeclaredIR:
    return DeclaredIR(a0=float(a0), C_obs=float(C_obs))


def deep_mond_speed(g_N: np.ndarray | float, ir: DeclaredIR) -> np.ndarray | float:
    """|g| = C_obs * sqrt(a0 * |g_N|) in deep-MOND limit."""
    g_abs = np.abs(g_N)
    return ir.C_obs * np.sqrt(ir.a0 * g_abs)


def simple_mu_interpolating(x: np.ndarray | float) -> np.ndarray | float:
    """mu(x) = x / sqrt(1+x^2) with x = |g|/a0 (standard simple form)."""
    return x / np.sqrt(1.0 + np.asarray(x, dtype=float) ** 2)


def aqual_g_from_gN(g_N_vec: np.ndarray, ir: DeclaredIR) -> np.ndarray:
    """Vector AQUAL: g parallel to g_N with |g| from simple-μ map.

    Uses a0_eff = C_obs^2 a0 so the deep-MOND limit is
    |g| = C_obs sqrt(a0 |g_N|).
    """
    g_N_vec = np.asarray(g_N_vec, dtype=float)
    nrm = float(np.linalg.norm(g_N_vec))
    if nrm < 1e-30:
        return np.zeros_like(g_N_vec)
    g_mag = float(aqual_g_magnitude(nrm, ir))
    return (g_mag / nrm) * g_N_vec


def a0_effective(ir: DeclaredIR) -> float:
    """a0_eff = C_obs^2 a0 so deep MOND is |g|=C_obs sqrt(a0 |g_N|)."""
    return float((ir.C_obs**2) * ir.a0)


def aqual_g_magnitude(g_N_mag: np.ndarray | float, ir: DeclaredIR) -> np.ndarray | float:
    """Scalar |g| given |g_N| under simple-mu AQUAL with a0_eff = C_obs^2 a0.

    Solves |g| mu(|g|/a0_eff) = |g_N| with mu(x)=x/sqrt(1+x^2).
    """
    g_N_mag = np.asarray(g_N_mag, dtype=float)
    a0_eff = a0_effective(ir)
    y = g_N_mag / a0_eff
    y2 = y * y
    z = 0.5 * (y2 + np.sqrt(y2 * y2 + 4.0 * y2))
    return np.sqrt(z) * a0_eff


def mu_of_grad_phi(grad_mag: np.ndarray | float, ir: DeclaredIR) -> np.ndarray | float:
    """μ(|∇Φ|/a0_eff) for the AQUAL divergence form ∇·(μ ∇Φ)=4πGρ."""
    a0_eff = a0_effective(ir)
    x = np.asarray(grad_mag, dtype=float) / a0_eff
    return simple_mu_interpolating(x)
