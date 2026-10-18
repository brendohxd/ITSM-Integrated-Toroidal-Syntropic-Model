"""Validated known initial constraints; full rank-changing IVP remains open."""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_CONTRACT_2026-10-18.md'
PREV='Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01/'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
PREP='Analysis/MasterTests/outputs/r4c1_initial_charge_completion_attempt_04/formulas.json'
RET='Analysis/MasterTests/outputs/r4c1_fixed_charge_retarded_comparison_attempt_03/trajectories.json'
PINS={
 CONTRACT:'88b0ddb963912de6ddca377108361bcb9a584686826a6934bdc598adb6b0a7a2',
 PREV+'formulas.json':'beaf647957a18ddd14881333de29cebc9a567ffcc62a9b4d775153984a0add73',
 PREV+'summary.json':'586fe456022419f65965750ecc3137cf74b6eafb84f3a4dec670f2f611f51b3f',
 'Analysis/MasterTests/test_01_r4c1_initial_constraint_v1.py':'6ba9c73d71d2ef9dd3fc59f34d5fe781d528d5636a29a85bed748290bda989ff',
 'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CONSTRAINT_V1_REPORT_2026-10-18.md':'44113ba26531526435206a520495e56e5d57cae3c8e6843595a0dc871d9dd305',
 PLANAR:'852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
 PREP:'b1f62daaebdb1602ccc20350669b22aeb601d7e8d8cccad4626e420e317bb6f3',
 RET:'3e36b9594ec4f186fff610a291011b6344b23ba98645922dfd7ad78d242ee4b3',
 'Analysis/MasterTests/test_01_r4c1_interacting_background.py':'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
 'Analysis/MasterTests/test_01_r4c1_initial_charge_completion_v4.py':'af22270b76b72d29a04bdfba366464bcc2482ec5f2e41f5ffe66061fee7f4020',
 'Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py':'4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada',
 'Analysis/MasterTests/test_01_r4c1_regulator_node_v1.py':'7126d03a3b3a3a525bf1ce4c8b31c8541901f9d7c45ad82c288db71cc97cfa25',
 'Theory/Gates/RES-001/RES001_R4C1_REGULATOR_NODE_V1_REPORT_2026-10-17.md':'b47dcf5e7fc340a015f2e7cdf273157bc6e2e1ba311bbc543a5f66596dbc83d2',
 'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md':'4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c',
 'GEMINI.md':'5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
 'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md':'d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md':'3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
 'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':'14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
}
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
ETAS=('1/4','1/64','1/1024')
SHA=lambda data:hashlib.sha256(data).hexdigest()
ENC=lambda data:(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CLEAN=lambda value:s.factor(s.cancel(s.expand(value)))
SHOW=lambda value:mp.nstr(value,60)
iv=mp.iv
READ=lambda name:json.loads((ROOT/name).read_bytes())


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


def lo(value):return mp.mpf(value._mpi_[0])
def hi(value):return mp.mpf(value._mpi_[1])
def point(value):return iv.mpf([value,value])
def upper(value):return point(hi(value))
def lower(value):return point(lo(value))
def box(value):return iv.mpf([-hi(value),hi(value)])
def midpoint(value):return (lo(value)+hi(value))/2
def pack(value):
 return dict(lower=SHOW(lo(value)),upper=SHOW(hi(value)),
  exact_binary_endpoints=[list(value._mpi_[0]),list(value._mpi_[1])])


class Eval:
 def __init__(self,expressions):
  self.expressions=list(expressions)
  if any(expr.atoms(s.Float) for expr in self.expressions):
   raise ValueError('Unregistered approximate constants in certificate expression')
  self.args=sorted(set().union(*(expr.free_symbols for expr in self.expressions)),key=str)
  self.fn=s.lambdify(self.args,self.expressions,'mpmath',cse=True)
  self.fi=s.lambdify(self.args,self.expressions,'mpmath',cse=True)
  self.fi.__globals__.update(mpf=iv.mpf,sqrt=iv.sqrt,sin=iv.sin,cos=iv.cos,
      pi=iv.pi,Abs=abs,abs=abs)
 def interval(self,values):return self.fi(*[values[str(a)] for a in self.args])
 def numeric(self,values):return self.fn(*[values[str(a)] for a in self.args])


def exact_fraction(raw):
 sign,man,exponent,bits=raw
 value=Fraction((-1 if sign else 1)*man,1)
 return value*(2**exponent if exponent>=0 else Fraction(1,2**(-exponent)))


def symbolic(ch):
 print('REUSE_EXACT_INITIAL_SYSTEM_BUILD_CONTROLLED_SHIFT_APPROXIMATION',flush=True)
 data=READ(PREV+'formulas.json')
 names='MP2 MU2 c1 c2 c3 c4 K_Q A b zeta Rc H H0 vz vz1 vz2 R q q2 ty x xz p Z Zd Z1 Z2 Zhat D rd pot k theta e alpha xi zc d'
 u={n:s.Symbol(n,real=True) for n in names.split()};u['p']=s.Symbol('p',positive=True)
 parse=lambda text:s.sympify(text,locals=u)
 E=parse(data['energy_without_dust']);flux=parse(data['lapse_flux_divergence'])
 H,HB,v,v1=u['H'],u['H0'],u['vz'],u['vz1']
 mu,k,c1,c2,c3,c4=[u[n] for n in ('MU2','k','c1','c2','c3','c4')]
 a,x,zc=u['alpha'],u['xi'],u['zc'];s0=c1+c2+c3
 A0=c1+2*c2+c4+(c2-c3+c4)*v*v
 AH=3*c1+5*c2+c3+2*c4+(2*c1+4*c2+2*c4)*v*v
 fcompact=mu*v*v1/(1+v*v)*(HB*A0-H*AH)+u['b']*u['p']*(u['Z']*v*v1+u['Z1']*v*v)
 ch.zero('compact_source_matches_sealed_action_formula',fcompact-parse(data['longitudinal']['f']))
 Q=lambda p:(2*x-1)*p-2*x*(1-x)*s.diff(p,x)
 J=lambda p:4*x*(1-x)*s.diff(p,x,2)+6*(1-2*x)*s.diff(p,x)-4*p
 C,S=s.symbols('C S',real=True)
 deriv=lambda e:-S*s.diff(e,C)+C*s.diff(e,S)
 for n in range(4):
  rr=C*S*C**(2*n);res=deriv(deriv(rr))-C*S*J(x**n).subs(x,C*C)
  ch.zero('polynomial_theta_operator_'+str(n),s.rem(s.Poly(s.expand(res),S),s.Poly(S*S+C*C-1,S)).as_expr())
 P0=mu*s0
 T=c4+(c1-(c2+c3)*a*x)/(1+a*x)
 W=-mu*k*k*a*((c2+T)*(1-x)-c2*x)
 fB=-mu*k*a*(HB*(c1+2*c2+c4+(c2-c3+c4)*a*x)
       -H*(3*c1+5*c2+c3+2*c4+(2*c1+4*c2+2*c4)*a*x))/(1+a*x)-3*u['b']*u['p']*zc*k*a*a*x
 def numerator(p):
  return CLEAN((1+a*x)*(-P0*k*k*((1+a*x)*J(p)-2*a*Q(p))+W*p-fB))
 poly=s.Integer(0);pieces=[]
 for n in range(1,4):
  known=s.Poly(numerator(poly),a).coeff_monomial(a**n)/(P0*k*k)
  mat=s.Matrix([[s.Poly(J(x**j),x).coeff_monomial(x**i) for j in range(n)] for i in range(n)])
  rhs=s.Matrix([s.Poly(CLEAN(known),x).coeff_monomial(x**i) for i in range(n)])
  coefficients=mat.inv()*rhs
  pn=CLEAN(sum(coefficients[j]*x**j for j in range(n)))
  poly+=a**n*pn;pieces.append(str(pn))
 residual=s.Poly(numerator(poly),a,x)
 for n in range(4):
  ch.zero('residual_lower_amplitude_order_'+str(n),s.Poly(residual.as_expr(),a).coeff_monomial(a**n))
 ch.add('finite_approximation_not_treated_as_exact',residual.as_expr()!=0)
 ch.zero('shift_H_dependence_affine',s.diff(poly,H,2))
 rterms=list(residual.terms())
 residual_eval=Eval([term for powers,term in rterms]+[s.diff(term,H) for powers,term in rterms])
 polynomial_eval=Eval([poly,Q(poly),s.diff(poly,H),s.diff(Q(poly),H)])
 ch.zero('energy_reflection_symmetry',E.subs({v1:-v1,u['R']:-u['R'],u['Z1']:-u['Z1']},simultaneous=True)-E)
 ch.zero('energy_amplitude_sign_symmetry',E.subs({v:-v,v1:-v1},simultaneous=True)-E)
 ch.zero('flux_reflection_symmetry',flux.subs({v1:-v1,u['R']:-u['R'],u['Z1']:-u['Z1']},simultaneous=True)-flux)
 ch.zero('flux_amplitude_sign_symmetry',flux.subs({v:-v,v1:-v1,u['vz2']:-u['vz2']},simultaneous=True)-flux)
 # A C2 cusp has zero quadratic coefficient; no ordinary third derivative is used.
 analytic=E.subs(u['A'],0)
 base={v:0,v1:0,u['R']:0,u['q']:0,u['Z']:0,u['Zd']:0,u['Z1']:0,H:HB,u['D']:u['d']}
 EH0=CLEAN(s.diff(analytic,H).subs(base))
 EW=CLEAN(s.diff(analytic,v,2).subs(base))
 EV1=CLEAN(s.diff(analytic,v1,2).subs(base))
 M=u['MP2']+mu*(c1+3*c2+c3)/2
 ch.zero('mean_root_nonzero_background_derivative',EH0+6*M*HB)
 phase2=u['d']*u['zeta']*u['Rc']**2/2
 H2=CLEAN(-(u['d']*phase2+(EW+k*k*EV1)/4)/EH0)
 H3=-4*u['A']*u['p']**3/(9*s.pi*M*HB)
 old=READ(PREP)
 prior3=s.sympify(old['necessary_initial_volume_velocity_abs_e3'],locals={
     'A':u['A'],'pd':u['p'],'H':HB,'M':M,'pi':s.pi})
 ch.zero('mean_cusp_counter_retains_original_volume_result',3*H3-prior3)
 prior2=s.sympify(old['quadratic_phase_counter'],locals={'R':u['Rc'],'d':u['d'],'zeta':u['zeta']})
 ch.zero('phase_counter_retains_original_result',phase2-prior2)
 # Exact removable normal numerators when complete forward momenta are used.
 sig,pp,bb,zz=s.symbols('sigma p_full b_full Zhat_full',real=True)
 ch.zero('psi_inverse_numerator_both_normal_jets',[(-sig**2*pp).subs(sig,0),s.diff(-sig**2*pp,sig).subs(sig,0)])
 ch.zero('Z_inverse_numerator_both_normal_jets',[(-bb*sig**2*zz).subs(sig,0),s.diff(-bb*sig**2*zz,sig).subs(sig,0)])
 theta=s.Symbol('theta',real=True);zdc=s.Symbol('zdc',real=True)
 zprofile=zc*a*s.cos(theta)**2;zdprofile=zdc*a*s.cos(theta)**2
 ch.zero('regulator_node_fields_and_first_spatial_jets',[
     e.subs(theta,s.pi/2) for e in (zprofile,zdprofile,s.diff(zprofile,theta),s.diff(zdprofile,theta))])
 energy_eval=Eval([E,flux,s.diff(E,H),s.diff(E,u['R']),s.diff(E,u['q'])])
 lower_eval=Eval([H2,phase2])
 mass= s.sympify(READ(PLANAR)['generic_frame_mass_squared'],locals=u)
 cv=s.sympify(READ(PLANAR)['generic_cV2'],locals=u)
 mass_eval=Eval([mass,cv])
 proof=dict(polynomial_pieces=pieces,residual_numerator=str(residual.as_expr()),
     residual_powers=[list(powers) for powers,coef in rterms],
     H2=str(H2),H3=str(H3),phase2=str(phase2),
     interval_precision=80,endpoint_precision=110,mpmath_version=mp.__version__,sympy_version=s.__version__,
     residual_proof='R=B*poly(alpha,x), x=cos^2(theta), B=cos(theta)sin(theta). Exact residual=B*N(alpha,x)/(1+alpha*x). |B|<=1/2, x in[0,1]. No asymptotic estimate replaces the residual.',
     error_proof='On a Dirichlet half-cell L=pi/(2k)<2/k, coercivity gives ||deltaRprime||2<=sqrt(L)*rinf/(2k*MU2*kappa). Therefore |deltaR|<=L*rinf/(2k*MU2*kappa). For J=P*deltaRprime, integral J/P=0 gives a zero of J; |deltaRprime|<=L*(Wmax*Rerr+rinf)/Pmin. The same proof applies to d_H R.',
     root_proof='Strict opposite mean signs plus continuity give existence. Strict negative total H derivative, including exact inverse sensitivity, gives uniqueness. Approximation errors are enclosed, not ignored.',
     positivity_proof='Density=-E_rest-local_flux is enclosed for all H in the fixed bracket, all angles and all |e|<=1/500.',
     known_constraint_definition='Exact transverse primitive, unique coercive R(H), unique mean root H(e), exact phase charge and pointwise lapse-defined density. This defines an implicit candidate; it is not an adopted evolved state.',
     node_proof='Inherited exact chi=Z+Delta psi+p divV and its transport. Initial psi and p are homogeneous, N=1, V=(0,w(z),0), and R vanishes at nodes by parity. Thus the initial nodal equations reduce to Z=0 and Zd=0. Both regulator profiles have cos^2 factors. Complete forward momenta give Fpsi=-w^2*p and FZ=-b*w^2*Zhat; numerator values and first normal jets vanish. Higher compatibility is not inferred.',
     unproved=['full higher/rank-changing Dirac consistency','persistence or nonlinear temporal Cauchy theorem','physical reduced Hessian/domain/window and healthy GR','identifying matter/nonlinear-force matching'])
 return u,dict(residual_eval=residual_eval,residual_terms=rterms,poly=polynomial_eval,
     energy=energy_eval,lower=lower_eval,mass=mass_eval),proof


def interval_prerequisites(ch):
 x=s.Symbol('x')
 f=Eval([x/s.Integer(3)])
 result=f.interval({'x':iv.mpf(1)})[0]
 ch.add('outward_rational_constant_printer',exact_fraction(result._mpi_[0])<=Fraction(1,3)<=exact_fraction(result._mpi_[1]))
 ch.add('interval_library_precision',iv.dps==80 and mp.mp.dps==110)
 src=inspect.getsource(f.fi)
 ch.add('rational_printer_uses_interval_mpf','mpf(1)/mpf(3)' in src,src.strip())
 test=iv.sqrt(iv.mpf(2))**2
 ch.add('interval_sqrt_squared_contains_exact_two',lo(test)<=2<=hi(test),pack(test))


def numeric_s(expr):return mp.mpf(str(s.N(expr,110)))
def interval_s(expr):
 if expr.is_Rational:return iv.mpf(int(expr.p))/iv.mpf(int(expr.q))
 if expr.func==s.Pow and expr.args[1]==s.Rational(1,2):return iv.sqrt(interval_s(expr.args[0]))
 if expr.is_Add:return sum((interval_s(a) for a in expr.args),iv.mpf(0))
 if expr.is_Mul:
  out=iv.mpf(1)
  for a in expr.args:out*=interval_s(a)
  return out
 if expr.is_Pow and expr.args[1].is_Integer:return interval_s(expr.args[0])**int(expr.args[1])
 raise ValueError('Nonexact parameter conversion '+str(expr))


def case_data(family,eta,functions):
 raw=READ(PLANAR)['families'][family]['parameter_map'];es=s.Symbol('eta');ee=s.Rational(eta)
 exact={name:s.sympify(value,locals={'eta':es}).subs(es,ee) for name,value in raw.items()}
 data={name:interval_s(value) for name,value in exact.items()}
 rc=iv.sqrt(interval_s(ee));data.update(Rc=rc,d=rc,rd=rc/4,p=interval_s(ee)/5,k=iv.mpf(40))
 pot=3*interval_s(ee)/2+interval_s(ee)**2*(iv.mpf(1)/24+iv.mpf(1)/28)+interval_s(ee)**3*(iv.mpf(1)/480+iv.mpf(3)/28)
 rho=iv.mpf(1)/5;M=data['MP2']+data['MU2']*(data['c1']+3*data['c2']+data['c3'])/2
 kin=data['d']**2+data['rd']**2+data['K_Q']*data['p']**2
 HB=iv.sqrt((kin/2+pot+rho)/(3*M));Hd=-(kin+rho)/(2*M)
 pd=-3*HB*data['p']-data['beta']*rho/data['K_Q'];rhod=(-3*HB+data['beta']*data['p'])*rho
 values=dict(data,H=HB,H0=HB,Hdot=Hd,psi_dot=data['p'],u0=rc,v0=iv.mpf(0),
             u_dot=iv.mpf(0),v_dot=data['d'])
 mass,cv=functions['mass'].interval(values);wdd=-(cv*data['k']**2+mass)
 zc=HB*data['p']+data['beta']*rho/data['K_Q']
 zdc=Hd*data['p']+HB*pd+data['beta']*rhod/data['K_Q']-wdd*data['p']
 data.update(H0=HB,pot=pot,zc=zc,zdc=zdc,rho=rho,M=M,Hdot=Hd,pdd=pd,wdd=wdd)
 emax=iv.mpf(1)/500;amax=upper(emax**2)
 data.update(emax=upper(emax),amax=amax,alpha=iv.mpf([0,hi(amax)]),e=iv.mpf([0,hi(emax)]))
 Hlo=49*HB/50;Hhi=51*HB/50;Hall=iv.mpf([lo(Hlo),hi(Hhi)])
 s0=data['c1']+data['c2']+data['c3']
 Tmax=abs(data['c4'])+abs(data['c1'])+abs(data['c2']+data['c3'])*amax
 kap=s0-amax*(2*abs(data['c2'])+Tmax)/4
 coerce=lower(data['MU2']*kap);Pmin=lower(data['MU2']*s0)
 Wmax=upper(data['MU2']*data['k']**2*amax*(2*abs(data['c2'])+Tmax))
 context=dict(data,H=Hall)
 residuals=functions['residual_eval'].interval(context)
 nn=len(functions['residual_terms'])
 def residual_bound(coeffs):
  total=iv.mpf(0)
  for (powers,expression),coef in zip(functions['residual_terms'],coeffs):
   total+=upper(abs(coef))*amax**powers[0]  # xi^j<=1.
  return upper(total/2)
 rmax=residual_bound(residuals[:nn]);rhmax=residual_bound(residuals[nn:])
 length=iv.mpf(2)/data['k']
 def errors(rr):
  Rerr=upper(length*rr/(2*data['k']*coerce))
  qerr=upper(length*(Wmax*Rerr+rr)/Pmin)
  return Rerr,qerr
 Rerr,qerr=errors(rmax);RHerr,qHerr=errors(rhmax)
 return dict(family=family,eta=eta,values=data,Hlo=Hlo,Hhi=Hhi,Hall=Hall,
     coerce=coerce,Pmin=Pmin,Wmax=Wmax,kappa=kap,residual=rmax,H_residual=rhmax,
     Rerr=Rerr,qerr=qerr,RHerr=RHerr,qHerr=qHerr)


def state_intervals(case,H,theta,functions):
 data=dict(case['values']);cs=iv.cos(theta);sn=iv.sin(theta);x=cs**2;B=cs*sn
 data.update(H=H,xi=x)
 poly,qpoly,polyH,qpolyH=functions['poly'].interval(data)
 a=data['alpha'];k=data['k']
 data.update(vz=data['e']*cs,vz1=-k*data['e']*sn,vz2=-k*k*data['e']*cs,
  R=B*poly+box(case['Rerr']),q=k*qpoly+box(case['qerr']),
  Z=data['zc']*a*x,Zd=data['zdc']*a*x,Z1=-2*k*data['zc']*a*B,
  Z2=-2*k*k*data['zc']*a*(2*x-1),
  D=data['d']/(1-data['zeta']*data['Rc']**2*a/2))
 RH=B*polyH+box(case['RHerr']);qH=k*qpolyH+box(case['qHerr'])
 energy,flux,EH,ER,Eq=functions['energy'].interval(data)
 return energy,energy+data['rho'],-energy-flux,EH+ER*RH+Eq*qH


def certify_case(case,functions,ch):
 attempts=[];selected=None
 for n in (16,32,64,128,256):
  meanlo=iv.mpf(0);meanhi=iv.mpf(0);meand=iv.mpf(0);densitylo=None;densityhi=None
  for j in range(n):
   theta=iv.mpf([lo(iv.pi*j/(2*n)),hi(iv.pi*(j+1)/(2*n))])
   elo,flo,rholo,dlo=state_intervals(case,case['Hlo'],theta,functions)
   ehi,fhi,rhohi,dhi=state_intervals(case,case['Hhi'],theta,functions)
   eall,fall,rhoall,dall=state_intervals(case,case['Hall'],theta,functions)
   meanlo+=flo/n;meanhi+=fhi/n;meand+=dall/n
   densitylo=lo(rhoall) if densitylo is None else min(densitylo,lo(rhoall))
   densityhi=hi(rhoall) if densityhi is None else max(densityhi,hi(rhoall))
  angular=1-case['values']['zeta']*case['values']['Rc']**2*case['values']['amax']
  strict=dict(low_mean_positive=lo(meanlo)>0,high_mean_negative=hi(meanhi)<0,
      mean_derivative_negative=hi(meand)<0,dust_density_positive=densitylo>0,
      local_phase_angular_positive=lo(angular)>0,
      coercivity_positive=lo(case['coerce'])>0)
  entry=dict(angular_boxes=n,mean_at_low_H=pack(meanlo),mean_at_high_H=pack(meanhi),
      total_H_mean_derivative=pack(meand),
      dust_density_all_H_angles=pack(iv.mpf([densitylo,densityhi])),
      local_phase_angular=pack(angular),strict_checks=strict)
  attempts.append(entry)
  if all(strict.values()):selected=entry;break
 tag=case['family']+'_'+case['eta']
 ch.add('uniform_constraint_root_and_density_'+tag,selected is not None,
        {'attempt_box_counts':[row['angular_boxes'] for row in attempts]},
        'strict outward bounds, all |e|<=1/500 and all angles in declared parity sector')
 return dict(family=case['family'],eta=case['eta'],
    status='CERTIFIED_KNOWN_CANONICAL_INITIAL_SURFACE' if selected else 'NOT_CERTIFIED_BY_REGISTERED_BOUNDS',
    H_background=pack(case['values']['H0']),H_root_bracket=pack(case['Hall']),
    amplitude_absolute_max=pack(case['values']['emax']),amplitude_squared_range=pack(case['values']['alpha']),
    shift_error=pack(case['Rerr']),shift_gradient_error=pack(case['qerr']),
    shift_H_error=pack(case['RHerr']),shift_H_gradient_error=pack(case['qHerr']),
    exact_operator_residual_bound=pack(case['residual']),
    exact_operator_H_residual_bound=pack(case['H_residual']),
    regulator_coefficient=pack(case['values']['zc']),regulator_velocity_coefficient=pack(case['values']['zdc']),
    attempts=attempts)


def archive_controls(ch,cases,functions):
 records=[];runs=READ(RET)['runs']
 ch.add('all18_archive_runs_retained',len(runs)==18 and {
  (r['family'],r['eta_exact'],r['method']) for r in runs}=={
  (f,e,m) for f in FAMILIES for e in ETAS for m in ('Radau','DOP853')})
 for ir,run in enumerate(runs):
  case=cases[run['family'],run['eta_exact']]
  values={name:midpoint(value) for name,value in case['values'].items()}
  values['H']=values['H0']
  H2,phase2=functions['lower'].numeric(values)
  ev=run['events'][0]
  q0=[mp.mpc(str(v[0]),str(v[1])) for v in ev['full_response']['mean']['response']]
  q2=[mp.mpc(str(v[0]),str(v[1])) for v in ev['full_response']['second']['response']]
  d0=[mp.mpc(str(v[0]),str(v[1])) for v in ev['full_response']['mean']['velocity']]
  d2=[mp.mpc(str(v[0]),str(v[1])) for v in ev['full_response']['second']['velocity']]
  errors=dict(phase=abs(phase2-mp.mpf(str(run['preparation']['phase_velocity'])))/(1+abs(phase2)),
    volume=abs(3*H2-mp.mpf(str(run['preparation']['volume_velocity'])))/(1+abs(3*H2)),
    regulator=mp.mpf(0),regulator_velocity=mp.mpf(0))
  for theta in (mp.pi/7,mp.pi/3,4*mp.pi/5):
   archivedZ=q0[19]+2*mp.re(q2[19]*mp.exp(2j*theta))
   archivedZd=d0[19]+2*mp.re(d2[19]*mp.exp(2j*theta))
   Z=values['zc']*mp.cos(theta)**2;Zd=values['zdc']*mp.cos(theta)**2
   errors['regulator']=max(errors['regulator'],abs(Z-archivedZ)/(1+abs(Z)+abs(archivedZ)))
   errors['regulator_velocity']=max(errors['regulator_velocity'],abs(Zd-archivedZd)/(1+abs(Zd)+abs(archivedZd)))
  for name,error in errors.items():ch.small('archive_'+name+'_'+str(ir)+'_'+run['family']+'_'+run['eta_exact']+'_'+run['method'],error,'1e-10')
  # Signed finite-amplitude diagnostics retain the exact action-defined charge.
  signed=[]
  for den in (500,1000,2000):
   for sign in (-1,1):
    ee=mp.mpf(sign)/den;zeta=values['zeta'];rc=values['Rc'];d=values['d']
    D=d/(1-zeta*rc*rc*ee*ee/2)
    residue=rc*D*(1-zeta*rc*rc*ee*ee/2)-rc*d
    ch.small('signed_charge_'+str(ir)+'_'+str(sign)+'_'+str(den),abs(residue),'1e-50')
    signed.append(dict(amplitude=str(sign)+'/'+str(den),charge_error=SHOW(abs(residue))))
  records.append(dict(family=run['family'],eta=run['eta_exact'],method=run['method'],
      H2=SHOW(H2),phase2=SHOW(phase2),errors={name:SHOW(value) for name,value in errors.items()},signed_controls=signed))
 return records


def calculate():
 mp.mp.dps=110;iv.dps=80
 pins,before=sources();ch=Checks();interval_prerequisites(ch)
 u,functions,proof=symbolic(ch)
 prior=READ(PREV+'summary.json')
 ch.add('inherited_shift_bridge_receipt_retained_not_rerun',
   prior['passed']==222 and prior['total']==222 and prior['physics_pass'] is False)
 cases={};certificates=[]
 for family in FAMILIES:
  for eta in ETAS:
   print('CERTIFY '+family+' eta='+eta,flush=True)
   case=case_data(family,eta,functions);cases[family,eta]=case
   certificates.append(certify_case(case,functions,ch))
 archives=archive_controls(ch,cases,functions)
 _,after=sources();ch.add('all_source_bytes_sidecars_and_metadata_preserved',before==after)
 ok=all(row['passed'] for row in ch.rows)
 certified=all(row['status']=='CERTIFIED_KNOWN_CANONICAL_INITIAL_SURFACE' for row in certificates)
 summary=dict(validation='PASS_KNOWN_INITIAL_CONSTRAINT_CERTIFICATES_ONLY' if ok and certified else 'FAIL_OR_INCONCLUSIVE_INITIAL_CERTIFICATES',
  passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows,
  source_sha256=pins,source_metadata=before,known_canonical_initial_constraints_certified=ok and certified,
  certified_case_count=sum(row['status']=='CERTIFIED_KNOWN_CANONICAL_INITIAL_SURFACE' for row in certificates),
  full_initial_data_admission=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
  physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
  status='KNOWN_INITIAL_SURFACE_ONLY_FULL_RANK_CHANGING_ADMISSION_AND_EVOLUTION_OPEN',
  missing_required_physics=['complete higher/rank-changing Dirac consistency and persistence',
   'physical reduced Hessian and temporal Cauchy/energy domain',
   'nonlinear evolution error, physical frequency/momentum window and healthy GR',
   'identifying matter-residue and nonlinear-force matching inputs'])
 return {'summary.json':summary,'proof.json':proof,'certificates.json':certificates,'archive_controls.json':archives}


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output');parser.add_argument('--replay')
 args=parser.parse_args()
 if bool(args.output)==bool(args.replay):parser.error('choose exactly one fresh output or read-only replay')
 dest=(ROOT/(args.output or args.replay)).resolve()
 if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science output root')
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
 su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','known_canonical_initial_constraints_certified','certified_case_count','status')}),flush=True)
 return 0 if su['passed']==su['total'] else 1


if __name__=='__main__':raise SystemExit(main())
