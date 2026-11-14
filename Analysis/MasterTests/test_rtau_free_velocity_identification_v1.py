"""Canonical/gauge versus action-Schur velocity coefficients; remainder open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_FREE_VELOCITY_IDENTIFICATION_V1_SPEC_2026-11-04.md'
PARENT='Analysis/MasterTests/outputs/rtau_paired_gauge_rate_v2_20261104/receipt.json'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
PRINCIPAL='Analysis/MasterTests/outputs/r4c1_rtau_prepared_principal_v3_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
I=[0,1,3,6,7,8,9,10,11,12]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
 parent,mixed,principal=[json.loads((ROOT/p).read_text()) for p in (PARENT,MIXED,PRINCIPAL)]
 pins=dict(parent['source_sha256'])
 for rel in (SPEC,PARENT,MIXED,PRINCIPAL,FACTORY,Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
 snap={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in (p,Path(str(p)+'.sha256')):
   if q.exists():snap[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 check('paired_gauge_parent_complete_in_scope',parent['passed']==parent['total']==15)
 # Noncommuting rational coefficient fixture, not a physical background.
 E=sp.eye(5)[:,:3];W=sp.eye(5)[3:,:]
 B=sp.Matrix([[sp.Rational(1,7),sp.Rational(1,13)],[sp.Rational(2,11),-sp.Rational(1,17)],[sp.Rational(3,19),sp.Rational(2,23)],[2,0],[0,3]])
 A=sp.diag(2,3,4,5,6)
 for j in range(4):A[j,j+1]=A[j+1,j]=sp.Rational(j+1,29)
 D=sp.Matrix(5,5,lambda i,j:sp.Rational(2*i-j+1,31+i+j))
 Pi=sp.eye(5)-B*(W*B).inv()*W;K=B.T*A*B
 M=E.T*(A-A*B*K.inv()*B.T*A)*E
 C=E.T*(D-A*B*K.inv()*B.T*D)*E
 Q=E.T*Pi*A.inv()*Pi.T*E
 check('exact_noncommuting_inverse_gauge_Schur_identity',Q==M.inv())
 check('exact_configuration_gradient_identity',E.T*Pi*A.inv()*D*E==M.inv()*C)
 check('canonical_momentum_lift_satisfies_leading_constraint',B.T*Pi.T*E==sp.zeros(2,3))
 U=E.row_join(B);upper=E.T*Pi
 check('universal_basis_factorization_control',upper*U==sp.eye(5)[:3,:])
 check('rational_fixture_is_not_accidentally_block_diagonal',E.T*A*B!=sp.zeros(3,2))
 s=sp.Rational(1,37)
 check('material_advection_coefficient_shift_exact',M.inv()*(C+s*M)==M.inv()*C+s*sp.eye(3))
 H={tuple(row['ij']):decode(row['value']) for row in mixed['full_mixed_Hessian_upper_triangle']}
 get=lambda i,j:H.get(tuple(sorted((i,j))),iv.mpf(0))
 sub=lambda rows,cols:[[get(i,j) for j in cols] for i in rows]
 tr=lambda a:[list(row) for row in zip(*a)]
 mul=lambda a,b:[[sum((a[i][k]*b[k][j] for k in range(len(b))),iv.mpf(0)) for j in range(len(b[0]))] for i in range(len(a))]
 add=lambda a,b:[[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
 neg=lambda a:[[-x for x in row] for row in a]
 contains=lambda x:lo(x)<=0<=hi(x)
 spec=importlib.util.spec_from_file_location('identified_velocity_profiles',ROOT/FACTORY)
 fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
 y,_=env['state'](env['J'].variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
 Bg=[[iv.mpf(0) for _ in range(3)] for _ in range(13)]
 for j,slot in enumerate((2,4,5)):
  Bg[slot][j]=y[0].c[0]*(2 if j==2 else 1);Bg[6+j][j]=-y[8].c[0]
 Aall=sub(range(14,27),range(14,27));Dall=sub(range(14,27),range(28,41))
 T=sub(range(14,27),range(45,48));Ks=sub(range(45,48),range(45,48));Ds=sub(range(45,48),range(28,41))
 check('cached_velocity_shift_covariance_enclosures_consistent',all(contains(x) for row in add(T,mul(Aall,Bg)) for x in row))
 check('cached_shift_kinetic_covariance_enclosures_consistent',all(contains(x) for row in add(Ks,neg(mul(mul(tr(Bg),Aall),Bg))) for x in row))
 check('cached_shift_gradient_covariance_enclosures_consistent',all(contains(x) for row in add(Ds,mul(tr(Bg),Dall)) for x in row))
 KI=[[decode(v) for v in row] for row in principal['whole_root_shift_inverse']]
 vv=[14+i for i in I];dd=[28+i for i in I];ss=range(45,48)
 Tv=sub(vv,ss)
 Meff=add(sub(vv,vv),neg(mul(mul(Tv,KI),tr(Tv))))
 Beff=add(sub(vv,dd),neg(mul(mul(Tv,KI),sub(ss,dd))))
 Brel=[[Beff[i][j]+y[44].c[0]*Meff[i][j] for j in range(10)] for i in range(10)]
 check('force_temporal_slot_kept_and_decoupled_as_in_action',all(get(14+i,26)==0 for i in range(12)) and all(get(26,j)==0 for j in (45,46,47)))
 check('ten_free_field_coefficient_blocks_include_force',len(Meff)==10 and I[-1]==12)
 check('all_effective_coefficient_bounds_finite',all(mp.isfinite(hi(v)) and mp.isfinite(lo(v)) for matrix in (Meff,Beff,Brel) for row in matrix for v in row))
 check('all_inherited_source_bytes_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snap.items()))
 return dict(kind='RTAU_FREE_VELOCITY_IDENTIFICATION_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,free_field_slots=I,
  kinetic_binary=[[binary(x) for x in row] for row in Meff],mixed_binary=[[binary(x) for x in row] for row in Beff],material_mixed_binary=[[binary(x) for x in row] for row in Brel],
  coefficient_identity='E^T*Pi*A^-1*Pi^T*E=M_eff^-1; E^T*Pi*A^-1*D*E=M_eff^-1*B_eff',
  exact_proof_basis='U=[E,B], upper rows U^-1=E^T*Pi; invert U^T*A*U by its Schur complement',
  scope='POINTWISE_ACTUAL_CANONICAL_GAUGE_FREE_VELOCITY_LEADING_COEFFICIENT_IDENTIFICATION_ONLY',
  interval_consistency_is_not_identity_proof=True,strong_velocity_remainder='NOT_ASSEMBLED',full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
 parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=parser.parse_args()
 if args.output:assert not args.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
 else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
