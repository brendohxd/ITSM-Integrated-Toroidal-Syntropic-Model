"""Full-metric auxiliary closure controls; no completed evolution claim."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_canonical_flow_second_jet_v2_attempt_01/summary.json'
MODULE='Analysis/MasterTests/r4c1_auxiliary_geometry_rate_v1.py'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_AUXILIARY_RATE_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 d=json.loads((ROOT/PARENT).read_text());assert d['passed']==d['total']==15;pins=dict(d['source_sha256']);snap={}
 for rel in (SELF,PARENT,MODULE,FACTORY,SPEC):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 ab=lambda x:max(abs(mp.mpf(t)) for t in x._mpi_);binary=lambda x:[list(v) for v in x._mpi_]
 aux=load('auxiliary_geometry',MODULE);ctx=load('auxiliary_background',FACTORY).prepare();J=ctx['J'];rows=[];metric_omitted=False;second_omitted=False
 for zs in ('0.3','1.1','2.4'):
  z=iv.mpf(zs);y,_=ctx['state'](J.variable(z),False);q=y[:14];d=y[28:42];v=y[14:28]
  psi4=iv.mpf(1)/1000*(iv.cos(z)/29+16*iv.cos(2*z)/31)
  dq=[J(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(14)]
  dd=[J(coefficients=[t.c[1],2*t.c[2],-t.c[1]/2]) for t in dq]
  dv=[J(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,-iv.mpf(i+1)/211]) for i in range(14)]
  dp4=iv.mpf(1)/17;out=aux.apply(ctx,q,d,psi4,v,dq,dd,dp4,dv)
  ze=max(ab((out['Z']-q[13]).c[k]) for k in range(3));te=ab(out['Zdot']-v[13].c[0])
  check('prepared_auxiliary_through_second_spatial_order_'+zs,ze<mp.mpf('1e-28'),mp.nstr(ze,40))
  check('prepared_actual_first_time_tangent_'+zs,te<mp.mpf('1e-28'),mp.nstr(te,40))
  independent=aux.independent_time_value(ctx,q,d,v)
  check('independent_inverse_metric_time_formula_'+zs,ab(out['Zdot']-independent)<mp.mpf('1e-28'))
  defects=[]
  for hs,tol in (('1e-12','1e-20'),('1e-16','1e-28')):
   h=mp.mpf(hs);qp=[a+h*b for a,b in zip(q,dq)];qm=[a-h*b for a,b in zip(q,dq)];dp=[a+h*b for a,b in zip(d,dd)];dm=[a-h*b for a,b in zip(d,dd)];vp=[a+h*b for a,b in zip(v,dv)];vm=[a-h*b for a,b in zip(v,dv)]
   numericZ=(-aux.laplacian(ctx,qp,dp,psi4+h*dp4)+aux.laplacian(ctx,qm,dm,psi4-h*dp4))/(2*h)
   numericT=(aux.independent_time_value(ctx,qp,dp,vp)-aux.independent_time_value(ctx,qm,dm,vm))/(2*h)
   err=max([ab((out['delta_Z']-numericZ).c[k]) for k in range(3)]+[ab(out['delta_Zdot']-numericT)])
   check('independent_spacetime_tangent_'+zs+'_'+hs,err<mp.mpf(tol),mp.nstr(err,40));defects.append(mp.nstr(err,40))
  hi,C=aux.coefficient(ctx,q,d);frozen=-hi[2][2].c[0]*2*dv[12].c[2]-C.c[0]*dv[12].c[1]
  metric_omitted=metric_omitted or ab(out['delta_Zdot']-frozen)>mp.mpf('1e-10')
  bad=list(dv);bad[12]=J(coefficients=[dv[12].c[0],dv[12].c[1],iv.mpf(0)])
  dropped=aux.apply(ctx,q,d,psi4,v,dq,dd,dp4,bad)
  second_omitted=second_omitted or ab(out['delta_Zdot']-dropped['delta_Zdot'])>mp.mpf('1e-10')
  check('unsupported_time_spatial_derivatives_not_fabricated_'+zs,out['time_spatial_jet']=='NOT_RETURNED')
  rows.append(dict(z=zs,Z=[binary(t) for t in out['Z'].c],delta_Z=[binary(t) for t in out['delta_Z'].c],Zdot=binary(out['Zdot']),delta_Zdot=binary(out['delta_Zdot']),finite_difference_defects=defects))
 check('omitted_metric_time_terms_rejected',metric_omitted);check('omitted_force_velocity_second_derivative_rejected',second_omitted)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_AUXILIARY_RATE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,point_controls=rows,scope='full metric auxiliary spatial jet and rate value for explicitly supplied field-rate jets',gauge_closed=False,current_density_closed=False,complete_prepared_evolution=False,physical_norm='NOT_DERIVED',review='DEFERRED',physics_pass=False,gate_effect='NONE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
