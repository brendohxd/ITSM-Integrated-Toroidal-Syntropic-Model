"""Generic planar WWR and fourth-order ray functional, NOT a physical amplitude.

Recompute from the unchanged covariant action, with all 22 independent response
fields. No old main, ODE integration, response inverse or provider is invoked.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = BASE + "r4c1_three_family_odd_tail_attempt_01/"
LEGACY = BASE + "r4c1_g3n4_attempt_01/formulas.json"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_PLANAR_COUPLED_VERTICES_V1_CONTRACT_2026-10-12.md"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
PINNED = {
    CONTRACT: "8238acc979693a2a24c3a8445ba31b449c97277ece23de3cb785cf6206ecc423",
    HELPER: "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224",
    LEGACY: "1dee96271de67aec5336ac84753c18728a65e130e05c1c7731559c5a6a49727a",
    PARENT + "summary.json": "e4370b6e11294207039397de217a3a9e6f04488d669cb6eb76182378fbab92f2",
    "Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_ODD_TAIL_V1_REPORT_2026-10-12.md":
        "c15bdc185eba841c2d9cf0c8b65577d51681d9121ff0ace317db11a3e1570ffc",
    "Theory/Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_REPORT_2026-10-08.md":
        "035d1480904b2459b6a4e8b6df91d381065a653fdeb49583fcdb3dbfc4ac49f4",
}
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != PINNED[HELPER]:
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
AXES = (0, 1, 3)
AXIS_LABEL = {0: "t", 1: "x", 3: "z"}
KEYS = tuple((i, 0) for i in range(5)) + tuple((i, 1) for i in range(3))
PROGRESS = None


def note(message):
    print(message, flush=True)
    if PROGRESS is not None:
        with PROGRESS.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"step": message}) + "\n")


def tidy(expr):
    return s.factor(s.cancel(s.expand(expr)))


class Jet:
    """Exact ring Q[symbols,e,d]/(e^5,d^2,e^3*d), not an analytic cusp expansion."""
    def __init__(self, value=0):
        if isinstance(value, Jet):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {k: s.sympify(v) for k, v in value.items() if v != 0 and k in KEYS}
        else:
            self.c = {(0, 0): s.sympify(value)} if value != 0 else {}

    def __add__(self, other):
        out = self.c.copy()
        for k, v in Jet(other).c.items():
            out[k] = out.get(k, 0) + v
        return Jet(out)

    __radd__ = __add__

    def __neg__(self):
        return Jet({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + -Jet(other)

    def __rsub__(self, other):
        return Jet(other) + -self

    def __mul__(self, other):
        out = {}
        for (i, j), v in self.c.items():
            for (ii, jj), vv in Jet(other).c.items():
                key = (i + ii, j + jj)
                if key in KEYS:
                    out[key] = out.get(key, 0) + v * vv
        return Jet(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Jet):
            raise TypeError("Jet inverses must be explicit")
        return Jet({k: v / s.sympify(other) for k, v in self.c.items()})

    def clean(self):
        return Jet({k: s.expand(v) for k, v in self.c.items()})

    def coeff(self, i, j):
        return self.c.get((i, j), s.Integer(0))


def zeros(n):
    return [[Jet() for _ in range(n)] for _ in range(n)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))).clean()
             for j in range(len(B[0]))] for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def scalar(v, A, w):
    return sum(v[i] * A[i][j] * w[j] for i in range(len(v)) for j in range(len(w))).clean()


def exact(checks, name, expr):
    xs = list(expr) if isinstance(expr, (list, tuple)) else [expr]
    rs = [tidy(x) for x in xs]
    ok = all(x == 0 for x in rs)
    checks.add(name, ok, "zero_exact" if ok else list(map(str, rs)), "zero_exact")


def derive(checks):
    a = s.Symbol("a", positive=True)
    names = ("H Hdot Hddot psi_dot psi_ddot psi_dddot MP2 MU2 K_Q b zeta beta C "
             "epsilon0 lambda0 c1 c2 c3 c4 u0 v0 r0 u_dot v_dot r_dot u_ddot "
             "v_ddot r_ddot C_dot epsilon_dot lambda_dot m2 lambda4 lambda6 "
             "Lambda mr2 lambda_r g_r rho_Lambda A")
    sy = {str(q): q for q in s.symbols(names, real=True)}
    sy["a"] = a
    R = {n: s.Symbol(n, real=True) for n in FIELDS}
    Rj = {ax: {n: s.Symbol(n + "_" + AXIS_LABEL[ax], real=True) for n in FIELDS}
          for ax in AXES}
    waves = {}
    for name in ("W", "B"):
        table = {(): s.Symbol(name, real=True)}
        for degree in (1, 2, 3):
            for multi in itertools.combinations_with_replacement(AXES, degree):
                table[multi] = s.Symbol(name + "_" + "".join(AXIS_LABEL[i] for i in multi), real=True)
        waves[name] = table
        sy.update({str(q): q for q in table.values()})
    maps = {ax: {} for ax in AXES}
    maps[0].update({a: a * sy["H"], sy["H"]: sy["Hdot"], sy["Hdot"]: sy["Hddot"],
                    sy["psi_dot"]: sy["psi_ddot"], sy["psi_ddot"]: sy["psi_dddot"],
                    sy["C"]: sy["C_dot"], sy["epsilon0"]: sy["epsilon_dot"],
                    sy["lambda0"]: sy["lambda_dot"]})
    for n in ("u", "v", "r"):
        maps[0][sy[n + "0"]] = sy[n + "_dot"]
        maps[0][sy[n + "_dot"]] = sy[n + "_ddot"]
    for ax in AXES:
        for table in waves.values():
            for multi, q in table.items():
                if len(multi) < 3:
                    maps[ax][q] = table[tuple(sorted(multi + (ax,)))]
        maps[ax].update({R[n]: Rj[ax][n] for n in FIELDS})

    def deriv(expr, ax):
        return s.expand(sum(s.diff(expr, q) * value for q, value in maps[ax].items()
                            if q in expr.free_symbols))

    def djet(obj, ax):
        return Jet({k: deriv(v, ax) for k, v in obj.c.items()}).clean() if ax in AXES else Jet()

    def q(name):
        return sy[name]

    W, B = waves["W"][()], waves["B"][()]
    Wt, Wx, Wz = (waves["W"][(i,)] for i in AXES)
    Bt, Bx, Bz = (waves["B"][(i,)] for i in AXES)
    H, p = q("H"), q("psi_dot")
    e, d = Jet({(1, 0): 1}), Jet({(0, 1): 1})
    N, invN, invN2 = 1 + d * R["alpha"], 1 - d * R["alpha"], 1 - 2 * d * R["alpha"]
    mi = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
    h = [[a * a * (int(i == j) + d * R[mi[i][j]]) for j in range(3)] for i in range(3)]
    hi = [[(int(i == j) - d * R[mi[i][j]]) / (a * a) for j in range(3)] for i in range(3)]
    shift = [(e * B * int(i == 1) + d * R[n]) / a for i, n in enumerate(("Sx", "Sy", "Sz"))]
    velocity = [(e * W * int(i == 1) + d * R[n]) / a for i, n in enumerate(("Vx", "Vy", "Vz"))]
    v2 = scalar(velocity, h, velocity)
    gam = (1 + v2 / 2 - v2 * v2 / 8).clean()
    normal = [(gam * invN).clean()] + [(velocity[i] - shift[i] * gam * invN).clean() for i in range(3)]
    frame = [((1 + d * R["nu"]) * value).clean() for value in normal]
    g, gi = zeros(4), zeros(4)
    g[0][0] = (-N * N + scalar(shift, h, shift)).clean()
    gi[0][0] = -invN2
    for i in range(3):
        g[0][i + 1] = g[i + 1][0] = sum(h[i][j] * shift[j] for j in range(3)).clean()
        gi[0][i + 1] = gi[i + 1][0] = (shift[i] * invN2).clean()
        for j in range(3):
            g[i + 1][j + 1] = h[i][j]
            gi[i + 1][j + 1] = (hi[i][j] - shift[i] * shift[j] * invN2).clean()
    prod = mm(g, gi)
    exact(checks, "planar_ADM_inverse_all_ring_coefficients", [prod[i][j].coeff(ii, jj)
          - int(i == j and ii == jj == 0) for i in range(4) for j in range(4) for ii, jj in KEYS])
    norm = scalar(normal, g, normal) + 1
    exact(checks, "normalized_n_all_ring_coefficients", [norm.coeff(i, j) for i, j in KEYS])
    off = scalar(frame, g, frame) + 1 + 2 * d * R["nu"]
    exact(checks, "independent_normal_U_variation_retained", [off.coeff(i, j) for i, j in KEYS])
    note("Building planar metric/frame connection from the generic action")
    Gamma = [[[sum(gi[c][j] * (djet(g[j][bb], aa) + djet(g[j][aa], bb)
                      - djet(g[aa][bb], j)) for j in range(4)).clean() / 2
               for bb in range(4)] for aa in range(4)] for c in range(4)]

    def nabla(vec):
        return [[(djet(vec[nu], mu) + sum(Gamma[nu][mu][j] * vec[j] for j in range(4))).clean()
                 for nu in range(4)] for mu in range(4)]

    DN, DU = nabla(normal), nabla(frame)
    accN = [sum(normal[j] * DN[j][i] for j in range(4)).clean() for i in range(4)]
    accU = [sum(frame[j] * DU[j][i] for j in range(4)).clean() for i in range(4)]
    I1 = sum(gi[i][j] * g[k][l] * DU[i][k] * DU[j][l] for i in range(4)
             for j in range(4) for k in range(4) for l in range(4)).clean()
    I2, I3, I4 = trace(DU) * trace(DU), trace(mm(DU, DU)), scalar(accU, g, accU)
    frameL = (-q("MU2") * (q("c1") * I1 + q("c2") * I2 + q("c3") * I3 - q("c4") * I4) / 2).clean()
    hp = [[(gi[i][j] + normal[i] * normal[j]).clean() for j in range(4)] for i in range(4)]
    volum = 1 + d * (R["alpha"] + (R["Mxx"] + R["Myy"] + R["Mzz"]) / 2)

    def grad(n, bg):
        return [bg + d * Rj[0][n], d * Rj[1][n], Jet(), d * Rj[3][n]]

    gradPsi, gradZ = grad("Pi", p), grad("Z", 0)
    Qu = sum(normal[i] * gradPsi[i] for i in range(4)).clean()
    Y = scalar(gradPsi, hp, gradPsi)
    forceTemporal = q("K_Q") * Qu * Qu / 2
    reg = (q("b") * d * d * R["Z"] * R["Z"] / 2 - q("b") * scalar(gradZ, hp, gradPsi)
           - q("b") * d * R["Z"] * sum(accN[i] * gradPsi[i] for i in range(4))).clean()
    uu, vv, rr = q("u0") + d * R["du"], q("v0") + d * R["dv"], q("r0") + d * R["dr"]
    gu, gv, gr = grad("du", q("u_dot")), grad("dv", q("v_dot")), grad("dr", q("r_dot"))
    current = [(vv * gu[i] - uu * gv[i]).clean() for i in range(4)]
    align = (-q("zeta") * scalar(current, hp, current) / 2).clean()
    ss = uu * uu + vv * vv
    pot = (q("m2") * ss / 2 + q("lambda4") * ss * ss / 8
           + q("lambda6") * ss * ss * ss / (24 * q("Lambda")**2) + q("mr2") * rr * rr / 2
           + q("lambda_r") * rr * rr * rr * rr / 4 + q("g_r") * ss * rr * rr / 4 + q("rho_Lambda"))
    canonical = (-scalar(gu, gi, gu) / 2 - scalar(gv, gi, gv) / 2 - scalar(gr, gi, gr) / 2 - pot).clean()
    taugrad = grad("T", q("C"))
    matter = -(q("epsilon0") + d * R["Em"]) * (
        q("C")**2 * (1 + 2 * d * q("beta") * R["Pi"]) * scalar(taugrad, gi, taugrad)
        + q("C")**4 * (1 + 4 * d * q("beta") * R["Pi"])) / 2
    mult = (q("lambda0") + d * R["LambdaU"]) * (scalar(frame, g, frame) + 1) / 2
    note("Building planar ADM Einstein source and analytic fourth coefficient")
    spatialGamma = [[[sum(hi[c][j] * (djet(h[j][bb], aa + 1) + djet(h[j][aa], bb + 1)
                          - djet(h[aa][bb], j + 1)) for j in range(3)).clean() / 2
                       for bb in range(3)] for aa in range(3)] for c in range(3)]
    shiftCov = [sum(h[i][j] * shift[j] for j in range(3)).clean() for i in range(3)]
    Ds = [[(djet(shiftCov[j], i + 1) - sum(spatialGamma[k][i][j] * shiftCov[k]
              for k in range(3))).clean() for j in range(3)] for i in range(3)]
    extrinsic = [[(invN * (djet(h[i][j], 0) - Ds[i][j] - Ds[j][i]) / 2).clean()
                  for j in range(3)] for i in range(3)]
    Km = mm(hi, extrinsic)
    EH = q("MP2") * (trace(mm(Km, Km)) - trace(Km) * trace(Km)) / 2
    R3 = d * s.Symbol("R3_response", real=True) * q("MP2") / 2
    sectors = {"Einstein_ADM": EH, "spatial_Ricci": R3, "frame": frameL,
               "alignment": align, "temporal_force": forceTemporal, "regulator": reg,
               "Cartesian_scalars_potential_portal": canonical, "dust": matter, "unit_multiplier": mult}
    mixes = {k: tidy((volum * v).coeff(2, 1)) for k, v in sectors.items()}
    contacts = {k: tidy((volum * v).coeff(4, 0)) for k, v in sectors.items()}
    quads = {k: tidy((volum * v).coeff(2, 0)) for k, v in sectors.items()}
    total, L4, L2 = (tidy(sum(xs.values())) for xs in (mixes, contacts, quads))
    expectedFrame = q("MU2") / 2 * ((q("c1") + q("c4")) * Wt**2
        - q("c1") * (Wx**2 + Wz**2) / a**2
        + (q("c1") + q("c3")) * (Wx * Bx + Wz * Bz) / a**2
        - (q("c1") + q("c3")) * (Bx**2 + Bz**2) / (2 * a**2)
        + 2 * (q("c4") - 3 * q("c2") - q("c3")) * H * W * Wt
        + (q("c4") - 2 * q("c1") - 9 * q("c2") - 3 * q("c3")) * H**2 * W**2)
    J = q("v0") * q("u_dot") - q("u0") * q("v_dot")
    expectedL2 = expectedFrame + q("MP2") * (Bx**2 + Bz**2) / (4 * a**2)
    expectedL2 += (q("K_Q") * p**2 - q("zeta") * J**2) * W**2 / 2
    exact(checks, "generic_planar_quadratic_action", L2 - expectedL2)
    for k in ("spatial_Ricci", "Cartesian_scalars_potential_portal", "dust", "unit_multiplier"):
        exact(checks, k + "_zero_direct_WWR_not_zero_coupled_response", mixes[k])
    for k in sectors:
        if k != "frame":
            exact(checks, k + "_zero_intrinsic_W4_on_registered_ray", contacts[k])
    coeffs, sources = {}, {}
    note("Varying all 22 response fields before family and first-shift substitution")
    for n in FIELDS:
        cv = tidy(s.diff(total, R[n]))
        cj = {ax: tidy(s.diff(total, Rj[ax][n])) for ax in AXES}
        coeffs[n] = {"value": cv, **{AXIS_LABEL[ax]: v for ax, v in cj.items()}}
        sources[n] = tidy(cv - deriv(cj[0], 0) - 3 * H * cj[0]
                          - deriv(cj[1], 1) - deriv(cj[3], 3))
    exact(checks, "full_mixed_functional_linear_in_retained_jets", total
          - sum(coeffs[n]["value"] * R[n] + sum(coeffs[n][AXIS_LABEL[ax]] * Rj[ax][n]
                  for ax in AXES) for n in FIELDS))
    old = common.read_json(LEGACY)
    collinear = {q: 0 for table in waves.values() for multi, q in table.items() if 1 in multi}
    collinear.update({Rj[1][n]: 0 for n in FIELDS})
    local = {str(q): q for q in total.free_symbols | L2.free_symbols}
    exact(checks, "legacy_unspecialized_collinear_WWR_exact", total.subs(collinear)
          - s.sympify(old["mixed_source_functional"], locals=local))
    exact(checks, "legacy_unspecialized_collinear_L2_exact", L2.subs(collinear)
          - s.sympify(old["quadratic_vector_action"], locals=local))
    swapfields = {"Sx": "Sz", "Sz": "Sx", "Vx": "Vz", "Vz": "Vx", "Mxx": "Mzz",
                  "Mzz": "Mxx", "Mxy": "Myz", "Myz": "Mxy"}
    rotation = {}
    for table in waves.values():
        for multi, qv in table.items():
            rotation[qv] = table[tuple(sorted(3 if ax == 1 else 1 if ax == 3 else ax for ax in multi))]
    for n in FIELDS:
        target = swapfields.get(n, n)
        rotation[R[n]] = R[target]
        for ax in AXES:
            rotation[Rj[ax][n]] = Rj[3 if ax == 1 else 1 if ax == 3 else 0][target]
    exact(checks, "x_z_exchange_covariance_WWR", total.xreplace(rotation) - total)
    exact(checks, "x_z_exchange_covariance_contact", L4.xreplace(rotation) - L4)
    vacuum = {H: 0, **{qv: 0 for qv in waves["B"].values()}}
    fixed = q("MU2") * W**2 * (-(q("c1") + q("c2") + q("c3")) * Wt**2
                              + q("c1") * (Wx**2 + Wz**2) / a**2) / 2
    exact(checks, "independent_fixed_metric_planar_contact_control", L4.subs(vacuum) - fixed)
    exact(checks, "covariant_Y_first_ray", Y.coeff(2, 0) - p**2 * W**2)
    exact(checks, "covariant_Y_first_response_cross", Y.coeff(1, 1) - 2 * p**2 * W * R["Vy"])
    exact(checks, "covariant_Y_no_intrinsic_fourth_term", Y.coeff(4, 0))
    checks.add("normal_response_source_not_removed", sources["nu"] != 0)
    checks.add("regulator_response_source_not_removed", sources["Z"] != 0)
    checks.add("planar_x_terms_not_removed", any(qv in total.free_symbols for multi, qv in waves["W"].items() if 1 in multi))
    checks.add("mixed_xz_metric_source_retained", sources["Mxz"] != 0)
    mean = {qv: 0 for table in waves.values() for multi, qv in table.items() if 1 in multi or 3 in multi}
    checks.add("homogeneous_compatible_source_not_removed", tidy(sources["alpha"].subs(mean)) != 0)
    alpha13, MT2 = q("MU2") * (q("c1") + q("c3")), q("MP2") - q("MU2") * (q("c1") + q("c3"))
    sigma, f2 = -alpha13 / MT2, q("MU2") * (q("c1") + q("c4"))
    shiftmap = {qv: sigma * waves["W"][multi] for multi, qv in waves["B"].items()}
    shifted = {n: tidy(v.subs(shiftmap)) for n, v in sources.items()}
    reducedL2 = tidy(L2.subs(shiftmap))
    EW = tidy(s.diff(reducedL2, W) - deriv(s.diff(reducedL2, Wt), 0)
              - 3 * H * s.diff(reducedL2, Wt) - deriv(s.diff(reducedL2, Wx), 1)
              - deriv(s.diff(reducedL2, Wz), 3))
    cV2 = (q("MU2") * q("c1") + alpha13**2 / (2 * MT2)) / f2
    mw2 = (-(3 * q("c2") + q("c3") - q("c4")) * q("Hdot") / (q("c1") + q("c4"))
           + 2 * H**2 - q("K_Q") * p**2 / f2 + q("zeta") * J**2 / f2)
    sol = -3 * H * Wt + cV2 * (waves["W"][(1, 1)] + waves["W"][(3, 3)]) / a**2 - mw2 * W
    exact(checks, "generic_first_direction_equation_frame_mass_not_canonical_mass",
          EW + f2 * (waves["W"][(0, 0)] - sol))
    temporal = (-deriv(shifted["alpha"], 0) - 3 * H * shifted["alpha"]
        + 2 * H * (shifted["Mxx"] + shifted["Myy"] + shifted["Mzz"])
        + (deriv(shifted["Sx"] + shifted["Vx"], 1) + deriv(shifted["Sz"] + shifted["Vz"], 3)) / a
        + q("u_dot") * shifted["du"] + q("v_dot") * shifted["dv"] + q("r_dot") * shifted["dr"]
        + p * shifted["Pi"] + q("C") * shifted["T"] + q("epsilon_dot") * shifted["Em"]
        + q("lambda_dot") * shifted["LambdaU"])
    momx = a * (deriv(shifted["Sx"], 0) + 4 * H * shifted["Sx"]) + 2 * deriv(shifted["Mxx"], 1) + deriv(shifted["Mxz"], 3)
    momz = a * (deriv(shifted["Sz"], 0) + 4 * H * shifted["Sz"]) + 2 * deriv(shifted["Mzz"], 3) + deriv(shifted["Mxz"], 1)
    note("Checking generic off-shell planar Ward identities with commuting third jets")
    wards = {"temporal": tidy(temporal - (H * W - Wt) * EW),
             "x": tidy(momx - Wx * EW), "z": tidy(momz - Wz * EW)}
    for n, residual in wards.items():
        exact(checks, "generic_planar_" + n + "_Ward_with_all_commuting_jets", residual)
    dims = {a: 0}
    assignments = {"H": 1, "Hdot": 2, "Hddot": 3, "psi_dot": 1, "psi_ddot": 2, "psi_dddot": 3,
                   "MP2": 2, "MU2": 2, "K_Q": 2, "zeta": -2, "epsilon0": 4, "lambda0": 4,
                   "epsilon_dot": 5, "lambda_dot": 5, "C_dot": 1, "m2": 2, "mr2": 2,
                   "Lambda": 1, "rho_Lambda": 4, "A": 1}
    dims.update({v: assignments.get(n, 0) for n, v in sy.items()})
    for n in ("u", "v", "r"):
        dims[sy[n + "0"]], dims[sy[n + "_dot"]], dims[sy[n + "_ddot"]] = 1, 2, 3
    fielddim = {n: 1 if n in ("du", "dv", "dr") else -1 if n == "T"
                else 4 if n in ("Em", "LambdaU") else 2 if n == "Z" else 0 for n in FIELDS}
    for n in FIELDS:
        dims[R[n]] = fielddim[n]
        dims.update({Rj[ax][n]: fielddim[n] + 1 for ax in AXES})
    for table in waves.values():
        dims.update({qv: len(multi) for multi, qv in table.items()})

    def dimension(expr):
        if expr.is_number:
            return 0
        if expr.is_Symbol:
            return dims[expr]
        if expr.is_Mul:
            return sum(dimension(v) for v in expr.args)
        if expr.is_Pow and expr.exp.is_number:
            return dimension(expr.base) * expr.exp
        if expr.is_Add:
            values = {dimension(v) for v in expr.args if v != 0}
            if len(values) != 1:
                raise ValueError("Inhomogeneous units: " + str(expr))
            return values.pop()
        raise ValueError("Unregistered dimension: " + str(expr))

    for n, expr in (("WWR", total), ("W4", L4), ("W2", L2)):
        checks.add(n + "_density_dimension_four", dimension(expr) == 4, str(dimension(expr)), "4")
    for n in FIELDS:
        for kind, expr in coeffs[n].items():
            pol = s.Poly(expr, *list(waves["W"].values()), *list(waves["B"].values()))
            checks.add("quadratic_wave_degree_" + n + "_" + kind,
                       expr == 0 or all(sum(power) == 2 for power, _ in pol.terms()))
    eta = s.Symbol("eta", positive=True)
    familymaps = {}
    for name, c2, c3 in (("archived_G3", -s.Rational(7, 48), -s.Rational(1, 80)),
                         ("new_B1_frame", s.Rational(1, 10), -s.Rational(1, 5)),
                         ("new_hierarchical", s.Rational(1, 10), -s.Rational(1, 5) + 3 * eta / 16)):
        sub = {q("MP2"): 1, q("MU2"): 2 * eta / 3, q("c1"): s.Rational(1, 5), q("c2"): c2,
               q("c3"): c3, q("c4"): s.Rational(1, 20), q("K_Q"): 3 * eta,
               q("b"): 5 * eta / 11, q("zeta"): eta / 13, q("beta"): 2 * eta**2 / 5,
               q("A"): 2 * eta**s.Rational(3, 2) / 7}
        sf = tidy(sigma.subs(sub))
        expected_MT = 1 if name == "new_B1_frame" else 1 - (eta if name == "archived_G3" else eta**2) / 8
        MT_lower = s.Integer(1) if name == "new_B1_frame" else s.Rational(7, 8)
        exact(checks, name + "_transverse_constraint_denominator_identity", MT2.subs(sub) - expected_MT)
        checks.add(name + "_eta_interior_transverse_constraint_nonsingular", MT_lower > 0,
                   {"sigma": str(sf), "MT2": str(expected_MT), "MT2_lower_bound": str(MT_lower),
                    "proof": "0<eta<=1 implies 0<eta,eta^2<=1; 1-eta^j/8>=7/8",
                    "domain": "0<eta<=1"})
        familymaps[name] = {"parameter_map": {str(k): str(v) for k, v in sub.items()},
            "sigma": str(sf), "f2": str(tidy(f2.subs(sub))), "cV2": str(tidy(cV2.subs(sub))),
            "frame_mass_squared": str(tidy(mw2.subs(sub))),
            "quadratic_action": str(tidy(reducedL2.subs(sub))),
            "intrinsic_analytic_fourth_coefficient": str(tidy(L4.subs(shiftmap).subs(sub))),
            "response_coefficients": {n: {k: str(tidy(v.subs(shiftmap).subs(sub)))
                                          for k, v in row.items()} for n, row in coeffs.items()},
            "scope": "Generic action first, then diagnostic family; no microscopic matching or physical amplitude"}
    formulas = {"field_order": list(FIELDS), "response_derivative_axes": ["t", "x", "z"],
        "jet_quotient": "e^5=d^2=e^3*d=0; analytic sectors only",
        "volume": "action = integral dt d^3x a^3 * displayed density; coefficient drift retained",
        "sector_WWR": {n: str(v) for n, v in mixes.items()}, "WWR_functional": str(total),
        "sector_intrinsic_W4": {n: str(v) for n, v in contacts.items()}, "intrinsic_W4": str(L4),
        "quadratic_vector_action": str(L2),
        "response_coefficients": {n: {k: str(v) for k, v in row.items()} for n, row in coeffs.items()},
        "Euler_sources_before_shift": {n: str(v) for n, v in sources.items()},
        "first_transverse_shift": str(sigma), "generic_reduced_vector_equation": str(EW),
        "generic_frame_mass_squared": str(tidy(mw2)), "generic_cV2": str(tidy(cV2)),
        "Ward_residuals": {n: str(v) for n, v in wards.items()},
        "families": familymaps, "spatial_Ricci_scope": "Zero direct WWR/W4 here; FULL generic response Hessian retained",
        "force": {"analytic_cubic_vertex_exists": False, "first_ray_density": "-A*abs(psi_dot*e*W)^3",
                  "directional_vector_source": "-3*A*abs(psi_dot)^3*e*abs(e)*W*abs(W)",
                  "fixed_response_ray_d_equals_e_squared_fourth_coefficient":
                      "-3*A*abs(psi_dot)^3*sign(e)*W*abs(W)*R_Vy",
                  "at_W_zero": "Zero leading coefficient; no division by W; force is C1, density C2, not C3 at zero",
                  "physical_response_sign": "Prepared cusp response changes sign; fixed-ray sign is NOT a solution sign rule"}}
    return formulas, mixes, contacts, sy, R, Rj


def numeric_inputs(index):
    params = {"a": "1.4", "H": "0.4", "MP2": "1.1", "MU2": "0.2", "c1": "0.2", "c2": "-0.14",
              "c3": "-0.0125", "c4": "0.05", "K_Q": "0.75", "b": "0.11", "zeta": "0.03",
              "beta": "0.02", "C": "1.3", "epsilon0": "0.07", "lambda0": "0.08", "u0": "0.4",
              "v0": "0.6", "r0": "0.13", "u_dot": "0.7", "v_dot": "-0.2", "r_dot": "0.03",
              "psi_dot": "0.125", "W": "0.3", "W_t": "-0.28", "W_x": "0.19", "W_z": "0.25",
              "B": "-0.2", "B_t": "0.11", "B_x": "-0.09", "B_z": "-0.16", "m2": "0.1",
              "lambda4": "0.3", "lambda6": "1", "Lambda": "2", "mr2": "0.2", "lambda_r": "0.4",
              "g_r": "0.5", "rho_Lambda": "0.09", "A": "0.14"}
    if index:
        params.update({"a": "1.8", "H": "0.23", "psi_dot": "-0.21", "W": "-0.37", "W_t": "0.18",
                       "W_x": "-0.14", "W_z": "-0.22", "u_dot": "-0.31", "v_dot": "0.12"})
    params = {k: mp.mpf(v) for k, v in params.items()}
    responses = {n: tuple(mp.mpf(v) for v in ((i + 1) * (1 if not index else (-1)**i) / 121,
                  (i % 5 - 2) / 157, (i % 3 - 1) / 139, (i % 7 - 3) / 173)) for i, n in enumerate(FIELDS)}
    return params, responses


def raw(e, d, p, responses):
    """Independent unexpanded matrices and exact first derivatives at one point.

    No polynomial-ring objects or exported coefficient expressions are used.
    Spatial Ricci is e-independent; its mixed/contact coefficient is zero.
    """
    a, H = p["a"], p["H"]
    mi = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
    M = mp.matrix([[responses[mi[i][j]][0] for j in range(3)] for i in range(3)])
    h = a * a * (mp.eye(3) + d * M)
    dh = []
    for ax in range(4):
        jj = {0: 1, 1: 2, 3: 3}.get(ax)
        dh.append((2 * H * h if ax == 0 else mp.matrix(3)) +
                  (a * a * d * mp.matrix([[responses[mi[i][j]][jj] for j in range(3)]
                                         for i in range(3)]) if jj else mp.matrix(3)))
    N = 1 + d * responses["alpha"][0]
    dN = [d * responses["alpha"][{0: 1, 1: 2, 3: 3}[ax]] if ax in AXES else mp.mpf(0) for ax in range(4)]
    shift = mp.matrix([(e * p["B"] * int(i == 1) + d * responses[n][0]) / a
                       for i, n in enumerate(("Sx", "Sy", "Sz"))])
    vel = mp.matrix([(e * p["W"] * int(i == 1) + d * responses[n][0]) / a
                     for i, n in enumerate(("Vx", "Vy", "Vz"))])
    ds, dv = [], []
    for ax in range(4):
        label, jj = AXIS_LABEL.get(ax), {0: 1, 1: 2, 3: 3}.get(ax)
        ds.append(mp.matrix([(e * p["B_" + label] * int(i == 1) + d * responses[n][jj]) / a
                            for i, n in enumerate(("Sx", "Sy", "Sz"))]) if label else mp.matrix(3, 1))
        dv.append(mp.matrix([(e * p["W_" + label] * int(i == 1) + d * responses[n][jj]) / a
                            for i, n in enumerate(("Vx", "Vy", "Vz"))]) if label else mp.matrix(3, 1))
        if ax == 0:
            ds[-1] -= H * shift
            dv[-1] -= H * vel
    gam = mp.sqrt(1 + (vel.T * h * vel)[0])
    dg = [(2 * (vel.T * h * dv[ax])[0] + (vel.T * dh[ax] * vel)[0]) / (2 * gam) for ax in range(4)]
    normal = mp.matrix([gam / N] + [vel[i] - shift[i] * gam / N for i in range(3)])
    dn = []
    for ax in range(4):
        t0 = dg[ax] / N - gam * dN[ax] / N**2
        dn.append(mp.matrix([t0] + [dv[ax][i] - ds[ax][i] * gam / N - shift[i] * t0 for i in range(3)]))
    g = mp.matrix(4)
    g[0, 0] = -N * N + (shift.T * h * shift)[0]
    for i in range(3):
        g[0, i + 1] = g[i + 1, 0] = (h * shift)[i]
        for j in range(3):
            g[i + 1, j + 1] = h[i, j]
    gder = []
    for ax in range(4):
        mat = mp.matrix(4)
        mat[0, 0] = -2 * N * dN[ax] + 2 * (shift.T * h * ds[ax])[0] + (shift.T * dh[ax] * shift)[0]
        cov = dh[ax] * shift + h * ds[ax]
        for i in range(3):
            mat[0, i + 1] = mat[i + 1, 0] = cov[i]
            for j in range(3):
                mat[i + 1, j + 1] = dh[ax][i, j]
        gder.append(mat)
    gi, hi = g**-1, h**-1
    Gamma = [[[sum(gi[c, j] * (gder[aa][j, bb] + gder[bb][j, aa] - gder[j][aa, bb])
                   for j in range(4)) / 2 for bb in range(4)] for aa in range(4)] for c in range(4)]
    DN = mp.matrix([[dn[mu][nu] + sum(Gamma[nu][mu][j] * normal[j] for j in range(4))
                     for nu in range(4)] for mu in range(4)])
    nu = 1 + d * responses["nu"][0]
    frame = nu * normal
    DU = nu * DN + mp.matrix([[d * responses["nu"][{0: 1, 1: 2, 3: 3}[mu]] * normal[j]
                              if mu in AXES else 0 for j in range(4)] for mu in range(4)])
    acc, accN = DU.T * frame, DN.T * normal
    I1 = sum(gi[i, j] * g[k, l] * DU[i, k] * DU[j, l] for i in range(4)
             for j in range(4) for k in range(4) for l in range(4))
    frameL = -p["MU2"] * (p["c1"] * I1 + p["c2"] * sum(DU[i, i] for i in range(4))**2
        + p["c3"] * sum(DU[i, j] * DU[j, i] for i in range(4) for j in range(4))
        - p["c4"] * (acc.T * g * acc)[0]) / 2
    G3 = [[[sum(hi[c, j] * (dh[aa + 1][j, bb] + dh[bb + 1][j, aa] - dh[j + 1][aa, bb])
                for j in range(3)) / 2 for bb in range(3)] for aa in range(3)] for c in range(3)]
    Ds = mp.matrix([[(dh[i + 1] * shift + h * ds[i + 1])[j]
                    - sum(G3[k][i][j] * (h * shift)[k] for k in range(3))
                    for j in range(3)] for i in range(3)])
    Km = hi * (dh[0] - Ds - Ds.T) / (2 * N)
    EH = p["MP2"] * (sum(Km[i, j] * Km[j, i] for i in range(3) for j in range(3))
                     - sum(Km[i, i] for i in range(3))**2) / 2

    def grad(n, bg):
        return mp.matrix([bg + d * responses[n][1], d * responses[n][2], 0, d * responses[n][3]])

    grads = {n: grad(n, p[bg]) for n, bg in (("du", "u_dot"), ("dv", "v_dot"), ("dr", "r_dot"), ("Pi", "psi_dot"))}
    uu, vv, rr = (p[bg] + d * responses[n][0] for n, bg in (("du", "u0"), ("dv", "v0"), ("dr", "r0")))
    current = vv * grads["du"] - uu * grads["dv"]
    hp = gi + normal * normal.T
    alignment = -p["zeta"] * (current.T * hp * current)[0] / 2
    temporal = p["K_Q"] * (normal.T * grads["Pi"])[0]**2 / 2
    zval, gz = d * responses["Z"][0], grad("Z", 0)
    regulator = p["b"] * zval * zval / 2 - p["b"] * (gz.T * hp * grads["Pi"])[0] - p["b"] * zval * (accN.T * grads["Pi"])[0]
    ss = uu * uu + vv * vv
    potential = (p["m2"] * ss / 2 + p["lambda4"] * ss**2 / 8 + p["lambda6"] * ss**3 / (24 * p["Lambda"]**2)
                 + p["mr2"] * rr**2 / 2 + p["lambda_r"] * rr**4 / 4 + p["g_r"] * ss * rr**2 / 4 + p["rho_Lambda"])
    canonical = -sum((grads[n].T * gi * grads[n])[0] for n in ("du", "dv", "dr")) / 2 - potential
    C = p["C"] * mp.exp(p["beta"] * d * responses["Pi"][0])
    tau = grad("T", p["C"])
    dust = -(p["epsilon0"] + d * responses["Em"][0]) * (C * C * (tau.T * gi * tau)[0] + C**4) / 2
    mult = (p["lambda0"] + d * responses["LambdaU"][0]) * ((frame.T * g * frame)[0] + 1) / 2
    volume = N * mp.sqrt(mp.det(h)) / a**3
    values = {"Einstein_ADM": EH, "spatial_Ricci": mp.mpf(0), "frame": frameL,
              "alignment": alignment, "temporal_force": temporal, "regulator": regulator,
              "Cartesian_scalars_potential_portal": canonical, "dust": dust, "unit_multiplier": mult}
    return {k: volume * v for k, v in values.items()}


def independent(checks, mixes, contacts, sy, R, Rj):
    mp.mp.dps = 80
    records = []
    for index in range(2):
        p, responses = numeric_inputs(index)
        sub = {sy[n]: s.Float(str(v), 85) for n, v in p.items() if n in sy}
        sub.update({R[n]: s.Float(str(responses[n][0]), 85) for n in FIELDS})
        for ax, jj in ((0, 1), (1, 2), (3, 3)):
            sub.update({Rj[ax][n]: s.Float(str(responses[n][jj]), 85) for n in FIELDS})
        targets = {}
        for kind, expressions in (("WWR", mixes), ("W4", contacts)):
            values = {}
            for n, expr in expressions.items():
                evaluated = expr.subs(sub)
                if evaluated.free_symbols:
                    raise ValueError("Unspecified independent-control inputs: " + str(evaluated.free_symbols))
                values[n] = mp.mpf(str(s.N(evaluated, 80)))
            targets[kind] = values
        rows, errors = [], {kind: {n: [] for n in mixes} for kind in targets}
        empty = {n: (mp.mpf(0),) * 4 for n in FIELDS}
        for hstr in ("0.001", "0.0005", "0.00025"):
            h = mp.mpf(hstr)
            fs = [raw(ee, dd, p, responses) for ee, dd in ((h, h), (h, -h), (-h, h), (-h, -h), (0, h), (0, -h))]
            cs = [raw(ee, 0, p, empty) for ee in (h, -h, h / 2, -h / 2, 0)]
            actual = {"WWR": {n: (fs[0][n] - fs[1][n] + fs[2][n] - fs[3][n] - 2 * (fs[4][n] - fs[5][n])) / (4 * h**3) for n in mixes},
                      "W4": {n: (cs[0][n] + cs[1][n] - 4 * (cs[2][n] + cs[3][n]) + 6 * cs[4][n]) / (mp.mpf("1.5") * h**4) for n in mixes}}
            er = {kind: {n: float(abs(value - targets[kind][n]) / max(mp.mpf(1), abs(targets[kind][n])))
                         for n, value in table.items()} for kind, table in actual.items()}
            for kind in targets:
                for n in mixes:
                    errors[kind][n].append(er[kind][n])
            rows.append({"step": hstr, "coefficients": {kind: {n: str(v) for n, v in table.items()} for kind, table in actual.items()}, "normalized_errors": er})
        for kind in targets:
            for n in mixes:
                errs = errors[kind][n]
                checks.add(f"independent_raw_planar_{index}_{kind}_{n}", errs[-1] <= 5e-7
                           and all(errs[j + 1] < errs[j] or max(errs[j + 1], errs[j]) <= 1e-12 for j in range(2)),
                           errs, "last<=5e-7; decreasing or <=1e-12 floor")
        records.append({"index": index, "params": {n: str(v) for n, v in p.items()},
                        "response_jets_value_t_x_z": {n: list(map(str, vs)) for n, vs in responses.items()},
                        "symbolic_targets": {kind: {n: str(v) for n, v in table.items()} for kind, table in targets.items()}, "rows": rows})
    note("Checking unsmoothed positive/negative force directions without a Taylor cubic")
    force_rows = []
    for sign in (-1, 1):
        A, p, W, rv = mp.mpf("0.14"), mp.mpf("-0.21"), mp.mpf("-0.37"), mp.mpf("0.09")
        expected = -3 * A * abs(p)**3 * sign * W * abs(W) * rv
        errors = []
        for step in ("0.001", "0.0005", "0.00025"):
            e = sign * mp.mpf(step)
            actual = (-A * abs(p * (e * W + e * e * rv))**3 + A * abs(p * e * W)**3) / e**4
            errors.append(float(abs(actual - expected)))
            force_rows.append({"sign": sign, "step": step, "quartic_coefficient": str(actual), "one_sided_limit": str(expected)})
        checks.add("force_fixed_ray_one_sided_limit_" + str(sign), errors[-1] <= 5e-7 and all(errors[j + 1] < errors[j] for j in range(2)), errors)
        checks.add("force_zero_ray_no_division_" + str(sign), -3 * A * abs(p)**3 * sign * mp.mpf(0) * abs(mp.mpf(0)) * rv == 0)
    return {"mp_decimal_digits": 80, "raw_geometry_is_unexpanded": True, "generic_planar_jets": records, "force_directions": force_rows}


def calculate():
    parent = common.read_json(PARENT + "summary.json")
    pins = dict(parent["source_sha256"])
    pins.update({PARENT + k: v for k, v in parent["artifacts"].items()})
    pins.update(PINNED)
    pins[SELF] = common.sha((ROOT / SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("source_pins_and_available_sidecars_before", True, {"pins": len(pins), "known_absent": missing})
    formulas, mixes, contacts, sy, R, Rj = derive(checks)
    note("Checking independent unexpanded planar action coefficients at 80 digits")
    controls = independent(checks, mixes, contacts, sy, R, Rj)
    failed_source = common.read_json(BASE + "r4c1_three_family_response_entry_attempt_01/summary.json")
    failed_time = common.read_json(BASE + "r4c1_three_family_time_response_attempt_02/summary.json")
    checks.add("earlier_source_Ward_failures_preserved", failed_source["passed"] == 958 and failed_source["total"] == 964)
    checks.add("earlier_time_mean_omission_failures_preserved", failed_time["passed"] == 10395 and failed_time["total"] == 10449)
    trajectory = BASE + "r4c1_three_family_time_response_attempt_02/trajectories.json"
    checks.add("coupled_trajectory_archive_unchanged", common.sha((ROOT / trajectory).read_bytes()) ==
               "8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d")
    checks.add("source_pins_and_available_sidecars_after", common.inspect_pins(pins) == missing)
    scope = {"classification": "GENERIC_PLANAR_COUPLED_INTERACTION_FUNCTIONAL_ONLY",
        "physical_amputated_eigenstate_amplitude_derived": False, "full_coupled_nonlinear_remainder_verified": False,
        "physical_frequency_momentum_window_demonstrated": False, "physical_cutoff_derived": False,
        "coupled_constraint_response_solved_here": False, "zero_mode_inverse_used": False,
        "spatial_Ricci_in_response_Hessian": "RETAINED_IN_PINNED_GENERIC_110_JET_EXPORT",
        "nonanalytic_force_Taylor_cubic_used": False, "trajectory_integrations_rerun": 0,
        "all_three_registered_families_retained": True, "Stage1": "COMPLETE_REGISTERED_LINEAR_PREPARED_DUST_SCOPE_ONLY",
        "Stage2": "INCOMPLETE_STOP_AND_ASSESS_DOMAIN_UNRESOLVED", "Stage3": "NOT_ENTERED_MATCHING_INPUTS_MISSING",
        "remaining": ["Coupled physical eigenstates and normalization, cubic/quartic exchange including metric/matter constraints",
                      "IR/zero-mode and finite-density state/endpoint prescriptions; no FLRW S-matrix assumed",
                      "Controlled adiabaticity, physical-energy norm, quartic dispersion and nonlinear remainder",
                      "Physical frequency/momentum domain, GR recovery, tensor and local-gravity compatibility",
                      "Identifying matter-residue and nonlinear-force matching; numerical prediction not available"],
        "physics_pass": False, "Rule9_cleared": False, "gate_effect": "NONE", "review_status": "DEFERRED",
        "canonical_tests_1_to_3": "HOLD_SUBSTANTIVE", "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS",
        "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED",
        "review_register_id": "R9-MT1-PLANAR-WWR-V1"}
    payloads = {"formulas.json": common.encode(formulas), "independent.json": common.encode(controls), "scope.json": common.encode(scope)}
    passed = sum(row["passed"] for row in checks.rows)
    ok = passed == len(checks.rows)
    summary = {"schema": "r4c1-planar-coupled-vertices-v1", "validation": "PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        "passed": passed, "total": len(checks.rows), "checks": checks.rows,
        "status": "GENERIC_PLANAR_WWR_AND_INTRINSIC_CONTACT_CHECKED_PHYSICAL_INTERACTION_OPEN" if ok else "PLANAR_COUPLED_VERTEX_ATTEMPT_REQUIRES_DISPOSITION",
        "source_sha256": dict(sorted(pins.items())), "script_sha256": pins[SELF], "artifacts": {k: common.sha(v) for k, v in payloads.items()},
        "inherited_sidecars_absent": missing, **scope,
        "runtime": {"python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__, "mp_decimal_digits": mp.mp.dps}}
    payloads["summary.json"] = common.encode(summary)
    return payloads, summary


def main():
    global PROGRESS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE + "r4c1_planar_coupled_vertices_attempt_01")
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    parser.add_argument("--progress", help="New private ignored progress file; never part of receipts")
    args = parser.parse_args()
    dest = (ROOT / (args.replay or args.output)).resolve()
    dest.relative_to((ROOT / BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    if args.progress:
        PROGRESS = (ROOT / args.progress).resolve()
        PROGRESS.relative_to((ROOT / ".local/itsm-context").resolve())
        with PROGRESS.open("x", encoding="utf-8") as f:
            f.write(json.dumps({"state": "STARTED", "mode": "replay" if args.replay else "new"}) + "\n")
    payloads, summary = calculate()
    if args.replay:
        for name, data in payloads.items():
            if (dest / name).read_bytes() != data:
                raise RuntimeError("Replay bytes differ: " + name)
            if (dest / (name + ".sha256")).read_text(encoding="utf-8") != common.sha(data) + "  " + name + "\n":
                raise RuntimeError("Replay sidecar differs: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            with (dest / name).open("xb") as f:
                f.write(data)
            with (dest / (name + ".sha256")).open("xb") as f:
                f.write((common.sha(data) + "  " + name + "\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    note(action)
    print(json.dumps({"action": action, **{k: summary[k] for k in ("validation", "passed", "total", "status", "physics_pass", "gate_effect", "Rule9_cleared")}}))
    for row in summary["checks"]:
        if not row["passed"]:
            print(json.dumps(row))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
