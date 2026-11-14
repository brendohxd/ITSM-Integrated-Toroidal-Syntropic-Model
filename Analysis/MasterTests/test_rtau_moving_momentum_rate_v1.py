"""Check the actual initial moving momentum lift and its force derivative."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
GATE = "Theory/Gates/RES-001/"
MANIFEST = GATE + "RES001_RTAU_DENSITY_OPERATOR_COMPARISON_V1_PREPARATION_INPUTS_2026-11-05.json"
CONTRACT = GATE + "RES001_RTAU_MOVING_MOMENTUM_RATE_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def periodic_controls():
    t, z = sp.symbols("t z", real=True)
    average = lambda f: sp.integrate(sp.expand(f), (z, 0, 2*sp.pi))/(2*sp.pi)
    u = 2 + (1+t)*sp.cos(z)
    ell = 1 + t*sp.cos(z)
    free = (1+t)*sp.cos(z)
    x = sp.cos(2*z) + (1+t)*sp.cos(z)
    eta = 1 + 2*t
    den = average(u)
    C = (eta-average(ell*free+u*x))/den
    reconstructed = ell*free + u*(x+C)
    relative = reconstructed.diff(t)-ell*free.diff(t)
    shape = u.diff(t)*(x+C)
    projected = u*x.diff(t)-u*average(u*x.diff(t))/den
    want = (ell.diff(t)*free + projected + shape - u*average(shape)/den
            + u*(eta.diff(t)-average((ell*free).diff(t)))/den)
    checks = dict(
        differentiated_reconstruction=sp.simplify(relative-want) == 0,
        actual_mean_rate_restored=sp.simplify(average(reconstructed.diff(t))-eta.diff(t)) == 0,
        omitting_moving_normalization_rejected=average(shape).subs(t, 0) != 0,
        omitting_prescribed_mean_rate_rejected=average(u*eta.diff(t)/den) == 2)
    # The independent Fourier convolution uses c=cos z and a single
    # input mode zeta_n. Compare it with the product-rule expansion.
    n = sp.symbols("n", integer=True, positive=True)
    actual = sp.Matrix([-n**2/(2*sp.I*(n-1)), -n**2/(2*sp.I*(n+1))])
    first = sp.Matrix([sp.I*n/2, sp.I*n/2])
    second = sp.Matrix([sp.I/2, -sp.I/2])
    last = sp.Matrix([-1/(2*sp.I*(n-1)), -1/(2*sp.I*(n+1))])
    checks["primitive_removes_exactly_one_force_derivative"] = (
        (actual-first-second-last).applyfunc(sp.simplify).is_zero_matrix)
    checks["first_order_term_survives"] = sp.limit(actual[1]/n, n, sp.oo) == sp.I/2
    # For the n=1 test the product has a mean and a second harmonic.
    # Evaluate the exact primitive of cos(z) D^2 cos(z) = -cos(z)^2.
    d = lambda f: sp.diff(f, z)
    primitive_at_one = -sp.sin(2*z)/4
    c, f = sp.cos(z), sp.cos(z)
    product = d(d(c))*f
    primitive_product = -sp.sin(2*z)/4
    expanded = c*d(f)-d(c)*f+2*average(d(c)*f)+primitive_product
    checks["zero_mode_identity"] = (
        sp.simplify(d(primitive_product)-product+average(product)) == 0
        and average(primitive_product) == 0
        and sp.simplify(primitive_at_one-expanded) == 0)
    # A distinct sine input gives a nonzero derivative-weighted mean.
    f = sp.sin(z)
    checks["weighted_mean_term_can_be_nonzero"] = 2*average(d(c)*f) == -1
    return checks


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    pins = json.loads((ROOT/MANIFEST).read_bytes())["source_sha256"]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix+".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    spec = importlib.util.spec_from_file_location("moving_momentum_factory", ROOT/FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = module.prepare()
    J = ctx["J"]
    par = ctx["env"]["env"]["exact"]["b"]
    b = iv.mpf(int(par.p))/int(par.q)
    cells = []
    for low, high in (("0.29", "0.31"), ("1.09", "1.11"), ("2.39", "2.41")):
        y, _ = ctx["state"](J.variable(iv.mpf([low, high])), True, [0, 0, 0])
        lapse, volume, *_ = ctx["geometry"](y[:14], y[28:42])
        kappa = 1/y[0].c[0]
        s = y[40].c[0]
        d = b*lapse.c[0]*volume.c[0]*kappa
        coefficient = kappa*s*d/2
        cells.append(dict(cell=[low, high], coefficient=[mp.nstr(lo(coefficient), 28),
                                                       mp.nstr(hi(coefficient), 28)],
                          excludes_zero=bool(lo(coefficient) > 0 or hi(coefficient) < 0)))
    checks = periodic_controls()
    checks["prepared_longitudinal_force_coefficient_nonzero_on_a_cell"] = any(
        c["excludes_zero"] for c in cells)
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(p), p.stat().st_mtime_ns) == value for p, value in snapshot.items())
    assert all(checks.values()), checks
    return dict(
        kind="RTAU_MOVING_MOMENTUM_RATE_V1",
        source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
        manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
        checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
        longitudinal_force_rate_term="u_L * psi_z * d * D_z(zeta)",
        coefficient_cells=cells,
        compatible_domain_scope="PREPARED_INITIAL_SLICE",
        full_reconstruction_rate="TRACE_CHARGE_GAUGE_RATE_OPEN",
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
        print("Moving momentum rate controls complete")


if __name__ == "__main__":
    main()
