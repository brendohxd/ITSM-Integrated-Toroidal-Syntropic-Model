"""Finite-time scalar chart and actual condensate-block history gains in B1."""
from pathlib import Path
from fractions import Fraction as Rat
import argparse,hashlib,json,sys
import sympy as s

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(Path(__file__).parent))
import test_01_r4c1_g3n5_dust_certified_numerical_v1 as c
k=c.k
PINS='Theory/Gates/RES-001/RES001_A16_FINITE_STATE_HISTORY_V1_INPUTS_2026-11-16.json'
BASE='Analysis/MasterTests/outputs/'
T=Rat(1,20)
def read(p):return json.loads((ROOT/p).read_text())
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def clean(m):return m.applyfunc(s.cancel)
def serial(m):return [[str(z) for z in row] for row in m.tolist()]
def exact(q):return Rat(q.p,q.q) if q.is_Rational else q
def save(p,o):
 p.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n',encoding='utf-8')
 Path(str(p)+'.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n',encoding='utf-8')

def fixture(checks):
 t,z=s.symbols('t z',real=True);D=s.zeros(3);D[0,1]=1;D[1,2]=t
 U=s.eye(3);U[0,1]=t-z;U[1,2]=(t*t-z*z)/2;U[0,2]=t**3/6-t*z*z/2+z**3/3
 checks['fixture_exact_noncommuting_propagator']=clean(s.diff(U,t)-D*U)==s.zeros(3)
 checks['fixture_identity_at_diagonal']=clean(U.subs(t,z)-s.eye(3))==s.zeros(3)
 checks['fixture_noncommutation_retained']=clean(D*D.subs(t,z)-D.subs(t,z)*D)!=s.zeros(3)
 h0=s.Matrix([1,2,-1]);src=s.Matrix([z,1,z*z]);retained=1+z+z*z
 h=U.subs(z,0)*h0+s.integrate(U*src*retained,(z,0,t))
 checks['fixture_volterra_hidden_equation']=clean(s.diff(h,t)-D*h-s.Matrix([t,1,t*t])*(1+t+t*t))==s.zeros(3,1)
 B=s.Matrix([[1,t,t*t]]);Ph=s.Matrix([[1,1,t]])
 for name,row in [('retained',B),('pressure',Ph)]:
  rhs=row*U.subs(z,0)*h0+s.integrate(row*U*src*retained,(z,0,t))
  checks['fixture_'+name+'_initial_and_feedback']=s.simplify((row*h-rhs)[0])==0
  checks['fixture_'+name+'_initial_term_not_omitted']=s.simplify((row*U.subs(z,0)*h0)[0])!=0
 frozen=s.eye(3)+(t-z)*D+(t-z)**2*D*D/2
 checks['fixture_frozen_exponential_rejected']=clean(s.diff(frozen,t)-D*frozen)!=s.zeros(3)

