"""Complete initial local Jacobi coefficients; no physical evolution/domain claim."""
import argparse,hashlib,importlib.util,json,multiprocessing
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json'
PSHA='342ad03354a13a650ef73798c43066a5af9dcabe021abd4714a779a40e4ace90'
OPERATOR='Analysis/MasterTests/outputs/r4c1_constrained_principal_v1_attempt_01/summary.json'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FULL_INITIAL_JACOBI_V1_CONTRACT_2026-10-29.md'
PHYSICAL=(0,1,3,6,7,8,9,10,11,12,13)
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)
pack=lambda a:[[show(z) for z in row] for row in a.tolist()]
norm=lambda a:max(abs(z) for z in a)
weak=None
beta=None
Q=None
T=None
Z=None
Pnum=None


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def setup():
    global weak,beta,Q,T,Z,Pnum
    ch=load('jacobi_original_registered',CHARGE);ch.setup();mp.mp.dps=110
    backend=load('jacobi_original_full_action',BACKEND)
    weak=backend.WeakAction(ch.en.body,ch.en.par);beta=ch.en.par['beta']
    Q=mp.matrix(56,20);T=mp.matrix(56,20);Z=mp.matrix(56,20)
    for i in range(16):Q[i,i]=1;T[16+i,i]=1;Z[32+i,i]=1
    for i in range(3):Q[48+i,16+i]=1;Z[51+i,16+i]=1
    Q[54,19]=1;Z[55,19]=1
    w=s.Symbol('w',real=True,nonzero=True);c=s.Symbol('c',real=True);zz=s.Symbol('Z_background',real=True)
    pp=s.Matrix([[s.sympify(t,locals={'w':w,'c':c,'Z_background':zz}) for t in row]
                 for row in READ(OPERATOR)['formulas']['reduced_pencil']])
    Pnum=s.lambdify((w,zz,c),pp,modules='mpmath')


def hessian(A):
    columns=[]
    for j in range(56):
        d=mp.matrix(56,1);d[j]=1;columns.append(weak.hv(A,d,mp.mpf('1e-26')))
    return mp.matrix([[columns[j][i] for j in range(56)] for i in range(56)])


def drift(A,v,eps):
    step=mp.mpf(eps)/(1+norm(v))
    plus=hessian([a+step*d for a,d in zip(A,v)])
    minus=hessian([a-step*d for a,d in zip(A,v)])
    return (plus-minus)/(2*step)


def coefficients(H,Ht,Hz):
    return dict(
        zero=Q.T*H*Q-T.T*Ht*Q-Z.T*Hz*Q,
        time=Q.T*H*T-T.T*H*Q-T.T*Ht*T-Z.T*Hz*T,
        space=Q.T*H*Z-Z.T*H*Q-T.T*Ht*Z-Z.T*Hz*Z,
        time_time=-T.T*H*T,time_space=-T.T*H*Z-Z.T*H*T,space_space=-Z.T*H*Z)


def action(coeff,jets):
    names=('zero','time','space','time_time','time_space','space_space')
    out=mp.matrix(len(jets[0]),1)
    for name,value in zip(names,jets):out+=coeff[name]*value
    return out


def euler(A,Dt,Dz):
    _,g=weak.gradient(A)
    gt=weak.hv(A,Dt,mp.mpf('1e-26'));gz=weak.hv(A,Dz,mp.mpf('1e-26'))
    return Q.T*g-T.T*gt-Z.T*gz


def pullback(lapse):
    R=mp.matrix(20,14)
    for j,i in enumerate(PHYSICAL):R[i,j]=1
    for i in range(3):R[16+i,11+i]=1
    R[19,9]=-beta*lapse
    return R


def linear_jet(jets):
    u,ut,uz,utt,utz,uzz=jets
    return Q*u+T*ut+Z*uz,Q*ut+T*utt+Z*utz,Q*uz+T*utz+Z*uzz


