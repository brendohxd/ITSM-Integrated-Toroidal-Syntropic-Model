"""Reference omission counterexamples and continuum endpoint reconstruction."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_v2_attempt_01/summary.json'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_VELOCITY_TANGENT_AUDIT_V1_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='f4efb6bc588528aa6287fa2cca2a8020f581fddc0564e0336b9e8bf52906a814'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256']);snap={}
 for p in (SELF,SPEC,PARENT):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 def interval(pair):
  lo,hi=(mp.mpf(tuple(x)) for x in pair);assert mp.isfinite(lo) and mp.isfinite(hi) and lo<=hi;return iv.mpf([lo,hi])
 bounds={k:interval(v) for k,v in d['bounds'].items()};cells=[interval(x['rate_difference']) for x in d['cell_root_rate_bounds']]
 check('all_cell_and_aggregate_interval_pairs_finite_ordered',len(cells)==32 and len(bounds)==10)
 dc=iv.sqrt(bounds['momentum_operator_difference']**2+bounds['clock_operator_difference']**2+bounds['U1_operator_difference']**2)
 gap=(iv.mpf(1)/20)*(1-dc**2)-6*dc-3*dc**2-bounds['energy_weighted_delta'];inverse=1/(1-dc)
 check('independent_constraint_operator_norm',mp.mpf(dc._mpi_[1])<mp.mpf('.004179'))
 check('independent_constraint_kernel_energy_lower',mp.mpf(gap._mpi_[0])>mp.mpf('.024'),mp.nstr(mp.mpf(gap._mpi_[0]),45))
 check('independent_constraint_right_inverse',mp.mpf(inverse._mpi_[1])<mp.mpf('1.004197'))
 check('recorded_bounds_agree_without_rounded_input',abs(mp.mpf(gap._mpi_[0])-mp.mpf(bounds['tangent_energy_lower']._mpi_[0]))<mp.mpf('1e-47'))
 check('root_uncertainty_distinct_from_background_departure',mp.mpf(bounds['root_rate_uncertainty']._mpi_[1])<mp.mpf('.000033') and max(mp.mpf(x._mpi_[1]) for x in cells)>mp.mpf('.003'))
 # Reference controls independent of primary code and all numerical centres.
 M=s.diag(*([1]*6+[s.Rational(1,6)]*3+[1,1,1,3]))
 for a in (0,3,5):
  for b in (0,3,5):M[a,b]-=s.Rational(16,15)
 H=s.sqrt(s.Rational(3469,4620));alpha=s.Rational(11,5)*H
 bg=s.Matrix([H,0,0,H,0,H,0,0,0,0,1,s.Rational(1,4),s.Rational(1,5)])
 qr=s.zeros(1,13);qr[10]=1;ir=-(M*bg).T
 raw=s.zeros(13,1)
 for j in (0,3,5):raw[j]=1
 energy=s.factor((raw.T*M*raw)[0]);check('omitted_mean_clock_charge_admits_negative_direction',energy<0 and (qr*raw)[0]==0 and (ir*raw)[0]!=0,str(energy))
 # Multiplying raw by cos(kz), k !=0, gives zero charge means but negative
 # averaged energy. Its nonzero-mode momentum constraint is not satisfied.
 momentum=raw[5]+16*(raw[0]+raw[3]);check('omitted_nonzero_momentum_admits_negative_direction',energy/2<0 and momentum!=0,str(energy/2))
 mean=s.zeros(13,1);mean[11]=1
 for j in (0,3,5):mean[j]=1/(12*alpha)
 check('nonzero_homogeneous_metric_reservoir_tangent_retained',(ir*mean).applyfunc(s.simplify)==s.zeros(1,1) and (qr*mean)[0]==0 and mean[0]!=0)
 check('retained_mean_tangent_energy_positive',s.factor((mean.T*M*mean)[0])>0,str(s.factor((mean.T*M*mean)[0])))
 # Generic nonzero-mode trace-difference and transverse trace coordinates.
 a,b=s.symbols('a b',real=True);v=s.zeros(13,1);v[0]=(a+b)/s.sqrt(2);v[3]=(a-b)/s.sqrt(2);v[5]=-16*s.sqrt(2)*a
 qe=s.expand((v.T*M*v)[0]);ne=s.expand((v.T*v)[0]);check('nonzero_mode_reference_gap_without_mode_cutoff',s.simplify(qe-(33*a*a+b*b))==0 and s.simplify(ne-(513*a*a+b*b))==0 and s.Rational(33,513)>s.Rational(1,20))
 check('circle_antiderivative_L2_bound',1/s.Integer(1)<=1) # Parseval multiplier 1/(ik), integers |k|>=1.
 check('projected_mean_momentum_not_claimed_solved','additional condition' in d['mean_momentum_equation'])
 holds=(d['physical_full_symplectic_operator']=='NOT_DERIVED' and d['initial_accelerations']=='NOT_DERIVED' and not d['nonlinear_time_evolution'] and not d['physics_pass'] and d['review']=='DEFERRED' and d['G1_G6']=='INCOMPLETE')
 check('full_physical_evolution_and_review_holds_retained',holds)
 failed=json.loads((ROOT/'Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_v1_attempt_01/summary.json').read_text())
 check('failed_total_departure_precheck_preserved',failed['passed']==20 and failed['total']==21 and any(c['name']=='whole_circle_certified_root_rate_bound' and not c['passed'] for c in failed['checks']))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_VELOCITY_TANGENT_AUDIT_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  same_author_control=True,independent_external_review=False,scope='planar fixed-field constraint-tangent velocity form only',review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 a=argparse.ArgumentParser();g=a.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);p=a.parse_args();d=calculate();data=ENC(d)
 if p.replay:assert p.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  p.output_dir.mkdir(parents=True,exist_ok=False);q=p.output_dir/'summary.json';q.write_bytes(data);Path(str(q)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(q))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
