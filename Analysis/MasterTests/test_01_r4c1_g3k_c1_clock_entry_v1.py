"""G3K-C1 v1: global REAL U-clock obstruction and comparator map entry.

Conditional entry diagnostic, not a coupled Cauchy/ghost/cutoff certificate.
No parent file is changed. Normal execution refuses an existing output path;
--replay recomputes and byte-compares receipts without writing anything.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import i0
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
BASE = "Analysis/MasterTests/outputs/"
DEFAULT_OUT = BASE + "r4c1_g3k_c1_attempt_01"
TOL = 1e-10
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_G3K_C1_CLOCK_ENTRY_CONTRACT_2026-10-09.md":
        "00ad4d640181736a2e8049568df181b2d3a64f58de61f0aa836d989f708713b1",
    "Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_SCALAR_REPORT_2026-10-08.md":
        "81c11fc9cc9efbb9ad6b2d6f0e2bd26653a13d2fb126031b4941ae326f782c31",
    "Theory/Gates/RES-001/RES001_R4C1_G3_TILTED_BACKGROUND_REPORT_2026-10-08.md":
        "f3ad690310aa762aff87f37fba961f5be9280b4c1844a9d608c2b90b5e037105",
    BASE + "r4c1_g3k_attempt_02/summary.json":
        "131e175a3d1a6979a7c3a68a6f5d84a21b533ce01a7850066fcfde5800d2d6ab",
    BASE + "r4c1_g3k_attempt_02/samples.json":
        "69102fff332222f34684151e08a218fd92c6ae7a5153fd49d5900cf9e4b430d5",
    BASE + "r4c1_g3t_attempt_02/initial_data.json":
        "c1b80b7c8cd1fd74e07fe797214a56f6c14f32f0416bb3966f6371cf4a85d243",
    BASE + "r4c1_g3t_attempt_02/trajectories.npy":
        "470bdd1212e45fb3334e549003a6d6233f26f396043924c2ccb9b20bf13c18cd",
    BASE + "r4c1_g3_attempt_01/summary.json":
        "930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75",
}
EXPECTED_MISSING_SIDECARS = {
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONZERO_GRADIENT_FORCE_LOCAL.md",
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md",
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def encode(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def discrepancy(a, b) -> float:
    return float(abs(a - b) / max(1.0, abs(a), abs(b)))


class Checks:
    def __init__(self):
        self.rows = []
        self.names = set()

    def add(self, name, passed, value=None, criterion="exact"):
        if name in self.names:
            raise ValueError("Duplicate assertion: " + name)
        self.names.add(name)
        self.rows.append({"name": name, "passed": bool(passed), "value": value,
                          "criterion": criterion})

    def small(self, name, value):
        self.add(name, math.isfinite(value) and value <= TOL, value, "<=1e-10")


def inspect_pins(pins):
    missing_sidecars = []
    for name, expected in sorted(pins.items()):
        path = ROOT / name
        if not path.is_file() or sha(path.read_bytes()) != expected:
            raise ValueError("Source missing or SHA mismatch: " + name)
        sidecar = Path(str(path) + ".sha256")
        if sidecar.exists():
            if sidecar.read_text(encoding="utf-8").split()[0].lower() != expected:
                raise ValueError("Source sidecar mismatch: " + name)
        else:
            missing_sidecars.append(name)
    if set(missing_sidecars) != EXPECTED_MISSING_SIDECARS:
        raise ValueError("Inherited sidecar availability changed: " + repr(missing_sidecars))
    return missing_sidecars


def symbolic_checks(checks):
    t, x, y, z = sp.symbols("t x y z", real=True)
    L = sp.Symbol("L_x", positive=True)
    N, a, q, w = (sp.Function(s)(t) for s in ("N", "a_parallel", "a_perp", "w"))
    gamma = sp.sqrt(1 + w**2)
    metric = sp.diag(-N**2, a**2, q**2, q**2)
    U = sp.Matrix([gamma / N, w / a, 0, 0])
    theta = metric * U
    checks.add("exact_unit_frame", sp.simplify((U.T * metric * U)[0] + 1) == 0)
    coords = [t, x, y, z]
    dtheta = {(i, j): sp.diff(theta[j], coords[i]) - sp.diff(theta[i], coords[j])
              for i in range(4) for j in range(4)}
    three_form = {str((i, j, k)): sp.simplify(theta[i] * dtheta[j, k]
                 - theta[j] * dtheta[i, k] + theta[k] * dtheta[i, j])
                  for i, j, k in itertools.combinations(range(4), 3)}
    checks.add("exact_Frobenius_local_only", all(v == 0 for v in three_form.values()))
    potentials = {}
    for sign in (1, -1):
        mu = sign / (a * w)  # positive on the respective sign(w)=sign patch
        potential = sign * (sp.Integral(N * gamma / (a * w), t) - x)
        gradient = sp.Matrix([sp.diff(potential, c) for c in coords])
        checks.add(f"exact_local_gradient_sign_{sign}",
                   all(sp.simplify(v) == 0 for v in gradient + mu * theta))
        checks.add(f"exact_timelike_local_gradient_sign_{sign}",
                   sp.simplify((gradient.T * metric.inv() * gradient)[0]
                               + 1 / (a**2 * w**2)) == 0)
        checks.add(f"exact_future_orientation_sign_{sign}",
                   sp.simplify((U.T * gradient)[0] - mu) == 0)
        change = sp.simplify(potential.subs(x, x + L) - potential)
        checks.add(f"exact_quotient_holonomy_sign_{sign}", change == -sign * L)
        potentials[str(sign)] = {"potential": str(potential), "mu": str(mu),
                                "cycle_change": str(change)}
    ap, wp, M = sp.symbols("a_positive abs_w positive_mu_integral", positive=True)
    checks.add("arbitrary_positive_mu_positive_tilt_period_negative", (-ap * wp * M).is_negative)
    checks.add("arbitrary_positive_mu_negative_tilt_period_positive", (ap * wp * M).is_positive)
    aligned = sp.Integral(N, t)
    checks.add("aligned_global_clock_control", sp.diff(aligned, t) == N
               and sp.diff(aligned, x) == 0)

    C, d, P = sp.symbols("C d P", positive=True)
    v2 = sp.Symbol("v_squared", positive=True)
    xi = sp.Symbol("xi", nonnegative=True)
    vg = sp.diff(P * sp.sqrt(C + d * P**2), P)
    expected_vg = (C + 2 * d * P**2) / sp.sqrt(C + d * P**2)
    checks.add("exact_comparator_group_velocity", sp.simplify(vg - expected_vg) == 0)
    checks.add("exact_positive_group_velocity_derivative", sp.simplify(sp.diff(vg, P)
               - d * P * (3 * C + 2 * d * P**2) / (C + d * P**2)**sp.Rational(3, 2)) == 0)
    wb = sp.Symbol("w_boost", real=True)
    gb = sp.sqrt(1 + wb**2)
    checks.add("exact_inverse_clock_map_determinant", sp.simplify(gb**2 - wb**2) == 1)
    for sign in (1, -1):
        omega_branch = sign * P * sp.sqrt(C + d * P**2)
        checks.add(f"exact_clock_map_slope_sign_{sign}",
                   sp.simplify(sp.diff(gb * P + wb * omega_branch, P)
                               - gb - sign * wb * expected_vg) == 0)
    polynomial = v2 * (C + 2 * xi)**2 - (C + xi)
    positive_root = (1 - 4 * v2 * C + sp.sqrt(1 + 8 * v2 * C)) / (8 * v2)
    negative_root = (1 - 4 * v2 * C - sp.sqrt(1 + 8 * v2 * C)) / (8 * v2)
    checks.add("exact_turning_root_plus", sp.simplify(polynomial.subs(xi, positive_root)) == 0)
    checks.add("exact_turning_root_minus", sp.simplify(polynomial.subs(xi, negative_root)) == 0)
    checks.add("exact_C_zero_boundary", sp.simplify(positive_root.subs(C, 0)
                                                     - 1 / (4 * v2)) == 0)
    checks.add("root_sign_condition_identity", sp.expand((1 + 8 * v2 * C)
               - (1 - 4 * v2 * C)**2 - 16 * v2 * C * (1 - v2 * C)) == 0)
    # Direct controls avoid dividing by v or d at their zero boundaries.
    controls = [
        (0.0, 1.0, 0.0, "unbounded_comparator"),
        (0.25, 0.0, 0.0, "unbounded_comparator"),
        (0.25, 0.0, 0.25, "unbounded_comparator"),
        (16.0, 0.0, 0.25, "orientation_degenerate_at_origin"),
        (20.0, 1.0, 0.25, "orientation_fails_at_origin"),
        (16.0, 1.0, 0.25, "orientation_degenerate_at_origin"),
    ]
    control_rows = []
    for i, (cc, dd, vv, expected) in enumerate(controls):
        result = comparator_domain(cc, dd, vv)["status"]
        checks.add(f"separate_zero_or_threshold_control_{i}", result == expected, result, expected)
        control_rows.append({"C": cc, "d": dd, "v": vv, "status": result})
    return {
        "geometry_assumptions": "N,a_parallel,a_perp>0; homogeneous B=0; fixed-sign nonzero w on the stated patch; I x T3",
        "U_flat": [str(vv) for vv in theta],
        "Frobenius_three_form": {k: str(vv) for k, vv in three_form.items()},
        "local_clock_patches": potentials,
        "positive_period_proof": [
            "A single-valued C1 REAL T has integral(dT)=0 on every closed x-cycle.",
            "If dT=-mu U_flat with continuous mu>0, this integral is -a_parallel(t)*w(t)*integral_0^Lx(mu dx).",
            "On the compact cycle continuity and strict positivity give min(mu)>0, so the integral of mu is >=Lx*min(mu)>0.",
            "For a_parallel>0, Lx>0 and nonzero homogeneous w this contradicts exactness, irrespective of spatial dependence of mu.",
            "This rejects a global REAL U-orthogonal clock, not local integrability or a non-orthogonal global clock.",
        ],
        "local_timelike_norm": "-1/(a_parallel^2*w^2)",
        "local_future_derivative": "U(T)=mu>0",
        "comparator": {
            "Omega": "+/-sqrt(C*P^2+d*P^4)",
            "omega": "gamma*Omega+w*P", "p": "gamma*P+w*Omega",
            "dp_dP_P_positive": "gamma +/- w*(C+2*d*P^2)/sqrt(C+d*P^2)",
            "paired_orientation_criterion": "abs(v)*v_g(abs(P))<1; v=w/gamma",
            "turning_variable": "xi=d*P^2", "turning_polynomial": str(polynomial),
            "xi_plus": str(positive_root), "xi_minus": str(negative_root),
            "band": "abs(P)<sqrt(xi_plus/d), only for d>0, abs(v)>0, v^2*C<1",
            "root_sign_argument": "F(0)=C*(v^2*C-1)<0 for C>0 and v^2*C<1; the quadratic leading coefficient is positive, so one root is negative and one positive. C=0 is a separately treated control.",
            "restriction": "Fixed-frame comparator map orientation only; neither a coupled physical domain nor an EFT cutoff.",
        },
        "separate_controls": control_rows,
    }


def comparator_domain(C, d, v):
    if C < 0 or d < 0 or not abs(v) < 1:
        raise ValueError("Outside comparator assumptions")
    u = v * v * C
    if u >= 1:
        return {"status": "orientation_degenerate_at_origin" if u == 1
                else "orientation_fails_at_origin", "P_turn": None}
    if v == 0 or d == 0:
        return {"status": "unbounded_comparator", "P_turn": None}
    xi = (1 - 4 * u + math.sqrt(1 + 8 * u)) / (8 * v * v)
    return {"status": "bounded_comparator", "P_turn": math.sqrt(xi / d), "xi": xi}


def independent_turns(C, v):
    def f(xx):
        return v * v * (C + 2 * xx)**2 - (C + xx)
    upper = 1.0
    if not f(0) < 0:
        raise ValueError("This registered finite-C root is not bracketable from zero")
    doublings = 0
    while f(upper) <= 0:
        upper *= 2
        doublings += 1
        if doublings > 1024:
            raise ValueError("Turning root bracket not found")
    brent = brentq(f, 0, upper, xtol=2e-14, rtol=4 * np.finfo(float).eps)
    cc, vv = mp.mpf(str(C)), mp.mpf(str(v))
    def mf(xx):
        return vv * vv * (cc + 2 * xx)**2 - (cc + xx)
    low, high = mp.mpf(0), mp.mpf(1)
    mp_doublings = 0
    if not mf(low) < 0:
        raise ValueError("High-precision finite-C root is not bracketable from zero")
    while mf(high) <= 0:
        high *= 2
        mp_doublings += 1
    for _ in range(200):
        middle = (low + high) / 2
        if middle == low or middle == high:
            break
        if mf(middle) > 0:
            high = middle
        else:
            low = middle
    bisect = (low + high) / 2
    return brent, bisect, doublings, mp_doublings


def calculate():
    mp.mp.dps = 50
    checks = Checks()
    # Verify the frozen summary before treating its dependency map as data.
    for name, expected in PINS.items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise ValueError("Frozen input mismatch: " + name)
    parent = read_json(BASE + "r4c1_g3k_attempt_02/summary.json")
    pins = dict(PINS)
    for mapping in (parent["source_sha256"], parent["transitive_source_sha256"]):
        for name, expected in mapping.items():
            if name in pins and pins[name] != expected:
                raise ValueError("Conflicting source identity: " + name)
            pins[name] = expected
    for name, expected in parent["artifacts"].items():
        pins[BASE + "r4c1_g3k_attempt_02/" + name] = expected
    script_hash = sha((ROOT / SELF).read_bytes())
    pins[SELF] = script_hash
    missing = inspect_pins(pins)
    checks.add("all_input_pins_and_available_sidecars_before", True,
               {"pins": len(pins), "sidecars": len(pins) - len(missing),
                "known_absent_sidecars": missing}, "exact recorded SHA256; absence explicitly retained")
    formulas = symbolic_checks(checks)
    initial = read_json(BASE + "r4c1_g3t_attempt_02/initial_data.json")
    original = read_json(BASE + "r4c1_g3_attempt_01/summary.json")
    parent_samples = read_json(BASE + "r4c1_g3k_attempt_02/samples.json")
    trajectories = np.load(ROOT / (BASE + "r4c1_g3t_attempt_02/trajectories.npy"), allow_pickle=False)
    checks.add("archived_trajectory_shape", trajectories.shape == (8, 17, 51), list(trajectories.shape))
    params = {float(row["eta"]): row["parameters"] for row in original["family"]}
    events = [{"eta": row["eta"], "tilt": row["tilt"], "t": 0.0,
               "kind": "initial", "method": "initial", "state": row["state"], "Y_archived": row["Y"],
               "C0_turn_archived": row["healthy_control_P_turn"]} for row in initial["cases"]]
    for run, trajectory in zip(initial["runs"], trajectories, strict=True):
        for index, t_expected in ((25, 0.0005), (50, 0.001)):
            checks.small(f"saved_time_{run['eta']}_{run['tilt']}_{index}",
                         discrepancy(float(trajectory[0, index]), t_expected))
            events.append({"eta": run["eta"], "tilt": run["tilt"],
                           "t": float(trajectory[0, index]), "kind": "saved_jet", "method": run["method"],
                           "state": trajectory[1:, index].tolist()})
    keys = [(row["eta"], row["tilt"], row["t"], row["method"]) for row in events]
    coordinate_event_count = len({(row["eta"], row["tilt"], row["t"]) for row in events})
    checks.add("forty_distinct_registered_method_jets", len(events) == len(set(keys)) == 40,
               {"method_tagged_jets": len(events), "eta_tilt_time_coordinates": coordinate_event_count},
               "24 initial states plus 16 saved method-tagged jets; do not call paired solvers independent physical backgrounds")
    controls = {(r["eta"], r["tilt"]): r for r in parent_samples["healthy_controls"]}
    checks.add("all_initial_finite_C_controls_present", len(controls) == 24
               and set(controls) == {(r["eta"], r["tilt"]) for r in initial["cases"]})

    # These dimensionless mu profiles are common to all frozen spatial cycles;
    # integrate each once, then evaluate its weighted period on all 40 events.
    profiles = []
    for e in (0.0, 0.25, 1.0):
        numeric, error_bound = quad(lambda xx: math.exp(e * math.cos(2 * math.pi * xx)),
                                    0, 1, epsabs=1e-13, epsrel=1e-13)
        em = mp.mpf(str(e))
        high_precision = mp.quad(lambda xx: mp.exp(em * mp.cos(2 * mp.pi * xx)), [0, 1])
        analytic = mp.besseli(0, em)  # L_x=1, not a physical circumference
        checks.small(f"profile_bessel_libraries_{e}", discrepancy(float(i0(e)), float(analytic)))
        profiles.append({"e": e, "scipy_integral": numeric, "scipy_error_estimate": error_bound,
                         "mp_integral_50digits": str(high_precision),
                         "bessel_integral_50digits": str(analytic)})

    event_rows = []
    fractions = (0.0, 0.5, 0.9, 0.999, 1.001, 1.1, 2.0)
    for index, event in enumerate(events):
        par = params[float(event["eta"])]
        state = event["state"]
        a = math.exp(state[0] + 2 * state[1])
        N = math.exp(-par["beta"] * state[6])
        w, psi_dot = state[2], state[14]
        gamma, v = math.sqrt(1 + w * w), w / math.sqrt(1 + w * w)
        mu = 1 / (a * w)
        Y = (w * psi_dot / N)**2
        C, d = 6 * par["A"] * math.sqrt(Y) / par["K"], par["b"] / par["K"]
        label = f"event_{index}"
        checks.add(label + "_registered_patch", a > 0 and N > 0 and w > 0 and psi_dot > 0
                   and C > 0 and d > 0 and v * v * C < 1,
                   {"w": w, "Y": Y, "v_squared_C": v * v * C}, "registered positive-tilt finite-C comparator assumptions")
        U = np.array([gamma / N, w / a])
        theta = np.array([-N * gamma, a * w])
        gradient = np.array([N * gamma / (a * w), -1.0])
        inverse_metric = np.diag([-1 / N**2, 1 / a**2])
        geometry_errors = {
            "normalization": discrepancy(float(U @ theta), -1.0),
            "gradient": float(np.linalg.norm(gradient + mu * theta)
                              / max(1.0, np.linalg.norm(gradient), np.linalg.norm(mu * theta))),
            "timelike_norm": discrepancy(float(gradient @ inverse_metric @ gradient), -1 / (a * a * w * w)),
            "future_derivative": discrepancy(float(U @ gradient), mu),
        }
        checks.small(label + "_geometry_identities", max(geometry_errors.values()))
        checks.add(label + "_local_clock_orientation", mu > 0 and float(U @ gradient) > 0)
        periods = []
        for profile in profiles:
            e = profile["e"]
            analytic_period = -a * w * float(mp.mpf(profile["bessel_integral_50digits"]))
            scipy_period = -a * w * profile["scipy_integral"]
            mp_period = -a * w * float(mp.mpf(profile["mp_integral_50digits"]))
            errors = [discrepancy(scipy_period, analytic_period), discrepancy(mp_period, analytic_period)]
            checks.small(label + f"_positive_mu_period_{e}", max(errors))
            checks.add(label + f"_nonzero_negative_period_{e}", analytic_period < 0
                       and scipy_period < 0 and mp_period < 0, analytic_period, "<0; a,w,mu>0")
            periods.append({"e": e, "analytic_period": analytic_period,
                            "scipy_period": scipy_period, "mp_period": mp_period,
                            "normalized_errors": errors})
        domain = comparator_domain(C, d, v)
        brent, bisect, doubles, mp_doubles = independent_turns(C, v)
        xi, turn = domain["xi"], domain["P_turn"]
        root_error = max(discrepancy(xi, brent), discrepancy(xi, float(bisect)))
        residual = abs(v * v * (C + 2 * xi)**2 - (C + xi)) / max(1.0, C + xi)
        checks.small(label + "_independent_turning_roots", root_error)
        checks.small(label + "_turning_polynomial_residual", residual)
        map_rows = []
        for fraction in fractions:
            P = fraction * turn
            vg = (C + 2 * d * P * P) / math.sqrt(C + d * P * P)
            slopes = [gamma + w * vg, gamma - w * vg]
            inside = all(slope > 0 for slope in slopes)
            checks.add(label + f"_strict_paired_band_{fraction}", inside == (fraction < 1),
                       {"P": P, "dp_dP": slopes}, "both slopes>0 iff fraction<1")
            map_rows.append({"P_over_turn": fraction, "P": P,
                             "dp_dP": slopes, "paired_orientation_preserved": inside})
        C0_turn = 1 / (2 * abs(v) * math.sqrt(d))
        if event["kind"] == "initial":
            control = controls[(event["eta"], event["tilt"])]
            checks.small(label + "_inherited_Y", discrepancy(Y, event["Y_archived"]))
            checks.small(label + "_G3K_C", discrepancy(C, control["c_psi_squared"]))
            checks.small(label + "_G3K_finite_C_turn", discrepancy(turn, control["preferred_P_turn"]))
            checks.small(label + "_G3T_separate_C0_turn", discrepancy(C0_turn, event["C0_turn_archived"]))
        checks.small(label + "_C0_formula_control", discrepancy(C0_turn, comparator_domain(0, d, v)["P_turn"]))
        event_rows.append({**event, "N": N, "a_parallel": a, "w": w,
                           "gamma": gamma, "v": v, "Y": Y, "C": C, "d": d,
                           "geometry_errors": geometry_errors, "positive_mu_periods": periods,
                           "comparator_domain": domain, "C0_comparator_turn": C0_turn,
                           "independent_xi_brent": brent, "independent_xi_mp_50digits": str(bisect),
                           "bracket_doublings": [doubles, mp_doubles],
                           "normalized_root_error": root_error, "normalized_turning_residual": residual,
                           "strict_band_probes": map_rows})

    retained_events = parent_samples["events"]
    checks.add("all_parent_events_preserved", len(retained_events) == 120, len(retained_events))
    for i, row in enumerate(retained_events):
        checks.add(f"parent_event_{i}_all_roots_and_formal_covectors", len(row["roots"]) == 14
                   and len(row["proper_covector_Omega_P"]) == 14,
                   {"roots": len(row["roots"]), "formal_covectors": len(row["proper_covector_Omega_P"])},
                   "14 retained, no health selection")
    rejection_tests = {
        "local_Frobenius_is_global_exactness": False,
        "circle_valued_potential_is_REAL_Cauchy_time": False,
        "cover_boost_removes_T3_holonomy": False,
        "comparator_turn_is_coupled_EFT_cutoff": False,
        "formal_complex_covectors_are_real_particle_poles": False,
        "deleting_parent_complex_or_growing_roots": False,
        "inverting_shift_at_k_zero_or_w_squared_one_fifth": False,
    }
    # No new Schur inverse is evaluated. Its exact zero factors are retained.
    kk, ww = sp.symbols("k w", real=True)
    shift_factor = kk**2 * (1 - 5 * ww**2)
    checks.add("pre_Schur_k_zero_boundary_retained", shift_factor.subs(kk, 0) == 0)
    checks.add("pre_Schur_w_squared_one_fifth_boundary_retained",
               sp.simplify(shift_factor.subs(ww, sp.sqrt(sp.Rational(1, 5)))) == 0)
    formulas["pre_Schur_boundary_factor_only_not_continuation_solution"] = str(shift_factor)
    formulas["rejected_inferences"] = rejection_tests
    formulas["nonclaims"] = [
        "No full coupled characteristic, symmetrizer, energy-residue or Cauchy classification.",
        "No physical ghost, instability, all-action no-go or action-derived EFT cutoff.",
        "No extension to spatially varying/sign-changing frames; no physical torus-size selection.",
        "No new K_Q or V calculation; no healthy continuous GR-limit certificate.",
        "No full Test1, Test2, Test3, MAT, UVIR, Stage4A or TOP-X4 promotion.",
    ]
    parent_failed = [r for r in original["checks"] if not r["passed"]]
    checks.add("failed_original_parent_assertion_retained", len(parent_failed) == 1
               and parent_failed[0]["name"] == "eta1_independent_fd_balances"
               and not parent_failed[0]["passed"], parent_failed,
               "preserve failure; entry geometry does not repair the G3 GR/background balance")
    after_missing = inspect_pins(pins)
    checks.add("all_input_pins_and_available_sidecars_after", after_missing == missing)
    count = sum(row["passed"] for row in checks.rows)
    all_pass = count == len(checks.rows)
    samples = {"background_events": event_rows, "positive_mu_profile_integrals": profiles,
               "profile_integration_count": 3, "weighted_period_evaluations": 120,
               "parent_events_unchanged_no_mode_selection": retained_events,
               "inherited_parent_failed_assertions": parent_failed}
    payloads = {"formulas.json": encode(formulas), "samples.json": encode(samples)}
    summary = {
        "schema": "r4c1-g3k-c1-clock-entry-v1", "control": "R4C1-G3K-C1",
        "validation": "PASS_LOCAL_CHECKS" if all_pass else "FAIL_LOCAL_CHECKS",
        "passed": count, "total": len(checks.rows), "checks": checks.rows,
        "status": "GLOBAL_REAL_U_ORTHOGONAL_CLOCK_REJECTED_FOR_REGISTERED_TILTED_T3; COUPLED_TIME_DOMAIN_OPEN" if all_pass else "ENTRY_AUDIT_FAILED",
        "disposition_scope": "Global REAL U-orthogonal time rejected only for stated homogeneous nonzero fixed-sign tilted T3 backgrounds; local preferred patches and non-orthogonal global times not rejected.",
        "source_sha256": dict(sorted(pins.items())), "script_sha256": script_hash,
        "inherited_sidecars_absent": missing, "inherited_G3K_source_count": 75,
        "artifacts": {name: sha(data) for name, data in payloads.items()},
        "background_event_count": 40, "eta_tilt_time_coordinate_count": coordinate_event_count,
        "event_count_interpretation": "40 distinct method-tagged archived state records at 32 eta/initial-tilt/time coordinates; paired methods are not distinct physical backgrounds.",
        "parent_event_count": len(retained_events),
        "parent_root_count": sum(len(r["roots"]) for r in retained_events),
        "max_geometry_normalized_error": max(max(r["geometry_errors"].values()) for r in event_rows),
        "max_turning_root_normalized_error": max(r["normalized_root_error"] for r in event_rows),
        "max_turning_polynomial_normalized_residual": max(r["normalized_turning_residual"] for r in event_rows),
        "max_weighted_period_normalized_error": max(max(p["normalized_errors"]) for r in event_rows for p in r["positive_mu_periods"]),
        "comparator_turn_range": [min(r["comparator_domain"]["P_turn"] for r in event_rows),
                                  max(r["comparator_domain"]["P_turn"] for r in event_rows)],
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "sympy": sp.__version__,
                    "mpmath": mp.__version__, "mp_decimal_digits": mp.mp.dps},
        "review_status": "DEFERRED", "Rule9_cleared": False,
        "review_dependencies": ["R9-MT1-G3K", "all direct and transitive G3K scientific/review debt"],
        "canonical_Test1_pass": False, "canonical_Test2_pass": False, "canonical_Test3_pass": False,
        "physics_pass": False, "gate_effect": "NONE", "MAT-001": "BLOCKED",
        "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED",
        "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED",
        "coupled_physical_time_domain_verified": False,
        "physical_EFT_cutoff_derived": False, "all_paths_no_go": False,
        "healthy_continuous_GR_limit_verified": False,
    }
    payloads["summary.json"] = encode(summary)
    return payloads, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=DEFAULT_OUT)
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    args = parser.parse_args()
    destination = (ROOT / (args.replay or args.output)).resolve()
    destination.relative_to((ROOT / BASE).resolve())
    if args.replay:
        if not destination.is_dir():
            raise FileNotFoundError("Replay output is absent")
    elif destination.exists():
        raise FileExistsError("Refusing existing output: " + destination.name)
    payloads, summary = calculate()
    if args.replay:
        for name, data in payloads.items():
            path = destination / name
            if path.read_bytes() != data:
                raise ValueError("Replay byte mismatch: " + name)
            if Path(str(path) + ".sha256").read_text(encoding="utf-8") != sha(data) + "  " + name + "\n":
                raise ValueError("Replay sidecar mismatch: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        destination.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            path = destination / name
            with path.open("xb") as handle:
                handle.write(data)
            with Path(str(path) + ".sha256").open("xb") as handle:
                handle.write((sha(data) + "  " + name + "\n").encode("utf-8"))
        action = "NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action": action, **{k: summary[k] for k in
          ("validation", "passed", "total", "status", "physics_pass", "gate_effect", "Rule9_cleared")}}, sort_keys=True))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
