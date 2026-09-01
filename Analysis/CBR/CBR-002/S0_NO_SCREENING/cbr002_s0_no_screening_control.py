#!/usr/bin/env python3
"""CBR-002 S0 unscreened cubic-force null control.

Propagates the exact isolated spherical static scaling while keeping the
invariant coupling C_obs symbolic.  It explicitly refuses to identify a force
ratio with PPN, laboratory, radiation, or strong-field observables that the
current action has not derived.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"

G = 6.67430e-11
M_SUN = 1.98847e30
AU = 149_597_870_700.0
A0_CONTROL = 1.2e-10


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def add_check(rows: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def benchmark(name: str, domain: str, mass_kg: float, radius_m: float, validity: str) -> dict[str, Any]:
    g_n = G * mass_kg / radius_m**2
    r_m = math.sqrt(G * mass_kg / A0_CONTROL)
    unit_ratio = math.sqrt(A0_CONTROL / g_n)
    return {
        "name": name,
        "domain": domain,
        "mass_kg": mass_kg,
        "radius_m": radius_m,
        "g_N_m_s2": g_n,
        "MOND_radius_m": r_m,
        "a5_over_aN_per_unit_C_obs": unit_ratio,
        "failure_condition_for_fractional_limit_epsilon": f"abs(C_obs) > epsilon/{unit_ratio:.12g}",
        "validity": validity,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "core_architecture": ROOT / "Theory/Core/ITSM_Core_Architecture.md",
        "solar_bound": ROOT / "Theory/Gates/CBR-002/SOLAR_SYSTEM_BOUND.md",
        "recovery_plan": ROOT / "Theory/Core/ITSM_Core_Recovery_Plan.md",
        "tier1_programme": ROOT / "Theory/Core/ITSM_Tier1_Route_Test_Programme.md",
    }
    text = {name: path.read_text(encoding="utf-8") for name, path in inputs.items()}
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "canonical_invariant_force_law_present",
        "C_obs = C_m^(3/2) / sqrt(C_IR)" in text["core_architecture"]
        and "g_P = C_obs sqrt(a0 g_N)" in text["core_architecture"],
    )
    add_check(
        checks,
        "force_ratio_not_misidentified_as_ppn",
        "not itself $|\\gamma-1|$" in text["solar_bound"],
    )
    add_check(
        checks,
        "like_for_like_requirement_present",
        "Validate against ephemerides" in text["recovery_plan"]
        and "binary dynamics rather than comparing" in text["recovery_plan"],
    )
    add_check(
        checks,
        "s0_scope_present",
        "S0 | No-screening control" in text["tier1_programme"],
    )

    rows = [
        benchmark("Sun at 1 AU", "solar_system", M_SUN, AU, "STATIC_ISOLATED_SPHERICAL_FORCE_RATIO_ONLY"),
        benchmark("Earth surface", "solar_system", 5.9722e24, 6.371e6, "STATIC_ISOLATED_SPHERICAL_FORCE_RATIO_ONLY"),
        benchmark("1 kg source at 0.1 m", "laboratory", 1.0, 0.1, "CONDITIONAL_ISOLATED_SOURCE; EXTERNAL_FIELD_AND_APPARATUS_BVP_OMITTED"),
        benchmark("1.4 Msun binary scale at 1e9 m", "pulsar", 1.4 * M_SUN, 1.0e9, "WEAK_FIELD_STATIC_RATIO_ONLY; RADIATION_AND_SENSITIVITIES_OMITTED"),
        benchmark("1.4 Msun object at 12 km", "compact_object", 1.4 * M_SUN, 12_000.0, "OUTSIDE_DERIVED_WEAK_FIELD_DOMAIN; BENCHMARK_ONLY"),
    ]
    solar_ratio = rows[0]["a5_over_aN_per_unit_C_obs"]
    add_check(checks, "sun_1au_reproduces_bounded_diagnostic", abs(solar_ratio - 1.4e-4) < 5e-6, ratio=solar_ratio)
    add_check(checks, "all_benchmark_ratios_finite_positive", all(math.isfinite(r["a5_over_aN_per_unit_C_obs"]) and r["a5_over_aN_per_unit_C_obs"] > 0 for r in rows))

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "CBR002_S0_NO_SCREENING_CONTROL",
        "calculation_status": "PASS_STATIC_NULL_CONTROL" if all_ok else "FAIL_PIPELINE",
        "route_disposition": "REJECT_S0_AS_COMPLETE_LOCAL_GRAVITY_ROUTE" if all_ok else "HOLD_PIPELINE_FAILURE",
        "exact_static_spherical_relations": {
            "force": "g_P = C_obs*sqrt(a0*g_N)",
            "ratio": "g_P/g_N = C_obs*sqrt(a0/g_N) = C_obs*r/r_M",
            "r_M": "sqrt(G*M/a0)",
            "failure_domain_for_like_for_like_fractional_limit_epsilon": "abs(C_obs) > epsilon*sqrt(g_N/a0) = epsilon*r_M/r",
        },
        "control_inputs": {
            "G_m3_kg_s2": G,
            "a0_m_s2": A0_CONTROL,
            "a0_status": "DIAGNOSTIC_CONTROL_VALUE_NOT_DERIVED_BY_MAT_001",
            "M_sun_kg": M_SUN,
            "AU_m": AU,
        },
        "domain_results": {
            "solar_system": "NONZERO_FORCE_RATIO_EXPOSED; PPN_AND_EPHEMERIS_OBSERVABLES_NOT_DERIVED",
            "laboratory": "ISOLATED_SOURCE_SCALING_EXPOSED; NONLINEAR_EXTERNAL_FIELD_AND_APPARATUS_SOLUTION_NOT_DERIVED",
            "pulsar": "STATIC_WEAK_FIELD_SCALING_EXPOSED; DIPOLE_RADIATION_AND_STRONG_FIELD_SENSITIVITIES_NOT_DERIVED",
            "compact_object": "WEAK_FIELD_SCALING_CANNOT_BE_EXTRAPOLATED_AS_A_STRONG_FIELD_PREDICTION",
        },
        "like_for_like_observational_pass": False,
        "screening_mechanism_imported": False,
        "C_obs_status": "NOT_DERIVED",
        "MAT_001_status": "BLOCKED",
        "SCR_001_status": "NOT_OPENED_BY_THIS_CONTROL",
        "physics_pass": False,
        "benchmarks": rows,
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "The exact isolated spherical cubic-force ratio is a null-control prediction. It is not a PPN parameter, an ephemeris residual, a laboratory apparatus solution, a pulsar radiation calculation, or a compact-object solution. S0 therefore cannot establish observational compliance and does not select any screening mechanism.",
    }

    json_path = OUT / "cbr002_s0_no_screening_control_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    csv_path = OUT / "cbr002_s0_no_screening_benchmarks.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    report = f"""# CBR-002 S0 no-screening control

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**Physics pass:** `false` · **MAT-001:** `BLOCKED`

