"""Original nodal frame coefficients and a necessary linear defect budget.

No nonlinear layer, discontinuous metric or weak-product rule is adopted.
"""
import argparse,ast,hashlib,importlib.util,inspect,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_nodal_transfer_v1_attempt_01/summary.json'
PSHA='b77447a1d97dfb8711594db66f3ec8ada3ac19d741fc3b5e9f886312189b4b71'
CAUCHY='Analysis/MasterTests/outputs/r4c1_inner_cauchy_v2_attempt_01/summary.json'
JAC='Analysis/MasterTests/outputs/r4c1_full_initial_jacobi_v1_attempt_01/summary.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_COUPLED_DEFECT_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_NODAL_TRANSFER_V1_REPORT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda v:mp.nstr(v,65)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def endpoint(q):
    sign,man,exp,_=q;return F((-1 if sign else 1)*man)*F(2)**exp


def iv(v):v=F(v);return mp.iv.mpf(v.numerator)/v.denominator
def pack(v):return dict(lower=str(endpoint(v._mpi_[0])),upper=str(endpoint(v._mpi_[1])))


def calculate():
    mp.mp.dps=120;mp.iv.dps=90;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        v=s.factor(s.cancel(z));check(name,v==0,str(v))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,REPORT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            f=ROOT/path;assert SHA(f.read_bytes())==want and Path(str(f)+'.sha256').read_text().split()[0].lower()==want,path
    verify();ch=load('defect_registered',CHARGE);ch.setup();mp.mp.dps=120
    body=ch.en.body;backend=load('defect_original_weak',BACKEND)
    eta=s.Symbol('eta');par={key:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
        for key,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    bg=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in bg.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='PARAMS' for z in t.targets))
    shared={v.arg:s.Rational(s.sympify(ast.unparse(v.value))) for v in call.keywords}
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    # The norm-cubed term is C2 with zero Hessian at zero projected gradient.
    radius=s.symbols('radius',positive=True)
    zero('physical_cubic_radial_Hessian_limit',s.limit(s.diff(radius**3,radius,2),radius,0))
    zero('physical_cubic_tangential_Hessian_limit',s.limit(s.diff(radius**3,radius)/radius,radius,0))
    tree=ast.parse(inspect.getsource(body.body));fun=tree.body[0]
    force=next(t for t in fun.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='force' for z in t.targets))
    assert ast.dump(force.value)==ast.dump(ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body)
    force.value=force.value.left;fun.name='defect_nodal_C2_body';ast.fix_missing_locations(tree)
    exec(compile(tree,'<original-action-exact-nodal-C2-partition>','exec'),body.__dict__)
    U,Z,Zz,Vt,Vz,Nz,hx,hy,hz,Sz=s.symbols('Vz Z Zz Vt Vz_z Nz hx_t hy_t hz_t Sz_z',real=True)
    H,sigma,rho=s.symbols('H sigma rho',real=True);p=s.Rational(1,20)
    q=[s.Integer(0)]*16;v=q.copy();d=q.copy()
    for i in (0,3,5):q[i]=s.Integer(1)
    q[8]=U;q[9]=q[11]=s.Rational(1,2);q[13]=Z;q[15]=rho
    v[0]=2*H+hx;v[3]=2*H+hy;v[5]=2*H+hz;v[8]=Vt
    v[10]=s.Rational(1,2)/(1-par['zeta']/4*s.Rational(1,250000)/2)
    v[11]=s.Rational(1,8);v[12]=p;v[14]=1;d[7]=sigma;d[8]=Vz;d[13]=Zz
    jets=q+v+d+[s.Integer(0)]*3+[0,0,Sz]+[s.Integer(1),Nz]
    origin=dict.fromkeys((U,Z,Zz,Vt,Vz,Nz,hx,hy,hz,Sz),s.Integer(0))
    oldbody,oldsqrt=body.body,body.sqrt
    try:
        body.body=body.defect_nodal_C2_body;body.sqrt=s.sqrt
        density=backend.WeakAction(body,par).density(jets)[0]
        pairs=[('time_mass',Vt,Vt,s.Rational(1,24),24,24),
            ('spatial_Hessian',Vz,Vz,-s.Rational(1,60),40,40),
            ('lapse_gradient_cross',Vt,Nz,s.Rational(1,24),24,55),
            ('metric_trace_hxx',Vz,hx,-s.Rational(1,120),40,16),
            ('metric_trace_hyy',Vz,hy,-s.Rational(1,120),40,19),
            ('metric_trace_hzz',Vz,hz,-s.Rational(1,120),40,21),
            ('shift_gradient_cross',Vz,Sz,s.Rational(1,60),40,53),
            ('direct_auxiliary_gradient',U,Zz,-par['b']*p,8,45),
            ('auxiliary_gradient_drift_space_zero',Vz,Zz,s.Integer(0),40,45),
            ('auxiliary_gradient_drift_time_zero',Vt,Zz,s.Integer(0),24,45),
            ('frame_spatial_current_auxiliary_zero',Vz,Z,s.Integer(0),40,13)]
        exact_coeff={}
        for name,left,right,want,_,_ in pairs:
            got=s.diff(density,left,right).subs(origin);zero('original_nodal_'+name,got-want);exact_coeff[name]=str(s.factor(got))
    finally:body.body=oldbody;body.sqrt=oldsqrt
    # Full physical-A original action numerical controls at each node slope.
    controls=[]
    numeric_par={key:mp.mpf(str(s.N(value,115))) for key,value in par.items()}
    for sign in (-1,1):
        # Replace symbols explicitly; H/rho/sigma values are irrelevant to
        # these coefficients, as the exact expressions above establish.
        sub={**origin,H:mp.mpf('0.4823203671'),sigma:mp.mpf(sign)*2/25,rho:mp.mpf(1)/5}
        A=[mp.mpf(str(s.N(s.sympify(z).subs(sub),115))) for z in jets]
        weak=backend.WeakAction(body,numeric_par)
        for step in ('1e-20','1e-26'):
            columns={}
            for col in sorted({row[5] for row in pairs}):
                unit=mp.matrix(56,1);unit[col]=1;columns[col]=weak.hv(A,unit,mp.mpf(step))
            error=max(abs(columns[col][row]-mp.mpf(str(s.N(want,115))))/(1+abs(columns[col][row])) for _,_,_,want,row,col in pairs)
            check('original_physical_A_node_control_'+str(sign)+'_'+step,error<mp.mpf('1e-18'),show(error))
            controls.append(dict(slope_sign=sign,complex_step=step,normalized_error=show(error),background_admission=False))
    # Independent finite-w unreduced operator control of the full coefficient.
    for filename in READ(JAC)['file_sha256']:
        row=READ((Path(JAC).parent/filename).as_posix());w=mp.cos(mp.mpf(row['theta']))/500
        got=mp.mpf(row['full_twenty_coefficients']['space'][8][13])
        want=-numeric_par['b']*mp.mpf(1)/20*mp.sqrt(1+w*w)
        error=abs(got-want)/(1+abs(got)+abs(want))
        check('finite_w_full_frame_aux_gradient_'+row['label'],error<mp.mpf('1e-18'),show(error))
    # Singular budget is a conditional LINEARIZED limit, not a choice to
    # admit discontinuous frame fields or undefined nonlinear products.
    tt,c=s.symbols('T c',positive=True);M,J,Dcur=s.symbols('M J Dcur',real=True)
    aa=s.Rational(4,625);bb=s.Rational(5,44);dd=s.Rational(1,60);mm=s.Rational(1,24)
    coefficient=s.factor(bb*p*p/dd);zero('feedback_factor',coefficient-s.Rational(3,176))
    formal=[]
    cbox=READ(CAUCHY)['actual_connection_coefficients']['power_3']
    ci=mp.iv.mpf([iv(F(cbox['lower'])).a,iv(F(cbox['upper'])).b])
    for sign in (-1,1):
        sig=sign*s.Rational(2,25)
        equations=[M+2*aa*c*tt**3+p*sig*J,dd*sig**2*J-bb*p*sig*M]
        solution=s.solve(equations,(M,J),dict=True)[0]
        zero('partial_auxiliary_balance_'+str(sign),equations[0].subs(solution))
        zero('partial_frame_delta_prime_balance_'+str(sign),equations[1].subs(solution))
        zero('surface_auxiliary_coefficient_'+str(sign),solution[M]+2*aa*c*tt**3/(1+coefficient))
        zero('required_scalar_dipole_'+str(sign),(-bb*aa*M+Dcur).subs({Dcur:bb*aa*M}))
        scalar_second=s.factor(-bb*aa*solution[M])
        check('finite_measure_scalar_currents_cannot_close_'+str(sign),scalar_second!=0)
        check('sourcefree_leading_frame_Cauchy_fails_'+str(sign),s.diff(solution[J],tt,2)!=0)
        # No auxiliary measure and no derivative-valued scalar current:
        # the three surface equations have no solution when c,T are positive.
        full=s.linsolve(equations+[bb*aa*M],(M,J))
        check('three_equation_measure_closure_rejected_'+str(sign),full is s.EmptySet or full==s.EmptySet)
        mcoef=s.factor(solution[M]/(c*tt**3));jcoef=s.factor(solution[J]/(c*tt**3))
        to_fraction=lambda z:F(int(z.p),int(z.q))
        mi=iv(to_fraction(mcoef))*ci;ji=iv(to_fraction(jcoef))*ci
        formal.append(dict(slope_sign=sign,surface_Z_T3=pack(mi),frame_jump_T3=pack(ji),
            required_scalar_current_dipole_T3=pack(iv(F(5,44))*iv(F(4,625))*mi),
            unbalanced_leading_frame_bulk_T1=pack(-iv(F(1,4))*ji)))
    # Delta'' pairs with phi''(0); any finite measure current contributes
    # at most a delta-prime under one divergence. Dust has no frame coupling.
    phi0,phi1,phi2,rhos=s.symbols('phi0 phi1 phi2 rho_surface',real=True)
    residual=-bb*aa*M*phi2+Dcur*phi2-rhos*phi0
    zero('highest_scalar_distribution_order',s.diff(residual,phi2)-(-bb*aa*M+Dcur))
    zero('dust_measure_has_no_second_derivative_test_component',s.diff(-rhos*phi0,phi2))
    verify()
    return dict(result_id='R4C1-COUPLED-DEFECT-V1',source_sha256=pins,checks=checks,
        original_nodal_coefficients=exact_coeff,independent_controls=controls,
        nodal_frame_row='-(1/24)*(Vz_tt+N_zt)+(1/60)*(Vz_zz+trace(h)_tz/2-Sz_zz)-(1/176)*Z_z plus lower terms',
        surface_budget=dict(auxiliary='M+2*a*c*T^3+p*sigma*J=0',frame='d*sigma^2*J-b*p*sigma*M=0',
            scalar='-b*a*M+Dcur=0;Dcur requires a delta-prime scalar current',
            assumptions='Continuous regular metric/lapse/shift; linearized registered nodal coefficients; no higher-order current defect unless explicitly retained.'),
        partial_surface_balances=formal,partial_auxiliary_frame_balance_not_a_solution=True,
        finite_measure_current_closure_rejected=all(c['passed'] for c in checks),leading_frame_Cauchy_conflict=all(c['passed'] for c in checks),
        nonlinear_current_dipole_derived=False,uniform_rescaled_current_bounds_proved=False,
        actual_on_shell_concentration_constructed=False,discontinuous_frame_or_metric_adopted=False,
        full_original_weak_continuations_excluded=False,time_evolution=False,
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
    print(json.dumps({k:result[k] for k in ('passed','total','finite_measure_current_closure_rejected','actual_on_shell_concentration_constructed','full_original_weak_continuations_excluded','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
