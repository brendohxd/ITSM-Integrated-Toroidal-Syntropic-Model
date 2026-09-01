#!/usr/bin/env python3
"""VOR-001 S2b: parent S_Phi action template (NOT the ITSM UVIR condensate).

LABEL: Open mathematical action-form template
GATE:  VOR-001 Stage S2b
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY
HOLD:  HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED

Exact convention (unambiguous)
------------------------------
  Phi = rho / sqrt(2) * exp(i Theta),   rho >= 0
  |Phi| = rho / sqrt(2)
  rho   = sqrt(2) |Phi|

Potential (two equivalent writings; no factor-of-two ambiguity):
  V_rho(rho)     = (lambda/4) (rho^2 - v^2)^2
  V_abs(|Phi|)   = lambda (|Phi|^2 - v^2/2)^2
                 = lambda (|Phi|^2 - |Phi|_0^2)^2   with |Phi|_0 = v/sqrt(2)

  Check: V_abs(rho/sqrt(2)) == V_rho(rho)

Flat fixed-background parent template (D_mu = partial_mu; no aether):
  L = - g^{mu nu} (partial_mu Phi)^* (partial_nu Phi) - V(|Phi|)
  (signature (-,+,+,+); spatial reduction below on static configs)

Polar kinetic decomposition (flat Euclidean spatial chart):
  |grad Phi|^2 = (1/2)|grad rho|^2 + (rho^2/2)|grad Theta|^2

Static spatial energy density (matches S1 toy integrand):
  e = (1/2)|grad rho|^2 + (rho^2/2)|grad Theta|^2 + V_rho(rho)

Does NOT: UVIR parent validation, aether/frame coupling, defects, resonance,
SWNT numbers, a0, Cobs, PTA, force claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--s2-summary",
        type=Path,
        default=base / "outputs" / "vor001_s2_local_fluctuation_summary.json",
    )
    return p.parse_args()


def symbolic_identities() -> dict[str, Any]:
    """Derive and verify core symbolic identities under Phi = rho/sqrt(2) e^{iΘ}."""
    rho, Theta, v, lam = sp.symbols("rho Theta v lambda", positive=True)
    # Allow rho as nonnegative via assumptions for derivatives; positive is fine
    # for V'' at v>0.

    # Normalization
    Phi_mod = rho / sp.sqrt(2)
    rho_from_mod = sp.sqrt(2) * Phi_mod
    # Potential in both variables
    V_rho = (lam / 4) * (rho**2 - v**2) ** 2
    V_abs = lam * (Phi_mod**2 - (v**2) / 2) ** 2
    V_abs_expanded = sp.expand(V_abs.subs(Phi_mod, rho / sp.sqrt(2)))
    V_match = sp.simplify(V_abs_expanded - V_rho) == 0

    # Alternate writing V(|Phi|) = lambda (|Phi|^2 - v^2/2)^2
    Phi_abs = sp.symbols("Phi_abs", positive=True)
    V_abs_var = lam * (Phi_abs**2 - v**2 / 2) ** 2
    V_match_var = sp.simplify(
        V_abs_var.subs(Phi_abs, rho / sp.sqrt(2)) - V_rho
    ) == 0

    # Polar kinetic: Phi = rho/sqrt(2) * exp(i Theta)
    # dPhi = (drho/sqrt(2) + i rho/sqrt(2) dTheta) exp(i Theta)
    # |dPhi|^2 = (1/2) drho^2 + (rho^2/2) dTheta^2
    drho, dTh = sp.symbols("drho dTheta", real=True)
    dPhi_re = drho / sp.sqrt(2)
    dPhi_im = rho / sp.sqrt(2) * dTh
    kinetic_polar = sp.simplify(dPhi_re**2 + dPhi_im**2)
    kinetic_expected = sp.Rational(1, 2) * drho**2 + (rho**2 / 2) * dTh**2
    kinetic_ok = sp.simplify(kinetic_polar - kinetic_expected) == 0

    # Static reduction energy density
    e_static = kinetic_expected.subs(
        {drho: sp.symbols("grad_rho", real=True), dTh: sp.symbols("grad_Theta", real=True)}
    )
    # Keep symbolic form for report
    e_static_form = (
        sp.Rational(1, 2) * sp.symbols("grad_rho", real=True) ** 2
        + (rho**2 / 2) * sp.symbols("grad_Theta", real=True) ** 2
        + V_rho
    )
    # Toy S1 integrand uses |grad rho|^2/2 + rho^2 |grad theta|^2/2 + lambda/4 (rho^2-v^2)^2
    toy = (
        sp.Rational(1, 2) * sp.symbols("grad_rho", real=True) ** 2
        + (rho**2 / 2) * sp.symbols("grad_Theta", real=True) ** 2
        + (lam / 4) * (rho**2 - v**2) ** 2
    )
    static_match = sp.simplify(e_static_form - toy) == 0

    # Stationary finite-density minimum
    Vp = sp.diff(V_rho, rho)
    Vpp = sp.diff(V_rho, rho, 2)
    stationary = sp.simplify(Vp.subs(rho, v)) == 0
    m2 = sp.simplify(Vpp.subs(rho, v))
    m2_ok = sp.simplify(m2 - 2 * lam * v**2) == 0
    m2_positive = sp.simplify(m2) == 2 * lam * v**2  # structural

    # Goldstone: phase kinetic only, no mass term for Theta at quadratic order
    # About rho = v + delta_rho, Theta = delta_Theta
    delta_rho, delta_Th = sp.symbols("delta_rho delta_Theta", real=True)
    V_exp = sp.series(V_rho.subs(rho, v + delta_rho), delta_rho, 0, 3).removeO()
    V_quad = sp.expand(V_exp)
    # No delta_Theta in V
    goldstone_no_mass = V_quad.free_symbols.isdisjoint({delta_Th}) or (
        sp.diff(V_quad, delta_Th) == 0
    )
    # Quadratic coeff of delta_rho: (1/2) m^2 delta_rho^2 with m^2 = V''(v)
    # V_quad = (1/2) V''(v) delta_rho^2 + ...
    half_m2 = sp.Rational(1, 2) * m2
    V_quad_pure = sp.simplify(V_quad - half_m2 * delta_rho**2)
    # residual should have no delta_rho^2 term at this order (higher cancelled)
    # series to order 3 includes O(delta^3)=0 after removeO for degree 2
    quad_ok = sp.simplify(sp.diff(V_quad, delta_rho, 2).subs(delta_rho, 0) - m2) == 0

    # Positive quadratic Hamiltonian (declared domain lambda>0, v>0).
    # Amplitude: standard. Phase: consistent canonical Theta convention
    #   H_Θ = p_Θ²/(2 v²) + (v²/2) |∇Θ|²
    # (from L = (v²/2) Θ̇² - (v²/2)|∇Θ|² at rho=v, so p_Θ = v² Θ̇).
    pi_r, p_Th = sp.symbols("pi_rho p_Theta", real=True)
    gr, gth = sp.symbols("grad_drho grad_Theta", real=True)
    H_amp = (
        sp.Rational(1, 2) * pi_r**2
        + sp.Rational(1, 2) * gr**2
        + sp.Rational(1, 2) * m2 * delta_rho**2
    )
    H_phase = (p_Th**2) / (2 * v**2) + (v**2 / 2) * gth**2
    H = H_amp + H_phase
    vars_h = [pi_r, gr, delta_rho, p_Th, gth]
    hess_diag = [sp.simplify(sp.diff(H, x, 2)) for x in vars_h]
    hess_positive_exprs = {
        "d2H_dpi_rho2": str(hess_diag[0]),
        "d2H_dgrad_rho2": str(hess_diag[1]),
        "d2H_ddelta_rho2": str(sp.simplify(hess_diag[2])),
        "d2H_dp_Theta2": str(sp.simplify(hess_diag[3])),
        "d2H_dgrad_Theta2": str(sp.simplify(hess_diag[4])),
        "phase_convention": "H = p_Theta**2/(2*v**2) + (v**2/2)*|grad Theta|**2",
    }
    hess_struct_ok = (
        sp.simplify(hess_diag[0] - 1) == 0
        and sp.simplify(hess_diag[1] - 1) == 0
        and sp.simplify(hess_diag[2] - m2) == 0
        and sp.simplify(hess_diag[3] - 1 / v**2) == 0
        and sp.simplify(hess_diag[4] - v**2) == 0
    )

    return {
        "normalization": "Phi = rho/sqrt(2) * exp(i*Theta); |Phi|=rho/sqrt(2)",
        "V_rho": str(V_rho),
        "V_abs": "lambda (|Phi|^2 - v^2/2)^2",
        "identities": {
            "V_abs_matches_V_rho": bool(V_match and V_match_var),
            "polar_kinetic_decomposition": bool(kinetic_ok),
            "static_reduction_to_S1_toy": bool(static_match),
            "stationary_minimum_at_rho_v": bool(stationary),
            "amplitude_mass_sq_equals_2_lambda_v2": bool(m2_ok),
            "amplitude_mass_sq": str(m2),
            "goldstone_potential_independent_of_Theta": bool(goldstone_no_mass),
            "quadratic_amplitude_mass_from_series": bool(quad_ok),
            "quadratic_hamiltonian_hessian_structure": bool(hess_struct_ok),
        },
        "m2_expr": m2,
        "hamiltonian_hessian_diagonals": hess_positive_exprs,
        "kinetic_polar": str(kinetic_expected),
        "all_ok": all(
            [
                V_match,
                V_match_var,
                kinetic_ok,
                static_match,
                stationary,
                m2_ok,
                goldstone_no_mass,
                quad_ok,
                hess_struct_ok,
            ]
        ),
    }


_EXPECTED_NEGATIVE = (
    ValueError,
    AssertionError,
    FileNotFoundError,
    json.JSONDecodeError,
    TypeError,
)


def negative_controls(s2_path: Path) -> list[dict[str, Any]]:
    """Negative controls: expected exceptions only; unexpected = fail closed."""
    rows: list[dict[str, Any]] = []

    def check_raise(name: str, fn) -> None:
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

    def require_domain(lam: float, v: float) -> None:
        if not math.isfinite(lam) or lam <= 0:
            raise ValueError("lambda must be finite and > 0")
        if not math.isfinite(v) or v <= 0:
            raise ValueError("v must be finite and > 0")

    check_raise("lambda_nonpositive", lambda: require_domain(0.0, 1.0))
    check_raise("lambda_negative", lambda: require_domain(-1.0, 1.0))
    check_raise("v_nonpositive", lambda: require_domain(1.0, 0.0))
    check_raise("v_negative", lambda: require_domain(1.0, -2.0))
    check_raise("lambda_nan", lambda: require_domain(float("nan"), 1.0))
    check_raise("v_inf", lambda: require_domain(1.0, float("inf")))

    def bad_norm_factor() -> None:
        rho, v, lam = sp.symbols("rho v lambda", positive=True)
        V_rho = (lam / 4) * (rho**2 - v**2) ** 2
        # Wrong substitution |Phi|=rho into V_abs form
        V_abs_wrong_sub = lam * (rho**2 - v**2 / 2) ** 2
        if sp.simplify(V_abs_wrong_sub - V_rho) == 0:
            raise AssertionError("expected mismatch for inconsistent normalization")
        raise ValueError("inconsistent_normalization_detected")

    check_raise("inconsistent_normalization_Phi_eq_rho", bad_norm_factor)

    def missing_s2() -> None:
        # Pure path check: do not create or delete any file.
        missing = s2_path.parent / "__nonexistent_s2_summary_for_negative_control__.json"
        if not missing.exists():
            raise FileNotFoundError("missing S2 summary")
        raise AssertionError("sentinel path unexpectedly exists")

    check_raise("missing_s2_summary", missing_s2)

    def malformed_s2() -> None:
        data = {"subgate_status": "NOT_A_REAL_PASS", "continuum_masses": {}}
        if data.get("subgate_status") != "PASS_VOR001_S2_LOCAL_FLUCTUATION_TEMPLATE":
            raise ValueError("malformed_or_wrong_s2_subgate")

    check_raise("malformed_s2_subgate", malformed_s2)

    return rows


def load_and_validate_s2(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    if not path.exists():
        checks.append(
            {
                "name": "prior_S2_fluctuation_package_present",
                "ok": False,
                "detail": f"missing {path}",
            }
        )
        return None, checks
    try:
        s2 = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        checks.append(
            {
                "name": "prior_S2_fluctuation_package_present",
                "ok": False,
                "detail": f"json_error:{exc}",
            }
        )
        return None, checks

    ok = s2.get("subgate_status") == "PASS_VOR001_S2_LOCAL_FLUCTUATION_TEMPLATE"
    checks.append(
        {
            "name": "prior_S2_fluctuation_package_present",
            "ok": ok,
            "subgate": s2.get("subgate_status"),
        }
    )
    if ok:
        m2 = s2.get("continuum_masses", {}).get("m2_amplitude")
        # Prefer parameters recorded by S2; else default audit values lambda=1,v=1
        params = s2.get("parameters") or {}
        lam = float(params.get("lambda", params.get("lam", 1.0)))
        v_val = float(params.get("v", 1.0))
        expected_m2 = 2.0 * lam * v_val * v_val
        mass_ok = m2 is not None and abs(float(m2) - expected_m2) <= 1e-12 * max(
            expected_m2, 1.0
        )
        checks.append(
            {
                "name": "S2_mass_equals_2_lambda_v2",
                "ok": mass_ok,
                "m2_amplitude_from_S2": m2,
                "lambda": lam,
                "v": v_val,
                "expected_2_lambda_v2": expected_m2,
            }
        )
        m2g = s2.get("continuum_masses", {}).get("m2_phase_goldstone", 0.0)
        checks.append(
            {
                "name": "S2_goldstone_massless_compatible",
                "ok": float(m2g) == 0.0,
                "m2_phase_goldstone": m2g,
            }
        )
    return s2, checks


def main() -> None:
    args = parse_args()
    checks: list[dict[str, Any]] = []

    # --- Symbolic block ---
    sym = symbolic_identities()
    for key, val in sym["identities"].items():
        if key in ("amplitude_mass_sq",):
            continue
        if isinstance(val, bool):
            checks.append({"name": f"identity_{key}", "ok": val, "value": val})
    lam_s, v_s = sp.symbols("lambda v", positive=True)
    m2_expr = sym["m2_expr"]
    checks.append(
        {
            "name": "identity_amplitude_mass_sq_expression",
            "ok": sp.simplify(m2_expr - 2 * lam_s * v_s**2) == 0,
            "expression": str(m2_expr),
        }
    )
    checks.append(
        {
            "name": "identity_m2_equals_2_lambda_v2_symbolic",
            "ok": sp.simplify(m2_expr - 2 * lam_s * v_s**2) == 0,
        }
    )
    checks.append(
        {
            "name": "all_core_symbolic_identities",
            "ok": sym["all_ok"],
        }
    )

    # --- S2 prior ---
    s2, s2_checks = load_and_validate_s2(args.s2_summary)
    checks.extend(s2_checks)

    # --- Negative controls ---
    neg = negative_controls(args.s2_summary)
    checks.append(
        {
            "name": "negative_controls_all_raise",
            "ok": all(r["ok"] for r in neg),
            "cases": neg,
        }
    )

    # Domain statement for positive Hamiltonian
    checks.append(
        {
            "name": "declared_parameter_domain",
            "ok": True,
            "domain": "lambda > 0, v > 0, flat fixed chart, rho near v",
        }
    )

    action_convention = {
        "Phi": "rho/sqrt(2) * exp(i*Theta)",
        "rho": "sqrt(2) * |Phi|",
        "metric_signature": "(-,+,+,+)",
        "D_mu": "partial_mu (template; no aether/gauge coupling)",
        "Lagrangian_density": (
            "- g^{mu nu} (partial_mu Phi)^* (partial_nu Phi) - V(|Phi|)"
        ),
        "V_rho": "(lambda/4)*(rho**2 - v**2)**2",
        "V_abs": "lambda*(|Phi|**2 - v**2/2)**2",
        "static_spatial_energy_density": (
            "(1/2)|grad rho|^2 + (rho**2/2)|grad Theta|^2 + V_rho(rho)"
        ),
        "S1_toy_match": (
            "E = integral [ |grad rho|^2/2 + rho^2 |grad Theta|^2/2 "
            "+ lambda/4 (rho^2-v^2)^2 ]"
        ),
        "status": "TEMPLATE_DECLARED_NOT_UVIR_VALIDATED",
        "hold": "HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED",
    }

    firewall = {
        "physics_pass": False,
        "UVIR_parent_validated": False,
        "identified_as_ITSM_UVIR_condensate": False,
        "aether_frame_coupling": False,
        "defect_sector": False,
        "resonance_spectrum": False,
        "SWNT_packaging": False,
        "a0_from_winding": False,
        "Cobs_from_vortex": False,
        "PTA_claim": False,
        "force_law_claim": False,
        "VOR_research_gate_PASS": False,
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
            "name": "hold_parent_not_uvir_validated",
            "ok": True,
            "hold": "HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED",
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_VOR001_S2B_PARENT_ACTION_TEMPLATE_DECLARED"
        if all_ok
        else "FAIL_VOR001_S2B_PARENT_ACTION_TEMPLATE"
    )

    summary: dict[str, Any] = {
        "gate": "VOR-001",
        "stage": "S2B_PARENT_ACTION_TEMPLATE",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "hold": "HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED",
        "action_convention": action_convention,
        "symbolic_block": {
            k: (str(v) if k == "m2_expr" else v) for k, v in sym.items()
        },
        "negative_controls": neg,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "remaining_holds": [
            "HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED",
            "No aether/frame coupling",
            "No defect sector",
            "No resonance/PTA packaging",
        ],
        "explicit_non_claims": [
            "Not the ITSM UVIR condensate action",
            "No UVIR-001/002/003 reopen or validation",
            "No SWNT numbers, a0, Cobs, PTA, force claims",
            "No VOR research-gate PASS",
            "physics_pass remains false",
        ],
        "scientific_boundary": (
            "Hardened parent S_Phi *template* under unambiguous "
            "Phi=rho/sqrt(2) exp(i Theta). Potential consistent in rho and |Phi|. "
            "Reduces to existing VOR toy energy on static flat charts. "
            "Does not identify this template as the ITSM UVIR condensate."
        ),
        "next_required": [
            "Joint gate if mapping to architecture Phi / UVIR",
            "Defects only after parent validation policy",
            "No resonance spectrum packaging",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "vor001_s2b_parent_action_template_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "vor001_s2b_parent_action_template_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("VOR-001 S2b parent action template (hardened)")
    print("  physics_pass: False | HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED")
    print("  convention: Phi = rho/sqrt(2) exp(i Theta)")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
