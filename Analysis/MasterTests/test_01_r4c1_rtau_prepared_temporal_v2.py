"""Unreduced prepared-slice temporal Hessian; not physical admission."""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PREPARED_TEMPORAL_V1_CONTRACT_2026-10-31.md'
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=45;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 parent=json.loads((ROOT/PARENT).read_text());assert SHA((ROOT/PARENT).read_bytes())=='449ce6a63c04a479fb8fc79cee62806ba5072d8dacac99f8614e9ab96e9ce014'
 pins=dict(parent['source_sha256'])
 for p in (SELF,CONTRACT,PARENT,'Analysis/MasterTests/test_01_r4c1_rtau_prepared_temporal_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v1_attempt_01/summary.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_PREPARED_TEMPORAL_V2_SPEC_2026-10-31.md'):pins[p]=SHA((ROOT/p).read_bytes())
 snapshots={}
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snapshots[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 backend=load('prepared_temporal_backend',BACKEND);types=backend.load('prepared_temporal_parameters',backend.QUADRATIC);par=types.parameters()
 action=backend.ClockGaugeAction('R-tau',par)
 # Symbolic body receives ordinary SymPy scalars, not two incompatible Jet classes.
 action.body.sqrt=s.sqrt;action.body.exp=s.exp;action.body.body.__globals__.update(sqrt=s.sqrt,exp=s.exp)
 w=s.Symbol('w',real=True);ys=s.symbols('k0:6')+s.symbols('x0:3')
 q=[s.Integer(z) for z in (1,0,0,1,0,1,0,0,0,1,0,1,0,0,0)];q[8]=w
 y=[ys[i]/(s.sqrt(2) if a!=b else 1) for i,(a,b) in enumerate(HM)]+list(ys[6:])+[s.Integer(0)]*3
 L=action.body.body(q,[s.Integer(0)]*15,y,s.Integer(0),par)
 M=s.hessian(L,ys).applyfunc(lambda z:s.factor(s.cancel(z)));M0=M.subs(w,0)
 expected=s.eye(9)
 for a in (0,3,5):
  for b in (0,3,5):expected[a,b]-=s.Rational(16,15)
 for a in range(6,9):expected[a,a]=s.Rational(1,6)
 check('fresh_full_metric_frame_zero_tilt_reference',M0==expected)
 check('all_six_metric_and_three_frame_rates_retained',M.shape==(9,9) and M.det()!=0)
 check('exact_symbolic_symmetry',M==M.T)
 check('zero_tilt_inertia_8_positive_1_negative',M0.eigenvals()=={s.Integer(1):5,-s.Rational(11,5):1,s.Rational(1,6):3})
 delta=(M-M0).applyfunc(s.factor)
 def iev(expr,wi):
  if expr==w:return wi
  if expr.is_Rational:return iv.mpf(int(expr.p))/int(expr.q)
  if expr.is_Add:return sum((iev(v,wi) for v in expr.args),iv.mpf(0))
  if expr.is_Mul:
   z=iv.mpf(1)
   for v in expr.args:z*=iev(v,wi)
   return z
  if expr.is_Pow:
   a,b=expr.args;v=iev(a,wi)
   return v**int(b) if b.is_Integer else v**iev(b,wi)
  raise TypeError(str(expr))
 upper=lambda x:mp.mpf(x._mpi_[1]);lower=lambda x:mp.mpf(x._mpi_[0]);binary=lambda x:[list(v) for v in x._mpi_]
 wi=iv.mpf([-1,1])/10000;entries=[[iev(delta[i,j],wi) for j in range(9)] for i in range(9)]
 rows=[sum((abs(x) for x in row),iv.mpf(0)) for row in entries];defect=max(upper(x) for x in rows)
 gap=iv.mpf(1)/6-iv.mpf(defect)
 check('uniform_metric_frame_inertia_and_inverse_gap',lower(gap)>mp.mpf('.16'),mp.nstr(lower(gap),40))
 check('all_interval_entries_finite_ordered',all(mp.isfinite(lower(x)) and mp.isfinite(upper(x)) and lower(x)<=upper(x) for row in entries for x in row))
 # The normal-frame tensor contractions transform orthogonally under spatial rotations.
 def tensor(v,ctx):
  h=ctx.zeros(3)
  for i,(a,b) in enumerate(HM):h[a,b]=h[b,a]=v[i]/(ctx.sqrt(2) if a!=b else (s.Integer(1) if ctx is s else mp.mpf(1)))
  return h
 def rotation_lift(R,ctx):
  T=ctx.zeros(9)
  for j in range(6):
   v=[ctx.mpf(0)]*6 if ctx is mp else [s.Integer(0)]*6;v[j]=1;K=R.T*tensor(v,ctx)*R
   for i,(a,b) in enumerate(HM):T[i,j]=K[a,b]*(ctx.sqrt(2) if a!=b else 1)
  T[6:9,6:9]=R.T;return T
 R=s.Matrix([[s.Rational(3,5),0,s.Rational(4,5)],[0,1,0],[-s.Rational(4,5),0,s.Rational(3,5)]])
 T=rotation_lift(R,s);check('Frobenius_rotation_lift_orthogonal',T.T*T==s.eye(9))
 qr=q.copy();qr[6:9]=list(R*s.Matrix([0,0,w]));Lg=action.body.body(qr,[s.Integer(0)]*15,y,s.Integer(0),par)
 Mg=s.hessian(Lg,ys);rot_error=(Mg-T.T*M*T).applyfunc(s.simplify)
 check('independent_nonaxial_full_action_rotation_control',rot_error==s.zeros(9))
 # Exact full force coefficient and its C2 extension bound: |b|^2 <= c Y.
 cc,ss,vz,g,aa,kq=s.symbols('c s Vz g A KQ',positive=True);gam=s.sqrt(1+cc)
 Y=cc*ss**2+2*gam*vz*ss*g+(1+vz*vz)*g*g;b=cc*ss+gam*vz*g
 force=kq*(gam*ss+vz*g)**2/2-aa*Y**s.Rational(3,2)
 force_h=kq*(1+cc)-3*aa*(cc*s.sqrt(Y)+b*b/s.sqrt(Y))
 check('full_force_second_variation_identity',s.simplify(s.diff(force,ss,2)-force_h)==0)
 cmax=iv.mpf(1)/100000000;gmax=iv.mpf(1)/10000;smax=iv.mpf(3)/10
 qmax=iv.sqrt(1+cmax)*gmax+iv.sqrt(cmax)*smax
 force_loss=6*(iv.mpf(2)/7)*cmax*qmax;force_lower=iv.mpf(3)-force_loss
 align_lower=1-(iv.mpf(1)/13)*cmax*(iv.mpf(1001)/1000)
 check('uniform_force_kinetic_coefficient_positive',lower(force_lower)>mp.mpf('2.99999999999'),mp.nstr(lower(force_lower),40))
 check('uniform_alignment_block_positive',lower(align_lower)>mp.mpf('.999999999'),mp.nstr(lower(align_lower),40))
 # Fixed prepared profiles put EVERY certified root inside this velocity domain.
 vmax2=(iv.mpf(3)/74000)**2+(iv.mpf(1)/41000)**2+(iv.mpf(1)/43000)**2
 pgrad=(iv.mpf(1)/29000+iv.mpf(2)/31000)*iv.exp(iv.mpf(1)/13000)
 spbound=(iv.mpf(1)/5+iv.mpf(1)/47000+(iv.mpf(1)/100)*pgrad)/(iv.mpf(99)/100)
 umag2=(1+iv.mpf(1)/17000)**2+(iv.mpf(1)/19000)**2
 check('fixed_profile_frame_domain_for_entire_root_ball',upper(vmax2)<lower(cmax))
 check('fixed_profile_gradient_and_scalar_domain',upper(pgrad)<lower(gmax) and upper(spbound)<lower(smax) and upper(umag2)<mp.mpf('1.001'))
 # Original unconstrained density numerical controls, not the homogeneous generator.
 pn={k:mp.mpf(int(v.p))/int(v.q) for k,v in par.items()};physical=backend.ClockGaugeAction('R-tau',pn,physical=True)
 tree=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate');fn=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 scope=dict(mp=mp,e=mp.mpf(1)/1000,beta=pn['beta']);exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<pinned-prepared-profiles>','exec'),scope)
 centre=json.loads((ROOT/NUMERICAL).read_text())['results'][-1];co=json.loads((ROOT/INVERSE).read_text())['parity_center_coefficients'];controls=[]
 mf=s.lambdify(w,M,'mpmath')
 for zs in ('0.3','1.1','2.4'):
  z=mp.mpf(zs);prof=scope['profiles'](z);qv=prof['q'];dv=prof['dz'];N=prof['N'];a=prof['scale'];ht=mp.mpf(centre['H'])+prof['lamdot'];vel=[mp.mpf(0)]*16
  for i in (0,3,5):vel[i]=2*ht*qv[i]
  for i in range(3):vel[6+i]=(prof['vt'][i]-ht*prof['vv'][i])/a
  vel[9]=prof['ud'];vel[10]=mp.mpf(centre['omega'])+prof['vd'];vel[11]=prof['rd'];vel[12]=prof['psd'];vel[14]=1
  shifts=[sum(mp.mpf(row[2*n-2])*mp.cos(n*z)+mp.mpf(row[2*n-1])*mp.sin(n*z) for n in range(1,17)) for row in co]
  shiftz=[sum(n*(-mp.mpf(row[2*n-2])*mp.sin(n*z)+mp.mpf(row[2*n-1])*mp.cos(n*z)) for n in range(1,17)) for row in co]
  values=qv+vel+dv+shifts+shiftz+[N,prof['Nz']];V=mp.matrix(prof['vv']);cn=(V.T*V)[0];wn=mp.sqrt(cn);e3=V/wn
  seed=mp.matrix([1,0,0]);e1=seed-e3*(e3.T*seed)[0];e1/=mp.norm(e1);e2=mp.matrix([e3[1]*e1[2]-e3[2]*e1[1],e3[2]*e1[0]-e3[0]*e1[2],e3[0]*e1[1]-e3[1]*e1[0]])
  rn=mp.matrix([[e1[i],e2[i],e3[i]] for i in range(3)]);tn=rotation_lift(rn,mp)
  predicted=mp.zeros(14);predicted[:9,:9]=tn.T*mf(wn)*tn
  current=mp.matrix([qv[10],-qv[9],0]);predicted[9:12,9:12]=mp.eye(3)-pn['zeta']*cn*current*current.T
  sn=(prof['psd']-shifts[2]*dv[12])/N;gn=dv[12]/a;gamma=mp.sqrt(1+cn)
  rest=mp.matrix([0,0,gn])+V*(sn+V[2]*gn/(gamma+1));qn=mp.norm(rest);bn=cn*sn+gamma*V[2]*gn
  correction=3*pn['A']*(cn*qn+bn*bn/qn);predicted[12,12]=pn['K_Q']*(1+cn)-correction
  scalings=[2*N*a*a/(mp.sqrt(2) if i in (1,2,4) else 1) for i in range(6)]+[N/a]*3+[N]*5
  D=mp.diag(scalings)
  def grad(vals):
   tape=physical.body.Tape();vs=[tape.var(vals[16+i]) for i in range(14)];allv=vals.copy();allv[16:30]=vs;L=physical.density(allv)[0];return tape.grad(L,vs)
  errors=[];allHs=[]
  for st,tolerance in (('1e-18','1e-28'),('1e-24','1e-40')):
   step=mp.mpf(st);hh=mp.zeros(14)
   for j in range(14):
    vv=values.copy();vv[16+j]+=mp.j*step;column=grad(vv)
    for i,x in enumerate(column):hh[i,j]=mp.im(x)/step
   normalized=D*hh*D/(N*a**3);err=max(abs(x) for x in normalized-predicted)
   check('full_action_Hessian_'+zs+'_'+st,err<mp.mpf(tolerance),mp.nstr(err,40));errors.append(mp.nstr(err,50));allHs.append(normalized)
  check('full_action_Z_primary_temporal_null_'+zs,max(abs(allHs[-1][13,j]) for j in range(14))<mp.mpf('1e-70') and abs(grad(values)[13])<mp.mpf('1e-70'))
  check('omitted_full_force_Hessian_rejected_'+zs,correction>mp.mpf('1e-25'),mp.nstr(correction,40))
  controls.append(dict(z=zs,errors=errors,force_correction=mp.nstr(correction,50),unreduced_temporal_matrix=[[mp.nstr(x,50) for x in row] for row in predicted.tolist()]))
 for f,(h,t) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snapshots))
 return dict(kind='R4C1_RTAU_PREPARED_TEMPORAL_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  normal_coordinates='Frobenius K6, independent normal frame X3, canonical u/v/r rates, normal psi rate, Z rate',
  metric_frame_matrix_aligned=[[str(x) for x in row] for row in M.tolist()],metric_frame_delta_enclosures=[[binary(x) for x in row] for row in entries],
  bounds=dict(metric_frame_row_defects=[binary(x) for x in rows],metric_frame_gap=binary(gap),force_norm_upper=binary(qmax),force_loss_upper=binary(force_loss),force_kinetic_lower=binary(force_lower),alignment_lower=binary(align_lower)),
  force_formula=str(force_h),controls=controls,unreduced_inertia=dict(positive=12,negative=1,zero=1),
  physical_ghost_verdict='NOT_DETERMINED_BY_UNREDUCED_INERTIA',physical_symplectic_quotient='NOT_DERIVED',initial_accelerations='NOT_DERIVED',
  nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
