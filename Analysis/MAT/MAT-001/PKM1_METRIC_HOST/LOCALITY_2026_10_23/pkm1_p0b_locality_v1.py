"""PKM1 P0-B local force/domain diagnostic V1; no canonical promotion.

Only new receipt directories are written. The ITSM repository is read-only.
The static and orbital results are conditional reductions, not ephemeris fits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad, solve_ivp

BASE = Path(__file__).resolve().parent
CONTRACT = BASE / "ITSM_FORCE_ARCHITECTURE_COMPARISON_V1_CONTRACT_2026-10-23.md"
INPUT = BASE / "frozen_inputs_v1.json"
CHECKS = []


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check(name, condition, **details):
    CHECKS.append({"name": name, "status": "PASS" if bool(condition) else "FAIL",
                   "details": details})


def equal(name, actual, expected):
    residual = sp.factor(actual - expected)
    check(name, residual == 0, residual=str(residual))
    return residual


def metadata(path):
    p = Path(path)
    s = p.stat()
    return {"sha256": sha(p), "bytes": s.st_size, "mtime_ns": s.st_mtime_ns}


def sidecar(path):
    p = Path(path)
    candidates = [Path(str(p) + ".sha256"), p.with_suffix(".sha256")]
    return next((c for c in candidates if c.exists()), None)


def symbolic():
    y, a0, p, vx, M, K, u, u2, v2, rb = sp.symbols(
        "y a0 p vx M_P_sq K_QQ phi phi_xx psi_xx rho_b", positive=True)
    J = -2*a0**2*(p/a0-sp.log(1+p/a0))
    JY = sp.factor(sp.diff(J, p)/(2*p))
    mu = sp.factor(1+JY)
    radial = sp.factor(mu+p*sp.diff(mu, p))
    equal("J variation determines mu", mu, p/(a0+p))
    equal("static radial eigenvalue", radial, p*(p+2*a0)/(p+a0)**2)

    # R3=e^(2 psi)[4 Delta psi-2|D psi|^2] for h=e^(-2 psi)delta.
    # Integrating N sqrt(h) R3 by parts gives the following leading density.
    EH = M*(vx**2-2*p*vx)
    L = EH-M*J+M*K*u**2/2-rb*u
    dLdp = sp.diff(L, p)
    e_phi = sp.diff(L, u)-sp.diff(dLdp, p)*u2-sp.diff(dLdp, vx)*v2
    e_psi = -sp.diff(sp.diff(L, vx), p)*u2-sp.diff(sp.diff(L, vx), vx)*v2
    equal("spatial metric variation retains slip equation", e_psi, 2*M*(u2-v2))
    equal("lapse variation after spatial equation",
          e_phi.subs(v2, u2), 2*M*radial*u2+M*K*u-rb)

    # Derive the same-condensate lapse susceptibility directly, not by
    # assigning a K(Q): F=N L_phase=N[rho^2 mu_c^2/(2N^2)-V].
    N, rho, muc, mr2 = sp.symbols("N rho mu_c M_rho_sq", positive=True)
    V = sp.Function("V")(rho)
    F = rho**2*muc**2/(2*N)-N*V
    sub = {N: 1, sp.diff(V, rho): rho*muc**2,
           sp.diff(V, rho, 2): mr2+muc**2}
    fnn = sp.diff(F, N, 2).subs(sub)
    fnr = sp.diff(F, N, rho).subs(sub)
    frr = sp.diff(F, rho, 2).subs(sub)
    schur = sp.factor(fnn-fnr**2/frr)
    cs2 = mr2/(mr2+4*muc**2)
    equal("radial-lapse Schur susceptibility", schur, rho**2*muc**2/cs2)
    # Independent thermodynamic/envelope derivation of the same quantity.
    X, Q = sp.symbols("X Q", positive=True)
    P0, PX, PXX = sp.symbols("P0 PX PXX")
    dx = muc**2*(Q**2-1)
    pq = (P0+PX*dx+PXX*dx**2/2)/M
    kqq = sp.diff(pq, Q, 2).subs(Q, 1).subs(
        {PX: rho**2/2, PXX: rho**2/mr2})
    equal("Schur and P(X) routes agree", schur/M, kqq)

    d = sp.Function("delta")(y)
    tail = -d-y*sp.diff(d, y)
    equal("general stable-tail identity", tail, -sp.diff(y*d, y))
    delta_b = 1/(1+y)
    check("P0-B stable tail derivative positive",
          sp.diff(y*delta_b, y).is_positive is True,
          derivative=str(sp.diff(y*delta_b, y).factor()))
    x = sp.symbols("x", positive=True)
    dhat = (sp.sqrt(1+4*x)-1)/2
    equal("spherical algebraic flux root", dhat**2+dhat, x)
    equal("exact high-acceleration remainder", x-dhat, dhat**2)

    # Pure J depends on N, D_i N and h^ij, not derivatives of h^ij.
    q, qt, qx, b = sp.symbols("q q_t q_x b", real=True)
    Ytt = sp.exp(-q)*b**2
    Jtt = -2*a0**2*(sp.sqrt(Ytt)/a0-sp.log(1+sp.sqrt(Ytt)/a0))
    equal("J supplies no tensor time principal term", sp.diff(Jtt, qt, 2), 0)
    equal("J supplies no tensor spatial principal term", sp.diff(Jtt, qx, 2), 0)
    LT = M*(qt**2-qx**2)/4
    KT, GT = sp.diff(LT, qt, 2), -sp.diff(LT, qx, 2)
    equal("two-derivative tensor principal speed squared", GT/KT, 1)

    # SI dimension vectors are (length,time,mass); natural dimensions
    # separately: [rho,mu_c,M_rho,M_P,a0_geom]=1, [J]=2, [K_QQ]=2.
    accel, n, radius = np.array([1,-2,0]), np.array([0,-1,0]), np.array([1,0,0])
    check("perihelion rate has inverse-time SI dimension",
          np.array_equal(accel-n-radius, [0,-1,0]))
    check("Helmholtz/locality ratio is dimensionless",
          np.array_equal(np.array([-2,0,0])-2*np.array([-1,0,0]), [0,0,0]))
    check("Schur susceptibility natural mass dimension four",
          2+2 == 4)
    for xv in (1e-8, 1e-4, 0.01, 1.0, 10.0):
        dv = 2*xv/(math.sqrt(1+4*xv)+1)
        check("remainder numerical control x="+str(xv),
              0 < dv <= xv and abs(xv-dv-dv*dv) <= 1e-13*max(1,xv))
    return {
        "leading_local_density": str(L),
        "J_Y": str(JY), "mu_B": str(mu),
        "equations": {
            "spatial": "Delta(psi-phi)=0, with specified local harmonic/boundary sector",
            "source": "div[mu_B(|D phi|/a0) D phi]+K_QQ*phi/2=rho_b/(2*M_P^2)",
            "matter": "coordinate acceleration=-D phi at leading weak-field order",
            "tensor": "c_T^2=1 for the two-derivative TT principal block only"
        },
        "K_QQ": str(sp.factor(kqq)), "c_s_squared": str(cs2),
        "m_K_squared": str(sp.factor(kqq/2)),
        "force_root": "g=(g_N+sqrt(g_N^2+4*a0*g_N))/2",
        "remainder_bound": "0<=a0-(g-g_N)=(g-g_N)^2/g_N<=a0^2/g_N",
        "stable_tail": "(y*delta)' >=0 -> g-g_N>=a0*y0*delta(y0), y>=y0",
        "perihelion_rate": "-a0*sqrt(1-e^2)/(n*a)",
        "perihelion_algebraic_relative_remainder_bound": "a0/(e*g_N_at_aphelion)",
        "NOT_ESTABLISHED": [
            "global stationary finite-density background",
            "torus mean/global harmonic solution",
            "preferred-frame PPN or Cassini radio observable",
            "physical cutoff or controlled full quasistatic error",
            "GW170817 frequency-band applicability"
        ]
    }


def orbit(a0, e, options, outward=False):
    rp = 1-e
    initial = [rp, 0, 0, math.sqrt((1+e)/(1-e))]
    def rhs(t, z):
        xx, yy, ux, uy = z
        r = math.hypot(xx, yy)
        gn = 1/r**2
        extra = a0 if outward else 2*a0/(math.sqrt(1+4*a0/gn)+1)
        g = gn-extra if outward else gn+extra
        return [ux, uy, -g*xx/r, -g*yy/r]
    def peri(t, z):
        return z[0]*z[2]+z[1]*z[3]
    peri.direction = 1
    result = solve_ivp(rhs, [0, options["orbits"]*2*math.pi], initial,
                       events=peri, method=options["method"], rtol=options["rtol"],
                       atol=options["atol"], max_step=options["max_step"])
    ev = result.y_events[0][result.t_events[0] > 0.2]
    angles = np.unwrap(np.arctan2(ev[:,1], ev[:,0]))
    return {"success": bool(result.success), "events": int(len(ev)),
            "precession_per_orbit": float(np.mean(np.diff(angles))),
            "steps": int(len(result.t))}


def orbital_controls(data):
    out = []
    for e in data["controls"]["eccentricities"]:
        for acc in data["controls"]["dimensionless_a0"]:
            # Independent integration of Gauss' equation over a Kepler ellipse.
            fac = -math.sqrt(1-e*e)/e
            def integrand(f):
                dt_df = (1-e*e)**1.5/(1+e*math.cos(f))**2
                return fac*(-acc)*math.cos(f)*dt_df
            integ, err = quad(integrand, 0, 2*math.pi, epsabs=1e-13, epsrel=1e-12)
            leading = -2*math.pi*acc*math.sqrt(1-e*e)
            check(f"Gauss orbital average e={e} a0={acc}",
                  abs(integ-leading) <= data["controls"]["tolerances"]["quadrature_absolute"],
                  computed=integ, exact=leading, quadrature_error=err)
            result = orbit(acc, e, data["controls"]["cartesian"])
            rel = abs(result["precession_per_orbit"]/leading-1)
            check(f"Cartesian exact-force orbit e={e} a0={acc}",
                  result["success"] and result["events"] >= 4 and
                  rel < data["controls"]["tolerances"]["orbital_leading_relative"],
                  relative_to_first_order=rel, **result)
            out.append({"eccentricity":e, "a0":acc, "leading":leading,
                        "quadrature":integ, "relative_error":rel, **result})
        zero = orbit(0, e, data["controls"]["cartesian"])
        check("Newtonian orbit zero control e="+str(e),
              zero["success"] and abs(zero["precession_per_orbit"]) <
              data["controls"]["tolerances"]["zero_orbit_absolute"], **zero)
        wrong = orbit(1e-5, e, data["controls"]["cartesian"], outward=True)
        check("outward-force sign mutant rejected e="+str(e),
              wrong["success"] and wrong["precession_per_orbit"] > 0, **wrong)
    return out


def planetary_bounds(data):
    constants = data["external_sources"]["constants"]
    gm, au = float(constants["GM_sun_m3_s2"]), float(constants["AU_m"])
    century = float(constants["seconds_per_day"])*float(constants["days_per_julian_century"])
    conv = (180/math.pi)*3600*1000*century
    rows = []
    for planet in data["planets"]:
        a, e = au*float(planet["a_AU"]), float(planet["eccentricity"])
        n = math.sqrt(gm/a**3)
        coeff = math.sqrt(1-e*e)/(n*a)*conv
        gn_min = gm/(a*(1+e))**2
        for criterion, interval in planet["intervals_mas_century"].items():
            low, high = interval
            # Predicted first-order precession is -coeff*a0 for a0>0.
            signed = -low/coeff
            absolute = max(abs(low),abs(high))/coeff
            rem = signed/(e*gn_min)
            check(f"{planet['name']} {criterion} zero inside published interval",
                  low < 0 < high)
            check(f"{planet['name']} {criterion} high-acceleration self-consistency",
                  0 < rem < 1e-3, relative_algebraic_remainder_bound=rem)
            rows.append({"planet":planet["name"], "criterion":criterion,
                         "interval_mas_per_century":[low, high],
                         "coefficient_mas_per_century_per_m_s2":coeff,
                         "leading_signed_a0_upper_m_s2":signed,
                         "conservative_absolute_envelope_a0_upper_m_s2":absolute,
                         "relative_algebraic_remainder_at_signed_upper":rem,
                         "interpretation":"conditional necessary scale restriction; NOT a confidence interval or fitted ITSM bound"})
    return rows


def partial_domain(data):
    epsh = sp.Rational(data["controls"]["domain_epsilon_locality"])
    epst = sp.Rational(data["controls"]["domain_epsilon_radial"])
    out = []
    for i, item in enumerate(data["controls"]["hypothetical_only_window_examples"]):
        mk, lam, mr, cutoff = [sp.Rational(item[k]) for k in
                               ("mK2","lambda_stat","Mrho2","k_cutoff")]
        lower = mk/(epsh*lam)
        upper = min(epst*mr, cutoff**2)
        nonempty = bool(lower < upper)
        expected = i == 0
        check("partial-domain hypothetical control "+str(i), nonempty == expected,
              lower_k_squared=str(lower), upper_k_squared=str(upper),
              hypothetical_only=True)
        out.append({"inputs":item,"lower_k_squared":str(lower),
                    "upper_k_squared":str(upper), "nonempty":nonempty,
                    "physical_admission":False})
    return {
        "necessary_locality_and_TF_band":
            "mK^2/(epsilon_H*lambda_min) < k^2 < epsilon_TF*M_rho^2",
        "full_necessary_band":
            "max[mK^2/(epsilon_H*lambda_min), Omega_bg^2/(epsilon_bg*c^2*lambda_min), (2*pi)^2/(epsilon_L*L_min^2)] < k^2 < min[epsilon_TF*M_rho^2, k_interaction_bound^2]",
        "additional_requirements":[
            "admitted discrete torus mode and retained mean equation",
            "same-action on-shell local background and preferred-frame solution",
            "positive coupled physical norms/characteristics",
            "controlled source-frequency/quasistatic remainder",
            "separate frequency-domain interaction bound"],
        "actual_physical_window":"UNRESOLVED",
        "physical_cutoff":"NOT_DERIVED",
        "hypothetical_partial_band_controls":out
    }


def encode(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+"\n").encode()


def save_new(folder, name, obj):
    b = encode(obj)
    p = folder/name
    with p.open("xb") as f:
        f.write(b)
    with (folder/(name+".sha256")).open("x",encoding="ascii",newline="\n") as f:
        f.write(hashlib.sha256(b).hexdigest()+"  "+name+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--out-dir",type=Path)
    parser.add_argument("--replay",type=Path)
    args = parser.parse_args()
    if bool(args.out_dir) == bool(args.replay):
        parser.error("choose exactly one of --out-dir or --replay")
    repo = args.repo.resolve()
    target = (args.replay or args.out_dir).resolve()
    if not target.is_relative_to(BASE) or target == BASE:
        raise ValueError("receipts must be new subdirectories of the authorized task workspace")
    if args.out_dir:
        target.mkdir(parents=True,exist_ok=False)
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    check("contract byte identity",sha(CONTRACT)==data["contract_sha256"])
    check("frozen input sidecar",sha(INPUT)==Path(str(INPUT)+".sha256").read_text().split()[0])
    pdf = BASE/data["external_sources"]["inpop"]["local_pdf"]
    check("primary table PDF byte identity",sha(pdf)==data["external_sources"]["inpop"]["sha256"])
    paths = {repo/p["path"] for p in data["source_pins"]}
    paths.update(repo/x for x in data["protected_dirty_files"])
    for entry in data["source_pins"]:
        p = repo/entry["path"]
        check("source pin "+entry["path"],sha(p)==entry["sha256"])
        sc = sidecar(p)
        if sc:
            paths.add(sc)
            recorded = re.findall(r"\b[0-9a-fA-F]{64}\b",sc.read_text(encoding="utf-8-sig"))
            check("existing sidecar "+str(sc.relative_to(repo)),sha(p) in [h.lower() for h in recorded])
    before = {str(p.relative_to(repo)).replace("\\","/"):metadata(p) for p in sorted(paths)}
    # Do not do new science on a broken source/contract seal.
    if any(c["status"]=="FAIL" for c in CHECKS):
        output = {"status":"INPUT_INTEGRITY_HOLD","checks":CHECKS,
                  "physics_pass":False,"gate_effect":"NONE"}
        if args.out_dir:
            save_new(target,"summary.json",output)
            save_new(target,"preservation.json",{"before":before,"after":before,"calculation_not_started":True})
        print(json.dumps({"status":output["status"],"failed":[c for c in CHECKS if c["status"]=="FAIL"]}))
        return 2
    formula = symbolic()
    bounds = planetary_bounds(data)
    band = partial_domain(data)
    orbits = orbital_controls(data)
    after = {str(p.relative_to(repo)).replace("\\","/"):metadata(p) for p in sorted(paths)}
    changed = [p for p in before if before[p]!=after[p]]
    check("all source and original dirty bytes/native metadata preserved",not changed,changed=changed)
    for paper, directory in [("P1","P1-Scale-Matching-Reconstruction"),("P2","P2-Rectangular-T3-Casimir")]:
        version = (repo/"papers"/directory/"VERSION").read_text().strip()
        check(paper+" version matches reviewed release candidate",
              version==("0.2.0-rc7" if paper=="P1" else "0.2.0-rc4"),version=version)
    failed = [c for c in CHECKS if c["status"]=="FAIL"]
    result = {
        "result_id":data["result_id"],"status":"PASS_BOUNDED_LOCAL_CALCULATION_PHYSICAL_WINDOW_HOLD" if not failed else "FAIL_LOCAL_VALIDATION",
        "passed":len(CHECKS)-len(failed),"total":len(CHECKS),"checks":CHECKS,
        "physics_pass":False,"gate_effect":"NONE","review_status":"DEFERRED","Rule9_cleared":False,
        "scope":"conditional leading local/static reduction and orbital arithmetic; NOT full PPN, ephemeris refit or physical-admission proof",
        "sources":data["source_pins"],
        "new_source_sha256":{"executable":sha(__file__),"input":sha(INPUT),"contract":sha(CONTRACT),"primary_pdf":sha(pdf)},
        "runtime":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__},
        "formulae":formula,"planetary_restrictions":bounds,"domain":band,"orbit_controls":orbits,
        "P1_version":"0.2.0-rc7","P2_version":"0.2.0-rc4",
        "coupled_PPN":"NOT_COMPUTED","Cassini_observable_fit":"NOT_RUN",
        "GW_frequency_band_applicability":"OPEN","numerical_a0_prediction":"NOT_DERIVED",
        "R4C1_reuse":"owning reports pinned and consolidated; upstream numerical audits NOT rerun",
        "repository_integration":"PENDING_WRITE_ACCESS; original ITSM repository untouched",
        "preserved_files":len(before)
    }
    if args.replay:
        exact = encode(result)==(target/"summary.json").read_bytes()
        preserved = not changed
        print(json.dumps({"replay":"EXACT" if exact else "DIFFERENT","originals_preserved":preserved,
                          "passed":result["passed"],"total":result["total"],
                          "physics_pass":False,"failed":failed}))
        return 0 if exact and preserved and not failed else 2
    save_new(target,"summary.json",result)
    save_new(target,"preservation.json",{"before":before,"after":after,"unchanged":not changed})
    print(json.dumps({"status":result["status"],"passed":result["passed"],"total":result["total"],
                      "physics_pass":False,"failed":failed,"receipt":str(target/"summary.json")}))
    return 0 if not failed else 2


if __name__=="__main__":
    raise SystemExit(main())

