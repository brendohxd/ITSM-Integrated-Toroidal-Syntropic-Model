"""Independent retained Volterra evolution from sealed kernel-only inputs."""
from pathlib import Path
from fractions import Fraction as Q
from concurrent.futures import ProcessPoolExecutor
import argparse,gzip,hashlib,json,sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_a16_numerical_kernel_v1 as n
c=n.c;k=n.k;ref=n.ref;T=Q(1,20);DEG=n.DEG;BASE=n.BASE
PINS='Theory/Gates/RES-001/RES001_A16_VOLTERRA_EVOLUTION_V1_INPUTS_2026-11-19.json'
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def save(p,o):
 p.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n',encoding='utf-8');Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
def compressed(p,o):
 data=gzip.compress(json.dumps(o,sort_keys=True,separators=(',',':')).encode(),compresslevel=6,mtime=0);p.write_bytes(data);Path(str(p)+'.sha256').write_text(hashlib.sha256(data).hexdigest()+'  '+p.name+'\n',encoding='utf-8');return hashlib.sha256(data).hexdigest()
def unpack(mat):return [[tuple(k.TM([k.IV(int(q)) for q in side]) for side in pair) for pair in row] for row in mat]
def derivative(mat,h):return [[(z[0].derivative(h),z[1].derivative(h)) for z in row] for row in mat]
def vecnumeric(mat):return n.numeric(mat).reshape(len(mat))
def progress(out,mode,msg):
 line=f'ell={mode}: {msg}';print(line,flush=True)
 with (ROOT/'.local/itsm-context'/(out.name+'-progress.log')).open('a',encoding='utf-8') as f:f.write(line+'\n')

def advance(filtered):
 """Only filtered factors, A/P_R, initial data and steps enter advancement."""
 mode=filtered['ell'];steps=filtered['steps'];h=T/steps
 state=[(k.ZERO,k.ZERO) for _ in range(20)];state[12]=(k.ONE,k.ZERO)
 h0=n.zeros(4,1);h0[2][0]=(k.TM.constant(k.IV.rational(1,mode),DEG),k.TM.constant(k.ZERO,DEG))
 curves=[];dR=dJ=MR=MJ=ap=0;checkzero=True;constant=True
 for fr in filtered['frames']:
  mats={name:unpack(fr[name]) for name in ['A','Pr','L','Rh','Lp']}
  forcing=n.multiply(mats['L'],h0)
  entries=[]
  for i in range(8):
   for j in range(8):
    if not n.tmzero(mats['A'][i][j]):entries.append((i,j,*mats['A'][i][j]))
   for j in range(4):
    if not n.tmzero(mats['L'][i][j]):entries.append((i,j+8,*mats['L'][i][j]))
   if not n.tmzero(forcing[i][0]):entries.append((i,12,*forcing[i][0]))
  for i in range(4):
   for j in range(8):
    if not n.tmzero(mats['Rh'][i][j]):entries.append((i+8,j,*mats['Rh'][i][j]))
  models,state,_,_=ref.step(entries,state,h)
  R=[[models[i]] for i in range(8)];J=[[models[i+8]] for i in range(4)]
  hplus=n.plus(h0,J)
  rhs=n.plus(n.multiply(mats['A'],R),n.multiply(mats['L'],hplus))
  integrand=n.multiply(mats['Rh'],R)
  dR=max(dR,n.tmnorm(n.minus(derivative(R,h),rhs)));dJ=max(dJ,n.tmnorm(n.minus(derivative(J,h),integrand)))
  MR=max(MR,n.tmnorm(R));MJ=max(MJ,n.tmnorm(J))
  P,loss=n.center(n.plus(n.multiply(mats['Pr'],R),n.multiply(mats['Lp'],hplus)));ap=max(ap,loss)
  constant &= models[12][0].coeff[0].lo==k.SCALE and models[12][0].sup()==k.SCALE and models[12][1].sup()==0 and all(x.lo==x.hi==0 for z in state[13:] for x in z)
  if fr['tile']==0:
   zero=[(k.ZERO,k.ZERO) for _ in range(20)];zero[12]=(k.ONE,k.ZERO)
   _,ends,_,_=ref.step([e for e in entries if e[1]!=12],zero,h)
   checkzero=all(x.is_zero() for z in ends[:12] for x in z)
  curves.append({'tile':fr['tile'],'R':n.pack(R),'J':n.pack(J),'P':n.pack(P),'R_rate':n.pack(derivative(R,h))})
 return curves,{'R_defect':dR,'J_defect':dJ,'R_amplitude':MR,'J_amplitude':MJ,'pressure_arithmetic':ap},checkzero and constant

