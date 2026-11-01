"""Whole-circle fixed-field constraint-tangent velocity coercivity.

No evolving/symplectic admission, physical cutoff, or new matched parameter.
"""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_prepared_temporal_v2_attempt_01/summary.json'
INVERSE='Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json'
NUMERICAL='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
PROFILE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_VELOCITY_TANGENT_V1_CONTRACT_2026-10-31.md'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/PARENT).read_bytes())=='aba30848eed3be2d4cb3f0122899ea0394aafcf93b6ebd4d91ecfb3b63f6ac93'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,PARENT,CONTRACT,'Analysis/MasterTests/test_01_r4c1_rtau_velocity_tangent_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_velocity_tangent_v1_attempt_01/summary.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_VELOCITY_TANGENT_V2_SPEC_2026-10-31.md'):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);binary=lambda x:[list(v) for v in x._mpi_]
 def interval(pair):
  a,b=(mp.mpf(tuple(z)) for z in pair);assert mp.isfinite(a) and mp.isfinite(b) and a<=b;return iv.mpf([a,b])
 # The reference constraints have orthonormal rows in the stated L2 codomain.
 M0=s.diag(*([1]*6+[s.Rational(1,6)]*3+[1,1,1,3]))
 for a in (0,3,5):
  for b in (0,3,5):M0[a,b]-=s.Rational(16,15)
 H0=s.sqrt(s.Rational(3469,4620));W0=s.Matrix([H0,0,0,H0,0,H0,0,0,0,0,1,s.Rational(1,4),s.Rational(1,5)])
 Q0=s.zeros(13,1);Q0[10]=1;I0=-M0*W0;L2=s.factor(((I0+Q0).T*(I0+Q0))[0]);L0=s.sqrt(L2)
 Cm=s.zeros(3,13);Cm[0,2]=Cm[1,4]=1;Cm[2,0]=Cm[2,3]=16/s.sqrt(513);Cm[2,5]=1/s.sqrt(513)
 Cg=Q0.T.col_join(((I0+Q0)/L0).T)
 check('reference_momentum_rows_orthonormal',(Cm*Cm.T-s.eye(3)).applyfunc(s.simplify)==s.zeros(3))
 check('reference_global_charge_rows_orthonormal',(Cg*Cg.T-s.eye(2)).applyfunc(s.simplify)==s.zeros(2))
 check('reference_full_temporal_norm_3',max(abs(v) for v in M0.eigenvals())==3)
 a,d,xy=s.symbols('a d xy',real=True);wg=s.Matrix([(a+d)/s.sqrt(2),xy,0,(a-d)/s.sqrt(2),0,-16*s.sqrt(2)*a])
 qg=s.expand((wg.T*M0[:6,:6]*wg)[0]);ng=s.expand((wg.T*wg)[0])
 check('reference_nonzero_mode_kernel_energy',s.simplify(qg-(33*a*a+d*d+xy*xy))==0 and s.simplify(ng-(513*a*a+d*d+xy*xy))==0)
 alpha2=s.Rational(121,25)*H0**2;b2=s.Rational(169,400)/(3*alpha2)
 mean_ratio=s.factor((1-s.Rational(11,5)*b2)/(1+b2))
 check('reference_mean_clock_and_U1_kernel_positive',mean_ratio>s.Rational(1,6),str(mean_ratio))
 reference_gap=s.Rational(1,20)
 check('reference_all_harmonics_and_means_gap',s.Rational(11,171)>reference_gap and s.Rational(1,6)>reference_gap)
 # Exact algebraic interpretation of the clock integrand retains the lapse flux.
 N,vol,x,shift,theta,offset=s.symbols('N vol x shift theta offset',real=True,nonzero=True)
 f=lambda y:y*y/2+y**3/7
 LN=N*vol*f((x-shift)/N+offset*theta)
 euler=s.simplify(N*s.diff(LN,N)-(LN-s.diff(LN,x)*(x-shift)))
 check('clock_weighted_lapse_scaling_identity',euler==0)
 # Bounds below use ALL certified roots, with no restriction on velocity parity.
 eps=iv.mpf(1)/1000;beta=iv.mpf(2)/5;rad=iv.mpf(1139)/100000000
 numerical=json.loads((ROOT/NUMERICAL).read_text())['results'][-1];co=json.loads((ROOT/INVERSE).read_text())['parity_center_coefficients']
 tree=ast.parse((ROOT/PROFILE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate');fn=next(n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name=='profiles')
 scope=dict(mp=iv,e=eps,beta=beta);exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<pinned-initial-profiles-interval>','exec'),scope)
 rootH=iv.mpf(numerical['H'])+iv.mpf([-1,1])*rad;rootomega=iv.mpf(numerical['omega'])+iv.mpf([-1,1])*rad
 h0=iv.sqrt(iv.mpf(3469)/4620);ref=[h0,iv.mpf(0),iv.mpf(0),h0,iv.mpf(0),h0]+[iv.mpf(0)]*4+[iv.mpf(1),iv.mpf(1)/4,iv.mpf(1)/5]
 Wdiff=mp.mpf(0);cells=[]
 for cell in range(32):
  left=iv.pi*(2*cell)/32;right=iv.pi*(2*cell+2)/32;z=iv.mpf([lo(left),hi(right)]);p=scope['profiles'](z)
  S=[];Sz=[]
  for row in co:
   S.append(sum((iv.mpf(row[2*n-2])*iv.cos(n*z)+iv.mpf(row[2*n-1])*iv.sin(n*z) for n in range(1,17)),iv.mpf(0))+iv.mpf([-1,1])*rad)
   Sz.append(sum((n*(-iv.mpf(row[2*n-2])*iv.sin(n*z)+iv.mpf(row[2*n-1])*iv.cos(n*z)) for n in range(1,17)),iv.mpf(0))+iv.mpf([-1,1])*rad)
  ell=-eps*iv.sin(z)/13;ht=rootH+p['lamdot'];N=p['N'];kp=(ht-S[2]*ell)/N
  W=[kp,iv.mpf(0),-Sz[0]/(iv.sqrt(2)*N),kp,-Sz[1]/(iv.sqrt(2)*N),kp-Sz[2]/N]
  Vz=[-eps*iv.sin(z)/74,-2*eps*iv.sin(2*z)/41,eps*iv.cos(z)/43]
  W += [(p['vt'][i]-ht*p['vv'][i]-S[2]*(Vz[i]-ell*p['vv'][i])+p['vv'][2]*Sz[i])/N for i in range(3)]
  W += [(p['ud']-S[2]*p['dz'][9])/N,(rootomega+p['vd']-S[2]*p['dz'][10])/N,(p['rd']-S[2]*p['dz'][11])/N,(p['psd']-S[2]*p['dz'][12])/N]
  dd=iv.sqrt(sum(((u-v)**2 for u,v in zip(W,ref)),iv.mpf(0)));Wdiff=max(Wdiff,hi(dd));cells.append(dict(cell=cell,rate_difference=binary(dd)))
 check('whole_circle_total_background_rate_bound_finite',mp.isfinite(Wdiff),mp.nstr(Wdiff,40))
 d9=max(hi(interval(x)) for x in parent['bounds']['metric_frame_row_defects'])
 loss=interval(parent['bounds']['force_loss_upper']);can_delta=(iv.mpf(1)/13)*(iv.mpf(1)/100000000)*(iv.mpf(1001)/1000)
 psi_delta=iv.mpf(3)/100000000+loss;dM=iv.mpf(max(d9,hi(can_delta),hi(psi_delta)))
 vmax=iv.exp(3*eps/13);dv=vmax-1;psmax=eps*(iv.mpf(1)/29+iv.mpf(1)/31)
 nvmax=iv.exp(3*eps/13+beta*psmax);de=3*(nvmax-1)+nvmax*dM
 ellmax=eps/13;vabs=[3*eps/74,eps/41,eps/43];vg=[eps/74,2*eps/41,eps/43]
 scgrad=[eps/17,2*eps/19,3*eps/23,eps*(iv.mpf(1)/29+iv.mpf(2)/31)]
 Anorm=iv.sqrt(3*ellmax**2+sum(((x+ellmax*y)**2 for x,y in zip(vg,vabs)),iv.mpf(0))+sum((x*x for x in scgrad),iv.mpf(0)))
 root_components=[rad*(1+ellmax),rad/iv.sqrt(2),rad*(1+ellmax),rad/iv.sqrt(2),rad*(2+ellmax)]
 root_components += [rad*(vabs[i]+vg[i]+ellmax*vabs[i]+vabs[2]) for i in range(3)]
 root_components += [rad*scgrad[0],rad*(1+scgrad[1]),rad*scgrad[2],rad*scgrad[3]]
 root_rate_uncertainty=iv.exp(beta*psmax)*iv.sqrt(sum((x*x for x in root_components),iv.mpf(0)))
 check('certified_root_rate_uncertainty_less_than_0_001',hi(root_rate_uncertainty)<mp.mpf('.001'),mp.nstr(hi(root_rate_uncertainty),40))
 dmom=iv.sqrt(2)*(3*dv+vmax*dM+vmax*(3+dM)*(eps/43+Anorm))
 dq=dv+vmax*(iv.sqrt((eps/17)**2+(eps/19)**2)+can_delta)
 w0norm=iv.sqrt(3*h0*h0+1+iv.mpf(1)/16+iv.mpf(1)/25)
 Lnorm=iv.sqrt(3*(iv.mpf(11)/5*h0)**2+iv.mpf(1)/16+iv.mpf(9)/25)
 di=(nvmax*(3+dM)*iv.mpf(Wdiff)+de*w0norm+dq)/Lnorm
 dc=iv.sqrt(dmom*dmom+di*di+dq*dq)
 coercive=(iv.mpf(1)/20)*(1-dc*dc)-6*dc-3*dc*dc-de
 inverse=1/(1-dc)
 check('bounded_actual_constraint_right_inverse',hi(dc)<1 and hi(inverse)<mp.mpf('1.01'),mp.nstr(hi(inverse),40))
 check('actual_fixed_field_tangent_energy_positive',lo(coercive)>mp.mpf('.01'),mp.nstr(lo(coercive),40))
 check('operator_difference_less_than_one_percent',hi(dc)<mp.mpf('.01'),mp.nstr(hi(dc),40))
 # Independent full-action mixed derivatives, using the actual prepared centre.
 backend=load('velocity_tangent_full_backend',BACKEND);types=backend.load('velocity_tangent_parameters',backend.QUADRATIC)
 par={k:mp.mpf(int(v.p))/int(v.q) for k,v in types.parameters().items()};action=backend.ClockGaugeAction('R-tau',par,physical=True)
 ns=dict(mp=mp,e=mp.mpf(1)/1000,beta=par['beta']);exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<pinned-original-point-profiles>','exec'),ns)
 controls=[]
 for point,export in zip(('0.3','1.1','2.4'),parent['controls']):
  assert export['z']==point;z=mp.mpf(point);p=ns['profiles'](z);a=p['scale'];N=p['N'];ell=-mp.mpf(1)/1000*mp.sin(z)/13;ht=mp.mpf(numerical['H'])+p['lamdot'];vel=[mp.mpf(0)]*16
  for i in (0,3,5):vel[i]=2*ht*p['q'][i]
  for i in range(3):vel[6+i]=(p['vt'][i]-ht*p['vv'][i])/a
  vel[9]=p['ud'];vel[10]=mp.mpf(numerical['omega'])+p['vd'];vel[11]=p['rd'];vel[12]=p['psd'];vel[14]=1
  S=[sum(mp.mpf(row[2*n-2])*mp.cos(n*z)+mp.mpf(row[2*n-1])*mp.sin(n*z) for n in range(1,17)) for row in co]
  Sz=[sum(n*(-mp.mpf(row[2*n-2])*mp.sin(n*z)+mp.mpf(row[2*n-1])*mp.cos(n*z)) for n in range(1,17)) for row in co]
  values=p['q']+vel+p['dz']+S+Sz+[N,p['Nz']];matrix=mp.matrix([[mp.mpf(x) for x in row[:13]] for row in export['unreduced_temporal_matrix'][:13]])
  # Exported matrix entries have 50 digits. Independent mixed-derivative
  # controls therefore use tolerances well above its finite serialization error.
  A=mp.zeros(13,3);B=mp.zeros(13,3)
  for i in (0,3,5):A[i,2]=ell
  B[2,0]=B[4,1]=1/mp.sqrt(2);B[5,2]=1
  for i in range(3):A[6+i,2]=a*p['dz'][6+i];B[6+i,i]=-p['vv'][2]
  for i in range(9,13):A[i,2]=p['dz'][i]
  T=mp.diag([2*N*a*a/(mp.sqrt(2) if i in (1,2,4) else 1) for i in range(6)]+[N/a]*3+[N]*4)
  Wbar=mp.matrix([(ht-S[2]*ell)/N,0,-Sz[0]/(mp.sqrt(2)*N),(ht-S[2]*ell)/N,-Sz[1]/(mp.sqrt(2)*N),(ht-S[2]*ell-Sz[2])/N]+[a*(vel[6+i]-S[2]*p['dz'][6+i]+p['q'][8]*Sz[i])/N for i in range(3)]+[(vel[i]-S[2]*p['dz'][i])/N for i in range(9,13)])
  j=mp.matrix([0]*13);j[9]=-p['q'][10];j[10]=p['q'][9]
  predictedI=-N*a**3*matrix*Wbar;predictedQ=a**3*matrix*j;predictedS=-a**3*A.T*matrix;predictedSz=-a**3*B.T*matrix
  def gradient(v):
   tape=action.body.Tape();indices=list(range(16,30))+list(range(48,56));nodes=[tape.var(v[i]) for i in indices];q=v.copy()
   for i,x in zip(indices,nodes):q[i]=x
   L=action.density(q)[0];return action.body.val(L),dict(zip(indices,tape.grad(L,nodes)))
  L,g0=gradient(values);theta=p['Nz']/N;I=N*(g0[54]+theta*g0[55]);identity=abs(I-(L-sum(g0[16+i]*(T*Wbar)[i] for i in range(13))))
  check('full_clock_flux_Noether_identity_'+point,identity<mp.mpf('1e-80'),mp.nstr(identity,40))
  errors=[]
  for hs,threshold in (('1e-18','1e-28'),('1e-24','1e-40')):
   h=mp.mpf(hs);errI=mp.mpf(0);errQ=mp.mpf(0);errS=mp.mpf(0);errSz=mp.mpf(0)
   for col in range(13):
    q=values.copy();q[16+col]+=mp.j*h*T[col,col];_,gg=gradient(q)
    errI=max(errI,abs(mp.im(N*(gg[54]+theta*gg[55]))/h-predictedI[col]))
    errQ=max(errQ,abs(mp.im(p['q'][9]*gg[26]-p['q'][10]*gg[25])/h-predictedQ[col]))
    errS=max(errS,max(abs(mp.im(gg[48+i])/h-predictedS[i,col]) for i in range(3)))
    errSz=max(errSz,max(abs(mp.im(gg[51+i])/h-predictedSz[i,col]) for i in range(3)))
   errs=[errI,errQ,errS,errSz];check('full_action_charge_and_momentum_mixed_'+point+'_'+hs,max(errs)<mp.mpf(threshold),[mp.nstr(x,40) for x in errs]);errors.append([mp.nstr(x,45) for x in errs])
  controls.append(dict(z=point,Noether_identity_error=mp.nstr(identity,45),mixed_derivative_errors=errors))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_VELOCITY_TANGENT_V2',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
  reference_gap=str(reference_gap),reference_charge_normalization_squared=str(L2),reference_mean_bound=str(mean_ratio),cell_root_rate_bounds=cells,
  bounds=dict(root_rate_uncertainty=binary(root_rate_uncertainty),temporal_delta=binary(dM),energy_weighted_delta=binary(de),Lie_lower_order_norm=binary(Anorm),momentum_operator_difference=binary(dmom),clock_operator_difference=binary(di),U1_operator_difference=binary(dq),total_constraint_difference=binary(dc),constraint_right_inverse=binary(inverse),tangent_energy_lower=binary(coercive)),
  controls=controls,scope='fixed prepared spatial fields; all L2 velocity harmonics and parities; projected momentum plus both fixed charges; extra mean momentum condition retained',
  mean_momentum_equation='average(A^T*a^3*M*W)=0 remains an additional condition; not erased',
  auxiliary_Z='primary zero momentum and secondary Z=-Delta psi inherited; no independent kinetic norm claimed',
  physical_full_symplectic_operator='NOT_DERIVED',initial_accelerations='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,
  canonical_parent_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
