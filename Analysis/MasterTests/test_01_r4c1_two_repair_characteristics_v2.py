"""Full coupled quadratic/current and initial characteristic comparison.

Fresh candidate actions; exact asymptotics are not a physical EFT cutoff.
Zero-mode reductions retain all homogeneous metric amplitudes.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
HELPER='Analysis/MasterTests/r4c1_two_repair_quadratic_v2.py'
PARENT='Analysis/MasterTests/outputs/r4c1_two_repair_comparison_v2_attempt_01/summary.json'
PSHA='964c24a88923a3326902eb8f5b37fa23a0f3ab6ee8964c60406e52211ea52f91'
OLD_DRIFT='Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V2_CONTRACT_2026-10-31.md'
EXECUTION='Theory/Gates/RES-001/RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V2_EXECUTION_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
    mp.mp.dps=120;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for e in entries if (v:=s.expand(clean(e)))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=json.loads((ROOT/PARENT).read_bytes());assert parent['passed']==parent['total']==70
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (SELF,HELPER,CONTRACT,EXECUTION,OLD_DRIFT):pins[path]=SHA((ROOT/path).read_bytes())
    snapshots={}
    for path,want in pins.items():
        f=ROOT/path;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,path
        for z in (f,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    spec=importlib.util.spec_from_file_location('repair_quadratic_helper',ROOT/HELPER)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    global clean;clean=helper.clean
    env=helper.setup();variables=env['variables'];initial=env['initial'];k=env['k'];par=env['par']
    a,H,u,v,r,du,dv,dr,p,psi,rho=variables
    dt=lambda z:sum(s.diff(z,w)*f for w,f in zip(variables,env['flow']))
    loc={str(z):z for z in variables+(k,)};loc['w']=s.Symbol('w',real=True)
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=loc) for z in row] for row in rows])
    old=json.loads((ROOT/OLD_DRIFT).read_bytes())['formulas']
    OM,OB,OQ,OMd,OBd=(parse(old[n]) for n in ('M','B','Q','M_dot','B_dot'))
    Of=OMd+OB-OB.conjugate().T;Or=OBd-OQ
    zero('common_background_constraint_preserved',dt(env['friedmann']))
    wave={};means={};controls=[]
    encode=lambda m:[[str(clean(z)) for z in row] for row in m.tolist()]

    for route in ('F-tau','R-tau'):
      for mean in (False,True):
        tag=route+('_mean' if mean else '_wave')
        d=helper.derive(route,env,mean);n,m=d['n'],d['m'];zi=d['slots'].index(13)
        check(tag+'_exact_no_Float',not any(mat.atoms(s.Float) for mat in (d['local'],d['unfixed'],d['M'],d['B'],d['Q'])))
        zero(tag+'_local_Hessian_symmetric',d['local']-d['local'].T)
        zero(tag+'_full_Hermitian',d['full']-d['full'].conjugate().T)
        zero(tag+'_auxiliary_velocity_row',d['full'][n+zi,:])
        zero(tag+'_constraint_solution',d['D']*d['solve']+d['cross'].conjugate().T)
        zero(tag+'_stationary_action_pullback',d['pull'].conjugate().T*d['full']*d['pull']-d['red'])
        zero(tag+'_lapse_coefficient',d['lapse_density_coefficient']+a**3)
        zero(tag+'_full_lapse_reconstruction',d['recovered_lapse'])
        zero(tag+'_kinetic_volume_scaling',d['M']-a**3*d['M'].subs(initial))
        zero(tag+'_moving_volume_kinetic_drift',d['Md']-3*H*d['M'])
        Omega=(d['B']-d['B'].conjugate().T).row_join(d['M']).col_join((-d['M']).row_join(s.zeros(m)))
        Od=(d['Bd']-d['Bd'].conjugate().T).row_join(d['Md']).col_join((-d['Md']).row_join(s.zeros(m)))
        zero(tag+'_actual_symplectic_transport',Od+d['G'].conjugate().T*Omega+Omega*d['G'])
        if mean:extra=s.zeros(1,2*m)
        elif route=='R-tau':extra=(par['b']*p*k*k/a**2*d['solve'][0,:]).applyfunc(clean)
        else:
            E=s.zeros(10,m)
            for j,slot in enumerate(d['slots'][:-1]):
                oldslots=(0,1,3,6,7,8,9,10,11,12)
                E[oldslots.index(slot),j]=1
            qmap=s.eye(2*m)[:m,:];vmap=s.eye(2*m)[m:2*m,:]
            frame_E=-(OM[5,:]*E*d['G'][m:2*m,:]+Of[5,:]*E*vmap+Or[5,:]*E*qmap)
            extra=(s.I*k/a**4*frame_E).applyfunc(clean)
        total_clock=(d['bare_clock_ward']-extra).applyfunc(clean)
        cw,cq=helper.friedmann_remainder(total_clock,env)
        pw,pq=helper.friedmann_remainder(d['phase_ward'],env)
        zero(tag+'_total_clock_Ward_mod_background_constraint',cw)
        zero(tag+'_full_U1_Ward_mod_background_constraint',pw)
        d['clock_extra']=extra;d['clock_remainder']=cw;d['phase_remainder']=pw
        if not mean:
            check(tag+'_bare_dust_continuity_is_not_the_full_equation',any(s.expand(z)!=0 for z in extra))
            up=s.zeros(d['lapse'].cols,2*m);up[:d['pull'].rows,:]=d['pull']
            epsi=s.zeros(1,2*m);epsi[0,d['slots'].index(12)]=1
            trace=s.zeros(1,2*m);trace[0,0]=trace[0,2]=1
            wrong_clock=(d['lapse_no_flux']*up/a**3+3*par['beta']*rho*epsi+rho*trace/2).applyfunc(clean)
            wrong=(wrong_clock.applyfunc(dt)+wrong_clock*d['G']+(3*H-par['beta']*p)*wrong_clock
                   -s.I*k*rho*d['solve'][3,:]/a-extra).applyfunc(clean)
            bad,_=helper.friedmann_remainder(wrong,env)
            check(tag+'_omitted_lapse_flux_rejected',any(s.expand(z)!=0 for z in bad))
            target=parse(parent['candidates'][route]['reduced_kinetic']).subs(loc['w'],0)
            zero(tag+'_first_bundle_kinetic_recovered',d['M'].subs(initial)-target)
            wave[route]=d
        else:
            eig=d['M'].subs(initial).eigenvals()
            d['mean_inertia']=[sum(mul for z,mul in eig.items() if z.is_positive),
                              sum(mul for z,mul in eig.items() if z.is_negative),
                              sum(mul for z,mul in eig.items() if z==0)]
            charges=d['clock_row'].col_join(d['phase_charge_row']).subs(initial)
            check(tag+'_two_fixed_charge_rows_independent',charges.rank()==2,charges.rank())
            check(tag+'_homogeneous_temporal_block_invertible',d['M'].det()!=0)
            means[route]=d
        print(tag+'_FULL_ACTION_AND_CURRENT_ROWS_COMPLETE',flush=True)

    # Initial mixed-order principal asymptotics of the complete determinant.
    omega,c,ys,zeta,yf=s.symbols('omega c speed_squared zeta fast_squared',real=True)
    characteristics={}
    for route,d in wave.items():
        m=d['m'];Mi=d['M'].subs(initial)
        Ci=(d['B']-d['B'].conjugate().T).subs(initial).applyfunc(clean)
        Qi=d['Q'].subs(initial).applyfunc(clean)
        coeff=lambda mat,n:mat.applyfunc(lambda z:clean(s.Poly(z,k).coeff_monomial(k**n)))
        C1=coeff(Ci,1);Q2=coeff(Qi,2);Q4=coeff(Qi,4)
        check(route+'_complete_quadratic_polynomial_orders',
              all(s.Poly(z,k).degree()<=1 for z in Ci) and all(s.Poly(z,k).degree()<=4 for z in Qi))
        P=s.zeros(m)
        P[0,0]=1;P[2,0]=-1;P[1,1]=1
        if route=='F-tau':
            P[0,2]=P[2,2]=1
            for j in range(3,7):P[j,j]=1
            scalar=list(range(2,7));sectors=[('tensor_plus',[0]),('tensor_cross',[1])]
            labels=['tensor_plus','tensor_cross','trace','du','dv','dr','dpsi']
        else:
            P[3,2]=1;P[4,3]=1;P[0,4]=P[2,4]=1
            for j in range(5,10):P[j,j]=1
            scalar=list(range(4,10))
            sectors=[('tensor_plus',[0]),('tensor_cross',[1]),('vector_x',[2]),('vector_y',[3])]
            labels=['tensor_plus','tensor_cross','vector_x','vector_y','trace','v_z','du','dv','dr','dpsi']
        mh=P.T*Mi*P;ch=P.T*C1*P;qh=P.T*Q2*P;qh4=P.T*Q4*P
        partgroups=[ix for _,ix in sectors]+[scalar]
        for idx,part in enumerate(partgroups):
            rest=[j for j in range(m) if j not in part]
            for name,mat in [('M',mh),('C1',ch),('Q2',qh),('Q4',qh4)]:
                zero(route+'_helicity_'+str(idx)+'_'+name,mat.extract(part,rest))
        speeds={}
        for name,ix in sectors:
            j=ix[0];speeds[name]=str(clean(-qh[j,j]/mh[j,j]))
        ms=mh.extract(scalar,scalar);cs=ch.extract(scalar,scalar)
        qs=qh.extract(scalar,scalar);qs4=qh4.extract(scalar,scalar)
        pencil=-omega**2*ms-s.I*omega*k*cs-k*k*qs-k**4*qs4
        det=clean(pencil.det(method='domain-ge'))
        po=s.Poly(s.together(det.subs(omega,c*k)),k)
        ordinary=clean(po.LC())
        cp=s.Poly(ordinary,c);check(route+'_ordinary_principal_even_frequency',all(j[0]%2==0 for j,_ in cp.terms()))
        ordinary_y=sum(val*ys**(mon[0]//2) for mon,val in cp.terms())
        ordinary_y=s.Poly(ordinary_y,ys).monic().as_expr()
        roots=s.roots(ordinary_y,ys)
        check(route+'_ordinary_roots_completely_resolved',sum(roots.values())==s.degree(ordinary_y,ys))
        fp=s.Poly(s.together(det.subs(omega,zeta*k*k)),k)
        zp=s.Poly(clean(fp.LC()),zeta)
        fast_y=sum(val*yf**(mon[0]//2) for mon,val in zp.terms())
        fast_y=s.Poly(fast_y,yf).monic().as_expr();fast_roots=s.roots(fast_y,yf)
        principal=dict(helicity_labels=labels,helicity_map=encode(P),
            scalar_principal_pencil=encode(pencil),scalar_determinant=str(s.factor(det)),
            ordinary_leading_k_degree=po.degree(),ordinary_speed_polynomial=str(s.factor(ordinary_y)),
            ordinary_squared_speeds={str(z):int(mult) for z,mult in roots.items()},
            fast_leading_k_degree=fp.degree(),fast_coefficient_polynomial=str(s.factor(fast_y)),
            fast_squared_coefficients={str(z):int(mult) for z,mult in fast_roots.items()},
            other_squared_speeds=speeds,negative_ordinary_squared_speeds=[str(z) for z in roots if z.is_negative],
            instantaneous_control_only=True,physical_cutoff_inferred=False)
        if route=='R-tau':
            # This is the limiting ordinary trace/frame block, not a projection of evolution.
            ix=[scalar[0],scalar[1]];mc=mh.extract(ix,ix);cc=ch.extract(ix,ix);qc=qh.extract(ix,ix)
            Ab=s.zeros(4);Ab[:2,2:4]=s.eye(2);Ab[2:4,:2]=mc.inv()*qc;Ab[2:4,2:4]=-mc.inv()*cc
            ev=Ab.eigenvals();alg=int(ev.get(s.Integer(0),0));geo=4-Ab.rank()
            principal['ordinary_trace_frame_balanced_generator']=encode(Ab)
            principal['zero_root_algebraic_multiplicity']=alg
            principal['zero_root_geometric_multiplicity']=geo
            principal['zero_root_kernel_square_dimension']=4-(Ab*Ab).rank()
            principal['standard_balanced_principal_zero_defective']=bool(alg>geo)
            principal['physical_constrained_norm_clearance']=False
            check('R_tau_zero_branch_is_explicitly_classified',alg>=geo and geo>=0)
        characteristics[route]=principal
        print(route+'_FULL_DETERMINANT_PRINCIPAL_FACTORIZED',flush=True)

    # Independent real quadrature and original physical-action directional checks.
    backend=env['backend'];oldtypes=env['old']
    conv=lambda z:mp.mpf(str(s.N(z,118)))
    vals=[conv(initial[z]) for z in variables];flow=[conv(z) for z in env['flow'].subs(initial)]
    physical_par={key:conv(z) for key,z in par.items()}
    for route,d in wave.items():
        local=d['local'];T=d['T'];full=d['full'];size=local.rows
        for kval in (1,7,40):
            direction=s.Matrix([s.Rational((j*7+3)%13-6,17)+s.I*s.Rational((j*5+1)%11-5,19) for j in range(T.cols)])
            localvec=T.subs(k,kval)*direction;re=localvec.applyfunc(s.re);im=localvec.applyfunc(s.im)
            zero(route+'_real_quadrature_k'+str(kval),
                 (re.T*local*re+im.T*local*im-direction.conjugate().T*full.subs(k,kval)*direction)[0])
        raw=backend.ClockGaugeAction(route,physical_par,physical=True)
        def physical_value(xx):
            return raw.density(helper.state(d['slots'],xx,vals,physical_par,mp.exp,False))[0]
        L0=physical_value([mp.mpf(0)]*size)
        numlocal=s.lambdify(variables,local,modules='mpmath')(*vals)
        for seed in (1,2):
            direction=mp.matrix([mp.mpf(((j+1)*(seed+3))%13-6)/(19+seed) for j in range(size)])
            expected=(direction.T*numlocal*direction)[0];errs=[]
            for hs in ('1e-10','1e-16'):
                h=mp.mpf(hs);fd=(physical_value([h*z for z in direction])+physical_value([-h*z for z in direction])-2*L0)/(h*h)
                err=abs(fd-expected)/(1+abs(expected))
                check(route+'_physical_full_C2_'+str(seed)+'_'+hs,err<1000*h,mp.nstr(err,65));errs.append(mp.nstr(err,65))
            controls.append(dict(route=route,kind='physical full C2',seed=seed,errors=errs))
        fb=s.lambdify(variables+(k,),d['B'],modules='mpmath')
        fbd=s.lambdify(variables+(k,),d['Bd'],modules='mpmath')
        for kval in (1,7,40):
            target=fbd(*vals,kval);errs=[]
            for hs in ('1e-14','1e-22'):
                h=mp.mpf(hs);plus=[z+h*f for z,f in zip(vals,flow)];minus=[z-h*f for z,f in zip(vals,flow)]
                value=(fb(*plus,kval)-fb(*minus,kval))/(2*h)
                err=max(abs(z) for z in value-target)/(1+max(abs(z) for z in target))
                check(route+'_actual_B_drift_k'+str(kval)+'_'+hs,err<1000*h*h,mp.nstr(err,65));errs.append(mp.nstr(err,65))
            controls.append(dict(route=route,kind='actual B time drift',k=kval,errors=errs))
    outputs={}
    for route in wave:
        dd={}
        for name,collection in [('nonzero_modes',wave),('homogeneous_mode',means)]:
            d=collection[route]
            dd[name]=dict(fields=[helper.LABELS[j] for j in d['slots'][:-1]],
                M=encode(d['M']),B=encode(d['B']),Q=encode(d['Q']),M_dot=encode(d['Md']),B_dot=encode(d['Bd']),
                initial_generator=encode(d['G'].subs(initial)),local_Hessian=encode(d['local']),
                algebraic_block=encode(d['D']),constraint_solution=encode(d['solve']),
                density_row=encode(d['rho_row']),epsilon_scaled_row=encode(d['epsilon_scaled_row']),
                clock_charge_row=encode(d['clock_row']),clock_extra_row=encode(d['clock_extra']),
                clock_Ward_remainder=encode(d['clock_remainder']),phase_charge_row=encode(d['phase_charge_row']),
                phase_current_row=encode(d['phase_current_row']),phase_Ward_remainder=encode(d['phase_remainder']))
            if name=='homogeneous_mode':
                dd[name]['raw_temporal_inertia']=d['mean_inertia']
                dd[name]['fixed_charge_phase_space_dimension']=2*d['m']-2
                dd[name]['interpretation']='All six metric amplitudes retained; homogeneous charge-restricted ODE control, not a new quantum-ghost verdict or full global reduction'
        dd['initial_characteristics']=characteristics[route];outputs[route]=dd
    for path,(digest,mtime) in snapshots.items():
        f=ROOT/path;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,path
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    return dict(kind='R4C1_TWO_REPAIR_CHARACTERISTICS_V2',passed=sum(z['passed'] for z in checks),total=len(checks),
        checks=checks,source_sha256=pins,independent_controls=controls,candidates=outputs,
        background_order=[str(z) for z in variables],background_flow=[str(clean(z)) for z in env['flow']],
        initial={str(z):str(initial[z]) for z in variables},
        fixed_charge_note='delta I=(a^3/C_bg)*clock_charge_row*x; delta Q=a^3*phase_charge_row*x; induced clock current has zero normal flux on clock slices',
        complete_interacting_physical_domain=False,physical_window_demonstrated=False,
        nonlinear_stability=False,canonical_parent_adopted=False,review='DEFERRED',Rule9_cleared=False,
        physics_pass=False,gate_effect='NONE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',MAT001='BLOCKED',G1_G6='INCOMPLETE')

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args()
    result=calculate();data=ENC(result)
    if a.replay:
        assert a.replay.read_bytes()==data,'immutable replay differs';print('READ_ONLY_REPLAY_EXACT',SHA(data))
    else:
        a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json'
        p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=result['passed'],total=result['total'],physics_pass=False,receipt=str(p))))
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':raise SystemExit(main())

