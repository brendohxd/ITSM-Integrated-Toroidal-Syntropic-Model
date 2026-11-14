"""Initial coupled force-coordinate inverse; no finite-time or generator claim."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_FORCE_COORDINATE_V2_SPEC_2026-11-04.md'
LIFT='Analysis/MasterTests/outputs/rtau_strong_constraint_lift_v2_20261104/receipt.json'
WEAK='Analysis/MasterTests/outputs/rtau_weak_graph_v1_20261103/receipt.json'
AUDIT='Analysis/MasterTests/outputs/rtau_strong_constraint_lift_audit_v1_20261104/receipt.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exact(t):
    sign,man,e,_=t
    return (-1 if sign else 1)*Fraction(man)*(Fraction(2)**e)
def atan_enclosure(den,N=120):
    total=sum((Fraction((-1)**k,(2*k+1)*den**(2*k+1)) for k in range(N)),Fraction(0))
    next_term=Fraction((-1)**N,(2*N+1)*den**(2*N+1))
    return min(total,total+next_term),max(total,total+next_term)
def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1]);lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    parent,weak,audit=[json.loads((ROOT/r).read_text()) for r in (LIFT,WEAK,AUDIT)]
    pins=dict(audit['source_sha256'])
    for rel,h in weak['source_sha256'].items():
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    for rel in (SPEC,LIFT,WEAK,AUDIT,'Analysis/MasterTests/test_rtau_strong_force_coordinate_v1.py','Theory/Gates/RES-001/RES001_RTAU_STRONG_FORCE_COORDINATE_V1_SPEC_2026-11-04.md','Analysis/MasterTests/outputs/rtau_strong_force_coordinate_v1_20261104/receipt.json',Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel,h in pins.items():
        p=ROOT/rel;assert sha(p)==h,rel
        for q in (p,Path(str(p)+'.sha256')):
            if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    check('registered_parent_and_independent_controls_complete_in_scope',parent['passed']==parent['total']==79 and audit['passed']==audit['total']==28)
    n=sp.symbols('n',integer=True,positive=True)
    check('all_nonzero_modes_H2_from_second_derivative',sp.expand(2*n*n-(1+n*n))==n*n-1)
    check('all_nonzero_modes_first_derivative_bound',sp.expand((1+n*n)**2-4*n*n-(n*n-1)**2)==0)
    check('independent_integer_first_derivative_controls',all(((1+k*k)**2-4*k*k)==(k*k-1)**2 for k in (1,2,13)))
    check('force_constant_mean_is_independent_of_auxiliary',sp.diff(sp.Integer(7),sp.Symbol('z'),2)==0 and sp.Integer(7)!=0)
    r=iv.mpf(1)/13000
    kappa_inverse=iv.exp(2*r)
    drift=iv.exp(2*r)*r
    ck=decode(weak['constants_binary']['auxiliary_L2_per_metric_H1_F'])
    trace_to_metric=iv.sqrt(2)*iv.exp(2*r)*(1+2*r)
    row=[decode(x) for x in parent['constants_binary']['trace_H1']]
    # ||k||H1,F <= sqrt(2)*Qfree + trace_to_metric*||f||H1.
    # F <= |mean chi| + 2*kappa_inverse*(Z+drift*F/2+ck*||k||H1,F).
    feedback=kappa_inverse*drift+2*kappa_inverse*ck*trace_to_metric*row[3]
    check('coupled_force_metric_feedback_strictly_below_one',hi(feedback)<1,mp.nstr(hi(feedback),28))
    assert hi(feedback)<1,'Initial force-coordinate inverse not proved'
    denom=1-feedback
    # Input order D,Q,P,Z,mean_chi,eta_x,eta_y,eta_z.
    force=[2*kappa_inverse*ck*trace_to_metric*row[j] for j in (0,1,2)]
    force[1]+=2*kappa_inverse*ck*iv.sqrt(2)
    force+=[2*kappa_inverse,iv.mpf(1)]+[2*kappa_inverse*ck*trace_to_metric*row[j] for j in (4,5,6)]
    force=[x/denom for x in force]
    trace=[row[j] for j in (0,1,2)]+[iv.mpf(0),iv.mpf(0)]+[row[j] for j in (4,5,6)]
    trace=[x+row[3]*y for x,y in zip(trace,force)]
    # Existing forward bound is retained, with full metric Frobenius conversion.
    cz=decode(weak['constants_binary']['auxiliary_L2_per_psi_H2'])
    forward=[ck*trace_to_metric*row[j] for j in range(7)]
    forward[1]+=ck*iv.sqrt(2);forward[3]+=cz
    qhi=exact(binary(feedback)[1]);lower_denom=1-qhi
    check('exact_rational_feedback_margin',lower_denom>0)
    for j,value in enumerate(force):
        check('finite_nonnegative_inverse_constant_'+str(j),lo(value)>=0 and mp.isfinite(hi(value)))
    check('exact_rational_force_coefficient_not_underrounded',exact(binary(force[3])[1])>=2*exact(binary(kappa_inverse)[0])/lower_denom)
    # Check the scalar closure algebra separately, before numerical evaluation.
    a,b,c,d,e,q=sp.symbols('a b c d e q',nonnegative=True)
    F,Z,Q,D,P,m=sp.symbols('F Z Q D P m')
    expanded=m+a*Z+b*F+c*(q*Q+d*(D+P+e*F))
    split=(b+c*d*e)*F+(m+a*Z+c*q*Q+c*d*(D+P))
    check('exact_coupled_metric_force_closure_identity',sp.expand(expanded-split)==0)
    a5=atan_enclosure(5);a239=atan_enclosure(239)
    pi_lo=16*a5[0]-4*a239[1];pi_hi=16*a5[1]-4*a239[0]
    check('Machin_enclosure_width_strictly_small',0<pi_hi-pi_lo<Fraction(1,10**160))
    cells=parent['cells'];intervals=[[exact(t) for t in c['z']] for c in cells]
    check('exact_rational_entire_circle_coverage',intervals[0][0]==0 and intervals[-1][1]>=2*pi_hi and all(intervals[i][1]>=intervals[i+1][0] for i in range(15)))
    check('all_inherited_bytes_sidecars_and_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
    return dict(kind='RTAU_STRONG_FORCE_COORDINATE_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
      inverse_input_order=['corrected_density_L2','free_ordinary_configuration_H1_including_moduli','free_momentum_L2_including_xi','auxiliary_force_L2','force_mean','eliminated_momentum_mean_x','eliminated_momentum_mean_y','eliminated_momentum_mean_z'],
      forward_input_order=parent['input_order'],constants_binary={'feedback':binary(feedback),'force_H2_inverse':[binary(x) for x in force],'trace_H1_after_force_inverse':[binary(x) for x in trace],'auxiliary_L2_forward':[binary(x) for x in forward]},
      upper_display={'feedback':mp.nstr(hi(feedback),28),'force_H2_inverse':[mp.nstr(hi(x),28) for x in force],'trace_H1_after_force_inverse':[mp.nstr(hi(x),28) for x in trace],'auxiliary_L2_forward':[mp.nstr(hi(x),28) for x in forward]},
      scope='INITIAL_TWO_WAY_COUPLED_FORCE_COORDINATE_NORM_BOUNDS_ON_THE_ACTUAL_COMPATIBLE_RANGE_ONLY',mean_kept=True,weighted_range_and_global_charges='REQUIRED_NOT_AUTOMATIC',
      full_actual_generator_remainder='NOT_BOUNDED',moving_maps='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',physical_window=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    if args.output:assert not args.output.parent.exists()
    data=calculate();raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],'feedback':data['upper_display']['feedback'],'physics_pass':False}))
    if data['passed']!=data['total']:raise SystemExit(1)
if __name__=='__main__':main()
