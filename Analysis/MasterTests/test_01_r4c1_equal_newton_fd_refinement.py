"""Post-failure R4C1-G3 balance refinement; preserves original 112/113 receipt."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

import test_01_r4c1_equal_newton_family as parent

ROOT = parent.ROOT
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_G3_FD_REFINEMENT_CONTRACT_2026-09-30.md":
        "44ff0e69324dded972029696c445a70f76b94b856771e5e0302fa66b94d722a4",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json":
        "930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy":
        "b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506",
    "Analysis/MasterTests/test_01_r4c1_equal_newton_family.py":
        "dfdec7c78ae4e57f247b2592b611e79d808d708813358a6dac015c387a7d9440",
}


def evaluate():
    parent.verify_inputs(PINS)
    original = json.loads((ROOT / "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json").read_text())
    parent.verify_inputs(original["source_sha256"])
    parent.verify_inputs(original["transitive_source_sha256"])
    import test_01_r4c1_interacting_background as bg
    sampled = np.load(ROOT / "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy", allow_pickle=False)
    p = original["family"][0]["parameters"]
    initial_map = original["family"][0]["runs"]["DOP853"]["initial_state"]
    initial = np.array([initial_map[name] for name in bg.NAMES])
    original_failure = [check for check in original["checks"] if not check["passed"]]
    audit = parent.Audit()
    audit.numeric("original_failure_preserved", len(original_failure) == 1 and
                  original_failure[0]["name"] == "eta1_independent_fd_balances" and
                  original_failure[0]["value"] >= 1e-7,
                  original_failure, "original 801-point balance failure retained")
    rows = []
    for im, method in enumerate(parent.METHODS):
        solution = solve_ivp(lambda t, y: bg.rhs(t, y, p), (0., 4.), initial,
                             method=method, rtol=1e-11, atol=1e-13, dense_output=True)
        audit.numeric(method+"_completed", solution.success and solution.t[-1] == 4,
                      solution.message, "t=4 reached")
        disagreement = float(np.max(np.abs(solution.sol(sampled[0, im, 0])-sampled[0, im, 1:]) /
                                    (1+np.abs(sampled[0, im, 1:]))))
        audit.numeric(method+"_stored_trajectory_agreement", disagreement < 1e-12,
                      disagreement, "<1e-12")
        residuals = [bg.finite_difference_balances(solution, p, n) for n in (801, 1601, 3201)]
        if method == "DOP853":
            audit.numeric("original_801_failure_reproduced", residuals[0]["maximum"] >= 1e-7,
                          residuals[0]["maximum"], "original 1e-7 bound still fails at 801 points")
        for row in residuals[1:]:
            audit.numeric(f"{method}_{row['points']}_balance_bound", row["maximum"] < 1e-7,
                          row["maximum"], "<1e-7 unchanged bound")
            audit.numeric(f"{method}_{row['points']}_spatial_metric_bound",
                          row["full_spatial_metric_fd_residual"] < 1e-7,
                          row["full_spatial_metric_fd_residual"], "<1e-7 unchanged bound")
        improvements = []
        for coarse, fine in zip(residuals, residuals[1:]):
            ratio = coarse["maximum"]/max(fine["maximum"], np.finfo(float).tiny)
            improvements.append(ratio)
            audit.numeric(f"{method}_{coarse['points']}_{fine['points']}_refinement",
                          ratio >= 4 or max(coarse["maximum"], fine["maximum"]) < 1e-9,
                          ratio, ">=4 or endpoint residuals both<1e-9")
        rows.append({"method": method, "stored_trajectory_disagreement": disagreement,
                     "grid_residuals": residuals, "improvement_ratios": improvements})
    passed = sum(bool(c["passed"]) for c in audit.checks)
    return {
        "schema": "r4c1-g3-fd-refinement-v1", "control": "R4C1-G3-FD",
        "validation": "PASS_SUPPLEMENTARY_REFINEMENT" if passed == len(audit.checks) else "FAIL_SUPPLEMENTARY_REFINEMENT",
        "passed": passed, "total": len(audit.checks), "checks": audit.checks,
        "original_validation": original["validation"], "original_passed": original["passed"],
        "original_total": original["total"], "original_failed_checks": original_failure,
        "original_receipt_changed": False, "post_failure_study": True,
        "parameters": p, "methods": rows, "source_sha256": PINS,
        "transitive_source_sha256": {**original["source_sha256"], **original["transitive_source_sha256"]},
        "script_sha256": parent.digest_bytes(Path(__file__).read_bytes()),
        "runtime": {"python": parent.platform.python_version(), "numpy": np.__version__,
                    "scipy": parent.scipy.__version__, "sympy": parent.s.__version__},
        "status": "SUPPLEMENTARY_FD_ERROR_DIAGNOSIS_ORIGINAL_RECEIPT_RETAINED",
        "physics_pass": False, "gate_effect": "NONE", "review_status": "DEFERRED", "Rule9_cleared": False,
        "healthy_continuous_GR_limit_verified": False, "full_interacting_Hessian_verified": False,
        "physical_EFT_cutoff_derived": False, "canonical_Test1_pass": False,
        "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="Analysis/MasterTests/outputs/r4c1_g3_fd_attempt_01")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    directory = (ROOT / args.output_dir).resolve()
    if not directory.is_relative_to(parent.OUTPUT_BASE.resolve()):
        raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    parent.verify_inputs(PINS)
    if not args.replay and directory.exists():
        raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record = evaluate()
    payload = (json.dumps(record, indent=2, allow_nan=False)+"\n").encode("utf-8")
    if args.replay:
        receipt = directory / "summary.json"
        same = receipt.exists() and receipt.read_bytes() == payload
        print(json.dumps({"replay": True, "prior_receipt_present": receipt.exists(), "byte_identical": same}))
    else:
        directory.mkdir(parents=True, exist_ok=False)
        (directory / "summary.json").write_bytes(payload)
        (directory / "summary.json.sha256").write_text(
            f"{parent.digest_bytes(payload)}  summary.json\n", encoding="ascii")
    print(json.dumps({k: record[k] for k in ("validation", "passed", "total", "status", "physics_pass")}))
    for check in record["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    if args.replay and receipt.exists() and not same:
        return 2
    return 0 if passed_all(record) else 1


def passed_all(record):
    return record["passed"] == record["total"]


if __name__ == "__main__":
    raise SystemExit(main())
