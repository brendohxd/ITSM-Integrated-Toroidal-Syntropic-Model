"""G3I: exact constrained-frame vertices and finite-angle probe scattering.

Metric frozen. No full finite-density cutoff/domain or healthy-GR claim.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
    'Theory/Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_CONTRACT_2026-10-08.md':'f54c7a7297350256ae199c3ba2b5f19266094c57739b95c6dad0ee253627d5f8',
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
    'Theory/Gates/ITSM_MASTER_TESTS_01_03_REQUIREMENT_DISPOSITION_2026-09-30.md':'9ccd38b3c1d20670c759488ce6f4ecd865355090733359cd506d7b01fd3c9ac3',
    'Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_CONTRACT_2026-09-30.md':'4bb989979850468d4322baeec9cbdaaaadd8318825724042711c062fc944e9f8',
    'Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md':'1b9fbc4185b61d1e37d7865baa811994e235523eb9ecc22432c733b4bc38aa04',
    'Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_DENSITY_REPORT_2026-10-08.md':'a247893f8f0cb15760c20cc24b4f19b91f701ce2aaa0ec585a534b3436b78d13',
    'Analysis/MasterTests/outputs/r4c1_g3df_attempt_01/summary.json':'877b6f630a6692965656005fc823a2141b21daac4d32461f77e28dd12905a5a3',
    'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json':'930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75',
    'Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy':'b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506',
    'Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_DOMAIN_PREFLIGHT_REPORT_2026-09-29.md':'2f151504d695ee442585653982cbbabfca2f520e864a802de306c0b013f3abc4',
}
ETAS=(1.,.25,.0625,.015625,.00390625,.0009765625)
COSINES=(s.Rational(1,2),s.Integer(0),-s.Rational(1,2))
MOMENTA=(.01,.1,1.,20.,40.,80.)
G3=s.Matrix([s.Rational(1,5),-s.Rational(7,48),-s.Rational(1,80),s.Rational(1,20)])

def sha(data):return hashlib.sha256(data).hexdigest()
def encode(data):return (json.dumps(data,indent=2,allow_nan=False)+'\n').encode()
def tidy(expr):
    if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))
def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:
            raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: '+name)
class Audit:
    def __init__(self):self.checks=[]
    def test(self,name,ok,value=None,criterion=None):
        self.checks.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def exact(self,name,expr):
        vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        vals=[tidy(v) for v in vals]
        self.test(name,all(v==0 for v in vals),'zero_exact' if all(v==0 for v in vals) else list(map(str,vals)))

def derive(audit):
    ep=s.Symbol('epsilon',real=True)
    MU2,f,p,MP,eta=s.symbols('MU2 f p M_P eta',positive=True)
    cs=s.symbols('c1 c2 c3 c4',real=True);c1,c2,c3,c4=cs;c14=c1+c4;c123=c1+c2+c3
    v=s.Matrix(s.symbols('vx vy vz',real=True))
    dv=s.Matrix(4,3,s.symbols('vt0:3 vx0:3 vy0:3 vz0:3',real=True))
    norm=(v.T*v)[0];sigma=s.sqrt(1+ep**2*norm)
    U=s.Matrix([sigma,*list(ep*v)])
    F=s.Matrix(4,4,lambda mu,nu:ep**2*(v.T*dv.row(mu).T)[0]/sigma if nu==0 else ep*dv[mu,nu-1])
    metric=s.diag(-1,1,1,1)
    audit.exact('exact_future_unit_constraint',(U.T*metric*U)[0]+1)
    for mu in range(4):
        audit.exact('differentiated_unit_constraint_'+str(mu),(U.T*metric*F.row(mu).T)[0])
    # Extract the exact unit chart coefficients without expanding discarded orders.
    Fc={d:F.applyfunc(lambda value:s.expand(s.series(value,ep,0,5).removeO()).coeff(ep,d)) for d in (1,2,4)}
    Uc={d:U.applyfunc(lambda value:s.expand(s.series(value,ep,0,5).removeO()).coeff(ep,d)) for d in (0,1,2,4)}
    Ac={d:sum((Fc[j].T*Uc[i] for i in Uc for j in Fc if i+j==d),s.zeros(4,1)) for d in (1,2,3)}
    invariant={j:{d:s.Integer(0) for d in (2,3,4)} for j in (1,2,3,4)}
    signs=(-1,1,1,1)
    for d in (2,3,4):
        for i in Fc:
            for j in Fc:
                if i+j!=d:continue
                invariant[1][d]+=sum(signs[mu]*signs[nu]*Fc[i][mu,nu]*Fc[j][mu,nu] for mu in range(4) for nu in range(4))
                invariant[2][d]+=s.trace(Fc[i])*s.trace(Fc[j])
                invariant[3][d]+=s.trace(Fc[i]*Fc[j])
        invariant[4][d]=sum(((Ac[i].T*metric*Ac[j])[0] for i in Ac for j in Ac if i+j==d),s.Integer(0))
    L={d:s.expand(-MU2*(c1*invariant[1][d]+c2*invariant[2][d]+c3*invariant[3][d]-c4*invariant[4][d])/2) for d in (2,3,4)}
    div=sum(dv[i+1,i] for i in range(3));vt=dv.row(0).T
    adv=s.Matrix([sum(v[j]*dv[j+1,i] for j in range(3)) for i in range(3)])
    ivt=(v.T*vt)[0]
    expect2=MU2*(c14*(vt.T*vt)[0]-c1*sum(dv[i,j]**2 for i in range(1,4) for j in range(3))-c2*div**2-c3*sum(dv[i+1,j]*dv[j+1,i] for i in range(3) for j in range(3)))/2
    expect3=-MU2*(c2*div*ivt+c3*sum(vt[i]*(v.T*dv.row(i+1).T)[0] for i in range(3))-c4*(vt.T*adv)[0])
    expect4=MU2*(-(c123+c4)*ivt**2+c1*sum((v.T*dv.row(i).T)[0]**2 for i in range(1,4))+c4*(norm*(vt.T*vt)[0]+(adv.T*adv)[0]))/2
    for d,expected in ((2,expect2),(3,expect3),(4,expect4)):
        audit.exact('direct_covariant_order_'+str(d),L[d]-expected)
    scaling={value:value/f for value in list(v)+list(dv)}
    canonical={d:s.expand(L[d].subs(scaling,simultaneous=True).subs(MU2,f**2/c14)) for d in L}
    # Independent quadratic plane-wave kernel from coefficient extraction.
    omega=s.Symbol('omega',real=True);k=s.Matrix(s.symbols('kx ky kz',real=True))
    aa=s.Matrix(s.symbols('a0:3'));bb=s.Matrix(s.symbols('b0:3'))
    def substitute_fields(expr,fields,derivatives):
        return s.expand(expr.subs(dict(zip(list(v)+list(dv),list(fields)+list(derivatives))),simultaneous=True))
    qfields=aa+bb
    qderiv=s.Matrix(4,3,lambda mu,nu:-s.I*omega*(aa[nu]-bb[nu]) if mu==0 else s.I*k[mu-1]*(aa[nu]-bb[nu]))
    quadratic=substitute_fields(canonical[2],qfields,qderiv)
    kernel=s.Matrix(3,3,lambda i,j:tidy(quadratic.coeff(aa[i]).coeff(bb[j])))
    kt=(k.T*k)[0];ct2=c1/c14;cl2=c123/c14
    expected_kernel=(omega**2-ct2*kt)*s.eye(3)+(ct2-cl2)*k*k.T
    audit.exact('derived_quadratic_propagator_kernel',kernel-expected_kernel)
    Pl=k*k.T/kt;Pt=s.eye(3)-Pl
    prop=Pt/(omega**2-ct2*kt)+Pl/(omega**2-cl2*kt)
    audit.exact('propagator_inverse',kernel*prop-s.eye(3))
    csub=dict(zip(cs,list(G3)))
    audit.exact('G3_transverse_probe_speed',ct2.subs(csub)-s.Rational(4,5))
    audit.exact('G3_longitudinal_probe_speed',cl2.subs(csub)-s.Rational(1,6))
    audit.exact('G3_canonical_frame_scale',(MU2*c14).subs(csub).subs(MU2,2*eta*MP**2/3)-eta*MP**2/6)
    audit.test('positive_probe_kinetic_and_speeds',ct2.subs(csub)>0 and cl2.subs(csub)>0 and c14.subs(csub)>0)

    amps=s.symbols('amp0:4');ws=s.symbols('omega0:4',real=True)
    ps=[s.Matrix([s.Symbol('kx'+str(i),real=True),0,s.Symbol('kz'+str(i),real=True)]) for i in range(4)]
    wave_y=sum(amps);deriv_y=s.Matrix([-s.I*sum(ws[j]*amps[j] for j in range(4)),*[
        s.I*sum(ps[j][i]*amps[j] for j in range(4)) for i in range(3)]])
    fields=s.Matrix([0,wave_y,0]);derivatives=s.zeros(4,3);derivatives[:,1]=deriv_y
    quartic=substitute_fields(canonical[4],fields,derivatives)
    G4=quartic
    for amp in amps:G4=G4.coeff(amp)
    G4=tidy(G4)
    expectedG4=-4*sum((-c123/(2*c14*f**2))*ws[i]*ws[j]+c1/(2*c14*f**2)*(ps[i].T*ps[j])[0] for i in range(4) for j in range(i+1,4))
    audit.exact('four_distinct_wave_contact_vertex',G4-expectedG4)
    a,b,h=s.symbols('ampA ampB ampInternal')
    om1,om2,om3=s.symbols('w1 w2 w3',real=True)
    p1=s.Matrix([s.Symbol('p1x',real=True),0,s.Symbol('p1z',real=True)])
    p2=s.Matrix([s.Symbol('p2x',real=True),0,s.Symbol('p2z',real=True)])
    p3=s.Matrix([s.Symbol('p3x',real=True),0,s.Symbol('p3z',real=True)])
    cubic=[]
    for polarization in range(3):
        field=s.Matrix([h if i==polarization else 0 for i in range(3)])
        field[1]+=a+b
        deriv=s.Matrix(4,3,lambda mu,nu:
            (-s.I*om3*h if mu==0 else s.I*p3[mu-1]*h) if nu==polarization else 0)
        deriv[:,1]+=s.Matrix([-s.I*(om1*a+om2*b),*[s.I*(p1[i]*a+p2[i]*b) for i in range(3)]])
        expr=substitute_fields(canonical[3],field,deriv).coeff(a).coeff(b).coeff(h)
        cubic.append(tidy(expr.subs({om3:-om1-om2,p3[0]:-p1[0]-p2[0],p3[2]:-p1[2]-p2[2]},simultaneous=True)))
    G3vertex=s.Matrix(cubic)
    expectedG3=((c2+c3)*(om1+om2)*(p1+p2)+c4*(om1*p2+om2*p1))/(c14*f)
    audit.exact('derived_all_polarization_cubic_vertex',G3vertex-expectedG3)
    audit.exact('internal_y_vertex_vanishes_for_planar_kinematics',G3vertex[1])
    audit.test('frozen_U0_nonlinearity_omission_rejected',tidy(L[4]-MU2*c4*(adv.T*adv)[0]/2)!=0)
    audit.test('acceleration_interaction_omission_rejected',tidy(canonical[3]-canonical[3].subs(c4,0))!=0)

    x=s.Symbol('cos_theta',real=True)
    def scattering(coefficients):
        cT=tidy(ct2.subs(coefficients));cL=tidy(cl2.subs(coefficients))
        E=s.sqrt(cT)*p;root=s.sqrt(1-x**2)
        momenta=[s.Matrix([0,0,p]),s.Matrix([0,0,-p]),s.Matrix([-p*root,0,-p*x]),s.Matrix([p*root,0,p*x])]
        energies=[E,E,-E,-E]
        audit.exact('COM_momentum_conservation_'+str(coefficients),sum(momenta,s.zeros(3,1)))
        audit.exact('COM_energy_conservation_'+str(coefficients),sum(energies))
        for i in range(4):
            audit.exact('external_mass_shell_'+str(coefficients)+'_'+str(i),energies[i]**2-cT*(momenta[i].T*momenta[i])[0])
        subs4={ws[i]:energies[i] for i in range(4)}
        subs4.update({ps[i][j]:momenta[i][j] for i in range(4) for j in (0,2)})
        contact=tidy(G4.subs(coefficients).subs(subs4,simultaneous=True))
        def vertex(i,j):
            dic={om1:energies[i],om2:energies[j]}
            dic.update({p1[a]:momenta[i][a] for a in (0,2)})
            dic.update({p2[a]:momenta[j][a] for a in (0,2)})
            return tidy(G3vertex.subs(coefficients).subs(dic,simultaneous=True))
        exchanged={}
        for name,left,right in [('s',(0,1),(2,3)),('t',(0,2),(1,3)),('u',(0,3),(1,2))]:
            gleft,gright=vertex(*left),vertex(*right)
            q=momenta[left[0]]+momenta[left[1]];frequency=energies[left[0]]+energies[left[1]]
            q2=tidy((q.T*q)[0])
            if q2==0:
                if frequency==0:raise RuntimeError('UNREGISTERED_ZERO_PROPAGATOR')
                propagator=s.eye(3)/frequency**2
            else:
                longitudinal=q*q.T/q2
                propagator=(s.eye(3)-longitudinal)/(frequency**2-cT*q2)+longitudinal/(frequency**2-cL*q2)
            audit.exact('exchange_vertex_transverse_'+str(coefficients)+'_'+name,(gleft.T*q)[0])
            exchanged[name]=tidy(-(gleft.T*propagator*gright)[0])
        return contact,exchanged,tidy(contact+sum(exchanged.values()))
    contact,exchange,total=scattering(csub)
    lorentz={c2:0,c3:0,c4:0}
    control=scattering(lorentz)
    audit.exact('redundant_identical_polarization_Lorentz_control',control[2])
    audit.test('control_off_shell_quartic_not_zero',canonical[4].subs(lorentz)!=0)
    audit.exact('COM_s_exchange_zero',exchange['s'])
    audit.exact('Bose_angle_crossing',total.subs(x,-x)-total)
    audit.test('exchange_omission_detected',tidy(total-contact)!=0)
    audit.test('wrong_exchange_sign_detected',tidy(total-(contact-sum(exchange.values())))!=0)
    total_eta=tidy(total.subs(f,s.sqrt(eta*MP**2/6)))
    ninety=tidy(total_eta.subs(x,0))
    audit.exact('planned_ninety_degree_comparator',ninety-s.Rational(388,25)*p**2/(eta*MP**2))
    audit.exact('fixed_angle_eta_homogeneity',s.diff(total_eta,eta)*eta+total_eta)
    audit.exact('momentum_degree_two',s.diff(total_eta,p)*p-2*total_eta)
    scale=tidy(s.solve(ninety-1,p)[0])
    audit.exact('probe_amplitude_one_scale',scale**2-25*eta*MP**2/388)
    audit.test('fixed_p_eta_endpoint_divergence',s.limit(ninety,eta,0,dir='+')==s.oo)
    invariant_force=tidy((s.Rational(2,7)*eta**s.Rational(3,2))/(3*eta)**s.Rational(3,2))
    audit.exact('force_invariant_stays_finite',invariant_force-2*s.sqrt(3)/63)
    formulas={str(d):str(tidy(L[d])) for d in L}
    formulas.update(canonical={str(d):str(tidy(canonical[d])) for d in canonical},
        quadratic_kernel=[[str(v) for v in row] for row in kernel.tolist()],cubic_WWV=[[str(v) for v in row] for row in G3vertex.tolist()],
        quartic_WWWW=str(G4),transverse_probe_speed_squared=str(ct2),
        longitudinal_probe_speed_squared=str(cl2),canonical_scale_squared='eta*M_P**2/6',
        probe_contact=str(contact),probe_exchange={key:str(value) for key,value in exchange.items()},
        probe_total=str(total),probe_total_eta=str(total_eta),ninety_degree_amplitude=str(ninety),
        ninety_degree_amplitude_one_scale=str(scale),lorentz_control_total=str(control[2]),
        dimension={'p':1,'M_P':1,'f':1,'amplitude':0},
        scope='Fixed-Minkowski-metric unit-frame probe, not coupled finite-density scattering')
    return dict(p=p,x=x,eta=eta,MP=MP,f=f,contact=contact,exchange=exchange,total=total_eta,scale=scale),formulas

def numerical(audit,d):
    family=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())
    old=np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
    audit.test('all_six_frozen_eta_members',tuple(v['eta'] for v in family['family'])==ETAS)
    rows=[];max_error=0.
    total=s.lambdify((d['eta'],d['p'],d['x'],d['MP']),d['total'],'numpy',cse=True)
    for ie,eta in enumerate(ETAS):
        params=family['family'][ie]['parameters']
        coefficient_error=max(abs(params[key]-float(value)) for key,value in zip(('c1','c2','c3','c4'),G3))
        audit.test(f'eta_{eta}_frozen_frame_coefficients',coefficient_error<=1e-15,coefficient_error)
        audit.test(f'eta_{eta}_canonical_scale_match',abs(params['MU2']*(params['c1']+params['c4'])-eta/6)<=1e-15)
        f=np.sqrt(eta/6)
        for x in COSINES:
            for p in MOMENTA:
                replacements={d['f']:f,d['p']:p,d['x']:x}
                contact=float(d['contact'].subs(replacements))
                exchanged={key:float(value.subs(replacements)) for key,value in d['exchange'].items()}
                assembled=contact+sum(exchanged.values())
                expected=float(total(eta,p,float(x),1.))
                err=abs(assembled-expected)/(1+abs(expected));max_error=max(max_error,err)
                label=f'eta_{eta}_cos_{float(x)}_p_{p}'
                audit.test(label+'_exact_numeric_amplitude',err<=1e-12,err,'<=1e-12 normalized')
                rows.append(dict(eta=eta,cos_theta=float(x),p_over_MP=p,contact=contact,
                    exchange=exchanged,total=assembled,probe_amplitude_le_one=abs(assembled)<=1,
                    weak_classification_scope='ORDER_ONE_FIXED_ANGLE_PROBE_ONLY',
                    normalized_symbolic_agreement=err))
    audit.test('full_108_amplitude_grid_exported',len(rows)==108)
    for x in COSINES:
        for p in MOMENTA:
            pair=[v['total'] for v in rows if v['cos_theta']==float(x) and v['p_over_MP']==p]
            errs=[abs(b/a-4) for a,b in zip(pair,pair[1:])]
            audit.test(f'cos_{float(x)}_p_{p}_eta_refinement_amplitude_scaling',max(errs)<=1e-12,max(errs))
    for eta in ETAS:
        for x in COSINES:
            values={v['p_over_MP']:v['total'] for v in rows if v['eta']==eta and v['cos_theta']==float(x)}
            ratios=[abs(values[b]/values[a]-4) for a,b in ((20.,40.),(40.,80.))]
            audit.test(f'eta_{eta}_cos_{float(x)}_momentum_doubling',max(ratios)<=1e-12,max(ratios))
    scales=[dict(eta=eta,f_over_MP=float(np.sqrt(eta/6)),p_probe_90_over_MP=float(d['scale'].subs({d['eta']:eta,d['MP']:1}))) for eta in ETAS]
    background=[]
    for ie,eta in enumerate(ETAS[:3]):
        for im,method in enumerate(family['trajectory']['methods']):
            tr=old[ie,im,:,0:201:2]
            audit.test(f'eta_{eta}_{method}_background_grid',len(tr[0])==101 and np.allclose(tr[0],np.linspace(0.,1.,101),rtol=0,atol=1e-15))
            a,H=tr[1],tr[2];limit=scales[ie]['p_probe_90_over_MP']
            audit.test(f'eta_{eta}_{method}_background_domain',bool(np.all(a>0) and np.all(H>0)))
            background.append(dict(eta=eta,method=method,p_probe_90_over_H_range=[float((limit/H).min()),float((limit/H).max())],
                conditional_ten_H_to_probe_interval_samples=int(np.count_nonzero(10*H<=limit)),
                inference_scope='VACUUM_PROBE_SCREEN_NOT_PHYSICAL_BACKGROUND_DOMAIN'))
            for k in (20.,40.,80.):
                p=k/a
                background.append(dict(eta=eta,method=method,k=k,p_over_H_range=[float((p/H).min()),float((p/H).max())],
                    p_over_probe_range=[float((p/limit).min()),float((p/limit).max())],
                    joint_probe_weak_and_p_ge_ten_H_samples=int(np.count_nonzero((p>=10*H)&(p<=limit))),
                    sampled_points=101,inference_scope='VACUUM_PROBE_SCREEN_NOT_PHYSICAL_BACKGROUND_DOMAIN'))
    return dict(amplitude_rows=rows,scales=scales,background_screen=background,max_symbolic_numeric_error=max_error)

def evaluate():
    verify(PINS)
    previous=json.loads((OUT/'r4c1_g3df_attempt_01/summary.json').read_bytes())
    inherited={**previous['source_sha256'],**previous['transitive_source_sha256']};verify(inherited)
    audit=Audit();data,formulas=derive(audit);numbers=numerical(audit,data)
    payloads={'formulas.json':encode(formulas),'grid.json':encode(numbers)}
    passed=sum(c['passed'] for c in audit.checks)
    result=dict(schema='r4c1-g3i-v1',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,
        transitive_source_sha256=inherited,script_sha256=sha(Path(__file__).read_bytes()),
        artifacts={name:sha(value) for name,value in payloads.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        numerical_summary=dict(amplitude_events=len(numbers['amplitude_rows']),max_numeric_error=numbers['max_symbolic_numeric_error'],
            scales=numbers['scales'],background_screen=numbers['background_screen']),
        status='CONDITIONAL_FRAME_PROBE_INTERACTION_SCALE_COLLAPSES_FULL_CUTOFF_OPEN' if passed==len(audit.checks) else 'FRAME_SCATTERING_FAILURES_REQUIRE_DISPOSITION',
        metric_perturbations='FROZEN_PROBE',finite_density_coupled_scattering_verified=False,
        probe_partial_wave_unitarity_verified=False,physical_EFT_cutoff='NOT_DERIVED',
        physical_validity_window_verified=False,full_loop_expansion_verified=False,
        healthy_continuous_full_GR_limit_verified=False,all_paths_no_go=False,
        physics_pass=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        Rule9_cleared=False,review_status='DEFERRED',gate_effect='NONE',
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
    return result,payloads

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3i_attempt_01')
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError('OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT')
    result,payloads=evaluate();payloads['summary.json']=encode(result)
    identical=None
    if args.replay:
        identical=all((directory/name).read_bytes()==value for name,value in payloads.items())
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,value in payloads.items():
            (directory/name).write_bytes(value)
            (directory/(name+'.sha256')).write_text(sha(value)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('validation','passed','total','status','physics_pass')}))
    for check in result['checks']:
        if not check['passed']:print(json.dumps(check))
    if args.replay and not identical:return 2
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':raise SystemExit(main())
