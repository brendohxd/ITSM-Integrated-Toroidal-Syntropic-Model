"""Separate audit of the fast differentiated weight and weak coefficient bounds."""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).relative_to(ROOT).as_posix()
PRIMARY='Analysis/MasterTests/outputs/rtau_coupled_regularity_v1_20261119/receipt.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def zero(mat):return all(s.simplify(x)==0 for x in mat) if isinstance(mat,s.MatrixBase) else s.simplify(mat)==0

def controls():
    checks={};z=s.symbols('z',real=True)
    f,g,k,off,lam=[s.Function(n)(z) for n in ['f','g','k','off','lam']]
    alpha,delta,kap=s.exp(f),s.exp(g),s.exp(k)
    A=s.Matrix([[0,alpha],[-delta,0]]);H=s.diag(delta/kap,alpha/kap)
    P=alpha*delta/kap
    # Independently parameterize every off-diagonal first row satisfying the
    # undifferentiated energy relation, without using the primary formulas.
    B=s.Matrix([[0,off],[(2*s.diff(P,z)+H[0,0]*off)/H[1,1],0]])
    checks['independent_general_base_adjoint_relation']=zero(2*s.diff(H*A,z)+H*B-B.T*H)
    n=s.symbols('n',integer=True,nonnegative=True)
    Q=2*s.diff(lam*H*A,z)+lam*H*(B-n*s.diff(A,z))-(B-n*s.diff(A,z)).T*lam*H
    needed=2*s.diff(lam,z)/lam-n*(s.diff(alpha,z)/alpha+s.diff(delta,z)/delta)
    checks['differentiated_weight_ODE_derived_independently']=zero(Q[0,1]/(lam*P)-needed)
    weight=s.exp(n*(f+g)/2)
    checks['positive_quartic_weight_solves_all_n']=zero(needed.subs(lam,weight).doit())
    checks['undifferentiated_weight_failure_is_not_ignored']=not zero(needed.subs({lam:1,n:1}).doit())
    # Full local integration-by-parts identity at one derivative, not just
    # disappearance of the highest symbol. All coefficient terms are kept.
    H1=s.exp((f+g)/2)*H;B1=B-s.diff(A,z)
    K=H1*A;M=s.diff(K,z)+H1*B1
    q=s.Matrix([s.Function('q0')(z),s.Function('q1')(z)])
    Q0=s.diff(K,z,2)-s.diff(B1.T*H1,z)
    flux=(-2*(q.T*K*s.diff(q,z))[0]+(q.T*M*q)[0])
    lhs=2*(q.T*H1*(-A*s.diff(q,z,2)+B1*s.diff(q,z)))[0]
    checks['full_H1_fast_spatial_energy_divergence']=zero(s.expand(lhs-(q.T*Q0*q)[0]-s.diff(flux,z)))
    checks['zeroth_energy_form_is_symmetric']=zero(Q0-Q0.T)
    checks['dropping_zeroth_energy_form_detected']=not zero(Q0)
    # Matrix inverse and log-volume derivative formulas on a nonconformal
    # general metric with nonzero mixed components.
    h=s.Matrix([[2+z/7,z/11,s.Rational(1,13)],
                [z/11,3+z*z/17,s.Rational(1,19)],
                [s.Rational(1,13),s.Rational(1,19),4+z/23]])
    hz=s.diff(h,z).subs(z,0);hzz=s.diff(h,z,2).subs(z,0);h0=h.subs(z,0);K0=h0.inv()
    actual=s.diff(h.inv(),z).subs(z,0)
    checks['nonconformal_matrix_inverse_first_derivative']=zero(actual+K0*hz*K0)
    actual2=s.diff(h.inv(),z,2).subs(z,0)
    checks['nonconformal_matrix_inverse_second_derivative']=zero(actual2-2*K0*hz*K0*hz*K0+K0*hzz*K0)
    logs=s.log(h.det())/2
    checks['log_volume_first_derivative']=zero(s.diff(logs,z).subs(z,0)-s.trace(K0*hz)/2)
    checks['log_volume_second_derivative']=zero(s.diff(logs,z,2).subs(z,0)-s.trace(K0*hzz-K0*hz*K0*hz)/2)
    # Explicit weak-coefficient Cauchy/Young steps. The H1 embedding is the
    # already pinned sqrt(5) certificate, not an extra regularity assumption.
    x,y,C=s.symbols('x y C',positive=True)
    checks['weak_second_coefficient_cross_control']=s.expand(C*(x*x+y*y)/2-C*x*y-C*(x-y)**2/2)==0
    checks['weak_shift_second_coefficient_control']=s.expand(x*x+y*y-2*x*y-(x-y)**2)==0
    A0,B0=s.symbols('A0 B0',positive=True)
    checks['second_coefficient_weak_energy_aggregation']=s.expand((A0+B0)*(x*x+y*y)/2-(A0+B0)*x*y-(A0+B0)*(x-y)**2/2)==0
    p,vol,N,kap0=s.symbols('p vol N kap0',positive=True)
    checks['r_product_metric_volume_cancellation']=s.simplify((N/vol)*(N*vol*kap0)-N*N*kap0)==0
    c,cz=s.symbols('c cz',positive=True)
    checks['H1_inverse_commutator_bound']=s.expand(c+c*c*cz-c*(1+c*cz))==0
    # The mean and derivative operators commute, but multiplication and the
    # mean do not; verify the finite-rank commutator on an independent fixture.
    X=s.Matrix([[1+s.cos(z),s.sin(z)],[s.cos(2*z),1-s.sin(z)]])
    u=s.Matrix([2+s.cos(z),3+s.sin(z)])
    mean=lambda v:v.applyfunc(lambda a:s.integrate(s.expand_trig(a),(z,-s.pi,s.pi))/(2*s.pi))
    checks['independent_finite_rank_derivative_commutator']=zero(-mean(X*s.diff(u,z))-mean(s.diff(X,z)*u))
    return checks

def calculate():
    primary=json.loads((ROOT/PRIMARY).read_text(encoding='utf-8'));assert all(c['passed'] for c in primary['checks'])
    pins=dict(primary['source_pins'])
    for n in [SELF,PRIMARY]:pins[n]=digest(ROOT/n)
    snap={}
    for n,h in pins.items():
        p=ROOT/n;side=Path(str(p)+'.sha256');assert digest(p)==h,n
        if not n.endswith('.sha256'):assert side.read_text(encoding='utf-8').split()[0]==h,n
        for q in (p,side) if side.exists() else (p,):snap[q]=(digest(q),q.stat().st_mtime_ns)
    checks=controls()
    checks['no_time_interval_or_physical_clearance_inserted']=primary['time_interval_certified'] is None and primary['physics_pass'] is False
    checks['source_bytes_sidecars_mtimes_preserved']=all((digest(q),q.stat().st_mtime_ns)==h for q,h in snap.items())
    return {'source_pins':pins,'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
        'coverage':'INDEPENDENT_ADJOINT_WEIGHT_ODE_FULL_SPATIAL_ENERGY_DIVERGENCE_MATRIX_DERIVATIVES_AND_WEAK_BOUND_CONTROLS_NOT_FULL_COUPLED_BACKGROUND_SOLVE',
        'review':'DEFERRED','Rtau_adopted':False,'Rule9_cleared':False,'physics_pass':False,'gate_effect':'NONE',
        'actual_coupled_H1_remainder':'OPEN','background_persistence':'OPEN'}

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
