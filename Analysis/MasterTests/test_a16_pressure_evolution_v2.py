"""Fresh continuous pressure certificate for the original-chart radial-rate seed."""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_certified_numerical_v1 as c
k=c.k
BASE='Analysis/MasterTests/outputs/'
PINS='Theory/Gates/RES-001/RES001_A16_PRESSURE_EVOLUTION_V2_INPUTS_2026-11-16.json'
T=Q(1,20)

def encode(o):return (json.dumps(o,sort_keys=True,indent=2)+'\n').encode()
def save(p,o):
 p.write_bytes(encode(o));Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
def read(p):return json.loads((ROOT/p).read_text())
def val(i):return float(Q(i,k.SCALE))
def endpoint(z):return [str(z[0].lo),str(z[1].lo)]
def fcomplex(z):return complex(val(z[0].lo),val(z[1].lo))

def step(entries,initial,h):
 """Single-column counterpart of the pinned four-column defect stepper."""
 coeff=[[z] for z in initial];residual=[0]*20
 for n in range(c.DEGREE):
  rhs=[(k.ZERO,k.ZERO) for _ in range(20)]
  for i,j,re,im in entries:
   for p in range(n+1):
    z=(re.coeff[p],im.coeff[p])
    if not (z[0].is_zero() and z[1].is_zero()):rhs[i]=c.complex_add(rhs[i],c.complex_mul(z,coeff[j][n-p]))
  for i in range(20):
   new=c.complex_center(c.complex_scale(rhs[i],h.numerator,h.denominator*(n+1)))
   coeff[i].append(new);actual=c.complex_scale(new,(n+1)*h.denominator,h.numerator)
   residual[i]+=c.complex_abs_upper((actual[0]-rhs[i][0],actual[1]-rhs[i][1]))
 for i,j,re,im in entries:
  aa=[re.coeff[p].abs_upper()+im.coeff[p].abs_upper() for p in range(c.DEGREE+1)]
  zz=[c.complex_abs_upper(z) for z in coeff[j]]
  residual[i]+=sum(k.upprod(value,zz[q]) for p,value in enumerate(aa) if value for q in range(max(0,c.DEGREE-p),c.DEGREE+1))
  residual[i]+=k.upprod(re.radius+im.radius,sum(zz))
 models=[(k.TM([z[0] for z in row]),k.TM([z[1] for z in row])) for row in coeff]
 end=[c.sum_complex(row) for row in coeff]
 assert all(q.lo==q.hi for z in end for q in z),'unaccounted tile jump'
 return models,end,max(residual),max(sum(c.complex_abs_upper(z) for z in row) for row in coeff)

def observe(entries,models,nrows=2):
 zero=k.TM.constant(k.ZERO,c.DEGREE);out=[(zero,zero) for _ in range(nrows)]
 for i,j,re,im in entries:out[i]=c.complex_add(out[i],c.complex_mul((re,im),models[j]))
 return out