## Exact bounded result

The unscreened standalone cubic branch gives

`g_P/g_N = C_obs sqrt(a0/g_N) = C_obs r/r_M`.

For any like-for-like fractional-force limit `epsilon`, this branch fails when

`abs(C_obs) > epsilon sqrt(g_N/a0) = epsilon r_M/r`.

Using `a0={A0_CONTROL:.3g} m/s^2` only as a diagnostic control value, the Sun
at 1 AU gives `{solar_ratio:.6g} * C_obs`. This reproduces the repository's
force-ratio diagnostic. It is not `gamma_PPN-1` and is not a Cassini verdict.

## Domain audit

- Solar System: the nonzero force ratio is exposed, but the physical metric,
  PPN parameters, Shapiro delay and ephemeris residuals are absent.
- Laboratory: the isolated-source scaling is calculable, but the nonlinear
  external-field/apparatus boundary-value problem is absent.
- Pulsars: a static weak-field ratio is calculable, but scalar radiation and
  strong-field sensitivities are absent.
- Compact objects: the current weak-field branch cannot be promoted to a
  neutron-star or black-hole prediction.

S0 is rejected as a complete local-gravity route. This is a null-control
failure of completeness, not evidence for kinetic screening, condensate
disruption, or any other S1-S4 mechanism.
"""
    report_path = OUT / "CBR-002_S0_NO_SCREENING_CONTROL.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, csv_path, report_path)) + "\n"
    (OUT / "cbr002_s0_no_screening_control.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
