"""R4C1-G3: direct tensor variation and separately frozen equal-Newton family.

Imports only pure background functions; never calls earlier writing main().
New outputs are write-once. --replay recalculates without filesystem writes.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_BASE = ROOT / "Analysis/MasterTests/outputs"
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md":
        "b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md":
        "0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b",
    "Theory/Gates/RES-001/RES001_R4C1_GR_EQUALITY_SCALAR_KINETIC_OBSTRUCTION_2026-09-30.md":
        "a8966e9bff26f8514fb466f5f9be67acab6fb0340760148e1d3c642e3a14a3d1",
    "Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_CONTRACT_2026-09-30.md":
        "4bb989979850468d4322baeec9cbdaaaadd8318825724042711c062fc944e9f8",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Analysis/MasterTests/test_01_r4c1_full_variation.py":
        "aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0",
}
ETAS = (1., .25, .0625, .015625, .00390625, .0009765625)
METHODS = ("DOP853", "Radau")


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def verify_inputs(pins):
    for name, expected in pins.items():
        actual = digest_bytes((ROOT / name).read_bytes())
        if actual != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {name}")


class Audit:
    def __init__(self):
        self.checks = []

    def exact(self, name, expression):
        residual = s.simplify(expression)
        self.checks.append({"name": name, "passed": residual == 0,
                            "residual": str(residual), "expected": "zero_exact"})

    def numeric(self, name, passed, value, criterion):
        self.checks.append({"name": name, "passed": bool(passed),
                            "value": value, "criterion": criterion})


def christoffels(metric, derivatives):
    inverse = metric.inv()
    dim = metric.rows
    return [[[s.simplify(sum(inverse[c, d] * (
        derivatives[a][d, b] + derivatives[b][d, a] - derivatives[d][a, b])
        for d in range(dim)) / 2) for b in range(dim)]
        for a in range(dim)] for c in range(dim)]


def tensor_control(audit):
    ep = s.Symbol("epsilon", real=True)
    z = s.Symbol("z", real=True)
    q = s.Function("q")(z)
    qdot = s.Symbol("qdot", real=True)
    MP, M = s.symbols("MP2 M", positive=True)
    c1, c2, c3, c4 = s.symbols("c1 c2 c3 c4", real=True)
    gamma = s.Matrix([[1, ep*q, 0], [ep*q, 1, 0], [0, 0, 1]])
    inverse = gamma.inv()
    spatial_derivatives = [s.zeros(3), s.zeros(3), gamma.diff(z)]
    connection = christoffels(gamma, spatial_derivatives)
    # Direct Ricci contraction, with no spatial ADM identity substituted.
    ricci = s.zeros(3)
    for a in range(3):
        for b in range(3):
            ricci[a, b] = sum(
                (s.diff(connection[k][a][b], z) if k == 2 else 0)
                - (s.diff(connection[k][a][k], z) if b == 2 else 0)
                + sum(connection[k][a][b]*connection[l][k][l]
                      - connection[l][a][k]*connection[k][b][l]
                      for l in range(3)) for k in range(3))
    curvature = s.simplify(sum(inverse[a, b]*ricci[a, b]
                              for a in range(3) for b in range(3)))
    volume = s.sqrt(gamma.det())
    raw_spatial = s.expand(s.series(MP*volume*curvature/2, ep, 0, 3)
                          .removeO()).coeff(ep, 2)
    boundary = MP*s.diff(q*s.diff(q, z), z)
    audit.exact("tensor_spatial_curvature_with_boundary",
                raw_spatial-boundary+MP*s.diff(q, z)**2/4)

    # Direct four-dimensional covariant frame invariants at an arbitrary jet.
    metric = s.diag(-1, gamma)
    dt_metric = s.zeros(4)
    dt_metric[1, 2] = dt_metric[2, 1] = ep*qdot
    four_derivatives = [dt_metric, s.zeros(4), s.zeros(4), metric.diff(z)]
    four_connection = christoffels(metric, four_derivatives)
    # U^a=(1,0,0,0), so nabla_a U^b=Gamma^b_a0, exactly unit.
    frame_derivative = s.Matrix(4, 4, lambda a, b: four_connection[b][a][0])
    inv_four = metric.inv()
    I1 = s.trace(inv_four*frame_derivative*metric*frame_derivative.T)
    I2 = s.trace(frame_derivative)**2
    I3 = s.trace(frame_derivative*frame_derivative)
    acceleration = frame_derivative.row(0)
    I4 = (acceleration*metric*acceleration.T)[0]
    extrinsic = dt_metric[1:4, 1:4]/2
    mixed = inverse*extrinsic
    square, trace_square = s.trace(mixed*mixed), s.trace(mixed)**2
    audit.exact("covariant_c1_equals_extrinsic_square", I1-square)
    audit.exact("covariant_c2_equals_extrinsic_trace_square", I2-trace_square)
    audit.exact("covariant_c3_equals_extrinsic_square", I3-square)
    audit.exact("aligned_frame_acceleration_zero", I4)
    frame_density = -M*volume*(c1*I1+c2*I2+c3*I3-c4*I4)/2
    eh_density = MP*volume*(square-trace_square)/2
    temporal = s.expand(s.series(frame_density+eh_density, ep, 0, 3)
                        .removeO()).coeff(ep, 2)
    expected_temporal = (MP-M*(c1+c3))*qdot**2/4
    audit.exact("tensor_temporal_quadratic_action", temporal-expected_temporal)
    probe = {MP: 1, M: s.Rational(2, 3), c1: s.Rational(1, 5),
             c3: -s.Rational(1, 80), qdot: 1}
    audit.numeric("omitted_frame_tensor_term_rejected",
                  s.simplify((temporal-MP*qdot**2/4).subs(probe)) != 0,
                  str(s.simplify((temporal-MP*qdot**2/4).subs(probe))),
                  "nonzero exact residual")
    audit.numeric("reversed_frame_tensor_sign_rejected",
                  s.simplify((temporal-(MP+M*(c1+c3))*qdot**2/4).subs(probe)) != 0,
                  str(s.simplify((temporal-(MP+M*(c1+c3))*qdot**2/4).subs(probe))),
                  "nonzero exact residual")
    return {"raw_spatial_density": str(raw_spatial),
            "spatial_boundary": str(boundary),
            "reduced_quadratic_density": "[(MP2-MU2*c13)*qdot^2-MP2*qz^2]/4",
            "tensor_speed_squared": "1/(1-alpha13)",
            "scope": "one physical TT polarization on isotropic vacuum frame control"}


def exact_family(audit):
    eta = s.Symbol("eta", positive=True)
    M, c1, c2, c3, c4 = (2*eta/3, s.Rational(1, 5), -s.Rational(7, 48),
                          -s.Rational(1, 80), s.Rational(1, 20))
    a13, a14, a2, aL = M*(c1+c3), M*(c1+c4), M*c2, M*(c1+c2+c3)
    MC, MT = 1+M*(c1+3*c2+c3)/2, 1-M*(c1+c3)
    KV, GV = M*(c1+c4), M*c1+M**2*(c1+c3)**2/(2*MT)
    expressions = {
        "alpha13": (a13, eta/8), "alpha14": (a14, eta/6),
        "alpha2": (a2, -7*eta/72), "alphaL": (aL, eta/36),
        "Mc2": (MC, 1-eta/12), "Mt2": (MT, 1-eta/8),
        "G_cos_over_G_static": ((1-a14/2)/MC, 1),
        "K_vector": (KV, eta/6),
        "c_vector_squared": (GV/KV, s.Rational(4, 5)+3*eta/(8*(8-eta))),
        "c_tensor_squared": (1/MT, 8/(8-eta)),
        "S1_D_over_H_squared": (4*MC*MT/(M*(c1+c2+c3)),
                                 144*(1-eta/12)*(1-eta/8)/eta),
        "canonical_force_cubic": ((s.Rational(2, 7)*eta**s.Rational(3, 2)) /
                                   (3*eta)**s.Rational(3, 2), 2*s.sqrt(3)/63),
        "canonical_regulator": ((s.Rational(5, 11)*eta)/(3*eta), s.Rational(5, 33)),
        "canonical_matter": ((s.Rational(2, 5)*eta**2)/s.sqrt(3*eta),
                              2*s.sqrt(3)*eta**s.Rational(3, 2)/15),
    }
    for name, (derived, expected) in expressions.items():
        audit.exact(name, derived-expected)
    audit.exact("tensor_speed_approaches_one", s.limit(1/MT, eta, 0, dir="+")-1)
    audit.exact("vector_kinetic_vanishes", s.limit(KV, eta, 0, dir="+"))
    audit.exact("force_kinetic_vanishes", s.limit(3*eta, eta, 0, dir="+"))
    audit.exact("tensor_cone_excess", 1/MT-1-eta/(8-eta))
    audit.exact("bare_ci_normalization_mutant", (c1+c3)-s.Rational(3, 16))
    audit.numeric("bare_ci_as_alpha_mutant_rejected", c1+c3 != a13.subs(eta, 1),
                  {"bare_c13": str(c1+c3), "alpha13_at_eta1": str(a13.subs(eta, 1))},
                  "bare c13 differs from dimensionless alpha13")
    # A general necessary-condition identity, distinct from this chosen path.
    x, y = s.symbols("alpha13 alpha14", real=True)
    aL_equal = (2*x-y)/3
    audit.exact("general_equal_Newton_scalar_relation", aL_equal-(x-(x+y)/3))
    return {name: str(s.factor(derived)) for name, (derived, _) in expressions.items()}


def family_background(audit, bg):
    grid = np.linspace(0., 4., 801)
    hg = np.sqrt(.2/3)
    ag = (1+1.5*hg*grid)**(2/3)
    control = np.array([ag, hg/(1+1.5*hg*grid), .2/ag**3])
    trajectory = np.empty((len(ETAS), len(METHODS), len(bg.NAMES)+1, len(grid)))
    rows = []
    for ie, eta in enumerate(ETAS):
        p = {**bg.PARAMS, "c2": -7/48, "c3": -1/80}
        for key in ("MU2", "zeta", "K", "b", "gr"):
            p[key] *= eta
        p["A"] *= eta**1.5
        p["beta"] *= eta**2
        initial = bg.initial(p)
        for index in (2, 5, 6, 7):
            initial[index] *= np.sqrt(eta)
        initial[9] *= eta
        initial[1] = np.sqrt(bg.physics(initial, p)["energy"]/(3*bg.effective_mass(p)))
        summaries, solutions = {}, {}
        for im, method in enumerate(METHODS):
            sol = solve_ivp(lambda t, y: bg.rhs(t, y, p), (0., 4.), initial,
                            method=method, rtol=1e-11, atol=1e-13, dense_output=True)
            solutions[method] = sol
            summary = bg.summarize_solution(sol, p)
            summaries[method] = summary
            values = sol.sol(grid)
            trajectory[ie, im, 0] = grid
            trajectory[ie, im, 1:] = values
            label = f"eta_{eta}_{method}"
            audit.numeric(label+"_completed", summary["success"], summary["message"], "t=4 reached")
            audit.numeric(label+"_sampled_domain", summary["all_finite"] and
                          min(summary[k] for k in ("min_a", "min_H", "min_rho_m")) > 0,
                          {k: summary[k] for k in ("min_a", "min_H", "min_rho_m")},
                          "finite fields; a,H,rho_m>0")
            for key in ("max_normalized_Friedmann", "max_charge_drift", "max_dust_integral_drift"):
                audit.numeric(label+"_"+key, summary[key] < 1e-8, summary[key], "<1e-8")
        values = trajectory[ie, 0, 1:]
        other = trajectory[ie, 1, 1:]
        disagreement = float(np.max(np.abs(values-other)/(1+np.abs(values))))
        audit.numeric(f"eta_{eta}_two_method_agreement", disagreement < 1e-8, disagreement, "<1e-8")
        MC = bg.effective_mass(p)
        MT = p["MP2"]-p["MU2"]*(p["c1"]+p["c3"])
        KV = p["MU2"]*(p["c1"]+p["c4"])
        cL = p["c1"]+p["c2"]+p["c3"]
        D = 4*values[1]**2*MC*MT/(p["MU2"]*cL)
        cV = (p["MU2"]*p["c1"]+p["MU2"]**2*(p["c1"]+p["c3"])**2/(2*MT))/KV
        certificate = {"K_force": p["K"], "K_vector": KV,
                       "min_D": float(D.min()), "max_D": float(D.max()),
                       "Mc2": MC, "Mt2": MT, "MU2_cL": p["MU2"]*cL,
                       "c_tensor_squared": p["MP2"]/MT, "c_vector_squared": cV}
        audit.numeric(f"eta_{eta}_inherited_kinetic_weights_positive",
                      min(certificate[k] for k in ("K_force", "K_vector", "min_D", "Mc2", "Mt2", "MU2_cL")) > 0,
                      certificate, "positive inherited S1/G1 weights on regular nonzero-mode chart")
        charge_initial = summaries["DOP853"]["initial_state"]["a"]**3 * (
            initial[2]*initial[5]-initial[4]*initial[3])
        audit.numeric(f"eta_{eta}_initial_charge", abs(charge_initial-eta) < 1e-14,
                      charge_initial, "equals eta within 1e-14; not fixed charge")
        error = float(np.max(np.abs(values[[0, 1, 10]]-control)/(1+np.abs(control))))
        row = {"eta": eta, "parameters": p, "runs": summaries,
               "two_method_disagreement": disagreement,
               "normalized_metric_dust_error": error, "inherited_kinetic_certificate": certificate}
        if eta == 1:
            fd = [bg.finite_difference_balances(solutions["DOP853"], p, n) for n in (201, 401, 801)]
            row["finite_difference_balances"] = fd
            audit.numeric("eta1_independent_fd_balances", fd[-1]["maximum"] < 1e-7,
                          fd[-1]["maximum"], "<1e-7")
            audit.numeric("eta1_independent_fd_spatial_metric", fd[-1]["full_spatial_metric_fd_residual"] < 1e-7,
                          fd[-1]["full_spatial_metric_fd_residual"], "<1e-7")
            improvement = fd[0]["maximum"]/max(fd[-1]["maximum"], np.finfo(float).tiny)
            audit.numeric("eta1_fd_balance_refinement", improvement >= 4 or
                          max(fd[0]["maximum"], fd[-1]["maximum"]) < 1e-9,
                          improvement, ">=4 or endpoint residuals both<1e-9")
        rows.append(row)
    errors = [r["normalized_metric_dust_error"] for r in rows]
    audit.numeric("background_errors_decrease", all(b < a for a, b in zip(errors, errors[1:])), errors,
                  "strict decrease across frozen factor-four eta steps")
    ratio = errors[-2]/errors[-1]
    audit.numeric("background_last_refinement", 2 < ratio < 6, ratio, "2<ratio<6")
    return rows, trajectory


def evaluate():
    verify_inputs(PINS)
    import test_01_r4c1_interacting_background as bg
    import test_01_r4c1_full_variation as variation
    verify_inputs(bg.PINS)
    verify_inputs(variation.PINS)
    audit = Audit()
    altered = {**PINS, next(iter(PINS)): "0"*64}
    rejected = False
    try:
        verify_inputs(altered)
    except RuntimeError as exc:
        rejected = "FROZEN_INPUT_HASH_MISMATCH" in str(exc)
    audit.numeric("source_pin_mutation_rejected", rejected, rejected, "reject before output creation")
    tensor = tensor_control(audit)
    formulas = exact_family(audit)
    rows, trajectory = family_background(audit, bg)
    buffer = io.BytesIO()
    np.save(buffer, trajectory, allow_pickle=False)
    payload = buffer.getvalue()
    passed = sum(bool(check["passed"]) for check in audit.checks)
    return {
        "schema": "r4c1-g3-equal-newton-family-v1", "candidate": "R4C1-v1", "control": "R4C1-G3",
        "validation": "PASS_LOCAL_CHECKS" if passed == len(audit.checks) else "FAIL_LOCAL_CHECKS",
        "passed": passed, "total": len(audit.checks), "checks": audit.checks,
        "tensor_control": tensor, "exact_family": formulas, "family": rows,
        "source_sha256": PINS, "transitive_source_sha256": {**bg.PINS, **variation.PINS},
        "script_sha256": digest_bytes(Path(__file__).read_bytes()),
        "trajectory": {"file": "trajectories.npy", "sha256": digest_bytes(payload),
                       "shape": list(trajectory.shape), "axes": ["eta", "method", "field", "sample"],
                       "etas": list(ETAS), "methods": list(METHODS), "fields": ["t", *bg.NAMES]},
        "runtime": {"python": platform.python_version(), "numpy": np.__version__,
                    "scipy": scipy.__version__, "sympy": s.__version__},
        "status": "CONDITIONAL_EQUAL_NEWTON_BACKGROUND_GR_LIMIT_OPEN",
        "scope": "vacuum tensor control and finite-time alternate homogeneous family; inherited scalar kinetic identity",
        "healthy_continuous_GR_limit_verified": False, "full_interacting_Hessian_verified": False,
        "physical_EFT_cutoff_derived": False, "all_paths_no_go": False,
        "canonical_Test1_pass": False, "canonical_Test2_pass": False, "canonical_Test3_pass": False,
        "physics_pass": False, "gate_effect": "NONE", "review_status": "DEFERRED", "Rule9_cleared": False,
        "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED",
        "V": "NOT_COMPUTED", "Stage4A": "CLOSED",
    }, payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="Analysis/MasterTests/outputs/r4c1_g3_attempt_01")
    parser.add_argument("--replay", action="store_true", help="pure recomputation, no output writes")
    args = parser.parse_args()
    directory = (ROOT / args.output_dir).resolve()
    if not directory.is_relative_to(OUTPUT_BASE.resolve()):
        raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify_inputs(PINS)
    if not args.replay and directory.exists():
        raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record, payload = evaluate()
    encoded = (json.dumps(record, indent=2, allow_nan=False)+"\n").encode("utf-8")
    if args.replay:
        previous = directory / "summary.json"
        same = previous.exists() and previous.read_bytes() == encoded
        print(json.dumps({"replay": True, "prior_receipt_present": previous.exists(),
                          "byte_identical": same,
                          "summary_sha256": digest_bytes(encoded)}))
    else:
        directory.mkdir(parents=True, exist_ok=False)
        for name, data in (("trajectories.npy", payload), ("summary.json", encoded)):
            (directory / name).write_bytes(data)
            (directory / (name+".sha256")).write_text(f"{digest_bytes(data)}  {name}\n", encoding="ascii")
    print(json.dumps({k: record[k] for k in ("validation", "passed", "total", "status", "physics_pass")}))
    for check in record["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    if args.replay and previous.exists() and not same:
        return 2
    return 0 if record["passed"] == record["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
