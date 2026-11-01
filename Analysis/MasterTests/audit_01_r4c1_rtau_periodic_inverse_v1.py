"""Independent full-action derivative controls and binary certificate audit."""
from pathlib import Path
import ast,argparse,hashlib,importlib.util,json
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
NUM='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_INVERSE_AUDIT_V1_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=80;mp.iv.dps=40;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='9c22269a9e40c331fd9c72ad72e44e9f67705524193293e2a11adc9f131827b9'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256'])
 for p in (SELF,PARENT,SPEC):pins[p]=SHA((ROOT/p).read_bytes())
 snaps={}
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snaps[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 def interval(ends):
  lo,hi=[mp.mpf(tuple(t)) for t in ends]
  assert mp.isfinite(lo) and mp.isfinite(hi) and lo<=hi
  return iv.mpf([lo,hi])
 def up(x):return mp.mpf(x._mpi_[1])
 def low(x):return mp.mpf(x._mpi_[0])
 rows=[mp.mpf(0)]*3;charges=[mp.mpf(0)]*2;paircount=0
 for cell in d['cell_enclosures']:
  for i,ends in enumerate(cell['shift_rows_binary']):
   v=interval(ends);assert low(v)>=0;rows[i]=max(rows[i],up(v));paircount+=1
  for i,ends in enumerate(cell['charge_rows_binary']):
   v=interval(ends);assert low(v)>=0;charges[i]=max(charges[i],up(v));paircount+=1
  assert mp.isfinite(mp.mpf(tuple(cell['rho_lower_binary']))) and mp.mpf(tuple(cell['rho_lower_binary']))>0
  assert cell['force_domain_verified'] is True
 a=(iv.mpf(33)/5)*iv.sqrt(iv.mpf(3469)/4620)
 q=max(38*iv.mpf(max(rows)),(iv.mpf(charges[0])+iv.mpf(charges[1]))/iv.mpf(low(a)),iv.mpf(charges[1]),key=up)
 claimed=interval(d['q_binary']);check('all_binary_derivative_cells_finite',True,paircount)
 check('q_recomputed_from_every_cell',low(claimed)<=low(q) and up(q)<=up(claimed))
 eta=interval(d['eta_binary']);r=interval(d['radius_binary']);margin=interval(d['selfmap_margin_binary'])
 check('contraction_and_strict_selfmap',up(q)<1 and up(eta+q*r)<low(r) and low(margin)>0)
 original=json.loads((ROOT/NUM).read_text())['results'][-1];co=np.array(d['parity_center_coefficients'])
 check('parity_center_exactly_recorded',all((co[i,j]==0) for i in range(3) for j in range(32) if (j%2==1 if i<2 else j%2==0)))
 backendpath=ROOT/'Analysis/MasterTests/r4c1_two_repair_actions_v2.py';sp=importlib.util.spec_from_file_location('inverse_audit_backend',backendpath);backend=importlib.util.module_from_spec(sp);sp.loader.exec_module(backend)
 old=backend.load('inverse_audit_parameters',backend.QUADRATIC);par={k:mp.mpf(int(v.p))/int(v.q) for k,v in old.parameters().items()}
 action=backend.ClockGaugeAction('R-tau',par,physical=True)
 source=ROOT/'Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py';tree=ast.parse(source.read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
 defs=[n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name in ('profiles','local')]
 scope=dict(mp=mp,np=np,e=mp.mpf(1)/1000,beta=par['beta'],b=action.body,action=action)
 exec(compile(ast.fix_missing_locations(ast.Module(body=defs,type_ignores=[])),'<pinned-original-full-local-gradient>','exec'),scope)
 N=65;theta=2*np.pi*(np.arange(N)+.37)/N;m=(N-1)//2
 B=np.column_stack([f(n*theta) for n in range(1,m+1) for f in (np.cos,np.sin)])
 Bz=np.column_stack([n*f(n*theta) for n in range(1,m+1) for f in (lambda t:-np.sin(t),np.cos)])
 D=(2/N)*Bz@B.T;S=B[:,:32]@co.T;Sz=Bz[:,:32]@co.T
 profiles=[scope['profiles'](2*mp.pi*(j+mp.mpf('.37'))/N) for j in range(N)]
 def evaluate(sh,ds,H,omega):
  gradients=np.array([scope['local'](p,sh[j],ds[j],H,omega) for j,p in enumerate(profiles)])
  ES=gradients[:,:3]-D@gradients[:,3:6];EN=gradients[:,6]-D@gradients[:,7]
  C=np.array([float(p['C']) for p in profiles]);I=float(np.mean(EN/C))
  Q=float(np.mean([float(p['q'][9])*gradients[j,9]-float(p['q'][10])*gradients[j,8] for j,p in enumerate(profiles)]))
  return ES,np.array([I,Q])
 a_float=float((mp.mpf(33)/5)*mp.sqrt(mp.mpf(3469)/4620));controls=[]
 for which in range(5):
  ds=np.zeros_like(S);dsz=np.zeros_like(S);ddsz=np.zeros_like(S);dh=0.;dw=0.
  if which<3:
   freq=2 if which==1 else 1
   if which<2:ds[:,which]=np.cos(freq*theta)/freq**2;dsz[:,which]=-np.sin(freq*theta)/freq;ddsz[:,which]=-np.cos(freq*theta)
   else:ds[:,which]=np.sin(theta);dsz[:,which]=np.cos(theta);ddsz[:,which]=-np.sin(theta)
  elif which==3:dh=1.
  else:dw=1.
  baseline=-ddsz*np.array([.5,.5,-1/15]);cbase=np.array([a_float*dh-dw,dw])
  for h in (1e-4,1e-5):
   p=evaluate(S+h*ds,Sz+h*dsz,original['H']+h*dh,original['omega']+h*dw)
   n=evaluate(S-h*ds,Sz-h*dsz,original['H']-h*dh,original['omega']-h*dw)
   defect=(p[0]-n[0])/(2*h)-baseline;cdef=(p[1]-n[1])/(2*h)-cbase
   observed=max(38*np.max(np.abs(defect)),(abs(cdef[0])+abs(cdef[1]))/a_float,abs(cdef[1]))
   check('independent_full_action_derivative_'+str(which)+'_'+str(h),observed<=float(up(q))+1e-5,float(observed))
   controls.append(dict(direction=which,step=h,preconditioned_observed_defect=float(observed)))
 for f,(h,t) in snaps.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_pinned_source_bytes_and_mtimes_preserved',True,len(snaps))
 return dict(kind='R4C1_RTAU_PERIODIC_INVERSE_AUDIT_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,controls=controls,
  finite_difference_controls_are_not_interval_proof=True,review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
