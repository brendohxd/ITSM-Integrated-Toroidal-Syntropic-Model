"""Bounded algebra/provenance checks for P1/P2 rc4; not physics clearance.

Run from the repository root with the existing itsm_env Python. Every receipt
is exclusive-created; use a fresh --output path for a later attempt.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAPERS = {
    "P1": "P1-Scale-Matching-Reconstruction",
    "P2": "P2-Rectangular-T3-Casimir",
}
FROZEN = {
    "papers/P1-Scale-Matching-Reconstruction/Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc3.pdf": "d16a339e866358dbe448e7438b2e2e7e5e8fb1614cda7ed4ef1f1b4c380ca827",
    "papers/P2-Rectangular-T3-Casimir/Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc3.pdf": "bbbfe121a3c91a47e29678b59aa43045b7d0e790bba3041adfa3fc6a6163a9e0",
    "Analysis/Casimir/CBR-001/cbr001_stage1.csv": "57847f382bafa562827413f19f416dbc3da004c95996413d05e0cb7fde0bb47c",
    "Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_scan.csv": "fe648629545f40a29ca3bdc93a5978c59d85210d9157918eb191d45e2056a4d9",
    "Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_thresholds.csv": "94b0ae4c6381ce3843952609d26ee9c73309a0b5275872c1ba97463702db37c4",
    "Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_summary.json": "9a5e80d2f713f01b02b7ea14c2460a344bcb2fcfdf814ea6696677d465c2ce3b",
    "papers/ReleasePackages/2026-10-09/P1_P2_LOCAL_REFEREE_REVIEW_AND_GROK_RECONCILIATION_2026-10-09.md": "51d25f5de27b2d659a6d83b4aa642594ff5ff4501da93786b278777b090d5bdd",
}
PRE_EDIT_TEX = {
    "P1": "4b0d0aefd22f81ea20057936ee7566f24eb12b9b49b2fb22bebdfdcc5a6f2510",
    "P2": "4f5e587c4882cc5a1937819c19c5eea85d4c0a29f3c59f932060f168e5467396",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()
    checks = []

    def check(name, passed, **evidence):
        checks.append({"name": name, "passed": bool(passed), **evidence})

    anchors = {}
    for rel, expected in FROZEN.items():
        anchors[rel] = sha(ROOT / rel)
        check("preserved:" + rel, anchors[rel] == expected,
              expected=expected, actual=anchors[rel])
    current_sources = {}
    for paper, directory in PAPERS.items():
        snapshot = HERE / "preserved_rc3" / directory / "main.tex"
        check(paper + ":pre_edit_source_preserved", sha(snapshot) == PRE_EDIT_TEX[paper])
        source = ROOT / "papers" / directory / "main.tex"
        text = source.read_text(encoding="utf-8")
        current_sources[str(source.relative_to(ROOT))] = sha(source)
        check(paper + ":version_date", "0.2.0-rc4 --- October 17, 2026" in text)
        check(paper + ":author_verification_not_pre_certified",
              "still requires the author's final verification" in text
              and "The author independently reviewed" not in text)

    c, hubble, length, cm, cir, a0, scale, lam = sp.symbols(
        "c H L C_m C_IR a_0 s lambda", positive=True)
    cycle_omega = 2 * sp.pi * c / length
    check("P1:cycle_clock_mismatch", sp.simplify(
        cycle_omega.subs(length, c / hubble) / hubble) == 2 * sp.pi)
    check("P1:cycle_clock_is_not_an_acceleration", sp.simplify(
        (hubble * length / (2 * sp.pi)).subs(length, c / hubble)) == c / (2 * sp.pi))
    cobs = cm ** sp.Rational(3, 2) / sp.sqrt(cir)
    check("P1:field_rescaling_invariant", sp.simplify(
        cobs.subs({cm: cm / scale, cir: cir / scale ** 3}, simultaneous=True) - cobs) == 0)
    effective = cobs ** 2 * a0
    check("P1:scale_reparameterization_degeneracy", sp.simplify(
        effective.subs({a0: lam * a0, cir: lam * cir}, simultaneous=True) - effective) == 0)
    check("P1:action_coefficient_unchanged", sp.simplify(
        (cir / a0).subs({a0: lam * a0, cir: lam * cir}, simultaneous=True) - cir / a0) == 0)
    check("P1:four_ninths_scale", sp.simplify(effective.subs(cm, (sp.Rational(2, 3) * sp.sqrt(cir)) ** sp.Rational(2, 3)) / a0) == sp.Rational(4, 9))

    n = sp.symbols("N", real=True)
    x = sp.symbols("x", real=True)
    hfun = sp.Function("H")(n)
    xfun = sp.Function("x")(n)
    q = (1 + x / 3) / (1 - 2 * x / 3)
    target = sp.Rational(3, 38)
    check("P2:q_x_target", sp.simplify(q.subs(x, target)) == sp.Rational(13, 12))
    direct = hfun * sp.diff(xfun * hfun, n) + 3 * hfun ** 2 * xfun
    required = hfun ** 2 * (sp.diff(xfun, n) + xfun * (3 + sp.diff(hfun, n) / hfun))
    check("P2:required_stress_identity", sp.simplify(direct - required) == 0)
    check("P2:constant_x_shape_drift", sp.simplify(
        sp.diff(sp.exp(target * n), n) / sp.exp(target * n)) == target)
    profile = sp.exp(-3 * n) - sp.exp(-4 * n)
    peak = sp.log(sp.Rational(4, 3))
    check("P2:small_source_peak_time", sp.simplify(sp.diff(profile, n).subs(n, peak)) == 0)
    maximum = sp.simplify(profile.subs(n, peak))
    check("P2:small_source_maximum", maximum == sp.Rational(27, 256))
    check("P2:required_small_source_amplitude", sp.simplify(target / maximum) == sp.Rational(128, 171))
    check("P2:de_Sitter_required_stress", 3 * target == sp.Rational(9, 38))

    cbr = ROOT / "Analysis/Casimir/CBR-001"
    with (cbr / "stage3b_outputs/cbr001_stage3b_thresholds.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    fraction_rows = [row for row in rows if row["epsilon_threshold"]]
    fractions = [float(row["max_abs_casimir_fraction"]) for row in fraction_rows]
    check("P2:four_nonperturbative_one_marginal", sum(f >= 0.1 for f in fractions) == 4
          and sum(0.01 <= f < 0.1 for f in fractions) == 1, fractions=fractions)
    check("P2:five_transient_two_no_crossing_one_invalid",
          {label: sum(row["classification"] == label for row in rows)
           for label in {row["classification"] for row in rows}} == {
               "TRANSIENT_CROSSING": 5, "NO_CROSSING": 2, "INVALID": 1})
    sensitivity_path = cbr / "release_sensitivity_outputs/p2_release_sensitivity_attempt_01/summary.json"
    sensitivity = json.loads(sensitivity_path.read_text(encoding="utf-8"))
    failure = [item for item in sensitivity["checks"] if not item["passed"]]
    check("P2:original_failure_still_a_failure", sensitivity["status"] == "FAIL"
          and sensitivity["passed"] == 18 and sensitivity["total"] == 19
          and len(failure) == 1 and failure[0]["name"] == "r0=1.5:threshold_stable",
          inherited_failure=failure)
    metrics = sensitivity["dynamic_solver"][1]
    relative = abs(metrics["baseline_epsilon"] - metrics["tight_epsilon"]) / abs(metrics["baseline_epsilon"])
    check("P2:reported_threshold_difference", math.isclose(relative,
          8.738442474237357e-5, rel_tol=1e-12), actual=relative)
    plot = ROOT / "papers" / PAPERS["P2"] / "figures/cbr001_stage3b_ratio.png"
    check("P2:figure_data_unchanged", sha(plot) == sha(cbr / "stage3b_outputs/cbr001_stage3b_ratio.png"))
    old_sidecar = HERE / "preserved_rc3" / PAPERS["P1"] / "main.tex.sha256"
    old_claim = old_sidecar.read_text(encoding="ascii").split()[0]
    old_actual = PRE_EDIT_TEX["P1"]
    # A pre-existing mismatch is disclosed, not retroactively called valid.
    provenance_note = {"pre_edit_sidecar_claim": old_claim,
                       "actual_pre_edit_source": old_actual,
                       "matched_at_start": old_claim == old_actual,
                       "original_sidecar_preserved": True}
    h0 = 70 * 1000 / 3.085677581491367e22
    numerical_scale = 299792458 * h0 / (2 * math.pi)
    result = {
        "scope": "P1/P2 rc4 local manuscript algebra and preservation only",
        "checks": checks, "passed": sum(check["passed"] for check in checks),
        "total": len(checks), "validation_pass": all(check["passed"] for check in checks),
        "physics_pass": False, "publication_ready": False,
        "independent_review": "PENDING; local checks are not Rule-9 clearance",
        "inherited_p2_sensitivity": {"status": "FAIL", "passed": 18, "total": 19,
                                    "source_sha256": sha(sensitivity_path)},
        "unresolved": ["P2 threshold peak-time/temporal-grid error certification",
                       "P2 separately evolved mean-Einstein/Raychaudhuri check",
                       "Dynamical renormalized-state calculation outside this closure scope",
                       "Author final cold read and declaration confirmation",
                       "Independent review and immutable public version before publication"],
        "frozen_input_sha256": anchors, "current_source_sha256": current_sources,
        "pre_existing_p1_sidecar_discrepancy": provenance_note,
        "p1_illustrative_units": {"H0_km_s_Mpc": 70, "a0_m_s2": numerical_scale,
                                  "a_eff_m_s2": 4 * numerical_scale / 9,
                                  "velocity_ratio_at_same_a0": math.sqrt(2 / 3)},
    }
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"passed": result["passed"], "total": result["total"],
                      "validation_pass": result["validation_pass"],
                      "inherited_p2_sensitivity": "FAIL 18/19", "physics_pass": False,
                      "receipt": str(args.output.relative_to(ROOT))}))
    return 0 if result["validation_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
