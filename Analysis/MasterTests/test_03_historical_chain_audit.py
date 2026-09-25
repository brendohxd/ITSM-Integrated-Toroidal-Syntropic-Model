"""Check the exact v7.2 transcription's broken circulation-to-acceleration chain."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as s

from tests_01_03_symbolic_audit import Audit, digest

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "Theory/Gates/ITSM_TEST_03_HISTORICAL_CHAIN_ADDENDUM_2026-09-25.md"
SOURCE = ROOT / "Theory/History/FullArchive/manuscripts/09_v6.1-v7.2-2026-03-09/v7.2_source.md"
SOURCE_SHA = "6069e4959dc8038d14de3c6489a7cc87f4d7acc53ed323443a63966e48730aa1"


def main():
    if digest(SOURCE) != SOURCE_SHA:
        raise RuntimeError("Frozen transcription changed; inspect source before rerunning")
    a = Audit()
    c,H,L,v,t,Gamma = s.symbols("c H L v t Gamma",positive=True)
    kappa,ell = c**2/H,c/H
    first = kappa/(2*s.pi*ell)
    middle = c**2/(2*s.pi*ell)
    a.check("stated_definitions_give_speed",first-c/(2*s.pi))
    a.check("printed_middle_gives_acceleration",middle-c*H/(2*s.pi))
    a.check("missing_frequency_factor",middle/first-H)
    # Exponents of L,T, independently computed from the declared dimensions.
    dim_c,dim_H = s.Matrix([1,-1]),s.Matrix([0,-1])
    dim_kappa,dim_ell = 2*dim_c-dim_H,dim_c-dim_H
    dim_first,dim_middle = dim_kappa-dim_ell,2*dim_c-dim_ell
    a.check("first_length_exponent",dim_first[0]-1)
    a.check("first_time_exponent_not_acceleration",dim_first[1]-(-2),True)
    a.check("middle_time_exponent",dim_middle[1]-(-2))
    a.check("ratio_time_exponent",(dim_middle-dim_first)[1]-(-1))
    # Straight-line covering coordinate; flat connection is zero. Coordinate
    # identification does not add acceleration at the edge of a chart.
    x = v*t
    a.check("flat_T3_cycle_acceleration",s.diff(x,t,2))
    circulation = s.integrate(v,(s.Symbol("x"),0,L))
    a.check("nonzero_cycle_circulation",circulation.subs({v:1,L:1}),True)
    a.check("fixed_circulation_sets_speed_not_acceleration",circulation.subs(v,Gamma/L)-Gamma)
    a.record(status="REJECT_HISTORICAL_CIRCULATION_CHAIN_NO_UNIQUE_CCHI",
             first_member=first,printed_middle=middle,ratio=middle/first,
             dimensions_first="L T^-1 (speed)",dimensions_middle="L T^-2 (acceleration)",
             source_lines="57,61,65",source_kind="available source.md transcription; original PDF not verified",
             topology_control="flat periodic geodesic; nonzero circulation, zero intrinsic spatial acceleration",
             independent_Cchi="NOT_DERIVED",observational_input="NONE")
    passed = all(row["passed"] for row in a.checks)
    payload = {"test":3,"addendum":"historical_chain","checks":a.checks,"results":a.results,
               "local_symbolic_validation":"PASS" if passed else "FAIL",
               "source_integrity_verified":True,
               "source_sha256":{"transcription":digest(SOURCE),"contract":digest(CONTRACT),
                                "executable":digest(Path(__file__)),
                                "shared_helper":digest(Path(__file__).with_name("tests_01_03_symbolic_audit.py"))},
               "runtime":{"python":sys.version.split()[0],"sympy":s.__version__},
               "physics_pass":False,"canonical_test_complete":False,"gate_effect":"NONE","Rule9":"NOT_COMPLETED"}
    target = Path(__file__).parent/"outputs/test_03_historical_chain_audit.json"
    target.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for path in (target,CONTRACT,Path(__file__)):
        path.with_suffix(path.suffix+".sha256").write_text(f"{digest(path)}  {path.name}\n",encoding="ascii")
    print(json.dumps({"validation":payload["local_symbolic_validation"],"passed":sum(row["passed"] for row in a.checks),
                      "total":len(a.checks),"status":a.results["status"],"first_member":str(first),
                      "middle_member":str(middle),"sha256":digest(target)}))
    if not passed:
        print(json.dumps([row for row in a.checks if not row["passed"]],indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
