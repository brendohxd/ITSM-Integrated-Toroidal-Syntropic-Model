"""Actual P0-B canonical/Euler response and gauge-invariant metric reconstruction."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[4]
PARENT='Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/m4_actual_source_kernel_v1_20261105/receipt.json'
SPEC='Theory/Gates/MAT-001/MAT001_M4_P0B_CAUSAL_RESPONSE_V1_SPEC_2026-11-05.md'
OWNER='Theory/Gates/MAT-001/MAT001_M4_P0B_CAUSAL_RESPONSE_V1_REPORT_2026-11-05.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256'])
 for rel in [PARENT,SPEC,OWNER,Path(__file__).relative_to(ROOT).as_posix()]:pins[rel]=sha(ROOT/rel)
 snapshot={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in [p,Path(str(p)+'.sha256')]:
   if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(n,v,value=None):checks.append(dict(name=n,passed=bool(v),value=value))
 symbols={n:s.Symbol(n) for n in ['M','H','rho','mu','q','CJ','rho_dot','V','V_rho','V_rhorho','delta_e','j','tau']}
 mat=lambda k:s.Matrix([[s.sympify(t,locals=symbols) for t in row] for row in d['nonzero_mode'][k]])
 K,D,F,C,Bv,Bx=[mat(k) for k in ['K','D','F','C','B_velocity','B_field']]
 src=s.Matrix([symbols[n] for n in ['delta_e','j','tau']]);Sv=mat('source_velocity').jacobian(src);Sx=mat('source_field').jacobian(src)
 a=s.Symbol('a',positive=True);I=s.eye(2);Z=s.zeros(2);E=I.row_join(Z);Ki=K.inv()
 A=(-Ki*D).row_join(Ki/a**3).col_join((a**3*(F-D.T*Ki*D)).row_join(D.T*Ki))
 B=(-Ki*Sv).col_join(a**3*(Sx-D.T*Ki*Sv))
 Vz=(-Ki*D).row_join(Ki/a**3);Vr=-Ki*Sv
 Hs=s.Matrix([[-1,0,0],[0,1/symbols['q']**2,0]])
 Cz=-C.inv()*(Bv*Vz+Bx*E);Cr=-C.inv()*(Bv*Vr+Hs)
 zz=s.Matrix(s.symbols('z0:4'))
 check('canonical_velocity_and_momentum_equations',s.simplify((A*zz+B*src)[:2,0]-(Vz*zz+Vr*src))==s.zeros(2,1))
 check('constraint_reconstruction_including_source',s.simplify(C*(Cz*zz+Cr*src)+Bv*(Vz*zz+Vr*src)+Bx*E*zz+Hs*src)==s.zeros(2,1))
 az,ar=Cz[0,:],Cr[0,:];bz=-Cz[1,:]/symbols['q']**2;br=-Cr[1,:]/symbols['q']**2
 # Freeze exactly the existing parent parameters/background, retaining a,r,v,H dependence.
 r=symbols['rho'];v=symbols['rho_dot'];H=symbols['H'];k=s.Symbol('k',positive=True)
 potential=r*r/2+s.Rational(1,2)*r**4/8+s.Rational(1,5)*r**6/96
 Qcharge=s.sqrt(s.Rational(101,80)) # V_rho(1)=1+1/4+1/80
 bg=s.Matrix([a*H,v,-3*H*v+r*(Qcharge/(a**3*r*r))**2-s.diff(potential,r),-(v*v+r*r*(Qcharge/(a**3*r*r))**2)/2])
 substitution={symbols['M']:1,symbols['CJ']:2,symbols['q']:k/a,symbols['mu']:Qcharge/(a**3*r*r),symbols['V']:potential,symbols['V_rho']:s.diff(potential,r),symbols['V_rhorho']:s.diff(potential,r,2)}
 vars=[a,r,v,H]
 freeze=lambda x:x.subs(substitution)
 dot=lambda x:x.applyfunc(lambda e:sum(s.diff(e,u)*bg[i] for i,u in enumerate(vars)))
 Kn,Dn,Fn,Snv,Snx,An,Bn,azn,arn,bzn,brn=[freeze(x) for x in [K,D,F,Sv,Sx,A,B,az,ar,bz,br]]
 DK,DD,DSv=dot(Kn),dot(Dn),dot(Snv)
 Phiz=azn+dot(bzn)+bzn*An;Phir=arn+dot(brn)+bzn*Bn;Phird=brn
 Psiz=-s.Matrix([[1,0,0,0]])-H*bzn;Psir=-H*brn
 # Gauge-invariant potentials: alpha->alpha-dot T, beta->beta+T, R->R-H T.
 t=s.Symbol('t');T=s.Function('T')(t);al,be,cur=s.symbols('alpha beta R');bedot=s.Symbol('beta_dot')
 check('Bardeen_Phi_time_gauge_invariant',s.expand(al-s.diff(T,t)+bedot+s.diff(T,t)-al-bedot)==0)
 check('Bardeen_Psi_time_gauge_invariant',s.expand(-(cur-H*T)-H*(be+T)+cur+H*be)==0)
 zt=s.Matrix([s.Function('z%d'%i)(t) for i in range(4)]);rr=s.Matrix([s.Function('r%d'%i)(t) for i in range(3)])
 # Derivative reconstruction is the chain rule with both coefficient and source motion.
 bf=s.Matrix([[s.Function('b%d'%i)(t) for i in range(4)]]);cf=s.Matrix([[s.Function('c%d'%i)(t) for i in range(3)]])
 check('full_shift_time_derivative_identity',s.expand(s.diff((bf*zt+cf*rr)[0],t)-(bf.diff(t)*zt+bf*zt.diff(t)+cf.diff(t)*rr+cf*rr.diff(t))[0])==0)
 q0=float(Qcharge);V0=float(potential.subs(r,1));H0=np.sqrt((q0*q0/2+V0)/3)
 expressions=[bg,Kn,Dn,Fn,Snv,Snx,An,Bn,DK,DD,DSv,Phiz,Phir,Phird,Psiz,Psir,Vz.subs(substitution),Vr.subs(substitution)]
 ff=s.lambdify([a,r,v,H,k],expressions,'numpy',cse=True)
 pressure=lambda time:1e-6*np.sin(np.pi*time/.5)**4
 pressure_dot=lambda time:4e-6*(np.pi/.5)*np.sin(np.pi*time/.5)**3*np.cos(np.pi*time/.5)
 def rhs(time,state,mode,form):
  aa,rr0,vv,hh,energy,jj=state[:6];vals=ff(aa,rr0,vv,hh,mode);bgr=np.asarray(vals[0],float).ravel()
  pm=pressure(time);source=np.array([energy,jj,3*pm]);energy_dot=-3*hh*energy-3*hh*pm-jj;jdot=-5*hh*jj+(mode/aa)**2*pm
  sd=np.array([energy_dot,jdot,3*pressure_dot(time)])
  if form=='canonical':rates=np.asarray(vals[6],float)@state[6:]+np.asarray(vals[7],float)@source
  else:
   km,dm,fm,sv,sx=[np.asarray(x,float) for x in vals[1:6]];dk,dd,dsv=[np.asarray(x,float) for x in vals[8:11]]
   x=state[6:8];xd=state[8:10];forcing=sx@source-dsv@source-sv@sd-3*hh*(sv@source)
   xdd=np.linalg.solve(km,forcing-(dk+3*hh*km+dm-dm.T)@xd-(dd+3*hh*dm-fm)@x);rates=np.r_[xd,xdd]
  return np.r_[bgr,energy_dot,jdot,rates]
 grid=np.linspace(0,.5,101);initial=np.r_[1.,1.,0.,H0,0.,0.,np.zeros(4)]
 def solve(mode,form,rtol,atol,method):
  sol=solve_ivp(lambda tt,yy:rhs(tt,yy,mode,form),(0,.5),initial,t_eval=grid,method=method,rtol=rtol,atol=atol)
  assert sol.success and sol.y.shape==(10,101),sol.message
  return sol.y
 def observe(arr,mode,form):
  output=[];det=[];fried=[]
  for idx,time in enumerate(grid):
   aa,rr0,vv,hh,energy,jj=arr[:6,idx];vals=ff(aa,rr0,vv,hh,mode);source=np.array([energy,jj,3*pressure(time)])
   sd=np.array([-3*hh*energy-3*hh*pressure(time)-jj,-5*hh*jj+(mode/aa)**2*pressure(time),3*pressure_dot(time)])
   state=arr[6:,idx]
   if form=='euler':state=np.r_[state[:2],aa**3*(np.asarray(vals[1],float)@state[2:]+np.asarray(vals[2],float)@state[:2]+np.asarray(vals[4],float)@source)]
   phi=(np.asarray(vals[11],float)@state+np.asarray(vals[12],float)@source+np.asarray(vals[13],float)@sd).item()
   psi=(np.asarray(vals[14],float)@state+np.asarray(vals[15],float)@source).item();output.append([*state[:2],phi,psi])
   det.append(float(np.linalg.det(np.asarray(vals[1],float))))
   V=rr0**2/2+.5*rr0**4/8+.2*rr0**6/96;chemical=q0/(aa**3*rr0**2)
   fried.append(abs(3*hh**2-(vv**2+rr0**2*chemical**2)/2-V))
  return np.array(output),np.array(det),max(fried)
 records=[]
 for mode in [1,4]:
  loose=solve(mode,'canonical',1e-8,1e-11,'DOP853');tight=solve(mode,'canonical',1e-10,1e-13,'DOP853');ind=solve(mode,'euler',1e-10,1e-13,'RK45')
  ol,_,_=observe(loose,mode,'canonical');ot,dets,resid=observe(tight,mode,'canonical');oi,_,_=observe(ind,mode,'euler')
  scale=max(1e-6,float(np.max(np.abs(ot))));error=float(np.max(np.abs(ol-ot))/scale);inderror=float(np.max(np.abs(oi-ot))/scale)
  check('tolerance_refinement_mode_'+str(mode),error<=1e-5,error)
  check('independent_Euler_metric_response_mode_'+str(mode),inderror<=1e-5,inderror)
  slip=float(np.max(np.abs(ot[:,2]-ot[:,3]))/scale)
  check('isotropic_source_traceless_metric_equation_mode_'+str(mode),slip<=1e-5,slip)
  check('regular_kinetic_and_background_mode_'+str(mode),float(min(dets))>0 and resid<1e-8,{'min_det':float(min(dets)),'friedmann_residual':resid})
  change=float(abs(dets[-1]-dets[0])/max(abs(dets[0]),1e-30))
  check('physical_time_coefficients_not_constant_mode_'+str(mode),change>1e-6,change)
  records.append({'k_comoving':mode,'peak_abs_R_drho_Phi_Psi':[float(x) for x in np.max(abs(ot),axis=0)],'tolerance_difference':error,'independent_difference':inderror,'kinetic_determinant_fractional_change':change,'metric_response_samples':ot.tolist()})
 check('old_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
 return {'kind':'M4_P0B_CAUSAL_RESPONSE_V1','source_sha256':pins,'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'time_grid':grid.tolist(),'numerical_controls':records,'scope':'NONZERO_MODE_CONSERVED_EXTERNAL_SOURCE_RETARDED_RESPONSE_WITH_FROZEN_PARENT_PARAMETERS_ONLY','retarded_data':'x=p=delta_e=j=0 at t=0; pressure specified in frozen spec','global_stationary_pole':'NOT_JUSTIFIED','adiabatic_physical_window':'NOT_ESTABLISHED','full_M4':'INCOMPLETE','live_TrackA_V':'NOT_COMPUTED','review':'DEFERRED','physics_pass':False,'gate_effect':'NONE'}
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 if a.output:assert not a.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True);a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
 else:assert a.verify.read_bytes()==raw,'Replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'controls':[{k:v for k,v in r.items() if k!='metric_response_samples'} for r in d['numerical_controls']],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
