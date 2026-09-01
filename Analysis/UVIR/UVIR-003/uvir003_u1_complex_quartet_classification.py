#!/usr/bin/env python3
"""Fail-closed U1 classification from sealed UVIR-003 transfer evidence.

This script does not reinterpret a numerical PASS as a physics pass. It checks
the already executable reduced-system outputs, records their hashes, applies
the preregistered U1 kill criterion, and writes a deterministic summary and
human-readable report.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
import sympy


BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs" / "u1_classification"
INPUTS = {
    "mode_resolved": BASE / "outputs" / "uvir003_mode_resolved_transfer_robustness_summary.json",
    "source_response": BASE / "outputs" / "uvir003_source_observable_retarded_response_summary.json",
    "adiabaticity": BASE / "outputs" / "uvir003_propagator_adiabaticity_transfer_summary.json",
    "background": BASE / "outputs" / "uvir003_frw_background_summary.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    data = {name: load(path) for name, path in INPUTS.items()}
    mode_cases = data["mode_resolved"]["case_results"]
    source_cases = data["source_response"]["case_results"]
    assert len(mode_cases) == 5 and len(source_cases) == 5
    assert all(c["numerical_status"] == "PASS_TRANSFER_AND_PAIR_ASSIGNMENT" for c in mode_cases)
    assert all(c["off_axis_complex_quartet_time_fraction"] > 0 for c in mode_cases)
    assert all(c["maximum_retained_matter_input_subspace_gain"] > 1 for c in mode_cases)
    assert all(c["response_status"] == "GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_QUARTET" for c in source_cases)

    baseline = next(c for c in mode_cases if c["case"] == "baseline")
    source = next(c for c in source_cases if c["case"] == "baseline")
    ceiling = 1.0 / source["maximum_gauge_projected_matter_response"]
    summary = {
        "audit": "UVIR-003_U1_CONTROLLED_COMPLEX_QUARTET_CLASSIFICATION",
        "calculation_status": "PASS_REPRODUCIBLE_CLASSIFICATION_PIPELINE",
        "physics_status": "HOLD_TIER1_CLOSURE",
        "u1_disposition": "FREEZE_UNCONTROLLED_LINEAR_RESPONSE_ON_DECLARED_BACKGROUND",
        "classification": "UNRESOLVED_BACKGROUND_PATHOLOGY_OR_UNCONTROLLED_RESPONSE",
        "not_classified_as": [
            "controlled_physical_Jeans_like_growth",
            "chart_or_gauge_artifact",
            "global_ITSM_no_go_theorem",
        ],
        "evidence": {
            "tested_cases": len(mode_cases),
            "all_cases_contain_off_axis_quartet": True,
            "baseline_quartet_time_fraction": baseline["off_axis_complex_quartet_time_fraction"],
            "baseline_quartet_interval_t": [source["quartet_start_t"], source["quartet_end_t"]],
            "baseline_quartet_interval_q_over_H": [source["quartet_start_q_over_H"], source["quartet_end_q_over_H"]],
            "baseline_full_transfer_gain": baseline["maximum_full_transfer_gain"],
            "baseline_matter_seeded_gain": baseline["maximum_retained_matter_input_subspace_gain"],
            "baseline_gauge_projected_matter_response": source["maximum_gauge_projected_matter_response"],
            "normalization_specific_linearity_ceiling": ceiling,
            "minimum_kinetic_eigenvalue": min(c["minimum_kinetic_eigenvalue"] for c in mode_cases),
            "maximum_pairing_residual": max(c["tracking_diagnostics"]["maximum_pairing_residual"] for c in mode_cases),
            "maximum_time_orbit_annihilation_residual": max(c["maximum_time_orbit_annihilation_residual"] for c in source_cases),
        },
        "interpretation": {
            "high_q_principal_sector": "real/hyperbolic in the existing control; finite-q quartet is not by itself proof of PDE non-hyperbolicity",
            "gauge_statement": "projected Q_rho/Q_chi source and readout retain the amplified response while the time-orbit residual remains numerical-small",
            "energy_statement": "positive reduced kinetic eigenvalues do not supply the missing signed Hamiltonian-energy/Krein classification",
            "backreaction_statement": "the normalization-specific ceiling is not a cosmological amplitude bound; it shows the declared linear calculation cannot control generic larger normalized sources",
        },
        "missing_for_promotion": [
            "dimensionful calibrated background and physical parameter domain",
            "signed Hamiltonian-energy/Krein classification through the quartet",
            "nonlinear backreaction evolution",
            "independent derivation and verification of the full reduced action",
        ],
        "input_sha256": {name: sha256(path) for name, path in INPUTS.items()},
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sympy.__version__,
        },
        "boundary": "This is a bounded dimensionless representative-background result. It freezes U1 under the uncontrolled-response kill criterion but does not reject every ITSM action or background.",
    }
    summary_path = OUT / "uvir003_u1_complex_quartet_classification_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# UVIR-003 U1 controlled complex-quartet classification

**Calculation status:** `PASS_REPRODUCIBLE_CLASSIFICATION_PIPELINE`  
**Physics status:** `HOLD_TIER1_CLOSURE`  
**U1 disposition:** `FREEZE_UNCONTROLLED_LINEAR_RESPONSE_ON_DECLARED_BACKGROUND`

## Result

All five tested on-shell, dimensionless neighboring cases contain an off-axis
complex quartet and amplify retained-matter input. In the baseline case the
quartet occupies t={source['quartet_start_t']:.2f} to {source['quartet_end_t']:.2f}; the full transfer gain is
{baseline['maximum_full_transfer_gain']:.6e}, the retained-matter-input gain is
{baseline['maximum_retained_matter_input_subspace_gain']:.6e}, and a source/readout projected onto
Q_rho/Q_chi retains response {source['maximum_gauge_projected_matter_response']:.6e}.

The corresponding normalization-specific linearity ceiling is {ceiling:.6e}.
This is not a physical cosmological amplitude bound. It is evidence that the
declared linear evolution does not control generic normalized sources above
that level without a nonlinear backreaction calculation.

## Classification

The quartet is not classified as controlled Jeans growth: its signed
Hamiltonian-energy/Krein character, calibrated physical timescale, and
nonlinear saturation are missing. It is not classified as a gauge/chart
artifact because the gauge-projected matter response survives and the
time-orbit annihilation residual is small. The high-q real control means the
finite-q quartet alone is not proof of PDE non-hyperbolicity.

The only defensible bounded verdict is
`UNRESOLVED_BACKGROUND_PATHOLOGY_OR_UNCONTROLLED_RESPONSE`. U1 is frozen by
the preregistered uncontrolled-backreaction criterion. This is not a global
no-go theorem for every ITSM action or background.

## Environment caveat

The runtime versions are recorded in the JSON. The live `itsm_env` package
set differs from the dirty `environment.yml` NumPy pin, so the environment is
recorded but not claimed to be an exact lockfile reproduction.
"""
    report_path = OUT / "UVIR-003_U1_COMPLEX_QUARTET_CLASSIFICATION.md"
    report_path.write_text(report, encoding="utf-8")
    seals = "\n".join(f"{sha256(p)}  {p.name}" for p in (summary_path, report_path)) + "\n"
    (OUT / "uvir003_u1_complex_quartet_classification.sha256").write_text(seals, encoding="ascii")
    print(json.dumps({"summary": str(summary_path), "report": str(report_path), "disposition": summary["u1_disposition"]}, indent=2))


if __name__ == "__main__":
    main()
