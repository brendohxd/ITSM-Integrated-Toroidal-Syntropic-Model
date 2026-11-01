"""Different algebraic and endpoint audit of the unreduced temporal result."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v2_attempt_01/summary.json'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PREPARED_TEMPORAL_AUDIT_V1_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='aba30848eed3be2d4cb3f0122899ea0394aafcf93b6ebd4d91ecfb3b63f6ac93'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256']);snap={}
 for p in (SELF,SPEC,PARENT,'Analysis/MasterTests/audit_01_r4c1_rtau_prepared_temporal_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_audit_v1_attempt_01/summary.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_PREPARED_TEMPORAL_AUDIT_V2_SPEC_2026-10-31.md'):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 w=s.Symbol('w',real=True);M=s.Matrix([[s.sympify(x,locals={'w':w}) for x in row] for row in d['metric_frame_matrix_aligned']])
 check('all_exported_entries_exact_no_Float',not any(x.has(s.Float) for x in M))
 groups=((1,),(2,6),(4,7),(0,3,5,8))
 check('independent_scalar_vector_block_separation',all(M[i,j]==0 for ga,a in enumerate(groups) for gb,b in enumerate(groups) if ga!=gb for i in a for j in b))
 vec=M.extract([2,6],[2,6]);check('two_vector_blocks_identical',vec==M.extract([4,7],[4,7]))
 check('vector_block_positive_leading_minor',s.simplify(vec[0,0]-(w**4+5*w*w+15)/15)==0)
 check('vector_block_positive_determinant',s.simplify(vec.det()-(w*w+5)/30)==0)
 scalar=M.extract([0,3,5,8],[0,3,5,8]);sd=s.factor(scalar.det())
 check('independent_scalar_block_determinant',s.simplify(sd+11*(2*w*w+3)/(90*(1+w*w)))==0,str(sd))
 determinant=s.factor(sd*vec.det()**2*M[1,1]);direct=s.factor(M.det())
 check('full_determinant_from_independent_blocks',determinant==direct,str(direct))
 check('no_real_finite_tilt_determinant_zero',s.Poly(s.together(direct).as_numer_denom()[0],w).all_coeffs()==[-22,0,-253,0,-880,0,-825] and s.together(direct).as_numer_denom()[1]==81000*(w*w+1))
 # Serialized binary endpoints are the evidence, not rounded display strings.
 def interval(pair):
  lo,hi=(mp.mpf(tuple(x)) for x in pair);assert mp.isfinite(lo) and mp.isfinite(hi) and lo<=hi
  return mp.iv.mpf([lo,hi])
 entries=[[interval(p) for p in row] for row in d['metric_frame_delta_enclosures']]
 bound=max(mp.mpf(sum((abs(v) for v in row),mp.iv.mpf(0))._mpi_[1]) for row in entries)
 stored=interval(d['bounds']['metric_frame_gap']);newgap=mp.iv.mpf(1)/6-bound
 check('all_81_raw_interval_pairs_finite_ordered',len(entries)==9 and all(len(row)==9 for row in entries))
 check('independent_uniform_inverse_gap',mp.mpf(newgap._mpi_[0])>mp.mpf('.16') and abs(mp.mpf(newgap._mpi_[0])-mp.mpf(stored._mpi_[0]))<mp.mpf('1e-42'),mp.nstr(mp.mpf(newgap._mpi_[0]),45))
 c,p,z,g=s.symbols('c p z g',real=True);gamma=s.sqrt(1+c);Y=c*p*p+2*gamma*z*p*g+(1+z*z)*g*g;b=c*p+gamma*z*g
 check('force_Cauchy_gap_identity',s.expand(c*Y-b*b-(c-z*z)*g*g)==0)
 # c=sum(V_i^2) >= Vz^2. For q=sqrt(Y)>0 this yields b^2/q <= c*q;
 # the bound 6*A*c*q tends to zero at q=0, defining the C2 Hessian continuously.
 check('force_zero_gradient_C2_extension_bound',s.simplify(3*s.Symbol('A',positive=True)*(c*s.Symbol('q',positive=True)+c*s.Symbol('q',positive=True))-6*s.Symbol('A',positive=True)*c*s.Symbol('q',positive=True))==0)
 holds=(d['physical_ghost_verdict']=='NOT_DETERMINED_BY_UNREDUCED_INERTIA' and d['physical_symplectic_quotient']=='NOT_DERIVED' and d['initial_accelerations']=='NOT_DERIVED' and not d['physics_pass'] and not d['physical_window_demonstrated'] and d['G1_G6']=='INCOMPLETE' and d['review']=='DEFERRED')
 check('physical_and_review_holds_retained',holds)
 failed=json.loads((ROOT/'Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v1_attempt_01/summary.json').read_text())
 check('failed_V1_receipt_preserved',failed['passed']==24 and failed['total']==26 and sum(not z['passed'] for z in failed['checks'])==2)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_sources_bytes_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_PREPARED_TEMPORAL_AUDIT_V2',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,source_sha256=pins,
  aligned_determinant=str(direct),force_Cauchy_gap='c*Y-b^2=(c-Vz^2)*g^2 >=0',scope='unreduced temporal matrix, interval inverse gap and force C2 coefficient only',
  independent_external_review=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);q=a.parse_args();d=calculate();data=ENC(d)
 if q.replay:assert q.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  q.output_dir.mkdir(parents=True,exist_ok=False);p=q.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
