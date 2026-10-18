"""Necessary node acceleration compatibility of the selected continuation."""
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
PARENT_SOURCE='Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py'
PARENT_SHA='d994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_PREFLIGHT_ADDENDUM_2026-10-18.md'
PROOF='Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/proof.json'
CERTS='Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/certificates.json'
PREV='Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01/formulas.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
READ=lambda name:json.loads((ROOT/name).read_bytes())
SHA=lambda data:hashlib.sha256(data).hexdigest()
ENC=lambda value:(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CLEAN=lambda value:s.factor(s.cancel(s.expand(value)))
SHOW=lambda value:mp.nstr(value,60)
if SHA((ROOT/PARENT_SOURCE).read_bytes())!=PARENT_SHA:raise ValueError('parent source drift before import')
spec=importlib.util.spec_from_file_location('frozen_initial_surface_utilities',ROOT/PARENT_SOURCE)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
iv=mp.iv
PINS=dict(base.PINS)
PINS.update({
 PARENT_SOURCE:PARENT_SHA,
 CONTRACT:'255484635f5a6f665ce65484cb665d640951e8b7400f482c4289a8ca99cfb0eb',
 'Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md':'4e81b770bcf5ad3b999ce34af37326803c1f73aba852b21f1d0bafb75c2a5f96',
 'Analysis/MasterTests/test_01_r4c1_node_acceleration_v1.py':'f91899a6add8ceff67b2358f63f6cc8f2ec8b18cc0d486a00039fa4b84250e1b',
 PROOF:'b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b',
 CERTS:'7c3465014fd85d7a98b905eed721c907f2f7764ccefadf856680ecf068d7127a',
 'Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/summary.json':'993b5cfffcb4b7c4106656a6929dfcc0379858c53e6556f60bb5b56b24ec5f4c',
 'Theory/Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_REPORT_2026-10-18.md':'7237b9649f08fe16746660415f418dd93b0268b81edb0871e6105abdca7c47ef',
 'Analysis/MasterTests/outputs/r4c1_initial_admission_replay_audit_attempt_01/audit.json':'9351821690ca15a3fe58b59b0b932090a229ecbc84c30bc700b2b36c39df3491',
 'Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md':'3019196b071b146a1e41cd055073ae02da2afa10b1cdb5ae49e0a63cf84a6eb6',
})


def sources():
 pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());metadata={}
 for name,digest in pins.items():
  path=ROOT/name
  if SHA(path.read_bytes())!=digest:raise ValueError('source hash drift '+name)
  sc=Path(str(path)+'.sha256')
  if sc.read_text().split()[0].lower()!=digest:raise ValueError('source sidecar mismatch '+name)
  for p in (path,sc):
   raw=p.read_bytes();metadata[p.relative_to(ROOT).as_posix()]=dict(
    sha256=SHA(raw),bytes=len(raw),mtime_ns=p.stat().st_mtime_ns)
 return pins,metadata


