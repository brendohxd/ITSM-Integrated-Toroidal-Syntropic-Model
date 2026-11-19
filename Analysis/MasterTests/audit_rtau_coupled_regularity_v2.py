"""Extend the separate coupled audit with general planar curvature geometry."""
from pathlib import Path
import argparse
import importlib.util
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/audit_rtau_coupled_regularity_v1.py'
SELF=Path(__file__).relative_to(ROOT).as_posix()
SPEC='Theory/Gates/RES-001/RES001_RTAU_COUPLED_REGULARITY_WEAK_GEOMETRY_V1_SPEC_2026-11-19.md'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def zero(a):return all(s.simplify(v)==0 for v in a) if isinstance(a,s.MatrixBase) else s.simplify(a)==0

def extra_controls():
    checks={};a,b,d,mx,my,c=s.symbols('a b d mx my c',real=True,nonzero=True)
    G=s.Matrix([[a,b],[b,d]]);m=s.Matrix([mx,my]);Gi=G.inv();H=G+m*m.T/c
    kap=1/c+(m.T*Gi*m)[0]/c**2
    coefficient=Gi*m*m.T*Gi/c**2-kap*Gi
    checks['full_planar_curvature_flux_trace_identity']=zero(coefficient+kap*H.inv())
    checks['Schur_determinant_substitution_is_not_valid_at_mixed_moduli']=not zero(coefficient+kap*Gi)
    dh=s.Matrix([[s.Symbol('dx'),s.Symbol('dy')],[s.Symbol('dy'),s.Symbol('dz')]])
    checks['curvature_flux_contraction_is_log_transverse_determinant']=zero(s.trace(coefficient*dh)+kap*s.trace(H.inv()*dh))
    # Independent direct use of the original flux's Christoffel contraction.
    metric=H.row_join(m).col_join(s.Matrix([[mx,my,c]]));K=metric.inv()
    deriv=dh.row_join(s.zeros(2,1)).col_join(s.zeros(1,3))
    Gamma=[[[sum(K[i,l]*((deriv[l,k] if j==2 else 0)+(deriv[l,j] if k==2 else 0)-(deriv[j,k] if l==2 else 0))/2 for l in range(3)) for k in range(3)] for j in range(3)] for i in range(3)]
    raw=sum(K[i,j]*Gamma[2][i][j]-K[i,2]*Gamma[j][i][j] for i in range(3) for j in range(3))
    checks['original_weak_action_Christoffel_flux_matches']=zero(raw+kap*s.trace(H.inv()*dh))
    # The weak second-coefficient bounds are multilinear Holder/Young,
    # requiring H1 of the fields, not Linfinity of coefficient derivatives.
    X,Y,A,B,mu=s.symbols('X Y A B mu',positive=True)
    checks['weak_cross_estimate_Young_remainder']=zero((A+B)*(X*X+Y*Y)/2-(A+B)*X*Y-(A+B)*(X-Y)**2/2)
    checks['weak_shift_estimate_combined_field_bound']=zero(A*X*X+B*Y*Y-mu*(X*X+Y*Y)-((A-mu)*X*X+(B-mu)*Y*Y))
    # Relative inverse derivatives used in the scalar coefficient bounds.
    z=s.symbols('z');hh=s.Matrix([[2+z/7,z/11,s.Rational(1,13)],[z/11,3+z*z/17,s.Rational(1,19)],[s.Rational(1,13),s.Rational(1,19),4+z/23]])
    kk=hh.inv();kap0=kk[2,2];h0=hh.subs(z,0);k0=h0.inv();hz=s.diff(hh,z).subs(z,0);hzz=s.diff(hh,z,2).subs(z,0)
    e=s.Matrix([0,0,1]);v=k0*e
    checks['relative_longitudinal_inverse_first_rate']=zero(s.diff(kap0,z).subs(z,0)+(v.T*hz*v)[0])
    checks['relative_longitudinal_inverse_second_rate']=zero(s.diff(kap0,z,2).subs(z,0)-(2*v.T*hz*k0*hz*v-v.T*hzz*v)[0])
    return checks

def calculate():
    spec=importlib.util.spec_from_file_location('coupled_regularity_base_audit',ROOT/BASE)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);data=mod.calculate()
    snap={}
    for name in [SELF,BASE,SPEC,'Analysis/MasterTests/outputs/rtau_coupled_regularity_audit_v1_20261119/receipt.json']:
        p=ROOT/name;side=Path(str(p)+'.sha256');h=digest(p);assert side.read_text(encoding='utf-8').split()[0]==h,name
        data['source_pins'][name]=h
        for q in (p,side):snap[q]=(digest(q),q.stat().st_mtime_ns)
    checks=extra_controls()
    checks['extra_source_bytes_sidecars_mtimes_preserved']=all((digest(q),q.stat().st_mtime_ns)==h for q,h in snap.items())
    data['checks'] += [{'name':n,'passed':bool(v)} for n,v in checks.items()]
    data['coverage']+=';DIRECT_CHRISTOFFEL_CURVATURE_FLUX_AND_RELATIVE_INVERSE_GEOMETRY'
    return data

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out');parser.add_argument('--replay');args=parser.parse_args()
    data=calculate();body=enc(data)
    if args.replay:assert (ROOT/args.replay).read_bytes()==body,'replay differs'
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);p=out/'receipt.json';p.write_bytes(body)
        Path(str(p)+'.sha256').write_bytes((digest(p)+'  '+p.relative_to(ROOT).as_posix()+'\n').encode())
    failed=[c['name'] for c in data['checks'] if not c['passed']]
    print(json.dumps({'passed':len(data['checks'])-len(failed),'total':len(data['checks']),'failures':failed,
        'pins':len(data['source_pins']),'physics_pass':False,'replay':bool(args.replay)}));assert not failed,failed
if __name__=='__main__':main()
