"""Action-derived R-tau clock current and whole prepared-circle bounds."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_CLOCK_FLUX_V1_CONTRACT_2026-11-01.md'
FACTORY='Analysis/MasterTests/r4c1_prepared_operator_factory_v1.py'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 def zero(n,x):check(n,s.simplify(x)==0,str(s.simplify(x)))
 assert SHA((ROOT/PARENT).read_bytes())=='dbcdacf8954e1cc59a2ebc42b91cd77f7a8e3473c2c54906b1f94e506455154d'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,PARENT,CONTRACT):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 # Projection of the covariant unit-normal Euler derivative in general 3D.
 Z,p,b,chi=s.symbols('Z p b chi',real=True,nonzero=True)
 K=s.Matrix([[s.Symbol('kxx'),s.Symbol('kxy'),s.Symbol('kxz')],[s.Symbol('kxy'),s.Symbol('kyy'),s.Symbol('kyz')],[s.Symbol('kxz'),s.Symbol('kyz'),s.Symbol('kzz')]])
 grad=s.Matrix(s.symbols('g0:3'));dp=s.Matrix(s.symbols('d0:3'));dz=s.Matrix(s.symbols('z0:3'))
 projected=b*(2*Z*(dp-K*grad)+Z*s.trace(K)*grad-(Z*dp+p*dz))
 candidate=b*(Z*dp+Z*(s.trace(K)*s.eye(3)-2*K)*grad-p*dz)
 check('general_extrinsic_curvature_projection_identity',(projected-candidate).applyfunc(s.simplify)==s.zeros(3,1))
 # Independent original-regulator variation in a curved 3+1 metric,
 # ds2=-N(t,z)^2 dt2+a(t,z)^2 (dx2+dy2+dz2), before imposing Z's equation.
 t,z=s.symbols('t z',real=True);N=s.Function('N')(t,z);a=s.Function('a')(t,z);psi=s.Function('psi')(t,z);zz=s.Function('Z')(t,z)
 th,tht,thz=s.symbols('theta theta_t theta_z',real=True)
 ch,sh=s.cosh(th),s.sinh(th);H=s.diff(a,t)/(a*N);lapseacc=s.diff(N,z)/(a*N)
 vZ=sh*s.diff(zz,t)/N+ch*s.diff(zz,z)/a
 vpsi=sh*s.diff(psi,t)/N+ch*s.diff(psi,z)/a
 accel=ch*tht/N+sh*thz/a+ch*lapseacc+sh*H
 L=b*N*a**3*(zz**2/2-vZ*vpsi-zz*accel*vpsi);aligned={th:0,tht:0,thz:0}
 EL=s.diff(L,th).subs(aligned)-s.diff(s.diff(L,tht).subs(aligned),t)-s.diff(s.diff(L,thz).subs(aligned),z)
 etheta=b/a*(zz*(s.diff(psi,t,z)/N-s.diff(psi,t)*s.diff(N,z)/N**2)+zz*H*s.diff(psi,z)-s.diff(psi,t)*s.diff(zz,z)/N)
 zero('independent_curved_original_action_clock_normal_variation',EL-N*a**3*etheta)
 check('omitted_expansion_current_term_rejected',s.simplify(EL-N*a**3*(etheta-b*zz*H*s.diff(psi,z)/a))!=0)
 # Clock-adapted current has F0=0, even with nonzero shift.
 nn,shift,eps,C,rho,beta=s.symbols('N shift epsilon C rho beta',positive=True)
 zero('adapted_projector_00',-1/nn**2+(1/nn)**2)
 zero('adapted_projector_0z',shift/nn**2+(1/nn)*(-shift/nn))
 zero('matter_clock_current_time_component',(eps*C*C*(-1/nn**2)).subs(C,1/nn)+eps/nn**4)
 zero('matter_clock_current_spatial_component',(eps*C*C*shift/nn**2).subs(C,1/nn)-eps*shift/nn**4)
 # Epsi,m=beta*T_m on the multiplier equation, independently of the current.
 X=s.Symbol('X');matter=-eps*(C*C*X+C**4)/2
 zero('matter_source_scalar_variation_on_constraint',(s.diff(matter,C)*beta*C).subs(X,-C*C)+beta*eps*C**4)
 rt,rz,pt,pz,ld,ell,sz,source=s.symbols('rho_t rho_z psi_t psi_z lambda_t lambda_z S_z E_tau',real=True)
 continuity=rt-shift*rz+(3*ld-beta*pt-sz-shift*(3*ell-beta*pz))*rho-source
 energy=rt-shift*rz+(3*ld-3*ell*shift-sz)*rho-beta*rho*(pt-shift*pz)-source
 zero('ADM_clock_continuity_and_matter_energy_equivalence',continuity-energy)
 k,amp,normal=s.symbols('k amp normal',positive=True);Zflat=k*k*amp*s.cos(k*z)
 zero('existing_flat_clock_operator_limit',s.diff(-b*normal*s.diff(Zflat,z),z)-b*normal*k**4*amp*s.cos(k*z))
 # Positive clock norm on the declared preparation; no null-clock extension.
 e=iv.mpf(1)/1000;psmax=e*(iv.mpf(1)/29+iv.mpf(1)/31);clocklower=iv.exp(-(iv.mpf(2)/5)*psmax)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(v) for v in x._mpi_]
 check('timelike_clock_normalization_nonsingular',lo(clocklower)>mp.mpf('.9999'))
 sp=importlib.util.spec_from_file_location('clock_flux_prepared_factory',ROOT/FACTORY);f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f);env=f.prepare();J=env['J'];j=env['j'];state=env['state']
 betaJ=J(iv.mpf(2)/5);bJ=J(iv.mpf(5)/11);eJ=J(e)
 def flux(theta,uncertain):
  y=state(theta,uncertain);h=y[0];n=j.exp(-betaJ*y[12]);volume=h**mp.mpf('1.5');S=y[44];Sz=y[47]
  p=(y[26]-S*y[40])/n
  psidot_z=-3*eJ*j.trig(3*theta)/47
  psi_zz=-eJ*(j.trig(theta,True)/29+4*j.trig(2*theta,True)/31)
  p_z=(psidot_z-Sz*y[40]-S*psi_zz)/n+betaJ*p*y[40]
  kx=(y[14]-S*y[28])/(2*n*h);ky=(y[17]-S*y[31])/(2*n*h);kz=(y[19]-S*y[33]-2*h*Sz)/(2*n*h)
  Fs=[bJ*y[13]*y[45]*y[40]/h,bJ*y[13]*y[46]*y[40]/h,
      bJ*n/h*(y[13]*p_z+y[13]*(kx+ky-kz)*y[40]-p*y[41])]
  weighted=n*volume*Fs[2];Etau=weighted.c[1]/(n*volume).c[0]
  return Fs,Etau
 cells=[];bounds=[mp.mpf(0)]*3;sourcebound=mp.mpf(0);allfinite=True
 for cell in range(32):
  theta=J.variable(iv.mpf([lo(iv.pi*(2*cell)/32),hi(iv.pi*(2*cell+2)/32)]));Fs,Etau=flux(theta,True)
  for axis,F in enumerate(Fs):bounds[axis]=max(bounds[axis],abs(lo(F.c[0])),abs(hi(F.c[0])))
  sourcebound=max(sourcebound,abs(lo(Etau)),abs(hi(Etau)))
  pairs=[v for F in Fs for v in F.c]+[Etau]
  allfinite=allfinite and all(mp.isfinite(lo(v)) and mp.isfinite(hi(v)) and lo(v)<=hi(v) for v in pairs)
  cells.append(dict(cell=cell,spatial_current=[dict(value=binary(F.c[0]),dz=binary(F.c[1])) for F in Fs],clock_Euler=binary(Etau)))
 check('all_current_and_source_interval_pairs_finite_ordered',allfinite,32*7)
 points=[];nonzero=False
 for zs in ('0.3','1.1','2.4'):
  Fs,Etau=flux(J.variable(iv.mpf(zs)),False);nonzero=nonzero or lo(Etau)>mp.mpf('1e-12') or hi(Etau)<-mp.mpf('1e-12')
  points.append(dict(z=zs,spatial_current=[binary(F.c[0]) for F in Fs],clock_Euler=binary(Etau)))
 check('omitted_local_regulator_clock_source_rejected',nonzero)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CLOCK_FLUX_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  covariant_current='F^alpha=(b/chi)[Z D^alpha p+Z(K h^alpha beta-2K^alpha beta)D_beta psi-p D^alpha Z]',
  definitions='p=t.partial psi, chi=sqrt(-partial tau^2), t=-partial tau/chi; Z independent until its equation',
  clock_Euler='E_tau,reg=div F',matter_transfer='div T_m=beta T_m grad psi-E_tau,reg grad tau',
  adapted_time_current=0,adapted_conservation='partial_t(N sqrt(h) rho)-partial_z(N sqrt(h) rho S^z+N sqrt(h) F^z)=0',
  clock_norm_lower=binary(clocklower),cell_enclosures=cells,current_abs_upper=[mp.nstr(x,45) for x in bounds],clock_Euler_abs_upper=mp.nstr(sourcebound,45),point_controls=points,
  direct_reconstructed_density_time_comparison='NOT_COMPUTED',higher_derivative_clock_evolution='OPEN',physical_symplectic_quotient='NOT_DERIVED',
  irreversible_entropy_production_derived=False,matching_identified=False,canonical_parent_adopted=False,nonlinear_time_evolution=False,
  review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
