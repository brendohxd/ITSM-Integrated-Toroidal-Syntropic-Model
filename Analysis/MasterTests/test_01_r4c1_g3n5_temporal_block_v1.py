"""Independent full-field temporal block; not a physical Hessian or evolution."""
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
PARENT = BASE + "r4c1_g3n4_force_attempt_01/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
MN = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
NULL_FIELDS = ("alpha", "Sx", "Sy", "Sz", "Em", "Z", "LambdaU")
MAIN_SOURCE = "Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v1.py"
MAIN_SHA = "0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_G3N5_TEMPORAL_BLOCK_CONTRACT_2026-10-09.md"
PINS = {
    PARENT + "summary.json": "ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287",
    PARENT + "independent.json": "dcd529971dc9eac6449619fc26284f3ea18a357f6406f44e35fb93145868d45e",
    MAIN_SOURCE: MAIN_SHA,
    CONTRACT: "a71a15d2e2d8620ce7b58666abed3eb512d31138a7628c2c648c8fe94ab0adfe",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_RESPONSE_KERNEL_CONTRACT_2026-10-09.md":
        "11cf25cef8cc0192f1f690dbf1f7fee2f9e0268eff508d7fb1a65709907f2c02",
}
CASES = (
    {"MP2": "1.1", "MU2": "0.2", "K_Q": "0.75", "C": "1.3", "epsilon0": "0.07",
     "c1": "0.2", "c2": "-0.14", "c3": "-0.0125", "c4": "0.05", "a": "1.4", "H": "0.4"},
    {"MP2": "1.3", "MU2": "0.11", "K_Q": "0.9", "C": "0.8", "epsilon0": "0.2",
     "c1": "0.13", "c2": "0.017", "c3": "-0.023", "c4": "0.04", "a": "1.8", "H": "0.23"},
)


def exact(checks, name, residual):
    values = list(residual) if isinstance(residual, (list, tuple, s.MatrixBase)) else [residual]
    reduced = [s.factor(s.expand(v)) for v in values]
    ok = all(v == 0 for v in reduced)
    checks.add(name, ok, "zero_exact" if ok else list(map(str, reduced)), "zero_exact")


