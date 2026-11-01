"""Prepared canonical-flow entry controls; full evolution remains incomplete."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
INPUTS='Theory/Verification/ITSM_RTAU_PREPARED_EVOLUTION_V1_INPUTS_2026-11-01.json'
FLOW='Analysis/MasterTests/r4c1_prepared_canonical_flow_v2.py'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_CANONICAL_FLOW_SECOND_JET_V2_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,rel):
 sp=importlib.util.spec_from_file_location(name,ROOT/rel);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 pins=dict(json.loads((ROOT/INPUTS).read_text())['source_sha256']);snap={}
 for rel in (SELF,INPUTS,FLOW,FACTORY,SPEC,'Analysis/MasterTests/r4c1_prepared_canonical_flow_v1.py','Analysis/MasterTests/test_01_r4c1_rtau_canonical_flow_entry_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_canonical_flow_entry_v1_attempt_01/summary.json'):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 ab=lambda x:max(abs(mp.mpf(t)) for t in x._mpi_);binary=lambda x:[list(v) for v in x._mpi_]
 fac=load('canonical_flow_point_factory',FACTORY);flow=load('prepared_canonical_flow',FLOW);rows=[];omit_flux=False;omit_drift=False
 for zs in ('0.3','1.1','2.4'):
  ctx=fac.point(zs);J=ctx['J'];L=ctx['L'];hj=ctx['hj']
  dq=[J(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(14)]
  dd=[J(coefficients=[t.c[1],2*t.c[2],-t.c[1]/2]) for t in dq]
  seed=[J(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,-iv.mpf(i+1)/211]) for i in range(13)]+[J(0)]
  ds=[J(coefficients=[iv.mpf(i+1)/113,-iv.mpf(i+2)/127,iv.mpf(i+1)/226]) for i in range(3)]
  dsz=[J(coefficients=[t.c[1],2*t.c[2],iv.mpf(0)]) for t in ds]
  dy=dq+seed+dd+ds+dsz
  dp=[sum((hj(L,14+i,k)*dy[k] for k in range(48)),J(0)) for i in range(14)]
  actual=flow.apply(ctx,dq,dd,dp,ds,dsz)
  ve=max(ab((a-b).c[k]) for a,b in zip(actual['field_rate'],seed) for k in (0,1,2))
  check('prescribed_rate_round_trip_'+zs,ve<mp.mpf('1e-28'),mp.nstr(ve,40))
  check('validated_rate_and_spatial_inverse_'+zs,max(ab(t) for t in actual['inverse_errors'])<mp.mpf('1e-35'))
  direct=[sum((hj(L,i,k)*dy[k] for k in range(48)),J(0)).c[0]-sum((hj(L,28+i,k)*dy[k] for k in range(48)),J(0)).c[1] for i in range(14)]
  pe=max(ab(a-b) for a,b in zip(actual['momentum_rate'],direct))
  check('complete_canonical_momentum_euler_rows_'+zs,pe<mp.mpf('1e-28'),mp.nstr(pe,40))
  omit_flux=omit_flux or any(mp.mpf(t._mpi_[0])>mp.mpf('1e-10') or mp.mpf(t._mpi_[1])<-mp.mpf('1e-10') for t in actual['spatial_flux'])
  omit_drift=omit_drift or any(mp.mpf(t._mpi_[0])>mp.mpf('1e-10') or mp.mpf(t._mpi_[1])<-mp.mpf('1e-10') for t in actual['coefficient_drift'])
  check('auxiliary_and_gauge_not_silently_closed_'+zs,actual['auxiliary_field_rate']=='NOT_SUPPLIED' and actual['gauge_shift']=='CALLER_SUPPLIED_NOT_SOLVED' and actual['current_density_row']=='NOT_CLOSED')
  rows.append(dict(z=zs,rate_defect=mp.nstr(ve,40),momentum_defect=mp.nstr(pe,40),momentum_rates=[binary(v) for v in actual['momentum_rate']],spatial_flux=[binary(v) for v in actual['spatial_flux']],coefficient_drift=[binary(v) for v in actual['coefficient_drift']]))
 check('omitted_spatial_euler_flux_rejected',omit_flux);check('omitted_spatial_coefficient_drift_rejected',omit_drift)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CANONICAL_FLOW_SECOND_JET_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,point_controls=rows,
  scope='unreduced canonical field/momentum entry block with caller-supplied shift; auxiliary row retained as secondary tangent',complete_prepared_evolution=False,gauge_velocity_solve='NOT_IMPLEMENTED',density_current_row='NOT_CLOSED',transport_comparison='NOT_COMPLETED',physical_norm='NOT_DERIVED',review='DEFERRED',physics_pass=False,gate_effect='NONE',goal='ACTIVE_INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
