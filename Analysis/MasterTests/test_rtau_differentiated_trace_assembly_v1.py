"""Verify differentiated trace/source assembly and actual leading drift."""

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
CONTRACT = GATE + "RES001_RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"
TRACE = OUT + "rtau_trace_green_rate_v3_20261109/receipt.json"
WARD = OUT + "rtau_ward_range_rate_v2_20261109/receipt.json"
GAUGE = OUT + "rtau_gauge_mean_trace_rate_v2_20261109/receipt.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def exact_controls():
    x, t = sp.symbols("x t")

    def modes(value):
        return [(term.as_powers_dict().get(x, 0), term)
                for term in sp.Add.make_args(sp.expand(value))]

    def D(value):
        return sp.expand(sum(sp.I*n*term for n, term in modes(value)))

    def mean(value):
        return sum(term for n, term in modes(value) if n == 0)

    def primitive(value):
        return sp.expand(sum(term/(sp.I*n) for n, term in modes(value) if n))

    def at(value):
        return sp.expand(value.subs(t, 0))

    def rate(value):
        return at(sp.diff(value, t))

    u, r, wgt, p, m, c, alpha, v, A, B, Fq, Fd, Fp = [
        (i+2)+x/(i+3)+x**-1/(i+4)+t*(1+x**2)/(i+5)
        for i in range(13)]
    f, shape, free, xi, chi, source, eta = [
        (i+1)+x**2/(i+2)+x**-2/(i+3)+t*(i+x) for i in range(1, 8)]
    eta = mean(eta)
    gauge = t*(2+x**3)
    lifted = p*f/2+u*primitive(r*f+wgt*source)
    normalized = lifted+u*(eta-mean(lifted))/mean(u)
    q = shape*f+free+gauge

    def qop(y):
        return A*y+B*D(y)-D(Fq*y+Fd*D(y))

    def pop(y):
        return -v*y

    current = qop(q)+pop(normalized)-D(Fp*free)-m*(c*primitive(xi)+alpha*D(chi))
    exact_rate = rate(current)
    lifted_rate = (p*sp.diff(f, t)/2+sp.diff(p, t)*f/2
                   +sp.diff(u, t)*primitive(r*f+wgt*source)
                   +u*primitive(r*sp.diff(f, t)+sp.diff(r, t)*f
                                +wgt*sp.diff(source, t)+sp.diff(wgt, t)*source))
    normal = (eta-mean(lifted))/mean(u)
    norm_rate = (lifted_rate+sp.diff(u, t)*normal
                 +u*(sp.diff(eta, t)-mean(lifted_rate)-mean(sp.diff(u, t))*normal)/mean(u))
    q_rate = shape*sp.diff(f, t)+sp.diff(shape, t)*f+sp.diff(free+gauge, t)
    separated = (qop(q_rate)+sp.diff(A, t)*q+sp.diff(B, t)*D(q)
                 -D(sp.diff(Fq, t)*q+sp.diff(Fd, t)*D(q))
                 +pop(norm_rate)-sp.diff(v, t)*normalized
                 -D(Fp*sp.diff(free, t)+sp.diff(Fp, t)*free)
                 -sp.diff(m*c, t)*primitive(xi)-m*c*primitive(sp.diff(xi, t))
                 -sp.diff(m*alpha, t)*D(chi)-m*alpha*D(sp.diff(chi, t)))
    # Split only the terms linear in the trace rate into the fixed operator.
    tr = sp.diff(f, t)
    yt = p*tr/2+u*primitive(r*tr)
    Ttr = yt-u*mean(yt)/mean(u)
    fixed_trace = qop(shape*tr)+pop(Ttr)
    explicit_remainder = (
        qop(sp.diff(shape, t)*f+sp.diff(free+gauge, t))
        +sp.diff(A, t)*q+sp.diff(B, t)*D(q)-D(sp.diff(Fq, t)*q+sp.diff(Fd, t)*D(q))
        +pop(norm_rate-Ttr)-sp.diff(v, t)*normalized
        -D(Fp*sp.diff(free, t)+sp.diff(Fp, t)*free)
        -sp.diff(m*c, t)*primitive(xi)-m*c*primitive(sp.diff(xi, t))
        -sp.diff(m*alpha, t)*D(chi)-m*alpha*D(sp.diff(chi, t)))
    return dict(
        exact_periodic_direct_rate_matches_separated_terms=exact_rate == at(separated),
        differentiated_current_is_fixed_trace_plus_remaining_source=
            exact_rate == at(fixed_trace+explicit_remainder),
        actual_momentum_mean_rate_preserved=sp.simplify(mean(at(norm_rate))-rate(eta)) == 0,
        moving_momentum_normalization_required=at(pop(sp.diff(u, t)*normal)) != 0,
        moving_shape_required=at(qop(sp.diff(shape, t)*f)) != 0,
        moving_gauge_source_required=at(qop(sp.diff(gauge, t))) != 0,
        moving_density_compensation_required=at(sp.diff(m*c, t)*primitive(xi)) != 0,
        differentiating_only_local_trace_operator_rejected=at(pop(Ttr)) != 0)


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    overlap = lambda a, b: lo(a) <= hi(b) and lo(b) <= hi(a)
    binary = lambda x: [list(a) for a in iv.mpf(x)._mpi_]
    pins = read(MANIFEST)["source_sha256"]
    for rel in (TRACE, WARD, GAUGE):
        path = ROOT/rel
        pins[rel] = path.with_suffix(".json.sha256").read_text().split()[0]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix+".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    for rel in (TRACE, WARD, GAUGE):
        assert all(c["passed"] for c in read(rel)["checks"]), rel
    spec = importlib.util.spec_from_file_location("trace_assembly_factory", ROOT/FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = module.prepare()
    J = ctx["J"]
    y, _ = ctx["state"](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    q, v = y[:14], y[14:28]
    first_jet = lambda a, b: J(coefficients=[a, b, iv.mpf(0)])
    Q = [first_jet(a.c[0], b.c[0]) for a, b in zip(q, v)]
    N, _, gamma, _, _ = ctx["geometry"](Q, [J(0)]*14)
    a = Q[0]**mp.mpf(".5")
    A2, C = -N*a, N*gamma/Q[0]
    L = Q[0].c[1]/(2*Q[0].c[0])
    beta = iv.mpf(2)/5
    nlog = -beta*v[12].c[0]
    frame = [Q[i].c[0] for i in (6, 7, 8)]
    frame_t = [Q[i].c[1] for i in (6, 7, 8)]
    gamma_t = Q[0].c[0]*sum((L*x*x+x*xdot for x, xdot in zip(frame, frame_t)),
                             iv.mpf(0))/gamma.c[0]
    checks = exact_controls()
    checks["actual_A2_time_rate_matches_explicit_formula"] = overlap(
        A2.c[1], A2.c[0]*(nlog+L))
    checks["actual_frame_source_time_rate_matches_explicit_formula"] = overlap(
        C.c[1], C.c[0]*(nlog+gamma_t/gamma.c[0]-2*L))
    checks["actual_highest_trace_and_frame_source_drifts_are_nonzero"] = (
        hi(A2.c[1]) < 0 and hi(C.c[1]) < 0)
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(path), path.stat().st_mtime_ns) == value for path, value in snapshot.items())
    assert all(checks.values()), checks
    return dict(kind="RTAU_DIFFERENTIATED_TRACE_ASSEMBLY_V1",
                source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
                manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                bounds_binary={"A2_t": binary(A2.c[1]), "C_t": binary(C.c[1])},
                interval_display={k: [mp.nstr(lo(val), 24), mp.nstr(hi(val), 24)]
                                  for k, val in {"A2_t": A2.c[1], "C_t": C.c[1]}.items()},
                scope="EXACT_COMPATIBLE_INITIAL_FIRST_JET_TRACE_ASSEMBLY",
                lower_order_total_numeric_bound="OPEN",
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
        print("Differentiated trace assembly controls complete")


if __name__ == "__main__":
    main()
