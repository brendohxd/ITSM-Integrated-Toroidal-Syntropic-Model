"""G3T: unchanged-action tilted homogeneous background and clock control."""
from __future__ import annotations
import argparse,hashlib,json,platform
from pathlib import Path
import numpy as np
import sympy as s
import scipy
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
'Theory/Gates/RES-001/RES001_R4C1_G3_TILTED_BACKGROUND_CONTRACT_2026-10-08.md':'508252d61dcdc73c28d9c568e4b80769aa1a3c88bb68cfc1a3306ccac078f9ac',
'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
'Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md':'952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27',
'Theory/Gates/RES-001/RES001_R4C1_G3V_SOURCE_INTEGRITY_ADDENDUM_2026-10-08.md':'6bd6808e2240354fd29b7204215e3bf0a33f53a109035afb0ed41d88b8a11834',
'Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_v1.py':'875aefe980e4b78a1173a69bbd129d81a7dc4b2b0872c0a16774bc7c177bfe8b',
'Analysis/MasterTests/outputs/r4c1_g3v_attempt_01/summary.json':'07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae',
'Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONZERO_GRADIENT_FORCE_LOCAL.md':'f58e85f8dd5d78fc563bdb537cb68db16379486920641126ea40e4d992134bf2',
'Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md':'d71848c053fbcae635e7071222e06419df839a0a169c87c58e84195c0f73b2fd',
'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json':'930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75',
'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy':'b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506',
'Analysis/MasterTests/test_01_r4c1_interacting_background.py':'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f'}
ETAS=(1.,.25,.0625,.015625,.00390625,.0009765625)
TILTS=(.5,.25,.125,.0625)
NAMES=('alpha','sigma','w','u','v','r','psi','z')
PNAMES=('MP2','MU2','c1','c2','c3','c4','K','A','b','zeta','beta','gr','m2','l4','l6','cutoff','mr2','lr','vacuum')
def sha(data):return hashlib.sha256(data).hexdigest()
def encode(data):return (json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
def verify(pins):
 for name,expected in pins.items():
  if sha((ROOT/name).read_bytes())!=expected:raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH '+name)
def tidy(x):return s.factor(s.cancel(x))
class Audit:
 def __init__(self):self.checks=[]
 def test(self,name,ok,value=None,criterion=None):self.checks.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
 def exact(self,name,expr):
  values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
  values=[tidy(x) for x in values]
  self.test(name,all(x==0 for x in values),'zero_exact' if all(x==0 for x in values) else list(map(str,values)),'zero_exact')

def covariance(audit):
 ap,bp,N=s.symbols('a_parallel a_perp N',positive=True)
 Hx,Hy,Nd,B,Bd,w,wd,p,pd=s.symbols('H_parallel H_perp N_dot B B_dot w w_dot psi_dot psi_ddot',real=True)
 gam=s.sqrt(1+w*w)
 def dt(x):return s.diff(x,ap)*ap*Hx+s.diff(x,bp)*bp*Hy+s.diff(x,N)*Nd+s.diff(x,B)*Bd+s.diff(x,w)*wd+s.diff(x,p)*pd
 g=s.diag(-N*N+B*B,ap*ap,bp*bp,bp*bp);g[0,1]=g[1,0]=ap*B
 gi=g.inv().applyfunc(tidy);U=s.Matrix([gam/N,(w-B*gam/N)/ap,0,0])
 dg=[g.applyfunc(dt),s.zeros(4),s.zeros(4),s.zeros(4)]
 G=[[[tidy(sum(gi[c,d]*(dg[i][d,j]+dg[j][d,i]-dg[d][i,j]) for d in range(4))/2) for j in range(4)] for i in range(4)] for c in range(4)]
 DU=s.Matrix(4,4,lambda i,j:tidy((dt(U[j]) if i==0 else 0)+sum(G[j][i][k]*U[k] for k in range(4))))
 acc=s.Matrix([tidy(sum(U[i]*DU[i,j] for i in range(4))) for j in range(4)])
 hp=(gi+U*U.T).applyfunc(tidy)
 I1=tidy(sum(gi[i,j]*g[k,l]*DU[i,k]*DU[j,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4) if gi[i,j]!=0 and g[k,l]!=0))
 Is=[I1,tidy(s.trace(DU)**2),tidy(s.trace(DU*DU)),tidy((acc.T*g*acc)[0])]
 expected=[(-wd*wd/(1+w*w)+Hx*Hx+2*Hy*Hy*(1+w*w))/N**2,
  (w*wd/gam+gam*(Hx+2*Hy))**2/N**2,
  (w*w*wd*wd/(1+w*w)+(1+w*w)*(Hx*Hx+2*Hy*Hy)+2*Hx*w*wd)/N**2,
  (wd+Hx*w)**2/N**2]
 audit.exact('exact_unit_frame',(U.T*g*U)[0]+1)
 audit.exact('exact_inverse',g*gi-s.eye(4))
 audit.exact('projector_idempotence',hp*g*hp-hp)
 audit.exact('projector_orthogonality',hp*g*U)
 for i in range(4):
  audit.exact('covariant_I'+str(i+1),Is[i]-expected[i])
  audit.exact('shift_and_lapse_velocity_absence_I'+str(i+1),s.diff(Is[i],B)+s.diff(Is[i],Bd)+s.diff(Is[i],Nd))
 audit.exact('homogeneous_acceleration_time',acc[0]-w*(wd+Hx*w)/N**2)
 Y=tidy(hp[0,0]*p*p)
 audit.exact('exact_tilted_Y',Y-w*w*p*p/N**2)
 Hess=s.Matrix(4,4,lambda i,j:(pd if i==j==0 else 0)-G[0][i][j]*p)
 Delta=tidy(sum(hp[i,j]*Hess[i,j] for i in range(4) for j in range(4))+s.trace(DU)*U[0]*p)
 expectD=(w*w*(pd-Nd*p/N)+w*wd*p+2*Hy*w*w*p)/N**2
 audit.exact('exact_tilted_Delta',Delta-expectD)
 audit.exact('scalar_dust_inverse_00',gi[0,0]+1/N**2)
 jets={ap:s.Rational(7,5),bp:s.Rational(6,5),Hx:s.Rational(2,5),Hy:s.Rational(1,3),N:s.Rational(9,10),
  Nd:s.Rational(1,11),B:-s.Rational(1,5),Bd:s.Rational(1,9),w:s.Rational(3,10),wd:-s.Rational(2,7),p:s.Rational(1,8),pd:-s.Rational(1,11)}
 diagnostics=dict(invariants=[str(tidy(x.subs(jets))) for x in Is],Y=str(Y.subs(jets)),Delta=str(Delta.subs(jets)))
 return dict(invariants=list(map(str,expected)),Y=str(Y),Delta=str(Delta),acceleration_time=str(acc[0]),covariant_diagnostic=diagnostics)

def derive(audit):
 q=s.Matrix(s.symbols('alpha sigma w u v r psi z',real=True));vel=s.Matrix(s.symbols('alpha_dot sigma_dot w_dot u_dot v_dot r_dot psi_dot z_dot',real=True))
 al,si,w,u,v,r,psi,z=q;hd,sd,wd,ud,vd,rd,p,zd=vel
 params=s.symbols(' '.join(PNAMES),real=True);MP,MU,c1,c2,c3,c4,K,A,b,zet,bet,gr,m2,l4,l6,cut,mr2,lr,vac=params
 gam2=1+w*w;Hx=hd+2*sd;Hy=hd-sd;Vol=s.exp(3*al);C=s.exp(bet*psi);N=s.Symbol('N',positive=True)
 I1=-wd*wd/gam2+Hx*Hx+2*Hy*Hy*gam2
 I2=w*w*wd*wd/gam2+6*w*wd*hd+9*gam2*hd*hd
 I3=w*w*wd*wd/gam2+gam2*(Hx*Hx+2*Hy*Hy)+2*Hx*w*wd
 I4=(wd+Hx*w)**2
 geometry=-3*MP*(hd*hd-sd*sd)-MU*(c1*I1+c2*I2+c3*I3-c4*I4)/2
 radius=u*u+v*v;J=v*ud-u*vd
 potential=m2*radius/2+l4*radius**2/8+l6*radius**3/(24*cut**2)+mr2*r*r/2+lr*r**4/4+gr*radius*r*r/4+vac
 T=geometry+(ud*ud+vd*vd+rd*rd+K*gam2*p*p-zet*w*w*J*J)/2-b*w*w*zd*p-b*z*w*(wd+Hx*w)*p
 # Positive w, positive psi_dot: exactly the smooth local branch of |w psi_dot|^3.
 Lpre=Vol*(T/N-A*w**3*p**3/N**2+N*(b*z*z/2-potential))
 rho=tidy(s.diff(Lpre,N)/Vol)
 tauD,epsilon=s.symbols('tau_dot epsilon',real=True)
 Ldust=Vol*epsilon*(C*C*tauD*tauD/N-N*C**4)/2
 audit.exact('dust_multiplier_constraint',s.diff(Ldust,epsilon)-Vol*(C*C*tauD*tauD/N-N*C**4)/2)
 audit.exact('lapse_dust_source_on_multiplier_shell',s.diff(Ldust,N).subs(tauD,N*C)+Vol*epsilon*C**4)
 L=s.expand(Lpre.subs(N,1/C))
 mom=s.Matrix([s.diff(L,x) for x in vel]);H=mom.jacobian(vel)
 rhs=s.Matrix([s.diff(L,x) for x in q])-mom.jacobian(q)*vel
 E=tidy((mom.T*vel)[0]-L)
 rhoClock=tidy(rho.subs(N,1/C))
 audit.exact('dust_energy_identity',E+Vol*rhoClock/C)
 charge=tidy(u*mom[4]-v*mom[3])
 audit.exact('alignment_corrected_charge',charge-Vol*C*(1-zet*w*w*radius)*(u*vd-v*ud))
 audit.exact('joint_field_velocity_rotation_noether_source',u*s.diff(L,v)-v*s.diff(L,u)+ud*mom[4]-vd*mom[3])
 m=tidy(H[6,7]);kap=H[6,6]
 audit.exact('psi_z_mixed_velocity',m+b*Vol*C*w*w)
 audit.exact('z_velocity_diagonal_zero',H[7,7])
 audit.exact('z_velocity_other_rows_zero',s.Matrix([H[i,7] for i in range(6)]))
 audit.exact('psi_z_negative_principal_determinant',H[6,6]*H[7,7]-H[6,7]**2+m*m)
 R=H[:6,:6];Rgeo=geometry.diff(hd,2) # separate matrix below
 geomH=s.hessian(geometry,(hd,sd,wd)).applyfunc(tidy)
 eta=s.Symbol('eta',positive=True)
 g3={MP:1,MU:2*eta/3,c1:s.Rational(1,5),c2:-s.Rational(7,48),c3:-s.Rational(1,80),c4:s.Rational(1,20)}
 geomG=geomH.subs(g3).applyfunc(tidy)
 detGeo=tidy(geomG.det())
 audit.exact('rest_block_geometry_factor',R[:3,:3]-Vol*C*geomH)
 audit.exact('rest_block_scalar_determinant',tidy(R[3:5,3:5].det())-(Vol*C)**2*(1-zet*w*w*radius))
 # Exact block congruence; the Schur correction vanishes since S^{-1}_{psi,psi}=0.
 invS=s.Matrix([[0,1/m],[1/m,-kap/m**2]])
 cross=H[:6,6:8]
 audit.exact('pair_inverse',H[6:8,6:8]*invS-s.eye(2))
 audit.exact('zero_pair_schur_correction',cross*invS*cross.T)
 aligned=tidy(L.subs({w:0,wd:0,si:0,sd:0,z:0,zd:0}))
 Mc=MP+MU*(c1+3*c2+c3)/2
 expected=Vol*C*(-3*Mc*hd*hd+(ud*ud+vd*vd+rd*rd+K*p*p)/2)-Vol*potential/C
 audit.exact('aligned_G3_background_control',aligned-expected)
 # Carruthers/Jacobson Eq7 control (opposite sigma convention, same normalized c_i).
 aHat=MU*(c1+c4)/MP;bHat=MU*(c1+c3)/MP;cHat=MU*c2/MP
 g=s.sqrt(gam2)
 published=s.Matrix([[2*(-6-aHat+(aHat-3*bHat-9*cHat)*gam2),4*aHat*w*w,2*(aHat-bHat-3*cHat)*g*w],
 [4*aHat*w*w,4*(3-2*aHat+(2*aHat-3*bHat)*gam2),4*(aHat-bHat)*g*w],
 [2*(aHat-bHat-3*cHat)*g*w,4*(aHat-bHat)*g*w,2*(aHat+(aHat-bHat-cHat)*w*w)]])*MP/2
 transform=s.diag(1,1,g)
 audit.exact('independent_published_geometry_Hessian',transform.T*geomH*transform-published)
 Nd,pdd=s.symbols('N_dot psi_ddot',real=True)
 regpre=Vol*(N*b*z*z/2-b*w*w*zd*p/N-b*z*w*(wd+Hx*w)*p/N)
 zmom=s.diff(regpre,zd)
 zEL=s.diff(regpre,z)-(s.diff(zmom,al)*hd+s.diff(zmom,w)*wd+s.diff(zmom,p)*pdd+s.diff(zmom,N)*Nd)
 delta=(w*w*(pdd-Nd*p/N)+w*wd*p+2*Hy*w*w*p)/N**2
 audit.exact('original_first_order_regulator_equation',zEL-b*N*Vol*(z+delta))
 higher=-b*N*Vol*delta**2/2
 audit.exact('eliminated_action_highest_time_Hessian',s.diff(higher,pdd,2)+b*Vol*w**4/N**3)
 coeff=-b*Vol*w**4/(2*N**3)
 audit.exact('nonzero_highest_time_derivative_Hessian',2*coeff+b*Vol*w**4/N**3)
 # Healthy fixed-frame comparator, not the interacting eigenstate spectrum.
 om,k=s.symbols('omega k',real=True);ga=s.sqrt(gam2);Om=ga*om-w*k;P=ga*k-w*om
 D=K*Om**2-b*P**4
 om2=K*gam2/(b*w**4)
 audit.exact('healthy_control_dust_zero_mode_roots',tidy(D.subs(k,0)-om**2*(K*gam2-b*w**4*om**2)))
 audit.exact('healthy_control_same_preferred_dispersion',tidy((K*ga**2*om**2-b*w**4*om**4).subs(om**2,om2)))
 formulas=dict(homogeneous_preclock_action=str(Lpre),regulator_equation=str(tidy(zEL)),eliminated_regulator_action=str(higher),dust_clock_action=str(L),lapse_density_rho=str(rhoClock),
  charge=str(charge),dust_energy=str(E),geometry_Hessian=[[str(tidy(x)) for x in geomH.row(i)] for i in range(3)],
  G3_geometry_determinant=str(detGeo),psi_z_hessian=[[str(tidy(x)) for x in H[6:8,6:8].row(i)] for i in range(2)],
  full_determinant='-m**2*det(R)',inertia='inertia(H)=inertia(R)+(one_positive,one_negative)',
  eliminated_highest_time_coefficient=str(coeff),eliminated_highest_time_Hessian=str(2*coeff),
  healthy_control=dict(dispersion=str(D),dust_zero_mode_omega_squared=str(om2),
   preferred_omega='gamma*omega',preferred_momentum='-w*omega',
   group_speed_at_extra_root='2*gamma/abs(w)',turning_momentum='sqrt(K/b)*gamma/(2*abs(w))',
   scope='fixed-frame positive preferred-energy comparator, not full R4C1 spectrum'))
 args=tuple(q)+tuple(vel)+params
 funcs={key:s.lambdify(args,value,'numpy',cse=True) for key,value in dict(H=H,rhs=rhs,L=L,E=E,rho=rhoClock,Q=charge,
  gradQ=s.Matrix([s.diff(charge,x) for x in tuple(q)+tuple(vel)]),gradE=s.Matrix([s.diff(E,x) for x in tuple(q)+tuple(vel)])).items()}
 return funcs,formulas

def raw_action(q,v,p):
 al,si,w,u,vv,r,psi,z=q;hd,sd,wd,ud,vd,rd,pd,zd=v
 ap=np.exp(al+2*si);bp=np.exp(al-si);Hx=hd+2*sd;Hy=hd-sd
 N=np.exp(-p['beta']*psi);Nd=1/11;B=-1/5;Bd=1/9;ga=np.sqrt(1+w*w);gd=w*wd/ga
 g=np.diag([-N*N+B*B,ap*ap,bp*bp,bp*bp]);g[0,1]=g[1,0]=ap*B
 dg=np.zeros((4,4,4));dg[0,0,0]=-2*N*Nd+2*B*Bd;dg[0,0,1]=dg[0,1,0]=ap*(Hx*B+Bd)
 dg[0,1,1]=2*ap*ap*Hx;dg[0,2,2]=dg[0,3,3]=2*bp*bp*Hy
 inv=np.linalg.inv(g);Gamma=np.zeros((4,4,4))
 for c in range(4):
  for i in range(4):
   for j in range(4):Gamma[c,i,j]=sum(inv[c,d]*(dg[i,d,j]+dg[j,d,i]-dg[d,i,j]) for d in range(4))/2
 U=np.array([ga/N,(w-B*ga/N)/ap,0.,0.])
 Ud=np.array([gd/N-ga*Nd/N**2,(wd-Bd*ga/N-B*gd/N+B*ga*Nd/N**2-Hx*(w-B*ga/N))/ap,0.,0.])
 D=np.einsum('jik,k->ij',Gamma,U);D[0]+=Ud
 acc=U@D;hp=inv+np.outer(U,U)
 I1=np.einsum('ij,kl,ik,jl',inv,g,D,D);I2=np.trace(D)**2;I3=np.trace(D@D);I4=acc@g@acc
 frame=-p['MU2']*(p['c1']*I1+p['c2']*I2+p['c3']*I3-p['c4']*I4)/2
 gravity=-p['MP2']*(Hy*Hy+2*Hx*Hy)/N**2
 radius=u*u+vv*vv;J=vv*ud-u*vd
 pot=p['m2']*radius/2+p['l4']*radius**2/8+p['l6']*radius**3/(24*p['cutoff']**2)+p['mr2']*r*r/2+p['lr']*r**4/4+p['gr']*radius*r*r/4+p['vacuum']
 force=p['K']*(U[0]*pd)**2/2-p['A']*abs(hp[0,0]*pd*pd)**1.5
 reg=p['b']*z*z/2-p['b']*hp[0,0]*zd*pd-p['b']*z*acc[0]*pd
 density=gravity+frame+(ud*ud+vd*vd+rd*rd)/(2*N*N)-p['zeta']*hp[0,0]*J*J/2-pot+force+reg
 return float(N*np.exp(3*al)*density)

def independent(audit,funcs,params):
 p=params[1];q=np.zeros(8);v=np.zeros(8)
 q[0]=(np.log(7/5)+2*np.log(6/5))/3;q[1]=(np.log(7/5)-np.log(6/5))/3;q[2]=3/10;q[6]=-np.log(9/10)/p['beta']
 v[0]=(2/5+2/3)/3;v[1]=(2/5-1/3)/3;v[2]=-2/7;v[6]=1/8
 args=tuple(q)+tuple(v)+tuple(p[x] for x in PNAMES)
 H=np.asarray(funcs['H'](*args),float);expected=float(funcs['L'](*args));actual=raw_action(q,v,p)
 audit.test('independent_raw_covariant_action',abs(actual-expected)/(1+abs(expected))<=1e-12,[actual,expected],'<=1e-12')
 records=[]
 for step in (1e-4,5e-5,2.5e-5):
  measured=np.zeros((8,8));f0=raw_action(q,v,p)
  for i in range(8):
   vi=np.zeros(8);vi[i]=step
   measured[i,i]=(raw_action(q,v+vi,p)-2*f0+raw_action(q,v-vi,p))/step**2
   for j in range(i):
    vj=np.zeros(8);vj[j]=step
    measured[i,j]=measured[j,i]=(raw_action(q,v+vi+vj,p)-raw_action(q,v+vi-vj,p)-raw_action(q,v-vi+vj,p)+raw_action(q,v-vi-vj,p))/(4*step**2)
  err=float(np.max(abs(measured-H))/(1+np.max(abs(H))))
  records.append(dict(h=step,max_normalized_error=err))
 audit.test('independent_velocity_Hessian',records[-1]['max_normalized_error']<=1e-5,records,'finest <=1e-5')
 return records

def numeric(audit,funcs):
 parent=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes());tr=np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
 audit.test('inherited_G3_failed_receipt_preserved',parent['passed']==112 and parent['total']==113 and parent['validation']=='FAIL_LOCAL_CHECKS')
 audit.test('registered_eta_grid',tuple(row['eta'] for row in parent['family'])==ETAS)
 params=[row['parameters'] for row in parent['family']]
 independent_records=independent(audit,funcs,params)
 rows=[];starts={};case_params={}
 def call(name,q,v,p):return funcs[name](*(tuple(q)+tuple(v)+tuple(p[x] for x in PNAMES)))
 def ode(t,y,p):
  q=y[:8];v=y[8:]
  if q[2]<=0 or v[6]<=0:raise RuntimeError('SMOOTH_BRANCH_DOMAIN_EXIT')
  H=np.asarray(call('H',q,v,p),float);force=np.asarray(call('rhs',q,v,p),float).ravel()
  acc=np.linalg.solve(H,force)
  return np.r_[v,acc]
 for ie,(eta,p) in enumerate(zip(ETAS,params)):
  old=parent['family'][ie]['runs']['DOP853']['initial_state'];rho0=old['rho_m'];p0=old['psid']
  check=np.array([old[x] for x in ('a','H','u','ud','v','vd','r','rd','psi','psid','rho_m','tau')])
  audit.test('archived_initial_array_'+str(eta),np.max(abs(tr[ie,0,1:,0]-check))<=1e-14)
  for tilt in TILTS:
   q=np.array([0.,0.,tilt,old['u'],old['v'],old['r'],old['psi'],0.]);v=np.array([0.,0.,0.,old['ud'],old['vd'],old['rd'],p0,0.])
   def setH(H):
    qq=q.copy();vv=v.copy();vv[0]=H;qq[7]=tilt**2*(H*p0+p['beta']*rho0/p['K'])
    return qq,vv
   def residual(H):
    qq,vv=setH(H);return float(call('rho',qq,vv,p))-rho0
   f0,fp,fm=residual(0),residual(1),residual(-1)
   coeff=np.array([(fp+fm)/2-f0,(fp-fm)/2,f0])
   roots=np.roots(coeff);admissible=[float(x.real) for x in roots if abs(x.imag)<1e-12 and x.real>0]
   label=f'eta_{eta}_w_{tilt}'
   audit.test(label+'_expanding_constraint_root',bool(admissible),[[float(x.real),float(x.imag)] for x in roots])
   if not admissible:continue
   hh=min(admissible,key=lambda x:abs(x-old['H']));q,v=setH(hh);y=np.r_[q,v];acc=ode(0,y,p)[8:]
   H=np.asarray(call('H',q,v,p),float);force=np.asarray(call('rhs',q,v,p),float).ravel()
   eigen=np.linalg.eigvalsh(H);rest=np.linalg.eigvalsh(H[:6,:6]);scale=max(1,float(np.max(abs(eigen))));threshold=scale*1e-13
   inertia=[int(sum(eigen>threshold)),int(sum(eigen<-threshold)),int(sum(abs(eigen)<=threshold))]
   rest_inertia=[int(sum(rest>threshold)),int(sum(rest<-threshold)),int(sum(abs(rest)<=threshold))]
   m=float(H[6,7]);detpair=float(np.linalg.det(H[6:8,6:8]))
   el=float(np.max(abs(H@acc-force))/(1+np.max(abs(force))))
   lapse=abs(residual(hh))/(1+rho0)
   pdd_old=-3*hh*p0-p['beta']*rho0/p['K']-p['beta']*p0*p0
   pdd_error=abs(acc[6]-pdd_old)/(1+abs(pdd_old))
   qgrad=np.asarray(call('gradQ',q,v,p),float).ravel();egrad=np.asarray(call('gradE',q,v,p),float).ravel()
   flux=float(qgrad@np.r_[v,acc]);edot=float(egrad@np.r_[v,acc])
   Y=tilt*tilt*p0*p0*np.exp(2*p['beta']*q[6])
   audit.test(label+'_initial_lapse',lapse<=1e-10,lapse,'<=1e-10')
   audit.test(label+'_all_reduced_EL',el<=1e-10,el,'<=1e-10')
   audit.test(label+'_matched_psi_acceleration',pdd_error<=1e-10,pdd_error,'<=1e-10')
   audit.test(label+'_Noether_jets',max(abs(flux),abs(edot))<=1e-10,[flux,edot],'<=1e-10')
   audit.test(label+'_positive_Y_and_dust',Y>0 and rho0>0)
   audit.test(label+'_rank_and_inertia',inertia==[6,2,0] and rest_inertia==[5,1,0],dict(full=inertia,rest=rest_inertia))
   audit.test(label+'_pair_determinant',abs(detpair+m*m)/(1+m*m)<=1e-12 and detpair<0,detpair)
   row=dict(eta=eta,tilt=tilt,H=hh,original_H=old['H'],constraint_roots=[[float(x.real),float(x.imag)] for x in roots],
    state=y.tolist(),acceleration=acc.tolist(),rho_m=rho0,Y=Y,lapse_residual=lapse,EL_residual=el,psi_acceleration_match=pdd_error,
    charge_derivative=flux,energy_derivative=edot,Hessian_eigenvalues=eigen.tolist(),Hessian_condition=float(np.linalg.cond(H)),
    full_inertia=inertia,rest_inertia=rest_inertia,psi_z_determinant=detpair,healthy_control_P_turn=float(np.sqrt(p['K']/p['b'])*np.sqrt(1+tilt*tilt)/(2*tilt)))
   rows.append(row);starts[(eta,tilt)]=y;case_params[(eta,tilt)]=p
 audit.test('all_24_initial_data_cases_retained',len(rows)==24,len(rows),24)
 runs=[];arrays=[];times=np.linspace(0.,1e-3,51)
 for eta in (1.,1/1024):
  for tilt in (.25,.0625):
   p=case_params[(eta,tilt)];y0=starts[(eta,tilt)];per=[]
   for method in ('DOP853','Radau'):
    sol=solve_ivp(lambda t,y:ode(t,y,p),(0.,1e-3),y0,method=method,rtol=1e-10,atol=1e-12,t_eval=times)
    label=f'eta_{eta}_w_{tilt}_{method}'
    audit.test(label+'_solver',sol.success and sol.y.shape==(16,51),sol.message)
    if not sol.success or sol.y.shape!=(16,51):continue
    ys=sol.y;ener=np.array([float(call('E',ys[:8,i],ys[8:,i],p)) for i in range(51)])
    charge=np.array([float(call('Q',ys[:8,i],ys[8:,i],p)) for i in range(51)])
    rho=np.array([float(call('rho',ys[:8,i],ys[8:,i],p)) for i in range(51)])
    edrift=float(np.max(abs(ener-ener[0]))/(1+abs(ener[0])))
    qdrift=float(np.max(abs(charge-charge[0]))/(1+abs(charge[0])))
    domain=bool(np.isfinite(ys).all() and np.min(ys[2])>0 and np.min(ys[14])>0 and np.min(rho)>0)
    audit.test(label+'_smooth_physical_domain',domain,[float(np.min(ys[2])),float(np.min(ys[14])),float(np.min(rho))])
    audit.test(label+'_energy_charge_drifts',max(edrift,qdrift)<=1e-8,[edrift,qdrift],'<=1e-8')
    runs.append(dict(eta=eta,tilt=tilt,method=method,nfev=sol.nfev,energy_drift=edrift,charge_drift=qdrift,
     min_w=float(np.min(ys[2])),min_psi_dot=float(np.min(ys[14])),min_rho_m=float(np.min(rho))))
    per.append(ys);arrays.append(np.vstack([times,ys]))
   if len(per)==2:
    difference=float(np.max(abs(per[0]-per[1])/(1+abs(per[1]))))
    audit.test(f'eta_{eta}_w_{tilt}_method_agreement',difference<=1e-8,difference,'<=1e-8')
 audit.test('eight_registered_runs_retained',len(runs)==8,len(runs),8)
 return dict(cases=rows,runs=runs,independent_Hessian=independent_records),np.array(arrays)

