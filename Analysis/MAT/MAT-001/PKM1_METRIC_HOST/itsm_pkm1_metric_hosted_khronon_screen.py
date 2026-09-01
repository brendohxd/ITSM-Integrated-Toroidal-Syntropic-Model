#!/usr/bin/env python3
"""PKM1 metric-hosted condensate-khronon broad-route screen.

This is a controlled alternative action class, not a modification of the live
canonical action.  It tests whether moving the low-acceleration operator into
the metric/foliation sector removes the independent matter-residue bottleneck.
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


def add_check(rows: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "core_architecture": ROOT / "Theory/Core/ITSM_Core_Architecture.md",
        "tier1_programme": ROOT / "Theory/Core/ITSM_Tier1_Route_Test_Programme.md",
        "force_hosting": ROOT / "Analysis/MAT/MAT-001/FORCE_HOSTING/outputs/mat001_force_hosting_readiness_summary.json",
        "m2": ROOT / "Analysis/MAT/MAT-001/M2_RADIAL_MATCHING/outputs/mat001_m2_radial_heavy_reduction_summary.json",
        "u2": ROOT / "Analysis/UVIR/UVIR-003/U2_A0_A2/outputs/uvir003_u2_a0_a2_nonzero_gradient_summary.json",
    }
    core = inputs["core_architecture"].read_text(encoding="utf-8")
    hosting = load(inputs["force_hosting"])
    m2 = load(inputs["m2"])
    u2 = load(inputs["u2"])
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "baseline_requires_new_force_host",
        hosting.get("hosting_status") == "NO_LIVE_HOST_READY_FOR_S_INT"
        and m2.get("route_disposition") == "REJECT_MINIMAL_M2_CLASSES_SOFT_RESIDUE_NOT_DERIVED"
        and u2.get("route_disposition") == "FREEZE_U2_AT_A0_A2_INCOMPLETE_ACTION_DOMAIN_AND_DOF",
    )
    add_check(
        checks,
        "identity_contains_phase_and_frame_inputs",
        "Phi = (rho/sqrt(2)) exp(i Theta)" in core
        and "A unit timelike field `U^mu`" in core
        and "nabla_mu Theta = -mu U_mu" in core,
    )

    # Candidate PKM1 in natural units:
    # S=(M_P^2/2) int sqrt(-g)[R-2 J(Y)+2 K(Q)] + S_m[g],
    # U_mu=-d_mu Theta/sqrt(-dTheta^2), a_mu=U^nu nabla_nu U_mu,
    # Y=a_mu a^mu.  Ordinary matter is minimally coupled to g_mu_nu.
    y, a0 = sp.symbols("y a0", positive=True)
    D = 1 + y + y**2 + y**3
    mu_interp = sp.factor(1 - 1 / D)
    J = a0**2 * (sp.log(1 + y) - sp.log(1 + y**2) / 2 - sp.atan(y))
    dJ_dY = sp.simplify(sp.diff(J, y) / (2 * a0**2 * y))
    add_check(
        checks,
        "explicit_interpolating_function_identity",
        sp.simplify(1 + dJ_dY - mu_interp) == 0,
        mu_y=str(mu_interp),
        J_y=str(J),
        J_Y=str(dJ_dY),
    )
    add_check(
        checks,
        "deep_acceleration_limit_exact",
        sp.limit(mu_interp / y, y, 0, dir="+") == 1
        and sp.limit(J / (-a0**2 * y**2), y, 0, dir="+") == 1,
        J_series=str(sp.series(J, y, 0, 7)),
        required_form="J=-Y+(2/(3*a0))*Y^(3/2)+O(Y^3/a0^4)",
    )
    add_check(
        checks,
        "high_acceleration_GR_limit",
        sp.limit(mu_interp, y, sp.oo) == 1
        and sp.limit(J, y, sp.oo) == -sp.pi * a0**2 / 2,
        mu_infinity=str(sp.limit(mu_interp, y, sp.oo)),
        J_infinity=str(sp.limit(J, y, sp.oo)),
    )
    mu_prime = sp.factor(sp.diff(mu_interp, y))
    radial_eigenvalue = sp.factor(mu_interp + y * mu_prime)
    add_check(
        checks,
        "static_ellipticity_for_positive_gradient",
        sp.ask(sp.Q.positive(mu_interp)) is True
        and sp.ask(sp.Q.positive(mu_prime)) is True
        and sp.ask(sp.Q.positive(radial_eigenvalue)) is True,
        transverse_eigenvalue=str(mu_interp),
        radial_eigenvalue=str(radial_eigenvalue),
        zero_gradient="DEGENERATE_AS_EXPECTED_FOR_DEEP_P3_BRANCH",
    )

    # Weak-field variation. EH contributes -M_P^2 Y; -M_P^2 J(Y)
    # supplies the metric-hosted modification. In a one-component gradient
    # proxy q=|grad Phi_N|, d[Y+J(Y)]/dq/(2q)=1+J_Y. Together with
    # M_P^2=1/(8 pi G), the J/EH part has the universal source normalization.
    # A generic K(Q), however, contributes a static Helmholtz term.  With
    # K=K_0+(K_QQ(1)/2)(Q-1)^2+..., Q-1=-Phi_N+..., the full leading equation
    # contains m_K^2 Phi_N with m_K^2=K_QQ(1)/2.
    MP2, G, rho_b = sp.symbols("M_P_sq G rho_b", positive=True)
    K_QQ = sp.symbols("K_QQ_at_1", real=True)
    q = sp.symbols("q", positive=True)
    J_q = J.subs(y, q / a0)
    gradient_factor = sp.simplify(sp.diff(q**2 + J_q, q) / (2 * q))
    source_prefactor = sp.simplify(1 / (2 * MP2)).subs(MP2, 1 / (8 * sp.pi * G))
    add_check(
        checks,
        "minimal_metric_source_normalization_and_variation",
        sp.simplify(gradient_factor - mu_interp.subs(y, q / a0)) == 0
        and source_prefactor == 4 * sp.pi * G,
        weak_field_action="L=-M_P^2[Y+J(Y)]+(M_P^2/2)*K_QQ(1)*Phi_N^2-rho_b*Phi_N",
        field_equation="div[mu(|grad Phi_N|/a0) grad Phi_N]+m_K^2*Phi_N=4*pi*G*rho_b, with m_K^2=K_QQ(1)/2",
        exact_AQUAL_subcase="K_QQ(1)=0, or a declared local regime in which m_K^2*Phi_N is negligible",
        euler_lagrange_gradient_factor=str(gradient_factor),
        source_prefactor=str(source_prefactor),
        static_mass_prefactor=str(K_QQ / 2),
        independent_C_m_present=False,
        independent_K_Q_residue_needed=False,
    )
    gN = sp.symbols("g_N", positive=True)
    gdeep = sp.sqrt(a0 * gN)
    add_check(
        checks,
        "deep_spherical_scaling",
        sp.simplify((gdeep / a0) * gdeep - gN) == 0,
        result="g=sqrt(a0*g_N)",
        domain="exact K_QQ(1)=0 subcase or local regime with negligible m_K^2*Phi_N",
        coefficient_status="FIXED_TO_ONE_BY_MINIMAL_METRIC_SOURCE_NORMALIZATION",
        a0_status="INPUT_SCALE_NOT_DERIVED",
    )

    # Broader two-scalar symmetry-locked portal control. An exact flat
    # direction protects a massless mode, but its normalized matter residue
    # remains an independent parent combination and the matter vertex breaks
    # the joint shift unless matter transforms.
    Zp, Zs = sp.symbols("Z_psi Z_sigma", positive=True)
    kappa, gs = sp.symbols("kappa g_sigma", real=True)
    helical_residue = sp.simplify(gs * kappa / sp.sqrt(Zp + Zs * kappa**2))
    add_check(
        checks,
        "helical_portal_control_remains_underdetermined",
        helical_residue.free_symbols == {gs, kappa, Zp, Zs},
        protected_heavy_coordinate="sigma-kappa*psi",
        canonical_residue=str(helical_residue),
        symmetry_breaking="g_sigma*sigma*T breaks the joint shift unless the matter sector transforms",
    )

    # Natural-unit dimensions for the candidate IR action.
    dims = {
        "M_P": 1,
        "R": 2,
        "Theta": 0,
        "rho": 1,
        "U": 0,
        "a_mu": 1,
        "Y=a^2": 2,
        "a0": 1,
        "J": 2,
        "K": 2,
    }
    add_check(
        checks,
        "mass_dimensions_close",
        2 * dims["M_P"] + dims["R"] == 4
        and 2 * dims["M_P"] + dims["J"] == 4
        and 2 * dims["M_P"] + dims["K"] == 4
        and dims["Y=a^2"] == 2 * dims["a_mu"],
        dimensions=dims,
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "PKM1_METRIC_HOSTED_CONDENSATE_KHRONON_BROAD_ROUTE",
        "calculation_status": "PASS_BOUNDED_SYMBOLIC_ROUTE_SCREEN" if all_ok else "FAIL_PIPELINE",
        "route_disposition": "SELECT_PKM1_FOR_A2_A6_DERIVATION_NOT_GATE_PROMOTION" if all_ok else "HOLD_PIPELINE_FAILURE",
        "candidate_action": {
            "IR_action": "S=(M_P^2/2) integral sqrt(-g)[R-2 J(Y)+2 K(Q)] + S_m[Psi_m,g]",
            "condensate_phase_map": "U_mu=-nabla_mu Theta/sqrt(-nabla_Theta^2); Q=sqrt(-nabla_Theta^2)/mu_Theta",
            "acceleration_invariant": "a_mu=U^nu nabla_nu U_mu; Y=a_mu a^mu",
            "matter_host": "single metric g_mu_nu; no direct psi*T vertex",
            "explicit_control_mu": str(mu_interp),
            "explicit_control_J": str(J),
        },
        "route_results": {
            "minimal_radial_M2": "REJECTED_PREVIOUSLY",
            "helical_symmetry_locked_scalar_portal": "REJECT_FREE_RESIDUE_AND_SYMMETRY_BREAKING_SPURION",
            "minimal_healthy_universal_vector_force_control": "REJECT_AS_DIRECT_ATTRACTIVE_FORCE_CONTROL_BECAUSE_EQUAL_SIGN_CHARGES_REPEL; DOES_NOT_EXCLUDE_GENERAL_VECTOR_TENSOR_GRAVITY",
            "PKM1_metric_hosted_condensate_khronon": "SURVIVES_A0_A1_STATIC_HOSTING_SCREEN",
        },
        "A0_identity": "PASS_CANDIDATE_CONDENSATE_PHASE_DEFINES_PREFERRED_FOLIATION",
        "A1_action": "PARTIAL_COVARIANT_IR_ACTION_MICROSCOPIC_ORIGIN_OF_J_AND_K_OPEN",
        "A2_symmetry_DOF": "HOLD_FULL_CONDENSATE_AMPLITUDE_KHRONON_METRIC_CONSTRAINT_COUNT_REQUIRED",
        "A3_static_limit": "PASS_CONDITIONAL_METRIC_HOSTED_MODIFIED_POISSON_REDUCTION_EXACT_AQUAL_ONLY_FOR_STATIC_K_NULL_OR_LOCAL_LIMIT",
        "A4_stability": "HOLD_ZERO_GRADIENT_DEGENERACY_IR_JEANS_AND_STRONG_COUPLING_REVIEW_REQUIRED",
        "A5_A6": "NOT_RUN",
        "resolved_bottleneck": "SEPARATE_DIRECT_MATTER_RESIDUE_BYPASSED_AT_IR_ACTION_LEVEL_BY_UNIVERSAL_MINIMAL_METRIC_COUPLING",
        "unresolved_burdens": [
            "derive J(Y) and its scale a0 from a finite-density condensate parent rather than selecting a MOND asymptotic",
            "derive K(Q) from the same complex-condensate amplitude/phase action without double counting",
            "perform the full ADM/Hamiltonian DOF count including rho, Theta and metric",
            "control the Y=0 degeneracy, IR Jeans sector and physical strong-coupling scale",
            "prove the smooth-phase map across winding sectors and specify defect-core completion",
            "derive PPN, lensing and cosmology inside the ITSM action rather than inheriting another theory's results",
        ],
        "external_primary_precedent": [
            {
                "citation": "Blanchet and Marsat, Phys. Rev. D 84, 044056 (2011)",
                "url": "https://arxiv.org/abs/1107.5264",
                "use": "metric-hosted preferred-foliation MOND precedent",
            },
            {
                "citation": "Blanchet and Skordis, JCAP 11 (2024) 040",
                "url": "https://arxiv.org/abs/2404.06584",
                "use": "covariant J(Y)+K(Q) action, weak-field limit and published stability caveats",
            },
            {
                "citation": "Flanagan, Astrophys. J. 958, 107 (2023)",
                "url": "https://arxiv.org/abs/2302.14846",
                "use": "nonrelativistic consistency and symmetric-background perturbation precedent",
            },
        ],
        "gate_firewall": {
            "MAT_001": "BLOCKED",
            "UVIR_003": "IN_PROGRESS",
            "V": "NOT_COMPUTED_IN_LIVE_ROUTE",
            "K_Q": "NOT_DERIVED_IN_LIVE_ROUTE",
            "downstream_opened": False,
            "physics_pass": False,
        },
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "PKM1 is a new controlled IR action class. The displayed J was deliberately constructed from a target interpolating function, so the weak-field calculation is an existence and normalization check, not an ITSM derivation of J or MOND. A generic K(Q) adds a static Helmholtz term; exact AQUAL requires K_QQ(1)=0 or a declared local regime where that term is negligible. Minimal metric coupling bypasses the separate matter-residue parameter within this candidate action. The audit does not derive J, K or a0 microscopically, complete the coupled DOF/stability analysis, or modify any live gate status.",
    }
    json_path = OUT / "itsm_pkm1_metric_hosted_khronon_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# PKM1 — metric-hosted condensate-khronon broad route

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**Physics pass:** `false` · **MAT-001:** `BLOCKED` · **UVIR-003:** `IN_PROGRESS`

## Candidate action

Use the smooth condensate phase to define the preferred foliation,

`U_mu=-d_mu Theta/sqrt(-d Theta squared)`,

and put the low-acceleration operator in the gravitational sector:

`S=(M_P^2/2) integral sqrt(-g)[R-2 J(Y)+2 K(Q)] + S_m[Psi_m,g]`,

where `Y=(U.nabla U)^2` and ordinary matter is minimally coupled to the single
metric `g`. This is a new controlled route, not the live action.

## Conditional exact weak-field result

For

`mu(y)=(y+y^2+y^3)/(1+y+y^2+y^3)`, `y=|grad Phi_N|/a0`,

the interpolating function was selected first for this route screen, and an
explicit primitive was then constructed as

`J=a0^2[ln(1+y)-ln(1+y^2)/2-atan(y)]`.

It satisfies `1+J_Y=mu`, `mu~y` at low acceleration and `mu->1` at high
acceleration. For `K=K_0+(K_QQ(1)/2)(Q-1)^2+...`, the stationary weak-field
equation is

`div[mu(|grad Phi_N|/a0) grad Phi_N]+m_K^2 Phi_N=4 pi G rho_b`,

with `m_K^2=K_QQ(1)/2`. Exact AQUAL is the `m_K=0` subcase, or a declared
local regime in which the Helmholtz term is negligible.

This is an existence and normalization check, not a derivation of `J` from
ITSM microphysics. The source normalization comes from the minimally coupled
metric. There is no independent `C_m`, and no `C_m/sqrt(K_Q)` residue is
needed. In the exact-AQUAL subcase, spherical deep acceleration gives
`g=sqrt(a0*g_N)` with coefficient one. The scale `a0` is still an input and
has **not** been derived.

## Why this is broader than M2/U2

PKM1 changes the force host instead of adding another scalar portal. It unifies
the condensate rest frame and khronon foliation and makes the metric lapse the
force potential. The helical two-scalar control still leaves
`g_sigma*kappa/sqrt(Z_psi+Z_sigma*kappa^2)` free, so it does not repair M2.

## Fail-closed burden

PKM1 survives only the A0-A1/static-hosting screen. It still requires a
microscopic derivation of `J`, `K` and `a0`; the full amplitude-phase-metric
constraint count; zero-gradient, Jeans and strong-coupling control; and a
global treatment of winding and defect cores. Published khronon results are
precedent, not evidence that the ITSM embedding passes those tests.

**Recommendation:** advance PKM1 alone to a bounded A2-A6 derivation while
retaining the existing separate-phonon route as a frozen control. Do not change
any gate status.
"""
    report_path = OUT / "ITSM_PKM1_METRIC_HOSTED_KHRONON_ROUTE.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "itsm_pkm1_metric_hosted_khronon.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
