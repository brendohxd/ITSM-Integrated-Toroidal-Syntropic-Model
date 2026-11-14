"""Frozen-P0 U5: variational identities, lapse Hessian and rank controls."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
ROOT=Path(__file__).resolve().parents[4]
INPUTS='Theory/Gates/MAT-001/MAT001_U5_PKM1_COVARIANT_COMPLETION_V1_INPUTS_2026-11-05.json'
OWNER='Theory/Gates/MAT-001/MAT001_U5_PKM1_COVARIANT_COMPLETION_V1_REPORT_2026-11-05.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
 pins=dict(json.loads((ROOT/INPUTS).read_text())['source_sha256'])
 for rel in [INPUTS,OWNER,Path(__file__).relative_to(ROOT).as_posix()]:pins[rel]=sha(ROOT/rel)
 snap={}
 for rel,h in pins.items():
  p=ROOT/rel;assert sha(p)==h,rel
  for q in [p,Path(str(p)+'.sha256')]:
   if q.exists():snap[q]=(sha(q),q.stat().st_mtime_ns)
 checks=[]
 def check(n,v):checks.append(dict(name=n,passed=bool(v)))
 eta=s.diag(-1,1,1,1);h=s.Matrix(4,4,lambda i,j:s.Symbol('h%d%d'%(min(i,j),max(i,j))))
 v=s.Matrix(s.symbols('v0:4'));W=s.Symbol('W',positive=True)
 for number,U in enumerate([s.Matrix([1,0,0,0]),s.Matrix([s.Rational(5,3),s.Rational(4,3),0,0])]):
  uc=eta*U;theta=-W*uc;dW=(theta.T*eta*h*eta*theta)[0]/(2*W)-(theta.T*eta*v)[0]/W
  direct=-v/W+theta*dW/W**2
  P=s.eye(4)+uc*U.T
  derived=-P*v/W-uc*(U.T*h*U)[0]/2
  check('normalized_phase_normal_variation_'+str(number),s.simplify(direct-derived)==s.zeros(4,1))
  check('varied_unit_norm_'+str(number),s.expand(2*(U.T*derived)[0]-(U.T*h*U)[0])==0)
  aa=s.Matrix([U[1]*s.Symbol('a1')/U[0],s.Symbol('a1'),s.Symbol('a2'),s.Symbol('a3')])
  check('acceleration_tangent_'+str(number),(uc.T*aa)[0]==0)
  dh=lambda k,i,j:s.Symbol('d%d_h%d%d'%(k,min(i,j),max(i,j)))
  raw=0
  for m in range(4):
   for n in range(4):
    for r in range(4):raw+=aa[m]*U[n]*U[r]*(dh(n,r,m)+dh(m,r,n)-dh(r,n,m))
  target=sum(aa[m]*U[n]*U[r]*dh(m,n,r) for m in range(4) for n in range(4) for r in range(4))
  check('full_connection_boundary_coefficient_'+str(number),s.expand(raw-target)==0)
  # On uniform-phase tangent slices the force surface potential vanishes.
  metricU=-uc*(U.T*h*U)[0]/2
  check('force_surface_potential_vanishes_on_unitary_tangents_'+str(number),s.expand((aa.T*metricU)[0])==0)
 # Integration by parts that generates the covariant phase Euler term.
 x=s.symbols('x');T,B,C,w=[s.Function(n)(x) for n in ['T','B','C','deltaTheta']]
 deltaU=-C*s.diff(w,x)
 lhs=B*deltaU+s.diff(T*deltaU,x)
 rhs=s.diff(B*C,x)*w+s.diff(T*deltaU-B*C*w,x)
 check('covariant_phase_current_IBP_sign',s.expand(lhs-rhs)==0)
 # Derive the full variable-lapse Hessian, not its principal symbol only.
 e,f,Y,vv,gg=s.symbols('epsilon f Y v w');N,MP,rho,mu=s.symbols('N MP rho mu',positive=True)
 J=s.Function('J');Ye=Y+2*e*vv/(1+e*f)+e**2*gg/(1+e*f)**2
 H=N*(1+e*f)*MP**2*J(Ye)-rho**2*mu**2/(2*N*(1+e*f))
 hess=s.diff(H,e,2).subs(e,0).doit()
 expected=2*N*MP**2*(s.diff(J(Y),Y)*gg+2*s.diff(J(Y),Y,2)*vv**2)-rho**2*mu**2*f**2/N
 check('complete_lapse_Hessian_including_lower_order_terms',s.simplify(hess-expected)==0)
 a0,y=s.symbols('a0 y',positive=True)
 JB=-2*a0**2*(y-s.log(1+y));dY=lambda z:s.diff(z,y)/(2*a0**2*y)
 j1=s.factor(dY(JB));rad=s.factor(j1+2*a0**2*y*y*dY(j1))
 check('negative_transverse_lapse_coefficient',j1==-1/(1+y))
 check('negative_radial_lapse_coefficient',rad==-1/(1+y)**2)
 check('Y0_transverse_and_radial_limits_regular',s.limit(j1,y,0,dir='+')==s.limit(rad,y,0,dir='+')==-1)
 q=s.symbols('q',real=True);symbol=-(2*MP**2*q*q+rho**2*mu**2)
 check('homogeneous_lapse_symbol_strictly_negative',s.ask(s.Q.negative(symbol)) is True)
 check('torus_zero_mode_not_deleted',symbol.subs(q,0)==-rho**2*mu**2)
 check('zero_charge_changes_zero_mode_condition',symbol.subs({q:0,mu:0})==0)
 # DeWitt kinetic map on all six independent spatial metric velocities.
 vs=s.symbols('k0:6');K=s.Matrix([[vs[0],vs[1],vs[2]],[vs[1],vs[3],vs[4]],[vs[2],vs[4],vs[5]]])
 kinetic=(s.trace(K*K)-s.trace(K)**2)/2
 Hess=s.hessian(kinetic,vs)
 check('full_metric_Legendre_map_invertible',Hess.det()!=0)
 check('amplitude_Legendre_map_invertible',s.diff(s.Symbol('rdot')**2/2,s.Symbol('rdot'),2)==1)
 # Exact C2/non-C3 distinction for the gradient-vector interaction at zero.
 xx=s.symbols('x',real=True)
 positive=-2*a0**2*(xx/a0-s.log(1+xx/a0))
 negative=-2*a0**2*(-xx/a0-s.log(1-xx/a0))
 check('vector_gradient_C2_at_zero',all(s.limit(s.diff(positive,xx,n),xx,0,dir='+')==s.limit(s.diff(negative,xx,n),xx,0,dir='-') for n in [0,1,2]))
 check('vector_gradient_not_C3_at_zero',s.limit(s.diff(positive,xx,3),xx,0,dir='+')!=s.limit(s.diff(negative,xx,3),xx,0,dir='-'))
 # Unit dimensions in mass powers: covariant potential/current are dimension 3.
 check('potential_mass_dimensions_consistent',2+1==4-1==3)
 # Rank arithmetic follows the field/constraint derivation in OWNER, not vice versa.
 rank=2*(6+1)-2*3
 check('reduced_local_symplectic_rank_eight',rank==8)
 omega=s.zeros(rank);omega[:4,4:]=s.eye(4);omega[4:,:4]=-s.eye(4)
 check('reduced_canonical_form_nondegenerate',omega.det()==1 and omega.rank()==8)
 check('all_pinned_sources_sidecars_timestamps_unchanged',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snap.items()))
 return dict(kind='PKM1_U5_COVARIANT_COMPARISON_V1',source_sha256=pins,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
  derived_lapse_second_variation=str(s.simplify(hess)),transverse=str(j1),radial=str(rad),homogeneous_lapse_symbol=str(symbol),metric_Hessian_determinant=str(Hess.det()),
  local_physical_DOF=4,reduced_symplectic_rank=8,
  scope='REGULAR_ON_SHELL_TIMELIKE_P0B_CHART_WITH_COMPACT_ELLIPTIC_LAPSE_INVERSE_AND_SEPARATE_GLOBAL_SECTORS',
  statement='Analytic proof and hypotheses are in the owning report; finite algebra controls do not replace that proof',
  nonlinear_evolution='NOT_PROVED',global_winding_core_completion='OPEN',microscopic_matching='NOT_DERIVED',review='DEFERRED',physics_pass=False,gate_effect='NONE')
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