def derive(ch):
 print('DERIVE_BOTH_SCALAR_EQUATIONS_AND_NODE_LIMIT',flush=True)
 K,A,b,beta,H,HB,p,w,wp,R,Rp,U,acc,slope,r1,rhon=s.symbols(
  'K A b beta H Hbg p w wprime R Rprime U acceleration slope r1 rho_node',real=True)
 q=s.Matrix(s.symbols('q0:4',real=True));zg=s.Matrix(s.symbols('zg0:4',real=True))
 av=s.Matrix(s.symbols('acc0:4',real=True));Z=s.Symbol('Z',real=True)
 gam=s.sqrt(1+w*w);n=s.Matrix([gam,0,w,0]);hp=s.diag(-1,1,1,1)+n*n.T
 Y=(q.T*hp*q)[0];Q=(n.T*q)[0]
 L=K*Q*Q/2-A*Y**s.Rational(3,2)+b*Z*Z/2-b*(zg.T*hp*q)[0]-b*Z*(av.T*q)[0]
 moment=s.Matrix([s.diff(L,qi) for qi in q])
 expected=K*Q*n-3*A*s.sqrt(Y)*hp*q-b*hp*zg-b*Z*av
 ch.zero('complete_original_force_regulator_momenta',moment-expected)
 ch.zero('original_regulator_gradient_momentum',s.Matrix([s.diff(L,zi) for zi in zg])+b*hp*q)
 # Matter variation is independent, before imposing its own multiplier equation.
 psi,eps,Xt=s.symbols('psi epsilon Xtau',real=True);C=s.exp(beta*psi)
 Lm=-eps*(C*C*Xt+C**4)/2
 matter=s.diff(Lm,psi).subs(Xt,-C*C)
 ch.zero('matter_source_from_independent_dust_variation',matter+beta*eps*C**4)
 # Full ADM geometry at the prescribed slice, before the node restriction.
 B00=w*((-HB*w-R*wp)+H*w)/gam
 By0=H*w
 acc0=CLEAN(gam*B00+w*By0)
 ch.zero('acceleration_term_kept_in_EZ',acc0-((2*H-HB)*w*w-R*w*wp))
 time_hp=2*(H-HB)*w*w
 divhpq=w*w*acc+time_hp*p+(-Rp*w*w-2*R*w*wp)*p+3*H*w*w*p
 EZ=CLEAN(Z+divhpq-acc0*p)
 candidate=Z+w*w*(acc+(3*H-HB-Rp)*p)-R*w*wp*p
 ch.zero('unreduced_EZ_on_full_initial_slice',EZ-candidate)
 z=s.Symbol('z',real=True)
 limit_EZ=CLEAN((EZ.subs({Z:U*slope**2*z*z,w:slope*z,wp:slope,R:r1*z,Rp:r1}))/(slope**2*z*z))
 ch.zero('regular_side_EZ_limit',limit_EZ-(U+acc+(3*H-HB-2*r1)*p))
 reg_acc=-U-(3*H-HB)*p+2*r1*p
 ch.zero('finite_acceleration_forced_by_regular_side',limit_EZ.subs(acc,reg_acc))
 ch.add('reject_omitted_acceleration_term_before_node_limit',
   CLEAN((acc0*p/(w*w)).subs({w:slope*z,wp:slope,R:r1*z}) )!=0)
 # At the node all regulator first jets and Z vanish; Zzz=2U*slope^2.
 Epsi=-K*(acc+(3*H-r1)*p)+2*b*U*slope*slope-beta*rhon
 compatibility=CLEAN(Epsi.subs(acc,reg_acc))
 G=(K+2*b*slope*slope)*U-K*HB*p-K*p*r1-beta*rhon
 ch.zero('simultaneous_scalar_node_compatibility',compatibility-G)
 ch.add('reject_omitting_shift_gradient',s.diff(Epsi,r1)!=0)
 ch.add('reject_omitting_regulator_spatial_Hessian',s.diff(Epsi,U)!=0)
 # Original C2 cusp: compute both one-sided divergences, not a third derivative.
 ss,pp=s.symbols('s_positive p_positive',positive=True)
 abs_cube=s.Abs(ss*z)**3
 P0=-3*A*pp**2*abs_cube
 dtP0=-3*A*abs_cube*(3*(H-HB)*pp**2+2*pp*acc)
 Pz=3*A*pp**2*r1*z*abs_cube
 cuspdiv=dtP0+s.diff(Pz,z)+3*H*P0
 for direction in ('+','-'):
  branch=cuspdiv.xreplace({s.Abs(z):z if direction=='+' else -z,s.sign(z):s.Integer(1 if direction=='+' else -1)})
  ch.zero('full_cusp_node_divergence_'+direction,s.limit(branch,z,0,dir=direction))
 # Coupled local repair Jacobian: mean equation and actual node condition.
 M,rho0,H0=s.symbols('M rho0 H0',positive=True)
 rr=s.Symbol('rest_energy',real=True)
 F=-3*M*H**2+rr+rho0
 rho_at_zero=3*M*H**2-rr
 G0=K*U-K*H0*p-beta*rho_at_zero
 jac=s.Matrix([[s.diff(F,H),s.diff(F,U)],[s.diff(G0,H),s.diff(G0,U)]]).subs(H,H0)
 ch.zero('coupled_mean_node_Jacobian',jac.det()+6*K*M*H0)
 dimensions={K:2,b:0,beta:0,HB:1,p:1,U:2,slope:1,r1:1,rhon:4}
 term_dimensions=[sum(dimensions[symbol]*power for symbol,power in term.as_powers_dict().items()
      if symbol in dimensions) for term in s.Add.make_args(s.expand(G))]
 ch.add('node_compatibility_mass_dimension_four',all(d==4 for d in term_dimensions),[int(d) for d in term_dimensions],
      'dimensionless psi and frame; [K_Q]=2,[b]=[beta]=0,[U]=2,[H]=[p]=[k]=1,[rho]=4')
 return dict(
  original_momenta=str(expected),EZ_initial=str(candidate),EZ_regular_node_limit=str(limit_EZ),
  psi_acceleration_from_EZ=str(reg_acc),Epsi_node=str(Epsi),compatibility=str(G),
  selected_U0='Hbg*p+beta*rho0/K_Q',
  selected_normalized_defect='G/e^2=2*b*U0*k^2-K_Q*p*(Rprime_node/e^2)-beta*(<Edelta>-Edelta_node-flux_node/e^2)',
  regularity='Necessary for finite continuous scalar normal acceleration; not a weak/distributional or all-action no-go theorem',
  other_sectors='Frame/metric/Cartesian potentials have no direct psi variation. Their geometry/current effects remain in n, hp, acc, divergence, and the independent matter trace.',
  node_cusp='Both one-sided original-cusp divergences vanish; no ordinary third derivative is inserted',
  repair_equation='(K_Q+2*b*k^2*e^2)*U=K_Q*Hbg*p+K_Q*p*Rprime_node+beta*rho_node; H,R,rho must be solved with U, not held at old values',
  local_repair_Jacobian=str(jac),local_repair_determinant=str(CLEAN(jac.det())),
  repair_scope='Nonzero determinant supplies only a local necessary-node-compatible branch via implicit-function reasoning; no explicit finite-amplitude repair, higher consistency or evolution is certified')


