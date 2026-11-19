"""Separate exact audit: source extraction, Schur geometry and Fourier range."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse
import ast
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).relative_to(ROOT).as_posix()
PRIMARY='Analysis/MasterTests/outputs/rtau_nonlinear_continuation_v2_20261119/receipt.json'
RAW='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def product(a,b):
    keys={i+j for i in a for j in b}
    return {k:sum((v*b.get(k-i,F(0)) for i,v in a.items()),F(0)) for k in keys}
def mean_product(a,b):return sum((v*b.get(-k,F(0)) for k,v in a.items()),F(0))
def norm2(a):return sum(v*v for v in a.values())
def add(a,b,scale=F(1)):
    return {k:a.get(k,F(0))+scale*b.get(k,F(0)) for k in set(a)|set(b)}

def calculate():
    primary=json.loads((ROOT/PRIMARY).read_text(encoding='utf-8'))
    assert all(c['passed'] for c in primary['checks'])
    pins=dict(primary['source_pins'])
    for n in [SELF,PRIMARY]:pins[n]=digest(ROOT/n)
    snap={}
    for n,h in pins.items():
        p=ROOT/n;sc=Path(str(p)+'.sha256');assert digest(p)==h,n
        if not n.endswith('.sha256'):assert sc.read_text(encoding='utf-8').split()[0]==h,n
        for v in (p,sc) if sc.exists() else (p,):snap[v]=(digest(v),v.stat().st_mtime_ns)
    checks={}
    # Extract the neutral scalar's kinetic term from the original action source.
    tree=ast.parse((ROOT/RAW).read_text(encoding='utf-8-sig'))
    body=next(v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name=='body')
    can=next(v.value for v in body.body if isinstance(v,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='can' for t in v.targets))
    N,V,vr,S,rz,p,hzz=s.symbols('N V vr S rz p hzz',positive=True)
    scope={'gu':[[0]*4,[0]*4,[(vr-S*rz)/N,0,0,rz]],
           'gi':[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,hzz]],
           'dot':lambda a,b:sum(x*y for x,y in zip(a,b)),
           'mv':lambda a,b:[sum(x*y for x,y in zip(row,b)) for row in a]}
    extracted=s.simplify(N*V*eval(compile(ast.Expression(can),'original_can','eval'),scope))
    checks['original_source_neutral_scalar_kinetic_term']=s.simplify(extracted-(V*(vr-S*rz)**2/(2*N)-N*V*hzz*rz**2/2))==0
    uses={t.id for v in body.body if isinstance(v,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='gu' for k in ast.walk(v.value)) for t in v.targets if isinstance(t,ast.Name)}
    checks['original_gu_only_enters_current_and_can']=uses=={'current','can'}
    current=next(v.value for v in body.body if isinstance(v,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='current' for t in v.targets))
    checks['alignment_current_excludes_neutral_scalar']=all(
        isinstance(v.slice,ast.Constant) and v.slice.value in (0,1)
        for v in ast.walk(current) if isinstance(v,ast.Subscript) and isinstance(v.value,ast.Name) and v.value.id=='gu')
    canonical=s.simplify((extracted-p*(vr-S*rz)).subs(vr,S*rz+N*p/V))
    checks['extracted_current_momentum_Hessian']=s.diff(canonical,p,2)==-N/V
    a,b,d,mx,my,c,f=s.symbols('a b d mx my c f',real=True,nonzero=True)
    G=s.Matrix([[a,b],[b,d]]);m=s.Matrix([mx,my]);H=s.exp(f)*G+m*m.T/c
    h=H.row_join(m).col_join(s.Matrix([[mx,my,c]]))
    det=s.factor(h.det())
    checks['full_Schur_trace_determinant']=s.simplify(det-c*s.exp(2*f)*(a*d-b*b))==0
    hzz_exact=s.factor(H.det()/det)
    chi=(d*mx*mx-2*b*mx*my+a*my*my)/(c*c*(a*d-b*b))
    checks['inverse_longitudinal_metric_changes_under_trace']=s.simplify(hzz_exact-1/c-s.exp(-f)*chi)==0
    checks['inverse_longitudinal_metric_trace_derivative']=s.simplify(s.diff(hzz_exact,f).subs(f,0)+chi)==0
    # Substitute the full geometric path, not a fixed h^{zz} fixture.
    path=canonical.subs({V:V*s.exp(f),hzz:1/c+s.exp(-f)*chi})
    checks['full_scalar_trace_gradient_term']=s.simplify(s.diff(path,f).subs(f,0)-(N*p*p/(2*V)-N*V*rz*rz/(2*c)))==0
    n=s.symbols('n',integer=True,positive=True)
    k=s.symbols('k',integer=True,positive=True)
    moment=s.simplify(n*n/4+s.summation(k*k,(k,1,n-1))/2+(n*n+2*s.summation(k*k,(k,1,n-1)))/8)
    checks['closed_fourth_moment_count']=s.simplify(moment-(2*n**3+n)/8)==0
    for size in range(1,11):
        support=list(range(size,2*size))+list(range(-2*size+1,-size+1))
        pair=Counter(x+y for x in support for y in support)
        fourth=F(sum(v*v for v in pair.values()),16)
        checks[f'independent_ordered_quadruple_count_N{size}']=fourth==F(2*size**3+size,8)
    basis=[{0:F(1)},{-1:F(1,2),1:F(1,2),-2:F(1,2),2:F(1,2)},
           {-1:F(1,2),1:F(1,2),-3:F(1,2),3:F(1,2)}]
    gram=s.Matrix([[s.Rational(mean_product(x,y)) for y in basis] for x in basis])
    checks['range_projection_Gram_positive']=all(v>0 for v in [gram[0,0],gram[:2,:2].det(),gram.det()])
    for size in range(1,10):
        fn={k:F(1,2) for k in list(range(size,2*size))+list(range(-2*size+1,-size+1))}
        coef=gram.inv()*s.Matrix([s.Rational(mean_product(fn,b)) for b in basis])
        gn=dict(fn)
        for value,basis_fn in zip(coef,basis):gn=add(gn,basis_fn,-F(value))
        checks[f'exact_compatible_range_and_contraction_N{size}']=all(mean_product(gn,b)==0 for b in basis) and norm2(gn)<=norm2(fn)
    m=s.symbols('m',positive=True)
    a2=1/(2*m*m);b2=m**4/4+1/(8*m**12)
    checks['concentration_survives_removed_output_mean']=s.limit(b2-a2*a2,m,s.oo)==s.oo
    checks['higher_H1_norm_is_not_hidden_in_L2_bound']=s.limit(m**16*a2,m,s.oo)==s.oo
    # Sufficient H1 embedding: integral comparison bounds the entire tail.
    partial=sum(F(1,k*k) for k in range(1,65))
    checks['explicit_Fourier_embedding_tail_majorant']=1+2*(partial+F(1,64))<5
    s0=s.symbols('sigma',real=True)
    checks['sub_quarter_regularity_concentration_exponent']=s.simplify((3-4*(s.Rational(1,2)+s0))-(1-4*s0))==0
    checks['fixed_I_counterexample_not_claimed']=primary['fixed_I_U1_nonlinear_admission']=='NOT_PROVED_BY_THE_COUNTEREXAMPLE'
    checks['future_interval_not_claimed']=primary['time_interval_certified'] is None and primary['background_persistence']=='OPEN'
    checks['original_source_bytes_sidecars_mtimes_preserved']=all((digest(v),v.stat().st_mtime_ns)==h for v,h in snap.items())
    return {'source_pins':pins,'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
        'coverage':'SEPARATE_SOURCE_KINETIC_EXTRACTION_SCHUR_GEOMETRY_QUADRUPLE_COUNTS_RANGE_PROJECTIONS_NOT_SECOND_FULL_BACKGROUND_SOLVE',
        'review':'DEFERRED','Rule9_cleared':False,'physics_pass':False,'gate_effect':'NONE',
        'Rtau_adopted':False,'background_persistence':'OPEN','energy_persistence':'OPEN'}

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
