"""Independent exact principal-form interpretation and omission controls.

Same-author audit; not independent external review or physical clearance.
"""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_prepared_principal_v3_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()

def calculate():
 d=json.loads((ROOT/PARENT).read_text());assert SHA((ROOT/PARENT).read_bytes())=='9689901a50cf2a41f51dea63ce8bbf5f01b8a5fccdab92337d23a6ff7636f152'
 pins=dict(d['source_sha256']);snap={}
 for rel in (SELF,PARENT):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 check('parent_all_registered_checks_pass',d['passed']==d['total']==30 and all(c['passed'] is True for c in d['checks']))
 matrix=lambda key:s.Matrix([[s.Rational(x) for x in row] for row in d[key]])[:9,:9]
 M=matrix('reference_kinetic');B=matrix('reference_mixed');G=matrix('reference_gradient');C=B+B.T
 # This Fourier convention follows the real-space Euler equation directly:
 # M*q_tt+(B+B^T)*q_tz+G*q_zz=0.
 A=s.zeros(18);A[:9,9:]=s.eye(9);A[9:,:9]=M.inv()*G;A[9:,9:]=-s.I*M.inv()*C
 q0=s.zeros(9,1);q0[5]=1
 w0=q0.col_join(s.zeros(9,1));q1=s.zeros(9,1);q1[0]=q1[2]=2*s.I;w1=q1.col_join(q0)
 check('actual_reference_zero_eigenvector',A*w0==s.zeros(18,1))
 check('explicit_zero_Jordan_partner',A*w1==w0)
 check('zero_eigenvector_geometric_dimension_one',18-A.rank()==1)
 check('zero_generalized_kernel_dimension_two',18-(A*A).rank()==2)
 # It is not enough to add an arbitrary positive weight to the action energy.
 trace=s.zeros(9,1);trace[0]=trace[2]=1
 positive_gradient=(trace.T*G*trace)[0]
 static_energy=-positive_gradient/2
 tensor=s.zeros(9,1);tensor[1]=1
 tensor_energy=-(tensor.T*G*tensor)[0]/2
 check('reference_principal_gradient_energy_is_indefinite',static_energy<0 and tensor_energy>0,[str(static_energy),str(tensor_energy)])
 # Reconstruct the condensate amplitude/phase co-metric from the alignment action.
 c,gamma,Vz,t=s.symbols('c gamma Vz t',real=True)
 phase=(1+t)*(c*c-1)-t*(gamma*c-Vz)**2
 check('phase_reference_squared_speed_14_over_13',s.factor(phase.subs({gamma:1,Vz:0,t:s.Rational(1,13)}))==c*c-s.Rational(14,13))
 check('phase_time_kinetic_from_actual_cometric',s.expand(phase).coeff(c,2)==1+t-t*gamma**2)
 expected=c*c*(c*c-1)**4*(c*c-s.Rational(1,3))*(c*c-s.Rational(4,5))**2*(c*c-s.Rational(14,13))
 det=s.factor((c*c*M-c*C+G).det(method='domain-ge')/M.det())
 check('ordinary_polynomial_independently_reconstructed',s.expand(det-expected)==0)
 # Auxiliary elimination followed by fast response: both pieces must be present.
 a,b,m,k=s.symbols('a b m k',nonzero=True,real=True)
 slow=-a*a*k*k/m;coupling=s.I*a*b*k**3/m;fast=-b*b*k**4/m
 schur=s.simplify(slow-coupling*s.conjugate(coupling)/fast)
 check('k_cubed_mixing_cancels_induced_k_squared_stiffness',schur==0)
 check('omitted_mixing_leaves_spurious_stiffness',slow!=0)
 check('whole_root_relative_coercivity_strict',s.Rational(d['whole_root_relative_kinetic_error'])<1)
 check('whole_root_nonzero_minor_perturbation_strict',s.Rational(d['whole_root_dust_minor_perturbation'])<1)
 check('no_full_evolution_or_physical_clearance_claim',d['physics_pass'] is False and d['physical_symplectic_quotient']=='NOT_DERIVED' and d['strong_hyperbolicity']=='NOT_ESTABLISHED' and d['nonlinear_time_evolution'] is False)
 for f,(h,mt) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==mt
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_PREPARED_PRINCIPAL_AUDIT_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  reference_zero_eigenvector=[str(v) for v in w0],reference_zero_Jordan_partner=[str(v) for v in w1],reference_static_trace_energy_per_k_squared=str(static_energy),reference_static_tensor_energy_per_k_squared=str(tensor_energy),
  scope='exact reference principal interpretation plus retained whole-root inequalities; not a full physical norm or variable-coefficient theorem',review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
