"""Deterministic elimination identity plus actual exported forcing support."""
from pathlib import Path
import argparse,hashlib,json
import sympy as S
ROOT=Path(__file__).resolve().parents[2]
PINS='Theory/Gates/RES-001/RES001_A16_HISTORY_MAP_V1_INPUTS_2026-11-15.json'
FORM='Analysis/MasterTests/outputs/r4c1_g3n5_dust_remainder_attempt_01/formulas.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for p,h in pins.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 t,s=S.symbols('t s',real=True)
 # det P=1, noncommuting time-dependent J=P'P^-1.
 P=S.Matrix([[1,t],[t*t,1+t**3]]);Ps=P.subs(t,s);J=P.diff(t)*P.inv();U=P*Ps.inv()
 source=S.Matrix([[1,t],[t*t,2]]);q=S.Matrix([1+t,t*t]);c0=S.Matrix([2,-1])
 integral=(Ps.inv()*source.subs(t,s)*q.subs(t,s)).applyfunc(lambda x:S.integrate(x,(s,0,t)))
 c=P*(c0+integral);R=S.Matrix([[1,t*t],[-t,2]])
 hist=(R*U*source.subs(t,s)*q.subs(t,s)).applyfunc(lambda x:S.integrate(S.expand(x),(s,0,t)))
 forcing=R*P*c0
 checks={}
 def zero(n,x):checks[n]=all(S.simplify(y)==0 for y in x)
 def different(n,x):checks[n]=any(S.simplify(y)!=0 for y in x)
 zero('fundamental_time_derivative',U.diff(t)-J*U)
 zero('fundamental_coincident_identity',U.subs(s,t)-S.eye(2))
 zero('fundamental_initial_identity',U.subs(t,0).subs(s,0)-S.eye(2))
 zero('complement_ode_with_source',c.diff(t)-J*c-source*q)
 zero('complement_initial_data',c.subs(t,0)-c0)
 zero('memory_plus_initial_forcing',R*c-forcing-hist)
 different('reject_dropped_initial_force',forcing)
 different('reject_dropped_history_feedback',hist)
 different('reject_reversed_endpoint_order',(U-Ps*P.inv()).subs({t:S.Rational(1,3),s:S.Rational(1,7)}))
 different('noncommuting_generator_fixture',J.subs(t,1)*J.subs(t,2)-J.subs(t,2)*J.subs(t,1))
 different('reject_frozen_coefficient_drift',U.diff(t)-J.subs(t,0)*U)
 # Independent scalar integrating-factor control: J=2t, source=0.
 scalar=S.exp(t*t);checks['scalar_homogeneous_initial_force']=S.simplify(S.diff(scalar,t)-2*t*scalar)==0 and scalar.subs(t,0)==1
 f=json.loads((ROOT/FORM).read_text());export=f['matrices']['complementary_forcing_R']
 assert export['shape']==[2,20]
 groups={'metric_scalar':[0,10],'tensor_chart':[1,2,11,12],'longitudinal_frame':[3,13],'transverse_frame':[4,5,14,15],'condensate_amplitudes':[6,7,16,17],'reservoir_amplitude':[8,18],'mixed_force_coordinate':[9,19]}
 active={}
 for name,cols in groups.items():
  active[name]=[{'row':e['row'],'column':e['column']} for e in export['entries'] if e['column'] in cols and S.simplify(sum(S.sympify(x) for x in e['terms']))!=0]
 checks['support_groups_cover_original_chart']=sorted(sum(groups.values(),[]))==list(range(20))
 checks['reservoir_amplitude_present']=bool(active['reservoir_amplitude'])
 checks['multiple_other_direct_channels']=all(bool(active[n]) for n in ['metric_scalar','longitudinal_frame','condensate_amplitudes','mixed_force_coordinate'])
 entry=next(e for e in export['entries'] if e['row']==0 and e['column']==8)
 a,rd,ell=S.symbols('a r_dot ell');expr=sum(S.sympify(x) for x in entry['terms'])
 checks['explicit_reservoir_position_entry']=S.simplify(expr+15*S.I*a*a*rd/(ell*ell))==0
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 data={'status':'PASS_DETERMINISTIC_HISTORY_IDENTITY_AND_CHART_SUPPORT','checks':checks,'inputs':pins,'direct_chart_support':active,'reservoir_position_entry':str(expr),'physical_kernel_numerically_evaluated':False,'reservoir_identity_established':False,'physics_pass':False,'review':'DEFERRED','gate_effect':'NONE','scope':'Exact noncommuting algebra fixture and actual saved R support; not physical kernel normalization, time-domain error certification or sector attribution.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(data,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode())
 print(json.dumps({'passed':sum(checks.values()),'checks':len(checks),'active_groups':[k for k,v in active.items() if v],'physics_pass':False}))
if __name__=='__main__':main()