def point(row):
    checks=[]
    def close(name,error):checks.append(dict(name=name,passed=bool(error<mp.mpf('1e-18')),error=show(error)))
    def reject(name,error):checks.append(dict(name=name,passed=bool(error>mp.mpf('1e-18')),error=show(error)))
    raw=READ(row['raw_point_source']);A=list(map(mp.mpf,raw['original_first_jet']))
    H=mp.matrix([[mp.mpf(z) for z in rr] for rr in raw['full_Hessian']])
    g=mp.matrix(list(map(mp.mpf,raw['gradient'])))
    Dt=mp.matrix(list(map(mp.mpf,row['complete_time_direction'])))
    Dz=mp.matrix(list(map(mp.mpf,row['complete_spatial_direction'])))
    # Full Euler rows in Y=(q16,S3,N) order; do not silently zero residuals.
    E=Q.T*g-T.T*H*Dt-Z.T*H*Dz
    ref=mp.matrix(list(map(mp.mpf,row['actual_initial_Euler16']+row['initial_shift_residuals']+[row['initial_lapse_residual']])))
    close('stored_complete_initial_Euler_bridge',norm(E-ref)/(1+norm(E)+norm(ref)))
    derivatives=[]
    for eps in ('1e-16','1e-20'):
        derivatives.append((drift(A,Dt,eps),drift(A,Dz,eps)))
    (Ht0,Hz0),(Ht,Hz)=derivatives
    close('whole_time_drift_two_steps',norm(Ht0-Ht)/(1+norm(Ht)))
    close('whole_space_drift_two_steps',norm(Hz0-Hz)/(1+norm(Hz)))
    J=coefficients(H,Ht,Hz)
    for name in ('time_time','time_space','space_space'):
        close('second_order_symmetry_'+name,norm(J[name]-J[name].T)/(1+norm(J[name])))
    close('formal_adjoint_first_time',norm(J['time']+J['time'].T+2*T.T*Ht*T+T.T*Hz*Z+Z.T*Hz*T)/(1+norm(J['time'])))
    close('formal_adjoint_first_space',norm(J['space']+J['space'].T+T.T*Ht*Z+Z.T*Ht*T+2*Z.T*Hz*Z)/(1+norm(J['space'])))
    no_drift=coefficients(H,mp.matrix(56),mp.matrix(56))
    reject('reject_deleted_background_drift',max(norm(J[key]-no_drift[key])/(1+norm(J[key])) for key in ('zero','time','space')))
    # Independent direct variation of all20 original Euler rows.
    full_jets=[mp.matrix([mp.mpf((j*(k+2)+3*k)%13-6)/(211+j+17*k) for j in range(20)]) for k in range(6)]
    dA,dDt,dDz=linear_jet(full_jets);pred=action(J,full_jets)
    for eps in ('1e-16','1e-20'):
        h=mp.mpf(eps)/(1+max(norm(v) for v in (dA,dDt,dDz)))
        values=[]
        for sign in (-1,1):values.append(euler([a+sign*h*d for a,d in zip(A,dA)],Dt+sign*h*dDt,Dz+sign*h*dDz))
        observed=(values[1]-values[0])/(2*h)
        close('direct_twenty_Euler_variation_'+eps,norm(observed-pred)/(1+norm(observed)+norm(pred)))
    R=pullback(A[54]);reduced={key:R.T*value*R for key,value in J.items()}
    connection=beta**2*A[54]*E[19];reduced['zero'][9,9]+=connection
    # epsilon/lapse remain a regular algebraic pair; epsilon need not be projected away by fiat.
    close('lapse_multiplier_algebraic_coefficient',abs(J['zero'][19,15]+1))
    close('lapse_multiplier_derivatives_absent',max(abs(J[key][19,15]) for key in ('time','space','time_time','time_space','space_space')))
    close('pulledback_multiplier_column_cancels',max(norm(R.T*value[:,15]) for value in J.values()))
    # Nonlinear lapse pullback: tau is fixed by the gauge, and N=e^(-beta*dpsi).
    small_jets=[mp.matrix([mp.mpf((j*(k+3)+2*k)%11-5)/(331+j+19*k) for j in range(14)]) for k in range(6)]
    yjets=[R*value for value in small_jets]
    a1,t1,z1=linear_jet(yjets);pred=action(reduced,small_jets)
    for eps in ('1e-16','1e-20'):
        h=mp.mpf(eps)/(1+max(norm(v) for v in (a1,t1,z1)))
        values=[]
        for sign in (-1,1):
            x=sign*h;Ap=[a+x*d for a,d in zip(A,a1)];tp=Dt+x*t1;zp=Dz+x*z1
            f,ft,fz,ftt,ftz,fzz=[v[9] for v in small_jets]
            nn=A[54]*mp.exp(-beta*x*f)
            Ap[54]=nn;Ap[55]=-beta*x*fz*nn
            tp[54]=-beta*x*ft*nn;tp[55]=(beta**2*x*x*ft*fz-beta*x*ftz)*nn
            zp[54]=Ap[55];zp[55]=(beta**2*x*x*fz*fz-beta*x*fzz)*nn
            full=euler(Ap,tp,zp);values.append(pullback(nn).T*full)
            close('nonlinear_clock_multiplier_constraint_'+eps+'_'+str(sign),abs(full[15]))
        observed=(values[1]-values[0])/(2*h)
        close('direct_nonlinear_clock_lapse_pullback_'+eps,norm(observed-pred)/(1+norm(observed)+norm(pred)))
    # Independent old principal operator, after the real constant shift-value Doppler adaptation.
    for ratio in (-1,0,2):
        ca=mp.mpf(ratio);co=ca-A[50]
        pp=-co**2*reduced['time_time']+co*reduced['time_space']-reduced['space_space']
        ss=pp[11:14,11:14]
        tail=mp.matrix(3,11)
        for j in range(11):tail[:,j]=mp.lu_solve(ss,pp[11:14,j])
        physical=pp[:11,:11]-pp[:11,11:14]*tail
        expected=mp.matrix(Pnum(A[7],A[13],ca))
        close('independent_constrained_principal_ratio_'+str(ratio),norm(physical-expected)/(1+norm(expected)))
    return dict(label=row['label'],theta=row['theta'],checks=checks,
                full_twenty_coefficients={key:pack(value) for key,value in J.items()},
                initial_fourteen_pullback_coefficients={key:pack(value) for key,value in reduced.items()},
                nonzero_background_Euler20=[show(z) for z in E],lapse_residual_connection=show(connection),
                drift_sha256=dict(time=SHA(ENC(pack(Ht))),space=SHA(ENC(pack(Hz)))),
                omitted_drift_effect=show(max(norm(J[key]-no_drift[key])/(1+norm(J[key])) for key in ('zero','time','space'))),
                full_shift_constraint_inverted=False,global_means_or_zero_modes_reduced=False,
                exact_node_operator_exported=False,physical_evolution=False)


