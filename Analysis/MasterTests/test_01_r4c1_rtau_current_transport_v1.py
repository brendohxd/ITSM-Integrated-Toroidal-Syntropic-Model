"""Action clock row and actual canonical charge/constraint transport controls."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,traceback
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_gauge_velocity_v1_attempt_01/summary.json'
MODULE='Analysis/MasterTests/r4c1_clock_current_transport_v1.py'
FLOW='Analysis/MasterTests/r4c1_prepared_canonical_flow_v2.py'
AUX='Analysis/MasterTests/r4c1_auxiliary_geometry_rate_v1.py'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_CURRENT_TRANSPORT_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[];records=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 parent=json.loads((ROOT/PARENT).read_text());assert parent['passed']==parent['total']==18
 assert SHA((ROOT/PARENT).read_bytes())=='b04c13cdc5a26673e5f91291c43e50edfb5f4a03bf4a0f68c2a317c95d53e92b'
 pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,PARENT,MODULE,FLOW,AUX,FACTORY,SPEC):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 ab=lambda x:max(abs(mp.mpf(t)) for t in x._mpi_);binary=lambda x:[list(v) for v in x._mpi_]
 current=load('full_current_transport',MODULE);flow=load('current_canonical_flow',FLOW);aux=load('current_auxiliary_geometry',AUX)
 factory=load('current_canonical_points',FACTORY);omitted_flux=False;omitted_aux=False;defect_seen=False
 for zs in ('0.3','1.1','2.4'):
  ctx=factory.point(zs);J=ctx['J'];q=ctx['q'];d=ctx['d'];v=ctx['v'];S=ctx['S'];Sz=ctx['Sz'];p=ctx['pi'];L=ctx['L'];grad=ctx['gradient'];hj=ctx['hj'];B=ctx['Bmatrix']
  zero=lambda n:[J(0) for _ in range(n)]
  dz=lambda t:J(coefficients=[t.c[1],2*t.c[2],iv.mpf(0)])
  F=current.flux(ctx,q,d,v,S,Sz)
  ctx['env']['current'][0]=ctx['y'];old,Etau=ctx['env']['ns']['flux'](J.variable(iv.mpf(zs)),False)
  err=max(ab((F[i]-ctx['n']*ctx['vol']*old[i]).c[k]) for i in range(3) for k in (0,1))
  check('frozen_action_current_all_components_'+zs,err<mp.mpf('1e-28'),mp.nstr(err,40))
  check('frozen_action_current_divergence_'+zs,ab(F[2].c[1]-(ctx['n']*ctx['vol']).c[0]*Etau)<mp.mpf('1e-28'))
  # Spatially consistent local jets, all independent metric/frame/scalar fields.
  dq=[J(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(14)]
  dd=[J(coefficients=[t.c[1],2*t.c[2],-t.c[1]/2]) for t in dq]
  dp=[J(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,iv.mpf(i+1)/211]) for i in range(13)]+[J(0)]
  w=[J(coefficients=[iv.mpf(i+1)/113,-iv.mpf(i+2)/127,iv.mpf(i+1)/226]) for i in range(3)];wz=[dz(t) for t in w]
  rate=flow.apply(ctx,dq,dd,dp,w,wz);dv=rate['field_rate']+[J(0)]
  th=J.variable(iv.mpf(zs));e=iv.mpf(1)/1000
  psi4=(e*(ctx['j'].trig(th,True)/29+16*ctx['j'].trig(2*th,True)/31)).c[0]
  ar=aux.apply(ctx,q,d,psi4,v,dq,dd,iv.mpf(1)/17,dv)
  dq[13]=ar['delta_Z'];dd[13]=dz(dq[13])
  rate=flow.apply(ctx,dq,dd,dp,w,wz);dv=rate['field_rate']+[J(0)]
  check('auxiliary_secondary_closed_'+zs,ab(rate['auxiliary_secondary_tangent'])<mp.mpf('1e-28'))
  check('background_auxiliary_spatial_jets_'+zs,max(ab((ar['Z']-q[13]).c[k]) for k in range(3))<mp.mpf('1e-28'))
  I=J(coefficients=[iv.mpf(2)/7,iv.mpf(3)/11,iv.mpf(0)]);deltaI=J(coefficients=[iv.mpf(5)/13,-iv.mpf(7)/17,iv.mpf(0)])
  row=current.linearized(ctx,q,d,v,S,Sz,dq,dd,dv,w,wz,I,deltaI)
  for hs,limit in (('1e-12','1e-20'),('1e-16','1e-28')):
   h=iv.mpf(hs)
   fp=current.flux(ctx,*[[x+h*y for x,y in zip(xs,ys)] for xs,ys in zip((q,d,v,S,Sz),(dq,dd,dv,w,wz))])
   fm=current.flux(ctx,*[[x-h*y for x,y in zip(xs,ys)] for xs,ys in zip((q,d,v,S,Sz),(dq,dd,dv,w,wz))])
   err=max(ab(((fp[i]-fm[i])/(2*h)-row['delta_flux'][i]).c[k]) for i in range(3) for k in (0,1))
   check('full_metric_current_tangent_'+zs+'_'+hs,err<mp.mpf(limit),mp.nstr(err,40))
  sh=flow.apply(ctx,zero(14),zero(14),zero(14),w,wz)
  shifted=current.linearized(ctx,q,d,v,S,Sz,zero(14),zero(14),sh['field_rate']+[J(0)],w,wz,I,J(0))
  err=max(ab(t.c[k]) for t in shifted['delta_flux'] for k in (0,1))
  check('pure_canonical_shift_normal_current_invariance_'+zs,err<mp.mpf('1e-28'),mp.nstr(err,40))
  check('pure_shift_density_transport_'+zs,ab(shifted['density_rate']-(I*w[2]).c[1])<mp.mpf('1e-28'))
  omitted_flux=omitted_flux or ab(row['delta_flux'][2].c[1])>mp.mpf('1e-10')
  wrong=current.linearized(ctx,q,d,v,S,Sz,dq[:13]+[J(0)],dd[:13]+[J(0)],dv,w,wz,I,deltaI)
  omitted_aux=omitted_aux or ab(wrong['density_rate']-row['density_rate'])>mp.mpf('1e-10')
  # Actual EL momentum rows; only metric/frame spatial derivatives are needed.
  dy=dq+dv+dd+w+wz
  pd=[];dpd=[]
  for i in range(14):
   fq=grad(L,i);fd=grad(L,28+i)
   tf=sum((hj(L,i,k)*dy[k] for k in range(48)),J(0));tg=sum((hj(L,28+i,k)*dy[k] for k in range(48)),J(0))
   pd.append(J(coefficients=[fq.c[0]-fd.c[1],fq.c[1]-2*fd.c[2] if i<9 else iv.mpf(0),iv.mpf(0)]))
   dpd.append(J(coefficients=[tf.c[0]-tg.c[1],tf.c[1]-2*tg.c[2] if i<9 else iv.mpf(0),iv.mpf(0)]))
  check('reconstructed_auxiliary_background_EL_'+zs,ab(pd[13].c[0])<mp.mpf('1e-28'))
  check('actual_momentum_rate_composition_'+zs,max(ab(dpd[i].c[0]-rate['momentum_rate'][i]) for i in range(14))<mp.mpf('1e-28'))
  # Local U(1) Noether identity, without averaging or imposing a desired graph.
  Qdot=v[9]*p[10]+q[9]*pd[10]-v[10]*p[9]-q[10]*pd[9]
  Qflux=-q[10]*grad(L,37)+q[9]*grad(L,38)
  deltaLd=lambda i:sum((hj(L,28+i,k)*dy[k] for k in range(48)),J(0))
  dQdot=dv[9]*p[10]+v[9]*dp[10]+dq[9]*pd[10]+q[9]*dpd[10]-dv[10]*p[9]-v[10]*dp[9]-dq[10]*pd[9]-q[10]*dpd[9]
  dQflux=-dq[10]*grad(L,37)-q[10]*deltaLd(9)+dq[9]*grad(L,38)+q[9]*deltaLd(10)
  check('actual_local_U1_background_transport_'+zs,ab(Qdot.c[0]+Qflux.c[1])<mp.mpf('1e-28'))
  check('actual_local_U1_tangent_transport_'+zs,ab(dQdot.c[0]+dQflux.c[1])<mp.mpf('1e-28'))
  # C_i=(B_i^T p)' - delta_iz p.q_z, a covector density.
  Bq=B(q);Bdq=B(dq);Bv=B(v);Bdv=B(dv);C=[];dC=[];Cd=[];dCd=[]
  body=sum((p[k]*d[k] for k in range(13)),J(0));dbody=sum((dp[k]*d[k]+p[k]*dd[k] for k in range(13)),J(0))
  for i in range(3):
   f=sum((Bq[k][i]*p[k] for k in range(9)),J(0));df=sum((Bdq[k][i]*p[k]+Bq[k][i]*dp[k] for k in range(9)),J(0))
   C.append(J(coefficients=[f.c[1]-(body.c[0] if i==2 else 0),2*f.c[2]-(body.c[1] if i==2 else 0),iv.mpf(0)]))
   dC.append(J(coefficients=[df.c[1]-(dbody.c[0] if i==2 else 0),2*df.c[2]-(dbody.c[1] if i==2 else 0),iv.mpf(0)]))
   ft=sum((Bv[k][i]*p[k]+Bq[k][i]*pd[k] for k in range(9)),J(0))
   dft=sum((Bdv[k][i]*p[k]+Bv[k][i]*dp[k]+Bdq[k][i]*pd[k]+Bq[k][i]*dpd[k] for k in range(9)),J(0))
   bt=sum((pd[k]*d[k]+p[k]*dz(v[k]) for k in range(13)),J(0))
   dbt=sum((dpd[k]*d[k]+pd[k]*dd[k]+dp[k]*dz(v[k])+p[k]*dz(dv[k]) for k in range(13)),J(0))
   Cd.append(ft.c[1]-(bt.c[0] if i==2 else 0));dCd.append(dft.c[1]-(dbt.c[0] if i==2 else 0))
  def lie_constraint(c,s,sz):
   return [s[2].c[0]*c[i].c[1]+sz[2].c[0]*c[i].c[0]+(sum(c[k].c[0]*sz[k].c[0] for k in range(3)) if i==2 else 0) for i in range(3)]
  lc=lie_constraint(C,S,Sz);ldc=lie_constraint(dC,S,Sz);ldelta=lie_constraint(C,w,wz)
  err=max(ab(Cd[i]-lc[i]) for i in range(3));derr=max(ab(dCd[i]-ldc[i]-ldelta[i]) for i in range(3))
  check('actual_background_spatial_constraint_transport_'+zs,err<mp.mpf('1e-28'),mp.nstr(err,40))
  check('actual_linearized_spatial_constraint_transport_'+zs,derr<mp.mpf('1e-28'),mp.nstr(derr,40))
  defect_seen=defect_seen or max(ab(t) for t in ldelta)>mp.mpf('1e-20')
  records.append(dict(z=zs,background_constraint=[binary(t.c[0]) for t in C],delta_constraint=[binary(t.c[0]) for t in dC],current_density_rate=binary(row['density_rate']),constraint_transport_error=mp.nstr(derr,40)))
  print('POINT_COMPLETED',zs,flush=True)
 check('omitted_regulator_current_rejected',omitted_flux)
 check('omitted_auxiliary_spatial_tangent_rejected',omitted_aux)
 check('nonzero_centre_constraint_drift_retained',defect_seen)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CURRENT_TRANSPORT_V1',passed=sum(t['passed'] for t in checks),total=len(checks),checks=checks,source_sha256=pins,point_controls=records,
  density_row='delta I_dot = partial_z(S^z delta I + I delta S^z + delta mathcalF^z)',momentum_transport='delta C_dot = Lie_S delta C + Lie_deltaS C',
  scope='full-metric local clock-current row and pointwise actual canonical U1/spatial-Noether transport controls; no evolution-norm theorem',
  returned_clock_spatial_rates='VALUE_ONLY',scalar_momentum_rate_spatial_derivatives='NOT_RETURNED',physical_norm='NOT_DERIVED',controlled_time_evolution=False,physical_window_demonstrated=False,
  review='DEFERRED',physics_pass=False,canonical_parent_adopted=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args()
 try:d=calculate();data=ENC(d)
 except Exception:
  if a.output_dir:
   a.output_dir.mkdir(parents=True,exist_ok=False);data=ENC(dict(error=traceback.format_exc(),script_sha256=SHA((ROOT/SELF).read_bytes())));p=a.output_dir/'failure.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n')
  raise
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
