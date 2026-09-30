"""Read-only finite-b linear scalar transfer on the pinned R4C1 B1 background.

Prints a machine-readable diagnostic; never calls any upstream main() and
never writes, replaces, or rehashes the frozen S1/S2 receipts.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

import test_01_r4c1_scalar_constraints as base
import test_01_r4c1_scalar_propagation as s2
import test_01_r4c1_interacting_background as bg
from test_01_r4c1_finite_b_principal import exact_zero, matrix


ROOT = Path(__file__).resolve().parents[2]
PINNED = {
    "Theory/Gates/RES-001/RES001_R4C1_FINITE_B_TRANSFER_CONTRACT_2026-09-30.md":
        "f2635f9754d6a2b597711057b8294a2d3d0247c864a277bf2d7e2bb75ec4a108",
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json":
        "27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json":
        "6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_transfers.json":
        "8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_summary.json":
        "56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv":
        "0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa",
    "Analysis/MasterTests/test_01_r4c1_finite_b_principal.py":
        "0e2c7f4babce65e04ad828e7f6da29248e4a3161b31ca174cdcd0980518aa7b5",
}
CASES = (("baseline", 1, s.Rational(5, 11)),
         ("corridor-1", 1, s.Rational(1, 1250)),
         ("corridor-2", 2, s.Rational(1, 10000)))
GRID = np.linspace(0.0, 4.0, 101)
SYMPLECTIC = np.block([[np.zeros((6, 6)), np.eye(6)],
                       [-np.eye(6), np.zeros((6, 6))]])


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, value: object = None,
              criterion: str | None = None) -> None:
        checks.append(dict(name=name, passed=bool(passed), value=value,
                           criterion=criterion))

    observed = {name: sha(ROOT / name) for name in PINNED}
    for name, digest in PINNED.items():
        check("source_pin_" + name, observed[name] == digest, observed[name], digest)
    if not all(item["passed"] for item in checks):
        print(json.dumps(dict(validation="FAIL_SOURCE_PIN", checks=checks), indent=2))
        return 1

    receipt = json.loads((ROOT / "Analysis/MasterTests/outputs/"
                          "test_01_r4c1_scalar_propagation_summary.json").read_text())
    for name, digest in {**receipt["inputs"], **receipt["artifacts"]}.items():
        check("S2_transitive_pin_" + name, sha(ROOT / name) == digest)
    check("S2_reference_scoped",
          receipt["validation"] == "PASS" and receipt["physics_pass"] is False
          and receipt["gate_effect"] == "NONE")
    if not all(item["passed"] for item in checks):
        print(json.dumps(dict(validation="FAIL_TRANSITIVE_PIN", checks=checks), indent=2))
        return 1

    symbols = {str(v): v for v in vars(base).values() if isinstance(v, s.Symbol)}
    raw1 = json.loads((ROOT / "Analysis/MasterTests/outputs/"
                       "test_01_r4c1_scalar_constraints_matrices.json").read_text())
    raw2 = json.loads((ROOT / "Analysis/MasterTests/outputs/"
                       "test_01_r4c1_scalar_propagation_matrices.json").read_text())
    K, M, V = (matrix(raw1[key], symbols) for key in ("K", "M", "V"))
    a, H, k, pd, C = base.a, base.H, base.k, base.pd, base.C
    check("K_M_b_independent", not K.has(base.b) and not M.has(base.b))
    check("V_b_affine", exact_zero(V.diff(base.b, 2)))
    J = s.eye(6)
    J[:, 4] = s.Matrix([base.ud, base.vd, base.rd, pd, C, k/a])
    R = J*s.diag(1, 1, 1, 1/s.sqrt(3), 1/(s.sqrt(66)*H), s.sqrt(6)) / a**s.Rational(3, 2)
    D = (a**3*R.T*V.diff(base.b)*R).applyfunc(s.cancel)
    expected_D = s.zeros(6)
    expected_D[3, 3] = k**4/(3*a**4)
    expected_D[3, 5] = expected_D[5, 3] = -s.sqrt(2)*pd*k**3/a**3
    expected_D[5, 5] = 6*pd**2*k**2/a**2
    check("exact_b_derivative_matches_principal_audit", exact_zero(D-expected_D))
    if not all(item["passed"] for item in checks):
        print(json.dumps(dict(validation="FAIL_ALGEBRA", checks=checks), indent=2))
        return 1

    Mc, G, W0 = (matrix(raw2[key], symbols) for key in ("Mc", "G", "W"))
    fMc = s.lambdify(s2.ARGS, Mc, "numpy", cse=True)
    fG = s.lambdify(s2.ARGS, G, "numpy", cse=True)
    flow = bg.integrate(bg.PARAMS, "DOP853", 1e-12, 1e-14)
    pinned = np.genfromtxt(ROOT / "Analysis/MasterTests/outputs/"
                           "test_01_r4c1_interacting_background_trajectory.csv",
                           delimiter=",", names=True)
    reference = np.vstack([pinned[name] for name in bg.NAMES])
    bg_error = float(np.max(abs(flow.sol(pinned["t"])-reference)/(1+abs(reference))))
    check("background_reproduces_pin", flow.success and bg_error < 1e-8,
          bg_error, "<1e-8")
    for label, _, bvalue in CASES:
        variant = dict(bg.PARAMS, b=float(bvalue))
        initial_equal = np.array_equal(bg.initial(variant), bg.initial(bg.PARAMS))
        rhs_equal = all(np.array_equal(bg.rhs(t, flow.sol(t), variant),
                                       bg.rhs(t, flow.sol(t), bg.PARAMS))
                        for t in (0., .5, 1., 2., 3., 4.))
        check(label+"_homogeneous_b_independence", initial_equal and rhs_equal)
    if not all(item["passed"] for item in checks):
        print(json.dumps(dict(validation="FAIL_BACKGROUND", checks=checks), indent=2))
        return 1

    frozen = json.loads((ROOT / "Analysis/MasterTests/outputs/"
                         "test_01_r4c1_scalar_propagation_transfers.json").read_text())
    frozen_baseline = np.asarray(next(row for row in frozen if row["n"] == 1)
                                 ["methods"][0]["endpoint_transfer"], float)
    rows = []
    for label, n, bvalue in CASES:
        b_float = float(bvalue)
        Wb = W0 + (bvalue-s.Rational(5, 11))*D
        fW = s.lambdify(s2.ARGS, Wb, "numpy", cse=True)
        wavenumber = float(2*np.pi*n)
        delta2 = float(bvalue**2*(2*s.pi*n)**5 /
                       (3*s.Rational(2, 7)*s.Rational(2, 5)*s.Rational(1, 50)))
        if label != "baseline":
            check(label+"_in_predeclared_contrast_window", delta2 < 1,
                  delta2, "necessary algebraic delta^2<1")

        def coeff(t: float) -> tuple[np.ndarray, np.ndarray]:
            args = s2.background_args(flow.sol(t), wavenumber)
            return np.asarray(fG(*args), float), np.asarray(fW(*args), float)

        def rhs(t: float, flat: np.ndarray) -> np.ndarray:
            gg, ww = coeff(t)
            F = flat.reshape(12, 12)
            return np.vstack((F[6:], -ww@F[:6]-gg@F[6:])).ravel()

        def jac(t: float, flat: np.ndarray) -> np.ndarray:
            gg, ww = coeff(t)
            return np.kron(s2.generator(gg, ww), np.eye(12))

        local_exponents = []
        for t in (0., 2., 4.):
            gg, ww = coeff(t)
            eigenvalues = np.linalg.eigvals(s2.generator(gg, ww))
            local_exponents.append(dict(t=t,
                max_positive_real=float(max(0., np.max(np.real(eigenvalues)))),
                max_abs_real=float(np.max(abs(np.real(eigenvalues))))))

        method_rows = []
        solutions = []
        for method in ("DOP853", "Radau"):
            started = time.monotonic()
            options = dict(jac=jac) if method == "Radau" else {}
            sol = solve_ivp(rhs, (0., 4.), np.eye(12).ravel(), method=method,
                            rtol=1e-9, atol=1e-11, t_eval=GRID, **options)
            ok = bool(sol.success and sol.t[-1] == 4. and np.all(np.isfinite(sol.y)))
            check(label+"_"+method+"_solver", ok, sol.message,
                  "success, t_end=4, finite")
            if not ok:
                method_rows.append(dict(method=method, success=False, message=sol.message))
                continue
            F = sol.y.T.reshape(-1, 12, 12)
            solutions.append(F)
            m0 = np.asarray(fMc(*s2.background_args(flow.sol(0.), wavenumber)), float)
            T0 = np.block([[np.eye(6), np.zeros((6, 6))], [m0, np.eye(6)]])
            T0inv = np.linalg.inv(T0)
            chart_amps = []
            canonical_amps = []
            sym_error = 0.
            for j, t in enumerate(GRID):
                mt = np.asarray(fMc(*s2.background_args(flow.sol(t), wavenumber)), float)
                Tt = np.block([[np.eye(6), np.zeros((6, 6))], [mt, np.eye(6)]])
                can = Tt@F[j]@T0inv
                resid = np.linalg.norm(can.T@SYMPLECTIC@can-SYMPLECTIC, 2)/(
                    1+np.linalg.norm(can, 2)**2)
                sym_error = max(sym_error, float(resid))
                chart_amps.append(float(np.linalg.svd(F[j], compute_uv=False)[0]))
                canonical_amps.append(float(np.linalg.svd(can, compute_uv=False)[0]))
            check(label+"_"+method+"_symplectic", sym_error < 1e-6,
                  sym_error, "<1e-6")
            method_rows.append(dict(method=method, success=True, nfev=sol.nfev,
                njev=sol.njev, seconds=time.monotonic()-started,
                max_symplectic_residual=sym_error,
                max_chart_amplification=max(chart_amps),
                endpoint_chart_amplification=chart_amps[-1],
                max_canonical_chart_amplification=max(canonical_amps),
                endpoint_transfer_sha256=hashlib.sha256(
                    np.asarray(F[-1], dtype="<f8").tobytes()).hexdigest()))
            if label == "baseline" and method == "DOP853":
                error = float(np.max(abs(F[-1]-frozen_baseline)) /
                              (1+np.max(abs(frozen_baseline))))
                check("baseline_endpoint_reproduces_frozen_S2", error < 1e-7,
                      error, "<1e-7")

        discrepancy = None
        if len(solutions) == 2:
            discrepancy = float(np.max(abs(solutions[0]-solutions[1])) /
                                (1+np.max(abs(solutions[1]))))
            check(label+"_two_solver_agreement", discrepancy < 1e-5,
                  discrepancy, "<1e-5")
        rows.append(dict(label=label, n=n, b=str(bvalue), k=wavenumber,
                         conditional_delta_squared=delta2,
                         local_instantaneous_exponents=local_exponents,
                         two_solver_discrepancy=discrepancy, methods=method_rows))

    count = sum(bool(item["passed"]) for item in checks)
    result = dict(schema="r4c1-finite-b-transfer-v1",
                  validation="PASS" if count == len(checks) else "FAIL",
                  passed=count, total=len(checks),
                  status=("FINITE_B_LINEAR_TRANSFER_VALIDATED_ONLY"
                          if count == len(checks) else "UNVALIDATED"),
                  physics_pass=False, gate_effect="NONE", Rule9_cleared=False,
                  review_status="DEFERRED", source_sha256=observed,
                  background_max_normalized_error=bg_error,
                  rows=rows, checks=checks,
                  limitations=["conditional linear scalar B1 chart only",
                               "delta<1 is not force-law accuracy",
                               "chart amplification is not invariant stability",
                               "no physical EFT cutoff or nonlinear coupled solve",
                               "no b=0 continuation or canonical gate promotion"])
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
