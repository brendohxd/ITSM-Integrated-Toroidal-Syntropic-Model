"""Independent rational coefficient/budget audit and endpoint pressure decomposition."""
from pathlib import Path
from fractions import Fraction as R
import argparse,gzip,hashlib,json,sys
import sympy as s
from functools import lru_cache
from math import isqrt
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import audit_a16_finite_state_history_v1 as ar
BASE='Analysis/MasterTests/outputs/'
PINS='Theory/Gates/RES-001/RES001_A16_NUMERICAL_KERNEL_AUDIT_V2_INPUTS_2026-11-19.json'
def read(p):return json.loads((ROOT/p).read_text())
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def mul(a,b):
 z=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]];return min(z),max(z)
def cadd(a,b):return add(a[0],b[0]),add(a[1],b[1])
def cneg(a):return neg(a[0]),neg(a[1])
def cmul(a,b):return add(mul(a[0],b[0]),neg(mul(a[1],b[1]))),add(mul(a[0],b[1]),mul(a[1],b[0]))
def inflate(z,e):return ((z[0][0]-e,z[0][1]+e),(z[1][0]-e,z[1][1]+e))
def cp(z,scale):
 re=sum(map(int,z[0]));im=sum(map(int,z[1]));return ((R(re,scale),R(re,scale)),(R(im,scale),R(im,scale)))
def endpoint(mat,scale):return [[cp(z,scale) for z in row] for row in mat]
def repr_interval(z):return [[str(a),str(b)] for a,b in z]
def lipschitz(mat,bg,ev):
 return max(sum(ar.absbound(ev(s.diff(s.re(q),v)))+ar.absbound(ev(s.diff(s.im(q),v))) for q in mat.row(i) for v in bg) for i in range(mat.rows))
def amplitude(frames,name,scale):
 return max(sum(sum(abs(int(v)) for side in pair for v in side) for pair in row) for f in frames for row in f[name])/R(scale)
