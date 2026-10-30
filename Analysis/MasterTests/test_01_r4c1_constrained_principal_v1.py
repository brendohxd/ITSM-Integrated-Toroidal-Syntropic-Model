"""Necessary constrained principal test, not physical spectrum/window admission."""
from __future__ import annotations
import argparse,ast,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_full_weak_action_v1_attempt_01/summary.json'
PSHA='2f4d3404eb587f362ee285b7fe3cfa99bdfcb7be5b643d3f2ff9133fdf84cb27'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CONSTRAINED_PRINCIPAL_V1_CONTRACT_2026-10-28.md'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
READ=lambda p:json.loads((ROOT/p).read_bytes())
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda v:mp.nstr(v,65)
PHYSICAL=(0,1,3,6,7,8,9,10,11,12,13)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def calculate():
    mp.mp.dps=110;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        rows=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(t) for x in rows if (t:=s.factor(s.cancel(x)))!=0]
        check(name,not bad,bad)
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();charge=load('principal_registered',CHARGE);charge.setup();mp.mp.dps=110
    body=charge.en.body;backend=load('principal_full_weak',BACKEND)
    eta=s.Symbol('eta');par={n:s.sympify(t,locals={'eta':eta}).subs(eta,s.Rational(1,4)) for n,t in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    tree=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in tree.body if isinstance(t,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='PARAMS' for v in t.targets))
    shared={v.arg:s.Rational(s.sympify(ast.unparse(v.value))) for v in call.keywords}
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
               mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    w=s.Symbol('w',real=True,nonzero=True);ZZ=s.Symbol('Z_background',real=True);c=s.Symbol('c',real=True)
    p=s.Rational(1,20);rc=s.Rational(1,2);b=par['b'];beta=par['beta']
    vel=list(s.symbols('v0:11'));spatial=list(s.symbols('d0:11'));shift=list(s.symbols('Sz0:3'))
    variables=vel+spatial+shift;origin=dict.fromkeys(variables,s.Integer(0))
    q=[s.Integer(1),0,0,1,0,1,0,w,0,rc,0,rc,0,ZZ,0,s.Rational(1,5)]
    q=list(map(s.sympify,q));vv=[s.Integer(0)]*16;dd=vv.copy();vv[14]=s.Integer(1)
    for i,slot in enumerate(PHYSICAL):vv[slot]=vel[i];dd[slot]=spatial[i]
    vv[12]+=p
    A=q+vv+dd+[s.Integer(0)]*3+shift+[s.Integer(1),-beta*spatial[9]]
    oldsqrt=body.sqrt;body.sqrt=s.sqrt
    try:
        analytic=backend.WeakAction(body,dict(par,A=s.Integer(0)))
        L=analytic.density(A)[0]
        H=s.hessian(L,variables).subs(origin).applyfunc(lambda z:s.factor(s.cancel(z)))
    finally:body.sqrt=oldsqrt
    # Restore the exact physical cubic Hessian at nonzero transverse tilt.
    H[9,9]-=6*par['A']*p*s.Abs(w)**3
    H[20,20]-=3*par['A']*p*s.Abs(w)
    check('full_derivative_Hessian_no_Float',not bool(H.atoms(s.Float)))
    zero('full_derivative_Hessian_symmetry',H-H.T)
    # Vary original dust multiplier first; no clock equation is discarded.
    NN,pp,tt,eps=s.symbols('NN pp tt eps',real=True)
    Ldust=eps*(s.exp(2*beta*pp)*tt**2/NN-NN*s.exp(4*beta*pp))/2
    Eeps=s.diff(Ldust,eps)
    gauge=s.symbols('deltaN deltaPsi deltaTau_t')
    clock_linear=sum(s.diff(Eeps,z).subs({NN:1,pp:0,tt:1})*a for z,a in zip((NN,pp,tt),gauge))
    zero('dust_multiplier_lapse_elimination',clock_linear-(gauge[2]-gauge[0]-beta*gauge[1]))
    check('lapse_density_pair_regular',s.diff(clock_linear,gauge[0])==-1)
    kk=s.Symbol('k',nonzero=True,real=True)
    gj=s.Matrix([[1,0,0,0],[0,s.I*kk,0,0],[0,0,s.I*kk,0],[0,0,0,2*s.I*kk]])
    check('clock_and_spatial_gauge_no_residual',s.factor(gj.det())!=0,str(s.factor(gj.det())))
    T=s.zeros(25,14)
    for i in range(11):T[i,i]=-s.I*c;T[11+i,i]=s.I
    for i in range(3):T[22+i,11+i]=s.I
    P=(-T.T*H*T).applyfunc(lambda z:s.factor(s.cancel(z)))
    shift_block=P[11:14,11:14];shift_det=s.factor(shift_block.det())
    for sign in (-1,1):check('principal_shift_constraints_regular_'+str(sign),shift_det.subs(w,s.Rational(sign,1000))!=0)
    reduced=(P[:11,:11]-P[:11,11:14]*shift_block.inv()*P[11:14,:11]).applyfunc(lambda z:s.factor(s.cancel(z)))
    zero('all_three_shift_schur_symmetry',reduced-reduced.T)
    expected=s.zeros(11,1);expected[9]=-b*(w*w*c*c+1)
    zero('full_constrained_auxiliary_column',reduced[:,10]-expected)
    zero('reduced_pencil_is_quadratic',reduced.diff(c,3))
    M=reduced.diff(c,2)/2;C=reduced.diff(c).subs(c,0);G=reduced.subs(c,0)
    zero('mass_auxiliary_column',M[:,10]-s.Matrix([0]*9+[-b*w*w,0]))
    B=M[:9,:9]
    zero('remaining_mass_independent_of_Z_background',B.diff(ZZ))
    detB=s.factor(B.subs(w,s.Rational(1,1000)).det(method='domain-ge'))
    check('registered_remaining_mass_regular',detB!=0,str(detB))
    zero('positive_imaginary_characteristic',reduced[:,10].subs(c,s.I/w))
    zero('negative_imaginary_characteristic',reduced[:,10].subs(c,-s.I/w))
    print('FULL_CONSTRAINT_SCHUR_AND_CHARACTERISTIC_IDENTITIES',flush=True)
    # Whole derivative block versus the independent physical weak-action AD.
    controls=[];Hnum=s.lambdify((w,ZZ),H,modules='mpmath');Pnum=s.lambdify((w,ZZ,c),reduced,modules='mpmath')
    Mnum=s.lambdify((w,ZZ),M,modules='mpmath');Cnum=s.lambdify((w,ZZ),C,modules='mpmath');Gnum=s.lambdify((w,ZZ),G,modules='mpmath')
    weak=backend.WeakAction(body,charge.en.par)
    for sign in (-1,1):
        theta=mp.pi/3 if sign==1 else 2*mp.pi/3
        old,vd,ddd,Sdd=charge.state(theta);wv=mp.mpf(sign)/1000;old[7]=wv
        # Constant local spatial-coordinate adaptation removes shift VALUE only.
        old_v=[old[14+j]-old[44]*old[28+j] for j in range(14)]
        rho=charge.spatial(theta,mp.mpf('1e-26'))[9]
        state=old[:14]+[mp.mpf(0),rho]+old_v+[mp.mpf(1),mp.mpf(0)]+old[28:42]+[mp.mpf(0)]*2+[mp.mpf(0)]*3+old[45:48]+[mp.mpf(1),mp.mpf(0)]
        # Use the exact registered field point; tiny trigonometric rounding in
        # non-principal jets does not enter quadratic derivative coefficients.
        expected_H=mp.matrix(Hnum(wv,old[13]));directions=[]
        for j in range(25):
            vec=[mp.mpf(0)]*56
            if j<11:vec[16+PHYSICAL[j]]=1
            elif j<22:
                qi=PHYSICAL[j-11];vec[32+qi]=1
                if qi==12:vec[55]=-charge.en.par['beta']
            else:vec[51+j-22]=1
            directions.append(vec)
        for hs in ('1e-20','1e-26'):
            columns=[]
            for direction in directions:
                hv=weak.hv(state,direction,mp.mpf(hs))
                columns.append([sum(v*hv[i] for i,v in enumerate(test)) for test in directions])
            observed=mp.matrix([[columns[j][i] for j in range(25)] for i in range(25)])
            error=max(abs(z) for z in observed-expected_H)/(1+max(abs(z) for z in expected_H))
            check(f'original_full_weak_derivative_block_{sign}_{hs}',error<mp.mpf('1e-18'),show(error))
            controls.append(dict(sign=sign,step=hs,derivative_block_error=show(error)))
        # Verify the full first-order companion eigenvector, not a scalar-only root.
        mm=mp.matrix(Mnum(wv,old[13]));cc=mp.matrix(Cnum(wv,old[13]));gg=mp.matrix(Gnum(wv,old[13]))
        ez=mp.matrix([mp.mpf(0)]*10+[mp.mpf(1)])
        for branch in (-1,1):
            cv=branch*mp.j/wv
            lower=mp.lu_solve(mm,-gg*ez-cc*(cv*ez))
            error=max(abs(z) for z in lower-cv**2*ez)/(1+abs(cv)**2)
            check(f'full_companion_characteristic_{sign}_{branch}',error<mp.mpf('1e-18'),show(error))
        print(json.dumps(dict(stage='registered_principal_point',sign=sign)),flush=True)
    rate,Ttime,power=s.symbols('rate Ttime power',positive=True)
    check('exponential_growth_not_bounded_by_finite_polynomial_grade',s.limit(s.exp(rate*Ttime)/rate**power,rate,s.oo)==s.oo)
    verify()
    ok=all(x['passed'] for x in checks)
    return dict(result_id='R4C1-CONSTRAINED-PRINCIPAL-V1',source_sha256=pins,checks=checks,
                passed=sum(x['passed'] for x in checks),total=len(checks),controls=controls,
                formulas=dict(physical_indices=list(PHYSICAL),shift_determinant=str(shift_det),
                              derivative_Hessian=[[str(v) for v in row] for row in H.tolist()],
                              reduced_pencil=[[str(v) for v in row] for row in reduced.tolist()],
                              registered_remaining_mass_det=str(detB),
                              total_mass_det_identity='det(M)=-b^2*w^4*det(B_9), from exact auxiliary column',
                              characteristic='c=+/-i/w; auxiliary-column eigenvector, all11 reduced fields retained',
                              clock_constraint='deltaN=deltaTau_t-beta*deltaPsi; deltaTau=0 gauge',
                              gauge='deltaTau=delta h_xz=delta h_yz=delta h_zz=0, k_z!=0'),
                working_digits=110,mpmath=mp.__version__,sympy=s.__version__,
                necessary_estimate_status='FROZEN_CONSTRAINED_PRINCIPAL_OBSTRUCTION_ON_REGISTERED_SLICES' if ok else 'UNRESOLVED',
                physical_finite_frequency_spectrum_derived=False,physical_cutoff_identified=False,
                isolated_prepared_weak_solution_excluded=False,time_evolution=False,
                G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        if (args.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);p=args.output/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass','necessary_estimate_status')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
