"""General planar fast commutator and coupled weak-coefficient estimates.

Conditional identities only: no actual background continuation is asserted.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/rtau_nonlinear_continuation_audit_v2_20261119/receipt.json'
GATE='Theory/Gates/RES-001/'
CONTRACT=GATE+'RES001_RTAU_COUPLED_REGULARITY_V1_CONTRACT_2026-11-19.md'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def zero(a):return all(s.simplify(x)==0 for x in a) if isinstance(a,s.MatrixBase) else s.simplify(a)==0

def force_controls():
    t,z=s.symbols('t z',real=True);beta,b=s.symbols('beta b',positive=True)
    k,alpha,l,psi=[s.Function(n)(t,z) for n in ['k','alpha','l','psi']]
    kap,a,vol,N=s.exp(k),s.exp(alpha),s.exp(l),s.exp(-beta*psi)
    d=b*N*vol*kap;ell=kap*(s.diff(l,z)+s.diff(k,z))
    A=s.Matrix([[0,kap*a],[-d,0]])
    B=s.Matrix([[0,-2*kap*s.diff(a,z)-ell*a],[s.diff(d,z)-beta*d*s.diff(psi,z),0]])
    H=s.diag(d/kap,a);omega=s.sqrt(b)*s.exp((-beta*psi+l+2*k+alpha)/2)
    checks={}
    checks['general_planar_d_geometry_identity']=zero(s.diff(d,z)/d-ell/kap+beta*s.diff(psi,z))
    checks['quartic_pair_positive_weight_algebra']=zero((H*A)+(H*A).T)
    checks['general_metric_base_energy_first_derivative_cancels']=zero(2*s.diff(H*A,z)+H*B-B.T*H)
    n=s.symbols('n',integer=True,nonnegative=True)
    Hn=omega**n*H
    commuted=B-n*s.diff(A,z)
    checks['all_integer_commutation_weight_identity']=zero(2*s.diff(Hn*A,z)+Hn*commuted-commuted.T*Hn)
    wrong=2*s.diff(H*A,z)+H*(B-s.diff(A,z))-(B-s.diff(A,z)).T*H
    checks['old_undifferentiated_weight_does_not_suffice']=not zero(wrong)
    checks['weight_uses_actual_quartic_frequency_coefficient']=zero(omega**2-kap*a*d)
    # Derive -Delta_h(aphi xi) directly for an arbitrary planar metric.
    xi=s.Function('xi')(z)
    lap=lambda f:-(s.diff(vol*kap*s.diff(f,z),z)/vol)
    expanded=s.expand(lap(a*xi))
    checks['full_metric_auxiliary_second_derivative_row']=zero(expanded.coeff(s.diff(xi,z,2))+kap*a)
    checks['full_metric_auxiliary_first_derivative_row']=zero(expanded.coeff(s.diff(xi,z))+2*kap*s.diff(a,z)+ell*a)
    Z=s.Function('Z')(z);ps=s.Function('psi0')(z);mu=s.Function('mu')(z);kk=s.Function('kk')(z)
    dd=b*s.exp(-beta*ps)*mu*kk
    reg=b*s.exp(-beta*ps)*mu*Z**2/2-dd*s.diff(Z,z)*s.diff(ps,z)+beta*dd*Z*s.diff(ps,z)**2
    euler=s.diff(reg,ps)-s.diff(s.diff(reg,s.diff(ps,z)),z)
    checks['general_regulator_second_derivative_row']=zero(s.expand(euler).coeff(s.diff(Z,z,2))-dd)
    checks['general_regulator_first_derivative_row']=zero(s.expand(euler).coeff(s.diff(Z,z))-s.diff(dd,z)+beta*dd*s.diff(ps,z))
    checks['dropping_lapse_regulator_term_is_detected']=not zero(
        s.expand(s.diff(reg-beta*dd*Z*s.diff(ps,z)**2,ps)
        -s.diff(s.diff(reg-beta*dd*Z*s.diff(ps,z)**2,s.diff(ps,z)),z)).coeff(s.diff(Z,z))
        -(s.diff(dd,z)-beta*dd*s.diff(ps,z)))
    return checks

def fourier_controls():
    # Small noncommuting matrix fixtures test identities of arbitrary dimension.
    I=s.I;dim=3;Z=s.zeros(dim)
    def add(*args):
        out={}
        for item in args:
            for k,v in item.items():out[k]=out.get(k,Z)+v
        return {k:v for k,v in out.items() if v!=Z}
    def scale(a,c):return {k:c*v for k,v in a.items()}
    def mul(a,b):
        out={}
        for k,v in a.items():
            for j,w in b.items():out[k+j]=out.get(k+j,Z)+v*w
        return {k:v for k,v in out.items() if v!=Z}
    def D(a):return {k:I*k*v for k,v in a.items() if k}
    def P(a):return {k:v/(I*k) for k,v in a.items() if k}
    def M(a):return {0:a[0]} if 0 in a and a[0]!=Z else {}
    def equal(a,b):return all(zero(add(a,scale(b,-1)).get(k,Z)) for k in set(a)|set(b))
    C={1:s.Matrix([[0,1,2],[3,0,0],[4,0,0]])/20,
       -1:s.Matrix([[0,2,-1],[1,0,0],[2,0,0]])/30}
    A={0:s.Matrix([[0,0,0],[0,0,2],[0,-3,0]]),1:s.diag(0,s.Rational(1,17),s.Rational(1,19))}
    B={0:s.Matrix([[1,2,3],[4,5,6],[7,8,9]])/7,-1:s.eye(3)/13}
    Bd={0:s.diag(1,2,3),1:s.eye(3)/11}
    U={0:s.eye(3),1:s.Matrix([[2,3,4],[0,1,2],[3,4,5]])/9,-2:s.eye(3)/5}
    T=lambda f:add(f,scale(P(mul(C,f)),I))
    checks={}
    checks['left_primitive_H1_commutator_keeps_all_means']=equal(add(D(T(U)),scale(T(D(U)),-1)),scale(P(mul(D(C),U)),I))
    checks['left_primitive_preserves_nonzero_means']=equal(M(T(U)),M(U))
    F=mul(C,A);Q=mul(C,B)
    Rmul=add(scale(D(F),I),scale(mul(A,D(C)),I),Q,scale(mul(Bd,C),-1))
    def R(f):
        return add(mul(Rmul,f),scale(M(mul(D(F),f)),-2*I),scale(P(mul(D(D(F)),f)),-I),
            scale(M(mul(Q,f)),-1),scale(P(mul(D(Q),f)),-1),mul(Bd,M(mul(C,f))))
    def Rc(f):
        return add(mul(D(Rmul),f),scale(M(mul(D(D(F)),f)),-2*I),scale(P(mul(D(D(D(F))),f)),-I),
            scale(M(mul(D(Q),f)),-1),scale(P(mul(D(D(Q)),f)),-1),
            mul(D(Bd),M(mul(C,f))),mul(Bd,M(mul(D(C),f))))
    checks['full_composition_H1_commutator_including_rank_terms']=equal(add(D(R(U)),scale(R(D(U)),-1)),Rc(U))
    dropped=lambda f:add(mul(Rmul,f),scale(P(mul(D(D(F)),f)),-I),scale(P(mul(D(Q),f)),-1))
    checks['dropping_finite_rank_terms_detected']=not equal(R(U),dropped(U))
    # D M_C - M_C D = M_{C_z}, not zero.
    checks['mean_commutator_sign']=equal(scale(M(mul(C,D(U))),-1),M(mul(D(C),U)))
    return checks

def coefficient_controls():
    checks={};x,y=s.symbols('x y',real=True)
    checks['cross_product_Young']=s.expand((x*x+y*y)/2-x*y-(x-y)**2/2)==0
    kap,A,B,N,v=s.symbols('kap A B N v',positive=True)
    checks['r_coefficients_volume_cancels_in_product']=s.simplify((N/v)*(N*v*kap)-N*N*kap)==0
    C,Sz,Cz=s.symbols('C Sz Cz',positive=True)
    checks['H1_inverse_triangle_bound']=s.expand(C*(1+C*Cz)-(C+C*C*Cz))==0
    # Conditional bounds evaluated only with the existing INITIAL chart values.
    c=s.Rational(2512053,1000000);cz=s.Rational(58385,1000000);cx=s.Rational(601920,1000000)
    initial={'T_H1_upper':str(1+cx+cz),'T_inverse_H1_upper':str(c*(1+c*cz)),
             'scope':'INITIAL_CHART_ONLY_NOT_FUTURE_BOUND'}
    checks['initial_H1_inverse_bound_finite']=c*(1+c*cz)<3
    r,U,V,mr,lam,g=s.symbols('r U V mr lam g',real=True)
    potential=mr*r*r/2+lam*r**4/4+g*(U*U+V*V)*r*r/4
    checks['actual_condensate_source_derivative']=s.expand(s.diff(potential,r)-(mr*r+lam*r**3+g*(U*U+V*V)*r/2))==0
    rr,uu,vv=s.Function('rr')(x),s.Function('uu')(x),s.Function('vv')(x)
    f=mr*rr+lam*rr**3+g*(uu*uu+vv*vv)*rr/2
    checks['actual_source_gradient_keeps_both_condensates']=s.expand(s.diff(f,x)-
        (mr+3*lam*rr**2+g*(uu*uu+vv*vv)/2)*s.diff(rr,x)-g*rr*(uu*s.diff(uu,x)+vv*s.diff(vv,x)))==0
    return checks,initial

def calculate():
    parent=json.loads((ROOT/PARENT).read_text(encoding='utf-8'));assert all(c['passed'] for c in parent['checks'])
    pins=dict(parent['source_pins'])
    for rel in [SELF,PARENT,CONTRACT,
        GATE+'RES001_RTAU_NONLINEAR_CONTINUATION_V2_REPORT_2026-11-19.md',
        GATE+'RES001_RTAU_MIXED_PRINCIPAL_ASSEMBLY_V1_REPORT_2026-11-04.md',
        GATE+'RES001_RTAU_PERIODIC_PRINCIPAL_COMPOSITION_V2_REPORT_2026-11-04.md',
        GATE+'RES001_RTAU_ACTUAL_FORCE_PAIR_V2_REPORT_2026-11-05.md']:
        h=digest(ROOT/rel);assert rel not in pins or pins[rel]==h,rel;pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;side=Path(str(p)+'.sha256');assert digest(p)==h,rel
        if not rel.endswith('.sha256'):assert side.read_text(encoding='utf-8').split()[0]==h,rel
        for q in (p,side) if side.exists() else (p,):snap[q]=(digest(q),q.stat().st_mtime_ns)
    checks=force_controls();checks.update(fourier_controls());more,initial=coefficient_controls();checks.update(more)
    checks['source_bytes_sidecars_mtimes_preserved']=all((digest(q),q.stat().st_mtime_ns)==h for q,h in snap.items())
    return {'source_pins':pins,'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
        'quartic_Hs_weight':'(kap*d*aphi)^(s/2)*diag(d/kap,aphi)',
        'initial_H1_chart':initial,
        'mathematical_scope':'GENERAL_PLANAR_FAST_PRINCIPAL_AND_PERIODIC_H1_IDENTITIES_PLUS_CONDITIONAL_COUPLED_WEAK_COEFFICIENT_BOUNDS',
        'general_ordinary_energy_continuation':'OPEN','actual_coupled_H1_remainder':'OPEN',
        'constraint_and_charge_domain_persistence':'OPEN','background_persistence':'OPEN',
        'time_interval_certified':None,'Rtau_adopted':False,'review':'DEFERRED',
        'Rule9_cleared':False,'physics_pass':False,'gate_effect':'NONE','G1_G6':'INCOMPLETE'}

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
