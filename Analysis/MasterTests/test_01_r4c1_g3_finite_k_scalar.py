"""G3K: full closed scalar Fourier action in dust-clock/radial gauge."""
from __future__ import annotations
import argparse,hashlib,io,json,platform
from pathlib import Path
import numpy as np
import sympy as s
import scipy
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicHermiteSpline
from scipy.optimize import linear_sum_assignment
import test_01_r4c1_g3_tilted_background as bg

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
'Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_SCALAR_CONTRACT_2026-10-08.md':'eaefd9650e265512a516cf9770e67e8b6e3297e7ab0de2ab095b4c6d448366f9',
'Theory/Gates/RES-001/RES001_R4C1_G3_TILTED_BACKGROUND_REPORT_2026-10-08.md':'f3ad690310aa762aff87f37fba961f5be9280b4c1844a9d608c2b90b5e037105',
'Analysis/MasterTests/test_01_r4c1_g3_tilted_background.py':'408320a076b4dabcfd01e4ec95d1cd7c7fcb788998012f85b64cc9f86916931b',
'Analysis/MasterTests/outputs/r4c1_g3t_attempt_02/summary.json':'386120a3d38819127341cdd2db6dec9741471783a19beab2d4d7f6c1eca073b6',
'Analysis/MasterTests/outputs/r4c1_g3t_attempt_02/initial_data.json':'c1b80b7c8cd1fd74e07fe797214a56f6c14f32f0416bb3966f6371cf4a85d243',
'Analysis/MasterTests/outputs/r4c1_g3t_attempt_02/trajectories.npy':'470bdd1212e45fb3334e549003a6d6233f26f396043924c2ccb9b20bf13c18cd',
'Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_SCALAR_REPORT_2026-09-30.md':'4d2ea777b8edfb23e52438e271286b8990da2f1720acb05dbd4707f8efb43de7',
'Analysis/MasterTests/test_01_r4c1_scalar_constraints.py':'977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed',
'Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json':'27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a'}
QN=('xi','w','u','v','r','psi','z');PN=bg.PNAMES
def sha(data):return hashlib.sha256(data).hexdigest()
def encode(data):return (json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
def verify(pins):
 for name,h in pins.items():
  if sha((ROOT/name).read_bytes())!=h:raise RuntimeError('FROZEN_SOURCE_DRIFT '+name)
def tidy(x):return s.factor(s.cancel(x))
def strings(M):return [[str(x) for x in M.row(i)] for i in range(M.rows)]
def norm(x):return float(np.linalg.norm(x))
class Audit:
 def __init__(self):self.checks=[]
 def test(self,name,ok,value=None,criterion=None):self.checks.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
 def exact(self,name,expr):
  vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr];vals=[tidy(x) for x in vals]
  self.test(name,all(x==0 for x in vals),'zero_exact' if all(x==0 for x in vals) else list(map(str,vals)),'zero_exact')