def derive(checks):
    d = s.Symbol("d", real=True)
    a = s.Symbol("a", positive=True)
    H = s.Symbol("H", real=True)
    MP, MU, K, C, eps, c1, c2, c3, c4 = s.symbols(
        "MP2 MU2 K_Q C epsilon0 c1 c2 c3 c4", real=True)
    D = {name: s.Symbol(name + "_t", real=True) for name in FIELDS}
    g = s.diag(-1, a**2, a**2, a**2)
    gi = g.inv()
    gt = s.zeros(4)
    gt[0, 0] = -2*d*D["alpha"]
    for i in range(3):
        gt[0, i+1] = gt[i+1, 0] = a*d*D[("Sx", "Sy", "Sz")[i]]
        for j in range(3):
            gt[i+1, j+1] = a**2*(2*H*int(i == j) + d*D[MN[i][j]])
    dg = [gt, s.zeros(4), s.zeros(4), s.zeros(4)]
    Gamma = [[[s.expand(sum(gi[c, j]*(dg[i][j, k]+dg[k][j, i]-dg[j][i, k])
                               for j in range(4))/2)
               for k in range(4)] for i in range(4)] for c in range(4)]
    compatibility = [dg[mu][i, j]-sum(Gamma[k][mu][i]*g[k, j]+Gamma[k][mu][j]*g[i, k]
                                     for k in range(4))
                     for mu in range(4) for i in range(4) for j in range(4)]
    exact(checks, "direct_connection_metric_compatibility", compatibility)
    U = s.Matrix([1, 0, 0, 0])
    Ut = s.Matrix([d*(D["nu"]-D["alpha"])] +
                  [d*(D[vn]-D[sn])/a for vn, sn in zip(("Vx", "Vy", "Vz"), ("Sx", "Sy", "Sz"))])
    exact(checks, "off_unit_norm_derivative_retained", (U.T*gt*U)[0]+2*(U.T*g*Ut)[0]+2*d*D["nu"])
    DU = s.Matrix(4, 4, lambda mu, nu: (Ut[nu] if mu == 0 else 0)+Gamma[nu][mu][0])
    accel = DU.T*U
    invariants = [s.expand(sum(gi[i, j]*g[k, l]*DU[i, k]*DU[j, l]
                               for i in range(4) for j in range(4) for k in range(4) for l in range(4))),
                  s.expand(s.trace(DU)**2), s.expand(s.trace(DU*DU)),
                  s.expand((accel.T*g*accel)[0])]
    M = s.Matrix(3, 3, lambda i, j: D[MN[i][j]])
    ex = H*s.eye(3)+d*M/2
    nt = d*D["nu"]
    vt2 = d**2*sum(D[k]**2 for k in ("Vx", "Vy", "Vz"))
    controls = [nt**2-vt2+s.trace(ex*ex), (nt+s.trace(ex))**2,
                nt**2+s.trace(ex*ex), -nt**2+vt2]
    for i in range(4):
        exact(checks, f"frame_invariant_{i+1}_independent_trace_formula", invariants[i]-controls[i])
    adm_direct = MP*(s.trace(ex*ex)-s.trace(ex)**2)/2
    frame_direct = -MU*(c1*invariants[0]+c2*invariants[1]+c3*invariants[2]-c4*invariants[3])/2
    scalar_direct = sum((s.Symbol(bg, real=True)+d*D[k])**2/2
                        for bg, k in (("u_dot", "du"), ("v_dot", "dv"), ("r_dot", "dr")))
    force_direct = K*(s.Symbol("psi_dot", real=True)+d*D["Pi"])**2/2
    dust_direct = eps*(C**2*(C+d*D["T"])**2-C**4)/2
    direct = s.expand(adm_direct+frame_direct+scalar_direct+force_direct+dust_direct).coeff(d, 2)
    c13, c14, ctheta, csum = c1+c3, c1+c4, c1+3*c2+c3, c1+c2+c3+c4
    tr = s.trace(M)
    expected = ((MP-MU*c13)*s.trace(M*M)-(MP+MU*c2)*tr**2)/8 \
        -MU*csum*D["nu"]**2/2-MU*c2*D["nu"]*tr/2 \
        +MU*c14*sum(D[k]**2 for k in ("Vx", "Vy", "Vz"))/2 \
        +(D["du"]**2+D["dv"]**2+D["dr"]**2+K*D["Pi"]**2+eps*C**2*D["T"]**2)/2
    exact(checks, "complete_temporal_quadratic_form_independent_match", direct-expected)
    order = [D[k] for k in FIELDS]
    block, other = s.hessian(direct, order), s.hessian(expected, order)
    exact(checks, "all_484_temporal_Hessian_entries_match", block-other)
    exact(checks, "temporal_Hessian_symmetric", block-block.T)
    for name in NULL_FIELDS:
        exact(checks, name+"_full_zero_velocity_row", block[FIELDS.index(name), :])
    trace_velocity, normal_velocity = s.symbols("trace_velocity normal_velocity", real=True)
    trace_sub = {D[k]: 0 for k in FIELDS}
    trace_sub.update({D[k]: trace_velocity/3 for k in ("Mxx", "Myy", "Mzz")})
    trace_sub[D["nu"]] = normal_velocity
    trace_block = s.hessian(expected.subs(trace_sub), (trace_velocity, normal_velocity))
    trace_det = MU*((2*MP+MU*ctheta)*csum-3*MU*c2**2)/12
    exact(checks, "trace_normal_exact_determinant", trace_block.det()-trace_det)
    symbols = {str(q): q for q in expected.free_symbols | {a, H}}
    rank_rows = []
    for index, values in enumerate(CASES):
        sub = {symbols[k]: s.Rational(v) for k, v in values.items()}
        generic = block.subs(sub)
        checks.add(f"generic_exact_raw_rank_{index}", generic.rank() == 15, generic.rank(), "15 unreduced velocities, not physical DOF")
        boundaries = {"MU2_zero": ({MU: 0}, 11), "K_Q_zero": ({K: 0}, 14),
                      "dust_density_zero": ({eps: 0}, 14), "c14_zero": ({c4: -c1}, 12),
                      "tensor_coefficient_zero": ({c3: MP/MU-c1}, 10),
                      "normal_trace_singular": ({c2: 0, c4: -c1-c3}, 14)}
        for name, (replacements, target) in boundaries.items():
            actual = block.subs(replacements, simultaneous=True).subs(sub).rank()
            checks.add(f"raw_rank_boundary_{index}_{name}", actual == target, actual, target)
            rank_rows.append({"case": index, "boundary": name, "rank": actual})
        mutations = {
            "omit_frame_normal": expected.subs(D["nu"], 0),
            "omit_normal_trace_mixing": expected+MU*c2*D["nu"]*tr/2,
            "drop_c4_from_boost": expected-MU*c4*sum(D[k]**2 for k in ("Vx", "Vy", "Vz"))/2,
            "reverse_Einstein_sign": expected-2*MP*(s.trace(M*M)-tr**2)/8,
            "insert_projector_trace": expected-MP*(s.trace(M*M)-tr**2)/24,
            "invent_lapse_velocity": expected+D["alpha"]**2/2,
            "dust_C4_instead_of_C2": expected+eps*(C**4-C**2)*D["T"]**2/2,
        }
        for name, changed in mutations.items():
            delta = s.hessian(changed-expected, order).subs(sub)
            checks.add(f"reject_{index}_{name}", any(v != 0 for v in delta), "matrix differs" if any(v != 0 for v in delta) else "UNREJECTED")
    formulas = {"fields": list(FIELDS), "velocity_order": list(map(str, order)),
                "quadratic_pure_velocity_density_over_a3": str(s.factor(expected)),
                "direct_quadratic_density_over_a3": str(s.factor(direct)),
                "frame_invariants": list(map(str, invariants)),
                "trace_normal_block": [[str(v) for v in row] for row in trace_block.tolist()],
                "trace_normal_determinant": str(s.factor(trace_det)),
                "entries": [{"row": i, "column": j, "value": str(s.factor(block[i, j]))}
                            for i in range(22) for j in range(22) if block[i, j] != 0],
                "null_velocity_rows": list(NULL_FIELDS), "generic_raw_rank": 15,
                "rank_boundary_controls": rank_rows,
                "physical_Hessian_or_DOF_claim": "NONE", "spatial_or_mixed_blocks": "NOT_SUPPLIED_BY_THIS_CONTROL"}
    return expected, block, symbols, D, formulas


