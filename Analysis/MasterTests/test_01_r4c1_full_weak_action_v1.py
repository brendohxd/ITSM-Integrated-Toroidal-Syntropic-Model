"""Audit the original full implicit planar weak action; no evolution claim."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_normalized_adm_ward_v2_attempt_01/summary.json'
PSHA='3ee19a8c481126be7bbf18fb0084893da9ff203721d613e526f157add91076e4'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FULL_WEAK_ACTION_V1_CONTRACT_2026-10-28.md'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
READ=lambda p:json.loads((ROOT/p).read_bytes())
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def ricci3(h,dh,ddh):
    hi=h**-1;dhi=-hi*dh*hi
    F=lambda l,i,j:((dh[l,j] if i==2 else 0)+(dh[l,i] if j==2 else 0)-(dh[i,j] if l==2 else 0))
    FF=lambda l,i,j:((ddh[l,j] if i==2 else 0)+(ddh[l,i] if j==2 else 0)-(ddh[i,j] if l==2 else 0))
    G=[[[sum(hi[k,l]*F(l,i,j) for l in range(3))/2 for j in range(3)] for i in range(3)] for k in range(3)]
    dG=[[[sum(dhi[k,l]*F(l,i,j)+hi[k,l]*FF(l,i,j) for l in range(3))/2 for j in range(3)] for i in range(3)] for k in range(3)]
    R=mp.matrix(3)
    for i in range(3):
        for j in range(3):
            R[i,j]=dG[2][i][j]-(sum(dG[k][i][k] for k in range(3)) if j==2 else 0)
            R[i,j]+=sum(G[k][k][l]*G[l][i][j]-G[k][j][l]*G[l][i][k] for k in range(3) for l in range(3))
    return R,sum(hi[i,j]*R[i,j] for i in range(3) for j in range(3)),G


def make_jet(seed):
    r=lambda a,b:mp.mpf(a)/b
    h=mp.matrix([[r(6,5),r(1,31),r(1,37)],[r(1,31),r(11,10),-r(1,41)],[r(1,37),-r(1,41),r(9,10)]])
    HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))
    q=[h[i,j] for i,j in HM]+[r(1,10),r(1+seed,33),-r(1,43),r(2,5),r(3,5),r(1,7),r(1,9),r(2,7),0,r(7,100)]
    v=[r((i+seed)%7-3,79+i) for i in range(16)];v[14]=r(6,5);v[15]=mp.mpf(0)
    d=[r((2*i+seed)%9-4,113+i) for i in range(16)];d[15]=mp.mpf(0)
    dd=[r((i+seed)%7-3,401+i) for i in range(16)];dd[15]=mp.mpf(0)
    S=[r(1,19),-r(1,23),r(1,29)];Sz=[r(1,73),-r(1,79),r(1,83)]
    return q+v+d+S+Sz+[r(10+seed,10),r(1+seed,47)],dd


def coordinate_context(A,dd,body):
    q,v,d,S,Sz,N,Nz=A[:16],A[16:32],A[32:48],A[48:51],A[51:54],A[54],A[55]
    h=mp.matrix(body.tensor(q));ht=mp.matrix(body.tensor(v));hz=mp.matrix(body.tensor(d));hzz=mp.matrix(body.tensor(dd))
    def point(t,z):
        hh=h+t*ht+z*hz+z*z*hzz/2;ss=mp.matrix(S)+z*mp.matrix(Sz);nn=N+Nz*z
        vv=mp.matrix(q[6:9])+t*mp.matrix(v[6:9])+z*mp.matrix(d[6:9])
        gam=mp.sqrt(1+(vv.T*hh*vv)[0]);n=mp.matrix([gam/nn,*list(vv-ss*gam/nn)])
        g=mp.zeros(4);g[0,0]=-nn*nn+(ss.T*hh*ss)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=(hh*ss)[i]
            for j in range(3):g[i+1,j+1]=hh[i,j]
        return g,n
    g,n=point(0,0);gi=g**-1
    def deriv(fn,mu):
        return mp.diff(lambda t:fn(t,0),0) if mu==0 else mp.diff(lambda z:fn(0,z),0) if mu==3 else mp.mpf(0)
    dg=[mp.matrix([[deriv(lambda t,z:point(t,z)[0][i,j],a) for j in range(4)] for i in range(4)]) for a in range(4)]
    conn=[[[sum(gi[a,l]*(dg[m][l,k]+dg[k][l,m]-dg[l][m,k]) for l in range(4))/2 for k in range(4)] for m in range(4)] for a in range(4)]
    Dn=mp.matrix([[deriv(lambda t,z:point(t,z)[1][a],m)+sum(conn[a][m][b]*n[b] for b in range(4)) for a in range(4)] for m in range(4)])
    grad={name:mp.matrix([v[i],0,0,d[i]]) for name,i in zip(('u','v','r','psi','Z','T'),(9,10,11,12,13,14))}
    R3=ricci3(h,hz,hzz)[1]
    lie=mp.matrix(body.tensor([S[2]*d[j]+(sum(h[i,a]*Sz[a] for a in range(3)) if k==2 else 0)
                              +(sum(h[k,a]*Sz[a] for a in range(3)) if i==2 else 0)
                              for j,(i,k) in enumerate(((0,0),(0,1),(0,2),(1,1),(1,2),(2,2)))]))
    return dict(g=g,gi=gi,n=n,DN=Dn,Kraw=(ht-lie)/(2*N),hi=h**-1,R3=R3,coord_grad=grad,
                u=q[9],v=q[10],r=q[11],psi=q[12],Z=q[13],epsilon=q[15])


def calculate():
    mp.mp.dps=110;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def close(name,a,b):
        error=abs(a-b)/(1+abs(a)+abs(b));check(name,error<mp.mpf('1e-18'),show(error));return error
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path in (BACKEND,CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();engine=load('weak_action_original',ENGINE);engine.setup();mp.mp.dps=110
    body=engine.body;backend=load('full_original_weak',BACKEND);weak=backend.WeakAction(body,engine.par)
    metric=body.tensor;controls=[]
    for seed in range(4):
        A,dd=make_jet(seed);h=mp.matrix(metric(A[:16]));dh=mp.matrix(metric(A[32:48]));ddh=mp.matrix(metric(dd))
        R3tensor,R3,G=ricci3(h,dh,ddh);hi=h**-1;vol=mp.sqrt(mp.det(h));N,Nz=A[54:56];MP=engine.par['MP2']
        gg,B=weak.curvature(A[:16],A[32:48])
        def B_at(z):
            hh=h+z*dh+z*z*ddh/2;hhz=dh+z*ddh
            q=[hh[i,j] for i,j in backend.HM]+A[6:16]
            dq=[hhz[i,j] for i,j in backend.HM]+A[38:48]
            return weak.curvature(q,dq)[1]
        Bz=mp.diff(B_at,0)
        close('nonlinear_Ricci_divergence_'+str(seed),gg+Bz,vol*R3)
        ctx=coordinate_context(A,dd,body)
        reference=N*vol*body.canonical.mp_body(ctx,engine.par,mp.zeros(12,1),0,0,coordinate=True)
        L,normal=weak.density(A)
        bridge=close('original_full_coordinate_action_'+str(seed),L+MP*(Nz*B+N*Bz)/2,reference)
        Wz=A[32:48]+[mp.mpf(0)]*16+dd+A[51:54]+[mp.mpf(0)]*3+[Nz,mp.mpf(0)]
        HessN=mp.matrix([[-G[2][i][j]*Nz for j in range(3)] for i in range(3)])
        lapN=sum(hi[i,j]*HessN[i,j] for i in range(3) for j in range(3))
        target=-MP*vol*(N*hi*(R3tensor-h*R3/2)*hi+hi*lapN-hi*HessN*hi)/2
        _,cg=weak.gradient(A,curvature_only=True)
        for hs in ('1e-20','1e-26'):
            hz=weak.hv(A,Wz,mp.mpf(hs),curvature_only=True)
            for j,(a,b) in enumerate(backend.HM):
                close(f'curvature_metric_Euler_{seed}_{j}_{hs}',cg[j]-hz[32+j],target[a,b]*(1 if a==b else 2))
            close(f'curvature_lapse_Euler_{seed}_{hs}',cg[54]-hz[55],MP*vol*R3/2)
        check('reject_deleted_lapse_curvature_flux_'+str(seed),abs(MP*Bz/2)>mp.mpf('1e-18'),show(abs(MP*Bz/2)))
        _,grad=weak.gradient(A)
        direction=[mp.mpf((i+seed)%7-3)/(101+i) for i in range(56)]
        direct=mp.diff(lambda t:weak.density([a+t*d for a,d in zip(A,direction)])[0],0)
        close('full_real_first_variation_'+str(seed),direct,sum(grad[i]*direction[i] for i in range(56)))
        lapseA=A.copy();lapseA[54]=mp.mpf(1);lapseA[55]=mp.mpf(0)
        ll,nn=weak.density(lapseA);_,lg=weak.gradient(lapseA)
        E=sum(lg[16+j]*nn[j] for j in range(16))-ll
        close('lapse_energy_weight_'+str(seed),lg[54],-E)
        gamma=mp.sqrt(1+(mp.matrix(lapseA[6:9]).T*h*mp.matrix(lapseA[6:9]))[0])
        J=gamma*sum(hi[2,j]*lg[22+j] for j in range(3))
        close('lapse_flux_with_Ricci_boundary_'+str(seed),lg[55],J-MP*B/2)
        for i in range(3):
            close(f'shift_undifferentiated_{seed}_{i}',lg[48+i],-sum(lg[16+j]*lapseA[32+j] for j in range(16)) if i==2 else 0)
            expected=-sum(lg[16+slot]*((h[a,i] if b==2 else 0)+(h[b,i] if a==2 else 0)) for slot,(a,b) in enumerate(backend.HM))+lapseA[8]*lg[22+i]
            close(f'shift_gradient_{seed}_{i}',lg[51+i],expected)
        controls.append(dict(seed=seed,coordinate_bridge=show(bridge),Ricci=show(R3),curvature_boundary_flux=show(B)))
        print(json.dumps(dict(stage='full_weak_jet',seed=seed)),flush=True)
    # An exact nonflat conformal benchmark fixes the curvature divergence sign.
    a=mp.mpf(1)/7;z=mp.mpf(11)/13;f=a*mp.sin(z);fp=a*mp.cos(z);fpp=-a*mp.sin(z)
    h=mp.eye(3)*mp.exp(2*f);dh=2*fp*h;ddh=(2*fpp+4*fp*fp)*h
    q=[h[i,j] for i,j in backend.HM]+[mp.mpf(0)]*10
    dq=[dh[i,j] for i,j in backend.HM]+[mp.mpf(0)]*10
    gg,B=weak.curvature(q,dq)
    close('conformal_Ricci_analytic',ricci3(h,dh,ddh)[1],mp.exp(-2*f)*(-4*fpp-2*fp*fp))
    close('conformal_GammaGamma_analytic',gg,2*mp.exp(f)*fp*fp)
    close('conformal_boundary_flux_analytic',B,-4*mp.exp(f)*fp)
    # First variations remain meaningful at exact alignment, without a third cusp tensor.
    charge=load('weak_registered_initial',CHARGE);charge.setup();mp.mp.dps=110
    weak=backend.WeakAction(charge.en.body,charge.en.par)
    for orientation in (-1,1):
        theta=mp.pi/2 if orientation==-1 else 3*mp.pi/2
        old,vd,dd,Sdd=charge.state(theta);old[7]=old[21]=old[13]=old[27]=old[41]=old[44]=mp.mpf(0)
        old[35]=mp.mpf(orientation)*mp.mpf(2)/25;vd[7]=-charge.en.vals['H0']*old[35]
        dd[7]=0;dd[13]=2*charge.en.U*old[35]**2;Sdd=[mp.mpf(0)]*3
        Wz=old[28:42]+vd+dd+old[45:48]+Sdd
        L,g=charge.en.gradient(old);_,normal=charge.en.density(old)
        hz=charge.en.hv(old,Wz,mp.mpf('1e-26'));rho=-sum(g[14+j]*normal[j] for j in range(14))+L-hz[22]
        A=old[:14]+[mp.mpf(0),rho]+old[14:28]+[mp.mpf(1),mp.mpf(0)]+old[28:42]+[mp.mpf(0)]*2+old[42:48]+[mp.mpf(1),mp.mpf(0)]
        _,grad=weak.gradient(A);direction=[mp.mpf((j+2)%5-2)/(137+j) for j in range(56)]
        observed=mp.diff(lambda t:weak.density([a+t*d for a,d in zip(A,direction)])[0],0)
        close('exact_alignment_first_variation_'+str(orientation),observed,sum(a*b for a,b in zip(grad,direction)))
        close('exact_initial_dust_multiplier_'+str(orientation),grad[15],0)
        close('exact_initial_dust_clock_momentum_'+str(orientation),grad[30],rho)
        check('node_positive_dust_'+str(orientation),rho>0,show(rho))
    # Actual registered-weight inverse countersequence; not admitted physical probes.
    y=s.Symbol('y',real=True);phi=(1-y*y)**4
    I0=s.integrate(phi**2,(y,-1,1));I4=s.integrate(y**4*phi**2,(y,-1,1))
    b=s.Rational(5,44);ee=s.Rational(1,500);kk=s.Integer(40)
    n=s.Symbol('n',positive=True)
    check('source_bound_tends_zero',s.limit(I4/n**3,n,s.oo)==0,str(I4))
    check('divided_rate_norm_diverges',s.limit(n*I0/(b*ee**2)**2,n,s.oo)==s.oo,str(I0))
    for nv in (2,4,8,16):
        bn=mp.mpf(5)/44;en=mp.mpf(1)/500
        source2=mp.quad(lambda yy:mp.sin(yy/nv)**4*(1-yy*yy)**8,[-1,0,1])*nv
        bound=(mp.mpf(int(I4.p))/int(I4.q))/nv**3
        check('registered_weight_source_bound_'+str(nv),source2<=bound,show(source2))
        qnorm2=nv*(mp.mpf(int(I0.p))/int(I0.q))/(bn*en*en)**2
        close('registered_weight_quotient_norm_'+str(nv),mp.quad(lambda yy:(nv/(bn*en*en)*(1-yy*yy)**4)**2,[-1,0,1])/nv,qnorm2)
    # A moving interface contributes a'[Pi]-[F] to Lq-DtPi-DzF.
    speed,jumpP,jumpF=s.symbols('speed jumpP jumpF')
    condition=jumpF-speed*jumpP
    check('moving_interface_stationarity',s.simplify(speed*jumpP-jumpF+condition)==0)
    check('reject_fixed_interface_shortcut',s.diff(condition,speed)==-jumpP)
    verify()
    return dict(result_id='R4C1-FULL-WEAK-ACTION-V1',source_sha256=pins,checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),controls=controls,
                formulas=dict(Euler='L_q-Dt(L_v)-Dz(L_d)=0; retain multiplier equation',
                              constraints='E_N=L_N-Dz(L_Nz); E_S=L_S-Dz(L_Sz)',
                              curvature='N sqrt(h) R3=N L_GammaGamma-Nz B+Dz(N B)',
                              Hperp='E_weak+Dz(J-MP2 B/2) at N=1,Nz=0, including dust',
                              interface='[L_d]-node_speed*[L_v]=0, absent a declared surface source',
                              inverse_source_norm_squared_bound=str(I4/n**3),
                              inverse_rate_norm_squared=str(n*I0/(b*ee**2)**2),
                              countersequence='xi=k(z-z_node), g=b e^2 sin(xi)^2; f_n=n sin(xi)^2 phi(n xi), phi(y)=(1-y^2)^4 on |y|<=1'),
                working_digits=110,mpmath=mp.__version__,sympy=s.__version__,
                variational_backend_only=True,evolved_domain_invariance_proved=False,
                time_evolution=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        if (args.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);p=args.output/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
