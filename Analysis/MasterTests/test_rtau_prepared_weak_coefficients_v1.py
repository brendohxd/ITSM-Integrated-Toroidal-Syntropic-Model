"""Actual initial-slice bounds plus independent full-metric local controls."""
from pathlib import Path
import argparse,hashlib,json,math
import mpmath as mp
import sympy as s
from r4c1_auxiliary_time_jets_v1 import calculate

ROOT=Path(__file__).resolve().parents[2]
NUM='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
GAUGE='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
SPEC='Theory/Gates/RES-001/RES001_RTAU_PREPARED_WEAK_COEFFICIENTS_V1_SPEC_2026-11-02.md'
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_PREPARED_WEAK_COEFFICIENTS_V1_CONTRACT_2026-11-02.md'


def run():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 checks=[]
 def check(name,ok):checks.append(dict(name=name,passed=bool(ok)))
 inherited=json.loads((ROOT/MANIFEST).read_text())['source_sha256']
 assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in inherited.items())
 n=json.loads((ROOT/NUM).read_text())['results'][-1]
 num,den=n['H'].as_integer_ratio();center=iv.mpf(num)/den
 r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000;radius=iv.mpf(1139)/100000000
 hi=lambda x:mp.mpf(x._mpi_[1]);lo=lambda x:mp.mpf(x._mpi_[0])
 binary=lambda x:[list(t) for t in x._mpi_]
 H=center+iv.mpf([-1,1])*radius
 M=iv.mpf(max(abs(lo(H)),abs(hi(H))))+eps/31;D=2*eps/31;E=iv.exp(2*r)
 bnd=json.loads((ROOT/GAUGE).read_text())['bounds']
 def interval(x):return iv.mpf([mp.mpf(tuple(t)) for t in x])
 j=iv.mpf(lo(interval(bnd['J_lower_binary'])))
 W=iv.mpf(hi(interval(bnd['drift_upper_binary'])))
 P=iv.mpf(hi(interval(bnd['drift_derivative_upper_binary'])))
 assert lo(j)>0
 old=dict(a=E,a_z=2*E*r,a_zz=E*(4*r*r+2*r),b=E*r,b_z=E*(r+2*r*r),a_t=2*E*M,b_t=E*(D+2*M*r))
 new=dict(a=iv.mpf(1),a_z=iv.mpf(0),a_zz=iv.mpf(0),b=2*r/j,b_z=2*(r+r*r)/j**2,a_t=2*M,b_t=2/j*(D+P*r+W*r+2*M*r))
 old['K_v']=E*(1+8*r+6*r*r);new['K_v']=1+2*r/j+2*(r+r*r)/j**2
 check('old_K_matches_full_coefficient_sum',lo(old['K_v'])<=hi(old['a']+2*old['a_z']+old['a_zz']+old['b']+old['b_z']) and hi(old['K_v'])>=lo(old['a']+2*old['a_z']+old['a_zz']+old['b']+old['b_z']))
 check('bounds_finite_nonnegative',all(mp.isfinite(hi(x)) and lo(x)>=0 for d in (old,new) for x in d.values()))
 check('nonzero_clock_mean_retained',lo(M)>0 and lo(new['a_t'])>0)
 # Independent full-metric coefficient extraction. Coordinate profiles are
 # rational fixtures, distinct from the analytic trigonometric bound proof.
 z=s.symbols('z');at=s.Rational(1,7);g=1+z*z/10;A=s.Rational(7,6)
 w=(1+z+z*z)/20;m=s.Rational(4,5);ell=s.diff(g,z)/g
 L=m+s.diff(w,z)+ell*w;J=g/A;a=g**-2
 oldh=g*g*s.eye(3);oldht=2*L*oldh
 newh=s.diag(g*g,g*g,A*A);newht=s.diag(2*g*g*(L-w*ell),2*g*g*(L-w*ell),2*A*A*m)
 for label,h,ht,der,u,refs in [
  ('old',oldh,oldht,lambda x:s.diff(x,z),z,[-2*a*L,a*(s.diff(L,z)-2*L*ell)]),
  ('prepared',newh,newht,lambda x:s.diff(x,z)/J,s.integrate(J,z),
   [-2*m/A**2,2/A**2/J*(s.diff(L,z)-s.diff(w,z)*ell-w*s.diff(ell,z)-2*m*ell)])]:
  def jets(x,order):
   out=[]
   for k in range(order+1):
    out.append(x.subs(z,at));x=der(x)
   return out
  x=u-u.subs(z,at)
  first=calculate(jets(h,3),jets(ht,3),jets(x,4),[0]*5)
  second=calculate(jets(h,3),jets(ht,3),jets(x*x/2,4),[0]*5)
  check(label+'_a_t_full_metric',s.simplify(second['Zt'][0]+refs[0].subs(z,at))==0)
  check(label+'_b_t_full_metric',s.simplify(first['Zt'][0]+refs[1].subs(z,at))==0)
  af=a if label=='old' else 1/A**2
  bf=a*ell if label=='old' else 2/A**2*ell/J
  check(label+'_a_value_full_metric',s.simplify(second['Z'][0]+s.sympify(af).subs(z,at))==0)
  check(label+'_b_z_full_metric',s.simplify(first['Z'][1]+der(bf).subs(z,at))==0)
 drift=2/A**2/J*(s.diff(w,z)*ell+w*s.diff(ell,z))
 check('omitted_drift_rejected',s.simplify(drift.subs(z,at))!=0)
 check('frozen_mean_rejected',-2*m/A**2!=0)
 paths=[Path(__file__).resolve(),ROOT/NUM,ROOT/GAUGE,ROOT/INVERSE,ROOT/MANIFEST,ROOT/SPEC,ROOT/CONTRACT,Path(__file__).with_name('r4c1_auxiliary_time_jets_v1.py')]
 return dict(scope='ACTUAL_INITIAL_BACKGROUND_COEFFICIENT_BOUNDS_ONLY',physics_pass=False,physical_norm='NOT_DERIVED',
  finite_time_estimate=False,checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),
  root_radius=binary(radius),H_interval=binary(H),original_bounds={k:binary(v) for k,v in old.items()},
  prepared_bounds={k:binary(v) for k,v in new.items()},
  upper_display={label:{k:mp.nstr(hi(v),16) for k,v in d.items()} for label,d in [('original',old),('prepared',new)]},
  original_volume=[binary(iv.exp(-3*r)),binary(iv.exp(3*r))],prepared_volume=[binary(iv.exp(-2*r)),binary(iv.exp(3*r))],
  source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 d=run();payload=(json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True,exist_ok=True)
  with a.output.open('xb') as f:f.write(payload)
 else:assert a.verify.read_bytes()==payload
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[t for t in d['checks'] if not t['passed']],'bounds':d['upper_display']},indent=2))
 raise SystemExit(0 if d['passed']==d['total'] else 1)
