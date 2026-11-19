"""Independent exact-rational interval and pressure-forcing audit; no solver imports."""
from pathlib import Path
from fractions import Fraction as R
from functools import lru_cache
import argparse,hashlib,json,math
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PINS='Theory/Gates/RES-001/RES001_A16_FINITE_STATE_HISTORY_AUDIT_V1_INPUTS_2026-11-16.json'
def read(p):return json.loads((ROOT/p).read_text())
def exponential_upper(x):
 n=max(180,2*math.ceil(x)+20)
 return sum((x**j/math.factorial(j) for j in range(n+1)),R(0))+x**(n+1)/math.factorial(n+1)/(1-x/R(n+2))
def evaluator(environment):
 @lru_cache(None)
 def ev(q):
  if q.is_Rational:return R(int(q.p),int(q.q)),R(int(q.p),int(q.q))
  if q.is_Symbol:return environment[q]
  if q.is_Add:
   z=[ev(x) for x in q.args];return sum((x[0] for x in z),R(0)),sum((x[1] for x in z),R(0))
  if q.is_Mul:
   lo=hi=R(1)
   for x in q.args:
    a,b=ev(x);vals=[lo*a,lo*b,hi*a,hi*b];lo,hi=min(vals),max(vals)
   return lo,hi
  if q.is_Pow and q.exp.is_Integer:
   lo,hi=ev(q.base);n=int(q.exp)
   if n<0:
    a,b=ev(q.base**(-n))
    if a<=0<=b:raise ZeroDivisionError('Unenclosed denominator')
    return 1/b,1/a
   vals=[lo**n,hi**n]
   if n%2==0 and lo<=0<=hi:vals.append(R(0))
   return min(vals),max(vals)
  raise ValueError('Unsupported rational interval node '+str(q))
 return ev
def absbound(pair):return max(abs(pair[0]),abs(pair[1]))
def matrixnorm(mat,ev):
 return max(sum(absbound(ev(s.re(x)))+absbound(ev(s.im(x))) for x in mat.row(i)) for i in range(mat.rows))
