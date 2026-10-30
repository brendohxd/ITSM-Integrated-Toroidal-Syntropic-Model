"""Normalized-frame off-shell Ward identity and conditional transport only."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_quartic_vector_node_jets_v1_attempt_01/summary.json'
PSHA='8995885054f651a0d2d9d5344e98ac1a6345019d901ad3d65e0cd23b96122b97'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NORMALIZED_ADM_WARD_V1_CONTRACT_2026-10-28.md'
CANON='Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py'
CSHA='4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada'
EXTRA={CANON:CSHA,
 'Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_attempt_02/summary.json':'ba203bf4c29ddf7834c5db2c2a7a98625343508ed3f24025a56b90438020d44b',
 'Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_backend_attempt_01/verification.json':'97d4ca6c7dbe6a7af27e21529d40532944cffb8f5d92f9781a52708b3391557a',
 'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
 'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md':'4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c'}
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)


def symbolic(check):
    N,gam=s.symbols('N gamma',positive=True)
    S=s.Matrix(s.symbols('S0:3',real=True));V=s.Matrix(s.symbols('V0:3',real=True))
    aN=s.Symbol('advN');aS=s.Matrix(s.symbols('advS0:3'));aV=s.Matrix(s.symbols('advV0:3'))
    ah=s.Matrix(3,3,lambda i,j:s.Symbol('advh'+str(min(i,j))+str(max(i,j))))
    D=s.Matrix(4,4,lambda a,b:s.Symbol('xi'+str(b)+'_'+str(a)))
    def reduce(x):
        num,den=s.fraction(s.cancel(s.expand(x)))
        return s.factor(s.Poly(num,gam).rem(s.Poly(gam**2-1-(V.T*V)[0],gam)).as_expr())/den
    def exact(name,x):
        rows=list(x) if isinstance(x,s.MatrixBase) else [x]
        bad=[str(t) for z in rows if (t:=reduce(z))!=0]
        check(name,not bad,bad)
    met=s.eye(4);met[0,0]=-N*N+(S.T*S)[0]
    gi=s.eye(4);gi[0,0]=-1/N**2
    for i in range(3):
        met[0,i+1]=met[i+1,0]=S[i]
        gi[0,i+1]=gi[i+1,0]=S[i]/N**2
        for j in range(3):gi[i+1,j+1]=int(i==j)-S[i]*S[j]/N**2
    advg=s.zeros(4);advg[0,0]=-2*N*aN+(S.T*ah*S)[0]+2*(S.T*aS)[0]
    for i in range(3):
        advg[0,i+1]=advg[i+1,0]=(ah*S)[i]+aS[i]
        for j in range(3):advg[i+1,j+1]=ah[i,j]
    delta_g=advg+D*met+met*D.T
    delta_gi=-gi*delta_g*gi
    delta_N=s.expand(N**3*delta_gi[0,0]/2)
    delta_S=s.Matrix([2*N*delta_N*gi[0,i+1]+N*N*delta_gi[0,i+1] for i in range(3)])
    n=s.Matrix([gam/N,*list(V-S*gam/N)])
    ag=((V.T*ah*V)[0]+2*(V.T*aV)[0])/(2*gam)
    an0=ag/N-gam*aN/N**2
    advn=s.Matrix([an0,*list(aV-S*an0-aS*gam/N)])
    delta_n=advn-D.T*n
    delta_V=s.Matrix([delta_n[i+1]+S[i]*delta_n[0]+n[0]*delta_S[i] for i in range(3)])
    want_N=aN+N*D[0,0]-N*sum(S[j]*D[j+1,0] for j in range(3))
    want_S=s.Matrix([aS[i]+D[0,i+1]-sum(S[j]*D[j+1,i+1] for j in range(3))
                      +S[i]*D[0,0]-sum((N*N*int(i==j)+S[i]*S[j])*D[j+1,0] for j in range(3)) for i in range(3)])
    want_V=s.Matrix([aV[i]-sum(V[j]*D[j+1,i+1] for j in range(3))
                      -sum((N*gam*int(i==j)+S[i]*V[j])*D[j+1,0] for j in range(3)) for i in range(3)])
    want_h=s.Matrix(3,3,lambda i,j:ah[i,j]+D[i+1,j+1]+D[j+1,i+1]+S[i]*D[j+1,0]+S[j]*D[i+1,0])
    exact('arbitrary_ADM_lapse_Lie_map',delta_N-want_N)
    exact('arbitrary_ADM_shift_Lie_map',delta_S-want_S)
    exact('normalized_frame_foliation_Lie_map',delta_V-want_V)
    exact('spatial_metric_Lie_map',delta_g[1:4,1:4]-want_h)
    exact('unit_chart_constraint',(n.T*met*n)[0]+1)
    J=n.jacobian(V)
    exact('unit_chart_vector_tangent',(n.T*met*J))
    exact('tangent_frame_Gram',J.T*met*J-(s.eye(3)-V*V.T/gam**2))
    exact('full_unit_tangent_projector',J*(s.eye(3)+V*V.T)*J.T-gi-n*n.T)
    exact('metric_induced_unit_variation',(n.T*delta_g*n)[0]+2*(n.T*met*delta_n)[0])
    F=s.Matrix(s.symbols('F0:4'));lam=s.Symbol('lambda_U')
    exact('unit_multiplier_drops_only_tangent_equation',J.T*(F+lam*met*n)-J.T*F)
    exact('radial_multiplier_reconstruction',(n.T*(F+(n.T*F)[0]*met*n))[0])
    # Euler-density integration by parts, in full 3D with arbitrary off-shell residues.
    coords=s.symbols('t x y z');t,*xx=coords
    fn=lambda name:s.Function(name)(*coords)
    NN=fn('N');gg=fn('gamma');SS=[fn('S'+str(i)) for i in range(3)]
    VV=[fn('V'+str(i)) for i in range(3)]
    hh=s.Matrix(3,3,lambda i,j:fn('h'+str(min(i,j))+str(max(i,j))))
    hi=s.Matrix(3,3,lambda i,j:fn('hi'+str(min(i,j))+str(max(i,j))))
    EE=s.Matrix(3,3,lambda i,j:fn('Eh'+str(min(i,j))+str(max(i,j))))
    EV=[fn('EV'+str(i)) for i in range(3)]
    scalars=[fn(n) for n in ('u','v','r','psi','Z','tau','epsilon')]
    EF=[fn('E'+str(i)) for i in range(len(scalars))]
    H=fn('Hperp');CC=[fn('C'+str(i)) for i in range(3)]
    Slo=list(hh*s.Matrix(SS))
    A=[NN*SS[j]*H+sum((NN**2*hi[i,j]+SS[i]*SS[j])*CC[i]+2*Slo[i]*EE[i,j]
                      -(NN*gg*hi[i,j]+SS[i]*VV[j])*EV[i] for i in range(3)) for j in range(3)]
    F0=(-H*s.diff(NN,t)-sum(CC[i]*s.diff(SS[i],t) for i in range(3))
        +sum(EE[i,j]*s.diff(hh[i,j],t) for i in range(3) for j in range(3))
        +sum(EV[i]*s.diff(VV[i],t) for i in range(3))+sum(a*s.diff(f,t) for a,f in zip(EF,scalars)))
    W0=F0+s.diff(NN*H+sum(SS[i]*CC[i] for i in range(3)),t)-sum(s.diff(A[j],xx[j]) for j in range(3))
    Wi=[];RC=[]
    for k in range(3):
        Fk=(-H*s.diff(NN,xx[k])-sum(CC[i]*s.diff(SS[i],xx[k]) for i in range(3))
            +sum(EE[i,j]*s.diff(hh[i,j],xx[k]) for i in range(3) for j in range(3))
            +sum(EV[i]*s.diff(VV[i],xx[k]) for i in range(3))+sum(a*s.diff(f,xx[k]) for a,f in zip(EF,scalars)))
        Wk=Fk+s.diff(CC[k],t)-sum(s.diff(SS[j]*CC[k]+sum(2*hh[i,k]*EE[i,j] for i in range(3))-VV[j]*EV[k],xx[j]) for j in range(3))
        residue=(-sum(EE[i,j]*s.diff(hh[i,j],xx[k]) for i in range(3) for j in range(3))
                 -sum(EV[i]*s.diff(VV[i],xx[k]) for i in range(3))-sum(a*s.diff(f,xx[k]) for a,f in zip(EF,scalars))
                 +sum(s.diff(sum(2*hh[i,k]*EE[i,j] for i in range(3))-VV[j]*EV[k],xx[j]) for j in range(3)))
        target=s.diff(CC[k],t)-sum(s.diff(SS[j]*CC[k],xx[j]) for j in range(3))-H*s.diff(NN,xx[k])-sum(CC[i]*s.diff(SS[i],xx[k]) for i in range(3))-residue
        check('off_shell_momentum_Ward_'+str(k),s.expand(Wk-target)==0)
        Wi.append(Wk);RC.append(residue)
    Lieh=s.Matrix(3,3,lambda i,j:sum(SS[k]*s.diff(hh[i,j],xx[k])+hh[i,k]*s.diff(SS[k],xx[j])+hh[j,k]*s.diff(SS[k],xx[i]) for k in range(3)))
    K=(hh.diff(t)-Lieh)/(2*NN)
    X=[(s.diff(VV[i],t)-sum(SS[j]*s.diff(VV[i],xx[j])-VV[j]*s.diff(SS[i],xx[j]) for j in range(3))
         +sum(gg*hi[i,j]*s.diff(NN,xx[j]) for j in range(3)))/NN for i in range(3)]
    hat=[(s.diff(f,t)-sum(SS[j]*s.diff(f,xx[j]) for j in range(3)))/NN for f in scalars]
    TH=(s.diff(H,t)-sum(s.diff(SS[j]*H,xx[j]) for j in range(3))
        -sum(s.diff(NN**2*hi[i,j]*CC[i],xx[j]) for i in range(3) for j in range(3))/NN
        +sum(2*K[i,j]*EE[i,j] for i in range(3) for j in range(3))+sum(X[i]*EV[i] for i in range(3))
        +sum(a*b for a,b in zip(hat,EF))+sum(s.diff(gg*hi[i,j]*EV[i],xx[j]) for i in range(3) for j in range(3)))
    check('off_shell_normalized_Hamiltonian_Ward',s.expand(W0-sum(SS[k]*Wi[k] for k in range(3))-NN*TH)==0)
    check('reject_frame_as_spacetime_scalars',s.simplify(want_V[0]-aV[0])!=0)
    check('reject_missing_vector_divergence',s.diff(s.Rational(5,4)*xx[0],xx[0])!=0,'5/4 nonzero residual witness')
    # Exact periodic energy controls for the conditional N=1 subsystem.
    z=s.Symbol('z',real=True)
    shift=s.Matrix([s.sin(z)/5,s.cos(2*z)/7,s.sin(z)/11])
    con=s.Matrix([s.cos(z)+s.Rational(1,4),s.sin(2*z),1+s.cos(z)/3])
    div=s.diff(shift[2],z)
    evolution=shift[2]*con.diff(z)+div*con+s.Matrix([0,0,(con.T*shift.diff(z))[0]])
    integral=lambda expr:s.integrate(s.expand_trig(s.expand(expr)),(z,-s.pi,s.pi))
    energy_rate=integral((con.T*evolution)[0])
    expected=integral(div*(con.T*con)[0]/2+con[2]*(con.T*shift.diff(z))[0])
    check('periodic_momentum_energy_identity',s.simplify(energy_rate-expected)==0,str(energy_rate))
    hc=1+s.cos(z)/7;hd=shift[2]*s.diff(hc,z)+div*hc
    check('periodic_zero_momentum_H_energy_identity',s.simplify(integral(hc*hd)-integral(div*hc*hc/2))==0)
    nmode=s.Symbol('n',positive=True,integer=True);amp=1/s.sqrt(nmode)
    check('reject_combined_L2_derivative_control',s.limit(amp,nmode,s.oo)==0 and s.limit(nmode*amp,nmode,s.oo)==s.oo)
    return dict(lapse_variation=str(want_N),shift_variation=[str(x) for x in want_S],frame_variation=[str(x) for x in want_V],
                off_shell_H=str(TH),off_shell_C=[str(x) for x in Wi],
                momentum_L2_squared_rate_bound='(||div S||inf+2||sym dS||op,inf)*||C||L2^2',
                H_L2_squared_rate_bound_when_C_zero='||div S||inf*||Hperp||L2^2')


def geometry(g,dg,ddg):
    gi=g**-1
    F=lambda a,b,c:dg[b][a,c]+dg[c][a,b]-dg[a][b,c]
    conn=[[[sum(gi[a,r]*F(r,b,c) for r in range(4))/2 for c in range(4)] for b in range(4)] for a in range(4)]
    dgi=[-gi*d*gi for d in dg]
    dc=[[[[sum(dgi[m][a,r]*F(r,b,c)+gi[a,r]*(ddg[m][b][r,c]+ddg[m][c][r,b]-ddg[m][r][b,c]) for r in range(4))/2
             for c in range(4)] for b in range(4)] for a in range(4)] for m in range(4)]
    ric=mp.matrix(4)
    for b in range(4):
        for c in range(4):
            ric[b,c]=sum(dc[a][a][b][c]-dc[c][a][b][a]
                         +sum(conn[a][a][r]*conn[r][b][c]-conn[a][c][r]*conn[r][b][a] for r in range(4)) for a in range(4))
    return gi,conn,sum(gi[b,c]*ric[b,c] for b in range(4) for c in range(4))


def covariant(data,par):
    g,dg,ddg,U,dU,fields,grad=data
    gi,conn,R=geometry(g,dg,ddg)
    ell=mp.sqrt(-(U.T*g*U)[0]);n=U/ell
    dell=[-((U.T*dg[m]*U)[0]+2*(U.T*g*dU[m,:].T)[0])/(2*ell) for m in range(4)]
    dn=mp.matrix([[dU[m,a]/ell-U[a]*dell[m]/ell**2 for a in range(4)] for m in range(4)])
    DU=mp.matrix([[dU[m,a]+sum(conn[a][m][b]*U[b] for b in range(4)) for a in range(4)] for m in range(4)])
    Dn=mp.matrix([[dn[m,a]+sum(conn[a][m][b]*n[b] for b in range(4)) for a in range(4)] for m in range(4)])
    acc=DU.T*U;an=Dn.T*n;hp=gi+n*n.T
    I1=sum(gi[i,j]*g[a,b]*DU[i,a]*DU[j,b] for i in range(4) for j in range(4) for a in range(4) for b in range(4))
    Lu=-par['MU2']*(par['c1']*I1+par['c2']*sum(DU[i,i] for i in range(4))**2
                    +par['c3']*sum(DU[i,j]*DU[j,i] for i in range(4) for j in range(4))
                    -par['c4']*(acc.T*g*acc)[0])/2
    current=fields['v']*grad['u']-fields['u']*grad['v']
    Q=(n.T*grad['psi'])[0];Y=(grad['psi'].T*hp*grad['psi'])[0]
    ss=fields['u']**2+fields['v']**2
    pot=(par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)
         +par['mr2']*fields['r']**2/2+par['lambda_r']*fields['r']**4/4+par['g_r']*ss*fields['r']**2/4+par['rho_Lambda'])
    C=mp.exp(par['beta']*fields['psi'])
    pieces=dict(Einstein=par['MP2']*R/2,frame=Lu,
                unit_multiplier=fields['lambda']*((U.T*g*U)[0]+1)/2,
                alignment=-par['zeta']*(current.T*hp*current)[0]/2,
                force=par['K_Q']*Q*Q/2-par['A']*Y**mp.mpf('1.5'),
                regulator=par['b']*fields['Z']**2/2-par['b']*(grad['Z'].T*hp*grad['psi'])[0]-par['b']*fields['Z']*(an.T*grad['psi'])[0],
                canonical=-sum((grad[f].T*gi*grad[f])[0] for f in ('u','v','r'))/2,
                potential=-pot,dust=-fields['epsilon']*(C*C*(grad['T'].T*gi*grad['T'])[0]+C**4)/2)
    volume=mp.sqrt(-mp.det(g))
    return {k:volume*v for k,v in pieces.items()},dict(gi=gi,conn=conn,ell=ell,n=n,Dn=Dn,Y=Y)


def make_jet(seed):
    rat=lambda a,b:mp.mpf(a)/b
    N=rat(6+seed,5);S=mp.matrix([rat(1,19),-rat(1,23),rat(1,29)])
    h=mp.matrix([[rat(6,5),rat(1,31),rat(1,37)],[rat(1,31),rat(11,10),-rat(1,41)],[rat(1,37),-rat(1,41),rat(9,10)]])
    V=mp.matrix([rat(1,10),rat(1+seed,33),-rat(1,43)]);gam=mp.sqrt(1+(V.T*h*V)[0])
    g=mp.zeros(4);g[0,0]=-N*N+(S.T*h*S)[0]
    for i in range(3):
        g[0,i+1]=g[i+1,0]=(h*S)[i]
        for j in range(3):g[i+1,j+1]=h[i,j]
    U=mp.matrix([gam/N,*list(V-S*gam/N)])*rat(7+seed,6)
    dg=[mp.matrix([[rat(((a+1)*(i+j+2)+seed)%11-5,131+a) for j in range(4)] for i in range(4)]) for a in range(4)]
    ddg=[[mp.matrix([[rat(((a+b+2)*(i+j+2)+seed)%13-6,401+a+b) for j in range(4)] for i in range(4)]) for b in range(4)] for a in range(4)]
    dU=mp.matrix([[rat(((a+1)*(i+2)+seed)%9-4,97+a) for i in range(4)] for a in range(4)])
    fields=dict(u=rat(2,5),v=rat(3,5),r=rat(1,7),psi=rat(1,9),Z=rat(2,7),epsilon=rat(7,100),**{'lambda':rat(3,17)})
    grad={name:mp.matrix([rat(2+j,23)]+[rat((i+j+seed)%5-2,113+i*2) for i in range(3)]) for j,name in enumerate(('u','v','r','psi','Z','T'))}
    return [g,dg,ddg,U,dU,fields,grad]


def lie_direction(data,seed,omit_connection=False):
    g,dg,ddg,U,dU,fields,grad=data
    rat=lambda a,b:mp.mpf(a)/b
    D=mp.matrix([[rat((a+2*b+seed)%7-3,31+a+b) for b in range(4)] for a in range(4)])
    DD=[[[rat((a+b+2*c+seed)%9-4,71+a+b+c) for c in range(4)] for b in range(4)] for a in range(4)]
    DDD=[[[[rat((a+b+c+2*d+seed)%11-5,211+a+b+c+d) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    delta_g=D*g+g*D.T
    delta_dg=[mp.matrix([[sum(D[m,c]*dg[c][a,b]+dg[m][c,b]*D[a,c]+g[c,b]*DD[m][a][c]
                                +dg[m][a,c]*D[b,c]+g[a,c]*DD[m][b][c] for c in range(4)) for b in range(4)] for a in range(4)]) for m in range(4)]
    delta_ddg=[]
    for m in range(4):
        row=[]
        for nn in range(4):
            mat=mp.matrix(4)
            for a in range(4):
                for b in range(4):
                    mat[a,b]=sum(DD[m][nn][c]*dg[c][a,b]+D[m,c]*ddg[nn][c][a,b]+D[nn,c]*ddg[m][c][a,b]
                                 +ddg[m][nn][c,b]*D[a,c]+dg[nn][c,b]*DD[m][a][c]+dg[m][c,b]*DD[nn][a][c]+g[c,b]*DDD[m][nn][a][c]
                                 +ddg[m][nn][a,c]*D[b,c]+dg[nn][a,c]*DD[m][b][c]+dg[m][a,c]*DD[nn][b][c]+g[a,c]*DDD[m][nn][b][c] for c in range(4))
            row.append(mat)
        delta_ddg.append(row)
    delta_U=-D.T*U
    delta_dU=mp.matrix([[sum(D[m,c]*dU[c,a]-dU[m,c]*D[c,a]-(0 if omit_connection else U[c]*DD[m][c][a]) for c in range(4)) for a in range(4)] for m in range(4)])
    delta_grad={name:D*value for name,value in grad.items()}
    return [delta_g,delta_dg,delta_ddg,delta_U,delta_dU,{k:mp.mpf(0) for k in fields},delta_grad],sum(D[i,i] for i in range(4))


def shifted(data,direction,amount):
    g,dg,ddg,U,dU,fields,grad=data
    ag,adg,addg,aU,adU,af,agrad=direction
    return [g+amount*ag,[a+amount*b for a,b in zip(dg,adg)],
            [[ddg[m][n]+amount*addg[m][n] for n in range(4)] for m in range(4)],
            U+amount*aU,dU+amount*adU,{k:v+amount*af[k] for k,v in fields.items()},
            {k:v+amount*agrad[k] for k,v in grad.items()}]


def calculate():
    mp.mp.dps=110
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def close(name,a,b):
        err=abs(a-b)/(1+abs(a)+abs(b));check(name,err<mp.mpf('1e-18'),show(err));return err
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('owning receipt drift')
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path,want in EXTRA.items():
        if path in pins and pins[path]!=want:raise ValueError('inherited source mismatch '+path)
        pins[path]=want
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();formulas=symbolic(check)
    print('SYMBOLIC_NORMALIZED_WARD_COMPLETE',flush=True)
    spec=importlib.util.spec_from_file_location('ward_original_canonical',ROOT/CANON)
    canon=importlib.util.module_from_spec(spec);spec.loader.exec_module(canon)
    par=canon.parameters('new_B1_frame','1/4','mp');controls=[]
    for seed in range(4):
        data=make_jet(seed);values,geo=covariant(data,par)
        check('smooth_control_domain_'+str(seed),geo['ell']>mp.mpf('0.5') and geo['Y']>0)
        direction,tr=lie_direction(data,seed)
        errors=[]
        for hs in ('1e-20','1e-26'):
            step=mp.mpf(hs);perturbed,_=covariant(shifted(data,direction,mp.j*step),par)
            for name,value in values.items():
                observed=mp.im(perturbed[name])/step;expected=tr*value
                errors.append(close(f'covariant_Lie_{seed}_{name}_{hs}',observed,expected))
        wrong,_=lie_direction(data,seed,omit_connection=True)
        bad,_=covariant(shifted(data,wrong,mp.j*mp.mpf('1e-26')),par)
        rejection=max(abs(mp.im(bad[n])/mp.mpf('1e-26')-tr*values[n])/(1+abs(values[n])) for n in ('frame','regulator'))
        check('reject_omitted_inhomogeneous_vector_jet_'+str(seed),rejection>mp.mpf('1e-18'),show(rejection))
        # Independent pinned coordinate contraction bridge on the unit chart.
        g,dg,ddg,U,dU,fields,grad=data
        n=geo['n'];conn=geo['conn'];dn=mp.matrix([[geo['Dn'][m,a]-sum(conn[a][m][b]*n[b] for b in range(4)) for a in range(4)] for m in range(4)])
        unit=[g,dg,ddg,n,dn,fields,grad];unit_values,unit_geo=covariant(unit,par)
        c=dict(g=g,gi=unit_geo['gi'],n=n,DN=unit_geo['Dn'],Kraw=mp.zeros(3),hi=g[1:4,1:4]**-1,
               R3=mp.mpf(0),coord_grad=grad,**{k:fields[k] for k in ('u','v','r','psi','Z','epsilon')})
        reference=canon.mp_body(c,par,mp.zeros(12,1),0,0,coordinate=True)
        own=sum(value for name,value in unit_values.items() if name not in ('Einstein','unit_multiplier'))
        bridge=close('original_coordinate_density_bridge_'+str(seed),own,mp.sqrt(-mp.det(g))*reference)
        controls.append(dict(seed=seed,max_Lie_error=show(max(errors)),connection_rejection=show(rejection),bridge_error=show(bridge),
                             ell=show(geo['ell']),Y=show(geo['Y'])))
        print(json.dumps(dict(stage='covariant_jet_complete',seed=seed)),flush=True)
    verify()
    return dict(result_id='R4C1-NORMALIZED-ADM-WARD-V1',source_sha256=pins,checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),formulas=formulas,controls=controls,
                working_digits=110,mpmath=mp.__version__,sympy=s.__version__,
                smooth_normalized_Ward_derived=all(c['passed'] for c in checks),
                constraint_propagation='CONDITIONAL_ON_EXISTING_EULER_SOLUTION_AND_VALID_WEAK_INTERFACES_UNIT_LAPSE',
                weak_extension_certified=False,time_evolution=False,G1_complete=False,physics_pass=False,
                gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        if (args.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);path=args.output/'summary.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
