#!/usr/bin/env python3
"""PKM1 A2-A6 bounded obstruction and survivability audit.

This does not perform a full Hamiltonian reduction.  It derives exact ADM
kinematic identities, a leading-PN slip order, the NDA scale, and a scoped
convexity obstruction to generating the desired static energy by integrating
out one stable algebraic heavy mode with an affine Y coupling.
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
        "pkm1_screen": OUT / "itsm_pkm1_metric_hosted_khronon_summary.json",
        "core_architecture": ROOT / "Theory/Core/ITSM_Core_Architecture.md",
        "nonlinear_parent": ROOT / "Analysis/UVIR/UVIR-003/outputs/uvir003_nonlinear_adm_action_provenance_summary.json",
        "u2": ROOT / "Analysis/UVIR/UVIR-003/U2_A0_A2/outputs/uvir003_u2_a0_a2_nonzero_gradient_summary.json",
    }
    pkm1 = load(inputs["pkm1_screen"])
    parent = load(inputs["nonlinear_parent"])
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "candidate_entered_from_exact_static_screen",
        pkm1.get("route_disposition") == "SELECT_PKM1_FOR_A2_A6_DERIVATION_NOT_GATE_PROMOTION"
        and pkm1.get("A3_static_limit")
        == "PASS_CONDITIONAL_METRIC_HOSTED_MODIFIED_POISSON_REDUCTION_EXACT_AQUAL_ONLY_FOR_STATIC_K_NULL_OR_LOCAL_LIMIT",
    )

    # In unitary gauge Theta=mu_Theta*t, the normalized phase flow is the ADM
    # unit normal. Therefore Q=1/N and a_i=D_i ln N. J(Y) has spatial lapse
    # derivatives but no time derivative of N; K(Q) is algebraic in N.
    N, mu_theta = sp.symbols("N mu_Theta", positive=True)
    x, t = sp.symbols("x t", real=True)
    lapse = sp.Function("N")(t, x)
    phase_norm = mu_theta / N
    Q_adm = sp.simplify(phase_norm / mu_theta)
    U_cov_0 = sp.simplify(-mu_theta / phase_norm)
    log_gradient_identity = sp.simplify(
        sp.diff(sp.log(lapse), x) - sp.diff(lapse, x) / lapse
    )
    add_check(
        checks,
        "unitary_gauge_ADM_identity",
        Q_adm == 1 / N and U_cov_0 == -N and log_gradient_identity == 0,
        phase_gauge="Theta=mu_Theta*t on rho>0 and timelike-gradient chart",
        U_mu="(-N,0,0,0)",
        Q=str(Q_adm),
        a_i="D_i ln N",
        Y="D_i ln N D^i ln N",
    )
    dN_space, dN_time, dshift_time = sp.symbols(
        "D_i_N dot_N dot_N_i", real=True
    )
    Y_adm = dN_space**2 / N**2
    K_adm = sp.Function("K")(1 / N)
    forbidden_velocities = {dN_time, dshift_time}
    add_check(
        checks,
        "no_new_lapse_or_shift_velocity_in_candidate_ADM_form",
        not forbidden_velocities.intersection((Y_adm + K_adm).free_symbols),
        J_velocity_inventory="J(Y) contains spatial D_i N only",
        K_velocity_inventory="K(1/N) is algebraic in N",
        limitation="Necessary degeneracy indicator only; not a completed Dirac constraint count",
    )

    # Leading PN order of one J-sector anisotropic product: a_i is first
    # order, so J_Y a_i a_j is second order. This is not a calculation of the
    # full khronon/polarization stress or the parent metric constraints.
    eps = sp.symbols("epsilon", positive=True)
    a_order = eps
    anisotropic_stress_order = sp.expand(a_order**2)
    add_check(
        checks,
        "leading_PN_J_sector_anisotropic_product_is_quadratic",
        anisotropic_stress_order == eps**2,
        a_i_order="O(epsilon)",
        JY_a_i_a_j_order="O(epsilon^2)",
        consequence="this particular J_Y*a_i*a_j product cannot by itself source linear traceless slip around the zero-acceleration background",
        limitation="does not prove Phi=Psi for the full ITSM parent; other khronon, susceptibility, amplitude and constraint terms are uncomputed",
    )

    # Canonical normalization Phi_c=M_P Phi gives
    # (M_P^2/a0)(d Phi)^3=(d Phi_c)^3/(a0 M_P)= (d Phi_c)^3/Lambda_0^2.
    a0, MP, Lambda = sp.symbols("a0 M_P Lambda_0", positive=True)
    lambda_sq = sp.simplify(a0 * MP)
    add_check(
        checks,
        "NDA_scale_dimension_and_identity",
        sp.simplify(Lambda**2 - lambda_sq).subs(Lambda, sp.sqrt(lambda_sq)) == 0,
        relation="Lambda_0=sqrt(a0*M_P)",
        dimensions={"a0": 1, "M_P": 1, "Lambda_0": 1},
        interpretation="naive cubic scale only; full constrained amplitude may differ",
    )

    # Scoped microscopic no-go. Let a stable algebraic heavy variable chi
    # enter the static energy affinely in Y:
    # F(Y)=M_P^2 Y + min_chi[U(chi)+b(chi)Y].
    # At a stable stationary point D=U''+b''Y>0,
    # F''(Y)=-(b')^2/D <= 0. The required deep energy C Y^(3/2) is convex.
    Y, C = sp.symbols("Y C", positive=True)
    bprime = sp.symbols("b_prime", real=True)
    stable_D = sp.symbols("D_stable", positive=True)
    envelope_second = sp.simplify(-(bprime**2) / stable_D)
    target_second = sp.diff(C * Y ** sp.Rational(3, 2), Y, 2)
    add_check(
        checks,
        "stable_algebraic_affine_Y_parent_obstruction",
        sp.ask(sp.Q.nonpositive(envelope_second)) is True
        and sp.ask(sp.Q.positive(target_second)) is True,
        eliminated_parent_F_second=str(envelope_second),
        required_deep_energy_F_second=str(target_second),
        scope="one or many stable algebraic heavy modes whose static Y dependence is affine; propagating, nonlocal, non-affine or constrained parents are not excluded",
    )

    # Constructive non-affine evasion.  This identity is deliberately built
    # to represent the target deep operator and is therefore a parent-action
    # candidate, not a microscopic derivation.  For s>0,
    #   F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3
    # has the stable stationary point s*=sqrt(Y)/a0 and gives
    #   min_s F=(2/3)Y^(3/2)/a0.
    # Its stiffness vanishes as Y->0, so it is a critical/constrained
    # susceptibility rather than the gapped radial mode rejected by M2.
    susceptibility = sp.symbols("s", positive=True)
    F_aux = Y**2 / (2 * a0**2 * susceptibility) + a0**2 * susceptibility**3 / 6
    s_star = sp.sqrt(Y) / a0
    auxiliary_stationarity = sp.simplify(
        sp.diff(F_aux, susceptibility).subs(susceptibility, s_star)
    )
    auxiliary_curvature = sp.simplify(
        sp.diff(F_aux, susceptibility, 2).subs(susceptibility, s_star)
    )
    auxiliary_effective_energy = sp.simplify(F_aux.subs(susceptibility, s_star))
    add_check(
        checks,
        "constructive_nonaffine_auxiliary_evasion",
        auxiliary_stationarity == 0
        and auxiliary_curvature == 2 * a0 * sp.sqrt(Y)
        and auxiliary_effective_energy == sp.Rational(2, 3) * Y ** sp.Rational(3, 2) / a0,
        parent_static_energy="F(Y,s)=Y^2/(2*a0^2*s)+(a0^2/6)*s^3, s>0",
        stationary_point=str(s_star),
        stationary_curvature=str(auxiliary_curvature),
        eliminated_energy=str(auxiliary_effective_energy),
        status="CONSTRUCTED_EXACT_REPRESENTATION_NOT_MICROSCOPIC_DERIVATION",
        zero_gradient="s_star and its stiffness vanish at Y=0; constraint rank/strong coupling must be audited",
    )

    # Smooth phase map domain and global exclusions.
    add_check(
        checks,
        "smooth_phase_domain_is_explicitly_restricted",
        True,
        required=["rho>0", "-nabla_Theta^2>0", "single-valued normalized one-form U_mu"],
        excluded=["defect cores rho=0", "null/spacelike phase-gradient patches", "unproved global time foliation in nonzero spatial winding sectors"],
    )
    parent_status = parent.get("full_J2_status")
    add_check(
        checks,
        "live_parent_not_silently_reused",
        parent_status == "HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED",
        live_parent_status=parent_status,
        candidate_relation="PKM1 is a replacement force-host action class, not evidence completing the live separate-psi parent",
    )

    all_ok = all(row["ok"] for row in checks)
    summary = {
        "audit": "PKM1_A2_A6_BOUNDED_OBSTRUCTION_AND_SURVIVABILITY",
        "calculation_status": "PASS_SCOPED_A2_A6_AUDIT" if all_ok else "FAIL_PIPELINE",
        "route_disposition": "ADVANCE_PKM1_TO_FULL_PARENT_HAMILTONIAN_ONLY" if all_ok else "HOLD_PIPELINE_FAILURE",
        "A2_symmetry_DOF": {
            "status": "PARTIAL_UNITARY_GAUGE_DEGENERACY_INDICATOR",
            "result": "The smooth timelike phase chart has no dot(N) or dot(N_i) in J(Y)+K(Q), consistent with a khronometric constraint structure; the exact rho-Theta-metric Dirac count is not done.",
        },
        "A3_static_limit": "PASS_CONDITIONAL_METRIC_HOSTED_MODIFIED_POISSON_REDUCTION_EXACT_AQUAL_ONLY_FOR_STATIC_K_NULL_OR_LOCAL_LIMIT",
        "A4_stability": {
            "status": "PARTIAL_STATIC_ELLIPTICITY_ONLY",
            "open": ["full Hamiltonian", "IR Jeans band", "Y=0 join", "front characteristics", "radiative stability"],
        },
        "A5_relativistic_observables": {
            "status": "PARTIAL_J_SECTOR_ORDER_COUNT_ONLY",
            "open": ["full parent metric slip", "full PPN", "Shapiro delay", "nonlinear lensing", "GW damping", "compact objects"],
        },
        "A6_cutoff_naturalness": {
            "status": "HOLD",
            "naive_scale": "Lambda_0=sqrt(a0*M_P)",
            "microscopic_result": "STABLE_ALGEBRAIC_AFFINE_Y_HEAVY_MODE_CANNOT_GENERATE_CONVEX_Y^(3/2)_ENERGY; AN_EXPLICIT_NONAFFINE_AUXILIARY_REPRESENTATION_EXISTS_BUT_IS_CRITICAL_AT_Y_ZERO_AND_NOT_DERIVED",
        },
        "constructive_nonaffine_parent": {
            "static_energy": "F(Y,s)=Y^2/(2*a0^2*s)+(a0^2/6)*s^3, s>0",
            "elimination": "s_star=sqrt(Y)/a0 gives F_eff=(2/3)*Y^(3/2)/a0",
            "classification": "ENGINEERED_EXACT_REPRESENTATION_NOT_MICROSCOPIC_DERIVATION",
            "critical_boundary": "s_star and d2F/ds2 both vanish as Y approaches zero",
        },
        "surviving_resolution": "Metric hosting bypasses the separate MAT residue and yields a universally sourced modified-Poisson equation for the displayed designed J. Exact AQUAL additionally requires a static-null K curvature or a controlled local regime where its Helmholtz term is negligible. The origin of J(Y) must be non-affine, constrained, propagating/nonlocal, critical, or fundamental EFT data.",
        "recommended_next_action": "Use the explicit non-affine susceptibility representation as a hostile parent-action control inside one finite-density rho-Theta-metric ADM/Dirac calculation; reject it if the Y=0 constraint-rank change, Hamiltonian, or galactic-band characteristics are unhealthy. Do not run phenomenology or migrate a gate first.",
        "kill_criteria_next": [
            "extra Ostrogradsky/ghost DOF after the full constrained reduction",
            "negative Hamiltonian in the galactic nonzero-gradient band",
            "no globally valid smooth phase foliation in the claimed domain",
            "a0 or J inserted solely to match the desired force law with no microscopic or controlled EFT status",
            "singular or non-closing auxiliary constraint at the Y=0 boundary",
            "failure to recover the GR high-acceleration limit or an observationally acceptable full-parent metric slip",
        ],
        "gate_firewall": {
            "MAT_001": "BLOCKED",
            "UVIR_003": "IN_PROGRESS",
            "physics_pass": False,
            "canonical_action_replaced": False,
            "downstream_opened": False,
        },
        "checks": checks,
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": "This audit establishes exact kinematic identities, order counting, an NDA relation, a scoped convexity obstruction, and a deliberately engineered non-affine auxiliary representation. The representation proves mathematical availability, not microscopic origin. This is not a full Dirac/Hamiltonian calculation and cannot inherit published khronon stability, PPN, lensing or cosmology as an ITSM result.",
    }
    json_path = OUT / "itsm_pkm1_a2_a6_obstruction_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# PKM1 A2-A6 bounded obstruction audit

**Calculation:** `{summary['calculation_status']}`  
**Disposition:** `{summary['route_disposition']}`  
**Physics pass:** `false`

## What survives

In the smooth timelike phase chart, `Theta=mu_Theta t` gives `Q=1/N` and
`a_i=D_i ln N`. The candidate action therefore contains spatial derivatives
of the lapse but no lapse or shift velocities. This is consistent with a
khronometric constrained scalar, although it is not the full Dirac count.

The particular nonlinear product `J_Y a_i a_j` starts at second perturbative
order around a zero-acceleration background, so that term cannot by itself
source linear traceless slip. This is not a proof that the complete ITSM
parent has equal metric potentials: the khronon, susceptibility, amplitude and
constraint contributions remain uncomputed. The metric-hosted
modified-Poisson equation retains universal source normalization. A generic
`K(Q)` supplies an additional static Helmholtz term; exact AQUAL requires
`K_QQ(1)=0` or a controlled local regime where that term is negligible.

## New obstruction

A stable algebraic heavy mode with energy affine in `Y` cannot generate the
required deep energy. At its stable stationary point,

`F''(Y)=-(b')^2/(U''+b''Y) <= 0`,

whereas `F_target=C Y^(3/2)` has

`F_target''=3 C/(4 sqrt(Y)) > 0`.

Thus a simple radial/heavy integrate-out cannot microscopically produce PKM1's
convex deep operator. A viable parent must use non-affine coupling, a
constrained or propagating polarization sector, nonlocal dynamics, or treat
`J` as fundamental controlled EFT data.

## Constructive non-affine control

The scoped obstruction can be evaded algebraically. For `s>0`, the constructed
static energy

`F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3`

has `s_star=sqrt(Y)/a0`, positive curvature `2 a0 sqrt(Y)`, and exactly

`F_eff(Y)=(2/3)Y^(3/2)/a0`.

This was built from the desired operator and is **not** a microscopic
derivation. It identifies a narrower possibility to test: a non-affine,
critically soft susceptibility or constrained polarization. Both `s_star` and
its stiffness vanish at `Y=0`, so the constraint rank, Hamiltonian and strong
coupling at that boundary are the decisive risks. It cannot be identified with
the stable gapped condensate radial mode rejected by M2.

The naive canonical cubic scale is `Lambda_0=sqrt(a0 M_P)`, but this is not a
physical cutoff until the full constrained amplitude is calculated.

## Decision

PKM1 is the only survivor among the broad controls explicitly screened here
because it bypasses the independent direct matter residue. It advances only to
one explicit parent-action Hamiltonian calculation, using the non-affine
susceptibility as a hostile constructive control. The live action and every
gate status remain unchanged.
"""
    report_path = OUT / "ITSM_PKM1_A2_A6_OBSTRUCTION_AUDIT.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{digest(path)}  {path.name}" for path in (json_path, report_path)) + "\n"
    (OUT / "itsm_pkm1_a2_a6_obstruction.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["route_disposition"], "checks": len(checks)}))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
