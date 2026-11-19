"""Independent scalar-stress audit of stored original-chart preparations."""
from pathlib import Path
import argparse,json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
PINS='Theory/Gates/RES-001/RES001_A16_SCALAR_PRESSURE_V1_INPUTS_2026-11-16.json'
DATA='Analysis/MasterTests/outputs/a16_matched_current_v1_20261116/receipt.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 u,v,r=s.symbols('u v r',real=True);rad=u*u+v*v
 U=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*rad*r*r/28
 point={u:1,v:0,r:1};grad=[s.diff(U,x).subs(point) for x in [u,v,r]]
 checks={'potential_derivatives':grad==[s.Rational(2341,1680),0,s.Rational(33,14)]};results=[]
 data=json.loads((ROOT/DATA).read_text())
 for row in data['results']:
  mode=row['ell'];records=[]
  for record in row['records']:
   stress=[]
   for i,p in enumerate(record['preparations']):
    x=s.Matrix([s.sympify(z) for z in p['full_initial_direction']])
    kinetic=x[17]+x[18]/4;potential=sum(c*x[j] for c,j in zip(grad,[6,7,8]));energy=s.simplify(kinetic+potential);pressure=s.simplify(kinetic-potential)
    momentum=s.simplify(s.I*mode*(x[7]+x[8]/4))
    checks[f'{mode}_{record["reservoir_input"]}_{i}_scalar_energy_zero']=energy==0
    checks[f'{mode}_{record["reservoir_input"]}_{i}_scalar_momentum_zero']=momentum==0
    stress.append({'energy':str(energy),'pressure':str(pressure),'kinetic':str(s.simplify(kinetic)),'potential':str(s.simplify(potential))})
   dp=s.simplify(s.sympify(stress[0]['pressure'])-s.sympify(stress[1]['pressure']))
   response=[s.sympify(z) for z in record['response_difference']]
   checks[f'{mode}_{record["reservoir_input"]}_area_pressure_identity']=s.simplify(response[5]+s.Rational(10,11)*dp)==0
   checks[f'{mode}_{record["reservoir_input"]}_flux_area_identity']=s.simplify(response[5]-2*s.I*mode*response[3])==0
   records.append({'reservoir_input':record['reservoir_input'],'scalar_stress':stress,'pressure_difference':str(dp),'pressures_identical':dp==0,'area_acceleration_difference':str(response[5])})
  results.append({'ell':mode,'records':records});print(json.dumps({'ell':mode,'pressure_differences':[z['pressure_difference'] for z in records]}),flush=True)
 assert all(checks.values()),[k for k,vv in checks.items() if not vv]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 p=out/'receipt.json';o={'status':'PASS_SCALAR_STRESS_AND_INITIAL_GEOMETRIC_RESPONSE_AUDIT','checks':checks,'inputs':pins,'results':results,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Combined declared canonical scalar-plus-potential stress at matched initial points; not independent reservoir stress, irreversible memory or finite-time physical clearance.'};p.write_bytes((json.dumps(o,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
