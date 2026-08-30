#!/usr/bin/env python3
"""MAT-001 M2 cheap radial/heavy-mode matching screen.

Tests the live source inventory and two minimal quadratic ways a heavy
condensate amplitude could communicate with a massless force scalar.  The
tested candidate classes are controls, not additions to the canonical action.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check(rows: list[dict[str, Any]], name: str, passed: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(passed), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "force_hosting": ROOT / "Analysis/MAT/MAT-001/FORCE_HOSTING/outputs/mat001_force_hosting_readiness_summary.json",
        "live_export": ROOT / "Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/outputs/mat001_live_uvir_export_inventory_summary.json",
        "r3_matter": ROOT / "Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/outputs/mat001_r3_covariant_matter_action_summary.json",
        "parent_condensate": ROOT / "Analysis/UVIR/UVIR-003/outputs/uvir003_nonlinear_adm_action_provenance_summary.json",
    }
    data = {name: load(path) for name, path in inputs.items()}
    checks: list[dict[str, Any]] = []
    check(checks, "live_force_host_has_no_matter_vertex", data["force_hosting"].get("hosting_status") == "NO_LIVE_HOST_READY_FOR_S_INT")
    check(checks, "live_same_chart_bundle_absent", data["live_export"].get("live_action_export_status") == "PARTIAL_NOT_SAME_CHART")
    r3_action = data["r3_matter"].get("action_freeze", {})
    r3_firewall = data["r3_matter"].get("status_firewall", {})
    check(
        checks,
        "declared_matter_action_targets_force_scalar_not_radial_mode",
        "A(psi)" in str(r3_action.get("matter_metric"))
        and "rho" not in str(r3_action.get("matter_metric"))
        and r3_firewall.get("V_computed") is False,
        matter_metric=r3_action.get("matter_metric"),
    )

    # Four-dimensional natural-unit dimensions.
    dims = {"sigma": 1, "psi": 1, "T": 4, "p2": 2, "Z_sigma": 0, "Z_psi": 0, "m": 1, "eta": 0, "mu": 2, "g_sigma": -1, "g_psi": -1}
    check(checks, "mass_dimensions_close", dims["g_sigma"] + dims["sigma"] + dims["T"] == 4 and dims["mu"] + dims["sigma"] + dims["psi"] == 4 and dims["eta"] + 1 + dims["sigma"] + 1 + dims["psi"] == 4, dimensions=dims)

    p2, m2, Zs, Zp = sp.symbols("p2 m_sigma_sq Z_sigma Z_psi", positive=True)
    eta = sp.symbols("eta", real=True)
    mu = sp.symbols("mu_mix", real=True)
    gs, gp = sp.symbols("g_sigma g_psi", real=True)
    Ds = Zs * (p2 + m2)

    # Candidate D: derivative mixing eta * d sigma . d psi. It preserves a
    # massless psi at p2=0, but the induced matter vertex vanishes as p2.
    mix_d = eta * p2
    Dp_d = sp.simplify(Zp * p2 - mix_d**2 / Ds)
    geff_d = sp.simplify(-mix_d * gs / Ds)
    response_d = sp.simplify(-geff_d / Dp_d)
    soft_vertex_d = sp.limit(geff_d, p2, 0, dir="+")
    soft_response_d = sp.limit(response_d, p2, 0, dir="+")
    check(checks, "derivative_mixing_has_no_soft_source_pole", soft_vertex_d == 0 and not soft_response_d.has(sp.zoo), soft_vertex=str(soft_vertex_d), soft_response=str(soft_response_d))

    # Candidate M: nonderivative mixing. It removes the massless pole unless a
    # bare psi mass counterterm is tuned to cancel the induced mass.
    Dp_m = sp.simplify(Zp * p2 - mu**2 / Ds)
    geff_m = sp.simplify(-mu * gs / Ds)
    Dp_m_zero = sp.simplify(Dp_m.subs(p2, 0))
    check(checks, "mass_mixing_lifts_massless_force_mode", Dp_m_zero != 0, induced_zero_momentum_operator=str(Dp_m_zero))
    tuned_counterterm = sp.simplify(mu**2 / (Zs * m2))
    Dp_tuned = sp.simplify(Dp_m + tuned_counterterm)
    z_eff = sp.limit(Dp_tuned / p2, p2, 0, dir="+")
    g_eff_soft = sp.limit(geff_m, p2, 0, dir="+")
    residue_tuned = sp.simplify(g_eff_soft / sp.sqrt(z_eff))
    free_symbols = sorted(str(x) for x in residue_tuned.free_symbols)
    check(checks, "tuned_massless_residue_remains_independent_wilson_combination", set(residue_tuned.free_symbols) >= {mu, gs, Zs, m2, Zp}, counterterm=str(tuned_counterterm), Z_eff=str(z_eff), g_eff_soft=str(g_eff_soft), g_phys_over_sqrt_Z=str(residue_tuned), free_symbols=free_symbols)

    # Direct force-scalar matter coupling supplies a pole but is exactly the
    # independent coupling M2 was supposed to derive.
    direct_residue = sp.simplify(gp / sp.sqrt(Zp))
    check(checks, "direct_force_vertex_is_not_derived_by_radial_integration", direct_residue.free_symbols == {gp, Zp}, direct_residue=str(direct_residue))

    # Exact uncoupled limit.
    uncoupled = [sp.simplify(x.subs({eta: 0, mu: 0, gs: 0, gp: 0})) for x in (geff_d, geff_m, direct_residue)]
    check(checks, "regular_uncoupled_limit", uncoupled == [0, 0, 0], values=[str(x) for x in uncoupled])

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "MAT001_M2_RADIAL_HEAVY_MODE_REDUCTION",
        "calculation_status": "PASS_CHEAP_SYMBOLIC_SCREEN" if all_ok else "FAIL_PIPELINE",
        "route_disposition": "REJECT_MINIMAL_M2_CLASSES_SOFT_RESIDUE_NOT_DERIVED" if all_ok else "HOLD_PIPELINE_FAILURE",
        "live_action_result": "STATIC_RADIAL_MATTER_SOURCE_ABSENT",
        "candidate_action_results": {
            "derivative_mixing": "NO_LONG_RANGE_SOURCE_POLE",
            "mass_mixing": "LIFTS_MASSLESS_MODE_UNLESS_TUNED",
            "tuned_mass_mixing": "LONG_RANGE_RESIDUE_DEPENDS_ON_INDEPENDENT_WILSON_COMBINATION",
            "direct_psi_matter_vertex": "INDEPENDENT_INPUT_NOT_RADIAL_DERIVATION",
        },
        "V_status": "NOT_COMPUTED",
        "K_Q_status": "NOT_DERIVED",
        "MAT_001_status": "BLOCKED",
        "physics_pass": False,
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "This is a quadratic soft-limit no-go for the live source inventory and the two minimal radial-to-force mixing classes tested. It is not a theorem against every nonlinear, symmetry-locked or multi-field UV completion.",
    }
    json_path = OUT / "mat001_m2_radial_heavy_reduction_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# MAT-001 M2 radial/heavy-mode reduction

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**MAT-001:** `BLOCKED` · **V:** `NOT_COMPUTED` · **K_Q:** `NOT_DERIVED`

## Result

The live parent contains the finite-density condensate amplitude, but its
declared matter action couples to the separate force scalar and does not export
a radial-mode matter source in the live same-chart quadratic bundle. The live
M2 route therefore hits its first kill criterion: the required static radial
source is absent.

Two minimal controlled extensions were tested without empirical inputs.
Derivative mixing preserves a massless force mode but makes the induced soft
matter vertex vanish as momentum squared, leaving only a contact response.
Nonderivative mixing lifts the massless force mode. Tuning a counterterm to
restore it produces

`g_phys/sqrt(Z_phys) = {residue_tuned}`,

which retains independent `mu_mix`, `g_sigma`, `Z_sigma`, `m_sigma_sq` and
`Z_psi`. A direct force-scalar matter vertex gives `{direct_residue}`, which is
an input rather than a radial-mode prediction.

This rejects the tested minimal M2 action classes as a derivation of `V`. It
does not reject every possible symmetry-locked nonlinear completion.
"""
    report_path = OUT / "MAT-001_M2_RADIAL_HEAVY_REDUCTION.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "mat001_m2_radial_heavy_reduction.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
