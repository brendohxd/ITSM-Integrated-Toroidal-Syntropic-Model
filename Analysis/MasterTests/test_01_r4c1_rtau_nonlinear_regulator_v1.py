"""Exact nonlinear regulator and controlled force-cusp interaction summands."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
INPUT='Analysis/MasterTests/outputs/r4c1_rtau_interactions_input_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_NONLINEAR_REGULATOR_V1_CONTRACT_2026-10-31.md'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=100;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 assert SHA((ROOT/INPUT).read_bytes())=='f06bfc8926b24f874c01ee000f0b34b71cf69906b4fc00278ed650c8640841d0'
 pins=dict(json.loads((ROOT/INPUT).read_text())['source_sha256'])
 for path in (SELF,INPUT,CONTRACT):pins[path]=SHA((ROOT/path).read_bytes())
 snapshots={}
 for path,want in pins.items():
  f=ROOT/path;sc=Path(str(f)+'.sha256');assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want
  for q in (f,sc):snapshots[q]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
 # Independent lapse N and K=sqrt(h)*h^zz; no use of a lapse equation.
 z=s.Symbol('z',real=True);b=s.Symbol('b',positive=True)
 N,V,K,Z,P=[s.Function(n)(z) for n in ('N','volume','K','Z','psi')]
 lag=b*(N*V*Z**2/2-N*K*s.diff(Z,z)*s.diff(P,z)-K*s.diff(N,z)*Z*s.diff(P,z))
 euler=s.diff(lag,Z)-s.diff(s.diff(lag,s.diff(Z,z)),z)
 lap=s.diff(K*s.diff(P,z),z)/V
 check('exact_auxiliary_Euler_with_lapse_flux',s.simplify(euler-b*N*V*(Z+lap))==0)
 wrong=lag+b*K*s.diff(N,z)*Z*s.diff(P,z)
 wrongE=s.diff(wrong,Z)-s.diff(s.diff(wrong,s.diff(Z,z)),z)
 check('omitted_acceleration_term_rejected',s.simplify(wrongE-euler)!=0)
 bulk=b*N*V*(Z**2/2+Z*lap);flux=-b*N*K*Z*s.diff(P,z)
 check('exact_periodic_integration_by_parts',s.simplify(lag-bulk-s.diff(flux,z))==0)
 check('eliminated_negative_square',s.simplify(bulk.subs(Z,-lap)+b*N*V*lap**2/2)==0)
 ep,U,L,W=s.symbols('epsilon U L W',real=True)
 exact=-b*ep**2*s.exp(-ep*U)*(L+ep*W)**2/2
 series=s.series(exact,ep,0,5).removeO()
 c3=-b*(2*L*W-U*L*L)/2
 c4=-b*(W*W-2*U*L*W+U*U*L*L/2)/2
 check('exact_metric_clock_cubic',s.expand(series.coeff(ep,3)-c3)==0)
 check('exact_metric_clock_quartic',s.expand(series.coeff(ep,4)-c4)==0)
 th=s.Symbol('theta',real=True);kk=s.Symbol('k',positive=True);beta=s.Rational(2,5)
 f=s.Rational(1,7)+s.cos(th)/5;g=-s.Rational(1,11)+2*s.cos(th+s.pi/3)/9
 l=kk**2*s.diff(g,th,2);w=kk**2*s.diff(f,th)*s.diff(g,th);uu=f+beta*g
 cube=s.expand_trig(c3.subs({U:uu,L:l,W:w,b:s.Rational(5,11)}))
 mean=s.simplify(s.integrate(s.expand(cube),(th,0,2*s.pi))/(2*s.pi))
 expected=s.Rational(5,11)*kk**4*s.Rational(2,9)**2*(s.Rational(1,7)-beta/11)/4
 check('cubic_torus_mean_retained',s.simplify(mean-expected)==0,str(mean))
 check('spatial_Laplacian_weighted_mean_flux',s.integrate(s.diff(s.exp(ep*f)*ep*kk*s.diff(g,th),th),(th,0,2*s.pi))==0)
 spec=importlib.util.spec_from_file_location('nonlinear_repair_backend',ROOT/BACKEND)
 backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
 old=backend.load('nonlinear_parameters',backend.QUADRATIC)
 conv=lambda v:mp.mpf(str(s.N(v,98)))
 par={k:conv(v) for k,v in old.parameters().items()}
 full=backend.ClockGaugeAction('R-tau',par,physical=True)
 analytic=backend.ClockGaugeAction('R-tau',{**par,'A':mp.mpf(0)},physical=True)
 ff=s.lambdify(th,f,'mpmath');gg=s.lambdify(th,g,'mpmath')
 fp=s.lambdify(th,s.diff(f,th),'mpmath');gp=s.lambdify(th,s.diff(g,th),'mpmath');gpp=s.lambdify(th,s.diff(g,th,2),'mpmath')
 F=mp.mpf(12)/35;G=mp.mpf(31)/99;Wb=mp.mpf(1);P1=mp.mpf(1)/23
 limit=mp.mpf('0.01');p=mp.mpf(1)/5;be=par['beta'];aa=par['A'];bb=par['b']
 tilt=[mp.mpf(1)/i for i in (13,17,19)];records=[]
 for kval in (1,7,40):
  G1=mp.mpf(2)*kval/9
  diffbound=F*mp.exp(limit*F)*G1+Wb*mp.exp(be*G*limit)*(P1+be*G*p)+limit*Wb**3*mp.exp(limit*F)*G1/2
  norm0bound=G1+p*Wb;J=3*F+be*G
  forcebound=aa*mp.exp(limit*J)*(J*norm0bound**3+3*(norm0bound+limit*diffbound)**2*diffbound)
  maxratio=mp.mpf(0);maxerr=mp.mpf(0)
  for theta in (mp.mpf(0),mp.pi/3,mp.pi):
   fv,gv=ff(theta),gg(theta);df=kval*fp(theta);dg=kval*gp(theta);ddg=kval*kval*gpp(theta);dp=mp.cos(theta)/23
   norm0=mp.sqrt(sum((p*t+(dg if j==2 else 0))**2 for j,t in enumerate(tilt)))
   Uv=fv+be*gv;Wv=df*dg
   regbound=bb/2*mp.exp(limit*abs(Uv))*(Uv**2*ddg**2/2+2*abs(Uv*ddg*Wv)+Wv**2)
   for hs in ('0.001','-0.001','0.00001','-0.00001'):
    e=mp.mpf(hs);scale=mp.exp(e*fv);normal=mp.exp(be*e*gv)*(p+e*dp)
    gamma=mp.sqrt(1+e*e*sum(t*t for t in tilt));grad=[mp.mpf(0),mp.mpf(0),dg/scale]
    rest=[grad[j]+tilt[j]*normal+e*e*tilt[j]*sum(t*x for t,x in zip(tilt,grad))/(gamma+1) for j in range(3)]
    force=-aa*mp.exp(e*(3*fv-be*gv))*abs(e)**3*sum(t*t for t in rest)**mp.mpf('1.5')
    lead=-aa*abs(e)**3*norm0**3
    check('force_control_'+str(kval)+'_'+str(len(records)),abs(force-lead)<=forcebound*e**4)
    reg=-bb/2*e*e*mp.exp(-e*Uv)*(ddg+e*Wv)**2
    r2=-bb*ddg**2/2;r3=-bb*(2*ddg*Wv-Uv*ddg**2)/2
    check('regulator_control_'+str(kval)+'_'+str(len(records)),abs(reg-e*e*r2-e**3*r3)<=regbound*e**4)
    q=[scale**2,0,0,scale**2,0,scale**2]+[e*t/scale for t in tilt]+[1+e*mp.sin(theta)/29,e*mp.cos(theta)/31,1+e*mp.sin(2*theta)/37,e*gv,-mp.exp(-2*e*fv)*(e*ddg+e*e*Wv),0,mp.mpf(1)/5]
    vel=[mp.mpf(0)]*16;dz=[mp.mpf(0)]*16
    for j in (0,3,5):vel[j]=2*conv(s.sqrt(s.Rational(3469,4620)))*q[j];dz[j]=2*e*df*q[j]
    for j,t in enumerate(tilt):dz[6+j]=-e*e*df*t/scale
    vel[10]=1;vel[11]=mp.mpf(1)/4;vel[12]=p+e*dp;vel[14]=1;dz[12]=e*dg
    state=q+vel+dz+[0]*6+[mp.exp(-be*e*gv),-be*mp.exp(-be*e*gv)*e*dg]
    difference=full.density(state)[0]-analytic.density(state)[0]
    err=abs(difference-force)/(1+abs(force));maxerr=max(maxerr,err)
    check('full_density_decomposition_'+str(kval)+'_'+str(len(records)),err<mp.mpf('1e-60'),mp.nstr(err,35))
    maxratio=max(maxratio,abs(force-lead)/(forcebound*e**4))
    records.append(dict(k=kval,theta=mp.nstr(theta,25),epsilon=hs))
  records.append(dict(k=kval,force_remainder_constant=mp.nstr(forcebound,50),largest_bound_ratio=mp.nstr(maxratio,40),largest_full_density_error=mp.nstr(maxerr,40)))
 # The norm-cubed term has distinct one-sided third derivatives on a nonzero ray.
 check('analytic_third_derivative_rejected',-6*aa != 6*aa)
 check('zero_leading_direction_retained',sum((p*t-p*t)**2 for t in tilt)==0)
 for f,(h,m) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==m
 check('source_and_sidecar_bytes_mtimes_preserved',True,len(snapshots))
 return dict(kind='R4C1_RTAU_NONLINEAR_REGULATOR_V1',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,source_sha256=pins,
  regulator=dict(Euler='b*N*sqrt(h)*(Z+Delta_h(psi))',eliminated='-b*N*sqrt(h)*Delta_h(psi)^2/2',cubic=str(c3),quartic=str(c4),packet_cubic_mean=str(mean),remainder='b/2*epsilon^4*exp(epsilon_max*abs(U))*(U^2*L^2/2+2*abs(U*L*W)+W^2)'),
  force=dict(cubic='-A*abs(epsilon)^3*norm(grad(g)+p*w)^3',boost_rest_gradient='grad(g)*exp(-epsilon*f)+w*psi_normal+epsilon^2*w*(w.dot(grad(g)))*exp(-epsilon*f)/(gamma+1)',remainder='A*epsilon^4*exp(epsilon_max*J)*(J*M^3+3*(M+epsilon_max*B)^2*B)',B='F*exp(epsilon_max*F)*G1+W*exp(beta*G*epsilon_max)*(P1+beta*G*abs(p))+epsilon_max*W^3*exp(epsilon_max*F)*G1/2',J='3*F+beta*G',M='G1+abs(p)*W'),
  controls=records,epsilon_domain='abs(epsilon)<=1/100',off_shell_packet_only=True,full_reduced_coupled_interactions='INCOMPLETE',nonlinear_lapse_shift_matter_solve='INCOMPLETE',nonlinear_domain_persistence=False,physical_window_demonstrated=False,canonical_parent_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
