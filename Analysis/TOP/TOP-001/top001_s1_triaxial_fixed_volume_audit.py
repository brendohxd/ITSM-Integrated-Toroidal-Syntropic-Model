#!/usr/bin/env python3
"""TOP-001 Stage S1: fixed-volume full-triaxial rectangular T^3 audit (hardened).

LABEL: mathematical-template-only
GATE:  TOP-001 Stage S1 (fixed boundary)
CLAIM: none Derived; physics_pass is always false
STATUS: OPEN_SCAFFOLD_ONLY

Separates from the reviewed biaxial scaffold
--------------------------------------------
Independent of top001_shape_template_audit.py (biaxial r-chart).
Two independent log-shape coordinates at fixed volume V.

Log-shape chart (fixed V)
-------------------------
  L_i = V^{1/3} exp(alpha_i),  sum_i alpha_i = 0
  Independent: (alpha_x, alpha_y);  alpha_z = -(alpha_x + alpha_y)
  Cubic: (0, 0)

Checks (hardened S1 continuation)
---------------------------------
1. Volume preservation under triaxial scan
2. Cubic limit: anisotropy A ~ 0
3. Non-cubic: A > 0
4. Axis-permutation covariance of directional moments
5. Refinement stability (default <= 1% relative, matching biaxial review)
6. Malformed inputs rejected
7. Volume scale invariance of hat{k} diagnostics (same alphas, different V)
8. Smooth approach to cubic (small alphas => small A)
9. Claim firewall packaging flags false

Does NOT: modulus action, Casimir, twisted BC preference, backreaction,
13/12, H0, a0, C_obs, cosmology.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


TWO_PI = 2.0 * math.pi
# Match reviewed biaxial refinement guardrail.
REFINEMENT_REL_MAX = 0.01


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--V", type=float, default=1.0, help="fixed volume")
    p.add_argument("--n-max", type=int, default=6)
    p.add_argument("--n-max-refined", type=int, default=10)
    p.add_argument(
        "--refinement-rel-max",
        type=float,
        default=REFINEMENT_REL_MAX,
        help="max relative change of A under n_max refinement",
    )
    return p.parse_args()


def validate_domain(V: float, n_max: int, n_max_refined: int) -> None:
    if not math.isfinite(V) or V <= 0:
        raise ValueError("V must be finite and positive")
    if n_max < 1:
        raise ValueError("n_max must be at least 1")
    if n_max_refined <= n_max:
        raise ValueError("n_max_refined must be greater than n_max")


def validate_log_shape(alpha_x: float, alpha_y: float) -> None:
    if not math.isfinite(alpha_x) or not math.isfinite(alpha_y):
        raise ValueError("log-shape coordinates must be finite")


def lengths_from_log_shape(
    V: float, alpha_x: float, alpha_y: float
) -> tuple[float, float, float, float]:
    """Return (Lx, Ly, Lz, alpha_z) with alpha_z = -(alpha_x+alpha_y)."""
    if not math.isfinite(V) or V <= 0:
        raise ValueError("V must be finite and positive")
    validate_log_shape(alpha_x, alpha_y)
    alpha_z = -(alpha_x + alpha_y)
    v13 = V ** (1.0 / 3.0)
    Lx = v13 * math.exp(alpha_x)
    Ly = v13 * math.exp(alpha_y)
    Lz = v13 * math.exp(alpha_z)
    if not all(math.isfinite(x) and x > 0 for x in (Lx, Ly, Lz)):
        raise ValueError("side lengths must be finite and positive")
    return Lx, Ly, Lz, alpha_z


def mode_wavevectors(
    Lx: float, Ly: float, Lz: float, n_max: int
) -> np.ndarray:
    if n_max < 1:
        raise ValueError("n_max must be at least 1")
    if not all(math.isfinite(L) and L > 0 for L in (Lx, Ly, Lz)):
        raise ValueError("side lengths must be finite and positive")
    ns = range(-n_max, n_max + 1)
    vecs = []
    for nx in ns:
        for ny in ns:
            for nz in ns:
                if nx == 0 and ny == 0 and nz == 0:
                    continue
                vecs.append(
                    (TWO_PI * nx / Lx, TWO_PI * ny / Ly, TWO_PI * nz / Lz)
                )
    arr = np.asarray(vecs, dtype=float)
    if arr.size == 0:
        raise ValueError("mode lattice is empty")
    if not np.all(np.isfinite(arr)):
        raise ValueError("mode lattice contains non-finite entries")
    return arr


def directional_diagnostics(kvecs: np.ndarray) -> dict[str, float]:
    """Directional second moments of hat{k}; A = max m_i - min m_i."""
    if kvecs.size == 0:
        raise ValueError("empty mode lattice")
    kn = np.linalg.norm(kvecs, axis=1)
    mask = kn > 0
    if not np.any(mask):
        raise ValueError("no positive |k| modes")
    khat = kvecs[mask] / kn[mask][:, None]
    if not np.all(np.isfinite(khat)):
        raise ValueError("non-finite hat{k}")
    m = np.mean(khat**2, axis=0)
    A = float(np.max(m) - np.min(m))
    if not math.isfinite(A):
        raise ValueError("non-finite anisotropy")
    return {
        "m_x": float(m[0]),
        "m_y": float(m[1]),
        "m_z": float(m[2]),
        "anisotropy_A": A,
        "n_modes": int(mask.sum()),
    }


def permute_lengths(
    Lx: float, Ly: float, Lz: float, order: str
) -> tuple[float, float, float]:
    pack = {"x": Lx, "y": Ly, "z": Lz}
    if sorted(order) != ["x", "y", "z"]:
        raise ValueError("order must be a permutation of xyz")
    return pack[order[0]], pack[order[1]], pack[order[2]]


def permute_moments(
    m_x: float, m_y: float, m_z: float, order: str
) -> tuple[float, float, float]:
    pack = {"x": m_x, "y": m_y, "z": m_z}
    return pack[order[0]], pack[order[1]], pack[order[2]]


def malformed_rejected(
    V: float,
    alpha_x: float,
    alpha_y: float,
    n_max: int,
    n_max_refined: int,
) -> bool:
    try:
        validate_domain(V, n_max, n_max_refined)
        validate_log_shape(alpha_x, alpha_y)
        lengths_from_log_shape(V, alpha_x, alpha_y)
    except (ValueError, OverflowError):
        return True
    return False


def shape_row(
    V: float, name: str, alpha_x: float, alpha_y: float, n_max: int
) -> dict[str, Any]:
    Lx, Ly, Lz, az = lengths_from_log_shape(V, alpha_x, alpha_y)
    diag = directional_diagnostics(mode_wavevectors(Lx, Ly, Lz, n_max))
    return {
        "name": name,
        "alpha_x": alpha_x,
        "alpha_y": alpha_y,
        "alpha_z": az,
        "Lx": Lx,
        "Ly": Ly,
        "Lz": Lz,
        "volume": Lx * Ly * Lz,
        "sum_alpha": alpha_x + alpha_y + az,
        **diag,
    }


def main() -> None:
    args = parse_args()
    V = float(args.V)
    n_max = int(args.n_max)
    n_max_ref = int(args.n_max_refined)
    ref_rel_max = float(args.refinement_rel_max)
    validate_domain(V, n_max, n_max_ref)
    if not math.isfinite(ref_rel_max) or ref_rel_max <= 0:
        raise ValueError("refinement-rel-max must be finite and positive")

    checks: list[dict[str, Any]] = []

    shape_points = [
        {"name": "cubic", "alpha_x": 0.0, "alpha_y": 0.0},
        {"name": "near_cubic", "alpha_x": 0.02, "alpha_y": -0.01},
        {"name": "triaxial_A", "alpha_x": 0.4, "alpha_y": -0.15},
        {"name": "triaxial_B", "alpha_x": -0.3, "alpha_y": 0.5},
        {"name": "triaxial_C", "alpha_x": 0.25, "alpha_y": 0.25},
        {"name": "nearly_biaxial", "alpha_x": 0.5, "alpha_y": 0.0},
        {"name": "strong_triaxial", "alpha_x": 0.6, "alpha_y": -0.4},
    ]

    scan_rows = [
        shape_row(V, p["name"], p["alpha_x"], p["alpha_y"], n_max)
        for p in shape_points
    ]

    vol_ok = all(
        abs(r["volume"] - V) <= 1e-12 * max(1.0, V)
        and abs(r["sum_alpha"]) < 1e-14
        for r in scan_rows
    )
    checks.append(
        {
            "name": "fixed_volume_preserved_under_triaxial_log_shape",
            "ok": vol_ok,
            "control_type": "constraint",
            "V_target": V,
            "max_abs_volume_error": max(abs(r["volume"] - V) for r in scan_rows),
        }
    )

    cubic = next(r for r in scan_rows if r["name"] == "cubic")
    checks.append(
        {
            "name": "cubic_limit_anisotropy_vanishes",
            "ok": cubic["anisotropy_A"] < 1e-14,
            "anisotropy_A": cubic["anisotropy_A"],
            "control_type": "negative",
        }
    )

    non_cubic = [r for r in scan_rows if r["name"] != "cubic"]
    checks.append(
        {
            "name": "non_cubic_shapes_have_positive_anisotropy",
            "ok": all(r["anisotropy_A"] > 1e-12 for r in non_cubic),
            "A_by_name": {r["name"]: r["anisotropy_A"] for r in non_cubic},
            "control_type": "positive_template",
            "note": "Chart sample result, not a global monotonic theorem",
        }
    )

    # Smooth approach: near_cubic A << strong_triaxial A and A_near > 0
    near = next(r for r in scan_rows if r["name"] == "near_cubic")
    strong = next(r for r in scan_rows if r["name"] == "strong_triaxial")
    smooth_ok = (
        near["anisotropy_A"] > 0
        and near["anisotropy_A"] < 0.25 * strong["anisotropy_A"]
    )
    checks.append(
        {
            "name": "smooth_approach_to_cubic_small_alphas_small_A",
            "ok": bool(smooth_ok),
            "A_near_cubic": near["anisotropy_A"],
            "A_strong_triaxial": strong["anisotropy_A"],
            "control_type": "continuity_template",
        }
    )

    # Axis-permutation covariance on triaxial_A
    ref = next(r for r in scan_rows if r["name"] == "triaxial_A")
    Lx, Ly, Lz = ref["Lx"], ref["Ly"], ref["Lz"]
    m_ref = (ref["m_x"], ref["m_y"], ref["m_z"])
    perm_ok = True
    perm_rows = []
    for order in ("xyz", "yxz", "zxy", "xzy", "zyx", "yzx"):
        Lp = permute_lengths(Lx, Ly, Lz, order)
        d = directional_diagnostics(mode_wavevectors(*Lp, n_max))
        m_expected = permute_moments(*m_ref, order)
        m_got = (d["m_x"], d["m_y"], d["m_z"])
        close = all(
            abs(a - b) < 1e-12 for a, b in zip(m_got, m_expected, strict=True)
        )
        A_close = abs(d["anisotropy_A"] - ref["anisotropy_A"]) < 1e-12
        row_ok = close and A_close
        perm_ok = perm_ok and row_ok
        perm_rows.append(
            {
                "order": order,
                "ok": row_ok,
                "m_got": list(m_got),
                "m_expected": list(m_expected),
                "A": d["anisotropy_A"],
            }
        )
    checks.append(
        {
            "name": "axis_permutation_covariance_of_directional_moments",
            "ok": perm_ok,
            "reference_shape": "triaxial_A",
            "permutations": perm_rows,
            "control_type": "covariance",
        }
    )

    # Refinement (tightened)
    tb = next(r for r in scan_rows if r["name"] == "triaxial_B")
    d_c = directional_diagnostics(
        mode_wavevectors(tb["Lx"], tb["Ly"], tb["Lz"], n_max)
    )
    d_f = directional_diagnostics(
        mode_wavevectors(tb["Lx"], tb["Ly"], tb["Lz"], n_max_ref)
    )
    rel = abs(d_f["anisotropy_A"] - d_c["anisotropy_A"]) / max(
        d_f["anisotropy_A"], 1e-30
    )
    refine_ok = (
        rel <= ref_rel_max
        and d_f["anisotropy_A"] > 0
        and d_c["anisotropy_A"] > 0
    )
    checks.append(
        {
            "name": "refinement_control_anisotropy_within_rel_max",
            "ok": bool(refine_ok),
            "A_n_max": d_c["anisotropy_A"],
            "A_n_max_refined": d_f["anisotropy_A"],
            "relative_change": rel,
            "refinement_rel_max": ref_rel_max,
            "n_max": n_max,
            "n_max_refined": n_max_ref,
            "control_type": "refinement",
        }
    )

    # Volume scale invariance: same alphas, V and 8V => same A (hat{k} only)
    V2 = 8.0 * V
    row_v1 = shape_row(V, "scale_ref", 0.4, -0.15, n_max)
    row_v2 = shape_row(V2, "scale_8V", 0.4, -0.15, n_max)
    scale_ok = (
        abs(row_v1["anisotropy_A"] - row_v2["anisotropy_A"]) < 1e-12
        and abs(row_v1["m_x"] - row_v2["m_x"]) < 1e-12
        and abs(row_v1["m_y"] - row_v2["m_y"]) < 1e-12
        and abs(row_v1["m_z"] - row_v2["m_z"]) < 1e-12
        and abs(row_v2["volume"] - V2) <= 1e-12 * max(1.0, V2)
    )
    checks.append(
        {
            "name": "volume_scale_invariance_of_hatk_diagnostics",
            "ok": bool(scale_ok),
            "A_V": row_v1["anisotropy_A"],
            "A_8V": row_v2["anisotropy_A"],
            "V": V,
            "V_scaled": V2,
            "control_type": "scale_invariance",
            "note": "hat{k} moments are scale-free for uniform L rescaling at fixed alphas",
        }
    )

    bad_cases = [
        {"label": "V_nonpositive", "V": 0.0, "ax": 0.1, "ay": 0.1, "nm": 6, "nr": 10},
        {"label": "V_negative", "V": -1.0, "ax": 0.0, "ay": 0.0, "nm": 6, "nr": 10},
        {"label": "V_nan", "V": float("nan"), "ax": 0.0, "ay": 0.0, "nm": 6, "nr": 10},
        {"label": "V_inf", "V": float("inf"), "ax": 0.0, "ay": 0.0, "nm": 6, "nr": 10},
        {
            "label": "alpha_inf",
            "V": 1.0,
            "ax": float("inf"),
            "ay": 0.0,
            "nm": 6,
            "nr": 10,
        },
        {
            "label": "alpha_nan",
            "V": 1.0,
            "ax": float("nan"),
            "ay": 0.0,
            "nm": 6,
            "nr": 10,
        },
        {"label": "n_max_zero", "V": 1.0, "ax": 0.0, "ay": 0.0, "nm": 0, "nr": 2},
        {
            "label": "n_max_refined_not_greater",
            "V": 1.0,
            "ax": 0.0,
            "ay": 0.0,
            "nm": 6,
            "nr": 6,
        },
        {
            "label": "n_max_refined_smaller",
            "V": 1.0,
            "ax": 0.0,
            "ay": 0.0,
            "nm": 6,
            "nr": 3,
        },
    ]
    mal_rows = []
    mal_ok = True
    for c in bad_cases:
        rejected = malformed_rejected(c["V"], c["ax"], c["ay"], c["nm"], c["nr"])
        mal_rows.append({"label": c["label"], "rejected": rejected})
        if not rejected:
            mal_ok = False
    checks.append(
        {
            "name": "malformed_inputs_rejected",
            "ok": mal_ok,
            "cases": mal_rows,
            "control_type": "malformed",
        }
    )

    packaging_flags = {
        "claims_modulus_action": False,
        "claims_casimir_tensor": False,
        "claims_twisted_preferred": False,
        "claims_backreaction": False,
        "claims_13_12_attractor": False,
        "claims_H0": False,
        "claims_a0_from_topology": False,
        "claims_Cobs": False,
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

    all_ok = all(c["ok"] for c in checks)
    status = (
        "PASS_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE"
        if all_ok
        else "FAIL_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE"
    )

    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "stage": "S1_FIXED_BOUNDARY_TRIAXIAL",
        "stage_revision": "S1_hardened_continuation",
        "label": "mathematical-template-only",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": status,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "log_shape_chart": {
            "name": "fixed_volume_log_shape_two_coords",
            "definition": (
                "L_i = V**(1/3)*exp(alpha_i), alpha_z = -(alpha_x+alpha_y), "
                "independent coordinates (alpha_x, alpha_y)"
            ),
            "cubic_point": {"alpha_x": 0.0, "alpha_y": 0.0},
            "independent_from_biaxial_r_chart": True,
            "biaxial_scaffold_file": "top001_shape_template_audit.py",
        },
        "fixed_volume": V,
        "refinement_rel_max_default": REFINEMENT_REL_MAX,
        "triaxial_scan": scan_rows,
        "checks": checks,
        "n_checks": len(checks),
        "forbidden_packaging_not_used": list(packaging_flags.keys()),
        "separations_demonstrated": [
            "fixed_volume_vs_two_log_shape_coordinates",
            "full_triaxial_vs_reviewed_biaxial_scaffold",
            "cubic_negative_control_vs_non_cubic_diagnostics",
            "axis_permutation_covariance_of_moments",
            "volume_scale_invariance_of_hatk_moments",
            "template_vs_physical_prediction",
        ],
        "scientific_boundary": (
            "Fixed-volume full-triaxial rectangular T^3 geometry and free-scalar "
            "mode-lattice diagnostics only. Does not compute Casimir tensors, "
            "backreaction, dynamical moduli actions, twisted BC preference, or "
            "any cosmological / force-law observable. physics_pass remains false."
        ),
        "next_research_stages": [
            "S1 complete as geometry template; optional dual-run hash freeze",
            "S2 CBR-001 interface without packaging (separate task)",
            "S3 dynamical S_mod only without forbidden targets",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "top001_s1_triaxial_fixed_volume_summary.json"
    payload_bytes = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    out.write_bytes(payload_bytes)
    content_hash = hashlib.sha256(payload_bytes).hexdigest()
    hash_path = args.output_dir / "top001_s1_triaxial_fixed_volume_summary.sha256"
    hash_path.write_bytes(f"{content_hash}  {out.name}\n".encode("utf-8"))

    print("TOP-001 Stage S1 triaxial fixed-volume audit (hardened)")
    print("  physics_pass:", summary["physics_pass"])
    print("  research_gate_status:", summary["research_gate_status"])
    print("  n_checks:", len(checks))
    for c in checks:
        mark = "OK" if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']}")
    print("STATUS:", status)
    print("JSON_SHA256:", content_hash)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
