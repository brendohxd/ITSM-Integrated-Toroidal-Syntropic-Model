"""Actual prepared initial acceleration construction and coarse bounds.

The exact solution is given by a pointwise inverse and periodic integrals.
Point samples are diagnostics; no sharp final gauge quadrature is claimed.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
GAUGE='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
TEMPORAL='Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v2_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_CONTRACT_2026-11-01.md'
FACTORY='Analysis/MasterTests/r4c1_prepared_operator_factory_v1.py'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 def zero(n,x):check(n,s.simplify(x)==0,str(s.simplify(x)))
 assert SHA((ROOT/PARENT).read_bytes())=='d916402a0751fa4a0409d2048ed4e38ea18dd9b5629836f6a3517fdd44e0b577'
 data=json.loads((ROOT/PARENT).read_text());pins=dict(data['source_sha256']);snap={}
 for p in (SELF,PARENT,CONTRACT,FACTORY,GAUGE):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(v) for v in x._mpi_]
 def interval(pair):
  a,b=(mp.mpf(tuple(v)) for v in pair);assert mp.isfinite(a) and mp.isfinite(b) and a<=b;return iv.mpf([a,b])
 # The second coordinate jet is declared, not inferred from conformal evolution.
 w,wp,ell,r,ht,htz,ellz,h,J,Ab,acc=s.symbols('w wp ell r ht htz ellz h J Ab acc',real=True,nonzero=True)
 ztt=2*w*wp+ell*w*w
 zero('inverse_coordinate_second_jet',ztt-2*w*(wp+ell*w)+ell*w*w)
 g_z=(2*ell*h-2*ell*h)/J**2
 g_tz=(4*ell*ht*h+2*htz*h-4*ell*ht*h-4*ell*r*h-2*(htz+ell*r)*h+6*ell*r*h)/J**2
 zero('initial_longitudinal_metric_spatial_derivative',g_z)
 zero('initial_longitudinal_metric_velocity_spatial_derivative',g_tz)
 transformed=(acc-4*r*(2*ht*h)+6*r*r*h)/J**2
 zero('metric_longitudinal_second_jet_offset',(transformed-acc/J**2).subs(h,Ab**2*J**2)-Ab**2*(-8*r*ht+6*r*r))
 st,S,Sz=s.symbols('st S Sz',real=True)
 shift_t=J*(st+r*S-w*ell*S-w*Sz+w*r)
 zero('shift_drift_second_coordinate_jet',shift_t.subs(r,wp+ell*w)-J*(st+wp*S-w*Sz+w*(wp+ell*w)))
 tz,tzp=s.symbols('tz tzp',real=True)
 zero('longitudinal_Lie_pushforward',(2*h*ell*tz+2*h*tzp).subs(h,Ab**2*J**2)/J**2-2*Ab**2*(tzp+ell*tz))
 # Exact auxiliary first tangent. Zddot still needs higher acceleration derivatives.
 Z,pz,pvz,pvzz=s.symbols('Z pz pvz pvzz',real=True)
 raw=-3*ht*Z-(-ht*Z+(htz*pz+pvzz+ell*pvz)/h)
 zero('auxiliary_first_time_tangent_identity',raw-(-2*ht*Z-(pvzz+ell*pvz+htz*pz)/h))
 # Whole certified-root bounds in the ORIGINAL coordinate rate norm.
 eps=iv.mpf(1)/1000;lam=eps/13;beta=iv.mpf(2)/5;psmax=eps*(iv.mpf(1)/29+iv.mpf(1)/31)
 gap=iv.mpf(16662666599)/100000000000
 td=json.loads((ROOT/TEMPORAL).read_text());check('declared_temporal_inverse_gap_supported',lo(interval(td['bounds']['metric_frame_gap']))>hi(gap))
 Tmax=2*iv.exp(beta*psmax+2*lam);weightmin=iv.exp(-beta*psmax-3*lam)
 invbound=Tmax*Tmax/(weightmin*gap)
 rhs=[interval(v) for v in data['initial_affine_forcing'][:13]]
 rhsnorm=iv.sqrt(sum((iv.mpf(max(abs(lo(v)),abs(hi(v))))**2 for v in rhs),iv.mpf(0)));afree=invbound*rhsnorm
 gauge=json.loads((ROOT/GAUGE).read_text());wmax=interval(gauge['bounds']['drift_upper_binary']);wpmax=interval(gauge['bounds']['drift_derivative_upper_binary'])
 Jmin=iv.exp(-2*lam);Jmax=iv.exp(2*lam);hmin=iv.exp(-2*lam);hmax=iv.exp(2*lam)
 centre=json.loads((ROOT/NUMERICAL).read_text())['results'][-1];radius=iv.mpf(1139)/100000000
 htmax=abs(iv.mpf(centre['H']))+radius+eps/31;rmax=2*eps/31
 kz=hmax*(8*rmax*htmax+6*rmax*rmax);bx=afree/Jmin;bz=afree/(Jmin*Jmin)+kz
 gradxy=2*bx/hmin;gradz=bz/hmin
 # Mean-free primitive has pi/2 bound. Fixing original-coordinate shift
 # means can add a constant of at most that same size: final bound pi.
 xixy=iv.pi*gradxy;xiz=iv.pi*gradz
 Txy=xixy;Tz=xiz/Jmin;Tp_xy=Jmax*gradxy;Tp_z=gradz+lam*xiz/Jmin
 metric=[2*hmax*lam*Tz,iv.mpf(0),hmax*Tp_xy,2*hmax*lam*Tz,hmax*Tp_xy,2*hmax*(lam*Tz+Tp_z)]
 vabs=[3*eps/74,eps/41,eps/43];vgrad=[eps/74,2*eps/41,eps/43]
 frame=[Tz*iv.exp(lam)*(vgrad[i]+lam*vabs[i])+iv.exp(lam)*vabs[2]*(Tp_xy if i<2 else Tp_z) for i in range(3)]
 scalgrad=[eps/17,2*eps/19,3*eps/23,eps*(iv.mpf(1)/29+iv.mpf(2)/31)]
 lie=iv.sqrt(sum((v*v for v in metric+frame+[Tz*g for g in scalgrad]),iv.mpf(0)))
 afinal=afree+lie
 pdmax=eps*(iv.mpf(1)/29+iv.mpf(2)/31);pddmax=eps*(iv.mpf(1)/29+iv.mpf(4)/31);pdddmax=eps*(iv.mpf(1)/29+iv.mpf(8)/31)
 Zmax=hmax*(pddmax+lam*pdmax);Zzmax=hmax*(pdddmax+lam*pdmax+lam*pddmax+2*lam*(pddmax+lam*pdmax))
 Zdotmax=2*htmax*Zmax+hmax*(9*eps/47+lam*3*eps/47+2*eps*pdmax/31)
 Znewdotmax=Zdotmax+wmax*Zzmax
 coeff=json.loads((ROOT/INVERSE).read_text())['parity_center_coefficients']
 Smax=[sum((abs(iv.mpf(x)) for x in row),iv.mpf(0))+radius for row in coeff]
 Szmax=[sum(((i//2+1)*abs(iv.mpf(x)) for i,x in enumerate(row)),iv.mpf(0))+radius for row in coeff]
 shiftbase=max(hi(wmax*Szmax[0]),hi(wmax*Szmax[1]),hi(Jmax*(wpmax*Smax[2]+wmax*Szmax[2]+wmax*rmax)))
 check('uniform_original_temporal_inverse_finite',hi(invbound)<mp.mpf(25),mp.nstr(hi(invbound),40))
 check('actual_initial_acceleration_and_gauge_bounds_finite',all(mp.isfinite(hi(x)) for x in (afree,bx,bz,xixy,xiz,Tz,Tp_xy,Tp_z,afinal)))
 check('auxiliary_first_tangent_bound_finite',hi(Znewdotmax)<mp.mpf('.001'),mp.nstr(hi(Znewdotmax),40))
 # Independent integration control on the ACTUAL prepared metric, with
 # manufactured forcing only. It is not a numerical final acceleration.
 ae=mp.mpf(1)/13000;abar=mp.besseli(0,ae);arc=lambda z:mp.exp(ae*mp.cos(z))/abar;hm=lambda z:mp.exp(2*ae*mp.cos(z))
 bfun=lambda z:1+mp.sin(z)+mp.cos(2*z)/5
 integral=lambda f:mp.quad(f,[0,mp.pi,2*mp.pi])
 cx=integral(lambda z:arc(z)*bfun(z)/hm(z))/integral(lambda z:arc(z)/hm(z))
 compatibility=integral(lambda z:arc(z)*(cx-bfun(z))/hm(z))
 check('periodic_weighted_gauge_inverse_control',abs(compatibility)<mp.mpf('1e-80'),mp.nstr(abs(compatibility),35))
 check('deleting_metric_mean_acceleration_rejected',abs(integral(lambda z:-arc(z)*bfun(z)/hm(z)))>mp.mpf(1))
 # Reuse the frozen mixed engine; the parent owns its full independent controls.
 sp=importlib.util.spec_from_file_location('initial_acceleration_factory',ROOT/FACTORY);factory=importlib.util.module_from_spec(sp);sp.loader.exec_module(factory);env=factory.prepare()
 sj=env['J'];second_at=env['second_at'];hj=env['hj'];point_controls=[]
 for zs in ('0.3','1.1','2.4'):
  vals,L,Y=second_at(sj.variable(iv.mpf(zs)),False)
  M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)];R=[]
  for i in range(13):
   rr=L.g.get(i,sj(0)).c[0]-L.g.get(28+i,sj(0)).c[1]
   rr-=sum((hj(L,14+i,k).c[0]*vals[14+k].c[0]+hj(L,14+i,28+k).c[0]*vals[14+k].c[1] for k in range(14)),iv.mpf(0));R.append(rr)
  midpoint=lambda x:(lo(x)+hi(x))/2
  mm=mp.matrix([[midpoint(x) for x in row] for row in M]);rr=mp.matrix([midpoint(x) for x in R]);xx=mp.lu_solve(mm,rr)
  strings=[mp.nstr(x,70) for x in xx];xx=[iv.mpf(x) for x in strings]
  residual=[R[i]-sum((M[i][k]*xx[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
  resnorm=iv.sqrt(sum((iv.mpf(max(abs(lo(x)),abs(hi(x))))**2 for x in residual),iv.mpf(0)));error=invbound*resnorm
  check('validated_actual_centre_particular_inverse_'+zs,hi(error)<mp.mpf('1e-35'),mp.nstr(hi(error),40))
  # Lie generator in the original coordinate q variables (all metric rates).
  D0=[[iv.mpf(0) for _ in range(3)] for _ in range(13)];D1=[[iv.mpf(0) for _ in range(3)] for _ in range(13)]
  for i in range(13):D0[i][2]=vals[28+i].c[0]
  hq=vals[0].c[0];D1[2][0]=D1[4][1]=hq;D1[5][2]=2*hq
  for i in range(3):D1[6+i][i]=-vals[8].c[0]
  errs=[]
  for b,offset in ((D0,42),(D1,45)):
   for i in range(13):
    for k in range(3):
     e=hj(L,14+i,offset+k).c[0]+sum((M[i][j]*b[j][k] for j in range(13)),iv.mpf(0));errs.append(max(abs(lo(e)),abs(hi(e))))
  check('actual_shift_drift_Lie_coupling_'+zs,max(errs)<mp.mpf('1e-35'),mp.nstr(max(errs),40))
  # A nonzero shift-rate jet tests the complete affine Euler family, not
  # a zero-drift physical choice or the final gauge quadrature.
  tt=[iv.mpf(2)/37,-iv.mpf(1)/41,iv.mpf(1)/43];tzj=[iv.mpf(1)/47,iv.mpf(2)/53,-iv.mpf(1)/59]
  aa=[xx[i]+sum((D0[i][k]*tt[k]+D1[i][k]*tzj[k] for k in range(3)),iv.mpf(0)) for i in range(13)]
  eq=[]
  for i in range(13):
   v=sum((M[i][j]*aa[j] for j in range(13)),iv.mpf(0))+sum((hj(L,14+i,42+k).c[0]*tt[k]+hj(L,14+i,45+k).c[0]*tzj[k] for k in range(3)),iv.mpf(0))-R[i]
   eq.append(max(abs(lo(v)),abs(hi(v))))
  check('nonzero_shift_drift_affine_Euler_control_'+zs,max(eq)<mp.mpf('1e-32'),mp.nstr(max(eq),40))
  point_controls.append(dict(z=zs,particular_acceleration_at_numerical_centre=strings,error_radius=binary(error),Lie_coupling_residual=mp.nstr(max(errs),40),affine_Euler_residual=mp.nstr(max(eq),40)))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 bounds=dict(original_temporal_inverse=invbound,particular_acceleration=afree,transformed_particular_xz=bx,transformed_particular_zz=bz,xi_transverse=xixy,xi_longitudinal=xiz,original_shift_rate_z=Tz,original_shift_rate_derivative_xy=Tp_xy,original_shift_rate_derivative_z=Tp_z,original_final_acceleration=afinal,auxiliary_Zdot=Zdotmax,prepared_auxiliary_Zdot=Znewdotmax)
 return dict(kind='R4C1_RTAU_INITIAL_ACCELERATION_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  bounds={k:binary(v) for k,v in bounds.items()},baseline_prepared_shift_rate_upper=mp.nstr(shiftbase,45),point_controls=point_controls,
  exact_construction=dict(particular='a0=M13^-1 R13',coordinate_extension='zeta=zeta0+t Jw; zeta_tt=0',transformed_bx='a0_xz/J',transformed_bz='a0_zz/J^2+Abar^2*(-8*r*lambda_dot+6*r^2)',r='lambda_dot-m=w_z+lambda_z*w',
   mean_constants='cx=<bx/hxx>_zeta/<1/hxx>_zeta; cy analogous; cz=<bz>_zeta',gauge_derivatives='xi_x,zeta=(-bx+cx)/hxx; xi_y analogous; xi_z,zeta=(-bz+cz)/(2 Abar^2)',
   primitive='periodic antiderivative; add translations so <T_old>_z=0',original_shift_rate='T_old=(xi_x,xi_y,xi_z/J)',prepared_shift_rate='(-w*Sx_z,-w*Sy_z,J*(w_z*Sz-w*Sz_z+w*r))+xi',actual_original_acceleration='a=a0+Lie_T_old(q)'),
  auxiliary_Zdot='-2*lambda_dot*Z-exp(-2lambda)*(psi_dot_zz+lambda_z*psi_dot_z+lambda_dot_z*psi_z)',
  Noether_identities=dict(momentum='E_Sdot=Dq^* E_q-ad_S^* E_S',phase='Qdot=-<Jphase.E_q>',clock='I=-H-<S.E_S>; Idot=<E_q.v-S.E_Sdot>'),
  initial_nonauxiliary_acceleration='CONSTRUCTED_FUNCTIONALLY_WITH_COARSE_BOUNDS',sharp_final_gauge_quadrature='NOT_COMPUTED',quantitative_auxiliary_Zddot='OPEN',physical_symplectic_quotient='NOT_DERIVED',local_clock_evolution_check='OPEN',
  nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
