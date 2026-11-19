"""Exact-integer Volterra defects and independent rational lift-budget audit."""
from pathlib import Path
from fractions import Fraction as R
import argparse,ast,gzip,hashlib,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import audit_a16_numerical_kernel_v2 as ar
BASE='Analysis/MasterTests/outputs/'
PINS='Theory/Gates/RES-001/RES001_A16_VOLTERRA_EVOLUTION_AUDIT_V1_INPUTS_2026-11-19.json'
def read(p):return json.loads((ROOT/p).read_text())
def zero():return [[0]*49,[0]*49]
def poly(z):return [list(map(int,side)) for side in z]
def addproduct(dest,a,b,sign=1):
 """Accumulate the exact complex polynomial product, with denominator S^2."""
 for x,y,side,sgn in [(a[0],b[0],0,1),(a[1],b[1],0,-1),(a[0],b[1],1,1),(a[1],b[0],1,1)]:
  for i,v in enumerate(x):
   if v:
    for j,w in enumerate(y):
     if w:dest[side][i+j]+=sign*sgn*v*w
def residual_bounds(fr,sol,scale,steps,mode):
 A=[[poly(z) for z in row] for row in fr['A']];L=[[poly(z) for z in row] for row in fr['L']];Rh=[[poly(z) for z in row] for row in fr['Rh']]
 Pr=[[poly(z) for z in row] for row in fr['Pr']];Lp=[[poly(z) for z in row] for row in fr['Lp']]
 rr=[poly(row[0]) for row in sol['R']];jj=[poly(row[0]) for row in sol['J']]
 hp=[[side[:] for side in z] for z in jj];hp[2][0][0]+=scale//mode
 bounds=[]
 for group,count in [('R',8),('J',4)]:
  vectors=rr if group=='R' else jj;worst=0
  for i in range(count):
   out=zero()
   for side in range(2):
    for n in range(24):out[side][n]=vectors[i][side][n+1]*(n+1)*20*steps*scale
   if group=='R':
    for j in range(8):addproduct(out,A[i][j],rr[j],-1)
    for j in range(4):addproduct(out,L[i][j],hp[j],-1)
   else:
    for j in range(8):addproduct(out,Rh[i][j],rr[j],-1)
   worst=max(worst,sum(abs(q) for side in out for q in side))
  bounds.append(R(worst,scale*scale))
 out=zero();pp=poly(sol['P'][0][0])
 for side in range(2):
  for j,z in enumerate(pp[side]):out[side][j]=z*scale
 for j in range(8):addproduct(out,Pr[0][j],rr[j],-1)
 for j in range(4):addproduct(out,Lp[0][j],hp[j],-1)
 pressure=R(sum(abs(q) for side in out for q in side),scale*scale)
 return bounds+[pressure]