def raw_density(d, params, velocities):
    a, H = params["a"], params["H"]
    g = mp.diag([-1, a*a, a*a, a*a])
    gi = g**-1
    gt = mp.matrix(4)
    gt[0, 0] = -2*d*velocities["alpha"]
    for i in range(3):
        gt[0, i+1] = gt[i+1, 0] = a*d*velocities[("Sx", "Sy", "Sz")[i]]
        for j in range(3):
            gt[i+1, j+1] = a*a*(2*H*int(i == j)+d*velocities[MN[i][j]])
    dg = [gt, mp.matrix(4), mp.matrix(4), mp.matrix(4)]
    Gamma = [[[sum(gi[c, j]*(dg[i][j, k]+dg[k][j, i]-dg[j][i, k]) for j in range(4))/2
               for k in range(4)] for i in range(4)] for c in range(4)]
    Ut = [d*(velocities["nu"]-velocities["alpha"])] + [
        d*(velocities[vn]-velocities[sn])/a for vn, sn in zip(("Vx", "Vy", "Vz"), ("Sx", "Sy", "Sz"))]
    DU = mp.matrix([[ (Ut[nu] if mu == 0 else 0)+Gamma[nu][mu][0]
                     for nu in range(4)] for mu in range(4)])
    acc = mp.matrix([DU[0, i] for i in range(4)])
    I1 = sum(gi[i, j]*g[k, l]*DU[i, k]*DU[j, l]
             for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    I2 = sum(DU[i, i] for i in range(4))**2
    I3 = sum(DU[i, j]*DU[j, i] for i in range(4) for j in range(4))
    I4 = (acc.T*g*acc)[0]
    frame = -params["MU2"]*(params["c1"]*I1+params["c2"]*I2+params["c3"]*I3-params["c4"]*I4)/2
    km = mp.matrix([[gt[i+1, j+1]/(2*a*a) for j in range(3)] for i in range(3)])
    adm = params["MP2"]*(sum(km[i, j]*km[j, i] for i in range(3) for j in range(3))
                         -sum(km[i, i] for i in range(3))**2)/2
    canonical = sum((mp.mpf((i+1))/7+d*velocities[k])**2/2 for i, k in enumerate(("du", "dv", "dr")))
    temporal = params["K_Q"]*(mp.mpf("0.125")+d*velocities["Pi"])**2/2
    dust = params["epsilon0"]*(params["C"]**2*(params["C"]+d*velocities["T"])**2-params["C"]**4)/2
    # At this point Y=0; projected alignment/regulator, potentials and unit
    # multiplier supply no pure-velocity quadratic term. No spatial term in
    # the full action is removed by this block extraction.
    return frame+adm+canonical+temporal+dust


def numerical(checks, quadratic, symbols, D):
    rows = []
    for index, values in enumerate(CASES):
        params = {k: mp.mpf(v) for k, v in values.items()}
        velocities = {name: mp.mpf((i+1)*(-1 if index and i % 2 else 1))/121
                      for i, name in enumerate(FIELDS)}
        sub = {symbols[k]: s.Rational(v) for k, v in values.items()}
        sub.update({D[k]: s.Rational((i+1)*(-1 if index and i % 2 else 1), 121)
                    for i, k in enumerate(FIELDS)})
        target = mp.mpf(str(s.N(quadratic.subs(sub), 65)))
        f0 = raw_density(mp.mpf(0), params, velocities)
        evaluations = []
        for step in ("0.001", "0.0005", "0.00025"):
            d = mp.mpf(step)
            actual = (raw_density(d, params, velocities)+raw_density(-d, params, velocities)-2*f0)/(2*d*d)
            error = abs(actual-target)/max(1, abs(actual), abs(target))
            checks.add(f"unexpanded_50digit_time_jet_{index}_{step}", error <= mp.mpf("1e-38"), str(error), "<=1e-38")
            evaluations.append({"d": step, "actual": str(actual), "target": str(target), "normalized_error": str(error)})
        rows.append({"case": index, "params": values, "velocities": {k: str(v) for k, v in velocities.items()}, "rows": evaluations})
    return rows


def compare_kernel(checks, directory, block, symbols, pins):
    dest = (ROOT/directory).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    summary_name = (dest/"summary.json").relative_to(ROOT).as_posix()
    parent = common.read_json(summary_name)
    if parent["script_sha256"] != MAIN_SHA:
        raise RuntimeError("Comparison is not the frozen G3N5 v1")
    for name, expected in parent["source_sha256"].items():
        if name in pins and pins[name] != expected:
            raise RuntimeError("Comparison source collision: "+name)
        pins[name] = expected
    for name, expected in parent["artifacts"].items():
        pins[(dest/name).relative_to(ROOT).as_posix()] = expected
    pins[summary_name] = common.sha((dest/"summary.json").read_bytes())
    common.inspect_pins(pins)
    checks.add("compared_full_kernel_parent_validation", parent["passed"] == parent["total"]
               and all(row["passed"] for row in parent["checks"]),
               {"passed": parent["passed"], "total": parent["total"], "validation": parent["validation"]})
    kernel = common.read_json((dest/"kernel.json").relative_to(ROOT).as_posix())
    indices = [kernel["jet_order"].index(k+"_t") for k in FIELDS]
    entries = {(row["row"], row["column"]): row["value"] for row in kernel["entries"]}
    residues = []
    for i in range(22):
        for j in range(22):
            text = entries.get((indices[i], indices[j]), "0")
            names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text))
            if "__" in text or not re.fullmatch(r"[A-Za-z_0-9+\-*/(). \t]+", text) or not names <= set(symbols):
                raise ValueError("Unexpected pure-time coefficient syntax")
            residues.append(s.sympify(text, locals=symbols)-block[i, j])
    exact(checks, "full_110_jet_kernel_all_484_time_entries_match", residues)
    return {"directory": directory, "summary_sha256": pins[summary_name],
            "kernel_sha256": pins[(dest/"kernel.json").relative_to(ROOT).as_posix()],
            "parent_validation": parent["validation"],
            "parent_failed_checks": [row for row in parent["checks"] if not row["passed"]]}