def covariance(audit):
 ap,bp,N=s.symbols('ap bp N',positive=True)
 Hx,Hy,Nd,Nx,B,Bt,Bx,xi,xit,xix,xixx,w,wt,wx=s.symbols('Hx Hy Nd Nx B Bt Bx xi xit xix xixx w wt wx',real=True)
 ga=s.sqrt(1+w*w);g=s.diag(-N*N+B*B,ap*ap,bp*bp*s.exp(2*xi),bp*bp*s.exp(2*xi));g[0,1]=g[1,0]=ap*B
 def dt(f):return s.diff(f,ap)*ap*Hx+s.diff(f,bp)*bp*Hy+s.diff(f,N)*Nd+s.diff(f,B)*Bt+s.diff(f,xi)*xit+s.diff(f,w)*wt
 def dx(f):return s.diff(f,N)*Nx+s.diff(f,B)*Bx+s.diff(f,xi)*xix+s.diff(f,xix)*xixx+s.diff(f,w)*wx
 inv=g.inv().applyfunc(tidy);U=s.Matrix([ga/N,(w-B*ga/N)/ap,0,0])
 dg=[g.applyfunc(dt),g.applyfunc(dx),s.zeros(4),s.zeros(4)]
 G=[[[tidy(sum(inv[c,l]*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j]) for l in range(4))/2) for j in range(4)] for i in range(4)] for c in range(4)]
 D=s.Matrix(4,4,lambda i,j:tidy((dt(U[j]) if i==0 else dx(U[j]) if i==1 else 0)+sum(G[j][i][l]*U[l] for l in range(4))))
 acc=s.Matrix([tidy(sum(U[i]*D[i,j] for i in range(4))) for j in range(4)])
 hp=(inv+U*U.T).applyfunc(tidy)
 I1=tidy(sum(inv[i,j]*g[k,l]*D[i,k]*D[j,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4) if inv[i,j]!=0 and g[k,l]!=0))
 Is=[I1,tidy(s.trace(D)**2),tidy(s.trace(D*D)),tidy((acc.T*g*acc)[0])]
 d0=(wt-B*wx/ap)/(ga*N)+Nx/(N*ap);d1=wx/(ga*ap)+(Hx-Bx/ap)/N
 f0=(Hy+xit-B*xix/ap)/N;f1=xix/ap;nF=ga*f0+w*f1
 expected=[-d0*d0+d1*d1+2*nF*nF,(w*d0+ga*d1+2*nF)**2,(w*d0+ga*d1)**2+2*nF*nF,(ga*d0+w*d1)**2]
 audit.exact('covariant_unit_frame',(U.T*g*U)[0]+1);audit.exact('covariant_projector',hp*g*hp-hp)
 for i in range(4):audit.exact('exact_scalar_I'+str(i+1),Is[i]-expected[i])
 p,px=s.symbols('psi_dot psi_x',real=True);grad=s.Matrix([p,px,0,0]);S=w*(p-B*px/ap)/N+ga*px/ap
 audit.exact('exact_longitudinal_Y',(grad.T*hp*grad)[0]-S*S)
 audit.exact('exact_acceleration_projection',(acc.T*grad)[0]-(ga*d0+w*d1)*S)
 audit.exact('no_shift_velocity',s.Matrix([s.diff(x,Bt) for x in Is]))
 # Independent intrinsic spatial Ricci scalar and extrinsic curvature.
 h=g[1:,1:];hi=h.inv();dh=[h.applyfunc(dx),s.zeros(3),s.zeros(3)]
 c=[[[tidy(sum(hi[k,l]*(dh[i][l,j]+dh[j][l,i]-dh[l][i,j]) for l in range(3))/2) for j in range(3)] for i in range(3)] for k in range(3)]
 Ric=s.Matrix(3,3,lambda i,j:sum((dx(c[k][i][j]) if k==0 else 0)-(dx(c[k][i][k]) if j==0 else 0)+sum(c[k][k][l]*c[l][i][j]-c[k][j][l]*c[l][i][k] for l in range(3)) for k in range(3)))
 R3=tidy(s.trace(hi*Ric))
 audit.exact('intrinsic_R3',R3+(4*xixx+6*xix*xix)/ap**2)
 shift_cov=s.Matrix([ap*B,0,0]);Ds=s.Matrix(3,3,lambda i,j:(dx(shift_cov[j]) if i==0 else 0)-sum(c[l][i][j]*shift_cov[l] for l in range(3)))
 Kij=(h.applyfunc(dt)-Ds-Ds.T)/(2*N);Km=hi*Kij
 audit.exact('exact_extrinsic_curvature',Km-s.diag((Hx-Bx/ap)/N,f0,f0))
 MP=s.Symbol('MP2',real=True);Vol=ap*bp**2*s.exp(2*xi)
 raw=MP*N*Vol*(R3+s.trace(Km*Km)-s.trace(Km)**2)/2
 first=MP*N*Vol*(xix*xix/ap**2+2*Nx*xix/(N*ap**2)-2*(Hx-Bx/ap)*f0/N-f0*f0)
 boundary=dx(-2*MP*N*Vol*xix/ap**2)
 audit.exact('spatial_boundary_density',raw-first-boundary)
 # Vary the multiplier and lapse before selecting the positive dust clock.
 epsilon,tauD,beta,psi,LapseEL=s.symbols('epsilon tau_dot beta psi LapseEL',real=True)
 C=s.exp(beta*psi)
 dust=Vol*epsilon*(C*C*tauD*tauD/N-N*C**4)/2
 audit.exact('preclock_dust_multiplier_constraint',2*s.diff(dust,epsilon)/Vol-(C*C*tauD*tauD/N-N*C**4))
 audit.exact('positive_dust_clock_shell',s.diff(dust,epsilon).subs({tauD:1,N:1/C}))
 audit.exact('preclock_lapse_dust_source',s.diff(dust,N).subs(tauD,N*C)+Vol*epsilon*C**4)
 audit.exact('lapse_solves_density_not_extra_metric_constraint',
   (LapseEL+s.diff(dust,N)).subs(tauD,N*C).subs(epsilon,LapseEL/(Vol*C**4)))
 audit.exact('reduced_psi_variation_retains_dust_source',
   (s.diff(dust,psi).subs(tauD,N*C).subs(epsilon,LapseEL/(Vol*C**4))+beta*N*LapseEL))
 return dict(frame_invariants=list(map(str,expected)),Y=str(S*S),R3=str(R3),Einstein_first_derivative_density=str(first),spatial_boundary_density=str(boundary))