def amplitude(frames,name,scale):return R(max(sum(abs(int(x)) for side in row[0] for x in side) for fr in frames for row in fr[name]),scale)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS);sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest();assert all(sha(p)==h for p,h in pins.items())
 data=read(BASE+'a16_volterra_evolution_v2_20261119/receipt.json');parent=read(BASE+'a16_numerical_kernel_v1_20261119/receipt.json')
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json');raw=read(BASE+'a16_finite_state_history_v3_20261116/formulas.json')
 sy={n:s.Symbol(n,real=True) for n in bc['background_order']};sy['a']=s.Symbol('a',positive=True);sy['ell']=s.Symbol('ell',positive=True);sy['I']=s.I
 bg=s.Matrix([sy[n] for n in bc['background_order']]);ell=sy['ell']
 Mi=s.Matrix([[s.sympify(q,locals=sy) for q in row] for row in raw['mixed_inverse']])
 obj=read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json')['balancing_map'];Bal=s.zeros(*obj['shape'])
 for entry in obj['entries']:Bal[entry['row'],entry['column']]=sum(s.sympify(q,locals=sy) for q in entry['terms'])
 E=s.zeros(20,12)
 for off,co in [(0,0),(10,6)]:
  E[off,co]=E[off+2,co]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,co+j]=1
 Lift=(Bal*E*Mi).applyfunc(s.cancel)
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json');boxes={sy[n]:(R(z[0])-R(1,100),R(z[1])+R(1,100)) for n,z in un['background_boxes'].items()}
 code=ast.parse((ROOT/'Analysis/MasterTests/test_a16_volterra_evolution_v2.py').read_text());advance=next(q for q in code.body if isinstance(q,ast.FunctionDef) and q.name=='advance')
 checks={'main_success_and_holds':data['passed']==data['total'] and not data['physics_pass'] and data['gate_effect']=='NONE' and data['review']=='DEFERRED','advancing_function_has_no_file_reads':not any(isinstance(q,ast.Call) and ((isinstance(q.func,ast.Name) and q.func.id in ['open','read','read_text','read_bytes']) or (isinstance(q.func,ast.Attribute) and q.func.attr in ['open','read','read_text','read_bytes'])) for q in ast.walk(advance))}
 full=read(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json');details=[];T=R(1,20)
 for row in data['modes']:
  mode=row['ell'];prefix=str(mode)+'_';base=ROOT/(BASE+f'a16_volterra_evolution_v2_20261119/ell_{mode}/')
  filt=json.loads(gzip.decompress((base/'coefficients_only.json.gz').read_bytes()));sol=json.loads(gzip.decompress((base/'solution.json.gz').read_bytes()));scale=int(sol['dyadic_scale']);steps=row['steps']
  checks[prefix+'sealed_input_hash']=hashlib.sha256((base/'coefficients_only.json.gz').read_bytes()).hexdigest()==row['input_sha256']
  checks[prefix+'sealed_solution_hash']=hashlib.sha256((base/'solution.json.gz').read_bytes()).hexdigest()==row['sealed_solution_sha256']
  checks[prefix+'reference_free_coefficient_input']=all(set(q)=={'tile','A','Pr','L','Rh','Lp'} for q in filt['frames'])
  checks[prefix+'full_time_grid']=len(sol['frames'])==len(filt['frames'])==steps and [f['tile'] for f in sol['frames']]==list(range(steps)) and R(sol['T'])==T
  old=next(q for q in parent['modes'] if q['ell']==mode)
  oldarc=json.loads(gzip.decompress((ROOT/(BASE+f'a16_numerical_kernel_v1_20261119/ell_{mode}/curves.json.gz')).read_bytes()))
  checks[prefix+'unchanged_kernel_coefficients']=all(fr[name]==oldfr[name] for fr,oldfr in zip(filt['frames'],oldarc['frames']) for name in ['L','Rh','Lp'])
  initial=all(int(z[side][0])==0 for key in ['R','J'] for rr in sol['frames'][0][key] for z in rr for side in [0,1]);continuous=True;maxd=[R(0)]*3
  for i,(fr,own) in enumerate(zip(filt['frames'],sol['frames'])):
   vals=residual_bounds(fr,own,scale,steps,mode);maxd=[max(a,b) for a,b in zip(maxd,vals)]
   if i:
    for key in ['R','J']:
     for prev,cur in zip(sol['frames'][i-1][key],own[key]):
      for side in [0,1]:continuous &= sum(map(int,prev[0][side]))==int(cur[0][side][0])
  checks[prefix+'zero_initial_retained_and_integrals']=initial;checks[prefix+'exact_tile_continuity']=continuous
  metrics={n:R(q) for n,q in row['metrics'].items()};factors={n:R(q) for n,q in row['factor_errors'].items()};co={n:R(q) for n,q in row['certificate_constants'].items()};defects={n:R(q) for n,q in row['physical_defects'].items()};err={n:R(q) for n,q in row['errors'].items()}
  checks[prefix+'exact_integer_retained_defect']=metrics['R_defect']>=maxd[0]
  checks[prefix+'exact_integer_quadrature_defect']=metrics['J_defect']>=maxd[1]
  checks[prefix+'exact_integer_pressure_arithmetic']=metrics['pressure_arithmetic']>=maxd[2]
  checks[prefix+'retained_amplitude']=metrics['R_amplitude']>=amplitude(sol['frames'],'R',scale)
  checks[prefix+'integral_amplitude']=metrics['J_amplitude']>=amplitude(sol['frames'],'J',scale)
  for n in ['L','Rh','Lp']:checks[prefix+n+'_factor_error_preserved']=factors[n]==R(old['errors'][n])
  checks[prefix+'A_Pr_factor_errors_valid']=factors['A']>=R(old['errors']['A']) and factors['Pr']>=R(old['errors']['Pr'])
  ev=ar.rational_evaluator({**boxes,ell:(R(mode),R(mode))});checks[prefix+'independent_lift_norm']=co['lift_norm']>=ar.ar.matrixnorm(Lift,ev)
  oc=next(q['constants'] for q in full['modes'] if q['ell']==mode)
  checks[prefix+'full_propagator_conversions']=co['KT']>=R(oc['K_T_infinity_to_Q']) and co['KI']>=R(oc['K_inverse_Q_to_infinity']) and co['exp_30T']>=ar.ar.exponential_upper(R(3,2))
  checks[prefix+'observation_and_hidden_propagator_constants']=all(co[key]>=R(old['norms'][name]) for key,name in [('NR','Rz'),('NP','Pz'),('NRd','Rdz')]) and co['Hprop']>=R(old['fundamental']['hidden_propagator_bound'])
  hp=R(1,mode)+metrics['J_amplitude']
  checks[prefix+'physical_R_defect']=defects['R']>=metrics['R_defect']+factors['A']*metrics['R_amplitude']+factors['L']*hp
  checks[prefix+'physical_J_defect']=defects['J']>=metrics['J_defect']+factors['Rh']*metrics['R_amplitude']
  checks[prefix+'balanced_forcing']=defects['balanced_forcing']>=co['lift_norm']*max(defects['R'],co['Hprop']*defects['J'])
  checks[prefix+'lift_evolution_error']=err['balanced_lift']>=co['KI']*co['exp_30T']*co['KT']*T*defects['balanced_forcing']
  checks[prefix+'retained_state_error']=err['retained_state']>=co['NR']*err['balanced_lift']
  checks[prefix+'pressure_error']=err['pressure']>=co['NP']*err['balanced_lift']+factors['Pr']*metrics['R_amplitude']+factors['Lp']*hp+metrics['pressure_arithmetic']
  checks[prefix+'retained_rate_error']=err['retained_rate']>=co['NRd']*err['balanced_lift']+defects['R']
  checks[prefix+'useful_absolute_accuracy']=all(q<R(1,10**8) for q in err.values())
  checks[prefix+'comparison_thresholds']=all(R(q)<R(1,10**8) for q in row['difference_majorants'].values())
  point=sol['frames'][-1]['P'][0][0];end=R(sum(map(int,point[0])),scale)
  checks[prefix+'certified_endpoint_sign']=end-err['pressure']>0 if mode==64 else end+err['pressure']<0
  details.append({'ell':mode,'independent_exact_defects':list(map(str,maxd)),'endpoint_pressure':str(end),'pressure_error':str(err['pressure'])})
 checks['inputs_unchanged']=all(sha(p)==h for p,h in pins.items())
 result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'independent_residuals':details,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Independent exact-integer evolution/quadrature/pressure residual and rational lift-budget audit. Not independent peer review, physical health or a memory-free reduction.'}
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False);p=out/'receipt.json';p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
 print(json.dumps({q:result[q] for q in ['status','passed','total']}));print('Failures:',[q for q,v in checks.items() if not v])
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
