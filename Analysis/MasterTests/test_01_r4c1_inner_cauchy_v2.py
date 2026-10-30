"""Certified connection coefficients for the necessary inner model only."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sy
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_inner_balance_v1_attempt_01/summary.json'
PSHA='4802390fc31a255135c339af0fa8efbe7a53166d245834ef06586ae2ee9d81f0'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_INNER_CAUCHY_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_INNER_BALANCE_V1_REPORT_2026-10-29.md'
V1='Analysis/MasterTests/test_01_r4c1_inner_cauchy_v1.py'
FAILED='Analysis/MasterTests/outputs/r4c1_inner_cauchy_v1_attempt_01/summary.json'
NOTE='Theory/Gates/RES-001/RES001_R4C1_INNER_CAUCHY_V2_IMPLEMENTATION_NOTE_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
a=F(4,625);b=F(5,44);K=F(3,4);kap=K/b
ORDER=512;FROB_ORDER=128;MATCH=16


def exact(endpoint):
    sign,man,exp,_=endpoint
    return F((-1 if sign else 1)*man)*F(2)**exp


def iv(x):
    x=F(x);return mp.iv.mpf(x.numerator)/x.denominator


def lo(x):return exact(x._mpi_[0])
def hi(x):return exact(x._mpi_[1])
def upper(x):return hi(abs(x))
def centered(center,radius):return iv(center)+mp.iv.mpf([-iv(radius).b,iv(radius).b])
def pack(x):return dict(lower=str(lo(x)),upper=str(hi(x)))
def ceil(x):return -((-x.numerator)//x.denominator)


def step(state,center,S,L):
    """One unit Taylor step, radius2 analytic disk and exact Cauchy tail."""
    c=F(center);R=F(2)
    dmin=4*a*(max(c,F(25,4))-R)**2
    row2=(42*a+22*a*(c+R)+1)/dmin
    row4=kap/dmin*row2+(20*a+14*a*(c+R))/dmin
    am=max(F(1),row2,row4)
    forcing2=abs(L)*(c+R)/dmin
    forcing=max(forcing2,kap/dmin*forcing2+abs(S)/(b*dmin))
    bound=(max(upper(x) for x in state)+R*forcing)*3**(2*ceil(am))
    tail=bound/F(2)**ORDER
    ff=[state[0],state[1]];gg=[state[2],state[3]]
    ai,bi,ki,ci,si,li=map(iv,(a,b,kap,c,S,L))
    D0=1+4*ai*ci*ci;D1=8*ai*ci;D2=4*ai
    for n in range(ORDER):
        dn=(n+2)*(n+1)
        rhs=li*(ci if n==0 else 1 if n==1 else 0)-gg[n]+22*ai*ci*(n+1)*ff[n+1]
        rhs+=(22*ai*n-42*ai-D2*n*(n-1))*ff[n]-D1*n*(n+1)*ff[n+1]
        fn=rhs/(D0*dn);ff.append(fn)
        rhs=ki*dn*fn+14*ai*ci*(n+1)*gg[n+1]
        rhs+=(14*ai*n-20*ai-D2*n*(n-1))*gg[n]-D1*n*(n+1)*gg[n+1]
        if n==0:rhs-=si/bi
        gg.append(rhs/(D0*dn))
    sums=[sum(ff[:ORDER+1],iv(0)),sum(((n+1)*ff[n+1] for n in range(ORDER+1)),iv(0)),
          sum(gg[:ORDER+1],iv(0)),sum(((n+1)*gg[n+1] for n in range(ORDER+1)),iv(0))]
    result=[z+mp.iv.mpf([-iv(tail).b,iv(tail).b]) for z in sums]
    return result,dict(center=str(c),denominator_lower=str(dmin),matrix_bound=str(am),
        forcing_bound=str(forcing),complex_state_majorant=str(bound),tail_bound=str(tail),state=list(map(pack,result)))


def transfer(S,L):
    state=[iv(0)]*4;records=[]
    for center in range(MATCH):
        state,row=step(state,center,F(S),F(L));records.append(row)
    return state,records


def frobenius(power):
    """Convergent infinity basis, normalized by the leading F coefficient."""
    A=lambda z:4*z*z-26*z+42
    B=lambda z:4*z*z-18*z+20
    ff=[F(1)];gg=[-a*A(power)]
    for k in range(1,FROB_ORDER+1):
        rho=power-2*k;pref=(rho+2)*(rho+1)
        gn=pref*(kap*ff[-1]-gg[-1])/(a*B(rho))
        fn=-(gn+pref*ff[-1])/(a*A(rho))
        ff.append(fn);gg.append(gn)
    point=F(MATCH);p0=F(4)**int(2*power);p1=p0/point
    values=[p0*sum(v/point**(2*k) for k,v in enumerate(ff)),
        p1*sum((power-2*k)*v/point**(2*k) for k,v in enumerate(ff)),
        p0*sum(v/point**(2*k) for k,v in enumerate(gg)),
        p1*sum((power-2*k)*v/point**(2*k) for k,v in enumerate(gg))]
    # For rho<=-10, max(abs(f_k),abs(g_k)/kap) grows at most160
    # per coefficient step. Proof is checked below for every later index.
    mn=max(abs(ff[-1]),abs(gg[-1])/kap);ratio=F(160)/point**2
    pref=mn/point**(2*FROB_ORDER)
    tail_value=p0*pref*ratio/(1-ratio)
    tail_deriv=p1*pref*((2*FROB_ORDER-power)*ratio/(1-ratio)+2*ratio/(1-ratio)**2)
    tails=[tail_value,tail_deriv,kap*tail_value,kap*tail_deriv]
    enclosure=[centered(v,t) for v,t in zip(values,tails)]
    return enclosure,dict(power=str(power),values=list(map(str,values)),tails=list(map(str,tails)),
        coefficient_sha256=SHA(ENC(dict(F=list(map(str,ff)),G=list(map(str,gg))))),
        coefficient_tail_ratio=str(ratio),state=list(map(pack,enclosure)))


def connection(matrix,y):
    # Midpoint inverse is only a preconditioner. Interval residual and
    # ||I-R*A||<1 enclose the exact solution for every admitted input.
    mid=lambda z:mp.mpf((lo(z)+hi(z)).numerator)/(lo(z)+hi(z)).denominator/2
    midA=mp.matrix([[mid(z) for z in row] for row in matrix]);midy=mp.matrix([mid(z) for z in y])
    R=midA**-1;chat=R*midy
    riv=[[mp.iv.mpf(R[i,j]) for j in range(4)] for i in range(4)]
    civ=[mp.iv.mpf(chat[i]) for i in range(4)]
    E=[[iv(int(i==j))-sum((riv[i][k]*matrix[k][j] for k in range(4)),iv(0)) for j in range(4)] for i in range(4)]
    q=max(sum(upper(z) for z in row) for row in E)
    assert q<1,'interval preconditioner did not certify invertibility'
    residual=[y[i]-sum((matrix[i][j]*civ[j] for j in range(4)),iv(0)) for i in range(4)]
    r=max(upper(sum((riv[i][k]*residual[k] for k in range(4)),iv(0))) for i in range(4))
    error=r/(1-q)
    enclosure=[z+mp.iv.mpf([-iv(error).b,iv(error).b]) for z in civ]
    return enclosure,dict(neumann_norm_upper=str(q),preconditioned_residual_upper=str(r),
        coefficient_error_upper=str(error),coefficients=list(map(pack,enclosure)))


def calculate():
    mp.mp.dps=160;mp.iv.dps=120;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):check(name,sy.factor(sy.cancel(z))==0,str(sy.factor(sy.cancel(z))))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,REPORT,V1,FAILED,NOTE,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path;assert SHA(file.read_bytes())==want and Path(str(file)+'.sha256').read_text().split()[0].lower()==want,path
    verify()
    ss=sy.symbols('s',real=True);rr=sy.symbols('r',real=True);v=sy.symbols('v',nonnegative=True)
    f=sy.Function('F')(ss);g=sy.Function('G')(ss);aa=sy.Rational(4,625)
    Top=lambda m,z:(1+4*aa*ss**2)*sy.diff(z,ss,2)-(4*m-6)*aa*ss*sy.diff(z,ss)+m*(m-1)*aa*z
    zero('indicial_scalar_factor',4*rr**2-26*rr+42-(2*rr-6)*(2*rr-7))
    zero('indicial_auxiliary_factor',4*rr**2-18*rr+20-(2*rr-4)*(2*rr-5))
    # All-tail majorant follows from explicit positive polynomial inequalities.
    rho=-(10+v)
    for name,z in [('A_at_least_702',4*rho**2-26*rho+42-702),
        ('B_at_least_4rho2',-18*rho+20),('prefactor_at_most_rho2',rho**2-(rho+2)*(rho+1))]:
        check('tail_'+name,all(c>=0 for c in sy.Poly(sy.expand(z),v).all_coeffs()))
    check('tail_weighted_norm_ratio_bound',kap/(a*702)/(2*a)+1/(4*a)<160 and 1/(2*a)<160)
    check('tail_series_converges_at_matching_point',F(160,MATCH**2)<1)
    # Exact integer modes also independently check signs and normalizations.
    f2=ss**2-sy.Rational(K+26*b*a)/(420*sy.Rational(b)*aa**2)
    g2=-6*aa*ss**2+sy.Rational(K+6*b*a)/(10*sy.Rational(b)*aa)
    f3=ss**3-sy.Rational(K+6*b*a)/(20*sy.Rational(b)*aa**2)*ss
    g3=sy.Rational(K/b)/aa*ss
    for label,ff,gg in [('even',f2,g2),('odd',f3,g3)]:
        zero('integer_'+label+'_auxiliary',gg+Top(7,ff))
        zero('integer_'+label+'_scalar',sy.Rational(K)*sy.diff(ff,ss,2)-sy.Rational(b)*Top(5,gg))
    source_symbol,lead_symbol=sy.symbols('S0 L',real=True)
    particular_f=lead_symbol*ss/(20*aa)+source_symbol/(840*sy.Rational(b)*aa**2)
    particular_g=-source_symbol/(20*sy.Rational(b)*aa)
    zero('exact_particular_scalar_equation',sy.Rational(K)*sy.diff(particular_f,ss,2)-sy.Rational(b)*Top(5,particular_g)-source_symbol)
    zero('exact_particular_auxiliary_equation',particular_g+Top(7,particular_f)-lead_symbol*ss)
    columns=[];frobs=[]
    for power in (F(2),F(5,2),F(3),F(7,2)):
        col,record=frobenius(power);columns.append(col);frobs.append(record)
    matrix=[[columns[j][i] for j in range(4)] for i in range(4)]
    transfers={};connections={};controls=[]
    for label,S,L in [('unit_S',1,0),('unit_L',0,1)]:
        state,record=transfer(S,L)
        particular=[iv(F(L)*MATCH/(20*a)+F(S)/(840*b*a*a)),iv(F(L)/(20*a)),-iv(F(S)/(20*b*a)),iv(0)]
        homogeneous=[v-pv for v,pv in zip(state,particular)]
        coeff,cert=connection(matrix,homogeneous)
        reconstruction=[particular[i]+sum((matrix[i][j]*coeff[j] for j in range(4)),iv(0)) for i in range(4)]
        check(label+'_affine_matching_reconstructs_full_state',all(lo(reconstruction[i])<=lo(state[i]) and hi(reconstruction[i])>=hi(state[i]) for i in range(4)))
        cert['particular_state']=list(map(pack,particular));cert['homogeneous_matching_state']=list(map(pack,homogeneous))
        transfers[label]=dict(steps=record,final_state=list(map(pack,state)))
        connections[label]=dict(enclosure=coeff,certificate=cert)
        check(label+'_certified_connection',F(cert['neumann_norm_upper'])<1)
        # Separate floating DOP853 control; not used to set any interval.
        def rhs(t,y):
            den=1+4*float(a)*t*t
            fp=(L*t-y[2]+22*float(a)*t*y[1]-42*float(a)*y[0])/den
            gp=(float(kap)*fp+14*float(a)*t*y[3]-20*float(a)*y[2]-S/float(b))/den
            return [y[1],fp,y[3],gp]
        ordinary=solve_ivp(rhs,(0,MATCH),[0.0]*4,method='DOP853',rtol=1e-12,atol=1e-14)
        center=[float((lo(z)+hi(z))/2) for z in state]
        error=max(abs(got-want)/(1+abs(got)+abs(want)) for got,want in zip(ordinary.y[:,-1],center))
        check(label+'_independent_ordinary_solver',ordinary.success and error<1e-8,str(error))
        controls.append(dict(label=label,method='DOP853',relative_error=str(error),used_for_certificate=False))
    qbox=parent['node_coefficient_bounds'];source=-iv(b)*mp.iv.mpf([iv(F(qbox['lower'])).a,iv(F(qbox['upper'])).b])
    lead=iv(F(9,560000))
    actual=[connections['unit_S']['enclosure'][j]*source+connections['unit_L']['enclosure'][j]*lead for j in range(4)]
    integer=[actual[0],actual[2]]
    nonzero=[lo(z)>0 or hi(z)<0 for z in integer]
    # These are outcomes, not conditions forced to pass: zero-containing
    # coefficients remain unresolved rather than being replaced by midpoints.
    check('actual_coefficients_have_finite_ordered_enclosures',all(lo(z)<=hi(z) for z in actual))
    zero('model_scalar_flux_jump_coefficient',-sy.Rational(b)*aa*(-12*aa)-12*sy.Rational(b)*aa**2)
    verify()
    return dict(result_id='R4C1-INNER-CAUCHY-V2',source_sha256=pins,checks=checks,
        equations=dict(first='K*Fdd-b*((1+4*a*s^2)*Gdd-14*a*s*Gd+20*a*G)=S0',
            second='G+(1+4*a*s^2)*Fdd-22*a*s*Fd+42*a*F=L*s',
            initial='F=Fd=G=Gd=0 at s=0',source_interval=pack(source),L='9/560000'),
        interval_digits=120,taylor_order=ORDER,frobenius_order=FROB_ORDER,matching_point=MATCH,
        frobenius=frobs,transfers=transfers,connections={key:value['certificate'] for key,value in connections.items()},
        independent_controls=controls,actual_connection_coefficients=dict(zip(['power_2','power_5_over_2','power_3','power_7_over_2'],map(pack,actual))),
        integer_coefficients_exclude_zero=nonzero,
        model_jump_coefficients=dict(scalar_residual_T2=pack(12*iv(b)*iv(a)**2*actual[0]),auxiliary_residual_T3=pack(2*iv(a)*actual[2])),
        selfsimilar_model_sourcefree_function_junction_rejected=any(nonzero) and all(c['passed'] for c in checks),
        rejection_scope='Actual regular off-node selfsimilar necessary-model Cauchy branch; function-valued source-free nodal gluing at finite positive T.',
        all_model_weak_continuations_excluded=False,full_original_weak_continuations_excluded=False,
        full_original_spacetime_remainder_proved=False,new_node_source_or_boundary_adopted=False,
        weak_solution_admitted=False,time_evolution=False,G1_complete=False,physics_pass=False,
        gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();result['passed']=sum(c['passed'] for c in result['checks']);result['total']=len(result['checks']);data=ENC(result)
    if args.replay:
        assert (args.replay/'summary.json').read_bytes()==data,'immutable replay mismatch';print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);file=args.output/'summary.json';file.write_bytes(data)
        Path(str(file)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','integer_coefficients_exclude_zero','selfsimilar_model_sourcefree_function_junction_rejected','full_original_weak_continuations_excluded','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
