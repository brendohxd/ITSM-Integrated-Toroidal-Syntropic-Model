"""Bound the prepared R-tau trace momentum lift and frame-flux drifts."""

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import r4c1_canonical_density_factory_v1 as factory
from test_rtau_differentiated_trace_assembly_v1 import (
    GATE, MANIFEST, OUT, ROOT, digest, read,
)


CONTRACT = GATE + "RES001_RTAU_TRACE_MOMENTUM_DRIFT_V1_CONTRACT_2026-11-09.md"
ASSEMBLY = OUT + "rtau_differentiated_trace_assembly_v1_20261109/receipt.json"
LIFT = OUT + "rtau_strong_constraint_lift_v4_20261104/receipt.json"
CLOCK = OUT + "r4c1_rtau_clock_density_v3_attempt_01/summary.json"


def exact_controls():
    x, t = sp.symbols("x t")

    def mean(f):
        return sp.expand(f).coeff(x, 0)

    def primitive(f):
        f = sp.expand(f)
        return sum(f.coeff(x, k)*x**k/(sp.I*k) for k in range(-6, 7) if k)

    a = 2+x/7+1/(7*x)+t*(3+x/11+1/(11*x))
    p = 1+x/5+1/(5*x)+t*(1+x**2/3+1/(3*x**2))
    f = 1+x+1/x
    R = (sp.I*x*sp.diff(a, x)*p-a*sp.I*x*sp.diff(p, x))/2
    R0, Rt = sp.expand(R.subs(t, 0)), sp.expand(sp.diff(R, t).subs(t, 0))
    # Use an independent periodic normalization with a changing mean and shape.
    u = 2+x/9+1/(9*x)+t*(1+x/7+1/(7*x))
    y = p*f/2+u*primitive(R*f)
    direct = sp.expand(sp.diff(y-u*mean(y)/mean(u), t).subs(t, 0))
    u0, ut, y0 = u.subs(t, 0), sp.diff(u, t), sp.expand(y.subs(t, 0))
    yt = sp.diff(p, t)*f/2+ut*primitive(R0*f)+u0*primitive(Rt*f)
    normalized = yt-u0*mean(yt)/mean(u0)
    moving = (ut-u0*mean(ut)/mean(u0))*mean(y0)/mean(u0)
    rt_term = u0*primitive(Rt*f)
    return {
        "direct_periodic_rate_matches_split": sp.expand(direct-normalized+moving) == 0,
        "mean_rate_is_zero_for_trace_operator": mean(direct) == 0,
        "omitting_moving_normalization_is_detected": sp.expand(moving) != 0,
        "omitting_longitudinal_primitive_rate_is_detected":
            sp.expand(rt_term-u0*mean(rt_term)/mean(u0)) != 0,
    }


