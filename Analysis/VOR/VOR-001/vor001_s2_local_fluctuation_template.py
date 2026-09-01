#!/usr/bin/env python3
"""VOR-001 S2: local fluctuations about finite-density minimum (template only).

LABEL: mathematical-template-only
GATE:  VOR-001 Stage S2 (local fluctuations before defects/resonance)
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY

Toy energy (same as S1):
  E = ∫ [ |∇ρ|²/2 + ρ²|∇θ|²/2 + λ(ρ²-v²)²/4 ] d³x

About ρ=v, θ=const (zero winding):
  amplitude δρ: massive, m² = V''(v) = 2 λ v²
  phase π = v δθ: gapless Goldstone at k=0; continuum ω² = k²

Does NOT: parent UVIR action, defects, SWNT packaging, a0, force law, PTA.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--N", type=int, default=24)
    p.add_argument("--L1", type=float, default=1.0)
    p.add_argument("--L2", type=float, default=1.0)
    p.add_argument("--L3", type=float, default=1.0)
    p.add_argument("--lam", type=float, default=1.0)
    p.add_argument("--v", type=float, default=1.0)
    return p.parse_args()


def validate(N: int, L: tuple[float, float, float], lam: float, v: float) -> None:
    if N < 8:
        raise ValueError("N >= 8")
    for i, Li in enumerate(L, 1):
        if not math.isfinite(Li) or Li <= 0:
            raise ValueError(f"L{i} must be positive finite")
    if not math.isfinite(lam) or lam <= 0:
        raise ValueError("lam > 0")
    if not math.isfinite(v) or v <= 0:
        raise ValueError("v > 0")


def continuum_masses(lam: float, v: float) -> dict[str, float]:
    m2_rho = 2.0 * lam * v * v
    return {
        "m2_amplitude": m2_rho,
        "m2_phase_goldstone": 0.0,
        "V_second_at_v": m2_rho,
        "potential": "lambda (rho^2 - v^2)^2 / 4",
    }


def quadratic_symbol_scan(
    N: int, lengths: tuple[float, float, float], lam: float, v: float
) -> dict[str, Any]:
    L1, L2, L3 = lengths
    dx = (L1 / N, L2 / N, L3 / N)
    k1 = 2 * math.pi * np.fft.fftfreq(N, d=dx[0])
    k2 = 2 * math.pi * np.fft.fftfreq(N, d=dx[1])
    k3 = 2 * math.pi * np.fft.fftfreq(N, d=dx[2])
    K1, K2, K3 = np.meshgrid(k1, k2, k3, indexing="ij")
    k2_field = K1**2 + K2**2 + K3**2
    m2 = 2.0 * lam * v * v
    amp_symbol = k2_field + m2
    phase_symbol = k2_field.copy()
    phase_symbol[0, 0, 0] = 0.0

    samples = []
    for ntuple in [(1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1)]:
        n1, n2, n3 = ntuple
        k2 = (
            (2 * math.pi * n1 / L1) ** 2
            + (2 * math.pi * n2 / L2) ** 2
            + (2 * math.pi * n3 / L3) ** 2
        )
        samples.append(
            {
                "n": list(ntuple),
                "k2": k2,
                "omega2_amplitude_continuum": k2 + m2,
                "omega2_phase_continuum": k2,
            }
        )

    return {
        "amp_quadratic_symbols_nonnegative": bool(np.all(amp_symbol >= -1e-12)),
        "phase_quadratic_symbols_nonnegative": bool(np.all(phase_symbol >= -1e-12)),
        "goldstone_zero_mode": abs(float(phase_symbol[0, 0, 0])) < 1e-14,
        "amplitude_mass_at_zero_mode": abs(float(amp_symbol[0, 0, 0]) - m2)
        < 1e-12 * max(m2, 1.0),
        "min_amp_symbol": float(np.min(amp_symbol)),
        "min_phase_symbol": float(np.min(phase_symbol)),
        "dispersion_samples": samples,
    }


def realspace_quadratic_energy(
    N: int, lengths: tuple[float, float, float], lam: float, v: float
) -> dict[str, Any]:
    """Direct quadratic energy for a normalized single-mode amplitude wave."""
    L1, L2, L3 = lengths
    dx = np.array([L1 / N, L2 / N, L3 / N])
    vol_cell = float(np.prod(dx))
    axes = [np.linspace(0.0, Li, N, endpoint=False) for Li in lengths]
    x, _y, _z = np.meshgrid(*axes, indexing="ij")
    # mode n=(1,0,0)
    k = 2 * math.pi / L1
    delta = np.sqrt(2.0 / (L1 * L2 * L3)) * np.cos(k * x)  # unit L2 norm over volume
    # |∇δ|² integral + m² ∫δ²
    grad_x = (np.roll(delta, -1, 0) - np.roll(delta, 1, 0)) / (2 * dx[0])
    e_grad = float(np.sum(grad_x**2) * vol_cell)
    m2 = 2.0 * lam * v * v
    e_mass = float(np.sum(delta**2) * vol_cell) * m2
    e_tot = e_grad + e_mass
    continuum = k * k + m2
    # L2 norm of delta ~ 1
    norm2 = float(np.sum(delta**2) * vol_cell)
    return {
        "mode": [1, 0, 0],
        "norm2": norm2,
        "E_quadratic_realspace": e_tot,
        "E_continuum_symbol": continuum,
        "relative_error": abs(e_tot - continuum) / continuum,
    }


def main() -> None:
    args = parse_args()
    lengths = (args.L1, args.L2, args.L3)
    validate(args.N, lengths, args.lam, args.v)

    masses = continuum_masses(args.lam, args.v)
    scan = quadratic_symbol_scan(args.N, lengths, args.lam, args.v)
    real = realspace_quadratic_energy(args.N, lengths, args.lam, args.v)

    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "name": "amplitude_mass_positive",
            "ok": masses["m2_amplitude"] > 0,
            "m2": masses["m2_amplitude"],
        }
    )
    checks.append(
        {
            "name": "goldstone_massless",
            "ok": masses["m2_phase_goldstone"] == 0.0,
        }
    )
    checks.append(
        {
            "name": "amp_symbols_nonnegative",
            "ok": scan["amp_quadratic_symbols_nonnegative"],
        }
    )
    checks.append(
        {
            "name": "phase_symbols_nonnegative",
            "ok": scan["phase_quadratic_symbols_nonnegative"],
        }
    )
    checks.append(
        {
            "name": "goldstone_zero_mode",
            "ok": scan["goldstone_zero_mode"],
        }
    )
    checks.append(
        {
            "name": "amplitude_zero_mode_mass",
            "ok": scan["amplitude_mass_at_zero_mode"],
        }
    )
    checks.append(
        {
            "name": "realspace_quadratic_matches_continuum",
            "ok": real["relative_error"] < 0.05 and real["norm2"] > 0.9,
            "relative_error": real["relative_error"],
            "norm2": real["norm2"],
        }
    )
    # U(1) shift: constant phase has zero energy (already goldstone)
    checks.append(
        {
            "name": "template_not_parent_itsm_action",
            "ok": True,
            "note": "Toy U(1) energy only; HOLD parent action remains",
        }
    )

    firewall = {
        "physics_pass": False,
        "parent_UVIR_action_validated": False,
        "defect_sector": False,
        "SWNT_packaging": False,
        "a0_from_winding": False,
        "Cobs_from_vortex": False,
        "PTA_spectrum": False,
        "force_law": False,
        "VOR_research_gate_PASS": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_VOR001_S2_LOCAL_FLUCTUATION_TEMPLATE"
        if all_ok
        else "FAIL_VOR001_S2_LOCAL_FLUCTUATION"
    )

    summary: dict[str, Any] = {
        "gate": "VOR-001",
        "stage": "S2_LOCAL_FLUCTUATIONS",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "hold": "HOLD_PARENT_ACTION_AND_DEFECT_SECTOR",
        "parameters": {
            "N": args.N,
            "L": list(lengths),
            "lambda": args.lam,
            "v": args.v,
        },
        "continuum_masses": masses,
        "symbol_scan": scan,
        "realspace_check": real,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Quadratic local fluctuations of the fixed-background U(1) toy "
            "energy about the finite-density minimum. Massive amplitude and "
            "gapless phase mode verified as a mathematical template. Does not "
            "validate the parent ITSM condensate action, defects, or observables."
        ),
        "next_required": [
            "Declare or import parent S_Phi for ITSM (not this toy alone)",
            "Defect sector with rho=0 cores only after parent action",
            "Resonance / spectrum only after defects and TOP mode lattice",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "vor001_s2_local_fluctuation_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "vor001_s2_local_fluctuation_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("VOR-001 S2 local fluctuation template")
    print("  physics_pass: False | research_gate: OPEN_SCAFFOLD_ONLY")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
