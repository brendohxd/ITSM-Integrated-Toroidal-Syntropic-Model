"""New quadratic fixed-charge preparation and coupled retarded comparison V1.

Perturbative coefficient calculation, NOT an admitted nonlinear solution,
physical scattering amplitude, EFT cutoff, GR clearance or matched prediction.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import block_diag
from scipy.optimize import brentq
from scipy.sparse import csr_matrix
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = BASE + "r4c1_planar_coupled_vertices_attempt_01/"
ARCHIVE = BASE + "r4c1_three_family_time_response_attempt_02/trajectories.json"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_RETARDED_COMPARISON_V1_CONTRACT_2026-10-13.md"
CHARGE = BASE + "r4c1_three_family_charge_domain_attempt_05/"
OLD_RET = BASE + "r4c1_retarded_cubic_backreaction_attempt_02/"
PINNED = {
    CONTRACT: "9940065da680b96d462df3f74b8457bb7116901d896e8aa82a1287d1d311d150",
    CHARGE + "summary.json": "54cd5450b784a21cfcac496ea7dc0e8b8ac4ebc5a74199225894919e54c2455e",
    "Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_DOMAIN_V5_REPORT_2026-10-13.md":
        "582fab6ecdcee40b2aacd09c2388128d18d35f6c90d5c90e6dfd447c793ab1c9",
    "Analysis/MasterTests/test_01_r4c1_retarded_cubic_backreaction_v2.py":
        "760a853d7fa79216286e9751efed3f920a6958a65aefbef8e0c3e63b4b4a5ab3",
    PARENT + "summary.json": "9e6ab752a0a57d95bcfdcac85ef67e59d0b9e0758eb73e12656d349b933c3268",
    "Theory/Gates/RES-001/RES001_R4C1_PLANAR_COUPLED_VERTICES_V1_REPORT_2026-10-12.md":
        "1f764b6b41e22549d82d9efd109facd8b5c85a3869aba0186fe014f71e4142bb",
    "Analysis/MasterTests/test_01_r4c1_three_family_time_response_v2.py":
        "8fec650e4c7d373a480fa087a72fb676cd9289c3d210c4f133320379a246b7ba",
    ARCHIVE: "8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d",
    "Theory/Gates/RES-001/RES001_R4C1_RETARDED_CUBIC_V2_COMPUTE_ADDENDUM_2026-10-13.md":
        "579528e428056db1b59e7f9a737e7285c29f46d82047c3aeafab6f13a06bed45",
    "Analysis/MasterTests/test_01_r4c1_retarded_cubic_backreaction_v1.py":
        "e0d4de2c9743f72d84aa1e18e8699b1a911fa99a5233b3ef70e0c9944e2b8da9",
}
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz", "Vx", "Vy", "Vz",
          "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
JETS = ("value", "t", "z", "tt", "tz", "zz")
GROUPS = {
    "metric": ("alpha", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz"),
    "frame": ("Sx", "Sy", "Sz", "Vx", "Vy", "Vz"),
    "scalar": ("du", "dv", "dr", "Pi"), "regulator": ("Z",),
}
FAMILIES = ("archived_G3", "new_B1_frame", "new_hierarchical")
ETAS = (Fraction(1, 4), Fraction(1, 64), Fraction(1, 1024))
K = 40
TEND = .05
TIMES = np.linspace(0., TEND, 21)
ODD = (1, 3, 5)
PROGRESS = None
sha = lambda body: hashlib.sha256(body).hexdigest()
read = lambda name: json.loads((ROOT / name).read_bytes())
encode = lambda obj: (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
serial = lambda z: np.stack((np.asarray(z).real, np.asarray(z).imag), axis=-1).tolist()
unserial = lambda z: np.asarray(z)[..., 0] + 1j * np.asarray(z)[..., 1]
realify = lambda z: np.r_[z.real, z.imag]
complexify = lambda z: z[:len(z) // 2] + 1j * z[len(z) // 2:]


def progress(**value):
    print(json.dumps(value, sort_keys=True), flush=True)
    if PROGRESS is not None:
        with PROGRESS.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def tidy(value):
    return s.factor(s.cancel(s.expand(value)))


class Checks:
    def __init__(self):
        self.rows = []
        self.names = set()

    def add(self, name, passed, value=None, criterion="exact"):
        if name in self.names:
            raise ValueError("Duplicate assertion " + name)
        self.names.add(name)
        self.rows.append(dict(name=name, passed=bool(passed), value=value, criterion=criterion))

    def exact(self, name, value):
        values = list(value) if isinstance(value, (list, tuple)) else [value]
        residual = [tidy(v) for v in values]
        ok = all(v == 0 for v in residual)
        self.add(name, ok, "zero_exact" if ok else list(map(str, residual)), "zero_exact")


def imports_and_pins():
    parent = read(CHARGE + "summary.json")
    pins = dict(parent["source_sha256"])
    pins.update({CHARGE + k: v for k, v in parent["artifacts"].items()})
    pins.update(PINNED)
    pins[SELF] = sha((ROOT / SELF).read_bytes())
    for name, expected in pins.items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise RuntimeError("Source drift before import: " + name)
    sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
    import test_01_r4c1_g3k_c1_clock_entry_v2 as common
    import test_01_r4c1_three_family_response_entry_v2 as prior
    import test_01_r4c1_three_family_time_response_v2 as time
    import test_01_r4c1_three_family_nonanalytic_entry_v1 as entry
    import test_01_r4c1_gr_family_survey_v2 as generic
    missing = common.inspect_pins(pins)
    return common, prior, time, entry, generic, pins, missing


def uniform_bounds(checks):
    """Exact rational certificate; norms here are comparison norms, not energy admission."""
    e = s.Symbol("eta", positive=True)
    E0 = s.Rational(1, 5) + 65 * e / 32 + 13 * e**2 / 168 + (s.Rational(1, 480) + s.Rational(3, 28) + s.Rational(3, 50)) * e**3
    recipe = (e + e / 16 + 3 * e * (e / 5)**2) / 2 + e / 2 + e**2 / 24 + e**3 / 480
    recipe += e + e**2 / 28 + 3 * e**3 / 28 + s.Rational(1, 5)
    checks.exact("action_recipe_initial_energy_identity", E0 - recipe)
    checks.add("initial_energy_polynomial_monotone_positive_eta", all(v > 0 for v in s.Poly(E0, e).all_coeffs()))
    checks.add("uniform_E0_below_3_over_4", E0.subs(e, s.Rational(1, 4)) < s.Rational(3, 4), str(E0.subs(e, s.Rational(1, 4))))
    for name, M in (("archived_G3", 1 - e / 12), ("new_B1_frame", 1 + e / 10), ("new_hierarchical", 1 + e / 10 + e**2 / 16)):
        checks.add(name + "_uniform_Mcos_interval", s.Rational(47, 48) <= M.subs(e, s.Rational(1, 4)) <= s.Rational(11, 10), str(M))
        derivative = s.Poly(s.diff(M, e), e).all_coeffs()
        checks.add(name + "_Mcos_monotone_domain_control", all(v < 0 for v in derivative) if name == "archived_G3" else all(v > 0 for v in derivative), list(map(str, derivative)))
    checks.add("H0_lower_from_energy_and_Mcos", s.Rational(1, 5) / (3 * s.Rational(11, 10)) > s.Rational(1, 25))
    checks.add("H0_upper_from_energy_and_Mcos", s.Rational(3, 4) / (3 * s.Rational(47, 48)) < s.Rational(9, 25))
    Hdot_abs = s.Rational(36, 47)
    checks.add("H_positive_bootstrap_to_registered_endpoint", s.Rational(1, 5) - Hdot_abs / 20 > 0)
    checks.exact("positive_force_velocity_lower_constant", s.Rational(1, 5) * (1 - s.Rational(9, 100)) - s.Rational(1, 200) - s.Rational(177, 1000))
    checks.add("a_upper_geometric_exponential", s.Rational(100, 97) < s.Rational(11, 10))
    checks.add("all_family_cV2_upper_bound", s.Rational(4, 5) + s.Rational(3, 224) < 1)
    mass_abs = 2 * Hdot_abs + s.Rational(18, 25) + s.Rational(9, 200) + s.Rational(3, 104)
    checks.add("all_family_frame_mass_abs_below_5_over_2", mass_abs < s.Rational(5, 2), str(mass_abs))
    checks.add("first_wave_amplitude_bound", s.Rational(121, 80) * s.Rational(80, 73)**2 < s.Rational(49, 25))
    qlower = s.Rational(80, 121) * K**2 - s.Rational(5, 2) - s.Rational(81, 100)
    checks.add("linear_canonical_root_frequency_above_32", qlower > 32**2, str(qlower))
    zero_upper = (s.Rational(11, 7) + s.Rational(9, 320)) / 32
    checks.add("Wronskian_first_zero_before_T", zero_upper < s.Rational(1, 20), str(zero_upper))
    checks.add("root_derivative_bound_from_peak_energy", 32 / s.Rational(6, 5) > 25)
    checks.add("a_power_3_over_2_below_6_over_5", s.Rational(11, 10)**3 < s.Rational(6, 5)**2)
    inherited_box = read(BASE + "r4c1_three_family_odd_tail_attempt_01/bounds.json")
    pi = inherited_box["pi"]
    # The interval endpoints are exact dyadics exported by the inherited arithmetic.
    lo = Fraction(int(pi["dyadic"][0]), 1 << inherited_box["arithmetic_bits"])
    hi = Fraction(int(pi["dyadic"][1]), 1 << inherited_box["arithmetic_bits"])
    checks.add("inherited_certified_pi_inside_3_and_22_over_7", 3 < lo <= hi < Fraction(22, 7))
    B0 = Fraction(1008, 228125)
    R5 = B0 / 32
    pref = Fraction(72, 625)
    expT = Fraction(4, 73)
    einput = expT * pref * R5
    input_point = Fraction(3, K) * einput
    total_r = Fraction(25, 16) * B0
    rtail = Fraction(3, K) * R5
    rdtail = Fraction(3, 50) * B0
    output_energy_coefficient = expT * pref * 12 * total_r
    output_point = Fraction(3, 50 * K) * output_energy_coefficient
    dmin, Cmax, Cdotmax = Fraction(25), Fraction(1001, 1000), Fraction(1001, 800000)
    tau1 = Cmax * rtail / dmin
    t2 = (input_point + output_point) / dmin
    t2 += (total_r * rtail + rdtail * total_r + Fraction(9, 5) * total_r * rtail) / dmin**2
    tau2 = Cmax * t2 + Cdotmax * total_r * rtail / dmin**2
    checks.add("N5_Fourier_energy_tail_prefactor_below_1_over_32", Fraction(128 * 1024) < Fraction(45 * 5**5))
    checks.add("retained_cusp_total_spectral_norm_control", Fraction(3, 8) < Fraction(5, 8)**2)
    checks.add("pointwise_Sobolev_constant_control", Fraction(22, 7)**2 / 3 < 4)
    checks.add("omitted_output_convolution_12_over_m_squared", Fraction(98, 9) < 12)
    checks.add("tau_tail_bounds_positive", tau1 > 0 and tau2 > 0)
    return dict(domain="0<eta<=1/4; k=40; t in [0,1/20]", exact_initial_energy=str(E0),
        constants=dict(E0_upper="3/4", Mcos_lower="47/48", Mcos_upper="11/10", H0_lower="1/5", H0_upper="3/5",
                       Hdot_abs="36/47", a_upper="100/97", pd_lower="177*eta/1000", pd_upper="eta/5",
                       cV2_lower="4/5", cV2_upper="1", frame_mass_abs_upper="5/2", mu="1", L="7/4", W_abs_upper="7/5"),
        linear_zero=dict(canonical_frequency_squared_lower=str(qlower), zero_time_upper=str(zero_upper), W_t_abs_lower="25",
            proof="While X and comparison y are positive, (X'y-Xy')'=(32^2-q)Xy<=0, so X<=y; after X's initial maximum, (X'^2+32^2 X^2)'=-2(q-32^2)XX'>=0. This certifies the linear zero only."),
        tails=dict(B0=str(B0), second_order_tail_energy_sqrt=str(R5)+"*eta^(7/2)",
                   omitted_input_third_energy_sqrt=str(einput)+"*eta^7", omitted_input_third_pointwise=str(input_point)+"*eta^7",
                   omitted_output_third_pointwise=str(output_point)+"*eta^7",
                   second_order_tail_pointwise=str(rtail)+"*eta^(7/2)", second_order_tail_velocity_pointwise=str(rdtail)+"*eta^(7/2)",
                   tau1_tail=str(tau1)+"*eta^(7/2)", tau2_tail=str(tau2)+"*eta^7"),
        tail_coefficients_rational=dict(tau1=str(tau1), tau2=str(tau2)),
        proof="Positive potential and Friedmann bootstrap, charge and force-current identities; mu-norm oscillator comparison and Parseval. h_l convolution tail uses |h_l|<=12/m^2 for m>=7, retained n<=5, plus sum_{m>5}m^-3<=1/50. Pointwise bounds use the full gradient energy, not L2 alone.",
        certificate_inputs="Exact approved recipe; NOT a certification of the binary64 numerical mirror",
        numerical_error_certified=False, full_nonlinear_remainder_certified=False, physical_EFT_window=False)


class SelfForce:
    """Euler derivatives of the new generic action export, not assumed contact rules."""
    def __init__(self, checks):
        data = read(PARENT + "formulas.json")
        checks.add("all22_new_vertex_label_order", tuple(data["field_order"]) == FIELDS)
        text = data["WWR_functional"] + " " + data["intrinsic_W4"]
        names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text))
        for family in data["families"].values():
            names.update(family["parameter_map"])
        names.update("eta Hdot psi_ddot u_ddot v_ddot r_ddot C_dot epsilon_dot lambda_dot W_tt W_tx W_tz W_xx W_xz W_zz B_tt B_tx B_tz B_xx B_xz B_zz".split())
        names.update(FIELDS)
        for n in ("W", "B", *FIELDS):
            names.add(n)
            names.update(n + "_" + suffix for suffix in ("t", "x", "z", "tt", "tx", "tz", "xx", "xz", "zz"))
        self.sy = {n: s.Symbol(n, real=True) for n in names}
        x = self.sy
        maps = {ax: {} for ax in ("t", "x", "z")}
        for name in ("W", "B", *FIELDS):
            maps["t"].update({x[name]: x[name + "_t"], x[name + "_t"]: x[name + "_tt"], x[name + "_x"]: x[name + "_tx"], x[name + "_z"]: x[name + "_tz"]})
            maps["x"].update({x[name]: x[name + "_x"], x[name + "_t"]: x[name + "_tx"], x[name + "_x"]: x[name + "_xx"], x[name + "_z"]: x[name + "_xz"]})
            maps["z"].update({x[name]: x[name + "_z"], x[name + "_t"]: x[name + "_tz"], x[name + "_x"]: x[name + "_xz"], x[name + "_z"]: x[name + "_zz"]})
        for left, right in dict(a="a*H", H="Hdot", psi_dot="psi_ddot", u0="u_dot", v0="v_dot", r0="r_dot",
                                u_dot="u_ddot", v_dot="v_ddot", r_dot="r_ddot", C="C_dot", epsilon0="epsilon_dot", lambda0="lambda_dot").items():
            if left in x:
                maps["t"][x[left]] = s.sympify(right, locals=x)

        def derivative(expr, ax):
            return s.expand(sum(s.diff(expr, q) * v for q, v in maps[ax].items() if q in expr.free_symbols))

        def Euler(expr, name, clean=True):
            raw = (s.diff(expr, x[name]) - derivative(s.diff(expr, x[name + "_t"]), "t")
                   - 3 * x["H"] * s.diff(expr, x[name + "_t"])
                   - derivative(s.diff(expr, x[name + "_x"]), "x") - derivative(s.diff(expr, x[name + "_z"]), "z"))
            return tidy(raw) if clean else s.expand(raw)

        mix = s.sympify(data["WWR_functional"], locals=x)
        contact = s.sympify(data["intrinsic_W4"], locals=x)
        sig = s.sympify(data["first_transverse_shift"], locals=x)
        shift = {x["B" + suffix]: sig * x["W" + suffix] for suffix in ("", "_t", "_x", "_z", "_tt", "_tx", "_tz", "_xx", "_xz", "_zz")}
        progress(stage="COEFFICIENT_WISE_THIRD_ORDER_EULER_DERIVATION")
        all_jets = ("value", "t", "x", "z", "tt", "tx", "tz", "xx", "xz", "zz")
        rows = {wave: {} for wave in ("W", "B")}
        original_linear_form = []
        for field in FIELDS:
            input_coefficients = {kind: s.sympify(data["response_coefficients"][field][kind], locals=x)
                                  for kind in ("value", "t", "x", "z")}
            for kind, val in input_coefficients.items():
                response_jet = x[field if kind == "value" else field + "_" + kind]
                original_linear_form.append(val * response_jet)
                substituted = tidy(val.subs(shift))
                residuals = [Euler(substituted, "W") - tidy((Euler(val, "W") + sig * Euler(val, "B")).subs(shift))]
                for axis in ("t", "x", "z"):
                    residuals.append(s.diff(substituted, x["W_" + axis])
                                     - (s.diff(val, x["W_" + axis]) + sig * s.diff(val, x["B_" + axis])).subs(shift))
                checks.exact("external_shift_chain_on_" + field + "_" + kind, residuals)
            C0, Ct, Cx, Cz = (input_coefficients[n] for n in ("value", "t", "x", "z"))
            for wave in ("W", "B"):
                qt, qx, qz = (x[wave + "_" + axis] for axis in ("t", "x", "z"))
                values = [Euler(C0, wave), Euler(Ct, wave) - s.diff(C0, qt),
                          Euler(Cx, wave) - s.diff(C0, qx), Euler(Cz, wave) - s.diff(C0, qz),
                          -s.diff(Ct, qt), -s.diff(Ct, qx) - s.diff(Cx, qt),
                          -s.diff(Ct, qz) - s.diff(Cz, qt), -s.diff(Cx, qx),
                          -s.diff(Cx, qz) - s.diff(Cz, qx), -s.diff(Cz, qz)]
                rows[wave][field] = dict(zip(all_jets, (tidy(v) for v in values)))
            progress(stage="COEFFICIENT_WISE_FIELD_COMPLETE", field=field)
        residual = s.expand(mix - s.Add(*original_linear_form))
        checks.add("input_WWR_all88_jet_linear_identity", residual == 0,
                   "zero_expanded" if residual == 0 else str(residual))
        raw_rows = {}
        for wave in ("W", "B"):
            reconstructed = s.Add(*(coef * x[field if jet == "value" else field + "_" + jet]
                                    for field in FIELDS for jet, coef in rows[wave][field].items()))
            residual = s.expand(Euler(mix, wave, clean=False) - reconstructed)
            checks.add(wave + "_DIRECT_full_product_Euler_vs_coefficient_wise", residual == 0,
                       "zero_expanded" if residual == 0 else str(residual))
            raw_rows[wave] = reconstructed
        EW4, EB4 = Euler(contact, "W"), Euler(contact, "B")
        full4 = tidy((EW4 + sig * EB4).subs(shift))
        checks.exact("external_first_shift_variation_in_contact", full4 - Euler(tidy(contact.subs(shift)), "W"))
        checks.add("omit_external_shift_is_not_generic_equivalence",
                   any(tidy((sig * coef).subs(shift)) != 0 for row in rows["B"].values() for coef in row.values())
                   and tidy((sig * EB4).subs(shift)) != 0)
        drift = -3 * x["H"] * s.diff(tidy(contact.subs(shift)), x["W_t"])
        checks.add("contact_volume_drift_not_zero", drift != 0)
        collinear = {q: 0 for n, q in x.items() if re.search(r"_(x|tx|xx|xz)$", n)}
        full4 = tidy(full4.subs(collinear))
        b4 = tidy(EB4.subs(shift).subs(collinear))
        response_symbols = [x[n if jet == "value" else n + "_" + jet] for n in FIELDS for jet in JETS]
        coefs = [[tidy((rows["W"][field][jet] + sig * rows["B"][field][jet]).subs(shift).subs(collinear))
                  for field in FIELDS for jet in JETS],
                 [tidy(rows["B"][field][jet].subs(shift).subs(collinear)) for field in FIELDS for jet in JETS]]
        fullmix, bmix = (s.Add(*(q * v for q, v in zip(response_symbols, row))) for row in coefs)
        for label, expr, row in zip(("vector", "shift"), (fullmix, bmix), coefs):
            checks.add(label + "_linear_response_jet_decomposition", s.expand(expr - sum(q * v for q, v in zip(response_symbols, row))) == 0)
        required = [n for n in FIELDS if coefs[0][FIELDS.index(n) * 6 + 3] != 0]
        checks.add("actual_required_second_time_derivatives_only_metric_and_norm", set(required) <= {"Mxx", "Myy", "Mzz", "nu"}, required)
        for n in ("T", "Em", "LambdaU"):
            checks.exact("no_direct_" + n + "_self_force_NOT_absent_coupled_response", [row[FIELDS.index(n) * 6 + j] for row in coefs for j in range(6)])
        wg = [x[n] for n in ("W", "W_t", "W_z", "W_tt", "W_tz", "W_zz")]
        checks.add("self_force_coefficient_degree_one_in_first_wave", all(v == 0 or all(sum(power) == 1 for power, _ in s.Poly(v, *wg).terms()) for row in coefs for v in row))
        checks.add("contact_self_force_degree_three", all(sum(power) == 3 for power, _ in s.Poly(full4, *wg).terms()))
        self.func = {}
        self.contact_func = {}
        self.export = dict(generic_vector_exchange=str(fullmix), generic_shift_exchange=str(bmix),
            generic_vector_contact=str(full4), generic_shift_contact=str(b4), required_Rtt=required,
            external_shift_scope="E_W+sigma E_B; third shift reconstructed from its constraint, no physical external-mode projection imposed during response evolution",
            vector_cusp_source="-6 A |psi_dot|^3 |W| R_c,Vy; directional, not a Taylor cubic")
        self.export["compiler"] = "V2 exact product-rule coefficient collection, checked against direct full WWR Euler expansion; no response-sector/global-polynomial factorization"
        self.group_indices = {n: np.array([FIELDS.index(f) * 6 + j for f in fs for j in range(6)]) for n, fs in GROUPS.items()}
        self.family_parameters = {}
        for name in FAMILIES:
            sub = {x[n]: s.sympify(v, locals=x) for n, v in data["families"][name]["parameter_map"].items()}
            expressions = [tidy(v.subs(sub)) for row in coefs for v in row]
            order = sorted({str(q) for v in expressions for q in v.free_symbols})
            self.func[name] = (order, s.lambdify([[x[n] for n in order]], expressions, "numpy", cse=True))
            cexpr = [tidy(v.subs(sub)) for v in (full4, b4)]
            corder = sorted({str(q) for v in cexpr for q in v.free_symbols})
            self.contact_func[name] = (corder, s.lambdify([[x[n] for n in corder]], cexpr, "numpy", cse=True))
            self.family_parameters[name] = (str(data["families"][name]["sigma"]), str(data["families"][name]["f2"]))
            checks.exact(name + "_local_cubic_redefinition_has_no_linear_zero_shift", (x["W"]**3).subs(x["W"], 0))
        checks.exact("tetrad_cubic_correction_vanishes_at_linear_zero", (x["Myy"] * x["W"] / 2).subs(x["W"], 0))

    def plus_coefficients(self, name, context):
        raw = {**context["raw"], "W": context["w"] / 2, "W_t": context["wd"] / 2,
               "W_z": 1j * K * context["w"] / 2, "W_tt": context["wd2"] / 2,
               "W_tz": 1j * K * context["wd"] / 2, "W_zz": -K**2 * context["w"] / 2}
        order, fun = self.func[name]
        return np.asarray(fun([raw[n] for n in order]), complex).reshape(2, 22 * 6)

    def contact_modes(self, name, context):
        theta = np.arange(8) * np.pi / 4
        co, si = np.cos(theta), np.sin(theta)
        raw = {**context["raw"], "W": context["w"] * co, "W_t": context["wd"] * co,
               "W_z": -K * context["w"] * si, "W_tt": context["wd2"] * co,
               "W_tz": -K * context["wd"] * si, "W_zz": -K**2 * context["w"] * co}
        order, fun = self.contact_func[name]
        values = np.asarray(fun([raw[n] for n in order]), complex)
        if values.shape == (2,):
            values = np.broadcast_to(values[:, None], (2, 8))
        return {mode: values @ np.exp(-1j * mode * theta) / 8 for mode in (1, 3)}


class SealedForce(SelfForce):
    """Evaluate the already-varied frozen self-force; no repeated action audit."""
    def __init__(self, checks):
        data = read(OLD_RET + 'formulas.json')
        planar = read(PARENT + 'formulas.json')
        texts = [data[n] for n in ('generic_vector_exchange','generic_shift_exchange',
                                  'generic_vector_contact','generic_shift_contact')]
        names = set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts)))
        names.add('eta')
        for family in FAMILIES:
            names.update(planar['families'][family]['parameter_map'])
        for field in FIELDS:
            names.add(field)
            names.update(field+'_'+j for j in JETS if j!='value')
        self.sy = x = {n:s.Symbol(n,real=True) for n in names}
        response = [x[n if j=='value' else n+'_'+j] for n in FIELDS for j in JETS]
        exchange = [s.sympify(t,locals=x) for t in texts[:2]]
        coefs = [[s.diff(expr,q) for q in response] for expr in exchange]
        for label, expr, row in zip(('vector','shift'),exchange,coefs):
            residual = s.expand(expr-s.Add(*(q*v for q,v in zip(response,row))))
            checks.add('sealed_'+label+'_complete132_jet_linear_identity',residual==0)
            checks.add('sealed_'+label+'_coefficients_no_response_symbols',
                       all(not(v.free_symbols & set(response)) for v in row))
        checks.add('sealed_complete22_field_order',tuple(planar['field_order'])==FIELDS)
        self.func = {}; self.contact_func = {}; self.family_parameters = {}
        self.group_indices = {n:np.array([FIELDS.index(f)*6+j for f in fs for j in range(6)])
                              for n,fs in GROUPS.items()}
        contact = [s.sympify(t,locals=x) for t in texts[2:]]
        for family in FAMILIES:
            sub = {x[n]:s.sympify(v,locals=x) for n,v in planar['families'][family]['parameter_map'].items()}
            expr = [v.subs(sub) for row in coefs for v in row]
            order = sorted({str(q) for v in expr for q in v.free_symbols})
            self.func[family] = order,s.lambdify([[x[n] for n in order]],expr,'numpy',cse=True)
            expr = [v.subs(sub) for v in contact]
            order = sorted({str(q) for v in expr for q in v.free_symbols})
            self.contact_func[family] = order,s.lambdify([[x[n] for n in order]],expr,'numpy',cse=True)
            self.family_parameters[family] = (str(planar['families'][family]['sigma']),str(planar['families'][family]['f2']))
            progress(stage='SEALED_SELF_FORCE_BOUND',family=family)
        self.export = {**data,'reuse':'Immutable retarded V2 Euler export; complete response jet/parameter binding'}


class ChargeRows:
    """Frozen action-derived affine currents plus independent analytic drift."""
    def __init__(self,checks):
        data = read(CHARGE+'canonical.json');planar = read(PARENT+'formulas.json')
        self.dyn = tuple(data['physical_fields']); self.functions = {}
        checks.add('fixed_charge_full13_physical_field_order',self.dyn==FIELDS[4:17])
        names = set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',
                              ' '.join(data[n] for n in ('Q2_affine','P2_affine','Em_constraint_affine'))))
        names.discard('Matrix');names.add('eta')
        for family in FAMILIES:names.update(planar['families'][family]['parameter_map'])
        x = {n:s.Symbol(n,real=True) for n in names};self.x=x
        parse = lambda text:s.sympify(text,locals={**x,'Matrix':s.Matrix})
        packs = {n:parse(data[k]) for n,k in dict(Q='Q2_affine',P='P2_affine',E='Em_constraint_affine').items()}
        checks.add('all_affine_rows_complete27',all(v.shape==(1,27) for v in packs.values()))
        dv = s.zeros(26,1); dx = s.zeros(26,1)
        dv[13+self.dyn.index('dv')]=1
        for name in ('Mxx','Myy','Mzz'):dx[13+self.dyn.index(name)]=s.Rational(2,3)
        J = s.Matrix([[(packs[n][:,:26]*v)[0] for v in (dv,dx)] for n in ('Q','P')])
        a,C,u,vd,H = [x[n] for n in ('a','C','u0','v_dot','H')]
        MC=x['MP2']+x['MU2']*(x['c1']+3*x['c2']+x['c3'])/2
        expected=s.Matrix([[a**3*u,0],[-a**3*vd/C,2*a**3*MC*H/C]])
        checks.exact('fixed_charge_generic_Jacobian_from_sealed_rows',list(J-expected))
        checks.exact('fixed_charge_generic_nonsingular_determinant',J.det()-2*a**6*u*MC*H/C)
        ph=-packs['Q'][26]/J[0,0]
        vl=-(packs['P'][26]+J[1,0]*ph)/J[1,1]
        seed=dv*ph+dx*vl
        for n in ('Q','P','E'):
            checks.exact('fixed_initial_'+n+'_affine_identity',(packs[n][:,:26]*seed)[0]+packs[n][26])
        eta=x['eta'];recipe={x['a']:1,x['C']:1,x['u0']:s.sqrt(eta),x['v0']:0,
                            x['u_dot']:0,x['v_dot']:s.sqrt(eta),x['w']:1,x['zeta']:eta/13}
        checks.exact('fixed_phase_velocity_exact_eta_recipe',ph.subs(recipe)-eta**s.Rational(5,2)/26)
        checks.add('reject_omitted_phase_counter',packs['Q'][26]!=0)
        checks.add('reject_omitted_volume_counter',J[1,1]!=0)
        self.export=dict(Jacobian=str(J),determinant=str(s.factor(J.det())),phase_velocity=str(ph),
                         volume_velocity=str(vl),Q2=str(packs['Q']),P2=str(packs['P']),Em=str(packs['E']),
                         initial_domain='a,C,H,u0,Mcos2>0; eta>0; no eta0/chart-singular inverse')
        const={x[n]:s.sympify(v,locals=x) for n,v in dict(m2='1',lambda4='1/3',lambda6='1/5',
                    Lambda='2',mr2='2',lambda_r='1/7',g_r='3*eta/7',rho_Lambda='0').items()}
        for family in FAMILIES:
            sub={x[n]:s.sympify(v,locals=x) for n,v in planar['families'][family]['parameter_map'].items()};sub.update(const)
            for name,expr in packs.items():
                expressions=[v.subs(sub) for v in expr]
                order=sorted({str(q) for v in expressions for q in v.free_symbols})
                self.functions[family,name]=order,s.lambdify([[x[n] for n in order]],expressions,'numpy',cse=True)
        progress(stage='FIXED_CHARGE_PREPARATION_IDENTITIES_COMPLETE')

    def at(self,family,name,data,p):
        b=data['background'];c=data['context']
        raw={**c['raw'],'rho':b[10],'w':b[12],'wd':b[13],'k':K}
        rate=dict(a=c['rate'][0],H=c['rate'][1],u0=c['rate'][2],u_dot=c['rate'][3],
                  v0=c['rate'][4],v_dot=c['rate'][5],r0=c['rate'][6],r_dot=c['rate'][7],
                  psi_dot=c['rate'][9],rho=c['rate'][10],C=c['raw']['C_dot'],w=b[13],wd=c['wd2'])
        order,fun=self.functions[family,name];values=np.array([raw[n] for n in order],float)
        coefficients=np.asarray(fun(values),complex).reshape(27)
        directions=np.array([rate.get(n,0.) for n in order],float)
        derivative=np.imag(np.asarray(fun(values+1j*1e-24*directions),complex).reshape(27))/1e-24
        return coefficients[:26],coefficients[26],derivative[:26],derivative[26]

    def seed(self,system,checks,label):
        p=system.p;b=system.first.sol(0.)
        MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        domain=all(v>0 for v in (b[0],b[1],b[2],MC,np.exp(p['beta']*b[8]),system.eta,
                                p['K_Q'],p['b'],p['MU2']*(p['c1']+p['c4']),
                                p['MP2']-p['MU2']*(p['c1']+p['c3'])))
        checks.add(label+'_declared_initial_J_domain',domain)
        if not domain:raise ValueError('Reject singular/nonpositive initial chart before reduction/inversion')
        data=system.at(0.);mean=data['mean']
        checks.add(label+'_complete_mean_coordinate_order',tuple(mean['dyn'])==self.dyn)
        q,o,_,_=self.at(system.name,'Q',data,p);v,t,_,_=self.at(system.name,'P',data,p)
        phase=13+self.dyn.index('dv');trace=np.zeros(26)
        for name in ('Mxx','Myy','Mzz'):trace[13+self.dyn.index(name)]=2/3
        J=np.array([[q[phase],q@trace],[v[phase],v@trace]],complex)
        MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        values=np.linalg.solve(J,-np.array([o,t]));seed=np.zeros(system.size,complex)
        seed[phase]=values[0];seed[:26]+=values[1]*trace
        checks.add(label+'_real_initial_counters',np.max(abs(values.imag))<=1e-12)
        for name in ('Q','P','E'):
            L,off,_,_=self.at(system.name,name,data,p);err=abs(L@seed[:26]+off)/(1+abs(off)+np.sum(abs(L*seed[:26])))
            checks.add(label+'_initial_fixed_'+name,err<=1e-10,float(err))
        checks.add(label+'_phase_eta_recipe_numeric',abs(values[0]-system.eta**2.5/26)<=1e-12)
        field=system.red.reconstruct(mean,seed[:26],p)
        checks.add(label+'_initial_full22_constraint',field['error']<=1e-9,field['error'])
        checks.add(label+'_initial_lapse_mean_density_zero',abs(field['q'][FIELDS.index('Em')])<=1e-10)
        return seed,dict(Jacobian=serial(J),free_offsets=serial(np.array([o,t])),
                         phase_velocity=float(values[0].real),volume_velocity=float(values[1].real),state=serial(seed))

    def verify(self,system,t,state,checks,label,finite=False):
        data=system.at(t);z=state[:26];flow=data['mean']['G']@z+data['mean']['g'];p=system.p
        field=system.red.reconstruct(data['mean'],z,p);rows={}
        for name in ('Q','P','E'):
            L,o,Ld,od=self.at(system.name,name,data,p)
            value=L@z+o;derivative=Ld@z+L@flow+od;scale=1+abs(o)+np.sum(abs(L*z))
            checks.add(label+'_'+name+'_real_mean',abs(value.imag)<=1e-10,float(abs(value.imag)))
            if name!='E':
                checks.add(label+'_'+name+'_zero_quadratic_charge',abs(value)/scale<=1e-7,float(abs(value)/scale))
                checks.add(label+'_'+name+'_zero_charge_derivative',abs(derivative)/(scale+np.sum(abs(L*flow)))<=1e-7,float(abs(derivative)))
            else:
                error=abs(value-field['q'][FIELDS.index('Em')])/(1+abs(value))
                drift=abs(derivative-field['qd'][FIELDS.index('Em')])/(1+abs(field['qd'][FIELDS.index('Em')]))
                checks.add(label+'_independent_lapse_density_value',error<=1e-7,float(error))
                checks.add(label+'_independent_lapse_density_drift',drift<=1e-7,float(drift))
            rows[name]=dict(value=float(value.real),derivative=float(derivative.real),cancellation_scale=float(scale))
        if finite:
            import test_01_r4c1_three_family_charge_domain_v5 as original_current
            second=system.red.reconstruct(data['second'],state[26:46],p)
            profile=field['q'],second['q'],field['qd'],second['qd'];controls={}
            mp=original_current.mp;mp.mp.dps=80
            for index,name in enumerate(('Q','P')):
                errors=[]
                for amp in ('0.000001','0.0000005','0.00000025'):
                    zero=sum(original_current.finite_current(profile,0,angle,p,data['background'])[index] for angle in (0,np.pi/2))/2
                    value=sum((original_current.finite_current(profile,amp,angle,p,data['background'])[index]+
                               original_current.finite_current(profile,'-'+amp,angle,p,data['background'])[index])/2 for angle in (0,np.pi/2))/2
                    coefficient=(value-zero)/mp.mpf(amp)**2
                    errors.append(float(abs(coefficient-rows[name]['value'])/(1+abs(rows[name]['value']))))
                checks.add(label+'_unexpanded_current_'+name,errors[-1]<=1e-7,errors)
                controls[name]=errors
            rows['unexpanded_current']=controls
        return dict(time=float(t),currents=rows)


class Context:
    """Parameterized eta, with no mutation of the frozen helper's global ETA."""
    def __init__(self, parent_time, prior, generic):
        binding = prior.Checks()
        self.bound = parent_time.TimeSources(prior, generic, binding)
        if not all(q["passed"] for q in binding.rows):
            raise RuntimeError("Pinned source compiler binding failed")
        self.g = generic
        self.binding_checks = binding.rows

    def at(self, name, eta, y, p, w, wd):
        rate = np.asarray(self.g.bg.rhs(0., y, p), float)
        small = 1e-24
        second = np.imag(np.asarray(self.g.bg.rhs(0., y.astype(complex) + 1j * small * rate, p), complex)) / small
        a, H, u, ud, v, vd, r, rd, psi, pd, rho, tau = y
        C = np.exp(p["beta"] * psi)
        raw = dict(eta=eta, a=a, H=H, Hdot=rate[1], Hddot=second[1], u0=u, v0=v, r0=r,
            u_dot=ud, v_dot=vd, r_dot=rd, u_ddot=rate[3], v_ddot=rate[5], r_ddot=rate[7],
            u_dddot=second[3], v_dddot=second[5], r_dddot=second[7], psi_dot=pd, psi_ddot=rate[9],
            psi_dddot=second[9], C=C, C_dot=p["beta"] * pd * C, epsilon0=rho / C**4,
            epsilon_dot=(rate[10] - 4 * p["beta"] * pd * rho) / C**4,
            lambda0=3 * p["MU2"] * p["c2"] * rate[1] - 3 * p["MU2"] * (p["c1"] + p["c3"]) * H**2,
            lambda_dot=3 * p["MU2"] * p["c2"] * second[1] - 6 * p["MU2"] * (p["c1"] + p["c3"]) * H * rate[1])
        order, fun = self.bound.mass[name]
        mass, cv, md = (float(v) for v in fun([raw[n] for n in order]))
        omega2 = cv * K**2 / a**2 + mass
        wd2 = -3 * H * wd - omega2 * w
        wd3 = -3 * rate[1] * wd - 3 * H * wd2 - (-2 * H * cv * K**2 / a**2 + md) * w - omega2 * wd
        return dict(raw=raw, rate=rate, mass=mass, cv=cv, omega2=omega2, w=w, wd=wd, wd2=wd2, wd3=wd3, k=K)

    def fourier(self, name, context):
        return self.bound.fourier(name, context)


