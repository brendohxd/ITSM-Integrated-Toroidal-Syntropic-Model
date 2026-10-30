"""Independent V1 verification: Binet angle evolution, not Cartesian time flow.

Does not import the primary executable or original P0 numerical implementation.
Writes only a new verification receipt; peer review remains deferred.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

BASE = Path(__file__).resolve().parent


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def binet(a0, e, cfg):
    h2 = 1-e*e
    def rhs(phi, z):
        u, up = z
        # Binet u''+u = g(1/u)/(h^2 u^2), using direct positive quadratic root.
        ratio = (1+math.sqrt(1+4*a0/(u*u)))/2
        return [up, ratio/h2-u]
    def maximum(phi, z):
        return z[1]
    maximum.direction = -1
    sol = solve_ivp(rhs, (0, cfg["orbits"]*2*math.pi), (1/(1-e),0),
                    events=maximum, method=cfg["method"], rtol=cfg["rtol"],
                    atol=cfg["atol"], max_step=cfg["max_step"])
    events = sol.t_events[0][sol.t_events[0]>0.2]
    drift = float(np.mean(np.diff(events)-2*math.pi))
    return bool(sol.success), len(events), drift


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary",type=Path,required=True)
    parser.add_argument("--primary-script",type=Path,required=True)
    parser.add_argument("--out-dir",type=Path)
    parser.add_argument("--replay",type=Path)
    args = parser.parse_args()
    if bool(args.out_dir)==bool(args.replay):
        parser.error("choose exactly one of --out-dir or --replay")
    target = (args.out_dir or args.replay).resolve()
    if not target.is_relative_to(BASE) or target==BASE:
        raise ValueError("output must be a new task-workspace subdirectory")
    if args.out_dir:
        target.mkdir(parents=True,exist_ok=False)
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    data = json.loads((BASE/"frozen_inputs_v1.json").read_text(encoding="utf-8"))
    checks = []
    def add(name, ok, **detail):
        checks.append({"name":name,"status":"PASS" if bool(ok) else "FAIL",
                       "details":detail})
    add("primary has no failed or unknown computational checks",
        bool(primary.get("checks")) and all(c["status"]=="PASS" for c in primary["checks"]))
    add("primary source identity",primary.get("new_source_sha256",{}).get("executable")==digest(args.primary_script))
    add("same frozen input",primary.get("new_source_sha256",{}).get("input")==digest(BASE/"frozen_inputs_v1.json"))
    if not all(c["status"]=="PASS" for c in checks):
        result = {"status":"HOLD_PRIMARY_NOT_VERIFIED","checks":checks,"physics_pass":False}
    else:
        rows = []
        for case in primary["orbit_controls"]:
            ok, events, drift = binet(case["a0"], case["eccentricity"], data["controls"]["binet"])
            delta = drift-case["precession_per_orbit"]
            add(f"Binet versus Cartesian e={case['eccentricity']} a0={case['a0']}",
                ok and events>=4 and abs(delta)<data["controls"]["tolerances"]["independent_absolute"],
                binet_precession_per_orbit=drift, Cartesian_difference=delta, events=events)
            rows.append({"eccentricity":case["eccentricity"],"a0":case["a0"],
                         "precession_per_orbit":drift,"difference":delta})
        constants = data["external_sources"]["constants"]
        gm = float(constants["GM_sun_m3_s2"])
        seconds = float(constants["days_per_julian_century"])*float(constants["seconds_per_day"])
        angular_mas = 180*3600000/math.pi
        bounds = []
        for planet in data["planets"]:
            rad = float(planet["a_AU"])*float(constants["AU_m"])
            e = float(planet["eccentricity"])
            # Independent form from A_R sqrt[a(1-e^2)/(GM)].
            coeff = math.sqrt(rad*(1-e*e)/gm)*seconds*angular_mas
            for crit, interval in planet["intervals_mas_century"].items():
                expected = -interval[0]/coeff
                actual = next(x for x in primary["planetary_restrictions"]
                              if x["planet"]==planet["name"] and x["criterion"]==crit)
                add(planet["name"]+" "+crit+" independent SI conversion",
                    math.isclose(expected,actual["leading_signed_a0_upper_m_s2"],rel_tol=2e-14),
                    recomputed_a0_upper_m_s2=expected)
                # An outward-force sign would incorrectly select the other end.
                add(planet["name"]+" "+crit+" inward sign retained",
                    actual["interval_mas_per_century"][0]==interval[0] and
                    actual["leading_signed_a0_upper_m_s2"]>0)
                bounds.append({"planet":planet["name"],"criterion":crit,"a0_upper_m_s2":expected})
        add("no Gaussian or forecast substitution",
            data["external_sources"]["inpop20a"]["bepicolombo_forecast_used"] is False
            and "NOT Gaussian" in data["external_sources"]["inpop"]["interpretation"])
        add("scope retained despite successful arithmetic",
            primary["physics_pass"] is False and primary["gate_effect"]=="NONE"
            and primary["domain"]["actual_physical_window"]=="UNRESOLVED"
            and primary["Cassini_observable_fit"]=="NOT_RUN")
        result = {"status":"PASS_INDEPENDENT_LOCAL_CONTROL" if all(c["status"]=="PASS" for c in checks) else "FAIL_INDEPENDENT_CONTROL",
                  "checks":checks,"orbits":rows,"bounds":bounds,"physics_pass":False,
                  "gate_effect":"NONE","review_status":"DEFERRED","Rule9_cleared":False,
                  "independent_peer_review":False}
    failed = [c for c in checks if c["status"]!="PASS"]
    result.update({"passed":len(checks)-len(failed),"total":len(checks),
                   "primary_summary_sha256":digest(args.primary),"verifier_sha256":digest(__file__),
                   "input_sha256":digest(BASE/"frozen_inputs_v1.json")})
    encoded = (json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    if args.replay:
        exact = encoded==(target/"verification.json").read_bytes()
        print(json.dumps({"replay":"EXACT" if exact else "DIFFERENT","failed":failed,
                          "passed":result["passed"],"total":result["total"],"physics_pass":False}))
        return 0 if exact and not failed else 2
    with (target/"verification.json").open("xb") as f:
        f.write(encoded)
    with (target/"verification.json.sha256").open("x",encoding="ascii",newline="\n") as f:
        f.write(hashlib.sha256(encoded).hexdigest()+"  verification.json\n")
    print(json.dumps({"status":result["status"],"passed":result["passed"],"total":result["total"],
                      "failed":failed,"physics_pass":False}))
    return 0 if not failed else 2


if __name__=="__main__":
    raise SystemExit(main())

