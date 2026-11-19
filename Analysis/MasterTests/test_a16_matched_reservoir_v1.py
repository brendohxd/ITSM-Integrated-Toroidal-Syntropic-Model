"""Matched retained values, two explicit compensations, actual map drift."""
from pathlib import Path
import sys,argparse,hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_remainder_v1 as old
PINS='Theory/Gates/RES-001/RES001_A16_MATCHED_RESERVOIR_V1_INPUTS_2026-11-16.json'
DATA='Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
 data=json.loads((ROOT/DATA).read_text());imp=lambda k:old.parent.import_matrix(data[k],bg.sy)
 L,F,O=[imp(n) for n in ['full_generator','full_field_reconstruction','actual_dust_observable']]
 E=s.zeros(20,12)
 for off,col in [(0,0),(10,6)]:
  E[off,col]=E[off+2,col]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,col+j]=1
 rad=u*u+v*v;alpha=F[0,:]
 configs=[(F[7,:]+F[9,:])/2,F[10,:],2*u*F[13,:]+2*v*F[14,:],(-v*F[13,:]+u*F[14,:])/rad,F[15,:],F[16,:]]
 brates=[None,None,2*u*ud+2*v*vd,(u*vd-v*ud)/rad,rd,pd]
 rows=[]
 for i,q in enumerate(configs):
  qd=bg.dt(q)+q*L
  if i>=2:qd-=brates[i]*alpha
  rows.append(qd)
 Q=s.Matrix.vstack(*(configs+rows));Qdot=bg.dt(Q);B=bg.dt(O)+O*L
 previous=json.loads((ROOT/'Analysis/MasterTests/outputs/a16_scalar_state_v1_20261116/receipt.json').read_text())
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 checks={};results=[]
 def clean(m):return m.applyfunc(s.cancel)
 def zero(name,m):checks[name]=all(s.simplify(x)==0 for x in m)
 for mode in [4,8,16,32,64]:
  point={**init,bg.ell:mode};ev=lambda m:clean(m.subs(point))
  q=ev(Q*E);qi=DM.from_Matrix(q,extension=True).to_field().inv().to_Matrix()
  observe=clean(ev(O*E)*qi);rate=clean(ev(B*E)*qi)
  generator=clean(ev((Qdot+Q*L)*E)*qi)
  prior=next(x for x in previous['results'] if x['ell']==mode)
  zero(f'{mode}_inherited_dust_map',observe-s.Matrix([[s.sympify(x) for x in row] for row in prior['dust_map']]))
  zero(f'{mode}_inherited_generator',generator-s.Matrix([[s.sympify(x) for x in row] for row in prior['generator']]))
  zero(f'{mode}_dust_velocity_is_retained_frame',observe[1,:]-s.eye(12)[1,:])
  records=[]
  for name,index in [('reservoir_configuration',4),('reservoir_normalized_rate',10)]:
   preps=[]
   for comp_label,comp in [('metric_area_rate',6),('condensate_phase_rate',9)]:
    assert observe[0,comp]!=0,'Declared compensation unavailable'
    y=s.zeros(12,1);y[index]=1;y[comp]=s.cancel(-observe[0,index]/observe[0,comp]);x=clean(E*qi*y)
    zero(f'{mode}_{index}_{comp}_full_state_reconstruction',ev(Q)*x-y)
    zero(f'{mode}_{index}_{comp}_matched_dust',observe*y)
    zero(f'{mode}_{index}_{comp}_force_values',y.extract([5,11],[0]))
    zero(f'{mode}_{index}_{comp}_direct_rate_map',ev(B)*x-rate*y)
    preps.append({'compensation':comp_label,'coefficient':str(y[comp]),'state_values':[str(z) for z in y],'full_initial_direction':[str(z) for z in x],'dust_rate':[str(z) for z in clean(rate*y)]})
   ym,yp=[s.Matrix([s.sympify(x) for x in p['state_values']]) for p in preps]
   difference=ym-yp;delta=clean(rate*difference)
   zero(f'{mode}_{index}_same_reservoir_values',difference.extract([4,10],[0]))
   zero(f'{mode}_{index}_difference_preserves_matched_dust',observe*difference)
   direct=clean(s.Matrix([s.sympify(x) for x in preps[0]['dust_rate']])-s.Matrix([s.sympify(x) for x in preps[1]['dust_rate']]))
   zero(f'{mode}_{index}_compensation_difference_explains_response',direct-delta)
   unit=s.eye(12)[:,index];checks[f'{mode}_{index}_uncompensated_input_changes_dust']=any(s.simplify(z)!=0 for z in observe*unit)
   records.append({'reservoir_input':name,'preparations':preps,'compensation_rate_difference':[str(z) for z in delta],'responses_identical':all(s.simplify(z)==0 for z in delta)})
  drift=clean(rate-observe*generator)
  checks[f'{mode}_observation_drift_nonzero']=any(s.simplify(z)!=0 for z in drift)
  results.append({'ell':mode,'records':records,'physical_state_dust_rate_map':[[str(x) for x in r] for r in rate.tolist()],'physical_observation_drift':[[str(x) for x in r] for r in drift.tolist()]})
  print(json.dumps({'ell':mode,'identical':[r['responses_identical'] for r in records],'differences':[r['compensation_rate_difference'] for r in records]}),flush=True)
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 receipt={'status':'PASS_MATCHED_INITIAL_PREPARATION_COMPARISON','checks':checks,'inputs':pins,'results':results,'physics_pass':False,'review':'DEFERRED','gate_effect':'NONE','scope':'Two declared linear initial compensation prescriptions; no gauge-invariant isolated reservoir source, finite-time response, bath or entropy law.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(receipt,sort_keys=True,indent=2)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