def evaluate():
 verify(PINS);parent=json.loads((OUT/'r4c1_g3v_attempt_01/summary.json').read_bytes())
 inherited={**parent['source_sha256'],**parent['transitive_source_sha256']};verify(inherited)
 audit=Audit();cov=covariance(audit);funcs,formulas=derive(audit);formulas['direct_covariance']=cov
 samples,tr=numeric(audit,funcs)
 import io
 buf=io.BytesIO();np.save(buf,tr,allow_pickle=False)
 payloads={'formulas.json':encode(formulas),'initial_data.json':encode(samples),'trajectories.npy':buf.getvalue()}
 passed=sum(x['passed'] for x in audit.checks);ok=passed==len(audit.checks)
 record=dict(schema='r4c1-g3t-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(audit.checks),checks=audit.checks,
  source_sha256=PINS,transitive_source_sha256=inherited,script_sha256=sha(Path(__file__).read_bytes()),
  artifacts={name:sha(data) for name,data in payloads.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__),
  status='CONDITIONAL_TILTED_LOCAL_IVP_WITH_CLOCK_DEPENDENT_REGULATOR_RANK' if ok else 'TILTED_CHECK_FAILURES_REQUIRE_DISPOSITION',
  initial_data_cases=len(samples['cases']),short_IVP_runs=len(samples['runs']),homogeneous_dust_clock_Hessian_inertia=[6,2,0] if ok else None,
  physical_ghost_proven=False,healthy_tilted_physical_domain_proven=False,full_finite_k_constraints_verified=False,
  preferred_Cauchy_domain_verified=False,physical_EFT_cutoff='NOT_DERIVED',full_finite_density_scattering_verified=False,
  homogeneous_G3_Taylor_vertex_obstruction_retained=True,quantum_completion_no_go=False,all_actions_no_go=False,
  physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,canonical_tests_1_to_3='HOLD_SUBSTANTIVE',
  MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED')
 payloads['summary.json']=encode(record)
 return record,payloads

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3t_attempt_01');parser.add_argument('--replay',action='store_true')
 args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
 if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
 if not args.replay and directory.exists():raise RuntimeError('REFUSE_EXISTING_OUTPUT_DIRECTORY')
 record,payloads=evaluate()
 if args.replay:
  identical=all((directory/name).read_bytes()==data for name,data in payloads.items())
  print(json.dumps(dict(replay=True,all_artifacts_byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
  if not identical:return 2
 else:
  directory.mkdir(parents=True,exist_ok=False)
  for name,data in payloads.items():
   (directory/name).write_bytes(data);(directory/(name+'.sha256')).write_text(sha(data)+'  '+name+'\n',encoding='ascii')
 print(json.dumps({key:record[key] for key in ('status','validation','passed','total','physics_pass')}))
 for c in record['checks']:
  if not c['passed']:print(json.dumps(c))
 return 0 if record['passed']==record['total'] else 1
if __name__=='__main__':raise SystemExit(main())
