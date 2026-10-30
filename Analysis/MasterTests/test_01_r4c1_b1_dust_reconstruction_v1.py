"""Original lapse-flux dust reconstruction and the full homogeneous B1 clock identity.

Prerequisite to a propagator certificate; not a new state or nonlinear admission.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json'
PSHA='e66aaa83814afb726ace2bbaf1543591ba6502c37440be4430aca2ad7375c3cb'
SOURCE='Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_B1_DUST_RECONSTRUCTION_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_B1_KINETIC_DRIFT_V1_REPORT_2026-10-29.md'
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
        for z in (f,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    old=load('B1_dust_quadratic_parent',SOURCE);par=old.parameters()
    backend=load('B1_dust_original_weak',old.BACKEND)
    a=s.Symbol('a',positive=True);H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    u,v,r,du,dv,dr,pp,P,rho=s.symbols('u v r du dv dr p psi rho',real=True)
    variables=(a,H,u,v,r,du,dv,dr,pp,P,rho)
    initial=dict(zip(variables,(1,s.sqrt(s.Rational(3469,4620)),1,0,1,0,1,s.Rational(1,4),s.Rational(1,5),0,s.Rational(1,5))))
    locals_={str(z):z for z in variables+(k,)}
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=locals_) for z in row] for row in rows])
    f=parent['formulas'];M,B,Q,Bd,Md=map(lambda key:parse(f[key]),('M','B','Q','B_dot','M_dot'))
    solve=parse(f['constraint_solution'])
    flow=s.Matrix([s.sympify(z,locals=locals_) for z in f['background_flow']])
    deriv=lambda z:sum(s.diff(z,t)*v0 for t,v0 in zip(variables,flow))
    def state(x,aa,hh,uu,vv0,rr,ud,vd,rd,p0,P0,rhom,pa,exp):
        q=[aa*aa,0,0,aa*aa,0,aa*aa,0,0,0,uu,vv0,rr,P0,0,0,
           (rhom+x[41])*exp(-4*pa['beta']*P0)]
        vel=[0]*16;dz=[0]*16
        for j in (0,3,5):vel[j]=2*hh*aa*aa
        vel[9]=ud;vel[10]=vd;vel[11]=rd;vel[12]=p0;vel[14]=exp(pa['beta']*P0)
        for i,j in enumerate(old.SLOTS):
            if i<3:q[j]+=aa*aa*x[i];vel[j]+=aa*aa*(x[11+i]+2*hh*x[i]);dz[j]=aa*aa*x[22+i]
            elif i<6:q[j]+=x[i]/aa;vel[j]+=(x[11+i]-hh*x[i])/aa;dz[j]=x[22+i]/aa
            else:q[j]+=x[i];vel[j]+=x[11+i];dz[j]=x[22+i]
        return q+vel+dz+[z/aa for z in x[33:36]]+[z/aa for z in x[36:39]]+[1+x[39],x[40]]
    weak=backend.WeakAction(old.original_body(True),par)
    x=[old.Jet.var(i) for i in range(42)]
    result=weak.density(state(x,*variables,par,old.jexp))[0]
    local=s.zeros(42)
    for (i,j),z in result.h.items():local[i,j]=local[j,i]=clean(z)
    check('independent_lapse_quadratic_no_Float',not bool(local.atoms(s.Float)))
    zero('independent_lapse_Hessian_symmetric',local-local.T)
    T=s.zeros(42,26)
    for i in range(11):T[i,i]=1;T[11+i,11+i]=1;T[22+i,i]=s.I*k
    for i in range(3):T[33+i,22+i]=1;T[36+i,22+i]=s.I*k
    T[39,9]=-par['beta'];T[40,9]=-s.I*k*par['beta'];T[41,25]=1
    # Form E_N BEFORE clock substitution, including the actual Euler flux.
    lapse=(local[39,:]*T).applyfunc(clean)
    flux=(-s.I*k*local[40,:]*T).applyfunc(clean)
    total=(lapse+flux).applyfunc(clean)
    zero('density_pair_coefficient',total[0,25]+a**3)
    pull=s.zeros(26,20);keep=list(range(10))+list(range(11,21));elim=[10,22,23,24]
    for i,j in enumerate(keep):pull[j,i]=1
    for i,j in enumerate(elim):pull[j,:]=solve[i,:]
    epsi=s.zeros(1,20);epsi[0,9]=1
    trace=s.zeros(1,20);trace[0,0]=trace[0,2]=1
    Erho=(total*pull/a**3).applyfunc(clean)
    rrho=(Erho+4*par['beta']*rho*epsi).applyfunc(clean)
    noflux=(lapse*pull/a**3+4*par['beta']*rho*epsi).applyfunc(clean)
    flux_density=(rrho-noflux).applyfunc(clean)
    check('lapse_flux_not_discardable',any(z!=0 for z in flux_density),[str(z) for z in flux_density])
    generator=s.zeros(20);generator[:10,10:20]=s.eye(10)
    generator[10:20,:10]=-M.inv()*(Bd-Q)
    generator[10:20,10:20]=-M.inv()*(Md+B-B.conjugate().T)
    generator=generator.applyfunc(clean)
    clock=(rrho-par['beta']*rho*epsi+rho*trace/2).applyfunc(clean)
    current=(-s.I*k*rho*solve[3,:]/a).applyfunc(clean)
    ward=(clock.applyfunc(deriv)+clock*generator+(3*H-par['beta']*pp)*clock+current).applyfunc(clean)
    zero('full_clock_conservation_initial',ward.subs(initial))
    # Test the exact on-shell ideal, without inserting a numerical Friedmann root.
    ss=u*u+v*v
    potential=ss/2+ss**2/24+ss**3/480+r*r+r**4/28+3*ss*r*r/28
    energy=(du*du+dv*dv+dr*dr+3*pp*pp)/2+potential+rho
    fried=3*s.Rational(11,10)*H*H-energy
    quot=[];remainders=[]
    for z in ward:
        num,den=s.fraction(clean(z));quo,rem=s.div(num,fried,H)
        quot.append(clean(quo/den));remainders.append(clean(rem/den))
    zero('full_clock_conservation_mod_background_constraint',s.Matrix(remainders))
    check('off_shell_vs_on_shell_status_decided',all(z==0 for z in remainders))
    wrong=(noflux-par['beta']*rho*epsi+rho*trace/2).applyfunc(clean)
    wrongward=(wrong.applyfunc(deriv)+wrong*generator+(3*H-par['beta']*pp)*wrong+current).subs(initial).applyfunc(clean)
    check('omitted_lapse_flux_rejected',any(z!=0 for z in wrongward),sum(z!=0 for z in wrongward))
    # Constraint reconstruction solves the complete local lapse row exactly.
    recover=pull.copy();recover[25,:]=Erho
    zero('complete_lapse_equation_reconstructed',total*recover)
    check('density_reconstruction_uses_velocities',any(rrho[0,j]!=0 for j in range(10,20)))
    print('ORIGINAL_LAPSE_FLUX_AND_CLOCK_CONSERVATION',flush=True)
    physical_par={n:mp.mpf(str(z.p))/int(z.q) for n,z in par.items()}
    physical=backend.WeakAction(old.original_body(False),physical_par)
    vals=[mp.mpf(str(s.N(initial[z],98))) for z in variables]
    controls=[]
    for seed in (1,2):
        direction=s.Matrix([s.Rational(((j+1)*(seed+3))%13-6,17+seed) for j in range(42)])
        dirnum=[mp.mpf(str(z.p))/int(z.q) for z in direction]
        for row in (39,40):
            target=clean((local[row,:]*direction)[0]).subs(initial).evalf(98);target=mp.mpf(str(target))
            errors=[]
            for hs in ('1e-12','1e-16'):
                step=mp.mpf(hs);answer=mp.mpf(0)
                for sd in (-1,1):
                    for sn in (-1,1):
                        xx=[sd*step*z for z in dirnum];xx[row]+=sn*step
                        answer+=sd*sn*physical.density(state(xx,*vals,physical_par,mp.exp))[0]
                observed=answer/(4*step**2);error=abs(observed-target)/(1+abs(target))
                check(f'original_physical_lapse_second_variation_{seed}_{row}_{hs}',error<100*step,mp.nstr(error,65));errors.append(error)
            controls.append(dict(seed=seed,row=row,normalized_errors=[mp.nstr(z,65) for z in errors]))
    for name,(digest,mtime) in snapshots.items():
        path=ROOT/name;assert SHA(path.read_bytes())==digest and path.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    encode=lambda mat:[[str(clean(z)) for z in row] for row in mat.tolist()]
    return dict(kind='R4C1_B1_DUST_RECONSTRUCTION_V1',passed=sum(z['passed'] for z in checks),total=len(checks),
        checks=checks,source_sha256=pins,independent_controls=controls,
        formulas=dict(density_row=encode(rrho),epsilon_scaled_row=encode(Erho),lapse_flux_density_row=encode(flux_density),
            clock_momentum_scaled_row=encode(clock),clock_surface_current_row=encode(current),
            clock_residual=encode(ward),background_constraint=str(fried),constraint_quotient=[str(z) for z in quot],
            constraint_remainder=[str(z) for z in remainders],
            density='delta rho=R_rho*(q,qdot); delta epsilon=C_bg^-4*(delta rho-4*beta*rho*delta psi)',
            clock='delta p_tau=(a^3/C_bg)*(delta rho-beta*rho*delta psi+rho*trace(gamma)/2)'),
        exact_clock_conservation=all(z==0 for z in remainders),clock_off_shell=all(z==0 for z in ward),
        finite_amplitude_density_positive_proved=False,controlled_perturbation_evolution=False,nodal_G1_admitted=False,
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
    print(json.dumps({k:result[k] for k in ('passed','total','exact_clock_conservation','clock_off_shell','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