def coordinate_controls(ch):
 print('INDEPENDENT_COORDINATE_DENSITY_VARIATIONS',flush=True)
 records=[]
 for seed in (0,1):
  for orientation in (-1,1):
   H=mp.mpf(2+seed)/7;HB=mp.mpf(3)/11;p=mp.mpf(1+seed)/9
   aa=mp.mpf(2-seed)/13;U=mp.mpf(3)/17;Ud=mp.mpf(2)/19;Zdd=mp.mpf(4)/23
   slope=mp.mpf(orientation)*(mp.mpf(1)/3);r1=mp.mpf(2)/29;ty=mp.mpf(3)/31
   syvel=mp.mpf(1)/37;rzvel=-mp.mpf(2)/41
   K=mp.mpf(3)/5;b=mp.mpf(5)/11;A=mp.mpf(2)/7;beta=mp.mpf(1)/17;rho=mp.mpf(1)/5
   hdd=mp.matrix([[mp.mpf(1+i+j+seed)/43 for j in range(3)] for i in range(3)])
   def point(t,z):
    h=(1+2*H*t)*mp.eye(3)+t*t*hdd/2;hi=h**-1
    S=mp.matrix([0,ty*z+syvel*t,r1*z+rzvel*t])
    V=mp.matrix([0,slope*z*(1-HB*t),0])
    gam=mp.sqrt(1+(V.T*h*V)[0]);n=mp.matrix([gam]+list(V-gam*S))
    g=mp.zeros(4);gi=mp.zeros(4);g[0,0]=-1+(S.T*h*S)[0];gi[0,0]=-1
    for i in range(3):
     g[0,i+1]=g[i+1,0]=(h*S)[i];gi[0,i+1]=gi[i+1,0]=S[i]
     for j in range(3):g[i+1,j+1]=h[i,j];gi[i+1,j+1]=hi[i,j]-S[i]*S[j]
    return h,g,gi,n
   def geometry(t,z):
    h,g,gi,n=point(t,z)
    dg=[]
    for mu in range(4):
     if mu in (1,2):dg.append(mp.zeros(4));continue
     dg.append(mp.matrix([[mp.diff(lambda vv:point(vv,z)[1][i,j],t) if mu==0 else mp.diff(lambda vv:point(t,vv)[1][i,j],z) for j in range(4)] for i in range(4)]))
    conn=[[[sum(gi[c,l]*(dg[a][l,bb]+dg[bb][l,a]-dg[l][a,bb]) for l in range(4))/2 for bb in range(4)] for a in range(4)] for c in range(4)]
    DN=mp.matrix([[mp.diff(lambda vv:point(vv,z)[3][j],t) if mu==0 else mp.diff(lambda vv:point(t,vv)[3][j],z) if mu==3 else 0 for j in range(4)] for mu in range(4)])
    for mu in range(4):
     for j in range(4):DN[mu,j]+=sum(conn[j][mu][l]*n[l] for l in range(4))
    return mp.sqrt(mp.det(h)),gi+n*n.T,n,DN.T*n
   def fields(t,z):
    zp=U*slope*slope*z*z+Ud*slope*slope*t*z*z+Zdd*t*t/2
    return mp.matrix([p+aa*t,0,0,0]),mp.matrix([Ud*slope*slope*z*z+Zdd*t,0,0,2*U*slope*slope*z+2*Ud*slope*slope*t*z]),zp
   def density(t,z,qp,qz,Zvalue):
    vol,hp,n,acc=geometry(t,z);Q=(n.T*qp)[0];Y=(qp.T*hp*qp)[0]
    return vol*(K*Q*Q/2-A*Y**mp.mpf('1.5')+b*Zvalue**2/2-b*(qz.T*hp*qp)[0]-b*Zvalue*(acc.T*qp)[0])
   def momentum(t,z,which,index):
    qp,qz,Zvalue=fields(t,z);original=qp if which=='psi' else qz
    def at(v):
     varied=mp.matrix(original);varied[index]=v
     return density(t,z,varied if which=='psi' else qp,varied if which=='Z' else qz,Zvalue)
    return mp.diff(at,original[index])
   def eulerZ(z):
    qp,qz,Zvalue=fields(0,z)
    direct=mp.diff(lambda value:density(0,z,qp,qz,value),Zvalue)
    return direct-mp.diff(lambda t:momentum(t,z,'Z',0),0)-mp.diff(lambda zz:momentum(0,zz,'Z',3),z)
   epsi=-mp.diff(lambda t:momentum(t,0,'psi',0),0)-mp.diff(lambda z:momentum(0,z,'psi',3),0)-beta*rho
   predicted=-K*(aa+(3*H-r1)*p)+2*b*U*slope*slope-beta*rho
   err=abs(epsi-predicted)/(1+abs(epsi)+abs(predicted))
   ch.small('coordinate_Epsi_node_'+str(seed)+'_'+str(orientation),err,'1e-50')
   zerrs=[]
   for z in (mp.mpf(1)/10,-mp.mpf(1)/10,mp.mpf(1)/20,-mp.mpf(1)/20):
    actual=eulerZ(z)/(b*slope*slope*z*z)
    expected=U+aa+(3*H-HB-2*r1)*p
    e=abs(actual-expected)/(1+abs(actual)+abs(expected));zerrs.append(e)
   ch.small('coordinate_EZ_regular_side_'+str(seed)+'_'+str(orientation),max(zerrs),'1e-50')
   records.append(dict(seed=seed,profile_slope=SHOW(slope),Epsi_error=SHOW(err),
      EZ_max_error=SHOW(max(zerrs)),metric_second_time_jets='all six nonzero',
      shift_time_jets=[SHOW(syvel),SHOW(rzvel)],regulator_second_time_jet=SHOW(Zdd)))
 return records


