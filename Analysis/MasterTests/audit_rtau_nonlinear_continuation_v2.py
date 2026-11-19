"""Extend the separate norm audit with exact variable-coefficient r energy."""
from pathlib import Path
import importlib.util
import hashlib
import json
import argparse
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/audit_rtau_nonlinear_continuation_v1.py'
SELF=Path(__file__).relative_to(ROOT).as_posix()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def energy_controls():
    t,z=s.symbols('t z',real=True)
    A,B,S,F,p,u=[s.Function(n)(t,z) for n in ['A','B','S','F','p','u']]
    D=lambda f:s.diff(f,z)
    pt=D(S*p+B*u)-F;ut=D(S*u+A*p)
    pz,uz=D(p),D(u)
    lhs=s.diff(A,t)*(p*p+pz*pz)/2+A*(p*pt+pz*D(pt))
    lhs+=s.diff(B,t)*(u*u+uz*uz)/2+B*(u*ut+uz*D(ut))
    Da=s.diff(A,t)-S*D(A);Db=s.diff(B,t)-S*D(B)
    rhs=(Da+A*D(S))*p*p/2+(Db+B*D(S))*u*u/2
    rhs+=(Da+3*A*D(S))*pz*pz/2+(Db+3*B*D(S))*uz*uz/2
    rhs+=D(A*B)*pz*uz+A*pz*(D(D(S))*p+D(D(B))*u)
    rhs+=B*uz*(D(D(S))*u+D(D(A))*p)-A*(p*F+pz*D(F))
    flux=S*(A*(p*p+pz*pz)+B*(u*u+uz*uz))/2+A*B*(p*u+pz*uz)
    residual=s.expand(lhs-rhs-D(flux))
    checks={'exact_variable_coefficient_first_derivative_energy_divergence':residual==0,
        'omitted_background_time_drift_detected':s.expand(residual+s.diff(A,t)*(p*p+pz*pz)/2)!=0,
        'omitted_coefficient_gradient_commutator_detected':s.expand(residual+D(A*B)*pz*uz)!=0,
        'omitted_second_spatial_coefficient_terms_detected':s.expand(residual+A*pz*D(D(B))*u+B*uz*D(D(A))*p)!=0,
        'omitted_condensate_potential_source_detected':s.expand(residual-A*(p*F+pz*D(F)))!=0}
    checks['u_Dr_compatibility_identity']=s.expand(ut-D(S*u+A*p))==0
    r0,U,V,m2,lam,g=s.symbols('r0 U V m2 lam g',real=True)
    potential=m2*r0*r0/2+lam*r0**4/4+g*(U*U+V*V)*r0*r0/4
    expected=m2*r0+lam*r0**3+g*(U*U+V*V)*r0/2
    checks['actual_neutral_potential_keeps_condensate_couplings']=s.expand(s.diff(potential,r0)-expected)==0
    x,y,a=s.symbols('x y a',positive=True)
    checks['weighted_cross_bound']=s.expand(x*x+y*y-2*x*y-(x-y)**2)==0
    checks['forcing_Young_bound']=s.expand(x*x+a*y*y/2-s.sqrt(2*a)*x*y-(x-s.sqrt(a/2)*y)**2)==0
    n=s.symbols('n',integer=True,positive=True)
    checks['r_H2_reconstruction_from_Dr_H1']=s.expand(2*n*n*(1+n*n)-(1+n*n)**2-(n**4-1))==0
    return checks

def calculate():
    spec=importlib.util.spec_from_file_location('separate_nonlinear_audit',ROOT/BASE)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=module.calculate()
    new=[SELF,BASE,'Analysis/MasterTests/outputs/rtau_nonlinear_continuation_audit_v1_20261119/receipt.json',
        'Theory/Gates/RES-001/RES001_RTAU_NONLINEAR_CONTINUATION_ENERGY_V1_SPEC_2026-11-19.md']
    snapshot={}
    for name in new:
        p=ROOT/name;side=Path(str(p)+'.sha256');h=digest(p)
        assert side.read_text(encoding='utf-8').split()[0]==h,name
        data['source_pins'][name]=h
        for q in (p,side):snapshot[q]=(digest(q),q.stat().st_mtime_ns)
    more=energy_controls()
    more['additional_sources_and_sidecars_preserved']=all((digest(q),q.stat().st_mtime_ns)==h for q,h in snapshot.items())
    data['checks'] += [{'name':n,'passed':bool(v)} for n,v in more.items()]
    data['coverage']+=';EXACT_NEUTRAL_SCALAR_FIRST_SPATIAL_DERIVATIVE_ENERGY_AND_OMISSION_CONTROLS'
    data['neutral_scalar_energy']='CONDITIONAL_COMPONENT_NOT_A_CLOSED_FULL_BACKGROUND_ESTIMATE'
    return data

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out');parser.add_argument('--replay');args=parser.parse_args()
    data=calculate();body=enc(data)
    if args.replay:assert (ROOT/args.replay).read_bytes()==body,'replay differs'
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);p=out/'receipt.json';p.write_bytes(body)
        Path(str(p)+'.sha256').write_bytes((digest(p)+'  '+p.relative_to(ROOT).as_posix()+'\n').encode())
    failures=[c['name'] for c in data['checks'] if not c['passed']]
    print(json.dumps({'passed':len(data['checks'])-len(failures),'total':len(data['checks']),
        'failures':failures,'pins':len(data['source_pins']),'physics_pass':False,'replay':bool(args.replay)}))
    assert not failures,failures
if __name__=='__main__':main()
