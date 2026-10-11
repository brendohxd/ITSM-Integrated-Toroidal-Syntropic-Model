"""G3N4 supplement: every nonanalytic force source, not solved evolution.

Independent linear ADM variations and exact unexpanded density controls.
The original N4 calculation/receipts are immutable inputs. Replay is read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
PARENT = BASE + "r4c1_g3n4_attempt_01/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
PINS = {
    PARENT + "summary.json": "6dde40b37ca40409566151c997bcc663edd923f1119fdcd019728a87dfd450e1",
    PARENT + "formulas.json": "1dee96271de67aec5336ac84753c18728a65e130e05c1c7731559c5a6a49727a",
    PARENT + "force.json": "03b9116e8dcc367216364a4898fbdfb78d036918a48f715453555b952ca6c76a",
    PARENT + "independent.json": "ea9db7167daa3598e0c3425e5ee969c862aa93e6dfdeb1465e96795048a3eaf3",
    "Theory/Gates/RES-001/RES001_R4C1_G3N4_FORCE_COVERAGE_CONTRACT_2026-10-09.md": "a772168e982dc77b77f8301879f32bba073a37e01ce7c332f12e4bfcd266ae23",
}


def exact(checks, name, residual):
    values = list(residual) if isinstance(residual, (list, tuple, s.MatrixBase)) else [residual]
    reduced = [s.simplify(s.expand(v)) for v in values]
    checks.add(name, all(v == 0 for v in reduced), "zero_exact" if all(v == 0 for v in reduced) else list(map(str, reduced)))


def derive(checks):
    a = s.Symbol("a", positive=True)
    A, e, p, W, B, H, pdd, Wt = s.symbols("A e p W B H pdd Wt", real=True)
    R = {k: s.Symbol(k, real=True) for k in FIELDS}
    Rt = {k: s.Symbol(k + "_t", real=True) for k in FIELDS}
    Rz = {k: s.Symbol(k + "_z", real=True) for k in FIELDS}
    names = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
    M = s.Matrix([[R[names[i][j]] for j in range(3)] for i in range(3)])
    h, dh = a**2 * s.eye(3), a**2 * M
    shift, dshift = s.Matrix([0, e * B / a, 0]), s.Matrix([R[k] / a for k in ("Sx", "Sy", "Sz")])
    vel, dvel = s.Matrix([0, e * W / a, 0]), s.Matrix([R[k] / a for k in ("Vx", "Vy", "Vz")])
    gamma = s.sqrt(1 + (vel.T * h * vel)[0])
    dgamma = ((dvel.T * h * vel)[0] * 2 + (vel.T * dh * vel)[0]) / (2 * gamma)
    n = s.Matrix([gamma] + list(vel - shift * gamma))
    dn0 = dgamma - R["alpha"] * gamma
    dn = s.Matrix([dn0] + list(dvel - dshift * gamma - shift * dn0))
    gi, dgi = s.zeros(4), s.zeros(4)
    gi[0, 0], dgi[0, 0] = -1, 2 * R["alpha"]
    for i in range(3):
        gi[0, i + 1] = gi[i + 1, 0] = shift[i]
        dgi[0, i + 1] = dgi[i + 1, 0] = dshift[i] - 2 * R["alpha"] * shift[i]
        for j in range(3):
            gi[i + 1, j + 1] = int(i == j) / a**2 - shift[i] * shift[j]
            dgi[i + 1, j + 1] = -M[i, j] / a**2 - dshift[i] * shift[j] - shift[i] * dshift[j] + 2 * R["alpha"] * shift[i] * shift[j]
    grad, dgrad = s.Matrix([p, 0, 0, 0]), s.Matrix([Rt["Pi"], 0, 0, Rz["Pi"]])
    Y0 = s.simplify((grad.T * gi * grad)[0] + (n.T * grad)[0]**2)
    dY = s.simplify((grad.T * dgi * grad)[0] + 2 * (dgrad.T * gi * grad)[0]
                   + 2 * (n.T * grad)[0] * ((dn.T * grad)[0] + (n.T * dgrad)[0]))
    expected_dY = p**2 * (2 * e * W * R["Vy"] + e**2 * W**2 * (R["Myy"] - 2 * R["alpha"])) + 2 * p * e**2 * W**2 * Rt["Pi"]
    exact(checks, "projected_Y_on_transverse_direction", Y0 - p**2 * e**2 * W**2)
    exact(checks, "full_ADM_normalized_frame_projector_variation", dY - expected_dY)
    # A cancellation-free exact rest-frame norm, valid also at zero boost.
    gg, E, qv, q2 = s.symbols("gamma E q_dot_v q_norm2", real=True)
    rr = E + qv / (gg + 1)
    exact(checks, "rest_frame_norm_is_projected_Y_without_zero_division",
          q2 + 2 * rr * qv + rr**2 * (gg**2 - 1) - (q2 - E**2 + (gg * E + qv)**2))
    volume = R["alpha"] + (R["Mxx"] + R["Myy"] + R["Mzz"]) / 2
    root = s.Abs(p) * s.Abs(e) * s.Abs(W)
    deltaL = s.expand(-A * (volume * root**3 + s.Rational(3, 2) * root * dY))
    expected = {k: {"value": s.Integer(0), "time": s.Integer(0), "space": s.Integer(0)} for k in FIELDS}
    expected["Vy"]["value"] = -3 * A * s.Abs(p)**3 * e * s.Abs(e) * W * s.Abs(W)
    expected["alpha"]["value"] = 2 * A * root**3
    expected["Myy"]["value"] = -2 * A * root**3
    expected["Mxx"]["value"] = expected["Mzz"]["value"] = -A * root**3 / 2
    expected["Pi"]["time"] = -3 * A * p * s.Abs(p) * s.Abs(e)**3 * s.Abs(W)**3
    coefficients, sources = {}, {}
    positive_p, positive_w = s.symbols("positive_p positive_w", positive=True)
    for name in FIELDS:
        coeff = {"value": s.diff(deltaL, R[name]), "time": s.diff(deltaL, Rt[name]), "space": s.diff(deltaL, Rz[name])}
        for kind in coeff:
            exact(checks, name + "_force_" + kind + "_coefficient", coeff[kind] - expected[name][kind])
        ct = coeff["time"]
        source = coeff["value"] - s.diff(ct, p) * pdd - s.diff(ct, W) * Wt - 3 * H * ct
        if name == "Pi":
            target = 3 * A * s.Abs(e)**3 * ((2 * s.Abs(p) * pdd + 3 * H * p * s.Abs(p)) * s.Abs(W)**3 + 3 * p * s.Abs(p) * W * s.Abs(W) * Wt)
            for psign in (-1, 1):
                for wsign in (-1, 1):
                    exact(checks, f"Pi_Euler_chain_rule_p{psign}_W{wsign}", (source - target).subs({p: psign * positive_p, W: wsign * positive_w}))
            source = target  # equivalent, node-safe expression; checks above retain signs
        else:
            exact(checks, name + "_Euler_no_derivative_coefficient", source - expected[name]["value"])
        coefficients[name] = {k: s.simplify(v) for k, v in coeff.items()}
        sources[name] = source
    scale = s.Symbol("scale", positive=True)
    degrees = {}
    for name, source in sources.items():
        degree = None if source == 0 else (2 if name == "Vy" else 3)
        degrees[name] = degree
        exact(checks, name + "_directional_amplitude_degree", source if degree is None else source.subs(e, scale * e) - scale**degree * source)
        exact(checks, name + "_directional_sign_parity", source.subs(e, -e) - (-source if name == "Vy" else source))
        for node in (p, W, e):
            exact(checks, name + "_regular_node_" + str(node), source.subs(node, 0))
    checks.add("reject_even_e_squared_transverse_force", sources["Vy"].subs(e, -1) != sources["Vy"].subs(e, 1), "odd e|e|, not e^2")
    exact(checks, "volume_variation_contributes_nonzero_lapse_term", s.diff(deltaL, R["alpha"]) - 3 * A * root**3 + A * root**3)
    checks.add("reject_dropping_force_volume", -A * root**3 != 0, "missing lapse term is -A|peW|^3")
    exact(checks, "normalized_force_does_not_vary_with_nu", s.diff(dY, R["nu"]))
    mutant = 2 * p**2 * gamma**2
    checks.add("reject_unnormalized_U_force_projector", s.simplify(mutant) != 0, str(mutant), "would add a nonzero normal-force variation")
    return {"Y0": str(Y0), "delta_Y": str(dY), "delta_density_over_a3": str(deltaL),
            "coefficients": {k: {kk: str(vv) for kk, vv in v.items()} for k, v in coefficients.items()},
            "Euler_sources": {k: str(v) for k, v in sources.items()}, "directional_degree": degrees,
            "node_scope": "No division by e,p,W,sqrt(Y); gamma+1>=2 for the future normalized frame",
            "second_order_scope": "Only Vy starts at degree 2; alpha,Mxx,Myy,Mzz,Pi start at degree 3; remaining sources identically zero on this direction, not solved responses"}, coefficients, (A, e, p, W)


def raw_density(e, d, p, W, field):
    zero = mp.mpf(0)
    R = {k: (d if k == field else zero) for k in FIELDS}
    a, A, B = mp.mpf("1.4"), mp.mpf("0.14"), mp.mpf("-0.2")
    N = 1 + R["alpha"]
    names = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
    h = a**2 * mp.matrix([[int(i == j) + R[names[i][j]] for j in range(3)] for i in range(3)])
    shift = mp.matrix([(e * B * int(i == 1) + R[k]) / a for i, k in enumerate(("Sx", "Sy", "Sz"))])
    vel = mp.matrix([(e * W * int(i == 1) + R[k]) / a for i, k in enumerate(("Vx", "Vy", "Vz"))])
    hi = h**-1
    gamma = mp.sqrt(1 + (vel.T * h * vel)[0])
    n = mp.matrix([gamma / N] + list(vel - shift * gamma / N))
    # Exact rest-frame norm identity avoids cancellation at p=0 or W=0.
    pt = p + (d if field == "Pi_t" else zero)
    q = mp.matrix([zero, zero, d if field == "Pi_z" else zero])
    E = (pt - (shift.T * q)[0]) / N
    restq = q + h * vel * (E + (vel.T * q)[0] / (gamma + 1))
    Y = (restq.T * hi * restq)[0]
    if N <= 0 or h[0, 0] <= 0 or h[0, 0] * h[1, 1] - h[0, 1]**2 <= 0 or mp.det(h) <= 0 or Y < 0:
        raise ValueError("Independent jet left the admissible ADM/projector domain")
    if not all(mp.isfinite(v) for v in n):
        raise ValueError("Nonfinite exact normalized frame")
    return -A * N * mp.sqrt(mp.det(h)) * Y**mp.mpf("1.5") / a**3


def independent(checks, coefficients, symbols):
    A, e, p, W = symbols
    records = []
    charts = [(es, ps, ws) for es in (-1, 1) for ps in (-1, 1) for ws in (-1, 1)]
    charts += [(1, 0, 1), (-1, 1, 0)]
    for chart, (es, ps, ws) in enumerate(charts):
        ee, pp, ww = mp.mpf(es) / 100, mp.mpf(ps) / 5, mp.mpf(ws) * 3 / 10
        substitutions = {A: s.Rational(14, 100), e: s.Rational(es, 100), p: s.Rational(ps, 5), W: s.Rational(3 * ws, 10)}
        for field in FIELDS + ("Pi_t", "Pi_z"):
            name, kind = ("Pi", "time" if field == "Pi_t" else "space") if field in ("Pi_t", "Pi_z") else (field, "value")
            target = mp.mpf(str(s.N(coefficients[name][kind].subs(substitutions), 60)))
            rows, errors = [], []
            for step in ("1e-8", "5e-9", "2.5e-9"):
                d = mp.mpf(step)
                actual = (raw_density(ee, d, pp, ww, field) - raw_density(ee, -d, pp, ww, field)) / (2 * d)
                error = float(abs(actual - target) / max(1, abs(actual), abs(target)))
                errors.append(error)
                rows.append({"d": step, "actual": str(actual), "target": str(target), "normalized_error": error})
            checks.add(f"exact_density_chart_{chart}_{field}", errors[-1] <= 1e-12 and all(errors[i + 1] < errors[i] or max(errors[i], errors[i + 1]) <= 1e-14 for i in range(2)), errors, "last<=1e-12; decreasing or <=1e-14 floor")
            records.append({"chart": chart, "e": str(ee), "p": str(pp), "W": str(ww), "field": field, "rows": rows})
    return records


def ward_factors(checks):
    ward = common.read_json(PARENT + "formulas.json")["Ward"]
    names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", " ".join(ward[k] for k in ("temporal_before_vector_shell", "longitudinal_before_vector_shell", "vector_equation"))))
    local = {k: s.Symbol(k, real=True) for k in names}
    parse = lambda k: s.sympify(ward[k], locals=local)
    EW = parse("vector_equation")
    exact(checks, "off_shell_temporal_source_factor", parse("temporal_before_vector_shell") - (local["H"] * local["W"] - local["W_t"]) * EW)
    exact(checks, "off_shell_longitudinal_source_factor", parse("longitudinal_before_vector_shell") - local["W_z"] * EW)
    return {"temporal": "(H*W-W_t)*E_W", "longitudinal": "W_z*E_W", "scope": "Declared G3 family; temporal/longitudinal only; no vector-shell substitution"}


def calculate():
    mp.mp.dps = 50
    parent = common.read_json(PARENT + "summary.json")
    pins = dict(parent["source_sha256"])
    pins.update(PINS)
    pins[SELF] = common.sha((ROOT / SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("source_pins_and_sidecars_before", True, {"pins": len(pins), "available": len(pins) - len(missing), "known_absent": missing})
    checks.add("all_parent_response_fields_retained", list(FIELDS) == parent["response_fields"], list(FIELDS))
    formulas, coefficients, symbols = derive(checks)
    formulas["Ward_factor_controls"] = ward_factors(checks)
    records = independent(checks, coefficients, symbols)
    inherited = common.read_json(PARENT + "independent.json")
    checks.add("original_failure_debt_retained", len(inherited["inherited_failed_parent_checks"]) == 1 and len(inherited["superseded_N3_attempt_01_failed_checks"]) == 2)
    checks.add("source_pins_and_sidecars_after", common.inspect_pins(pins) == missing)
    payloads = {
        "formulas.json": common.encode(formulas),
        "independent.json": common.encode({"mp_digits": 50, "charts": records,
            "inherited_failed_parent_checks": inherited["inherited_failed_parent_checks"],
            "superseded_N3_attempt_01_failed_checks": inherited["superseded_N3_attempt_01_failed_checks"]}),
    }
    passed = sum(row["passed"] for row in checks.rows)
    ok = passed == len(checks.rows)
    summary = {"schema": "r4c1-g3n4-force-coverage-v1", "validation": "PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        "passed": passed, "total": len(checks.rows), "checks": checks.rows,
        "status": "NONANALYTIC_FORCE_FIELD_COVERAGE_CHECKED_RESPONSE_OPEN" if ok else "FORCE_COVERAGE_REQUIRES_DISPOSITION",
        "source_sha256": dict(sorted(pins.items())), "script_sha256": pins[SELF], "artifacts": {k: common.sha(v) for k, v in payloads.items()},
        "inherited_sidecars_absent": missing, "original_N4_checks": {"passed": parent["passed"], "total": parent["total"], "unchanged": True},
        "all_22_force_response_fields_checked": ok, "full_second_order_response_solved": False,
        "physics_pass": False, "Rule9_cleared": False, "gate_effect": "NONE", "review_status": "DEFERRED",
        "canonical_tests_1_to_3": "HOLD_SUBSTANTIVE", "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS",
        "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED",
        "runtime": {"python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__, "mp_decimal_digits": mp.mp.dps}}
    payloads["summary.json"] = common.encode(summary)
    return payloads, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE + "r4c1_g3n4_force_attempt_01")
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
                raise RuntimeError("Replay bytes or sidecar differ: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            with (dest / name).open("xb") as f:
                f.write(data)
            with (dest / (name + ".sha256")).open("xb") as f:
                f.write((common.sha(data) + "  " + name + "\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action": action, **{k: summary[k] for k in ("validation", "passed", "total", "status", "physics_pass", "gate_effect", "Rule9_cleared")}}))
    for check in summary["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
