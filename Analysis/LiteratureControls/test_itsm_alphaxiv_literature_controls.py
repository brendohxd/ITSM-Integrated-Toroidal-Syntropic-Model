#!/usr/bin/env python3
"""Reproducible literature controls for R4C1 and CBR-001.

This executable implements the frozen contract in
Theory/Verification/ITSM_ALPHAXIV_LITERATURE_CONTROLS_CONTRACT_2026-09-30.md.
It is a control calculation only and cannot promote a physics gate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import platform
import sys
import warnings
from pathlib import Path
from typing import Any, Callable, Sequence

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import IntegrationWarning, quad


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = Path(
    "Theory/Verification/"
    "ITSM_ALPHAXIV_LITERATURE_CONTROLS_CONTRACT_2026-09-30.md"
)
CBR_MODULE = Path("Analysis/Casimir/CBR-001/casimir_t3_lattice.py")
OUTPUT_ROOT = Path("Analysis/LiteratureControls/outputs")

PINNED_INPUTS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md": (
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3"
    ),
    "Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md": (
        "3019196b071b146a1e41cd055073ae02da2afa10b1cdb5ae49e0a63cf84a6eb6"
    ),
    "Theory/Gates/RES-001/RES001_R4C1_G3_DENSITY_ACTION_REPORT_2026-09-30.md": (
        "8a1c2245fc02307c5e70c7b4c1064872e82464c4c411d3095e97575c730b1876"
    ),
    "Analysis/Casimir/CBR-001/casimir_t3_lattice.py": (
        "5f0515fab37cdfc0de837bcbc36011260815c5275dc6755a3226144811f04b87"
    ),
    "Analysis/Casimir/CBR-001/README.md": (
        "6b5122e9b59c671fd0f88e4c990b344cc2d9569e01279516363a7135ba633b65"
    ),
    str(CONTRACT).replace("\\", "/"): (
        "85d817fb8583305437e6c3bfebe2650f1a726461205d27048109f623ca878c77"
    ),
}

CUTOFFS = (20, 30, 40, 60, 80, 120)
GEOMETRIES = (
    (1.0, 1.0, 1.0),
    (1.0, 1.25, 1.25),
    (1.0, 1.0, 2.0),
    (0.8, 1.1, 1.4),
)

RHO_REL_TOL = 2.0e-4
PRESSURE_NORM_TOL = 5.0e-4
TRACE_REL_TOL = 5.0e-5
SYMMETRY_REL_TOL = 5.0e-5
SCALE = 1.7
FD_RELATIVE_STEP = 2.0e-4
THETA_TERM_TOL = 1.0e-16


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    return (text + "\n").encode("utf-8")


def verify_pins() -> dict[str, str]:
    actual: dict[str, str] = {}
    failures: list[str] = []
    for relative, expected in PINNED_INPUTS.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing: {relative}")
            continue
        observed = sha256_file(path)
        actual[relative] = observed
        if observed != expected:
            failures.append(
                f"hash mismatch: {relative}: expected {expected}, observed {observed}"
            )
    if failures:
        raise RuntimeError("Input provenance failure:\n" + "\n".join(failures))
    return actual


def load_cbr_module() -> Any:
    path = ROOT / CBR_MODULE
    spec = importlib.util.spec_from_file_location("itsm_cbr001_lattice", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load CBR module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def theta_zero(x: float) -> float:
    """Return sum_{n in Z} exp(-x n^2), using the Jacobi transform as needed."""
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("theta argument must be finite and positive")

    if x >= math.pi:
        exponent_scale = x
        prefactor = 1.0
    else:
        exponent_scale = math.pi * math.pi / x
        prefactor = math.sqrt(math.pi / x)

    if exponent_scale >= -math.log(THETA_TERM_TOL):
        tail = 0.0
    else:
        max_index = int(
            math.ceil(math.sqrt(-math.log(THETA_TERM_TOL) / exponent_scale))
        )
        tail = math.fsum(
            math.exp(-exponent_scale * index * index)
            for index in range(1, max_index + 1)
        )
    return prefactor * (1.0 + 2.0 * tail)


def heat_kernel_s4(lengths: Sequence[float]) -> tuple[float, dict[str, float]]:
    side = tuple(float(value) for value in lengths)
    if len(side) != 3 or not all(math.isfinite(x) and x > 0.0 for x in side):
        raise ValueError("three finite positive side lengths are required")
    volume = math.prod(side)

    def small_integrand(y: float) -> float:
        if y == 0.0:
            return 2.0 * math.pi ** 1.5 / volume
        t = y * y
        product = math.prod(theta_zero(length * length * t) for length in side)
        return 2.0 * y**3 * (product - 1.0)

    def large_integrand(t: float) -> float:
        product = math.prod(theta_zero(length * length * t) for length in side)
        return t * (product - 1.0)

    with warnings.catch_warnings():
        warnings.simplefilter("error", IntegrationWarning)
        small, small_error = quad(
            small_integrand,
            0.0,
            1.0,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=300,
        )
        large, large_error = quad(
            large_integrand,
            1.0,
            math.inf,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=300,
        )
    value = small + large
    if not math.isfinite(value) or value <= 0.0:
        raise RuntimeError(f"invalid heat-kernel S4 result: {value!r}")
    return value, {
        "large_interval_error_estimate": float(large_error),
        "small_interval_error_estimate": float(small_error),
    }


def heat_energy(lengths: Sequence[float]) -> tuple[float, float, dict[str, float]]:
    side = tuple(float(value) for value in lengths)
    s4, diagnostics = heat_kernel_s4(side)
    rho = -s4 / (2.0 * math.pi * math.pi)
    return math.prod(side) * rho, rho, diagnostics


def richardson_derivative(
    function: Callable[[float], float],
    center: float,
    relative_step: float,
) -> tuple[float, dict[str, float]]:
    step = center * relative_step

    def central(h: float) -> float:
        return (function(center + h) - function(center - h)) / (2.0 * h)

    coarse = central(step)
    fine = central(step / 2.0)
    extrapolated = (4.0 * fine - coarse) / 3.0
    return extrapolated, {
        "central_coarse": coarse,
        "central_fine": fine,
        "richardson_delta": abs(extrapolated - fine),
        "step": step,
    }


def heat_stress(lengths: Sequence[float]) -> dict[str, Any]:
    side = tuple(float(value) for value in lengths)
    energy, rho, integral_diagnostics = heat_energy(side)
    volume = math.prod(side)
    pressures: list[float] = []
    derivative_diagnostics: list[dict[str, float]] = []

    for axis in range(3):
        def energy_at_axis(value: float, axis: int = axis) -> float:
            changed = list(side)
            changed[axis] = value
            return heat_energy(changed)[0]

        derivative, diagnostics = richardson_derivative(
            energy_at_axis,
            side[axis],
            FD_RELATIVE_STEP,
        )
        area = volume / side[axis]
        pressures.append(-derivative / area)
        derivative_diagnostics.append(diagnostics)

    trace = -rho + math.fsum(pressures)
    return {
        "energy": energy,
        "integral_diagnostics": integral_diagnostics,
        "lengths": list(side),
        "pressure_derivative_diagnostics": derivative_diagnostics,
        "pressures": pressures,
        "rho": rho,
        "trace": trace,
    }


def direct_stress(module: Any, lengths: Sequence[float]) -> dict[str, Any]:
    samples = [module.lattice_stress(lengths, cutoff) for cutoff in CUTOFFS]
    observables = {
        "rho": [sample.rho for sample in samples],
        "p1": [sample.p1 for sample in samples],
        "p2": [sample.p2 for sample in samples],
        "p3": [sample.p3 for sample in samples],
    }
    extrapolated: dict[str, float] = {}
    coefficients: dict[str, list[float]] = {}
    for name, values in observables.items():
        limit, fit = module.extrapolate_to_infinity(CUTOFFS, values, order=2)
        extrapolated[name] = limit
        coefficients[name] = [float(value) for value in fit]
    pressures = [
        extrapolated["p1"],
        extrapolated["p2"],
        extrapolated["p3"],
    ]
    return {
        "cutoffs": list(CUTOFFS),
        "fit_coefficients_constant_1_over_n_1_over_n2": coefficients,
        "lengths": [float(value) for value in lengths],
        "pressures": pressures,
        "rho": extrapolated["rho"],
        "sample_values": observables,
        "trace": -extrapolated["rho"] + math.fsum(pressures),
    }


def relative_error(observed: float, expected: float, floor: float = 1.0e-14) -> float:
    return abs(observed - expected) / max(abs(expected), floor)


def make_check(
    identifier: str,
    observed: Any,
    threshold: Any,
    passed: bool,
    description: str,
) -> dict[str, Any]:
    return {
        "description": description,
        "id": identifier,
        "observed": observed,
        "passed": bool(passed),
        "threshold": threshold,
    }


def symbolic_density_control() -> dict[str, Any]:
    a, M, H, rho_c, k = sp.symbols("a M H rho_c k", positive=True, finite=True)
    omega_term = rho_c / (M**2 * H**2)
    k11_uncoupled = a**2 * M**2 * H**2 * omega_term / 2
    converted = sp.simplify(2 * a**3 * k11_uncoupled / k**2)
    target = a**5 * rho_c / k**2
    residual = sp.simplify(converted - target)
    return {
        "aoki_action_overall_half": False,
        "aoki_variable": "delta_c/k",
        "converted_K_D": str(converted),
        "exact_residual": str(residual),
        "interaction_extension": (
            "a**5*M**2*H**2*(3*Omega_c + alpha_m2 - alpha_bar_m1**2)/k**2"
        ),
        "passed": residual == 0,
        "r4c1_target_K_D": str(target),
    }


def compute_payloads() -> tuple[dict[str, Any], dict[str, Any]]:
    input_hashes = verify_pins()
    cbr = load_cbr_module()
    symbolic = symbolic_density_control()
    checks: list[dict[str, Any]] = [
        make_check(
            "AOKI_UNCOUPLED_DUST_NORMALIZATION",
            symbolic["exact_residual"],
            "exactly 0",
            symbolic["passed"],
            "Convention conversion reproduces K_D=a^5 rho_c/k^2 exactly.",
        )
    ]

    comparisons: list[dict[str, Any]] = []
    heat_by_geometry: dict[tuple[float, float, float], dict[str, Any]] = {}
    for index, geometry in enumerate(GEOMETRIES, start=1):
        heat = heat_stress(geometry)
        direct = direct_stress(cbr, geometry)
        heat_by_geometry[geometry] = heat
        rho_discrepancy = relative_error(direct["rho"], heat["rho"])
        pressure_discrepancies = [
            abs(direct_value - heat_value)
            / max(abs(heat_value), abs(heat["rho"]), 1.0e-14)
            for direct_value, heat_value in zip(direct["pressures"], heat["pressures"])
        ]
        trace_relative = abs(heat["trace"]) / max(abs(heat["rho"]), 1.0e-14)
        checks.append(
            make_check(
                f"CBR_G{index}_RHO_METHOD_AGREEMENT",
                rho_discrepancy,
                RHO_REL_TOL,
                rho_discrepancy <= RHO_REL_TOL,
                f"Direct-lattice and heat-kernel rho agree for {geometry}.",
            )
        )
        for axis, discrepancy in enumerate(pressure_discrepancies, start=1):
            checks.append(
                make_check(
                    f"CBR_G{index}_P{axis}_METHOD_AGREEMENT",
                    discrepancy,
                    PRESSURE_NORM_TOL,
                    discrepancy <= PRESSURE_NORM_TOL,
                    f"Direct and energy-derivative p{axis} agree for {geometry}.",
                )
            )
        checks.append(
            make_check(
                f"CBR_G{index}_HEAT_TRACE",
                trace_relative,
                TRACE_REL_TOL,
                trace_relative <= TRACE_REL_TOL,
                f"Heat-kernel stress is traceless for {geometry}.",
            )
        )
        comparisons.append(
            {
                "direct_lattice": direct,
                "geometry_id": index,
                "heat_kernel": heat,
                "pressure_normalized_discrepancies": pressure_discrepancies,
                "rho_relative_discrepancy": rho_discrepancy,
                "trace_relative": trace_relative,
            }
        )

    cube = heat_by_geometry[GEOMETRIES[0]]
    cube_pressure_spread = (
        max(cube["pressures"]) - min(cube["pressures"])
    ) / max(abs(cube["rho"]), 1.0e-14)
    cube_equation_errors = [
        relative_error(pressure, cube["rho"] / 3.0)
        for pressure in cube["pressures"]
    ]
    checks.extend(
        [
            make_check(
                "CBR_CUBE_PRESSURE_EQUALITY",
                cube_pressure_spread,
                SYMMETRY_REL_TOL,
                cube_pressure_spread <= SYMMETRY_REL_TOL,
                "Cube directional pressures are equal.",
            ),
            make_check(
                "CBR_CUBE_EQUATION_OF_STATE",
                max(cube_equation_errors),
                SYMMETRY_REL_TOL,
                max(cube_equation_errors) <= SYMMETRY_REL_TOL,
                "Each cube pressure equals rho/3.",
            ),
        ]
    )

    base_geometry = GEOMETRIES[-1]
    base = heat_by_geometry[base_geometry]
    permutation = (base_geometry[2], base_geometry[0], base_geometry[1])
    permuted = heat_stress(permutation)
    expected_permuted_pressures = [
        base["pressures"][2],
        base["pressures"][0],
        base["pressures"][1],
    ]
    permutation_rho_error = relative_error(permuted["rho"], base["rho"])
    permutation_pressure_errors = [
        relative_error(observed, expected)
        for observed, expected in zip(
            permuted["pressures"], expected_permuted_pressures
        )
    ]
    checks.append(
        make_check(
            "CBR_PERMUTATION_COVARIANCE",
            {
                "max_pressure_relative_error": max(permutation_pressure_errors),
                "rho_relative_error": permutation_rho_error,
            },
            SYMMETRY_REL_TOL,
            max([permutation_rho_error, *permutation_pressure_errors])
            <= SYMMETRY_REL_TOL,
            "Permuting lengths permutes pressures and preserves rho.",
        )
    )

    scaled_geometry = tuple(SCALE * value for value in base_geometry)
    scaled = heat_stress(scaled_geometry)
    scaling_factor = SCALE**-4
    scaling_rho_error = relative_error(
        scaled["rho"], base["rho"] * scaling_factor
    )
    scaling_pressure_errors = [
        relative_error(observed, expected * scaling_factor)
        for observed, expected in zip(scaled["pressures"], base["pressures"])
    ]
    checks.append(
        make_check(
            "CBR_LENGTH_SCALING",
            {
                "max_pressure_relative_error": max(scaling_pressure_errors),
                "rho_relative_error": scaling_rho_error,
            },
            SYMMETRY_REL_TOL,
            max([scaling_rho_error, *scaling_pressure_errors])
            <= SYMMETRY_REL_TOL,
            "Scaling all lengths by 1.7 scales the stress by lambda^-4.",
        )
    )

    control_pass = all(check["passed"] for check in checks)
    script_relative = Path(__file__).resolve().relative_to(ROOT).as_posix()
    summary = {
        "checks": checks,
        "comparisons": comparisons,
        "control_pass": control_pass,
        "exclusions": [
            "No R4C1-to-Aoki interacting-operator dictionary is derived.",
            "No full R4C1 kinetic, gradient, constraint, or all-scale stability claim is made.",
            "The state-dependent isotropic torus zero mode is not fixed by this control.",
            "The minimally coupled scalar terms in arXiv:2603.12319 are outside this conformal-scalar benchmark.",
            "No anisotropic dynamical backreaction, observational fit, gate promotion, or publication-readiness claim is made.",
        ],
        "gate_promotion": "NONE",
        "input_hashes": input_hashes,
        "method": {
            "direct_cutoffs": list(CUTOFFS),
            "direct_extrapolation": "constant + 1/N + 1/N^2 least-squares fit",
            "heat_kernel": "Mellin integral with Jacobi transform and adaptive quadrature",
            "pressure": "energy derivative, central differences and one Richardson extrapolation",
        },
        "permutation_control": {
            "base": base,
            "expected_permuted_pressures": expected_permuted_pressures,
            "permutation": list(permutation),
            "permuted": permuted,
        },
        "physics_closure_claimed": False,
        "provenance": {
            "contract": CONTRACT.as_posix(),
            "external_sources": [
                {
                    "arxiv": "2504.17293v2",
                    "control": "uncoupled dust-density normalization and interaction-basis comparison",
                    "title": "Effective field theory of coupled dark energy and dark matter",
                },
                {
                    "arxiv": "2603.12319",
                    "control": "nonzero-mode conformal-scalar rectangular-T3 stress",
                    "title": "Quantum Signatures of Cosmic Topology: How Casimir Backreaction Transmits Isotropy Violation",
                },
            ],
            "script": script_relative,
            "script_sha256": sha256_file(Path(__file__).resolve()),
        },
        "result_classification": (
            "PASS_CONTROL_ONLY" if control_pass else "FAIL_CONTROL"
        ),
        "scaling_control": {
            "base": base,
            "scale": SCALE,
            "scaled": scaled,
            "scaled_geometry": list(scaled_geometry),
        },
        "schema": "itsm-alphaxiv-literature-controls-v1",
        "symbolic_density_control": symbolic,
        "tolerances": {
            "pressure_normalized": PRESSURE_NORM_TOL,
            "rho_relative": RHO_REL_TOL,
            "symmetry_relative": SYMMETRY_REL_TOL,
            "trace_relative": TRACE_REL_TOL,
        },
        "toolchain": {
            "numpy": np.__version__,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
    }

    formulas = {
        "aoki_2504.17293v2": {
            "action_convention": "quadratic action written without an overall 1/2",
            "converted_density_kinetic_coefficient": (
                "K_D = 2*a^3*K_11/k^2 = a^5*M^2*H^2*"
                "(3*Omega_c + alpha_m2 - alpha_bar_m1^2)/k^2"
            ),
            "dark_matter_variable": "delta_c/k",
            "k11": (
                "a^2*M^2*H^2*(3*Omega_c + alpha_m2 - alpha_bar_m1^2)/2"
            ),
            "uncoupled_dust_substitution": "3*Omega_c = rho_c/(M^2*H^2)",
        },
        "negro_2603.12319": {
            "conformal_nonzero_mode_pressure": (
                "p_i=(1/(2*pi^2))*sum[(R_n^2-4*L_i^2*n_i^2)/R_n^6]"
            ),
            "conformal_nonzero_mode_rho": (
                "rho=-(1/(2*pi^2))*sum[R_n^-4]"
            ),
            "de_sitter_scaling": "H^4*eta^4 = a^-4",
            "zero_mode": "state-dependent isotropic term excluded from this benchmark",
        },
        "r4c1": {
            "density_kinetic_coefficient": "K_D=a^5*rho_m/k^2",
            "exchange_identities": [
                "nabla_mu T_m^(mu nu)=Q_mp^nu",
                "nabla_mu T_P^(mu nu)=-Q_mp^nu+Q_syn^nu",
                "nabla_mu T_R^(mu nu)=-Q_syn^nu",
            ],
        },
        "schema": "itsm-alphaxiv-literature-formulas-v1",
    }
    return summary, formulas


def sidecar_bytes(filename: str, data: bytes) -> bytes:
    return f"{sha256_bytes(data)}  {filename}\n".encode("ascii")


def write_first_run(output_directory: Path, payloads: dict[str, bytes]) -> None:
    output_directory.mkdir(parents=True, exist_ok=False)
    for filename, data in payloads.items():
        path = output_directory / filename
        path.write_bytes(data)
        (output_directory / f"{filename}.sha256").write_bytes(
            sidecar_bytes(filename, data)
        )


def replay(output_directory: Path, payloads: dict[str, bytes]) -> list[str]:
    failures: list[str] = []
    for filename, expected in payloads.items():
        path = output_directory / filename
        sidecar = output_directory / f"{filename}.sha256"
        if not path.is_file():
            failures.append(f"missing receipt: {path}")
            continue
        observed = path.read_bytes()
        if observed != expected:
            failures.append(f"byte mismatch: {path}")
        expected_sidecar = sidecar_bytes(filename, observed)
        if not sidecar.is_file():
            failures.append(f"missing sidecar: {sidecar}")
        elif sidecar.read_bytes() != expected_sidecar:
            failures.append(f"sidecar mismatch: {sidecar}")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--attempt",
        default="01",
        help="new immutable attempt suffix (default: 01)",
    )
    group.add_argument(
        "--replay",
        type=Path,
        help="recompute and compare against an existing attempt without writing",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary, formulas = compute_payloads()
    payloads = {
        "formulas.json": canonical_json_bytes(formulas),
        "summary.json": canonical_json_bytes(summary),
    }

    if args.replay is not None:
        output_directory = (
            args.replay if args.replay.is_absolute() else ROOT / args.replay
        )
        failures = replay(output_directory, payloads)
        result = {
            "control_pass": summary["control_pass"],
            "mode": "replay",
            "receipt_byte_match": not failures,
            "replay_failures": failures,
        }
        print(json.dumps(result, allow_nan=False, sort_keys=True))
        return 0 if summary["control_pass"] and not failures else 1

    output_directory = ROOT / OUTPUT_ROOT / f"alphaxiv_controls_attempt_{args.attempt}"
    write_first_run(output_directory, payloads)
    result = {
        "checks_passed": sum(check["passed"] for check in summary["checks"]),
        "checks_total": len(summary["checks"]),
        "control_pass": summary["control_pass"],
        "mode": "first_run",
        "output_directory": output_directory.relative_to(ROOT).as_posix(),
        "result_classification": summary["result_classification"],
    }
    print(json.dumps(result, allow_nan=False, sort_keys=True))
    return 0 if summary["control_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
