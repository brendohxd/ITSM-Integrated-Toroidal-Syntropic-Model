#!/usr/bin/env python3
"""TOP-001 S2: referee-grade CBR-001 bridge (fixed rectangular T^3 scaffold).

LABEL: Conditional interface bridge; free-field stress only
GATE:  TOP-001 Stage S2 (CBR tools call with TOP-owned geometry)
CLAIM: none Derived cosmology; physics_pass is always false
STATUS: OPEN_SCAFFOLD_ONLY

Numerical authority: Analysis/Casimir/CBR-001/casimir_t3_lattice.py

Does NOT: S_mod, twisted preference, 13/12 packaging, H0, a0, Cobs, cosmology.
Template/calculation PASS is not TOP research-gate PASS.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


# Default refining integer ladder for measured multi-cutoff behaviour
DEFAULT_CUTOFFS = (20, 30, 40, 60, 80)


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    repo = base.parents[2]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--repo-root",
        type=Path,
        default=repo,
        help="repository root for relative path embedding in JSON",
    )
    p.add_argument(
        "--cbr-module",
        type=Path,
        default=repo / "Analysis" / "Casimir" / "CBR-001" / "casimir_t3_lattice.py",
    )
    p.add_argument("--V", type=float, default=1.0, help="fixed volume (>0 finite)")
    p.add_argument(
        "--cutoff",
        type=int,
        default=40,
        help="primary lattice cutoff (positive integer)",
    )
    p.add_argument(
        "--cutoffs",
        type=int,
        nargs="+",
        default=list(DEFAULT_CUTOFFS),
        help="strictly increasing positive integers for multi-cutoff scan",
    )
    p.add_argument(
        "--scale",
        type=float,
        default=1.7,
        help="uniform length scale factor for rho,p ∝ s^{-4} test",
    )
    return p.parse_args()


def load_cbr(path: Path):
    spec = importlib.util.spec_from_file_location("casimir_t3_lattice", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def validate_V(V: float) -> None:
    if isinstance(V, bool) or not isinstance(V, (int, float)):
        raise ValueError("V must be a real number")
    if not math.isfinite(V) or V <= 0.0:
        raise ValueError("V must be finite and > 0")


def validate_cutoff(cutoff: int) -> None:
    if isinstance(cutoff, bool) or not isinstance(cutoff, int):
        raise ValueError("cutoff must be an integer")
    if cutoff < 1:
        raise ValueError("cutoff must be a positive integer (>= 1)")


def validate_cutoffs(cutoffs: list[int]) -> tuple[int, ...]:
    if len(cutoffs) < 2:
        raise ValueError("need at least two cutoffs for multi-cutoff scan")
    out: list[int] = []
    for c in cutoffs:
        validate_cutoff(c)
        out.append(c)
    for a, b in zip(out, out[1:]):
        if b <= a:
            raise ValueError("cutoffs must be strictly increasing (refining)")
    return tuple(out)


def lengths_from_log(V: float, ax: float, ay: float) -> tuple[float, float, float]:
    """Fixed-volume log-shape chart: L_i = V^{1/3} exp(alpha_i), sum alpha=0."""
    validate_V(V)
    if not (math.isfinite(ax) and math.isfinite(ay)):
        raise ValueError("log-shape coordinates must be finite")
    az = -(ax + ay)
    L0 = V ** (1.0 / 3.0)
    if not math.isfinite(L0) or L0 <= 0.0:
        raise ValueError("failed to form positive side length scale from V")
    L = (L0 * math.exp(ax), L0 * math.exp(ay), L0 * math.exp(az))
    if not all(math.isfinite(x) and x > 0.0 for x in L):
        raise ValueError("produced non-finite or nonpositive side lengths")
    return L


def is_genuinely_triaxial(L: tuple[float, float, float], rel: float = 1e-9) -> bool:
    a, b, c = sorted(L)
    return (b - a) > rel * b and (c - b) > rel * c


def is_genuine_biaxial(L: tuple[float, float, float], rel: float = 1e-9) -> bool:
    """Exactly one pair of equal sides; not cubic (two equal, one distinct)."""
    vals = sorted(float(x) for x in L)
    a, b, c = vals
    # equality of a pair
    eq_ab = abs(b - a) <= rel * max(b, 1e-30)
    eq_bc = abs(c - b) <= rel * max(c, 1e-30)
    eq_ac = abs(c - a) <= rel * max(c, 1e-30)
    n_eq_pairs = int(eq_ab) + int(eq_bc) + int(eq_ac)
    # genuine biaxial: exactly one equality pair among sorted consecutive
    # (two lengths equal) and not all three equal
    if eq_ac:  # all three equal within chain
        return False
    return (eq_ab and not eq_bc) or (eq_bc and not eq_ab)


def repo_relative(path: Path, repo_root: Path) -> str:
    """Stable path for JSON: relative to repo root with forward slashes."""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        # Fall back to as_posix without drive-only absolute OneDrive leak if possible
        parts = path.resolve().parts
        if "Analysis" in parts:
            i = parts.index("Analysis")
            return "/".join(parts[i:])
        return path.name


def stress_dict(cbr: Any, L: tuple[float, float, float], cutoff: int) -> dict[str, Any]:
    st = cbr.lattice_stress(L, cutoff)
    return {
        "L": [float(L[0]), float(L[1]), float(L[2])],
        "volume": float(L[0] * L[1] * L[2]),
        "rho": float(st.rho),
        "p": [float(st.p1), float(st.p2), float(st.p3)],
        "energy": float(st.energy),
        "trace": float(st.trace),
        "cutoff": int(st.cutoff),
    }


_EXPECTED_NEGATIVE = (ValueError, TypeError, OverflowError, FloatingPointError)


def run_malformed_controls(cbr: Any) -> list[dict[str, Any]]:
    """Negative controls: must raise an *expected* exception; unexpected = fail closed."""
    cases: list[tuple[str, Any]] = [
        ("V_nonpositive", lambda: lengths_from_log(0.0, 0.0, 0.0)),
        ("V_negative", lambda: lengths_from_log(-1.0, 0.0, 0.0)),
        ("V_nan", lambda: lengths_from_log(float("nan"), 0.0, 0.0)),
        ("V_inf", lambda: lengths_from_log(float("inf"), 0.1, -0.05)),
        ("alpha_nan", lambda: lengths_from_log(1.0, float("nan"), 0.0)),
        ("cutoff_zero", lambda: cbr.lattice_stress((1.0, 1.0, 1.0), 0)),
        ("cutoff_negative", lambda: cbr.lattice_stress((1.0, 1.0, 1.0), -3)),
        ("L_nonpositive", lambda: cbr.lattice_stress((1.0, 0.0, 1.0), 10)),
        ("L_nan", lambda: cbr.lattice_stress((1.0, float("nan"), 1.0), 10)),
    ]
    rows: list[dict[str, Any]] = []
    for name, fn in cases:
        try:
            fn()
            rows.append(
                {
                    "case": name,
                    "raised": False,
                    "error": "",
                    "ok": False,
                    "detail": "expected exception not raised",
                }
            )
        except _EXPECTED_NEGATIVE as exc:
            rows.append(
                {
                    "case": name,
                    "raised": True,
                    "error": type(exc).__name__,
                    "ok": True,
                }
            )
        except Exception as exc:  # noqa: BLE001 — unexpected: fail closed
            rows.append(
                {
                    "case": name,
                    "raised": True,
                    "error": f"unexpected:{type(exc).__name__}",
                    "ok": False,
                    "detail": "unexpected exception class (fail closed)",
                }
            )
    return rows


def multi_cutoff_table(
    cbr: Any, L: tuple[float, float, float], cutoffs: tuple[int, ...]
) -> dict[str, Any]:
    """Measure rho(N) and successive relative changes; no invented pass tolerance."""
    rows = []
    prev_rho = None
    for N in cutoffs:
        st = cbr.lattice_stress(L, N)
        rho = float(st.rho)
        rel_change = None if prev_rho is None else abs(rho - prev_rho) / max(abs(prev_rho), 1e-30)
        rows.append(
            {
                "cutoff": N,
                "rho": rho,
                "p": [float(st.p1), float(st.p2), float(st.p3)],
                "successive_rel_change_rho": rel_change,
            }
        )
        prev_rho = rho

    changes = [r["successive_rel_change_rho"] for r in rows if r["successive_rel_change_rho"] is not None]
    # Convergence *behaviour*: successive relative changes should be nonincreasing
    # on the refining ladder for free-field lattice sums (measured, not forced).
    monotone_nonincreasing = all(
        changes[i + 1] <= changes[i] * (1.0 + 1e-9) + 1e-15
        for i in range(len(changes) - 1)
    ) if len(changes) >= 2 else False

    # Also report max successive change on the upper half of the ladder
    half = max(1, len(changes) // 2)
    upper = changes[-half:] if changes else []
    max_upper_rel = float(max(upper)) if upper else float("nan")

    # Extrapolation via CBR authority when enough points
    y_inf = None
    if len(cutoffs) >= 4:
        try:
            y_inf, _coef = cbr.extrapolate_to_infinity(
                list(cutoffs), [r["rho"] for r in rows], order=2
            )
        except Exception as exc:  # noqa: BLE001
            y_inf = f"extrapolation_failed:{type(exc).__name__}"

    last = rows[-1]["rho"]
    penult = rows[-2]["rho"] if len(rows) >= 2 else None
    final_pair_rel = (
        None
        if penult is None
        else abs(last - penult) / max(abs(penult), 1e-30)
    )

    # Pass criterion from *measured* final-pair behaviour: require that the
    # last successive relative change is smaller than the first (refinement
    # actually reduces change), and report the measured values. No absolute
    # flattering eps invented for "good enough" Casimir physics.
    first_change = changes[0] if changes else None
    improved = (
        first_change is not None
        and final_pair_rel is not None
        and final_pair_rel < first_change
    )

    return {
        "geometry": "cubic_unit_volume_reference",
        "L": list(L),
        "cutoffs": list(cutoffs),
        "rows": rows,
        "successive_rel_changes": changes,
        "monotone_nonincreasing_successive_changes": monotone_nonincreasing,
        "max_successive_rel_change_upper_half": max_upper_rel,
        "final_pair_rel_change": final_pair_rel,
        "first_pair_rel_change": first_change,
        "refinement_reduces_successive_change": improved,
        "extrapolated_rho_inf_order2": y_inf,
        "pass_rule": (
            "PASS if refining ladder is strictly increasing integers and the "
            "final successive |Δρ|/|ρ| is strictly smaller than the first "
            "successive change (measured improvement). Absolute tolerance is "
            "not imposed."
        ),
        "ok": improved and len(cutoffs) >= 2,
    }


def main() -> None:
    args = parse_args()
    checks: list[dict[str, Any]] = []

    # --- Input validation (domain) ---
    try:
        validate_V(args.V)
        v_ok = True
        v_err = ""
    except ValueError as exc:
        v_ok = False
        v_err = str(exc)
    checks.append({"name": "V_finite_positive", "ok": v_ok, "detail": v_err or args.V})

    try:
        validate_cutoff(args.cutoff)
        c_ok = True
        c_err = ""
    except ValueError as exc:
        c_ok = False
        c_err = str(exc)
    checks.append(
        {"name": "cutoff_valid_integer", "ok": c_ok, "detail": c_err or args.cutoff}
    )

    try:
        cutoffs = validate_cutoffs(list(args.cutoffs))
        # primary cutoff should lie on or within the refining ladder span
        ladder_ok = True
        cut_err = ""
    except ValueError as exc:
        cutoffs = tuple(DEFAULT_CUTOFFS)
        ladder_ok = False
        cut_err = str(exc)
    checks.append(
        {
            "name": "cutoffs_strictly_increasing_refining",
            "ok": ladder_ok,
            "cutoffs": list(cutoffs),
            "detail": cut_err,
        }
    )

    if not (v_ok and c_ok and ladder_ok):
        # Still attempt to write a FAIL summary for determinism of failure path
        summary = {
            "gate": "TOP-001",
            "stage": "S2_CBR001_BRIDGE",
            "calculation_status": "FAIL",
            "subgate_status": "FAIL_TOP001_S2_CBR001_BRIDGE",
            "research_gate_status": "OPEN_SCAFFOLD_ONLY",
            "physics_pass": False,
            "checks": checks,
        }
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out = args.output_dir / "top001_s2_cbr001_bridge_summary.json"
        payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
        out.write_bytes(payload)
        h = hashlib.sha256(payload).hexdigest().upper()
        (args.output_dir / "top001_s2_cbr001_bridge_summary.sha256").write_bytes(
            f"{h}  {out.name}\n".encode("utf-8")
        )
        print("STATUS: FAIL_TOP001_S2_CBR001_BRIDGE")
        print("JSON_SHA256:", h)
        raise SystemExit(1)

    cbr = load_cbr(args.cbr_module)

    # --- Fixed-volume shape samples ---
    # Biaxial: alpha_x = alpha_y => Lx = Ly ≠ Lz (two equal lengths).
    # Triaxial: three distinct L_i.
    samples = {
        "cubic": lengths_from_log(args.V, 0.0, 0.0),
        "biaxial": lengths_from_log(args.V, 0.12, 0.12),  # Lx=Ly, Lz=V^{1/3}e^{-0.24}
        "triaxial": lengths_from_log(args.V, 0.25, -0.10),  # three distinct L_i
    }
    checks.append(
        {
            "name": "triaxial_sample_genuinely_triaxial",
            "ok": is_genuinely_triaxial(samples["triaxial"]),
            "L": list(samples["triaxial"]),
        }
    )
    Lb = samples["biaxial"]
    checks.append(
        {
            "name": "biaxial_sample_two_equal_lengths",
            "ok": is_genuine_biaxial(Lb),
            "L": list(Lb),
            "note": "alpha_x=alpha_y => Lx=Ly ≠ Lz at fixed V",
        }
    )
    checks.append(
        {
            "name": "biaxial_Lx_equals_Ly",
            "ok": abs(Lb[0] - Lb[1]) <= 1e-12 * max(Lb[0], Lb[1]),
            "Lx": Lb[0],
            "Ly": Lb[1],
            "Lz": Lb[2],
        }
    )
    checks.append(
        {
            "name": "biaxial_Lz_distinct",
            "ok": abs(Lb[2] - Lb[0]) > 1e-9 * max(Lb),
            "Lz": Lb[2],
        }
    )

    results: dict[str, Any] = {}
    for name, L in samples.items():
        results[name] = stress_dict(cbr, L, args.cutoff)
        checks.append(
            {
                "name": f"fixed_volume_{name}",
                "ok": abs(results[name]["volume"] - args.V) <= 1e-12 * args.V,
                "volume": results[name]["volume"],
                "V": args.V,
            }
        )

    # --- Cubic pressure isotropy (exact symmetry of cube; finite-N residual) ---
    pc = results["cubic"]["p"]
    rho_c = results["cubic"]["rho"]
    p_spread = max(pc) - min(pc)
    # On the cube, p1=p2=p3 analytically for the continuum/infinite-N limit;
    # lattice_stress on a cube is exactly isotropic by construction of the sum.
    # Require exact equality within float noise relative to |rho|.
    iso_tol = 1e-12 * max(abs(rho_c), 1.0)
    checks.append(
        {
            "name": "cubic_pressure_isotropy",
            "ok": p_spread <= iso_tol,
            "p_spread": p_spread,
            "tol": iso_tol,
            "p": pc,
        }
    )

    # --- Anisotropic pressure response (biaxial + triaxial) ---
    for name in ("biaxial", "triaxial"):
        p = results[name]["p"]
        spread = max(p) - min(p)
        checks.append(
            {
                "name": f"anisotropic_pressure_{name}",
                "ok": spread > 1e-12 * max(abs(x) for x in p + [1e-30]),
                "p_spread": spread,
                "p": p,
            }
        )

    # --- Axis-permutation covariance of stress ---
    # Swap L1↔L2 on triaxial sample: p1↔p2, rho invariant
    L_t = samples["triaxial"]
    base = cbr.lattice_stress(L_t, args.cutoff)
    swapped = cbr.lattice_stress((L_t[1], L_t[0], L_t[2]), args.cutoff)
    perm_rho_err = abs(swapped.rho - base.rho) / max(abs(base.rho), 1e-30)
    perm_p_err = max(
        abs(swapped.p1 - base.p2) / max(abs(base.p2), 1e-30),
        abs(swapped.p2 - base.p1) / max(abs(base.p1), 1e-30),
        abs(swapped.p3 - base.p3) / max(abs(base.p3), 1e-30),
    )
    # Use CBR's own permutation residual scale if available; else float-tight
    perm_ok = perm_rho_err < 1e-12 and perm_p_err < 1e-12
    checks.append(
        {
            "name": "axis_permutation_covariance",
            "ok": perm_ok,
            "rho_rel_err": perm_rho_err,
            "p_rel_err": perm_p_err,
        }
    )

    # --- Uniform-length scaling rho, p ∝ s^{-4} (CBR scaling_test on cubic) ---
    scale = float(args.scale)
    if not math.isfinite(scale) or scale <= 0 or abs(scale - 1.0) < 1e-12:
        scale = 1.7
    sc = cbr.scaling_test(samples["cubic"], args.cutoff, scale=scale)
    # Measured errors must be at floating-point / discrete consistency level.
    # Use the *measured* errors as diagnostics; pass if all relative errors
    # are << 1 (scaling identity holds to better than 0.1% on this tool).
    # Report measured values; threshold taken as max(1e-9, 10 * machine roundoff scale)
    # relative to typical O(1) identities — not a flattering Casimir continuum tol.
    scale_errs = [
        sc["rho_relative_error"],
        sc["pressure_max_relative_error"],
        sc["energy_relative_error"],
    ]
    # Energy scales as s^{-1} in CBR scaling_test (E = V*rho, V~s^3, rho~s^{-4})
    scale_ok = all(e < 1e-9 for e in scale_errs)
    checks.append(
        {
            "name": "uniform_length_scaling_rho_p_s_m4",
            "ok": scale_ok,
            "scale": scale,
            "measured": sc,
            "pass_rule": "CBR-001 scaling_test relative errors each < 1e-9 (tool identity)",
        }
    )

    # --- Multi-cutoff convergence (measured behaviour) ---
    conv = multi_cutoff_table(cbr, samples["cubic"], cutoffs)
    checks.append(
        {
            "name": "multi_cutoff_refinement_improves_successive_change",
            "ok": conv["ok"],
            "first_pair_rel_change": conv["first_pair_rel_change"],
            "final_pair_rel_change": conv["final_pair_rel_change"],
            "monotone_nonincreasing": conv["monotone_nonincreasing_successive_changes"],
            "pass_rule": conv["pass_rule"],
        }
    )

    # --- Malformed input rejection ---
    malformed = run_malformed_controls(cbr)
    checks.append(
        {
            "name": "malformed_input_rejection",
            "ok": all(r["ok"] for r in malformed),
            "cases": malformed,
        }
    )

    # --- Claim firewall ---
    firewall = {
        "physics_pass": False,
        "TOP_research_gate_PASS": False,
        "S_mod_introduced": False,
        "twisted_preference": False,
        "persistent_13_12": False,
        "H0_from_Casimir": False,
        "a0_from_topology": False,
        "Cobs_from_topology": False,
        "cosmology_claim": False,
        "template_PASS_equals_physics_PASS": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )
    checks.append(
        {
            "name": "status_labels_scaffold_only",
            "ok": True,
            "research_gate_status": "OPEN_SCAFFOLD_ONLY",
            "physics_pass": False,
            "note": "subgate template PASS is not TOP physics/gate PASS",
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_TOP001_S2_CBR001_BRIDGE_TEMPLATE"
        if all_ok
        else "FAIL_TOP001_S2_CBR001_BRIDGE"
    )

    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "stage": "S2_CBR001_BRIDGE",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "pass_distinction": {
            "template_or_calculation_PASS": all_ok,
            "TOP_physics_pass": False,
            "TOP_research_gate_PASS": False,
        },
        "parameters": {
            "V": args.V,
            "cutoff": args.cutoff,
            "cutoffs": list(cutoffs),
            "scale": scale,
        },
        "cbr_module": repo_relative(args.cbr_module, args.repo_root),
        "cbr_numerical_authority": "casimir_t3_lattice.lattice_stress",
        "shape_samples": {k: list(v) for k, v in samples.items()},
        "stress_at_primary_cutoff": results,
        "multi_cutoff_convergence": conv,
        "malformed_controls": malformed,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "limitations": [
            "Finite lattice cutoff N; continuum Casimir is extrapolated only diagnostically",
            "Free massless scalar on rectangular T^3 only (CBR-001 Stage-1 authority)",
            "Fixed BC / fixed volume template — no dynamical moduli",
            "No driven anisotropic stress (CBR-002)",
            "No renormalization-scheme comparison beyond CBR-001 tool",
        ],
        "explicit_non_claims": [
            "No TOP research-gate PASS",
            "No physics_pass",
            "No S_mod / dynamical shape potential",
            "No twisted E2/E3 preference",
            "No persistent free-field 13/12 attractor",
            "No H0, a0, Cobs, or cosmology from this bridge",
            "No MAT/UVIR claim upgrade",
        ],
        "scientific_boundary": (
            "Referee-grade scaffold bridging TOP-owned fixed-volume rectangular "
            "T^3 geometry samples into the existing CBR-001 free-scalar Casimir "
            "lattice tool. Free-field anisotropic stress is a mechanism input "
            "only. Template PASS is not TOP physics or research-gate PASS."
        ),
        "next_required": [
            "Author review of measured multi-cutoff table before any freeze language",
            "S_mod only after explicit firewall review of any potential",
            "CBR-002 for driven persistence (not free field)",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "top001_s2_cbr001_bridge_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "top001_s2_cbr001_bridge_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("TOP-001 S2 CBR-001 bridge (hardened)")
    print("  physics_pass: False | research_gate: OPEN_SCAFFOLD_ONLY")
    print("  template/calculation PASS != TOP physics/gate PASS")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
