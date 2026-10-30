"""Controlled initial cusp balance and a necessary near-node model diagnostic.

No nonlinear space-time remainder, causal propagator or weak admission.
"""
import argparse,hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_full_node_current_v1_attempt_01/summary.json'
PSHA='20903f24484d1b0fec37e00b036182404638edd68984a84bef33c1692ae64a92'
POLE='Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v2_attempt_01/summary.json'
KIN='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
JAC='Analysis/MasterTests/outputs/r4c1_full_initial_jacobi_v1_attempt_01/summary.json'
JOINT='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
CERTS='Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/certificates.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_auxiliary_pole_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_INNER_BALANCE_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_FULL_NODE_CURRENT_V1_REPORT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda v:mp.nstr(v,65)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def calculate():
    mp.mp.dps=130;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        rows=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(x) for z in rows if (x:=s.factor(s.cancel(z)))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,REPORT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            f=ROOT/path
            assert SHA(f.read_bytes())==want and Path(str(f)+'.sha256').read_text().split()[0].lower()==want,path
    verify();en=load('inner_initial_bound',ENGINE);po=READ(POLE)
    w,H,HB,U,W,T,wp,Rp,ap,Tz=s.symbols('w H HB U W T wp Rp aPsi Tz',real=True)
    A,b,p,beta,K=s.Rational(1,28),s.Rational(5,44),s.Rational(1,20),s.Rational(1,40),s.Rational(3,4)
    qvars={'w':w,'H':H,'HB':HB,'U':U,'W':W,'T':T,'wp':wp,'Rp':Rp,'aPsi':ap}
    qfull=s.sympify(po['formulas']['initial_auxiliary_cusp_quotient'],locals=qvars)
    apfull=-3*H*p+HB*p+T*wp*p-U-W*w*w+Rp*p
    q0=A*p/b*(3*p*HB+6*U+2*beta*p*p)
    source=-b*q0;apnode=apfull.subs({w:0,Rp:T*wp})
    rawsource=3*A*p*p*(6*H-3*HB-3*T*wp-Rp)+6*A*p*ap-2*beta*A*p**3
    zero('exact_node_H_and_shift_cancellation',rawsource.subs(ap,apnode).subs(Rp,T*wp)-source)
    zero('original_auxiliary_cusp_node_coefficient',qfull.subs({w:0,ap:apnode}).subs(Rp,T*wp)-q0)
    Bmat=s.Matrix([[s.sympify(v,locals={'w':w}) for v in row] for row in READ(KIN)['formulas']['B']])
    Cvec=s.Matrix([s.sympify(v,locals={'w':w,'Z':s.Symbol('Z')}).subs(s.Symbol('Z'),w*w*(U+W*w*w)) for v in READ(KIN)['formulas']['C']])
    rr=s.Matrix([0]*12);slots=(0,3,5,7)
    force=s.Matrix([-A*p**3*w**3/2,-2*A*p**3*w**3,-A*p**3*w**3/2,-3*A*p**3*w*w])
    response=Bmat.extract(slots,slots).inv(method='DM')*force
    for i,v in zip(slots,response):rr[i]=s.cancel(v)
    remainder=s.cancel((Cvec.T*rr)[0]/(b*w**3)+6*A*p*W/b*w*w-3*A*p*p/b*w*Tz)
    zero('exact_full_normal_cusp_remainder',qfull.subs(ap,apfull).subs(Rp,T*wp+w*Tz)-q0-remainder)
    for i in (6,7,8):zero('all_frame_leading_mass_'+str(i),Bmat[i,i].subs(w,0)-s.Rational(1,24))
    for i in (6,7,8):
        for j in (6,7,8):
            if i!=j:zero('frame_mass_cross_at_node_'+str(i)+'_'+str(j),Bmat[i,j].subs(w,0))
    lead=s.Rational(9,560000);coefficient=s.Rational(297,2800000)
    zero('frame_cusp_drives_scalar_jerk',-p*s.limit(rr[7]/w**2,w,0)-lead)
    zero('inner_auxiliary_third_jet_matches_pole',K*lead/b-coefficient)
    cert=next(z for z in READ(CERTS) if z['family']=='new_B1_frame' and z['eta']=='1/4')
    hb0,hb1=map(en.endpoint,cert['H_background']['exact_binary_endpoints'])
    u0lo=hb0/20+F(1,150);u0hi=hb1/20+F(1,150)
    ulo,uhi=F(49,50)*u0lo,F(51,50)*u0hi
    check('restricted_joint_root_and_box_certified',READ(JOINT)['certificate_status']=='RESTRICTED_FOUR_CONDITION_ROOT_CERTIFIED')
    check('input_box_positive_within_inherited_envelopes',0<hb0<=hb1<1 and 0<ulo<uhi<1)
    qvalue=lambda hh,uu:F(11,700)*(F(3,20)*hh+6*uu+F(1,8000))
    qlo,qhi=qvalue(hb0,ulo),qvalue(hb1,uhi)
    env={key:F(value) for key,value in po['envelopes'].items()};r=F(1,1000);bn=F(5,44)
    CQ=env['CF']*env['Ma']/bn+6*F(1,28)*F(1,20)*38/bn*r+3*F(1,28)*F(1,20)**2/bn*F(1,20)
    check('initial_auxiliary_cusp_positive_on_entire_frozen_neighborhood',qlo-CQ*r>0)
    rradius=F(po['certified_radius']);cn=F(297,2800000)
    ratio_lo=F(2,3)*(qlo-CQ*rradius)/cn;ratio_hi=2*(qhi+CQ*rradius)/cn
    check('initial_derivative_ratio_scale_is_positive',0<ratio_lo<ratio_hi)
    # Independent full20 initial Jacobi templates; every field is kept.
    weights=[7]*6+[6]*3+[7]*3+[7,5,9,3]+[6]*3+[7]
    names=('zero','time','space','time_time','time_space','space_space');orders=(0,2,1,4,3,2)
    graded=[]
    for name in READ(JAC)['file_sha256']:
        row=READ((Path(JAC).parent/name).as_posix())
        if 'node' not in row['label']:continue
        angle=mp.mpf(row['theta']);wv=mp.cos(angle)/500;u=abs(wv)
        sigma=-mp.mpf(2)/25 if 'node1' in row['label'] else mp.mpf(2)/25
        matrices={key:mp.matrix([[mp.mpf(v) for v in rr] for rr in row['full_twenty_coefficients'][key]]) for key in names}
        errors=[]
        for key,order in zip(names,orders):
            for i,power in ((12,3),(13,5),(6,2),(7,2),(8,2)):
                for j in range(20):
                    got=matrices[key][i,j]*u**(weights[j]-order-power)
                    if key in ('space','time_space'):got*=sigma
                    if key=='space_space':got*=sigma*sigma
                    target=mp.mpf(0)
                    if key=='zero' and (i,j)==(12,15):target=-mp.mpf(1)/40
                    if key=='zero' and (i,j)==(13,13):target=mp.mpf(5)/44
                    if key=='time_time':
                        if (i,j)==(12,12):target=-mp.mpf(3)/4
                        if (i,j) in ((12,13),(13,12)):target=mp.mpf(5)/44
                        if i in (6,7,8) and i==j:target=-mp.mpf(1)/24
                    if key=='space_space' and (i,j) in ((12,13),(13,12)):target=mp.mpf(5)/44*sigma*sigma
                    if key=='time' and (i,j)==(13,7):target=mp.mpf(5)/44*mp.mpf(1)/20*mp.sign(wv)
                    if key=='space' and (i,j)==(13,8):target=mp.mpf(5)/44*mp.mpf(1)/20*sigma
                    errors.append((abs(got-target),key,i,j))
        worst=max(errors)
        graded.append(dict(label=row['label'],absw=show(u),maximum_template_deviation=show(worst[0]),key=worst[1],row=worst[2],column=worst[3]))
        # Exact finite-w identities check the dangerous negatively weighted
        # entries; template deviations themselves are observations, not bounds.
        raw=next(z for z in READ('Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json')['points'] if z['label']==row['label'])
        inp=READ(raw['raw_point_source'])['original_first_jet'];hh=mp.mpf(READ(JOINT)['point']['H'])
        hb=mp.mpf(hb0.numerator)/hb0.denominator;tv=mp.mpf(inp[50])/wv;rpv=mp.mpf(inp[53]);wpv=mp.mpf(inp[39])
        exacts=[('potential',matrices['zero'][13,13],mp.mpf(5)/44),
            ('frame_time',matrices['time'][13,7],mp.mpf(5)/44*mp.mpf(1)/20*wv),
            ('normal_frame_divergence',matrices['space'][13,8],mp.mpf(5)/44*mp.mpf(1)/20*mp.sqrt(1+wv*wv)),
            ('auxiliary_time_drift',matrices['time'][12,13],mp.mpf(5)/44*wv*wv*(7*hh-3*hb-3*tv*wpv-rpv))]
        for label,got,want in exacts:
            error=abs(got-want)/(1+abs(got)+abs(want));check('original_finite_w_'+label+'_'+row['label'],error<mp.mpf('1e-18'),show(error))
    # The required lower potential, normal divergence and density term are
    # explicit; omission is not accepted as a new leading model.
    check('all_four_orientations_exported',len(graded)==4)
    # Exact variable-coefficient fourth-order and commuting factors.
    x,t=s.symbols('x t',real=True);f=s.Function('Psi')(t,x);a=s.Rational(4,625);kappa=K/b
    Lop=lambda z:x*x*s.diff(z,t,2)+a*s.diff(z,x,2)
    expanded=x**4*s.diff(f,t,4)+2*a*x*x*s.diff(f,t,2,x,2)+4*a*x*s.diff(f,t,2,x)+2*a*s.diff(f,t,2)+a*a*s.diff(f,x,4)
    zero('variable_coefficient_square_retains_commutators',Lop(Lop(f))-expanded)
    gamma=s.sqrt(kappa)
    zero('complex_second_order_factorization',Lop(Lop(f)-s.I*gamma*s.diff(f,t))+s.I*gamma*s.diff(Lop(f)-s.I*gamma*s.diff(f,t),t)-Lop(Lop(f))-kappa*s.diff(f,t,2))
    check('dropping_variable_coefficient_commutators_changes_operator',s.expand(expanded-(x**4*s.diff(f,t,4)+2*a*x*x*s.diff(f,t,2,x,2)+a*a*s.diff(f,x,4)))!=0)
    for sign in (-1,1):zero('cusp_forcing_second_normal_derivative_'+str(sign),s.diff(sign*x**3,x,2)-6*sign*x)
    # Hermite ladder proves every integer level; no finite-level scan is used.
    y=s.symbols('y',real=True);v=s.Function('v')(y)
    osc=lambda z:-s.diff(z,y,2)+y*y*z
    raise_op=lambda z:-s.diff(z,y)+y*z
    zero('Hermite_ground_state',osc(s.exp(-y*y/2))-s.exp(-y*y/2))
    zero('Hermite_all_level_ladder',osc(raise_op(v))-raise_op(osc(v))-2*raise_op(v))
    n=s.symbols('n',integer=True,nonnegative=True);lam=lambda j:a*(2*j+1)**2-kappa
    zero('all_lower_levels_gap_factor',lam(15)-lam(n)-4*a*(15-n)*(n+16))
    zero('all_upper_levels_gap_factor',lam(n)-lam(16)-4*a*(n-16)*(n+17))
    zero('nearest_lower_level',lam(15)+s.Rational(281,625))
    zero('nearest_upper_level',lam(16)-s.Rational(231,625))
    check('all_level_nonzero_frequency_gap',s.Rational(231,625)>0 and s.Rational(281,625)>s.Rational(231,625))
    # Independent finite Hermite-polynomial oscillator identities, both nearest
    # levels included; normalization is irrelevant to the differential identity.
    for j in (0,1,2,15,16):
        polynomial=s.hermite(j,y)
        zero('independent_Hermite_level_'+str(j),s.diff(polynomial,y,2)-2*y*s.diff(polynomial,y)+2*j*polynomial)
    verify()
    return dict(result_id='R4C1-INNER-BALANCE-V1',source_sha256=pins,checks=checks,
        exact_formulas=dict(auxiliary_cusp_node=str(q0),scalar_node_source=str(source),initial_acceleration_remainder=str(remainder),
            scaling='t=epsilon^2*T,w=epsilon*X; deltaZ=epsilon^5*Z,deltaPsi=epsilon^7*Psi,deltaVi=epsilon^6*Vi',
            leading_operator='L=X^2*d_TT+(4/625)*d_XX',scalar_fourth_order='L^2+(33/5)*d_TT',
            scalar_forcing='(S0/b)*abs(X)^3+6*(9/560000)*(4/625)*abs(X)*T'),
        node_coefficient_bounds=dict(lower=str(qlo),upper=str(qhi),quotient_remainder_constant=str(CQ),
            statement='abs(delta(aZ)/abs(w)-Q0)<=C_Q*abs(w),0<abs(w)<=1/1000'),
        initial_derivative_ratio=dict(lower=str(ratio_lo),upper=str(ratio_hi),domain='0<abs(w)<=1/134217728',
            statement='lower*w^2<=delta(aZ)/delta(jZ)<=upper*w^2; not a time interval'),
        initial_full_twenty_graded_controls=graded,
        necessary_model=dict(frame='V_TT=-(9/28000)*X*abs(X); Vx_TT=Vz_TT=0',
            clock_lapse='E_T=0;E=2*A*p^3*abs(X)^3;Theta_T=N+beta*Psi',
            scalar='K*Psi_TT-b*L(Z)=S0*abs(X)^3',
            auxiliary='Z+L(Psi)+p*X*V_T+p*sigma*Vz_X=0; Vz=0 follows only with zero leading initial data',
            metric_constraint_completion_proved=False),
        hermite_model=dict(kappa=str(kappa),sigma_squared=str(a),nearest_levels=[15,16],
            nearest_level_coefficients=['-281/625','231/625'],all_level_gap='231/625',
            estimate='finite Hermite spans,omega!=0: norm(u)<=625/(231*omega^2)*norm(P_omega*u)',
            whole_line_normal_model_only=True,zero_frequency_resolved=False,causal_Cauchy_propagator=False),
        controlled_initial_cusp_remainder=True,uniform_full_original_spacetime_remainder=False,
        full_inner_metric_constraint_completion=False,actual_torus_source_in_model_domain_proved=False,
        physical_window_established=False,weak_solution_admitted=False,time_evolution=False,
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        reference='NIST DLMF 18.3,18.8: Hermite normalization/ODE; model factor and gap derived here')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();result['passed']=sum(c['passed'] for c in result['checks']);result['total']=len(result['checks']);data=ENC(result)
    if args.replay:
        assert (args.replay/'summary.json').read_bytes()==data,'immutable replay mismatch';print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);f=args.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','controlled_initial_cusp_remainder','uniform_full_original_spacetime_remainder','weak_solution_admitted','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
