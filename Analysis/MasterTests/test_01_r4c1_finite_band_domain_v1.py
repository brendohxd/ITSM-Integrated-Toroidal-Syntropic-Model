"""Exact finite-band domain obstruction for the registered initial construction."""
import argparse,hashlib,json
from pathlib import Path
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_constrained_principal_v1_attempt_01/summary.json'
PSHA='652ae6656487c2cee1fbbc1a8e353f7681ccd83e993294e3e1ea11f178888824'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
JERK='Analysis/MasterTests/outputs/r4c1_quartic_total_jerk_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FINITE_BAND_DOMAIN_V1_CONTRACT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda z:mp.nstr(z,65)


def calculate():
    mp.mp.dps=110;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        rows=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(t) for z in rows if (t:=s.factor(s.cancel(z)))!=0]
        check(name,not bad,bad)
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();w=s.Symbol('w',real=True);A=s.Rational(1,28);p=s.Rational(1,20)
    B=s.Matrix([[s.sympify(z,locals={'w':w}) for z in row] for row in READ(KINETIC)['formulas']['B']])
    sector=(0,3,5,7);rest=tuple(j for j in range(12) if j not in sector)
    zero('actual_metric_Vy_sector_isolation',B.extract(sector,rest))
    f=s.Matrix([-A*p**3*w**3/2,-2*A*p**3*w**3,-A*p**3*w**3/2,-3*A*p**3*w*w])
    response=(B.extract(sector,sector).inv()*f).applyfunc(s.cancel)
    positive=s.factor(response[3]);quotient=s.factor(s.cancel(positive/w**2))
    zero('positive_branch_even',positive.subs(w,-w)-positive)
    check('no_node_denominator',s.fraction(quotient)[1].subs(w,0)!=0)
    leading=s.cancel(quotient.subs(w,0))
    zero('actual_cusp_leading_coefficient',leading+s.Rational(9,28000))
    zero('constant_and_linear_positive_branch',s.Matrix([positive.subs(w,0),s.diff(positive,w).subs(w,0)]))
    zero('second_derivative_jump_in_w',2*s.diff(positive,w,2).subs(w,0)-4*leading)
    # Cross-check the prior jerk kernel; no new frozen-frame approximation.
    prior=s.sympify(READ(JERK)['formulas']['actual_cusp_positive_branch'],locals={'w':w})
    rebuilt=s.cancel(-p*(response[3]/w+sum(response[j] for j in range(3))/2))
    zero('original_coupled_jerk_kernel_reproduced',rebuilt-prior)
    jumps=[]
    for sign in (-1,1):
        sigma=s.Rational(sign*2,25);jump=s.factor(4*leading*sigma*abs(sigma))
        zero('normal_jump_orientation_'+str(sign),jump+s.Rational(sign*9,1093750))
        jumps.append(dict(slope=str(sigma),Vy_acceleration_second_normal_jump=str(jump)))
    # Distributional third derivative of the actual piecewise kernel.
    funcs=s.lambdify(w,[positive,s.diff(positive,w),s.diff(positive,w,2),s.diff(positive,w,3)],modules='mpmath')
    e=mp.mpf(1)/500;k=mp.mpf(40);coef=mp.mpf(-9)/28000
    pieces=((mp.mpf(0),mp.pi/2,1),(mp.pi/2,3*mp.pi/2,-1),(3*mp.pi/2,2*mp.pi,1))
    controls=[]
    for harmonic in (1,3):
        test=lambda theta:mp.sin(harmonic*theta)
        test3=lambda theta:-harmonic**3*mp.cos(harmonic*theta)
        def lhs(theta,sign):return -sign*funcs(e*mp.cos(theta))[0]*test3(theta)
        def regular(theta,sign):
            ww=e*mp.cos(theta);wt=-e*mp.sin(theta);wtt=-ww;wttt=-wt
            vv=funcs(ww)
            return sign*(vv[3]*wt**3+3*vv[2]*wt*wtt+vv[1]*wttt)*test(theta)
        left=k*k*sum(mp.quad(lambda t:lhs(t,sign),[a,b]) for a,b,sign in pieces)
        smooth=k*k*sum(mp.quad(lambda t:regular(t,sign),[a,b]) for a,b,sign in pieces)
        jump=k*k*4*coef*e*e*(-test(mp.pi/2)+test(3*mp.pi/2))
        err=abs(left-smooth-jump)/(1+abs(left)+abs(smooth)+abs(jump))
        check('actual_weak_third_derivative_sin'+str(harmonic),err<mp.mpf('1e-30'),show(err))
        omission=abs(left-smooth)/(1+abs(left)+abs(smooth))
        check('reject_omitted_interface_sin'+str(harmonic),omission>mp.mpf('1e-18'),show(omission))
        controls.append(dict(harmonic=harmonic,error=show(err),interface=show(jump),omission=show(omission)))
    check('finite_band_smoothness_necessary_condition_fails',leading!=0,
          'An exact finite Fourier subspace has only smooth representatives; its C2-time L2 acceleration remains in that subspace')
    verify()
    return dict(result_id='R4C1-FINITE-BAND-DOMAIN-V1',source_sha256=pins,checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),
                formulas=dict(actual_Vy_cusp_positive_branch=str(positive),leading_coefficient=str(leading),
                              physical_branch='sign(w)*positive_branch(w); positive_branch is analytic and even',
                              node_jumps=jumps),weak_controls=controls,
                exact_finite_band_C2_time_L2_continuation_rejected=True,
                finite_band_approximation_rejected=False,all_prepared_weak_solutions_excluded=False,
                time_evolution=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
                working_digits=110,sympy=s.__version__,mpmath=mp.__version__)


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=parser.parse_args();r=calculate();data=ENC(r)
    if a.replay:
        if (a.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);f=a.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:r[k] for k in ('passed','total','exact_finite_band_C2_time_L2_continuation_rejected')}))
    raise SystemExit(0 if r['passed']==r['total'] else 2)


if __name__=='__main__':main()
