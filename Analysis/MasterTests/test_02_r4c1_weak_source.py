"""R4C1-T2P2 finite-b small-source diagnostic on a fixed-frame T3 snapshot.

The continuum estimate is written in the owning report. Grid checks do not
solve the coupled metric/frame/dust system or promote Master Test 2.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md":
        "c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a",
    "Theory/Gates/RES-001/RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md":
        "5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad",
    "Analysis/MasterTests/test_02_r4c1_periodic_force.py":
        "8e1b398c70cd1308252d743acbb4d2a7fcef02c28d3b79b0f124f5c3f85a6727",
    "Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json":
        "fb59f3bf28e1b57c5294448f011731e805fe2f7928d12d40de210abb24f762bc",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md":
        "81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b",
    "Theory/Gates/RES-001/RES001_R4C1_WEAK_SOURCE_CONTRACT_2026-09-29.md":
        "53542c4c5c850bb299937634fc49abe702b4d54871b4f7181d15a2730a7ed271",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pins() -> dict[str, str]:
    for rel, expected in PINS.items():
        path = ROOT / rel
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {rel}")
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists() and sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
            raise RuntimeError(f"FROZEN_INPUT_SIDECAR_MISMATCH: {rel}")
    parent_name = "Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json"
    parent = json.loads((ROOT / parent_name).read_text(encoding="utf-8"))
    if (parent.get("validation") != "PASS" or parent.get("passed") != 46
            or parent.get("total") != 46 or parent.get("physics_pass") is not False
            or parent.get("gate_effect") != "NONE"):
        raise RuntimeError("PARENT_RECEIPT_STATUS_MISMATCH")
    inherited = parent.get("source_sha256")
    if not isinstance(inherited, dict) or not inherited:
        raise RuntimeError("PARENT_SOURCE_MAP_MISSING")
    for rel, expected in inherited.items():
        path = ROOT / rel
        if not path.is_file() or sha256(path) != expected:
            raise RuntimeError(f"PARENT_SOURCE_HASH_MISMATCH: {rel}")
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists() and sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
            raise RuntimeError(f"PARENT_SOURCE_SIDECAR_MISMATCH: {rel}")
    b1_name = "Analysis/MasterTests/test_01_r4c1_interacting_background.py"
    if inherited.get(b1_name) != PINS[b1_name]:
        raise RuntimeError("B1_SOURCE_PIN_CONFLICT")
    return inherited


def record(checks: list[dict], name: str, passed: bool, **detail: object) -> None:
    checks.append({"name": name, "passed": bool(passed), **detail})


def run() -> dict:
    inherited = verify_pins()
    # Import definitions only after checking the module and its sources.
    import test_02_r4c1_periodic_force as t2

    checks: list[dict] = []
    params = t2.b1_params()
    expected = {"A": Fraction(2, 7), "b": Fraction(5, 11),
                "beta": Fraction(2, 5), "K": Fraction(3)}
    for key, value in expected.items():
        record(checks, f"B1_{key}_frozen", params[key] == value,
               value=str(params[key]), expected=str(value))
    A, b, beta = (float(params[key]) for key in ("A", "b", "beta"))
    epsilons = (Fraction(1), Fraction(1, 4), Fraction(1, 16),
                Fraction(1, 64), Fraction(1, 256))
    all_grids: list[dict] = []
    for n in (17, 25, 33):
        branches: list[dict] = []
        for epsilon in epsilons:
            e = float(epsilon)
            grid = t2.TorusGrid(n, A, b, beta)
            grid.delta *= e
            grid.source_scale *= e
            linear = grid.linear_solution()
            analytic_linear = -(beta / b) * grid.delta
            linear_exact_difference = float(np.max(np.abs(linear - analytic_linear)))
            record(checks, f"N{n}_e{epsilon}_linear_field_exact",
                   linear_exact_difference < 1e-12,
                   value=linear_exact_difference, threshold=1e-12)
            control = t2.TorusGrid(n, 0.0, b, beta)
            control.delta *= e
            control.source_scale *= e
            _, linear_gradient = control.energy_gradient(linear.ravel())
            linear_residual = float(np.sqrt(np.mean(linear_gradient**2)) / grid.source_scale)
            record(checks, f"N{n}_e{epsilon}_A0_residual",
                   linear_residual < 1e-10,
                   value=linear_residual, threshold=1e-10)
            result = t2.minimize_convex(grid, linear)
            diag = grid.diagnostics(result.x, result)
            psi = result.x.reshape((n, n, n))
            psi = psi - psi.mean()
            relative_to_linear = float(np.sqrt(np.mean((psi - linear)**2)) /
                                       np.sqrt(np.mean(linear**2)))
            gradients = grid.fields(psi)[0]
            gradient_rms = float(np.sqrt(np.mean(sum(g * g for g in gradients))))
            force_over_sqrt_e = beta * gradient_rms / np.sqrt(e)
            branches.append({"epsilon": str(epsilon), "n": n,
                             "relative_nonlinear_correction": relative_to_linear,
                             "force_over_sqrt_epsilon": force_over_sqrt_e,
                             "gradient_rms": gradient_rms,
                             "linear_residual_normalized": linear_residual,
                             **diag})
            tag = f"N{n}_e{epsilon}"
            record(checks, tag + "_finite_converged",
                   result.success and np.all(np.isfinite(result.x)) and
                   np.isfinite(relative_to_linear) and np.isfinite(force_over_sqrt_e),
                   optimizer_message=str(result.message))
            record(checks, tag + "_zero_mean_positive_density",
                   abs(diag["psi_mean"]) < 1e-12 and
                   abs(diag["source_mean"]) < 1e-12 and
                   diag["total_density_min"] >= 2 / 25 - 1e-12,
                   values=[diag["psi_mean"], diag["source_mean"], diag["total_density_min"]])
            record(checks, tag + "_strong_residual",
                   diag["strong_residual_normalized"] < 1e-5,
                   value=diag["strong_residual_normalized"], threshold=1e-5)
            for label, value in diag["weak_residuals_normalized"].items():
                record(checks, tag + "_weak_" + label, value < 1e-5,
                       value=value, threshold=1e-5)
        corrections = [row["relative_nonlinear_correction"] for row in branches]
        record(checks, f"N{n}_linear_limit_monotone",
               all(corrections[i] > corrections[i + 1] for i in range(4))
               and corrections[-1] < 1e-2,
               values=corrections, final_threshold=1e-2)
        forces = [row["force_over_sqrt_epsilon"] for row in branches]
        ratio = forces[3] / forces[4]
        record(checks, f"N{n}_force_sqrt_ratio",
               1.5 <= ratio <= 2.5, value=ratio, interval=[1.5, 2.5])
        record(checks, f"N{n}_finite_b_indispensable_at_small_e",
               branches[-1]["omit_b_residual_normalized"] > 1e-2,
               value=branches[-1]["omit_b_residual_normalized"], threshold=1e-2)
        all_grids.append({"n": n, "branches": branches,
                          "relative_corrections": corrections,
                          "force_over_sqrt_epsilon": forces,
                          "small_e_force_ratio": ratio})
    for e_index, epsilon in enumerate(epsilons):
        for axis in ("x", "y", "z"):
            c25 = all_grids[1]["branches"][e_index]["fundamental_cosine_coefficients"][axis]
            c33 = all_grids[2]["branches"][e_index]["fundamental_cosine_coefficients"][axis]
            change = abs(c25 - c33) / max(abs(c33), 1e-12)
            record(checks, f"e{epsilon}_cos_{axis}_grid_25_33",
                   change < 5e-3, relative_change=change, threshold=5e-3)
    zero_grid = t2.TorusGrid(17, A, b, beta)
    zero_grid.delta[:] = 0.0
    zero = np.zeros((17, 17, 17))
    zero_energy, zero_derivative = zero_grid.energy_gradient(zero.ravel())
    zero_force = float(max(np.max(np.abs(component))
                           for component in zero_grid.fields(zero)[0]))
    record(checks, "zero_source_zero_field_force_control",
           zero_energy == 0.0 and np.max(np.abs(zero_derivative)) == 0.0
           and zero_force == 0.0,
           energy=zero_energy, derivative_max=float(np.max(np.abs(zero_derivative))),
           force_max=zero_force)
    passed = sum(bool(item["passed"]) for item in checks)
    return {"schema": "r4c1-t2p2-weak-source-v1",
            "validation": "PASS_LOCAL_CHECKS" if passed == len(checks) else "FAIL_LOCAL_CHECKS",
            "passed": passed, "total": len(checks), "checks": checks,
            "status": "FINITE_B_WEAK_SOURCE_LINEAR_CONDITIONAL_ONLY",
            "scope": "static aligned-frame T3 contrast; no coupled physical weak-field solution",
            "grids": all_grids, "source_sha256": PINS,
            "transitive_source_sha256": inherited,
            "script_sha256": sha256(Path(__file__)),
            "theorem": "continuum H2 estimate separate in owning report, not proven by grid checks",
            "canonical_Test2_pass": False, "physical_periodic_solution_verified": False,
            "quasistatic_error_bounded": False, "physical_EFT_domain_proved": False,
            "C_chi": "NOT_DERIVED", "a0": "NOT_PREDICTED",
            "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
            "review_status": "DEFERRED", "MAT-001": "BLOCKED",
            "UVIR-003": "IN_PROGRESS", "Stage4A": "CLOSED"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt", default="01", choices=("01", "02", "03"))
    args = parser.parse_args()
    receipt = run()
    path = ROOT / f"Analysis/MasterTests/outputs/r4c1_t2p2_attempt_{args.attempt}/summary.json"
    payload = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise RuntimeError(f"EXISTING_RECEIPT_DIFFERS: {path}")
    else:
        with path.open("xb") as stream:
            stream.write(payload)
    sidecar = path.with_name(path.name + ".sha256")
    sidecar_text = f"{sha256(path)}  {path.name}\n"
    if sidecar.exists():
        if sidecar.read_text(encoding="ascii") != sidecar_text:
            raise RuntimeError(f"EXISTING_RECEIPT_SIDECAR_DIFFERS: {sidecar}")
    else:
        with sidecar.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(sidecar_text)
    print(json.dumps({"validation": receipt["validation"], "passed": receipt["passed"],
                      "total": receipt["total"], "status": receipt["status"],
                      "physics_pass": False, "receipt_sha256": sha256(path)}))
    for item in receipt["checks"]:
        if not item["passed"]:
            print(json.dumps(item))
    return 0 if receipt["validation"] == "PASS_LOCAL_CHECKS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
