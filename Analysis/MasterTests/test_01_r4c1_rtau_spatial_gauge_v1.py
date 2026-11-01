"""Exact prepared-slice spatial gauge identities and full-action controls."""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_CONTRACT_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 def zero(name,z):check(name,s.simplify(z)==0,str(s.simplify(z)))
 assert SHA((ROOT/PARENT).read_bytes())=='9c22269a9e40c331fd9c72ad72e44e9f67705524193293e2a11adc9f131827b9'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256'])
 for p in (SELF,PARENT,CONTRACT):pins[p]=SHA((ROOT/p).read_bytes())
 snapshots={}
 for rel,want in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==want and sc.read_text().split()[0].lower()==want
  for f in (p,sc):snapshots[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 h,A,N=s.symbols('h Abar N',positive=True)
 ht,m,ell,w,sz,szd,sxd,pz,pt,pzz,vx,vy,vz,gamma=s.symbols('lambda_t mean_lambda_t lambda_z w Sz Sz_z Sx_z phi_z phi_t phi_zz Vx Vy Vz gamma',real=True)
 Jac=s.sqrt(h)/A;wp=ht-m-ell*w;newSz=Jac*(sz-w);newSzd=szd-wp+ell*(sz-w)
 zero('extrinsic_transverse_covariance',(2*h*(ht-w*ell)-newSz*2*h*ell/Jac)/(2*N)-h*(ht-sz*ell)/N)
 zero('extrinsic_longitudinal_covariance',A*A*(m-newSzd)/N-(h*(ht-sz*ell-szd)/N)/Jac**2)
 zero('extrinsic_mixed_covariance',-h*sxd/(2*N*Jac)-(-h*sxd/(2*N))/Jac)
 zero('scalar_normal_velocity',(pt-w*pz-newSz*pz/Jac)/N-(pt-sz*pz)/N)
 check('omitted_velocity_drift_rejected',s.simplify((pt-newSz*pz/Jac)/N-(pt-sz*pz)/N)!=0)
 zero('frame_norm_preserved',h*(vx*vx+vy*vy)+A*A*(Jac*vz)**2-h*(vx*vx+vy*vy+vz*vz))
 zero('frame_time_dependent_vector_transform',Jac*(vz-gamma*sz/N)+Jac*w*gamma/N-(Jac*vz-gamma*newSz/N))
 zero('auxiliary_spatial_Laplacian_covariance',s.sqrt(h)*(pzz+ell*pz)/(h*A*Jac)-(pzz+ell*pz)/h)
 zero('volume_and_clock_charge_measure',h*A*Jac-h**s.Rational(3,2))
 # Longitudinal frame velocity's additional Jacobian-time term is essential.
 jt,jz=s.symbols('J_t J_z',real=True)
 zero('vector_velocity_drift_identity',(jt-w*jz).subs({jt:Jac*(ht-m),jz:Jac*ell})-Jac*wp)
 backendsp=importlib.util.spec_from_file_location('gauge_full_backend',ROOT/'Analysis/MasterTests/r4c1_two_repair_actions_v2.py')
 backend=importlib.util.module_from_spec(backendsp);backendsp.loader.exec_module(backend)
 old=backend.load('gauge_control_parameters',backend.QUADRATIC);par={k:mp.mpf(int(v.p))/int(v.q) for k,v in old.parameters().items()}
 action=backend.ClockGaugeAction('R-tau',par,physical=True)
 tree=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
 profdef=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 e=mp.mpf(1)/1000;a=e/13;scope=dict(mp=mp,e=e,beta=par['beta'])
 exec(compile(ast.fix_missing_locations(ast.Module(body=[profdef],type_ignores=[])),'<pinned-original-profiles>','exec'),scope);profiles=scope['profiles']
 H=mp.mpf(json.loads((ROOT/NUMERICAL).read_text())['results'][-1]['H']);omega=mp.mpf(json.loads((ROOT/NUMERICAL).read_text())['results'][-1]['omega'])
 coefficients=parent['parity_center_coefficients']
 abar=mp.besseli(0,a);ratio=mp.besseli(2,a)/abar
 q0=mp.quad(lambda t:mp.exp(a*mp.cos(t)),[0,mp.pi,2*mp.pi])/(2*mp.pi)
 q2=mp.quad(lambda t:mp.exp(a*mp.cos(t))*mp.cos(2*t),[0,mp.pi,2*mp.pi])/(2*mp.pi*q0)
 check('independent_arc_normalization',abs(q0-abar)<mp.mpf('1e-70'),mp.nstr(abs(q0-abar),30))
 check('independent_weighted_velocity_mean',abs(q2-ratio)<mp.mpf('1e-70'),mp.nstr(abs(q2-ratio),30))
 def geo(z):
  lam=a*mp.cos(z);ld=-a*mp.sin(z);J=mp.exp(lam)/abar
  mean=H+e*ratio/31;ht=H+e*mp.cos(2*z)/31
  drift=mp.exp(-lam)*e/31*mp.quad(lambda t:mp.exp(a*mp.cos(t))*(mp.cos(2*t)-ratio),[0,z])
  driftz=ht-mean-ld*drift
  return J,drift,driftz,mean,ld
 check('periodic_drift_flux',abs(geo(2*mp.pi)[1])<mp.mpf('1e-70'))
 check('arc_map_period',abs(mp.quad(lambda z:mp.exp(a*mp.cos(z))/abar,[0,mp.pi,2*mp.pi])-2*mp.pi)<mp.mpf('1e-70'))
 def data(z,new=False):
  prof=profiles(z);q=prof['q'].copy();dz=prof['dz'].copy();vel=[mp.mpf(0)]*16;ht=H+prof['lamdot']
  for idx in (0,3,5):vel[idx]=2*ht*q[idx]
  for idx in range(3):vel[6+idx]=(prof['vt'][idx]-ht*prof['vv'][idx])/prof['scale']
  vel[9]=prof['ud'];vel[10]=omega+prof['vd'];vel[11]=prof['rd'];vel[12]=prof['psd'];vel[14]=1
  S=[];Sz=[]
  for row in coefficients:
   S.append(sum(mp.mpf(row[2*n-2])*mp.cos(n*z)+mp.mpf(row[2*n-1])*mp.sin(n*z) for n in range(1,17)))
   Sz.append(sum(n*(-mp.mpf(row[2*n-2])*mp.sin(n*z)+mp.mpf(row[2*n-1])*mp.cos(n*z)) for n in range(1,17)))
  nv,nz=prof['N'],prof['Nz'];J,drift,dzdrift,mean,ld=geo(z)
  if new:
   oq=q.copy();ov=vel.copy();od=dz.copy();os=S.copy();osz=Sz.copy()
   q[5]=abar**2;q[8]=J*oq[8]
   for idx in range(16):dz[idx]=od[idx]/J;vel[idx]=ov[idx]-drift*od[idx]
   dz[5]=0;vel[5]=2*abar**2*mean
   dz[8]=od[8]+ld*oq[8];vel[8]=J*(ov[8]-drift*od[8]+dzdrift*oq[8])
   S[2]=J*(os[2]-drift);Sz=[osz[0]/J,osz[1]/J,osz[2]-dzdrift+ld*(os[2]-drift)]
   nz=prof['Nz']/J
  return q+vel+dz+S+Sz+[nv,nz]
 def gradient(z,new=False):
  values=data(z,new);tape=action.body.Tape();indices=(54,55,25,26);variables=[tape.var(values[i]) for i in indices]
  for i,x in zip(indices,variables):values[i]=x
  L=action.density(values)[0];return tape.grad(L,variables)
 def EN(z,new=False):
  gg=gradient(z,new);flux_derivative=mp.diff(lambda t:gradient(t,new)[1],z)
  return gg[0]-flux_derivative/(geo(z)[0] if new else 1)
 controls=[]
 for zs in ('0.3','1.1','2.4'):
  z=mp.mpf(zs);J,drift,wp,mean,ld=geo(z);o=data(z);n=data(z,True)
  go=gradient(z);gn=gradient(z,True)
  errN=abs(EN(z,True)-EN(z)/J)/(1+abs(EN(z)/J))
  errQ=max(abs(gn[i]-go[i]/J)/(1+abs(go[i]/J)) for i in (2,3))
  check('full_lapse_Euler_covariance_'+zs,errN<mp.mpf('1e-60'),mp.nstr(errN,50))
  check('full_condensate_momentum_covariance_'+zs,errQ<mp.mpf('1e-60'),mp.nstr(errQ,50))
  oldnormal=(o[25]-o[50]*o[41])/o[54];newnormal=(n[25]-n[50]*n[41])/n[54]
  check('actual_scalar_velocity_control_'+zs,abs(oldnormal-newnormal)<mp.mpf('1e-70'))
  badnormal=(o[25]-n[50]*n[41])/n[54]
  check('untransformed_velocity_rejection_'+zs,abs(badnormal-oldnormal)>mp.mpf('1e-20'))
  controls.append(dict(z=zs,lapse_Euler_error=mp.nstr(errN,50),condensate_momentum_error=mp.nstr(errQ,50)))
 # Uniform bounds use only the exact fixed lambda profile, not a fitted root.
 mp.iv.dps=40;iv=mp.iv;ai=iv.mpf(1)/13000;epsi=iv.mpf(1)/1000
 Jlo=iv.exp(-2*ai);Jhi=iv.exp(2*ai);drift_bound=2*iv.pi*(epsi/31)*iv.exp(2*ai)
 drift_derivative=2*epsi/31+ai*drift_bound
 transform_norm=iv.exp(4*ai)*(1+2*ai);transformed_correction=transform_norm*(iv.mpf(1139)/100000000)
 check('gauge_jacobian_strictly_positive',mp.mpf(Jlo._mpi_[0])>0)
 check('uniform_transformed_C2_root_uncertainty',mp.mpf(transform_norm._mpi_[1])<mp.mpf('1.000462') and mp.mpf(transformed_correction._mpi_[1])<mp.mpf('0.00001140'))
 gap_xy=iv.exp(-2*ai);gap_z=2*gap_xy
 check('mean_free_gauge_operator_gaps_positive',mp.mpf(gap_xy._mpi_[0])>0 and mp.mpf(gap_z._mpi_[0])>0)
 for f,(h,t) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snapshots))
 binary=lambda x:[list(t) for t in x._mpi_]
 return dict(kind='R4C1_RTAU_SPATIAL_GAUGE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  map='zeta=integral_0^z exp(lambda)/Abar; J=exp(lambda)/Abar; w=zeta_t/J',
  metric='diag(exp(2lambda),exp(2lambda),Abar^2) on the initial slice only',
  shift='Snew_zeta=J*(Sold_z-w); Snew_x,y=Sold_x,y',
  frame_velocity='Vnew_zeta_dot=J*(Vz_dot-w*Vz_z+w_z*Vz); transverse_dot=old_dot-w*old_z',
  mean_rate='Abar_dot/Abar=H+(epsilon/31)*weighted_average(cos(2z))',
  bounds=dict(J_lower_binary=binary(Jlo),J_upper_binary=binary(Jhi),drift_upper_binary=binary(drift_bound),drift_derivative_upper_binary=binary(drift_derivative),
              transformed_C2_norm_binary=binary(transform_norm),transformed_root_correction_binary=binary(transformed_correction),gauge_gap_xy_binary=binary(gap_xy),gauge_gap_z_binary=binary(gap_z)),
  controls=controls,scope='initial gauge orbit and velocity compatibility; homogeneous metric moduli retained',
  conformal_ansatz_assumed_preserved=False,reduced_physical_Cauchy_operator='NOT_DERIVED',initial_accelerations='NOT_DERIVED',nonlinear_time_evolution=False,
  review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
