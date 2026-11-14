"""Verify the prepared physical-density rate projection and derivative order."""

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
CONTRACT = GATE + "RES001_RTAU_PHYSICAL_DENSITY_RATE_V1_CONTRACT_2026-11-09.md"
FACTORY = "Analysis/MasterTests/r4c1_canonical_density_factory_v1.py"
DRIFT = OUT + "rtau_density_operator_drift_v2_20261109/receipt.json"
TRACE = OUT + "rtau_trace_green_rate_v3_20261109/receipt.json"
FORCE = OUT + "rtau_actual_force_pair_v2_20261105/receipt.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((ROOT / rel).read_bytes())


def fourier_controls():
    x, t = sp.symbols("x t")

    def modes(expr):
        return [(term.as_powers_dict().get(x, 0), term)
                for term in sp.Add.make_args(sp.expand(expr))]

    def D(expr):
        return sp.expand(sum(sp.I*n*term for n, term in modes(expr)))

    def mean(expr):
        return sum(term for n, term in modes(expr) if n == 0)

    def P(expr):
        return sp.expand(sum(term/(sp.I*n) for n, term in modes(expr) if n))

    S, c, a, h, j, B, d, r, v, b0, k, g, J, K = [
        (i+2) + x/(i+3) + 1/(x*(i+4)) + t*x**2/(i+5) for i in range(14)]
    xi, zeta, chi, q, Y, w, gauge, Rw, Rx, Rz = [
        i + x**2/(i+2) + x**-3/(i+3) for i in range(1, 11)]
    # Specify material rows first, then construct actual time rates.
    Mxi = d*D(D(zeta)) + r*D(zeta) - v*D(xi) + Rx
    Mzeta = -k*b0*D(D(xi)) - g*D(xi) - v*D(zeta) + J*D(Y) + Rz
    Mchi = b0*xi-v*D(chi)+K*q+gauge
    Mq = 1+x**4
    rho = w+c*P(xi)-a*xi-h*D(chi)+B*q-j*zeta
    rho_t = (S*D(w)+Rw + c.diff(t)*P(xi) + c*P(S*D(xi)+Mxi)
             -a.diff(t)*xi-a*(S*D(xi)+Mxi)
             -h.diff(t)*D(chi)-h*D(S*D(chi)+Mchi)
             +B.diff(t)*q+B*(S*D(q)+Mq)-j.diff(t)*zeta-j*(S*D(zeta)+Mzeta))
    independent = sp.expand((rho_t-S*D(rho)).subs(t, 0))
    coeff_drift = sum((b.diff(t)-S*D(b))*value
                      for b, value in ((c, P(xi)), (-a, xi), (-h, D(chi)),
                                       (B, q), (-j, zeta)))
    shift_mean = S*mean(xi)-mean(S*xi)-P(D(S)*xi)
    force_mean = 2*mean(D(d)*zeta)-mean(r*zeta)+mean(v*xi)
    primitive_lower = (-D(d)*zeta+P(D(D(d))*zeta)+r*zeta-P(D(r)*zeta)
                       -v*xi+P(D(v)*xi)+P(Rx)+force_mean)
    principal = (j*k*b0*D(D(xi))-a*d*D(D(zeta))
                 +(a*v+j*g-h*b0)*D(xi)+(c*d-a*r+j*v)*D(zeta)-j*J*D(Y))
    clock_lower = D(b0)*xi-v*D(D(chi))+(D(S)-D(v))*D(chi)+D(K*q+gauge)
    remainder = (Rw+coeff_drift+c*(shift_mean+primitive_lower)
                 -a*Rx-j*Rz-h*clock_lower+B*Mq)
    at_slice = lambda expr: sp.expand(expr.subs(t, 0))
    return dict(
        direct_physical_rate_equals_explicit_rows=independent == at_slice(principal+remainder),
        zero_material_row_for_physical_density_rejected=at_slice(principal) != 0,
        omitted_reverse_ordinary_force_coupling_rejected=at_slice(j*J*D(Y)) != 0,
        omitted_original_primitive_means_rejected=at_slice(c*force_mean) != 0,
        omitted_clock_gauge_derivative_rejected=at_slice(h*D(gauge)) != 0,
        omitted_coefficient_drift_rejected=at_slice(coeff_drift) != 0,
        omitted_clock_shift_commutator_rejected=at_slice(h*D(S)*D(chi)) != 0)


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    pins = read(MANIFEST)["source_sha256"]
    for rel in (DRIFT, TRACE):
        path = ROOT / rel
        pins[rel] = path.with_suffix(".json.sha256").read_text().split()[0]
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT / rel
        assert digest(path) == expected, rel
        for item in (path, path.with_suffix(path.suffix + ".sha256")):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    for rel in (DRIFT, TRACE, FORCE):
        assert all(c["passed"] for c in read(rel)["checks"]), rel
    spec = importlib.util.spec_from_file_location("physical_rate_factory", ROOT / FACTORY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = module.prepare()
    J = ctx["J"]
    par = ctx["env"]["env"]["exact"]["b"]
    b = iv.mpf(int(par.p))/int(par.q)
    cells = []
    for low, high in (("0.29", "0.31"), ("1.09", "1.11"), ("2.39", "2.41")):
        y, _ = ctx["state"](J.variable(iv.mpf([low, high])), True, [0, 0, 0])
        N = ctx["geometry"](y[:14], y[28:42])[0].c[0]
        p = (y[26].c[0]-y[44].c[0]*y[40].c[0])/N
        minus_ad = -b*N*p/y[0].c[0]
        cells.append(dict(cell=[low, high],
                          interval_binary=[list(x) for x in minus_ad._mpi_],
                          interval_display=[mp.nstr(lo(minus_ad), 24), mp.nstr(hi(minus_ad), 24)],
                          excludes_zero=bool(lo(minus_ad) > 0 or hi(minus_ad) < 0)))
    checks = fourier_controls()
    checks["prepared_second_order_coefficient_excludes_zero"] = any(
        c["excludes_zero"] for c in cells)
    checks["pinned_bytes_sidecars_and_timestamps_preserved"] = all(
        (digest(path), path.stat().st_mtime_ns) == value
        for path, value in snapshot.items())
    assert all(checks.values()), checks
    return dict(kind="RTAU_PHYSICAL_DENSITY_RATE_V1",
                source_sha256=digest(Path(__file__)), contract_sha256=digest(ROOT/CONTRACT),
                manifest_sha256=digest(ROOT/MANIFEST), pinned_sources=len(pins),
                checks=[dict(name=k, passed=bool(v)) for k, v in checks.items()],
                second_order_projection="b*Z*kappa*aphi*D^2(xi)-(p/mu)*d*D^2(zeta)",
                minus_p_d_over_mu=cells,
                scope="INITIAL_OBSERVABLE_RATE_ON_COMPATIBLE_DATA",
                moving_range_and_charge_transport="OPEN",
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
        print("Physical density rate controls complete")


if __name__ == "__main__":
    main()
