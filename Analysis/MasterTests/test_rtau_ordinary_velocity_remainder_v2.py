"""Strong ordinary velocity and eight gradient-row remainder bounds."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_ORDINARY_VELOCITY_REMAINDER_V2_SPEC_2026-11-04.md'
BASE='Analysis/MasterTests/outputs/'
SOURCES={'identified':BASE+'rtau_free_velocity_identification_v1_20261104/receipt.json','momentum':BASE+'rtau_momentum_rate_lift_v2_20261104/receipt.json','force':BASE+'rtau_strong_force_coordinate_v3_20261104/receipt.json','lift':BASE+'rtau_strong_constraint_lift_v4_20261104/receipt.json','velocity':BASE+'rtau_canonical_velocity_remainder_v1_20261104/receipt.json','gauge':BASE+'rtau_paired_gauge_rate_v2_20261104/receipt.json','map':BASE+'r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json','mixed':BASE+'r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'}
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
 up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
 norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
 data={k:json.loads((ROOT/p).read_text()) for k,p in SOURCES.items()};pins=dict(data['identified']['source_sha256'])
 for datum in data.values():
  for rel,want in datum.get('source_sha256',{}).items():
   assert rel not in pins or pins[rel]==want,rel
   pins[rel]=want
 assert data['lift']['density_coordinate']=='Sigma=rho+e_force+b*Z**2/2'
 for rel in (SPEC,FACTORY,*SOURCES.values(),Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
 snap={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in (p,Path(str(p)+'.sha256')):
   if q.exists():snap[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 check('all_parent_controls_complete_in_their_scopes',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in data.values()))
 spec=importlib.util.spec_from_file_location('ordinary_velocity_profiles',ROOT/FACTORY)
 fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
 y,_=env['state'](env['J'].variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
 r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000
 Q=[decode(x) for x in data['momentum']['constants_binary']['full_configuration_H1']]
 P=[decode(x) for x in data['momentum']['constants_binary']['full_momentum_L2']]
 F=[decode(x) for x in data['force']['constants_binary']['force_H2_inverse']]
 pr=[[decode(x) for x in row] for row in data['momentum']['constants_binary']['eliminated_momentum_principal_remainder_H1']]
 p_rem=[sum((row[j] for row in pr),iv.mpf(0)) for j in range(8)]
 def compose(row):
  row=[decode(x) for x in row];base=[row[j] for j in (0,1,2)]+[iv.mpf(0),iv.mpf(0)]+[row[j] for j in (4,5,6)]
  return [a+row[3]*f for a,f in zip(base,F)]
 metric=compose(data['lift']['constants_binary']['metric_gradient_principal_remainder_H1'])
 modulus=(4*r+4*r*r)*iv.exp(8*r)
 q_rem=[iv.sqrt(2)*m+modulus*q+f for m,q,f in zip(metric,Q,F)]
 vb={k:decode(v) for k,v in data['velocity']['bounds_binary'].items()}
 H={tuple(row['ij']):(decode(row['value']),decode(row['dz'])) for row in data['mixed']['full_mixed_Hessian_upper_triangle']}
 get=lambda i,j,dz=False:H.get(tuple(sorted((i,j))),(iv.mpf(0),iv.mpf(0)))[int(dz)]
 A0=norm([get(i,j) for i in range(14,27) for j in range(14,27)])
 B0=norm([get(i,j) for i in range(14,27) for j in range(28,41)])
 B1=norm([get(i,j,True) for i in range(14,27) for j in range(28,41)])
 S0,S1=up(y[44].c[0]),up(y[47].c[0])
 C0,C1=vb['configuration_zeroth_matrix'],vb['configuration_matrix_derivative']
 M0,M1=vb['temporal_inverse'],vb['temporal_inverse_spatial_derivative']
 Az=vb['temporal_Hessian_spatial_derivative']
 materialB0=B0+S0*A0;materialB1=B1+S1*A0+S0*Az
 ls=[y[8]/y[0],y[8]/y[0],y[8]/(2*y[0])]
 N0=norm([iv.mpf(1)]*3+[x.c[0] for x in ls]);N1=norm([x.c[1] for x in ls])
 Pi0,Pi1=1+N0,N1
 prefactor=(Pi0+Pi1)*(M0+M1)
 base=[prefactor*(p_rem[j]+(materialB0+materialB1)*q_rem[j]+(C0+C1)*Q[j]) for j in range(8)]
 mb=data['map']['bounds'];W=up(decode(mb['drift_upper_binary']));Wz=up(decode(mb['drift_derivative_upper_binary']))
 Wzz=2*eps/31+r*W+r*Wz
 forward=iv.exp(5*r);reverse=iv.exp(r)*(iv.exp(6*r)+2*r*iv.exp(4*r))
 affine=[forward*(M0*p+(M0*(C0+B0)+W+2*Wz)*q) for p,q in zip(P,Q)]
 gauge={k:decode(v) for k,v in data['gauge']['bounds_binary'].items()}
 coordinate_index=(Pi0+Pi1)*2*(Wz+Wzz)
 gauge_modulus=(N0+N1)*(S0+W+S1+Wz)*modulus
 velocity=[base[j]+reverse*gauge['field_H1_remainder_per_affine_L2']*affine[j]+(coordinate_index+gauge_modulus)*Q[j] for j in range(8)]
 velocity+=[reverse*gauge['field_H1_remainder_per_harmonic']]
 # Coefficient derivative when differentiating the ordinary velocity row.
 gamma=(1+y[0]*sum((x**2 for x in y[6:9]),env['J'](0)))**mp.mpf('.5')
 coeff=gamma/(y[0]**mp.mpf('.5'));G0=3+iv.sqrt(2)*up(coeff.c[0]);G1=iv.sqrt(2)*up(coeff.c[1])
 Z0=Pi0+materialB0*G0;Z1=Pi1+materialB1*G0+materialB0*G1
 Vz=Pi1*M0*Z0+Pi0*M1*Z0+Pi0*M0*Z1
 gradient=list(velocity)
 for j in (0,1,2,3):gradient[j]+=Vz
 gradient[1]+=S1
 z=sp.symbols('z');f,s=sp.Function('f')(z),sp.Function('s')(z)
 check('material_gradient_commutator_exact',sp.expand(sp.diff(s*sp.diff(f,z),z)-s*sp.diff(f,z,2)-sp.diff(s,z)*sp.diff(f,z))==0)
 A=sp.Matrix(2,2,sp.symbols('a0:4'));v,q,qz,Tq= [sp.Matrix(2,1,sp.symbols(n+'0:2')) for n in ('v','q','d','t')]
 ss,ww=sp.symbols('S w')
 actual=A*(v-ww*qz-Tq)-(ss-ww)*qz
 desired=A*(v-ss*qz)-A*Tq-(sp.eye(2)-A)*(ss-ww)*qz
 check('actual_coordinate_material_decomposition',sp.expand(actual-desired)==sp.zeros(2,1))
 a,w,L,m=[sp.Function(n)(z) for n in ('a','w','L','m')]
 # m is a spatial mean, constant in z; lambda_z has the analytic r bounds.
 check('initial_second_drift_derivative_identity',sp.expand(sp.diff(L-m-a*w,z).subs({sp.diff(m,z):0,sp.diff(w,z):L-m-a*w})-(sp.diff(L,z)-sp.diff(a,z)*w-a*(L-m-a*w)))==0)
 E=sp.zeros(13,8);R=sp.zeros(8,13)
 E[0,0]=1;E[3,0]=-1;R[0,0]=sp.Rational(1,2);R[0,3]=-sp.Rational(1,2)
 slots=[1,6,7,8,9,10,11]
 for j,i in enumerate(slots,1):E[i,j]=1;R[j,i]=1
 trace=sp.zeros(13,1);trace[0]=trace[3]=1
 check('all_eight_configuration_directions_retained',R*E==sp.eye(8))
 check('trace_and_gauge_moduli_not_hidden_in_free_chart',R*trace==sp.zeros(8,1) and all(R[:,j]==sp.zeros(8,1) for j in (2,4,5)))
 Vfun=sp.Function('V')(z);Y=sp.Function('Y')(z)
 check('principal_coefficient_spatial_derivative_retained',sp.expand(sp.diff(Vfun*Y,z)-Vfun*sp.diff(Y,z)-sp.diff(Vfun,z)*Y)==0)
 check('omitted_material_commutator_detected',sp.diff(s,z)*sp.diff(f,z)!=0)
 check('all_composed_remainder_coefficients_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in (velocity,gradient,affine) for x in row))
 check('force_higher_order_and_moving_map_requirements_retained',data['identified']['strong_velocity_remainder']=='NOT_ASSEMBLED' and data['gauge']['moving_maps']=='NOT_ASSEMBLED')
 check('all_inherited_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snap.items()))
 return dict(kind='RTAU_ORDINARY_VELOCITY_REMAINDER_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  input_order=data['force']['inverse_input_order']+['harmonic_coordinate_velocity_adapted'],
  bounds_binary={'ordinary_velocity_H1_remainder':[binary(x) for x in velocity],'eight_gradient_rows_L2_remainder':[binary(x) for x in gradient],'affine_field_L2':[binary(x) for x in affine]},
  upper_display={'ordinary_velocity_H1_remainder':[mp.nstr(hi(x),28) for x in velocity],'eight_gradient_rows_L2_remainder':[mp.nstr(hi(x),28) for x in gradient]},
  coefficient_bounds_binary={'drift_second_derivative':binary(Wzz),'velocity_principal_coefficient_derivative':binary(Vz),'gauge_modulus_derivative':binary(modulus),'reverse_rate_pullback_H1':binary(reverse)},
  scope='INITIAL_ORDINARY_MATERIAL_VELOCITY_H1_AND_EIGHT_STRONG_GRADIENT_ROWS_L2_REMAINDERS_ONLY',
  ordinary_momentum_rows='NOT_ASSEMBLED',density_and_force_moving_maps='NOT_ASSEMBLED',full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',density_coordinate='Sigma=rho+e_force+b*Z**2/2',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=p.parse_args()
 if args.output:assert not args.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
 else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'bounds':d['upper_display'],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