def build(audit):
 ap,bp=s.symbols('ap bp',positive=True);Hx,Hy=s.symbols('Hx Hy',real=True)
 q=s.Matrix(s.symbols(' '.join(QN),real=True));d=s.Matrix(s.symbols(' '.join(n+'_dot' for n in QN),real=True));x=s.Matrix(s.symbols(' '.join(n+'_x' for n in QN),real=True))
 B,Bx=s.symbols('B B_x',real=True)
 pars=s.symbols(' '.join(PN),real=True);MP,MU,c1,c2,c3,c4,K,A,b,zet,bet,gr,m2,l4,l6,cut,mr2,lr,vac=pars
 xi,w,u,v,r,psi,z=q;xit,wt,ut,vt,rt,pt,zt=d;xix,wx,ux,vx,rx,px,zx=x
 C=s.exp(bet*psi);N=1/C;ga=s.sqrt(1+w*w);Vol=ap*bp**2*s.exp(2*xi)
 e0=lambda ft,fx:(ft-B*fx/ap)/N
 e1=lambda fx:fx/ap
 d0=e0(wt,wx)/ga-bet*px/ap;d1=e1(wx)/ga+(Hx-Bx/ap)/N
 f0=(Hy+xit-B*xix/ap)/N;f1=xix/ap;nF=ga*f0+w*f1
 I1=-d0*d0+d1*d1+2*nF*nF;I2=(w*d0+ga*d1+2*nF)**2;I3=(w*d0+ga*d1)**2+2*nF*nF;I4=(ga*d0+w*d1)**2
 Q=lambda ft,fx:ga*e0(ft,fx)+w*e1(fx)
 S=lambda ft,fx:w*e0(ft,fx)+ga*e1(fx)
 Jt=v*ut-u*vt;Jx=v*ux-u*vx
 radius=u*u+v*v
 pot=m2*radius/2+l4*radius**2/8+l6*radius**3/(24*cut**2)+mr2*r*r/2+lr*r**4/4+gr*radius*r*r/4+vac
 proper=MP*(xix*xix/ap**2-2*bet*px*xix/ap**2-2*(Hx-Bx/ap)*f0/N-f0*f0)
 proper-=MU*(c1*I1+c2*I2+c3*I3-c4*I4)/2
 proper+=sum((e0(ft,fx)**2-e1(fx)**2)/2 for ft,fx in ((ut,ux),(vt,vx),(rt,rx)))-pot
 proper+=-zet*S(Jt,Jx)**2/2+K*Q(pt,px)**2/2-A*S(pt,px)**3
 proper+=b*z*z/2-b*S(zt,zx)*S(pt,px)-b*z*(ga*d0+w*d1)*S(pt,px)
 L=N*Vol*proper
 jets=tuple(q)+tuple(d)+tuple(x)+(B,Bx);zero={xi:0,xit:0,B:0,Bx:0,**{xx:0 for xx in x}}
 gradient=[s.diff(L,a) for a in jets];full=s.zeros(23)
 print('Building exact coupled scalar jet Hessian...',flush=True)
 for i in range(23):
  for j in range(i,23):full[i,j]=full[j,i]=s.diff(gradient[i],jets[j])
 H=full.subs(zero).applyfunc(tidy)
 variables=(ap,bp,Hx,Hy)+tuple(q[1:])+tuple(d[1:])
 flows=s.symbols(' '.join('flow_'+str(i) for i in range(len(variables))),real=True)
 print('Differentiating every background coefficient at fixed k...',flush=True)
 Hdot=s.Matrix(23,23,lambda i,j:sum(s.diff(H[i,j],a)*f for a,f in zip(variables,flows) if H[i,j].has(a)))
 bh=H[22,22];expected=-MU*ap*bp**2*C*(c1+c2+c3-(c4-c2-c3)*w*w)/ap**2
 audit.exact('generic_longitudinal_shift_coefficient',bh-expected)
 audit.exact('no_B_mass_or_B_dot',H[21,21])
 audit.exact('B_Bx_cross_drops_from_diagonal',H[21,22]-H[22,21])
 audit.exact('no_B_velocity_coupling_without_gradient',H[21,7:14])
 eta=s.Symbol('eta',positive=True);g3={MP:1,MU:2*eta/3,c1:s.Rational(1,5),c2:-s.Rational(7,48),c3:-s.Rational(1,80),c4:s.Rational(1,20),K:3*eta}
 shiftG=tidy(bh.subs(g3))
 audit.exact('G3_shift_rank_surface',shiftG+eta*bp**2*C*(1-5*w*w)/(36*ap))
 audit.exact('critical_surface_not_inverted',shiftG.subs(w,1/s.sqrt(5)))
 # Real/time part of the Fourier reduction; F=-ik H_Bx,d.
 T=H[7:14,7:14];fd=H[22,7:14]
 Ksmall=(T-fd.T*fd/bh).applyfunc(tidy)
 aligned=Ksmall.subs({w:0,wt:0,z:0,zt:0,Hx:Hy}).subs(g3).applyfunc(tidy)
 dbar=144*(1-eta/12)*(1-eta/8)/eta
 audit.exact('aligned_S1_G3S_full_kinetic',aligned-ap*bp**2*C*s.diag(dbar,eta/6,1,1,1,3*eta,0))
 audit.exact('aligned_z_velocity_row_zero',aligned[6,:])
 audit.exact('aligned_z_full_velocity_row_zero',H[13,:].subs({w:0,wt:0,z:0,zt:0,Hx:Hy}))
 audit.exact('aligned_z_algebraic_diagonal',H[6,6].subs({w:0,wt:0,z:0,zt:0})-b*ap*bp**2/C)
 audit.exact('retained_z_mixed_time_coefficient',Ksmall[5,6]+b*ap*bp**2*C*w*w)
 audit.exact('retained_z_time_diagonal_zero',Ksmall[6,6])
 formulas=dict(q=list(QN),jet_order=[str(a) for a in jets],dust_clock_scalar_action=str(L),
  shift_gradient_coefficient=str(bh),G3_shift_gradient_coefficient=str(shiftG),shift_rank_surface='w**2=1/5; k=0 separate',
  reduced_kinetic=strings(Ksmall),aligned_kinetic=strings(aligned),
  operator='Tred q_ddot+(Tred_dot+Wred-Wred_dagger)q_dot+(Wred_dot-Vred)q=0',
  scope='complete closed scalar axis sector; no arbitrary-direction/tensor/vector physical cutoff')
 fH=s.lambdify(variables+pars,H,'numpy',cse=True);fHd=s.lambdify(variables+pars+tuple(flows),Hdot,'numpy',cse=True)
 fullfunc=s.lambdify((ap,bp,Hx,Hy)+jets+pars,full,'numpy',cse=True)
 Lfunc=s.lambdify((ap,bp,Hx,Hy)+jets+pars,L,'numpy',cse=True)
 return dict(H=fH,Hdot=fHd,fullH=fullfunc,L=Lfunc),formulas