def calculate():
 pins=read(PINS)
 before={p:(hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),(ROOT/p).stat().st_mtime_ns) for p in pins}
 assert all(before[p][0]==h for p,h in pins.items()),'input drift'
 checks=c.common.Checks();c.arithmetic_controls(checks)
 print("Constructing full coupled pressure maps",flush=True)
 bg=c.old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
 mats={name:c.old.parent.import_matrix(obj,bg.sy) for name,obj in read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json').items()}
 L,F,B,Bi=[mats[name] for name in ['full_generator','full_field_reconstruction','balancing_map','balancing_map_inverse']]
 alpha=F[0,:];proper=lambda row,rate:bg.dt(row)+row*L-rate*alpha
 kinetic=ud*proper(F[13,:],ud)+vd*proper(F[14,:],vd)+rd*proper(F[15,:],rd)
 U=s.expand(bg.energy-(ud*ud+vd*vd+rd*rd+3*pd*pd)/2-rho)
 potential=sum((s.diff(U,q)*F[i,:] for q,i in [(u,13),(v,14),(r,15)]),s.zeros(1,20))
 P=(kinetic-potential).applyfunc(s.cancel);area=(F[7,:]+F[9,:])/2
 obs=s.Matrix.vstack(P,area);obsz=(obs*Bi).applyfunc(s.cancel)
 pr=bg.dt(P)+P*L-bg.dt(s.Matrix([(ud*ud+vd*vd+rd*rd)/2-U]))[0]*alpha
 init_values=[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]
 ip=dict(zip(bg.bg,init_values));seed=s.zeros(20,1);seed[16]=1
 beta=s.Rational(2,5);Pi=F[16,:]
 number=s.I*bg.ell/a*mats['actual_dust_observable'][0,:]+(F[4,:]+F[7,:]+F[9,:])/2-beta*Pi
 flux=-s.I*bg.ell/(a*a*C)*F[17,:]-F[1,:]/a
 held=s.Matrix.vstack(number,flux,area,bg.dt(area)+area*L,F[10,:],Pi,proper(Pi,pd),F[15,:],proper(F[15,:],rd),kinetic+potential,P)
 checks.add('initial_eleven_holds',all(s.simplify(z)==0 for z in (held*seed).subs(ip)))
 checks.add('direct_initial_pressure_rate',s.simplify((pr*seed)[0].subs(ip)+s.Rational(2341,840))==0)
 checks.add('pressure_map_background_drift_retained',any(q!=0 for q in bg.dt(P)))
 checks.add('lapse_coupling_retained',any(s.cancel(q)!=0 for q in P-(ud*(bg.dt(F[13,:])+F[13,:]*L)+vd*(bg.dt(F[14,:])+F[14,:]*L)+rd*(bg.dt(F[15,:])+F[15,:]*L)-potential)))
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
 checks.add('identical_background_approximant',bc['degree']==40 and bc['digits']==70 and bc['background_order']==[str(q) for q in bg.bg])
 background=[k.TM([k.IV.fraction(Q(pair[0])*T**j) for j,pair in enumerate(row)]) for row in bc['background_coefficients']]
 assert all(Q(pair[1])==0 for row in bc['background_coefficients'] for pair in row)
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 boxes={bg.sy[name]:k.IV(k.IV.fraction(Q(z[0])-Q(1,100)).lo,k.IV.fraction(Q(z[1])+Q(1,100)).hi) for name,z in un['background_boxes'].items()}
 oldcert=read(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json')
 eb=k.IV.fraction(Q(oldcert['background']['error'])).hi
 checks.add('inherited_background_margin',Q(oldcert['background']['continuation_margin'])>Q(oldcert['background']['error']))
 checks.add('full_vector_Q_bound',Q(un['mu_exact'])<60 and all(Q(x)>=Q(1,9) for x in un['lower_metric_diagonal']))
 checks.add('old_certificate_not_physics_clearance',not oldcert['physics_pass'])
 ev=c.evaluators(dict(zip(bg.bg,background)),40);be=c.evaluators(boxes)
 ratefun=s.lambdify([list(bg.bg)],bg.rates,'numpy',cse=True)
 rows=[];alltiles={}
 true0=np.array([float(x) for x in init_values]);amplification=k.exp_upper(k.IV.rational(3,2))
 for mode in [4,8,16,32,64]:
  print('ell='+str(mode)+' pressure enclosure starting',flush=True)
  az=mats['balanced_generator'].subs(bg.ell,mode);oz=obsz.subs(bg.ell,mode)
  ag=[(i,j,ev(re),ev(im)) for i,j,re,im in c.split_matrix(az)]
  og=[(i,j,ev(re),ev(im)) for i,j,re,im in c.split_matrix(oz)]
  oldrow=next(z for z in oldcert['modes'] if z['ell']==mode);steps=oldrow['steps'];h=T/steps
  constants={name:k.IV.fraction(Q(value)).hi for name,value in oldrow['constants'].items()}
  lips=[c.matrix_lipschitz(oz[i,:],bg.bg,be) for i in range(2)]
  norms=[c.matrix_norm(oz[i,:],be) for i in range(2)]
  init_ev=c.evaluators({**{q:c.evaluators({})(x) for q,x in ip.items()},bg.ell:k.IV.rational(mode)})
  column=c.interval_matrix(B*seed,init_ev)
  state=[c.complex_center(row[0]) for row in column]
  initial_error=max(c.complex_abs_upper((z[0]-row[0][0],z[1]-row[0][1])) for z,row in zip(state,column))
  initial_state=[fcomplex(z) for z in state];defect=amplitude=0;tiles=[];ends=[];chain=hashlib.sha256()
  for tile in range(steps):
   local=c.restrict_entries(ag,tile,steps)
   models,end,d,bound=step(local,state,h)
   if tile==0:
    padded=[[state[i]]+[(k.ZERO,k.ZERO)]*3 for i in range(20)]
    ref,refend,refd,refa=c.state_polynomial(local,padded,h)
    checks.add('four_column_reference_'+str(mode),all([(q.lo,q.hi) for q in models[i][j].coeff]==[(q.lo,q.hi) for q in ref[i][0][j].coeff] and models[i][j].radius==ref[i][0][j].radius for i in range(20) for j in range(2)) and refd==d and refa==bound)
    zm,ze,zd,za=step(local,[(k.ZERO,k.ZERO)]*20,h)
    checks.add('zero_solution_'+str(mode),zd==za==0 and all(q.is_zero() for z in ze for q in z))
    nm,ne,nd,na=step(local,[(-q[0],-q[1]) for q in state],h)
    checks.add('negative_seed_symmetry_'+str(mode),nd==d and na==bound and all(endpoint(ne[i])==endpoint((-end[i][0],-end[i][1])) for i in range(20)))
   observed=observe(c.restrict_entries(og,tile,steps),models)
   digest=hashlib.sha256(encode([[[q.lo,q.hi] for q in z.coeff] for pair in models for z in pair])).hexdigest();chain.update(bytes.fromhex(digest))
   tiles.append({'tile':tile,'t_start':str(tile*h),'t_end':str((tile+1)*h),'polynomial_sha256':digest,'defect_upper':str(d),'amplitude_upper':str(bound),'observation_polynomial_ranges':[[[str(z.range().lo),str(z.range().hi)] for z in pair] for pair in observed]})
   ends.append({'state':[fcomplex(z) for z in end],'observation':[complex(val(pair[0].at().center().lo),val(pair[1].at().center().lo)) for pair in observed]})
   defect=max(defect,d);amplitude=max(amplitude,bound);state=end
   if (tile+1)%64==0:print('ell='+str(mode)+' tile '+str(tile+1)+'/'+str(steps),flush=True)
  forcing=defect+k.upprod(k.upprod(constants['L_Az'],eb),amplitude)
  ew=k.upprod(amplification,k.upprod(constants['K_T_infinity_to_Q'],initial_error+k.IV(forcing).scale(T.numerator,T.denominator).hi))
  ze=k.upprod(constants['K_inverse_Q_to_infinity'],ew)
  errors=[k.upprod(n,ze)+k.upprod(k.upprod(l,eb),amplitude) for n,l in zip(norms,lips)]
  for tile in tiles:
   tile['certified_observation_ranges']=[[[str(int(z[0])-error),str(int(z[1])+error)] for z in pair] for pair,error in zip(tile['observation_polynomial_ranges'],errors)]
   lo,hi=map(int,tile['certified_observation_ranges'][0][0]);tile['real_pressure_sign']='negative' if hi<0 else 'positive' if lo>0 else 'unresolved_or_zero'
  lf=s.lambdify([list(bg.bg)],L.subs(bg.ell,mode),'numpy',cse=True)
  bf=s.lambdify([list(bg.bg)],B.subs(bg.ell,mode),'numpy',cse=True)
  of=s.lambdify([list(bg.bg)],obs.subs(bg.ell,mode),'numpy',cse=True)
  def rhs(t,y):return np.r_[np.asarray(ratefun(y[:11])).reshape(11),np.asarray(lf(y[:11]))@y[11:]]
  numerical=solve_ivp(rhs,(0,float(T)),np.r_[true0,np.array(seed,dtype=complex).reshape(20)],method='DOP853',rtol=2e-12,atol=2e-14,max_step=min(.001,1/mode**2),t_eval=np.arange(1,steps+1)*float(h))
  assert numerical.success
  state_diff=obs_diff=0.
  for j,end in enumerate(ends):
   y=numerical.y[:,j];state_diff=max(state_diff,float(np.max(np.abs(np.asarray(bf(y[:11]))@y[11:]-end['state']))))
   obs_diff=max(obs_diff,float(np.max(np.abs(np.asarray(of(y[:11]))@y[11:]-end['observation']))))
  checks.add('independent_full_original_chart_solver_'+str(mode),state_diff<1e-7 and obs_diff<1e-7,{'balanced_state':state_diff,'observations':obs_diff},'diagnostic tolerance 1e-7; not the certificate')
  checks.add('fresh_pressure_error_below_1e8_'+str(mode),errors[0]<k.IV.rational(1,10**8).lo)
  checks.add('fresh_full_state_error_below_1e8_'+str(mode),ze<k.IV.rational(1,10**8).lo)
  signs={name:sum(t['real_pressure_sign']==name for t in tiles) for name in ['negative','positive','unresolved_or_zero']}
  rows.append({'ell':mode,'steps':steps,'initial_balanced':[endpoint(z) for z in [c.complex_center(row[0]) for row in column]],'background_error_upper':k.upper_fraction(eb),'initial_error_upper':k.upper_fraction(initial_error),'state_defect_upper':k.upper_fraction(defect),'state_amplitude_upper':k.upper_fraction(amplitude),'state_error_upper':k.upper_fraction(ze),'observation_errors':[k.upper_fraction(q) for q in errors],'observation_norms':[k.upper_fraction(q) for q in norms],'observation_lipschitz':[k.upper_fraction(q) for q in lips],'sign_tile_counts':signs,'tile_chain_sha256':chain.hexdigest(),'final_state':[endpoint(z) for z in state],'final_observation':[[z.real,z.imag] for z in ends[-1]['observation']],'independent_solver_max_errors':{'state':state_diff,'observation':obs_diff}})
  alltiles[str(mode)]=tiles
  print(json.dumps({'ell':mode,'pressure_error':val(errors[0]),'final_pressure':rows[-1]['final_observation'][0],'sign_tiles':signs}),flush=True)
 checks.add('immutable_inputs',all((hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),(ROOT/p).stat().st_mtime_ns)==before[p] for p in pins))
 result={'status':'PASS_CONTINUOUS_FINITE_MODE_PRESSURE_RESPONSE' if all(row['passed'] for row in checks.rows) else 'FAIL_CONTINUOUS_FINITE_MODE_PRESSURE_RESPONSE','checks':checks.rows,'inputs':pins,'passed':sum(z['passed'] for z in checks.rows),'total':len(checks.rows),'modes':rows,'domain':{'t':['0','1/20'],'ell':[4,8,16,32,64],'seed':'original chart delta u_dot=1, other slots zero'},'observation_order':['combined_canonical_scalar_pressure','transverse_metric_area'],'dyadic_scale':str(k.SCALE),'no_projection_during_evolution':True,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Conditional finite-mode linear pressure response; no nonlinear, physical-window, EOS, entropy or matching clearance.'}
 return result,alltiles

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 result,tiles=calculate();save(out/'receipt.json',result);save(out/'tiles.json',tiles)
 print(json.dumps({q:result[q] for q in ['status','passed','total','physics_pass']}))
 if result['passed']!=result['total']:raise SystemExit(1)
if __name__=='__main__':main()
