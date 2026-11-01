"""Inverse-coordinate two-jet and action Noether identity controls."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_INITIAL_ACCELERATION_AUDIT_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='dbcdacf8954e1cc59a2ebc42b91cd77f7a8e3473c2c54906b1f94e506455154d'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256']);snap={}
 for p in (SELF,SPEC,PARENT,'Analysis/MasterTests/audit_01_r4c1_rtau_initial_acceleration_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_audit_v1_attempt_01/summary.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_INITIAL_ACCELERATION_AUDIT_V2_SPEC_2026-11-01.md'):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 def pair(p):
  a,b=(mp.mpf(tuple(x)) for x in p);assert mp.isfinite(a) and mp.isfinite(b) and a<=b;return a,b
 bounds={k:pair(p) for k,p in d['bounds'].items()}
 check('all_uniform_bounds_finite_ordered',set(bounds)==set(['original_temporal_inverse', 'particular_acceleration', 'transformed_particular_xz', 'transformed_particular_zz', 'xi_transverse', 'xi_longitudinal', 'original_shift_rate_z', 'original_shift_rate_derivative_xy', 'original_shift_rate_derivative_z', 'original_final_acceleration', 'auxiliary_Zdot', 'prepared_auxiliary_Zdot']))
 check('coarse_actual_bounds_are_not_time_accuracy_claims',bounds['original_final_acceleration'][1]<531 and bounds['prepared_auxiliary_Zdot'][1]<mp.mpf('.000476') and not d['nonlinear_time_evolution'])
 check('three_actual_particular_inverse_certificates',len(d['point_controls'])==3 and all(pair(p['error_radius'])[1]<mp.mpf('1e-35') and mp.mpf(p['affine_Euler_residual'])<mp.mpf('1e-32') for p in d['point_controls']))
 # General spatial Noether identity from parameter integration by parts.
 z,t=s.symbols('z t',real=True)
 E=s.Matrix([s.Function('E0')(t,z),s.Function('E1')(t,z)])
 xi=s.Matrix([s.Function('x0')(t,z),s.Function('x1')(t,z)])
 S=s.Matrix([s.Function('S0')(t,z),s.Function('S1')(t,z)])
 variation=(E.T*(xi.diff(t)+xi[1]*S.diff(z)-S[1]*xi.diff(z)))[0]
 coeff=-E.diff(t)+(S[1]*E).diff(z)+s.Matrix([0,(E.T*S.diff(z))[0]])
 boundary=s.diff((E.T*xi)[0],t)-s.diff(S[1]*(E.T*xi)[0],z)
 check('spatial_Noether_multiplier_identity',s.simplify(variation-(coeff.T*xi)[0]-boundary)==0)
 Eq=s.Matrix([s.Function('F0')(t,z),s.Function('F1')(t,z)])
 D0=s.Matrix(2,2,lambda i,j:s.Function('a'+str(i)+str(j))(t,z));D1=s.Matrix(2,2,lambda i,j:s.Function('b'+str(i)+str(j))(t,z))
 lhs=(Eq.T*(D0*xi+D1*xi.diff(z)))[0]
 rhs=((D0.T*Eq-(D1.T*Eq).diff(z)).T*xi)[0]+s.diff((Eq.T*D1*xi)[0],z)
 check('full_field_Lie_formal_adjoint_identity',s.simplify(lhs-rhs)==0)
 # Numerical inverse coordinates retain the frozen first jet. The second
 # metric jet is deliberately not an evolving conformal solution.
 e=mp.mpf(1)/1000;a=e/13;abar=mp.besseli(0,a);ratio=mp.besseli(2,a)/abar
 H=mp.mpf(json.loads((ROOT/NUMERICAL).read_text())['results'][-1]['H']);point=mp.mpf('.3')
 J0=lambda q:mp.exp(a*mp.cos(q))/abar
 r=lambda q:e*(mp.cos(2*q)-ratio)/31
 ht=lambda q:H+e*mp.cos(2*q)/31
 zeta0=lambda q:mp.quad(lambda v:mp.exp(a*mp.cos(v)),[0,q])/abar
 zeta1=lambda q:(e/31)/abar*mp.quad(lambda v:mp.exp(a*mp.cos(v))*(mp.cos(2*v)-ratio),[0,q])
 target=zeta0(point);zmap=lambda tau:mp.findroot(lambda q:zeta0(q)+tau*zeta1(q)-target,point,df=lambda q:J0(q)*(1+tau*r(q)),solver='newton')
 w=zeta1(point)/J0(point);ell=-a*mp.sin(point);wp=r(point)-ell*w
 acc0=mp.mpf(d['point_controls'][0]['particular_acceleration_at_numerical_centre'][5]);cross0=mp.mpf(d['point_controls'][0]['particular_acceleration_at_numerical_centre'][2])
 afun=lambda q:acc0+mp.sin(3*q)-mp.sin(3*point)
 cfun=lambda q:cross0+mp.cos(q)-mp.cos(point)
 def metric(tau):
  q=zmap(tau);h=mp.exp(2*a*mp.cos(q));return (h+tau*2*ht(q)*h+tau*tau*afun(q)/2)/(J0(q)*(1+tau*r(q)))**2
 def cross(tau):
  q=zmap(tau);return tau*tau*cfun(q)/(2*J0(q)*(1+tau*r(q)))
 expected=acc0/J0(point)**2+abar**2*(-8*r(point)*ht(point)+6*r(point)**2)
 coeff=json.loads((ROOT/INVERSE).read_text())['parity_center_coefficients'][2]
 Sold=lambda q:sum(mp.mpf(coeff[2*n-2])*mp.cos(n*q)+mp.mpf(coeff[2*n-1])*mp.sin(n*q) for n in range(1,17))
 Soldz=lambda q:sum(n*(-mp.mpf(coeff[2*n-2])*mp.sin(n*q)+mp.mpf(coeff[2*n-1])*mp.cos(n*q)) for n in range(1,17))
 T=lambda q:mp.mpf(1)/43+mp.sin(q)/71
 def transformed_shift(tau):
  q=zmap(tau);return J0(q)*(1+tau*r(q))*(Sold(q)+tau*T(q))-zeta1(q)
 expected_shift=J0(point)*(T(point)+wp*Sold(point)-w*Soldz(point)+w*r(point))
 controls=[]
 for hs,tol in (('1e-6','1e-8'),('1e-9','1e-14')):
  h=mp.mpf(hs);got=(metric(h)+metric(-h)-2*metric(0))/(h*h);gc=(cross(h)+cross(-h)-2*cross(0))/(h*h)
  gs=(transformed_shift(h)-transformed_shift(-h))/(2*h)
  errors=[abs(got-expected),abs(gc-cross0/J0(point)),abs(gs-expected_shift)]
  check('independent_inverse_coordinate_metric_and_shift_'+hs,max(errors)<mp.mpf(tol),[mp.nstr(x,40) for x in errors]);controls.append(dict(step=hs,errors=[mp.nstr(x,45) for x in errors]))
 check('omitted_metric_coordinate_second_jet_rejected',abs(expected-acc0/J0(point)**2)>mp.mpf('1e-8'))
 # Independent direct differentiation of the auxiliary geometric relation.
 lam=lambda tau,q:a*mp.cos(q)+tau*ht(q)
 lz=lambda tau,q:-a*mp.sin(q)-tau*2*e*mp.sin(2*q)/31
 pz=lambda tau,q:e*(-mp.sin(q)/29-2*mp.sin(2*q)/31)-tau*3*e*mp.sin(3*q)/47
 pzz=lambda tau,q:e*(-mp.cos(q)/29-4*mp.cos(2*q)/31)-tau*9*e*mp.cos(3*q)/47
 Z=lambda tau,q:-mp.exp(-2*lam(tau,q))*(pzz(tau,q)+lz(tau,q)*pz(tau,q))
 zdot=-2*ht(point)*Z(0,point)-mp.exp(-2*lam(0,point))*(-9*e*mp.cos(3*point)/47+lz(0,point)*(-3*e*mp.sin(3*point)/47)-2*e*mp.sin(2*point)*pz(0,point)/31)
 err=abs(mp.diff(lambda tau:Z(tau,point),0)-zdot)
 check('independent_auxiliary_first_time_tangent',err<mp.mpf('1e-80'),mp.nstr(err,40))
 check('sharp_gauge_and_higher_auxiliary_holds_retained',d['sharp_final_gauge_quadrature']=='NOT_COMPUTED' and d['quantitative_auxiliary_Zddot']=='OPEN' and d['physical_symplectic_quotient']=='NOT_DERIVED' and not d['physics_pass'] and d['review']=='DEFERRED' and d['G1_G6']=='INCOMPLETE')
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_INITIAL_ACCELERATION_AUDIT_V2',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,coordinate_controls=controls,
  same_author_control=True,independent_external_review=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