def raw_action(ap,bp,Hx,Hy,j,p):
 q=np.array(j[:7]);d=np.array(j[7:14]);x=np.array(j[14:21]);B,Bx=j[21:]
 xi,w,u,v,r,psi,z=q;xit,wt,ut,vt,rt,pt,zt=d;xix,wx,ux,vx,rx,px,zx=x
 N=np.exp(-p['beta']*psi);Nd=1/11;Nx=-p['beta']*N*px;Bt=1/9
 yy=bp*bp*np.exp(2*xi);ga=np.sqrt(1+w*w);gat=w*wt/ga;gax=w*wx/ga
 g=np.diag([-N*N+B*B,ap*ap,yy,yy]);g[0,1]=g[1,0]=ap*B
 dg=np.zeros((4,4,4));dg[0,0,0]=-2*N*Nd+2*B*Bt;dg[1,0,0]=-2*N*Nx+2*B*Bx
 dg[0,0,1]=dg[0,1,0]=ap*(Hx*B+Bt);dg[1,0,1]=dg[1,1,0]=ap*Bx
 dg[0,1,1]=2*ap*ap*Hx;dg[0,2,2]=dg[0,3,3]=2*yy*(Hy+xit);dg[1,2,2]=dg[1,3,3]=2*yy*xix
 inv=np.linalg.inv(g);G=np.zeros((4,4,4))
 for c in range(4):
  for a in range(4):
   for bidx in range(4):G[c,a,bidx]=sum(inv[c,l]*(dg[a,l,bidx]+dg[bidx,l,a]-dg[l,a,bidx]) for l in range(4))/2
 U=np.array([ga/N,(w-B*ga/N)/ap,0,0]);DU=np.zeros((4,4))
 for a,wa,Na,Ba in ((0,wt,Nd,Bt),(1,wx,Nx,Bx)):
  DU[a,0]=w*wa/(ga*N)-ga*Na/N**2
  DU[a,1]=(wa-Ba*ga/N-B*w*wa/(ga*N)+B*ga*Na/N**2-(Hx*(w-B*ga/N) if a==0 else 0))/ap
 DU+=np.einsum('jik,k->ij',G,U);acc=U@DU;hp=inv+np.outer(U,U)
 Is=[np.einsum('ij,kl,ik,jl',inv,g,DU,DU),np.trace(DU)**2,np.trace(DU@DU),acc@g@acc]
 frame=-p['MU2']*(p['c1']*Is[0]+p['c2']*Is[1]+p['c3']*Is[2]-p['c4']*Is[3])/2
 h=g[1:,1:];hi=np.linalg.inv(h);dh=np.zeros((3,3,3));dh[0,1,1]=dh[0,2,2]=2*yy*xix
 ddh=np.zeros_like(dh);ddh[0,1,1]=ddh[0,2,2]=yy*(2*(3/100)+4*xix*xix);dhi=-hi@dh[0]@hi
 c=np.zeros((3,3,3));dc=np.zeros_like(c)
 for k in range(3):
  for a in range(3):
   for bidx in range(3):
    for l in range(3):
     combo=dh[a,l,bidx]+dh[bidx,l,a]-dh[l,a,bidx];dcombo=ddh[a,l,bidx]+ddh[bidx,l,a]-ddh[l,a,bidx]
     c[k,a,bidx]+=hi[k,l]*combo/2;dc[k,a,bidx]+=(dhi[k,l]*combo+hi[k,l]*dcombo)/2
 Ric=np.zeros((3,3))
 for a in range(3):
  for bidx in range(3):
   Ric[a,bidx]=dc[0,a,bidx]-(sum(dc[k,a,k] for k in range(3)) if bidx==0 else 0)
   Ric[a,bidx]+=sum(c[k,k,l]*c[l,a,bidx]-c[k,bidx,l]*c[l,a,k] for k in range(3) for l in range(3))
 R3=np.trace(hi@Ric)
 shift=np.array([ap*B,0,0]);Ds=np.zeros((3,3));Ds[0,0]=ap*Bx
 Ds-=np.einsum('lij,l->ij',c,shift)
 extr=(dg[0,1:,1:]-Ds-Ds.T)/(2*N);mixed=hi@extr
 grav=p['MP2']*(R3+np.trace(mixed@mixed)-np.trace(mixed)**2)/2
 canon=0
 for ft,fx in ((ut,ux),(vt,vx),(rt,rx)):
  grad=np.array([ft,fx,0,0]);canon-=grad@inv@grad/2
 J=np.array([v*ut-u*vt,v*ux-u*vx,0,0]);psiG=np.array([pt,px,0,0]);zG=np.array([zt,zx,0,0])
 Y=psiG@hp@psiG;Q=U@psiG
 align=-p['zeta']*(J@hp@J)/2;force=p['K']*Q*Q/2-p['A']*max(0,Y)**1.5
 reg=p['b']*z*z/2-p['b']*(zG@hp@psiG)-p['b']*z*(acc@psiG)
 rad=u*u+v*v;pot=p['m2']*rad/2+p['l4']*rad**2/8+p['l6']*rad**3/(24*p['cutoff']**2)+p['mr2']*r*r/2+p['lr']*r**4/4+p['gr']*rad*r*r/4+p['vacuum']
 Vol=ap*yy;boundary=-2*p['MP2']*N*Vol/ap**2*((Nx/N+2*xix)*xix+3/100)
 return float(N*Vol*(grav+frame+canon+align+force+reg-pot)-boundary)

