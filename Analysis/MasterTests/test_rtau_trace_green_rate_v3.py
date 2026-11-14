"""Extend the corrected initial trace inverse and bound its rate responses."""

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
CONTRACT = GATE + "RES001_RTAU_TRACE_GREEN_RATE_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"
MOMENTUM = OUT + "rtau_moving_momentum_rate_v1_20261109/receipt.json"
LIFT = OUT + "rtau_strong_constraint_lift_v4_20261104/receipt.json"
INVERSE = OUT + "r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def exact_controls():
    z = sp.symbols("z", real=True)
    a2 = -2 + sp.sin(z)/3
    a1 = sp.cos(z)/7
    f = 2 + sp.cos(z) + sp.sin(2*z)
    D = lambda v: sp.diff(v, z)
    Kf = (1 + sp.sin(z))*f + 2*sp.integrate(f, (z, 0, 2*sp.pi))/(2*sp.pi)
    principal_source = a2*(D(D(f))-f)
    full_source = a2*D(D(f))+a1*D(f)+Kf
    m = 2 + sp.sin(z)
    v = 1 + sp.sin(2*z)
    direct_pairing = sp.integrate(m*D(f)*v, (z, 0, 2*sp.pi))
    dual_pairing = -sp.integrate(f*D(m*v), (z, 0, 2*sp.pi))
    k = sp.symbols("k", real=True)
    nonzero_mass = sp.Rational(17, 16)
    mean_mass = -sp.Rational(4951, 8400)
    return dict(
        nonconstant_principal_parametrix_residual=
            sp.simplify(full_source-principal_source-(a1*D(f)+Kf+a2*f)) == 0,
        actual_nonlocal_mean_retained=sp.simplify(Kf-(1+sp.sin(z))*f) == 4,
        longitudinal_source_dual_product_rule=sp.simplify(direct_pairing-dual_pairing) == 0,
        omitting_longitudinal_coefficient_derivative_rejected=
            sp.simplify(direct_pairing+sp.integrate(f*m*D(v), (z, 0, 2*sp.pi))) != 0,
        corrected_reference_nonzero_mode_smoothing=
            sp.simplify((k*k+nonzero_mass)-(1+k*k)) == sp.Rational(1, 16),
        corrected_reference_mean_invertible=mean_mass != 0)


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    absolute = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    decode = lambda x: iv.mpf([mp.mpf(tuple(a)) for a in x])
    rational = lambda x: iv.mpf(int(x.p))/int(x.q)
    binary = lambda x: [list(a) for a in iv.mpf(x)._mpi_]
    pins = read(MANIFEST)["source_sha256"]
    moving_path = ROOT/MOMENTUM
    pins[MOMENTUM] = moving_path.with_suffix(".json.sha256").read_text().split()[0]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT / rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix + ".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    lift, inverse, moving = [read(p) for p in (LIFT, INVERSE, MOMENTUM)]
    assert all(c["passed"] for r in (lift, inverse, moving) for c in r["checks"])
    assert len(lift["cells"]) == 16
    spec = importlib.util.spec_from_file_location("trace_green_factory", ROOT/FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = module.prepare()
    J, D = ctx["J"], ctx["D"]
    # The same first-differential evaluator as the corrected Sigma lift.
    # Spatial Taylor coefficients remain available without forming a Hessian.
    def first_mul(self, other):
        other = self.cast(other)
        zero = self.scalar(0)
        g = {i: self.g.get(i, zero)*other.c + other.g.get(i, zero)*self.c
             for i in self.g.keys() | other.g.keys()}
        return type(self)(self.c*other.c, {i: value for i, value in g.items() if value != 0})

    def first_unary(self, value, first, second):
        return type(self)(value, {i: first*g for i, g in self.g.items() if g != 0})

    D.__mul__ = first_mul
    D.__rmul__ = first_mul
    D.unary = first_unary
    grad, geometry, lie = ctx["gradient"], ctx["geometry"], ctx["lie"]
    b = rational(ctx["env"]["env"]["exact"]["b"])
    oldA = {k: decode(v) for k, v in inverse["whole_root_trace_coefficients"].items()}
    old_bounds = {k: decode(v) for k, v in inverse["bounds"].items()}
    pi_ref = -iv.mpf(11)*iv.sqrt(iv.mpf(3469)/4620)/10
    trace_lifts = (old_bounds["transverse_x"], old_bounds["transverse_y"],
                   absolute(pi_ref)+old_bounds["longitudinal_difference"])
    checks = exact_controls()
    cells = []
    for record in lift["cells"]:
        spatial = decode(record["z"])
        y, _ = ctx["state"](J.variable(spatial), True, [0, 0, 0])
        L = ctx["evaluate"](y)
        assert not L.h
        q, v, g, S, Sz = y[:14], y[14:28], y[28:42], y[42:45], y[45:48]
        p = [grad(L, 14+i) for i in range(14)]
        a2 = q[0]
        a = a2**mp.mpf(".5")
        az = J(coefficients=[a2.c[1], 2*a2.c[2], iv.mpf(0)])
        N, mu, gamma, H, _ = geometry(q, g)
        material = [x-y for x, y in zip(v, lie(q, g, S, Sz))]

        def trace_flux(dq, dg):
            Q = [D(x, {0: dv}) for x, dv in zip(q, dq)]
            G = [D(x, {0: dv}) for x, dv in zip(g, dg)]
            n, volume, frame, hinv, curvature_flux = geometry(Q, G)
            F = (sum((n*frame*hinv[i][2]*D(p[6+i]) for i in range(3)), D(0))
                 -n*curvature_flux/2-n*volume*Q[13]*hinv[2][2]*G[12]*b)
            return F.g.get(0, J(0))

        zero = [J(0)]*14
        qtrace, dtrace = zero.copy(), zero.copy()
        for i in (0, 3):
            qtrace[i], dtrace[i] = a2, az
        U0 = trace_flux(qtrace, dtrace)
        U1 = trace_flux(zero, qtrace)
        V1 = a2*(grad(L, 28)+grad(L, 31)+(p[0]+p[3])*S[2])
        c1 = -(N*mu*q[13]*H[2][2]*g[12])*b
        a1 = V1.c[0]-U0.c[0]-U1.c[1]+c1.c[0]
        a1_z = V1.c[1]-U0.c[1]-2*U1.c[2]+c1.c[1]
        old_a1 = oldA["A1"] + decode(record["trace_correction_1"])
        checks[f"A1_value_matches_pinned_enclosure_cell_{record['cell']}"] = (
            lo(a1) <= hi(old_a1) and lo(old_a1) <= hi(a1))
        checks[f"compensated_c1_matches_cell_{record['cell']}"] = (
            lo(c1.c[0]) <= hi(decode(record["trace_correction_1"]))
            and lo(decode(record["trace_correction_1"])) <= hi(c1.c[0]))
        Kbound = absolute(oldA["A0"]+decode(record["trace_correction_0"]))
        Kbound += sum((absolute(material[i].c[0])*T
                       for i, T in zip((2, 4, 5), trace_lifts)), iv.mpf(0))
        reciprocal = 1/(N*a)
        E = absolute(reciprocal.c[0])+2*absolute(reciprocal.c[1])+2*absolute(reciprocal.c[2])
        lower = absolute(a1)+absolute(a1_z)+Kbound+absolute((N*a).c[0])
        C = N*gamma/a2
        source = material[5]*(g[12]*N*mu*H[2][2]/(2*a2))*b
        cells.append(dict(E=E, lower=lower, C=absolute(C.c[0])+absolute(C.c[1]),
                          longitudinal=absolute(source.c[0])+absolute(source.c[1])))
    maximum = lambda key: iv.mpf(max(hi(c[key]) for c in cells))
    G1 = iv.mpf(max(hi(decode(r["Green_bound"])) for r in lift["cells"]))
    G2 = maximum("E")*(1+G1*maximum("lower"))
    longitudinal = G1*maximum("longitudinal")
    frame = G2*maximum("C")
    # Integrate the normalized trace equation with the original primitive.
    # P:H^-1 -> L2 has norm sqrt(2), bounded above here by 2.
    gradient_remainder = maximum("E")*(3*maximum("C")+2*maximum("lower")*frame)
    estimates = dict(G_Hminus1_to_H1=G1, E_Hminus2_to_L2=maximum("E"),
                     L_minus_principal_L2_to_Hminus1=maximum("lower"),
                     G_Hminus2_to_L2=G2,
                     longitudinal_trace_H1_per_zeta_L2=longitudinal,
                     frame_trace_L2_per_frame_rate_Hminus1=frame,
                     frame_trace_gradient_remainder_L2_per_frame_rate_Hminus1=gradient_remainder)
    checks["finite_positive_whole_circle_bounds"] = all(
        lo(value) > 0 and mp.isfinite(hi(value)) for value in estimates.values())
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(path), path.stat().st_mtime_ns) == value
        for path, value in snapshot.items())
    assert all(checks.values()), checks
    return dict(kind="RTAU_TRACE_GREEN_RATE_V3",
                source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
                manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                bounds_binary={k: binary(v) for k, v in estimates.items()},
                upper_display={k: mp.nstr(hi(v), 30) for k, v in estimates.items()},
                scope="INITIAL_PROJECTED_TRACE_INVERSE_AND_TWO_RATE_COMPONENTS",
                moving_trace_operator_and_charge_gauge_rates="OPEN",
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
        print("Corrected trace Green rate controls complete")


if __name__ == "__main__":
    main()