def calculate(workers):
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify();results=[]
    if workers==1:
        setup()
        for row in parent['points']:
            value=point(row);results.append(value);print(json.dumps(dict(completed=value['label'])),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=setup) as pool:
            futures=[pool.submit(point,row) for row in parent['points']]
            for future in as_completed(futures):
                value=future.result();results.append(value);print(json.dumps(dict(completed=value['label'])),flush=True)
    results.sort(key=lambda r:r['label']);files={r['label']+'.json':ENC(r) for r in results}
    checks=[dict(c,point=r['label']) for r in results for c in r['checks']]
    # Exact second-field-variation coefficient; residuals are not erased.
    beta,chi=s.symbols('beta chi',real=True)
    checks.append(dict(name='exact_nonlinear_lapse_second_variation',passed=s.diff(s.exp(-beta*chi),chi,2).subs(chi,0)==beta**2))
    verify()
    summary=dict(result_id='R4C1-FULL-INITIAL-JACOBI-V1',source_sha256=pins,
                 file_sha256={name:SHA(data) for name,data in files.items()},checks=checks,
                 passed=sum(c['passed'] for c in checks),total=len(checks),
                 coefficient_order=['zero','time','space','time_time','time_space','space_space'],
                 full_fields='q16,S3,N',pullback_fields='hxx,hxy,hyy,Vx,Vy,Vz,u,v,r,psi,Z,Sx,Sy,Sz',
                 working_digits=110,stored_digits=65,drift_steps=['1e-16','1e-20'],Hessian_step='1e-26',
                 mpmath=mp.__version__,sympy=s.__version__,full_initial_local_operator_exported=True,
                 actual_reduced_frequency_source_exported=False,spatial_constraint_inverse_derived=False,
                 global_zero_modes_reduced=False,exact_node_operator_exported=False,
                 drift_error_interval_certified=False,time_evolution=False,G1_complete=False,
                 physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)
    files['summary.json']=ENC(summary);return summary,files


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    p.add_argument('--workers',type=int,choices=(1,2,3,4),default=3);a=p.parse_args()
    summary,files=calculate(a.workers)
    if a.replay:
        for name,data in files.items():
            f=a.replay/name
            if f.read_bytes()!=data or Path(str(f)+'.sha256').read_text().split()[0].lower()!=SHA(data):
                raise ValueError('immutable replay mismatch '+name)
        print('ALL_SEVEN_FILES_READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False)
        for name,data in files.items():
            f=a.output/name;f.write_bytes(data)
            Path(str(f)+'.sha256').write_text(SHA(data)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({k:summary[k] for k in ('passed','total','full_initial_local_operator_exported','actual_reduced_frequency_source_exported','G1_complete','physics_pass')}))
    raise SystemExit(0 if summary['passed']==summary['total'] else 2)


if __name__=='__main__':main()
