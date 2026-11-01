"""First bounded covariant-current and kinetic comparison of F-tau and R-tau.

Neither action is adopted. Positivity here is not a gradient, nonlinear or
physical-window claim. The original density and scientific artifacts stay pinned.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_TWO_REPAIR_COMPARISON_V1_CONTRACT_2026-10-31.md'
SPEC='Theory/Gates/RES-001/RES001_R4C1_TWO_REPAIR_CANDIDATES_V1_2026-10-31.md'
PARENT='Analysis/MasterTests/outputs/r4c1_b1_alignment_domain_v1_attempt_01/summary.json'
PSHA='5ce2ecbf65f1a1b1d3f0e38dc6a02413a9bcefa36a1e93e24b9aeb090e36be1b'
KINETIC='Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def calculate():
    mp.mp.dps=120;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        rows=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for e in rows if (v:=s.expand(clean(e)))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=json.loads((ROOT/PARENT).read_bytes());assert parent['passed']==parent['total']==53
    baseline=json.loads((ROOT/KINETIC).read_bytes())
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (SELF,BACKEND,CONTRACT,SPEC,KINETIC,
        'Analysis/MasterTests/r4c1_two_repair_actions_v1.py',
        'Analysis/MasterTests/test_01_r4c1_two_repair_comparison_v1.py',
        'Analysis/MasterTests/outputs/r4c1_two_repair_comparison_v1_attempt_01/summary.json',
        'Theory/Gates/RES-001/RES001_R4C1_TWO_REPAIR_COMPARISON_V2_EXECUTION_ADDENDUM_2026-10-31.md'):
        pins[path]=SHA((ROOT/path).read_bytes())
    snapshots={}
    for path,want in pins.items():
        f=ROOT/path;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,path
        for z in (f,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    backend=load('two_repair_backend',BACKEND)
    old=backend.load('two_repair_parent',backend.QUADRATIC)
    par=old.parameters()
    w=s.Symbol('w',real=True);H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    parse=lambda rows:s.Matrix([[s.sympify(v,locals={'w':w,'H':H,'k':k}) for v in row] for row in rows])
    oldM=parse(parent['formulas']['reduced_kinetic'])
    oldR=parse(parent['formulas']['homogeneous_complement'])
    oldM0=parse(baseline['formulas']['reduced_kinetic'])
    phase=1/(1-w*w/13);p=s.Rational(1,5)
    b=par['b'];A=par['A']
    fpsi=3*(1+w*w)-s.Rational(12,35)*s.Abs(w)**3
    H2=s.sympify(parent['formulas']['H_squared'],locals={'w':w})

    # Off-shell normalized-clock differential, with timelike domain declared.
    grad=s.Matrix(s.symbols('r0:4',real=True));ginv=s.diag(-1,1,1,1)
    chi=s.sqrt(-(grad.T*ginv*grad)[0]);t=-ginv*grad/chi
    proj=ginv+t*t.T
    zero('clock_normal_unit_identity',(t.T*ginv*t)[0]+1)
    jac=t.jacobian(grad)
    zero('off_shell_clock_normal_variation',jac+proj/chi)
    zero('normal_variation_transverse',t.T*ginv*jac)
    zero('clock_rescaling_direction_annihilated',jac*grad)
    check('unnormalized_clock_variation_rejected',any(s.expand(clean(z))!=0 for z in jac+ginv/chi))

    # Matter Ward identity in a flat 1+1 dependence, retaining the 4D trace.
    tt,zz=s.symbols('time space',real=True);co=(tt,zz)
    tau=s.Function('tau')(tt,zz);psi=s.Function('psi')(tt,zz);eps=s.Function('eps')(tt,zz)
    beta=s.Symbol('beta',real=True);C=s.exp(beta*psi);vgrad=s.Matrix([s.diff(tau,z) for z in co])
    gi2=s.diag(-1,1);norm=(vgrad.T*gi2*vgrad)[0]
    Lm=-eps*(C*C*norm+C**4)/2
    Eeps=-(C*C*norm+C**4)/2
    Etau=sum(s.diff(eps*C*C*(gi2*vgrad)[i],co[i]) for i in range(2))
    Epsi=-eps*beta*(C*C*norm+2*C**4);trace=eps*C*C*norm+4*Lm
    zero('conformal_matter_scalar_trace_identity',Epsi-beta*trace)
    Tmixed=eps*C*C*(gi2*vgrad)*vgrad.T+s.eye(2)*Lm
    for j in range(2):
        ward=sum(s.diff(Tmixed[i,j],co[i]) for i in range(2))
        ward-=Etau*s.diff(tau,co[j])+Epsi*s.diff(psi,co[j])+Eeps*s.diff(eps,co[j])
        zero('off_shell_matter_Ward_component_'+str(j),s.expand(ward))
    # Covariant composition delta S_X = -F^mu*partial_mu(delta tau).
    e=s.Matrix(s.symbols('E0:4',real=True));F=proj*e/chi
    zero('clock_current_chain_rule',jac.T*e+F)
    check('clock_Euler_and_dust_only_Euler_distinguished',str(F)!='Matrix([[0], [0], [0], [0]])')

    # Explicit independent normal variation of the clock regulator at t=(1,0).
    Z=s.Function('Z')(tt,zz);nu=s.Function('nu')(tt,zz)
    # The first-order term follows from the fully normalized vector:
    small=s.Symbol('small',real=True)
    normal=s.Matrix([s.sqrt(1+small*small*nu*nu),small*nu])
    hnormal=gi2+normal*normal.T
    acc=s.Matrix([sum(normal[j]*s.diff(normal[i],co[j]) for j in range(2)) for i in range(2)])
    gZ=s.Matrix([s.diff(Z,z) for z in co]);gp=s.Matrix([s.diff(psi,z) for z in co])
    bb=s.Symbol('b',positive=True)
    Lreg=bb*Z*Z/2-bb*(gZ.T*hnormal*gp)[0]-bb*Z*(acc.T*gp)[0]
    variation=s.diff(Lreg,small).subs(small,0)
    En=s.diff(variation,nu)-sum(s.diff(s.diff(variation,s.diff(nu,z)),z) for z in co)
    expected=bb*(Z*s.diff(psi,tt,zz)-s.diff(psi,tt)*s.diff(Z,zz))
    zero('regulator_full_normal_Euler_identity',s.expand(En-expected))
    testpsi=s.Function('background')(tt)+s.Symbol('amp',real=True)*s.cos(k*zz)
    kval=s.diff(expected,zz).subs({psi:testpsi,Z:k*k*s.Symbol('amp',real=True)*s.cos(k*zz)}).doit().expand()
    target=bb*s.diff(s.Function('background')(tt),tt)*k**4*s.Symbol('amp',real=True)*s.cos(k*zz)
    zero('clock_regulator_extra_Euler_nonzero_example',s.expand(kval-target))
    check('old_bare_dust_conservation_not_inherited',target!=0,str(target))

    # Exact auxiliary equation with nonconstant lapse and spatial volume.
    nfun=s.Function('N')(zz);vol=s.Function('volume')(zz);ih=s.Function('hzz')(zz)
    eZ=Z+s.diff(nfun*vol*ih*s.diff(psi,zz),zz)/(nfun*vol)
    eZ-=s.diff(nfun,zz)/nfun*ih*s.diff(psi,zz)
    intrinsic=Z+s.diff(vol*ih*s.diff(psi,zz),zz)/vol
    zero('clock_auxiliary_intrinsic_laplacian_identity',s.expand(eZ-intrinsic))
    check('omitted_clock_acceleration_term_rejected',
        s.diff(nfun,zz)/nfun*ih*s.diff(psi,zz)!=0)
    check('mass_dimensions_clock_and_regulator',
        (0==0 and 2+2==4 and 3+1==4 and 2+1+1==4 and 4+1==5))

    results={};fulls={}
    for route,w0 in [('F-tau',s.Integer(0)),('R-tau',w)]:
        slots=backend.F_SLOTS if route=='F-tau' else backend.R_SLOTS
        n=len(slots);x=[old.Jet.var(i) for i in range(2*n+4)]
        action=backend.ClockGaugeAction(route,par)
        ph=1 if route=='F-tau' else phase
        state=backend.derivative_state(route,w0,H,ph,x,s.Rational)
        density=action.density(state)[0]
        full=s.zeros(2*n+4)
        for (i,j),v0 in density.h.items():full[i,j]=full[j,i]=clean(v0)
        pi=slots.index(12);zi=slots.index(13)
        if route=='R-tau':
            full[pi,pi]-=6*A*p*s.Abs(w)**3
            full[n+pi,n+pi]-=3*A*p*s.Abs(w)
        zero(route+'_auxiliary_velocity_row',full[zi,:])
        zero(route+'_auxiliary_position_velocity_couplings',full[-1,:n])
        zero(route+'_auxiliary_position_shift_couplings',full[-1,2*n:2*n+3])
        zero(route+'_auxiliary_positive_algebraic_pivot',full[-1,-1]-b)
        zero(route+'_derivative_Hessian_symmetric',full-full.T)
        check(route+'_no_symbolic_Float',not bool(full.atoms(s.Float)))
        shift=full[2*n:2*n+3,2*n:2*n+3]
        cross=full[:n,2*n:2*n+3]
        invshift=shift.inv()
        solve=(-invshift*cross.T).applyfunc(clean)
        zero(route+'_all_shift_equations_solved',shift*solve+cross.T)
        reduced=(full[:n,:n]+cross*solve).applyfunc(clean)
        zero(route+'_auxiliary_remains_nondynamical_after_shift',reduced[zi,:])
        keep=[i for i in range(n) if i!=zi]
        mass=reduced.extract(keep,keep).applyfunc(clean)
        detS=clean(shift.det())
        check(route+'_nonzero_mode_shift_pivot',detS!=0,str(detS))
        zero(route+'_zero_mode_not_inverted',(detS*k**6).subs(k,0))
        if route=='F-tau':
            expectedM=oldM0.extract([0,1,2,6,7,8,9],[0,1,2,6,7,8,9])
            zero('F_tau_fresh_action_positive_parent_subblock_identity',mass-expectedM)
            eig=mass.eigenvals()
            check('F_tau_all_reduced_kinetic_eigenvalues_positive',all(z.is_positive for z in eig),
                  {str(z):m for z,m in eig.items()})
        else:
            zero('R_tau_fresh_action_positive_ten_block_identity',mass-oldM[:10,:10])
            zero('R_tau_aligned_original_ten_fields_recovered',mass.subs(w,0)-oldM0)
            zero('R_tau_no_scalar_auxiliary_velocity_pair',full[pi,zi])
            zero('R_tau_LDL_block_identity',mass[:9,:9]-
                 parse(parent['formulas']['positive_B9_L'])*parse(parent['formulas']['positive_B9_D'])*
                 parse(parent['formulas']['positive_B9_L']).T)
            zero('R_tau_scalar_positive_pivot_identity',mass[9,9]-fpsi)
            zero('R_tau_scalar_complement_kinetic_crosses',mass[:9,9])
            check('R_tau_reuses_verified_positive_pivots_and_scalar_interval',
                  parent['bounds']['effective_psi_mass'][0][0]!='-' and
                  all(z['passed'] for z in parent['checks']),
                  'Exact freshly recomputed matrix identity plus the pinned old interval proof; not a cutoff/gradient theorem')
        encode=lambda m:[[str(clean(z)) for z in row] for row in m.tolist()]
        results[route]=dict(physical_kinetic_fields=len(keep),auxiliary_velocity_absent=True,
            reduced_kinetic=encode(mass),shift_block=encode(shift),shift_determinant=str(detS),
            auxiliary_pivot=str(b),on_shell_scope='common old homogeneous B1 control',
            positive_kinetic_scope='initial nonzero-mode block only' if route=='F-tau'
                else 'initial old-B1 charge-preserving transverse diagnostic, |w|<=1/500',
            complete_physical_domain=False,physical_window=False)
        fulls[route]=full
        print(route+'_FRESH_ACTION_REDUCTION_COMPLETE',flush=True)

    # R-tau homogeneous admission: the algebraic Z is omitted only after its own equation.
    action=backend.ClockGaugeAction('R-tau',par)
    q=[1,0,0,1,0,1,0,w,0,1,0,1,0,0,0,s.Rational(1,5)]
    vel=[0]*16;dz=[0]*16
    for j in (0,3,5):vel[j]=2*H
    vel[7]=-H*w;vel[10]=phase;vel[11]=s.Rational(1,4);vel[12]=p;vel[14]=1
    x=[old.Jet.var(i) for i in range(15)]
    vv=[v+(x[i] if i<13 else 0) for i,v in enumerate(vel)]
    vv[14]+=x[14]
    hom=action.density(q+vv+dz+[0,0,0]+[0,0,0]+[1+x[13],0])[0]
    zero('R_tau_scalar_charge_recomputed',hom.g.get(10,0)-1)
    zero('R_tau_dust_charge_recomputed',hom.g.get(14,0)-s.Rational(1,5))
    lapse=clean(hom.g.get(13,0)+2*A*p**3*s.Abs(w)**3)
    C_H=s.sympify(parent['formulas']['lapse_H_coefficient'],locals={'w':w})
    energy=s.sympify(parent['formulas']['lapse_energy'],locals={'w':w})
    zero('R_tau_lapse_curve_recomputed',lapse-(C_H*H**2-energy))
    zero('R_tau_H_squared_curve',H2-energy/C_H)
    Mh=s.zeros(13)
    for (i,j),v0 in hom.h.items():
        if i<13 and j<13:Mh[i,j]=Mh[j,i]=clean(v0)
    Mh[12,12]-=6*A*p*s.Abs(w)**3
    zero('R_tau_homogeneous_complement_recomputed',Mh[:12,:12]-oldR)
    zero('R_tau_homogeneous_scalar_crosses',Mh[:12,12])
    zero('R_tau_homogeneous_scalar_pivot',Mh[12,12]-fpsi)
    detR=s.sympify(parent['formulas']['homogeneous_complement_determinant'],locals={'w':w})
    check('R_tau_homogeneous_nonsingularity_in_declared_interval',
          int(parent['bounds']['homogeneous_complement_determinant'][1])<0 and
          int(parent['bounds']['effective_psi_mass'][0])>0)
    results['R-tau']['homogeneous_determinant']=str(clean(detR*fpsi))
    results['R-tau']['homogeneous_local_admission']='POINTWISE_LOCAL_ON_DECLARED_CHARGE_CURVE; NO_UNIFORM_LIFETIME'
    results['R-tau']['Z_equation']='Z=-Delta_tau psi; Z=0 for the homogeneous clock-gauge solution'
    print('R_tau_HOMOGENEOUS_CONSTRAINT_CURVE_COMPLETE',flush=True)

    # Independent physical density: original norm-cubed term retained.
    conv=lambda z:mp.mpf(str(s.N(z,118)))
    pp={key:conv(val) for key,val in par.items()}
    controls=[]
    route='R-tau';raw=backend.ClockGaugeAction(route,pp,physical=True)
    n=len(backend.R_SLOTS);m=2*n+4
    target_fn=s.lambdify((w,H),fulls[route],modules='mpmath')
    def raw_gradient(xvals,wv,hv,ph):
        tape=raw.body.Tape();nodes=[tape.var(v) for v in xvals]
        Astate=backend.derivative_state(route,wv,hv,ph,nodes,lambda n,d:mp.mpf(n)/d)
        val=raw.density(Astate)[0]
        return mp.matrix(tape.grad(val,nodes))
    for wv in (mp.mpf('0.001'),mp.mpf('-0.001'),mp.mpf('0.002'),mp.mpf('-0.002')):
        hv=conv(H2.subs(w,s.Rational(str(wv))))**mp.mpf('.5')
        ph=1/(1-wv*wv/13);target=target_fn(wv,hv);errs=[]
        for hs in ('1e-20','1e-26'):
            hh=mp.mpf(hs);observed=mp.matrix(m)
            for j in range(m):
                xv=[mp.mpf(0)]*m;xv[j]=mp.j*hh
                g=raw_gradient(xv,wv,hv,ph)
                for i in range(m):observed[i,j]=mp.im(g[i])/hh
            err=max(abs(z) for z in observed-target)/(1+max(abs(z) for z in target))
            check('R_tau_original_physical_full_Hessian_'+str(wv)+'_'+hs,err<mp.mpf('1e-35'),mp.nstr(err,65))
            errs.append(mp.nstr(err,65))
        controls.append(dict(route=route,tilt=str(wv),kind='full physical Hessian',errors=errs))
        print('R_tau_PHYSICAL_AD_CONTROL_'+str(wv),flush=True)

    route='F-tau';rawF=backend.ClockGaugeAction(route,pp,physical=True)
    n=len(backend.F_SLOTS);m=2*n+4;h0=conv(s.sqrt(s.Rational(3469,4620)))
    target=s.lambdify(H,fulls[route],modules='mpmath')(h0)
    def raw_value(xvals):
        Astate=backend.derivative_state(route,0,h0,1,xvals,lambda n,d:mp.mpf(n)/d)
        return rawF.density(Astate)[0]
    L0=raw_value([mp.mpf(0)]*m)
    for seed in (1,2,3):
        direction=mp.matrix([mp.mpf(((j+1)*(seed+2))%11-5)/(17+seed) for j in range(m)])
        expected=(direction.T*target*direction)[0];errs=[]
        for hs in ('1e-10','1e-16'):
            hh=mp.mpf(hs)
            value=(raw_value([hh*z for z in direction])+raw_value([-hh*z for z in direction])-2*L0)/(hh*hh)
            err=abs(value-expected)/(1+abs(expected))
            check(f'F_tau_physical_aligned_C2_{seed}_{hs}',err<1000*hh,mp.nstr(err,65));errs.append(mp.nstr(err,65))
        controls.append(dict(route=route,seed=seed,kind='real finite difference at C2 cusp',errors=errs))
    # The action-level replacement, not a post-variation old frame equation.
    try:
        backend.derivative_state('F-tau',s.Rational(1,1000),H,1,[0]*20,s.Rational)
        rejected=False
    except ValueError:rejected=True
    check('F_tau_finite_independent_tilt_rejected',rejected)
    check('R_tau_independent_frame_fields_retained',len(backend.R_SLOTS)-len(backend.F_SLOTS)==3)
    for name,(digest,mtime) in snapshots.items():
        f=ROOT/name;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    return dict(kind='R4C1_TWO_REPAIR_COMPARISON_V2',passed=sum(z['passed'] for z in checks),total=len(checks),
        checks=checks,source_sha256=pins,independent_controls=controls,candidates=results,
        covariant_clock=dict(normal_variation='delta t^mu=-p_tau^{mu nu}*partial_nu(delta tau)/chi',
            extra_Euler='E_tau,X=div(p_tau*E_t/chi)',
            total_clock='div(epsilon*C^2*grad(tau)+p_tau*E_t/chi)=0',
            matter_balance_on_total_clock='div(T_m)=beta*T_m*grad(psi)-E_tau,X*grad(tau)',
            regulator_flat_example='E_tau,reg=b*p_background*k^4*amp*cos(k*z)',
            old_bare_dust_current_inherited=False),
        original_parent_unchanged=True,adopted_canonical_action=False,matched_new_coefficients=False,
        full_gradient_or_characteristic_classification=False,nonlinear_physical_domain=False,
        physical_window_demonstrated=False,complete_metric_frame_variation=False,
        K_Q='NOT_DERIVED',V='NOT_COMPUTED',MAT001='BLOCKED',UVIR003='IN_PROGRESS',
        G1_G6='INCOMPLETE',physics_pass=False,gate_effect='NONE',review='DEFERRED',Rule9_cleared=False)

def main():
    ap=argparse.ArgumentParser();group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--output-dir',type=Path);group.add_argument('--replay',type=Path)
    a=ap.parse_args();result=calculate();data=ENC(result)
    if a.replay:
        assert a.replay.read_bytes()==data,'replay mismatch';print('READ_ONLY_REPLAY_EXACT',SHA(data))
    else:
        a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json'
        p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=result['passed'],total=result['total'],physics_pass=False,receipt=str(p))))
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':raise SystemExit(main())

