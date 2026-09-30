"""T2P3: coupled finite-mode linear-limit and matter-metric dictionary.

This verifies a bounded consequence of the existing conditional B1/S1/S2
exports. It does not evolve the nonlinear inhomogeneous ITSM equations.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_COUPLED_LINEAR_LIMIT_CONTRACT_2026-09-29.md":
        "84b391bb6da5a6ceabb6feefa03b48f754550fc7f436bfd62033ecdb24267bdb",
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md":
        "4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c",
    "Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md":
        "82708666dfce4ef214b614bc7da31b294d7569539b97292aaa9a79e906e6266f",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md":
        "0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md":
        "653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json":
        "27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_summary.json":
        "10bdc2ac1faeb30203cd75f5015ab41e64dd19b6cef37193f6987baf85bfc033",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json":
        "6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_transfers.json":
        "8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_summary.json":
        "56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735",
    "Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md":
        "81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pin(path: str, expected: str) -> None:
    source = ROOT / path
    if not source.is_file() or sha(source) != expected:
        raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {path}")
    sidecar = source.with_name(source.name + ".sha256")
    if sidecar.exists():
        wanted = f"{expected}  {source.name}\n"
        if sidecar.read_text(encoding="ascii") != wanted:
            raise RuntimeError(f"FROZEN_INPUT_SIDECAR_MISMATCH: {path}")


def verify_sources() -> dict[str, str]:
    for path, expected in PINS.items():
        verify_pin(path, expected)
    inherited: dict[str, str] = {}
    for name in (
        "test_01_r4c1_scalar_constraints_summary.json",
        "test_01_r4c1_scalar_propagation_summary.json",
    ):
        summary = json.loads((ROOT / "Analysis/MasterTests/outputs" / name).read_text())
        if (summary.get("physics_pass") is not False
                or summary.get("gate_effect") != "NONE"
                or summary.get("Rule9_cleared") is not False):
            raise RuntimeError(f"PARENT_STATUS_CHANGED: {name}")
        for group in ("inputs", "artifacts"):
            for path, expected in summary[group].items():
                key = path.replace("\\", "/")
                if key in inherited and inherited[key] != expected:
                    raise RuntimeError(f"CONFLICTING_PARENT_PIN: {key}")
                inherited[key] = expected
    for path, expected in inherited.items():
        verify_pin(path, expected)
    return inherited


def record(checks: list[dict], name: str, passed: bool, **detail: object) -> None:
    checks.append({"name": name, "passed": bool(passed), **detail})


def symbols_for(*expressions: str) -> dict[str, sp.Symbol]:
    words = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", " ".join(expressions)))
    return {word: sp.Symbol(word) for word in words}


def exact_zero(expr: sp.Expr) -> bool:
    return sp.factor(sp.cancel(expr)) == 0


def run() -> dict:
    inherited = verify_sources()
    checks: list[dict] = []
    output = ROOT / "Analysis/MasterTests/outputs"
    s1 = json.loads((output / "test_01_r4c1_scalar_constraints_matrices.json").read_text())
    s2 = json.loads((output / "test_01_r4c1_scalar_propagation_matrices.json").read_text())
    transfers = json.loads((output / "test_01_r4c1_scalar_propagation_transfers.json").read_text())

    record(checks, "S1_field_order",
           s1["q"] == ["du", "dv", "dr", "dpsi", "dtau", "w"]
           and s1["auxiliaries"] == ["alpha", "shift", "depsilon", "z"])
    record(checks, "S1_reduced_shapes",
           all(len(s1[key]) == 6 and all(len(row) == 6 for row in s1[key])
               for key in ("K", "M", "V")))
    record(checks, "S1_preconstraint_shape",
           len(s1["preconstraint_hessian"]) == 16
           and all(len(row) == 16 for row in s1["preconstraint_hessian"]))
    record(checks, "S2_canonical_shapes",
           all(len(s2[key]) == 6 and all(len(row) == 6 for row in s2[key])
               for key in ("q_from_x", "Mc", "Vc", "G", "W")))
    a_token = re.compile(r"(?<![A-Za-z0-9_])A(?![A-Za-z0-9_])")
    matrices = [s1[key] for key in ("K", "M", "V")]
    matrices += [s2[key] for key in ("q_from_x", "Mc", "Vc", "G", "W")]
    record(checks, "quadratic_matrices_independent_of_A",
           not any(a_token.search(str(item)) for matrix in matrices
                   for row in matrix for item in row))

    names = symbols_for(*s1["auxiliary_solutions"][:3])
    names["alpha"] = sp.Symbol("alpha")
    alpha_expr, shift_expr, depsilon_expr = [
        sp.sympify(value, locals=names) for value in s1["auxiliary_solutions"][:3]
    ]
    sym = lambda name: names[name]
    aa, CC, HH, kk = (sym(x) for x in ("a", "C", "H", "k"))
    beta, pd, rho = (sym(x) for x in ("beta", "psi_dot", "rho_m"))
    dpsi, dtau, dtaut = (sym(x) for x in ("dpsi", "dtau", "dtau_t"))
    shift, tdot = sp.symbols("shift tdot")
    T = aa**2 * shift / kk
    phi_from_metric = sp.cancel((2*CC**2*(sym("alpha") + beta*dpsi)
                                 - 2*CC**2*(tdot + beta*pd*T)) / (2*CC**2))
    psi_from_metric = sp.cancel(-(2*CC**2*aa**2*beta*dpsi
                                 - 2*CC**2*aa**2*(HH + beta*pd)*T)
                                / (2*CC**2*aa**2))
    record(checks, "time_shift_removes_matter_shift",
           exact_zero(CC**2 * aa**2 * shift - CC**2 * kk * T))
    record(checks, "matter_Phi_dictionary",
           exact_zero(phi_from_metric
                      - (sym("alpha") + beta*dpsi - tdot - beta*pd*T)))
    record(checks, "matter_Psi_dictionary",
           exact_zero(psi_from_metric - ((HH + beta*pd)*T - beta*dpsi)))
    record(checks, "S1_dust_lapse_constraint",
           exact_zero(alpha_expr + beta*dpsi - dtaut/CC))
    record(checks, "matter_Phi_after_dust_constraint",
           exact_zero(phi_from_metric.subs(sym("alpha"), alpha_expr)
                      - (dtaut/CC - tdot - beta*pd*T)))
    record(checks, "reject_wrong_shift_sign",
           not exact_zero(CC**2*aa**2*shift + CC**2*kk*T))
    record(checks, "reject_omitted_shift_time_derivative",
           not exact_zero(phi_from_metric
                          - (sym("alpha") + beta*dpsi - beta*pd*T)))
    record(checks, "reject_omitted_conformal_background_derivative",
           not exact_zero(phi_from_metric
                          - (sym("alpha") + beta*dpsi - tdot)))

    cL = sym("c1") + sym("c2") + sym("c3")
    Mc2 = sym("MP2") + sym("MU2")*(sym("c1") + 3*sym("c2") + sym("c3"))/2
    de_coeff = sp.diff(depsilon_expr, dtau)
    shift_coeff = sp.diff(shift_expr, dtau)
    de_expected = -2*HH*Mc2*rho/(CC**5*sym("MU2")*cL)
    shift_expected = rho/(CC*sym("MU2")*cL*kk)
    record(checks, "dust_multiplier_density_coefficient",
           exact_zero(de_coeff - de_expected))
    record(checks, "dust_shift_coefficient",
           exact_zero(shift_coeff - shift_expected))
    source_N = sp.cancel(de_coeff + 3*(HH + beta*pd)*(rho/CC**4)
                         *aa**2*shift_coeff/kk)
    initial = {
        aa: 1, CC: 1, HH: sp.sqrt(sp.Rational(3469, 4620)),
        rho: sp.Rational(1, 5), pd: sp.Rational(1, 5),
        beta: sp.Rational(2, 5), sym("MP2"): 1,
        sym("MU2"): sp.Rational(2, 3),
        sym("c1"): sp.Rational(1, 5),
        sym("c2"): sp.Rational(1, 10),
        sym("c3"): -sp.Rational(1, 5), kk: 2*sp.pi,
    }
    density_value = float(source_N.subs(initial).evalf(50))
    record(checks, "nonzero_Jordan_dust_density_in_Newtonian_gauge_n1",
           np.isfinite(density_value) and abs(density_value) > 1e-2,
           amplitude=density_value, threshold_abs=1e-2)
    record(checks, "reject_zero_density_source_claim", abs(density_value) > 1e-2)

    transfer_rows = []
    record(checks, "S2_mode_set", [row["n"] for row in transfers] == [1, 2, 4, 8])
    seed = np.array([1., -2., 3., -4., 5., -6., 2., -1., 4., -3., 6., -5.]) / 6
    for row in transfers:
        n = row["n"]
        methods = {entry["method"]: entry for entry in row["methods"]}
        valid = set(methods) == {"DOP853", "Radau"} and all(
            methods[method]["success"] for method in ("DOP853", "Radau")
        )
        record(checks, f"n{n}_two_solvers_present", valid)
        if not valid:
            continue
        first = np.asarray(methods["DOP853"]["endpoint_transfer"], float)
        second = np.asarray(methods["Radau"]["endpoint_transfer"], float)
        finite = first.shape == (12, 12) and second.shape == (12, 12) \
            and np.all(np.isfinite(first)) and np.all(np.isfinite(second))
        record(checks, f"n{n}_transfer_shape_and_finiteness", finite)
        if not finite:
            continue
        disagreement = float(np.max(abs(first-second))/(1+np.max(abs(second))))
        record(checks, f"n{n}_two_solver_endpoint_agreement",
               disagreement < 1e-5, value=disagreement, threshold=1e-5)
        baseline = first @ seed
        scale_errors = []
        for amplitude in (1., .25, .0625):
            actual = first @ (amplitude*seed)
            error = float(np.max(abs(actual-amplitude*baseline))
                          / (1+amplitude*np.max(abs(baseline))))
            scale_errors.append(error)
        worst_scale = max(scale_errors)
        record(checks, f"n{n}_stored_linear_transfer_scales",
               worst_scale < 1e-12, value=worst_scale, threshold=1e-12)
        transfer_rows.append({"n": n, "endpoint_disagreement": disagreement,
                              "max_scaling_residual": worst_scale})

    passed = sum(check["passed"] for check in checks)
    return {
        "schema": "r4c1-t2p3-coupled-linear-limit-v1",
        "validation": "PASS_LOCAL_CHECKS" if passed == len(checks) else "FAIL_LOCAL_CHECKS",
        "passed": passed, "total": len(checks), "checks": checks,
        "status": "COUPLED_LINEAR_NO_SQRT_ASYMPTOTE_CONDITIONAL_ONLY",
        "scope": "finite nonzero Fourier modes about B1; nonlinear weak-field domain untested",
        "source_sha256": PINS, "transitive_source_sha256": inherited,
        "script_sha256": sha(Path(__file__)),
        "Jordan_density_source_initial_n1": density_value,
        "transfer_checks": transfer_rows,
        "analytic_result": "linear finite-mode IVP and observables scale with amplitude; proof in owning report",
        "C_chi": "NOT_DERIVED", "a0": "NOT_PREDICTED",
        "canonical_Test2_pass": False, "physical_weak_field_solution": False,
        "quasistatic_error_bounded": False, "physical_EFT_domain_proved": False,
        "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
        "review_status": "DEFERRED", "MAT-001": "BLOCKED",
        "UVIR-003": "IN_PROGRESS", "Stage4A": "CLOSED",
    }


def main() -> int:
    receipt = run()
    path = ROOT / "Analysis/MasterTests/outputs/r4c1_t2p3_attempt_01/summary.json"
    payload = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != payload:
            raise RuntimeError(f"EXISTING_RECEIPT_DIFFERS: {path}")
    else:
        with path.open("xb") as stream:
            stream.write(payload)
    sidecar = path.with_name(path.name + ".sha256")
    expected = f"{sha(path)}  {path.name}\n"
    if sidecar.exists():
        if sidecar.read_text(encoding="ascii") != expected:
            raise RuntimeError(f"EXISTING_RECEIPT_SIDECAR_DIFFERS: {sidecar}")
    else:
        with sidecar.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(expected)
    print(json.dumps({"validation": receipt["validation"],
                      "passed": receipt["passed"], "total": receipt["total"],
                      "physics_pass": False, "receipt_sha256": sha(path)}))
    for check in receipt["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    return 0 if receipt["validation"] == "PASS_LOCAL_CHECKS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
