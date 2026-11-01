"""Mixed-regularity physical density/canonical norm for the unadopted R-tau.

Reuses the complete new quadratic action, never the old-action propagator.
All estimates are linear, control-unit and background-domain scoped.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_two_repair_characteristics_v3_attempt_01/summary.json'
PSHA='acc0558461b0e7882edc6e59baae4d9b2d886fb33882bd0bc5928834a1a57515'
HELPER='Analysis/MasterTests/r4c1_two_repair_quadratic_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PHYSICAL_NORM_V1_CONTRACT_2026-10-31.md'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PHYSICAL_NORM_V1_EXECUTION_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))

def calculate():
    mp.mp.dps=120;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,obj):
        entries=list(obj) if isinstance(obj,s.MatrixBase) else [obj]
        bad=[str(v) for z in entries if (v:=clean(z))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=json.loads((ROOT/PARENT).read_bytes());assert parent['passed']==parent['total']==129
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (SELF,HELPER,CONTRACT,SPEC,'Analysis/MasterTests/test_01_r4c1_rtau_physical_norm_v1.py','Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v1_attempt_01/summary.json','Theory/Gates/RES-001/RES001_R4C1_RTAU_PHYSICAL_NORM_V2_EXECUTION_ADDENDUM_2026-10-31.md'):pins[path]=SHA((ROOT/path).read_bytes())
    snapshots={}
    for path,want in pins.items():
        f=ROOT/path;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,path
        for p in (f,sc):snapshots[p.relative_to(ROOT).as_posix()]=(SHA(p.read_bytes()),p.stat().st_mtime_ns)
    spec=importlib.util.spec_from_file_location('rtau_norm_background',ROOT/HELPER)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    env=helper.setup();variables=env['variables'];a,H,u,v,r,du,dv,dr,p,psi,rho=variables
    k=env['k'];kap=s.Symbol('kappa',positive=True);par=env['par'];initial=env['initial']
    loc={str(z):z for z in variables+(k,)}
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=loc) for z in row] for row in rows])
    dt=lambda z:sum(s.diff(z,w)*f for w,f in zip(variables,env['flow']))-H*kap*s.diff(z,kap)
    mod=lambda mat:helper.friedmann_remainder(mat,env)[0].reshape(mat.rows,mat.cols) if mat.rows==1 else mat.applyfunc(lambda z:helper.friedmann_remainder(s.Matrix([[z]]),env)[0][0])
    enc=lambda mat:[[str(clean(z)) for z in row] for row in mat.tolist()]
    wave=parent['candidates']['R-tau']['nonzero_modes']
    M,B,Q,Md,Bd=(parse(wave[n]) for n in ('M','B','Q','M_dot','B_dot'))
    zero('actual_M_drift_reused_and_checked',M.applyfunc(dt)-Md)
    zero('actual_B_drift_reused_and_checked',B.applyfunc(dt)-Bd)
    G=s.zeros(20);G[:10,10:]=s.eye(10)
    G[10:,:10]=-M.inv()*(Bd-Q);G[10:,10:]=-M.inv()*(Md+B-B.conjugate().T)
    G=G.applyfunc(clean)
    P=parse(parent['candidates']['R-tau']['initial_characteristics']['helicity_map'])
    I=s.diag(P,P);Gh=(I.inv()*G*I).applyfunc(clean)
    si=list(range(4,10));ix=si+[j+10 for j in si];other=[i for i in range(20) if i not in ix]
    zero('full_scalar_other_helicity_decoupling',Gh.extract(ix,other))
    zero('full_other_scalar_decoupling',Gh.extract(other,ix))
    Ms=(P.T*M*P).extract(si,si);Bs=(P.T*B*P).extract(si,si)
    canonical=(Ms.inv()*Bs).applyfunc(clean)
    Gs=mod(Gh.extract(ix,ix).subs(k,a*kap)).applyfunc(clean)
    rho_row=mod((parse(wave['density_row'])*I).extract([0],ix).subs(k,a*kap)).applyfunc(clean)
    zero('on_shell_density_curvature_coefficient',rho_row[0,0]-kap**2)
    T=s.zeros(12);T[0,:]=rho_row
    T[0,11]+=par['K_Q']*p;T[0,5]+=par['K_Q']*par['beta']*p*p
    for j in range(1,5):T[j,j]=kap
    T[5,5]=kap**2
    T[6:11,:6]=canonical[:5,:].subs(k,a*kap)
    for j in range(5):T[6+j,6+j]=1
    T[11,11]=1
    T=T.applyfunc(clean);Ti=T.inv().applyfunc(clean);Td=T.applyfunc(dt).applyfunc(clean)
    zero('physical_map_inverse',T*Ti-s.eye(12))
    denominator=kap**2+du**2+dv**2+dr**2
    # Determinant is independently computed; no cancellation is assumed.
    detT=clean(T.det(method='domain-ge'))
    zero('canonical_density_pivot',detT-kap**6*denominator)
    YG=((Td+T*Gs)*Ti).applyfunc(clean)
    zero('full_generator_conjugacy_with_actual_drift',YG*T-Td-T*Gs)
    check('omitting_time_dependent_map_drift_rejected',any(z!=0 for z in Td))
    A2=YG.applyfunc(lambda z:clean(s.limit(z/kap**2,kap,s.oo)))
    A1=(YG-kap**2*A2).applyfunc(lambda z:clean(s.limit(z/kap,kap,s.oo)))
    R=(YG-kap**2*A2-kap*A1).applyfunc(clean)
    check('mixed_principal_coefficients_finite',not (A2.has(s.oo,s.zoo,s.nan) or A1.has(s.oo,s.zoo,s.nan)))
    qgrad=s.Matrix([[1+par['zeta']*v*v,-par['zeta']*u*v],[-par['zeta']*u*v,1+par['zeta']*u*u]])
    L3=s.Matrix([[-s.I/198,1,0],[s.Rational(12,11),18*s.I,0],[0,0,1]])
    H3=L3.conjugate().T*s.diag(1,s.Rational(1,3),1)*L3
    E=s.zeros(12);E[0,0]=1
    for i,ii in enumerate((1,6,7)):
        for j,jj in enumerate((1,6,7)):E[ii,jj]=H3[i,j]
    E[2:4,2:4]=qgrad;E[4,4]=1;E[5,5]=par['b']
    for j in (8,9,10):E[j,j]=1
    E[11,11]=par['K_Q'];E=E.applyfunc(clean)
    zero('energy_Hermitian',E-E.conjugate().T)
    zero('quartic_principal_energy_cancellation',A2.conjugate().T*E+E*A2)
    zero('ordinary_principal_energy_cancellation',A1.conjugate().T*E+E*A1)
    zero('trace_frame_positive_factorization',H3-L3.conjugate().T*s.diag(1,s.Rational(1,3),1)*L3)
    check('trace_frame_strict_principal_minors',all(H3[:j,:j].det()>0 for j in (1,2,3)))
    check('trace_frame_two_block_trace_below_110',s.trace(H3[:2,:2])<110,{'two_block_trace':str(s.trace(H3[:2,:2])),'full_trace':str(s.trace(H3))})
    zero('trace_frame_two_block_determinant',H3[:2,:2].det()-s.Rational(1,3))
    zero('condensate_positive_rank_one_form',qgrad-s.eye(2)-par['zeta']*s.Matrix([v,-u])*s.Matrix([[v,-u]]))
    ai=list(range(5))+list(range(6,11));ordinary=A1.extract(ai,ai)
    zero('fast_ordinary_principal_decoupling_A1',A1.extract([5,11],ai).col_join(A1.extract(ai,[5,11]).T))
    zero('quartic_principal_only_force_block',A2.extract(ai,list(range(12))))
    zero('quartic_force_block',A2.extract([5,11],[5,11])-s.Matrix([[0,1],[-par['b']/par['K_Q'],0]]))
    # Rank of the action-derived ordinary matrix is tested without suppressing a mode.
    oi=ordinary.subs(initial);ep=oi.charpoly().as_expr();lam=next(iter(ep.free_symbols)) if ep.free_symbols else s.Symbol('lambda')
    alg=min(mon[0] for mon,val in s.Poly(ep,lam).terms());geo=ordinary.rows-oi.rank()
    check('zero_branch_retained_semisimple_in_physical_principal',alg==geo==2,[int(alg),int(geo)])
    print('PHYSICAL_MAP_AND_PRINCIPAL_ENERGY_COMPLETE',flush=True)

    # Exact absolute-coefficient majorants, not fitted numerical eigenvalues.
    def polynomial_bound(z):
        num,den=s.fraction(clean(z)); dp=s.Poly(den,*variables)
        terms=dp.terms()
        if len(terms)!=1 or any(n and variables[j]!=a for j,n in enumerate(terms[0][0])):
            raise ValueError('unregistered background denominator '+str(den))
        mon,c=terms[0];factor=2**sum(mon)/abs(c)
        return clean(factor*sum(abs(c)*2**sum(mon) for mon,c in s.Poly(num,*variables).terms()))
    def rational_bound(z):
        if z==0:return s.Integer(0)
        num,den=s.fraction(clean(z));c,fac=s.factor_list(den,kap);power=0
        for f,n in fac:
            if clean(f-kap)==0:power+=n
            elif clean(f-denominator)==0:power+=2*n
            else:raise ValueError('unregistered momentum denominator '+str(f))
        result=s.Integer(0)
        for (j,),coef in s.Poly(num,kap).terms():
            if j>power:raise ValueError('unbounded remainder coefficient '+str(z))
            result+=polynomial_bound(coef/c)*2**(power-j)
        return clean(result)
    def matrix_bound(mat):
        bounds=mat.applyfunc(rational_bound)
        return clean(sum(bounds)),bounds
    rb,rb_entries=matrix_bound(R)
    check('remainder_bound_finite_nonnegative',rb.is_finite and rb>=0,str(rb))
    S=s.diag(kap,kap,kap,kap,kap,kap**2,1,1,1,1,1,1)
    O=rho_row.col_join(S)
    L=s.zeros(12,13);L[0,0]=1;L[0,12]=par['K_Q']*p
    L[0,6]=par['K_Q']*par['beta']*p*p/kap**2
    for j in range(1,6):L[j,j+1]=1
    J=canonical.row_join(s.eye(6))
    L[6:11,1:13]=J[:5,:].subs(k,a*kap)*S.inv()
    L[11,12]=1
    zero('natural_observable_to_physical_map',L*O-T)
    N=(O*Ti).applyfunc(clean)
    zero('physical_to_natural_observable_map',N*T-O)
    lb,_=matrix_bound(L);nb,_=matrix_bound(N)
    # Include reconstructed auxiliary, lapse, and differentiated shift quantities.
    rec=(parse(wave['constraint_solution'])*I).extract(list(range(4)),ix).subs(k,a*kap)
    rec=s.diag(1,kap,kap,kap)*rec*Ti
    recon_bound,_=matrix_bound(rec.applyfunc(clean))
    energy_rate=clean(330*(s.Rational(16,13)+220*rb))
    print('UNIFORM_SCALAR_REMAINDER_AND_RECONSTRUCTION_BOUNDED',flush=True)

    other_data={};other_rates=[]
    for idx,name in enumerate(('tensor_plus','tensor_cross','vector_x','vector_y')):
        indexes=[idx,idx+10];g=Gh.extract(indexes,indexes).subs(k,a*kap).applyfunc(clean)
        mass=(P.T*M*P)[idx,idx];bval=(P.T*B*P)[idx,idx]
        tw=s.Matrix([[kap,0],[clean(bval/mass),1]]);tiw=tw.inv();tdw=tw.applyfunc(dt)
        gw=((tdw+tw*g)*tiw).applyfunc(clean)
        aa=gw.applyfunc(lambda z:clean(s.limit(z/kap,kap,s.oo)))
        cs=clean(-aa[1,0]);he=s.diag(cs,1)
        zero(name+'_principal_positive_wave',aa-s.Matrix([[0,1],[-cs,0]]))
        check(name+'_squared_speed_positive',cs>0,str(cs))
        zero(name+'_principal_energy_cancellation',aa.conjugate().T*he+he*aa)
        ro=(gw-kap*aa).applyfunc(clean);bo,_=matrix_bound(ro)
        rate=clean(2*max(cs,1)*bo/min(cs,1));other_rates.append(rate)
        other_data[name]=dict(generator=enc(gw),squared_speed=str(cs),remainder_bound=str(bo),energy_rate=str(rate))

    mean=parent['candidates']['R-tau']['homogeneous_mode'];m0=13
    MM,BB,QQ,MD,BD=(parse(mean[n]) for n in ('M','B','Q','M_dot','B_dot'))
    G0=s.zeros(26);G0[:m0,m0:]=s.eye(m0)
    G0[m0:,:m0]=-MM.inv()*(BD-QQ);G0[m0:,m0:]=-MM.inv()*(MD+BB-BB.conjugate().T)
    G0=mod(G0).applyfunc(clean);mean_bound=clean(sum(polynomial_bound(z) for z in G0))
    for n,scaling in (('clock_charge_row',3*H-par['beta']*p),('phase_charge_row',3*H)):
        row=parse(mean[n]);zero('mean_'+n+'_preserved',mod(row.applyfunc(dt)+row*G0+scaling*row))
    charges=parse(mean['clock_charge_row']).col_join(parse(mean['phase_charge_row'])).subs(initial)
    check('mean_fixed_charge_rows_independent',charges.rank()==2)
    flow_bounds=[polynomial_bound(z) for z in env['flow']]
    biggest=max(flow_bounds);Tmax=s.Rational(1,200)
    lower=[s.Rational(1,2)]+[-s.Integer(2)]*9+[s.Rational(1,20)]
    upper=[s.Integer(2)]*11
    margins=[min(clean(initial[z]-lo),clean(hi-initial[z])) for z,lo,hi in zip(variables,lower,upper)]
    check('background_box_strict_exit_bound',all(Tmax*b<margin for b,margin in zip(flow_bounds,margins)),
          {'T':str(Tmax),'flow_bounds':[str(z) for z in flow_bounds],'margins':[str(z) for z in margins]})
    zero('background_Friedmann_constraint_preserved',sum(s.diff(env['friedmann'],z)*f for z,f in zip(variables,env['flow'])))
    print('OTHER_HELICITIES_MEAN_AND_BACKGROUND_CONTROL_COMPLETE',flush=True)

    # Independent numerical actual-map-drift and physical reconstruction controls.
    num=lambda z:mp.mpf(str(s.N(z,118)))
    vals=[num(initial[z]) for z in variables];fv=[num(z) for z in env['flow'].subs(initial)]
    ft=s.lambdify(variables+(kap,),T,modules='mpmath')
    ftd=s.lambdify(variables+(kap,),Td,modules='mpmath')
    controls=[]
    for kval in (1,7,40):
        expected=ftd(*vals,kval);errors=[]
        for hs in ('1e-14','1e-22'):
            h=mp.mpf(hs);plus=[z+h*f for z,f in zip(vals,fv)];minus=[z-h*f for z,f in zip(vals,fv)]
            fd=(ft(*plus,kval/plus[0])-ft(*minus,kval/minus[0]))/(2*h)
            err=max(abs(z) for z in fd-expected)/(1+max(abs(z) for z in expected))
            check('actual_map_drift_k'+str(kval)+'_'+hs,err<1000*h*h,mp.nstr(err,65));errors.append(mp.nstr(err,65))
        controls.append(dict(k=kval,actual_map_drift_errors=errors))
        point={**initial,kap:s.Integer(kval)}
        tv=T.subs(point);tiv=Ti.subs(point);ov=O.subs(point);ev=E.subs(point)
        x=s.Matrix([s.Rational((7*j+3)%17-8,19)+s.I*s.Rational((11*j+2)%13-6,23) for j in range(12)])
        yy=tv*x
        zero('independent_complex_state_reconstruction_k'+str(kval),tiv*yy-x)
        energy=clean((yy.conjugate().T*ev*yy)[0]);obs=clean((x.conjugate().T*ov.conjugate().T*ov*x)[0])
        check('positive_natural_norm_equivalence_k'+str(kval),energy>0 and obs>0 and
              energy>=obs/(330*nb**2) and energy<=110*lb**2*obs)
        # Directly check the claimed complete energy-derivative identity.
        cmat=(E.applyfunc(dt)+YG.conjugate().T*E+E*YG-E.applyfunc(dt)-R.conjugate().T*E-E*R).applyfunc(clean)
        zero('full_energy_derivative_identity_k'+str(kval),cmat.subs(point))
    for path,(digest,mtime) in snapshots.items():
        f=ROOT/path;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,path
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    return dict(kind='R4C1_RTAU_PHYSICAL_NORM_V2',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,
        source_sha256=pins,variables=[str(z) for z in variables],scalar_field_order=['Gamma','v_z','du','dv','dr','dpsi'],
        physical_variables=['sigma','kappa*v_z','kappa*du','kappa*dv','kappa*dr','kappa^2*dpsi','Pi_Gamma','Pi_vz','Pi_u','Pi_v','Pi_r','dpsi_dot'],
        scalar=dict(T=enc(T),T_inverse=enc(Ti),T_dot=enc(Td),density_row=enc(rho_row),canonical_momentum_shift=enc(canonical.subs(k,a*kap)),
            physical_generator=enc(YG),A2=enc(A2),A1=enc(A1),remainder=enc(R),energy_form=enc(E),
            map_determinant=str(detT),remainder_entry_bounds=enc(rb_entries),remainder_norm_bound=str(rb),
            coercivity_lower='1/330',coercivity_upper='110',energy_growth_rate=str(energy_rate),
            natural_to_physical_norm_bound=str(lb),physical_to_natural_norm_bound=str(nb),reconstructed_constraint_bound=str(recon_bound),
            physical_principal_zero_algebraic=int(alg),physical_principal_zero_geometric=int(geo)),
        other_helicities=other_data,homogeneous=dict(generator=enc(G0),euclidean_generator_bound=str(mean_bound),energy_growth_rate=str(2*mean_bound),fixed_charge_level_dimension=24),
        background=dict(time_interval=['0',str(Tmax)],flow_bound=[str(z) for z in flow_bounds],box='a in [1/2,2]; rho in [1/20,2]; all other registered coordinates have absolute value <=2',
                        kappa_min='1/2',comoving_modes='|k|>=1 in the registered control units; k=0 separate'),
        independent_controls=controls,linear_control_estimate_only=True,nonlinear_Cauchy_theorem=False,
        physical_window_demonstrated=False,microscopic_clock_choice_justified=False,canonical_parent_adopted=False,
        review='DEFERRED',Rule9_cleared=False,physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',MAT001='BLOCKED')

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);args=ap.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        assert args.replay.read_bytes()==data,'immutable replay differs';print('READ_ONLY_REPLAY_EXACT',SHA(data))
    else:
        args.output_dir.mkdir(parents=True,exist_ok=False);f=args.output_dir/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=result['passed'],total=result['total'],physics_pass=False,receipt=str(f))))
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':raise SystemExit(main())
