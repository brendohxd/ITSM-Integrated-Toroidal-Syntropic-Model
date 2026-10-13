"""Frozen one-family canonical audit, mixed-order symbol and slow action."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
OLD='Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v1.py'
INDEPENDENT='Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_principal_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_NONZERO_CHARACTERISTIC_CONTRACT_2026-10-11.md'
PINS={OLD:'6b9cc5f402957172c0dfcaa2f0a81997235287380e77a60c4649eb9e16a09f37',
      INDEPENDENT:'01adbf26bec2db76e485915477b43bd0dba6ab4c3f3c41b0bcce6cf954c1cc6a',
      CONTRACT:'c38337a6f439bf1556c8c250a1d14a1166f3133bac67aa4eb71a2d005160fe9c',
      BASE+'r4c1_g3n5_attempt_02/summary.json':'560e369d7795ed8e06d0c2c26350d3b412a53c577da82f0669e68f6ee04f5666',
      BASE+'r4c1_g3n5_constraint_response_attempt_02/summary.json':'04705ea37aa944a567387073b1eda81c824d447566d061ddfd684abfbf30649d',
      BASE+'r4c1_g3n5_mean_mode_energy_attempt_04/summary.json':'bdda5069e8650b2bcdb5cb897978c493f480443e7ad254479c20502c6fac5c93',
      BASE+'r4c1_g3n5_nonzero_principal_attempt_02/summary.json':'cf753b645edee69813aefa050ee1719b0d2d8d34a44ba28c1b89ef8859dcaa8c',
      'Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_REPORT_2026-10-11.md':'331b596dada0073ee1d50da69d3a8bbb8475c0b9cd7b8b246c5d03c7d536339f'}
for name in (OLD, INDEPENDENT):
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=PINS[name]:
        raise RuntimeError('Frozen imported source drift: '+name)
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_constraint_response_v1 as old
import test_01_r4c1_g3n5_nonzero_principal_v2 as separate
common=old.common


def exact(checks,name,expr):
    values=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    bad=[]
    for j,v in enumerate(values):
        q=s.expand(v)
        if q!=0:q=s.cancel(q)
        if q!=0:bad.append({'index':j,'residual':str(q)})
    checks.add(name,not bad,bad,'zero_exact')


def ex(mat):return mat.applyfunc(s.expand)


def exports(mat):return old.matrix_export(mat)


def import_matrix(obj,sy):
    out=s.zeros(*obj['shape'])
    for row in obj['entries']:
        out[row['row'],row['column']]=s.Add(*(s.sympify(v,locals=sy) for v in row['terms']))
    return out


def snapshot(paths):
    return {str(q.relative_to(ROOT)):dict(sha=common.sha(q.read_bytes()),size=q.stat().st_size,
                                        mtime_ns=q.stat().st_mtime_ns) for q in paths}


def inherited_pins():
    pins=dict(PINS)
    parents=[q for q in PINS if q.endswith('/summary.json')]
    parents.extend([BASE+'r4c1_g3n5_constraint_response_attempt_01/summary.json',
                    BASE+'r4c1_g3n5_nonzero_principal_attempt_01/summary.json'])
    for rel in parents:
        parent=common.read_json(rel)
        pairs=list(parent['source_sha256'].items())+[(str(Path(rel).parent).replace('\\','/')+'/'+k,v)
                for k,v in parent.get('artifacts',{}).items()]
        pairs.append((rel,common.sha((ROOT/rel).read_bytes())))
        for name,value in pairs:
            if name in pins and pins[name]!=value:raise ValueError('Conflicting parent pin '+name)
            pins[name]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    return pins


def calculate():
    pins=inherited_pins();missing=common.inspect_pins(pins)
    paths=[ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').is_file())
    before=snapshot(paths)
    checks=common.Checks()
    checks.add('all_source_pins_before',True,{'pins':len(pins),'sidecars':len(pins)-len(missing),'absent':missing})
    print('Reuse full 22-field kernel; derive positive-x family',flush=True)
    op=old.Operator(checks)
    ell=s.Symbol('ell',positive=True);p=s.Symbol('p',positive=True)
    ch=op.chart(checks,(ell,0,0))
    F=s.Matrix(ch['F']).applyfunc(s.nsimplify)
    U=s.zeros(22,4)
    for j,name in enumerate(ch['aux']):U[old.IDX[name],j]=1
    sub=dict(zip(op.k,(ell,0,0)))
    LA,LB,LBT,LK=[ex(m.subs(sub)) for m in (op.LA,op.LB,op.LBT,op.LK)]
    Ys,Vs=ex(U.T*LA*F),ex(U.T*LB*F)
    inv=ch['inverse'];a,H=op.bg[:2];vol=a**3
    A=ex(F.T*LA*F-Ys.conjugate().T*inv*Ys)
    R=ex(F.T*LBT*F-Vs.conjugate().T*inv*Ys)
    K=ch['K'];Ki=K.inv()
    for name,mat in [('A',A),('K',K)]:exact(checks,'reduced_'+name+'_Hermitian',mat-mat.conjugate().T)
    E0,E1,E2=(ch['symbolic'][key] for key in ('E0','E1','E2'))
    exact(checks,'A_R_K_evolving_Euler_value',E0-A+op.dtm(R)+3*H*R)
    exact(checks,'A_R_K_evolving_Euler_velocity',E1-R.conjugate().T+R+op.dtm(K)+3*H*K)
    # Canonical one-form: auxiliary coordinates can depend on y_dot, but
    # their unreduced momenta vanish. They cannot add hidden symplectic terms.
    Q0,Q1=ch['symbolic']['Q0'],ch['symbolic']['Q1']
    C0=ex(LK*op.dtm(Q0)+LBT*Q0)
    C1=ex(LK*(Q0+op.dtm(Q1))+LBT*Q1)
    exact(checks,'unreduced_momenta_no_reduced_acceleration',LK*Q1)
    exact(checks,'canonical_one_form_value_pullback',F.T*C0-R)
    exact(checks,'canonical_one_form_velocity_pullback',F.T*C1-K)
    exact(checks,'auxiliary_momenta_value_zero',U.T*C0)
    exact(checks,'auxiliary_momenta_velocity_zero',U.T*C1)
    zero_rows=[old.IDX[q] for q in ('alpha','T','nu','Em','LambdaU')]
    exact(checks,'eliminated_gauge_multiplier_coordinates_have_no_one_form',
          C0[zero_rows,:].row_join(C1[zero_rows,:]))
    # In (y,p_y), p_y=a^3(K y_dot+R y), and y_dot=Ki(p_y/a^3-Ry).
    HH=ex(s.BlockMatrix([[vol*(R.conjugate().T*Ki*R-A),-R.conjugate().T*Ki],
                         [-Ki*R,Ki/vol]]).as_explicit())
    J=s.zeros(20);J[:10,10:]=s.eye(10);J[10:,:10]=-s.eye(10)
    M=s.zeros(20);M[:10,:10]=s.eye(10);M[10:,:10]=vol*R;M[10:,10:]=vol*K
    L=s.zeros(20);L[:10,10:]=s.eye(10);L[10:,:10]=Ki*E0;L[10:,10:]=Ki*E1
    exact(checks,'complete_Hamiltonian_Hermitian',HH-HH.conjugate().T)
    exact(checks,'Hamiltonian_matrix_symplectic', (J*HH).conjugate().T*J+J*(J*HH))
    exact(checks,'Hamilton_Euler_time_dependent_canonical_map',J*HH*M-M*L-op.dtm(M))
    exact(checks,'exact_momentum_Hessian_inverse',vol*HH[10:,10:]*K-s.eye(10))
    exact(checks,'canonical_map_nonsingular_determinant',M.det()-vol**10*K.det())
    saved=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_01/coefficients.json')
    ref=next(q for q in saved['charts'] if q['mode']==[1,0,0])
    parse_sy={**op.sy,'I':s.I,'sqrt':s.sqrt}
    for name,mat in ch['symbolic'].items():
        exact(checks,'saved_ell_one_'+name,mat.subs(ell,1)-import_matrix(ref['matrices'][name],parse_sy))
    # Orthogonal residual-SO(2) decomposition: h,TT+,TTx,Vx,Vy,Vz,du,dv,dr,Pi.
    O=s.eye(10);O[:3,:3]=s.Matrix([[1/s.sqrt(2),1/s.sqrt(2),0],
                                 [0,0,1],[1/s.sqrt(2),-1/s.sqrt(2),0]])
    def physical(mat):return ex((O.T*mat*O).subs(ell,a*p))
    Ap,Rp,Kp=map(physical,(A,R,K))
    def dtp(mat):
        return mat.applyfunc(lambda x:s.expand(op.dt(x)-H*p*s.diff(x,p)))
    def degree(x):
        return max((q.as_powers_dict().get(p,0) for q in s.Add.make_args(s.expand(x)) if q!=0),default=-100)
    def leading0(mat,label):
        checks.add(label+'_has_no_positive_power',all(degree(q)<=0 for q in mat),
                   str(max(degree(q) for q in mat)),'max degree <=0')
        return ex(mat).applyfunc(lambda x:x.coeff(p,0))
    groups=((1,),(2,),(4,),(5,),(0,3,6,7,8,9))
    for name,mat in [('A',Ap),('R',Rp),('K',Kp)]:
        residual=mat.copy()
        for ids in groups:
            for i in ids:
                for j in ids:residual[i,j]=0
        exact(checks,'SO2_block_separation_'+name,residual)
    # Independent hand-derived real-space ADM/frame/regulator principal density.
    independent=separate.derive();scalar=[0,3,9];other=[1,2,4,5,6,7,8]
    Apr=Ap.applyfunc(lambda q:s.Add(*(q.coeff(p,j)*p**j for j in (2,3,4))))
    Rpr=Rp.applyfunc(lambda q:q.coeff(p,1)*p)
    for name,mat,ind in [('A',Apr,independent['A']),('R',Rpr,independent['R']),('K',Kp,independent['K'])]:
        exact(checks,'separate_scalar_principal_'+name,mat.extract(scalar,scalar)-ind)
    exact(checks,'separate_other_principal_A',Apr.extract(other,other)-independent['Aother'])
    exact(checks,'separate_other_principal_K',Kp.extract(other,other)-independent['Kother'])
    w,c,sig=independent['omega'],independent['c'],independent['sigma']
    pencil=ex(Kp*w*w-s.I*w*(Rpr.conjugate().T-Rpr)+Apr)
    scalar_det=s.factor(pencil.extract(scalar,scalar).det())
    exact(checks,'separate_full_scalar_pencil_determinant',scalar_det-independent['determinant'])
    full_det=s.factor(scalar_det*s.prod(pencil[i,i] for i in (1,2,4,5))*pencil.extract([6,7,8],[6,7,8]).det())
    wave=s.factor(s.expand(full_det.subs(w,c*p)).coeff(p,22))
    wave_target=-c*c*(c*c-1)**4*(5*c*c-4)**2*(3*c*c-1)*(13*c*c-op.bg[2]**2-op.bg[4]**2-13)/224640
    exact(checks,'all_wave_scale_root_multiplicities',wave-wave_target)
    fast=s.factor(s.expand(full_det.subs(w,sig*p*p)).coeff(p,40))
    fast_target=sig**18*(33*sig*sig-5)/3456
    exact(checks,'all_fast_scale_root_multiplicities',fast-fast_target)
    companion=independent['companion'];poly=companion.charpoly()
    exact(checks,'zero_speed_characteristic_multiplicity',poly.as_expr()-poly.gen**2*(poly.gen**2-s.Rational(1,3)))
    checks.add('zero_speed_geometric_multiplicity_one',len(companion.nullspace())==1,1,'algebraic 2, geometric 1')
    exact(checks,'zero_speed_Jordan_chain_eigenvector',companion*independent['zero'])
    exact(checks,'zero_speed_Jordan_chain_generalized',companion*independent['generalized']-independent['zero'])
    checks.add('zero_speed_is_retained_not_removed',ch['dimension']==10,10,'unchanged complete reduced chart')
    # Finite-wavenumber invertible coordinate map; obtain a formal slow action
    # only after the entire evolving quadratic action is transformed.
    print('Derive complete evolving formal slow action; keep its sign',flush=True)
    ids=[0,3,6,7,8,9];As,Rs,Ks=[m.extract(ids,ids) for m in (Ap,Rp,Kp)]
    Ts=s.diag(1/p,1,1/p,1/p,1/p,1/p**2)
    Ts[5,1]=s.I*op.bg[8]/p
    Td=dtp(Ts)
    AL=leading0(ex(Ts.conjugate().T*As*Ts+Td.conjugate().T*Ks*Td+
                  Td.conjugate().T*Rs*Ts+Ts.conjugate().T*Rs.conjugate().T*Td),'slow_A')
    RL=leading0(ex(Ts.conjugate().T*Ks*Td+Ts.conjugate().T*Rs*Ts),'slow_R')
    KL=leading0(ex(Ts.conjugate().T*Ks*Ts),'slow_K')
    W=s.zeros(6);aux=[0,2,3,4,5]
    for i in aux:W[i,1]=RL[i,1];W[1,i]=s.conjugate(RL[i,1])
    exact(checks,'slow_boundary_W_Hermitian',W-W.conjugate().T)
    AN, RN=ex(AL-op.dtm(W)-3*H*W),ex(RL-W)
    exact(checks,'slow_auxiliary_has_no_velocity',KL[aux,:].col_join(RN[aux,:]))
    Da=AN.extract(aux,aux);invslow=Da.inv()
    exact(checks,'slow_algebraic_inverse_regular',ex(Da*invslow-s.eye(5)))
    ys=AN.extract(aux,[1]);vs=RN.conjugate().T.extract(aux,[1])
    afinal=s.cancel(AN[1,1]-(ys.conjugate().T*invslow*ys)[0])
    rfinal=s.cancel(RN[1,1]-(vs.conjugate().T*invslow*ys)[0])
    kfinal=s.cancel(KL[1,1]-(vs.conjugate().T*invslow*vs)[0])
    exact(checks,'formal_slow_time_coefficient_negative',kfinal+s.Rational(11,6))
    exact(checks,'slow_remaining_mixed_coefficient_real',rfinal-s.conjugate(rfinal))
    ef0=s.cancel(afinal-op.dt(rfinal)-3*H*rfinal)
    ef1=s.cancel(-op.dt(kfinal)-3*H*kfinal)
    # Cross-check with independently exported unreduced Euler matrices, not
    # just the Legendre expression. Time derivatives are at fixed ell.
    e0,e1,e2=[physical(q).extract(ids,ids) for q in (E0,E1,E2)]
    EL0=leading0(ex(Ts.conjugate().T*(e0*Ts+e1*Td+e2*dtp(Td))),'slow_direct_E0')
    EL1=leading0(ex(Ts.conjugate().T*(e1*Ts+2*e2*Td)),'slow_direct_E1')
    EL2=leading0(ex(Ts.conjugate().T*e2*Ts),'slow_direct_E2')
    f=s.zeros(6,1);f[1]=1;uu=s.zeros(6,5)
    for j,i in enumerate(aux):uu[i,j]=1
    q0=f-uu*invslow*ys;q1=-uu*invslow*vs
    exact(checks,'direct_full_Euler_slow_value',
          (f.T*(EL0*q0+EL1*op.dtm(q0)+EL2*op.dtm(op.dtm(q0))))[0]-ef0)
    exact(checks,'direct_full_Euler_slow_velocity',
          (f.T*(EL0*q1+EL1*(q0+op.dtm(q1))+EL2*(2*op.dtm(q0)+op.dtm(op.dtm(q1)))))[0]-ef1)
    exact(checks,'direct_full_Euler_slow_acceleration',
          (f.T*(EL1*q1+EL2*(q0+2*op.dtm(q1))))[0]+kfinal)
    # Inherited singular boundaries are classified without using their inverse.
    fixed={op.sy[k]:v for k,v in old.PARAMS.items()};fixed.update({a:1,**dict(zip(op.k,(1,0,0)))})
    boundaries=(('regular',{},4),('k_zero',{q:0 for q in op.k},1),('b_zero',{op.sy['b']:0},3),
                ('MU2_zero',{op.sy['MU2']:0},3),('longitudinal_zero',{op.sy['c2']:-op.sy['c1']-op.sy['c3']},3),
                ('tensor_zero',{op.sy['c3']:op.sy['MP2']/op.sy['MU2']-op.sy['c1']},2))
    ranks={}
    for name,changes,target in boundaries:
        rank=int(op.generic_aux.subs(changes,simultaneous=True).subs(fixed).rank());ranks[name]=rank
        checks.add('singular_domain_classification_'+name,rank==target,rank,target)
    exact(checks,'C_zero_dust_clock_degeneracy',op.G0[old.IDX['T'],0].subs(op.bg[-1],0))
    # Numerical controls: no new background integration or old main invocation.
    background=np.load(ROOT/(BASE+'r4c1_g3n5_constraint_response_attempt_01/background.npy'),allow_pickle=False)
    checks.add('same_257_saved_background_points',background.shape==(257,11),list(background.shape))
    checks.add('saved_positive_a_C_rho',bool(np.isfinite(background).all() and np.min(background[:,[0,9,10]])>0))
    Hd=ex(HH.subs(ell,a*p));Md=ex(M.subs(ell,a*p));Ld=ex(L.subs(ell,a*p));Mdt=ex(op.dtm(M).subs(ell,a*p))
    num=s.lambdify([op.bg,p],(Hd,Md,Ld,Mdt),modules='numpy',cse=True)
    eqerr=0.;eigerr=0.;realerr=0.;samples=[];min_kinetic=float(min(K.eigenvals()))
    for i,bg in enumerate(background):
        hn,mn,ln,mdn=[np.asarray(x,dtype=complex) for x in num(bg,1/bg[0])]
        terms=(np.asarray(J,dtype=complex)@hn@mn,-mn@ln,-mdn)
        eqerr=max(eqerr,float(np.linalg.norm(sum(terms),np.inf)/max(sum(np.linalg.norm(z,np.inf) for z in terms),1e-20)))
        if i in (0,128,256):
            for kval in (1,2,4,8,16,32,64,128):
                hn=np.asarray(num(bg,kval)[0],dtype=complex);gn=np.asarray(J,dtype=complex)@hn
                ev,vec=np.linalg.eig(gn)
                residual=np.linalg.norm(gn@vec-vec*ev,np.inf)/max(np.linalg.norm(gn@vec,np.inf)+np.linalg.norm(vec*ev,np.inf),1e-20)
                eigerr=max(eigerr,float(residual))
                hr=np.block([[hn.real,-hn.imag],[hn.imag,hn.real]])
                jr=np.kron(np.eye(2),np.asarray(J,dtype=float))
                rr=np.linalg.norm((jr@hr).T@jr+jr@(jr@hr),np.inf)/max(2*np.linalg.norm(hr,np.inf),1e-20)
                realerr=max(realerr,float(rr))
                samples.append(dict(background_index=i,p=kval,max_frozen_growth=float(np.max(ev.real)),
                                    eigenvector_condition=float(np.linalg.cond(vec)),eigen_residual=float(residual),
                                    frequencies=[[float(z.real),float(z.imag)] for z in (1j*ev)]))
    for name,value in [('all_saved_Hamilton_Euler_normalized',eqerr),('finite_control_eigen_residual',eigerr),
                       ('both_real_quadratures_symplectic',realerr)]:
        checks.add(name,np.isfinite(value) and value<=1e-10,value,'<=1e-10')
    checks.add('exact_positive_chart_K',min_kinetic>0,str(min_kinetic),'minimum exact eigenvalue >0; chart only')
    # Full Hamiltonian retains the indefinite spatial trace term. Completing
    # the momentum square gives energy -a^3 A/2 at y_dot=0.
    exact(checks,'retained_negative_trace_energy_coefficient',-Ap[0,0].coeff(p,2)/2+s.Rational(1,8))
    matrices={'A':A,'R':R,'K':K,'Hamiltonian':HH,'canonical_velocity_map':M,
              'unreduced_momentum_value':vol*C0,'unreduced_momentum_velocity':vol*C1,
              'SO2_A':Ap,'SO2_R':Rp,'SO2_K':Kp,'principal_pencil':pencil,'wave_companion':companion,
              'slow_A':AN,'slow_R':RN,'slow_K':KL,'slow_Q0':q0,'slow_Q1':q1}
    sy={**op.sy,'ell':ell,'p':p,'omega':w,'c':c,'sigma':sig,'I':s.I,'sqrt':s.sqrt}
    bundle={k:exports(v) for k,v in matrices.items()};loaded=json.loads(common.encode(bundle))
    for name,mat in matrices.items():exact(checks,'serialized_roundtrip_'+name,import_matrix(loaded[name],sy)-mat)
    checks.add('all_source_pins_after',common.inspect_pins(pins)==missing)
    checks.add('all_input_metadata_preserved',snapshot(paths)==before,{'files':len(before),'hash_size_mtime_ns':True})
    failed_binary=[q for q in common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_01/summary.json')['checks'] if not q['passed']]
    failed_ind=[q for q in common.read_json(BASE+'r4c1_g3n5_nonzero_principal_attempt_01/summary.json')['checks'] if not q['passed']]
    formulas=dict(momentum='p_y=a^3*(K*y_dot+R*y)',quadratic_Hamiltonian='1/2*(y,p_y)^dagger*HH*(y,p_y)',
                  mode_family='k=(ell,0,0), ell>0; integer ell on coordinate T3; negative conjugate included',
                  real_canonical_pairs_per_plus_minus_pair=20,complex_chart_coordinates=10,
                  scalar_principal_determinant=str(scalar_det),full_principal_determinant=str(full_det),
                  wave_scale_factor=str(wave),fast_scale_factor=str(fast),
                  wave_squared_speeds={'TT':'1 (two)','frame_transverse':'4/5 (two)',
                                      'matter_radial_and_r':'1 (two)','matter_phase':'1+(u0^2+v0^2)/13',
                                      'frame_scalar':'1/3','dust_slow':'0 (algebraic two, geometric one)'},
                  dispersive_branch='omega^2=(5/33)*p^4+subleading terms',
                  zero_Jordan_chain={'eigenvector':list(map(str,independent['zero'])),
                                     'generalized':list(map(str,independent['generalized']))},
                  formal_slow=dict(variable='Vx',A=str(afinal),R=str(rfinal),K=str(kfinal),
                                  E0=str(ef0),E1=str(ef1),E2=str(-kfinal),
                                  rescaling='h,du,dv,dr scaled by 1/p; Pi=i*psi_dot*Vx/p+chi/p^2; p_dot=-H*p',
                                  inverse_domain='diag(1/4,-G_matter,-1,-b), det G_matter=1+(u0^2+v0^2)/13>0; b=5/11',
                                  nonclaim='Formal asymptotic action; not a full finite-k canonical restriction or physical EFT ghost certificate'))
    diag=dict(samples=samples,background_order=list(old.BG_NAMES),canonical_matrix_residual=eqerr,
              finite_eigen_residual=eigerr,real_quadrature_residual=realerr,singular_ranks=ranks,
              preserved_binary64_failures=failed_binary,preserved_independent_v1_failures=failed_ind,
              adverse_disposition={'wave_principal_eigenvectors_complete':False,
                                   'zero_speed_Jordan_defect':True,'formal_slow_K':'-11/6',
                                   'complete_Hamiltonian_positive':False},
              nonclaims=['No physical cutoff/window or torus calibration','No all-direction strong hyperbolicity',
                         'No relativistic causality certificate','No full physical stability/ghost classification',
                         'No nonlinear source closure, healthy GR, G_eff/PPN or microscopic matching',
                         'Frozen instantaneous growth is not evolving-background stability'])
    payloads={'matrices.json':common.encode(bundle),'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag)}
    passed=sum(q['passed'] for q in checks.rows)
    summary=dict(schema='r4c1-g3n5-nonzero-characteristic-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
                 passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='CONDITIONAL_NONZERO_FAMILY_WITH_ZERO_SPEED_JORDAN_OBSTRUCTION',
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                 wave_principal_complete=False,formal_zero_speed_Jordan_defect=True,
                 formal_slow_time_coefficient='-11/6',physical_Hessian_verified=False,physical_EFT_cutoff_derived=False,
                 canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
                 source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=missing,
                 source_metadata_preserved=len(before),artifacts={k:common.sha(v) for k,v in payloads.items()},
                 runtime={'python':platform.python_version(),'sympy':s.__version__,'numpy':np.__version__},
                 review_dependencies=['B1/G3N4/full G3N5 kernel and constraints','Homogeneous energy and charge sectors',
                                      'All inherited review/physics debt'],
                 comparison_scope='Separate real-space derivation by same agent; no independent external reviewer')
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    payloads['summary.json']=common.encode(summary)
    return payloads,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_nonzero_characteristic_attempt_01')
    ap.add_argument('--replay');a=ap.parse_args()
    dest=(ROOT/(a.replay or a.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if not a.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if a.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    data,summary=calculate()
    if a.replay:
        for name,body in data.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():
                raise RuntimeError('Exact replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in data.items():
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if a.replay else 'NEW_RECEIPTS_WRITTEN',**{k:summary[k] for k in ('validation','passed','total','status','physics_pass','gate_effect')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
