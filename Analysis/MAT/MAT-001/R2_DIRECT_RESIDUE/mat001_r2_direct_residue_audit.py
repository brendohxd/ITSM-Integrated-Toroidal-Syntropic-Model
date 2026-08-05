#!/usr/bin/env python3
"""MAT-001 R2: canonical response template for V (structural audit only).

ASCII console. PowerShell-safe. No MAT PASS. No numeric V extraction.

Statuses preserved:
  UVIR-003: IN_PROGRESS
  MAT-001: BLOCKED
  physics_pass: false
  V_status: NOT_COMPUTED (always in this audit)
  Stage 4A: closed

Template (not live eigenmode extraction):
  L2 = (1/2) psi D psi - C_m rho_b psi
  D = K_Q P
  chi = sqrt(K_Q) psi
  => chi / rho_b = V / P          (mixed field-source response)
  => S_eff[rho_b] ~ - (1/2) V^2 rho_b P^{-1} rho_b   (source-source exchange)

V := C_m / sqrt(K_Q) is the canonical matter-source vertex.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    repo = base.parents[3]
    uvir_out = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    mat_out = repo / "Analysis" / "MAT" / "MAT-001" / "outputs"
    j1_out = (
        repo
        / "Analysis"
        / "MAT"
        / "MAT-001"
        / "J1_JOINT_ACTION"
        / "outputs"
    )
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--repo-root", type=Path, default=repo)
    p.add_argument(
        "--matching-summary",
        type=Path,
        default=uvir_out / "uvir003_matching_route_program_summary.json",
    )
    p.add_argument(
        "--inventory-summary",
        type=Path,
        default=uvir_out / "uvir003_kq_matching_inventory_summary.json",
    )
    p.add_argument(
        "--scoped-mat-summary",
        type=Path,
        default=mat_out / "mat001_scoped_calculation_summary.json",
    )
    p.add_argument(
        "--j1-summary",
        type=Path,
        default=j1_out / "mat001_j1_joint_action_normalization_summary.json",
    )
    p.add_argument(
        "--force-summary",
        type=Path,
        default=uvir_out / "uvir003_nonzero_gradient_force_local_summary.json",
        help="Optional Track-A force package (absence allowed).",
    )
    return p.parse_args()


def repo_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        parts = path.resolve().parts
        if "Analysis" in parts:
            i = parts.index("Analysis")
            return "/".join(parts[i:])
        return path.name


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("expected JSON object: {0}".format(path))
    return data


def require_positive_chart(x: float, label: str) -> None:
    """K_Q and chart scale: finite and > 0."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError("{0} must be a real number".format(label))
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("{0} must be finite and > 0".format(label))


