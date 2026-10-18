"""Exact nonlinear initial-slice system; full data certification remains open."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_INITIAL_CONSTRAINT_V1_CONTRACT_2026-10-18.md'
CANON='Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py'
RET='Analysis/MasterTests/outputs/r4c1_fixed_charge_retarded_comparison_attempt_03/trajectories.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
PINS={
 CONTRACT:'1f2585c61811c41e0524b88209ee2f0761bf2aa27d388d138a66e4725dca90bc',
 CANON:'4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada',
 RET:'3e36b9594ec4f186fff610a291011b6344b23ba98645922dfd7ad78d242ee4b3',
 PLANAR:'852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
 'Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py':'7321e53304864f0832a3e5a6ce3fce5dc2d156d3fa12d29df267b93910730b3f',
 'Analysis/MasterTests/test_01_r4c1_interacting_background.py':'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
 'Analysis/MasterTests/test_01_r4c1_initial_charge_completion_v4.py':'af22270b76b72d29a04bdfba366464bcc2482ec5f2e41f5ffe66061fee7f4020',
 'Analysis/MasterTests/test_01_r4c1_regulator_node_v1.py':'7126d03a3b3a3a525bf1ce4c8b31c8541901f9d7c45ad82c288db71cc97cfa25',
 'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V4_REPORT_2026-10-16.md':'6b81ceff4cde8c9d933259ac34fbdccb4bcf4118f188c734de8a2577613a6c36',
 'Theory/Gates/RES-001/RES001_R4C1_REGULATOR_NODE_V1_REPORT_2026-10-17.md':'b47dcf5e7fc340a015f2e7cdf273157bc6e2e1ba311bbc543a5f66596dbc83d2',
 'Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_REPORT_2026-10-17.md':'8c4496eacdb0d2447445e4a1949b683e033f042a7332c659701e2273d2bf23ea',
 'Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md':'3019196b071b146a1e41cd055073ae02da2afa10b1cdb5ae49e0a63cf84a6eb6',
 'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md':'4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c',
 'GEMINI.md':'5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
 'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md':'d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md':'3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
 'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':'14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
}
SHA=lambda data:hashlib.sha256(data).hexdigest()
ENC=lambda data:(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
SHOW=lambda value:mp.nstr(value,45)
CLEAN=lambda value:s.factor(s.cancel(s.expand(value)))
NUM=lambda value:mp.mpf(str(value))
CX=lambda value:mp.mpc(NUM(value[0]),NUM(value[1]))
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
ETAS=('1/4','1/64','1/1024')


class Checks:
 def __init__(self):self.rows=[];self.names=set()
 def add(self,name,ok,value=None,criterion='exact'):
  if name in self.names:raise ValueError('duplicate check '+name)
  self.names.add(name);self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
 def zero(self,name,value):
  values=list(value) if isinstance(value,(list,tuple,s.MatrixBase)) else [value]
  bad=[str(q) for v in values if (q:=CLEAN(v))!=0]
  self.add(name,not bad,bad)
 def small(self,name,value,tolerance):
  self.add(name,mp.isfinite(value) and value<=mp.mpf(tolerance),SHOW(value),'<='+tolerance)


def sources():
 pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());metadata={}
 for name,digest in pins.items():
  path=ROOT/name
  if SHA(path.read_bytes())!=digest:raise ValueError('source hash drift '+name)
  sc=Path(str(path)+'.sha256')
  if sc.read_text().split()[0].lower()!=digest:raise ValueError('source sidecar mismatch '+name)
  for p in (path,sc):
   data=p.read_bytes();metadata[p.relative_to(ROOT).as_posix()]=dict(
       sha256=SHA(data),bytes=len(data),mtime_ns=p.stat().st_mtime_ns)
 return pins,metadata


def derive(ch):
 print('DERIVE_FULL_RESTRICTED_DENSITY_AND_SHIFT_SYSTEM',flush=True)
 names='MP2 MU2 c1 c2 c3 c4 K_Q A b zeta Rc H H0 vz vz1 vz2 R q q2 ty x xz p Z Zd Z1 Z2 Zhat D rd pot k theta e'
 u={n:s.Symbol(n,real=True) for n in names.split()}
 u['p']=s.Symbol('p',positive=True)
 MP,MU,c1,c2,c3,c4=[u[n] for n in ('MP2','MU2','c1','c2','c3','c4')]
 H,HB,v,v1,v2,R,q,q2,t,x,xz,p,Z,Zd,Z1,Zh,D,rd,pot=[u[n] for n in (
     'H','H0','vz','vz1','vz2','R','q','q2','ty','x','xz','p','Z','Zd','Z1','Zhat','D','rd','pot')]
 gam=s.sqrt(1+v*v)
 K=s.Matrix([[H,0,0],[0,H,-t/2],[0,-t/2,H-q]])
 V=s.Matrix([0,v,0]);X=s.Matrix([0,x,xz]);DV=s.zeros(3);DV[2,1]=v1
 B=s.zeros(4)
 B[0,0]=(V.T*(X+K*V))[0]/gam
 for j in range(3):B[0,j+1]=(X+K*V)[j]
 for i in range(3):
  B[i+1,0]=sum(V[j]*DV[i,j] for j in range(3))/gam+(K*V)[i]
  for j in range(3):B[i+1,j+1]=DV[i,j]+gam*K[i,j]
 metric=s.diag(-1,1,1,1);n=s.Matrix([gam,0,v,0])
 acc=B.T*n;hp=metric+n*n.T;pg=s.Matrix([p,0,0,0]);zg=s.Matrix([Zh,0,0,Z1])
 I1=sum(metric[i,i]*metric[j,j]*B[i,j]**2 for i in range(4) for j in range(4))
 I3=s.trace(B*B)
 frame=-MU*(c1*I1+c2*s.trace(B)**2+c3*I3-c4*(acc.T*metric*acc)[0])/2
 gravity=MP*(s.trace(K*K)-s.trace(K)**2)/2
 reg=u['b']*Z*Z/2-u['b']*(zg.T*hp*pg)[0]-u['b']*Z*(acc.T*pg)[0]
 force=u['K_Q']*(n.T*pg)[0]**2/2-u['A']*p**3*s.Abs(v)**3
 scalar=(D*D+rd*rd)/2-u['zeta']*u['Rc']**2*D*D*v*v/2-pot
 L=CLEAN(gravity+frame+reg+force+scalar)
 # Differentiation precedes the restriction Xz=0. Its momentum drives the lapse flux.
 pvz=CLEAN(s.diff(L,xz).subs(xz,0))
 energy=CLEAN(sum(u[name]*s.diff(L,u[name]) for name in ('H','q','ty','x','xz','p','Zhat','D','rd'))-L)
 sub={x:-HB*v-R*v1,xz:0,Zh:Zd-R*Z1}
 LS=CLEAN(L.subs(sub));E=CLEAN(energy.subs(sub))
 coeff=CLEAN(s.diff(LS,t,2));affine=CLEAN(s.diff(LS,t).subs(t,0))
 ty_sol=CLEAN(-affine/coeff)
 den=MP-MU*(c1+c3+2*c3*v*v-2*c4*(1+v*v)*v*v)
 ty_expected=-MU*(c1+c3+2*c3*v*v)*v1/(gam*den)
 ch.zero('transverse_first_integral_from_full_density',s.diff(LS,t).subs(t,ty_sol))
 ch.zero('transverse_explicit_solution',ty_sol-ty_expected)
 ch.zero('transverse_denominator',2*coeff-den)
 ch.zero('no_transverse_shift_value_in_restricted_density',s.diff(LS,R,t))
 LE=CLEAN(LS.subs(t,ty_sol))
 dz=lambda f:CLEAN(s.diff(f,v)*v1+s.diff(f,v1)*v2+s.diff(f,Z)*Z1+s.diff(f,Z1)*u['Z2'])
 PP=CLEAN(-s.diff(LE,q,2));BB=CLEAN(s.diff(LE,R,q));CC=CLEAN(s.diff(LE,R,2))
 DD=CLEAN(s.diff(LE,q).subs({R:0,q:0}));EE=CLEAN(s.diff(LE,R).subs({R:0,q:0}))
 WW=CLEAN(dz(BB)-CC);ff=CLEAN(EE-dz(DD))
 TT=c4+(c1-(c2+c3)*v*v)/(1+v*v)
 ch.zero('longitudinal_principal_coefficient',PP-MU*(c1+c2+c3)*(1+v*v))
 ch.zero('longitudinal_mixed_coefficient',BB+MU*c2*v*v1)
 ch.zero('longitudinal_potential',WW+MU*((c2+TT)*v1*v1+c2*v*v2))
 EL=CLEAN(s.diff(LE,R)-dz(s.diff(LE,q))-s.diff(s.diff(LE,q),R)*q-s.diff(LE,q,2)*q2)
 ch.zero('full_longitudinal_Euler_identity',EL-(PP*q2+dz(PP)*q-WW*R+ff))
 for name in ('D','rd','pot','K_Q','A','Zd'):
  ch.zero('longitudinal_source_independent_of_'+name,s.diff(ff,u[name]))
 for name in ('H','H0'):
  ch.zero('longitudinal_source_affine_'+name,s.diff(ff,u[name],2))
 E=CLEAN(E.subs(t,ty_sol));flux=CLEAN(gam*pvz.subs(sub).subs(t,ty_sol))
 fluxdiv=dz(flux)
 ch.add('local_lapse_flux_not_identically_zero',fluxdiv!=0,str(flux))
 ch.zero('cusp_lapse_energy_sign',s.diff(E,u['A'])+2*p**3*s.Abs(v)**3)
 baseE=CLEAN(E.subs({v:0,v1:0,R:0,q:0,Z:0,Zd:0,Z1:0}))
 M=MP+MU*(c1+3*c2+c3)/2
 ch.zero('zero_amplitude_background_energy',baseE+3*M*H*H-(u['K_Q']*p*p+D*D+rd*rd)/2-pot)
 # Leading longitudinal coefficient, derived before reading its archived value.
 e,theta,k=u['e'],u['theta'],u['k']
 fexp=ff.subs({H:HB,v:e*s.cos(theta),v1:-k*e*s.sin(theta),v2:-k*k*e*s.cos(theta),Z:0,Z1:0})
 f2=s.simplify(s.diff(fexp,e,2).subs(e,0)/2)
 r2=s.simplify(f2/(4*k*k*MU*(c1+c2+c3)))
 ch.zero('quadratic_longitudinal_bridge_equation',-MU*(c1+c2+c3)*k*k*s.diff(r2,theta,2)-f2)
 ch.zero('quadratic_longitudinal_odd_parity',r2.subs(theta,-theta)+r2)
 ch.zero('quadratic_longitudinal_node_value',r2.subs(theta,s.pi/2))
 formula=dict(
  density=str(L),restricted_density=str(LS),frame_tensor=str(B),
  transverse=dict(derivative=str(ty_sol),denominator=str(den),
      first_integral='L_ty=0; Cy=partial_z L_ty',mean='primitive is odd in V_y, so its full-period mean vanishes'),
  longitudinal=dict(P=str(PP),B=str(BB),W=str(WW),f=str(ff),
      equation='-(P*Rprime)prime+W*R=f; R=Sz',
      quadratic_R2=str(r2),sector='odd, pi-periodic in theta=kz; zero mean and zero at leading profile nodes'),
  energy_without_dust=str(E),lapse_flux=str(flux),lapse_flux_divergence=str(fluxdiv),
  lapse_equation='epsilon=-E_rest-partial_z(gamma*pVz) at N=C=a=1',
  mean_equation='<E_rest>+rho0=0; local flux retained before periodic averaging',
  charge='D=d/(1-zeta*Rc^2*e^2/2); local angular factor 1-zeta*Rc^2*e^2',
  coercivity=dict(s0='c1+c2+c3',Tmax='abs(c4)+abs(c1)+abs(c2+c3)*Emax^2',
      kappa='s0-Emax^2*(2abs(c2)+Tmax)/4',
      proof='P>=MU2*s0, |W|<=MU2*k^2*Emax^2*(2abs(c2)+Tmax), ||R||<=||Rprime||/(2k)',
      lower_bound='int[P Rprime^2+W R^2]>=MU2*kappa*||Rprime||^2',
      source_bound='||Rprime||<=||f||/(2k MU2 kappa)',
      exclusions='Only declared odd parity sector; no full zero-mode, GR endpoint, Cauchy or physical-window conclusion'),
  full_initial_acceptance='OPEN: mean root, full candidate density/positivity, regulator completion and certified lower-order/full-constraint bridge not supplied by operator reduction alone')
 return u,dict(L=L,LS=LS,E=E,flux=flux,fluxdiv=fluxdiv,ty=ty_sol,P=PP,W=WW,f=ff,R2=r2),formula


def coordinate_case(H,H0,v,v1,Sy,R,q,ty,p,Z,Zd,Z1,D,rd,Rc):
 """Independent four-coordinate metric and normalized-frame first jets."""
 def point(xx):
  tt,zz=xx[0],xx[3]
  h=(1+2*H*tt)*mp.eye(3)
  S=mp.matrix([0,Sy+ty*zz,R+q*zz])
  V=mp.matrix([0,v+v1*zz-H0*v*tt,0])
  gam=mp.sqrt(1+(V.T*h*V)[0]);n=mp.matrix([gam]+list(V-gam*S))
  g=mp.zeros(4);g[0,0]=-1+(S.T*h*S)[0]
  for i in range(3):
   g[0,i+1]=g[i+1,0]=(h*S)[i]
   for j in range(3):g[i+1,j+1]=h[i,j]
  return g,n
 origin=[mp.mpf(0)]*4;g,n=point(origin);gi=g**-1
 def partial(fn,mu):
  def at(z):
   xx=list(origin);xx[mu]=z;return fn(xx)
  return mp.diff(at,0)
 dg=[mp.matrix([[partial(lambda xx:point(xx)[0][i,j],a) for j in range(4)] for i in range(4)]) for a in range(4)]
 conn=[[[sum(gi[c,l]*(dg[a][l,b]+dg[b][l,a]-dg[l][a,b]) for l in range(4))/2
          for b in range(4)] for a in range(4)] for c in range(4)]
 DN=mp.matrix([[partial(lambda xx:point(xx)[1][b],a)+sum(conn[b][a][l]*n[l] for l in range(4))
                for b in range(4)] for a in range(4)])
 K=mp.matrix([[H,0,0],[0,H,-ty/2],[0,-ty/2,H-q]])
 grads={name:mp.matrix([D if name=='v' else rd if name=='r' else p if name=='psi' else Zd if name=='Z' else 1 if name=='T' else 0,0,0,Z1 if name=='Z' else 0]) for name in ('u','v','r','psi','Z','T')}
 DV=mp.zeros(3);DV[2,1]=v1
 return dict(g=g,gi=gi,n=n,DN=DN,Kraw=K,R3=mp.mpf(0),u=Rc,v=mp.mpf(0),r=Rc,
   psi=mp.mpf(0),Z=Z,epsilon=mp.mpf('0.2'),coord_grad=grads,
   h=mp.eye(3),hi=mp.eye(3),V=mp.matrix([0,v,0]),gamma=mp.sqrt(1+v*v),DV=DV,
   proper={name:grad[0]-R*grad[3] for name,grad in grads.items()},
   spatial={name:mp.matrix(list(grad)[1:]) for name,grad in grads.items()})


def independent(ch,u,expr,old):
 print('ORIGINAL_COORDINATE_DENSITY_CONTROLS',flush=True)
 args=[u[n] for n in sorted(u) if u[n] in expr['LS'].free_symbols]
 fn=s.lambdify(args,expr['LS'],'mpmath',cse=True)
 records=[]
 for amplitude in (mp.mpf(1)/500,-mp.mpf(1)/500,mp.mpf(1)/1000,-mp.mpf(1)/1000,mp.mpf(1)/2000,-mp.mpf(1)/2000):
  for angle in (mp.pi/7,mp.pi/3,4*mp.pi/5):
   H,HB=mp.mpf(2)/7,mp.mpf(3)/11
   v=amplitude*mp.cos(angle);v1=-40*amplitude*mp.sin(angle)
   R=amplitude**2*mp.sin(2*angle)/13;q=80*amplitude**2*mp.cos(2*angle)/13
   Sy=amplitude*mp.cos(angle)/17;ty=-40*amplitude*mp.sin(angle)/17
   p=mp.mpf(1)/20;Z=amplitude**2*mp.cos(angle)**2/19
   Z1=-40*amplitude**2*mp.sin(2*angle)/19;Zd=amplitude**2*mp.cos(angle)**2/23
   for family in FAMILIES:
    for eta in ETAS:
     par=old.parameters(family,eta,'mp');rc=mp.sqrt(mp.mpf(s.Rational(eta).p)/int(s.Rational(eta).q))
     D=rc;rd=rc/4
     c=coordinate_case(H,HB,v,v1,Sy,R,q,ty,p,Z,Zd,Z1,D,rd,rc)
     direct=old.mp_body(c,par,mp.zeros(12,1),p,Zd,coordinate=True,include_dust=False)
     pot=par['m2']*rc**2/2+par['lambda4']*rc**4/8+par['lambda6']*rc**6/(24*par['Lambda']**2)+par['mr2']*rc**2/2+par['lambda_r']*rc**4/4+par['g_r']*rc**4/4+par['rho_Lambda']
     values=dict(par,H=H,H0=HB,vz=v,vz1=v1,R=R,q=q,ty=ty,p=p,Z=Z,Zd=Zd,Z1=Z1,D=D,rd=rd,Rc=rc,pot=pot)
     candidate=fn(*[values[str(a)] for a in args])
     err=abs(direct-candidate)/max(1,abs(direct),abs(candidate))
     tag=family+'_'+eta+'_'+SHOW(amplitude)+'_'+SHOW(angle)
     ch.small('full_coordinate_density_'+tag,err,'1e-50')
     records.append(dict(family=family,eta=eta,amplitude=SHOW(amplitude),angle=SHOW(angle),density_error=SHOW(err)))
 return records


def controls(ch,u,expr,old):
 print('COERCIVITY_AND_ARCHIVED_QUADRATIC_SHIFT_BRIDGE',flush=True)
 planar=json.loads((ROOT/PLANAR).read_bytes())
 eta_sym=s.Symbol('eta')
 certs=[]
 for family in FAMILIES:
  for eta in ETAS:
   par={name:s.sympify(value,locals={'eta':eta_sym}).subs(eta_sym,s.Rational(eta))
        for name,value in planar['families'][family]['parameter_map'].items()}
   Emax=s.Rational(1,500);mu=par['MU2'];mp2=par['MP2']
   c1,c2,c3,c4=[par[n] for n in ('c1','c2','c3','c4')]
   tmax=abs(c4)+abs(c1)+abs(c2+c3)*Emax**2
   kap=CLEAN(c1+c2+c3-Emax**2*(2*abs(c2)+tmax)/4)
   den=CLEAN(mp2-mu*abs(c1+c3)-2*mu*(abs(c3)+abs(c4)*(1+Emax**2))*Emax**2)
   tag=family+'_'+eta
   ch.add('exact_longitudinal_coercivity_'+tag,mu>0 and kap>0,str(mu*kap),'positive exact rational; all |e|<=1/500')
   ch.add('exact_transverse_denominator_'+tag,den>0,str(den),'positive exact rational; all |e|<=1/500')
   certs.append(dict(family=family,eta=eta,amplitude_bound=str(Emax),kappa=str(kap),
       weighted_coercivity=str(mu*kap),transverse_denominator_lower=str(den)))
 # The archive is read only after deriving the new R2 expression.
 args=[u[n] for n in sorted(u) if u[n] in expr['R2'].free_symbols]
 fn=s.lambdify(args,expr['R2'],'mpmath',cse=True)
 runs=json.loads((ROOT/RET).read_bytes())['runs']
 ch.add('all18_archived_initial_runs_retained',len(runs)==18 and {
  (r['family'],r['eta_exact'],r['method']) for r in runs}=={
   (f,e,m) for f in FAMILIES for e in ETAS for m in ('Radau','DOP853')})
 records=[]
 for ir,run in enumerate(runs):
  ev=run['events'][0];bg=list(map(NUM,ev['background_and_first_wave']))
  par=old.parameters(run['family'],run['eta_exact'],'mp')
  q0=list(map(CX,ev['full_response']['mean']['response']))
  q2=list(map(CX,ev['full_response']['second']['response']))
  errors=[]
  for theta in (mp.pi/7,mp.pi/3,4*mp.pi/5):
   values=dict(par,H0=bg[1],k=40,theta=theta)
   action=fn(*[values[str(a)] for a in args])
   archived=q0[3]+2*mp.re(q2[3]*mp.exp(2j*theta))  # Sz is original field index 3.
   errors.append(abs(action-archived)/(1+abs(action)+abs(archived)))
  err=max(errors)
  ch.small('quadratic_longitudinal_archive_'+str(ir)+'_'+run['family']+'_'+run['eta_exact']+'_'+run['method'],err,'1e-10')
  records.append(dict(family=run['family'],eta=run['eta_exact'],method=run['method'],
                      maximum_quadratic_shift_error=SHOW(err)))
 return dict(exact_coercivity=certs,archive_bridge=records)


def calculate():
 mp.mp.dps=80
 pins,before=sources();ch=Checks();u,expr,formula=derive(ch)
 spec=importlib.util.spec_from_file_location('r4c1_initial_original',ROOT/CANON)
 old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 rows=independent(ch,u,expr,old)
 numeric=controls(ch,u,expr,old)
 _,after=sources();ch.add('all_sources_sidecars_and_metadata_preserved',before==after)
 ok=all(row['passed'] for row in ch.rows)
 summary=dict(validation='PASS_EXACT_INITIAL_SYSTEM_CONTROLS_ONLY' if ok else 'FAIL_INITIAL_SYSTEM_IDENTITIES_OR_CONTROLS',
  passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,
  source_sha256=pins,source_metadata=before,initial_data_acceptance_met=False,
  full_nonlinear_initial_data_admitted=False,stage2_complete=False,stage3_entered=False,
  physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
  status='PARTIAL_EXACT_INITIAL_CONSTRAINT_SYSTEM_FULL_DATA_CERTIFICATION_OPEN',
  missing_initial_acceptance=['certify the mean H root with both exact global charges',
   'construct full lapse-derived density and prove its pointwise positivity',
   'complete regulator data and all normal-jet compatibility, with exact lower-order bridge',
   'verify every local constraint on the completed candidate with controlled errors'],
  missing_physical_acceptance=['persistence and full 3D/rank-changing reduction',
   'physical Hessian, Cauchy/energy domain, nonlinear remainder and physical validity window',
   'healthy GR and identifying matter-residue/nonlinear-force matching inputs'])
 return {'summary.json':summary,'formulas.json':formula,'independent.json':rows,'controls.json':numeric}


def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output');parser.add_argument('--replay');args=parser.parse_args()
 if bool(args.output)==bool(args.replay):parser.error('choose exactly one fresh output or read-only replay')
 dest=(ROOT/(args.output or args.replay)).resolve()
 if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific output root')
 if args.output:dest.mkdir(parents=True,exist_ok=False)
 original={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
 data=calculate();payloads={name:ENC(value) for name,value in data.items()}
 for name,value in list(payloads.items()):payloads[name+'.sha256']=(SHA(value)+'  '+name+'\n').encode('ascii')
 if args.replay:
  if set(original)!=set(payloads):raise ValueError('replay file-set mismatch')
  for name,value in payloads.items():
   path=dest/name
   if path.read_bytes()!=value or (SHA(path.read_bytes()),path.stat().st_size,path.stat().st_mtime_ns)!=original[name]:
    raise ValueError('replay byte/metadata mismatch '+name)
  print('READ_ONLY_REPLAY_EXACT',flush=True)
 else:
  for name,value in payloads.items():
   with (dest/name).open('xb') as stream:stream.write(value)
 su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','initial_data_acceptance_met','status')}),flush=True)
 return 0 if su['passed']==su['total'] else 1


if __name__=='__main__':raise SystemExit(main())