def zero(mat):return all(s.cancel(x)==0 for x in mat)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=read(PINS);sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
 assert all(sha(p)==h for p,h in pins.items())
 data=read(BASE+'a16_finite_state_history_v3_20261116/receipt.json');f=read(BASE+'a16_finite_state_history_v3_20261116/formulas.json')
 bc=read(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
 sy={n:s.Symbol(n,real=True) for n in bc['background_order']};sy['a']=s.Symbol('a',positive=True);sy['ell']=s.Symbol('ell',positive=True);sy['I']=s.I
 bg=s.Matrix([sy[n] for n in bc['background_order']]);a,H,u,ud,v,vd,r,rd,pd,rho,C=bg;ell=sy['ell'];p=ell/a
 matrix=lambda name:s.Matrix([[s.sympify(z,locals=sy) for z in row] for row in f[name]])
 K,W,Wdot,D,J,Z=[matrix(name) for name in ['hidden_principal_K','hidden_metric_W','hidden_metric_drift','hidden_generator_D','hidden_principal_J','hidden_energy_half']]
 A,B,Cm=[matrix(name) for name in ['retained_generator_A','hidden_to_retained_B','retained_to_hidden_C']]
 Pr=matrix('pressure_row');Map,Inv=matrix('scalar_map'),matrix('scalar_inverse')
 rad=u*u+v*v;U=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*rad*r*r/28
 flow=s.Matrix([a*H,-s.Rational(5,11)*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho),ud,-3*H*ud-s.diff(U,u),vd,-3*H*vd-s.diff(U,v),rd,-3*H*rd-s.diff(U,r),-3*H*pd-2*rho/15,(-3*H+2*pd/5)*rho,2*pd*C/5])
 dt=lambda mat:mat.applyfunc(lambda q:sum(s.diff(q,b)*flow[i] for i,b in enumerate(bg)))
 checks={
  'direct_trace_of_principal_K':s.cancel(s.trace(K)-2-rad/13)==0,
  'direct_determinant_of_principal_K':s.cancel(K.det()-1-rad/13)==0,
  'independent_scalar_inverse':zero(Map*Inv-s.eye(12)) and zero(Inv*Map-s.eye(12)),
  'weighted_principal_skew':zero(W*J+J.conjugate().T*W),
  'metric_drift_from_independent_background':zero(Wdot-dt(W)),
  'actual_weighted_energy_derivative':zero(2*Z-Wdot-W*D-D.conjugate().T*W),
  'positive_metric_outer_product':zero(W-s.eye(4)-s.diag(s.Matrix([v,-u])*s.Matrix([[v,-u]])/13,s.zeros(2))),
  'V2_V3_matrices_unchanged':(ROOT/(BASE+'a16_finite_state_history_v2_20261116/formulas.json')).read_bytes()==(ROOT/(BASE+'a16_finite_state_history_v3_20261116/formulas.json')).read_bytes(),
  'physical_hold_retained':not data['physics_pass'] and data['gate_effect']=='NONE' and data['review']=='DEFERRED'
 }
 initial=dict(zip(bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 h0=s.Matrix([0,0,1/ell,0]);P_R,P_h=Pr[:,:8],Pr[:,8:]
 hidden_derivative=((dt(P_h)+P_h*D)*h0)[0];retained_derivative=(P_R*B*h0)[0]
 forcing={}
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 boxes={sy[n]:(R(v[0])-R(1,100),R(v[1])+R(1,100)) for n,v in un['background_boxes'].items()}
 details=[];T=R(1,20)
 for row in data['modes']:
  mode=row['ell'];env={**boxes,ell:(R(mode),R(mode))};ev=evaluator(env)
  forcing[mode]={'direct_hidden_pressure_rate':str(s.simplify(hidden_derivative.subs({**initial,ell:mode}))),'retained_pressure_rate':str(s.simplify(retained_derivative.subs({**initial,ell:mode})))}
  checks[f'{mode}_initial_pressure_zero']=s.simplify((P_h*h0)[0].subs({**initial,ell:mode}))==0
  checks[f'{mode}_hidden_initial_data_cannot_be_deleted']=s.simplify((hidden_derivative+retained_derivative).subs({**initial,ell:mode})+s.Rational(2341,840))==0
  for name,mat in [('scalar_map_norm',Map),('scalar_inverse_norm',Inv),('scalar_inverse_drift_norm',dt(Inv)),('B_norm',B),('C_norm',Cm),('pressure_hidden_norm',P_h),('pressure_retained_norm',P_R)]:
   checks[f'{mode}_{name}_rational_interval']=R(row[name])>=matrixnorm(mat,ev)
  independent=[]
  for i in range(4):
   upper=ev(s.re(Z[i,i]))[1]
   for j in range(4):
    if j!=i:upper+=absbound(ev(s.re(Z[i,j])))+absbound(ev(s.im(Z[i,j])))
   independent.append(upper)
  mu=R(row['hidden_mu']);exp=R(row['hidden_exp_mu_T_bound']);conv=R(row['hidden_norm_conversion'])
  checks[f'{mode}_signed_energy_Gershgorin']=mu>=max([R(0)]+independent)
  checks[f'{mode}_whole_interval_positive_chart']=0<R(row['phase_squared_lower'])<=ev(rad)[0] and R(row['momentum_lower'])>0
  checks[f'{mode}_metric_upper']=R(row['hidden_metric_upper'])>=1+ev(rad)[1]/13
  checks[f'{mode}_norm_conversion']=conv**2>=4*R(row['hidden_metric_upper'])
  checks[f'{mode}_exponential_tail']=exp>=exponential_upper(mu*T)
  checks[f'{mode}_full_scalar_amplification']=R(row['scalar_full_propagator_T_bound'])>=R(row['scalar_full_propagator_prefactor'])*exponential_upper(R(3,2))
  bn,cn,ph=[R(row[n]) for n in ['B_norm','C_norm','pressure_hidden_norm']]
  expected={'hidden_propagator_infinity':conv*exp,'retained_initial_forcing':conv*exp*bn,'retained_kernel':conv*exp*bn*cn,'pressure_initial_forcing':conv*exp*ph,'pressure_kernel':conv*exp*ph*cn}
  expected['retained_feedback_integral_per_history_sup']=T*expected['retained_kernel'];expected['pressure_feedback_integral_per_history_sup']=T*expected['pressure_kernel']
  checks[f'{mode}_exact_history_gain_formulas']=all(R(row['gains'][n])>=q for n,q in expected.items())
  details.append({'ell':mode,'independent_energy_row_upper':[str(q) for q in independent]})
 checks['inputs_preserved']=all(sha(p)==h for p,h in pins.items())
 result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'forcing_rate_decomposition':forcing,'independent_energy_bounds':details,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Independent exact-rational box and weighted-energy/gain audit with direct hidden-data pressure response; no independent peer review or physical-domain promotion.'}
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False);q=out/'receipt.json';q.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8');Path(str(q)+'.sha256').write_text(hashlib.sha256(q.read_bytes()).hexdigest()+'  '+q.name+'\n',encoding='utf-8')
 print(json.dumps({n:result[n] for n in ['status','passed','total']}));print('Failures:',[n for n,v in checks.items() if not v]);print('Forcing:',forcing)
 if not all(checks.values()):raise SystemExit(1)
if __name__=='__main__':main()
