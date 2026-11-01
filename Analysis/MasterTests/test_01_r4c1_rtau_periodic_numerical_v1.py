"""Full nonlinear periodic numerical preparation; continuum bounds NOT supplied."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_nonlinear_constraints_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_PREPARATION_V1_CONTRACT_2026-10-31.md'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_NUMERICAL_V1_SPEC_2026-10-31.md'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=40
 assert SHA((ROOT/PARENT).read_bytes())=='202ead4f7fd5d26d3eae4ec1ccc05798f2b8ef646eb7468a1a09103e3c13a987'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256'])
 for f in (SELF,PARENT,CONTRACT,SPEC):pins[f]=SHA((ROOT/f).read_bytes())
 snapshots={}
 for f,want in pins.items():
  p=ROOT/f;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==want and sc.read_text().split()[0].lower()==want
  for q in (p,sc):snapshots[q]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
 spec=importlib.util.spec_from_file_location('periodic_physical_backend',ROOT/BACKEND)
 backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
 old=backend.load('periodic_parameter_source',backend.QUADRATIC)
 par={k:mp.mpf(str(v.p))/int(v.q) for k,v in old.parameters().items()}
 action=backend.ClockGaugeAction('R-tau',par,physical=True);b=action.body
 e=mp.mpf(1)/1000;beta=par['beta'];h0=mp.sqrt(mp.mpf(3469)/4620)
 def profiles(theta):
  c=lambda n:mp.cos(n*theta);sn=lambda n:mp.sin(n*theta)
  lam=e*c(1)/13;ld=-e*sn(1)/13;ldd=-e*c(1)/13
  ps=e*(c(1)/29+c(2)/31);pd=e*(-sn(1)/29-2*sn(2)/31)
  pdd=e*(-c(1)/29-4*c(2)/31);pddd=e*(sn(1)/29+8*sn(2)/31)
  scale=mp.exp(lam)
  vv=[e*(1+c(1)/2)/37,e*c(2)/41,e*sn(1)/43]
  vd=[-e*sn(1)/74,-2*e*sn(2)/41,e*c(1)/43]
  vt=[e*c(2)/67,e*c(1)/71,e*sn(2)/73]
  q=[scale**2,0,0,scale**2,0,scale**2]+[x/scale for x in vv]+[1+e*c(1)/17,e*c(2)/19,1+e*c(3)/23,ps,-mp.exp(-2*lam)*(pdd+ld*pd),0,0]
  dz=[mp.mpf(0)]*16
  for j in (0,3,5):dz[j]=2*ld*q[j]
  for j in range(3):dz[6+j]=(vd[j]-ld*vv[j])/scale
  dz[9]=-e*sn(1)/17;dz[10]=-2*e*sn(2)/19;dz[11]=-3*e*sn(3)/23;dz[12]=pd
  dz[13]=-mp.exp(-2*lam)*(pddd+ldd*pd+ld*pdd-2*ld*(pdd+ld*pd))
  N=mp.exp(-beta*ps)
  return dict(q=q,dz=dz,scale=scale,vv=vv,vt=vt,lamdot=e*c(2)/31,
              ud=e*c(2)/53,vd=e*c(1)/59,rd=mp.mpf(1)/4+e*c(1)/61,
              psd=mp.mpf(1)/5+e*c(3)/47,N=N,Nz=-beta*N*pd,
              volume=scale**3,C=1/N)
 def local(prof,shift,shiftz,H,omega):
  vals=[mp.mpf(float(x)) for x in shift]+[mp.mpf(float(x)) for x in shiftz]+[prof['N'],prof['Nz'],prof['ud'],mp.mpf(float(omega))+prof['vd']]
  tape=b.Tape();x=[tape.var(z) for z in vals]
  vel=[mp.mpf(0)]*16;ht=mp.mpf(float(H))+prof['lamdot']
  for j in (0,3,5):vel[j]=2*ht*prof['q'][j]
  for j in range(3):vel[6+j]=(prof['vt'][j]-ht*prof['vv'][j])/prof['scale']
  vel[9]=x[8];vel[10]=x[9];vel[11]=prof['rd'];vel[12]=prof['psd'];vel[14]=1
  state=prof['q']+vel+prof['dz']+x[:6]+x[6:8]
  value=action.density(state)[0];gradient=tape.grad(value,x)
  return np.array([float(z) for z in gradient])
 results=[];checks=[]
 for count in (9,17,33):
  angles=2*np.pi*np.arange(count)/count;m=(count-1)//2
  B=np.column_stack([f(n*angles) for n in range(1,m+1) for f in (np.cos,np.sin)])
  Bz=np.column_stack([n*f(n*angles) for n in range(1,m+1) for f in (lambda t:-np.sin(t),np.cos)])
  D=(2/count)*Bz@B.T;freq=np.repeat(np.arange(1,m+1),2)
  profs=[profiles(2*mp.pi*j/count) for j in range(count)]
  coeff=np.zeros((3,count-1));H=float(h0);omega=1.;history=[];terminal=None
  def evaluate(co,Hh,om):
   S=B@co.T;Sz=Bz@co.T
   grads=np.array([local(profs[j],S[j],Sz[j],Hh,om) for j in range(count)])
   ES=grads[:,:3]-D@grads[:,3:6]
   EN=grads[:,6]-D@grads[:,7]
   vol=np.array([float(z['volume']) for z in profs]);C=np.array([float(z['C']) for z in profs])
   rho=EN/vol
   I=np.mean(EN/C)
   Q=np.mean([float(z['q'][9])*grads[j,9]-float(z['q'][10])*grads[j,8] for j,z in enumerate(profs)])
   projected=(2/count)*(B.T@ES).T
   return dict(projected=projected,I=I,Q=Q,ES=ES,rho=rho,S=S,grads=grads,EN=EN,C=C)
  for iteration in range(30):
   data=evaluate(coeff,H,omega)
   res=max(np.max(np.abs(data['projected'])),abs(data['I']-.2),abs(data['Q']-1))
   history.append(float(res))
   print('GRID',count,'ITER',iteration,'RES',format(res,'.4e'),flush=True)
   if res<1e-10:terminal=data;break
   for j,pivot in enumerate((.5,.5,-1/15)):coeff[j]-=data['projected'][j]/(pivot*freq**2)
   H-=(data['I']-.2+data['Q']-1)/(float(6*mp.mpf(11)/10*h0))
   omega-=data['Q']-1
  if terminal is None:terminal=evaluate(coeff,H,omega)
  mean=np.mean(terminal['ES'],axis=0)
  checks.extend([dict(name='grid_'+str(count)+'_projected_and_charge_residual',passed=history[-1]<1e-10,value=history[-1]),
                 dict(name='grid_'+str(count)+'_integrated_momentum_retained',passed=bool(np.max(np.abs(mean))<1e-10),value=mean.tolist()),
                 dict(name='grid_'+str(count)+'_positive_density',passed=bool(np.min(terminal['rho'])>0),value=float(np.min(terminal['rho'])))])
  noflux=np.mean(terminal['grads'][:,6]/terminal['C'])
  results.append(dict(nodes=count,H=H,omega=omega,history=history,mean_momentum=mean.tolist(),rho_min=float(np.min(terminal['rho'])),rho_max=float(np.max(terminal['rho'])),
                      clock_charge=float(terminal['I']),U1_charge=float(terminal['Q']),clock_charge_if_lapse_flux_omitted=float(noflux),
                      shift_coefficients=coeff.tolist(),full_nodal_shift_residual=float(np.max(np.abs(terminal['ES']))),
                      lapse_min=min(float(z['N']) for z in profs),physical_tilt_max=max(float(mp.sqrt(sum(x*x for x in z['vv']))) for z in profs)))
 for f,(h,mtime) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==mtime
 checks.append(dict(name='all_pinned_source_bytes_and_mtimes_preserved',passed=True))
 return dict(kind='R4C1_RTAU_PERIODIC_NUMERICAL_V1',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,source_sha256=pins,epsilon='1/1000',results=results,
  fields='all metric/frame/condensate/reservoir/force profiles from frozen specification; exact Z, positive-clock lapse; all nonconstant shift modes',
  continuum_tail_bound='NOT_SUPPLIED',validated_nonlinear_inverse='NOT_SUPPLIED',continuum_preparation_admitted=False,
  fixed_charge_targets=dict(clock='1/5',U1='1'),full_reduced_interactions='INCOMPLETE',physical_window_demonstrated=False,
  review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
