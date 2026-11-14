"""Initial R-tau corrected-density row and physical-density coefficient drift."""

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
CONTRACT = GATE + "RES001_RTAU_DENSITY_OPERATOR_DRIFT_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def load_factory():
    spec = importlib.util.spec_from_file_location("density_drift_factory", ROOT / FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prepare()


def exact_controls():
    t, z = sp.symbols("t z", real=True)
    u, v = sp.Matrix([1, t]), sp.Matrix([1, 2*t])
    L = u * v.T
    G = v * u.T / ((u.T*u)[0] * (v.T*v)[0])
    P, Q = G*L, L*G
    naive = -G * L.diff(t) * G
    exact = naive + G*Q.diff(t) + P.diff(t)*G
    density = sp.Matrix([[1, 0, 0]])
    cross = sp.Matrix([[0, 0, 0], [0, 0, t+1], [0, 2-t, 0]])
    # Primitive commutator on a zero-mean test input: D^-1 P0 acts on
    # the differentiated product with its mean removed in the original chart.
    shift, momentum = 1 + sp.cos(z), sp.cos(z)
    mean = lambda f: sp.integrate(f, (z, 0, 2*sp.pi)) / (2*sp.pi)
    commutator = mean(shift*momentum) - shift*mean(momentum)
    a, b = sp.Function("a")(t), sp.Function("b")(t)
    return {
        "moving_inverse_product_rule": (G.diff(t)-exact).applyfunc(sp.simplify).is_zero_matrix,
        "naive_moving_inverse_fails_on_compatible_source":
            (G.diff(t)*u - naive*u).subs(t, 0) == sp.Matrix([0, 2]),
        "compatible_source_range_motion_retained":
            ((sp.eye(2)-Q)*u.diff(t)-Q.diff(t)*u).applyfunc(sp.simplify).is_zero_matrix,
        "periodic_normal_form_density_row_unchanged": (density*cross).is_zero_matrix,
        "primitive_mean_term_can_be_nonzero": commutator == sp.Rational(1, 2),
        "observable_coefficient_drift_required": (a*b).diff(t)-a*b.diff(t) == a.diff(t)*b,
    }


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    absolute = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    decode = lambda x: iv.mpf([mp.mpf(tuple(a)) for a in x])
    bound = lambda x: mp.nstr(hi(absolute(x)), 34)
    rational = lambda x: iv.mpf(int(x.p))/int(x.q)
    pins = read(MANIFEST)["source_sha256"]
    snap = {}
    for rel, expected in pins.items():
        path = ROOT / rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix + ".sha256")):
            if item.exists():
                snap[item] = (digest(item), item.stat().st_mtime_ns)
    checks = exact_controls()
    v1 = read(OUT + "rtau_strong_density_normal_form_v1_20261103/receipt.json")
    v2 = read(OUT + "rtau_strong_density_normal_form_v2_20261103/receipt.json")
    actual = read(OUT + "rtau_actual_corrected_density_v4_20261105/receipt.json")
    force = read(OUT + "rtau_actual_force_pair_v2_20261105/receipt.json")
    momentum = read(OUT + "rtau_momentum_rate_lift_v2_20261104/receipt.json")
    inverse = read(OUT + "rtau_strong_force_coordinate_v3_20261104/receipt.json")
    for result in (v1, v2, actual, force, momentum, inverse):
        assert all(c["passed"] for c in result["checks"])
    ctx = load_factory()
    J, D = ctx["J"], ctx["D"]
    y, _ = ctx["state"](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    q, vel, grad = y[:14], y[14:28], y[28:42]

    def first_jet(x, dx):
        return J(coefficients=[x, dx, iv.mpf(0)])

    qtime = [first_jet(x.c[0], v.c[0]) for x, v in zip(q, vel)]
    Q = [D.var(x, i) for i, x in enumerate(qtime)]
    _, mu, gamma, hinv, _ = ctx["geometry"](Q, [J(0)]*14)
    lapse = ctx["geometry"](q, grad)[0]
    p = (vel[12]-y[44]*grad[12])/lapse
    p_rate = hi(absolute(decode(v2["bounds_binary"]["normal_p_time"])))
    pn = first_jet(p.c[0], iv.mpf([-p_rate, p_rate]))
    sn = first_jet(grad[12].c[0], vel[12].c[1])
    pd, sd = D.var(pn, 100), D.var(sn, 101)
    h = [[Q[0], Q[1], Q[2]], [Q[1], Q[3], Q[4]], [Q[2], Q[4], Q[5]]]
    rest = [hinv[i][2]*sd + Q[6+i]*(pd+Q[8]*sd/(gamma+1)) for i in range(3)]
    Y = sum((h[i][j]*rest[i]*rest[j] for i in range(3) for j in range(3)), D(0))
    positive_Y = decode(force["coefficient_controls_binary"]["positive_Y"])
    assert lo(positive_Y) > 0
    root = first_jet(positive_Y, Y.c.c[1])**mp.mpf("0.5")
    U = gamma*pd + Q[8]*sd
    pars = ctx["env"]["env"]["exact"]
    KQ, A, b = [rational(pars[k]) for k in ("K_Q", "A", "b")]
    first = lambda i: U.c*U.g.get(i, J(0))*KQ-root*Y.g.get(i, J(0))*(3*A)/2
    fps = ((U.g[100]*U.g[101]+U.c*U.h.get((100, 101), J(0)))*KQ
           -(root*Y.h.get((100, 101), J(0))+Y.g[100]*Y.g[101]/(root*2))*(3*A)/2)
    volume = [(first(i)+pn*first(100)*mu.g.get(i, J(0))/mu.c).c[1]
              for i in range(13)]
    volume_rate = iv.sqrt(sum((absolute(x)**2 for x in volume), iv.mpf(0)))
    momentum_rate = absolute((pn/mu.c).c[1])
    gradient_rate = absolute((pn*fps).c[1])
    # The registered metric first jet is conformal. No future conformality
    # is required for this differentiation on the initial slice.
    Lconf = vel[0]/(2*q[0])
    lam_z = grad[0]/(2*q[0])
    kappa = 1/q[0].c[0]
    Zt = 2*Lconf.c[0]*q[13].c[0] - kappa*(
        2*vel[12].c[2] + lam_z.c[0]*vel[12].c[1] + Lconf.c[1]*grad[12].c[0])
    zeta_rate = absolute(b*Zt)
    primitive_rate = absolute(decode(v1["bounds_binary"]["coefficient_time"]))
    qlift = map(decode, momentum["constants_binary"]["full_configuration_H1"])
    plift = map(decode, momentum["constants_binary"]["full_momentum_L2"])
    flift = map(decode, inverse["constants_binary"]["force_H2_inverse"])
    coefficients = [(primitive_rate+momentum_rate)*pl + gradient_rate*fl + volume_rate*ql
                    for ql, pl, fl in zip(qlift, plift, flift)]
    assert len(coefficients) == 8
    coefficients[3] += zeta_rate
    checks["finite_whole_root_coefficient_drift"] = all(
        mp.isfinite(hi(x)) and lo(x) >= 0 for x in coefficients)
    checks["initial_material_density_source_reused"] = (
        len(actual["upper_display"]["initial_original_coordinate_density_source_L2"]) == 9)
    checks["all_pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(path), path.stat().st_mtime_ns) == value for path, value in snap.items())
    assert all(checks.values()), checks
    return dict(
        kind="RTAU_INITIAL_DENSITY_OPERATOR_DRIFT_V2",
        physics_pass=False, gate_effect="NONE", review_status="DEFERRED",
        Rtau_adopted=False, G1_G6="INCOMPLETE",
        source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
        pinned_manifest_sha256=digest(ROOT/MANIFEST), pinned_files=len(pins),
        checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
        density_principal_material_row="ZERO_ON_REGISTERED_COMPATIBLE_NORM",
        material_source_coefficients=actual["upper_display"]["initial_original_coordinate_density_source_L2"],
        observable_coefficient_drift=dict(primitive=bound(primitive_rate),
                                        momentum=bound(momentum_rate), gradient=bound(gradient_rate),
                                        field=bound(volume_rate), auxiliary=bound(zeta_rate)),
        drift_input_coefficients=[bound(x) for x in coefficients],
        moving_reconstruction_rate="OPEN", actual_time_tube="NOT_ESTABLISHED")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--replay", type=Path)
    args = parser.parse_args()
    payload = (json.dumps(calculate(), indent=2, allow_nan=False) + "\n").encode()
    if args.replay:
        assert args.replay.read_bytes() == payload
        print("Byte-identical read-only replay")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open("xb") as stream:
            stream.write(payload)
        print("Initial density drift calculation complete")


if __name__ == "__main__":
    main()