def rational_evaluator(environment):
 @lru_cache(None)
 def ev(q):
  if q.is_Rational:return R(int(q.p),int(q.q)),R(int(q.p),int(q.q))
  if q.is_Symbol:return environment[q]
  if q.is_Add:
   z=[ev(x) for x in q.args];return sum((x[0] for x in z),R(0)),sum((x[1] for x in z),R(0))
  if q.is_Mul:
   out=(R(1),R(1))
   for x in q.args:out=mul(out,ev(x))
   return out
  if q.is_Pow and q.exp==s.Rational(1,2) and q.base.is_Rational:
   n,d=int(q.base.p),int(q.base.q)
   if n<0:raise ValueError('Negative real square root')
   scale=2**320;root=isqrt(n*scale*scale//d)
   upper=root if root*root*d==n*scale*scale else root+1
   assert root*root*d<=n*scale*scale<=upper*upper*d
   return R(root,scale),R(upper,scale)
  if q.is_Pow and q.exp.is_Integer:
   lo,hi=ev(q.base);n=int(q.exp)
   if n<0:
    a,b=ev(q.base**(-n))
    if a<=0<=b:raise ZeroDivisionError('Unenclosed denominator')
    return 1/b,1/a
   vals=[lo**n,hi**n]
   if n%2==0 and lo<=0<=hi:vals.append(R(0))
   return min(vals),max(vals)
  raise ValueError('Unsupported audit interval node '+str(q))
 return ev
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS);sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest();assert all(sha(p)==h for p,h in pins.items())
 cert=read(BASE+'a16_numerical_kernel_v1_20261119/receipt.json');src=read(BASE+'a16_finite_state_history_v3_20261116/formulas.json')
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json');un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 sy={n:s.Symbol(n,real=True) for n in bc['background_order']};sy['a']=s.Symbol('a',positive=True);sy['ell']=s.Symbol('ell',positive=True);sy['I']=s.I
 bg=s.Matrix([sy[n] for n in bc['background_order']]);a,H,u,ud,v,vd,r,rd,pd,rho,C=bg;ell=sy['ell']
 mat=lambda name:s.Matrix([[s.sympify(q,locals=sy) for q in row] for row in src[name]])
 original=read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json')
 def imported(name):
  obj=original[name];out=s.zeros(*obj['shape'])
  for entry in obj['entries']:out[entry['row'],entry['column']]=sum(s.sympify(q,locals=sy) for q in entry['terms'])
  return out
 L,Bi=imported('full_generator'),imported('balancing_map_inverse')
 extract=s.zeros(12,20)
 for off,co in [(0,0),(10,6)]:
  extract[co,off]=extract[co,off+2]=s.Rational(1,2)
  for j,i in enumerate([3,6,7,8,9],1):extract[co+j,off+i]=1
 rad=u*u+v*v;potential=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*rad*r*r/28
 flow=s.Matrix([a*H,-s.Rational(5,11)*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho),ud,-3*H*ud-s.diff(potential,u),vd,-3*H*vd-s.diff(potential,v),rd,-3*H*rd-s.diff(potential,r),-3*H*pd-2*rho/15,(-3*H+2*pd/5)*rho,2*pd*C/5])
 dt=lambda m:m.applyfunc(lambda q:sum(s.diff(q,b)*flow[i] for i,b in enumerate(bg)))
 M=mat('mixed_map');pm=mat('pressure_row');rmap=(M[:8,:]*extract).applyfunc(s.cancel);pmap=(pm*M*extract).applyfunc(s.cancel)
 expressions={'D':mat('hidden_generator_D'),'A':mat('retained_generator_A'),'B':mat('hidden_to_retained_B'),'C':mat('retained_to_hidden_C'),'Ph':pm[:,8:],'Pr':pm[:,:8],'Rz':(rmap*Bi).applyfunc(s.cancel),'Pz':(pmap*Bi).applyfunc(s.cancel),'Rdz':((dt(rmap)+rmap*L)*Bi).applyfunc(s.cancel)}
 boxes={sy[n]:(R(z[0])-R(1,100),R(z[1])+R(1,100)) for n,z in un['background_boxes'].items()}
 checks={'main_success_and_physical_hold':cert['passed']==cert['total'] and not cert['physics_pass'] and cert['gate_effect']=='NONE' and cert['review']=='DEFERRED'};decompositions=[];T=R(1,20)
 for row in cert['modes']:
  mode=row['ell'];prefix=str(mode)+'_';ev=rational_evaluator({**boxes,ell:(R(mode),R(mode))})
  for n,expr in expressions.items():
   checks[prefix+n+'_independent_norm']=R(row['norms'][n])>=ar.matrixnorm(expr,ev)
   checks[prefix+n+'_independent_lipschitz']=R(row['lipschitz'][n])>=lipschitz(expr,bg,ev)
  E={n:R(v) for n,v in row['errors'].items()};N={n:R(v) for n,v in row['norms'].items()};Lip={n:R(v) for n,v in row['lipschitz'].items()};loss={n:R(v) for n,v in row['centering_errors'].items()};Mamp={n:R(v) for n,v in row['nominal_amplitudes'].items()};f={n:R(v) for n,v in row['fundamental'].items()}
  eb=f['background_error'];ez=R(row['reference_state_error']);mz=R(row['reference_state_amplitude'])
  checks[prefix+'Gronwall_exponential']=f['absolute_Gronwall_amplification']>=ar.exponential_upper(N['D']*T)
  checks[prefix+'forward_error']=E['U']>=f['absolute_Gronwall_amplification']*T*(f['U_defect']+Lip['D']*eb*f['U_amplitude'])
  checks[prefix+'inverse_error']=E['V']>=f['absolute_Gronwall_amplification']*T*(f['V_defect']+Lip['D']*eb*f['V_amplitude'])
  checks[prefix+'factor_L_error']=E['L']>=N['B']*E['U']+Lip['B']*eb*f['U_amplitude']+loss['L']
  checks[prefix+'factor_Rh_error']=E['Rh']>=N['C']*E['V']+Lip['C']*eb*f['V_amplitude']+loss['Rh']
  checks[prefix+'factor_Lp_error']=E['Lp']>=N['Ph']*E['U']+Lip['Ph']*eb*f['U_amplitude']+loss['Lp']
  checks[prefix+'factor_A_error']=E['A']>=Lip['A']*eb+loss['A'];checks[prefix+'factor_Pr_error']=E['Pr']>=Lip['Pr']*eb+loss['Pr']
  for name,source in [('R','Rz'),('P','Pz'),('Rd','Rdz')]:checks[prefix+name+'_reference_error']=E['reference_'+name]>=N[source]*ez+Lip[source]*eb*mz+loss[name]
  checks[prefix+'retained_kernel_error']=E['kernel_retained']>=E['L']*Mamp['Rh']+Mamp['L']*E['Rh']+E['L']*E['Rh']
  checks[prefix+'pressure_kernel_error']=E['kernel_pressure']>=E['Lp']*Mamp['Rh']+Mamp['Lp']*E['Rh']+E['Lp']*E['Rh']
  checks[prefix+'physical_integral_error']=E['integral_physical']>=T*(E['Rh']*Mamp['R']+Mamp['Rh']*E['reference_R']+E['Rh']*E['reference_R'])
  hp=R(1,mode)+Mamp['I'];ei=E['integral_physical'];hprop=f['hidden_propagator_bound']
  checks[prefix+'pressure_memory_error']=E['pressure_memory']>=N['Pr']*E['reference_R']+E['Pr']*Mamp['R']+E['Lp']*hp+N['Ph']*hprop*ei+loss['memP']
  checks[prefix+'retained_rate_memory_error']=E['retained_rate_memory']>=N['A']*E['reference_R']+E['A']*Mamp['R']+E['L']*hp+N['B']*hprop*ei+loss['memRd']
  checks[prefix+'useful_absolute_accuracy']=all(E[n]<R(1,10**8) for n in ['kernel_retained','kernel_pressure','pressure_memory','retained_rate_memory'])
  checks[prefix+'continuous_reconstruction_control']=all(R(z)<R(1,10**8) for z in row['difference_majorants'].values())
  path=BASE+'a16_numerical_kernel_v1_20261119/ell_'+str(mode)+'/curves.json.gz';raw=(ROOT/path).read_bytes();archive=json.loads(gzip.decompress(raw));frames=archive['frames'];scale=int(archive['dyadic_scale'])
  checks[prefix+'archive_integrity']=hashlib.sha256(raw).hexdigest()==row['archive_sha256'] and len(raw)==row['archive_bytes']
  checks[prefix+'archive_coverage']=len(frames)==row['steps']==archive['steps'] and [q['tile'] for q in frames]==list(range(row['steps'])) and R(archive['T'])==T and archive['degree']==24 and scale==2**256
  checks[prefix+'archive_error_budgets']=archive['physical_error_bounds']==row['errors']
  for n,key in [('L','L'),('Rh','Rh'),('Lp','Lp'),('R_reference','R')]:checks[prefix+n+'_archived_amplitude']=Mamp[key]>=amplitude(frames,n,scale)
  last=frames[-1];rt=endpoint(last['R_reference'],scale);pt=endpoint(last['P_reference'],scale)[0][0]
  rt=[[inflate(z,E['reference_R']) for z in rr] for rr in rt];pt=inflate(pt,E['reference_P'])
  # Exact rational end-background polynomial, enlarged by its certified error.
  bgend=[sum((R(pair[0])*T**j for j,pair in enumerate(rr)),R(0)) for rr in bc['background_coefficients']]
  endev=rational_evaluator({**{q:(v-eb,v+eb) for q,v in zip(bg,bgend)},ell:(R(mode),R(mode))})
  direct=((R(0),R(0)),(R(0),R(0)))
  for j in range(8):direct=cadd(direct,cmul((endev(s.re(pm[0,j])),endev(s.im(pm[0,j]))),rt[j][0]))
  lp=endpoint(last['Lp'],scale)[0][2];initial=inflate((tuple(q/R(mode) for q in lp[0]),tuple(q/R(mode) for q in lp[1])),E['Lp']/mode)
  feedback=cadd(cadd(pt,cneg(direct)),cneg(initial))
  decompositions.append({'ell':mode,'t':str(T),'pressure':repr_interval(pt),'direct_retained_pressure':repr_interval(direct),'hidden_initial_forcing':repr_interval(initial),'history_feedback_pressure':repr_interval(feedback),'meaning':'Term decomposition on the supplied full retained history, not evolution after deleting a term.'})
 checks['inputs_preserved']=all(sha(p)==h for p,h in pins.items())
 result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'endpoint_decomposition':decompositions,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Independent rational coefficient/budget/archive audit and interval endpoint decomposition. Not independent peer review or autonomous retained-only evolution.'}
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False);p=out/'receipt.json';p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')
 print(json.dumps({n:result[n] for n in ['status','passed','total']}));print('Failures:',[n for n,v in checks.items() if not v])
 print('Endpoint pressure contributions:',[(d['ell'],[(n,float(R(d[n][0][0]))) for n in ['pressure','direct_retained_pressure','hidden_initial_forcing','history_feedback_pressure']]) for d in decompositions])
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
