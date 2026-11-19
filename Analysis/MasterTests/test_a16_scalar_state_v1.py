"""Reconstructed scalar state in unchanged B1; no physical gate clearance."""
from pathlib import Path
import sys,argparse,hashlib,json
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_remainder_v1 as old
PINS='Theory/Gates/RES-001/RES001_A16_SCALAR_STATE_V1_INPUTS_2026-11-16.json'
DATA='Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
 data=json.loads((ROOT/DATA).read_text());imp=lambda k:old.parent.import_matrix(data[k],bg.sy)
 L=imp('full_generator');F=imp('full_field_reconstruction');O=imp('actual_dust_observable')
 # Constant original-chart SO(2) scalar/tensor/transverse decomposition.
 E=s.zeros(20,12);T=s.zeros(20,8)
 for offset,coff in [(0,0),(10,6)]:
  E[offset,coff]=1;E[offset+2,coff]=1
  for j,i in enumerate([3,6,7,8,9],1):E[offset+i,coff+j]=1
 for offset,coff in [(0,0),(10,4)]:
  T[offset,coff]=1;T[offset+2,coff]=-1
  for j,i in enumerate([1,4,5],1):T[offset+i,coff+j]=1
 full=E.row_join(T);P=full.inv();Ls=P*L*full
 checks={}
 def zero(name,m):checks[name]=all(s.cancel(x)==0 for x in m)
 zero('constant_decomposition_inverse',P*full-s.eye(20))
 zero('scalar_rates_independent_of_tensor_transverse',Ls[:12,12:])
 zero('complement_rates_independent_of_scalars',Ls[12:,:12])
 alpha=F[0,:];area=(F[7,:]+F[9,:])/2;vx=F[10,:]
 density=2*u*F[13,:]+2*v*F[14,:];rad=u*u+v*v
 phase=(-v*F[13,:]+u*F[14,:])/rad
 configs=[area,vx,density,phase,F[15,:],F[16,:]]
 bg_rates=[None,None,2*u*ud+2*v*vd,(u*vd-v*ud)/rad,rd,pd]
 proper=[]
 for i,row in enumerate(configs):
  rate=bg.dt(row)+row*L
  if i>=2:rate-=bg_rates[i]*alpha
  proper.append(rate)
 Q=s.Matrix.vstack(*(configs+proper));Qdot=bg.dt(Q);B=Qdot+Q*L
 zero('reconstructed_state_has_no_tensor_transverse_part',Q*T)
 zero('dust_has_no_tensor_transverse_part',O*T)
 zero('state_rate_has_no_tensor_transverse_part',B*T)
 polar=s.Matrix([[2*u,2*v],[-v/rad,u/rad]])
 zero('density_phase_inverse',polar*s.Matrix([[u/(2*rad),-v],[v/(2*rad),u]])-s.eye(2))
 checks['density_phase_determinant_two']=s.cancel(polar.det()-2)==0
 zero('area_reconstruction',area*E-s.eye(12)[0,:])
 zero('frame_reconstruction',vx*E-s.eye(12)[1,:])
 checks['scalar_lapse_rate_correction_retained']=any(s.cancel(x)!=0 for x in proper[5]-(bg.dt(configs[5])+configs[5]*L))
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 checks['registered_background_on_shell']=s.simplify(bg.constraint.subs(init))==0
 results=[]
 for mode in [4,8,16,32,64]:
  point={**init,bg.ell:mode};ev=lambda m:m.applyfunc(lambda x:s.cancel(x.subs(point)))
  q=ev(Q*E);b=ev(B*E);qd=ev(Qdot*E);o=ev(O*E)
  domain=lambda m:DM.from_Matrix(m,extension=True).to_field()
  dq=domain(q);rank=dq.rank();stack=domain(q.col_join(b)).rank();row={'ell':mode,'map_rank':rank,'stacked_rank':stack}
  checks[f'{mode}_coefficient_drift_nonzero']=any(x!=0 for x in qd)
  if rank==12:
   qi=dq.inv().to_Matrix();generator=(b*qi).applyfunc(s.cancel);dust=(o*qi).applyfunc(s.cancel)
   zero(f'{mode}_initial_generator_recomposition',generator*q-b)
   zero(f'{mode}_dust_recomposition',dust*q-o)
   zero(f'{mode}_inverse_identity',qi*q-s.eye(12))
   row.update(closed_initial=True,determinant=str(s.factor(q.det())),generator=[[str(x) for x in r] for r in generator.tolist()],dust_map=[[str(x) for x in r] for r in dust.tolist()])
  else:
   kernel=dq.nullspace().to_Matrix();w=[]
   for i in range(kernel.rows):
    d=kernel[i,:].T;y=(b*d).applyfunc(s.simplify)
    if any(x!=0 for x in y):
     zero(f'{mode}_null_witness',q*d);w=[str(x) for x in d];break
   row.update(closed_initial=stack==rank,witness=w)
  results.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ['generator','dust_map','witness']}),flush=True)
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 receipt={'status':'PASS_RECONSTRUCTED_SCALAR_STATE_CONTROL','checks':checks,'inputs':pins,'configuration_order':['transverse_area','longitudinal_frame','condensate_density','condensate_phase','reservoir','force'],'rate_conventions':['coordinate','coordinate','normalized_frame','normalized_frame','normalized_frame','normalized_frame'],'results':results,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Exact symbolic scalar block split and registered initial map/generator; no time-uniform map inverse, positive energy, physical gauge/source admission or thermodynamic reservoir.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
