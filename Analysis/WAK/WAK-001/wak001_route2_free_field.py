#!/usr/bin/env python3
"""WAK-001 Route-II free-field template audit.

This tests a local preferred-frame quadratic calculation family with J_W = 0.
It is not a derived ITSM wake action and does not establish a physical wake.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class FreeWakeParameters:
    kinetic: float
    speed_sq: float
    mass_sq: float

    def validate(self) -> None:
        values = (self.kinetic, self.speed_sq, self.mass_sq)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("all parameters must be finite")
        if self.kinetic <= 0.0:
            raise ValueError("kinetic coefficient must be strictly positive")
        if self.speed_sq < 0.0:
            raise ValueError("negative speed squared is a gradient instability")
        if self.speed_sq > 1.0:
            raise ValueError("characteristic lies outside the declared matter cone")
        if self.mass_sq < 0.0:
            raise ValueError("negative mass squared is outside the stable template domain")

    def omega_sq(self, wave_number: float) -> float:
        self.validate()
        if not math.isfinite(wave_number):
            raise ValueError("wave number must be finite")
        return self.speed_sq * wave_number**2 + self.mass_sq / self.kinetic

    def hamiltonian_density(
        self,
        field: float,
        time_derivative: float,
        gradient_norm: float,
    ) -> float:
        self.validate()
        return (
            0.5 * self.kinetic * time_derivative**2
            + 0.5 * self.kinetic * self.speed_sq * gradient_norm**2
            + 0.5 * self.mass_sq * field**2
        )

    def static_susceptibility(self, wave_number: float) -> float:
        """Return W_k/J_k for the linear static sourced equation."""
        self.validate()
        denominator = self.kinetic * self.speed_sq * wave_number**2 + self.mass_sq
        if denominator <= 0.0:
            raise ValueError("static zero mode is not invertible in this template")
        return 1.0 / denominator


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def expect_invalid(parameters: FreeWakeParameters) -> bool:
    try:
        parameters.validate()
    except ValueError:
        return True
    return False


def main() -> None:
    args = parse_args()
    parameters = FreeWakeParameters(kinetic=1.2, speed_sq=0.36, mass_sq=0.8)
    parameters.validate()

    wave_numbers = (0.0, 0.5, 1.0, 2.0, 10.0)
    dispersion = [
        {"wave_number": k, "omega_sq": parameters.omega_sq(k)}
        for k in wave_numbers
    ]
    dispersion_positive = all(item["omega_sq"] > 0.0 for item in dispersion)

    energy_samples = (
        parameters.hamiltonian_density(0.0, 0.0, 0.0),
        parameters.hamiltonian_density(1.0, 0.0, 0.0),
        parameters.hamiltonian_density(0.0, 1.0, 0.0),
        parameters.hamiltonian_density(0.0, 0.0, 1.0),
        parameters.hamiltonian_density(0.7, -0.4, 1.3),
    )
    energy_nonnegative = all(value >= 0.0 for value in energy_samples)
    nontrivial_energy_positive = all(value > 0.0 for value in energy_samples[1:])

    susceptibility = [
        {"wave_number": k, "response": parameters.static_susceptibility(k)}
        for k in wave_numbers
    ]
    susceptibility_finite = all(
        math.isfinite(item["response"]) and item["response"] > 0.0
        for item in susceptibility
    )

    invalid_cases = {
        "zero_kinetic": FreeWakeParameters(0.0, 0.36, 0.8),
        "ghost_kinetic": FreeWakeParameters(-1.0, 0.36, 0.8),
        "gradient_instability": FreeWakeParameters(1.2, -0.01, 0.8),
        "acausal_characteristic": FreeWakeParameters(1.2, 1.01, 0.8),
        "tachyonic_mass": FreeWakeParameters(1.2, 0.36, -0.01),
    }
    negative_controls = {
        name: expect_invalid(candidate) for name, candidate in invalid_cases.items()
    }

    checks = {
        "dispersion_positive": dispersion_positive,
        "hamiltonian_nonnegative": energy_nonnegative,
        "nontrivial_energy_positive": nontrivial_energy_positive,
        "characteristic_inside_matter_cone": 0.0 <= parameters.speed_sq <= 1.0,
        "static_susceptibility_finite": susceptibility_finite,
        **{f"negative_{name}_rejected": passed for name, passed in negative_controls.items()},
    }
    all_ok = all(checks.values())
    status = (
        "PASS_WAK001_ROUTE2_FREE_TEMPLATE"
        if all_ok
        else "FAIL_WAK001_ROUTE2_FREE_TEMPLATE"
    )

    summary = {
        "gate": "WAK-001",
        "stage": "Stage 2 Route-II free-field screen",
        "label": "mathematical-template-only",
        "status": status,
        "calculation_pass": all_ok,
        "physics_pass": False,
        "physical_wake_law": "NOT_YET_DERIVED",
        "source": "J_W=0",
        "parameters": asdict(parameters),
        "dispersion": dispersion,
        "energy_samples": list(energy_samples),
        "static_susceptibility": susceptibility,
        "checks": checks,
        "scientific_boundary": (
            "Local frozen preferred-frame free-field template only. No metric/frame "
            "variation, interaction-derived exchange, dissipation, UVIR mode inventory, "
            "AQUAL correction, lensing, galaxy, cluster or anisotropy claim."
        ),
        "next": [
            "derive metric and preferred-frame variation from one declared trial action",
            "compare the W mode against the Phi, U and psi mode inventory",
            "retain J_W=0 until the free mode avoids duplication",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "wak001_route2_free_field_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("WAK-001 Route-II free-field template audit")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("WAK-001 gate: OPEN")
    print("Physical wake law: NOT_YET_DERIVED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
