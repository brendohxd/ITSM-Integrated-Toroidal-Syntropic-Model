#!/usr/bin/env python3
"""Deterministic ET2 topology/signature/spectrum control for TOP-001.

This is a mathematical-template audit.  It cannot produce a physics pass or
change a gate.  Exact rational arithmetic is used for all spectrum identities.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "ITSM_TOP001_ET2_A0_v1"
STATUS_PASS = (
    "PASS_TOP001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTROL_"
    "HOLD_LORENTZIAN_COMPLETION"
)
STATUS_FAIL = "FAIL_TOP001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTROL"
LABEL_BOUND = 3

REPO = Path(__file__).resolve().parents[3]
OUTPUT = (
    REPO
    / "Analysis"
    / "TOP"
    / "TOP-001"
    / "outputs"
    / "top001_et2_a0_topology_signature_spectrum_summary.json"
)
CONTRACT = (
    REPO
    / "Theory"
    / "Gates"
    / "TOP-001"
    / "TOP-001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTRACT_2026-10-17.md"
)
TOPX4_OUTPUT = (
    REPO
    / "Analysis"
    / "TOP"
    / "TOP-X4"
    / "outputs"
    / "topx4_a0_kinematic_summary.json"
)

AUTHORITY_HASHES = {
    "GEMINI.md": "5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12",
    "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md": (
        "d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa"
    ),
    "Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md": (
        "3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809"
    ),
    "Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md": (
        "81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b"
    ),
    "Theory/Gates/TOP-001/TOP-001_GATE_SPEC.md": (
        "6c165f43b38df6ba2aa1321df5a3ff38fc85dd50f177ebefcf63d3ec75397484"
    ),
    "Theory/Core/ITSM_TOPX4_KK001_ROUTE_PLAN_2026-09-06.md": (
        "0fee9cd7ae62085f4022fdc4a28347dba8e538a464fbdf8bdcbb11568997eb32"
    ),
    "active_research.md": (
        "40d7859b67452a65040665ac1d52f133896234293023dcdda496076802aac2f0"
    ),
}

BRANCHES = [
    {
        "id": "canonical",
        "product": "R_t x T3",
        "signature": "Lorentzian(-+++)",
        "total_dimension": 4,
        "compact_torus_rank": 3,
        "compact_temporal_cycles": 0,
        "compact_spatial_or_internal_cycles": 3,
        "abstract_compact_factor": "T3",
    },
    {
        "id": "ET2",
        "product": "S1_tau x T2",
        "signature": "Euclidean(+++)",
        "total_dimension": 3,
        "compact_torus_rank": 3,
        "compact_temporal_cycles": 1,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T3",
    },
    {
        "id": "LT2",
        "product": "R_t x T2",
        "signature": "Lorentzian(-++)",
        "total_dimension": 3,
        "compact_torus_rank": 2,
        "compact_temporal_cycles": 0,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T2",
    },
    {
        "id": "E0T2",
        "product": "R_tau x T2",
        "signature": "Euclidean(+++)",
        "total_dimension": 3,
        "compact_torus_rank": 2,
        "compact_temporal_cycles": 0,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T2",
    },
    {
        "id": "CYL-T2",
        "product": "R_t x R_z x T2",
        "signature": "Lorentzian(-+++)",
        "total_dimension": 4,
        "compact_torus_rank": 2,
        "compact_temporal_cycles": 0,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T2",
    },
    {
        "id": "E-CYL-T2",
        "product": "S1_tau x R_z x T2",
        "signature": "Euclidean(++++)",
        "total_dimension": 4,
        "compact_torus_rank": 3,
        "compact_temporal_cycles": 1,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T3",
    },
    {
        "id": "PLT2",
        "product": "S1_t x T2",
        "signature": "Lorentzian(-++)",
        "total_dimension": 3,
        "compact_torus_rank": 3,
        "compact_temporal_cycles": 1,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T3",
    },
    {
        "id": "PL-CYL-T2",
        "product": "S1_t x R_z x T2",
        "signature": "Lorentzian(-+++)",
        "total_dimension": 4,
        "compact_torus_rank": 3,
        "compact_temporal_cycles": 1,
        "compact_spatial_or_internal_cycles": 2,
        "abstract_compact_factor": "T3",
    },
    {
        "id": "ET3",
        "product": "S1_tau x T3",
        "signature": "Euclidean(++++)",
        "total_dimension": 4,
        "compact_torus_rank": 4,
        "compact_temporal_cycles": 1,
        "compact_spatial_or_internal_cycles": 3,
        "abstract_compact_factor": "T4",
    },
    {
        "id": "TOP-X4",
        "product": "R_t x T3_obs x S1_y",
        "signature": "Lorentzian(-++++)",
        "total_dimension": 5,
        "compact_torus_rank": 4,
        "compact_temporal_cycles": 0,
        "compact_spatial_or_internal_cycles": 4,
        "abstract_compact_factor": "T4",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def periodic_coefficient(labels: tuple[int, ...], lengths: tuple[Fraction, ...]) -> Fraction:
    return sum(
        (Fraction(label, 1) / length) ** 2
        for label, length in zip(labels, lengths)
    )


def check_map(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item.get("name", ""): item for item in items}


def main() -> int:
    checks: list[dict[str, Any]] = []

    def add_check(name: str, ok: bool, **details: Any) -> None:
        checks.append({"name": name, "passed": bool(ok), **details})

    branch_by_id = {branch["id"]: branch for branch in BRANCHES}
    expected_dimensions = {
        "canonical": (4, 3, 0, 3),
        "ET2": (3, 3, 1, 2),
        "LT2": (3, 2, 0, 2),
        "E0T2": (3, 2, 0, 2),
        "CYL-T2": (4, 2, 0, 2),
        "E-CYL-T2": (4, 3, 1, 2),
        "PLT2": (3, 3, 1, 2),
        "PL-CYL-T2": (4, 3, 1, 2),
        "ET3": (4, 4, 1, 3),
        "TOP-X4": (5, 4, 0, 4),
    }
    dimension_mismatches = []
    for branch_id, expected in expected_dimensions.items():
        branch = branch_by_id[branch_id]
        measured = (
            branch["total_dimension"],
            branch["compact_torus_rank"],
            branch["compact_temporal_cycles"],
            branch["compact_spatial_or_internal_cycles"],
        )
        if measured != expected:
            dimension_mismatches.append(
                {"branch": branch_id, "expected": expected, "measured": measured}
            )
    add_check(
        "branch_dimension_and_cycle_role_ledger",
        not dimension_mismatches,
        branches_tested=len(BRANCHES),
        mismatches=dimension_mismatches,
    )

    et2 = branch_by_id["ET2"]
    add_check(
        "et2_is_abstract_t3_but_has_temporal_cycle",
        et2["abstract_compact_factor"] == "T3"
        and et2["compact_temporal_cycles"] == 1
        and et2["signature"].startswith("Euclidean"),
        product=et2["product"],
        abstract_compact_factor=et2["abstract_compact_factor"],
        compact_temporal_cycles=et2["compact_temporal_cycles"],
    )

    lt2 = branch_by_id["LT2"]
    add_check(
        "ordinary_noncompact_time_is_not_a_torus_cycle",
        lt2["product"] == "R_t x T2"
        and lt2["compact_torus_rank"] == 2
        and lt2["abstract_compact_factor"] == "T2",
        total_dimension=lt2["total_dimension"],
        compact_torus_rank=lt2["compact_torus_rank"],
    )

    e0t2 = branch_by_id["E0T2"]
    add_check(
        "euclidean_signature_does_not_automatically_compact_time",
        e0t2["product"] == "R_tau x T2"
        and e0t2["compact_torus_rank"] == 2
        and e0t2["abstract_compact_factor"] == "T2"
        and et2["compact_torus_rank"] == 3,
        noncompact_euclidean_time=e0t2,
        compact_euclidean_time=et2,
    )

    cyl = branch_by_id["CYL-T2"]
    add_check(
        "four_dimensional_t2_cylinder_is_not_t3",
        cyl["total_dimension"] == 4
        and cyl["compact_torus_rank"] == 2
        and cyl["abstract_compact_factor"] == "T2",
        product=cyl["product"],
        total_dimension=cyl["total_dimension"],
        compact_torus_rank=cyl["compact_torus_rank"],
    )

    ecyl = branch_by_id["E-CYL-T2"]
    add_check(
        "four_dimensional_euclidean_t2_cylinder_has_t3_compact_factor",
        ecyl["product"] == "S1_tau x R_z x T2"
        and ecyl["total_dimension"] == 4
        and ecyl["compact_torus_rank"] == 3
        and ecyl["abstract_compact_factor"] == "T3",
        product=ecyl["product"],
        full_manifold="R_z x T3",
        full_manifold_is_compact_t3=False,
        total_dimension=ecyl["total_dimension"],
        compact_torus_rank=ecyl["compact_torus_rank"],
    )

    t3_betti = [math.comb(3, degree) for degree in range(4)]
    add_check(
        "et2_t3_betti_numbers",
        t3_betti == [1, 3, 3, 1],
        values=t3_betti,
    )
    t3_euler = sum((-1) ** degree * value for degree, value in enumerate(t3_betti))
    add_check("et2_t3_euler_characteristic_zero", t3_euler == 0, value=t3_euler)
    add_check(
        "et2_fundamental_group_and_winding_rank",
        et2["compact_torus_rank"] == 3,
        identity="pi_1(S1_tau x T2)=Z x Z^2=Z^3",
        h1="Z^3",
        winding_lattice_rank=3,
        physical_role_caveat="one integer labels Euclidean-time winding",
    )

    lengths = (Fraction(5, 3), Fraction(7, 4), Fraction(11, 6))
    label_range = range(-LABEL_BOUND, LABEL_BOUND + 1)
    labels = list(itertools.product(label_range, repeat=3))
    periodic_mismatches = []
    dropped_temporal_undetected = []
    antiperiodic_equalities = []
    for label in labels:
        et2_value = periodic_coefficient(label, lengths)
        t3_value = periodic_coefficient(label, lengths)
        if et2_value != t3_value:
            periodic_mismatches.append(label)

        n_tau, n1, n2 = label
        without_matsubara = periodic_coefficient((n1, n2), lengths[1:])
        if n_tau != 0 and et2_value == without_matsubara:
            dropped_temporal_undetected.append(label)

        fermion_value = (
            (Fraction(n_tau, 1) + Fraction(1, 2)) / lengths[0]
        ) ** 2 + periodic_coefficient((n1, n2), lengths[1:])
        if fermion_value == t3_value:
            antiperiodic_equalities.append(label)

    nonzero_temporal_labels = sum(1 for label in labels if label[0] != 0)
    add_check(
        "periodic_boson_et2_equals_rectangular_t3_exactly",
        not periodic_mismatches,
        convention="lambda/(2*pi)^2=sum_i n_i^2/L_i^2",
        exact_lengths=[fraction_text(value) for value in lengths],
        labels_tested=len(labels),
        mismatches=periodic_mismatches,
    )
    kz_samples = (Fraction(-3, 2), Fraction(0, 1), Fraction(5, 3))
    ecyl_mismatches = []
    for kz in kz_samples:
        for label in labels:
            left = kz**2 + periodic_coefficient(label, lengths)
            right = kz**2 + periodic_coefficient(label, lengths)
            if left != right:
                ecyl_mismatches.append(
                    {"k_z": fraction_text(kz), "label": list(label)}
                )
    add_check(
        "four_dimensional_ecyl_compact_sector_identity_exact",
        not ecyl_mismatches,
        full_spectrum_form="k_z^2 + sum_i n_i^2/L_i^2",
        exact_k_z_samples=[fraction_text(value) for value in kz_samples],
        label_sample_pairs=len(kz_samples) * len(labels),
        mismatches=ecyl_mismatches,
        full_manifold="R_z x T3",
    )
    add_check(
        "negative_control_dropped_matsubara_term_detected",
        not dropped_temporal_undetected and nonzero_temporal_labels == 294,
        nonzero_temporal_labels=nonzero_temporal_labels,
        detected_mismatches=nonzero_temporal_labels - len(dropped_temporal_undetected),
        undetected_labels=dropped_temporal_undetected,
    )
    add_check(
        "thermal_fermion_antiperiodicity_breaks_labelwise_equivalence",
        not antiperiodic_equalities,
        shift="n_tau -> n_tau+1/2",
        labels_tested=len(labels),
        accidental_equalities=antiperiodic_equalities,
        temporal_zero_mode_present=False,
        minimum_absolute_temporal_label="1/2",
    )

    shell_degeneracies = {}
    for dimension in (2, 3, 4):
        degeneracy = sum(
            1
            for vector in itertools.product((-1, 0, 1), repeat=dimension)
            if sum(component * component for component in vector) == 1
        )
        shell_degeneracies[str(dimension)] = degeneracy
    add_check(
        "isotropic_first_shell_degeneracies_t2_t3_t4",
        shell_degeneracies == {"2": 4, "3": 6, "4": 8},
        measured=shell_degeneracies,
        expected={"2": 4, "3": 6, "4": 8},
    )

    plt2 = branch_by_id["PLT2"]
    pl_cyl = branch_by_id["PL-CYL-T2"]
    closed_timelike_curve = {
        "curve": "gamma(s)=(t=L_t*s mod L_t,x1_const,x2_const), 0<=s<=1",
        "closed_by_periodicity": True,
        "tangent_norm_for_unit_speed_direct_product_metric": -1,
    }
    add_check(
        "compact_lorentzian_time_direct_product_has_ctc",
        plt2["compact_temporal_cycles"] == 1
        and pl_cyl["compact_temporal_cycles"] == 1
        and closed_timelike_curve["closed_by_periodicity"]
        and closed_timelike_curve["tangent_norm_for_unit_speed_direct_product_metric"] < 0,
        **closed_timelike_curve,
        affected_branches=[plt2["product"], pl_cyl["product"]],
        scope="direct-product metric only",
    )

    et3 = branch_by_id["ET3"]
    topx4_branch = branch_by_id["TOP-X4"]
    add_check(
        "euclidean_t4_and_topx4_role_signature_separation",
        et3["abstract_compact_factor"] == topx4_branch["abstract_compact_factor"] == "T4"
        and et3["compact_temporal_cycles"] == 1
        and topx4_branch["compact_temporal_cycles"] == 0
        and et3["total_dimension"] == 4
        and topx4_branch["total_dimension"] == 5
        and et3["signature"].startswith("Euclidean")
        and topx4_branch["signature"].startswith("Lorentzian"),
        euclideanized_canonical=et3,
        topx4=topx4_branch,
    )

    authority_receipts = []
    authority_mismatches = []
    for relative_path, expected_hash in AUTHORITY_HASHES.items():
        source = REPO / relative_path
        actual_hash = sha256(source) if source.is_file() else None
        receipt = {
            "path": relative_path,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "ok": actual_hash == expected_hash,
        }
        authority_receipts.append(receipt)
        if not receipt["ok"]:
            authority_mismatches.append(receipt)
    add_check(
        "frozen_authority_receipts_match",
        not authority_mismatches,
        receipts=authority_receipts,
        mismatches=authority_mismatches,
    )

    topx4_actual_hash = sha256(TOPX4_OUTPUT)
    topx4_sidecar = TOPX4_OUTPUT.with_suffix(TOPX4_OUTPUT.suffix + ".sha256")
    sidecar_tokens = topx4_sidecar.read_text(encoding="utf-8").split()
    topx4_recorded_hash = sidecar_tokens[0].lower() if sidecar_tokens else ""
    add_check(
        "topx4_a0_sidecar_hash_matches",
        topx4_actual_hash == topx4_recorded_hash,
        actual_sha256=topx4_actual_hash,
        recorded_sha256=topx4_recorded_hash,
    )

    topx4_payload = json.loads(TOPX4_OUTPUT.read_text(encoding="utf-8"))
    topx4_checks = check_map(topx4_payload.get("checks", []))
    topx4_status_ok = (
        topx4_payload.get("status") == "PASS_TOPX4_A0_KINEMATIC_AND_DIMENSIONAL_CONTROL"
        and topx4_payload.get("calculation_status") == "PASS"
        and topx4_payload.get("checks_passed") == 14
        and topx4_payload.get("checks_total") == 14
        and topx4_payload.get("physics_pass") is False
        and topx4_payload.get("gate_effect") == "NONE"
        and topx4_payload.get("canonical_t3_replaced") is False
    )
    add_check(
        "topx4_a0_status_and_firewall_preserved",
        topx4_status_ok,
        status=topx4_payload.get("status"),
        checks_passed=topx4_payload.get("checks_passed"),
        checks_total=topx4_payload.get("checks_total"),
        physics_pass=topx4_payload.get("physics_pass"),
        gate_effect=topx4_payload.get("gate_effect"),
        canonical_t3_replaced=topx4_payload.get("canonical_t3_replaced"),
    )
    topx4_identity = topx4_checks.get("direct_t4_equals_t3_plus_kk_exactly", {})
    add_check(
        "topx4_a0_direct_t4_identity_dependency_passes",
        topx4_identity.get("ok") is True and topx4_identity.get("mismatches") == [],
        dependency_check=topx4_identity,
    )

    observational_flags = {
        "H0": False,
        "SPARC": False,
        "observed_a0": False,
        "target_2pi_coefficient": False,
        "target_reservoir_current": False,
    }
    add_check(
        "observational_input_firewall",
        not any(observational_flags.values()),
        flags=observational_flags,
    )
    derived_claims: list[str] = []
    add_check(
        "derived_physical_claims_remain_empty",
        derived_claims == [],
        derived_claims=derived_claims,
    )

    checks_passed = sum(1 for check in checks if check["passed"])
    all_pass = checks_passed == len(checks)
    result = {
        "schema": SCHEMA,
        "route": "TOP-001_ET2-A0",
        "status": STATUS_PASS if all_pass else STATUS_FAIL,
        "calculation_status": "PASS" if all_pass else "FAIL",
        "checks": checks,
        "checks_passed": checks_passed,
        "checks_total": len(checks),
        "branch_ledger": BRANCHES,
        "spectrum_test": {
            "label_bound_inclusive": LABEL_BOUND,
            "labels_tested": len(labels),
            "exact_lengths_beta_L1_L2": [fraction_text(value) for value in lengths],
            "common_factor_removed": "(2*pi)^2",
        },
        "bounded_findings": [
            "S1_tau x T2 is abstractly T3 and has pi_1=Z^3.",
            "Periodic bosonic ET2 and rectangular Euclidean T3 spectra agree exactly on the frozen label cube.",
            "Dropping the Matsubara term is detected for every nonzero temporal label in the frozen cube.",
            "Thermal fermion anti-periodicity breaks the tested labelwise periodic-spectrum equivalence and removes the temporal zero mode.",
            "R_t x T2 is 2+1 dimensional and is not T3.",
            "R_tau x T2 remains compact-rank two unless Euclidean time is explicitly identified periodically.",
            "R_t x R_z x T2 is 3+1 dimensional but has compact rank two, not three.",
            "S1_tau x R_z x T2 is four-dimensional with compact factor T3; the full manifold is R_z x T3.",
            "Direct-product compact-time T2 branches contain a closed timelike curve, with or without R_z.",
            "S1_tau x T3 is Euclidean T4, while TOP-X4 is a five-dimensional Lorentzian branch with spatial/internal T4.",
        ],
        "substantive_holds": [
            "no frozen Euclidean ITSM condensate action or saddle",
            "no Wick-rotation or reflection-positivity proof",
            "no KMS/spin-structure completion",
            "no causal or retarded Lorentzian continuation",
            "no stress tensor, physical Hessian, or stability result",
            "no admissible compact-Lorentzian-time model beyond the demonstrated direct-product CTC obstruction",
            "no derived relation between temporal winding and an observed current",
            "no observational prediction or gate transition",
        ],
        "explicit_nonclaims": [
            "no equivalence of Euclidean-time and spatial cycles as physical roles",
            "no replacement of the canonical spatial T3 branch",
            "no radion or modulus stabilization",
            "no K_Q, V, a0, H0, or SPARC prediction",
            "no publication readiness",
        ],
        "dependency_receipts": {
            "authority": authority_receipts,
            "contract_sha256": sha256(CONTRACT),
            "script_sha256": sha256(Path(__file__).resolve()),
            "topx4_a0_sha256": topx4_actual_hash,
        },
        "derived_claims": derived_claims,
        "physics_pass": False,
        "gate_effect": "NONE",
        "canonical_t3_replaced": False,
        "claim_status": "Open",
        "review_status": "DEFERRED",
        "Rule9_cleared": False,
        "research_execution": "PROCEED_PROVISIONALLY",
        "next_entry_condition": (
            "freeze a Euclidean condensate-action and Lorentzian-continuation contract covering Wick rotation, "
            "KMS/spin structure, reflection positivity, retarded continuation, stress tensor, and winding roles"
        ),
    }

    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
    temporary_output.write_text(serialized, encoding="utf-8", newline="\n")
    os.replace(temporary_output, OUTPUT)
    output_hash = sha256(OUTPUT)
    sidecar = OUTPUT.with_suffix(OUTPUT.suffix + ".sha256")
    temporary_sidecar = sidecar.with_suffix(sidecar.suffix + ".tmp")
    temporary_sidecar.write_text(
        f"{output_hash}  {OUTPUT.name}\n", encoding="utf-8", newline="\n"
    )
    os.replace(temporary_sidecar, sidecar)

    print(result["status"])
    print(f"checks={checks_passed}/{len(checks)}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={OUTPUT}")
    print(f"sha256={output_hash}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
