"""Full-action conditional junctions and a finite-action concentration test.

The test family is not a solution of the coupled equations or an adopted state.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_inner_cauchy_v2_attempt_01/summary.json'
PSHA='af69719181338bae198181b7f6ee973cbcfb65a0166e160f206d973e8edfadd3'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NODAL_TRANSFER_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_INNER_CAUCHY_V2_REPORT_2026-10-29.md'
ACTION='Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md'
VARIATION='Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda v:mp.nstr(v,65)


def endpoint(q):
    sign,man,exp,_=q
    return F((-1 if sign else 1)*man)*F(2)**exp


def iv(v):
    v=F(v);return mp.iv.mpf(v.numerator)/v.denominator


def pack(v):return dict(lower=str(endpoint(v._mpi_[0])),upper=str(endpoint(v._mpi_[1])))


def calculate():
    mp.mp.dps=110;mp.iv.dps=90;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        bad=s.simplify(expr);check(name,bad==0,str(bad))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total'] and parent['selfsimilar_model_sourcefree_function_junction_rejected']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,REPORT,ACTION,VARIATION,Path(__file__).relative_to(ROOT).as_posix()):
        got=SHA((ROOT/path).read_bytes())
        if path in pins:assert pins[path]==got,path
        pins[path]=got
    def verify():
        for path,want in pins.items():
            f=ROOT/path;assert SHA(f.read_bytes())==want and Path(str(f)+'.sha256').read_text().split()[0].lower()==want,path
    verify()
    b=s.Rational(5,44);a=s.Rational(4,625)
    Z,D=s.symbols('Z DeltaPsi',real=True)
    zero('original_auxiliary_square_completion',b*Z**2/2+b*Z*D-(b*(Z+D)**2/2-b*D**2/2))
    zero('original_auxiliary_equation_sign',s.diff(b*Z**2/2+b*Z*D,Z)-b*(Z+D))
    x=s.symbols('x',real=True);h=s.Function('h')(x);acc=s.Function('acc')(x);f=s.Function('f')(x)
    Delta=lambda z:s.diff(h*s.diff(z,x),x)-acc*s.diff(z,x)
    adjoint=lambda z:s.diff(h*s.diff(z,x)+acc*z,x)
    zero('formal_adjoint_acceleration_retained',adjoint(f)-Delta(f)-2*acc*s.diff(f,x)-s.diff(acc,x)*f)
    check('formal_adjoint_not_silently_self_adjoint',s.expand(adjoint(f)-Delta(f))!=0)
    w,v=s.symbols('w velocity',real=True)
    metric=s.diag(-1,1,1,1);n=s.Matrix([s.sqrt(1+w*w),0,w,0]);normal=s.Matrix([-v,0,0,1])
    proj=metric+n*n.T;nn=s.simplify((normal.T*proj*normal)[0])
    zero('moving_registered_node_projected_normal_norm',nn-(1+w*w*v*v))
    zero('registered_node_is_noncharacteristic',nn.subs(w,0)-1)
    location=s.symbols('location',real=True)
    model_norm=a+location**2*v**2
    check('real_node_motion_cannot_cancel_model_normal_coefficient',a>0 and s.Poly(model_norm,location,v).coeff_monomial(1)==a)
    # Highest interface distributions are independent, even with a dust
    # Radon surface density: a delta cannot cancel a delta-prime coefficient.
    zjump,gradjump,phi0,phi1=s.symbols('jumpZ jumpGrad phi0 phi1',real=True)
    highest_aux=b*nn*gradjump*phi0
    highest_scalar=-b*nn*zjump*phi1
    zero('auxiliary_interface_test_constant',s.diff(highest_aux,phi0)-b*nn*gradjump)
    zero('scalar_double_layer_test_linear',s.diff(highest_scalar,phi1)+b*nn*zjump)
    check('delta_prime_cannot_be_nonnegative_dust_measure',-s.diff((1+x)**2,x).subs(x,0)<0 and -s.diff((1-x)**2,x).subs(x,0)>0)
    # Explicit normal smoothing component. epsilon is a scaling parameter,
    # not a newly chosen physical cutoff or a prescribed junction source.
    xx,tt,eps,c=s.symbols('X T epsilon c',positive=True)
    smooth=c*tt**3*s.sqrt(xx**2+eps**2*tt**2)
    correction=smooth-c*tt**3*xx
    core=-a*c*eps**2*tt**5/(xx**2+eps**2*tt**2)**s.Rational(3,2)
    zero('normal_auxiliary_core_from_smoothed_scalar',-a*s.diff(smooth,xx,2)-core)
    for order in range(5):zero('off_node_scalar_initial_jet_unchanged_'+str(order),s.diff(correction,tt,order).subs(tt,0))
    zero('first_changed_off_node_scalar_jet',s.diff(correction,tt,5).subs(tt,0)-60*c*eps**2/xx)
    zero('smoothing_uniform_bound_rationalization',(s.sqrt(xx**2+eps**2*tt**2)-xx)*(s.sqrt(xx**2+eps**2*tt**2)+xx)-eps**2*tt**2)
    # sqrt(X^2+l^2)<=abs(X)+l follows by squaring:2*abs(X)*l>=0.
    ell=s.symbols('ell',positive=True)
    check('uniform_smoothing_bound_has_nonnegative_square_difference',s.expand((xx+ell)**2-(xx*xx+ell*ell))==2*xx*ell)
    y=s.symbols('y',real=True)
    kernel=(1+y*y)**(-s.Rational(3,2))
    zero('kernel_mass_antiderivative',s.diff(y/s.sqrt(1+y*y),y)-kernel)
    zero('kernel_positive_first_moment_antiderivative',s.diff(-1/s.sqrt(1+y*y),y)-y*kernel)
    mass=s.limit(y/s.sqrt(1+y*y),y,s.oo)-s.limit(y/s.sqrt(1+y*y),y,-s.oo)
    zero('kernel_mass_exact',mass-2)
    first=2*(s.limit(-1/s.sqrt(1+y*y),y,s.oo)+1)
    zero('kernel_absolute_first_moment_exact',first-2)
    theta=s.symbols('theta',real=True)
    normint=s.integrate(s.cos(theta)**4,(theta,-s.pi/2,s.pi/2))
    zero('kernel_square_integral_exact',normint-3*s.pi/8)
    # Under X=epsilon*T*y: core dX=-a*c*T^3*k(y)dy.
    zero('core_mass_scaling',s.simplify(core.subs(xx,eps*tt*y)*eps*tt)+a*c*tt**3*kernel)
    zero('core_L2_scaling',s.simplify(core.subs(xx,eps*tt*y)**2*eps*tt)-a*a*c*c*tt**5/eps/(1+y*y)**3)
    # Original fields:Z_phys=epsilon^5*core, dw dt=epsilon^3*dX dT.
    zero('original_auxiliary_square_action_scaling',eps**10*eps**3/eps-eps**12)
    zero('rescaled_auxiliary_square_is_not_uniform',eps**12/eps**13-1/eps)
    physical_t,physical_w=s.symbols('physical_t physical_w',positive=True)
    physical_core=-a*c*physical_t**5/(physical_w**2+physical_t**2)**s.Rational(3,2)
    zero('physical_and_rescaled_core_agree',physical_core.subs({physical_t:eps**2*tt,physical_w:eps*xx})-eps**5*core)
    zero('physical_core_amplitude_scale',physical_core.subs(physical_w,physical_t*y)+a*c*physical_t**2/(1+y*y)**s.Rational(3,2))
    zero('physical_core_spatial_gradient_scale',s.diff(physical_core,physical_w).subs(physical_w,physical_t*y)-3*a*c*physical_t*y/(1+y*y)**s.Rational(5,2))
    zero('physical_core_time_gradient_scale',s.diff(physical_core,physical_t).subs(physical_w,physical_t*y)+a*c*physical_t*(5/(1+y*y)**s.Rational(3,2)-3/(1+y*y)**s.Rational(5,2)))
    zero('new_scalar_double_derivative_defect_sign',-b*a*(-2*a*c)-2*b*a*a*c)
    # Quantitative weak bound uses the finite first kernel moment:
    # |<core+2*a*c*T^3 delta,phi>|<=2*a*c*epsilon*T^4*Lip(phi).
    controls=[]
    for e in (mp.mpf(1)/10,mp.mpf(1)/100):
        value=2*mp.quad(lambda yy:(1+yy*yy)**(-mp.mpf('1.5'))*mp.exp(-(e*yy)**2),[0,1,1/e,mp.inf])
        difference=abs(value-2)
        check('independent_gaussian_weak_limit_e'+mp.nstr(e,3),difference<=2*e,show(difference))
        controls.append(dict(epsilon=show(e),normalized_pairing=show(value),mass_error=show(difference),proved_error_bound=show(2*e)))
    square=2*mp.quad(lambda yy:(1+yy*yy)**-3,[0,1,mp.inf])
    check('independent_L2_integral_control',abs(square-3*mp.pi/8)<mp.mpf('1e-90'),show(abs(square-3*mp.pi/8)))
    cb=parent['actual_connection_coefficients']['power_3']
    ci=mp.iv.mpf([iv(F(cb['lower'])).a,iv(F(cb['upper'])).b])
    defect=2*iv(F(5,44))*iv(F(4,625))**2*ci
    check('scalar_defect_double_layer_excludes_zero',endpoint(defect._mpi_[0])>0)
    verify()
    return dict(result_id='R4C1-NODAL-TRANSFER-V1',source_sha256=pins,checks=checks,
        full_action_identities=dict(auxiliary='E_Z=b*(Z+Delta psi)',
            Delta='div(h grad psi)-a dot grad psi',adjoint='Delta_dagger Z=div(h grad Z+Z*a)',
            square='L_reg=bulk b/2*(Z+Delta psi)^2-b/2*(Delta psi)^2 minus b*div(Z*h*grad psi)',
            scalar_gradient_junction='[normal gradient psi]=0 if h(N,N)>0 and Z has no surface distribution',
            auxiliary_value_junction='[Z]=0 if matter is a Radon measure and metric/frame are continuous with piecewise bounded first derivatives',
            remaining_scalar_surface='b*(N.h.[grad Z]+Z*N.[a])-beta*rho_surface=0 after the two regular junctions'),
        diagnostic_family=dict(correction='c*T^3*(sqrt(X^2+epsilon^2*T^2)-abs(X))',
            core=str(core),initial_scalar_jets_preserved_off_node='orders0 through4',
            uniform_correction_bound='abs(c)*epsilon*T^4',
            mass='-2*a*c*T^3',weak_error='2*a*abs(c)*epsilon*T^4*norm(phi_prime)_infinity',
            rescaled_L2_square='3*pi*a^2*c^2*T^5/(8*epsilon)',
            original_chart_auxiliary_square_spacetime_action='b*pi*a^2*c^2*epsilon^12/32 for0<T<1',
            measure='dw dt chart; smooth bounded physical volume Jacobian preserves scaling',
            sourcefree_scalar_failure='2*b*a^2*c*T^3*delta_second(X)',scalar_failure_coefficient=pack(defect)),
        independent_controls=controls,regular_limit_transfers_model_scalar_cusp_obstruction=True,
        unscaled_finite_action_implies_uniform_rescaled_auxiliary_L2=False,
        smoothing_family_solves_full_scalar_equation=False,smoothing_family_adopted=False,
        full_original_spacetime_limit_proved=False,full_original_weak_continuations_excluded=False,
        actual_concentrated_on_shell_layer_constructed=False,time_evolution=False,
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();result['passed']=sum(c['passed'] for c in result['checks']);result['total']=len(result['checks']);data=ENC(result)
    if args.replay:
        assert (args.replay/'summary.json').read_bytes()==data,'immutable replay mismatch';print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);f=args.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','unscaled_finite_action_implies_uniform_rescaled_auxiliary_L2','smoothing_family_solves_full_scalar_equation','full_original_weak_continuations_excluded','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