def benchmark(audit,funcs,p):
 ap,bp,Hx,Hy=7/5,6/5,2/5,1/3
 q=[.07,.3,.75,.2,.6,-np.log(.9)/p['beta'],.08]
 d=[-.11,-2/7,.1,-.08,.07,.125,.03];x=[.13,.17,.03,-.02,.01,.05,-.04]
 j=np.array(q+d+x+[-.2,.37]);args=(ap,bp,Hx,Hy)+tuple(j)+tuple(p[n] for n in PN)
 expected=float(funcs['L'](*args));actual=raw_action(ap,bp,Hx,Hy,j,p)
 audit.test('independent_full_covariant_action',abs(actual-expected)/(1+abs(expected))<=1e-12,[actual,expected],'<=1e-12')
 H=np.asarray(funcs['fullH'](*args),float);records=[]
 for h in (1e-4,5e-5,2.5e-5):
  numerical=np.zeros((23,23));f0=actual
  for i in range(23):
   a=np.zeros(23);a[i]=h
   numerical[i,i]=(raw_action(ap,bp,Hx,Hy,j+a,p)-2*f0+raw_action(ap,bp,Hx,Hy,j-a,p))/h**2
   for k in range(i):
    c=np.zeros(23);c[k]=h
    numerical[i,k]=numerical[k,i]=(raw_action(ap,bp,Hx,Hy,j+a+c,p)-raw_action(ap,bp,Hx,Hy,j+a-c,p)-raw_action(ap,bp,Hx,Hy,j-a+c,p)+raw_action(ap,bp,Hx,Hy,j-a-c,p))/(4*h*h)
  err=float(np.max(abs(numerical-H))/(1+np.max(abs(H))));records.append(dict(h=h,error=err))
 audit.test('independent_23_jet_Hessian',records[-1]['error']<=1e-5,records,'finest <=1e-5')
 return records

def fourier(H,k):
 T=H[7:14,7:14].astype(complex);W=H[7:14,:7]+1j*k*H[7:14,14:21]
 V=H[:7,:7]+1j*k*(H[:7,14:21]-H[14:21,:7])+k*k*H[14:21,14:21]
 F=H[21,7:14]-1j*k*H[22,7:14]
 G=H[21,:7]+1j*k*H[21,14:21]-1j*k*H[22,:7]+k*k*H[22,14:21]
 A=float(H[21,21]+k*k*H[22,22])
 return T,W,V,F,G,A

def reduce_pair(H,Hd,k):
 T,W,V,F,G,A=fourier(H,k);Td,Wd,Vd,Fd,Gd,Ad=fourier(Hd,k)
 if A==0:raise RuntimeError('SHIFT_SCHUR_SINGULAR')
 dagger=lambda a:a.conj().T
 fc=np.outer(F.conj(),F);wc=np.outer(F.conj(),G);vc=np.outer(G.conj(),G)
 Tr=T-fc/A;Wr=W-wc/A;Vr=V-vc/A
 Trd=Td-(np.outer(Fd.conj(),F)+np.outer(F.conj(),Fd))/A+fc*Ad/A**2
 Wrd=Wd-(np.outer(Fd.conj(),G)+np.outer(F.conj(),Gd))/A+wc*Ad/A**2
 Br=Trd+Wr-dagger(Wr);Er=Wrd-Vr
 return dict(T=Tr,W=Wr,V=Vr,Tdot=Trd,Wdot=Wrd,B=Br,E=Er,raw=(T,W,V,F,G,A,Td,Wd,Fd,Gd,Ad))

def reconstruction(m,q,v,acc):
 T,W,V,F,G,A,Td,Wd,Fd,Gd,Ad=m['raw']
 b=-(F@v+G@q)/A
 bd=-(Fd@v+F@acc+Gd@q+G@v)/A+(F@v+G@q)*Ad/A**2
 EL=T@acc+(Td+W-W.conj().T)@v+(Wd-V)@q+F.conj()*bd+(Fd.conj()-G.conj())*b
 denom=1+norm(T@acc)+norm((Td+W-W.conj().T)@v)+norm((Wd-V)@q)+norm(F.conj()*bd)+norm((Fd.conj()-G.conj())*b)
 constraint=F@v+G@q+A*b
 return float(norm(EL)/denom),float(abs(constraint)/(1+abs(F@v)+abs(G@q)+abs(A*b)))

def conditioned_modes(m):
 T=m['T'].real;B=m['B'];E=m['E']
 scale=np.maximum(abs(np.diag(T)),1e-30);scale[6]=abs(T[5,6])**2/max(abs(T[5,5]),abs(T[5,6]),1e-30)
 D0=np.diag(1/np.sqrt(scale));Tc=D0@T@D0
 vals,U=np.linalg.eigh(Tc)
 inertia=[int(sum(vals>1e-10)),int(sum(vals<-1e-10)),int(sum(abs(vals)<=1e-10))]
 if inertia[2]:raise RuntimeError('UNRESOLVED_KINETIC_RANK')
 D=D0@U@np.diag(1/np.sqrt(abs(vals)));TT=D.T@T@D;BB=D.T@B@D;EE=D.T@E@D
 A=np.block([[np.zeros((7,7)),np.eye(7)],[-np.linalg.solve(TT,EE),-np.linalg.solve(TT,BB)]])
 values,vec=np.linalg.eig(A);order=np.lexsort((values.imag,values.real));values=values[order];vec=vec[:,order]
 residuals=[]
 for lam,col in zip(values,vec.T):
  physical=D@col[:7];r=(lam*lam*m['T']+lam*B+E)@physical
  denom=(abs(lam)**2*norm(m['T'])+abs(lam)*norm(B)+norm(E))*norm(physical)
  residuals.append(float(norm(r)/max(denom,1e-300)))
 return values,residuals,inertia,float(np.linalg.cond(Tc)),float(norm(TT-np.diag(np.sign(vals)))/(1+norm(TT)))

