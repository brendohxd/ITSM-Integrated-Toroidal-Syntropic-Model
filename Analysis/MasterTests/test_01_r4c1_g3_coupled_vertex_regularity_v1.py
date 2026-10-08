"""G3V: metric/dust-constrained transverse quadratic action and force regularity.

No full finite-density scattering amplitude, physical EFT cutoff or gate pass.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
 'Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_CONTRACT_2026-10-08.md':'53940518eeff7ca46fb5a9373db6e4637360eeedaeffcba6044af5cc580ac3ac',
 'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
 'Theory/Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_REPORT_2026-10-08.md':'035d1480904b2459b6a4e8b6df91d381065a653fdeb49583fcdb3dbfc4ac49f4',
 'Analysis/MasterTests/outputs/r4c1_g3i_attempt_01/summary.json':'0d85d136e7c7a3c4cd4b49d984f70d3bfdbdd70aed82b3fc423181028aa1d9c7',
 'Theory/Gates/RES-001/RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md':'b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404',
 'Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md':'c2a5c82f285dc04adcfffed4ba5c562661ddca98c4d045802ffb6e88bfeefd68',
 'Analysis/MasterTests/test_01_r4c1_scalar_constraints.py':'977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed',
 'Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json':'27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a',
 'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json':'930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75',
 'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy':'b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506',
}
ETAS=(1.,.25,.0625,.015625,.00390625,.0009765625)
TIMES=(0.,.5,1.,2.,3.,4.)
KS=(20.,40.,80.)

def sha(data):return hashlib.sha256(data).hexdigest()
def encode(data):return (json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
def verify(pins):
 for name,digest in pins.items():
  if sha((ROOT/name).read_bytes())!=digest:raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: '+name)
def tidy(expr):
 if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
 return s.factor(s.cancel(expr))
class Audit:
 def __init__(self):self.checks=[]
 def test(self,name,ok,value=None,criterion=None):
  self.checks.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
 def exact(self,name,expr):
  vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
  residual=[tidy(v) for v in vals]
  self.test(name,all(v==0 for v in residual),'zero_exact' if all(v==0 for v in residual) else list(map(str,residual)))

def derive(audit):
 ep=s.Symbol('epsilon',real=True)
 a,N,MP,MU,A,KQ,b,zeta,C,f=s.symbols('a N MP2 MU2 A K_Q b zeta C f',positive=True)
 H,Hd,w,wt,wz,B,Bt,Bz,pd,pdd,J=s.symbols('H Hdot w w_t w_z B B_t B_z psi_dot psi_ddot J0',real=True)
 c1,c2,c3,c4=s.symbols('c1 c2 c3 c4',real=True);cs=(c1,c2,c3,c4)
 def tr(expr):
  if isinstance(expr,s.MatrixBase):return expr.applyfunc(tr)
  poly=s.Poly(s.expand(expr),ep)
  return sum(value*ep**powers[0] for powers,value in poly.terms() if powers[0]<=2)
 def d(expr,index):
  if index==0:return a*H*s.diff(expr,a)+wt*s.diff(expr,w)+Bt*s.diff(expr,B)
  if index==3:return wz*s.diff(expr,w)+Bz*s.diff(expr,B)
  return s.Integer(0)
 # N retained exactly for the unit, matter and force identities.
 g=s.diag(-N**2+ep**2*B**2,a*a,a*a,a*a);g[0,2]=g[2,0]=ep*a*B
 gi=s.diag(-1/N**2,a**-2,(1-ep**2*B**2/N**2)/a**2,a**-2)
 gi[0,2]=gi[2,0]=ep*B/(a*N**2)
 boost=s.sqrt(1+ep**2*w*w)
 U=s.Matrix([boost/N,0,ep*(w-B*boost/N)/a,0])
 audit.exact('exact_ADM_inverse',g*gi-s.eye(4))
 audit.exact('exact_ADM_unit_frame',(U.T*g*U)[0]+1)
 projector=gi+U*U.T
 audit.exact('exact_projector_idempotence',projector*g*projector-projector)
 audit.exact('exact_projector_orthogonality',projector*g*U)
 grad=s.Matrix([pd,0,0,0]);Y=tidy((grad.T*projector*grad)[0])
 audit.exact('exact_transverse_Y_retains_lapse',Y-pd**2*ep**2*w**2/N**2)
 Q=(U.T*grad)[0]
 audit.exact('exact_temporal_force_block',N*KQ*Q**2/2-KQ*pd**2*(1+ep**2*w**2)/(2*N))
 audit.exact('exact_alignment_block',-N*zeta*J**2*projector[0,0]/2+zeta*J**2*ep**2*w**2/(2*N))
 alpha=s.Symbol('delta_N',real=True)
 dust_constraint=C**4*(1-1/N**2)
 audit.exact('dust_first_order_lapse_constraint',s.diff(dust_constraint.subs(N,1+ep*alpha),ep).subs(ep,0)-2*C**4*alpha)
 audit.test('pure_spin1_dust_lapse_solution',s.solve(2*C**4*alpha,alpha)==[0])
 dotphi,potential,epsilon_m=s.symbols('dot_phi V_background epsilon_m',real=True)
 scalar_density=N*(-((s.Matrix([dotphi,0,0,0]).T*gi*s.Matrix([dotphi,0,0,0]))[0])/2-potential)
 dust_density=-N*epsilon_m*(C**2*(s.Matrix([C,0,0,0]).T*gi*s.Matrix([C,0,0,0]))[0]+C**4)/2
 audit.exact('homogeneous_scalar_no_transverse_shift_source',s.diff(scalar_density,B))
 audit.exact('irrotational_dust_no_transverse_shift_source',s.diff(dust_density,B))
 # Apply the first-order dust lapse constraint on the pure spin-1 direction.
 gg=g.subs(N,1);inv=gi.subs(N,1)
 Ut=U.subs(N,1).applyfunc(lambda value:tr(s.series(value,ep,0,3).removeO()))
 Gamma=[[[tr(sum(inv[c,j]*(d(gg[j,bb],aa)+d(gg[j,aa],bb)-d(gg[aa,bb],j)) for j in range(4))/2)
          for bb in range(4)] for aa in range(4)] for c in range(4)]
 D=s.Matrix(4,4,lambda mu,nu:tr(d(Ut[nu],mu)+sum(Gamma[nu][mu][j]*Ut[j] for j in range(4))))
 acceleration=s.Matrix([tr(sum(Ut[j]*D[j,i] for j in range(4))) for i in range(4)])
 I1=tr(sum(tr(inv[i,j]*gg[k,l])*tr(D[i,k]*D[j,l]) for i in range(4) for j in range(4)
        for k in range(4) for l in range(4) if inv[i,j]!=0 and gg[k,l]!=0))
 I2=tr(s.trace(D)**2);I3=tr(s.trace(D*D))
 I4=tr((acceleration.T*gg*acceleration)[0])
 frame=tr(-MU*(c1*I1+c2*I2+c3*I3-c4*I4)/2)
 frame2=tidy(s.expand(frame).coeff(ep,2))
 audit.exact('frame_background_density',s.expand(frame).coeff(ep,0)+3*MU*(c1+3*c2+c3)*H**2/2)
 audit.exact('no_transverse_shift_velocity',s.diff(frame2,Bt))
 # Einstein ADM bulk term, with the inherited fixed-boundary/GHY convention.
 extrinsic=a*a*H*s.eye(3);extrinsic[1,2]=extrinsic[2,1]=-ep*a*Bz/2
 Kmixed=extrinsic/a**2
 eh=MP*(s.trace(Kmixed*Kmixed)-s.trace(Kmixed)**2)/2
 eh2=tidy(s.expand(eh).coeff(ep,2))
 audit.exact('Einstein_vector_shift_block',eh2-MP*Bz**2/(4*a**2))
 expected_frame2=MU*((c1+c4)*wt**2-c1*wz**2/a**2+(c1+c3)*wz*Bz/a**2
       -(c1+c3)*Bz**2/(2*a**2)+2*(c4-3*c2-c3)*H*w*wt
       +(c4-2*c1-9*c2-3*c3)*H**2*w**2)/2
 audit.exact('direct_full_background_frame_quadratic',frame2-expected_frame2)
 analytic2=tidy(frame2+eh2+(KQ*pd**2-zeta*J**2)*w**2/2)
 shift_solution=tidy(s.solve(s.diff(analytic2,Bz),Bz)[0])
 audit.exact('transverse_shift_constraint',s.diff(analytic2,Bz).subs(Bz,shift_solution))
 audit.exact('shift_gradient_solution',shift_solution+MU*(c1+c3)*wz/(MP-MU*(c1+c3)))
 reduced=tidy(analytic2.subs(Bz,shift_solution))
 kinetic=tidy(s.diff(reduced,wt,2));gradient=tidy(-a**2*s.diff(reduced,wz,2))
 audit.exact('constrained_vector_kinetic',kinetic-MU*(c1+c4))
 audit.exact('constrained_vector_gradient',gradient-MU*c1-MU**2*(c1+c3)**2/(2*(MP-MU*(c1+c3))))
 vacuum=reduced.subs({H:0,pd:0,J:0})
 audit.exact('vacuum_control_after_constraint',vacuum-(kinetic*wt**2-gradient*wz**2/a**2)/2)
 cross=tidy(s.diff(reduced,w,wt));position=tidy(s.diff(reduced,w,2))
 crossdot=s.diff(cross,H)*Hd
 massw=tidy((crossdot+3*H*cross-position)/kinetic)
 massX=tidy(massw-3*Hd/2-9*H**2/4)
 eta=s.Symbol('eta',positive=True)
 g3={MP:1,MU:2*eta/3,c1:s.Rational(1,5),c2:-s.Rational(7,48),c3:-s.Rational(1,80),
      c4:s.Rational(1,20),KQ:3*eta,zeta:eta/13,b:5*eta/11,A:2*eta**s.Rational(3,2)/7}
 audit.exact('G3_kinetic',kinetic.subs(g3)-eta/6)
 audit.exact('G3_speed',tidy((gradient/kinetic).subs(g3))-s.Rational(4,5)-3*eta/(8*(8-eta)))
 audit.exact('G3_background_mass_w',massw.subs(g3)-2*(Hd+H**2)+18*pd**2-6*J**2/13)
 audit.exact('G3_canonical_mass_X',massX.subs(g3)-Hd/2+H**2/4+18*pd**2-6*J**2/13)
 # Direct rest-space regulator variation in the interacting transverse chart.
 hp=tr(inv+Ut*Ut.T);second=s.zeros(4);second[0,0]=pdd
 Hess=s.Matrix(4,4,lambda i,j:tr(second[i,j]-Gamma[0][i][j]*pd))
 Delta=tr(sum(hp[i,j]*Hess[i,j] for i in range(4) for j in range(4))+s.trace(D)*Ut[0]*pd)
 deltas=[tidy(s.expand(Delta).coeff(ep,i)) for i in range(3)]
 audit.exact('regulator_background_zero',deltas[0])
 audit.exact('regulator_spin1_first_variation_zero',deltas[1])
 audit.exact('regulator_second_variation',deltas[2]-pd*w*wt-(pdd+2*H*pd)*w**2)
 z2=s.Symbol('z2',real=True)
 reg4=b*z2**2/2+b*z2*deltas[2]
 audit.exact('regulator_second_order_auxiliary_solution',s.diff(reg4,z2).subs(z2,-deltas[2]))
 audit.exact('direct_regulator_quartic_pullback',reg4.subs(z2,-deltas[2])+b*deltas[2]**2/2)
 # Stationary auxiliary correction at cubic order, evaluated on the actual shift.
 Bz2=s.Symbol('second_order_shift_gradient',real=True)
 audit.exact('second_order_shift_cannot_change_cubic',Bz2*s.diff(analytic2,Bz).subs(Bz,shift_solution))
 angle=s.Symbol('angle',real=True)
 average=tidy(4*s.integrate(s.cos(angle)**3,(angle,0,s.pi/2))/(2*s.pi))
 audit.exact('periodic_absolute_cosine_cube_average',average-4/(3*s.pi))
 Cc=s.Symbol('C_cusp',positive=True)
 force=-a**3*A*s.Abs(ep*w*pd)**3/N**2
 expected_coefficient=-a**3*A*s.Abs(w*pd)**3
 positive=-a**3*A*s.Abs(w*pd)**3*ep**3/(1+ep*alpha)**2
 negative=+a**3*A*s.Abs(w*pd)**3*ep**3/(1+ep*alpha)**2
 audit.exact('positive_cubic_coefficient_independent_lapse',s.limit(positive/ep**3,ep,0,dir='+')-expected_coefficient)
 audit.exact('negative_amplitude_cube_coefficient',s.limit(negative/(-ep)**3,ep,0,dir='-')-expected_coefficient)
 audit.exact('leading_cubic_auxiliary_source_zero',s.diff(expected_coefficient,alpha)+s.diff(expected_coefficient,B))
 audit.exact('right_third_derivative',s.diff(-Cc*ep**3,ep,3)+6*Cc)
 audit.exact('left_third_derivative',s.diff(+Cc*ep**3,ep,3)-6*Cc)
 audit.test('nonzero_cusp_precludes_common_third_derivative',-6*Cc!=6*Cc)
 audit.exact('symmetric_odd_difference_misses_even_cusp',-Cc*s.Abs(2*ep)**3+2*Cc*s.Abs(ep)**3-2*Cc*s.Abs(-ep)**3+Cc*s.Abs(-2*ep)**3)
 audit.exact('A_zero_transverse_control',force.subs(A,0))
 audit.exact('psi_dot_zero_transverse_control',force.subs(pd,0))
 # A force-gradient direction is retained even when psi_dot vanishes.
 pi_z,k,Pi=s.symbols('pi_z k Pi',real=True)
 normal=s.Matrix([1/N,0,-ep*B/(a*N),0])
 normal_projector=gi+normal*normal.T
 gradient_psi=s.Matrix([pd,0,0,ep*pi_z])
 scalarY=tidy((gradient_psi.T*normal_projector*gradient_psi)[0])
 audit.exact('scalar_gradient_direction_auxiliary_independence',scalarY-ep**2*pi_z**2/a**2)
 scalar_cusp=-A*s.Abs(k*Pi)**3*average
 audit.test('psi_dot_zero_not_full_C3_control',scalar_cusp!=0)
 canonical_local=tidy(A*s.Abs(pd)**3/f**3)
 canonical_X=tidy(canonical_local/a**s.Rational(3,2))
 audit.exact('G3_local_cusp_coefficient',canonical_local.subs(g3).subs(f,s.sqrt(eta/6))-12*s.sqrt(6)*s.Abs(pd)**3/7)
 arguments=(a,H,w,wt,wz,B,Bt,Bz,MU,c1,c2,c3,c4)
 funcs=dict(frame2=s.lambdify(arguments,frame2,'numpy',cse=True),
            Delta2=s.lambdify((a,H,w,wt,pd,pdd),deltas[2],'numpy',cse=True))
 formulas=dict(frame_background=str(s.expand(frame).coeff(ep,0)),frame_quadratic=str(frame2),
     Einstein_quadratic=str(eh2),full_analytic_vector_quadratic=str(analytic2),shift_gradient_solution=str(shift_solution),
     constrained_vector_quadratic=str(reduced),K_vector=str(kinetic),G_vector=str(gradient),
     friction_w='3*H',mass_w=str(massw),canonical_X_mass=str(massX),
     G3_mass_w=str(tidy(massw.subs(g3))),G3_mass_X=str(tidy(massX.subs(g3))),
     exact_transverse_Y=str(Y),Delta_coefficients=list(map(str,deltas)),direct_regulator_quartic=str(-b*deltas[2]**2/2),
     exact_nonanalytic_force=str(force),periodic_average_factor=str(average),
     local_cusp_coefficient=str(canonical_local),comoving_X_cusp_coefficient=str(canonical_X),
     scalar_gradient_cusp=str(scalar_cusp),right_third_derivative='-6*C_cusp',left_third_derivative='+6*C_cusp',
     normalized_canonical_fields={'local':'V=f*w','comoving':'X=a**(3/2)*f*w','f_squared':'MU2*(c1+c4)'},
     scope='Full spin-1 quadratic constraint block and leading force regularity; not complete J2/quartic/scattering')
 return dict(funcs=funcs,g3=g3),formulas

def raw_covariance(epsilon,jets,params):
 a,H=jets['a'],jets['H'];B=epsilon*jets['B'];w=epsilon*jets['w']
 Bt,Bz=epsilon*jets['B_t'],epsilon*jets['B_z']
 wt,wz=epsilon*jets['w_t'],epsilon*jets['w_z']
 g=np.diag([-1+B*B,a*a,a*a,a*a]);g[0,2]=g[2,0]=a*B
 inv=np.linalg.inv(g);dg=np.zeros((4,4,4))
 dg[0,0,0]=2*B*Bt;dg[3,0,0]=2*B*Bz
 dg[0,0,2]=dg[0,2,0]=a*(H*B+Bt)
 dg[3,0,2]=dg[3,2,0]=a*Bz
 for i in (1,2,3):dg[0,i,i]=2*a*a*H
 Gamma=np.einsum('cj,jab->cab',inv,np.transpose(dg,(1,0,2))+np.transpose(dg,(1,2,0))-dg)/2
 boost=np.sqrt(1+w*w);U=np.array([boost,0,(w-B*boost)/a,0])
 dU=np.zeros((4,4))
 for mu,w_der,b_der in ((0,wt,Bt),(3,wz,Bz)):
  boost_der=w*w_der/boost
  dU[mu,0]=boost_der
  dU[mu,2]=(w_der-b_der*boost-B*boost_der-(H*(w-B*boost) if mu==0 else 0))/a
 D=dU+np.einsum('bac,c->ab',Gamma,U);acceleration=U@D
 I=(np.einsum('ab,cd,ac,bd',inv,g,D,D),np.trace(D)**2,np.trace(D@D),acceleration@g@acceleration)
 frame=-params['MU2']*(params['c1']*I[0]+params['c2']*I[1]+params['c3']*I[2]-params['c4']*I[3])/2
 hp=inv+np.outer(U,U);grad=np.array([jets['psi_dot'],0.,0.,0.])
 Y=float(grad@hp@grad);Hess=-Gamma[0]*jets['psi_dot'];Hess[0,0]+=jets['psi_ddot']
 Delta=float(np.sum(hp*Hess)+np.trace(D)*(U@grad))
 force=-a**3*params['A']*max(Y,0.)**1.5
 return dict(frame=float(frame),Y=Y,Delta=Delta,force=force,
      inverse_error=float(np.max(abs(g@inv-np.eye(4)))),unit_error=float(abs(U@g@U+1)),
      projector_error=float(np.max(abs(hp@g@hp-hp))))

def independent(audit,data):
 jets=dict(a=7/5,H=2/5,w=3/10,B=-1/5,w_t=-2/7,w_z=1/4,B_t=1/9,B_z=-1/6,psi_dot=1/8,psi_ddot=-1/11)
 eta=.25;params=dict(MU2=2*eta/3,c1=1/5,c2=-7/48,c3=-1/80,c4=1/20,A=(2/7)*eta**1.5)
 args=[jets[k] for k in ('a','H','w','w_t','w_z','B','B_t','B_z')]+[params[k] for k in ('MU2','c1','c2','c3','c4')]
 expected=float(data['funcs']['frame2'](*args))
 expectedD=float(data['funcs']['Delta2'](*[jets[k] for k in ('a','H','w','w_t','psi_dot','psi_ddot')]))
 baseline=raw_covariance(0.,jets,params);Cpoint=jets['a']**3*params['A']*abs(jets['psi_dot']*jets['w'])**3
 records=[];errors=[];Derrors=[];third_errors=[]
 for h in (1e-3,5e-4,2.5e-4):
  plus=[raw_covariance(j*h,jets,params) for j in (1,2,3)]
  minus=[raw_covariance(-j*h,jets,params) for j in (1,2,3)]
  coefficient=(plus[0]['frame']+minus[0]['frame']-2*baseline['frame'])/(2*h*h)
  err=abs(coefficient-expected)/max(1.,abs(expected));errors.append(err)
  delta=(plus[0]['Delta']+minus[0]['Delta']-2*baseline['Delta'])/(2*h*h)
  derr=abs(delta-expectedD)/max(1.,abs(expectedD));Derrors.append(derr)
  right=(plus[2]['force']-3*plus[1]['force']+3*plus[0]['force']-baseline['force'])/h**3/Cpoint
  left=(minus[2]['force']-3*minus[1]['force']+3*minus[0]['force']-baseline['force'])/(-h)**3/Cpoint
  terr=max(abs(right+6),abs(left-6));third_errors.append(terr)
  pe=max(v[key] for v in plus+minus for key in ('inverse_error','unit_error','projector_error'))
  ye=max(abs(v['Y']-jets['psi_dot']**2*(j*h*jets['w'])**2)/(1+abs(v['Y'])) for j,v in enumerate(plus,1))
  audit.test(f'h_{h}_independent_geometry_projector',pe<=1e-12,pe)
  audit.test(f'h_{h}_independent_Y',ye<=1e-12,ye)
  records.append(dict(h=h,expected_frame_coefficient=expected,frame_coefficient=coefficient,frame_error=err,
       expected_Delta_coefficient=expectedD,Delta_coefficient=delta,Delta_error=derr,
       normalized_right_third=right,normalized_left_third=left,third_error=terr,projector_error=pe,Y_error=ye))
 audit.test('independent_full_frame_second_difference',errors[-1]<=1e-5 and all(errors[i+1]<errors[i] or max(errors[i+1],errors[i])<=1e-8 for i in range(2)),errors)
 audit.test('independent_regulator_second_variation',Derrors[-1]<=1e-5,Derrors)
 audit.test('independent_cubic_one_sided_jump',third_errors[-1]<=1e-5,third_errors)
 return dict(jets=jets,parameters=params,point_cusp_coefficient=Cpoint,records=records)

def numerical(audit):
 family=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())
 tr=np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
 audit.test('six_archived_eta_values',tuple(v['eta'] for v in family['family'])==ETAS)
 audit.test('original_failed_derivative_assertion_retained',family['validation']=='FAIL_LOCAL_CHECKS' and family['passed']==112 and family['total']==113)
 rows=[];average=4/(3*np.pi)
 for ie,eta in enumerate(ETAS):
  params=family['family'][ie]['parameters']
  for im,method in enumerate(family['trajectory']['methods']):
   for k in KS:
    group=[]
    for t in TIMES:
     index=int(round(t*200));audit.test(f'grid_eta_{eta}_{method}_k_{k}_t_{t}',tr[ie,im,0,index]==t)
     a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=tr[ie,im,1:,index]
     C=np.exp(params['beta']*psi);J=v*ud-u*vd
     Mc2=params['MP2']+params['MU2']*(params['c1']+3*params['c2']+params['c3'])/2
     Hd=-(ud**2+vd**2+rd**2+params['K']*pd**2+rho)/(2*Mc2)
     pdd=-3*H*pd-params['beta']*rho/params['K']
     f2=params['MU2']*(params['c1']+params['c4']);Mt2=params['MP2']-params['MU2']*(params['c1']+params['c3'])
     gradient=params['MU2']*params['c1']+params['MU2']**2*(params['c1']+params['c3'])**2/(2*Mt2)
     massw=2*(Hd+H*H)-18*pd*pd+6*J*J/13
     massX=Hd/2-H*H/4-18*pd*pd+6*J*J/13
     cLocal=params['A']*abs(pd)**3/f2**1.5
     cX=cLocal/a**1.5
     cAvg=cX*average
     scalar_det=C**8*params['MU2']*params['b']*k*k*(params['c1']+params['c2']+params['c3'])
     row=dict(eta=eta,method=method,t=t,k=k,a=float(a),H=float(H),rho_m=float(rho),psi_dot=float(pd),psi_ddot=float(pdd),
         charge_current_J0=float(J),K_vector=float(f2),G_vector=float(gradient),M_tensor2=float(Mt2),
         vector_shift_fourier_Hessian=float(Mt2*(k/a)**2/2),scalar_auxiliary_determinant=float(scalar_det),
         vector_mass_w=float(massw),canonical_X_mass=float(massX),local_frozen_frequency_squared=float(gradient/f2*(k/a)**2+massX),
         cusp_local_coefficient=float(cLocal),cusp_X_coefficient=float(cX),averaged_cusp_X_coefficient=float(cAvg),
         right_third_derivative=float(-6*cAvg),left_third_derivative=float(6*cAvg),
         ordinary_transverse_third_vertex_exists=bool(cAvg==0),
         zero_transverse_cusp_does_not_certify_full_C3=True)
     rows.append(row);group.append(row)
    label=f'eta_{eta}_{method}_k_{k}'
    audit.test(label+'_coupled_chart_and_ranks',all(v['a']>0 and v['H']>0 and v['rho_m']>0 and v['K_vector']>0 and
       v['M_tensor2']>0 and v['scalar_auxiliary_determinant']>0 and v['vector_shift_fourier_Hessian']>0 for v in group))
    audit.test(label+'_finite_coefficients',all(np.isfinite(v[key]) for v in group for key in ('G_vector','vector_mass_w','canonical_X_mass','cusp_local_coefficient','averaged_cusp_X_coefficient')))
    audit.test(label+'_one_sided_signs',all(v['right_third_derivative']<=0 and v['left_third_derivative']>=0 for v in group))
 audit.test('216_registered_events_retained',len(rows)==216)
 return dict(rows=rows,events=len(rows),nonzero_transverse_cusp_events=sum(v['averaged_cusp_X_coefficient']>0 for v in rows),
      min_K_vector=min(v['K_vector'] for v in rows),min_scalar_auxiliary_determinant=min(v['scalar_auxiliary_determinant'] for v in rows),
      min_vector_shift_Hessian=min(v['vector_shift_fourier_Hessian'] for v in rows),
      min_local_cusp=min(v['cusp_local_coefficient'] for v in rows),max_local_cusp=max(v['cusp_local_coefficient'] for v in rows))

def evaluate():
 verify(PINS)
 parent=json.loads((OUT/'r4c1_g3i_attempt_01/summary.json').read_bytes())
 inherited={**parent['source_sha256'],**parent['transitive_source_sha256']};verify(inherited)
 audit=Audit();data,formulas=derive(audit);control=independent(audit,data);samples=numerical(audit)
 payloads={'formulas.json':encode(formulas),'samples.json':encode(samples),'independent.json':encode(control)}
 passed=sum(c['passed'] for c in audit.checks)
 record=dict(schema='r4c1-g3v-v1',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
     passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=inherited,
     script_sha256=sha(Path(__file__).read_bytes()),artifacts={name:sha(value) for name,value in payloads.items()},
     runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
     numerical_summary={key:value for key,value in samples.items() if key!='rows'},independent=control,
     status='COUPLED_ORDINARY_TAYLOR_SCATTERING_BLOCKED_BY_FORCE_REGULARITY' if passed==len(audit.checks) else 'COUPLED_VERTEX_CHECK_FAILURES_REQUIRE_DISPOSITION',
     ordinary_full_cubic_vertex_verified=False,full_J2_assembled=False,full_quartic_Schur_verified=False,
     full_finite_density_scattering_verified=False,probe_amplitude_survival_on_background='NOT_DETERMINED',
     explicit_nonanalytic_prescription='NOT_SUPPLIED',physical_EFT_cutoff='NOT_DERIVED',
     physical_validity_window_verified=False,healthy_continuous_full_GR_limit_verified=False,
     classical_evolution_no_go=False,quantum_completion_no_go=False,all_paths_no_go=False,
     physics_pass=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
     review_status='DEFERRED',Rule9_cleared=False,gate_effect='NONE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',
     K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
 return record,payloads

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3v_attempt_01')
 parser.add_argument('--replay',action='store_true')
 args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
 if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
 verify(PINS)
 if not args.replay and directory.exists():raise RuntimeError('OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT')
 record,payloads=evaluate();payloads['summary.json']=encode(record)
 identical=None
 if args.replay:
  identical=all((directory/name).read_bytes()==value for name,value in payloads.items())
  print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
 else:
  directory.mkdir(parents=True,exist_ok=False)
  for name,value in payloads.items():
   (directory/name).write_bytes(value);(directory/(name+'.sha256')).write_text(sha(value)+'  '+name+'\n',encoding='ascii')
 print(json.dumps({key:record[key] for key in ('validation','passed','total','status','physics_pass')}))
 for check in record['checks']:
  if not check['passed']:print(json.dumps(check))
 if args.replay and not identical:return 2
 return 0 if record['passed']==record['total'] else 1

if __name__=='__main__':raise SystemExit(main())
