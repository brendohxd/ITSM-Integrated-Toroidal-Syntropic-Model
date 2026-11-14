"""Initial weighted range rate from the canonical spatial Ward identity."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GATE = "Theory/Gates/RES-001/"
OUT = "Analysis/MasterTests/outputs/"
MANIFEST = GATE + "RES001_RTAU_DENSITY_OPERATOR_COMPARISON_V1_PREPARATION_INPUTS_2026-11-05.json"
CONTRACT = GATE + "RES001_RTAU_WARD_RANGE_RATE_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"
PHYSICAL = OUT + "rtau_physical_density_rate_v1_20261109/receipt.json"
TRACE = OUT + "rtau_trace_green_rate_v3_20261109/receipt.json"
WARD = OUT + "r4c1_rtau_current_transport_v2_attempt_01/summary.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def exact_controls():
    z = sp.symbols("z", real=True)
    t = sp.symbols("t", real=True)
    D = lambda f: sp.diff(f, z)
    M = lambda f: sp.integrate(sp.expand(f), (z, 0, 2*sp.pi))/(2*sp.pi)
    w = 2+sp.cos(z)/3+t*sp.sin(z)/7
    F = 1+sp.sin(z)+t*sp.cos(z)+t/5
    W = -sp.cos(z)+t*sp.sin(z)
    E = (D(W)-F)/w
    c = M(F)
    residual_check = sp.cancel(w*E)
    rate_check = sp.cancel(sp.diff(w, t)*E+w*sp.diff(E, t))
    a = sp.Function("a")(z)
    trace = sp.Function("f")(z)
    Ptrace = sp.Function("p")(z)
    pm = sp.Function("m")(z)
    src = sp.Function("s")(z)
    R = (D(a)*Ptrace-a*D(Ptrace))/2
    original = D(2*a*a*pm)-D(a*a)*pm-Ptrace*D(a*a*trace)-src
    factorized = 2*a*(D(a*pm-a*Ptrace*trace/2)-R*trace-src/(2*a))
    C = (sp.sin(z), sp.cos(z), 2+sp.cos(2*z))
    shift = (sp.cos(z), sp.sin(2*z), sp.sin(z))
    wz = w.subs(t, 0)
    lie_L = D(shift[2]*C[2])+sum(D(v)*ci for v, ci in zip(shift, C))
    direct = -M(wz*lie_L)
    dual = M(shift[2]*D(wz)*C[2]+sum(v*D(wz*ci) for v, ci in zip(shift, C)))
    off_range = -c/w
    S = sp.sin(z)
    ward = D(S*off_range)+D(S)*off_range
    actual_projected = -w*ward-sp.diff(w, t)*off_range
    expected_projected = c*(-S*D(w)/w+2*D(S)+sp.diff(w, t)/w)
    return dict(
        actual_longitudinal_integrating_factor=sp.expand(original-factorized) == 0,
        weighted_residual_equals_negative_range=sp.simplify(M(residual_check)+c) == 0,
        differentiated_weighted_residual=M(rate_check) == -sp.diff(c, t),
        omitting_weight_rate_rejected=sp.simplify((sp.diff(w, t)*E).subs({z: 0, t: 0})) != 0
            or sp.simplify((sp.diff(w, t)*E).subs({z: sp.pi/2, t: 0})) != 0,
        covector_density_defect_dual_pairing=sp.simplify(direct-dual) == 0,
        transverse_shift_index_term_required=M(wz*D(shift[0])*C[0]) != 0,
        projected_homogeneous_ward_rate=sp.simplify(actual_projected-expected_projected) == 0,
        periodic_transverse_and_charge_fluxes_have_zero_mean=
            all(M(D(v)) == 0 for v in (wz*lie_L, wz*C[1]+S*C[2], S*F)))


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    absolute = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    binary = lambda x: [list(a) for a in iv.mpf(x)._mpi_]
    pins = read(MANIFEST)["source_sha256"]
    for rel in (PHYSICAL, TRACE):
        path = ROOT/rel
        pins[rel] = path.with_suffix(".json.sha256").read_text().split()[0]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix+".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    for rel in (PHYSICAL, TRACE, WARD):
        assert rel in pins and all(c["passed"] for c in read(rel)["checks"]), rel

    spec = importlib.util.spec_from_file_location("ward_range_factory", ROOT/FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = module.prepare()
    J, D = ctx["J"], ctx["D"]

    def first_mul(self, other):
        other = self.cast(other)
        zero = self.scalar(0)
        g = {i: self.g.get(i, zero)*other.c+other.g.get(i, zero)*self.c
             for i in self.g.keys() | other.g.keys()}
        return type(self)(self.c*other.c, {i: v for i, v in g.items() if v != 0})

    def first_unary(self, value, first, second):
        return type(self)(value, {i: first*g for i, g in self.g.items() if g != 0})

    D.__mul__ = D.__rmul__ = first_mul
    D.unary = first_unary
    y, _ = ctx["state"](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    L = ctx["evaluate"](y)
    assert not L.h
    q, gradq = y[:13], y[28:41]
    p = [ctx["gradient"](L, 14+i) for i in range(13)]
    shift, a2 = y[44], q[0]
    w = 1/(2*a2**mp.mpf(".5"))
    qflux = sum((p_i*d_i for p_i, d_i in zip(p, gradq)), J(0))
    C0, C1 = [], []
    for j, slot in enumerate((2, 4, 5)):
        flux = a2*p[slot]*(2 if j == 2 else 1)-q[8]*p[6+j]
        C0.append(flux.c[1]-(qflux.c[0] if j == 2 else 0))
        C1.append(2*flux.c[2]-(qflux.c[1] if j == 2 else 0))
    defect_components = [w.c[0]*cp+(2 if j == 2 else 1)*w.c[1]*ci
                         for j, (ci, cp) in enumerate(zip(C0, C1))]
    defect = iv.sqrt(sum((absolute(v)**2 for v in defect_components), iv.mpf(0)))
    logarithmic_rate = -y[14].c[0]/(2*a2.c[0])+shift.c[0]*gradq[0].c[0]/(2*a2.c[0])
    checks = exact_controls()
    checks["finite_whole_root_defect_and_rate"] = all(
        mp.isfinite(hi(absolute(v))) for v in (defect, logarithmic_rate, *C0, *C1))
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(p), p.stat().st_mtime_ns) == value for p, value in snapshot.items())
    assert all(checks.values()), checks
    return dict(kind="RTAU_WARD_RANGE_RATE_V2",
                source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
                manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                coefficient_bound_binary=binary(defect),
                coefficient_bound_upper=mp.nstr(hi(defect), 30),
                homogeneous_coefficient_enclosure_binary=binary(logarithmic_rate),
                homogeneous_coefficient_display=[mp.nstr(lo(logarithmic_rate), 26),
                                                 mp.nstr(hi(logarithmic_rate), 26)],
                exact_initial_range_and_charge_tangency="CONDITIONAL_ON_FULL_EULER_AUXILIARY_JET",
                finite_time_compatible_inverse="OPEN",
                review_status="DEFERRED", physics_pass=False, gate_effect="NONE")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--replay", type=Path)
    args = parser.parse_args()
    payload = (json.dumps(calculate(), indent=2, allow_nan=False)+"\n").encode()
    if args.replay:
        assert args.replay.read_bytes() == payload
        print("Byte-identical read-only replay")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open("xb") as stream:
            stream.write(payload)
        print("Weighted Ward range rate controls complete")


if __name__ == "__main__":
    main()
