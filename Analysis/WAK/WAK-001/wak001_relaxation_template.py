#!/usr/bin/env python3
"""WAK-001 Stage-1 mathematical audit for a minimal relaxation template.

This script tests

    tau * (d_t + v * d_x) W + W = kappa * S

on a periodic one-dimensional domain. It does not assert that this equation is
the ITSM wake law and it does not fit any physical coefficient.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math


TOL = 1.0e-12


@dataclass(frozen=True)
class RelaxationTemplate:
    tau: float
    velocity: float
    coupling: float
    matter_light_speed: float = 1.0

    def validate_domain(self) -> None:
        if not math.isfinite(self.tau) or self.tau <= 0.0:
            raise ValueError("tau must be finite and strictly positive")
        if not math.isfinite(self.velocity):
            raise ValueError("velocity must be finite")
        if abs(self.velocity) > self.matter_light_speed:
            raise ValueError("transport characteristic is outside matter cone")
        if not math.isfinite(self.coupling):
            raise ValueError("coupling must be finite")

    def source_free_eigenvalue(self, wave_number: float) -> complex:
        """Return lambda for W proportional to exp(lambda*t + i*k*x)."""
        self.validate_domain()
        return complex(-1.0 / self.tau, -self.velocity * wave_number)

    def harmonic_transfer(self, wave_number: float, omega: float) -> complex:
        """Return W/S for exp(i*k*x - i*omega*t)."""
        self.validate_domain()
        detuning = omega - self.velocity * wave_number
        return self.coupling / complex(1.0, -self.tau * detuning)

    def source_free_energy_ratio(self, elapsed: float) -> float:
        """E(t)/E(0) for E = integral W^2/2 on a periodic domain."""
        self.validate_domain()
        if elapsed < 0.0:
            raise ValueError("elapsed time must be non-negative")
        return math.exp(-2.0 * elapsed / self.tau)


def assert_close(actual: complex | float, expected: complex | float, label: str) -> None:
    error = abs(actual - expected)
    scale = max(1.0, abs(expected))
    if error > TOL * scale:
        raise AssertionError(f"{label}: error {error:.3e} exceeds tolerance")


def positive_controls() -> dict[str, float]:
    model = RelaxationTemplate(tau=2.5, velocity=0.4, coupling=0.7)
    model.validate_domain()

    eigenvalue = model.source_free_eigenvalue(wave_number=3.0)
    assert_close(eigenvalue.real, -0.4, "source-free decay rate")
    assert_close(eigenvalue.imag, -1.2, "advective phase rate")

    static = model.harmonic_transfer(wave_number=0.0, omega=0.0)
    assert_close(static, model.coupling, "static response")

    resonant_advection = model.harmonic_transfer(wave_number=3.0, omega=1.2)
    assert_close(resonant_advection, model.coupling, "comoving static response")

    detuning = 10.0
    high_frequency = model.harmonic_transfer(wave_number=0.0, omega=detuning)
    expected_gain = abs(model.coupling) / math.sqrt(1.0 + (model.tau * detuning) ** 2)
    assert_close(abs(high_frequency), expected_gain, "high-frequency attenuation")

    elapsed = 4.0
    energy_ratio = model.source_free_energy_ratio(elapsed)
    assert_close(energy_ratio, math.exp(-2.0 * elapsed / model.tau), "energy decay")

    pole_frequency = model.velocity * 3.0 - 1j / model.tau
    dispersion_residual = 1.0 - 1j * model.tau * (
        pole_frequency - model.velocity * 3.0
    )
    assert_close(dispersion_residual, 0.0j, "dispersion pole")

    return {
        "decay_rate": eigenvalue.real,
        "characteristic_speed": model.velocity,
        "static_gain": abs(static),
        "high_frequency_gain": abs(high_frequency),
        "energy_ratio": energy_ratio,
    }


def negative_controls() -> int:
    invalid = (
        RelaxationTemplate(tau=0.0, velocity=0.1, coupling=1.0),
        RelaxationTemplate(tau=-1.0, velocity=0.1, coupling=1.0),
        RelaxationTemplate(tau=1.0, velocity=1.01, coupling=1.0),
    )
    failures_caught = 0
    for model in invalid:
        try:
            model.validate_domain()
        except ValueError:
            failures_caught += 1
    if failures_caught != len(invalid):
        raise AssertionError("negative controls did not all fail")
    return failures_caught


def main() -> None:
    values = positive_controls()
    failures_caught = negative_controls()

    print("WAK-001 relaxation-template audit")
    for key, value in values.items():
        print(f"{key}: {value:.12g}")
    print(f"negative_controls_caught: {failures_caught}")
    print("PASS_WAK001_RELAXATION_TEMPLATE_MATH")
    print("WAK-001 gate: OPEN")
    print("Physical wake law: NOT_YET_DERIVED")


if __name__ == "__main__":
    main()
