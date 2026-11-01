"""Attempt a quantitative periodic nonlinear inverse on the full correction ball."""
from pathlib import Path
import ast,argparse,hashlib,importlib.util,json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_interval_residual_v3_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
HELPER='Analysis/MasterTests/r4c1_interval_spatial_jet_v4.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_CONTRACT_2026-10-31.md'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=40;iv=mp.iv;checks=[]
 def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
 assert SHA((ROOT/PARENT).read_bytes())=='d116cbb8c71241c4e3c85c1b260f082f5e30306dbf51243d26e446e36e797484'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256'])
 for f in (SELF,PARENT,HELPER,CONTRACT,SPEC):pins[f]=SHA((ROOT/f).read_bytes())
 snaps={}
 for rel,want in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==want and sc.read_text().split()[0].lower()==want
  for f in (p,sc):snaps[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 j=load('inverse_spatial_jet',HELPER);j.ORDER=1;J=j.Jet;engine=j.Adapter()
 backend=load('inverse_candidate_backend','Analysis/MasterTests/r4c1_two_repair_actions_v2.py')
 old=backend.load('inverse_parameters',backend.QUADRATIC);params={k:J(iv.mpf(int(v.p))/int(v.q)) for k,v in old.parameters().items()}
 action=backend.ClockGaugeAction('R-tau',params,physical=True);scope=action.body.body.__globals__;scope['mp']=engine
 tree=ast.parse((ROOT/backend.ORIGINAL).read_text(encoding='utf-8-sig'));body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
 for node in body.body:
  if isinstance(node,ast.Assign):
   if any(isinstance(t,ast.Name) and t.id=='force' for t in node.targets):
    assert isinstance(node.value,ast.BinOp) and isinstance(node.value.op,ast.Sub);node.value=node.value.left
   if any(isinstance(t,ast.Name) and t.id=='reg' for t in node.targets):node.value=ast.Constant(0)
 exec(compile(ast.fix_missing_locations(ast.Module(body=[body],type_ignores=[])),'<analytic-summand-only>','exec'),scope);action.body.body=scope['body']
 tree=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
 fn=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 ps=dict(mp=engine,e=J(iv.mpf(1)/1000),beta=params['beta']);exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<pinned-profiles>','exec'),ps)
 profile=ps['profiles'];candidate=json.loads((ROOT/NUMERICAL).read_text())['results'][-1]
 coefficients=candidate['shift_coefficients'];projected=[];displacement=iv.mpf(0)
 for axis,row in enumerate(coefficients):
  new=[];axis_error=iv.mpf(0)
  for index,c in enumerate(row):
   keep=(index%2==0) if axis<2 else (index%2==1)
   new.append(c if keep else 0.)
   if not keep:axis_error+=abs(iv.mpf(c))*(index//2+1)**2
  displacement=iv.mpf([max(j.lower(displacement),j.lower(axis_error)),max(j.upper(displacement),j.upper(axis_error))]);projected.append(new)
 radius=iv.mpf(1)/1000;check('explicit_parity_center_near_original',j.upper(displacement)<j.lower(radius),mp.nstr(j.upper(displacement),30))
 a0=(iv.mpf(33)/5)*iv.sqrt(iv.mpf(3469)/4620);alo=j.lower(a0)
 check('periodic_green_inverse_bound',j.upper(15*iv.pi**2/4)<38)
 # First-order propagation, including a zero-crossing square, is checked independently.
 x=J.variable(iv.mpf([-.1,.1]));square=x**2
 check('first_order_square_interval',j.lower(square.c[0])==0 and j.upper(square.c[0])>=mp.mpf('.01'))
 check('first_order_exp_derivative',j.lower(j.exp(J.variable(iv.mpf(0))).c[1])==j.upper(j.exp(J.variable(iv.mpf(0))).c[1])==1)
 def gradient(prof,X):
  H=X[6];omega=X[7];tape=action.body.Tape()
  vals=X[:6]+[prof['N'],prof['Nz'],prof['ud'],omega+prof['vd']];nodes=[tape.var(x) for x in vals]
  vel=[J(0) for _ in range(16)];ht=H+prof['lamdot']
  for q in (0,3,5):vel[q]=2*ht*prof['q'][q]
  for q in range(3):vel[6+q]=(prof['vt'][q]-ht*prof['vv'][q])/prof['scale']
  vel[9]=nodes[8];vel[10]=nodes[9];vel[11]=prof['rd'];vel[12]=prof['psd'];vel[14]=J(1)
  val=action.density(prof['q']+vel+prof['dz']+nodes[:6]+nodes[6:8])[0]
  return tape.grad(val,nodes)
 def charges(gr,prof):return ((gr[6]-params['beta']*prof['dz'][12]*gr[7])/prof['C'],prof['q'][9]*gr[9]-prof['q'][10]*gr[8])
 # Homogeneous charge reference from the same action.
 ps['e']=J(0);prof=profile(J.variable(iv.mpf(0)));z=[J(0) for _ in range(8)];z[6]=J(iv.sqrt(iv.mpf(3469)/4620));z[7]=J(1)
 ref=[]
 for index in (6,7):
  plus=z.copy();minus=z.copy();plus[index]+=1;minus[index]-=1
  qp=charges(gradient(prof,plus),prof);qm=charges(gradient(prof,minus),prof)
  ref.append([(x-y)/2 for x,y in zip(qp,qm)])
 targets=[a0,iv.mpf(0),iv.mpf(-1),iv.mpf(1)]
 actual=[ref[0][0].c[0],ref[0][1].c[0],ref[1][0].c[0],ref[1][1].c[0]]
 check('homogeneous_action_charge_reference',all(j.abs_upper(x-t)<mp.mpf('1e-30') for x,t in zip(actual,targets)))
 ps['e']=J(iv.mpf(1)/1000)
 # Rigorous cusp bounds, subject to the domain checks below.
 force_shift=6*(iv.mpf(2)/7)*(iv.mpf(101)/100)**2*(iv.mpf(2)/10000)*(iv.mpf(2)/100000000)**2
 force_I=6*(iv.mpf(2)/7)*(iv.mpf(101)/99)*(iv.mpf(2)/100000000)*((iv.mpf(2)/10000)**2+(iv.mpf(3)/10)*(iv.mpf(2)/10000)*(iv.mpf(1)/10000))
 force_rho=(iv.mpf(2)/7)*((iv.mpf(2)/10000)**3+3*(iv.mpf(3)/10)*(iv.mpf(2)/10000)**2/10000)
 check('full_cusp_derivative_and_density_bounds',j.upper(force_shift)<mp.mpf('1e-17') and j.upper(force_I)<mp.mpf('1e-12') and j.upper(force_rho)<mp.mpf('1e-10'))
 def upabs(x):return j.upper(abs(x))
 count=32;rows=[mp.mpf(0)]*3;Irow=mp.mpf(0);Qrow=mp.mpf(0);rho_min=mp.inf;cell_data=[];domain_ok=True
 for cell in range(count):
  lo=iv.pi*(2*cell)/count;hi=iv.pi*(2*cell+2)/count;theta=J.variable(iv.mpf([j.lower(lo),j.upper(hi)]));prof=profile(theta)
  ss=[];sz=[]
  for row in projected:
   val=J(0);dz=J(0)
   for n in range(1,17):
    c=J(row[2*n-2]);sn=J(row[2*n-1]);val+=c*engine.cos(n*theta)+sn*engine.sin(n*theta);dz+=n*(-c*engine.sin(n*theta)+sn*engine.cos(n*theta))
   ss.append(J(coefficients=[val.c[0]+iv.mpf([-j.upper(radius),j.upper(radius)]),val.c[1]+iv.mpf([-j.upper(radius),j.upper(radius)])]))
   sz.append(J(coefficients=[dz.c[0]+iv.mpf([-j.upper(radius),j.upper(radius)]),dz.c[1]+iv.mpf([-j.upper(radius),j.upper(radius)])]))
  X=ss+sz+[J(iv.mpf(candidate['H'])+iv.mpf([-j.upper(radius),j.upper(radius)])),J(iv.mpf(candidate['omega'])+iv.mpf([-j.upper(radius),j.upper(radius)]))]
  allzero=[J(0) for _ in range(8)];der=[]
  for index in range(8):
   plus=allzero.copy();minus=allzero.copy();plus[index]+=1;minus[index]-=1
   gp=gradient(prof,plus);gm=gradient(prof,minus);der.append([(x-y)/2 for x,y in zip(gp,gm)])
  K0=(iv.mpf(1)/2,iv.mpf(1)/2,-iv.mpf(1)/15);localrows=[]
  for i in range(3):
   total=iv.mpf(0)
   for q in range(3):
    A=der[q][i].c[0]-der[q][3+i].c[1]
    B=der[3+q][i].c[0]-der[q][3+i].c[0]-der[3+q][3+i].c[1]
    C=der[3+q][3+i].c[0]-(K0[i] if q==i else 0)
    total+=abs(A)+abs(B)+abs(C)
   for q in (6,7):total+=abs(der[q][i].c[0]-der[q][3+i].c[1])
   total+=force_shift;rows[i]=max(rows[i],j.upper(total));localrows.append(j.endpoints(total))
  cder=[]
  for index in range(8):
   plus=X.copy();minus=X.copy();plus[index]+=1;minus[index]-=1
   cp=charges(gradient(prof,plus),prof);cm=charges(gradient(prof,minus),prof);cder.append([(x-y)/2 for x,y in zip(cp,cm)])
  charge_bounds=[]
  for which in (0,1):
   bound=iv.mpf(0)
   for q in range(3):bound+=abs(cder[q][which].c[0]-cder[3+q][which].c[1])
   baselineH=a0 if which==0 else iv.mpf(0);baselineOmega=iv.mpf(-1) if which==0 else iv.mpf(1)
   bound+=abs(cder[6][which].c[0]-baselineH)+abs(cder[7][which].c[0]-baselineOmega)
   if which==0:bound+=force_I
   charge_bounds.append(j.endpoints(bound))
   if which==0:Irow=max(Irow,j.upper(bound))
   else:Qrow=max(Qrow,j.upper(bound))
  gb=gradient(prof,X);rho=(gb[6].c[0]-gb[7].c[1])/prof['volume'].c[0]-force_rho;rho_min=min(rho_min,j.lower(rho))
  normal=(prof['psd']-X[2]*prof['dz'][12])/prof['N']
  v2=sum(t*t for t in prof['vv']);gphys=prof['dz'][12]/prof['scale']
  ok=all(j.lower(prof[key].c[0])>=mp.mpf('.99') and j.upper(prof[key].c[0])<=mp.mpf('1.01') for key in ('N','C','volume'))
  ok=ok and j.upper(v2.c[0])<=mp.mpf('1e-8') and upabs(prof['dz'][12].c[0])<=mp.mpf('1e-4') and upabs(gphys.c[0])<=mp.mpf('1e-4') and upabs(X[2].c[0])<=mp.mpf('.01') and upabs(normal.c[0])<=mp.mpf('.3')
  domain_ok=domain_ok and ok
  cell_data.append(dict(index=cell,shift_rows_binary=localrows,charge_rows_binary=charge_bounds,rho_lower_binary=list(j.lower(rho)._mpf_),force_domain_verified=bool(ok)))
  if cell%4==0:print('INVERSE_CELLS',cell+1,'OF',count,flush=True)
 # Precondition componentwise to avoid treating the charge inverse as a wave inverse.
 qbound=max(iv.mpf(38)*iv.mpf(max(rows)),(iv.mpf(Irow)+iv.mpf(Qrow))/iv.mpf(alo),iv.mpf(Qrow),key=j.upper)
 rr=parent['results'][-1];res=[iv.mpf(mp.mpf(tuple(x))) for x in rr['residual_upper_binary']]
 def interval_binary(ends):return iv.mpf([mp.mpf(tuple(ends[0])),mp.mpf(tuple(ends[1]))])
 ri=abs(interval_binary(rr['clock_charge_binary'])-iv.mpf(1)/5);rq=abs(interval_binary(rr['U1_charge_binary'])-1)
 eta_original=max(38*max(res,key=j.upper),(ri+rq)/iv.mpf(alo),rq,key=j.upper)
 eta=eta_original+(1+qbound)*displacement;margin=radius-eta-qbound*radius
 check('force_domain_on_whole_correction_ball',domain_ok)
 check('positive_density_on_whole_correction_ball',mp.isfinite(rho_min) and rho_min>0,mp.nstr(rho_min,35))
 check('uniform_contraction_q_less_than_one',mp.isfinite(j.upper(qbound)) and j.upper(qbound)<1,mp.nstr(j.upper(qbound),35))
 check('ball_maps_strictly_inside_itself',mp.isfinite(j.lower(margin)) and j.lower(margin)>0,mp.nstr(j.lower(margin),35))
 for f,(h,t) in snaps.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snaps))
 success=all(c['passed'] for c in checks)
 return dict(kind='R4C1_RTAU_PERIODIC_INVERSE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  parity_center_coefficients=projected,center_C2_displacement_binary=j.endpoints(displacement),radius_binary=j.endpoints(radius),
  shift_derivative_rows_approx=[mp.nstr(x,35) for x in rows],charge_derivative_rows_approx=[mp.nstr(x,35) for x in (Irow,Qrow)],
  q_binary=j.endpoints(qbound),eta_binary=j.endpoints(eta),selfmap_margin_binary=j.endpoints(margin),
  q_upper_approx=mp.nstr(j.upper(qbound),35),eta_upper_approx=mp.nstr(j.upper(eta),35),margin_lower_approx=mp.nstr(j.lower(margin),35),rho_lower_approx=mp.nstr(rho_min,35),
  force_shift_bound_binary=j.endpoints(force_shift),force_clock_bound_binary=j.endpoints(force_I),force_density_bound_binary=j.endpoints(force_rho),
  cell_enclosures=cell_data,computer_assisted_inequalities_pass=success,
  scope='reflection-symmetric periodic initial constraint slice; full continuum residual and correction ball; no projected evolution',
  nonlinear_time_evolution=False,reduced_coupled_interactions='INCOMPLETE',physical_window_demonstrated=False,canonical_parent_adopted=False,
  review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
