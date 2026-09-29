"""R4C1-PD1 exact necessary-condition audit; no physical EFT cutoff inferred.

Reads a pinned B1 parameter literal without importing/running any prior
receipt-producing script. A local PASS is not a Test-1 physics pass.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md":
        "b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md":
        "653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9",
    "Theory/Gates/RES-001/RES001_R4C1_S4H_UNIFORM_ENVELOPE_REPORT_2026-09-29.md":
        "3517579269b26bed5e9c03315dba67d7241442ec690f332b3808576861001314",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Theory/Gates/ITSM_MASTER_TEST_01_SOURCE_VECTOR_CLOSURE_CONTRACT_2026-09-24.md":
        "a1fa48eca3db80b510b111d0bc22b5d92904eaa78f4d6e0dbab6840cbc3b7448",
    "Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_DOMAIN_PREFLIGHT_CONTRACT_2026-09-29.md":
        "64c2b954071dc294475324290e7046d7bdaf42615518da4b755c4c4a9bf4b73b",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pinned_sources() -> None:
    for rel, expected in PINS.items():
        path = ROOT / rel
        if sha256(path) != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {rel}")
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists():
            if sidecar.read_text(encoding="ascii").strip() != f"{expected}  {path.name}":
                raise RuntimeError(f"SOURCE_SIDECAR_MISMATCH: {rel}")


def fraction_literal(node: ast.AST) -> Fraction:
    """Evaluate only arithmetic literals in B1's pinned PARAMS declaration."""
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return Fraction(str(node.value))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = fraction_literal(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left, right = fraction_literal(node.left), fraction_literal(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    raise ValueError("Nonliteral B1 parameter expression")


def b1_literals() -> dict[str, sp.Rational]:
    rel = "Analysis/MasterTests/test_01_r4c1_interacting_background.py"
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
    matches = [node.value for node in tree.body
               if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == "PARAMS"
                       for target in node.targets)]
    if len(matches) != 1 or not isinstance(matches[0], ast.Call):
        raise ValueError("B1 PARAMS declaration not uniquely found")
    call = matches[0]
    if not isinstance(call.func, ast.Name) or call.func.id != "dict" or call.args:
        raise ValueError("B1 PARAMS is not a literal dict call")
    values = {}
    for item in call.keywords:
        if item.arg is None:
            raise ValueError("B1 PARAMS expansion is not allowed")
        value = fraction_literal(item.value)
        values[item.arg] = sp.Rational(value.numerator, value.denominator)
    return values


def run_checks() -> dict:
    params = b1_literals()
    checks = []

    def exact(name: str, value, expected=0) -> None:
        residual = sp.simplify(value - expected)
        checks.append({"name": name, "passed": residual == 0,
                       "residual": str(residual), "expected": "zero_exact"})

    def true(name: str, predicate, detail: str) -> None:
        checks.append({"name": name, "passed": bool(predicate), "detail": detail})

    a14, a13, a2 = sp.symbols("alpha14 alpha13 alpha2", real=True)
    d_stat = 1 - a14 / 2
    d_cos = 1 + (a13 + 3 * a2) / 2
    equality_surface = a14 + a13 + 3 * a2
    exact("static_cosmological_equality_surface", d_stat - d_cos,
          -equality_surface / 2)

    mu, mp = params["MU2"], params["MP2"]
    c1, c2, c3, c4 = (params[key] for key in ("c1", "c2", "c3", "c4"))
    B14, B13, B2 = mu * (c1 + c4) / mp, mu * (c1 + c3) / mp, mu * c2 / mp
    fixed_surface = sp.simplify(equality_surface.subs({a14: B14, a13: B13, a2: B2}))
    ratio = sp.simplify((d_stat / d_cos).subs({a14: B14, a13: B13, a2: B2}))
    exact("B1_alpha14", B14, sp.Rational(1, 6))
    exact("B1_alpha13", B13)
    exact("B1_three_alpha2", 3 * B2, sp.Rational(1, 5))
    exact("B1_equality_surface_offset", fixed_surface, sp.Rational(11, 30))
    exact("B1_Gcos_over_Gstatic", ratio, sp.Rational(5, 6))
    true("zero_exchange_not_pure_GR", ratio != 1,
         "fixed B1 frame; isolated nonzero-mode control only")
    bare_ratio = sp.simplify((d_stat / d_cos).subs(
        {a14: c1 + c4, a13: c1 + c3, a2: c2}))
    true("bare_c_i_mutant_rejected", bare_ratio != ratio,
         f"bare ratio {bare_ratio} differs from normalized {ratio}")

    eta = sp.symbols("eta", positive=True)
    K, A, b = params["K"], params["A"], params["b"]
    canonical_cubic = sp.simplify((A * eta) / (K * eta) ** sp.Rational(3, 2))
    exact("registered_canonical_cubic", canonical_cubic,
          2 * sp.sqrt(3) / (63 * sp.sqrt(eta)))
    true("registered_cubic_diverges", sp.limit(canonical_cubic, eta, 0) == sp.oo,
         "q=a=1 gives eta^(-1/2), not a uniformly weak canonical limit")
    q = sp.Rational(1)
    true("monomial_exponent_rejection_controls",
         all((a - 3 * q / 2 >= 0) == expected
             for a, expected in ((sp.Rational(1), False),
                                 (sp.Rational(3, 2), True),
                                 (sp.Rational(2), True))),
         "for q>0 and positive coefficients, non-divergence needs a>=3q/2")

    # These are dimensions of coefficients, NOT scattering or EFT cutoffs.
    dimK, dimA, dimb = 2, 1, 0
    exact("regulator_scale_mass_dimension", sp.Rational(dimK - dimb, 2), 1)
    exact("cubic_coefficient_inverse_scale_mass_dimension",
          sp.Rational(3 * dimK, 4) - sp.Rational(dimA, 2), 1)
    regulator_scale = sp.sqrt(K / b)
    cubic_coefficient_scale = sp.sqrt(K ** sp.Rational(3, 2) / A)
    exact("B1_regulator_coefficient_scale", regulator_scale, sp.sqrt(sp.Rational(33, 5)))
    exact("B1_cubic_coefficient_scale_squared", cubic_coefficient_scale ** 2,
          sp.Rational(21, 2) * sp.sqrt(3))
    exact("B1_condensate_potential_Lambda", params["cutoff"], 2)

    p0 = sp.Integer(8) * 10 ** 13
    k_sufficient = sp.Integer(48) * 10 ** 14
    n_sufficient = sp.Integer(8) * 10 ** 14
    exact("full_interval_sufficient_k", k_sufficient, 60 * p0)
    true("axial_integer_mode_sufficient",
         2 * 3 * n_sufficient == k_sufficient and bool(sp.pi > 3),
         "k=2*pi*|n|; pi>3 makes |n|>=8e14 sufficient")
    true("formal_p0_exceeds_coefficient_scales",
         bool(p0 > regulator_scale and p0 > cubic_coefficient_scale),
         "magnitude comparison only; neither scale is a certified p_max")

    return {
        "checks": checks,
        "algebra": {
            "equality_surface": "alpha14+alpha13+3*alpha2=0",
            "B1_surface_offset": str(fixed_surface),
            "B1_Gcos_over_Gstatic": str(ratio),
            "bare_ci_mutant_ratio": str(bare_ratio),
            "monomial_cubic_exponent": "a-3*q/2",
            "registered_canonical_cubic": str(canonical_cubic),
            "regulator_coefficient_scale": str(regulator_scale),
            "cubic_coefficient_scale": str(cubic_coefficient_scale),
            "condensate_potential_Lambda": str(params["cutoff"]),
            "formal_p0": str(p0),
            "full_interval_sufficient_k": str(k_sufficient),
            "axial_integer_n_sufficient": str(n_sufficient),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt", default="01", choices=("01", "02", "03"))
    args = parser.parse_args()
    pinned_sources()
    result = run_checks()
    checks = result["checks"]
    passed = sum(item["passed"] for item in checks)
    record = {
        "candidate": "R4C1-v1",
        "control": "R4C1-PD1",
        "validation": "PASS" if passed == len(checks) else "FAIL",
        "passed": passed,
        "total": len(checks),
        **result,
        "source_sha256": PINS,
        "script_sha256": sha256(Path(__file__)),
        "status": "PHYSICAL_WINDOW_UNDETERMINED_FIXED_B1_GR_SHORTCUT_REJECTED",
        "scope": "exact necessary conditions; no physical cutoff, full IVP, alternative GR path, or parent closure",
        "physical_pmax_derived": False,
        "full_interval_physical_overlap_verified": False,
        "all_paths_GR_no_go": False,
        "healthy_continuous_GR_limit_verified": False,
        "canonical_Test1_pass": False,
        "physics_pass": False,
        "gate_effect": "NONE",
        "Rule9_cleared": False,
        "review_status": "DEFERRED",
        "MAT-001": "BLOCKED",
        "UVIR-003": "IN_PROGRESS",
        "K_Q": "NOT_DERIVED",
        "V": "NOT_COMPUTED",
        "Stage4A": "CLOSED",
    }
    out = ROOT / "Analysis/MasterTests/outputs" / f"r4c1_pd1_attempt_{args.attempt}" / "summary.json"
    payload = (json.dumps(record, sort_keys=True, indent=2) + "\n").encode("utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        if out.read_bytes() != payload:
            raise RuntimeError(f"EXISTING_RECEIPT_DIFFERS: {out}")
    else:
        with out.open("xb") as stream:
            stream.write(payload)
    sidecar = out.with_name(out.name + ".sha256")
    sidecar_text = f"{sha256(out)}  {out.name}\n"
    if sidecar.exists():
        if sidecar.read_text(encoding="ascii") != sidecar_text:
            raise RuntimeError(f"EXISTING_RECEIPT_SIDECAR_DIFFERS: {sidecar}")
    else:
        with sidecar.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(sidecar_text)
    print(json.dumps({"validation": record["validation"], "passed": passed,
                      "total": len(checks), "status": record["status"],
                      "physics_pass": False, "receipt_sha256": sha256(out)}))
    for item in checks:
        if not item["passed"]:
            print(json.dumps(item))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
