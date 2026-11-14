"""Exact audit of rho/Sigma substitution; no numerical physics clearance."""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_SIGMA_RECONSTRUCTION_REPAIR_V1_CONTRACT_2026-11-04.md'
BASE='Analysis/MasterTests/outputs/rtau_ordinary_momentum_remainder_v2_20261104/receipt.json'
OWNERS=[
 'Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md',
 'Theory/Gates/RES-001/RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_REPORT_2026-11-03.md',
 'Analysis/MasterTests/test_rtau_strong_constraint_lift_v2.py',
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
    inherited=json.loads((ROOT/BASE).read_text())['source_sha256']
    pins=dict(inherited)
    for rel in [BASE,CONTRACT,*OWNERS,Path(__file__).relative_to(ROOT).as_posix()]:
        if rel in pins:assert pins[rel]==sha(ROOT/rel),rel
        pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel,want in pins.items():
        p=ROOT/rel;assert sha(p)==want,rel
        for q in [p,Path(str(p)+'.sha256')]:
            if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
    checks=[]
    def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
    mu,M,p,b,Z,rho=sp.symbols('mu M p b Z rho',nonzero=True)
    dmu,dM,dp,dq,ds,dpi,dZ,drho,dSigma=sp.symbols('dmu dM dp dq ds dpi dZ drho dSigma')
    f,fp,fpp,fpq,fps,fq,fs=sp.symbols('f fp fpp fpq fps fq fs')
    # Multivariate first jet: no equation of motion or f specialization.
    de=p*fpp*dp+(p*fpq-fq)*dq+(p*fps-fs)*ds
    dpi_formula=mu*(fpp*dp+fpq*dq+fps*ds)+fp*dmu
    canonical=p*dpi/mu-p*fp*dmu/mu-fq*dq-fs*ds
    check('generic_canonical_Legendre_differential',sp.expand(canonical.subs(dpi,dpi_formula)-de)==0)
    energy=p*fp-f
    Sigma=rho+energy+b*Z**2/2
    actual=M*drho+rho*dM
    correct=(M*dSigma+rho*dM-M*(canonical+b*Z*dZ))
    check('correct_total_current_differential',sp.expand(correct.subs(dSigma,drho+canonical+b*Z*dZ)-actual)==0)
    other=M*dSigma+Sigma*dM
    check('compensated_current_is_different',sp.expand(other-(M*dSigma+rho*dM))!=0)
    wrong=M*dSigma+rho*dM
    check('wrong_map_missing_term_exact',sp.expand(correct-wrong+M*(canonical+b*Z*dZ))==0)
    # Pure canonical variation, fixed metric/field/auxiliary: defect=-N*p*dpi.
    N=sp.symbols('N',nonzero=True)
    fixture=sp.expand((correct-wrong).subs({dmu:0,dq:0,ds:0,dZ:0,M:N*mu}))
    check('nonzero_omission_rejection_control',sp.simplify(fixture+N*p*dpi)==0 and fixture!=0)
    z=sp.symbols('z',real=True)
    check('mean_free_countercontrol_retains_zero_integrated_first_variation',sp.integrate(sp.cos(z),(z,0,2*sp.pi))==0)
    check('regulator_first_variation_not_discarded',sp.diff(correct,dZ)==-M*b*Z)
    check('measure_first_variation_not_discarded',sp.diff(correct,dM)==rho)
    # Reference is an algebraic rest-control only, not a new admitted solution.
    rho0=sp.Rational(1,5);pfp0=sp.Rational(3,25);e0=pfp0/2
    sigma0=rho0+e0
    nm=sp.Rational(553,400)-rho0-pfp0
    mm=-sp.Rational(2263,8400)-rho0-pfp0
    check('reference_compensated_density_differs_from_rho',sigma0==sp.Rational(13,50))
    check('corrected_reference_nonzero_mass',nm==sp.Rational(17,16))
    check('corrected_reference_mean_mass',mm==-sp.Rational(4951,8400))
    check('reference_mean_not_deleted',mm<0 and mm!=0)
    check('preserved_sources_and_sidecars_unchanged',all(sha(q)==h and q.stat().st_mtime_ns==t for q,(h,t) in snapshot.items()))
    return dict(kind='RTAU_SIGMA_COORDINATE_DEFECT_V1',source_sha256=pins,
        passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        scope='EXACT_COORDINATE_DEFECT_AND_REFERENCE_CONTROL_ONLY',
        defect='Strong reconstruction V2 substituted Sigma for rho in delta I_total',
        omitted_term='-M*(delta e_force+b*Z*delta Z)',
        canonical_energy_differential='(p/mu)*delta pi-p*f_p*delta mu/mu-sum(f_q*delta q)-f_s*delta s',
        corrected_reference=dict(nonzero_mass=str(nm),mean_mass=str(mm),Sigma=str(sigma0)),
        reconstruction_repair='NOT_YET_CERTIFIED',dependent_bounds='HOLD_SUBSTANTIVE',
        physics_pass=False,review='DEFERRED',gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=ap.parse_args()
    if a.output:assert not a.output.parent.exists(),'Fresh directory required'
    data=calculate();raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if a.output:
        a.output.parent.mkdir(parents=True);a.output.write_bytes(raw)
        Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
    else:assert a.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({k:data[k] for k in ['kind','passed','total','scope','dependent_bounds','physics_pass']}))
    if data['passed']!=data['total']:raise SystemExit(1)
if __name__=='__main__':main()
