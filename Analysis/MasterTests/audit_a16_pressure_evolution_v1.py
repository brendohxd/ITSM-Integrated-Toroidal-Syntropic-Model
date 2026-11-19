"""Independent rational error-budget and tile-coverage audit; no solver imports."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math
ROOT=Path(__file__).resolve().parents[2]
PINS='Theory/Gates/RES-001/RES001_A16_PRESSURE_EVOLUTION_AUDIT_V1_INPUTS_2026-11-16.json'
BASE='Analysis/MasterTests/outputs/'
def read(p):return json.loads((ROOT/p).read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS)
 assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in pins.items())
 cert=read(BASE+'a16_pressure_evolution_v3_20261116/receipt.json')
 tiles=read(BASE+'a16_pressure_evolution_v3_20261116/tiles.json')
 old=read(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json')
 # Positive-term exponential series with geometric majorant of its entire tail.
 x=F(3,2);N=160
 series=sum((x**j/math.factorial(j) for j in range(N+1)),F(0))
 exponential_upper=series+x**(N+1)/math.factorial(N+1)/(1-x/F(N+2))
 checks={};details=[];scale=int(cert['dyadic_scale']);T=F(1,20)
 checks['frozen_acceptance_and_physics_hold']=cert['passed']==cert['total']==88 and not cert['physics_pass'] and cert['gate_effect']=='NONE' and cert['review']=='DEFERRED'
 checks['propagation_unchanged_by_control_repair']=(ROOT/(BASE+'a16_pressure_evolution_v2_20261116/tiles.json')).read_bytes()==(ROOT/(BASE+'a16_pressure_evolution_v3_20261116/tiles.json')).read_bytes()
 for row in cert['modes']:
  mode=row['ell'];o=next(r for r in old['modes'] if r['ell']==mode);co={k:F(v) for k,v in o['constants'].items()}
  eb,ei,d,M,ez=[F(row[k]) for k in ['background_error_upper','initial_error_upper','state_defect_upper','state_amplitude_upper','state_error_upper']]
  independent_state_bound=exponential_upper*co['K_inverse_Q_to_infinity']*co['K_T_infinity_to_Q']*(ei+T*(d+co['L_Az']*eb*M))
  checks[f'{mode}_independent_exact_error_formula']=ez>=independent_state_bound
  checks[f'{mode}_background_certificate_preserved']=eb>=F(old['background']['error']) and eb<F(1,10**30)
  for i,(err,norm,lip) in enumerate(zip(row['observation_errors'],row['observation_norms'],row['observation_lipschitz'])):
   checks[f'{mode}_observation_{i}_error_formula']=F(err)>=F(norm)*ez+F(lip)*eb*M
  checks[f'{mode}_useful_accuracy']=ez<F(1,10**8) and F(row['observation_errors'][0])<F(1,10**8)
  ts=tiles[str(mode)];end=F(0);chain=hashlib.sha256();valid=True;signs={'negative':0,'positive':0,'unresolved_or_zero':0}
  for n,t in enumerate(ts):
   valid &= t['tile']==n and F(t['t_start'])==end and F(t['t_end'])-end==T/row['steps'];end=F(t['t_end'])
   chain.update(bytes.fromhex(t['polynomial_sha256']))
   for i in range(2):
    e=F(row['observation_errors'][i])*scale
    valid &= e.denominator==1
    for j in range(2):
     lo,hi=map(int,t['observation_polynomial_ranges'][i][j]);a,b=map(int,t['certified_observation_ranges'][i][j])
     valid &= a==lo-int(e) and b==hi+int(e) and a<=b
   lo,hi=map(int,t['certified_observation_ranges'][0][0]);sign='negative' if hi<0 else 'positive' if lo>0 else 'unresolved_or_zero'
   valid &= sign==t['real_pressure_sign'];signs[sign]+=1
  checks[f'{mode}_complete_outward_tiles']=valid and end==T and len(ts)==row['steps'] and signs==row['sign_tile_counts']
  checks[f'{mode}_tile_chain']=chain.hexdigest()==row['tile_chain_sha256']
  checks[f'{mode}_independent_solver_control']=max(row['independent_solver_max_errors'].values())<1e-7
  details.append({'ell':mode,'independent_state_bound':str(independent_state_bound),'reported_state_error':str(ez),'signs':signs})
 checks['inputs_unchanged']=all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in pins.items())
 result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'details':details,'inputs':pins,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Independent rational audit of the conditional numerical certificate; not independent scientific review.'}
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False);p=out/'receipt.json';p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
 print(json.dumps({k:result[k] for k in ['status','passed','total']}));print('Failures:',[k for k,v in checks.items() if not v])
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
