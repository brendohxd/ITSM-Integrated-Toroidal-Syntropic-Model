"""Initial all-mode bound on the nonlocal Sigma trace-operator drift."""

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import r4c1_canonical_density_factory_v1 as factory
from test_rtau_trace_momentum_drift_v2 import (
    ROOT, GATE, OUT, MANIFEST, LIFT, CLOCK, digest, read,
)

CONTRACT = GATE + "RES001_RTAU_NONLOCAL_TRACE_DRIFT_V1_CONTRACT_2026-11-09.md"
DRIFT = OUT + "rtau_trace_momentum_drift_v2_20261109/receipt.json"
GREEN = OUT + "rtau_trace_green_rate_v3_20261109/receipt.json"
ACCEL = OUT + "r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json"


def exact_controls():
    z, t = sp.symbols("z t", real=True)
    q = sp.sin(z)*(1+t)+2+t**2
    shift = sp.cos(z)+t*sp.sin(2*z)
    velocity = sp.diff(q, t)
    # Longitudinal covariant rank-two component, the h_zz slot.
    lie = lambda field, s: s*sp.diff(field, z)+2*field*sp.diff(s, z)
    material = velocity-lie(q, shift)
    acceleration0 = sp.diff(q, t, 2)-lie(q, sp.diff(shift, t))
    residual = sp.expand(sp.diff(material, t)-acceleration0+lie(velocity, shift))
    U, T, Ud, Td = sp.symbols("U T Ud Td")
    return {
        "material_rate_cancels_shift_rate_exactly": residual == 0,
        "omitting_lie_velocity_is_detected": sp.expand(lie(velocity, shift)) != 0,
        "omitting_shift_rate_before_cancellation_is_detected":
            sp.expand(lie(q, sp.diff(shift, t))) != 0,
        "nonlocal_product_drift_has_both_terms":
            sp.diff(-(U+t*Ud)*(T+t*Td), t).subs(t, 0) == -Ud*T-U*Td,
    }


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    magnitude = lambda x: max(abs(lo(x)), abs(hi(x)))
    decode = lambda x: iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary = lambda x: [list(v) for v in iv.mpf(x)._mpi_]
    acceleration = read(ACCEL)
    pins = dict(read(MANIFEST)["source_sha256"])
    for rel, expected in acceleration["source_sha256"].items():
        assert rel not in pins or pins[rel] == expected, rel
        pins[rel] = expected
    direct = (CONTRACT, DRIFT, GREEN, ACCEL, LIFT, CLOCK,
              "Analysis/MasterTests/test_rtau_trace_momentum_drift_v2.py",
              "Analysis/MasterTests/test_rtau_differentiated_trace_assembly_v1.py",
              "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py")
    for rel in direct:
        path = ROOT/rel
        expected = path.with_suffix(path.suffix+".sha256").read_text().split()[0].lower()
        assert rel not in pins or pins[rel] == expected, rel
        pins[rel] = expected
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert digest(path) == expected, rel
        sidecar = path.with_suffix(path.suffix+".sha256")
        if sidecar.exists():
            assert sidecar.read_text().split()[0].lower() == expected, rel
        for item in (path, sidecar):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    drift, green, lift = map(read, (DRIFT, GREEN, LIFT))
    assert all(c["passed"] for parent in (acceleration, drift, green, lift)
               for c in parent["checks"])
    assert acceleration["passed"] == acceleration["total"]
    ctx = factory.prepare()
    mp.mp.dps, mp.iv.dps = 100, 60
    J = ctx["J"]
    cells = []
    for record in lift["cells"]:
        y, _ = ctx["state"](J.variable(decode(record["z"])), True, [0, 0, 0])
        q, v, g, S, Sz = y[:14], y[14:28], y[28:42], y[42:45], y[45:48]
        vz = [J(coefficients=[a.c[1], 2*a.c[2], iv.mpf(0)]) for a in v]
        lie_q = ctx["lie"](q, g, S, Sz)
        lie_v = ctx["lie"](v, vz, S, Sz)
        cells.append({"cell": record["cell"],
                      "U": [v[i].c[0]-lie_q[i].c[0] for i in (2, 4, 5)],
                      "Lie_velocity": [lie_v[i].c[0] for i in (2, 4, 5)]})
    afree = decode(acceleration["bounds"]["particular_acceleration"])
    G2 = decode(green["bounds_binary"]["G_Hminus2_to_L2"])
    all_drift = drift["cell_enclosures"]
    sup = lambda xs: iv.mpf(max(magnitude(x) for x in xs))
    Rnorm = sup(decode(c["R"]) for c in all_drift)
    bounds = {}
    terms = []
    for i, name in enumerate(("x", "y", "longitudinal")):
        unorm = sup(c["U"][i] for c in cells)
        udot = afree+sup(c["Lie_velocity"][i] for c in cells)
        uweight = sup(decode(c["u"][i]) for c in all_drift)
        minweight = iv.mpf(min(lo(decode(c["u"][i])) for c in all_drift))
        assert lo(minweight) > 0
        ynorm = sup(decode(c["p"][i]) for c in all_drift)
        if i == 2:
            ynorm += uweight*Rnorm
        tnorm = (1+uweight/minweight)*ynorm
        tdot = decode(drift["bounds_binary"][f"Tdot_{name}_L2_to_L2"])
        term = udot*tnorm+unorm*tdot
        terms.append(term)
        bounds.update({f"U_{name}": unorm, f"Udot_{name}": udot,
                       f"T_{name}_L2_to_L2": tnorm, f"Kdot_{name}_L2_to_L2": term})
    bounds["Kdot_L2_to_L2"] = sum(terms, iv.mpf(0))
    bounds["Green_Kdot_L2_to_L2"] = G2*bounds["Kdot_L2_to_L2"]
    checks = exact_controls()
    checks.update(
        all_prepared_circle_cells_retained=len(cells) == len(all_drift) == 16,
        background_particular_acceleration_enclosure_positive=lo(afree) > 0,
        inherited_projected_green_bound_positive=lo(G2) > 0,
        nonlocal_bound_contains_three_positive_contributions=all(lo(x) > 0 for x in terms),
        all_bounds_finite=all(mp.isfinite(hi(x)) for x in bounds.values()),
        pinned_sources_and_sidecars_preserved=all(
            (digest(p), p.stat().st_mtime_ns) == stamp for p, stamp in snapshot.items()),
    )
    assert all(checks.values()), checks
    return dict(kind="RTAU_NONLOCAL_TRACE_DRIFT_V1", source_sha256=digest(Path(__file__)),
                contract_sha256=pins[CONTRACT], source_pins=pins, pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                bounds_binary={k: binary(v) for k, v in bounds.items()},
                outward_upper_display={k: mp.nstr(hi(v), 30) for k, v in bounds.items()},
                scope="CONDITIONAL_INITIAL_NONLOCAL_TRACE_BLOCK_DRIFT",
                local_current_drift="OPEN", full_coupled_energy="OPEN",
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
        print("Nonlocal trace drift controls complete")


if __name__ == "__main__":
    main()
