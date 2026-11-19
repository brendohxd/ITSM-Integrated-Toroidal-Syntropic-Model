"""Exact coefficient jets and bounded six/eight-row initial closure."""
from pathlib import Path
from functools import lru_cache
import argparse,hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
ROOT=Path(__file__).resolve().parents[2]
PINS='Theory/Gates/RES-001/RES001_A16_RESPONSE_COMBINATIONS_V1_INPUTS_2026-11-16.json'
DATA='Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json'
K=s.QQ.algebraic_field(s.sqrt(2),s.sqrt(s.Rational(3469,4620)),s.I)
N=4;Z=K.zero;ONE=K.one
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):return tuple(sum((a[j]*b[n-j] for j in range(n+1)),Z) for n in range(N))
def inv(a):
 if a[0]==Z:raise ZeroDivisionError('zero jet denominator')
 out=[ONE/a[0]]
 for n in range(1,N):out.append(-sum((a[j]*out[n-j] for j in range(1,n+1)),Z)/a[0])
 return tuple(out)
def powj(a,n):
 if n<0:return powj(inv(a),-n)
 out=(ONE,Z,Z,Z)
 while n:
  if n%2:out=mul(out,a)
  a=mul(a,a);n//=2
 return out
def mat(rows):return DM(rows,(len(rows),len(rows[0])),K)
def transport(A,L):
 return [A[n+1].scalarmul(K.convert(n+1))+sum_dm([A[j].matmul(L[n-j]) for j in range(n+1)]) for n in range(len(A)-1)]
def sum_dm(xs):
 out=xs[0]
 for x in xs[1:]:out=out+x
 return out
def select(A,B,limit):
 chosen=[];current=A;rank=A.rank()
 for i in range(B.shape[0]):
  row=B.extract([i],list(range(20)));trial=current.vstack(row);nr=trial.rank()
  if nr>rank:chosen.append(i);current=trial;rank=nr
  if len(chosen)==limit:break
 return chosen