def calculate(comparison):
    mp.mp.dps = 50
    parent = common.read_json(PARENT+"summary.json")
    pins = dict(parent["source_sha256"])
    pins.update(PINS)
    pins[SELF] = common.sha((ROOT/SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("all_source_pins_and_sidecars_before", True,
               {"pins": len(pins), "available_sidecars": len(pins)-len(missing), "known_absent": missing})
    quadratic, block, symbols, D, formulas = derive(checks)
    numbers = numerical(checks, quadratic, symbols, D)
    compared = compare_kernel(checks, comparison, block, symbols, pins) if comparison else None
    inherited = common.read_json(PARENT+"independent.json")
    checks.add("inherited_G3_and_N3_failures_retained", len(inherited["inherited_failed_parent_checks"]) == 1
               and len(inherited["superseded_N3_attempt_01_failed_checks"]) == 2)
    checks.add("all_source_pins_and_sidecars_after", common.inspect_pins(pins) == missing)
    payloads = {"formulas.json": common.encode(formulas),
                "independent.json": common.encode({"mp_digits": 50, "jets": numbers, "full_kernel_comparison": compared,
                  "inherited_failed_parent_checks": inherited["inherited_failed_parent_checks"],
                  "superseded_N3_attempt_01_failed_checks": inherited["superseded_N3_attempt_01_failed_checks"]})}
    passed = sum(row["passed"] for row in checks.rows)
    ok = passed == len(checks.rows)
    summary = {"schema": "r4c1-g3n5-temporal-block-v1", "passed": passed, "total": len(checks.rows), "checks": checks.rows,
               "validation": "PASS_LOCAL_CONTROLS" if ok else "FAIL_LOCAL_CONTROLS",
               "status": ("TEMPORAL_BLOCK_AND_FULL_KERNEL_COMPARISON_CHECKED" if compared else
                          "TEMPORAL_BLOCK_CHECKED_FULL_KERNEL_COMPARISON_PENDING") if ok else "TEMPORAL_BLOCK_REQUIRES_DISPOSITION",
               "full_kernel_comparison_completed": compared is not None,
               "pending_requirements": (["Full G3N5 kernel comparison"] if not compared else [])+
                   ["Constraint/gauge reduction and compatible initial data", "Coupled response and full nonlinear evolution",
                    "Physical spectrum/stability, cutoff, continuous healthy GR and inherited C1/C2 holds"],
               "fields": list(FIELDS), "raw_generic_velocity_rank": 15, "physical_DOF_count": "NOT_COMPUTED",
               "source_sha256": dict(sorted(pins.items())), "inherited_sidecars_absent": missing,
               "script_sha256": pins[SELF], "artifacts": {k: common.sha(v) for k, v in payloads.items()},
               "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False, "review_status": "DEFERRED",
               "full_second_order_response_solved": False, "full_nonlinear_evolution_verified": False,
               "physical_Hessian_verified": False, "canonical_tests_1_to_3": "HOLD_SUBSTANTIVE",
               "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED",
               "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED",
               "review_dependencies": ["R9-MT1-G3N5", "all inherited scientific and review debt"],
               "runtime": {"python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__, "mp_decimal_digits": mp.mp.dps}}
    payloads["summary.json"] = common.encode(summary)
    return payloads, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE+"r4c1_g3n5_time_block_attempt_01")
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    parser.add_argument("--compare-kernel", metavar="G3N5_OUTPUT")
    args = parser.parse_args()
    dest = (ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    payloads, summary = calculate(args.compare_kernel)
    if args.replay:
        for name, data in payloads.items():
            if (dest/name).read_bytes() != data or (dest/(name+".sha256")).read_text() != common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Replay bytes or sidecar differ: "+name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            with (dest/name).open("xb") as out:
                out.write(data)
            with (dest/(name+".sha256")).open("xb") as out:
                out.write((common.sha(data)+"  "+name+"\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action": action, **{k: summary[k] for k in (
        "validation", "passed", "total", "status", "full_kernel_comparison_completed", "physics_pass", "gate_effect", "Rule9_cleared")}}))
    for row in summary["checks"]:
        if not row["passed"]:
            print(json.dumps(row))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