def evaluate_numeric(audit,funcs):
 parent=json.loads((OUT/'r4c1_g3t_attempt_02/initial_data.json').read_bytes())
 family=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())['family']
 params={row['eta']:row['parameters'] for row in family}
 bg_audit=bg.Audit();bgfunc,_=bg.derive(bg_audit)
 audit.test('inherited_pure_background_derivation',all(c['passed'] for c in bg_audit.checks),len(bg_audit.checks))
 def bg_rhs(y,p):
  q=y[:8];v=y[8:];args=tuple(q)+tuple(v)+tuple(p[n] for n in PN)
  H=np.asarray(bgfunc['H'](*args),float);rhs=np.asarray(bgfunc['rhs'](*args),float).ravel()
  return np.r_[v,np.linalg.solve(H,rhs)]
 def coeff(y,p,k):
  q=y[:8];v=y[8:];acc=bg_rhs(y,p)[8:];al,si,w,u,vv,r,psi,z=q
  ap=np.exp(al+2*si);bp=np.exp(al-si);Hx=v[0]+2*v[1];Hy=v[0]-v[1]
  point=(ap,bp,Hx,Hy,w,u,vv,r,psi,z)+tuple(v[2:])
  flow=(ap*Hx,bp*Hy,acc[0]+2*acc[1],acc[0]-acc[1])+tuple(v[2:])+tuple(acc[2:])
  values=point+tuple(p[n] for n in PN)
  H=np.asarray(funcs['H'](*values),float);Hd=np.asarray(funcs['Hdot'](*(values+flow)),float)
  return reduce_pair(H,Hd,k),H,(ap,bp,np.exp(-p['beta']*psi))
 # Exact background action mapping, also at nonzero transverse curvature.
 homogeneous=[]
 for ic,case in enumerate(parent['cases']):
  y=np.array(case['state']);p=params[case['eta']];q=y[:8].copy();d=y[8:].copy()
  xi=.07;xit=-.11;ap=np.exp(q[0]+2*q[1]);bp=np.exp(q[0]-q[1])
  jets=(xi,)+tuple(q[2:])+(xit,)+tuple(d[2:])+(0.,)*9
  parameters=tuple(p[n] for n in PN)
  value=float(funcs['L'](*( (ap,bp,d[0]+2*d[1],d[0]-d[1])+jets+parameters )))
  q[0]+=2*xi/3;q[1]-=xi/3;d[0]+=2*xit/3;d[1]-=xit/3
  old=float(bgfunc['L'](*(tuple(q)+tuple(d)+parameters)))
  error=abs(value-old)/(1+abs(old))
  homogeneous.append(dict(eta=case['eta'],tilt=case['tilt'],normalized_action_error=error))
  audit.test(f'homogeneous_action_mapping_{ic}',error<=1e-12,error,'<=1e-12; xi=.07,xi_dot=-.11')
 checks_fd=benchmark(audit,funcs,params[.25])
 curves=np.load(OUT/'r4c1_g3t_attempt_02/trajectories.npy',allow_pickle=False)
 audit.test('sealed_background_array_shape',curves.shape==(8,17,51))
 interpolants={};interp_checks=[]
 for i,run in enumerate(parent['runs']):
  eta=run['eta'];tilt=run['tilt'];method=run['method'];ys=curves[i,1:].T;times=curves[i,0]
  slopes=np.array([bg_rhs(y,params[eta]) for y in ys])
  spline=CubicHermiteSpline(times,ys,slopes)
  error=0.
  for t in np.linspace(0,1e-3,101):
   y=spline(t);r=bg_rhs(y,params[eta]);err=float(np.max(abs(spline(t,1)-r)/(1+abs(r))));error=max(error,err)
  interp_checks.append(dict(eta=eta,tilt=tilt,method=method,max_flow_discrepancy=error))
  audit.test(f'background_interp_{i}',error<=1e-6,error,'<=1e-6 numerical interpolation witness')
  interpolants[(eta,tilt,method)]=spline
 events=[]
 for row in parent['cases']:events.append((row['eta'],row['tilt'],0.,'initial',np.array(row['state'])))
 for key,spline in interpolants.items():
  for t in (.0005,.001):events.append((*key[:2],t,key[2],spline(t)))
 audit.test('40_registered_background_jets',len(events)==40,len(events),40)
 rows=[];matrices=[];comparison={};root_comparison={}
 rng=np.random.default_rng(81421)
 for ie,(eta,tilt,t,method,y) in enumerate(events):
  p=params[eta]
  for k in (20.,40.,80.):
   m,H,geom=coeff(y,p,k);ap,bp,N=geom
   roots,residuals,inertia,cond,congruence=conditioned_modes(m)
   label=f'event_{ie}_k_{k}'
   herm=max(norm(m['T']-m['T'].conj().T)/(1+norm(m['T'])),norm(m['V']-m['V'].conj().T)/(1+norm(m['V'])))
   audit.test(label+'_Hermitian',herm<=1e-10,herm)
   testq=rng.normal(size=7)+1j*rng.normal(size=7);testv=rng.normal(size=7)+1j*rng.normal(size=7)
   testacc=-np.linalg.solve(m['T'],m['B']@testv+m['E']@testq)
   EL,aux=reconstruction(m,testq,testv,testacc)
   audit.test(label+'_retained_constraints_and_EL',max(EL,aux)<=1e-9,[EL,aux],'<=1e-9')
   audit.test(label+'_complete_eigenpair_residual',max(residuals)<=1e-7,max(residuals),'<=1e-7')
   audit.test(label+'_static_conditioning_identity',congruence<=1e-9,congruence)
   audit.test(label+'_finite_coefficients',all(np.isfinite(m[n]).all() for n in ('T','W','V','Tdot','Wdot')) and m['raw'][5]!=0)
   pa=k/ap;freq=1j*roots/N;gam=np.sqrt(1+y[2]**2)
   mapped=[[float((gam*om-y[2]*pa).real),float((gam*om-y[2]*pa).imag),
     float((gam*pa-y[2]*om).real),float((gam*pa-y[2]*om).imag)] for om in freq]
   rows.append(dict(eta=eta,tilt=tilt,t=t,method=method,k=k,shift_coefficient=m['raw'][5],
    kinetic_inertia=inertia,conditioned_kinetic_condition=cond,roots=[[float(z.real),float(z.imag)] for z in roots],
    max_eigenpair_residual=max(residuals),max_real_exponent=float(np.max(roots.real)),
    proper_covector_Omega_P=mapped,interpretation='instantaneous time-dependent scalar operator; no physical growth or EFT classification'))
   matrices.append(np.array([m[n] for n in ('T','W','V','Tdot','Wdot')]))
   if method!='initial':
     comparison[(eta,tilt,t,k,method)]=np.array([m[n] for n in ('T','B','E')])
     root_comparison[(eta,tilt,t,k,method)]=roots
 comparisons=[]
 for (eta,tilt,t,k,method),value in comparison.items():
  if method!='DOP853':continue
  other=comparison[(eta,tilt,t,k,'Radau')]
  error=float(np.max(abs(value-other)/(1+abs(other))))
  left=root_comparison[(eta,tilt,t,k,method)];right=root_comparison[(eta,tilt,t,k,'Radau')]
  costs=abs(left[:,None]-right[None,:])/(1+np.maximum(abs(left[:,None]),abs(right[None,:])))
  li,ri=linear_sum_assignment(costs)
  comparisons.append(dict(eta=eta,tilt=tilt,t=t,k=k,coefficient_discrepancy=error,
   matched_root_normalized_discrepancy=float(np.max(costs[li,ri])),
   matched_root_absolute_discrepancy=float(np.max(abs(left[li]-right[ri]))),
   root_assignment=[[int(a),int(b)] for a,b in zip(li,ri)],
   root_comparison_interpretation='retained diagnostic; no stability or positivity pass requirement'))
  audit.test(f'coefficient_method_{eta}_{tilt}_{t}_{k}',error<=1e-6,error,'<=1e-6')
 audit.test('120_scalar_events_retained',len(rows)==120,len(rows),120)
 # Healthy preferred-frame control with finite projected-gradient stiffness.
 controls=[]
 for eta,p in params.items():
  for tilt in (.5,.25,.125,.0625):
   case=next(r for r in parent['cases'] if r['eta']==eta and r['tilt']==tilt)
   S0=np.sqrt(case['Y']);c2=6*p['A']*S0/p['K'];ga=np.sqrt(1+tilt*tilt);v=tilt/ga;d=p['b']/p['K']
   om2=(ga*ga-c2*tilt*tilt)/(d*tilt**4)
   om=np.sqrt(om2);Om=ga*om;P=-tilt*om;res=abs(Om*Om-c2*P*P-d*P**4)/(1+Om*Om+d*P**4)
   equation=[4*v*v*d*d,(4*v*v*c2-1)*d,v*v*c2*c2-c2]
   candidates=np.roots(equation);xs=[r.real for r in candidates if abs(r.imag)<1e-10 and r.real>0]
   turn=np.sqrt(xs[0]);vg=(c2*turn+2*d*turn**3)/np.sqrt(c2*turn*turn+d*turn**4)
   audit.test(f'healthy_control_{eta}_{tilt}',res<=1e-12 and abs(v*vg-1)<=1e-12,[res,float(v*vg)])
   controls.append(dict(eta=eta,tilt=tilt,c_psi_squared=c2,dust_zero_k_omega_squared=om2,preferred_P_extra=float(abs(P)),preferred_P_turn=float(turn),
    interpretation='healthy fixed-frame control only; not coupled scalar cutoff'))
 # Nonautonomous scalar evolution on the fixed archived DOP853 backgrounds.
 runs=[];arrays=[];times=np.linspace(0,1e-3,51)
 for eta in (1.,1/1024):
  tilt=.25;p=params[eta];spline=interpolants[(eta,tilt,'DOP853')]
  for k in (20.,80.):
   c0=np.zeros(14,complex);c0[5]=1.;y0=np.r_[c0.real,c0.imag];pair=[]
   def rhs(t,state):
    c=state[:14]+1j*state[14:];q=c[:7];v=c[7:]
    m,_,_=coeff(spline(t),p,k)
    acc=-np.linalg.solve(m['T'],m['B']@v+m['E']@q)
    derivative=np.r_[v,acc];return np.r_[derivative.real,derivative.imag]
   for method in ('DOP853','Radau'):
    sol=solve_ivp(rhs,(0.,1e-3),y0,method=method,rtol=1e-10,atol=1e-12,t_eval=times)
    label=f'linear_{eta}_{k}_{method}';good=sol.success and sol.y.shape==(28,51) and np.isfinite(sol.y).all()
    audit.test(label+'_solver',good,sol.message)
    if not good:continue
    cs=sol.y[:14]+1j*sol.y[14:];worst=0.;maxEL=0.;maxaux=0.;maxB=0.
    for it,t in enumerate(times):
     y=spline(t);m,_,(ap,bp,N)=coeff(y,p,k);q=cs[:7,it];v=cs[7:,it]
     acc=-np.linalg.solve(m['T'],m['B']@v+m['E']@q);rr,aa=reconstruction(m,q,v,acc);maxEL=max(maxEL,rr);maxaux=max(maxaux,aa)
     shift=-(m['raw'][3]@v+m['raw'][4]@q)/m['raw'][5];maxB=max(maxB,float(abs(shift)))
     w=y[2];pt=y[14];S0=w*pt/N;ga=np.sqrt(1+w*w)
     deltaS=pt*q[1]/N+w*v[5]/N+(p['beta']*S0+1j*k*ga/ap)*q[5]
     worst=max(worst,float(1e-12*abs(deltaS)/S0))
    audit.test(label+'_smooth_amplitude_patch',worst<=.01,worst,'physical amplitude 1e-12; <=0.01')
    audit.test(label+'_reconstructed_EL',max(maxEL,maxaux)<=1e-9,[maxEL,maxaux])
    runs.append(dict(eta=eta,tilt=tilt,k=k,method=method,nfev=sol.nfev,gradient_fraction=worst,max_shift_for_unit_mode=maxB,max_EL_residual=maxEL,max_auxiliary_residual=maxaux))
    arrays.append(np.vstack([times.astype(complex),cs]));pair.append(cs)
   if len(pair)==2:
    error=float(np.max(abs(pair[0]-pair[1])/(1+abs(pair[1]))))
    audit.test(f'linear_method_{eta}_{k}',error<=1e-7,error,'<=1e-7')
 audit.test('eight_scalar_IVP_runs_retained',len(runs)==8,len(runs),8)
 return dict(events=rows,method_comparisons=comparisons,healthy_controls=controls,evolution_runs=runs,
  background_interpolation=interp_checks,independent_Hessian=checks_fd,homogeneous_action_mapping=homogeneous,
  matrix_order=['Tred','Wred','Vred','Tred_dot','Wred_dot']),np.array(matrices),np.array(arrays)