def check_state(A,B):
 ra=A.rank();rb=A.vstack(B).rank();basis=A.nullspace();w=None
 for i in range(basis.shape[0]):
  d=basis.extract([i],list(range(20))).transpose();y=B.matmul(d)
  if not y.is_zero_matrix:
   assert A.matmul(d).is_zero_matrix
   w={'direction':[str(x) for x in d.to_Matrix()],'rate_difference':[str(x) for x in y.to_Matrix()]};break
 assert (rb>ra)==(w is not None)
 return {'retained_rank':ra,'stacked_rank':rb,'closed_at_initial_point':rb==ra,'witness':w,'map':[[str(x) for x in row] for row in A.to_Matrix().tolist()]}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for p,h in pins.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 names=['a','H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho_m','C'];sy={n:s.Symbol(n,real=True) for n in names};sy.update(ell=s.Symbol('ell',positive=True),I=s.I,sqrt=s.sqrt)
 bg=[sy[n] for n in names];a,H,u,ud,v,vd,r,rd,pd,rho,C=bg
 rad=u*u+v*v;V=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*rad*r*r/28
 rates=[a*H,-s.Rational(5,11)*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho),ud,-3*H*ud-s.diff(V,u),vd,-3*H*vd-s.diff(V,v),rd,-3*H*rd-s.diff(V,r),-3*H*pd-s.Rational(2,15)*rho,(-3*H+s.Rational(2,5)*pd)*rho,s.Rational(2,5)*pd*C]
 values=[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]
 data=json.loads((ROOT/DATA).read_text())
 def parse(name,rows=None):
  obj=data[name];nr,nc=obj['shape'];out=s.zeros(nr if rows is None else len(rows),nc)
  for e in obj['entries']:
   if rows is None or e['row'] in rows:out[e['row'] if rows is None else rows.index(e['row']),e['column']]=sum(s.sympify(t,locals=sy) for t in e['terms'])
  return out
 L=parse('full_generator');O=parse('actual_dust_observable');fields=parse('full_field_reconstruction',[0,16]);alpha,Pi=fields[0,:],fields[1,:]
 epi=s.zeros(1,20);epi[0,9]=1;ed=s.zeros(1,20);ed[0,19]=1
 assert Pi==epi and Pi*L==ed
 A4=O.col_join(Pi).col_join(ed-pd*alpha)
 checks={'actual_force_field_and_rate':True}
 rational=mul((ONE,ONE,Z,Z),inv((ONE,-ONE,Z,Z)));checks['rational_reciprocal_jet']=rational==(ONE,K.convert(2),K.convert(2),K.convert(2))
 try:inv((Z,ONE,Z,Z));checks['reject_zero_denominator']=False
 except ZeroDivisionError:checks['reject_zero_denominator']=True
 def evaluate_with(jets,mode):
  @lru_cache(None)
  def ev(e):
   if not e.free_symbols:return (K.from_sympy(e),Z,Z,Z)
   if e in jets:return jets[e]
   if e==sy['ell']:return (K.convert(mode),Z,Z,Z)
   if e.is_Add:
    out=(Z,Z,Z,Z)
    for t in e.args:out=add(out,ev(t))
    return out
   if e.is_Mul:
    out=(ONE,Z,Z,Z)
    for t in e.args:out=mul(out,ev(t))
    return out
   if e.is_Pow and e.exp.is_Integer:return powj(ev(e.base),int(e.exp))
   raise ValueError(str(e))
  return ev
 jets={x:(K.from_sympy(val),Z,Z,Z) for x,val in zip(bg,values)}
 for order in range(1,N):
  ev=evaluate_with(jets,4);coeff=[ev(q)[order-1]/K.convert(order) for q in rates]
  jets={x:tuple(coeff[i] if j==order else jets[x][j] for j in range(N)) for i,x in enumerate(bg)}
 point=dict(zip(bg,values));point[sy['ell']]=4;ev=evaluate_with(jets,4)
 # Independent direct differentiation of two nontrivial observation coefficients.
 def dt(e):return sum(s.diff(e,x)*v for x,v in zip(bg,rates) if x in e.free_symbols)
 for label,expr in [('dust',A4[0,0]),('lapse_rate',A4[3,0])]:
  d=expr
  for n in range(3):
   checks[f'direct_symbolic_{label}_derivative_{n}']=K.from_sympy(s.cancel(d.subs(point)))/K.convert(s.factorial(n))==ev(expr)[n]
   if n<2:d=dt(d)
 energy=(ud*ud+vd*vd+rd*rd+3*pd*pd)/2+V+rho
 checks['initial_friedmann_shell']=s.simplify((s.Rational(33,10)*H*H-energy).subs(point))==0
 results=[]
 for mode in [4,8,16,32,64]:
  ev=evaluate_with(jets,mode)
  def matrix_jets(expr):
   q=[[ev(expr[i,j]) for j in range(expr.cols)] for i in range(expr.rows)]
   return [mat([[q[i][j][n] for j in range(expr.cols)] for i in range(expr.rows)]) for n in range(N)]
  Lj=matrix_jets(L);Aj=matrix_jets(A4);Bj=transport(Aj,Lj)
  inherited=check_state(Aj[0],Bj[0]);checks[f'{mode}_inherited_4_6']=(inherited['retained_rank'],inherited['stacked_rank'])==(4,6)
  selected=select(Aj[0],Bj[0],2);checks[f'{mode}_two_extra_rows']=len(selected)==2
  six=[Aj[n].vstack(Bj[n].extract(selected,list(range(20)))) for n in range(3)];Bsix=transport(six,Lj)
  rsix=check_state(six[0],Bsix[0]);row={'ell':mode,'six_added_rate_indices':selected,'six':rsix}
  checks[f'{mode}_six_has_coefficient_drift']=not six[1].is_zero_matrix
  if not rsix['closed_at_initial_point']:
   sel8=select(six[0],Bsix[0],2)
   eight=[six[n].vstack(Bsix[n].extract(sel8,list(range(20)))) for n in range(2)]
   Beight=transport(eight,Lj);row.update(eight_added_six_rate_indices=sel8,eight=check_state(eight[0],Beight[0]))
   checks[f'{mode}_eight_has_coefficient_drift']=not eight[1].is_zero_matrix
  results.append(row)
  print(json.dumps({'ell':mode,'selected':selected,'six_ranks':[rsix['retained_rank'],rsix['stacked_rank']],'eight_ranks':None if 'eight' not in row else [row['eight']['retained_rank'],row['eight']['stacked_rank']]}),flush=True)
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 p=out/'receipt.json';receipt={'checks':checks,'inputs':pins,'results':results,'status':'PASS_BOUNDED_INITIAL_RESPONSE_ROW_TEST','physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Exact Taylor jets and registered initial nonzero modes; no time tube, physical gauge/source admission or minimal-state theorem.'}
 p.write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
