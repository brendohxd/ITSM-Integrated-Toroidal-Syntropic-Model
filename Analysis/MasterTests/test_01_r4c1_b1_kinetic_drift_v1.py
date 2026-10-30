"""Background-dependent old B1 quadratic action and actual initial time drift.

No nonlinear window, vortical admission, or matching inference.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json'
PSHA='829b013edc716cb2a7c9a2a4161bf2830186b0d68673b8b57e3928deb5a1d53a'
SOURCE='Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_B1_KINETIC_DRIFT_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_B1_REDUCED_KINETIC_V1_REPORT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda v:(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def calculate():
    mp.mp.dps=100;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for q in entries if (v:=clean(q))!=0];check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=json.loads((ROOT/PARENT).read_bytes());assert parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name in (SELF,CONTRACT,REPORT):pins[name]=SHA((ROOT/name).read_bytes())
    snapshots={}
    for name,want in pins.items():
        f=ROOT/name;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,name
        for q in (f,sc):snapshots[q.relative_to(ROOT).as_posix()]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
    old=load('B1_quadratic_parent',SOURCE);par=old.parameters()
    backend=load('B1_drift_original_weak',old.BACKEND)
    weak=backend.WeakAction(old.original_body(True),par)
    a=s.Symbol('a',positive=True);H=s.Symbol('H',real=True);k=s.Symbol('k',nonzero=True,real=True)
    u,v,r,du,dv,dr,pp,P,rho=s.symbols('u v r du dv dr p psi rho',real=True)
    variables=(a,H,u,v,r,du,dv,dr,pp,P,rho)
    initial=dict(zip(variables,(1,s.sqrt(s.Rational(3469,4620)),1,0,1,0,1,s.Rational(1,4),s.Rational(1,5),0,s.Rational(1,5))))
    x=[old.Jet.var(i) for i in range(39)]
    q=[a*a,0,0,a*a,0,a*a,0,0,0,u,v,r,P,0,0,rho*s.exp(-4*par['beta']*P)]
    vv=[0]*16;dd=[0]*16
    for j in (0,3,5):vv[j]=2*H*a*a
    vv[9]=du;vv[10]=dv;vv[11]=dr;vv[12]=pp;vv[14]=s.exp(par['beta']*P)
    for i,j in enumerate(old.SLOTS):
        if i<3:
            q[j]+=a*a*x[i];vv[j]+=a*a*(x[11+i]+2*H*x[i]);dd[j]=a*a*x[22+i]
        elif i<6:
            q[j]+=x[i]/a;vv[j]+=(x[11+i]-H*x[i])/a;dd[j]=x[22+i]/a
        else:q[j]+=x[i];vv[j]+=x[11+i];dd[j]=x[22+i]
    NN=old.jexp(-par['beta']*x[9])
    jets=q+vv+dd+[z/a for z in x[33:36]]+[z/a for z in x[36:39]]+[NN,-par['beta']*NN*x[31]]
    density=weak.density(jets)[0]
    local=s.zeros(39)
    for (i,j),z in density.h.items():local[i,j]=local[j,i]=clean(z)
    check('general_quadratic_no_Float',not bool(local.atoms(s.Float)))
    T=s.zeros(39,25)
    for i in range(11):T[i,i]=1;T[11+i,11+i]=1;T[22+i,i]=s.I*k
    for i in range(3):T[33+i,22+i]=1;T[36+i,22+i]=s.I*k
    full=(T.conjugate().T*local*T).applyfunc(clean)
    zero('general_Fourier_Hermitian',full-full.conjugate().T)
    zero('general_Z_velocity_row_zero',full[21,:])
    keep=list(range(10))+list(range(11,21));elim=[10,22,23,24]
    A=full.extract(keep,keep);cross=full.extract(keep,elim);D=full.extract(elim,elim)
    zero('general_algebraic_block',D-s.diag(5*a**3/11,a*k**2/2,a*k**2/2,-a*k**2/15))
    zero('general_algebraic_determinant',D.det()+a**6*k**6/132)
    Dinv=s.diag(*[1/z for z in D.diagonal()]);solve=(-Dinv*cross.conjugate().T).applyfunc(clean)
    red=(A+cross*solve).applyfunc(clean)
    zero('general_eliminated_equations',D*solve+cross.conjugate().T)
    M=red[10:20,10:20];B=red[10:20,:10];Q=red[:10,:10]
    parse=lambda rows:s.Matrix([[s.sympify(z,locals={'H':H,'k':k}) for z in row] for row in rows])
    M0=parse(parent['formulas']['reduced_kinetic'])
    zero('general_positive_kinetic_volume_identity',M-a**3*M0)
    for name,mat,key in (('M',M,'reduced_kinetic'),('B',B,'reduced_velocity_field'),('Q',Q,'reduced_field_field')):
        zero('initial_parent_recovered_'+name,mat.subs(initial)-parse(parent['formulas'][key]).subs(initial))
    print('GENERAL_B1_QUADRATIC_REDUCTION_EXACT',flush=True)
    Mc=par['MP2']+par['MU2']*(par['c1']+par['c3']+3*par['c2'])/2
    ss=u*u+v*v
    mass=par['m2']+par['lambda4']*ss/2+par['lambda6']*ss**2/(4*par['Lambda']**2)+par['g_r']*r*r/2
    flow=s.Matrix([a*H,-(du*du+dv*dv+dr*dr+par['K_Q']*pp*pp+rho)/(2*Mc),
        du,dv,dr,-3*H*du-mass*u,-3*H*dv-mass*v,
        -3*H*dr-par['mr2']*r-par['lambda_r']*r**3-par['g_r']*ss*r/2,
        -3*H*pp-par['beta']*rho/par['K_Q'],pp,(-3*H+par['beta']*pp)*rho])
    potential=(par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)
               +par['mr2']*r*r/2+par['lambda_r']*r**4/4+par['g_r']*ss*r*r/4)
    energy=(du*du+dv*dv+dr*dr+par['K_Q']*pp*pp)/2+potential+rho
    deriv=lambda z:sum(s.diff(z,t)*f for t,f in zip(variables,flow))
    zero('actual_background_energy_drift',deriv(energy)+3*H*(du*du+dv*dv+dr*dr+par['K_Q']*pp*pp+rho))
    zero('actual_background_constraint_preservation',deriv(3*Mc*H*H-energy))
    Md=(3*H*M).applyfunc(clean)
    zero('moving_volume_derivative',M.applyfunc(deriv)-Md)
    Bd=B.applyfunc(deriv).applyfunc(clean)
    mini=lambda mat:mat.subs(initial).applyfunc(clean)
    mi,bi,qi,mdi,bdi=map(mini,(M,B,Q,Md,Bd))
    friction=mdi+bi-bi.conjugate().T;restoring=bdi-qi
    generator=s.zeros(20);generator[:10,10:20]=s.eye(10)
    generator[10:20,:10]=-mi.inv()*restoring;generator[10:20,10:20]=-mi.inv()*friction
    generator=generator.applyfunc(clean)
    Omega=(bi-bi.conjugate().T).row_join(mi).col_join((-mi).row_join(s.zeros(10)))
    Omegad=(bdi-bdi.conjugate().T).row_join(mdi).col_join((-mdi).row_join(s.zeros(10)))
    zero('actual_time_dependent_symplectic_transport',Omegad+generator.conjugate().T*Omega+Omega*generator)
    C=s.eye(20);C[10:20,:10]=bi;C[10:20,10:20]=mi
    Cd=s.zeros(20);Cd[10:20,:10]=bdi;Cd[10:20,10:20]=mdi
    J=s.zeros(20);J[:10,10:20]=s.eye(10);J[10:20,:10]=-s.eye(10)
    zero('actual_time_derivative_of_canonical_pullback',Omegad-Cd.conjugate().T*J*C-C.conjugate().T*J*Cd)
    wrong=generator.copy();wrong[10:20,:10]+=mi.inv()*bdi;wrong[10:20,10:20]+=mi.inv()*mdi
    missing=(Omegad+wrong.conjugate().T*Omega+Omega*wrong).applyfunc(clean)
    check('frozen_drift_omission_rejected',any(z!=0 for z in missing),sum(z!=0 for z in missing))
    zero('general_volume_positive_pivot_factor',M.det()-a**30*mi.det())
    print('BACKGROUND_DRIFT_AND_SYMPLECTIC_TRANSPORT_EXACT',flush=True)
    # Independent numerical differentiation of generated general matrices at fixed comoving k.
    args=list(variables)+[k];func=s.lambdify(args,B,modules='mpmath')
    convert=lambda z:mp.mpf(str(s.N(z,98)))
    vals=[convert(initial[t]) for t in variables];fd=[convert(z) for z in flow.subs(initial)]
    controls=[]
    for kval in (1,7,40):
        target=s.lambdify(k,bdi,modules='mpmath')(kval);errors=[]
        for hs in ('1e-12','1e-18'):
            hh=mp.mpf(hs)
            plus=func(*[v0+hh*f for v0,f in zip(vals,fd)],kval)
            minus=func(*[v0-hh*f for v0,f in zip(vals,fd)],kval)
            observed=(plus-minus)/(2*hh);error=max(abs(z) for z in observed-target)/(1+max(abs(z) for z in target))
            check(f'actual_tangent_B_drift_k{kval}_{hs}',error<100*hh**2,mp.nstr(error,65));errors.append(error)
        check(f'tangent_drift_convergence_k{kval}',errors[1]<errors[0]/mp.mpf('1e8'))
        controls.append(dict(k=kval,normalized_errors=[mp.nstr(z,65) for z in errors]))
    for name,(digest,mtime) in snapshots.items():
        path=ROOT/name;assert SHA(path.read_bytes())==digest and path.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    encode=lambda mat:[[str(clean(v)) for v in row] for row in mat.tolist()]
    return dict(kind='R4C1_B1_KINETIC_DRIFT_V1',passed=sum(z['passed'] for z in checks),total=len(checks),
        checks=checks,source_sha256=pins,independent_controls=controls,
        formulas=dict(background_order=[str(z) for z in variables],background_flow=[str(clean(z)) for z in flow],
            initial={str(z):str(initial[z]) for z in variables},fixed_comoving_k=True,
            constraint_block=encode(D),constraint_solution=encode(solve),M=encode(M),B=encode(B),Q=encode(Q),
            M_dot=encode(Md),B_dot=encode(Bd),initial_generator=encode(generator),
            initial_B_dot=encode(bdi),initial_M_dot=encode(mdi),
            equation='M*qdd+(M_dot+B-B^dagger)*qdot+(B_dot-Q)*q=0',
            two_form_transport='Omega_dot+G^dagger*Omega+Omega*G=0',kinetic_inertia='(10,0,0) for a>0'),
        interval_kinetic_signature='positive along the old homogeneous B1 background; no full stability theorem',
        controlled_perturbation_evolution=False,physical_window_demonstrated=False,nodal_G1_admitted=False,
        physics_pass=False,gate_effect='NONE',review='DEFERRED',G1='INCOMPLETE',G2='INCOMPLETE',G3='INCOMPLETE',
        G4='INCOMPLETE',G5='INCOMPLETE',G6='INCOMPLETE',MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--out');g.add_argument('--replay');args=parser.parse_args()
    if args.out and (ROOT/args.out).exists():raise FileExistsError(args.out)
    result=calculate();data=ENC(result)
    if args.replay:
        target=ROOT/args.replay;assert target.read_bytes()==data,'immutable replay mismatch'
        assert Path(str(target)+'.sha256').read_text().split()[0]==SHA(data);print('IMMUTABLE_REPLAY_EXACT',flush=True)
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);path=out/'summary.json'
        path.write_bytes(data);Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','interval_kinetic_signature','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
