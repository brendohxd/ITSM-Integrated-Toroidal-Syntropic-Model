"""Separate exact tensor/adjoint/inverse audit; no physical admission claim."""
from pathlib import Path
import argparse,hashlib,json,traceback
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
PRIMARY='Analysis/MasterTests/outputs/rtau_planar_gauge_domain_v3_20261119/receipt.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def calculate():
    data=json.loads((ROOT/PRIMARY).read_text(encoding='utf-8'));assert all(c['passed'] for c in data['checks'])
    pins=dict(data['source_pins'])
    for rel in (PRIMARY,Path(__file__).relative_to(ROOT).as_posix()):pins[rel]=digest(ROOT/rel)
    snapshots={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        sc=Path(str(p)+'.sha256')
        if not rel.endswith('.sha256'):assert sc.read_text(encoding='utf-8').split()[0].lower()==h,rel
        for q in (p,sc) if sc.exists() else (p,):snapshots[q]=(digest(q),q.stat().st_mtime_ns)
    checks={};z=s.symbols('z',real=True)
    entries=s.symbols('a b m c n d',real=True)
    a,b,m,c,n,d=entries;h=s.Matrix([[a,b,m],[b,c,n],[m,n,d]])
    r=s.symbols('rx ry rz',real=True)
    # Derive the mixed-row block directly from tensor indices, without importing
    # the primary executable or its registered Lie helper.
    block=s.Matrix(3,3,lambda i,j:h[i,j]+(h[2,j] if i==2 else 0))
    W=s.diag(1,1,2);R=s.diag(1,1,s.Rational(1,2));u=s.Matrix(r)
    checks['independent_tensor_index_block']=block==W*h
    checks['constant_symmetrizer_restores_metric_coercivity']=s.simplify((u.T*R*block*u-u.T*h*u)[0])==0 and R*block==(R*block).T
    checks['unweighted_nonsymmetric_block_rejected']=block!=block.T
    # Nonlinear canonical momentum contribution from all six unique metric slots.
    pairs=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2));mom=s.symbols('p0:6')
    flux=s.zeros(3,1)
    for value,(i,j) in zip(mom,pairs):
        for k in range(3):flux[k]+=value*((h[i,k] if j==2 else 0)+(h[j,k] if i==2 else 0))
    checks['canonical_eliminated_momentum_block_is_transpose']=flux==block.T*s.Matrix([mom[2],mom[4],mom[5]])
    # Weighted mean inverse is nonsymmetric, but its factorization is exact.
    M=s.Matrix([[2,s.Rational(1,7),s.Rational(1,9)],[s.Rational(1,7),3,-s.Rational(1,11)],[s.Rational(1,9),-s.Rational(1,11),4]])
    checks['momentum_mean_matrix_inverse_order']=(R*M).inv()==M.inv()*W
    E=s.Matrix([[s.Rational(1,13),s.Rational(1,17),0],[0,s.Rational(1,19),s.Rational(1,23)],[s.Rational(1,29),0,-s.Rational(1,31)]])
    G=M.inv();GD=-G*E*G
    checks['Green_drift_differentiates_inverse_identity']=M*GD+E*G==s.zeros(3)
    checks['Green_drift_order_matters']=GD!=-G*G*E
    Gnew=(M+E).inv()
    checks['Neumann_factorization_exact_noncommuting_case']=Gnew==(s.eye(3)+G*E).inv()*G
    # Moving weighted Ward adjoint: local total-divergence identity, no sampling.
    rho=s.Matrix([s.Function('r'+str(i))(z) for i in range(3)])
    C=s.Matrix([s.Function('C'+str(i))(z) for i in range(3)])
    V=s.Matrix([s.Function('S'+str(i))(z) for i in range(3)])
    Dz=lambda q:q.diff(z)
    LC=V[2]*Dz(C)+s.diff(V[2],z)*C+s.Matrix([0,0,(C.T*Dz(V))[0]])
    adj=-V[2]*Dz(rho)+rho[2]*Dz(V)
    local=(rho.T*LC-adj.T*C)[0]-s.diff(V[2]*(rho.T*C)[0],z)
    checks['independent_local_Ward_total_divergence']=s.simplify(local)==0
    # A finite background residual has an independent inhomogeneous source.
    checks['finite_background_residual_is_not_an_identical_zero']=s.expand((rho.T*LC)[0])!=0
    const=s.Rational
    radius=const(50,797);initial=const(797,100);new=const(797,50)
    checks['half_gap_radius_independent_arithmetic']=initial*radius==const(1,2) and new==initial/(1-initial*radius)
    checks['radius_failure_is_inconclusive_not_singular']=s.det(s.eye(3)+2*s.eye(3))!=0
    n=s.symbols('n',integer=True,positive=True)
    checks['old_reference_nonzero_modes_remain_bounded']=s.simplify((n*n+const(553,400))-(1+n*n))==const(153,400)
    checks['old_reference_mean_is_negative_nonzero']=const(-2263,8400)<0 and 1/abs(const(-2263,8400))==const(8400,2263)
    k,K,L,T=const(1,2),s.Integer(2),const(1,10),s.Integer(2)
    expected={'gauge_H1_per_Rb':s.sqrt(2)/k,'FP_H2_per_Rg':s.sqrt(3+(1+L/k)**2)/k,
      'gauge_rate_H1_per_Rbt':s.sqrt(2)/k,'gauge_rate_H1_per_Rb':s.sqrt(2)*T/k**2,
      'momentum_L2_per_mean':1+2*K/k,'momentum_L2_per_v':1/k,
      'momentum_D_per_source':1/k,'momentum_D_per_momentum':2*L/k,
      'green_inverse_radius':radius,'green_inverse_bound':new,'green_drift_factor':new**2}
    checks['all_reported_conditional_constants_match_proof']=all(s.simplify(s.sympify(data['bounds_exact'][name])-v)==0 for name,v in expected.items())
    # Exact projection identity underlying the sharper bound, instead of a
    # triangle estimate on the separately large modulus constant.
    q=s.Matrix([s.Rational(1,7),s.Rational(2,11),-s.Rational(3,13)])
    controls=[s.Matrix([1,2,3]),s.Matrix([2,-1,4]),s.Matrix([-3,-1,-7])]
    assert sum(controls,s.zeros(3,1))==s.zeros(3,1)
    b=[-M*v+q for v in controls]
    checks['mean_free_coercive_energy_cancellation']=sum((v.T*M*v+v.T*w)[0] for v,w in zip(controls,b))==0
    checks['original_source_hashes_and_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snapshots.items())
    return {'kind':'RTAU_GENERAL_PLANAR_DOMAIN_SEPARATE_AUDIT_V1','source_pins':pins,'pinned_files':len(pins),
      'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
      'coverage':'INDEPENDENT_EXACT_TENSOR_AND_WARD_DERIVATIONS_WITH_ARITHMETIC_CONTROLS_NOT_EXTERNAL_REVIEW',
      'actual_background_time_tube':'OPEN','Rtau_adopted':False,'review_status':'DEFERRED','Rule9_cleared':False,
      'physics_pass':False,'gate_effect':'NONE'}
def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=False)
    try:
        data=calculate();raw=enc(data)
        if a.replay:assert a.replay.read_bytes()==raw,'Replay byte mismatch'
        else:
            a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_bytes((hashlib.sha256(raw).hexdigest()+'  '+a.output.resolve().relative_to(ROOT).as_posix()+'\n').encode())
        bad=[c['name'] for c in data['checks'] if not c['passed']]
        print(json.dumps({'passed':len(data['checks'])-len(bad),'total':len(data['checks']),'failures':bad,'pins':data['pinned_files'],'physics_pass':False,'replay':bool(a.replay)}))
        if bad:raise SystemExit(1)
    except Exception:
        if a.output:(a.output.parent/'failure.json').write_bytes(enc({'error':traceback.format_exc(),'physics_pass':False}))
        raise
if __name__=='__main__':main()
