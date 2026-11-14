"""Independent periodic, all-frequency and rational-endpoint lift controls."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/rtau_strong_constraint_lift_v2_20261104/receipt.json'
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_CONSTRAINT_LIFT_AUDIT_V1_SPEC_2026-11-04.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rational(t):
    sign,man,exponent,_=t
    return (-1 if sign else 1)*Fraction(man)*(Fraction(2)**exponent)
def calculate():
    d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256'])
    for rel in (PARENT,SPEC,Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel,h in pins.items():
        p=ROOT/rel;assert sha(p)==h,rel
        for q in (p,Path(str(p)+'.sha256')):
            if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    check('parent_has_no_failed_component_controls',d['passed']==d['total']==79 and all(c['passed'] for c in d['checks']))
    check('parent_keeps_full_generator_and_time_holds',d['full_actual_generator_remainder']=='NOT_BOUNDED' and d['actual_time_tube']=='NOT_ESTABLISHED' and d['physics_pass'] is False)
    z=sp.symbols('z',real=True);n=sp.symbols('n',integer=True,positive=True)
    A=-2-sp.sin(z)/10;a1=sp.cos(2*z)/11;ell=-sp.Rational(3,4)+sp.sin(3*z)/17
    p=2+sp.cos(z)/7;f=3+sp.sin(z)/5
    # Nonlocal multiplication by mean(f) and the original primitive of f-mean.
    Kf=sp.cos(z)*3+(-sp.cos(z)/5)/13+f/19
    C=A*ell;g=sp.diff(f,z)-ell*p
    r=A*sp.diff(f,z,2)+a1*sp.diff(f,z)+Kf-sp.diff(C*p,z)
    rhs=r-a1*g-Kf+(sp.diff(A,z)-a1)*ell*p
    check('independent_periodic_nonlocal_gradient_identity',sp.expand(A*sp.diff(g,z)-rhs)==0)
    check('fixture_retains_nonzero_means',sp.integrate(p,(z,-sp.pi,sp.pi))/(2*sp.pi)==2 and sp.integrate(f,(z,-sp.pi,sp.pi))/(2*sp.pi)==3)
    mass=sp.Rational(473,400);cn=sp.Rational(7,5)
    # For p_n=e^(inz), L=-D^2+mass, and Lf=D(cn*p_n).
    fz=-cn*n*n/(n*n+mass);gcoef=sp.factor(fz+cn)
    check('exact_reference_high_frequency_lift',sp.simplify(gcoef-cn*mass/(n*n+mass))==0)
    polynomial=sp.Poly(sp.expand((n*n+mass)**2-(1+n*n)),n)
    check('all_integer_modes_H1_remainder_bound',all(x>=0 for x in polynomial.all_coeffs()) and polynomial.TC()>0)
    wrong=(1+n*n)*fz*fz
    check('omitted_leading_lift_has_unbounded_H1_norm',sp.limit(wrong/n**2,n,sp.oo)==cn*cn)
    check('wrong_leading_sign_has_unbounded_H1_norm',sp.limit((1+n*n)*(fz-cn)**2/n**2,n,sp.oo)==4*cn*cn)
    current_mean=-sp.Rational(2263,8400);physical_mean=current_mean-sp.Rational(1,5)
    check('density_measure_mean_shift_exact',physical_mean==-sp.Rational(3943,8400) and str(physical_mean)==d['reference_physical_density_mean_mass'])
    cells=d['cells'];intervals=[[rational(t) for t in c['z']] for c in cells]
    check('sixteen_cells_cover_without_internal_gaps',len(cells)==16 and intervals[0][0]==0 and all(intervals[i][1]>=intervals[i+1][0] for i in range(15)))
    reference=Fraction(8400,3943)
    for i,c in enumerate(cells):
        qhi=rational(c['Neumann_contraction'][1]);Ghi=rational(c['Green_bound'][1])
        check('exact_rational_Green_upper_cell_'+str(i),0<=qhi<1 and Ghi>=reference/(1-qhi))
    # Coverage endpoint must contain 2*pi; use a separately bounded rational pi.
    pi_lower=Fraction(314159265358979323846264338327950288419716939937510,10**50)
    pi_upper=pi_lower+Fraction(1,10**50)
    check('last_cell_reaches_full_circle',intervals[-1][1]>=2*pi_upper or intervals[-1][1]>=2*pi_lower and sp.N(sp.Rational(intervals[-1][1].numerator,intervals[-1][1].denominator)-2*sp.pi,90)>0)
    check('all_original_bytes_and_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
    return dict(kind='RTAU_STRONG_CONSTRAINT_LIFT_AUDIT_V1',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_sha256=pins,
        scope='SAME_AUTHOR_INDEPENDENT_PERIODIC_ALL_FREQUENCY_AND_EXACT_ARITHMETIC_CONTROLS_ONLY',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,
        full_actual_generator_remainder='NOT_BOUNDED',actual_time_tube='NOT_ESTABLISHED')
def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    if args.output:assert not args.output.parent.exists()
    data=calculate();raw=(json.dumps(data,sort_keys=True,indent=2)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],'physics_pass':False}))
    if data['passed']!=data['total']:raise SystemExit(1)
if __name__=='__main__':main()
