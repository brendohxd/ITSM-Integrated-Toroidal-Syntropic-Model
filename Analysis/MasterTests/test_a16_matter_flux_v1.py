"""Current dictionary and full-drift conservation for the existing probes."""
from pathlib import Path
import sys,argparse,json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_remainder_v1 as old
PINS='Theory/Gates/RES-001/RES001_A16_MATTER_FLUX_V1_INPUTS_2026-11-16.json'
BASE='Analysis/MasterTests/outputs/'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;beta=s.Rational(2,5)
 data=json.loads((ROOT/(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json')).read_text());imp=lambda k:old.parent.import_matrix(data[k],bg.sy)
 L,F,O=[imp(n) for n in ['full_generator','full_field_reconstruction','actual_dust_observable']]
 volume=(F[4,:]+F[7,:]+F[9,:])/2;Pi=F[16,:];T=F[17,:];shift=F[1,:];alpha=F[0,:]
 delta_rho=C**4*F[18,:]+4*beta*rho*Pi
 N=s.I*ell/a*O[0,:]+volume-beta*Pi
 flux=-s.I*ell/(a*a*C)*T-shift/a
 checks={}
 def zero(name,m):checks[name]=all(bg.shell(x)==0 for x in m)
 zero('dust_density_dictionary',s.I*ell/a*O[0,:]-delta_rho/rho)
 zero('clock_multiplier_constraint',bg.dt(T)+T*L-C*alpha-beta*C*Pi)
 zero('background_clock_number_conserved',s.Matrix([bg.dt(s.Matrix([a**3*rho/C]))[0]]))
 zero('densitized_current_continuity',bg.dt(N)+N*L+s.I*ell*flux)
 zero('clock_gauge_tau_perturbation_zero',T)
 checks['frame_variable_not_actual_coordinate_flux']=any(bg.shell(x)!=0 for x in flux+O[1,:]/a)
 prior=json.loads((ROOT/(BASE+'a16_matched_reservoir_v1_20261116/receipt.json')).read_text())
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 results=[]
 for oldrow in prior['results']:
  mode=oldrow['ell'];point={**init,ell:mode};ev=lambda m:m.subs(point).applyfunc(s.cancel)
  records=[]
  for record in oldrow['records']:
   vectors=[s.Matrix([s.sympify(x) for x in p['full_initial_direction']]) for p in record['preparations']]
   density=[ev(N)*x for x in vectors];currents=[(ev(flux)*x).applyfunc(s.simplify) for x in vectors]
   delta=currents[0]-currents[1];rates=[(ev(bg.dt(N)+N*L)*x).applyfunc(s.simplify) for x in vectors]
   checks[f'{mode}_{record["reservoir_input"]}_conserved_density_matched']=all(s.simplify(x)==0 for z in density for x in z)
   for i in range(2):checks[f'{mode}_{record["reservoir_input"]}_{i}_continuity']=s.simplify(rates[i][0]+s.I*mode*currents[i][0])==0
   records.append({'reservoir_input':record['reservoir_input'],'normalized_coordinate_fluxes':[str(z[0]) for z in currents],'flux_difference':str(s.simplify(delta[0])),'actual_flux_matched':s.simplify(delta[0])==0,'conserved_density_rates':[str(z[0]) for z in rates]})
  results.append({'ell':mode,'records':records});print(json.dumps({'ell':mode,'actual_flux_matched':[x['actual_flux_matched'] for x in records]}),flush=True)
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 p=out/'receipt.json';o={'status':'PASS_CURRENT_DICTIONARY_AND_PREPARATION_AUDIT','checks':checks,'inputs':pins,'results':results,'physics_pass':False,'review':'DEFERRED','gate_effect':'NONE','scope':'Existing nonzero-mode initial preparations and symbolic linear clock continuity. Physical flux matching is reported, not forced to PASS.'};p.write_bytes((json.dumps(o,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
