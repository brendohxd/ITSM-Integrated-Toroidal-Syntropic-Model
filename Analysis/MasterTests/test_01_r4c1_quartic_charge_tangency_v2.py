"""V2 physical-density quotient and full-generator initial dust/phase controls."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import traceback
import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
ENGINE = 'Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
ESHA = '2cbb055c8a4172ef9e75daa7b80a92c5f979aadc817e29d7cace6115adb47ec5'
PRIMARY = 'Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
PARENT = 'Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v1_attempt_01/summary.json'
PSHA = 'bb1da6eefe1f0d769745498956ab1f3d100f83e0e5b64871c82135edd63b4c61'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_QUARTIC_CHARGE_TANGENCY_V2_NORMALIZATION_2026-10-28.md'
WORKING = 'Theory/Gates/RES-001/RES001_R4C1_QUARTIC_CONSTRAINT_TANGENCY_WORKING_ALGEBRA_2026-10-28.md'
ACTION = 'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md'
VARIATION = 'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
READ = lambda p: json.loads((ROOT / p).read_bytes())
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
STEPS = ('1e-20', '1e-26')
TOL = mp.mpf('1e-18')
en = None
W4 = None
shifts = None


def show(x):
    return mp.nstr(x, 65)


def norm(x):
    return max(abs(t) for t in x)


def rel(a, b):
    return abs(a-b)/(1+abs(a)+abs(b))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coefficients(modes):
    p = en.par
    HB = en.vals['H0']
    matrix = mp.matrix(modes)
    rhs = mp.matrix(modes, 1)
    for j in range(64):
        theta = 2*mp.pi*j/64
        w = mp.cos(theta)/500
        wp = -40*mp.sin(theta)/500
        wpp = -1600*w
        P = p['MU2']*(p['c1']+p['c2']+p['c3'])*(1+w*w)
        tt = p['c4']+(p['c1']-(p['c2']+p['c3'])*w*w)/(1+w*w)
        potential = -p['MU2']*((p['c2']+tt)*wp**2+p['c2']*w*wpp)
        A0 = p['c1']+2*p['c2']+p['c4']+(p['c2']-p['c3']+p['c4'])*w*w
        AH = 3*p['c1']+5*p['c2']+p['c3']+2*p['c4']+(2*p['c1']+4*p['c2']+2*p['c4'])*w*w
        f = (p['MU2']*w*wp*(HB*A0-en.H*AH)/(1+w*w)
             +3*p['b']*en.vals['p']*en.U*w**3*wp
             +5*p['b']*en.vals['p']*W4*w**5*wp)
        sn = [mp.sin(2*(i+1)*theta) for i in range(modes)]
        ds = [80*(i+1)*mp.cos(2*(i+1)*theta) for i in range(modes)]
        for a in range(modes):
            rhs[a] += f*sn[a]/64
            for b in range(modes):
                matrix[a,b] += (P*ds[a]*ds[b]+potential*sn[a]*sn[b])/64
    return list(mp.lu_solve(matrix, rhs))


def shift_at(theta, modes=12):
    coeff = shifts[modes]
    return (sum(a*mp.sin(2*(i+1)*theta) for i,a in enumerate(coeff)),
            sum(a*80*(i+1)*mp.cos(2*(i+1)*theta) for i,a in enumerate(coeff)))


def setup():
    global en, W4, shifts
    if SHA((ROOT/ENGINE).read_bytes()) != ESHA:
        raise ValueError('original engine drift')
    en = load('quartic_charge_engine_v2', ENGINE)
    en.setup()
    mp.mp.dps = 110
    point = READ(PRIMARY)['point']
    en.H, en.U, en.Ud, W4 = [mp.mpf(point[k]) for k in ('H','U','Ud','W')]
    shifts = {n: coefficients(n) for n in (8,12)}
    en.shift = shift_at


def state(theta):
    A, vd, dd, Sdd = en.initial(theta)
    w, wp, wpp = A[7], A[35], dd[7]
    A[13] = en.U*w*w+W4*w**4
    A[41] = (2*en.U*w+4*W4*w**3)*wp
    dd[13] = 2*en.U*(wp*wp+w*wpp)+W4*(12*w*w*wp*wp+4*w**3*wpp)
    return A,vd,dd,Sdd


def spatial(theta, step):
    A,vd,dd,Sdd = state(theta)
    L,grad = en.gradient(A)
    Wz = A[28:42]+vd+dd+A[45:48]+Sdd
    hz = en.hv(A,Wz,step)
    _,normal = en.density(A)
    energy = sum(grad[14+j]*normal[j] for j in range(14))-L
    w,wp = A[7],A[35]
    gam = mp.sqrt(1+w*w)
    flux = gam*hz[22]+w*wp*grad[22]/gam
    rho = -energy-flux
    gamdot = (en.H-en.vals['H0'])*w*w/gam
    Jdot = (gamdot-2*en.H*gam)*grad[22]+gam*(grad[8]-hz[36])
    return A,vd,dd,Sdd,L,grad,hz,energy,flux,rho,Jdot


def energy_at(A):
    L,grad = en.gradient(A)
    _,normal = en.density(A)
    return sum(grad[14+j]*normal[j] for j in range(14))-L


def solve(theta, step, real_control=False):
    A,vd,dd,Sdd,L,grad,hz,energy,flux,rho,Jdot = spatial(theta,step)
    Wt = A[14:28]+[mp.mpf(0)]*14+vd+[mp.mpf(0)]*6
    ht = en.hv(A,Wt,step)
    cols = []
    for j in range(14):
        direction = [mp.mpf(0)]*48
        direction[14+j] = 1
        cols.append(en.hv(A,direction,step)[14:28,0])
    matrix = mp.matrix([[cols[j][i] for j in range(14)] for i in range(14)])
    rhs = mp.matrix([grad[j]-ht[14+j]-hz[28+j] for j in range(14)])
    rhs[12] -= en.par['beta']*rho
    acc = mp.lu_solve(matrix,rhs)
    full_t = A[14:28]+list(acc)+vd+[mp.mpf(0)]*6
    Edot = mp.im(energy_at([a+mp.j*step*b for a,b in zip(A,full_t)]))/step
    rho_z = 40*mp.diff(lambda t:spatial(t,step)[9],theta)
    dz_Jdot = 40*mp.diff(lambda t:spatial(t,step)[10],theta)
    densitized_rho_dot = -Edot-dz_Jdot
    # The lapse equation is E+Dz(J)+sqrt(h)*rho=0.
    # h=I only AFTER differentiating that quotient.
    volume_rate = sum(A[14+j] for j in (0,3,5))/2
    rho_dot = densitized_rho_dot-volume_rate*rho
    R,Rp = shift_at(theta)
    expected = R*rho_z+(-3*en.H+Rp+en.par['beta']*en.vals['p'])*rho
    momentum_dot = ht[14:28,0]+matrix*acc
    ptheta = en.vals['Rc']*grad[24]
    phase_dot = en.vals['Rc']*momentum_dot[10]-A[24]*grad[23]
    phase_expected = Rp*ptheta+R*en.vals['Rc']*hz[24]
    phase_spatial = en.vals['Rc']*grad[38]
    checks = []
    def check(name,value,tol='1e-18'):
        checks.append(dict(name=name,value=show(value),criterion='normalized < '+tol,
                           passed=bool(value<mp.mpf(tol))))
    check('Hessian_symmetry',norm(matrix-matrix.T)/(1+norm(matrix)))
    check('Euler_solve',norm(matrix*acc-rhs)/(1+norm(rhs)))
    check('dust_Hamiltonian_tangency',rel(rho_dot,expected))
    check('phase_charge_tangency',rel(phase_dot,phase_expected))
    check('phase_spatial_current',rel(phase_spatial,-R*ptheta))
    if real_control:
        Ereal = mp.diff(lambda t:energy_at([a+t*b for a,b in zip(A,full_t)]),0)
        check('independent_real_energy_drift',rel(Ereal,Edot))
        def volume_at(t):
            qt=[A[i]+t*A[14+i] for i in range(14)]
            return mp.sqrt(en.body.det3(en.body.tensor(qt)))
        physical_real=mp.diff(lambda t:(rho+t*densitized_rho_dot)/volume_at(t),0)
        check('independent_real_density_quotient',rel(physical_real,rho_dot))
        check('independent_real_metric_volume_rate',rel(mp.diff(volume_at,0),volume_rate))
        for j in (0,7,12,13):
            el = en.independent_euler(A,vd,dd,Sdd,acc,j)
            if j == 12:
                el -= en.par['beta']*rho
            check('independent_real_Euler_'+str(j),abs(el)/(1+norm(rhs)))
    return dict(acc=acc,rho=rho,rho_z=rho_z,Edot=Edot,flux=flux,
                rho_dot=rho_dot,densitized_rho_dot=densitized_rho_dot,
                volume_rate=volume_rate,dust_expected=expected,phase_dot=phase_dot,
                phase_expected=phase_expected,checks=checks)


def task(item):
    label,theta_text,real_control = item
    checks = []
    try:
        theta = mp.mpf(theta_text)
        values = []
        for hs in STEPS:
            value = solve(theta,mp.mpf(hs),real_control)
            checks.extend(dict(c,name=hs+'_'+c['name']) for c in value['checks'])
            values.append(value)
        a,b = values
        def check(name,value,tol='1e-18'):
            checks.append(dict(name=name,value=show(value),criterion='normalized < '+tol,
                               passed=bool(value<mp.mpf(tol))))
        for key in ('rho','rho_dot','dust_expected','phase_dot','phase_expected','Edot'):
            check('two_step_'+key,rel(a[key],b[key]))
        check('two_step_acceleration',norm(a['acc']-b['acc'])/(1+norm(a['acc'])+norm(b['acc'])))
        r8,r12 = shift_at(theta,8),shift_at(theta,12)
        check('independent_8_12_shift',max(rel(x,y) for x,y in zip(r8,r12)),'1e-25')
        p=en.par;w=mp.cos(theta)/500;wp=-40*mp.sin(theta)/500;wpp=-1600*w
        P=p['MU2']*(p['c1']+p['c2']+p['c3'])*(1+w*w)
        Pz=2*p['MU2']*(p['c1']+p['c2']+p['c3'])*w*wp
        tt=p['c4']+(p['c1']-(p['c2']+p['c3'])*w*w)/(1+w*w)
        V=-p['MU2']*((p['c2']+tt)*wp*wp+p['c2']*w*wpp)
        A0=p['c1']+2*p['c2']+p['c4']+(p['c2']-p['c3']+p['c4'])*w*w
        AH=3*p['c1']+5*p['c2']+p['c3']+2*p['c4']+(2*p['c1']+4*p['c2']+2*p['c4'])*w*w
        f=(p['MU2']*w*wp*(en.vals['H0']*A0-en.H*AH)/(1+w*w)
           +3*p['b']*en.vals['p']*en.U*w**3*wp+5*p['b']*en.vals['p']*W4*w**5*wp)
        Rpp=40*mp.diff(lambda t:shift_at(t)[1],theta)
        check('shift_ODE_residual',abs(-P*Rpp-Pz*r12[1]+V*r12[0]-f)/(1+abs(f)))
        omitted_drift=b['rho_dot']-2*en.H*b['flux']
        omitted_beta=b['dust_expected']-p['beta']*en.vals['p']*b['rho']
        volume_effect=rel(b['densitized_rho_dot'],b['dust_expected'])
        checks.append(dict(name='reject_omitted_metric_volume_drift',value=show(volume_effect),
                           criterion='normalized mismatch > 1e-18',passed=bool(volume_effect>mp.mpf('1e-18'))))
        drift_effect=rel(omitted_drift,b['dust_expected'])
        beta_effect=rel(b['rho_dot'],omitted_beta)
        checks.extend([dict(name='reject_omitted_inverse_metric_drift',value=show(drift_effect),
                            criterion='normalized mismatch > 1e-18',passed=bool(drift_effect>mp.mpf('1e-18'))),
                       dict(name='reject_omitted_dust_beta_term',value=show(beta_effect),
                            criterion='normalized mismatch > 1e-18',passed=bool(beta_effect>mp.mpf('1e-18')))])
        result=dict(label=label,theta=theta_text,checks=checks,
                    values={k:([show(x) for x in v] if k=='acc' else show(v))
                            for k,v in b.items() if k!='checks'})
    except Exception:
        checks.append(dict(name='unexpected_exception',passed=False,traceback=traceback.format_exc()))
        result=dict(label=label,theta=theta_text,checks=checks)
    return result


def identities():
    u,v,ut,vt,uz,vz,R,gam,Vz,zeta=sy.symbols('u v ut vt uz vz R gam Vz zeta',real=True)
    yt,yv=ut-R*uz,vt-R*vz
    jt=v*yt-u*yv;jz=v*uz-u*vz;ss=u*u+v*v
    phase=(yt*yt+yv*yv-uz*uz-vz*vz)/2-zeta*(-jt*jt+jz*jz+(gam*jt+Vz*jz)**2)/2
    phase-=ss/2+ss**2/8+ss**3/24
    pairs=((u,-v),(v,u),(ut,-vt),(vt,ut),(uz,-vz),(vz,uz))
    variation=sy.expand(sum(sy.diff(phase,x)*dx for x,dx in pairs))
    charge=u*sy.diff(phase,vt)-v*sy.diff(phase,ut)
    current=u*sy.diff(phase,vz)-v*sy.diff(phase,uz)
    current_identity=sy.expand((current+R*charge).subs({uz:0,vz:0,Vz:0}))
    epsilon,C,tau_t,beta,p,rho,vol,H,Rp,rhoz=sy.symbols('epsilon C tau_t beta p rho vol H Rp rhoz',real=True)
    Ldust=-epsilon*(-C*C*tau_t*tau_t+C**4)/2
    clock=sy.diff(Ldust,tau_t)
    clock_identity=sy.expand(clock.subs(tau_t,C)*C-epsilon*C**4)
    multiplier=sy.expand(sy.diff(Ldust,epsilon).subs(tau_t,C))
    Lpsi=sy.expand((C*beta*sy.diff(Ldust,C)).subs(tau_t,C)+beta*epsilon*C**4)
    required=R*rhoz+(-3*H+Rp+beta*p)*rho
    dilution=sy.expand(vol/C*(required+3*H*rho-beta*p*rho)-vol/C*(R*rhoz+Rp*rho))
    vals={'global_U1_variation':variation,'initial_phase_flux':current_identity,
          'future_dust_clock_momentum':clock_identity,'dust_multiplier_future_root':multiplier,
          'on_shell_dust_scalar_source':Lpsi,'dust_current_dilution':dilution}
    t,hh,rr,rrdot=sy.symbols('t hh rr rrdot',real=True)
    volume=sy.sqrt(sy.det(sy.eye(3)*(1+2*hh*t)))
    vals['metric_volume_derivative']=sy.simplify(sy.diff(volume,t).subs(t,0)-3*hh)
    vals['physical_density_quotient']=sy.simplify(sy.diff((rr+t*rrdot)/volume,t).subs(t,0)-(rrdot-3*hh*rr))
    return [dict(name=k,passed=bool(v==0),exact_remainder=str(v)) for k,v in vals.items()]


def pins_before():
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:
        raise ValueError('owning receipt drift')
    pins=dict(READ(PARENT)['source_sha256'])
    for path in (PARENT,PRIMARY,ENGINE,CONTRACT,WORKING,ACTION,VARIATION,SELF):
        value=SHA((ROOT/path).read_bytes())
        if path in pins and pins[path]!=value:
            raise ValueError('inherited source drift '+path)
        pins[path]=value
    verify(pins)
    return pins


def verify(pins):
    for path,want in pins.items():
        file=ROOT/path
        if SHA(file.read_bytes())!=want:
            raise ValueError('source drift '+path)
        sidecar=Path(str(file)+'.sha256')
        if not sidecar.exists() or sidecar.read_text().split()[0].lower()!=want:
            raise ValueError('sidecar drift '+path)


def calculate(workers):
    pins=pins_before()
    setup()
    jobs=[('interior_pi4',show(mp.pi/4),True),('interior_3pi4',show(3*mp.pi/4),True)]
    for node in (1,3):
        for offset in ('0.1','0.01'):
            for side in (-1,1):
                jobs.append((f'node{node}_{side}_{offset}',show(node*mp.pi/2+side*mp.mpf(offset)),False))
    results=[]
    if workers==1:
        for job in jobs:
            result=task(job);results.append(result)
            print(json.dumps(dict(completed=result['label'],passed=all(c['passed'] for c in result['checks']))),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=setup) as pool:
            futures=[pool.submit(task,j) for j in jobs]
            for future in as_completed(futures):
                result=future.result();results.append(result)
                print(json.dumps(dict(completed=result['label'],passed=all(c['passed'] for c in result['checks']))),flush=True)
    results.sort(key=lambda r:r['label'])
    exact=identities()
    checks=exact+[dict(c,point=r['label']) for r in results for c in r['checks']]
    verify(pins)
    return dict(result_id='R4C1-QUARTIC-CHARGE-TANGENCY-V2',working_digits=110,
                steps=list(STEPS),mpmath=mp.__version__,sympy=sy.__version__,
                source_sha256=pins,checks=checks,points=results,
                passed=sum(c['passed'] for c in checks),total=len(checks),
                interpretation='Registered numerical initial point controls and exact current identities; not continuum transport',
                continuum_constraint_transport_certified=False,time_evolution=False,
                G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path)
    group.add_argument('--replay',type=Path)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if args.workers not in (1,2,3,4):
        raise ValueError('workers must be 1..4')
    result=calculate(args.workers);data=ENC(result)
    if args.replay:
        if (args.replay/'summary.json').read_bytes()!=data:
            raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False)
        path=args.output/'summary.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':
    main()
