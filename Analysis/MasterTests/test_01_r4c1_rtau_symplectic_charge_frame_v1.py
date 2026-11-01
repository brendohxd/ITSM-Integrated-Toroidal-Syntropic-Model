"""Initial weak symplectic chart, charge frame and exact transport controls.

No quantitative prepared evolution generator or physical norm is supplied.
"""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_audit_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
ROOT_RECEIPT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_CONTRACT_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='25d6da6f28a4e0f5601825999bb8fb891e3fe486087e3e61eb63adbab136895e'
 pins=dict(json.loads((ROOT/PARENT).read_text())['source_sha256']);snap={}
 for rel in (SELF,PARENT,INVERSE,NUMERICAL,ROOT_RECEIPT,CONTRACT):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(v) for v in x._mpi_]
 interval=lambda pair:iv.mpf([mp.mpf(tuple(v)) for v in pair])
 inverse=json.loads((ROOT/INVERSE).read_text());numerical=json.loads((ROOT/NUMERICAL).read_text())['results'][-1]
 co=json.loads((ROOT/ROOT_RECEIPT).read_text())['parity_center_coefficients']
 eps=iv.mpf(1)/1000;ell=iv.mpf(1)/13000;hc=iv.mpf(numerical['H']);radius=iv.mpf(1139)/100000000
 volume_low=3*iv.exp(-3*ell)*(hc-radius-eps/31)
 volume_high=3*iv.exp(3*ell)*(hc+radius+eps/31)
 origin_low=eps/34*iv.exp(-2*ell);origin_high=eps/34*iv.exp(2*ell)
 determinant_low=volume_low*origin_low
 check('whole_root_clock_flow_volume_response_nonzero',lo(volume_low)>0,mp.nstr(lo(volume_low),40))
 check('whole_root_translation_origin_response_nonzero',lo(origin_low)>0,mp.nstr(lo(origin_low),40))
 check('actual_charge_translation_frame_regular',lo(determinant_low)>0,mp.nstr(lo(determinant_low),40))
 check('certified_background_reflection_signature',all(co[2][2*k]==0 for k in range(16)) and all(co[i][2*k+1]==0 for i in (0,1) for k in range(16)))
 # The reference-to-adapted coordinate map has J=a/average(a).
 # These are the moduli-momentum derivatives at fixed configuration BEFORE
 # replacing trace by current density; density cross terms remain in pullback.
 moduli_trans=iv.exp(iv.mpf([-4,4])*ell);moduli_long=iv.mpf([lo(iv.exp(-2*ell)),1])
 check('weighted_moduli_momentum_map_regular',lo(moduli_trans)>0 and lo(moduli_long)>0)
 em=mp.mpf(1)/1000;lm=mp.mpf(1)/13000;H=mp.mpf(numerical['H'])
 Abar=mp.besseli(0,lm);vol_bessel=-3*(H*mp.besseli(0,3*lm)+em/31*mp.besseli(2,3*lm))
 origin_bessel=-em/34*Abar*(mp.besseli(0,lm)-mp.besseli(2,lm))
 def shift(z):
  val=mp.mpf(0);der=mp.mpf(0)
  for k in range(1,17):
   a=mp.mpf(co[2][2*k-2]);b=mp.mpf(co[2][2*k-1]);val+=a*mp.cos(k*z)+b*mp.sin(k*z);der+=k*(-a*mp.sin(k*z)+b*mp.cos(k*z))
  return val,der
 def row(z):
  la=lm*mp.cos(z);a=mp.exp(la);lz=-lm*mp.sin(z);S,Sz=shift(z)
  u=1+em*mp.cos(z)/17;v=em*mp.cos(2*z)/19;uz=-em*mp.sin(z)/17;vz=-2*em*mp.sin(2*z)/19;J=a/Abar
  udot=em*mp.cos(2*z)/53;ht=H+em*mp.cos(2*z)/31
  return [-3*a**3*ht+a**3*(3*lz*S+Sz),uz/J*mp.sin(z),u,(-udot+S*uz)*mp.sin(z),-v*mp.sin(z),vz/J]
 integral_controls=[]
 for count in (64,128):
  values=[sum((row(2*mp.pi*k/count)[i] for k in range(count)),mp.mpf(0))/count for i in range(6)]
  defect=max(abs(values[0]-vol_bessel),abs(values[1]-origin_bessel),abs(values[2]-1),*(abs(x) for x in values[3:]))
  check('independent_profile_integrals_'+str(count),defect<mp.mpf('1e-40'),mp.nstr(defect,40))
  integral_controls.append(dict(nodes=count,values=[mp.nstr(x,75) for x in values],defect=mp.nstr(defect,40)))
 # General periodic coefficient adjoint identity: derivative terms matter.
 z=s.symbols('z');u,v,a2,a1,a0=[s.Function(k)(z) for k in ('u','v','a2','a1','a0')]
 Lv=a2*s.diff(v,z,2)+a1*s.diff(v,z)+a0*v
 Lsu=s.diff(a2*u,z,2)-s.diff(a1*u,z)+a0*u
 flux=u*a2*s.diff(v,z)-s.diff(a2*u,z)*v+u*a1*v
 check('exact_local_operator_adjoint_boundary_identity',s.expand(u*Lv-Lsu*v-s.diff(flux,z))==0)
 naive=a2*s.diff(u,z,2)-a1*s.diff(u,z)+a0*u
 check('omitted_coefficient_derivatives_rejected',s.expand(Lsu-naive)!=0)
 # Exact finite algebra controls of arbitrary nonconstant multiplication and
 # mean operators. These do not represent a physical Fourier truncation.
 size=4;one=s.ones(size,1);avg=one.T/size;P0=s.eye(size)-one*avg
 W0=s.diag(s.Rational(1001,1000),s.Rational(1999,2000),s.Rational(3001,3000),s.Rational(3999,4000))
 w=W0*one/((avg*W0*one)[0]);Pi=s.eye(size)-w*avg
 D=s.Matrix([[0,1,0,-1],[-1,0,1,0],[0,-1,0,1],[1,0,-1,0]])/2
 PM=s.diag(-2,-s.Rational(19,10),-s.Rational(21,10),-s.Rational(9,5));RM=s.diag(1,2,-1,3)/100
 Tz=Pi*(PM/2+W0*D*P0*RM)
 Tzstar=(PM/2-RM*P0*D*W0)*(s.eye(size)-one*w.T/size)
 check('exact_weighted_longitudinal_adjoint',Tz.T==Tzstar)
 check('retained_longitudinal_mean_projection',avg*Tz==s.zeros(1,size))
 check('omitted_weighted_mean_adjoint_rejected',Tz.T!=PM/2-RM*P0*D*W0)
 check('omitted_antiderivative_adjoint_sign_rejected',Tz.T!=(PM/2+RM*P0*D*W0)*(s.eye(size)-one*w.T/size))
 # Pullback includes the momentum/momentum block when the inverse depends
 # on momenta; testing only a density-momentum off-diagonal is insufficient.
 LS=-D*D+s.Rational(553,400)*P0-s.Rational(2263,8400)*one*avg+W0*D/100
 Green=LS.inv();Mden=s.diag(1,s.Rational(1001,1000),s.Rational(999,1000),s.Rational(1002,1000));CP=Green*D/7
 zero=s.zeros(size);S=Green.row_join(CP).col_join(zero.row_join(s.eye(size)))
 Om=zero.row_join(Mden).col_join((-Mden).row_join(zero));pulled=S.T*Om*S
 check('density_trace_cross_block_is_inverse_adjoint',pulled[:size,size:]==Green.T*Mden)
 check('inverse_momentum_dependence_creates_pp_block',pulled[size:,size:]==CP.T*Mden-Mden*CP and pulled[size:,size:]!=zero)
 check('pullback_is_skew_and_nondegenerate_in_algebra_control',pulled+pulled.T==s.zeros(2*size) and pulled.det()!=0)
 # Autonomous clock Hamiltonian: I=-H0 on the momentum surface. This general
 # canonical identity checks row/vector transport, not a prepared PDE estimate.
 q1,q2,p1,p2=s.symbols('q1 q2 p1 p2');xx=s.Matrix([q1,q2,p1,p2]);J=s.zeros(4);J[:2,2:]=s.eye(2);J[2:,:2]=-s.eye(2)
 Ham=(q1*q1+q2*q2+p1*p1+p2*p2)/2;Q=q1*p2-q2*p1
 gh=s.Matrix([s.diff(Ham,t) for t in xx]);gq=s.Matrix([s.diff(Q,t) for t in xx]);A=J*s.hessian(Ham,xx);XH=J*gh;XI=-XH
 check('commuting_internal_charge_algebra_control',(gq.T*J*gh)[0]==0)
 check('fixed_clock_level_contains_actual_time_flow',s.expand((gh.T*XI)[0])==0 and XI!=s.zeros(4,1))
 check('clock_constraint_row_transport',s.hessian(Ham,xx)*XH+A.T*gh==s.zeros(4,1))
 check('clock_flow_vector_transport',XI.jacobian(xx)*XH-A*XI==s.zeros(4,1))
 t=s.symbols('t',real=True);TT=s.diag(s.exp(t),1);JJ=s.Matrix([[0,1],[-1,0]]);AA=JJ*s.diag(2,3);YY=TT.inv().T*JJ*TT.inv();GG=(s.diff(TT,t)+TT*AA)*TT.inv();bad=TT*AA*TT.inv()
 good=s.simplify(s.diff(YY,t)+GG.T*YY+YY*GG);wrong=s.simplify(s.diff(YY,t)+bad.T*YY+YY*bad)
 check('moving_chart_symplectic_transport_exact',good==s.zeros(2))
 check('omitted_chart_time_derivative_rejected',wrong!=s.zeros(2))
 contraction=interval(inverse['bounds']['inverse_contraction']);Gbound=interval(inverse['coupled_inverse_L2_H2_bound'])
 tail=Gbound*contraction**64;Ktail=iv.exp(2*ell)*tail
 psmax=eps*(iv.mpf(1)/29+iv.mpf(1)/31);Kprincipal=iv.exp(iv.mpf([-1,1])*(ell+iv.mpf(2)/5*psmax))
 check('inherited_neumann_representation_tail_explicit',hi(Ktail)<mp.mpf('1e-15'),mp.nstr(hi(Ktail),40))
 check('density_symplectic_principal_order_minus_two_nonsingular',lo(Kprincipal)>0)
 for f,(h,mt) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==mt
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  volume_clock_response_magnitude=[binary(volume_low),binary(volume_high)],translation_origin_response_magnitude=[binary(origin_low),binary(origin_high)],frame_determinant_lower=binary(determinant_low),profile_integrals=integral_controls,
  moduli_momentum_factors=dict(transverse_interval=binary(moduli_trans),longitudinal_interval=binary(moduli_long),transverse_exact='1/I0(2*ell)',longitudinal_exact='1/I0(ell)^2'),
  density_trace_momentum_block='G^* multiplication(a^2); full cross/pp/moduli terms retained by inverse congruence',density_block_principal='a/(N*k^2)',density_block_principal_magnitude=binary(Kprincipal),neumann_64_term_operator_tail=binary(Ktail),
  fixed_charge_kernel='after spatial quotient, span(X_I,X_Q); X_H0=-X_I is retained physical clock evolution, not automatically quotiented',
  scope='initial weak symplectic chart and global charge regularity; algebra fixtures are not physical finite-mode dynamics',strong_L2_symplectic_inverse=False,prepared_evolution_generator='NOT_COMPUTED',variable_coefficient_physical_norm='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
