"""Initial canonical momentum/current-density inverse on its compatible range.

No physical evolution estimate or canonical adoption is asserted.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_canonical_density_graph_v2_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_CONTRACT_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='0cb96db2f86ead50721f7e0bb87aacfa262c189b905f0fbd46677ed47acfcf1c'
 pins=dict(json.loads((ROOT/PARENT).read_text())['source_sha256']);snap={}
 for rel in (SELF,PARENT,FACTORY,CONTRACT):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);ab=lambda x:max(abs(lo(x)),abs(hi(x)))
 binary=lambda x:[list(v) for v in x._mpi_]
 interval=lambda pair:iv.mpf([mp.mpf(tuple(v)) for v in pair])
 sp=importlib.util.spec_from_file_location('coupled_inverse_factory',ROOT/FACTORY);fac=importlib.util.module_from_spec(sp);sp.loader.exec_module(fac);env=fac.prepare()
 par=env['env']['env']['exact'];H2=s.Rational(3469,4620);H=s.sqrt(H2);pi=-s.Rational(11,10)*H
 ts=s.Rational(1,2)*(1+s.Rational(1,16)+par['K_Q']/25)
 pot=par['m2']/2+par['lambda4']/8+par['lambda6']/(24*par['Lambda']**2)+par['mr2']/2+par['lambda_r']/4+par['g_r']/4+par['rho_Lambda']
 rho=s.simplify(s.Rational(33,10)*H2-ts-pot)
 check('same_action_reference_clock_density',rho==s.Rational(1,5))
 f=s.symbols('f');vol=1+f
 def ham(pzz):
  xx=[pi*(1+f),pi*(1+f),pzz];tm=2*(sum(x*x for x in xx)-s.Rational(16,33)*sum(xx)**2)/vol
  return -tm-ts/vol-vol*pot
 Cn=s.simplify(s.diff(ham(pi*(1+f)),f).subs(f,0));Cm=s.simplify(s.diff(ham(pi),f).subs(f,0));r0=2*H
 check('coupled_reference_nonzero_coefficient',Cn==s.Rational(553,400),str(Cn))
 check('reference_mean_coefficient_retained_and_nonzero',Cm==-s.Rational(2263,8400),str(Cm))
 check('omitted_longitudinal_momentum_changes_operator',s.simplify(Cn-Cm)==s.Rational(3469,2100))
 R0=1/abs(Cm)
 check('all_fourier_reference_L2_to_H2_inverse',Cn>1 and R0>1 and s.simplify(Cn-Cm+r0*pi)==0,str(R0))
 # Independent symbolic derivation of the weighted longitudinal equation.
 z=s.symbols('z');aa,pt,ff,pp,src=[s.Function(t)(z) for t in ('a','pt','f','pc','src')]
 lam=s.diff(aa,z)/aa;R=aa*(lam*pt-s.diff(pt,z))/2
 lhs=s.diff(2*aa*aa*pp,z)-s.diff(aa*aa,z)*pp-pt*s.diff(aa*aa*ff,z)-src
 rhs=2*aa*(s.diff(aa*pp-aa*pt*ff/2,z)-R*ff-src/(2*aa))
 check('exact_longitudinal_integrating_factor',s.expand(lhs-rhs)==0)
 def coefficients(ctx,y,L):
  J=ctx['J'];D=ctx['D'];grad=ctx['gradient'];geometry=ctx['geometry'];lie=ctx['lie'];b=ctx['b']
  q=y[:14];d=y[28:42];v=y[14:28];S=y[42:45];Sz=y[45:48];p=[grad(L,14+i) for i in range(14)]
  a2=q[0];a=a2**mp.mpf('.5');n,_,_,_,_=geometry(q,d)
  az=J(coefficients=[a2.c[1],2*a2.c[2],iv.mpf(0)])
  def variation(dq,dd):
   qq=[D(x,{0:t}) for x,t in zip(q,dq)];ddd=[D(x,{0:t}) for x,t in zip(d,dd)]
   nn,vv,gg,hh,flux=geometry(qq,ddd)
   F=sum((nn*gg*hh[i][2]*D(p[6+i]) for i in range(3)),D(0))-nn*flux/2-b*nn*vv*qq[13]*hh[2][2]*ddd[12]
   return F.g.get(0,J(0))
  dq=[J(0) for _ in range(14)];dd=[J(0) for _ in range(14)]
  for i in (0,3):dq[i]=a2;dd[i]=az
  U0=variation(dq,dd)
  for i in (0,3):dq[i]=J(0);dd[i]=a2
  U1=variation(dq,dd)
  PT=p[0]+p[3]
  V0=a2*(grad(L,0)+grad(L,3))+az*(grad(L,28)+grad(L,31))+PT*S[2]*az+a2*(p[2]*Sz[0]+p[4]*Sz[1])
  V1=a2*(grad(L,28)+grad(L,31)+PT*S[2])
  A0=V0.c[0]-U0.c[1];A1=V1.c[0]-U0.c[0]-U1.c[1];A2=-U1.c[0]
  rv=[x-t for x,t in zip(v,lie(q,d,S,Sz))]
  return dict(A0=A0,A1=A1,A2=A2,PT=PT,p=p,rv=rv,n=n,a=a,trace_principal_defect=A2+(n*a).c[0])
 # Only values/first spatial coefficients enter. The unused highest shift
 # jet is not a C3-error assertion and is never used as physical initial data.
 J=env['J'];whole=J.variable(iv.mpf([0,hi(2*iv.pi)]));y,_=env['state'](whole,True,[0,0,0]);L=env['evaluate'](y);co=coefficients(env,y,L)
 check('whole_root_trace_principal_enclosures_consistent',lo(co['trace_principal_defect'])<=0<=hi(co['trace_principal_defect']))
 h0=iv.sqrt(iv.mpf(3469)/4620);p0=-iv.mpf(11)/10*h0;rref=2*h0
 lmax=iv.mpf(1)/13000;w0max=iv.exp(lmax);wmax=iv.exp(2*lmax);contrast=wmax-1
 PT=co['PT'];a=co['a'];a2=y[0];lambda_z=a2.c[1]/(2*a2.c[0]);RR=a.c[0]*(lambda_z*PT.c[0]-PT.c[1])/2
 dP=iv.mpf(ab(PT.c[0]/2-p0));Rmax=iv.mpf(ab(RR))
 Terr=(1+wmax)*(dP+w0max*Rmax)+abs(p0)*contrast
 tx=iv.mpf(ab(co['p'][2].c[0]))*(1+iv.exp(4*lmax));ty=iv.mpf(ab(co['p'][4].c[0]))*(1+iv.exp(4*lmax))
 d2=iv.mpf(ab(co['A2']+1));d1=iv.mpf(ab(co['A1']));d0=iv.mpf(ab(co['A0']-iv.mpf(int(Cm.p))/int(Cm.q)))
 dr=iv.mpf(ab(co['rv'][5].c[0]-rref));rzmax=iv.mpf(ab(co['rv'][5].c[0]));rx=iv.mpf(ab(co['rv'][2].c[0]));ry=iv.mpf(ab(co['rv'][4].c[0]))
 error=d2+d1/2+d0+rx*tx+ry*ty+rzmax*Terr+dr*abs(p0)
 reference_inverse=iv.mpf(int(R0.p))/int(R0.q);contraction=reference_inverse*error
 check('whole_root_coupled_periodic_inverse_contraction',hi(contraction)<1,mp.nstr(hi(contraction),40))
 inverse_bound=reference_inverse/(1-contraction) if hi(contraction)<1 else None
 # The range retains the exact weighted compatibility; transverse means
 # are physical data. No finite Fourier or parity restriction is adopted.
 check('reference_mean_block_not_replaced_by_positive_mass',Cm<0 and Cn>0)
 controls=[]
 for zs in ('0.3','1.1','2.4'):
  ctx=fac.point(zs);Jp=ctx['J'];yy=ctx['y'];LL=ctx['L'];cc=coefficients(ctx,yy,LL);pc=[iv.mpf(1)/37,-iv.mpf(1)/41,iv.mpf(1)/43]
  for index in range(3):
   fj=[iv.mpf(0),iv.mpf(0),iv.mpf(0)];fj[index]=iv.mpf(1);fjet=Jp(coefficients=[fj[0],fj[1],fj[2]/2]);qvar=yy[0]*fjet
   dq=[Jp(0) for _ in range(14)];dd=[Jp(0) for _ in range(14)]
   for i in (0,3):dq[i]=qvar;dd[i]=Jp(coefficients=[qvar.c[1],2*qvar.c[2],iv.mpf(0)])
   lz=yy[0].c[1]/(2*yy[0].c[0]);pt=cc['PT'];px=cc['p'][2];py=cc['p'][4]
   slopes=[-2*lz*pc[0]-px.c[1]*fj[0]-px.c[0]*fj[1]-2*lz*px.c[0]*fj[0],-2*lz*pc[1]-py.c[1]*fj[0]-py.c[0]*fj[1]-2*lz*py.c[0]*fj[0],-lz*pc[2]+pt.c[0]*fj[1]/2+lz*pt.c[0]*fj[0]]
   dp=[Jp(0) for _ in range(14)]
   for slot,value,slope in zip((2,4,5),pc,slopes):dp[slot]=Jp(coefficients=[value,slope,iv.mpf(0)])
   result=ctx['run_probe']('coupled_trace_basis_'+str(index),dq,dd,dp,[Jp(0)]*3,[Jp(0)]*3)
   prediction=cc['A0']*fj[0]+cc['A1']*fj[1]+cc['A2']*fj[2]-sum((cc['rv'][slot].c[0]*value for slot,value in zip((2,4,5),pc)),iv.mpf(0))
   defect=interval(result['density'])-prediction
   check('direct_coupled_trace_row_'+zs+'_'+str(index),ab(defect)<mp.mpf('1e-28'),mp.nstr(ab(defect),40))
   actual_momentum=[]
   for i in range(3):
    fixed=sum((ctx['Bq'][k][i]*dp[k] for k in range(14)),Jp(0)).c[1]
    if i==2:fixed-=sum((dp[k]*yy[28+k] for k in range(14)),Jp(0)).c[0]
    actual_momentum.append(interval(result['momentum_omitted_geometry'][i])+fixed)
   check('direct_completed_momentum_equations_'+zs+'_'+str(index),max(ab(t) for t in actual_momentum)<mp.mpf('1e-28'))
   controls.append(dict(z=zs,basis=index,density_defect=binary(defect),completed_momentum=[binary(v) for v in actual_momentum]))
  check('inherited_point_inverse_and_graph_controls_'+zs,all(c['passed'] is True for c in ctx['checks']))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  reference_nonzero_mass=str(Cn),reference_mean_mass=str(Cm),reference_inverse_L2_H2=str(R0),
  whole_root_trace_coefficients={k:binary(co[k]) for k in ('A0','A1','A2')},
  bounds={k:binary(v) for k,v in dict(trace_second=d2,trace_first=d1,trace_zeroth=d0,transverse_x=tx,transverse_y=ty,longitudinal_difference=Terr,longitudinal_integrating_factor=Rmax,operator_perturbation=error,inverse_contraction=contraction).items()},
  coupled_inverse_L2_H2_bound=binary(inverse_bound) if inverse_bound is not None else None,point_controls=controls,
  range='projected momentum and density inverse, with exact longitudinal weighted mean compatibility; U1 tangent solved separately, clock input integral fixed; all three eliminated momentum means retained',
  nontrivial_range_example='even physical tensor-cross configuration cos(nz), every n>=1, with even current-density source; parity makes longitudinal compatibility odd; no parity restriction adopted',
  physical_symplectic_quotient='NOT_DERIVED',variable_coefficient_evolution_norm='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
