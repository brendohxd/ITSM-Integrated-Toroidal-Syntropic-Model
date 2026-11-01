"""Prepared full canonical momentum/charge tangents and local density map.

No full periodic physical inverse or evolution estimate is asserted.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_prepared_principal_audit_v2_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_clock_density_operator_factory_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V1_CONTRACT_2026-11-01.md'
INITIAL='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='d168acacc483ed9026fab18b80702675b92349b0c68d92388bcf05f020bae345'
 pins=dict(json.loads((ROOT/PARENT).read_text())['source_sha256']);snap={}
 for p in (SELF,PARENT,FACTORY,CONTRACT,INITIAL,'Analysis/MasterTests/test_01_r4c1_rtau_canonical_density_graph_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_canonical_density_graph_v1_attempt_01/failure.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_SPEC_2026-11-01.md'):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  f=ROOT/rel;sc=Path(str(f)+'.sha256');assert SHA(f.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for p in (f,sc):snap[p]=(SHA(p.read_bytes()),p.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);ab=lambda x:max(abs(lo(x)),abs(hi(x)));mid=lambda x:(lo(x)+hi(x))/2
 binary=lambda x:[list(v) for v in x._mpi_]
 interval=lambda pair:iv.mpf([mp.mpf(tuple(x)) for x in pair])
 norm=lambda xs:iv.sqrt(sum((iv.mpf(ab(x))**2 for x in xs),iv.mpf(0)))
 sp=importlib.util.spec_from_file_location('canonical_density_factory',ROOT/FACTORY);factory=importlib.util.module_from_spec(sp);sp.loader.exec_module(factory);env=factory.prepare()
 J=env['J'];D=env['D'];j=env['j'];state=env['state'];evaluate=env['evaluate'];gradient=env['gradient'];hj=env['hj'];lie=env['lie'];hm=env['hm']
 beta=mp.mpf(2)/5;b=mp.mpf(5)/11;tol=mp.mpf('1e-28');Z=iv.mpf(0)
 Minv=interval(json.loads((ROOT/INITIAL).read_text())['bounds']['original_temporal_inverse'])
 def geometry(q,d):
  h=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]];dh=[[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]
  det=h[0][0]*(h[1][1]*h[2][2]-h[1][2]*h[2][1])-h[0][1]*(h[1][0]*h[2][2]-h[1][2]*h[2][0])+h[0][2]*(h[1][0]*h[2][1]-h[1][1]*h[2][0])
  inv=[[((h[(k+1)%3][(i+1)%3]*h[(k+2)%3][(i+2)%3]-h[(k+1)%3][(i+2)%3]*h[(k+2)%3][(i+1)%3]))/det for k in range(3)] for i in range(3)]
  vol=det**mp.mpf('.5');gamma=(1+sum((q[6+i]*h[i][k]*q[6+k] for i in range(3) for k in range(3)),q[0]*0))**mp.mpf('.5')
  n=(-beta*q[12]).exp() if isinstance(q[12],D) else j.exp(-beta*q[12])
  G=[[[sum((inv[k][l]*((dh[l][jj] if ii==2 else 0)+(dh[l][ii] if jj==2 else 0)-(dh[ii][jj] if l==2 else 0))/2 for l in range(3)),q[0]*0) for jj in range(3)] for ii in range(3)] for k in range(3)]
  flux=vol*(sum((inv[ii][jj]*G[2][ii][jj] for ii in range(3) for jj in range(3)),q[0]*0)-sum((inv[ii][2]*G[jj][ii][jj] for ii in range(3) for jj in range(3)),q[0]*0))
  return n,vol,gamma,inv,flux
 # Independent exact IBP check: lapse-gradient and Z-gradient terms cancel.
 x=s.symbols('x');nf,vf,hf,zf,pf=[s.Function(t)(x) for t in ('n','v','h','Z','psi')];bb=s.symbols('b')
 reg=bb*nf*vf*zf*zf/2-bb*nf*vf*hf*s.diff(zf,x)*s.diff(pf,x)-bb*vf*zf*hf*s.diff(nf,x)*s.diff(pf,x)
 bn=-bb*nf*vf*zf*hf*s.diff(pf,x)
 target=bb*nf*vf*(zf*zf/2+zf*s.diff(vf*hf*s.diff(pf,x),x)/vf)
 check('exact_regulator_lapse_improvement_cancellation',s.expand(reg-s.diff(bn,x)-target)==0)
 zz,lap=s.symbols('Z lap');on=-bb*lap*lap/2
 check('auxiliary_on_shell_energy_and_first_variation',s.expand((bb*(zz*zz/2+zz*lap)).subs(zz,-lap)-on)==0 and s.diff(bb*(zz*zz/2+zz*lap),zz).subs(zz,-lap)==0)
 # Fixed profiles give exact all-root leading trace ellipticity.
 psmax=iv.mpf(1)/1000*(iv.mpf(1)/29+iv.mpf(1)/31);ell=iv.mpf(1)/13000
 trace_bound=iv.exp(iv.mpf([-1,1])*(iv.mpf(2)/5*psmax+ell))
 check('whole_initial_root_trace_principal_coefficient_nonsingular',lo(trace_bound)>0,binary(trace_bound))
 records=[];omitted_improvement=False;omitted_geometry=False
 for zs in ('0.3','1.1','2.4'):
  theta=J.variable(iv.mpf(zs));y,_=state(theta,False);L=evaluate(y);LR=evaluate(y,True)
  q=y[:14];d=y[28:42];v=y[14:28];S=y[42:45];Sz=y[45:48];pi=[gradient(L,14+i) for i in range(14)]
  n,vol,gamma,hinv,flux=geometry(q,d);PN=gradient(LR,49)
  PNcan=sum((gamma*hinv[i][2]*pi[6+i] for i in range(3)),J(0))-flux/2-b*vol*q[13]*hinv[2][2]*d[12]
  pndef=max(ab((PN-PNcan).c[i]) for i in (0,1))
  check('raw_lapse_gradient_equals_canonical_flux_'+zs,pndef<tol,mp.nstr(pndef,40))
  # Exact canonical local shift generators and their field variations.
  def Bmatrix(qq):
   hh=[[qq[0],qq[1],qq[2]],[qq[1],qq[3],qq[4]],[qq[2],qq[4],qq[5]]];out=[[J(0) for _ in range(3)] for _ in range(14)]
   for k,(aa,bb) in enumerate(hm):
    for i in range(3):out[k][i]=(hh[aa][i] if bb==2 else J(0))+(hh[bb][i] if aa==2 else J(0))
   for i in range(3):out[6+i][i]=-qq[8]
   return out
  Bq=Bmatrix(q);rv=[a-c for a,c in zip(v,lie(q,d,S,Sz))]
  M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
  Mz=[[hj(L,14+i,14+k).c[1] for k in range(13)] for i in range(13)]
  def solve(rhs):
   ans=mp.lu_solve(mp.matrix([[mid(x) for x in row] for row in M]),mp.matrix([mid(x) for x in rhs]));xx=[iv.mpf(mp.nstr(t,75)) for t in ans]
   err=Minv*norm([rhs[i]-sum((M[i][k]*xx[k] for k in range(13)),Z) for i in range(13)])
   return [iv.mpf([lo(x)-hi(err),hi(x)+hi(err)]) for x in xx],err
  def run_probe(label,dq,dd,dp,w,wz):
   rhs=[dp[i]-sum((hj(L,14+i,k)*dq[k]+hj(L,14+i,28+k)*dd[k] for k in range(14)),J(0))-sum((hj(L,14+i,42+k)*w[k]+hj(L,14+i,45+k)*wz[k] for k in range(3)),J(0)) for i in range(13)]
   dv0,e0=solve([x.c[0] for x in rhs]);dv1,e1=solve([rhs[i].c[1]-sum((Mz[i][k]*dv0[k] for k in range(13)),Z) for i in range(13)])
   dv=[J(coefficients=[a,c,Z]) for a,c in zip(dv0,dv1)]+[J(0)];dy=dq+dv+dd+w+wz
   dpc=[sum((hj(L,14+i,k)*dy[k] for k in range(48)),J(0)) for i in range(14)]
   residual=max(ab((dpc[i]-dp[i]).c[k]) for i in range(14) for k in (0,1))
   check('canonical_rate_inverse_'+zs+'_'+label,hi(e0)<mp.mpf('1e-35') and hi(e1)<mp.mpf('1e-35') and residual<mp.mpf('1e-35'),mp.nstr(max(hi(e0),hi(e1),residual),40))
   dn=-beta*n*dq[12];nz=-beta*n*d[12];dnz=-beta*(n*dd[12]+nz*dq[12]);draw=dy+[dn,dnz]
   dBNraw=dn*PN+n*sum((hj(LR,49,k)*draw[k] for k in range(50)),J(0))
   qq=[D(t,{0:a}) for t,a in zip(q,dq)];ddd=[D(t,{0:a}) for t,a in zip(d,dd)]
   nn,vv,gg,hh,ff=geometry(qq,ddd)
   rawcoef=[nn*gg*hh[i][2] for i in range(3)]
   fieldpart=sum((rawcoef[i]*D(pi[6+i]) for i in range(3)),D(0))-nn*ff/2-b*nn*vv*qq[13]*hh[2][2]*ddd[12]
   dBNcan=fieldpart.g.get(0,J(0))+sum((n*gamma*hinv[i][2]*dpc[6+i] for i in range(3)),J(0))
   lie_delta=lie(dq,dd,S,Sz);lie_w=lie(q,d,w,wz)
   dihat=sum((gradient(L,k)*dy[k] for k in range(48)),J(0))-sum((dpc[i]*rv[i]+pi[i]*(dv[i]-lie_delta[i]-lie_w[i]) for i in range(14)),J(0))
   direct=dihat.c[0]-dBNraw.c[1]
   canonical=-sum((rv[i]*dpc[i] for i in range(14)),J(0))+sum((gradient(L,i)*dq[i]+gradient(L,28+i)*dd[i]+pi[i]*lie_delta[i] for i in range(14)),J(0))
   expected=canonical.c[0]-dBNcan.c[1]
   check('full_canonical_local_density_'+zs+'_'+label,ab(direct-expected)<tol,mp.nstr(ab(direct-expected),40))
   dB=Bmatrix(dq);mom=[];short=[]
   for i in range(3):
    fluxp=sum((Bq[k][i]*dpc[k]+dB[k][i]*pi[k] for k in range(14)),J(0))
    value=fluxp.c[1]-(sum((dpc[k]*d[k]+pi[k]*dd[k] for k in range(14)),J(0)).c[0] if i==2 else Z)
    directmom=sum((hj(L,42+i,k)*dy[k] for k in range(48)),J(0)).c[0]-sum((hj(L,45+i,k)*dy[k] for k in range(48)),J(0)).c[1]
    mom.append(directmom-value)
    fixed_field=sum((Bq[k][i]*dpc[k] for k in range(14)),J(0)).c[1]
    if i==2:fixed_field-=sum((dpc[k]*d[k] for k in range(14)),J(0)).c[0]
    short.append(directmom-fixed_field)
   check('full_field_momentum_tangent_'+zs+'_'+label,max(ab(x) for x in mom)<tol,mp.nstr(max(ab(x) for x in mom),40))
   # Local phase-charge variation includes the field-dependent generator.
   dqcharge=q[9]*dpc[10]-q[10]*dpc[9]+pi[10]*dq[9]-pi[9]*dq[10]
   return dict(label=label,density=binary(direct),without_improvement=binary(dihat.c[0]),momentum_omitted_geometry=[binary(t) for t in short],phase_charge_variation=binary(dqcharge.c[0]))
  def zeros(n):return [J(0) for _ in range(n)]
  probes=[]
  # Full jet control: every field, momentum, both real parities and nonzero shift.
  dq=[J(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(14)]
  dd=[J(coefficients=[t.c[1],2*t.c[2],-t.c[1]/2]) for t in dq]
  dp=[J(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,Z]) for i in range(13)]+[J(0)]
  w=[J(coefficients=[iv.mpf(i+1)/113,-iv.mpf(i+2)/127,iv.mpf(i+1)/226]) for i in range(3)];wz=[J(coefficients=[t.c[1],2*t.c[2],Z]) for t in w]
  row=run_probe('all_fields_momenta_and_shift',dq,dd,dp,w,wz);probes.append(row)
  omitted_geometry=omitted_geometry or any(lo(interval(v))>mp.mpf('1e-12') or hi(interval(v))<-mp.mpf('1e-12') for v in row['momentum_omitted_geometry'])
  for label,slots,expected in (('trace_second_derivative',[0,3],-n/q[0]**mp.mpf('.5')),('force_second_derivative',[12],b*n*vol*q[13]*hinv[2][2])):
   dq=zeros(14);dd=zeros(14)
   for i in slots:dq[i]=J(coefficients=[Z,Z,iv.mpf(1)/2]);dd[i]=J(coefficients=[Z,iv.mpf(1),Z])
   row=run_probe(label,dq,dd,zeros(14),zeros(3),zeros(3));probes.append(row)
   check('physical_density_principal_'+zs+'_'+label,ab(interval(row['density'])-expected.c[0])<tol,mp.nstr(ab(interval(row['density'])-expected.c[0]),40))
   if label=='trace_second_derivative':omitted_improvement=omitted_improvement or ab(interval(row['density'])-interval(row['without_improvement']))>mp.mpf('.9')
  for axis in range(3):
   dp=zeros(14);dp[6+axis]=J(coefficients=[Z,iv.mpf(1),Z]);row=run_probe('frame_momentum_derivative_'+str(axis),zeros(14),zeros(14),dp,zeros(3),zeros(3));probes.append(row)
   expected=-n*gamma*hinv[axis][2]
   check('physical_density_frame_momentum_coefficient_'+zs+'_'+str(axis),ab(interval(row['density'])-expected.c[0])<tol)
  dq=zeros(14);dd=zeros(14);dq[13]=J(coefficients=[iv.mpf(1),iv.mpf(2),iv.mpf(3)]);dd[13]=J(coefficients=[iv.mpf(2),iv.mpf(6),Z])
  row=run_probe('independent_auxiliary_field',dq,dd,zeros(14),zeros(3),zeros(3));probes.append(row)
  check('auxiliary_first_density_variation_cancels_on_secondary_'+zs,ab(interval(row['density']))<tol)
  records.append(dict(z=zs,lapse_gradient_identity_defect=mp.nstr(pndef,40),probes=probes))
 check('omitted_local_lapse_improvement_rejected',omitted_improvement)
 check('omitted_field_dependent_momentum_generator_rejected',omitted_geometry)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,point_controls=records,
  whole_initial_trace_coefficient_magnitude=binary(trace_bound),local_density_highest_derivatives='-N*MP2/(2a)*(dhxx_zz+dhyy_zz)-N*gamma/a^2*dpVz_z+b*N*a*Z*dpsi_zz',
  momentum_tangent='(B^T*dp+dB^T*p)_z-e_z*(dp.q_z+p.dq_z)',phase_tangent='u*dp_v-v*dp_u+p_v*du-p_u*dv',clock_tangent='integral(dI_density); improvement integrates to zero on periodic torus',
  full_periodic_trace_inverse='NOT_DERIVED',physical_symplectic_quotient='NOT_DERIVED',variable_coefficient_physical_norm='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
