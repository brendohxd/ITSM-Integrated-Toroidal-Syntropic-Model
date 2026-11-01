"""Prepared clock-density full second variation and canonical operator.

All bounds are initial planar coefficient bounds, not an evolution theorem.
"""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json,types
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_v2_attempt_01/summary.json'
ROOT_RECEIPT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_MIXED_OPERATOR_V1_CONTRACT_2026-10-31.md'
SECOND='Analysis/MasterTests/r4c1_second_variation_jet_v1.py'
SPATIAL='Analysis/MasterTests/r4c1_interval_spatial_jet_v4.py'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='f4efb6bc588528aa6287fa2cca2a8020f581fddc0564e0336b9e8bf52906a814'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,PARENT,CONTRACT,SECOND,SPATIAL):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 j=load('mixed_spatial_jets',SPATIAL);j.ORDER=1;J=j.Jet;engine=j.Adapter()
 second=load('mixed_second_variations',SECOND);D=second.Second;D.scalar=staticmethod(J.cast);D.exponential=staticmethod(j.exp)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(z) for z in x._mpi_]
 # Nested differentiation must preserve value squares and their spatial jets.
 xx=D.var(J.variable(iv.mpf(2)),0);ff=xx**3
 check('nested_second_and_spatial_derivative_control',ff.h[0,0].c[0]==12 and ff.h[0,0].c[1]==6 and ff.g[0].c[1]==12)
 gamma,t,p,gn=s.symbols('gamma t p gn',positive=True);c=gamma**2-1
 boosted=gn+2*t*(p+t/(gamma+1))+c*(p+t/(gamma+1))**2
 unboosted=gn+c*p*p+2*gamma*t*p+t*t
 check('stable_norm_identity_for_arbitrary_metric',s.simplify(boosted-unboosted)==0)
 aa=s.Matrix(2,2,s.symbols('a0:4'));bb=s.Matrix(2,2,s.symbols('b0:4'));bd=s.Matrix(2,2,s.symbols('d0:4'))
 om0=aa-aa.T+bd.T;om1=bb+bb.T
 check('formal_two_form_skew_adjoint_identity',om0+om0.T-bd-bd.T==s.zeros(2))
 check('omitted_variable_coefficient_drift_rejected',aa-aa.T+(aa-aa.T).T-bd-bd.T!=s.zeros(2))
 backend=load('mixed_candidate_backend',BACKEND);old=backend.load('mixed_parameters',backend.QUADRATIC);exact=old.parameters()
 params={k:D(J(iv.mpf(int(v.p))/int(v.q))) for k,v in exact.items()}
 action=backend.ClockGaugeAction('R-tau',params,physical=True);scope=action.body.body.__globals__
 class Algebra:
  def mpf(self,x=0):return mp.mpf(x) if isinstance(x,str) and x in ('.5','0.5','1.5') else D(x)
  def sqrt(self,x):return D.cast(x)**mp.mpf('.5')
  def exp(self,x):return D.cast(x).exp()
 alg=Algebra();scope.update(mp=alg,sqrt=alg.sqrt,exp=alg.exp);action.body.sqrt=alg.sqrt;action.body.exp=alg.exp
 lastY=[]
 def stable_Y(h,hi,V,gam,gp):
  spatial=gp[1:];vg=action.body.dot(V,spatial);rest=[x+v*(gp[0]+vg/(gam+1)) for x,v in zip(action.body.mv(hi,spatial),V)]
  Y=action.body.dot(rest,action.body.mv(h,rest));lastY[:]=[Y];return Y
 scope['stable_Y']=stable_Y
 tree=ast.parse((ROOT/backend.ORIGINAL).read_text(encoding='utf-8-sig'));body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
 for node in body.body:
  if isinstance(node,ast.Assign):
   if any(isinstance(t,ast.Name) and t.id=='Y' for t in node.targets):
    assert ast.unparse(node.value)=='dot(gp, mv(hp, gp))';node.value=ast.parse('stable_Y(h,hi,V,gam,gp)',mode='eval').body
   if any(isinstance(t,ast.Name) and t.id=='reg' for t in node.targets):node.value=ast.Constant(0)
 exec(compile(ast.fix_missing_locations(ast.Module(body=[body],type_ignores=[])),'<equivalent-general-metric-clock-body>','exec'),scope);action.body.body=scope['body']
 # Combine the exact old temporal-regulator cancellation BEFORE interval AD.
 weak=ast.parse((ROOT/backend.WEAK).read_text());cl=next(n for n in weak.body if isinstance(n,ast.ClassDef) and n.name=='WeakAction');fn=next(n for n in cl.body if isinstance(n,ast.FunctionDef) and n.name=='density')
 temp=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='temporal' for t in n.targets))
 assert ast.unparse(temp.value)=="-p['b'] * zh * (c * ps + gamma * q[8] * d[12])"
 temp.value=ast.parse("p['b']*q[13]**2/2-p['b']*hi[2][2]*d[13]*d[12]-p['b']*q[13]*hi[2][2]*(Nz/N)*d[12]",mode='eval').body
 ds=dict(mp=mp);exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<exact-combined-clock-regulator>','exec'),ds);density=types.MethodType(ds['density'],action.core)
 tree=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate');profile=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 pc=compile(ast.fix_missing_locations(ast.Module(body=[profile],type_ignores=[])),'<pinned-prepared-profiles>','exec')
 sc=dict(mp=engine,e=J(iv.mpf(1)/1000),beta=J(iv.mpf(2)/5));exec(pc,sc)
 numerical=json.loads((ROOT/NUMERICAL).read_text())['results'][-1];co=json.loads((ROOT/ROOT_RECEIPT).read_text())['parity_center_coefficients']
 radius=iv.mpf(1139)/100000000
 def state(z,uncertain):
  pr=sc['profiles'](z);shift=[];shiftz=[]
  for row in co:
   a=J(0);b=J(0)
   for n in range(1,17):
    a+=J(row[2*n-2])*j.trig(n*z,True)+J(row[2*n-1])*j.trig(n*z)
    b+=n*(-J(row[2*n-2])*j.trig(n*z)+J(row[2*n-1])*j.trig(n*z,True))
   if uncertain:
    a+=J(coefficients=[iv.mpf([-1,1])*radius]*2);b+=J(coefficients=[iv.mpf([-1,1])*radius]*2)
   shift.append(a);shiftz.append(b)
  H=J(numerical['H']);omega=J(numerical['omega'])
  if uncertain:H+=J(iv.mpf([-1,1])*radius);omega+=J(iv.mpf([-1,1])*radius)
  v=[J(0) for _ in range(14)];ht=H+pr['lamdot']
  for i in (0,3,5):v[i]=2*ht*pr['q'][i]
  for i in range(3):v[6+i]=(pr['vt'][i]-ht*pr['vv'][i])/pr['scale']
  v[9]=pr['ud'];v[10]=omega+pr['vd'];v[11]=pr['rd'];v[12]=pr['psd']
  return pr['q'][:14]+v+pr['dz'][:14]+shift+shiftz
 beta=mp.mpf(2)/5
 def lifted(y):
  n=(-beta*y[12]).exp();nz=-beta*n*y[40]
  return y[:14]+[0,0]+y[14:28]+[1,0]+y[28:42]+[0,0]+y[42:45]+y[45:48]+[n,nz]
 def second_at(z,uncertain):
  values=state(z,uncertain);vars=[D.var(v,i) for i,v in enumerate(values)];result=density(lifted(vars))[0]
  return values,result,lastY[0]
 def hj(L,i,k):return L.h.get((min(i,k),max(i,k)),J(0))
 # One outward enclosure of the whole circle; perturbation modes are not truncated.
 whole=J.variable(iv.mpf([0,hi(2*iv.pi)]));vals,L,Y=second_at(whole,True)
 check('strict_rest_gradient_domain_whole_circle',lo(Y.c.c[0])>0,mp.nstr(lo(Y.c.c[0]),40))
 records=[];finite=True
 for ij,x in sorted(L.h.items()):
  for v in x.c:finite=finite and mp.isfinite(lo(v)) and mp.isfinite(hi(v)) and lo(v)<=hi(v)
  records.append(dict(ij=list(ij),value=binary(x.c[0]),dz=binary(x.c[1])))
 check('all_mixed_value_and_spatial_derivative_enclosures_finite',finite,len(records)*2)
 check('auxiliary_momentum_and_velocity_Hessian_exact_zero',L.g.get(27,J(0))==0 and all(hj(L,27,k)==0 for k in range(48)))
 check('other_momenta_independent_of_auxiliary_field_and_gradient',all(hj(L,14+i,k)==0 for i in range(13) for k in (13,41)))
 rhs=[]
 for i in range(14):
  value=L.g.get(i,J(0)).c[0]-L.g.get(28+i,J(0)).c[1]
  value-=sum((hj(L,14+i,k).c[0]*vals[14+k].c[0]+hj(L,14+i,28+k).c[0]*vals[14+k].c[1] for k in range(14)),iv.mpf(0))
  rhs.append(value)
 check('initial_affine_Euler_forcing_enclosures_finite',all(mp.isfinite(lo(x)) and mp.isfinite(hi(x)) for x in rhs))
 check('auxiliary_Euler_constraint_enclosure_contains_zero',lo(rhs[13])<=0<=hi(rhs[13]))
 # Original uncombined density controls have no stable-norm or forward-AD rewrite.
 originalpar={k:mp.mpf(int(v.p))/int(v.q) for k,v in exact.items()};original=backend.ClockGaugeAction('R-tau',originalpar,physical=True)
 nr=dict(mp=mp,e=mp.mpf(1)/1000,beta=beta);exec(pc,nr)
 def numeric_state(z):
  p=nr['profiles'](z);v=[mp.mpf(0)]*14;ht=mp.mpf(numerical['H'])+p['lamdot']
  for i in (0,3,5):v[i]=2*ht*p['q'][i]
  for i in range(3):v[6+i]=(p['vt'][i]-ht*p['vv'][i])/p['scale']
  v[9]=p['ud'];v[10]=mp.mpf(numerical['omega'])+p['vd'];v[11]=p['rd'];v[12]=p['psd']
  S=[sum(mp.mpf(row[2*n-2])*mp.cos(n*z)+mp.mpf(row[2*n-1])*mp.sin(n*z) for n in range(1,17)) for row in co]
  Sz=[sum(n*(-mp.mpf(row[2*n-2])*mp.sin(n*z)+mp.mpf(row[2*n-1])*mp.cos(n*z)) for n in range(1,17)) for row in co]
  return p['q'][:14]+v+p['dz'][:14]+S+Sz
 def phi(y):
  n=mp.exp(-beta*y[12]);return y[:14]+[0,0]+y[14:28]+[1,0]+y[28:42]+[0,0]+y[42:48]+[n,-beta*n*y[40]]
 def full_gradient(a):
  tape=original.body.Tape();nodes=[tape.var(x) for x in a];l=original.density(nodes)[0];return original.body.val(l),mp.matrix(tape.grad(l,nodes))
 controls=[]
 for zs in ('0.3','1.1','2.4'):
  z=mp.mpf(zs);values,lp,yp=second_at(J.variable(iv.mpf(z)),False);y=numeric_state(z);a=phi(y);ln,gn=full_gradient(a)
  jac=mp.zeros(56,48)
  for base,offset,count in ((0,0,14),(16,14,14),(32,28,14),(48,42,6)):
   for i in range(count):jac[base+i,offset+i]=1
  jac[54,12]=-beta*a[54];jac[55,12]=-beta*a[55];jac[55,40]=-beta*a[54]
  curvature=mp.zeros(48);curvature[12,12]=beta*beta*(a[54]*gn[54]+a[55]*gn[55]);curvature[12,40]=curvature[40,12]=beta*beta*a[54]*gn[55]
  check('omitted_lapse_second_pullback_rejected_'+zs,max(abs(x) for x in curvature)>mp.mpf('1e-12'))
  check('original_density_point_contained_'+zs,lo(lp.c.c[0])-mp.mpf('1e-40')<=ln<=hi(lp.c.c[0])+mp.mpf('1e-40'))
  gp=jac.T*gn;gok=all(lo(lp.g.get(i,J(0)).c[0])-mp.mpf('1e-40')<=gp[i]<=hi(lp.g.get(i,J(0)).c[0])+mp.mpf('1e-40') for i in range(48))
  check('original_full_gradient_pullback_contained_'+zs,gok)
  errors=[]
  for hs,tol in (('1e-18','1e-24'),('1e-24','1e-32')):
   step=mp.mpf(hs);err=mp.mpf(0);ok=True
   for col in range(48):
    aa=[v+mp.j*step*jac[i,col] for i,v in enumerate(a)];_,gg=full_gradient(aa);column=jac.T*mp.matrix([mp.im(v)/step for v in gg])+curvature[:,col]
    for row,x in enumerate(column):
     enclosure=hj(lp,row,col).c[0];distance=max(lo(enclosure)-x,x-hi(enclosure),mp.mpf(0));err=max(err,distance);ok=ok and distance<mp.mpf(tol)
   check('original_full_Hessian_pullback_'+zs+'_'+hs,ok,mp.nstr(err,40));errors.append(mp.nstr(err,45))
  drift=max(max(abs(lo(hj(lp,14+i,28+k).c[1]+hj(lp,14+k,28+i).c[1])),abs(hi(hj(lp,14+i,28+k).c[1]+hj(lp,14+k,28+i).c[1]))) for i in range(14) for k in range(14))
  check('actual_variable_coefficient_spatial_drift_nonzero_'+zs,drift>mp.mpf('1e-12'),mp.nstr(drift,40))
  controls.append(dict(z=zs,Hessian_distance_errors=errors,spatial_drift_size=mp.nstr(drift,45),lapse_curvature_size=mp.nstr(max(abs(x) for x in curvature),45)))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_MIXED_OPERATOR_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  jet_layout='q14,v14,d14,S3,Sz3; N=exp(-beta psi), Nz=-beta N psi_z; dust positive-clock branch',
  enclosure_domain='entire 2pi circle, all certified roots and their C2 shift uncertainty; fixed prepared fields only',
  full_mixed_Hessian_upper_triangle=records,implicit_other_entries='symmetric completion; missing upper entries exactly zero',
  rest_gradient_squared_lower=binary(Y.c.c[0]),initial_affine_forcing=[binary(x) for x in rhs],controls=controls,
  canonical_momentum_variation='delta pi=A delta q+M delta v+B partial_z delta q+C delta S+D partial_z delta S',
  canonical_two_form=dict(qq_constant='A-A^T+(B^T)_z',qq_derivative='B+B^T',qv='M',qS='C+D partial_z',other_blocks='negative formal adjoints; remaining diagonal blocks zero'),
  initial_Euler='M qddot+C Sdot+D partial_z Sdot= L_q-partial_z L_d-A v-B partial_z v',
  full_physical_symplectic_quotient='NOT_DERIVED',initial_accelerations='NOT_SOLVED',future_gauge_and_constraint_persistence=False,
  nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
