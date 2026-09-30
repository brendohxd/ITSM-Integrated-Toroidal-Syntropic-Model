"""Read-only exact finite-b continuation of the R4C1 S1/S2 scalar principal symbol.

This diagnostic never calls the S1/S2 receipt-writing main functions and never
modifies their frozen B1 sources or artifacts. Its PASS is algebraic only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_scalar_constraints as base
import test_01_r4c1_scalar_propagation as s2


ROOT = Path(__file__).resolve().parents[2]
S1 = ROOT / "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json"
S2 = ROOT / "Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json"
PINS = {
    S1: "27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a",
    S2: "6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70",
    ROOT / "Analysis/MasterTests/test_01_r4c1_scalar_constraints.py":
        "977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed",
    ROOT / "Analysis/MasterTests/test_01_r4c1_scalar_propagation.py":
        "745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda",
}


def matrix(raw: list[list[str]], symbols: dict[str, s.Symbol]) -> s.Matrix:
    return s.Matrix([[s.sympify(value, locals=symbols) for value in row] for row in raw])


def exact_zero(value: s.Matrix | s.Expr) -> bool:
    entries = value if isinstance(value, s.MatrixBase) else (value,)
    return all(s.cancel(s.expand(entry)) == 0 for entry in entries)


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool) -> None:
        checks.append({"name": name, "passed": bool(passed)})

    observed = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in PINS}
    for path, expected in PINS.items():
        check("source_pin_" + str(path.relative_to(ROOT)),
              observed[str(path.relative_to(ROOT))] == expected)
    if not all(item["passed"] for item in checks):
        print(json.dumps({"validation": "FAIL_SOURCE_PIN", "checks": checks,
                          "observed_sha256": observed}, indent=2))
        return 1

    raw1 = json.loads(S1.read_text(encoding="utf-8"))
    raw2 = json.loads(S2.read_text(encoding="utf-8"))
    symbols = {str(value): value for value in vars(base).values()
               if isinstance(value, s.Symbol)}
    K, M, V = (matrix(raw1[key], symbols) for key in ("K", "M", "V"))
    a, H, k, pd, C, b = base.a, base.H, base.k, base.pd, base.C, base.b
    check("K_and_M_independent_of_b", not K.has(b) and not M.has(b))
    check("V_affine_in_b", exact_zero(V.diff(b, 2)))

    Dq = V.diff(b)
    expected_q = s.zeros(6)
    expected_q[3, 3] = k**4 / a**4
    expected_q[3, 5] = expected_q[5, 3] = -k**3 * pd / a**3
    expected_q[5, 5] = k**2 * pd**2 / a**2
    check("exact_S1_regulator_matrix", exact_zero(Dq - expected_q))

    J = s.eye(6)
    J[:, 4] = s.Matrix([base.ud, base.vd, base.rd, pd, C, k/a])
    R = J * s.diag(1, 1, 1, 1/s.sqrt(3),
                   1/(s.sqrt(66)*H), s.sqrt(6)) / a**s.Rational(3, 2)
    D = (a**3 * R.T * Dq * R).applyfunc(s.cancel)
    p = s.Symbol("p", real=True)
    Dp = D.subs(k, a*p).applyfunc(s.cancel)
    expected = s.zeros(6)
    expected[3, 3] = p**4/3
    expected[3, 5] = expected[5, 3] = -s.sqrt(2)*pd*p**3
    expected[5, 5] = 6*pd**2*p**2
    check("exact_canonical_regulator_matrix", exact_zero(Dp-expected))
    check("canonical_regulator_rank_one", exact_zero(D[3, 3]*D[5, 5]-D[3, 5]**2))

    W = matrix(raw2["W"], symbols)
    G = matrix(raw2["G"], symbols)
    slow = [0, 1, 2, 4, 5]
    b0 = s.Rational(5, 11)

    def coeff(mat: s.Matrix, degree: int) -> s.Matrix:
        mp = mat.subs(k, a*p)
        return mp.applyfunc(lambda entry: s.Poly(s.cancel(entry), p).nth(degree))

    W2 = coeff(W, 2).extract(slow, slow)
    cross = coeff(W, 3).extract(slow, [3])
    v4 = coeff(W, 4)[3, 3]
    G1 = coeff(G, 1).extract(slow, slow)
    L0 = matrix(raw2["slow_principal_V"], symbols)
    G0 = matrix(raw2["slow_principal_G"], symbols)
    check("frozen_quartic_coefficient", exact_zero(v4-b0/3))
    expected_cross = s.Matrix([0, 0, 0, 0, -s.sqrt(2)*b0*pd])
    check("frozen_cubic_cross", exact_zero(cross-expected_cross))
    check("frozen_slow_Schur_recomputed", exact_zero(W2-cross*cross.T/v4-L0))
    check("frozen_slow_gyro_recomputed", exact_zero(G1-G0))

    db = b-b0
    W2b = W2 + db*coeff(D, 2).extract(slow, slow)
    crossb = cross + db*coeff(D, 3).extract(slow, [3])
    v4b = v4 + db*coeff(D, 4)[3, 3]
    Lb = W2b-crossb*crossb.T/v4b
    check("positive_b_quartic_is_b_over_3", exact_zero(v4b-b/3))
    check("positive_b_slow_principal_invariant", exact_zero(Lb-L0))
    check("Schur_omission_rejected", not exact_zero(W2b-W2))
    auxdet = s.sympify(raw1["auxiliary_determinant"], locals=symbols)
    expected_det = C**8*base.MU*b*k**2*(base.c1+base.c2+base.c3)
    check("auxiliary_determinant_factor", exact_zero(auxdet-expected_det))
    check("b_zero_singular_endpoint_rejected",
          exact_zero(auxdet.subs(b, 0)) and
          not exact_zero(auxdet.subs(s2.PARAMETER_SUBS)))

    passed = sum(bool(item["passed"]) for item in checks)
    result = {
        "schema": "r4c1-finite-b-principal-v1",
        "validation": "PASS" if passed == len(checks) else "FAIL",
        "passed": passed,
        "total": len(checks),
        "candidate": "R4C1-v1",
        "domain": "finite b>0; same B1 background and other coefficients; H!=0; k!=0",
        "principal_fast_omega_squared_over_p4": "b/3",
        "slow_principal_b_dependence": "none",
        "slow_characteristic": raw2["slow_characteristic"],
        "zero_branch_status": "defective in the inherited canonical chart",
        "physics_pass": False,
        "gate_effect": "NONE",
        "Rule9_cleared": False,
        "review_status": "DEFERRED",
        "limitations": ["No b=0 continuation", "No uniform energy or full IVP result",
                        "No physical EFT cutoff", "No nonlinear coupled force-law proof"],
        "source_sha256": observed,
        "checks": checks,
    }
    print(json.dumps(result, indent=2))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
