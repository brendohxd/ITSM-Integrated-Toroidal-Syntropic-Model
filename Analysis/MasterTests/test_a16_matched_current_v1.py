"""Actual current and geometry matching under two declared condensate preps."""
from pathlib import Path
import sys,argparse,json,hashlib
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_remainder_v1 as old
PINS='Theory/Gates/RES-001/RES001_A16_MATCHED_CURRENT_V1_INPUTS_2026-11-16.json'
BASE='Analysis/MasterTests/outputs/'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;beta=s.Rational(2,5)
 data=json.loads((ROOT/(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json')).read_text());imp=lambda n:old.parent.import_matrix(data[n],bg.sy)
 L,F,O=[imp(n) for n in ['full_generator','full_field_reconstruction','actual_dust_observable']]
 E=s.zeros(20,12)
 for off,col in [(0,0),(10,6)]:
  E[off,col]=E[off+2,col]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,col+j]=1
 rad=u*u+v*v;alpha=F[0,:];area=(F[7,:]+F[9,:])/2
 configs=[area,F[10,:],2*u*F[13,:]+2*v*F[14,:],(-v*F[13,:]+u*F[14,:])/rad,F[15,:],F[16,:]]
 br=[None,None,2*u*ud+2*v*vd,(u*vd-v*ud)/rad,rd,pd];rates=[]
 for i,q in enumerate(configs):
  qr=bg.dt(q)+q*L
  if i>=2:qr-=br[i]*alpha
  rates.append(qr)
 Q=s.Matrix.vstack(*(configs+rates));B=bg.dt(O)+O*L
 N=s.I*ell/a*O[0,:]+(F[4,:]+F[7,:]+F[9,:])/2-beta*F[16,:]
 flux=-s.I*ell/(a*a*C)*F[17,:]-F[1,:]/a
 checks={};results=[]
 def zero(name,m):checks[name]=all(s.simplify(z)==0 for z in m)
 zero('clock_current_continuity_symbolic',(bg.dt(N)+N*L+s.I*ell*flux).applyfunc(bg.shell))
 zero('clock_multiplier_symbolic',(bg.dt(F[17,:])+F[17,:]*L-C*alpha-beta*C*F[16,:]).applyfunc(bg.shell))
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 for mode in [4,8,16,32,64]:
  point={**init,ell:mode};clean=lambda m:m.applyfunc(s.cancel);ev=lambda m:clean(m.subs(point))
  q=ev(Q*E);qi=DM.from_Matrix(q,extension=True).to_field().inv().to_Matrix();lift=E*qi
  observe=clean(ev(O)*lift);number=clean(ev(N)*lift);flow=clean(ev(flux)*lift)
  G=clean(ev(bg.dt(Q)+Q*L)*lift)
  number_rate=clean(ev(bg.dt(N)+N*L)*lift);dust_rate=clean(ev(B)*lift);flow_rate=clean(ev(bg.dt(flux)+flux*L)*lift)
  response=s.Matrix.vstack(dust_rate,number_rate,flow_rate,G[1,:],G[6,:])
  records=[]
  for input_name,index in [('reservoir_configuration',4),('reservoir_normalized_rate',10)]:
   preps=[]
   for label,cols in [('phase_and_phase_rate',[3,9]),('phase_and_modulus',[3,2])]:
    Cmat=s.Matrix([[number[0,j] for j in cols],[flow[0,j] for j in cols]])
    assert s.simplify(Cmat.det())!=0,'Declared compensation is singular'
    coeff=clean(-Cmat.inv()*s.Matrix([number[0,index],flow[0,index]]))
    y=s.zeros(12,1);y[index]=1
    for j,val in zip(cols,coeff):y[j]=val
    x=clean(lift*y);tag=f'{mode}_{index}_{label}'
    zero(tag+'_reconstructed_state',ev(Q)*x-y)
    zero(tag+'_matched_current',s.Matrix.vstack(number,flow)*y)
    zero(tag+'_matched_dust',observe*y)
    zero(tag+'_matched_geometry_frame_force',y.extract([0,1,5,6,11],[0]))
    zero(tag+'_zero_lapse_and_shift',ev(s.Matrix.vstack(alpha,F[1,:]))*x)
    zero(tag+'_zero_conserved_density_rate',number_rate*y)
    zero(tag+'_zero_energy_density_rate',dust_rate[0,:]*y)
    zero(tag+'_direct_response',ev(s.Matrix.vstack(B,bg.dt(N)+N*L,bg.dt(flux)+flux*L,(bg.dt(Q)+Q*L)[1,:],(bg.dt(Q)+Q*L)[6,:]))*x-response*y)
    output=clean(response*y)
    preps.append({'protocol':label,'compensation_slots':cols,'compensation':[str(z) for z in coeff],'scalar_state':[str(z) for z in y],'full_initial_direction':[str(z) for z in x],'response':[str(z) for z in output]})
   y1,y2=[s.Matrix([s.sympify(z) for z in p['scalar_state']]) for p in preps];diff=y1-y2
   zero(f'{mode}_{index}_same_reservoir',diff.extract([4,10],[0]));zero(f'{mode}_{index}_same_current',s.Matrix.vstack(number,flow)*diff)
   delta=clean(response*diff)
   records.append({'reservoir_input':input_name,'preparations':preps,'response_difference':[str(z) for z in delta],'responses_identical':all(s.simplify(z)==0 for z in delta)})
  results.append({'ell':mode,'records':records});print(json.dumps({'ell':mode,'identical':[x['responses_identical'] for x in records],'differences':[x['response_difference'] for x in records]}),flush=True)
 assert all(checks.values()),[k for k,vv in checks.items() if not vv]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 receipt={'status':'PASS_MATCHED_CURRENT_GEOMETRY_INITIAL_COMPARISON','checks':checks,'inputs':pins,'response_order':['D_dot','Vx_dot','N_tau_dot','F_tau_dot','Vx_dot_crosscheck','area_ddot'],'results':results,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Declared same-clock linear initial preparations. No isolated reservoir source, finite-time certificate, invariant curvature/force or thermal mechanism.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