def run_mode(mode,out_name):
 out=ROOT/out_name;folder=out/('ell_'+str(mode));folder.mkdir(exist_ok=False);progress(out,mode,'preparing kernel-only input')
 parent=read(BASE+'a16_numerical_kernel_v1_20261119/receipt.json');old=next(r for r in parent['modes'] if r['ell']==mode)
 # Reference fields are deliberately not included in the advancing input.
 old_path=ROOT/(BASE+f'a16_numerical_kernel_v1_20261119/ell_{mode}/curves.json.gz')
 src_frames=json.loads(gzip.decompress(old_path.read_bytes()))['frames']
 frames=[{key:f[key] for key in ['tile','L','Rh','Lp']} for f in src_frames];del src_frames
 bg=c.old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
 raw=read(BASE+'a16_finite_state_history_v3_20261116/formulas.json')
 parse=lambda name:s.Matrix([[s.sympify(x,locals=bg.sy) for x in row] for row in raw[name]])
 A=parse('retained_generator_A').subs(bg.ell,mode);Pr=parse('pressure_row')[:,:8].subs(bg.ell,mode)
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
 polynomials=[k.TM([k.IV.fraction(Q(z[0])*T**j) for j,z in enumerate(row)]) for row in bc['background_coefficients']]
 ev=c.evaluators(dict(zip(bg.bg,polynomials)),40);steps=old['steps'];h=T/steps
 ag={name:[(i,j,ev(re),ev(im)) for i,j,re,im in c.split_matrix(expr)] for name,expr in [('A',A),('Pr',Pr)]}
 losses={'A':0,'Pr':0}
 for f in frames:
  for name,cols in [('A',8),('Pr',8)]:
   rows=8 if name=='A' else 1
   arr,loss=n.center(n.entries_matrix(c.restrict_entries(ag[name],f['tile'],steps),rows,cols));f[name]=n.pack(arr);losses[name]=max(losses[name],loss)
 filtered={'schema':'a16-kernel-only-evolution-input-v1','ell':mode,'steps':steps,'T':str(T),'degree':DEG,'dyadic_scale':str(k.SCALE),'R0':'zero','h0':['0','0',str(Q(1,mode)),'0'],'frames':frames}
 input_hash=compressed(folder/'coefficients_only.json.gz',filtered)
 checks={'filtered_input_has_no_reference_or_hidden_generator':all(set(f)=={'tile','L','Rh','Lp','A','Pr'} for f in frames)}
 progress(out,mode,'advancing eight retained variables and four memory quadratures')
 curves,metrics,structural=advance(filtered)
 trajectory_hash=compressed(folder/'solution.json.gz',{'schema':'a16-independent-volterra-curves-v1','ell':mode,'steps':steps,'T':str(T),'degree':DEG,'dyadic_scale':str(k.SCALE),'frames':curves})
 checks['causal_forcing_and_constant_control']=structural
 checks['sealed_solution_before_reference_comparison']=(folder/'solution.json.gz').is_file()
 # All quantities below certify or compare already sealed independent curves.
 progress(out,mode,'sealed; deriving residual-lift certificate')
 matrices={name:c.old.parent.import_matrix(obj,bg.sy) for name,obj in read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json').items()}
 Bal=matrices['balancing_map'];Az=matrices['balanced_generator'];Mi=parse('mixed_inverse')
 E=s.zeros(20,12)
 for off,co in [(0,0),(10,6)]:
  E[off,co]=E[off+2,co]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,co+j]=1
 mixed=parse('retained_generator_A').row_join(parse('hidden_to_retained_B')).col_join(parse('retained_to_hidden_C').row_join(parse('hidden_generator_D')))
 Lift=(Bal*E*Mi).applyfunc(s.cancel)
 defect=(bg.dt(Lift)+Lift*mixed-Az*Lift).applyfunc(s.cancel)
 checks['exact_moving_lift_conjugacy_on_shell']=all(q==0 or bg.constraint_reduce_scalar(q)==0 for q in defect)
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 mixed0=s.zeros(12,1);mixed0[10]=s.Rational(1,mode);original0=s.zeros(20,1);original0[16]=1
 checks['initial_lift_matches_original_radial_seed']=all(s.simplify(q.subs({**init,bg.ell:mode}))==0 for q in Lift*mixed0-Bal*original0)
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 boxes={bg.sy[name]:k.IV(k.IV.fraction(Q(z[0])-Q(1,100)).lo,k.IV.fraction(Q(z[1])+Q(1,100)).hi) for name,z in un['background_boxes'].items()};be=c.evaluators(boxes)
 lift_norm=c.matrix_norm(Lift.subs(bg.ell,mode),be)
 fund=old['fundamental'];eb=n.scaled(fund['background_error']);Hprop=n.scaled(fund['hidden_propagator_bound'])
 eA=n.times(n.scaled(old['lipschitz']['A']),eb)+losses['A'];ePr=n.times(n.scaled(old['lipschitz']['Pr']),eb)+losses['Pr']
 eL=n.scaled(old['errors']['L']);eRh=n.scaled(old['errors']['Rh']);eLp=n.scaled(old['errors']['Lp'])
 mr,mj=metrics['R_amplitude'],metrics['J_amplitude'];hp=k.IV.rational(1,mode).hi+mj
 rR=metrics['R_defect']+n.times(eA,mr)+n.times(eL,hp);rJ=metrics['J_defect']+n.times(eRh,mr)
 balanced_forcing=n.times(lift_norm,max(rR,n.times(Hprop,rJ)))
 full=next(row for row in read(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json')['modes'] if row['ell']==mode)
 KT=n.scaled(full['constants']['K_T_infinity_to_Q']);KI=n.scaled(full['constants']['K_inverse_Q_to_infinity']);amp=k.exp_upper(k.IV.rational(3,2))
 ez=n.times(n.times(n.times(KI,amp),KT),n.hscale(balanced_forcing,T))
 NR,NP,NRd=[n.scaled(old['norms'][name]) for name in ['Rz','Pz','Rdz']]
 eR=n.times(NR,ez);eP=n.times(NP,ez)+n.times(ePr,mr)+n.times(eLp,hp)+metrics['pressure_arithmetic'];eRd=n.times(NRd,ez)+rR
 errors={'balanced_lift':ez,'retained_state':eR,'pressure':eP,'retained_rate':eRd}
 for name,value in errors.items():checks[name+'_absolute_accuracy']=value<k.IV.rational(1,10**8).lo
 references=json.loads(gzip.decompress(old_path.read_bytes()))['frames']
 differences={name:0 for name in ['R','P','R_rate']}
 for own,other in zip(curves,references):
  for key,rkey in [('R','R_reference'),('P','P_reference'),('R_rate','R_rate_reference')]:
   differences[key]=max(differences[key],n.tmnorm(n.minus(unpack(own[key]),unpack(other[rkey]))))
 for name,value in differences.items():checks[name+'_continuous_reference_agreement']=value<k.IV.rational(1,10**8).lo
 # Independent floating integration consumes the same filtered Volterra input.
 floatframes=[]
 for fr in frames:
  data={}
  for key in ['A','L','Rh','Pr','Lp']:
   arr=np.array([[[complex(int(z[0][j])/k.SCALE,int(z[1][j])/k.SCALE) for j in range(DEG+1)] for z in row] for row in fr[key]])
   data[key]=np.moveaxis(arr,2,0)
  floatframes.append(data)
 def vals(t):
  pos=min(max(t/float(h),0),steps);tile=min(int(pos),steps-1);x=pos-tile
  return {key:np.polynomial.polynomial.polyval(x,floatframes[tile][key]) for key in ['A','L','Rh','Pr','Lp']}
 h0num=np.array([0,0,1/mode,0],complex)
 def rhs(t,y):
  vv=vals(t);return np.r_[vv['A']@y[:8]+vv['L']@(h0num+y[8:]),vv['Rh']@y[:8]]
 sol=solve_ivp(rhs,(0,float(T)),np.zeros(12,complex),method='DOP853',rtol=2e-11,atol=2e-14,max_step=min(.0005,1/(4*mode**2)),t_eval=np.linspace(0,float(T),steps+1));assert sol.success
 worstR=worstP=0.
 for j,fr in enumerate(curves,1):
  yy=sol.y[:,j];vv=vals(j*float(h));pn=(vv['Pr']@yy[:8]+vv['Lp']@(h0num+yy[8:]))[0]
  worstR=max(worstR,float(np.max(np.abs(vecnumeric(unpack(fr['R']))-yy[:8]))));worstP=max(worstP,abs(vecnumeric(unpack(fr['P']))[0]-pn))
 checks['independent_filtered_realization_solver']=worstR<1e-7 and worstP<1e-7
 end={key:[[z.real,z.imag] for z in vecnumeric(unpack(curves[-1][key]))] for key in ['R','J','P']}
 result={'ell':mode,'steps':steps,'checks':checks,'metrics':{q:k.upper_fraction(v) for q,v in metrics.items()},'factor_errors':{q:k.upper_fraction(v) for q,v in [('A',eA),('Pr',ePr),('L',eL),('Rh',eRh),('Lp',eLp)]},'certificate_constants':{q:k.upper_fraction(v) for q,v in [('lift_norm',lift_norm),('Hprop',Hprop),('KT',KT),('KI',KI),('exp_30T',amp),('NR',NR),('NP',NP),('NRd',NRd)]},'physical_defects':{'R':k.upper_fraction(rR),'J':k.upper_fraction(rJ),'balanced_forcing':k.upper_fraction(balanced_forcing)},'errors':{q:k.upper_fraction(v) for q,v in errors.items()},'difference_majorants':{q:k.upper_fraction(v) for q,v in differences.items()},'independent_solver_errors':{'R':worstR,'P':worstP},'input_sha256':input_hash,'sealed_solution_sha256':trajectory_hash,'endpoint':end}
 save(folder/'receipt.json',result);progress(out,mode,'complete '+json.dumps({q:float(Q(v)) for q,v in result['errors'].items()}))
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS);before={p:(sha(p),(ROOT/p).stat().st_mtime_ns) for p in pins};assert all(before[p][0]==h for p,h in pins.items())
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 with ProcessPoolExecutor(max_workers=5) as pool:rows=list(pool.map(run_mode,[4,8,16,32,64],[args.output_dir]*5))
 checks={str(row['ell'])+'_'+q:v for row in rows for q,v in row['checks'].items()};checks['immutable_source_hashes_and_timestamps']=all((sha(p),(ROOT/p).stat().st_mtime_ns)==before[p] for p in pins)
 receipt={'status':'PASS_INDEPENDENT_RETAINED_VOLTERRA_EVOLUTION' if all(checks.values()) else 'FAIL_INDEPENDENT_RETAINED_VOLTERRA_EVOLUTION','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'modes':rows,'domain':{'t':['0','1/20'],'ell':[4,8,16,32,64]},'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Independent retained Volterra evolution with four causal quadrature accumulators, certified via the unchanged-action error lift. No memory-free reduction, physical health, irreversible bath or matching.'}
 save(out/'receipt.json',receipt);print(json.dumps({q:receipt[q] for q in ['status','passed','total','physics_pass']}),flush=True)
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
