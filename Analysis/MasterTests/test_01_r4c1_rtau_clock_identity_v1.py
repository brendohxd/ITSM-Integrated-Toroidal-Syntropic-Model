"""Action Ward identity with independent density/current and off-shell controls.

Only the initial classical consistency implication is in scope. No evolution
or physical admission follows from this identity.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
FACTORY='Analysis/MasterTests/r4c1_clock_density_operator_factory_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_CLOCK_IDENTITY_V1_CONTRACT_2026-11-01.md'
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 assert SHA((ROOT/PARENT).read_bytes())=='9bec36b8aaa37c511779cd420e5b351203f8c9be787e6b0d1593230215a786b3'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256']);snap={}
 for p in (SELF,FACTORY,CONTRACT,PARENT):pins[p]=SHA((ROOT/p).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256')
  assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 # Exact, non-diagonal ADM and unit-frame transformation coefficients.
 hh=s.symbols('h0:6');h=s.Matrix([[hh[0],hh[1],hh[2]],[hh[1],hh[3],hh[4]],[hh[2],hh[4],hh[5]]])
 S=s.Matrix(s.symbols('S0:3'));V=s.Matrix(s.symbols('V0:3'));g=s.Matrix(s.symbols('g0:3'))
 N,gamma,alpha=s.symbols('N gamma alpha',nonzero=True)
 dot=lambda a,b:(a.T*b)[0]
 dh=(h*S)*g.T+g*(h*S).T;dN=N*(alpha-dot(S,g))
 dS=S*alpha-N**2*h.inv()*g-S*dot(S,g)
 dV=-gamma*N*h.inv()*g-S*dot(V,g)
 dg=s.cancel((dot(V,dh*V)+2*dot(V,h*dV))/(2*gamma))
 zero=lambda x:s.cancel(x)==0
 check('unit_frame_gamma_gradient_coefficient',zero(dg+N*dot(V,g)))
 U0=gamma/N;Ui=V-gamma*S/N
 check('contravariant_U0_time_diffeomorphism',zero(dg/N-gamma*dN/N**2+U0*alpha+dot(Ui,g)))
 dUi=dV-dg*S/N-gamma*dS/N+gamma*S*dN/N**2
 check('contravariant_spatial_U_time_diffeomorphism',all(zero(x) for x in dUi))
 g00=-N**2+dot(S,h*S);g0=h*S
 check('metric_g0i_time_diffeomorphism',all(zero(x) for x in dh*S+h*dS-g0*alpha-g00*g))
 check('metric_g00_time_diffeomorphism',zero(-2*N*dN+2*dot(S,h*dS)+dot(S,dh*S)-2*g00*alpha))
 # Spatial Ward adjoint cancels every quadratic shift-momentum term.
 z=s.symbols('z');sf=[s.Function('s'+str(i))(z) for i in range(3)];ef=[s.Function('e'+str(i))(z) for i in range(3)]
 cancel=s.diff(sum(sf[i]*sf[2]*ef[i] for i in range(3)),z)-sum(sf[i]*s.diff(sf[2]*ef[i],z) for i in range(3))-sf[2]*sum(ef[i]*s.diff(sf[i],z) for i in range(3))
 check('spatial_Ward_shift_quadratic_cancellation',s.expand(cancel)==0)
 # D1(S)-P vanishes for h; it equals gamma*N*h^{-1} for V.
 Pmetric=[dh[a,b] for a,b in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))]
 Dmetric=[(h*S)[a]*g[b]+(h*S)[b]*g[a] for a,b in ((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))]
 check('metric_spatial_adjoint_flux_cancels_time_gradient',all(zero(a-b) for a,b in zip(Dmetric,Pmetric)))
 check('frame_spatial_adjoint_flux_is_gamma_N_inverse_metric',all(zero(x) for x in -S*dot(V,g)-dV-gamma*N*h.inv()*g))
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1])
 ab=lambda x:max(abs(lo(x)),abs(hi(x)))
 binary=lambda x:[list(v) for v in x._mpi_]
 def interval(pair):return iv.mpf([mp.mpf(tuple(x)) for x in pair])
 def norm(xs):return iv.sqrt(sum((iv.mpf(ab(x))**2 for x in xs),iv.mpf(0)))
 spec=importlib.util.spec_from_file_location('clock_identity_factory',ROOT/FACTORY)
 factory=importlib.util.module_from_spec(spec);spec.loader.exec_module(factory);env=factory.prepare()
 J=env['J'];j=env['j'];state=env['state'];evaluate=env['evaluate'];gradient=env['gradient'];hj=env['hj'];forcing=env['forcing'];balance=env['balance'];lie=env['lie']
 initial=json.loads((ROOT/env['INITIAL']).read_text());Minv=interval(initial['bounds']['original_temporal_inverse'])
 def solve(M,R):
  mid=lambda x:(lo(x)+hi(x))/2
  x=mp.lu_solve(mp.matrix([[mid(v) for v in row] for row in M]),mp.matrix([mid(v) for v in R]))
  xi=[iv.mpf(mp.nstr(v,75)) for v in x]
  error=Minv*norm([R[i]-sum((M[i][k]*xi[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
  return [iv.mpf([lo(v)-hi(error),hi(v)+hi(error)]) for v in xi],error
 def momentum(y,L):
  n=j.exp(-(iv.mpf(2)/5)*y[12]);coef=n*n/y[0]
  es=[gradient(L,42+i).c[0]-gradient(L,45+i).c[1] for i in range(3)]
  esz=[gradient(L,42+i).c[1]-2*gradient(L,45+i).c[2] for i in range(3)]
  return coef.c[1]*es[2]+coef.c[0]*esz[2],es,esz
 def identity(theta,y,L,LR,acc,accz):
  R,Rz=forcing(y,L);M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
  eq=[R[i]-sum((M[i][k]*acc[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
  eqz=[Rz[i]-sum((hj(L,14+i,14+k).c[1]*acc[k]+M[i][k]*accz[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
  eq.append(gradient(L,13).c[0]-gradient(L,41).c[1])
  eqz.append(gradient(L,13).c[1]-2*gradient(L,41).c[2])
  rv=[v-a for v,a in zip(y[14:28],lie(y[:14],y[28:42],y[42:45],y[45:48]))]
  n=j.exp(-(iv.mpf(2)/5)*y[12]);gamma=j.sqrt(J(1)+y[0]*sum((x*x for x in y[6:9]),J(0)))
  fcoef=gamma*n/y[0];frame=fcoef.c[1]*eq[8]+fcoef.c[0]*eqz[8]
  mom,es,esz=momentum(y,L);aux=eq[13]*rv[13].c[0]
  predicted=mom+sum((a*v.c[0] for a,v in zip(eq,rv)),iv.mpf(0))+frame
  measured=balance(theta,y,L,LR,acc,accz)['residual']
  return dict(measured=measured,predicted=predicted,defect=measured-predicted,frame_flux=frame,auxiliary_work=aux,momentum_divergence=mom,euler=eq,euler_z=eqz)
 rows=[];probes=[];tol=mp.mpf('1e-28')
 for old in parent['point_controls']:
  zs=old['z'];theta=J.variable(iv.mpf(zs));y,_=state(theta,False);L=evaluate(y)
  mom,es,esz=momentum(y,L);oldres=interval(old['clock']['residual'])
  check('centre_residual_equals_momentum_divergence_'+zs,ab(oldres-mom)<tol,mp.nstr(ab(oldres-mom),40))
  rows.append(dict(z=zs,momentum_divergence=binary(mom),old_residual=binary(oldres),difference=binary(oldres-mom),momentum=[binary(v) for v in es]))
  if zs!='0.3':continue
  LR=evaluate(y,True);R,Rz=forcing(y,L);M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
  acc,ae=solve(M,R);accz,aze=solve(M,[Rz[i]-sum((hj(L,14+i,14+k).c[1]*acc[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
  check('validated_acceleration_inverse_and_derivative',hi(ae)<mp.mpf('1e-35') and hi(aze)<mp.mpf('1e-35'))
  cases=[('on_shell_centre',y,L,LR,acc,accz)]
  bad=list(acc);bad[8]+=iv.mpf(1)/7
  cases.append(('off_shell_frame_acceleration',y,L,LR,bad,accz))
  ya=list(y);ya[13]+=J(iv.mpf(1)/1000)
  cases.append(('off_shell_auxiliary_value',ya,evaluate(ya),evaluate(ya,True),acc,accz))
  for label,yy,ll,raw,aa,az in cases:
   result=identity(theta,yy,ll,raw,aa,az)
   check('full_local_identity_'+label,ab(result['defect'])<tol,mp.nstr(ab(result['defect']),40))
   if label=='off_shell_frame_acceleration':
    omitted=result['defect']+result['frame_flux']
    check('omitting_frame_flux_rejected',lo(omitted)>mp.mpf('1e-10') or hi(omitted)<-mp.mpf('1e-10'),mp.nstr(ab(omitted),40))
   if label=='off_shell_auxiliary_value':
    omitted=result['defect']+result['auxiliary_work']
    check('omitting_auxiliary_Euler_work_rejected',lo(omitted)>mp.mpf('1e-10') or hi(omitted)<-mp.mpf('1e-10'),mp.nstr(ab(omitted),40))
   probes.append(dict(label=label,**{k:([binary(x) for x in v] if isinstance(v,list) else binary(v)) for k,v in result.items()}))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_CLOCK_IDENTITY_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,centre_controls=rows,off_shell_controls=probes,identity_tolerance='1e-28',
  identity='R=div(N^2 h^-1 E_S)+E_q.(v-Lie_S q)+div(gamma N h^-1 E_V)',
  initial_clock_consistency='conditional on exact reconstructed lapse/multiplier and all initial field/momentum Euler equations',
  parent_independent_box_certificate=False,physical_symplectic_quotient='NOT_DERIVED',nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args()
 data=calculate();encoded=ENC(data)
 if a.replay:assert a.replay.read_bytes()==encoded;print('READ_ONLY_REPLAY_EXACT',SHA(encoded))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(encoded);Path(str(p)+'.sha256').write_text(SHA(encoded)+'\n');print(json.dumps(dict(passed=data['passed'],total=data['total'],receipt=str(p))))
 return 0 if data['passed']==data['total'] else 1
if __name__=='__main__':raise SystemExit(main())
