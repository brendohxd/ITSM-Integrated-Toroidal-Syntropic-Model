"""Fresh full quadratic and unfixed-lapse reduction for F-tau and R-tau."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
F_WAVE=(0,1,3,9,10,11,12,13)
R_WAVE=(0,1,3,6,7,8,9,10,11,12,13)
F_MEAN=(0,1,2,3,4,5,9,10,11,12,13)
R_MEAN=tuple(range(14))
LABELS=('gamma_xx','gamma_xy','gamma_xz','gamma_yy','gamma_yz','gamma_zz',
        'v_x','v_y','v_z','du','dv','dr','dpsi','dZ')
clean=lambda z:s.factor(s.cancel(z))

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def setup():
    backend=load('two_repair_full_backend',BACKEND)
    old=backend.load('two_repair_full_types',backend.QUADRATIC);par=old.parameters()
    a=s.Symbol('a',positive=True);H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    u,v,r,du,dv,dr,p,psi,rho=s.symbols('u v r du dv dr p psi rho',real=True)
    variables=(a,H,u,v,r,du,dv,dr,p,psi,rho)
    initial=dict(zip(variables,(1,s.sqrt(s.Rational(3469,4620)),1,0,1,0,1,s.Rational(1,4),s.Rational(1,5),0,s.Rational(1,5))))
    Mc=par['MP2']+par['MU2']*(par['c1']+par['c3']+3*par['c2'])/2
    ss=u*u+v*v
    mass=par['m2']+par['lambda4']*ss/2+par['lambda6']*ss**2/(4*par['Lambda']**2)+par['g_r']*r*r/2
    flow=s.Matrix([a*H,-(du*du+dv*dv+dr*dr+par['K_Q']*p*p+rho)/(2*Mc),
        du,dv,dr,-3*H*du-mass*u,-3*H*dv-mass*v,
        -3*H*dr-par['mr2']*r-par['lambda_r']*r**3-par['g_r']*ss*r/2,
        -3*H*p-par['beta']*rho/par['K_Q'],p,(-3*H+par['beta']*p)*rho])
    potential=par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)
    potential+=par['mr2']*r*r/2+par['lambda_r']*r**4/4+par['g_r']*ss*r*r/4
    energy=(du*du+dv*dv+dr*dr+par['K_Q']*p*p)/2+potential+rho
    return dict(backend=backend,old=old,par=par,variables=variables,initial=initial,
        flow=flow,k=k,friedmann=3*Mc*H*H-energy)

def slots_for(route,mean=False):
    return (F_MEAN if route=='F-tau' else R_MEAN) if mean else (F_WAVE if route=='F-tau' else R_WAVE)

def state(slots,x,variables,par,exp,unfixed=False):
    a,H,u,v,r,du,dv,dr,p,psi,rho=variables;n=len(slots)
    C=exp(par['beta']*psi)
    de=x[3*n+8] if unfixed else 0
    q=[a*a,0,0,a*a,0,a*a,0,0,0,u,v,r,psi,0,0,(rho+de)/C**4]
    vel=[0]*16;dz=[0]*16
    for j in (0,3,5):vel[j]=2*H*a*a
    vel[9]=du;vel[10]=dv;vel[11]=dr;vel[12]=p;vel[14]=C
    for i,j in enumerate(slots):
        if j<6:
            q[j]+=a*a*x[i];vel[j]+=a*a*(x[n+i]+2*H*x[i]);dz[j]=a*a*x[2*n+i]
        elif j<9:
            q[j]+=x[i]/a;vel[j]+=(x[n+i]-H*x[i])/a;dz[j]=x[2*n+i]/a
        else:
            q[j]+=x[i];vel[j]+=x[n+i];dz[j]=x[2*n+i]
    jpsi=slots.index(12)
    N=1+x[3*n+6] if unfixed else exp(-par['beta']*x[jpsi])
    Nz=x[3*n+7] if unfixed else -par['beta']*N*x[2*n+jpsi]
    return q+vel+dz+[z/a for z in x[3*n:3*n+3]]+[z/a for z in x[3*n+3:3*n+6]]+[N,Nz]

def derive(route,env,mean=False):
    backend,old,par=env['backend'],env['old'],env['par']
    variables,k=env['variables'],env['k'];a,H,u,v,r,du,dv,dr,p,psi,rho=variables
    dt=lambda z:sum(s.diff(z,w)*f for w,f in zip(variables,env['flow']))
    slots=slots_for(route,mean);n=len(slots);zi=slots.index(13)
    action=backend.ClockGaugeAction(route,par)
    # One exact Jet class throughout the newly assembled field variation.
    action.body.sqrt=old.jsqrt;action.body.exp=old.jexp
    action.body.body.__globals__.update(sqrt=old.jsqrt,exp=old.jexp)
    def hessian(unfixed):
        count=3*n+(9 if unfixed else 6)
        x=[old.Jet.var(i) for i in range(count)]
        L=action.density(state(slots,x,variables,par,old.jexp,unfixed))[0]
        mat=s.zeros(count)
        for (i,j),z in L.h.items():mat[i,j]=mat[j,i]=clean(z)
        return mat
    local=hessian(False);cols=2*n+(0 if mean else 3)
    T=s.zeros(3*n+6,cols)
    for i in range(n):
        T[i,i]=1;T[n+i,n+i]=1
        if not mean:T[2*n+i,i]=s.I*k
    if not mean:
        for i in range(3):T[3*n+i,2*n+i]=1;T[3*n+3+i,2*n+i]=s.I*k
    full=(T.conjugate().T*local*T).applyfunc(clean)
    keep=list(i for i in range(n) if i!=zi)+list(n+i for i in range(n) if i!=zi)
    elim=[zi]+([] if mean else list(range(2*n,2*n+3)))
    D=full.extract(elim,elim);cross=full.extract(keep,elim)
    if any(z!=0 for i in range(D.rows) for j,z in enumerate(D.row(i)) if i!=j):
        raise ValueError('unexpected nondiagonal algebraic block; do not silently diagonalize')
    Dinv=s.diag(*[1/z for z in D.diagonal()])
    solve=(-Dinv*cross.conjugate().T).applyfunc(clean)
    red=(full.extract(keep,keep)+cross*solve).applyfunc(clean)
    m=n-1;M=red[m:2*m,m:2*m];B=red[m:2*m,:m];Q=red[:m,:m]
    Md=M.applyfunc(dt).applyfunc(clean);Bd=B.applyfunc(dt).applyfunc(clean)
    Minv=M.inv();G=s.zeros(2*m);G[:m,m:2*m]=s.eye(m)
    G[m:2*m,:m]=-Minv*(Bd-Q);G[m:2*m,m:2*m]=-Minv*(Md+B-B.conjugate().T)
    G=G.applyfunc(clean)
    pull=s.zeros(cols,2*m)
    for i,j in enumerate(keep):pull[j,i]=1
    for i,j in enumerate(elim):pull[j,:]=solve[i,:]
    # Lapse variation before clock substitution, retaining the Euler flux.
    unfixed=hessian(True);ucols=cols+1
    U=s.zeros(3*n+9,ucols);U[:3*n+6,:cols]=T
    ip=slots.index(12)
    U[3*n+6,ip]=-par['beta']
    if not mean:U[3*n+7,ip]=-s.I*k*par['beta']
    U[3*n+8,-1]=1
    en_no_flux=(unfixed[3*n+6,:]*U).applyfunc(clean)
    en=(en_no_flux+(-s.I*k*unfixed[3*n+7,:]*U if not mean else s.zeros(1,ucols))).applyfunc(clean)
    upull=s.zeros(ucols,2*m);upull[:cols,:]=pull
    e_row=(en*upull/a**3).applyfunc(clean)
    epsi=s.zeros(1,2*m);qindex={slot:i for i,slot in enumerate(slots) if slot!=13}
    # Z is last in each field ordering; remaining dynamic indices are unchanged.
    epsi[0,qindex[12]]=1
    trace=s.zeros(1,2*m)
    for slot in (0,3,5):
        if slot in qindex:trace[0,qindex[slot]]=1
    rho_row=(e_row+4*par['beta']*rho*epsi).applyfunc(clean)
    clock=(rho_row-par['beta']*rho*epsi+rho*trace/2).applyfunc(clean)
    sz=solve[3,:] if not mean else s.zeros(1,2*m)
    bare_clock=(clock.applyfunc(dt)+clock*G+(3*H-par['beta']*p)*clock-
        (s.I*k*rho*sz/a if not mean else s.zeros(1,2*m))).applyfunc(clean)
    charge=s.zeros(1,2*m);J=u*dv-v*du
    charge[0,qindex[9]]=dv;charge[0,qindex[10]]=-du
    charge[0,m+qindex[9]]=-v;charge[0,m+qindex[10]]=u
    charge+=J*(par['beta']*epsi+trace/2)
    jz=s.zeros(1,2*m)
    if not mean:
        jz[0,qindex[9]]+=s.I*k*(1+par['zeta']*(u*u+v*v))*v/a**2
        jz[0,qindex[10]]-=s.I*k*(1+par['zeta']*(u*u+v*v))*u/a**2
        jz-=J*sz/a
        if route=='R-tau':jz[0,qindex[8]]-=par['zeta']*(u*u+v*v)*J/a
    charge_ward=(charge.applyfunc(dt)+charge*G+3*H*charge+
        (s.I*k*jz if not mean else s.zeros(1,2*m))).applyfunc(clean)
    recover=upull.copy();recover[-1,:]=e_row
    return dict(route=route,mean=mean,slots=slots,n=n,m=m,local=local,T=T,full=full,
        keep=keep,elim=elim,D=D,cross=cross,solve=solve,red=red,M=M,B=B,Q=Q,Md=Md,Bd=Bd,
        G=G,pull=pull,unfixed=unfixed,lapse=en,lapse_no_flux=en_no_flux,
        lapse_density_coefficient=en[0,-1],rho_row=rho_row,epsilon_scaled_row=e_row,
        clock_row=clock,bare_clock_ward=bare_clock,phase_charge_row=charge,
        phase_current_row=jz,phase_ward=charge_ward,recovered_lapse=(en*recover).applyfunc(clean))

def friedmann_remainder(row,env):
    H=env['variables'][1];F=env['friedmann'];remainders=[];quotients=[]
    for z in row:
        num,den=s.fraction(clean(z));q,r=s.div(num,F,H)
        remainders.append(clean(r/den));quotients.append(clean(q/den))
    return s.Matrix([remainders]),s.Matrix([quotients])

