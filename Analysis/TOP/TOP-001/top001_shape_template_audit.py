#!/usr/bin/env python3
"""TOP-001 mathematical-template-only shape / mode-lattice audit.

LABEL: mathematical-template-only
GATE:  TOP-001 (Open scaffold)
CLAIM: none Derived; physics_pass is always false

Scope (fixed rectangular T^3)
-----------------------------
1. Fix volume V = Lx*Ly*Lz and scan shape ratios.
2. Free massless scalar mode lattice:
       k(n) = 2 pi * sqrt( (n_x/Lx)^2 + (n_y/Ly)^2 + (n_z/Lz)^2 )
   for n in Z^3 \\ {0}, truncated at |n_i| <= n_max.
3. Directional second-moment diagnostic of mode directions (template only).
4. Negative control: cubic lengths => diagnostic ~ 0.
5. Refinement control: increase n_max; diagnostic stable within tolerance.

Does NOT compute Casimir sums, backreaction, 13/12, H0, a0, or C_obs.
Does NOT prefer twisted E2/E3.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


TWO_PI = 2.0 * math.pi


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--V", type=float, default=1.0, help="fixed volume")
    p.add_argument("--n-max", type=int, default=6, help="mode truncation |n_i|<=n_max")
    p.add_argument("--n-max-refined", type=int, default=10)
    return p.parse_args()


def validate_inputs(V: float, n_max: int, n_max_refined: int) -> None:
    """Reject malformed domains before constructing a mode lattice."""
    if not math.isfinite(V) or V <= 0:
        raise ValueError("V must be finite and positive")
    if n_max < 1:
        raise ValueError("n_max must be at least 1")
    if n_max_refined <= n_max:
        raise ValueError("n_max_refined must be greater than n_max")


def invalid_inputs_rejected(V: float, n_max: int, n_max_refined: int) -> bool:
    """Return true only when the declared malformed input is rejected."""
    try:
        validate_inputs(V, n_max, n_max_refined)
    except ValueError:
        return True
    return False


def lengths_biaxial(V: float, r: float) -> tuple[float, float, float]:
    """Biaxial chart: L_t = r * L_p, L_p = L_p, L_3 = L_p, V = r L_p^3.

    So L_p = (V/r)^{1/3}, L_t = r L_p, L_y = L_p, L_z = L_p.
    """
    if not math.isfinite(V) or not math.isfinite(r) or r <= 0 or V <= 0:
        raise ValueError("V and r must be finite and positive")
    L_p = (V / r) ** (1.0 / 3.0)
    L_t = r * L_p
    return L_t, L_p, L_p


def mode_wavevectors(
    Lx: float, Ly: float, Lz: float, n_max: int
) -> np.ndarray:
    """Return array of shape (M, 3) of k-vectors excluding zero mode."""
    lengths = (Lx, Ly, Lz)
    if any(not math.isfinite(L) or L <= 0 for L in lengths):
        raise ValueError("side lengths must be finite and positive")
    if n_max < 1:
        raise ValueError("n_max must be at least 1")
    ns = range(-n_max, n_max + 1)
    vecs = []
    for nx in ns:
        for ny in ns:
            for nz in ns:
                if nx == 0 and ny == 0 and nz == 0:
                    continue
                kx = TWO_PI * nx / Lx
                ky = TWO_PI * ny / Ly
                kz = TWO_PI * nz / Lz
                vecs.append((kx, ky, kz))
    return np.asarray(vecs, dtype=float)


def directional_anisotropy_diagnostic(kvecs: np.ndarray) -> dict[str, float]:
    """Template diagnostic: variance of unit-direction components.

    For an isotropic cubic lattice in the continuum limit of dense modes,
    the three axis-aligned second moments of hat{k}_i^2 should approach 1/3.
    On a truncated lattice we use:
        A = max_i m_i - min_i m_i
    where m_i = mean(hat{k}_i^2) over modes with |k|>0.
    Cubic symmetry => A ~ 0 (up to truncation noise).
    """
    if kvecs.ndim != 2 or kvecs.shape[1] != 3 or kvecs.shape[0] == 0:
        raise ValueError("kvecs must be a non-empty array with shape (M, 3)")
    if not np.all(np.isfinite(kvecs)):
        raise ValueError("kvecs must contain only finite values")
    kn = np.linalg.norm(kvecs, axis=1)
    mask = kn > 0
    khat = kvecs[mask] / kn[mask][:, None]
    m = np.mean(khat**2, axis=0)
    A = float(np.max(m) - np.min(m))
    return {
        "m_x": float(m[0]),
        "m_y": float(m[1]),
        "m_z": float(m[2]),
        "anisotropy_A": A,
        "n_modes": int(mask.sum()),
    }


def volume_of(Lx: float, Ly: float, Lz: float) -> float:
    return float(Lx * Ly * Lz)


def main() -> None:
    args = parse_args()
    V = float(args.V)
    validate_inputs(V, args.n_max, args.n_max_refined)
    checks: list[dict[str, Any]] = []

    # --- Fixed-volume biaxial scan ---
    ratios = [0.5, 1.0, 1.5, 2.0]
    scan_rows = []
    vol_ok = True
    for r in ratios:
        Lx, Ly, Lz = lengths_biaxial(V, r)
        vol = volume_of(Lx, Ly, Lz)
        if abs(vol - V) > 1e-12 * max(1.0, V):
            vol_ok = False
        kvecs = mode_wavevectors(Lx, Ly, Lz, args.n_max)
        diag = directional_anisotropy_diagnostic(kvecs)
        scan_rows.append(
            {
                "r": r,
                "Lx": Lx,
                "Ly": Ly,
                "Lz": Lz,
                "volume": vol,
                **diag,
            }
        )

    checks.append(
        {
            "name": "fixed_volume_under_biaxial_scan",
            "ok": vol_ok,
            "V_target": V,
            "control_type": "constraint",
        }
    )

    # --- Negative control: cubic r=1 => A small ---
    elongated = [row for row in scan_rows if abs(row["r"] - 1.0) > 1e-15]
    # For exact cubic Lx=Ly=Lz, hat{k} statistics on a cubic lattice of n are
    # symmetric under axis permutation => A should be ~0 within float noise.
    Lx, Ly, Lz = lengths_biaxial(V, 1.0)
    kvecs_c = mode_wavevectors(Lx, Ly, Lz, args.n_max)
    diag_c = directional_anisotropy_diagnostic(kvecs_c)
    cubic_strict_ok = diag_c["anisotropy_A"] < 1e-14
    checks.append(
        {
            "name": "negative_control_cubic_mode_anisotropy_vanishes",
            "ok": bool(cubic_strict_ok),
            "anisotropy_A": diag_c["anisotropy_A"],
            "control_type": "negative",
        }
    )

    # Every tested non-cubic shape should differ from the cubic control.
    noncubic_ok = all(
        row["anisotropy_A"] > diag_c["anisotropy_A"] + 1e-15 for row in elongated
    )
    checks.append(
        {
            "name": "tested_noncubic_shapes_have_nonzero_anisotropy_diagnostic",
            "ok": bool(noncubic_ok),
            "A_cubic": diag_c["anisotropy_A"],
            "A_values": {str(row["r"]): row["anisotropy_A"] for row in scan_rows},
            "control_type": "positive_template",
        }
    )

    # --- Refinement control at r=2 ---
    Lx, Ly, Lz = lengths_biaxial(V, 2.0)
    d_coarse = directional_anisotropy_diagnostic(
        mode_wavevectors(Lx, Ly, Lz, args.n_max)
    )
    d_fine = directional_anisotropy_diagnostic(
        mode_wavevectors(Lx, Ly, Lz, args.n_max_refined)
    )
    rel = abs(d_fine["anisotropy_A"] - d_coarse["anisotropy_A"]) / max(
        d_fine["anisotropy_A"], 1e-30
    )
    # The declared default changes by about 4.5e-4; retain a 1% guardrail.
    refine_ok = (
        rel < 0.01
        and d_fine["anisotropy_A"] > 0
        and d_coarse["anisotropy_A"] > 0
    )
    checks.append(
        {
            "name": "refinement_control_anisotropy_stable_order",
            "ok": bool(refine_ok),
            "A_n_max": d_coarse["anisotropy_A"],
            "A_n_max_refined": d_fine["anisotropy_A"],
            "relative_change": rel,
            "n_max": args.n_max,
            "n_max_refined": args.n_max_refined,
            "control_type": "refinement",
        }
    )

    # --- Firewall flags (must remain false) ---
    packaging_flags = {
        "claims_13_12_attractor": False,
        "claims_H0_72_97": False,
        "claims_a0_from_topology": False,
        "claims_Cobs_2_3_from_geometry": False,
        "claims_twisted_preferred_without_comparison": False,
        "claims_casimir_stress_computed": False,
        "claims_cosmology": False,
    }
    checks.append(
        {
            "name": "claim_firewall_packaging_flags_false",
            "ok": all(v is False for v in packaging_flags.values()),
            "flags": packaging_flags,
            "control_type": "firewall",
        }
    )

    # --- Malformed-domain negative controls ---
    invalid_controls = [
        ("negative_control_nonpositive_volume_rejected", 0.0, 6, 10),
        ("negative_control_nonfinite_volume_rejected", math.nan, 6, 10),
        ("negative_control_empty_mode_lattice_rejected", 1.0, 0, 10),
        ("negative_control_nonrefining_cutoff_rejected", 1.0, 6, 6),
    ]
    for name, invalid_V, invalid_n, invalid_refined in invalid_controls:
        checks.append(
            {
                "name": name,
                "ok": invalid_inputs_rejected(
                    invalid_V, invalid_n, invalid_refined
                ),
                "control_type": "negative",
            }
        )

    all_ok = all(c["ok"] for c in checks)
    status = (
        "PASS_TOP001_MATH_TEMPLATE_ONLY"
        if all_ok
        else "FAIL_TOP001_MATH_TEMPLATE"
    )

    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "label": "mathematical-template-only",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": status,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "fixed_volume": V,
        "biaxial_scan": scan_rows,
        "checks": checks,
        "forbidden_packaging_not_used": list(packaging_flags.keys()),
        "separations_demonstrated": [
            "fixed_volume_vs_shape_ratio",
            "mode_lattice_geometry_vs_casimir_stress",
            "cubic_negative_control_vs_elongated_shape",
            "template_vs_physical_prediction",
        ],
        "scientific_boundary": (
            "Fixed-volume rectangular T^3 shape and free-scalar mode-lattice "
            "anisotropy diagnostics only. Does not compute Casimir tensors, "
            "backreaction, 13/12 attractors, dynamical moduli actions, twisted "
            "BC preference, or any cosmological observable."
        ),
        "cbr001_baseline_reminder": (
            "Free-field Casimir anisotropy exists (CBR-001); persistent free-field "
            "13/12 attractor does not. This template does not recompute CBR-001."
        ),
        "next_research_stages": [
            "S1 full triaxial charts if needed",
            "S2 interface to CBR-001 pipeline without packaging",
            "S3 dynamical S_mod only without forbidden targets",
            "S4 twisted comparison before any preference upgrade",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "top001_shape_template_audit_summary.json"
    # Deterministic key order
    with out.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print("TOP-001 mathematical-template-only audit")
    print("  physics_pass:", summary["physics_pass"])
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']}")
    print("STATUS:", status)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