def calculate():
 pins=read(PINS);before={p:(digest(p),(ROOT/p).stat().st_mtime_ns) for p in pins}
 assert all(before[p][0]==h for p,h in pins.items()),'input drift'
 bg=c.old.Background();a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;p=ell/a;beta=s.Rational(2,5)
 mats={name:c.old.parent.import_matrix(obj,bg.sy) for name,obj in read(BASE+'r4c1_g3n5_dust_finite_k_attempt_01/matrices.json').items()}
 L,F,Bal,Bali=[mats[z] for z in ['full_generator','full_field_reconstruction','balancing_map','balancing_map_inverse']]
 checks={}
 def zero(name,m):checks[name]=all(x==0 for x in clean(m))
 E=s.zeros(20,12);Tc=s.zeros(20,8)
 for off,co in [(0,0),(10,6)]:
  E[off,co]=E[off+2,co]=1
  for j,i in enumerate([3,6,7,8,9],1):E[off+i,co+j]=1
 for off,co in [(0,0),(10,4)]:
  Tc[off,co]=1;Tc[off+2,co]=-1
  for j,i in enumerate([1,4,5],1):Tc[off+i,co+j]=1
 full=E.row_join(Tc);decomp=full.inv();Ls=clean(decomp[:12,:]*L*E)
 zero('scalar_block_invariance',decomp[12:,:]*L*E)
 zero('complement_block_invariance',decomp[:12,:]*L*Tc)
 alpha=F[0,:];area=(F[7,:]+F[9,:])/2
 configs=[area,F[10,:],2*u*F[13,:]+2*v*F[14,:],(-v*F[13,:]+u*F[14,:])/(u*u+v*v),F[15,:],F[16,:]]
 bgrates=[None,None,2*u*ud+2*v*vd,(u*vd-v*ud)/(u*u+v*v),rd,pd]
 rates=[]
 for i,row in enumerate(configs):
  q=bg.dt(row)+row*L
  if i>=2:q-=bgrates[i]*alpha
  rates.append(q)
 Qfull=clean(s.Matrix.vstack(*(configs+rates)));S=clean(Qfull*E)
 zero('scalar_observation_annihilates_complement',Qfull*Tc)
 zero('clock_lapse_exact',alpha*E+beta*s.eye(12)[5,:])
 A=S[:6,:6];Dmap=S[6:,:6]
 zero('configuration_has_no_velocity_block',S[:6,6:])
 zero('rate_velocity_block_matches_configurations',S[6:,6:]-A)
 Ai=s.eye(6);rad=u*u+v*v
 Ai[2,2]=u/(2*rad);Ai[2,3]=-v;Ai[3,2]=v/(2*rad);Ai[3,3]=u
 zero('independent_polar_inverse',A*Ai-s.eye(6))
 checks['configuration_determinant_two']=s.cancel(A.det()-2)==0
 Si=clean(Ai.row_join(s.zeros(6)).col_join((-Ai*Dmap*Ai).row_join(Ai)))
 zero('full_scalar_inverse_left',Si*S-s.eye(12));zero('full_scalar_inverse_right',S*Si-s.eye(12))
 checks['scalar_determinant_four_on_regular_chart']=s.cancel(A.det()**2-4)==0
 Sdot=bg.dt(S);Sidot=bg.dt(Si)
 zero('inverse_drift_identity',Sdot*Si+S*Sidot)
 Gs=clean((Sdot+S*Ls)*Si)
 zero('finite_scalar_generator_recomposition',Gs*S-Sdot-S*Ls)
 checks['scalar_drift_cannot_be_omitted']=any(x!=0 for x in clean(Sdot*Si))
 retained=[0,1,4,5,6,7,10,11]
 proper=lambda row,rate:bg.dt(row)+row*L-rate*alpha
 hidden=[F[13,:],F[14,:],proper(F[13,:],ud)/p,proper(F[14,:],vd)/p]
 M=clean(s.Matrix.vstack(*(list(Qfull[retained,:].row(i) for i in range(8))+hidden))*E)
 Mi=s.zeros(12)
 for i,j in [(0,0),(1,1),(2,8),(3,9),(4,2),(5,3),(6,4),(7,5),(10,6),(11,7)]:Mi[i,j]=1
 Mi[8,10]=p;Mi[9,11]=p
 for i,vel in [(8,ud),(9,vd),(10,rd),(11,pd)]:Mi[i,3]=-beta*vel
 zero('mixed_split_inverse_left',Mi*M-s.eye(12));zero('mixed_split_inverse_right',M*Mi-s.eye(12))
 pp=s.Symbol('pp',positive=True);Mp=M.copy()
 for i in [10,11]:
  for j in range(12):Mp[i,j]=clean(s.Matrix([M[i,j]*p/pp]))[0]
 Mdot_explicit=(bg.dt(Mp)-H*pp*Mp.diff(pp)).subs(pp,p)
 zero('momentum_drift_total_derivative',Mdot_explicit-bg.dt(M))
 Gen=clean((bg.dt(M)+M*Ls)*Mi)
 zero('mixed_generator_recomposition',Gen*M-bg.dt(M)-M*Ls)
 drift_omission=clean((bg.dt(Mp).subs(pp,p)+M*Ls)*Mi-Gen)
 expected=s.zeros(12);expected[10,10]=expected[11,11]=-H
 zero('omitted_momentum_drift_exact_defect',drift_omission-expected)
 checks['momentum_drift_omission_is_nonzero']=drift_omission!=s.zeros(12)
 Ar,Br,Cr,Dh=Gen[:8,:8],Gen[:8,8:],Gen[8:,:8],Gen[8:,8:]
 J=s.zeros(4);J[:2,2:]=s.eye(2);J[2:,:2]=-s.eye(2)
 zero('candidate_wave_principal_is_skew',J+J.conjugate().T)
 Sym=clean((Dh+Dh.conjugate().T)/2)
 zero('hidden_energy_principal_cancellation',Sym-(Dh-p*J+(Dh-p*J).conjugate().T)/2)
 residual=clean(Dh-p*J)
 checks['hidden_residual_has_no_growing_momentum_power']=all(x==0 or s.degree(s.fraction(x)[0],ell)<=s.degree(s.fraction(x)[1],ell) for x in residual)
 kinetic_bg=ud*ud+vd*vd+rd*rd;U=s.expand(bg.energy-(kinetic_bg+3*pd*pd)/2-rho)
 P=ud*proper(F[13,:],ud)+vd*proper(F[14,:],vd)+rd*proper(F[15,:],rd)
 P-=sum((s.diff(U,q)*F[i,:] for q,i in [(u,13),(v,14),(r,15)]),s.zeros(1,20))
 Pmix=clean(P*E*Mi);Pexpected=s.zeros(1,12)
 Pexpected[2]=-s.diff(U,r);Pexpected[6]=rd
 Pexpected[8]=-s.diff(U,u);Pexpected[9]=-s.diff(U,v);Pexpected[10]=p*ud;Pexpected[11]=p*vd
 zero('independent_canonical_pressure_observation',Pmix-Pexpected)
 zero('pressure_reconstruction',Pmix*M-P*E)
 fixture(checks)
 print(json.dumps({'symbolic_checks':sum(checks.values()),'total':len(checks),'failures':[n for n,q in checks.items() if not q]}),flush=True)
 un=read(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
 boxes={bg.sy[name]:k.IV(k.IV.fraction(Rat(z[0])-Rat(1,100)).lo,k.IV.fraction(Rat(z[1])+Rat(1,100)).hi) for name,z in un['background_boxes'].items()}
 ev=c.evaluators(boxes);phase_lower=ev(rad).lo
 checks['whole_interval_phase_patch_positive']=phase_lower>0
 checks['whole_interval_background_denominators_positive']=all(boxes[q].lo>0 for q in [a,rho,C])
 oldcert=read(BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01/certificate.json')
 checks['inherited_background_continuation_margin']=Rat(oldcert['background']['continuation_margin'])>Rat(oldcert['background']['error'])
 norm=lambda mat:Rat(c.matrix_norm(mat,ev),k.SCALE)
 initial=dict(zip(bg.bg,[s.Integer(1),s.sqrt(s.Rational(3469,4620)),s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(1),s.Integer(1),s.Rational(1,4),s.Rational(1,5),s.Rational(1,5),s.Integer(1)]))
 rows=[]
 for mode in [4,8,16,32,64]:
  print('ell='+str(mode)+' computing whole-box map and history gains',flush=True)
  sub=lambda mat:mat.subs(ell,mode)
  # Re-evaluate the actual Hermitian hidden generator at each mode.
  herm=sub(Sym);bounds=[]
  for i in range(4):
   re,im=s.expand_complex(herm[i,i]).as_real_imag();assert im==0;upper=ev(re).hi
   for j in range(4):
    if j!=i:
     re,im=s.expand_complex(herm[i,j]).as_real_imag();upper+=ev(re).abs_upper()+ev(im).abs_upper()
   bounds.append(upper)
  mu=max([0]+bounds);exph=Rat(k.exp_upper(k.IV(mu).scale(T.numerator,T.denominator)),k.SCALE)
  bn,cn,prn,phn=[norm(sub(mat)) for mat in [Br,Cr,Pmix[:,:8],Pmix[:,8:]]]
  co=next(q['constants'] for q in oldcert['modes'] if q['ell']==mode)
  forward=norm(sub(Qfull*Bali));inverse=norm(sub(Bal*E*Si))
  prefactor=forward*Rat(co['K_inverse_Q_to_infinity'])*Rat(co['K_T_infinity_to_Q'])*inverse
  fullamp=prefactor*Rat(k.exp_upper(k.IV.rational(3,2)),k.SCALE)
  gains={'hidden_propagator_infinity':2*exph,'retained_initial_forcing':2*bn*exph,'retained_kernel':2*bn*cn*exph,'pressure_initial_forcing':2*phn*exph,'pressure_kernel':2*phn*cn*exph}
  gains['retained_feedback_integral_per_history_sup']=T*gains['retained_kernel']
  gains['pressure_feedback_integral_per_history_sup']=T*gains['pressure_kernel']
  entries={'ell':mode,'phase_squared_lower':str(Rat(phase_lower,k.SCALE)),'momentum_lower':str(Rat(mode)/Rat(boxes[a].hi,k.SCALE)),'scalar_map_norm':str(norm(sub(S))),'scalar_inverse_norm':str(norm(sub(Si))),'scalar_inverse_drift_norm':str(norm(sub(Sidot))),'physical_to_balanced_norm':str(inverse),'balanced_to_physical_norm':str(forward),'scalar_full_propagator_prefactor':str(prefactor),'scalar_full_propagator_T_bound':str(fullamp),'hidden_mu':str(Rat(mu,k.SCALE)),'hidden_gershgorin_rows':[str(Rat(q,k.SCALE)) for q in bounds],'hidden_exp_mu_T_bound':str(exph),'B_norm':str(bn),'C_norm':str(cn),'pressure_retained_norm':str(prn),'pressure_hidden_norm':str(phn),'gains':{n:str(q) for n,q in gains.items()}}
  checks[str(mode)+'_all_chart_and_gain_bounds_finite_positive']=all(q>=0 for q in gains.values()) and entries['momentum_lower']!='0' and phase_lower>0
  # Initial hidden seed has no retained entries, and is not zeroed by elimination.
  original=s.zeros(12,1);original[8]=1;new=clean((sub(M)*original).subs(initial))
  zero(str(mode)+'_radial_seed_retained_zero',new[:8,:])
  target=s.zeros(4,1);target[2]=s.Rational(1,mode)
  zero(str(mode)+'_radial_seed_hidden_normalization',new[8:,:]-target)
  rows.append(entries)
  print(json.dumps({'ell':mode,'hidden_mu':float(Rat(mu,k.SCALE)),'hidden_exp_bound':float(exph),'kernel_bound':float(gains['retained_kernel'])}),flush=True)
 checks['immutable_input_hashes_and_timestamps']=all((digest(p),(ROOT/p).stat().st_mtime_ns)==before[p] for p in pins)
 result={'status':'PASS_FINITE_SCALAR_CHART_AND_BOUNDED_HISTORY' if all(checks.values()) else 'FAIL_FINITE_SCALAR_CHART_AND_BOUNDED_HISTORY','checks':checks,'passed':sum(checks.values()),'total':len(checks),'inputs':pins,'domain':{'t':['0','1/20'],'ell':[4,8,16,32,64],'phase':'u^2+v^2>0, local linear chart only'},'retained_order':['area','Vx','r','Pi','area_coordinate_rate','Vx_coordinate_rate','proper_r_rate','proper_force_rate'],'hidden_order':['delta_u','delta_v','proper_u_rate/p','proper_v_rate/p'],'modes':rows,'physics_pass':False,'gate_effect':'NONE','review':'DEFERRED','scope':'Exact finite-time scalar map and bounded deterministic 8+4 history law. No evaluated numerical two-time kernel, useful instantaneous approximation, irreversible bath, entropy, physical window or matching clearance.'}
 formulas={'scalar_map':serial(S),'scalar_inverse':serial(Si),'scalar_generator':serial(Gs),'mixed_map':serial(M),'mixed_inverse':serial(Mi),'retained_generator_A':serial(Ar),'hidden_to_retained_B':serial(Br),'retained_to_hidden_C':serial(Cr),'hidden_generator_D':serial(Dh),'hidden_hermitian_part':serial(Sym),'pressure_row':serial(Pmix),'history_law':['Rdot=A R+B U_D(t,0) h0+integral_0^t B(t)U_D(t,s)C(s)R(s) ds','P=P_R R+P_h U_D(t,0) h0+integral_0^t P_h(t)U_D(t,s)C(s)R(s) ds'],'hidden_propagator_rule':'partial_t U_D(t,s)=D(t)U_D(t,s), U_D(s,s)=I; no frozen exponential'}
 return result,formulas

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True);args=ap.parse_args()
 out=ROOT/args.output_dir;out.mkdir(parents=True,exist_ok=False)
 result,formulas=calculate();save(out/'receipt.json',result);save(out/'formulas.json',formulas)
 print(json.dumps({n:result[n] for n in ['status','passed','total','physics_pass']}))
 if result['passed']!=result['total']:raise SystemExit(1)
if __name__=='__main__':main()
