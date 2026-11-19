"""Pressure-rate sufficiency under exact named current/geometry/state holds."""
from pathlib import Path
import sys,argparse,json,hashlib
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_remainder_v1 as old
PINS='Theory/Gates/RES-001/RES001_A16_PRESSURE_STATE_V1_INPUTS_2026-11-16.json'
DATA='Analysis/MasterTests/outputs/r4c1_g3n5_dust_finite_k_attempt_01/matrices.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 pins=json.loads((ROOT/PINS).read_text())
 for f,h in pins.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 bg=old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;beta=s.Rational(2,5)
 data=json.loads((ROOT/DATA).read_text());imp=lambda k:old.parent.import_matrix(data[k],bg.sy)
 L,F,O=[imp(k) for k in ['full_generator','full_field_reconstruction','actual_dust_observable']]
 E=s.zeros(20,12)
 for off,col in [(0,0),(10,6)]:
  E[off,col]=E[off+2,col]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,col+j]=1
 alpha=F[0,:];area=(F[7,:]+F[9,:])/2;Pi=F[16,:]
 proper=lambda row,rate:bg.dt(row)+row*L-rate*alpha
 force_rate=proper(Pi,pd);reservoir_rate=proper(F[15,:],rd)
 kinetic_bg=ud*ud+vd*vd+rd*rd
 U=s.expand(bg.energy-(kinetic_bg+3*pd*pd)/2-rho)
 kinetic=ud*proper(F[13,:],ud)+vd*proper(F[14,:],vd)+rd*proper(F[15,:],rd)
 potential=sum((s.diff(U,q)*F[i,:] for q,i in [(u,13),(v,14),(r,15)]),s.zeros(1,20))
 energy=kinetic+potential;pressure=kinetic-potential
 pressure_bg=kinetic_bg/2-U
 pressure_rate=bg.dt(pressure)+pressure*L-bg.dt(s.Matrix([pressure_bg]))[0]*alpha
 modulus=2*u*F[13,:]+2*v*F[14,:];modulus_rate=proper(modulus,2*u*ud+2*v*vd)
 number=s.I*ell/a*O[0,:]+(F[4,:]+F[7,:]+F[9,:])/2-beta*Pi
 flux=-s.I*ell/(a*a*C)*F[17,:]-F[1,:]/a
 held_names=['N_tau','F_tau','area','area_coordinate_rate','Vx','Pi','P_n','reservoir','reservoir_normalized_rate','scalar_energy']
 held=s.Matrix.vstack(number,flux,area,bg.dt(area)+area*L,F[10,:],Pi,force_rate,F[15,:],reservoir_rate,energy)
 init=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 checks={};results=[]
 checks['pressure_lapse_rate_correction_retained']=any(s.cancel(x)!=0 for x in pressure_rate-(bg.dt(pressure)+pressure*L))
 checks['pressure_background_drift_retained']=any(s.cancel(x)!=0 for x in bg.dt(pressure))
 for mode in [4,8,16,32,64]:
  point={**init,ell:mode};ev=lambda m:m.subs(point).applyfunc(s.cancel)
  h=ev(held*E);p=ev(pressure*E);pr=ev(pressure_rate*E);m=ev(modulus_rate*E)
  hp=h.col_join(p);full=hp.col_join(m)
  dom=lambda q:DM.from_Matrix(q,extension=True).to_field()
  dh=dom(hp);rank=dh.rank();rate_rank=dom(hp.col_join(pr)).rank();full_rank=dom(full).rank()
  kernel=dh.nullspace().to_Matrix();witnesses=[]
  for i in range(kernel.rows):
   d=kernel[i,:].T
   assert all(s.simplify(x)==0 for x in hp*d)
   witnesses.append({'direction':[str(s.simplify(x)) for x in d],'pressure_rate':str(s.simplify((pr*d)[0])),'modulus_rate':str(s.simplify((m*d)[0]))})
  checks[f'{mode}_rank_nullspace_dimension']=kernel.rows==12-rank
  witness_changes=any(s.sympify(w['pressure_rate'])!=0 for w in witnesses)
  checks[f'{mode}_rank_witness_agreement']=(rate_rank>rank)==witness_changes
  row={'ell':mode,'held_rank':dom(h).rank(),'held_plus_pressure_rank':rank,'plus_pressure_rate_rank':rate_rank,'plus_modulus_rate_rank':full_rank,'witnesses':witnesses}
  if full_rank==12:
   inv=dom(full).inv().to_Matrix();coeff=(pr*inv).applyfunc(s.cancel)
   checks[f'{mode}_pressure_rate_factorization']=all(s.simplify(x)==0 for x in coeff*full-pr)
   row['pressure_rate_coefficients']=[str(x) for x in coeff]
   row['modulus_rate_coefficient']=str(coeff[-1])
  # Distinct explicit canonical-field control, not a rank-selected basis.
  radial=s.zeros(12,1);radial[8]=1 # delta u_dot, other original scalar slots zero.
  checks[f'{mode}_radial_direction_preserves_all_holds']=all(s.simplify(x)==0 for x in hp*radial)
  checks[f'{mode}_radial_modulus_rate_two']=s.simplify((m*radial)[0]-2)==0
  expected=-2*s.diff(U,u).subs(point)
  checks[f'{mode}_direct_canonical_pressure_derivative']=s.simplify((pr*radial)[0]-expected)==0
  if full_rank==12:checks[f'{mode}_quotient_matches_canonical_derivative']=s.simplify(coeff[-1]+s.diff(U,u).subs(point))==0
  results.append(row)
  print(json.dumps({'ell':mode,'ranks':[row['held_rank'],rank,rate_rank,full_rank],'modulus_rate_coefficient':row.get('modulus_rate_coefficient')}),flush=True)
 assert all(checks.values()),[k for k,vv in checks.items() if not vv]
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 o={'status':'PASS_INITIAL_PRESSURE_STATE_INFORMATION_CONTROL','checks':checks,'inputs':pins,'held_row_names':held_names+['scalar_pressure','normalized_modulus_squared_rate'],'results':results,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Canonical combined scalar pressure at the registered initial event. Not a material equation of state, irreversible bath, physical-domain certificate or finite-time constitutive closure.'}
 p=out/'receipt.json';p.write_bytes((json.dumps(o,sort_keys=True,indent=2)+'\n').encode());Path(str(p)+'.sha256').write_bytes((hashlib.sha256(p.read_bytes()).hexdigest()+'  receipt.json\n').encode());print(json.dumps({'passed':sum(checks.values()),'total':len(checks)}))
if __name__=='__main__':main()
