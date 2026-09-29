"""R4C1-C2: bounded periodic contrast response under a frozen A sweep.

The accompanying report gives the continuum convexity argument. This
numerical witness is not a physical torus solution or blind a0 prediction.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

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
    "Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json":
        "49b10df599d6158f02ae6e55febe054f5b6fe2e3a2b53ee70daf7196f44d2fcf",
    "Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md":
        "81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b",
    "Theory/Gates/RES-001/RES001_R4C1_PERIODIC_IDENTIFIABILITY_CONTRACT_2026-09-29.md":
        "dd711d678c824e7f414b9170c164fc3cc101d880134df9d58012a5c0ddbf6d7a",
    "Theory/Gates/RES-001/RES001_R4C1_PERIODIC_IDENTIFIABILITY_PIN_ADDENDUM_2026-09-29.md":
        "637b4b48cd153551dfa98052e1beecace868b4bfd44f9ea38eb15cb0466c65e0",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pins() -> None:
    for rel, expected in PINS.items():
        path = ROOT / rel
        if sha256(path) != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {rel}")
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists() and sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
            raise RuntimeError(f"SOURCE_SIDECAR_MISMATCH: {rel}")


def verify_parent_source_maps() -> dict[str, str]:
    parent_names = (
        "Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json",
        "Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json",
    )
    verified: dict[str, str] = {}
    for parent_name in parent_names:
        parent = json.loads((ROOT / parent_name).read_text(encoding="utf-8"))
        source_map = parent.get("source_sha256")
        if not isinstance(source_map, dict) or not source_map:
            raise RuntimeError(f"PARENT_SOURCE_MAP_MISSING: {parent_name}")
        for rel, expected in source_map.items():
            if rel in verified and verified[rel] != expected:
                raise RuntimeError(f"PARENT_SOURCE_MAP_CONFLICT: {rel}")
            path = ROOT / rel
            if not path.is_file() or sha256(path) != expected:
                raise RuntimeError(f"PARENT_SOURCE_HASH_MISMATCH: {rel}")
            sidecar = path.with_name(path.name + ".sha256")
            if sidecar.exists() and sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
                raise RuntimeError(f"PARENT_SOURCE_SIDECAR_MISMATCH: {rel}")
            verified[rel] = expected
    b1_name = "Analysis/MasterTests/test_01_r4c1_interacting_background.py"
    if verified.get(b1_name) != "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f":
        raise RuntimeError("B1_LITERAL_SOURCE_NOT_PINNED")
    return verified


def record(checks: list[dict], name: str, passed: bool, **details: object) -> None:
    checks.append({"name": name, "passed": bool(passed), **details})


def run() -> dict:
    verify_pins()
    transitive_pins = verify_parent_source_maps()
    # This import is intentionally after the source pin, and its guarded
    # main() is never called; old receipt producers remain untouched.
    import test_02_r4c1_periodic_force as t2

    checks: list[dict] = []
    params = t2.b1_params()
    expected = {"A": Fraction(2, 7), "b": Fraction(5, 11),
                "beta": Fraction(2, 5), "K": Fraction(3)}
    for key, value in expected.items():
        record(checks, f"B1_{key}_frozen", params[key] == value,
               value=str(params[key]), expected=str(value))

    A0, b, beta, K = (params[key] for key in ("A", "b", "beta", "K"))
    ratios = (Fraction(1, 4), Fraction(1), Fraction(4))
    invariant = [sp.simplify(sp.Rational((A0 * ratio).numerator,
                                         (A0 * ratio).denominator) /
                             sp.Rational(K.numerator, K.denominator)**sp.Rational(3, 2))
                 for ratio in ratios]
    record(checks, "physical_A_over_K32_changes_not_chart_rescaling",
           invariant[0] < invariant[1] < invariant[2] and b / K == Fraction(5, 33)
           and beta**2 / K == Fraction(4, 75),
           invariant_values=[str(value) for value in invariant])

    source = ROOT / "Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json"
    parent = json.loads(source.read_text(encoding="utf-8"))
    record(checks, "T2P1_is_local_only_not_parent_promotion",
           parent.get("validation") == "PASS" and parent.get("passed") == parent.get("total") == 46
           and parent.get("physics_pass") is False and parent.get("gate_effect") == "NONE"
           and parent.get("canonical_Test2_pass") is False)
    c1 = json.loads((ROOT / "Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json")
                    .read_text(encoding="utf-8"))
    record(checks, "C1_background_not_Test3_promotion",
           c1.get("physics_pass") is False and c1.get("gate_effect") == "NONE")

    grids: list[dict] = []
    A_float, b_float, beta_float = map(float, (A0, b, beta))
    for n in (17, 25, 33):
        rows: list[dict] = []
        fields: list[np.ndarray] = []
        powers: list[float] = []
        for ratio in ratios:
            grid = t2.TorusGrid(n, A_float * float(ratio), b_float, beta_float)
            linear = grid.linear_solution()
            result = t2.minimize_convex(grid, linear)
            diagnostic = grid.diagnostics(result.x, result)
            psi = result.x.reshape((n, n, n))
            psi = psi - psi.mean()
            gradient = grid.fields(psi)[0]
            cubic_power = float(np.mean(sum(g * g for g in gradient)**1.5))
            row = {"n": n, "A_ratio": str(ratio), "A_invariant": str(invariant[ratios.index(ratio)]),
                   "cubic_gradient_mean": cubic_power, **diagnostic}
            rows.append(row)
            fields.append(psi)
            powers.append(cubic_power)
            tag = f"N{n}_A{ratio}"
            record(checks, tag + "_finite_converged", bool(result.success and
                   np.all(np.isfinite(result.x)) and np.isfinite(cubic_power)),
                   optimizer_message=str(result.message))
            record(checks, tag + "_strong_residual", diagnostic["strong_residual_normalized"] < 1e-5,
                   value=diagnostic["strong_residual_normalized"], threshold=1e-5)
            record(checks, tag + "_zero_mean", abs(diagnostic["psi_mean"]) < 1e-12,
                   value=diagnostic["psi_mean"], threshold=1e-12)
            for label, value in diagnostic["weak_residuals_normalized"].items():
                record(checks, tag + "_weak_" + label, value < 1e-5,
                       value=value, threshold=1e-5)
        reference_rms = float(np.sqrt(np.mean(fields[1]**2)))
        adjacent_sep = [float(np.sqrt(np.mean((fields[i] - fields[i + 1])**2)) /
                              reference_rms) for i in (0, 1)]
        relative_P = [(powers[i] - powers[i + 1]) / powers[1] for i in (0, 1)]
        record(checks, f"N{n}_strict_cubic_power_order",
               powers[0] > powers[1] > powers[2] and min(relative_P) > 1e-4,
               values=powers, relative_adjacent_gaps=relative_P)
        record(checks, f"N{n}_nonzero_response_separation",
               reference_rms > 0 and min(adjacent_sep) > 1e-4,
               relative_adjacent_RMS=adjacent_sep)
        record(checks, f"N{n}_false_equal_response_mutant_rejected",
               all(sep > 1e-4 for sep in adjacent_sep))
        grids.append({"n": n, "branches": rows, "cubic_gradient_means": powers,
                      "relative_adjacent_P_gaps": relative_P,
                      "relative_adjacent_response_RMS": adjacent_sep})

    for ratio_index, ratio in enumerate(ratios):
        for axis in ("x", "y", "z"):
            c25 = grids[1]["branches"][ratio_index]["fundamental_cosine_coefficients"][axis]
            c33 = grids[2]["branches"][ratio_index]["fundamental_cosine_coefficients"][axis]
            change = abs(c25 - c33) / max(abs(c33), 1e-12)
            record(checks, f"A{ratio}_cos_{axis}_grid_25_33", change < 5e-3,
                   relative_change=change, threshold=5e-3)

    zero_controls = []
    for ratio in ratios:
        grid = t2.TorusGrid(17, A_float * float(ratio), b_float, beta_float)
        grid.delta[:] = 0.0
        zero = np.zeros((17, 17, 17))
        energy, derivative = grid.energy_gradient(zero.ravel())
        zero_controls.append((energy, float(np.max(np.abs(derivative)))))
    record(checks, "zero_source_exception_reproduced",
           all(energy == 0.0 and gradient == 0.0 for energy, gradient in zero_controls),
           values=zero_controls)

    passed = sum(bool(item["passed"]) for item in checks)
    return {"schema": "r4c1-c2-periodic-identifiability-v1",
            "validation": "PASS_LOCAL_CHECKS" if passed == len(checks) else "FAIL_LOCAL_CHECKS",
            "passed": passed, "total": len(checks), "checks": checks,
            "status": "CONDITIONAL_T3_ON_SHELL_A_DEPENDENCE_NOT_UNIQUE_CCHI",
            "scope": "static aligned-frame T3 contrast; no coupled physical solution or target data",
            "grids": grids, "zero_source_controls": zero_controls,
            "source_sha256": PINS, "script_sha256": sha256(Path(__file__)),
            "transitive_source_sha256": transitive_pins,
            "continuum_theorem": "separate analytic coercivity/strict-convexity/injectivity/monotonicity argument in owning report; not proved by grid checks",
            "C_chi": "NOT_DERIVED", "a0": "NOT_PREDICTED",
            "canonical_Test3_pass": False, "analyst_blinded": False,
            "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
            "review_status": "DEFERRED", "MAT-001": "BLOCKED",
            "UVIR-003": "IN_PROGRESS", "Stage4A": "CLOSED"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt", default="01", choices=("01", "02", "03"))
    args = parser.parse_args()
    result = run()
    path = ROOT / f"Analysis/MasterTests/outputs/r4c1_c2_attempt_{args.attempt}/summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
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
    print(json.dumps({"validation": result["validation"], "passed": result["passed"],
                      "total": result["total"], "status": result["status"],
                      "physics_pass": False, "receipt_sha256": sha256(path)}))
    for item in result["checks"]:
        if not item["passed"]:
            print(json.dumps(item))
    return 0 if passed_all(result) else 1


def passed_all(result: dict) -> bool:
    return result["validation"] == "PASS_LOCAL_CHECKS"


if __name__ == "__main__":
    raise SystemExit(main())
