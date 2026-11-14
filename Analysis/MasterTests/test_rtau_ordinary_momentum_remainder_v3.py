"""Nine actual ordinary canonical momentum-row L2 remainders; force open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_ORDINARY_MOMENTUM_REMAINDER_V3_SPEC_2026-11-04.md'
BASE='Analysis/MasterTests/outputs/'
SOURCES={'parent':BASE+'rtau_ordinary_velocity_remainder_v2_20261104/receipt.json','momentum':BASE+'rtau_momentum_rate_lift_v2_20261104/receipt.json','force':BASE+'rtau_strong_force_coordinate_v3_20261104/receipt.json','lift':BASE+'rtau_strong_constraint_lift_v4_20261104/receipt.json','velocity':BASE+'rtau_canonical_velocity_remainder_v1_20261104/receipt.json','gauge':BASE+'rtau_paired_gauge_rate_v2_20261104/receipt.json','mixed':BASE+'r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'}
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
ORD=[0,1,3,6,7,8,9,10,11]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
 up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
 norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
 data={k:json.loads((ROOT/p).read_text()) for k,p in SOURCES.items()};pins=dict(data['parent']['source_sha256'])
 for datum in data.values():
  for rel,want in datum.get('source_sha256',{}).items():
   assert rel not in pins or pins[rel]==want,rel
   pins[rel]=want
 assert data['lift']['density_coordinate']=='Sigma=rho+e_force+b*Z**2/2'
 for rel in (SPEC,FACTORY,'Analysis/MasterTests/test_rtau_ordinary_momentum_remainder_v1.py','Theory/Gates/RES-001/RES001_RTAU_ORDINARY_MOMENTUM_REMAINDER_V1_SPEC_2026-11-04.md','Analysis/MasterTests/outputs/rtau_ordinary_momentum_remainder_v1_20261104/failure.json',*SOURCES.values(),Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
 snap={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in (p,Path(str(p)+'.sha256')):
   if q.exists():snap[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 check('all_parent_controls_complete_only_in_scope',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in data.values()))
 # Independent exact noncommuting block-action fixture, not a selected state.
 E=sp.eye(4)[:,:2];Bg=sp.Matrix([[sp.Rational(1,7),sp.Rational(2,13)],[sp.Rational(3,11),-sp.Rational(1,17)],[2,0],[0,3]])
 A=sp.diag(2,3,4,5);A[0,3]=A[3,0]=sp.Rational(1,19);A[1,2]=A[2,1]=sp.Rational(2,23)
 D=sp.Matrix(4,4,lambda i,j:sp.Rational(2*i-j+1,29+i+j));G=sp.diag(3,-2,4,1)
 K=Bg.T*A*Bg;M=E.T*(A-A*Bg*K.inv()*Bg.T*A)*E
 C=E.T*(D-A*Bg*K.inv()*Bg.T*D)*E;Gr=E.T*(G-D.T*Bg*K.inv()*Bg.T*D)*E
 P=sp.Matrix(sp.symbols('p0:2'));X=sp.Matrix(sp.symbols('x0:2'));v=M.inv()*(P-C*X)
 nu=-K.inv()*Bg.T*(A*E*v+D*E*X);vr=E*v+Bg*nu
 check('exact_canonical_flux_Schur_identity',sp.simplify(E.T*(D.T*vr+G*E*X)-C.T*v-Gr*X)==sp.zeros(2,1))
 check('exact_fixture_momentum_and_constraint',sp.simplify(E.T*(A*vr+D*E*X)-P)==sp.zeros(2,1) and sp.simplify(Bg.T*(A*vr+D*E*X))==sp.zeros(2,1))
 z=sp.symbols('z');S=sp.Function('S')(z);p=sp.Function('p')(z);flux=sp.Function('F')(z)
 check('material_flux_commutator_exact',sp.expand(-sp.diff(flux,z)-S*sp.diff(p,z)+sp.diff(flux+S*p,z)-sp.diff(S,z)*p)==0)
 aa,bb,cc,gg,vv,q,x=sp.symbols('a b c g v q x')
 pp=aa*vv+(bb+S*aa)*x+cc*q
 old=bb*(vv+S*x)+gg*x+S*pp+sp.Symbol('dq')*q
 target=(bb+S*aa)*vv+(gg+2*S*bb+S*S*aa)*x+(sp.Symbol('dq')+S*cc)*q
 check('zeroth_order_material_flux_retained',sp.expand(old-target)==0)
 check('omitted_zeroth_flux_changes_rate',sp.diff((sp.Function('C')(z)*sp.Function('q')(z)),z)!=0)
 T=sp.symbols('T',nonzero=True);Lw,gc,p0=sp.symbols('Lw gc p0')
 check('paired_moving_coordinate_momentum_cancellation',sp.expand((T*(p0-Lw)+gc)/T+Lw-p0-gc/T)==0)
 Q=[decode(x) for x in data['momentum']['constants_binary']['full_configuration_H1']]
 Pc=[decode(x) for x in data['momentum']['constants_binary']['full_momentum_L2']]
 F=[decode(x) for x in data['force']['constants_binary']['force_H2_inverse']]
 rp=[[decode(x) for x in row] for row in data['momentum']['constants_binary']['eliminated_momentum_principal_remainder_H1']]
 Rp=[sum((row[j] for row in rp),iv.mpf(0)) for j in range(8)]
 row=[decode(x) for x in data['lift']['constants_binary']['metric_gradient_principal_remainder_H1']]
 base=[row[j] for j in (0,1,2)]+[iv.mpf(0),iv.mpf(0)]+[row[j] for j in (4,5,6)]
 metric=[a+row[3]*f for a,f in zip(base,F)]
 r=iv.mpf(1)/13000;modulus=(4*r+4*r*r)*iv.exp(8*r)
 Rq=[iv.sqrt(2)*m+modulus*q+f for m,q,f in zip(metric,Q,F)]
 H={tuple(row['ij']):(decode(row['value']),decode(row['dz'])) for row in data['mixed']['full_mixed_Hessian_upper_triangle']}
 get=lambda i,j,dz=False:H.get(tuple(sorted((i,j))),(iv.mpf(0),iv.mpf(0)))[int(dz)]
 bn=lambda rows,cols,dz=False:norm([get(i,j,dz) for i in rows for j in cols])
 check('ordinary_auxiliary_flux_columns_exact_zero',all(tuple(sorted((28+i,j))) not in H for i in ORD for j in (13,41)))
 check('ordinary_auxiliary_gradient_only_two_metric_rows',all(tuple(sorted((i,41))) not in H for i in ORD if i not in (0,3)))
 spec=importlib.util.spec_from_file_location('ordinary_momentum_profiles',ROOT/FACTORY)
 fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
 y,_=env['state'](env['J'].variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
 S0,S1=up(y[44].c[0]),up(y[47].c[0])
 vb={k:decode(v) for k,v in data['velocity']['bounds_binary'].items()};M0=vb['temporal_inverse'];M1=vb['temporal_inverse_spatial_derivative']
 A0=bn(range(14,27),range(14,27));A1=vb['temporal_Hessian_spatial_derivative']
 B0=bn(range(14,27),range(28,41));B1=bn(range(14,27),range(28,41),True)
 G0=bn(range(28,41),range(28,41));G1=bn(range(28,41),range(28,41),True)
 C0,C1=vb['configuration_zeroth_matrix'],vb['configuration_matrix_derivative']
 Dq0=bn(range(28,41),range(13));Dq1=bn(range(28,41),range(13),True)
 Br0=B0+S0*A0;Br1=B1+S1*A0+S0*A1
 Gr0=G0+2*S0*B0+S0*S0*A0
 Gr1=G1+2*S1*B0+2*S0*B1+2*S0*S1*A0+S0*S0*A1
 Fq=Dq0+Dq1+(S0+S1)*C0+S0*C1
 rawR=[(M0+M1)*(Rp[j]+(Br0+Br1)*Rq[j]+(C0+C1)*Q[j]) for j in range(8)]
 fluxR=[(Br0+Br1)*rawR[j]+(Gr0+Gr1)*Rq[j]+Fq*Q[j] for j in range(8)]
 rawv=[M0*(pc+(C0+B0)*q) for pc,q in zip(Pc,Q)]
 localQ=bn(ORD,range(13))+bn(ORD,range(28,41));localV=bn(ORD,range(14,27));localZ=bn(ORD,[13])
 local=[localQ*Q[j]+localV*rawv[j]+S1*Pc[j] for j in range(8)];local[3]+=localZ
 # Exact inherited regulator principal coefficient; interval overlap is a
 # consistency check, not the identity's proof.
 aq=-env['j'].exp(y[12]*(-mp.mpf(2)/5))*y[40]/(2*(y[0]**mp.mpf('.5')))*(iv.mpf(5)/11)
 check('retained_auxiliary_gradient_coefficient_consistent',all(lo(get(i,41)-aq.c[0])<=0<=hi(get(i,41)-aq.c[0]) for i in (0,3)))
 ls=[y[8]/y[0],y[8]/y[0],y[8]/(2*y[0])];N0=norm([iv.mpf(1)]*3+[a.c[0] for a in ls]);N1=norm([a.c[1] for a in ls]);Pi0=1+N0;Pi1=N1
 gamma=(1+y[0]*sum((a**2 for a in y[6:9]),env['J'](0)))**mp.mpf('.5');c=gamma/(y[0]**mp.mpf('.5'))
 Q0=3+iv.sqrt(2)*up(c.c[0]);Q1=iv.sqrt(2)*up(c.c[1]);Z0=Pi0+Br0*Q0;Z1=Pi1+Br1*Q0+Br0*Q1
 V0=M0*Z0;V1=M1*Z0+M0*Z1
 flux_derivative=Br1*V0+Br0*V1+Gr1*Q0+Gr0*Q1
 gauge={k:decode(v) for k,v in data['gauge']['bounds_binary'].items()}
 affine=[decode(x) for x in data['parent']['bounds_binary']['affine_field_L2']]
 momentum=[fluxR[j]+local[j]+iv.exp(5*r)*gauge['paired_momentum_L2_per_affine_L2']*affine[j] for j in range(8)]
 for j in (0,1,2,3):momentum[j]+=flux_derivative
 momentum+=[iv.exp(5*r)*gauge['paired_momentum_L2_per_harmonic']]
 check('all_nine_rows_and_global_input_columns_retained',len(ORD)==9 and len(momentum)==9)
 check('all_actual_momentum_remainder_coefficients_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for x in momentum))
 check('inherited_sources_sidecars_timestamps_unchanged',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snap.items()))
 return dict(kind='RTAU_ORDINARY_MOMENTUM_REMAINDER_V3',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  input_order=data['parent']['input_order'],bounds_binary={'nine_momentum_rows_L2_remainder':[binary(x) for x in momentum],'flux_coefficient_derivative':binary(flux_derivative),'regular_flux_H1':[binary(x) for x in fluxR]},
  upper_display={'nine_momentum_rows_L2_remainder':[mp.nstr(hi(x),28) for x in momentum]},
  principal='negative derivative of the same-action material Schur flux plus retained a_q*D_z(delta_Z) in metric rows 0,3',
  scope='INITIAL_NINE_ORDINARY_CANONICAL_MOMENTUM_ROWS_L2_REMAINDER_IN_PHYSICAL_STRONG_DATA_NORM_ONLY',
  force_density_moving_maps='NOT_ASSEMBLED',full_compatible_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',density_coordinate='Sigma=rho+e_force+b*Z**2/2',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
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
