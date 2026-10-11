"""Exact comparison of immutable full-v2 and independent temporal kernels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
FULL = BASE + "r4c1_g3n5_attempt_02/"
TIME = BASE + "r4c1_g3n5_time_block_attempt_01/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_G3N5_KERNEL_TIME_COMPARISON_CONTRACT_2026-10-10.md"
PINS = {
    FULL + "summary.json": "560e369d7795ed8e06d0c2c26350d3b412a53c577da82f0669e68f6ee04f5666",
    TIME + "summary.json": "5f079b1e9848dcbdcebac5ffeb7944d9d24f454684b1e0b288f5cebbfd84f265",
    CONTRACT: "2d1098fbb289066ec1bfa141dbd63f9915ea489d7bd23713466f0c746fc71d64",
}
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
SYMBOLS = {name: s.Symbol(name, real=True) for name in
           ("MP2", "MU2", "c1", "c2", "c3", "c4", "K_Q", "C", "epsilon0")}
SYMBOLS.update({name + "_t": s.Symbol(name + "_t", real=True) for name in FIELDS})


def parse(text):
    names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text))
    if "__" in text or not re.fullmatch(r"[A-Za-z_0-9+\-*/(). \t]+", text) or not names <= set(SYMBOLS):
        raise ValueError("Unexpected pure-time expression syntax")
    return s.sympify(text, locals=SYMBOLS)


def merge(pins, name, value):
    if name in pins and pins[name] != value:
        raise ValueError("Conflicting source pin: " + name)
    pins[name] = value


def calculate():
    parents = [common.read_json(folder + "summary.json") for folder in (FULL, TIME)]
    pins = dict(PINS)
    for folder, parent in zip((FULL, TIME), parents):
        for name, value in parent["source_sha256"].items():
            merge(pins, name, value)
        for name, value in parent["artifacts"].items():
            merge(pins, folder + name, value)
    pins[SELF] = common.sha((ROOT / SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("all_source_pins_and_sidecars_before", True,
               {"pins": len(pins), "available_sidecars": len(pins) - len(missing), "known_absent": missing})
    for label, parent in zip(("full_kernel", "independent_time"), parents):
        checks.add(label + "_parent_local_validation", parent["passed"] == parent["total"]
                   and all(row["passed"] for row in parent["checks"]))
        checks.add(label + "_parent_holds_preserved", parent["physics_pass"] is False
                   and parent["gate_effect"] == "NONE" and parent["Rule9_cleared"] is False
                   and parent["canonical_tests_1_to_3"] == "HOLD_SUBSTANTIVE")
    kernel = common.read_json(FULL + "kernel.json")
    old = common.read_json(TIME + "formulas.json")
    checks.add("identical_complete_field_and_jet_order", tuple(parents[0]["response_fields"]) == FIELDS
               and tuple(old["fields"]) == FIELDS and kernel["shape"] == [110, 110]
               and kernel["jet_order"] == list(FIELDS) + [k + "_" + c for c in "txyz" for k in FIELDS])
    entries = {(row["row"], row["column"]): row["value"] for row in kernel["entries"]}
    previous = {(row["row"], row["column"]): row["value"] for row in old["entries"]}
    indices = [kernel["jet_order"].index(k + "_t") for k in FIELDS]
    full = s.Matrix(22, 22, lambda i, j: parse(entries.get((indices[i], indices[j]), "0")))
    time = s.Matrix(22, 22, lambda i, j: parse(previous.get((i, j), "0")))
    residuals = [s.expand(x) for x in full - time]
    failures = [{"row": i // 22, "column": i % 22, "difference": str(x)}
                for i, x in enumerate(residuals) if x != 0]
    checks.add("all_484_temporal_entries_match_exactly", not failures, failures, "zero_exact for all entries")
    checks.add("both_temporal_blocks_exactly_symmetric", full == full.T and time == time.T)
    velocities = s.Matrix([SYMBOLS[k + "_t"] for k in FIELDS])
    density_difference = s.expand((velocities.T * full * velocities)[0] / 2
                                  - parse(old["quadratic_pure_velocity_density_over_a3"]))
    checks.add("pure_time_action_reconstruction_matches_direct_geometry", density_difference == 0,
               str(density_difference), "zero_exact")
    control = {SYMBOLS[k]: s.Rational(v) for k, v in
               dict(MP2="1.1", MU2="0.2", K_Q="0.75", C="1.3", epsilon0="0.07",
                    c1="0.2", c2="-0.14", c3="-0.0125", c4="0.05").items()}
    displaced = s.Matrix(22, 22, lambda i, j: parse(entries.get(
        (indices[(i + 1) % 22], indices[(j + 1) % 22]), "0")))
    checks.add("reject_displaced_time_index", any(s.expand(q).subs(control) != 0 for q in displaced - time),
               "cyclically shifted velocity labels differ at the frozen generic point")
    wrong = full.copy()
    wrong[0, 0] += 1
    checks.add("reject_invented_lapse_velocity", any(s.expand(q).subs(control) != 0 for q in wrong - time))
    inherited = common.read_json(FULL + "independent.json")
    checks.add("original_G3_N3_failures_retained", len(inherited["inherited_failed_parent_checks"]) == 1
               and len(inherited["superseded_N3_attempt_01_failed_checks"]) == 2)
    checks.add("all_source_pins_and_sidecars_after", common.inspect_pins(pins) == missing)
    evidence = {"fields": list(FIELDS), "time_indices_in_full_kernel": indices,
                "exact_entries_compared": 484, "nonzero_differences": failures,
                "pure_time_density_difference": str(density_difference),
                "independent_control_source": TIME,
                "inherited_failed_parent_checks": inherited["inherited_failed_parent_checks"],
                "superseded_N3_attempt_01_failed_checks": inherited["superseded_N3_attempt_01_failed_checks"],
                "nonclaim": "No constraint reduction, solved response, physical DOF count or external review"}
    payloads = {"comparison.json": common.encode(evidence)}
    passed = sum(row["passed"] for row in checks.rows)
    summary = {"schema": "r4c1-g3n5-kernel-time-comparison-v1", "passed": passed,
               "total": len(checks.rows), "checks": checks.rows,
               "validation": "PASS_LOCAL_CHECKS" if passed == len(checks.rows) else "FAIL_LOCAL_CHECKS",
               "status": "FULL_V2_INDEPENDENT_TEMPORAL_COMPARISON_CHECKED" if not failures and passed == len(checks.rows)
                         else "KERNEL_TIME_COMPARISON_REQUIRES_DISPOSITION",
               "source_sha256": dict(sorted(pins.items())), "script_sha256": pins[SELF],
               "artifacts": {name: common.sha(data) for name, data in payloads.items()},
               "inherited_sidecars_absent": missing, "full_kernel_comparison_completed": not failures,
               "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False, "review_status": "DEFERRED",
               "canonical_tests_1_to_3": "HOLD_SUBSTANTIVE", "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS",
               "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED"}
    payloads["summary.json"] = common.encode(summary)
    return payloads, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE + "r4c1_g3n5_time_compare_attempt_01")
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    args = parser.parse_args()
    dest = (ROOT / (args.replay or args.output)).resolve()
    dest.relative_to((ROOT / BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    payloads, summary = calculate()
    if args.replay:
        for name, data in payloads.items():
            if (dest / name).read_bytes() != data or (dest / (name + ".sha256")).read_text() != common.sha(data) + "  " + name + "\n":
                raise RuntimeError("Exact replay mismatch: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            with (dest / name).open("xb") as out:
                out.write(data)
            with (dest / (name + ".sha256")).open("xb") as out:
                out.write((common.sha(data) + "  " + name + "\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action": action, **{k: summary[k] for k in
                     ("validation", "passed", "total", "status", "physics_pass", "gate_effect")}}))
    for row in summary["checks"]:
        if not row["passed"]:
            print(json.dumps(row))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
