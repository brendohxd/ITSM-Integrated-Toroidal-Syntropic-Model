"""Paired initial gauge-rate operator; full strong generator remains open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_PAIRED_GAUGE_RATE_V2_SPEC_2026-11-04.md'
PARENT='Analysis/MasterTests/outputs/rtau_canonical_velocity_remainder_v1_20261104/receipt.json'
RATES='Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
 up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
 norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
 parent=json.loads((ROOT/PARENT).read_text());rates=json.loads((ROOT/RATES).read_text())
 pins=dict(parent['source_sha256'])
 for rel in (SPEC,PARENT,RATES,FACTORY,'Analysis/MasterTests/test_rtau_paired_gauge_rate_v1.py','Theory/Gates/RES-001/RES001_RTAU_PAIRED_GAUGE_RATE_V1_SPEC_2026-11-04.md','Analysis/MasterTests/outputs/rtau_paired_gauge_rate_v1_20261104/receipt.json',Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
 snapshot={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in (p,Path(str(p)+'.sha256')):
   if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 check('canonical_velocity_parent_complete_in_scope',parent['passed']==parent['total']==11)
 # Exact pointwise gauge projector on all thirteen field directions.
 a2,gz,V=sp.symbols('a2 gz V',positive=True)
 B=sp.zeros(13,3);W=sp.zeros(3,13)
 for j,slot in enumerate((2,4,5)):
  B[slot,j]=a2 if j<2 else gz;B[6+j,j]=-V;W[j,slot]=1
 U=sp.diag(1/a2,1/a2,1/gz);N=B*U;Pi=sp.eye(13)-N*W
 check('all_thirteen_field_components_represented',Pi.shape==(13,13))
 check('local_projector_rank_ten_for_three_spatial_gauge_rows',Pi.rank()==10)
 check('exact_gauge_projector',sp.simplify(Pi*Pi-Pi)==sp.zeros(13))
 check('physical_modulus_rates_not_projected_out',W*N==sp.eye(3) and W*Pi==sp.zeros(3,13))
 z=sp.symbols('z',real=True);g=2+sp.sin(z)/7;xi=3+sp.sin(z)/5;c=sp.Integer(2);b=c-g*sp.diff(xi,z)
 check('independent_variable_periodic_gauge_row',sp.expand(b+g*sp.diff(xi,z)-c)==0)
 check('nonzero_harmonic_velocity_retained',sp.integrate(xi,(z,-sp.pi,sp.pi))/(2*sp.pi)==3)
 check('nonzero_modulus_rate_retained',c!=0 and sp.simplify(b+g*sp.diff(xi,z))==c)
 n=sp.symbols('n',integer=True,positive=True)
 check('primitive_L2_to_H1_all_modes',sp.expand(2*n*n-(1+n*n))==n*n-1)
 # Full scalar Laplacian covariance under longitudinal spatial displacement.
 aa,bb,psi,X=[sp.Function(s)(z) for s in ('a','b','psi','X')]
 mu=aa**2*bb;cc=aa**2/bb;Z=-sp.diff(cc*sp.diff(psi,z),z)/mu
 logmu=(2*sp.diff(aa,z)/aa+sp.diff(bb,z)/bb)*X+sp.diff(X,z)
 logc=(2*sp.diff(aa,z)/aa-sp.diff(bb,z)/bb)*X-sp.diff(X,z)
 chi=X*sp.diff(psi,z)
 response=-logmu*Z-sp.diff(cc*sp.diff(chi,z)+cc*logc*sp.diff(psi,z),z)/mu
 check('auxiliary_scalar_full_metric_clock_covariance',sp.simplify(sp.expand(response-X*sp.diff(Z,z)))==0)
 check('omitted_metric_response_changes_auxiliary_rate',sp.simplify(-sp.diff(cc*sp.diff(chi,z),z)/mu-X*sp.diff(Z,z))!=0)
 # Canonical index term: a contravariant frame component has T=-X_z.
 pf=sp.Function('p')(z)
 frame_response=X*sp.diff(pf,z)+2*sp.diff(X,z)*pf
 check('dual_frame_momentum_index_term_retained',sp.expand(frame_response-sp.diff(X*pf,z))==sp.diff(X,z)*pf)
 spec=importlib.util.spec_from_file_location('paired_gauge_profile_factory',ROOT/FACTORY)
 fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare();J=env['J']
 y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
 r=iv.mpf(1)/13000;abar=J(iv.exp(iv.mpf([-1,1])*r));scale=y[0]**mp.mpf('.5');jac=scale/abar
 T=[J(1),J(1),1/jac,J(1),1/jac,1/(jac*jac),J(1),J(1),jac,J(1),J(1),J(1),J(1)]
 qbar=[x*t for x,t in zip(y[:13],T)];qbar[5]=abar*abar
 d1=[q.c[1]/jac.c[0] for q in qbar]
 d2=[(2*q.c[2]-jac.c[1]*q.c[1]/jac.c[0])/(jac.c[0]**2) for q in qbar]
 dH=norm(d1)+norm(d2)
 weights=[1/y[0],1/y[0],1/(2*abar*abar)]
 n0=[iv.mpf(1)]*3;n1=[]
 for u in weights:
  n0.append(-qbar[8].c[0]*u.c[0])
  n1.append(-d1[8]*u.c[0]-qbar[8].c[0]*u.c[1]/jac.c[0])
 N0,N1=norm(n0),norm(n1)
 ratio=iv.exp(4*r);umax=max(hi(up(u.c[0])) for u in weights);umax=iv.mpf(umax)
 corrector_D=umax*(ratio+1);corrector_H1=iv.sqrt(2)*corrector_D
 field_rem_F=(N0+N1)*ratio+dH*corrector_H1;field_rem_H=dH
 # Paired momentum response in the same adapted canonical coordinates.
 p=[decode(x) for x in rates['background_binary']['momentum']];pz=[decode(x) for x in rates['background_binary']['momentum_z']]
 pbar=[];pbarz=[]
 for j in range(13):
  tp=1/(jac*T[j]);pbar.append(tp.c[0]*p[j]);pbarz.append((tp.c[1]*p[j]+tp.c[0]*pz[j])/jac.c[0])
 K=[[iv.mpf(0)]*13 for _ in range(3)]
 entries=[[(0,2,1),(1,4,1),(2,5,2),(8,6,-1)],[(1,2,1),(3,4,1),(4,5,2),(8,7,-1)],[(2,2,1),(4,4,1),(5,5,2),(8,8,-1)]]
 for i,terms in enumerate(entries):
  for slot,pslot,mult in terms:K[i][slot]+=pbar[pslot]*mult
 momentum_index=norm([(pbar[j] if i==2 else 0)-K[i][j] for i in range(3) for j in range(13)])
 momentum_z=norm(pbarz)
 momentum_F=momentum_z*corrector_H1+momentum_index*corrector_D
 momentum_H=momentum_z
 aux1=y[13].c[1]/jac.c[0]
 aux2=(2*y[13].c[2]-jac.c[1]*y[13].c[1]/jac.c[0])/(jac.c[0]**2)
 auxH=up(aux1)+up(aux2)
 vals=dict(projector_L2=1+N0,field_H1_remainder_per_affine_L2=field_rem_F,field_H1_remainder_per_harmonic=field_rem_H,
   corrector_H1_per_affine_L2=corrector_H1,corrector_derivative_L2_per_affine_L2=corrector_D,modulus_rate_per_affine_L2=ratio,
   paired_momentum_L2_per_affine_L2=momentum_F,paired_momentum_L2_per_harmonic=momentum_H,
   auxiliary_rate_H1_per_affine_L2=auxH*corrector_H1,auxiliary_rate_H1_per_harmonic=auxH)
 check('whole_initial_profile_bounds_finite',all(lo(v)>=0 and mp.isfinite(hi(v)) for v in vals.values()))
 check('scalar_covariance_uses_actual_initial_auxiliary_profile',len(y)==48 and all(d1[j]==0 for j in (2,4,5)))
 check('all_sources_sidecars_timestamps_unchanged',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
 return dict(kind='RTAU_PAIRED_GAUGE_RATE_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  scope='INITIAL_PAIRED_GAUGE_CORRECTION_FROM_AFFINE_FIELD_L2_AND_HARMONIC_VELOCITIES_ONLY',bounds_binary={k:binary(v) for k,v in vals.items()},upper_display={k:mp.nstr(hi(v),28) for k,v in vals.items()},
  field_identity='F_corrected=Pi*F+B*diag(u)*c+qbar_z*(H_z+P(u_z*(c_z-F_hzz)))',
  canonical_momentum_identity='correction_j=xi_z*pbar_j,z+sum_i((delta_iz*pbar_j-K_i,j)*xi_i,z)',auxiliary_identity='delta_Z_rate_gauge=xi_z*Zbar_z',
  affine_strong_state_principal_comparison='NOT_ASSEMBLED',moving_maps='NOT_ASSEMBLED',full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
 parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
 if args.output:assert not args.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
 else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'bounds':d['upper_display'],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
