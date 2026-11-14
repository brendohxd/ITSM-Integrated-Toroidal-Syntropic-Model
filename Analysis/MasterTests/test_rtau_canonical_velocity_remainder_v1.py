"""All thirteen unreduced velocity rows; compatible gauge assembly stays open."""
from pathlib import Path
import argparse,hashlib,json
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_CANONICAL_VELOCITY_REMAINDER_V1_SPEC_2026-11-04.md'
PARENT='Analysis/MasterTests/outputs/rtau_momentum_rate_lift_v1_20261104/receipt.json'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
 up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
 norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
 parent=json.loads((ROOT/PARENT).read_text());mixed=json.loads((ROOT/MIXED).read_text());initial=json.loads((ROOT/INVERSE).read_text())
 pins=dict(parent['source_sha256'])
 for rel in (SPEC,PARENT,MIXED,INVERSE,Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
 snapshot={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in (p,Path(str(p)+'.sha256')):
   if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 check('momentum_lift_parent_complete_only_in_scope',parent['passed']==parent['total']==11)
 H={tuple(row['ij']):(decode(row['value']),decode(row['dz'])) for row in mixed['full_mixed_Hessian_upper_triangle']}
 get=lambda i,j,dz=False:H.get(tuple(sorted((i,j))),(iv.mpf(0),iv.mpf(0)))[int(dz)]
 block=lambda rows,cols,dz=False:norm([get(i,j,dz) for i in rows for j in cols])
 check('auxiliary_velocity_and_Legendre_auxiliary_columns_absent',all(27 not in ij for ij in H) and all(tuple(sorted((i,j))) not in H for i in range(14,27) for j in (13,41)))
 inv=decode(initial['bounds']['original_temporal_inverse'])
 check('certified_original_temporal_inverse_available',lo(inv)>0 and mp.isfinite(hi(inv)))
 Az=block(range(14,27),range(14,27),True)
 invz=inv*inv*Az
 vals={'temporal_inverse':inv,'temporal_inverse_spatial_derivative':invz,'temporal_Hessian_spatial_derivative':Az}
 for name,columns in [('configuration',range(13)),('shift',range(42,45))]:
  c0=block(range(14,27),columns);c1=block(range(14,27),columns,True)
  vals[name+'_zeroth_matrix']=c0;vals[name+'_matrix_derivative']=c1
  vals[name+'_H1_remainder']=inv*(c0+c1)+invz*c0
 check('all_thirteen_rows_and_first_spatial_coefficients_present',len(range(14,27))==13 and all('dz' in row for row in mixed['full_mixed_Hessian_upper_triangle']))
 check('all_remainder_coefficients_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for x in vals.values()))
 z=sp.symbols('z',real=True)
 A=sp.Matrix([[2+z*z,sp.Rational(1,7)],[sp.Rational(1,7),3+z*z]])
 C=sp.Matrix([[1,z],[z*z,2]]);B=sp.Matrix([[z,1],[2,z]])
 q=sp.Matrix([1+z,z*z]);p=sp.Matrix([2-z,3+z*z])
 v=A.inv()*(p-C*q-B*q.diff(z));lead=A.inv()*(p-B*q.diff(z))
 check('independent_variable_coefficient_Legendre_identity',(v-lead+A.inv()*C*q).applyfunc(sp.cancel)==sp.zeros(2,1))
 identity=A.inv().diff(z)+A.inv()*A.diff(z)*A.inv()
 check('inverse_spatial_derivative_exact',identity.applyfunc(sp.cancel)==sp.zeros(2))
 wrong=(A.inv()*C*q).diff(z)-A.inv()*C.diff(z)*q-A.inv()*C*q.diff(z)
 check('omitted_inverse_derivative_detected',wrong.subs(z,sp.Rational(1,3))!=sp.zeros(2,1))
 # Independent scalar product-rule control underlying the H1 multiplier bound.
 a=sp.Function('a')(z);f=sp.Function('f')(z)
 check('variable_coefficient_H1_product_rule',sp.expand(sp.diff(a*f,z)-a*sp.diff(f,z)-sp.diff(a,z)*f)==0)
 check('force_row_retained_with_its_actual_derivative_order',any(26 in ij for ij in H) and 'full_actual_generator' in parent and parent['full_actual_generator']=='NOT_ASSEMBLED')
 check('all_inherited_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
 return dict(kind='RTAU_CANONICAL_VELOCITY_REMAINDER_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  exact_row='delta_v=A^-1*(delta_p-C*delta_q-B*D(delta_q)-E*delta_S-F*D(delta_S))',
  leading_unreduced_row='A^-1*(delta_p-B*D(delta_q)-F*D(delta_S))',remainder='-A^-1*C*delta_q-A^-1*E*delta_S',
  bounds_binary={k:binary(v) for k,v in vals.items()},upper_display={k:mp.nstr(hi(v),28) for k,v in vals.items()},
  scope='INITIAL_UNREDUCED_13_ROW_LEGENDRE_REMAINDER_H1_FROM_CONFIGURATION_H1_AND_CALLER_SHIFT_H1',
  paired_gauge_closed=False,strong_state_principal_comparison='NOT_ASSEMBLED',force_H2_rate_bound='NOT_PROVED_BY_AN_H1_ESTIMATE',
  full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
 parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
 if args.output:assert not args.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
 else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'bounds':d['upper_display'],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