def interval_setup(ch):
 print('BUILD_FINITE_NORMALIZED_DEFECT_FROM_FROZEN_ENERGY',flush=True)
 names='MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 vz vz1 vz2 R q p Z Zd Z1 Z2 D rd pot k alpha xi zc zdc rs qs CC SS eeabs'
 u={n:s.Symbol(n,real=True) for n in names.split()};u['p']=s.Symbol('p',positive=True)
 par=lambda text:s.sympify(text,locals=u)
 old=READ(PREV);E=par(old['energy_without_dust']);flux=par(old['lapse_flux_divergence'])
 v,v1,e,C,S,al=[u[n] for n in ('vz','vz1','eeabs','CC','SS','alpha')]
 aa=s.Symbol('e_exact',real=True)
 M=u['MP2']+u['MU2']*(u['c1']+3*u['c2']+u['c3'])/2
 Ebase=-3*M*u['H']**2+(u['K_Q']*u['p']**2+u['D']**2+u['rd']**2)/2+u['pot']
 analytic=E.subs(u['A'],0);num,den=s.fraction(analytic)
 angular_num=s.expand(num-den*Ebase)
 sub={v:aa*C,v1:-u['k']*aa*S,u['R']:aa**2*u['rs'],u['q']:aa**2*u['qs'],
      u['Z']:u['zc']*aa**2*C*C,u['Zd']:u['zdc']*aa**2*C*C,
      u['Z1']:-2*u['k']*u['zc']*aa**2*C*S}
 ne=s.Poly(s.expand(angular_num.subs(sub)),aa)
 de=s.Poly(s.expand(den.subs(sub)),aa)
 ch.zero('normalized_energy_numerator_constant',ne.coeff_monomial(1))
 ch.zero('normalized_energy_numerator_linear',ne.coeff_monomial(aa))
 ch.add('all_energy_amplitude_powers_even',all(power[0]%2==0 for power,coef in ne.terms()+de.terms()))
 nalpha=sum(coef*al**(power[0]//2-1) for power,coef in ne.terms() if power[0]>=2)
 dalpha=sum(coef*al**(power[0]//2) for power,coef in de.terms())
 delta=nalpha/dalpha-2*u['A']*u['p']**3*e*C**3  # quadrant C>=0, |e| retained.
 # Local flux at the node is kept before averaging; there is no division by a node.
 fn=flux.subs({v:0,v1:-u['k']*aa,u['vz2']:0,u['R']:0,u['Z']:0,u['Zd']:0,u['Z1']:0},simultaneous=True)
 fs=CLEAN(fn/aa**2)
 ch.add('node_flux_normalization_regular',aa not in fs.free_symbols and fs!=0,str(fs))
 proof=READ(PROOF);pns=[par(text) for text in proof['polynomial_pieces']]
 scaled=sum(al**j*pn for j,pn in enumerate(pns))
 x=u['xi'];Q=lambda f:(2*x-1)*f-2*x*(1-x)*s.diff(f,x)
 poly=base.Eval([scaled,Q(scaled)])
 power_min=min(p[0] for p in proof['residual_powers'])
 ch.add('scaled_error_bound_uses_actual_residual_order',power_min>=4,power_min,
        'Residual starts alpha^4; inherited linear error bounds scale by alpha without division through zero')
 # Exact leading defect, using periodic monomial means, not a numerical extrapolation.
 d0=delta.subs({al:0,e:0,u['D']:u['Rc']})
 leading_p=pns[0].subs(u['H'],u['H0'])
 qs0=u['k']*Q(leading_p).subs(x,C*C)
 leading=s.expand(d0.subs({u['H']:u['H0'],u['rs']:C*S*leading_p.subs(x,C*C),u['qs']:qs0}))
 pol=s.Poly(leading,C,S)
 average=s.Integer(0)
 for (i,j),coef in pol.terms():
  if i%2 or j%2:continue
  m,n=i//2,j//2
  avg=s.factorial(2*m)*s.factorial(2*n)/(4**(m+n)*s.factorial(m)*s.factorial(n)*s.factorial(m+n))
  average+=coef*avg
 node=CLEAN(leading.subs({C:0,S:1}))
 qnode0=CLEAN(u['k']*Q(leading_p).subs(x,0))
 U0=u['H0']*u['p']+u['beta']*s.Rational(1,5)/u['K_Q']
 G2=CLEAN(2*u['b']*U0*u['k']**2-u['K_Q']*u['p']*qnode0-u['beta']*(average-node-fs))
 normalization=dict(normalized_energy_analytic=str(nalpha/dalpha),normalized_cusp='-2A p^3 |e| cos^3(theta) on quadrant',
      normalized_node_flux=str(fs),leading_defect=str(G2),
      scaled_error_proof='For every residual term alpha^n,n>=4, alpha^(n-1)<=amax_out^n/amax_exact on 0<alpha<=amax_exact. Inherited R/Rprime error estimates are linear in the residual bound with fixed positive coercivity constants. Thus inherited maximum errors divided by amax_exact enclose the normalized errors uniformly; this is not an absolute error divided by alpha near zero.',
      mean_elimination='At the certified mean root rho0=-<E>. Hence (rho_node-rho0)/alpha=<Edelta>-Edelta_node-flux_node/alpha. Constant Ebase(H,D) cancels exactly. Enclose the resulting expression over the inherited H bracket containing that root.',
      leading_scope='Exact leading coefficient, not by itself a finite-amplitude certificate')
 return u,dict(delta=base.Eval([delta]),flux=base.Eval([fs]),poly=poly,leading=base.Eval([G2])),normalization


def interval_cases(ch,u,fn):
 cases=[];previous=READ(CERTS);proof=READ(PROOF)
 eta_symbol=s.Symbol('eta');zero=iv.mpf(0);one=iv.mpf(1)
 def unpack(record):
  a,b=record['exact_binary_endpoints']
  return iv.mpf([mp.mpf(tuple(a)),mp.mpf(tuple(b))])
 for item in previous:
  family,eta=item['family'],item['eta']
  print('CERTIFY_NODE_DEFECT '+family+' eta='+eta,flush=True)
  raw=READ(PLANAR)['families'][family]['parameter_map']
  vals={key:base.interval_s(s.sympify(value,locals={'eta':eta_symbol}).subs(eta_symbol,s.Rational(eta))) for key,value in raw.items()}
  rc=iv.sqrt(base.interval_s(s.Rational(eta)))
  et=base.interval_s(s.Rational(eta))
  potential=3*et/2+et**2*(iv.mpf(1)/24+iv.mpf(1)/28)+et**3*(iv.mpf(1)/480+iv.mpf(3)/28)
  vals.update(Rc=rc,D=rc,rd=rc/4,pot=potential,k=iv.mpf(40),p=et/5,
       H0=unpack(item['H_background']),H=unpack(item['H_root_bracket']),
       zc=unpack(item['regulator_coefficient']),zdc=unpack(item['regulator_velocity_coefficient']),
       alpha=unpack(item['amplitude_squared_range']),
       eeabs=iv.mpf([0,base.hi(unpack(item['amplitude_absolute_max']))]))
  amax_exact=iv.mpf(1)/250000
  rerr=base.upper(unpack(item['shift_error'])/amax_exact)
  qerr=base.upper(unpack(item['shift_gradient_error'])/amax_exact)
  attempts=[];resolved=None
  for n in (16,32,64,128,256):
   total=iv.mpf(0)
   for j in range(n):
    theta=iv.mpf([base.lo(iv.pi*j/(2*n)),base.hi(iv.pi*(j+1)/(2*n))])
    C,S=iv.cos(theta),iv.sin(theta);B=C*S
    vv=dict(vals,xi=C*C)
    ps,qs=fn['poly'].interval(vv)
    vv.update(CC=C,SS=S,rs=B*ps+base.box(rerr),qs=vals['k']*qs+base.box(qerr))
    vv['D']=rc/(1-vals['zeta']*rc*rc*vals['alpha']/2)
    total+=fn['delta'].interval(vv)[0]/n
   vn=dict(vals,xi=zero);ps0,qs0=fn['poly'].interval(vn)
   qnode=vals['k']*qs0+base.box(qerr)
   vn.update(CC=zero,SS=one,rs=zero,qs=qnode)
   vn['D']=rc/(1-vals['zeta']*rc*rc*vals['alpha']/2)
   node=fn['delta'].interval(vn)[0];fl=fn['flux'].interval(vn)[0]
   rho_scaled=total-node-fl
   defect=2*vals['b']*vals['zc']*vals['k']**2-vals['K_Q']*vals['p']*qnode-vals['beta']*rho_scaled
   state='VIOLATED_POSITIVE_DEFECT' if base.lo(defect)>0 else 'VIOLATED_NEGATIVE_DEFECT' if base.hi(defect)<0 else 'UNRESOLVED_BY_BOUNDS'
   attempts.append(dict(boxes=n,defect_over_e_squared=base.pack(defect),
       density_difference_over_e_squared=base.pack(rho_scaled),node_shift_gradient_over_e_squared=base.pack(qnode),
       node_flux_over_e_squared=base.pack(fl),status=state))
   if state!='UNRESOLVED_BY_BOUNDS':resolved=state;break
  ch.add('node_acceleration_decision_'+family+'_'+eta,resolved is not None,
     {'attempts':[r['boxes'] for r in attempts],'decision':resolved or 'UNRESOLVED_BY_BOUNDS'},
     'strict nonzero interval rejects only selected continuation, not the action')
  # Exact reference point leading coefficient is an independent comparison, not the finite proof.
  value={name:base.midpoint(v) for name,v in vals.items()};value['H']=value['H0']
  leading=fn['leading'].numeric(value)[0]
  ch.add('leading_control_inside_finite_enclosure_'+family+'_'+eta,
      base.lo(defect)<=leading<=base.hi(defect),SHOW(leading),
      'the exact e->0 reference coefficient must lie in the outward all-amplitude bracket enclosure')
  cases.append(dict(family=family,eta=eta,amplitude_scope='0<|e|<=1/500, both signs',
      status=resolved or 'UNRESOLVED_BY_BOUNDS',attempts=attempts,leading_defect=SHOW(leading),
      selected_continuation_acceleration_consistent=False if resolved else None,
      normalized_shift_error=base.pack(rerr),normalized_shift_gradient_error=base.pack(qerr)))
 return cases


def calculate():
 mp.mp.dps=110;iv.dps=80
 pins,before=sources();ch=base.Checks()
 equations=derive(ch);independent=coordinate_controls(ch)
 u,functions,normalization=interval_setup(ch)
 audit=READ('Analysis/MasterTests/outputs/r4c1_initial_admission_replay_audit_attempt_01/audit.json')
 ch.add('parent_strict_audited_replay_inherited',audit['read_only_replay_passed'] is True and audit['earlier_cli_failure_relabelled'] is False)
 cases=interval_cases(ch,u,functions)
 _,after=sources();ch.add('all_source_bytes_sidecars_and_metadata_preserved',before==after)
 ok=all(row['passed'] for row in ch.rows)
 rejected=sum(row['status'].startswith('VIOLATED_') for row in cases)
 summary=dict(validation='PASS_NODE_ACCELERATION_COMPATIBILITY_AUDIT_ONLY' if ok else 'FAIL_OR_UNRESOLVED_NODE_ACCELERATION_AUDIT',
  passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows,
  source_sha256=pins,source_metadata=before,rejected_selected_continuation_cases=rejected,
  tested_case_count=len(cases),action_no_go=False,repair_adopted_or_evolved=False,
  full_initial_data_admission=False,stage2_complete=False,stage3_entered=False,
  physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
  status='NECESSARY_NODE_ACCELERATION_TEST_ONLY_HIGHER_COMPLETION_AND_EVOLUTION_OPEN',
  missing_required_physics=['coupled node-compatible higher-order regulator completion',
    'higher consistency and persistence through rank-changing strata',
    'physical Hessian/Cauchy/energy domain, nonlinear remainder, physical window and healthy GR',
    'identifying matter-residue and nonlinear-force matching inputs'])
 return {'summary.json':summary,'equations.json':equations,'normalization.json':normalization,
         'independent.json':independent,'cases.json':cases}


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output');parser.add_argument('--replay')
 args=parser.parse_args()
 if bool(args.output)==bool(args.replay):parser.error('choose exactly one fresh output or read-only replay')
 dest=(ROOT/(args.output or args.replay)).resolve()
 if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science output root')
 if args.output:dest.mkdir(parents=True,exist_ok=False)
 original={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
 results=calculate();payloads={name:ENC(value) for name,value in results.items()}
 for name,raw in list(payloads.items()):payloads[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode('ascii')
 if args.replay:
  if set(original)!=set(payloads):raise ValueError('replay file-set mismatch')
  for name,raw in payloads.items():
   path=dest/name
   if path.read_bytes()!=raw:raise ValueError('recomputed bytes differ '+name)
   actual=(SHA(path.read_bytes()),path.stat().st_size,path.stat().st_mtime_ns)
   if actual!=original[name]:raise ValueError('original input metadata changed '+name+': '+str(original[name])+' -> '+str(actual))
  print('READ_ONLY_REPLAY_EXACT',flush=True)
 else:
  for name,raw in payloads.items():
   with (dest/name).open('xb') as stream:stream.write(raw)
 su=results['summary.json'];print(json.dumps({key:su[key] for key in ('validation','passed','total','rejected_selected_continuation_cases','action_no_go','status')}),flush=True)
 return 0 if su['passed']==su['total'] else 1


if __name__=='__main__':raise SystemExit(main())