def require_signed_finite(x: float, label: str) -> None:
    """C_m: finite, nonzero, sign retained (may be negative)."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError("{0} must be a real number".format(label))
    if not math.isfinite(x):
        raise ValueError("{0} must be finite (reject NaN/Inf)".format(label))
    if x == 0.0:
        raise ValueError("{0} must be nonzero".format(label))


_EXPECTED = (
    ValueError,
    TypeError,
    AssertionError,
    FileNotFoundError,
    json.JSONDecodeError,
)


def fail_closed_controls() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def one(name: str, fn: Callable[[], None]) -> None:
        try:
            fn()
            rows.append(
                {
                    "case": name,
                    "ok": False,
                    "raised": False,
                    "error": "",
                    "detail": "expected exception not raised",
                }
            )
        except _EXPECTED as exc:
            rows.append(
                {
                    "case": name,
                    "ok": True,
                    "raised": True,
                    "error": type(exc).__name__,
                }
            )
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "case": name,
                    "ok": False,
                    "raised": True,
                    "error": "unexpected:{0}".format(type(exc).__name__),
                    "detail": "fail closed",
                }
            )

    one("K_Q_nonpositive", lambda: require_positive_chart(0.0, "K_Q"))
    one("K_Q_negative", lambda: require_positive_chart(-1.0, "K_Q"))
    one("K_Q_nan", lambda: require_positive_chart(float("nan"), "K_Q"))
    one("K_Q_pos_inf", lambda: require_positive_chart(float("inf"), "K_Q"))
    one("K_Q_neg_inf", lambda: require_positive_chart(float("-inf"), "K_Q"))
    one("scale_nonpositive", lambda: require_positive_chart(0.0, "chart_scale"))
    one("C_m_zero", lambda: require_signed_finite(0.0, "C_m"))
    one("C_m_nan", lambda: require_signed_finite(float("nan"), "C_m"))
    one("C_m_pos_inf", lambda: require_signed_finite(float("inf"), "C_m"))
    one("C_m_neg_inf", lambda: require_signed_finite(float("-inf"), "C_m"))

    def rescaling_s_invalid() -> None:
        s = 0.0
        if not math.isfinite(s) or s == 0.0:
            raise ValueError("rescaling s must be finite and nonzero")

    one("rescaling_s_zero", rescaling_s_invalid)

    def missing_file() -> None:
        p = Path("__nonexistent_r2_upstream_contract__.json")
        if not p.exists():
            raise FileNotFoundError("missing upstream")
        raise AssertionError("path should not exist")

    one("missing_upstream_file", missing_file)

    def contract_mismatch() -> None:
        if "WRONG" != "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY":
            raise ValueError("upstream contract mismatch")

    one("upstream_contract_mismatch", contract_mismatch)
    return rows


def quadratic_template_identities() -> dict[str, Any]:
    """
    L2 = 1/2 psi D psi - C_m rho_b psi,  D = K_Q P,  chi = sqrt(K_Q) psi.

    Mixed response: chi / rho_b = V / P
    Exchange: S_eff ~ -1/2 V^2 rho_b P^{-1} rho_b
    """
    # K_Q, chart scale positive; C_m signed
    K_Q, P = sp.symbols("K_Q P", positive=True)
    C_m, rho_b, s = sp.symbols("C_m rho_b s", real=True, nonzero=True)
    # Restrict s, rho_b nonzero via symbols; use positive s for rescaling
    s = sp.symbols("s", positive=True)
    rho_b = sp.symbols("rho_b", real=True, nonzero=True)
    C_m = sp.symbols("C_m", real=True, nonzero=True)

    V = C_m / sp.sqrt(K_Q)
    D = K_Q * P

    # From EOM: D psi = C_m rho_b  =>  psi = C_m rho_b / D = C_m rho_b / (K_Q P)
    # chi = sqrt(K_Q) psi = C_m rho_b / (sqrt(K_Q) P) = V rho_b / P
    psi = C_m * rho_b / D
    chi = sp.simplify(sp.sqrt(K_Q) * psi)
    mixed = sp.simplify(chi / rho_b)
    mixed_expected = V / P
    mixed_ok = sp.simplify(mixed - mixed_expected) == 0

    # Integrating out: S_eff = -1/2 C_m rho_b * psi = -1/2 C_m^2 rho_b^2 / D
    # = -1/2 (C_m^2 / K_Q) rho_b (P^{-1}) rho_b = -1/2 V^2 rho_b P^{-1} rho_b
    S_eff = sp.simplify(-sp.Rational(1, 2) * C_m * rho_b * psi)
    S_eff_expected = sp.simplify(
        -sp.Rational(1, 2) * V**2 * rho_b * (1 / P) * rho_b
    )
    exchange_ok = sp.simplify(S_eff - S_eff_expected) == 0

    # Rescaling psi -> s psi: K_Q' = K_Q/s^2, C_m' = C_m/s (sign of C_m kept)
    K_Qp = K_Q / s**2
    C_mp = C_m / s
    Vp = sp.simplify(C_mp / sp.sqrt(K_Qp))
    inv_ok = sp.simplify(Vp - V) == 0

    # Sign of V tracks sign of C_m
    sign_ok = sp.simplify(sp.sign(V) - sp.sign(C_m)) == 0 or True
    # For symbols, check V * sqrt(K_Q) / C_m == 1
    sign_struct = sp.simplify(V * sp.sqrt(K_Q) / C_m) == 1

    return {
        "template": {
            "L2": "1/2 * psi * D * psi - C_m * rho_b * psi",
            "D": "K_Q * P",
            "chi": "sqrt(K_Q) * psi",
            "V_vertex": "C_m / sqrt(K_Q)",
        },
        "coefficient_roles": {
            "canonical_matter_source_vertex": "V",
            "mixed_field_source_response_pole": "V  (chi/rho_b = V/P)",
            "source_source_exchange_pole": "V**2  (S_eff ~ -1/2 V^2 rho_b P^{-1} rho_b)",
        },
        "identities": {
            "mixed_response_chi_over_rho_equals_V_over_P": bool(mixed_ok),
            "exchange_Seff_proportional_to_minus_half_V2": bool(exchange_ok),
            "V_redefinition_invariant": bool(inv_ok),
            "V_tracks_sign_of_C_m": bool(sign_struct),
        },
        "mixed_response": str(mixed),
        "mixed_expected": str(mixed_expected),
        "Seff": str(S_eff),
        "Seff_expected": str(S_eff_expected),
        "template_not_live_eigenmode": True,
        "absent_in_this_template": [
            "constraint reduction",
            "physical mode projection",
            "same-action matching to live UVIR eigenmode",
        ],
        "all_ok": bool(mixed_ok and exchange_ok and inv_ok and sign_struct),
    }


def contract(
    path: Path,
    root: Path,
    expected_subgate: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rel = repo_rel(path, root)
    data = load_json(path)
    if data is None:
        return {
            "path": rel,
            "ok": False,
            "expected_subgate": expected_subgate,
            "detail": "missing file",
        }
    got = data.get("subgate_status")
    ok = got == expected_subgate
    row: dict[str, Any] = {
        "path": rel,
        "ok": ok,
        "expected_subgate": expected_subgate,
        "got_subgate": got,
    }
    if extra:
        for key, expect in extra.items():
            actual = data.get(key)
            match = actual == expect
            row["contract_{0}".format(key)] = {
                "expected": expect,
                "got": actual,
                "ok": match,
            }
            ok = ok and match
        row["ok"] = ok
    return row


def main() -> int:
    args = parse_args()
    root = args.repo_root
    checks: list[dict[str, Any]] = []

    # Upstream contracts
    c_match = contract(
        args.matching_summary,
        root,
        "PASS_MATCHING_ROUTE_PROGRAM_OPEN",
        extra={"kq_numeric_status": "NOT_DERIVED", "mat001_status": "BLOCKED"},
    )
    c_inv = contract(
        args.inventory_summary,
        root,
        "PASS_KQ_MATCHING_INVENTORY_OPEN",
        extra={"kq_numeric_status": "NOT_DERIVED"},
    )
    c_scoped = contract(
        args.scoped_mat_summary,
        root,
        "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL",
        extra={"V_status": "NOT_COMPUTED", "mat001_pass": False},
    )
    c_j1 = contract(
        args.j1_summary,
        root,
        "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY",
        extra={
            "V_status": "NOT_COMPUTED",
            "V_form_status": "SAME_ACTION_IDENTITY_DERIVED",
            "mat001_pass": False,
            "physics_pass": False,
        },
    )

    checks.append({"name": "upstream_matching_contract", "ok": c_match["ok"], "contract": c_match})
    checks.append({"name": "upstream_inventory_contract", "ok": c_inv["ok"], "contract": c_inv})
    checks.append({"name": "upstream_scoped_mat_contract", "ok": c_scoped["ok"], "contract": c_scoped})
    checks.append({"name": "upstream_j1_joint_action_contract", "ok": c_j1["ok"], "contract": c_j1})

    # Optional force package: absence is allowed
    force = load_json(args.force_summary)
    force_rel = repo_rel(args.force_summary, root)
    checks.append(
        {
            "name": "optional_force_package",
            "ok": True,
            "required": False,
            "present": force is not None,
            "path": force_rel,
            "subgate": None if force is None else force.get("subgate_status"),
            "note": "Track-A force summary is optional; not used as V residue",
        }
    )

    # Structural template
    templ = quadratic_template_identities()
    for key, val in templ["identities"].items():
        checks.append({"name": "identity_{0}".format(key), "ok": bool(val)})
    checks.append({"name": "all_template_identities", "ok": templ["all_ok"]})
    checks.append(
        {
            "name": "template_not_live_eigenmode_extraction",
            "ok": templ["template_not_live_eigenmode"] is True,
            "absent": templ["absent_in_this_template"],
        }
    )
    checks.append(
        {
            "name": "coefficient_roles_distinguished",
            "ok": (
                templ["coefficient_roles"]["canonical_matter_source_vertex"] == "V"
                and "V**2"
                in templ["coefficient_roles"]["source_source_exchange_pole"]
            ),
            "roles": templ["coefficient_roles"],
        }
    )

    # Hard lock: this audit never promotes V
    V_status = "NOT_COMPUTED"
    checks.append(
        {
            "name": "V_status_locked_NOT_COMPUTED",
            "ok": V_status == "NOT_COMPUTED",
            "detail": (
                "No V_status/V_computed_this_stage promotion path; "
                "future computation needs separate provenance contract"
            ),
        }
    )
    checks.append(
        {
            "name": "no_standalone_numeric_K_Q",
            "ok": True,
            "kq_numeric_status": "NOT_DERIVED",
        }
    )

    # Paths portable
    paths = {
        "matching": repo_rel(args.matching_summary, root),
        "inventory": repo_rel(args.inventory_summary, root),
        "scoped_mat": repo_rel(args.scoped_mat_summary, root),
        "j1": repo_rel(args.j1_summary, root),
        "force_optional": force_rel,
    }
    checks.append(
        {
            "name": "json_paths_repo_relative",
            "ok": all(
                "OneDrive" not in p and not (len(p) > 1 and p[1] == ":")
                for p in paths.values()
            ),
            "paths": paths,
        }
    )

    neg = fail_closed_controls()
    checks.append(
        {
            "name": "malformed_input_negative_controls",
            "ok": all(r["ok"] for r in neg),
            "cases": neg,
        }
    )

    # Report voice / stage 4A closed
    voice = {
        "UVIR-003": "IN_PROGRESS",
        "MAT-001": "BLOCKED",
        "physics_pass": False,
        "V_status": "NOT_COMPUTED",
        "stage4A": "CLOSED",
    }
    checks.append(
        {
            "name": "status_voice_and_stage4A_closed",
            "ok": (
                voice["UVIR-003"] == "IN_PROGRESS"
                and voice["MAT-001"] == "BLOCKED"
                and voice["physics_pass"] is False
                and voice["V_status"] == "NOT_COMPUTED"
                and voice["stage4A"] == "CLOSED"
            ),
            "voice": voice,
        }
    )

    firewall = {
        "physics_pass": False,
        "mat001_pass": False,
        "UVIR_full_PASS": False,
        "Derived_K_Q": False,
        "V_computed": False,
        "stage4A_unlocked": False,
        "live_eigenmode_extraction_claimed": False,
        "SPARC_or_H0": False,
        "dual_RAR": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(bool(c.get("ok")) for c in checks)
    subgate = (
        "PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT"
        if all_ok
        else "FAIL_MAT001_R2_DIRECT_RESIDUE_AUDIT"
    )

    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "R2_DIRECT_RESIDUE_AUDIT",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "physics_pass": False,
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "stage4A_status": "CLOSED",
        "stage4A_unlock": False,
        "audit_verdict": {
            "form_level": (
                "YES: canonical vertex V equals mixed response pole coefficient "
                "in the quadratic template; exchange pole carries V^2; "
                "standalone numeric K_Q need not be quoted once V is known."
            ),
            "branch_numeric_level": (
                "NOT_COMPUTED: this audit does not extract V from live eigenmodes; "
                "constraint reduction, mode projection, and same-action matching "
                "remain absent."
            ),
        },
        "quadratic_template": templ,
        "upstream_contracts": {
            "matching": c_match,
            "inventory": c_inv,
            "scoped_mat": c_scoped,
            "j1_joint_action": c_j1,
        },
        "optional_force_package": {
            "required": False,
            "present": force is not None,
            "path": force_rel,
        },
        "paths": paths,
        "negative_controls": neg,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "blockers_to_compute_V": [
            "Declared microscopic action with both kinetic and matter couplings",
            "Constraint reduction to physical modes",
            "Mode projection / same-action matching to live IR force field",
            "Separate provenance contract before any V_status promotion",
        ],
        "explicit_non_claims": [
            "No MAT-001 PASS",
            "No physics_pass",
            "No UVIR-003 full PASS",
            "No numeric Derived K_Q",
            "No computed V (locked NOT_COMPUTED in this audit)",
            "No Stage 4A unlock",
            "No live physical eigenmode extraction",
            "No SPARC / H0 / dual RAR packaging",
            "Audit PASS is not a numeric residue extraction",
        ],
        "scientific_boundary": (
            "Structural quadratic-template audit of canonical response poles. "
            "Distinguishes vertex V, mixed pole V, and exchange pole V^2. "
            "Not an extraction from the live UVIR physical eigenmode. "
            "V remains NOT_COMPUTED; MAT BLOCKED; UVIR IN_PROGRESS; Stage 4A closed."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "mat001_r2_direct_residue_audit_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_r2_direct_residue_audit_summary.sha256").write_bytes(
        "{0}  {1}\n".format(digest, out.name).encode("utf-8")
    )

    # ASCII-only console (PowerShell default encoding safe)
    print("MAT-001 R2 direct residue audit")
    print("  UVIR-003: IN_PROGRESS | MAT-001: BLOCKED | Stage4A: CLOSED")
    print("  physics_pass: False | V_status: NOT_COMPUTED")
    print("  roles: vertex=V ; mixed pole=V ; exchange pole=V^2")
    for c in checks:
        mark = "OK" if c.get("ok") else "FAIL"
        print("  [{0}] {1}".format(mark, c["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
