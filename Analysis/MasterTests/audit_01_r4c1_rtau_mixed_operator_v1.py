"""Independent variational identities and full coefficient endpoint audit."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_MIXED_OPERATOR_AUDIT_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='d916402a0751fa4a0409d2048ed4e38ea18dd9b5629836f6a3517fdd44e0b577'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256']);snap={}
 for p in (SELF,SPEC,PARENT):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 def endpoints(pair):
  a,b=(mp.mpf(tuple(v)) for v in pair);assert mp.isfinite(a) and mp.isfinite(b) and a<=b;return a,b
 records=d['full_mixed_Hessian_upper_triangle'];indices=[tuple(r['ij']) for r in records]
 for r in records:endpoints(r['value']);endpoints(r['dz'])
 for r in d['initial_affine_forcing']:endpoints(r)
 yl,yh=endpoints(d['rest_gradient_squared_lower'])
 check('all_1399_coefficient_derivative_forcing_domain_pairs_finite',len(records)==692 and len(d['initial_affine_forcing'])==14)
 check('upper_triangle_unique_ordered_complete_schema',len(indices)==len(set(indices)) and all(0<=i<=j<48 for i,j in indices) and 'exactly zero' in d['implicit_other_entries'])
 check('force_rest_norm_positive_before_C3_use',yl>mp.mpf('7.3e-12'))
 check('auxiliary_velocity_all_temporal_coefficients_exact_zero',all(27 not in ij for ij in indices))
 check('no_auxiliary_rate_assumption_enters_other_momenta',all(tuple(sorted((14+i,k))) not in indices for i in range(13) for k in (13,41)))
 a,b=endpoints(d['initial_affine_forcing'][13]);check('auxiliary_initial_Euler_interval_contains_zero',a<=0<=b)
 # Independent lapse-map curvature; these terms are not J^T H J.
 beta,psi,dp=s.symbols('beta psi dp',real=True);N=s.exp(-beta*psi);Nz=-beta*N*dp
 check('lapse_map_second_derivative',s.simplify(s.diff(N,psi,2)-beta**2*N)==0)
 check('lapse_gradient_map_second_derivatives',s.simplify(s.diff(Nz,psi,2)-beta**2*Nz)==0 and s.simplify(s.diff(Nz,psi,dp)-beta**2*N)==0)
 z=s.Symbol('z',real=True)
 A=s.Matrix(2,2,lambda i,j:s.Function('a'+str(i)+str(j))(z));B=s.Matrix(2,2,lambda i,j:s.Function('b'+str(i)+str(j))(z))
 x=s.Matrix([s.Function('x0')(z),s.Function('x1')(z)]);y=s.Matrix([s.Function('y0')(z),s.Function('y1')(z)])
 K0=A-A.T+B.T.diff(z);K1=B+B.T
 check('variable_coefficient_two_form_formal_skew_adjoint',(K0+K0.T-K1.diff(z)).applyfunc(s.simplify)==s.zeros(2))
 primitive=(x.T*(A*y+B*y.diff(z))-(A*x+B*x.diff(z)).T*y)[0]
 represented=(x.T*(K0*y+K1*y.diff(z)))[0]
 boundary=(x.T*B.T*y)[0]
 check('full_two_form_identity_modulo_periodic_boundary',s.simplify(primitive-represented+s.diff(boundary,z))==0)
 check('omitted_spatial_drift_not_skew_adjoint',(A-A.T+(A-A.T).T-K1.diff(z)).applyfunc(s.simplify)!=s.zeros(2))
 # Auxiliary Euler equation from actual clock-regulator summand; lapse
 # derivative terms cancel only when the complete flux is retained.
 nn=s.Function('N')(z);vv=s.Function('volume')(z);hh=s.Function('hzz')(z);zz=s.Function('Z')(z);pp=s.Function('psi')(z);br=s.Symbol('b',nonzero=True)
 L=br*nn*vv*zz**2/2-br*nn*vv*hh*s.diff(zz,z)*s.diff(pp,z)-br*vv*zz*hh*s.diff(nn,z)*s.diff(pp,z)
 EL=s.diff(L,zz)-s.diff(s.diff(L,s.diff(zz,z)),z)
 target=br*nn*vv*(zz+s.diff(vv*hh*s.diff(pp,z),z)/vv)
 check('auxiliary_lapse_flux_cancellation_general_metric',s.simplify(EL-target)==0)
 check('full_original_density_controls_and_rejections_pass',all(mp.mpf(c['lapse_curvature_size'])>mp.mpf('1e-12') and mp.mpf(c['spatial_drift_size'])>mp.mpf('1e-12') and mp.mpf(c['Hessian_distance_errors'][0])<mp.mpf('1e-24') and mp.mpf(c['Hessian_distance_errors'][1])<mp.mpf('1e-32') for c in d['controls']))
 failed=[json.loads((ROOT/f'Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v{i}_attempt_01/failure.json').read_text()) for i in (1,2,3)]
 check('all_failed_versions_remain_uncompleted',all(v['validation']=='NOT_COMPLETED' and not v['physics_pass'] for v in failed))
 check('physical_quotient_and_acceleration_holds_retained',d['full_physical_symplectic_quotient']=='NOT_DERIVED' and d['initial_accelerations']=='NOT_SOLVED' and not d['physics_pass'] and not d['future_gauge_and_constraint_persistence'] and d['G1_G6']=='INCOMPLETE' and d['review']=='DEFERRED')
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_MIXED_OPERATOR_AUDIT_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  interval_pairs=2*len(records)+15,same_author_control=True,independent_external_review=False,physics_pass=False,review='DEFERRED',gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
