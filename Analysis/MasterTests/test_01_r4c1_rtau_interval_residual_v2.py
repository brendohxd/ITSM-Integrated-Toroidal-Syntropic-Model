"""Attempt continuum residual/charge enclosures, no inverse/existence claim."""
from pathlib import Path
import ast,argparse,hashlib,importlib.util,json,math
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
HELPER='Analysis/MasterTests/r4c1_interval_spatial_jet_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_INTERVAL_RESIDUAL_V1_CONTRACT_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=40;checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 assert SHA((ROOT/PARENT).read_bytes())=='58fc8db6b8d10ee57f2974e0415685ded3cfe9e80745044b19b551b7827c0d60'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256'])
 for p in (SELF,PARENT,HELPER,CONTRACT):pins[p]=SHA((ROOT/p).read_bytes())
 snapshots={}
 for path,h in pins.items():
  p=ROOT/path;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snapshots[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 j=load('interval_spatial_jet',HELPER);J=j.Jet;iv=mp.iv;engine=j.Adapter()
 backend=load('interval_candidate_backend','Analysis/MasterTests/r4c1_two_repair_actions_v2.py')
 old=backend.load('interval_parameter_source',backend.QUADRATIC);exact=old.parameters()
 pars={k:J(iv.mpf(int(v.p))/int(v.q)) for k,v in exact.items()}
 originalpars={k:mp.mpf(int(v.p))/int(v.q) for k,v in exact.items()}
 action=backend.ClockGaugeAction('R-tau',pars,physical=True)
 original=backend.ClockGaugeAction('R-tau',originalpars,physical=True)
 scope=action.body.body.__globals__;scope['mp']=engine
 def stable_Y(q,dq,normal):
  scale=action.body.sqrt(q[0]);vf=[scale*q[6+i] for i in range(3)]
  grad=[0,0,dq[12]/scale];gamma=action.body.sqrt(1+sum(v*v for v in vf));vg=sum(v*g for v,g in zip(vf,grad))
  return sum((g+v*(normal+vg/(gamma+1)))**2 for v,g in zip(vf,grad))
 scope['stable_Y']=stable_Y
 tree=ast.parse((ROOT/backend.ORIGINAL).read_text(encoding='utf-8-sig'))
 body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
 # Retain the declared R-tau removal of the old regulator.
 for node in body.body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='Y' for t in node.targets):
   assert ast.unparse(node.value)=='dot(gp, mv(hp, gp))';node.value=ast.parse('stable_Y(q,dq,s)',mode='eval').body
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='reg' for t in node.targets):node.value=ast.Constant(0)
 exec(compile(ast.fix_missing_locations(ast.Module(body=[body],type_ignores=[])),'<equivalent-conformal-interval-body>','exec'),scope)
 action.body.body=scope['body']
 t=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
 profile=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 code=compile(ast.fix_missing_locations(ast.Module(body=[profile],type_ignores=[])),'<pinned-periodic-profile>','exec')
 sc=dict(mp=engine,e=J(iv.mpf(1)/1000),beta=pars['beta']);exec(code,sc)
 sr=dict(mp=mp,e=mp.mpf(1)/1000,beta=originalpars['beta']);exec(code,sr)
 candidate=d['results'][-1];H=candidate['H'];omega=candidate['omega'];coeff=candidate['shift_coefficients']
 def state_and_gradient(theta,interval):
  lib=engine if interval else mp;prof=(sc if interval else sr)['profiles'](theta)
  S=[];Sz=[]
  for row in coeff:
   ss=lib.mpf(0);sz=lib.mpf(0)
   for n in range(1,17):
    c=lib.mpf(row[2*n-2]);sn=lib.mpf(row[2*n-1])
    ss+=c*lib.cos(n*theta)+sn*lib.sin(n*theta);sz+=n*(-c*lib.sin(n*theta)+sn*lib.cos(n*theta))
   S.append(ss);Sz.append(sz)
  target=action if interval else original;bt=target.body;tape=bt.Tape()
  vals=S+Sz+[prof['N'],prof['Nz'],prof['ud'],lib.mpf(omega)+prof['vd']]
  variables=[tape.var(v) for v in vals];vel=[lib.mpf(0) for _ in range(16)];ht=lib.mpf(H)+prof['lamdot']
  for idx in (0,3,5):vel[idx]=2*ht*prof['q'][idx]
  for idx in range(3):vel[6+idx]=(prof['vt'][idx]-ht*prof['vv'][idx])/prof['scale']
  vel[9]=variables[8];vel[10]=variables[9];vel[11]=prof['rd'];vel[12]=prof['psd'];vel[14]=lib.mpf(1)
  value=target.density(prof['q']+vel+prof['dz']+variables[:6]+variables[6:8])[0]
  return bt.val(value),tape.grad(value,variables),prof
 # Independent elementary jet tests and original-density point containment.
 for point in ('0.5','0.7'):
  x=J.variable(iv.mpf(point));xx=mp.mpf(point)
  for label,jet,fn in [('exp',j.exp(x),mp.exp),('sin',j.trig(x),mp.sin),('power',x**mp.mpf('1.5'),lambda z:z**mp.mpf('1.5'))]:
   for n in range(5):
    actual=mp.diff(fn,xx,n)/math.factorial(n);interval=jet.c[n]
    check('elementary_'+point+'_'+label+'_'+str(n),j.lower(interval)<=actual<=j.upper(interval))
 for point in ('0.3','1.1'):
  vv,gg,pp=state_and_gradient(J.variable(iv.mpf(point)),True)
  ref,gr,_=state_and_gradient(mp.mpf(point),False)
  check('original_density_interval_contains_'+point,j.lower(vv.c[0])<=ref<=j.upper(vv.c[0]))
  check('original_gradient_interval_contains_'+point,all(j.lower(x.c[0])<=r<=j.upper(x.c[0]) for x,r in zip(gg,gr)))
 print('INTERVAL_JET_AND_ORIGINAL_DENSITY_CONTROLS_COMPLETE',flush=True)
 def outputs(gr,prof):
  residual=[]
  for q in range(3):residual.append([gr[q].c[n]-(n+1)*gr[3+q].c[n+1] for n in range(4)])
  en=J(coefficients=[gr[6].c[n]-(n+1)*gr[7].c[n+1] for n in range(4)]+[iv.mpf(0)])
  rho=en/prof['volume'];I=(gr[6]-pars['beta']*prof['dz'][12]*gr[7])/prof['C']
  Q=prof['q'][9]*gr[9]-prof['q'][10]*gr[8]
  return residual,rho,I,Q
 allresults=[]
 for count in (32,64):
  cells=[];chargeI=iv.mpf(0);chargeQ=iv.mpf(0);rmax=[mp.mpf(0)]*3;rholow=mp.inf
  h=iv.pi/count
  for idx in range(count):
   center=iv.pi*(2*idx+1)/count
   left=iv.pi*(2*idx)/count;right=iv.pi*(2*idx+2)/count
   domain=iv.mpf([j.lower(left),j.upper(right)])
   _,gc,pc=state_and_gradient(J.variable(center),True)
   _,gb,pb=state_and_gradient(J.variable(domain),True)
   rc,rhoc,Ic,Qc=outputs(gc,pc);rb,rhob,Ib,Qb=outputs(gb,pb)
   bound=[]
   for comp in range(3):
    enclosure=sum((abs(rc[comp][n])*h**n for n in range(3)),iv.mpf(0))+abs(rb[comp][3])*h**3
    rmax[comp]=max(rmax[comp],j.upper(enclosure));bound.append(j.endpoints(enclosure))
   rholow=min(rholow,j.lower(rhob.c[0]))
   for cen,box,which in ((Ic,Ib,'I'),(Qc,Qb,'Q')):
    error=abs(box.c[3])*h**3/4
    average=cen.c[0]+cen.c[2]*h*h/3+iv.mpf([-j.upper(error),j.upper(error)])
    if which=='I':chargeI+=average/count
    else:chargeQ+=average/count
   cells.append(dict(index=idx,residual_bounds_binary=bound,density_interval_binary=j.endpoints(rhob.c[0])))
   if idx%8==0:print('CELLS',count,'DONE',idx+1,flush=True)
  check('all_cells_'+str(count)+'_finite_residual',all(mp.isfinite(x) for x in rmax))
  check('all_cells_'+str(count)+'_positive_density',rholow>0,mp.nstr(rholow,30))
  allresults.append(dict(cells=count,residual_upper_approx=[mp.nstr(x,30) for x in rmax],residual_upper_binary=[list(x._mpf_) for x in rmax],
                         density_lower_approx=mp.nstr(rholow,30),clock_charge_binary=j.endpoints(chargeI),U1_charge_binary=j.endpoints(chargeQ),
                         clock_error_upper_approx=mp.nstr(j.abs_upper(chargeI-iv.mpf(1)/5),30),U1_error_upper_approx=mp.nstr(j.abs_upper(chargeQ-1),30),cell_enclosures=cells))
 for f,(digest,mtime) in snapshots.items():assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime
 check('all_pinned_inputs_bytes_and_mtimes_preserved',True,len(snapshots))
 return dict(kind='R4C1_RTAU_INTERVAL_RESIDUAL_V2',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  interval_precision=40,spatial_jet_order=4,results=allresults,rounding='outward interval operations; exact binary endpoint tuples retained',
  validated_nonlinear_inverse='NOT_SUPPLIED',continuum_preparation_admitted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
