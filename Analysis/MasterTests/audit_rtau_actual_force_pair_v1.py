"""Independent complete force-current/auxiliary differential decompositions."""
from pathlib import Path
import argparse,hashlib,json
from fractions import Fraction
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/rtau_actual_force_pair_v2_20261105/receipt.json'
SPEC='Theory/Gates/RES-001/RES001_RTAU_ACTUAL_FORCE_PAIR_AUDIT_V1_SPEC_2026-11-05.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exact(t):
    sign,man,e,_=t;return (-1 if sign else 1)*Fraction(man)*Fraction(2)**e
def calculate():
    parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256'])
    for rel in [PARENT,SPEC,Path(__file__).relative_to(ROOT).as_posix()]:pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel,want in pins.items():
        p=ROOT/rel;assert sha(p)==want,rel
        for q in [p,Path(str(p)+'.sha256')]:
            if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
    checks=[]
    def check(n,ok):checks.append(dict(name=n,passed=bool(ok)))
    check('parent_component_controls_complete',parent['passed']==parent['total']==29)
    check('parent_keeps_full_generator_time_holds',parent['full_actual_generator']=='NOT_ASSEMBLED' and parent['actual_time_tube']=='NOT_ESTABLISHED' and parent['physics_pass'] is False)
    z=sp.symbols('z');beta,b=sp.symbols('beta b')
    fn=lambda n:sp.Function(n)(z)
    d,Z,s,M,Io,energy,xi,chi,zeta,vp,p,mu,fp,fs,dlm,dlmu,dfq,dd,dfsq,dfss,dSig,shift=[fn(n) for n in ['d','Z','s','M','Io','energy','xi','chi','zeta','vp','p','mu','fp','fs','dlM','dlmu','dfq','dd','dfsq','dfss','dSigma','S']]
    D=lambda f:sp.diff(f,z)
    de=p*xi/mu-p*fp*dlmu-dfq-fs*D(chi)
    dL=b*M*Z*zeta+b*M*Z**2*dlm/2-d*s*D(zeta)-d*D(Z)*D(chi)-D(Z)*s*dd+beta*d*s**2*zeta+2*beta*d*Z*s*D(chi)+beta*Z*s**2*dd
    current=D(shift)*xi+D(-vp*xi-dfsq-dfss*D(chi)+d*D(zeta)+D(Z)*dd-2*beta*(d*s*zeta+d*Z*D(chi)+Z*s*dd))+beta*((M*energy-Io)*dlm+M*(de-dSig))-beta*dL
    principal=d*sp.diff(zeta,z,2)+(D(d)-beta*d*s)*D(zeta)-vp*D(xi)
    localQ=beta*((M*energy-Io)*dlm-M*p*fp*dlmu-M*dfq)+beta*(D(Z)*s-beta*Z*s**2)*dd-beta*b*M*Z**2*dlm/2
    remainder=(D(shift)-D(vp)+beta*M*p/mu)*xi+D(-dfsq+(D(Z)-2*beta*Z*s)*dd)+D((-dfss-2*beta*d*Z)*D(chi))+localQ+(beta*d*D(Z)-2*beta**2*d*Z*s-beta*M*fs)*D(chi)+(-2*beta*D(d*s)-beta*b*M*Z-beta**2*d*s**2)*zeta-beta*M*dSig
    check('complete_canonical_current_remainder_exact',sp.expand(current-principal-remainder)==0)
    check('omitting_other_current_source_rejected',sp.expand(current-principal-remainder+beta*M*dSig)!=0)
    check('omitting_local_regulator_Z_term_rejected',sp.expand(current-principal-remainder+beta*b*M*Z*zeta)!=0)
    # Auxiliary decomposition, retaining arbitrary coefficient functions.
    k,ell,ap,v,B,Bpsi,P,Q,L,V,q,Y,rq,rv,G2,G1,Gq0,Gq1=[fn(n) for n in ['k','ell','ap','v','B','Bpsi','P','Q','L','V','q','Y','rq','rv','G2','G1','Gq0','Gq1']]
    Op=lambda u:-k*sp.diff(u,z,2)-ell*D(u)
    aux=-k*sp.diff(chi,z,2)-ell*D(chi)+P*q+Q*D(q)
    actual=Op(ap*xi-v*D(chi)+B*q+Bpsi*chi)+P*(V*Y+rv)+Q*D(V*Y+rv)+G2*sp.diff(chi,z,2)+G1*D(chi)+Gq0*q+Gq1*D(q)
    fast=-k*ap*sp.diff(xi,z,2)-(2*k*D(ap)+ell*ap)*D(xi)-v*D(aux)
    coupling=(-k*B*L+Q*V+v*Q*L)*D(Y)
    R=(-k*sp.diff(ap,z,2)-ell*D(ap))*xi
    R+=(2*k*D(v)-v*D(k)-k*Bpsi+G2)*sp.diff(chi,z,2)
    R+=(k*sp.diff(v,z,2)+ell*D(v)-v*D(ell)-2*k*D(Bpsi)-ell*Bpsi+G1)*D(chi)
    R+=(-k*sp.diff(Bpsi,z,2)-ell*D(Bpsi))*chi
    R+=(-k*B*D(L)+P*V+Q*D(V)+v*Q*D(L))*Y
    R+=(-k*B+v*Q)*D(rq)+P*rv+Q*D(rv)
    R+=(-2*k*D(B)-ell*B+v*(P+D(Q))+Gq1)*D(q)
    R+=(-k*sp.diff(B,z,2)-ell*D(B)+v*D(P)+Gq0)*q
    residual=sp.expand(actual-fast-coupling-R)
    residual=residual.subs(sp.diff(q,z,2),D(L)*Y+L*D(Y)+D(rq)).doit()
    check('complete_auxiliary_cross_coupling_and_remainder_exact',sp.expand(residual)==0)
    check('omitted_ordinary_derivative_coupling_detected',sp.expand(coupling)!=0)
    # Instantaneous conformal coefficient derivatives, not a future ansatz.
    t=sp.symbols('t');a=sp.Function('a')(t,z);ph=sp.Function('psi')(t,z)
    ht=sp.diff(a,t)/a;lam=sp.diff(a,z)/a;ss=sp.diff(ph,z)
    check('auxiliary_P_transverse_time_derivative_exact',sp.simplify(sp.diff(lam*ss/a**4,t)-(sp.diff(ht,z)*ss+lam*sp.diff(ss,t)-4*ht*lam*ss)/a**4)==0)
    check('auxiliary_P_longitudinal_time_derivative_exact',sp.simplify(sp.diff(sp.diff(ss,z)/a**4,t)-(sp.diff(ss,t,z)-4*ht*sp.diff(ss,z))/a**4)==0)
    check('auxiliary_Q_time_derivative_exact',sp.simplify(sp.diff(ss/a**4,t)-(sp.diff(ss,t)-4*ht*ss)/a**4)==0)
    g,w,p0,s0,kap=sp.symbols('g w p s kap');cv=g*g-1
    rest=cv*(p0+w*s0/(g+1))**2+2*w*s0*(p0+w*s0/(g+1))+kap*s0*s0
    expanded=cv*p0*p0+2*g*w*p0*s0+(kap+w*w)*s0*s0
    check('positive_sum_square_force_Y_identity',sp.factor(rest-expanded)==0)
    n=sp.symbols('n',integer=True,positive=True)
    check('H2_first_derivative_half_bound_all_integer_modes',sp.expand((1+n*n)**2-4*n*n-(n*n-1)**2)==0)
    check('H2_second_derivative_L2_bound',sp.expand((1+n*n)**2-n**4)==2*n*n+1)
    rows=parent['bounds_binary'];uniform={}
    for key,row in rows.items():
        check('nine_nonnegative_finite_bounds_'+key,len(row)==9 and all(exact(v[0])>=0 and exact(v[1])>=exact(v[0]) for v in row))
        maximum=max(exact(v[1]) for v in row);upper=(maximum.numerator+maximum.denominator-1)//maximum.denominator
        uniform[key]=upper;check('outward_uniform_summary_'+key,Fraction(upper)>=maximum)
    check('all_source_bytes_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
    return dict(kind='RTAU_ACTUAL_FORCE_PAIR_AUDIT_V1',source_sha256=pins,checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),uniform_sum_norm_bounds=uniform,scope='SAME_AUTHOR_INDEPENDENT_COMPLETE_DIFFERENTIAL_IDENTITIES_AND_EXACT_ENDPOINT_CONTROLS_ONLY',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED')
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=ap.parse_args()
    if a.output:assert not a.output.parent.exists()
    d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
    if a.output:
        a.output.parent.mkdir(parents=True);a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
    else:assert a.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'uniform':d['uniform_sum_norm_bounds'],'physics_pass':False}))
    if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
