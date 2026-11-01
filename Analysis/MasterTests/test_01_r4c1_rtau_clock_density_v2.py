"""Higher root jets and direct local reconstructed-clock comparison.

Centre diagnostics and continuum interval certificates are explicitly distinct.
"""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_clock_flux_v1_attempt_01/summary.json'
INITIAL='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
PRINCIPAL='Analysis/MasterTests/outputs/r4c1_rtau_nonlinear_constraints_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
CLOCK_SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_clock_flux_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_CLOCK_DENSITY_V1_CONTRACT_2026-11-01.md'
FACTORY='Analysis/MasterTests/r4c1_prepared_operator_factory_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='471748908020df864be786a073a29b5e5dd94a187456ed6686b9d0a5996ead4a'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,PARENT,CONTRACT,FACTORY,'Analysis/MasterTests/test_01_r4c1_rtau_clock_density_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v1_attempt_01/failure.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_CLOCK_DENSITY_V2_SPEC_2026-11-01.md'):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(v) for v in x._mpi_]
 ab=lambda x:max(abs(lo(x)),abs(hi(x)))
 def interval(pair):
  a,b=(mp.mpf(tuple(x)) for x in pair);assert mp.isfinite(a) and mp.isfinite(b) and a<=b;return iv.mpf([a,b])
 def norm(v):return iv.sqrt(sum((iv.mpf(ab(x))**2 for x in v),iv.mpf(0)))
 sp=importlib.util.spec_from_file_location('clock_density_higher_factory',ROOT/FACTORY);factory=importlib.util.module_from_spec(sp);sp.loader.exec_module(factory);env=factory.prepare(order=2)
 J=env['J'];j=env['j'];D=env['D'];density=env['density'];profiles=env['sc']['profiles'];hm=env['hm']
 eps=J(iv.mpf(1)/1000);beta=mp.mpf(2)/5;radius=iv.mpf(1139)/100000000
 # Independent analytic check of the new nested spatial second coefficient.
 x=D.var(J.variable(iv.mpf(6)/5),0);test=x.exp()*x*x
 expected=iv.exp(iv.mpf(6)/5)*((iv.mpf(6)/5)**2+8*(iv.mpf(6)/5)+12)
 check('nested_Hessian_second_spatial_coefficient',lo(2*test.h[0,0].c[2])<=hi(expected) and hi(2*test.h[0,0].c[2])>=lo(expected))
 numerical=json.loads((ROOT/NUMERICAL).read_text())['results'][-1];co=json.loads((ROOT/INVERSE).read_text())['parity_center_coefficients']
 def state(theta,uncertain,third=None):
  pr=profiles(theta);S=[];Sz=[];centre_third=[];box=iv.mpf([-1,1])*radius
  for row in co:
   a=J(0);b=J(0)
   for n in range(1,17):
    a+=J(row[2*n-2])*j.trig(n*theta,True)+J(row[2*n-1])*j.trig(n*theta)
    b+=n*(-J(row[2*n-2])*j.trig(n*theta)+J(row[2*n-1])*j.trig(n*theta,True))
   centre_third.append(2*b.c[2])
   if uncertain:
    assert third is not None
    a+=J(coefficients=[box,box,box/2]);b+=J(coefficients=[box,box,iv.mpf(0)])
   if third is not None:b.c[2]=iv.mpf(third[len(S)])/2
   S.append(a);Sz.append(b)
  H=J(numerical['H']);omega=J(numerical['omega'])
  if uncertain:H+=J(box);omega+=J(box)
  ht=H+pr['lamdot'];v=[J(0) for _ in range(14)]
  for k in (0,3,5):v[k]=2*ht*pr['q'][k]
  for k in range(3):v[6+k]=(pr['vt'][k]-ht*pr['vv'][k])/pr['scale']
  v[9]=pr['ud'];v[10]=omega+pr['vd'];v[11]=pr['rd'];v[12]=pr['psd']
  ell=-eps*j.trig(theta)/13;pvz=-3*eps*j.trig(3*theta)/47;pvzz=-9*eps*j.trig(3*theta,True)/47;htz=-2*eps*j.trig(2*theta)/31
  v[13]=-2*ht*pr['q'][13]-(pvzz+ell*pvz+htz*pr['dz'][12])/pr['q'][0]
  return pr['q'][:14]+v+pr['dz'][:14]+S+Sz,centre_third
 def lifted(y,raw=False):
  n=y[48] if raw else (-beta*y[12]).exp();nz=y[49] if raw else -beta*n*y[40]
  return y[:14]+[0,0]+y[14:28]+[1,0]+y[28:42]+[0,0]+y[42:48]+[n,nz]
 def evaluate(y,raw=False):
  if raw:
   n=j.exp(-beta*y[12]);y=y+[n,-beta*n*y[40]]
  return density(lifted([D.var(x,i) for i,x in enumerate(y)],raw))[0]
 def hj(L,i,k):return L.h.get((min(i,k),max(i,k)),J(0))
 def gradient(L,i):return L.g.get(i,J(0))
 def forcing(y,L):
  R=[];Rz=[]
  for i in range(13):
   r=gradient(L,i).c[0]-gradient(L,28+i).c[1];rz=gradient(L,i).c[1]-2*gradient(L,28+i).c[2]
   for k in range(14):
    a=hj(L,14+i,k);b=hj(L,14+i,28+k);v=y[14+k]
    r-=a.c[0]*v.c[0]+b.c[0]*v.c[1]
    rz-=a.c[1]*v.c[0]+a.c[0]*v.c[1]+b.c[1]*v.c[1]+b.c[0]*2*v.c[2]
   R.append(r);Rz.append(rz)
  return R,Rz
 whole=J.variable(iv.mpf([0,hi(2*iv.pi)]));y0,_=state(whole,True,[0,0,0]);L0=evaluate(y0)
 Eprime=[gradient(L0,42+i).c[1]-2*gradient(L0,45+i).c[2] for i in range(3)]
 principal=json.loads((ROOT/PRINCIPAL).read_text());kn=s.Rational(principal['shift']['minimum_singular_value_bound']);kn=iv.mpf(int(kn.p))/int(kn.q)
 psmax=iv.mpf(1)/1000*(iv.mpf(1)/29+iv.mpf(1)/31);lam=iv.mpf(1)/13000
 Kinv=iv.exp((iv.mpf(2)/5)*psmax+3*lam)/kn;thirdbound=Kinv*norm(Eprime)
 check('third_shift_derivative_bound_finite',mp.isfinite(hi(thirdbound)),mp.nstr(hi(thirdbound),40))
 thirdbox=iv.mpf([-hi(thirdbound),hi(thirdbound)])
 yg,_=state(whole,True,[thirdbox]*3);Lg=evaluate(yg);LRg=evaluate(yg,True)
 Rg,Rzg=forcing(yg,Lg);initial=json.loads((ROOT/INITIAL).read_text())
 Minv=interval(initial['bounds']['original_temporal_inverse']);A0=interval(initial['bounds']['particular_acceleration'])
 Mz=max(sum(ab(hj(Lg,14+i,14+k).c[1]) for k in range(13)) for i in range(13))
 Az=Minv*(norm(Rzg)+iv.mpf(Mz)*A0)
 check('particular_acceleration_derivative_bound_finite',mp.isfinite(hi(Az)),mp.nstr(hi(Az),40))
 check('raw_lapse_flux_independent_of_auxiliary_acceleration',hj(LRg,49,27)==0 and all(hj(Lg,14+i,27)==0 for i in range(14)))
 # Reuse the frozen explicit-current equation, with this caller's higher jets.
 tree=ast.parse((ROOT/CLOCK_SOURCE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate');ff=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='flux')
 current=[None];ns=dict(mp=mp,J=J,j=j,betaJ=J(beta),bJ=J(iv.mpf(5)/11),eJ=eps,state=lambda theta,uncertain:current[0])
 exec(compile(ast.fix_missing_locations(ast.Module(body=[ff],type_ignores=[])),'<pinned-clock-current-equation>','exec'),ns)
 def tensor(q):return [[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
 def lie(q,d,S,Sz):
  h=tensor(q);out=[]
  for k,(a,b) in enumerate(hm):out.append(S[2]*d[k]+(sum(h[a][i]*Sz[i] for i in range(3)) if b==2 else 0)+(sum(h[b][i]*Sz[i] for i in range(3)) if a==2 else 0))
  out += [S[2]*d[6+i]-q[8]*Sz[i] for i in range(3)]
  out += [S[2]*d[i] for i in range(9,14)]
  return out
 def generators(y):
  z=J(0);A=[[z for _ in range(3)] for _ in range(13)];B=[[z for _ in range(3)] for _ in range(13)];h=tensor(y[:14])
  for i in range(13):A[i][2]=y[28+i]
  for k,(a,b) in enumerate(hm):
   for col in range(3):B[k][col]=(h[a][col] if b==2 else z)+(h[b][col] if a==2 else z)
  for k in range(3):B[6+k][k]=-y[8]
  return A,B
 def balance(theta,y,L,LR,acc,accz,T=None,Tz=None,Tzz=None):
  T=T or [iv.mpf(0)]*3;Tz=Tz or [iv.mpf(0)]*3;Tzz=Tzz or [iv.mpf(0)]*3
  q=y[:14];v=y[14:28];dq=y[28:42];S=y[42:45];Sz=y[45:48];n=j.exp(-beta*q[12]);nz=-beta*n*dq[12]
  pi=[gradient(L,14+i) for i in range(14)];Rvel=[x-a for x,a in zip(v,lie(q,dq,S,Sz))]
  Ihat=L.c-sum((x*a for x,a in zip(pi,Rvel)),J(0));BN=n*gradient(LR,49)
  v0=[x.c[0] for x in v];vz=[x.c[1] for x in v];vzz=[2*x.c[2] for x in v]
  acc=list(acc)+[iv.mpf(0)];accz=list(accz)+[iv.mpf(0)]
  pit=[]
  for i in range(14):
   t=sum((hj(L,14+i,k).c[0]*v0[k]+hj(L,14+i,14+k).c[0]*acc[k]+hj(L,14+i,28+k).c[0]*vz[k] for k in range(14)),iv.mpf(0))
   t+=sum((hj(L,14+i,42+k).c[0]*T[k]+hj(L,14+i,45+k).c[0]*Tz[k] for k in range(3)),iv.mpf(0));pit.append(t)
  lieSv=lie(v0,vz,[x.c[0] for x in S],[x.c[0] for x in Sz]);lieTq=lie([x.c[0] for x in q],[x.c[0] for x in dq],T,Tz)
  It=sum((gradient(L,i).c[0]*v0[i]+gradient(L,28+i).c[0]*vz[i]-pit[i]*Rvel[i].c[0]+pi[i].c[0]*(lieSv[i]+lieTq[i]) for i in range(14)),iv.mpf(0))
  It+=sum((gradient(L,42+k).c[0]*T[k]+gradient(L,45+k).c[0]*Tz[k] for k in range(3)),iv.mpf(0))
  ndot=-beta*n*v[12];nzdot=-beta*(ndot*dq[12]+n*(-3*eps*j.trig(3*theta)/47))
  Q=iv.mpf(0);Qz=iv.mpf(0)
  def add(coef,a,az):
   nonlocal Q,Qz
   Q+=coef.c[0]*a;Qz+=coef.c[1]*a+coef.c[0]*az
  for k in range(14):
   add(hj(LR,49,k),v0[k],vz[k]);add(hj(LR,49,14+k),acc[k],accz[k]);add(hj(LR,49,28+k),vz[k],vzz[k])
  for k in range(3):add(hj(LR,49,42+k),T[k],Tz[k]);add(hj(LR,49,45+k),Tz[k],Tzz[k])
  add(hj(LR,49,48),ndot.c[0],ndot.c[1]);add(hj(LR,49,49),nzdot.c[0],nzdot.c[1])
  PN=gradient(LR,49);BTz=ndot.c[1]*PN.c[0]+ndot.c[0]*PN.c[1]+n.c[1]*Q+n.c[0]*Qz
  Idensity=Ihat.c[0]-BN.c[1];Idensity_z=Ihat.c[1]-2*BN.c[2];Idensity_t=It-BTz
  current[0]=y;Fs,Etau=ns['flux'](theta,False);regflux_z=Etau*(n*q[0]**mp.mpf('1.5')).c[0]
  transport=Idensity_z*S[2].c[0]+Idensity*Sz[2].c[0]
  return dict(residual=Idensity_t-transport-regflux_z,without_regulator=Idensity_t-transport,without_lapse_improvement=It-(Ihat.c[1]*S[2].c[0]+Ihat.c[0]*Sz[2].c[0])-regflux_z,
   density_time=Idensity_t,regulator_flux_derivative=regflux_z,density=Idensity)
 allbox=[iv.mpf([-hi(A0),hi(A0)])]*13;zbox=[iv.mpf([-hi(Az),hi(Az)])]*13
 bg=balance(whole,yg,Lg,LRg,allbox,zbox)
 check('whole_root_clock_residual_enclosure_finite',all(mp.isfinite(lo(v)) and mp.isfinite(hi(v)) and lo(v)<=hi(v) for v in bg.values()))
 check('whole_root_residual_contains_zero_without_precision_claim',lo(bg['residual'])<=0<=hi(bg['residual']))
 def solve(M,R):
  mid=lambda x:(lo(x)+hi(x))/2;mm=mp.matrix([[mid(x) for x in row] for row in M]);rr=mp.matrix([mid(x) for x in R]);x=mp.lu_solve(mm,rr)
  xi=[iv.mpf(mp.nstr(v,75)) for v in x];r=[R[i]-sum((M[i][k]*xi[k] for k in range(13)),iv.mpf(0)) for i in range(13)];error=Minv*norm(r)
  return [iv.mpf([lo(v)-hi(error),hi(v)+hi(error)]) for v in xi],error
 points=[];omission_rejected=False
 for zs in ('0.3','1.1','2.4'):
  theta=J.variable(iv.mpf(zs));y,third=state(theta,False);L=evaluate(y);LR=evaluate(y,True);R,Rz=forcing(y,L)
  M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)];acc,ae=solve(M,R)
  accz,aze=solve(M,[Rz[i]-sum((hj(L,14+i,14+k).c[1]*acc[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
  check('validated_particular_and_derivative_inverse_'+zs,hi(ae)<mp.mpf('1e-35') and hi(aze)<mp.mpf('1e-35'))
  ybase,_=state(theta,False,[0,0,0]);Lbase=evaluate(ybase);actual=[gradient(L,42+i).c[1]-2*gradient(L,45+i).c[2] for i in range(3)]
  predicted=[gradient(Lbase,42+i).c[1]-2*gradient(Lbase,45+i).c[2]-sum((hj(Lbase,45+i,45+k).c[0]*third[k] for k in range(3)),iv.mpf(0)) for i in range(3)]
  check('highest_shift_jet_affine_extraction_'+zs,max(ab(a-b) for a,b in zip(actual,predicted))<mp.mpf('1e-35'))
  # Independent raw/clock gradient chain rule at the actual centre.
  n=j.exp(-beta*y[12]);nz=-beta*n*y[40]
  chainq=gradient(LR,12)-beta*n*gradient(LR,48)-beta*nz*gradient(LR,49)
  chaind=gradient(LR,40)-beta*n*gradient(LR,49)
  check('independent_lapse_gradient_pullback_'+zs,ab((gradient(L,12)-chainq).c[0])<mp.mpf('1e-35') and ab((gradient(L,40)-chaind).c[0])<mp.mpf('1e-35'))
  b=balance(theta,y,L,LR,acc,accz);check('direct_local_clock_density_comparison_'+zs,ab(b['residual'])<mp.mpf('1e-8'),mp.nstr(ab(b['residual']),40))
  omission_rejected=omission_rejected or lo(b['without_regulator'])>mp.mpf('1e-8') or hi(b['without_regulator'])<-mp.mpf('1e-8')
  T=[iv.mpf(2)/37,-iv.mpf(1)/41,iv.mpf(1)/43];Tz=[iv.mpf(1)/47,iv.mpf(2)/53,-iv.mpf(1)/59];Tzz=[-iv.mpf(1)/61,iv.mpf(2)/67,-iv.mpf(1)/71]
  D0,D1=generators(y)
  ac=[acc[i]+sum((D0[i][k].c[0]*T[k]+D1[i][k].c[0]*Tz[k] for k in range(3)),iv.mpf(0)) for i in range(13)]
  acz=[accz[i]+sum((D0[i][k].c[1]*T[k]+D0[i][k].c[0]*Tz[k]+D1[i][k].c[1]*Tz[k]+D1[i][k].c[0]*Tzz[k] for k in range(3)),iv.mpf(0)) for i in range(13)]
  shifted=balance(theta,y,L,LR,ac,acz,T,Tz,Tzz)
  check('paired_nonzero_gauge_drift_density_time_invariance_'+zs,ab(shifted['density_time']-b['density_time'])<mp.mpf('1e-30'))
  points.append(dict(z=zs,clock={k:binary(v) for k,v in b.items()},inverse_error=binary(ae),derivative_inverse_error=binary(aze),centre_momentum_derivative_defect=[binary(v) for v in actual]))
 check('omitted_regulator_source_rejected',omission_rejected)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CLOCK_DENSITY_V2',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  whole_circle_third_shift_bound=binary(thirdbound),shift_principal_inverse_bound=binary(Kinv),highest_jet_forcing=[binary(v) for v in Eprime],
  whole_circle_particular_acceleration_derivative_bound=binary(Az),whole_root_clock={k:binary(v) for k,v in bg.items()},point_controls=points,
  root_third_jet='derived from differentiated momentum ODE; not Fourier truncation',centre_comparison_tolerance='1e-8',continuum_local_clock_certificate=False,
  raw_lapse_density='Ihat-partial_z(N L_Nz)',actual_auxiliary_Zdot_retained=True,auxiliary_Zddot_used=False,
  sharp_final_gauge_quadrature='NOT_COMPUTED',physical_symplectic_quotient='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,
  review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
