"""Explicit post-run GR dust consistency control, not preregistered/healthy-GR proof."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"Analysis/MasterTests/outputs"
PINS={
    "Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/summary.json":
        "1f13df62495f3a39198b697a7387f14086338306a8a5e24462b1e873800f1b5a",
    "Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/formulas.json":
        "f634e510fd6e04f51f0c2c6cc1f43d284b0b0c9e5d9c44d4a3b4de9d8a35e87f",
    "Analysis/MasterTests/test_01_r4c1_g3_zero_evolution.py":
        "31e753b1f4cf965e4998e3acb035b646252d1b5615db75ea3331b1e3ba76d059",
}


def sha(content):return hashlib.sha256(content).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: "+name)


def evaluate():
    verify(PINS)
    parent=json.loads((OUT/"r4c1_g3e_attempt_01/summary.json").read_bytes())
    inherited={**parent["source_sha256"],**parent["transitive_source_sha256"]}
    verify(inherited)
    raw=json.loads((OUT/"r4c1_g3e_attempt_01/formulas.json").read_bytes())
    eta,a,H,pd,rho=s.symbols("eta a H psi_dot rho_m",positive=True)
    ud,vd,rd=s.symbols("u_dot v_dot r_dot",real=True)
    symbols={str(x):x for x in (eta,a,H,pd,rho,ud,vd,rd)}
    parse=lambda text:s.sympify(text,locals=symbols)
    mass=parse(raw["normalized_coefficients"][0]);beta=2*eta**2/5
    Hd=-6*(ud**2+vd**2+rd**2+3*eta*pd**2+rho)/(12-eta)
    pdd=-3*H*pd-2*eta*rho/15
    compact=-H**2/4-Hd/2-6*rho/(12-eta)+beta*(pdd+H*pd)-beta**2*pd**2
    checks=[]
    def exact(name,expression):
        vals=list(expression) if isinstance(expression,s.MatrixBase) else [expression]
        residual=[s.factor(s.cancel(val)) for val in vals]
        ok=all(val==0 for val in residual)
        checks.append(dict(name=name,passed=bool(ok),residual="zero_exact" if ok else list(map(str,residual))))
    exact("compact_evolving_mass",mass-compact)
    N=s.sqrt(eta)*s.Matrix([[parse(val) for val in raw["physical_leading_maps"][key]]
                           for key in ("density_contrast","comoving_dust_divergence")])
    N=N.applyfunc(lambda val:s.factor(s.cancel(val)))
    exact("normalized_physical_map_determinant",N.det()-(12-eta)/(a**4*rho))
    dust={eta:0,ud:0,vd:0,rd:0,pd:0,rho:3*H**2}
    exact("Einstein_dust_mass_boundary",mass.subs(dust)+H**2)
    density_row=N[0,:].applyfunc(lambda val:s.limit(val,eta,0,dir="+")).subs(rho,3*H**2)
    expected=s.Matrix([[-s.sqrt(6)/(3*a**s.Rational(5,2)*H),
                         2*s.sqrt(6)/(3*a**s.Rational(5,2)*H**2)]])
    exact("GR_density_map_from_actual_export",density_row-expected)
    chi,chid=s.symbols("chi chidot",real=True)
    density=(density_row*s.Matrix([chi,chid]))[0]
    flow={a:a*H,H:-3*H**2/2,chi:chid,chid:H**2*chi}
    dt=lambda expr:sum(s.diff(expr,z)*fz for z,fz in flow.items())
    exact("GR_density_growth_equation",dt(dt(density))+2*H*dt(density)-3*H**2*density/2)
    H0=s.Symbol("H_ref",positive=True)
    for power in (s.Integer(2),-s.Rational(1,2)):
        exact("canonical_power_"+str(power),(power**2-3*power/2-1)*H**2)
        physical=density.subs({chi:a**power,chid:power*H*a**power},simultaneous=True).subs(H,H0/a**s.Rational(3,2))
        exact("density_power_"+str(power-1),physical-s.sqrt(6)*(2*power-1)*a**(power-1)/(3*H0))
    passed=sum(check["passed"] for check in checks)
    return dict(schema="r4c1-g3e-postrun-gr-density-v1",validation="PASS_LOCAL_CHECKS" if passed==len(checks) else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(checks),checks=checks,source_sha256=PINS,transitive_source_sha256=inherited,
        script_sha256=sha(Path(__file__).read_bytes()),runtime=dict(python=platform.python_version(),sympy=s.__version__),
        timing="Explicit post-run analytic consistency control, not preregistered",
        physical_amplitude="X= sqrt(eta)*chi/k; eta constant on each member",
        normalized_physical_map=[[str(val) for val in row] for row in N.tolist()],
        boundary_density=str(s.factor(density)),boundary_canonical_equation="chiddot-H^2*chi=0",
        boundary_density_equation="Dddot+2H*Ddot-(rho_m/2)*D=0; rho_m=3H^2; MP2=1",
        density_powers=["a","a^(-3/2)"],status="CONDITIONAL_RECONSTRUCTED_GR_DUST_LIMIT_CONTROL_ONLY",
        physics_pass=False,full_IVP_verified=False,healthy_continuous_GR_limit_verified=False,
        physical_EFT_cutoff_derived=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        review_status="DEFERRED",Rule9_cleared=False,gate_effect="NONE")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3e_gr_attempt_01")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    result=evaluate();payload=(json.dumps(result,indent=2,allow_nan=False)+"\n").encode("utf-8")
    same=None
    if args.replay:
        same=(directory/"summary.json").read_bytes()==payload
        print(json.dumps(dict(replay=True,byte_identical=same,summary_sha256=sha(payload))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        (directory/"summary.json").write_bytes(payload)
        (directory/"summary.json.sha256").write_text(sha(payload)+"  summary.json\n",encoding="ascii")
    print(json.dumps({key:result[key] for key in ("validation","passed","total","status","physics_pass")}))
    for check in result["checks"]:
        if not check["passed"]:print(json.dumps(check))
    if args.replay and not same:return 2
    return 0 if result["passed"]==result["total"] else 1


if __name__=="__main__":raise SystemExit(main())