def first_differentials_only(dual):
    def product(self, other):
        other = self.cast(other)
        zero = self.scalar(0)
        grad = {i: self.g.get(i, zero)*other.c+other.g.get(i, zero)*self.c
                for i in self.g.keys() | other.g.keys()}
        return type(self)(self.c*other.c, {i: v for i, v in grad.items() if v != 0})

    def unary(self, value, first, second):
        return type(self)(value, {i: first*g for i, g in self.g.items() if g != 0})

    dual.__mul__ = dual.__rmul__ = product
    dual.unary = unary


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    magnitude = lambda x: max(abs(lo(x)), abs(hi(x)))
    decode = lambda x: iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary = lambda x: [list(v) for v in iv.mpf(x)._mpi_]
    pins = read(MANIFEST)["source_sha256"]
    for rel in (CONTRACT, ASSEMBLY, LIFT, CLOCK):
        path = ROOT/rel
        sidecar = path.with_suffix(path.suffix+".sha256")
        pins[rel] = sidecar.read_text().split()[0].lower()
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        sidecar = path.with_suffix(path.suffix+".sha256")
        assert digest(path) == expected, rel
        if sidecar.exists():
            assert sidecar.read_text().split()[0].lower() == expected, rel
        for item in (path, sidecar):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    assembly, lift, clock = map(read, (ASSEMBLY, LIFT, CLOCK))
    assert all(check["passed"] for parent in (assembly, lift, clock)
               for check in parent["checks"])
    mp.mp.dps, mp.iv.dps = 100, 60
    ctx = factory.prepare()
    mp.mp.dps, mp.iv.dps = 100, 60
    J = ctx["J"]
    first_differentials_only(ctx["D"])
    grad = ctx["gradient"]
    third_bound = hi(decode(clock["whole_circle_third_shift_bound"]))
    assert mp.isfinite(third_bound) and third_bound > 0
    third = iv.mpf([-third_bound, third_bound])
    cells = []
    checks = exact_controls()
    for record in lift["cells"]:
        z = decode(record["z"])
        y, _ = ctx["state"](J.variable(z), True, [third]*3)
        action = ctx["evaluate"](y)
        assert not action.h
        q, v, g = y[:14], y[14:28], y[28:42]
        a = q[0]**mp.mpf(".5")
        rate = v[0]/(2*q[0])
        at = a*rate
        p = [grad(action, 14+i) for i in (0, 3, 2, 4)]
        pt = []
        for i in (0, 3, 2, 4):
            local, flux = grad(action, i), grad(action, 28+i)
            pt.append(J(coefficients=[local.c[0]-flux.c[1],
                                      local.c[1]-2*flux.c[2], iv.mpf(0)]))
        ptr, ptrt = p[0]+p[1], pt[0]+pt[1]
        R = (a.c[1]*ptr.c[0]-a.c[0]*ptr.c[1])/2
        Rt = (at.c[1]*ptr.c[0]+a.c[1]*ptrt.c[0]
              -at.c[0]*ptr.c[1]-a.c[0]*ptrt.c[1])/2
        N, _, gamma, _, _ = ctx["geometry"](q, g)
        gamma_t = q[0]*sum((rate*q[i]**2+q[i]*v[i] for i in (6, 7, 8)), J(0))/gamma
        C = N*gamma/q[0]
        Ct = C*(-(iv.mpf(2)/5)*v[12]+gamma_t/gamma-2*rate)
        u = [(1/a**j).c[0] for j in (2, 2, 1)]
        cells.append(dict(u=u, L=rate.c[0], p=[p[2].c[0], p[3].c[0], ptr.c[0]/2],
                          pt=[pt[2].c[0], pt[3].c[0], ptrt.c[0]/2],
                          R=R, Rt=Rt, Ct=Ct.c[0], D_Ct=Ct.c[1]))

    def sup(values):
        return iv.mpf(max(magnitude(v) for v in values))

    rate_span = (iv.mpf(max(hi(cell["L"]) for cell in cells))
                 -iv.mpf(min(lo(cell["L"]) for cell in cells)))
    max_rate = sup(cell["L"] for cell in cells)
    R_norm, Rt_norm = (sup(cell[k] for cell in cells) for k in ("R", "Rt"))
    estimates = {}
    for i, (slot, j) in enumerate(zip(("x", "y", "longitudinal"), (2, 2, 1))):
        U = sup(cell["u"][i] for cell in cells)
        u_min = iv.mpf(min(lo(cell["u"][i]) for cell in cells))
        assert lo(u_min) > 0
        normalized = 1+U/u_min
        normalized_rate = j*rate_span*U/u_min
        Y = sup(cell["p"][i] for cell in cells)
        Yt = sup(cell["pt"][i] for cell in cells)
        if slot == "longitudinal":
            Y += U*R_norm
            Yt += U*(j*max_rate*R_norm+Rt_norm)
        estimates[f"Tdot_{slot}_L2_to_L2"] = normalized*Yt+normalized_rate*Y
        estimates[f"normalization_rate_{slot}_L2_to_L2"] = normalized_rate
    estimates["Cdot_multiplier_Hminus1"] = sup(c["Ct"] for c in cells)+sup(c["D_Ct"] for c in cells)
    estimates["Rt_Linfinity"] = Rt_norm
    prior = decode(assembly["bounds_binary"]["C_t"])
    checks.update(
        inherited_circle_partition_retained=len(cells) == 16,
        frame_rate_consistent_with_independent_time_jet=all(
            lo(prior) <= hi(cell["Ct"]) and lo(cell["Ct"]) <= hi(prior) for cell in cells),
        coefficient_enclosures_are_finite=all(mp.isfinite(hi(v)) and lo(v) >= 0
                                               for v in estimates.values()),
        pinned_bytes_sidecars_and_timestamps_preserved=all(
            (digest(path), path.stat().st_mtime_ns) == stamp for path, stamp in snapshot.items()),
    )
    assert all(checks.values()), checks
    return dict(kind="RTAU_TRACE_MOMENTUM_DRIFT_V1", source_sha256=digest(Path(__file__)),
                contract_sha256=pins[CONTRACT], manifest_sha256=digest(ROOT/MANIFEST),
                pinned_sources=len(pins), checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                bounds_binary={k: binary(v) for k, v in estimates.items()},
                cell_enclosures=[{k: [binary(v) for v in vs] if isinstance(vs, list) else binary(vs)
                                  for k, vs in c.items()} for c in cells],
                scope="CONDITIONAL_INITIAL_FIXED_INPUT_LIFT_AND_FRAME_FLUX_DRIFT",
                full_coupled_bound="OPEN", review_status="DEFERRED", physics_pass=False, gate_effect="NONE")


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
        print("Trace momentum drift controls complete")


if __name__ == "__main__":
    main()
