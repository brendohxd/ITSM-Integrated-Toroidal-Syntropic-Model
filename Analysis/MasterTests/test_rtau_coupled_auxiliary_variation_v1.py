"""Coupled local variation controls and actual initial weak-rate constants."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COUPLED_AUXILIARY_VARIATION_V1_SPEC_2026-11-02.md'
PRIOR='Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'


def strong(h,hz,V,Vz,p1,p2,v1,v2):
 H=h.inv();Ht=-H*V*H;a=H[2,2];at=Ht[2,2]
 b=a*s.trace(H*hz)/2-(H*hz*H)[2,2]
 bt=at*s.trace(H*hz)/2+a*s.trace(Ht*hz+H*Vz)/2-(Ht*hz*H+H*Vz*H+H*hz*Ht)[2,2]
 return -a*p2-b*p1,-at*p2-a*v2-bt*p1-b*v1


def variation(h,V,psi,v,k,l,chi,eta,z):
 H=h.inv();Ht=-H*V*H;mu=s.sqrt(h.det());mut=mu*s.trace(H*V)/2
 a=H[2,2];at=Ht[2,2];c=mu*a;ct=mut*a+mu*at
 E=H/2;Et=Ht/2
 D=mu*(-H[:,2]*H[2,:]+a*H/2)
 Dt=mut*(-H[:,2]*H[2,:]+a*H/2)+mu*(-Ht[:,2]*H[2,:]-H[:,2]*Ht[2,:]+at*H/2+a*Ht/2)
 pair=lambda a,b:s.trace(a.T*b)
 d=pair(E,k);dt=pair(E,l)+pair(Et,k)
 F=c*s.diff(chi,z)+pair(D,k)*s.diff(psi,z)
 G=ct*s.diff(chi,z)+(pair(D,l)+pair(Dt,k))*s.diff(psi,z)+pair(D,k)*s.diff(v,z)
 Z,Zt=strong(h,s.diff(h,z),V,s.diff(V,z),s.diff(psi,z),s.diff(psi,z,2),s.diff(v,z),s.diff(v,z,2))
 return (-d*Z-s.diff(F,z)/mu,
         -dt*Z-d*Zt+mut*s.diff(F,z)/mu**2-s.diff(G,z)/mu-s.diff(c*s.diff(eta,z),z)/mu)


def run():
 checks=[]
 def check(n,ok):checks.append(dict(name=n,passed=bool(ok)))
 z,e=s.symbols('z e',real=True);at=s.Rational(1,7);g=1+z*z/10
 h=g*g*s.eye(3);L=s.Rational(4,5)+z/31;V=2*L*h
 psi=z*z/3+z**3/5;v=s.Rational(1,5)+z**4/7
 k=(1+z/5)*s.Matrix([[1,2,3],[2,-1,4],[3,4,2]])/19
 l=(1-z/9)*s.Matrix([[2,-1,3],[-1,4,2],[3,2,-2]])/23
 chi=z+z*z/11;eta=z**3/13
 dz,dzt=variation(h,V,psi,v,k,l,chi,eta,z)
 val=lambda x:x.subs(z,at)
 # Independent strong coefficient formula, differentiated in one external
 # perturbation parameter after spatial jets are evaluated exactly.
 ref=strong(val(h)+e*val(k),val(s.diff(h,z))+e*val(s.diff(k,z)),
            val(V)+e*val(l),val(s.diff(V,z))+e*val(s.diff(l,z)),
            val(s.diff(psi,z))+e*val(s.diff(chi,z)),val(s.diff(psi,z,2))+e*val(s.diff(chi,z,2)),
            val(s.diff(v,z))+e*val(s.diff(eta,z)),val(s.diff(v,z,2))+e*val(s.diff(eta,z,2)))
 check('full_six_component_deltaZ',s.simplify(val(dz)-s.diff(ref[0],e).subs(e,0))==0)
 check('full_six_component_deltaZt',s.simplify(val(dzt)-s.diff(ref[1],e).subs(e,0))==0)
 zero=s.zeros(3)
 _,no_l=variation(h,V,psi,v,k,zero,chi,eta,z)
 check('omitting_metric_velocity_rejected',s.simplify(val(dzt-no_l))!=0)
 # Active spatial Lie variations include tensor-index terms. Time-independent
 # w: delta Z_t=w partial_z Z_t, without quotienting physical time.
 w=1+z/17
 def lie(T):
  R=w*s.diff(T,z)
  for i in range(3):
   for j in range(3):R[i,j]+=s.diff(w,z)*(int(i==2)*T[2,j]+int(j==2)*T[i,2])
  return R
 ld,lt=variation(h,V,psi,v,lie(h),lie(V),w*s.diff(psi,z),w*s.diff(v,z),z)
 Z,Zt=strong(h,s.diff(h,z),V,s.diff(V,z),s.diff(psi,z),s.diff(psi,z,2),s.diff(v,z),s.diff(v,z,2))
 check('Lie_full_metric_deltaZ',s.simplify(val(ld-w*s.diff(Z,z)))==0)
 check('Lie_full_metric_deltaZt',s.simplify(val(lt-w*s.diff(Zt,z)))==0)
 harmonic,_=variation(h,V,psi,v,s.eye(3),zero,s.S.Zero,s.S.Zero,z)
 check('constant_metric_mode_not_deleted',s.simplify(val(harmonic))!=0)
 # Exact arithmetic inequalities below bound the ACTUAL trigonometric initial
 # profiles, not the rational fixture. No grid extrema or centre substitution.
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
 prior=json.loads((ROOT/PRIOR).read_text())
 decode=lambda x:iv.mpf([mp.mpf(tuple(a)) for a in x])
 hi=lambda x:mp.mpf(x._mpi_[1]);lo=lambda x:mp.mpf(x._mpi_[0])
 r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000
 H=decode(prior['H_interval']);M=iv.mpf(max(abs(lo(H)),abs(hi(H))))+eps/31;B=2*eps/31
 S1=eps*(iv.mpf(1)/29+iv.mpf(2)/31);S2=eps*(iv.mpf(1)/29+iv.mpf(4)/31)
 V1=3*eps/47;V2=9*eps/47;ex=lambda n:iv.exp(n*r)
 Z0=ex(2)*(S2+r*S1);Zt0=2*M*Z0+ex(2)*(V2+r*V1+B*S1)
 E0=iv.sqrt(3)*ex(2)/2;Et0=2*M*E0;D0=iv.sqrt(3)*ex(1)/2;Dt0=M*D0
 Q1=ex(3)*(1+3*r);P1=3*ex(3)*(M+B+3*M*r);c0=ex(1);ct0=M*c0
 C=dict(eta=decode(prior['original_bounds']['K_v']),chi_z=P1*c0+Q1*ct0,
        metric=Et0*Z0+E0*Zt0+P1*D0*S1+Q1*(Dt0*S1+D0*V1),
        metric_velocity=E0*Z0+Q1*D0*S1)
 check('actual_initial_constants_positive_finite',all(lo(x)>0 and mp.isfinite(hi(x)) for x in C.values()))
 sources=[Path(__file__).resolve(),ROOT/SPEC,ROOT/PRIOR,ROOT/'Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py',
          ROOT/'Theory/Gates/RES-001/RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md']
 return dict(scope='COUPLED_AUXILIARY_OBSERVABLE_COMPONENT_ONLY',physical_norm='NOT_DERIVED',physics_pass=False,
  checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),
  constants_binary={k:[list(a) for a in v._mpi_] for k,v in C.items()},
  constants_upper_display={k:mp.nstr(hi(v),16) for k,v in C.items()},
  canonical_velocity_pullback='NOT_ESTABLISHED',finite_time_estimate=False,
  source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})


if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 d=run();raw=(json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True,exist_ok=True)
  with a.output.open('xb') as f:f.write(raw)
 else:assert a.verify.read_bytes()==raw
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[x for x in d['checks'] if not x['passed']],
                   'bounds':d['constants_upper_display']},indent=2))
 raise SystemExit(0 if d['passed']==d['total'] else 1)