def evaluate():
 verify(PINS);parent=json.loads((OUT/'r4c1_g3t_attempt_02/summary.json').read_bytes())
 inherited={**parent['source_sha256'],**parent['transitive_source_sha256']};verify(inherited)
 audit=Audit();cov=covariance(audit);funcs,formulas=build(audit);formulas['covariant_validation']=cov
 samples,matrices,curves=evaluate_numeric(audit,funcs)
 payloads={'formulas.json':encode(formulas),'samples.json':encode(samples)}
 for name,array in (('matrices.npy',matrices),('linear_trajectories.npy',curves)):
  f=io.BytesIO();np.save(f,array,allow_pickle=False);payloads[name]=f.getvalue()
 passed=sum(c['passed'] for c in audit.checks)
 receipt=dict(schema='r4c1-g3k-v2',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
  passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=inherited,
  script_sha256=sha(Path(__file__).read_bytes()),artifacts={name:sha(data) for name,data in payloads.items()},
  runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__),
  status='CONDITIONAL_COUPLED_FINITE_K_SCALAR_OPERATOR_WITH_EXPLICIT_SHIFT_RANK_SURFACE' if passed==len(audit.checks) else 'SCALAR_OPERATOR_FAILURES_REQUIRE_DISPOSITION',
  scalar_events=len(samples['events']),scalar_IVP_runs=len(samples['evolution_runs']),shift_rank_surface='w**2=1/5',
  arbitrary_direction_full_spectrum_verified=False,physical_ghost_proven=False,physical_instability_proven=False,
  preferred_Cauchy_domain_verified=False,global_T3_preferred_leaves_verified=False,physical_EFT_cutoff='NOT_DERIVED',
  full_scattering_verified=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
  canonical_tests_1_to_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED')
 payloads['summary.json']=encode(receipt)
 return receipt,payloads

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3k_attempt_02');ap.add_argument('--replay',action='store_true')
 args=ap.parse_args();directory=(ROOT/args.output_dir).resolve()
 if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
 if not args.replay and directory.exists():raise RuntimeError('REFUSE_EXISTING_OUTPUT_DIRECTORY')
 receipt,payloads=evaluate()
 if args.replay:
  identical=all((directory/name).read_bytes()==data for name,data in payloads.items())
  print(json.dumps(dict(replay=True,all_artifacts_byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
  if not identical:return 2
 else:
  directory.mkdir(parents=True,exist_ok=False)
  for name,data in payloads.items():
   (directory/name).write_bytes(data);(directory/(name+'.sha256')).write_text(sha(data)+'  '+name+'\n',encoding='ascii')
 print(json.dumps({k:receipt[k] for k in ('validation','passed','total','status','physics_pass')}))
 for c in receipt['checks']:
  if not c['passed']:print(json.dumps(c))
 return 0 if receipt['passed']==receipt['total'] else 1
if __name__=='__main__':raise SystemExit(main())
