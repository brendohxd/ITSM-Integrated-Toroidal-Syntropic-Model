"""Initial canonical momentum means, moduli and direct R-tau trace rate."""

import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GATE = "Theory/Gates/RES-001/"
OUT = "Analysis/MasterTests/outputs/"
MANIFEST = GATE + "RES001_RTAU_DENSITY_OPERATOR_COMPARISON_V1_PREPARATION_INPUTS_2026-11-05.json"
CONTRACT = GATE + "RES001_RTAU_GAUGE_MEAN_TRACE_RATE_V1_CONTRACT_2026-11-09.md"
MIXED = OUT + "r4c1_rtau_mixed_operator_v4_attempt_01/summary.json"
WEAK = OUT + "rtau_weak_canonical_rate_v2_20261103/receipt.json"
GAUGE = OUT + "rtau_initial_gauge_composition_v2_20261103/receipt.json"
LIFT = OUT + "rtau_momentum_rate_lift_v2_20261104/receipt.json"
COEFF = OUT + "rtau_prepared_weak_coefficients_v1_20261102/receipt.json"
WARD = OUT + "rtau_ward_range_rate_v2_20261109/receipt.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def exact_controls():
    z, t = sp.symbols("z t", real=True)
    D = lambda f: sp.diff(f, z)
    M = lambda f: sp.integrate(sp.expand(f), (z, 0, 2*sp.pi))/(2*sp.pi)
    a, cross_x, cross_y, hzz = sp.symbols("a hxz hyz hzz")
    h = sp.Matrix([[a, 0, cross_x], [0, a, cross_y], [cross_x, cross_y, hzz]])
    inds = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))
    B = sp.Matrix([[(h[i, j] if k == 2 else 0)+(h[k, j] if i == 2 else 0)
                    for j in range(3)] for i, k in inds])
    p = sp.Matrix(sp.symbols("p0:6"))
    K = sp.Matrix.hstack(*(B.diff(q).T*p for q in (cross_x, cross_y, hzz)))
    expected = sp.Matrix([[2*p[5], 0, 0], [0, 2*p[5], 0], [p[2], p[4], 2*p[5]]])
    px, py, pz = sp.sin(z), sp.cos(z), 2+sp.sin(2*z)
    sx, sy, sz = sp.cos(2*z), sp.sin(2*z), sp.cos(z)
    gauge = sz*D(px)+D(sz)*px-2*pz*D(sx)-px*D(sz)
    regulator = (2+sp.sin(z))*D(sp.cos(z))
    adapted_weight, adapted_p = 1-t*sp.cos(z), 2+sp.cos(z)+t*sp.sin(z)
    H = 2+t*sp.cos(z)
    metric = H*(1+sp.sin(z)+t*sp.cos(2*z))
    return dict(
        actual_metric_index_matrix=K == expected,
        scalar_density_transport_has_zero_mean=M(D(sz*px)) == 0,
        paired_mean_identity=M(gauge+2*pz*D(sx)+px*D(sz)) == 0,
        omitting_transverse_index_term_rejected=M(2*pz*D(sx)) != 0,
        regulator_gradient_integrates_by_parts=M(regulator+D(2+sp.sin(z))*sp.cos(z)) == 0,
        omitting_moving_adapted_weight_rejected=M(sp.diff(adapted_weight, t)*adapted_p) != 0,
        direct_trace_rate_includes_moving_scale=sp.simplify(
            sp.diff(metric/H, t)-sp.diff(metric, t)/H+sp.diff(H, t)*metric/H**2) == 0,
        independent_harmonic_shift_preserves_original_metric_momentum_mean=all(
            M(D(v)) == 0 for v in (px, py, pz)))


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    absolute = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    decode = lambda x: iv.mpf([mp.mpf(tuple(a)) for a in x])
    binary = lambda x: [list(a) for a in iv.mpf(x)._mpi_]
    norm = lambda xs: iv.sqrt(sum((absolute(x)**2 for x in xs), iv.mpf(0)))
    pins = read(MANIFEST)["source_sha256"]
    pins[WARD] = (ROOT/WARD).with_suffix(".json.sha256").read_text().split()[0]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix+".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    parents = [MIXED, WEAK, GAUGE, LIFT, COEFF, WARD]
    assert all(rel in pins for rel in parents)
    mixed, weak, gauge, lift, coeff, ward = [read(p) for p in parents]
    assert all(c["passed"] for r in (mixed, weak, gauge, lift, coeff, ward)
               for c in r["checks"])
    H = {tuple(row["ij"]): decode(row["value"])
         for row in mixed["full_mixed_Hessian_upper_triangle"]}
    Hz = {tuple(row["ij"]): decode(row["dz"])
          for row in mixed["full_mixed_Hessian_upper_triangle"]}
    hh = lambda i, j, entries=H: entries.get(tuple(sorted((i, j))), iv.mpf(0))
    Q = list(map(decode, lift["constants_binary"]["full_configuration_H1"]))
    P = list(map(decode, lift["constants_binary"]["full_momentum_L2"]))
    assert len(Q) == len(P) == 8
    Q.append(iv.mpf(0))
    P.append(iv.mpf(0))
    Z = [iv.mpf(i == 3) for i in range(9)]
    harmonic = [iv.mpf(i == 8) for i in range(9)]
    gauge_input = gauge["canonical_input_constants_binary"]
    velocity = list(map(decode, weak["coefficients_binary"]["field_rate_L2"]))
    assert hi(velocity[2]) == 0

    def compose(row):
        p, q, f, h = map(decode, row)
        assert hi(f) == 0
        return [p*pp+q*qq+h*hh for pp, qq, hh in zip(P, Q, harmonic)]

    v0 = [velocity[0]*pp+velocity[1]*qq for pp, qq in zip(P, Q)]
    shift = compose(gauge_input["corrective_shift_H1_original"])
    moduli = compose(gauge_input["physical_metric_modulus_rates"])
    corrected_v = [v+velocity[3]*s for v, s in zip(v0, shift)]
    pbg = list(map(decode, weak["background_binary"]["momentum"]))
    eta = []
    for j in (2, 4, 5):
        nq = norm(hh(j, i) for i in range(13))+norm(hh(j, i) for i in range(28, 41))
        nv = norm(hh(j, i) for i in range(14, 27))
        nz = absolute(hh(j, 13))+absolute(hh(j, 41, Hz))
        gauge_norm = 2*absolute(pbg[5])+(absolute(pbg[j]) if j != 5 else 0)
        eta.append([nq*q+nv*v+nz*z+gauge_norm*s
                    for q, v, z, s in zip(Q, v0, Z, shift)])
    Lscale = absolute(decode(coeff["H_interval"]))+iv.mpf(1)/31000
    scale = iv.exp(iv.mpf(2)/13000)/iv.sqrt(2)
    trace = [scale*(v+2*Lscale*q) for v, q in zip(corrected_v, Q)]
    checks = exact_controls()
    checks["auxiliary_velocity_absent_in_mean_rows"] = all(
        tuple(sorted((j, 27))) not in H for j in (2, 4, 5))
    checks["independent_harmonics_reach_shift_bound"] = hi(shift[-1]) > 0
    checks["finite_outward_bounds"] = all(
        lo(x) >= 0 and mp.isfinite(hi(x)) for row in (*eta, trace, shift, moduli) for x in row)
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(p), p.stat().st_mtime_ns) == value for p, value in snapshot.items())
    assert all(checks.values()), checks
    estimates = dict(eliminated_momentum_mean_x_rate=eta[0],
                     eliminated_momentum_mean_y_rate=eta[1],
                     eliminated_momentum_mean_z_rate=eta[2],
                     direct_trace_rate_L2=trace, corrective_shift_H1=shift,
                     metric_modulus_rate_vector=moduli)
    return dict(kind="RTAU_GAUGE_MEAN_TRACE_RATE_V1",
                source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
                manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                bounds_binary={k: [binary(x) for x in row] for k, row in estimates.items()},
                upper_per_sum={k: mp.nstr(max(hi(x) for x in row), 30)
                               for k, row in estimates.items()},
                scope="INITIAL_GAUGE_CLOSED_MEANS_AND_DIRECT_TRACE_RATE",
                differentiated_trace_inverse_comparison="OPEN",
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
        print("Initial dynamical mean and direct trace rate controls complete")


if __name__ == "__main__":
    main()
