"""P0-B actual scalar matter-source dressing and evolving FRW kernel."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parents[4]
INPUTS='Theory/Gates/MAT-001/MAT001_M4_P0B_ACTUAL_SOURCE_KERNEL_V1_INPUTS_2026-11-05.json'
OWNER='Theory/Gates/MAT-001/MAT001_M4_P0B_SHEAR_SOURCE_REPAIR_V2_REPORT_2026-11-05.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 pins=dict(json.loads((ROOT/INPUTS).read_text())['source_sha256'])
 for rel in [INPUTS,OWNER,'Analysis/MAT/MAT-001/PKM1_METRIC_HOST/m4_actual_source_kernel_v2.py','Analysis/MAT/MAT-001/PKM1_METRIC_HOST/m4_actual_source_kernel_v1.py','Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/m4_actual_source_kernel_v1_20261105/receipt.json',Path(__file__).relative_to(ROOT).as_posix()]:pins[rel]=sha(ROOT/rel)
 snap={}
 for rel,want in pins.items():
  p=ROOT/rel;assert sha(p)==want,rel
  for q in [p,Path(str(p)+'.sha256')]:
   if q.exists():snap[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(n,v):checks.append(dict(name=n,passed=bool(v)))
 M,H,r,mu,q,CJ=s.symbols('M H rho mu q CJ',positive=True)
 rd,V,Vr,Vrr=s.symbols('rho_dot V V_rho V_rhorho',real=True)
 X=s.Matrix(s.symbols('R drho'));vel=s.Matrix(s.symbols('Rdot drhodot'))
 alpha,Sigma,density,j,tau=s.symbols('alpha Sigma delta_e j tau',real=True)
 cc=s.Matrix([alpha,Sigma]);source=s.Matrix([-density,-j/q**2]);direct=s.Matrix([tau,0])
 C=s.Matrix([[CJ*q*q-2*V,2*M*H],[2*M*H,0]])
 Bv=s.Matrix([[6*M*H,-rd],[-2*M,0]])
 Bx=s.Matrix([[2*M*q*q,-(Vr+r*mu*mu)],[0,-rd]])
 K0=s.diag(-6*M,1);D0=s.Matrix([[-18*M*H,0],[3*rd,0]])
 F0=s.Matrix([[2*M*q*q-18*V,3*(r*mu*mu-Vr)],[3*(r*mu*mu-Vr),mu*mu-Vrr-q*q]])
 L0=(vel.T*K0*vel)[0]/2+(vel.T*D0*X)[0]+(X.T*F0*X)[0]/2
 b=Bv*vel+Bx*X
 full=L0+(cc.T*(b+source))[0]+(cc.T*C*cc)[0]/2+(X.T*direct)[0]
 solved=-C.inv()*(b+source)
 reduced=s.expand(full.subs(dict(zip(cc,solved)),simultaneous=True))
 K=s.simplify(K0-Bv.T*C.inv()*Bv);D=s.simplify(D0-Bv.T*C.inv()*Bx);F=s.simplify(F0-Bx.T*C.inv()*Bx)
 sv=s.simplify(-Bv.T*C.inv()*source);sx=s.simplify(direct-Bx.T*C.inv()*source)
 contact=s.factor(-(source.T*C.inv()*source)[0]/2)
 target=(vel.T*K*vel)[0]/2+(vel.T*D*X)[0]+(X.T*F*X)[0]/2+(vel.T*sv)[0]+(X.T*sx)[0]+contact
 check('actual_constraint_solution_including_matter',s.simplify(C*solved+b+source)==s.zeros(2,1))
 check('complete_source_dressed_reduction',s.simplify(reduced-target)==0)
 check('source_contact_retained',contact!=0)
 check('omitted_constraint_source_dressing_detected',s.simplify(sv)!=s.zeros(2,1))
 V_os=3*M*H*H-(rd*rd+r*r*mu*mu)/2
 K_expected=s.Matrix([[(rd*rd+r*r*mu*mu+CJ*q*q)/(H*H),-rd/H],[-rd/H,1]])
 check('actual_nonzero_mode_kinetic_matches_parent',s.simplify(K.subs(V,V_os)-K_expected)==s.zeros(2))
 check('nonzero_mode_constraint_domain',s.factor(C.det())==-4*M*M*H*H)
 # Matter first variation and periodic shift-source sign.
 z=s.symbols('z',real=True);beta=s.cos(z);T0z=s.sin(z)
 check('periodic_shift_source_IBP',s.integrate(s.diff(beta,z)*T0z+beta*s.diff(T0z,z),(z,0,2*s.pi))==0)
 check('shear_source_sign',-s.diff(beta,z,2)==beta)
 ds=s.Symbol('div_shift')
 oldshift=-2*M*Sigma*vel[0]+2*M*H*alpha*Sigma-rd*Sigma*X[1]
 admshift=2*M*ds*vel[0]-2*M*H*alpha*ds+rd*ds*X[1]
 check('independent_ADM_and_amplitude_shift_sign',s.expand(oldshift.subs(Sigma,-ds)-admshift)==0)
 check('opposite_shear_identification_rejected',s.expand(oldshift.subs(Sigma,ds)-admshift)!=0)
 hm=s.diag(-2*alpha,2*X[0],2*X[0],2*X[0]);stress=s.diag(density,s.Symbol('px'),s.Symbol('py'),s.Symbol('pz'))
 first=s.trace(stress*hm)/2
 check('metric_energy_and_trace_source',s.expand(first+alpha*density-X[0]*(stress[1,1]+stress[2,2]+stress[3,3]))==0)
 # Full time-dependent Euler operator including a^3 and derivative sources.
 t=s.symbols('t',real=True);a=s.Function('a')(t);HH=s.diff(a,t)/a
 xx=s.Matrix([s.Function('x0')(t),s.Function('x1')(t)]);vv=xx.diff(t)
 kt=s.Matrix([[s.Function('k0')(t),s.Function('k1')(t)],[s.Function('k1')(t),s.Function('k2')(t)]])
 dt=s.Matrix(2,2,lambda i,j:s.Function('d%d%d'%(i,j))(t))
 ft=s.Matrix([[s.Function('f0')(t),s.Function('f1')(t)],[s.Function('f1')(t),s.Function('f2')(t)]])
 uv=s.Matrix([s.Function('v0')(t),s.Function('v1')(t)]);ux=s.Matrix([s.Function('s0')(t),s.Function('s1')(t)])
 Lt=a**3*((vv.T*kt*vv)[0]/2+(vv.T*dt*xx)[0]+(xx.T*ft*xx)[0]/2+(vv.T*uv)[0]+(xx.T*ux)[0])
 EL=s.Matrix([s.diff(s.diff(Lt,vv[i]),t)-s.diff(Lt,xx[i]) for i in range(2)])/a**3
 op=kt*xx.diff(t,2)+(kt.diff(t)+3*HH*kt+dt-dt.T)*vv+(dt.diff(t)+3*HH*dt-ft)*xx
 forcing=ux-uv.diff(t)-3*HH*uv
 check('full_evolving_kernel_and_source_Euler_identity',s.simplify(EL-op+forcing)==s.zeros(2,1))
 check('missing_background_time_derivatives_rejected',s.simplify(kt.diff(t)*vv+dt.diff(t)*xx)!=s.zeros(2,1))
 # Time-dependent field chart: transformed source and contact preserve response.
 R=s.Matrix([[1,t],[0,1]]);vy=R.T*uv;xy=R.T*ux+R.diff(t).T*uv
 check('time_dependent_source_chart_covariance',s.simplify(xy-vy.diff(t)-3*HH*vy-R.T*forcing)==s.zeros(2,1))
 # Homogeneous mode: scalar shift divergence is identically zero, not free.
 bv0=Bv[0,:];bx0=Bx[0,:].subs(q,0);C0=-2*V
 Kh=s.simplify(K0-bv0.T*bv0/C0)
 Dh=s.simplify(D0-bv0.T*bx0/C0);Fh=s.simplify(F0.subs(q,0)-bx0.T*bx0/C0)
 svh=s.simplify(bv0.T*density/C0);sxh=s.simplify(direct+bx0.T*density/C0);ch=s.factor(-density**2/(2*C0))
 Lhom=L0.subs(q,0)+alpha*((bv0*vel+bx0*X)[0]-density)+C0*alpha**2/2+(X.T*direct)[0]
 alphah=-((bv0*vel+bx0*X)[0]-density)/C0
 th=(vel.T*Kh*vel)[0]/2+(vel.T*Dh*X)[0]+(X.T*Fh*X)[0]/2+(vel.T*svh)[0]+(X.T*sxh)[0]+ch
 check('actual_homogeneous_one_constraint_reduction',s.simplify(Lhom.subs(alpha,alphah)-th)==0)
 det_h=s.factor(Kh.det().subs(V,V_os));wanted=3*M*r*r*mu*mu/V_os
 check('homogeneous_kinetic_determinant',s.simplify(det_h-wanted)==0)
 check('homogeneous_mode_differs_from_q_to_zero',s.simplify(Kh.subs(V,V_os)-K_expected.subs(q,0))!=s.zeros(2))
 # Independently derive conservation for scalar stress components on FRW.
 E=s.Function('E')(t,z);mom=s.Function('mom')(t,z)
 px,py,pz=[s.Function(n)(t,z) for n in ['px','py','pz']]
 coords=[t,s.Symbol('x'),s.Symbol('y'),z];g=s.diag(-1,a*a,a*a,a*a);gi=g.inv()
 Gamma=lambda u,v,w:sum(gi[u,l]*(s.diff(g[l,w],coords[v])+s.diff(g[l,v],coords[w])-s.diff(g[v,w],coords[l]))/2 for l in range(4))
 T=s.Matrix([[E,0,0,mom],[0,px/a**2,0,0],[0,0,py/a**2,0],[mom,0,0,pz/a**2]])
 div=[]
 for nu in [0,3]:
  div.append(s.simplify(sum(s.diff(T[mu0,nu],coords[mu0])+sum(Gamma(mu0,mu0,l)*T[l,nu]+Gamma(nu,mu0,l)*T[mu0,l] for l in range(4)) for mu0 in range(4))))
 check('matter_energy_Ward_identity',s.simplify(div[0]-s.diff(E,t)-3*HH*E-HH*(px+py+pz)-s.diff(mom,z))==0)
 check('matter_momentum_Ward_identity',s.simplify(div[1]-s.diff(mom,t)-5*HH*mom-s.diff(pz,z)/a**2)==0)
 # Exact independent rational reduction fixture, including derivative sources.
 substitutions={M:2,H:s.Rational(1,3),r:3,rd:s.Rational(1,5),mu:2,q:4,CJ:4,V:5,Vr:7,Vrr:11,density:13,j:17,tau:19}
 fixture=full.subs(substitutions);stationary=s.solve([s.diff(fixture,alpha),s.diff(fixture,Sigma)],[alpha,Sigma])
 check('independent_rational_source_fixture',s.expand(fixture.subs(stationary)-target.subs(substitutions))==0)
 check('original_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snap.items()))
 encode=lambda mat:[[str(s.factor(v)) for v in mat.row(i)] for i in range(mat.rows)]
 return dict(kind='M4_P0B_ACTUAL_SOURCE_KERNEL_V3',source_sha256=pins,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
  nonzero_mode={'fields':['R','delta_rho'],'constraints':['alpha','Sigma=-Delta beta/a^2'],'C':encode(C),'B_velocity':encode(Bv),'B_field':encode(Bx),'K':encode(K),'D':encode(D),'F':encode(F),'source_velocity':encode(sv),'source_field':encode(sx),'source_contact':str(contact),'domain':'q!=0,H!=0,rho>0,mu!=0; conserved external stress'},
  homogeneous={'C':str(C0),'K':encode(Kh),'D':encode(Dh),'F':encode(Fh),'source_velocity':encode(svh),'source_field':encode(sxh),'source_contact':str(ch),'domain':'k=0 scalar source; V!=0 for this elimination; harmonic vector constraints separate'},
  time_operator='K*d_t^2+(dot K+3H K+D-D.T)*d_t+(dot D+3H D-F)',time_source='s_x-dot s_v-3H s_v',
  scope='ACTUAL_PARENT_SCALAR_EXTERNAL_MATTER_SOURCE_AND_TIME_DEPENDENT_KERNEL_EXPORT_ONLY',
  physical_pole_residue='NOT_ESTABLISHED_ON_EVOLVING_BACKGROUND',full_M4='INCOMPLETE',live_TrackA_V='NOT_COMPUTED',review='DEFERRED',physics_pass=False,gate_effect='NONE')
def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 if a.output:assert not a.output.parent.exists()
 d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True);a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
 else:assert a.verify.read_bytes()==raw,'Replay differs'
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'physics_pass':False}))
 if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