def jets_affine(data, mode):
    n = len(data["dyn"])
    q = np.column_stack((data["Q0"], data["Q1"]))
    qd = np.column_stack((data["Q0d"] + data["Q1"] @ data["AA"], data["Q0"] + data["Q1d"] + data["Q1"] @ data["BB"]))
    qdd = data["F"] @ np.column_stack((data["AA"], data["BB"]))
    offset = data["us"]
    offset_d = data["usd"] + data["Q1"] @ data["ff"]
    offset_dd = data["F"] @ data["ff"]
    matrix = np.stack((q, qd, 1j * mode * q, qdd, 1j * mode * qd, -mode**2 * q), axis=1).reshape(22 * 6, 2 * n)
    source = np.stack((offset, offset_d, 1j * mode * offset, offset_dd, 1j * mode * offset_d, -mode**2 * offset), axis=1).reshape(22 * 6)
    return matrix, source


def cosine_abs_coefficient(mode):
    if mode % 2:
        return 0.
    return 2 * (-1)**(abs(mode) // 2 + 1) / (np.pi * (mode**2 - 1))


class ResponseSystem:
    """Full evolving 26+20 response states; third-order channels are downstream."""
    def __init__(self, name, eta, method, first, p, contexts, reduction, self_force):
        self.name, self.eta, self.method, self.first, self.p = name, float(eta), method, first, p
        self.ctx, self.red, self.sf = contexts, reduction, self_force
        self.cache = {}
        self.calls = 0
        self.ranges = {"mean": slice(0, 26), "second": slice(26, 46), "odd_hat": slice(46, 52)}
        offset = 52
        self.channels = {}
        for label, modes in (("contact", (1, 3)), *((n, (1, 3)) for n in GROUPS), ("cusp_hat", ODD)):
            for mode in modes:
                self.channels[label, mode] = slice(offset, offset + 2)
                offset += 2
        self.size = offset

    def at(self, t):
        if self.cache.get("t") == t:
            return self.cache["data"]
        b = self.first.sol(t)
        c = self.ctx.at(self.name, self.eta, b[:12], self.p, b[12], b[13])
        so0, so2 = self.ctx.fourier(self.name, c)
        mean = self.red.at(b[:12], self.p, 0, so0[:22], so0[22:])
        second = self.red.at(b[:12], self.p, 2 * K, so2[:22], so2[22:])
        G = np.zeros((self.size, self.size), complex)
        force = np.zeros(self.size, complex)
        G[:46, :46] = block_diag(mean["G"], second["G"])
        force[:46] = np.r_[mean["g"], second["g"]]
        f2 = self.p["MU2"] * (self.p["c1"] + self.p["c4"])
        eta35 = self.eta**3.5
        odd_forcing = []
        for j, mode in enumerate(ODD):
            sl = slice(46 + 2 * j, 48 + 2 * j)
            G[sl, sl] = [[0, 1], [-(c["cv"] * (mode * K)**2 / b[0]**2 + c["mass"]), -3 * b[1]]]
            bn = -8 * (-1)**((mode - 1) // 2) / (np.pi * mode * (mode * mode - 4))
            source = -3 * self.p["A"] * abs(b[9])**3 * b[12] * abs(b[12]) * bn / 2
            force[sl.start + 1] = source / (f2 * eta35)
            odd_forcing.append(source)
        L0, off0 = jets_affine(mean, 0)
        L2, off2 = jets_affine(second, 2 * K)
        cp = self.sf.plus_coefficients(self.name, c)
        contacts = self.sf.contact_modes(self.name, c)
        exchange = {}
        for label, indices in self.sf.group_indices.items():
            row = cp[:, indices]
            a0, a2 = L0[indices], L2[indices]
            v0, v2 = off0[indices], off2[indices]
            exchange[label, 1] = (np.column_stack((row @ a0, row.conj() @ a2)), row @ v0 + row.conj() @ v2)
            exchange[label, 3] = (np.column_stack((np.zeros((2, 26), complex), row @ a2)), row @ v2)
        cusp_factor = -6 * self.p["A"] * abs(b[9])**3 * abs(b[12]) / (f2 * eta35)
        for (label, mode), sl in self.channels.items():
            G[sl, sl] = [[0, 1], [-(c["cv"] * (mode * K)**2 / b[0]**2 + c["mass"]), -3 * b[1]]]
            if label == "contact":
                force[sl.start + 1] = contacts[mode][0] / f2
            elif label == "cusp_hat":
                for j, n in enumerate(ODD):
                    conv = cosine_abs_coefficient(mode - n) + cosine_abs_coefficient(mode + n)
                    G[sl.start + 1, 46 + 2 * j] = cusp_factor * conv
            else:
                matrix, offset = exchange[label, mode]
                G[sl.start + 1, :46] = matrix[0] / f2
                force[sl.start + 1] = offset[0] / f2
        data = dict(background=b, context=c, mean=mean, second=second, G=G, forcing=force,
                    contact=contacts, exchange=exchange, odd_forcing=odd_forcing, f2=f2,
                    L0=L0, off0=off0, L2=L2, off2=off2, plus=cp)
        self.cache = dict(t=t, data=data)
        return data

    def rhs(self, t, z):
        data = self.at(t)
        self.calls += 1
        if self.calls % 800 == 0:
            progress(stage="RETARDED_RESPONSE_RUNNING", family=self.name, eta=self.eta, method=self.method, rhs_calls=self.calls, t=float(t))
        return realify(data["G"] @ complexify(z) + data["forcing"])

    def jac(self, t, z):
        G = self.at(t)["G"]
        return csr_matrix(np.block([[G.real, -G.imag], [G.imag, G.real]]))

    def physical_channels(self, state):
        out = {}
        for key, sl in self.channels.items():
            out[key] = state[sl] * (self.eta**7 if key[0] == "cusp_hat" else 1.)
        return out

    def point_values(self, state):
        channels = self.physical_channels(state)
        r = self.eta**3.5 * np.array([state[46 + 2 * j] for j in range(3)])
        rd = self.eta**3.5 * np.array([state[47 + 2 * j] for j in range(3)])
        parts = {label: float(2 * sum(v[0].real for (n, _), v in channels.items() if n == label))
                 for label in ("contact", *GROUPS, "cusp_hat")}
        return dict(r_c=float(2 * sum(r.real)), r_c_t=float(2 * sum(rd.real)),
                    w3=float(sum(parts.values())), w3_parts=parts)


def tail_numbers(bounds, eta):
    root_num, root_den = math.isqrt(eta.numerator), math.isqrt(eta.denominator)
    if root_num**2 != eta.numerator or root_den**2 != eta.denominator:
        raise ValueError("Registered eta must have exact rational square root")
    eta35 = eta**3 * Fraction(root_num, root_den)
    result = {}
    for label, power in (("tau1", eta35), ("tau2", eta**7)):
        value = Fraction(bounds["tail_coefficients_rational"][label]) * power
        result[label] = dict(exact_rational=str(value), display_upper=float(np.nextafter(float(value), np.inf)))
    return result


def clock_geometry(b, p, q, values, e):
    """Unexpanded truncated configuration, not an exact nonlinear solution."""
    a, H, psi = b[0], b[1], b[8]
    mi = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
    index = {n: i for i, n in enumerate(FIELDS)}
    h = a * a * (np.eye(3) + e * e * np.array([[q[index[mi[i][j]]].real for j in range(3)] for i in range(3)]))
    Cbg = np.exp(p["beta"] * psi)
    C = Cbg * np.exp(p["beta"] * e * e * q[index["Pi"]].real)
    N = Cbg / C
    shift = e * e * np.array([q[index[n]].real for n in ("Sx", "Sy", "Sz")]) / a
    sigma = -p["MU2"] * (p["c1"] + p["c3"]) / (p["MP2"] - p["MU2"] * (p["c1"] + p["c3"]))
    shift[1] += (e * sigma * b[12] + e * abs(e) * sigma * values["r_c"] + e**3 * values.get("B3", 0.)) / a
    vel = e * e * np.array([q[index[n]].real for n in ("Vx", "Vy", "Vz")]) / a
    # The even response has no Vy. The directional cusp has the e|e| sign.
    vel[1] = (e * b[12] + e * abs(e) * values["r_c"] + e**3 * values["w3"]) / a
    gamma = np.sqrt(1 + vel @ h @ vel)
    normal = np.r_[gamma / N, vel - shift * gamma / N]
    g = np.zeros((4, 4))
    g[0, 0] = -N * N + shift @ h @ shift
    g[0, 1:] = g[1:, 0] = h @ shift
    g[1:, 1:] = h
    taugrad = np.array([Cbg, 0., 0., 0.])
    dust = -np.linalg.solve(g, taugrad) / C
    tetrad = np.zeros(4)
    tetrad[2] = 1 / np.sqrt(h[1, 1])
    measured = normal @ g @ tetrad
    expected = np.sqrt(h[1, 1]) * vel[1]
    return dict(unit_error=float(abs(normal @ g @ normal + 1)), dust_unit_error=float(abs(dust @ g @ dust + 1)),
        clock_norm_error=float(abs(taugrad @ np.linalg.solve(g, taugrad) + C * C)),
        dust_normal_error=float(np.max(abs(dust - np.r_[1 / N, -shift / N]))),
        tetrad_error=float(max(abs(dust @ g @ tetrad), abs(tetrad @ g @ tetrad - 1), abs(measured - expected))),
        measured_transverse_velocity=float(measured), relative_lorentz_factor=float(gamma),
        h_min=float(np.min(np.linalg.eigvalsh(h))), truncated_epsilon=float((b[10] / Cbg**4) + e * e * q[index["Em"]].real))


def run_case(name, eta, method, contexts, reduction, self_force, entry, generic, checks, bounds, charge):
    if eta not in ETAS:raise ValueError('Unregistered eta: no endpoint or chart extrapolation')
    ef = float(eta)
    label = name + "_eta" + str(eta).replace("/", "_") + "_" + method
    p, y0 = entry.initial_conditions(generic, name, ef)
    progress(stage="FIRST_WAVE", family=name, eta=ef, method=method)

    def first_rhs(t, z):
        c = contexts.at(name, ef, z[:12], p, z[12], z[13])
        return np.r_[c["rate"], z[13], c["wd2"]]

    first = solve_ivp(first_rhs, (0., TEND), np.r_[y0, 1., 0.], method=method,
                      rtol=1e-10, atol=1e-12, max_step=.001, dense_output=True)
    checks.add(label + "_first_wave_complete", first.success and first.t[-1] == TEND)
    if not first.success:
        raise RuntimeError("First wave failed: " + first.message)
    checks.add(label + "_linear_zero_bracket", first.sol(0.)[12] > 0 and first.sol(TEND)[12] < 0)
    root = brentq(lambda t: float(first.sol(t)[12]), 0., TEND, xtol=5e-15, rtol=1e-14)
    root_first = first.sol(root)
    checks.add(label + "_certified_linear_root_derivative_control", abs(root_first[13]) > 25, float(root_first[13]), ">25; analytic exact-recipe proof separate")
    system = ResponseSystem(name, eta, method, first, p, contexts, reduction, self_force)
    seed, preparation = charge.seed(system,checks,label)
    options = dict(jac=system.jac) if method == "Radau" else {}
    progress(stage="FIXED_CHARGE_FULL_COUPLED_RESPONSE", family=name, eta=ef, method=method, complex_states=system.size,
             phase_velocity=preparation['phase_velocity'],volume_velocity=preparation['volume_velocity'])
    response = solve_ivp(system.rhs, (0., TEND), realify(seed), method=method,
                         rtol=1e-10, atol=1e-12, max_step=.001, dense_output=True, **options)
    checks.add(label + "_coupled_cubic_response_complete", response.success and response.t[-1] == TEND,
               dict(nfev=response.nfev, njev=response.njev, message=response.message))
    if not response.success:
        raise RuntimeError("Retarded response failed: " + response.message)
    sampled = [complexify(response.sol(t)) for t in TIMES]
    states = np.array(sampled)
    bstates = first.sol(TIMES).T
    other_method = 'Radau' if method=='DOP853' else 'DOP853'
    def difference_rhs(t,z):
        return realify(system.at(t)['G']@complexify(z))
    options_delta=dict(jac=system.jac) if other_method=='Radau' else {}
    progress(stage='INDEPENDENT_HOMOGENEOUS_DIFFERENCE',family=name,eta=ef,method=other_method)
    difference=solve_ivp(difference_rhs,(0.,TEND),realify(seed),method=other_method,
                         rtol=1e-10,atol=1e-12,max_step=.001,dense_output=True,**options_delta)
    checks.add(label+'_homogeneous_companion_complete',difference.success and difference.t[-1]==TEND)
    if not difference.success:raise RuntimeError('Homogeneous companion failed: '+difference.message)
    delta=np.array([complexify(difference.sol(t)) for t in TIMES])
    original=next(r for r in read(OLD_RET+'trajectories.json')['runs']
                  if r['family']==name and r['eta_exact']==str(eta) and r['method']==method)
    archived=unserial(original['scaled_response_and_third_states'])
    first_error=float(np.max(abs(bstates-np.asarray(original['first_order_states']))/
                            (1+abs(np.asarray(original['first_order_states'])))))
    superposition=float(np.max(abs(states-archived-delta)/(1+abs(states)+abs(archived)+abs(delta))))
    checks.add(label+'_fresh_first_vs_immutable_parent_all21',first_error<=1e-7,first_error)
    checks.add(label+'_independent_homogeneous_superposition_all78_all21',superposition<=1e-7,superposition)
    unchanged=list(range(26,52))
    for (group,mode),sl in system.channels.items():
        if group in ('contact','cusp_hat') or mode==3:unchanged.extend(range(sl.start,sl.stop))
    checks.add(label+'_triangular_unchanged_delta_channels',np.max(abs(delta[:,unchanged]))<=1e-10,float(np.max(abs(delta[:,unchanged]))))
    charges=[charge.verify(system,float(t),z,checks,label+'_node'+str(i),finite=i in (0,10,20))
             for i,(t,z) in enumerate(zip(TIMES,states))]
    checks.add(label + "_cosine_cusp_invariant_real", np.max(abs(states[:, 46:52].imag)) <= 1e-12,
               float(np.max(abs(states[:, 46:52].imag))))
    events = []
    max_constraint = 0.
    min_mean_kinetic = 0.
    for ti, t in enumerate(sorted(set((0., .025, TEND, float(root))))):
        data = system.at(t)
        z = complexify(response.sol(t))
        item = {}
        for key, mode in (("mean", 0), ("second", 2 * K)):
            d = data[key]
            q = reduction.reconstruct(d, z[system.ranges[key]], p)
            max_constraint = max(max_constraint, q["error"])
            checks.add(label + "_all22_response_at" + str(ti) + "_" + key, q["error"] <= 1e-9, q["error"])
            checks.add(label + "_unit_normal_response_at" + str(ti) + "_" + key,
                       max(abs(q["q"][FIELDS.index("nu")]), abs(q["qd"][FIELDS.index("nu")])) <= 1e-12)
            item[key] = dict(response=serial(q["q"]), velocity=serial(q["qd"]), normalized_residual=q["error"],
                             kinetic_eigenvalues=np.linalg.eigvalsh(d["K"]).tolist())
            if key == "mean":
                min_mean_kinetic = min(min_mean_kinetic, float(np.min(np.linalg.eigvalsh(d["K"]))))
        flow = data["G"] @ z + data["forcing"]
        mode_receipts = []
        for mode in ODD:
            values = system.physical_channels(z)
            q3 = sum(v[0] for (_, n), v in values.items() if n == mode)
            q3d = sum(v[1] for (_, n), v in values.items() if n == mode)
            q3dd = sum(flow[sl.start + 1] * (ef**7 if component == "cusp_hat" else 1.)
                       for (component, n), sl in system.channels.items() if n == mode)
            source = np.zeros(2, complex)
            if mode in (1, 3):
                source += data["contact"][mode]
                for group in GROUPS:
                    matrix, offset = data["exchange"][group, mode]
                    source += matrix @ z[:46] + offset
            cusp = -6 * p["A"] * abs(data["background"][9])**3 * abs(data["background"][12])
            source[0] += cusp * ef**3.5 * sum((cosine_abs_coefficient(mode - n) + cosine_abs_coefficient(mode + n)) * z[46 + 2 * j] for j, n in enumerate(ODD))
            a, H = data["background"][:2]
            alpha13 = p["MU2"] * (p["c1"] + p["c3"])
            MT2 = p["MP2"] - alpha13
            sig = -alpha13 / MT2
            D = MT2 * (mode * K)**2 / (2 * a * a)
            B3 = sig * q3 - source[1] / D
            terms = [-data["f2"] * q3dd, -data["f2"] * 3 * H * q3d,
                     -data["f2"] * data["context"]["mass"] * q3,
                     -p["MU2"] * p["c1"] * (mode * K)**2 * q3 / a**2,
                     alpha13 * (mode * K)**2 * B3 / (2 * a * a)]
            vec = sum(terms)
            shift = D * (B3 - sig * q3)
            effective_source = source[0]
            source[0] = effective_source - sig * source[1]
            scale = max(1e-30, sum(abs(v) for v in terms) + abs(source[0])
                        + abs(D * B3) + abs(D * sig * q3) + abs(source[1]))
            error = float(max(abs(vec + source[0]), abs(shift + source[1])) / scale)
            checks.add(label + "_third_vector_and_shift_at" + str(ti) + "_m" + str(mode), error <= 1e-9, error)
            mode_receipts.append(dict(mode=mode, vector=serial(np.array([q3, q3d, q3dd])), third_shift=serial(np.array([B3])),
                                      full_source_W_and_B=serial(source), effective_vector_source=serial(np.array([effective_source])),
                                      residual_scale="sum of absolute unreduced acceleration/damping/mass/gradient/shift/source terms", normalized_residual=error))
        point = system.point_values(z)
        point["B3"] = float(2 * sum(unserial(item["third_shift"])[0].real for item in mode_receipts))
        qpoint = unserial(item["mean"]["response"]) + 2 * unserial(item["second"]["response"]).real
        checks.add(label + "_worldline_reflection_at" + str(ti),
                   max(abs(qpoint[FIELDS.index(n)]) for n in ("Sx", "Sz", "Vx", "Vz", "Mxy", "Myz")) <= 1e-8,
                   {n: float(abs(qpoint[FIELDS.index(n)])) for n in ("Sx", "Sz", "Vx", "Vz", "Mxy", "Myz")})
        geometry = clock_geometry(data["background"], p, qpoint, point, .002)
        negative_geometry = clock_geometry(data["background"], p, qpoint, point, -.002)
        checks.add(label + "_unexpanded_physical_reflection_at" + str(ti),
                   abs(geometry["measured_transverse_velocity"] + negative_geometry["measured_transverse_velocity"]) <= 1e-10
                   and abs(geometry["relative_lorentz_factor"] - negative_geometry["relative_lorentz_factor"]) <= 1e-10)
        checks.add(label + "_unexpanded_clock_and_tetrad_at" + str(ti),
                   max(geometry[n] for n in ("unit_error", "dust_unit_error", "clock_norm_error", "dust_normal_error", "tetrad_error")) <= 1e-10, geometry)
        checks.add(label + "_truncated_chart_domain_ONLY_at" + str(ti), geometry["h_min"] > 0 and geometry["truncated_epsilon"] > 0, geometry,
                   "truncated configuration only; not nonlinear physical-window admission")
        events.append(dict(time=float(t), background_and_first_wave=data['background'].tolist(),
                           full_response=item, third_vector_shift=mode_receipts, clock_geometry=geometry))
    checks.add(label + "_mean_negative_kinetic_control_recorded_not_classified", min_mean_kinetic < 0, min_mean_kinetic,
               "retain pre-physical-energy finding; not a ghost verdict")
    data = system.at(root)
    z = complexify(response.sol(root))
    point = system.point_values(z)
    c, b = data["context"], data["background"]
    root_charge=charge.verify(system,float(root),z,checks,label+'_fresh_root',finite=False)
    t1 = -point["r_c"] / b[13]
    t2 = -(point["w3"] + point["r_c_t"] * t1 + c["wd2"] * t1 * t1 / 2) / b[13]
    tau1 = c["raw"]["C"] * t1
    tau2 = c["raw"]["C"] * t2 + c["raw"]["C_dot"] * t1 * t1 / 2
    tau2_parts = {label: -c["raw"]["C"] * val / b[13] for label, val in point["w3_parts"].items()}
    tau2_parts["root_chain"] = tau2 - sum(tau2_parts.values())
    checks.add(label + "_clock_tau2_component_sum", abs(tau2 - sum(tau2_parts.values())) <= 1e-12)
    root_controls = []
    for e in (.002, .001, .0005):
        def v_over_e(t):
            bs = first.sol(t)
            pv = system.point_values(complexify(response.sol(t)))
            return bs[12] + abs(e) * pv["r_c"] + e * e * pv["w3"]
        actual_t = brentq(v_over_e, 0., TEND, xtol=5e-15, rtol=1e-14)
        actual_tau = float(first.sol(actual_t)[11])
        expected = float(b[11] + abs(e) * tau1 + e * e * tau2)
        error = float(abs(actual_tau - expected) / (e * e))
        negative_error = abs(v_over_e(actual_t) - (first.sol(actual_t)[12] + abs(-e) * system.point_values(complexify(response.sol(actual_t)))["r_c"] + (-e)**2 * system.point_values(complexify(response.sol(actual_t)))["w3"]))
        checks.add(label + "_root_reflection_sign_" + str(e), negative_error <= 1e-14, float(negative_error))
        root_controls.append(dict(e=e, direct_truncated_zero_time=float(actual_t), direct_dust_clock=actual_tau,
                                  second_order_clock_expansion=expected, residual_divided_by_e_squared=error))
    errors = [r["residual_divided_by_e_squared"] for r in root_controls]
    checks.add(label + "_truncated_root_chain_control", errors[-1] <= 1e-6 and all(errors[j + 1] < errors[j] or max(errors[j + 1], errors[j]) <= 1e-9 for j in range(2)),
               errors, "last<=1e-6; decreasing or <=1e-9 numerical floor; NOT full nonlinear remainder")
    f2 = data["f2"]
    delta_root=complexify(difference.sol(root));delta_point=system.point_values(delta_root)
    predicted_change=-c['raw']['C']*delta_point['w3']/b[13]
    delta_clock=float(tau2-original['timing']['tau2'])
    error=float(abs(delta_clock-predicted_change)/(1+abs(tau2)+abs(original['timing']['tau2'])))
    checks.add(label+'_independent_companion_dust_clock_difference',error<=1e-7,error)
    checks.add(label+'_unchanged_first_directional_clock',
               abs(tau1-original['timing']['tau1'])/(1+abs(tau1))<=1e-7)
    checks.add(label+'_unchanged_linear_root_controls',
               max(abs(root-original['timing']['linear_coordinate_zero']),
                   abs(b[11]-original['timing']['linear_dust_clock']),
                   abs(b[13]-original['timing']['linear_W_t'])/(1+abs(b[13])))<=1e-7)
    timing = dict(linear_coordinate_zero=float(root), linear_dust_clock=float(b[11]), linear_W_t=float(b[13]),
        tau1=float(tau1), tau2=float(tau2), canonical_initial_amplitude="xi=sqrt(f2)*e at a(0)=1",
        f2=float(f2), tau1_per_abs_xi=float(tau1 / np.sqrt(f2)), tau2_per_xi_squared=float(tau2 / f2),
        eta_times_tau2_per_xi_squared=float(ef * tau2 / f2), tau2_parts={k: float(v) for k, v in tau2_parts.items()},
        eta_times_tau2_parts_per_xi_squared={k: float(ef * v / f2) for k, v in tau2_parts.items()},
        harmonic_tail_ONLY_bounds=tail_numbers(bounds, eta), root_controls=root_controls,
        numerical_error_certified=False, true_nonlinear_timing_remainder_verified=False, physical_frequency_band_admitted=False)
    progress(stage="CASE_COMPLETE", family=name, eta=ef, method=method, tau2_per_xi_squared=timing["tau2_per_xi_squared"],
             eta_times_tau2_per_xi_squared=timing["eta_times_tau2_per_xi_squared"],
             old_tau2_per_xi_squared=original['timing']['tau2_per_xi_squared'],nfev=response.nfev)
    record = dict(family=name, eta=ef, eta_exact=str(eta), k=K, method=method, times=TIMES.tolist(), first_order_states=bstates.tolist(),
        scaled_response_and_third_states=serial(states), scaled_state_ranges={k: [v.start, v.stop] for k, v in system.ranges.items()},
        third_state_channels={k + "_m" + str(m): [v.start, v.stop] for (k, m), v in system.channels.items()},
        scaling="second cusp eta^(7/2); third cusp eta^7; all other states physical coefficient units", timing=timing,
        events=events, maximum_22field_second_order_residual=max_constraint, mean_kinetic_control_min=min_mean_kinetic,
        response_nfev=response.nfev, response_njev=response.njev, first_nfev=first.nfev,
        preparation=preparation,charge_controls=charges,root_charge_control=root_charge,
        homogeneous_difference_states=serial(delta),homogeneous_difference_root=serial(delta_root),
        difference_method=other_method,difference_nfev=difference.nfev,
        comparison=dict(old_timing=original['timing'],new_timing=timing,
                        tau2_difference=delta_clock,tau2_per_xi_squared_difference=delta_clock/f2,
                        homogeneous_predicted_tau2_difference=float(predicted_change),
                        first_archive_error=first_error,homogeneous_superposition_error=superposition),
        scope="Full linear second response plus sourced transverse third response; NOT all third-order fields, nonlinear solution or physical cutoff")
    return record


def calculate(compiler_only=False):
    common, prior, time, entry, generic, pins, missing = imports_and_pins()
    paths=[ROOT/n for n in pins]
    paths += [Path(str(p)+'.sha256') for p in list(paths) if Path(str(p)+'.sha256').exists()]
    snapshot=lambda:[(str(p.relative_to(ROOT)),sha(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in paths]
    before=snapshot()
    checks = Checks()
    checks.add("all_source_pins_and_sidecars_before", True, dict(pins=len(pins), known_absent=missing))
    checks.add("kernel_field_order_explicit_bijection", tuple(generic.FIELDS) == FIELDS)
    bounds = read(OLD_RET+'bounds.json')
    checks.add('inherited_tail_certificate_keeps_nonlinear_and_physical_holds',
               bounds['numerical_error_certified'] is False and bounds['full_nonlinear_remainder_certified'] is False and bounds['physical_EFT_window'] is False)
    self_force = SealedForce(checks)
    charge = ChargeRows(checks)
    if compiler_only:
        print(json.dumps(dict(action="COMPILER_ONLY_CONTROL", validation="PASS_LOCAL_CHECKS" if all(r["passed"] for r in checks.rows) else "FAIL_LOCAL_CHECKS",
            passed=sum(r["passed"] for r in checks.rows), total=len(checks.rows),
            failed=[r for r in checks.rows if not r["passed"]], physics_pass=False,
            full_programme_complete=False, numerical_integrations_started=False)))
        return None, dict(passed=sum(r["passed"] for r in checks.rows), total=len(checks.rows))
    if not all(r["passed"] for r in checks.rows):
        for row in checks.rows:
            if not row["passed"]:
                print(json.dumps(row))
        raise RuntimeError("Exact compiler controls failed before integrations")
    contexts = Context(time, prior, generic)
    reduction = time.EvolvingReduction(prior, generic)
    runs = []
    for name in FAMILIES:
        for eta in ETAS:
            pair = [run_case(name, eta, method, contexts, reduction, self_force, entry, generic, checks, bounds,charge)
                    for method in ("DOP853", "Radau")]
            a, b = pair
            xs, ys = unserial(a["scaled_response_and_third_states"]), unserial(b["scaled_response_and_third_states"])
            error = float(np.max(abs(xs - ys) / (1 + abs(xs) + abs(ys))))
            te = max(abs(a["timing"][q] - b["timing"][q]) / (1 + abs(a["timing"][q]) + abs(b["timing"][q]))
                     for q in ("linear_dust_clock", "tau1_per_abs_xi", "tau2_per_xi_squared"))
            tag = name + "_eta" + str(eta).replace("/", "_")
            checks.add(tag + "_two_method_NEW_scaled_trajectory_agreement", error <= 1e-7, error)
            checks.add(tag + "_two_method_dust_clock_coefficient_agreement", te <= 1e-7, float(te))
            runs.extend(pair)
    checks.add("old_source_failure_preserved", (read(BASE + "r4c1_three_family_response_entry_attempt_01/summary.json")["passed"],
               read(BASE + "r4c1_three_family_response_entry_attempt_01/summary.json")["total"]) == (958, 964))
    checks.add("old_time_failure_preserved", (read(BASE + "r4c1_three_family_time_response_attempt_02/summary.json")["passed"],
               read(BASE + "r4c1_three_family_time_response_attempt_02/summary.json")["total"]) == (10395, 10449))
    checks.add("old_trajectory_bytes_unchanged", sha((ROOT / ARCHIVE).read_bytes()) == PINNED[ARCHIVE])
    checks.add("all_source_pins_and_sidecars_after", common.inspect_pins(pins) == missing)
    checks.add('all_source_and_sidecar_metadata_preserved',snapshot()==before)
    scope = dict(classification="QUADRATIC_FIXED_CHARGE_PREPARATION_AND_COUPLED_CUBIC_COMPARISON",
        Stage1="COMPLETE_REGISTERED_LINEAR_PREPARED_DUST_SCOPE_ONLY", Stage2="INCOMPLETE_STOP_AND_ASSESS_DOMAIN_UNRESOLVED",
        Stage3="NOT_ENTERED_IDENTIFYING_MATCHING_MISSING", all_three_families_retained=True,
        full_second_order_even_response_retained=True, all_third_order_fields_solved=False,
        physical_eigenstate_scattering_amplitude=False, physical_EFT_cutoff_derived=False,
        continuous_physical_frequency_momentum_window=False, healthy_GR_recovery_demonstrated=False,
        continuous_finite_numerical_error_certified=False, full_nonlinear_remainder_controlled=False,
        harmonic_tail_certificate_scope="Exact registered recipe comparison norm, NOT numerical-mirror error, physical energy or nonlinear remainder",
        physical_energy_or_fixed_charge_admission=False, review_status="DEFERRED", Rule9_cleared=False,
        quadratic_initial_charge_prescription='Q2=P2=0; new seed only, no continuous projection',
        complete_nonlinear_fixed_charge_reduction=False,old_preparation_rewritten=False,
        independent_companion='all78state homogeneous difference, other ODE method',
        physics_pass=False, gate_effect="NONE", canonical_tests_1_to_3="HOLD_SUBSTANTIVE",
        **{"MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED", "V": "NOT_COMPUTED", "Stage4A": "CLOSED", "TOP-X4": "UNCHANGED"},
        review_register_id="R9-MT1-FIXED-CHARGE-RETARDED-V1",
        remaining=["Admit the complete physical-energy/constraint/fixed-charge/singular domain, not just this transverse coefficient",
                   "Control finite numerical mirror and full nonlinear solution remainder; all-sector continuous physical frequency band",
                   "Justified GR recovery and full tensor/local-gravity compatibility", "Genuine matter-residue and nonlinear-force identifying matching inputs"])
    bodies = {"formulas.json": encode(dict(**self_force.export,preparation=charge.export,harmonic_convolution="h_(m-n) r_n+h_(m+n) conjugate(r_n); |cos| has infinite even spectrum",
        clock_zero="t0+|e|t1+e^2 t2; T=0 dust clock, physical relative tetrad velocity; no full nonlinear prediction")),
        "bounds.json": encode(bounds), "trajectories.json": encode(dict(runs=runs)), "scope.json": encode(scope)}
    passed = sum(r["passed"] for r in checks.rows)
    ok = passed == len(checks.rows)
    verification = dict(validation="PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS", passed=passed, total=len(checks.rows), checks=checks.rows, **scope)
    bodies["verification.json"] = encode(verification)
    summary = dict(schema="r4c1-fixed-charge-retarded-comparison-v1", **verification,
        status="QUADRATIC_FIXED_CHARGE_COMPARISON_CHECKED_PHYSICAL_WINDOW_OPEN" if ok else "FIXED_CHARGE_COMPARISON_REQUIRES_DISPOSITION",
        source_sha256=dict(sorted(pins.items())), script_sha256=pins[SELF], artifacts={n: sha(v) for n, v in bodies.items()},
        source_compiler_binding_check_count=len(contexts.binding_checks), inherited_sidecars_absent=missing,
        source_metadata_preserved=len(before),
        runtime=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, sympy=s.__version__,
                     rtol=1e-10, atol=1e-12, max_step=.001), diagnostics_grid=dict(etas=list(map(str, ETAS)), k=K, time=[0., TEND], families=list(FAMILIES)))
    bodies["summary.json"] = encode(summary)
    return bodies, summary


def main():
    global PROGRESS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=BASE + "r4c1_fixed_charge_retarded_comparison_attempt_01")
    parser.add_argument("--replay", metavar="EXISTING_OUTPUT")
    parser.add_argument("--progress")
    parser.add_argument("--compiler-check-only", action="store_true")
    args = parser.parse_args()
    dest = (ROOT / (args.replay or args.output)).resolve()
    dest.relative_to((ROOT / BASE).resolve())
    if args.compiler_check_only and args.replay:
        raise ValueError("Compiler-only control is not a scientific replay")
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    if args.progress:
        PROGRESS = (ROOT / args.progress).resolve()
        PROGRESS.relative_to((ROOT / ".local/itsm-context").resolve())
        with PROGRESS.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(dict(state="STARTED", mode="replay" if args.replay else "new")) + "\n")
    bodies, summary = calculate(args.compiler_check_only)
    if args.compiler_check_only:
        return 0 if summary["passed"] == summary["total"] else 1
    if args.replay:
        for name, body in bodies.items():
            if (dest / name).read_bytes() != body:
                raise RuntimeError("Replay bytes differ: " + name)
            if (dest / (name + ".sha256")).read_text(encoding="utf-8") != sha(body) + "  " + name + "\n":
                raise RuntimeError("Replay sidecar differs: " + name)
        action = "READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True, exist_ok=False)
        for name, body in bodies.items():
            with (dest / name).open("xb") as stream:
                stream.write(body)
            with (dest / (name + ".sha256")).open("xb") as stream:
                stream.write((sha(body) + "  " + name + "\n").encode())
        action = "NEW_RECEIPTS_WRITTEN"
    progress(stage=action, **{k: summary[k] for k in ("validation", "passed", "total", "status", "physics_pass", "Rule9_cleared")})
    for row in summary["checks"]:
        if not row["passed"]:
            print(json.dumps(row))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
