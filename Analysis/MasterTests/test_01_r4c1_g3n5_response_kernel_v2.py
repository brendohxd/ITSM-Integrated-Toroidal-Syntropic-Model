"""G3N5 v2: exact expanded export; unchanged full-field unreduced kernel.

Frozen R4C1 action; independent off-unit normal variation; periodic Ricci
boundary identity; exact unexpanded density controls. Original inputs immutable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
PARENT = BASE + "r4c1_g3n4_force_attempt_01/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
COORDS = "txyz"
M_NAMES = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
PINS = {
    PARENT + "summary.json": "ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287",
    PARENT + "formulas.json": "e042b6b365cc1fded9b799643a4d90881eef1520839f5a31eef8d7edcfce9c57",
    PARENT + "independent.json": "dcd529971dc9eac6449619fc26284f3ea18a357f6406f44e35fb93145868d45e",
    "Theory/Gates/RES-001/RES001_R4C1_G3N4_COUPLED_SOURCE_REPORT_2026-10-09.md": "1c7eca17f22a8e3e3ec39bb09017d05908b133f130b1f24e85f523b18af47a4b",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_RESPONSE_KERNEL_CONTRACT_2026-10-09.md": "11cf25cef8cc0192f1f690dbf1f7fee2f9e0268eff508d7fb1a65709907f2c02",
    "Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v1.py": "0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_EXPORT_V2_ADDENDUM_2026-10-09.md": "fbd2a6085c0b2909a1549bb0bbefe32ed87696f124cb4778e797d7659990e7f0",
}


def tidy(x):
    return s.factor(s.expand(x))


def export_exact(x, label, audit):
    """Expand without factorization; reconstruct from the actual printed terms."""
    if not audit:
        print("G3N5 v2: exporting exact expanded expressions", flush=True)
    expanded = s.expand(x)
    symbols = {str(q): q for q in expanded.free_symbols}
    terms = [str(q) for q in s.Add.make_args(expanded)]
    # Parsing each additive term avoids a huge left-associated Python AST.
    # These strings are generated here, never accepted from model/user input.
    restored = s.expand(s.Add(*(s.sympify(q, locals=symbols) for q in terms)))
    value = str(expanded)
    difference = s.expand(restored - expanded)
    audit.append({"path": label, "roundtrip_exact": difference == 0 and str(restored) == value,
                  "reconstruction_difference": str(difference), "term_count": len(terms),
                  "expression_sha256": common.sha(value.encode()), "expanded_terms": terms})
    return value


class Jet2:
    """Exact polynomial ring modulo d^3, not numerical differentiation."""
    def __init__(self, value=0):
        self.c = list(value.c) if isinstance(value, Jet2) else ([s.sympify(v) for v in value] if isinstance(value, (list, tuple)) else [s.sympify(value), s.Integer(0), s.Integer(0)])
        if len(self.c) != 3:
            raise ValueError("Exactly three jet coefficients")

    def __add__(self, other):
        other = Jet2(other)
        return Jet2([self.c[i] + other.c[i] for i in range(3)])

    __radd__ = __add__

    def __neg__(self):
        return Jet2([-v for v in self.c])

    def __sub__(self, other):
        return self + -Jet2(other)

    def __rsub__(self, other):
        return Jet2(other) + -self

    def __mul__(self, other):
        other = Jet2(other)
        return Jet2([sum(self.c[j] * other.c[i - j] for j in range(i + 1)) for i in range(3)])

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Jet2):
            raise TypeError("Explicit inverse jets required")
        return Jet2([v / s.sympify(other) for v in self.c])

    def clean(self):
        return Jet2([s.expand(v) for v in self.c])


def zeros(n, m=None):
    return [[Jet2() for _ in range(m or n)] for _ in range(n)]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))).clean() for j in range(len(B[0]))] for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def scalar(v, A, w):
    return sum(v[i] * A[i][j] * w[j] for i in range(len(v)) for j in range(len(w))).clean()


def exact(checks, name, residual):
    values = list(residual) if isinstance(residual, (list, tuple)) else [residual]
    reduced = [tidy(v) for v in values]
    ok = all(v == 0 for v in reduced)
    checks.add(name, ok, "zero_exact" if ok else list(map(str, reduced)), "zero_exact")


def derive(checks):
    a = s.Symbol("a", positive=True)
    H, Hd, p, pdd = s.symbols("H Hdot psi_dot psi_ddot", real=True)
    MP, MU, K, b, zeta, beta, C, eps, lam = s.symbols("MP2 MU2 K_Q b zeta beta C epsilon0 lambda0", real=True)
    c1, c2, c3, c4 = s.symbols("c1 c2 c3 c4", real=True)
    u, v, r, ud, vd, rd, udd, vdd, rdd, epsdot, lamdot = s.symbols("u0 v0 r0 u_dot v_dot r_dot u_ddot v_ddot r_ddot epsilon_dot lambda_dot", real=True)
    m2, l4, l6, cutoff, mr2, lr, portal, vacuum = s.symbols("m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda", real=True)
    R = {k: s.Symbol(k, real=True) for k in FIELDS}
    D = {k: [s.Symbol(k + "_" + c, real=True) for c in COORDS] for k in FIELDS}
    DD = {k: {(i, j): s.Symbol(k + "_" + COORDS[i] + COORDS[j], real=True) for i in range(4) for j in range(i, 4)} for k in FIELDS}
    bgdt = {a: a * H, H: Hd, p: pdd, u: ud, v: vd, r: rd, ud: udd, vd: vdd, rd: rdd, C: beta * p * C, eps: epsdot, lam: lamdot}
    maps = []
    for mu in range(4):
        mapping = dict(bgdt) if mu == 0 else {}
        for k in FIELDS:
            mapping[R[k]] = D[k][mu]
            for nu in range(4):
                mapping[D[k][nu]] = DD[k][tuple(sorted((mu, nu)))]
        maps.append(mapping)

    def deriv(expr, mu):
        return s.expand(sum(s.diff(expr, q) * dq for q, dq in maps[mu].items() if q in expr.free_symbols))

    def dj(obj, mu):
        return Jet2([deriv(vv, mu) for vv in obj.c]).clean()

    d = Jet2([0, 1, 0])
    alpha = R["alpha"]
    N, invN, invN2 = 1 + d * alpha, Jet2([1, -alpha, alpha**2]), Jet2([1, -2 * alpha, 3 * alpha**2])
    M = [[R[M_NAMES[i][j]] for j in range(3)] for i in range(3)]
    M2 = [[sum(M[i][k] * M[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    h = [[a**2 * (int(i == j) + d * M[i][j]) for j in range(3)] for i in range(3)]
    hi = [[Jet2([int(i == j), -M[i][j], M2[i][j]]) / a**2 for j in range(3)] for i in range(3)]
    shift = [d * R[k] / a for k in ("Sx", "Sy", "Sz")]
    vel = [d * R[k] / a for k in ("Vx", "Vy", "Vz")]
    gamma = 1 + d * d * sum(R[k]**2 for k in ("Vx", "Vy", "Vz")) / 2
    normal = [(gamma * invN).clean()] + [(vel[i] - shift[i] * gamma * invN).clean() for i in range(3)]
    U = [((1 + d * R["nu"]) * vv).clean() for vv in normal]
    g, gi = zeros(4), zeros(4)
    g[0][0], gi[0][0] = (-N * N + scalar(shift, h, shift)).clean(), -invN2
    for i in range(3):
        g[0][i + 1] = g[i + 1][0] = sum(h[i][j] * shift[j] for j in range(3)).clean()
        gi[0][i + 1] = gi[i + 1][0] = (shift[i] * invN2).clean()
        for j in range(3):
            g[i + 1][j + 1], gi[i + 1][j + 1] = h[i][j], (hi[i][j] - shift[i] * shift[j] * invN2).clean()
    prod = mm(g, gi)
    exact(checks, "ADM_inverse_all_three_directions", [prod[i][j].c[k] - int(i == j and k == 0) for i in range(4) for j in range(4) for k in range(3)])
    exact(checks, "normalized_frame_exact_to_order_two", (scalar(normal, g, normal) + 1).c)
    exact(checks, "independent_off_unit_normal_variation", (scalar(U, g, U) + 1 + 2 * d * R["nu"] + d * d * R["nu"]**2).c)
    trM = sum(M[i][i] for i in range(3))
    trM2 = sum(M[i][j] * M[j][i] for i in range(3) for j in range(3))
    vol1, vol2 = alpha + trM / 2, alpha * trM / 2 + trM**2 / 8 - trM2 / 4
    volume = Jet2([1, vol1, vol2])
    print("Deriving full four-dimensional connection and raw frame invariants...", flush=True)
    Gamma = [[[sum(gi[c][j] * (dj(g[j][bb], aa) + dj(g[j][aa], bb) - dj(g[aa][bb], j)) for j in range(4)).clean() / 2 for bb in range(4)] for aa in range(4)] for c in range(4)]

    def nabla(vector):
        return [[(dj(vector[nu], mu) + sum(Gamma[nu][mu][j] * vector[j] for j in range(4))).clean() for nu in range(4)] for mu in range(4)]

    DU, DN = nabla(U), nabla(normal)
    accU = [sum(U[j] * DU[j][i] for j in range(4)).clean() for i in range(4)]
    accN = [sum(normal[j] * DN[j][i] for j in range(4)).clean() for i in range(4)]
    I1 = sum(gi[i][j] * g[k][l] * DU[i][k] * DU[j][l] for i in range(4) for j in range(4) for k in range(4) for l in range(4)).clean()
    I2, I3, I4 = trace(DU) * trace(DU), trace(mm(DU, DU)), scalar(accU, g, accU)
    frame = -MU * (c1 * I1 + c2 * I2 + c3 * I3 - c4 * I4) / 2
    hp = [[(gi[i][j] + normal[i] * normal[j]).clean() for j in range(4)] for i in range(4)]
    gradpsi = [p + d * D["Pi"][0]] + [d * D["Pi"][i] for i in range(1, 4)]
    gradz = [d * D["Z"][i] for i in range(4)]
    Q = sum(normal[i] * gradpsi[i] for i in range(4)).clean()
    temporal = K * Q * Q / 2
    regulator = b * d * d * R["Z"]**2 / 2 - b * scalar(gradz, hp, gradpsi) - b * d * R["Z"] * sum(accN[i] * gradpsi[i] for i in range(4))
    uu, vv, rr = u + d * R["du"], v + d * R["dv"], r + d * R["dr"]
    gu = [ud + d * D["du"][0]] + [d * D["du"][i] for i in range(1, 4)]
    gv = [vd + d * D["dv"][0]] + [d * D["dv"][i] for i in range(1, 4)]
    gr = [rd + d * D["dr"][0]] + [d * D["dr"][i] for i in range(1, 4)]
    current = [(vv * gu[i] - uu * gv[i]).clean() for i in range(4)]
    alignment = -zeta * scalar(current, hp, current) / 2
    ss = uu * uu + vv * vv
    pot = m2 * ss / 2 + l4 * ss * ss / 8 + l6 * ss * ss * ss / (24 * cutoff**2) + mr2 * rr * rr / 2 + lr * rr * rr * rr * rr / 4 + portal * ss * rr * rr / 4 + vacuum
    kinetic = -scalar(gu, gi, gu) / 2 - scalar(gv, gi, gv) / 2 - scalar(gr, gi, gr) / 2
    C2 = C**2 * (1 + 2 * beta * d * R["Pi"] + 2 * beta**2 * d * d * R["Pi"]**2)
    C4 = C**4 * (1 + 4 * beta * d * R["Pi"] + 8 * beta**2 * d * d * R["Pi"]**2)
    gtau = [C + d * D["T"][0]] + [d * D["T"][i] for i in range(1, 4)]
    dust = -(eps + d * R["Em"]) * (C2 * scalar(gtau, gi, gtau) + C4) / 2
    multiplier = (lam + d * R["LambdaU"]) * (scalar(U, g, U) + 1) / 2
    print("Retaining ADM gravity, spatial Ricci and its periodic divergence...", flush=True)
    G3 = [[[sum(hi[c][j] * (dj(h[j][bb], aa + 1) + dj(h[j][aa], bb + 1) - dj(h[aa][bb], j + 1)) for j in range(3)).clean() / 2 for bb in range(3)] for aa in range(3)] for c in range(3)]
    shiftcov = [sum(h[i][j] * shift[j] for j in range(3)).clean() for i in range(3)]
    Ds = [[(dj(shiftcov[j], i + 1) - sum(G3[k][i][j] * shiftcov[k] for k in range(3))).clean() for j in range(3)] for i in range(3)]
    extrinsic = [[(invN * (dj(h[i][j], 0) - Ds[i][j] - Ds[j][i]) / 2).clean() for j in range(3)] for i in range(3)]
    km = mm(hi, extrinsic)
    adm = MP * (trace(mm(km, km)) - trace(km) * trace(km)) / 2
    Ricci = [[sum(dj(G3[k][i][j], k + 1) - dj(G3[k][i][k], j + 1) + sum(G3[k][k][l] * G3[l][i][j] - G3[k][j][l] * G3[l][i][k] for l in range(3)) for k in range(3)).clean() for j in range(3)] for i in range(3)]
    R3 = sum(hi[i][j] * Ricci[i][j] for i in range(3) for j in range(3)).clean()
    rawcurv = s.expand((volume * MP * R3 / 2).c[2])
    second = [(DD[k][(i, j)], k, i, j) for k in set(sum((list(row) for row in M_NAMES), [])) for i in range(1, 4) for j in range(i, 4)]
    bulk, boundary = rawcurv, [s.Integer(0) for _ in range(3)]
    for q, name, i, j in sorted(second, key=lambda item: str(item[0])):
        coef = s.diff(rawcurv, q)
        bulk -= coef * q + deriv(coef, i) * D[name][j]
        boundary[i - 1] += coef * D[name][j]
    bulk = s.expand(bulk)
    exact(checks, "spatial_Ricci_explicit_divergence_identity", rawcurv - bulk - sum(deriv(boundary[i], i + 1) for i in range(3)))
    divM = [sum(D[M_NAMES[i][j]][i + 1] for i in range(3)) for j in range(3)]
    gradtr = [sum(D[M_NAMES[j][j]][i + 1] for j in range(3)) for i in range(3)]
    independent_curv = MP / (2 * a**2) * (-sum(D[M_NAMES[i][j]][k]**2 for i in range(3) for j in range(3) for k in range(1, 4)) / 4
        + sum(vv**2 for vv in gradtr) / 4 + sum(vv**2 for vv in divM) / 2 - sum(divM[i] * gradtr[i] for i in range(3)) / 2
        - sum(D["alpha"][i + 1] * (divM[i] - gradtr[i]) for i in range(3)))
    # Two first-derivative bulk forms may differ by a remaining first-jet divergence.
    # Use the derived bulk as the operator source; retain the exact difference.
    curv_difference = s.expand(bulk - independent_curv)
    curv_EL = [s.diff(curv_difference, R[k]) - sum(deriv(s.diff(curv_difference, D[k][i]), i) for i in range(1, 4)) for k in FIELDS]
    exact(checks, "spatial_Ricci_independent_Fierz_Pauli_Euler_match", curv_EL)
    sectors = {"Einstein_ADM": adm, "frame": frame, "temporal_force": temporal, "alignment": alignment,
               "regulator": regulator, "Cartesian_kinetics": kinetic, "potential_portal_vacuum": -pot, "dust": dust, "unit_multiplier": multiplier}
    L2 = {k: s.expand((volume * value).c[2]) for k, value in sectors.items()}
    L1 = {k: s.expand((volume * value).c[1]) for k, value in sectors.items()}
    L2["spatial_Ricci_bulk"] = bulk
    L1["spatial_Ricci_divergence"] = s.expand((volume * MP * R3 / 2).c[1])
    Y = scalar(gradpsi, hp, gradpsi)
    exact(checks, "nonanalytic_projected_Y_has_zero_constant_and_linear", Y.c[:2])
    Y2expected = sum((D["Pi"][i + 1] / a + p * R[name])**2 for i, name in enumerate(("Vx", "Vy", "Vz")))
    exact(checks, "nonanalytic_projected_Y_full_three_direction_square", Y.c[2] - Y2expected)
    exact(checks, "all_direction_alignment_density", L2["alignment"] + zeta * sum(((v * D["du"][i + 1] - u * D["dv"][i + 1]) / a + (v * ud - u * vd) * R[name])**2 for i, name in enumerate(("Vx", "Vy", "Vz"))) / 2)
    expected_reg = b * R["Z"]**2 / 2 - b * sum(D["Z"][i + 1] * (D["Pi"][i + 1] / a**2 + p * R[name] / a) for i, name in enumerate(("Vx", "Vy", "Vz")))
    exact(checks, "all_direction_auxiliary_regulator_density", L2["regulator"] - expected_reg)
    q1 = D["Pi"][0] - alpha * p
    q2 = p * (alpha**2 + sum(R[k]**2 for k in ("Vx", "Vy", "Vz")) / 2) - alpha * D["Pi"][0] + sum((R[vn] - R[sn]) * D["Pi"][i + 1] / a for i, (vn, sn) in enumerate(zip(("Vx", "Vy", "Vz"), ("Sx", "Sy", "Sz"))))
    exact(checks, "all_direction_temporal_force_density", L2["temporal_force"] - K * (q1**2 + 2 * p * q2 + 2 * vol1 * p * q1 + vol2 * p**2) / 2)
    total = s.expand(sum(L2.values()))
    for k in ("alpha", "Sx", "Sy", "Sz", "Em", "LambdaU", "Z"):
        exact(checks, k + "_no_own_velocity_density", s.diff(total, D[k][0]))
    print("Exporting the complete sparse 110-jet Hessian and 22 Euler operators...", flush=True)
    jets = [R[k] for k in FIELDS] + [D[k][i] for i in range(4) for k in FIELDS]
    poly = s.Poly(total, *jets)
    checks.add("homogeneous_quadratic_all_110_jets", all(sum(powers) == 2 for powers, coefficient in poly.terms() if coefficient != 0))
    entries = {}
    for powers, coefficient in poly.terms():
        occupied = [i for i, power in enumerate(powers) if power]
        if len(occupied) == 1:
            entries[(occupied[0], occupied[0])] = 2 * coefficient
        elif len(occupied) == 2:
            i, j = occupied
            entries[(i, j)] = entries[(j, i)] = coefficient
        else:
            raise ValueError("Nonquadratic jet monomial")
    exact(checks, "sparse_Hessian_reconstructs_complete_action", total - sum(coef * jets[i] * jets[j] for (i, j), coef in entries.items()) / 2)
    checks.add("sparse_Hessian_exact_symmetry", all(entries.get((j, i), 0) == coef for (i, j), coef in entries.items()))
    EL = {k: s.expand(s.diff(total, R[k]) - deriv(s.diff(total, D[k][0]), 0) - 3 * H * s.diff(total, D[k][0]) - sum(deriv(s.diff(total, D[k][i]), i) for i in range(1, 4))) for k in FIELDS}
    exact(checks, "unit_multiplier_equation_retains_normal_constraint", EL["LambdaU"] + R["nu"])
    exact(checks, "dust_multiplier_equation_retains_conformal_constraint", EL["Em"] - C**3 * (D["T"][0] - C * alpha - beta * C * R["Pi"]))
    exact(checks, "regulator_equation_retains_all_three_directions", EL["Z"] - b * (R["Z"] + sum(DD["Pi"][(i, i)] / a**2 + p * D[vn][i] / a for i, vn in enumerate(("Vx", "Vy", "Vz"), 1))))
    all_response = jets + [q for values in DD.values() for q in values.values()]
    checks.add("all_22_Euler_operators_linear", all(s.Poly(expr, *all_response).total_degree() <= 1 for expr in EL.values()))
    benchmark = {q: 0 for q in jets}
    W, Wt, Wz, B, Bz = s.symbols("W W_t W_z B B_z", real=True)
    benchmark.update({R["Vy"]: W, D["Vy"][0]: Wt, D["Vy"][3]: Wz, R["Sy"]: B, D["Sy"][3]: Bz})
    expected_frame = MU * ((c1 + c4) * Wt**2 - c1 * Wz**2 / a**2 + (c1 + c3) * Wz * Bz / a**2 - (c1 + c3) * Bz**2 / (2 * a**2)
        + 2 * (c4 - 3 * c2 - c3) * H * W * Wt + (c4 - 2 * c1 - 9 * c2 - 3 * c3) * H**2 * W**2) / 2
    exact(checks, "complete_G3V_transverse_action_before_shift_solution", total.subs(benchmark) - expected_frame - MP * Bz**2 / (4 * a**2) - (K * p**2 - zeta * (v * ud - u * vd)**2) * W**2 / 2)
    flat = {q: 0 for q in jets}
    aa, sx = s.symbols("lapse_control longitudinal_shift_gradient", real=True)
    flat.update({R["alpha"]: aa, D["Sx"][1]: sx})
    exact(checks, "flat_spatial_metric_EH_scalar_limit", L2["Einstein_ADM"].subs(flat) + 3 * MP * H**2 * aa**2 + 2 * MP * H * aa * sx / a)
    tt = {q: 0 for q in jets}
    ft, gt, fz, gz = s.symbols("TT_f_t TT_g_t TT_f_z TT_g_z", real=True)
    tt.update({D["Mxx"][0]: ft, D["Myy"][0]: -ft, D["Mxy"][0]: gt, D["Mxx"][3]: fz, D["Myy"][3]: -fz, D["Mxy"][3]: gz})
    exact(checks, "vacuum_TT_gravity_principal_block", (L2["Einstein_ADM"] + bulk).subs(tt).subs(H, 0) - MP * (ft**2 + gt**2 - (fz**2 + gz**2) / a**2) / 4)
    export_audit = []
    formulas = {"scope": "Unreduced 22-field aligned homogeneous isotropic background; all x,y,z derivatives; not solved response or physical Hessian",
        "sector_quadratic_densities_over_a3": {k: export_exact(vv, "quadratic/" + k, export_audit) for k, vv in L2.items()},
        "sector_linear_densities_over_a3": {k: export_exact(vv, "linear/" + k, export_audit) for k, vv in L1.items()},
        "Euler_operators_over_a3": {k: export_exact(vv, "Euler/" + k, export_audit) for k, vv in EL.items()},
        "spatial_Ricci": {"raw_quadratic": export_exact(rawcurv, "Ricci/raw", export_audit), "bulk": export_exact(bulk, "Ricci/bulk", export_audit), "boundary_flux": [export_exact(x, "Ricci/flux/" + str(i), export_audit) for i, x in enumerate(boundary)], "independent_first_derivative_bulk": export_exact(independent_curv, "Ricci/independent_bulk", export_audit), "bulk_difference_with_zero_Euler_operator": export_exact(curv_difference, "Ricci/difference", export_audit)},
        "nonanalytic_force": {"projected_Y_quadratic": export_exact(Y.c[2], "force/Y2", export_audit), "quadratic_density": "0", "directional_cubic_density": "-A*abs(d)^3*(sum_i(Pi_i/a+psi_dot*V_i)^2)^(3/2)", "ordinary_cubic_vertex": "NOT_DEFINED_AT_Y_ZERO", "force_not_removed": True},
        "background_time_relation": "C_dot=beta*psi_dot*C; remaining background jets unrestricted before an on-shell physical solve",
        "mass_dimensions": {"metric_frame": 0, "du_dv_dr": 1, "Pi": 0, "T": -1, "Em_LambdaU": 4, "Z": 2, "derivative": 1, "K_Q": 2, "A": 1, "b": 0}}
    kernel = {"jet_order": list(map(str, jets)), "shape": [len(jets), len(jets)], "entries": [{"row": i, "column": j, "value": export_exact(coef, f"kernel/{i}/{j}", export_audit)} for (i, j), coef in sorted(entries.items())],
              "Euler_measure": "E=dL/dR-(partial_t+3H)dL/dR_t-sum_i partial_i dL/dR_i; background derivatives retained", "physical_rank_or_sign_claim": "NONE"}
    checks.add("all_exported_expressions_exact_roundtrip", all(row["roundtrip_exact"] for row in export_audit),
               {"expressions": len(export_audit), "failed": [row for row in export_audit if not row["roundtrip_exact"]]}, "exact, no numerical tolerance")
    return formulas, kernel, s.expand(sum(vv for k, vv in L2.items() if k != "spatial_Ricci_bulk")), {str(q): q for q in total.free_symbols}, R, D, export_audit


def numeric_inputs(index):
    values = {"a": "1.4", "H": "0.4", "MP2": "1.1", "MU2": "0.2", "c1": "0.2", "c2": "-0.14", "c3": "-0.0125", "c4": "0.05", "K_Q": "0.75", "b": "0.11", "zeta": "0.03", "beta": "0.02", "C": "1.3", "epsilon0": "0.07", "lambda0": "0.08", "u0": "0.4", "v0": "0.6", "r0": "0.13", "u_dot": "0.7", "v_dot": "-0.2", "r_dot": "0.03", "psi_dot": "0.125", "m2": "0.1", "lambda4": "0.3", "lambda6": "1", "Lambda": "2", "mr2": "0.2", "lambda_r": "0.4", "g_r": "0.5", "rho_Lambda": "0.09"}
    if index:
        values.update({"a": "1.8", "H": "0.23", "psi_dot": "-0.21", "u_dot": "-0.31", "v_dot": "0.12"})
    params = {k: mp.mpf(vv) for k, vv in values.items()}
    jets = {k: [mp.mpf((i + 1) * (1 if not index else (-1)**i)) / 121] + [mp.mpf(((i + j * 3) % 7) - 3) / (157 + j * 8) for j in range(4)] for i, k in enumerate(FIELDS)}
    return params, jets


def raw_analytic(d, params, jets):
    def response(k, x):
        return jets[k][0] + sum(jets[k][i + 1] * x[i] for i in range(4))

    def point(x):
        aa = params["a"] * mp.exp(params["H"] * x[0])
        N = 1 + d * response("alpha", x)
        h = aa**2 * mp.matrix([[int(i == j) + d * response(M_NAMES[i][j], x) for j in range(3)] for i in range(3)])
        shift = mp.matrix([d * response(k, x) / aa for k in ("Sx", "Sy", "Sz")])
        vel = mp.matrix([d * response(k, x) / aa for k in ("Vx", "Vy", "Vz")])
        gamma = mp.sqrt(1 + (vel.T * h * vel)[0])
        n = mp.matrix([gamma / N] + list(vel - shift * gamma / N))
        U = (1 + d * response("nu", x)) * n
        g = mp.matrix(4)
        g[0, 0] = -N**2 + (shift.T * h * shift)[0]
        for i in range(3):
            g[0, i + 1] = g[i + 1, 0] = (h * shift)[i]
            for j in range(3):
                g[i + 1, j + 1] = h[i, j]
        return g, n, U, h, shift, N

    x0 = [mp.mpf(0)] * 4

    def derivative(fn, mu):
        def evaluate(value):
            xx = list(x0)
            xx[mu] = value
            return fn(xx)
        return mp.diff(evaluate, mp.mpf(0))

    g, n, U, h, shift, N = point(x0)
    gi, hi = g**-1, h**-1
    dg = [mp.matrix([[derivative(lambda x: point(x)[0][i, j], mu) for j in range(4)] for i in range(4)]) for mu in range(4)]
    Gamma = [[[sum(gi[c, j] * (dg[aa][j, bb] + dg[bb][j, aa] - dg[j][aa, bb]) for j in range(4)) / 2 for bb in range(4)] for aa in range(4)] for c in range(4)]
    def nabla(component):
        vec = n if component == 1 else U
        return mp.matrix([[derivative(lambda x: point(x)[component][nu], mu) + sum(Gamma[nu][mu][j] * vec[j] for j in range(4)) for nu in range(4)] for mu in range(4)])
    DN, DU = nabla(1), nabla(2)
    accN, accU = DN.T * n, DU.T * U
    I1 = sum(gi[i, j] * g[k, l] * DU[i, k] * DU[j, l] for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    frame = -params["MU2"] * (params["c1"] * I1 + params["c2"] * sum(DU[i, i] for i in range(4))**2 + params["c3"] * sum(DU[i, j] * DU[j, i] for i in range(4) for j in range(4)) - params["c4"] * (accU.T * g * accU)[0]) / 2
    dh = [mp.matrix([[derivative(lambda x: point(x)[3][i, j], mu + 1) for j in range(3)] for i in range(3)]) for mu in range(3)]
    ht = mp.matrix([[derivative(lambda x: point(x)[3][i, j], 0) for j in range(3)] for i in range(3)])
    G3 = [[[sum(hi[c, j] * (dh[aa][j, bb] + dh[bb][j, aa] - dh[j][aa, bb]) for j in range(3)) / 2 for bb in range(3)] for aa in range(3)] for c in range(3)]
    Dshift = mp.matrix([[derivative(lambda x: (point(x)[3] * point(x)[4])[j], i + 1) - sum(G3[k][i][j] * (h * shift)[k] for k in range(3)) for j in range(3)] for i in range(3)])
    km = hi * (ht - Dshift - Dshift.T) / (2 * N)
    adm = params["MP2"] * (sum(km[i, j] * km[j, i] for i in range(3) for j in range(3)) - sum(km[i, i] for i in range(3))**2) / 2
    grads = {k: mp.matrix([params[bg] + d * jets[k][1]] + [d * jets[k][i + 1] for i in range(1, 4)]) for k, bg in (("du", "u_dot"), ("dv", "v_dot"), ("dr", "r_dot"), ("Pi", "psi_dot"))}
    uu, vv, rr = (params[bg] + d * jets[k][0] for k, bg in (("du", "u0"), ("dv", "v0"), ("dr", "r0")))
    hp = gi + n * n.T
    current = vv * grads["du"] - uu * grads["dv"]
    alignment = -params["zeta"] * (current.T * hp * current)[0] / 2
    temporal = params["K_Q"] * (n.T * grads["Pi"])[0]**2 / 2
    zgrad = mp.matrix([d * jets["Z"][i + 1] for i in range(4)])
    regulator = params["b"] * (d * jets["Z"][0])**2 / 2 - params["b"] * (zgrad.T * hp * grads["Pi"])[0] - params["b"] * d * jets["Z"][0] * (accN.T * grads["Pi"])[0]
    ss = uu**2 + vv**2
    potential = params["m2"] * ss / 2 + params["lambda4"] * ss**2 / 8 + params["lambda6"] * ss**3 / (24 * params["Lambda"]**2) + params["mr2"] * rr**2 / 2 + params["lambda_r"] * rr**4 / 4 + params["g_r"] * ss * rr**2 / 4 + params["rho_Lambda"]
    canonical = -sum((grads[k].T * gi * grads[k])[0] for k in ("du", "dv", "dr")) / 2 - potential
    CC = params["C"] * mp.exp(params["beta"] * d * jets["Pi"][0])
    tau = mp.matrix([params["C"] + d * jets["T"][1]] + [d * jets["T"][i + 1] for i in range(1, 4)])
    dust = -(params["epsilon0"] + d * jets["Em"][0]) * (CC**2 * (tau.T * gi * tau)[0] + CC**4) / 2
    multiplier = (params["lambda0"] + d * jets["LambdaU"][0]) * ((U.T * g * U)[0] + 1) / 2
    return N * mp.sqrt(mp.det(h)) / params["a"]**3 * (adm + frame + alignment + temporal + regulator + canonical + dust + multiplier)


def independent(checks, quadratic, symbols, R, D):
    records = []
    for index in range(2):
        params, jets = numeric_inputs(index)
        sub = {symbols[k]: s.Float(str(v), 60) for k, v in params.items() if k in symbols}
        sub.update({R[k]: s.Float(str(jets[k][0]), 60) for k in FIELDS})
        sub.update({D[k][i]: s.Float(str(jets[k][i + 1]), 60) for k in FIELDS for i in range(4)})
        expr = quadratic.subs(sub)
        if expr.free_symbols:
            raise ValueError("Unspecified independent-control symbols: " + str(expr.free_symbols))
        target = mp.mpf(str(s.N(expr, 60)))
        f0 = raw_analytic(mp.mpf(0), params, jets)
        errors, rows = [], []
        for step in ("0.001", "0.0005", "0.00025"):
            d = mp.mpf(step)
            actual = (raw_analytic(d, params, jets) + raw_analytic(-d, params, jets) - 2 * f0) / (2 * d**2)
            error = float(abs(actual - target) / max(1, abs(actual), abs(target)))
            errors.append(error)
            rows.append({"d": step, "actual": str(actual), "target": str(target), "normalized_error": error})
        checks.add(f"all_direction_exact_unexpanded_jet_{index}", errors[-1] <= 1e-5 and all(errors[i + 1] < errors[i] or max(errors[i], errors[i + 1]) <= 1e-12 for i in range(2)), errors, "last<=1e-5; decreasing or <=1e-12 floor")
        records.append({"params": {k: str(v) for k, v in params.items()}, "response_jets": {k: list(map(str, v)) for k, v in jets.items()}, "rows": rows})
    return records


def calculate():
    mp.mp.dps = 50
    parent = common.read_json(PARENT + "summary.json")
    pins = dict(parent["source_sha256"])
    pins.update(PINS)
    pins[SELF] = common.sha((ROOT / SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("all_source_pins_and_sidecars_before", True, {"pins": len(pins), "available_sidecars": len(pins) - len(missing), "known_absent": missing})
    print("G3N5 v2: deriving the unchanged complete 22-field kernel", flush=True)
    formulas, kernel, quadratic, symbols, R, D, export_audit = derive(checks)
    print("G3N5 v2: running unchanged independent unexpanded-density controls", flush=True)
    controls = independent(checks, quadratic, symbols, R, D)
    inherited = common.read_json(PARENT + "independent.json")
    checks.add("original_G3_and_N3_failures_retained", len(inherited["inherited_failed_parent_checks"]) == 1 and len(inherited["superseded_N3_attempt_01_failed_checks"]) == 2)
    checks.add("all_source_pins_and_sidecars_after", common.inspect_pins(pins) == missing)
    payloads = {"formulas.json": common.encode(formulas), "kernel.json": common.encode(kernel),
                "export_audit.json": common.encode({"representation": "exact_expanded_additive_terms", "roundtrip_records": export_audit}),
                "independent.json": common.encode({"mp_digits": 50, "scope": "Non-Ricci analytic density; spatial Ricci checked by independent exact Euler/divergence identity", "jets": controls,
                    "inherited_failed_parent_checks": inherited["inherited_failed_parent_checks"], "superseded_N3_attempt_01_failed_checks": inherited["superseded_N3_attempt_01_failed_checks"]})}
    passed = sum(row["passed"] for row in checks.rows)
    ok = passed == len(checks.rows)
    summary = {"schema": "r4c1-g3n5-response-kernel-v2", "validation": "PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS", "passed": passed, "total": len(checks.rows), "checks": checks.rows,
        "status": "FULL_FIELD_THREE_DIRECTION_UNREDUCED_KERNEL_CHECKED_RESPONSE_OPEN" if ok else "RESPONSE_KERNEL_REQUIRES_DISPOSITION",
        "response_fields": list(FIELDS), "jet_dimension": 110, "spatial_directions": ["x", "y", "z"], "kernel_nonzero_entries": len(kernel["entries"]),
        "export_representation": "exact_expanded_roundtrip_checked", "exported_expression_count": len(export_audit),
        "source_sha256": dict(sorted(pins.items())), "script_sha256": pins[SELF], "artifacts": {k: common.sha(v) for k, v in payloads.items()}, "inherited_sidecars_absent": missing,
        "full_second_order_response_solved": False, "full_nonlinear_evolution_verified": False, "physical_Hessian_verified": False, "physical_EFT_cutoff_derived": False,
        "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False, "review_status": "DEFERRED", "canonical_tests_1_to_3": "HOLD_SUBSTANTIVE",
        "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED",
        "review_dependencies": ["R9-MT1-G3N4", "all inherited scientific and review debt"],
        "runtime": {"python": platform.python_version(), "sympy": s.__version__, "mpmath": mp.__version__, "mp_decimal_digits": mp.mp.dps}}
    payloads["summary.json"] = common.encode(summary)
    return payloads, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE + "r4c1_g3n5_attempt_02")
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    args = parser.parse_args()
    dest = (ROOT / (args.replay or args.output)).resolve()
    dest.relative_to((ROOT / BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    payloads, summary = calculate()
    if args.replay:
        for name, data in payloads.items():
            if (dest / name).read_bytes() != data or (dest / (name + ".sha256")).read_text() != common.sha(data) + "  " + name + "\n":
                raise RuntimeError("Replay bytes or sidecar differ: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in payloads.items():
            with (dest / name).open("xb") as f:
                f.write(data)
            with (dest / (name + ".sha256")).open("xb") as f:
                f.write((common.sha(data) + "  " + name + "\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action": action, **{k: summary[k] for k in ("validation", "passed", "total", "status", "physics_pass", "gate_effect", "Rule9_cleared")}}))
    for check in summary["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
