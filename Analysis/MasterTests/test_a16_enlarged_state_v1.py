"""Exact initial retained-state closure; no finite-time extrapolation."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parents[2]
PINS='Theory/Gates/RES-001/RES001_A16_ENLARGED_STATE_V1_INPUTS_2026-11-15.json'
DATA='Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for p,h in pins.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 names=['a','H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho_m','C']
 sy={n:s.Symbol(n,real=True) for n in names};sy.update(ell=s.Symbol('ell',positive=True),I=s.I,sqrt=s.sqrt)
 a,H,u,ud,v,vd,r,rd,pd,rho,C=[sy[n] for n in names]
 rad=u*u+v*v;V=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*rad*r*r/28
 rates=[a*H,-s.Rational(5,11)*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho),ud,-3*H*ud-s.diff(V,u),vd,-3*H*vd-s.diff(V,v),rd,-3*H*rd-s.diff(V,r),-3*H*pd-s.Rational(2,15)*rho,(-3*H+s.Rational(2,5)*pd)*rho,s.Rational(2,5)*pd*C]
 initial=dict(zip([sy[n] for n in names],[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 data=json.loads((ROOT/DATA).read_text());checks={};results=[]
 def matrix(name,rows=None):
  obj=data[name];nr,nc=obj['shape'];m=s.zeros(nr if rows is None else len(rows),nc)
  for e in obj['entries']:
   if rows is None or e['row'] in rows:m[e['row'] if rows is None else rows.index(e['row']),e['column']]=sum(s.sympify(x,locals=sy) for x in e['terms'])
  return m
 L=matrix('full_generator');O=matrix('actual_dust_observable');field=matrix('full_field_reconstruction',[0,16]);alpha,Pi=field[0,:],field[1,:]
 # Pi is the original tenth chart coordinate; its coordinate-time rate is slot 19.
 epi=s.zeros(1,20);epi[0,9]=1;epid=s.zeros(1,20);epid[0,19]=1
 checks['force_field_reconstruction']=Pi==epi
 checks['coordinate_force_rate_reconstruction']=Pi*L==epid
 proper=epid-pd*alpha;Aplus=O.col_join(Pi).col_join(proper)
 def ev(m,point):return m.applyfunc(lambda e:s.cancel(e.subs(point)))
 def derivative_at(m,point):
  vals=[s.cancel(x.subs(point)) for x in rates]
  return m.applyfunc(lambda e:s.cancel(sum(s.diff(e,sy[n]).subs(point)*val for n,val in zip(names,vals) if sy[n] in e.free_symbols)))
 def domain(m):return DomainMatrix.from_Matrix(m,extension=True).to_field()
 for mode in [4,8,16,32,64]:
  point={**initial,sy['ell']:s.Integer(mode)};Lp=ev(L,point)
  obs=ev(Aplus,point);drift=derivative_at(Aplus,point);rate=drift+obs*Lp
  cases={}
  for label,n in [('dust',2),('dust_force',4)]:
   A=obs[:n,:];B=rate[:n,:];da=domain(A);ra=da.rank();rab=domain(A.col_join(B)).rank()
   kernel=da.nullspace().to_Matrix();witness=None
   for i in range(kernel.rows):
    d=kernel[i,:].T;y=B*d
    if any(s.simplify(x)!=0 for x in y):
     assert all(s.simplify(x)==0 for x in A*d)
     witness={'direction':[str(s.simplify(x)) for x in d],'retained_rate_difference':[str(s.simplify(x)) for x in y]};break
   checks[f'{mode}_{label}_rank_nullspace_agree']=(rab>ra)==(witness is not None)
   checks[f'{mode}_{label}_retained_rows_independent']=ra==n
   cases[label]={'retained_rank':ra,'stacked_rank':rab,'initial_closed':rab==ra,'witness':witness}
  # In-memory omission comparisons do not change the actual calculation.
  checks[f'{mode}_lapse_term_retained']=any(x!=0 for x in obs[3,:]-ev(epid,point))
  checks[f'{mode}_background_drift_retained']=any(x!=0 for x in drift)
  results.append({'ell':mode,'cases':cases})
  print(f'ell={mode}: '+str({k:(v['retained_rank'],v['stacked_rank']) for k,v in cases.items()}),flush=True)
 assert all(checks.values()),[k for k,vv in checks.items() if not vv]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 receipt={'status':'PASS_INITIAL_RANK_AND_NULLSPACE_CONTROL','checks':checks,'inputs':pins,'results':results,'observable_definition':['D','Vx','Pi in fixed gauge','Pi_dot-psi_dot*alpha'],'physics_pass':False,'review':'DEFERRED','gate_effect':'NONE','scope':'Exact registered initial event and nonzero modes; witnesses are initial chart directions, not certified finite-time new trajectories or isolated reservoir interventions.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
