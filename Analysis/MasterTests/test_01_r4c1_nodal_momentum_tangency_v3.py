"""High-precision initial first variations; never a frozen-envelope Hessian."""
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

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
OLD='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v1.py'
OLD_SHA='77b8b7d45ca9ea6b16fbea175c162ca98355382bf72b1ee26026b97437181a08'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V3_WEIGHT_ADDENDUM_2026-10-20.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/OLD).read_bytes())!=OLD_SHA:raise ValueError('V1 source drift')
spec=importlib.util.spec_from_file_location('frozen_initial_momentum_v1',ROOT/OLD)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
lift,nodal,canonical,base=old.lift,old.nodal,old.canonical,old.base
PINS=dict(old.PINS)
PINS.update({
 'Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v2.py':'4dd1be8d7cfe8877841b380227c2c24f2d41ed1146ccf12781cdd28881f2e253',
 'Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V2_PRECISION_CONTRACT_2026-10-20.md':'cb960191f1a9270613c2f2c03fa82986ccae351d48a979115fc8c72e3d8da964',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_02/summary.json':'6cad75fa82d4bf9cc64074f834837910aedc9ccc69e6c8f2ce604c967293aabc',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_02/independent.json':'68eb656f7321da43e05e2b4467c94021061b71638275fa369d16ff67df78d3b7',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_02/formulas.json':'a99cedccfa53fb81492dbe7bc43b048ca8d29294050dd2dea95d90b5b750bd5f'})
PINS.update({OLD:OLD_SHA,CONTRACT:'df86efc15fa0ae37957114909309df5772592b4abd629269928e967fddb59032',
 'Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V1_REPORT_2026-10-20.md':
 'd71b05ae29f5042ba13a7dcf00f2047e1dce03a6fc5f5665bdd603798bfc3f4d',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_01/summary.json':
 '69270f59143ef1a381074c1851aaef0d99836ac3a459ff61af2ac3145d63f4b3',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_01/independent.json':
 '15330fbfe01c1ef4aefe953282390373a04b18cad5017b20e408675c37d42a09'})
_PROGRESS=None
STEPS=('1e-18','1e-22')

def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};records={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0].lower()!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();records[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    return pins,records

def val(x):return x.v if isinstance(x,Node) else x

class Tape:
    def __init__(self):self.nodes=[]
    def var(self,x):return Node(self,x,())
    def grad(self,root,variables):
        for q in self.nodes:q.a=mp.mpf(0)
        if isinstance(root,Node):
            root.a=mp.mpf(1)
            for q in reversed(self.nodes):
                if q.a:
                    for parent,weight in q.parents:parent.a+=q.a*weight
        return [q.a if isinstance(q,Node) else mp.mpf(0) for q in variables]

class Node:
    __slots__=('t','v','parents','a')
    def __init__(self,t,v,parents):
        self.t=t;self.v=v;self.parents=parents;self.a=mp.mpf(0);t.nodes.append(self)
    def __add__(self,b):
        if not isinstance(b,Node) and b==0:return self
        return Node(self.t,self.v+val(b),((self,mp.mpf(1)),)+(((b,mp.mpf(1)),) if isinstance(b,Node) else ()))
    __radd__=__add__
    def __neg__(self):return Node(self.t,-self.v,((self,mp.mpf(-1)),))
    def __sub__(self,b):return mp.mpf(0) if b is self else self+(-b)
    def __rsub__(self,b):return b+(-self)
    def __mul__(self,b):
        if not isinstance(b,Node) and b==0:return mp.mpf(0)
        return Node(self.t,self.v*val(b),((self,val(b)),)+(((b,self.v),) if isinstance(b,Node) else ()))
    __rmul__=__mul__
    def __truediv__(self,b):
        z=val(b)
        return Node(self.t,self.v/z,((self,mp.mpf(1)/z),)+(((b,-self.v/z**2),) if isinstance(b,Node) else ()))
    def __rtruediv__(self,b):return Node(self.t,b/self.v,((self,-b/self.v**2),))
    def __pow__(self,e):
        if isinstance(e,Node):raise TypeError('variable exponent not supported')
        if e==0:return mp.mpf(1)
        if self.v==0 and e>1:weight=mp.mpf(0)
        else:weight=e*self.v**(e-1)
        return Node(self.t,self.v**e,((self,weight),))

def unary(fn,df,x):
    return Node(x.t,fn(x.v),((x,df(x.v)),)) if isinstance(x,Node) else fn(x)
def sqrt(x):return x**mp.mpf('.5')
def sin(x):return unary(mp.sin,mp.cos,x)
def cos(x):return unary(mp.cos,lambda z:-mp.sin(z),x)
def exp(x):return unary(mp.exp,mp.exp,x)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(A,b):return [dot(r,b) for r in A]
def tr(A):return sum(A[i][i] for i in range(len(A)))
def trans(A):return [list(x) for x in zip(*A)]
def mm(A,B):return [[dot(r,c) for c in trans(B)] for r in A]
def mean(x):return sum(x)/len(x)
def det3(A):
    a,b,c=A[0];d,e,f=A[1];g,h,i=A[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
def inv3(A):
    a,b,c=A[0];d,e,f=A[1];g,h,i=A[2];z=det3(A)
    return [[(e*i-f*h)/z,(c*h-b*i)/z,(b*f-c*e)/z],
            [(f*g-d*i)/z,(a*i-c*g)/z,(c*d-a*f)/z],
            [(d*h-e*g)/z,(b*g-a*h)/z,(a*e-b*d)/z]]
def tensor(q):return [[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
def Dmul(A,x):return [dot(r,[a-x[0] for a in x]) for r in A]

def geometry(q,dq):
    h=tensor(q);hi=inv3(h);dh=tensor(dq);V=q[6:9]
    G=[[[sum(hi[k][l]*((dh[l][j] if i==2 else 0)+(dh[l][i] if j==2 else 0)
        -(dh[i][j] if l==2 else 0))/2 for l in range(3)) for j in range(3)] for i in range(3)] for k in range(3)]
    DV=[[(dq[6+j] if i==2 else 0)+sum(G[j][i][k]*V[k] for k in range(3)) for j in range(3)] for i in range(3)]
    volume=sqrt(det3(h));gam=sqrt(1+dot(V,mv(h,V)))
    return h,hi,DV,volume,gam

def body(q,dq,y,s,par,R3=0):
    """Original normalized-frame scalar density; independent list contractions."""
    h,hi,DV,volume,gam=geometry(q,dq);V=q[6:9];K=tensor(y[:6])
    hv=mv(h,V);kv=mv(K,V);a=[x+z for x,z in zip(y[6:9],mv(hi,kv))]
    B=[[0]*4 for _ in range(4)];B[0][0]=dot(V,mv(h,a))/gam
    for j in range(3):B[0][j+1]=a[j]
    khi=mm(K,hi)
    for i in range(3):
        B[i+1][0]=dot(hv,DV[i])/gam+kv[i]
        for j in range(3):B[i+1][j+1]=DV[i][j]+gam*khi[i][j]
    g=[[0]*4 for _ in range(4)];gi=[[0]*4 for _ in range(4)];g[0][0]=gi[0][0]=-1
    for i in range(3):
        for j in range(3):g[i+1][j+1],gi[i+1][j+1]=h[i][j],hi[i][j]
    n=[gam]+list(V);hp=[[gi[i][j]+n[i]*n[j] for j in range(4)] for i in range(4)]
    acc=mv(trans(B),n)
    I1=tr(mm(mm(mm(gi,B),g),trans(B)))
    frame=-par['MU2']*(par['c1']*I1+par['c2']*tr(B)**2+par['c3']*tr(mm(B,B))-par['c4']*dot(acc,mv(g,acc)))/2
    gp=[s,0,0,dq[12]];gz=[0,0,0,dq[13]]
    gu=[[y[9+j],0,0,dq[9+j]] for j in range(3)]
    current=[q[10]*gu[0][i]-q[9]*gu[1][i] for i in range(4)]
    Y=dot(gp,mv(hp,gp))
    force=par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')
    reg=par['b']*q[13]**2/2-par['b']*(dot(gz,mv(hp,gp))+q[13]*dot(acc,gp))
    align=-par['zeta']*dot(current,mv(hp,current))/2
    can=-sum(dot(v,mv(gi,v)) for v in gu)/2
    ss=q[9]**2+q[10]**2
    pot=(par['m2']*ss/2+par['lambda4']*ss**2/8+par['lambda6']*ss**3/(24*par['Lambda']**2)
         +par['mr2']*q[11]**2/2+par['lambda_r']*q[11]**4/4+par['g_r']*ss*q[11]**2/4+par['rho_Lambda'])
    km=mm(hi,K);adm=par['MP2']*(tr(mm(km,km))-tr(km)**2+R3)/2
    return adm+frame+force+reg+align+can-pot

def local_derivatives(q,dq,y,s,par):
    tape=Tape();v=[tape.var(z) for z in list(y)+[s]]
    L=body(q,dq,v[:12],v[12],par)
    return val(L),tape.grad(L,v)

def build_data(point,initial,n,offset,precision):
    mp.mp.dps=precision;mp.iv.dps=80
    par,vals,H,U,Ud,g8,g12=lift.setup(point,initial)
    e=mp.mpf(1)/500;k=mp.mpf(40);s=vals['p'];Rc=vals['Rc'];HB=vals['H0']
    theta=[(1 if offset==0 else 3)*mp.pi/2+2*mp.pi*j/n for j in range(n)]
    sine=[mp.mpf(1 if offset==0 else -1) if j==0 else mp.sin(t) for j,t in enumerate(theta)]
    w=[mp.mpf(0) if j==0 else e*mp.cos(t) for j,t in enumerate(theta)]
    wp=[-k*e*z for z in sine]
    D=[[mp.mpf(0) if i==j else k*mp.mpf(-1)**(i-j)/(2*mp.sin(mp.pi*(i-j)/n)) for j in range(n)] for i in range(n)]
    I=[[2*sum(mp.sin(2*mp.pi*m*(i-j)/n)/m for m in range(1,(n+1)//2))/(n*k) for j in range(n)] for i in range(n)]
    R,Rp=map(list,zip(*(g12(t) for t in theta)))
    q=[];p=[];recipes=[];Rs=[];ells=[];L0=[];Ppsi=[]
    phase=Rc/(1-par['zeta']*Rc**2*e**2/2)
    for j in range(n):
        qq=[mp.mpf(0)]*15
        for i in (0,3,5):qq[i]=mp.mpf(1)
        qq[7]=w[j];qq[9]=qq[11]=Rc;qq[13]=U*w[j]**2
        dq=[mp.mpf(0)]*15;dq[7]=wp[j];dq[13]=2*U*w[j]*wp[j]
        den=par['MP2']-par['MU2']*(par['c1']+par['c3']+2*par['c3']*w[j]**2-2*par['c4']*(1+w[j]**2)*w[j]**2)
        ty=-par['MU2']*(par['c1']+par['c3']+2*par['c3']*w[j]**2)*wp[j]/(mp.sqrt(1+w[j]**2)*den)
        yy=[mp.mpf(0)]*12
        yy[0]=yy[3]=H;yy[4]=-ty/2;yy[5]=H-Rp[j]
        yy[7]=-HB*w[j]-R[j]*wp[j];yy[10]=phase;yy[11]=Rc/4
        zero=[mp.mpf(0)]*12
        _,d0=local_derivatives(qq,dq,zero,s,par);ell=d0[:12];columns=[]
        for c in range(12):
            b=zero.copy();b[c]=mp.mpf(1)
            _,ds=local_derivatives(qq,dq,b,s,par)
            columns.append([ds[i]-ell[i] for i in range(12)])
        RR=trans(columns);LL,dd=local_derivatives(qq,dq,yy,s,par)
        PP=mv(RR,yy);PP=[v+u for v,u in zip(PP,ell)]
        pp=[mp.mpf(0)]*15;pp[:6]=[a/2 for a in PP[:6]];pp[6:12]=PP[6:]
        g=par['b']*w[j]**2;zh=Ud*w[j]**2-R[j]*dq[13]
        pp[12]=dd[12]-g*zh;pp[13]=-g*s
        q.append(qq);p.append(pp);recipes.append(yy);Rs.append(RR);ells.append(ell);L0.append(LL);Ppsi.append(pp[12])
    F=[mp.sqrt(1+w[j]**2)*p[j][8] for j in range(n)]
    dF=Dmul(D,F)
    for j in range(n):p[j][14]=-(dot([2*x for x in p[j][:6]]+p[j][6:12],recipes[j])-L0[j]+Ppsi[j]*s+dF[j])
    raw=dict(n=n,theta=theta,sine=sine,D=D,I=I,q=q,p=p,rate=s,Rc=Rc,H=H,HB=HB,U=U,Ud=Ud,
        R=R,Rp=Rp,wp=wp,Zdot=[Ud*x*x/s for x in w],par=par,recipes=recipes,Rs=Rs,ells=ells,
        Qtheta=Rc**2,Qdust=mp.mpf(1)/5,PM=[2*mean([a[2]/2 for a in p]),2*mean([a[4]/2 for a in p]),mean([a[5] for a in p])])
    X=dict(Q=[[a[0],a[1],a[3],*a[6:9],Rc,mp.mpf(0),a[11],a[14],a[13],s] for a in q],
           P=[[b[0],b[1],b[3],*b[6:9],b[9],a[9]*b[10]-Rc**2,b[11],b[14]-raw['Qdust']] for a,b in zip(q,p)],
           M=[mp.mpf(0),mp.mpf(0),mp.mpf(1)],PM=raw['PM'].copy(),tau=mp.mpf(0))
    return raw,X

def coordinates(X,raw):
    n=raw['n'];sine=raw['sine'];s2=mean([z*z for z in sine])
    dy=[X['Q'][i][4]-raw['q'][i][7] for i in range(n)];c=mean([a*b for a,b in zip(sine,dy)])/s2
    anglemean=mean([x[7] for x in X['Q']]);Tmean=mean([x[9] for x in X['Q']])
    q=[]
    for i,x in enumerate(X['Q']):
        a=x[7]-anglemean;r=x[6]
        q.append([x[0],x[1],X['M'][0],x[2],X['M'][1],X['M'][2],x[3],raw['q'][i][7]+dy[i]-c*sine[i],x[5],
            r*cos(a),r*sin(a),x[8],X['tau'],x[10],x[9]-Tmean])
    return q

def restore(X,raw):
    q=coordinates(X,raw);n=raw['n'];D=raw['D'];sine=raw['sine'];par=raw['par']
    anglemean=mean([x[7] for x in X['Q']]);ptmean=mean([x[7] for x in X['P']]);pTmean=mean([x[9] for x in X['P']])
    p=[];g=[];hi=[]
    for i,(x,b) in enumerate(zip(X['Q'],X['P'])):
        a=x[7]-anglemean;pt=raw['Qtheta']+b[7]-ptmean;r=x[6]
        pp=[b[0],b[1],0,b[2],0,0,*b[3:6],b[6]*cos(a)-pt*sin(a)/r,b[6]*sin(a)+pt*cos(a)/r,b[8],0,0,raw['Qdust']+b[9]-pTmean]
        h=tensor(q[i]);hh=inv3(h);vol=sqrt(det3(h));gg=par['b']*vol*dot(q[i][6:9],mv(h,q[i][6:9]))
        pp[13]=-gg*x[11];p.append(pp);g.append(gg);hi.append(hh)
    dq=trans([Dmul(D,c) for c in trans(q)])
    s2=mean([z*z for z in sine]);pvmean=mean([sine[i]*p[i][7] for i in range(n)])/s2
    for i in range(n):p[i][7]-=pvmean*sine[i]
    pvzvz=Dmul(D,[p[i][8]*q[i][8] for i in range(n)])
    S=[sum(p[i][a]*dq[i][a] for a in (0,1,3))+dot(p[i][6:9],dq[i][6:9])+pvzvz[i]+dot(p[i][9:],dq[i][9:]) for i in range(n)]
    d=mean([sine[i]*dq[i][7] for i in range(n)]);lam=-mean(S)/d
    for i in range(n):p[i][7]+=lam*sine[i];S[i]+=lam*sine[i]*dq[i][7]
    rz=mv(raw['I'],S)
    rr=[[p[i][6]*q[i][8]/2,p[i][7]*q[i][8]/2,rz[i]/2] for i in range(n)]
    A=[[mean([h[i][j] for h in hi]) for j in range(3)] for i in range(3)]
    hir=[mv(h,r) for h,r in zip(hi,rr)];M=[X['PM'][0]/2,X['PM'][1]/2,X['PM'][2]]
    const=mv(inv3(A),[M[j]-mean([r[j] for r in hir]) for j in range(3)])
    for i in range(n):
        pi=mv(hi[i],[rr[i][j]+const[j] for j in range(3)])
        p[i][2]=2*pi[0];p[i][4]=2*pi[1];p[i][5]=pi[2]
    return dict(q=q,p=p,g=g,dq=dq,S=S,lam=lam,d=d)

def envelope(q,p,dq,s,y,par,R3):
    h,hi,DV,vol,gam=geometry(q,dq)
    E=dot([2*x for x in p[:6]]+p[6:12],y)-vol*body(q,dq,y,s,par,R3)
    dust=p[14]*sqrt(exp(par['beta']*q[12])**2+hi[2][2]*dq[14]**2)
    F=gam*dot(hi[2],p[6:9])
    return E+dust,F,vol,DV

def functional(X,raw,ys):
    out=restore(X,raw);q,p,dq=out['q'],out['p'],out['dq'];D=raw['D']
    # Exact first Ricci variation at the flat base; NOT a nonlinear Ricci/Hessian.
    Rlin=[-x for x in Dmul(D,Dmul(D,[a[0]+a[3] for a in q]))]
    E=[];F=[];CE=[];chi=[]
    for i in range(raw['n']):
        s=X['Q'][i][11];ee,ff,vol,DV=envelope(q[i],p[i],dq[i],s,ys[i],raw['par'],Rlin[i])
        E.append(ee);F.append(ff);CE.append(ee+vol*raw['par']['K_Q']*s*s)
        chi.append(q[i][13]+s*tr(DV))
    dF=Dmul(D,F);dsinv=Dmul(D,[1/x[11] for x in X['Q']])
    out.update(H=mean([E[i]/X['Q'][i][11]-F[i]*dsinv[i] for i in range(raw['n'])]),
               E=E,F=F,CE=[a+b for a,b in zip(CE,dF)],chi=chi)
    return out

def baseline(raw,X):
    out=restore(X,raw);ys=[];error=mp.mpf(0)
    for i,p in enumerate(out['p']):
        rhs=[2*x for x in p[:6]]+p[6:12]
        rhs=[a-b for a,b in zip(rhs,raw['ells'][i])]
        y=list(mp.lu_solve(mp.matrix(raw['Rs'][i]),mp.matrix(rhs)));ys.append(y)
        _,der=local_derivatives(out['q'][i],out['dq'][i],y,raw['rate'],raw['par'])
        actual=[2*x for x in p[:6]]+p[6:12]
        error=max(error,max(abs(a-b)/(1+abs(a)+abs(b)) for a,b in zip(der[:12],actual)))
    return ys,error

def variables(X,tape):
    Y={k:([[tape.var(x) for x in row] for row in v] if k in ('Q','P') else
          [tape.var(x) for x in v] if k in ('M','PM') else tape.var(v)) for k,v in X.items()}
    return Y,flatten(Y)
def flatten(X):return [v for k in ('Q','P') for row in X[k] for v in row]+X['M']+X['PM']+[X['tau']]
def unpack(flat,n):
    return dict(Q=[flat[12*i:12*(i+1)] for i in range(n)],
        P=[flat[12*n+10*i:12*n+10*(i+1)] for i in range(n)],
        M=flat[22*n:22*n+3],PM=flat[22*n+3:22*n+6],tau=flat[-1])
def dot_chart(a,b):return dot(flatten(a),flatten(b))
def shifted(X,T,h):
    return {k:([[x+1j*h*y for x,y in zip(row,tr)] for row,tr in zip(v,T[k])] if k in ('Q','P') else
        [x+1j*h*y for x,y in zip(v,T[k])] if k in ('M','PM') else v+1j*h*T[k]) for k,v in X.items()}

def original_generator(X,raw,ys,original):
    q=coordinates(X,raw);n=raw['n'];D=raw['D'];par=raw['par'];s=raw['rate']
    angles=[a[7]-mean([v[7] for v in X['Q']]) for a in X['Q']]
    p=[a.copy() for a in original['p']]
    for i in range(n):
        r=X['Q'][i][6];pt=original['q'][i][9]*original['p'][i][10]
        pr=original['p'][i][9];a=angles[i]
        p[i][9]=pr*cos(a)-pt*sin(a)/r;p[i][10]=pr*sin(a)+pt*cos(a)/r
    dq=trans([Dmul(D,c) for c in trans(q)])
    Rlin=[-z for z in Dmul(D,Dmul(D,[a[0]+a[3] for a in q]))]
    sy_shift=mv(raw['I'],[-2*y[4] for y in raw['recipes']])
    shift=[[0,z/s,r/s] for z,r in zip(sy_shift,raw['R'])];sp=trans([Dmul(D,c) for c in trans(shift)])
    vals=[]
    for i in range(n):
        E,F,vol,DV=envelope(q[i],p[i],dq[i],s,ys[i],par,Rlin[i]);h=tensor(q[i]);dh=tensor(dq[i]);V=q[i][6:9]
        g=par['b']*vol*dot(V,mv(h,V));zh=raw['Ud']*raw['q'][i][7]**2-raw['R'][i]*(2*raw['U']*raw['q'][i][7]*raw['wp'][i])
        vals.append((E+p[i][12]*s+(p[i][13]+g*s)*zh)/s)
        for a,(j,k) in enumerate(canonical.HM):
            lie=shift[i][2]*dh[j][k]
            if k==2:lie+=dot(h[j],sp[i])
            if j==2:lie+=dot([h[l][k] for l in range(3)],sp[i])
            vals[-1]+=p[i][a]*lie
        vals[-1]+=dot(p[i][6:9],[shift[i][2]*dq[i][6+j]-q[i][8]*sp[i][j] for j in range(3)])
        vals[-1]+=dot(p[i][9:],[shift[i][2]*x for x in dq[i][9:]])
    return mean(vals)

def original_local(q,dq,y,s,par):
        h,hi,DV,vol,gam=geometry(q,dq)
        c=dict(h=mp.matrix(h),hi=mp.matrix(hi),V=mp.matrix(q[6:9]),gamma=gam,DV=mp.matrix(DV),
            u=q[9],v=q[10],r=q[11],psi=q[12],Z=q[13],R3=mp.mpf(0),epsilon=mp.mpf(1),proper={'T':mp.mpf(1)},
            spatial={name:mp.matrix([0,0,dq[j]]) for name,j in (('u',9),('v',10),('r',11),('psi',12),('Z',13),('T',14))})
        return vol*canonical.mp_body(c,par,mp.matrix(y),s,0,include_dust=False)

def independent_local(ch,raw,ys,out):
    errors=[]
    for i in (0,1):
        q,dq,y=out['q'][i],out['dq'][i],ys[i]
        basevars=list(q)+list(dq)+list(y)+[raw['rate']]
        tape=Tape();variables=[tape.var(v) for v in basevars]
        qq,dd,yy,ss=variables[:15],variables[15:30],variables[30:42],variables[42]
        L=geometry(qq,dd)[3]*body(qq,dd,yy,ss,raw['par']);grad=tape.grad(L,variables)
        got=val(L);want=original_local(q,dq,y,raw['rate'],raw['par'])
        errors.append(abs(got-want)/(1+abs(got)+abs(want)))
        for j in range(43):
            def f(t):
                a=basevars.copy();a[j]=t
                return original_local(a[:15],a[15:30],a[30:42],a[42],raw['par'])
            d=mp.diff(f,basevars[j])
            errors.append(abs(grad[j]-d)/(1+abs(grad[j])+abs(d)))
    ch.small('independent_original_density_value_and_43_derivatives',max(errors),'1e-40')
    return max(errors)

def precision_run(point,initial,n,offset,precision,ch):
    raw,X=build_data(point,initial,n,offset,precision);ys,legendre_error=baseline(raw,X)
    ch.small('local_Legendre_stationarity',legendre_error,'1e-40')
    tape=Tape();Y,vs=variables(X,tape);out=functional(Y,raw,ys);grad=unpack(tape.grad(out['H'],vs),n)
    values={k:val(v) if k in ('H','lam','d') else v for k,v in out.items()}
    baseline_out=functional(X,raw,ys)
    ch.add('positive_clock_radius_and_dust',raw['rate']>0 and min(v[6] for v in X['Q'])>0 and min(p[14] for p in baseline_out['p'])>0)
    ch.small('global_translation_constraint',abs(mean(baseline_out['S'])),'1e-40')
    di=mm(raw['D'],raw['I'])
    ch.small('same_odd_grid_primitive',max(abs(di[i][j]-(int(i==j)-mp.mpf(1)/n)) for i in range(n) for j in range(n)),'1e-40')
    # Initial full density for the independent unreduced functional, lapse restored locally.
    original=dict(q=baseline_out['q'],p=[p.copy() for p in baseline_out['p']])
    df=Dmul(raw['D'],baseline_out['F'])
    for i in range(n):original['p'][i][12]=-(baseline_out['E'][i]+df[i])/raw['rate']
    ref_tape=Tape();refX,refvars=variables(X,ref_tape)
    refgrad=unpack(ref_tape.grad(original_generator(refX,raw,ys,original),refvars),n)
    Zdot=raw['Zdot'];cross_root=mean([raw['rate']*Zdot[i]*out['g'][i] for i in range(n)])
    cross=unpack(tape.grad(cross_root,vs),n)
    T=dict(Q=[[n*x for x in row]+[mp.mpf(0),mp.mpf(0)] for row in grad['P']],
        P=[[-n*(grad['Q'][i][j]+cross['Q'][i][j]) for j in range(10)] for i in range(n)],
        M=grad['PM'].copy(),PM=[-a-b for a,b in zip(grad['M'],cross['M'])],tau=mp.mpf(1))
    for i in range(n):
        ratio=raw['Rp'][i] if i==0 else raw['R'][i]*raw['wp'][i]/raw['q'][i][7]
        T['Q'][i][10]=Zdot[i]
        T['Q'][i][11]=(-raw['U']-(3*raw['H']-raw['HB']-raw['Rp'][i])*raw['rate']+raw['rate']*ratio)/raw['rate']
    target=[[2*raw['H']/raw['rate'],0,2*raw['H']/raw['rate'],0,
        -raw['HB']*q[7]/raw['rate'],0,0,0,raw['Rc']/(4*raw['rate']),0] for q in raw['q']]
    coordinate_error=max([abs(T['Q'][i][j]-target[i][j])/(1+abs(T['Q'][i][j])+abs(target[i][j])) for i in range(n) for j in range(10)]
        +[abs(T['M'][j]-(2*raw['H']/raw['rate'] if j==2 else 0))/(1+abs(T['M'][j])) for j in range(3)])
    ch.small('inherited_initial_coordinate_control_not_imposed',coordinate_error,'1e-8')
    referr=max([abs(T['P'][i][j]+n*refgrad['Q'][i][j])/(1+abs(T['P'][i][j])+abs(n*refgrad['Q'][i][j])) for i in range(n) for j in range(10)]
        +[abs(T['PM'][j]+refgrad['M'][j])/(1+abs(T['PM'][j])+abs(refgrad['M'][j])) for j in range(3)])
    ch.small('original_unreduced_all_momentum_rates',referr,'1e-7')
    currents={}
    for name,j,pj in (('phase',7,[q[9]*p[10]-q[10]*p[9] for q,p in zip(original['q'],original['p'])]),('dust',9,[p[14] for p in original['p']])):
        want=[a/raw['rate'] for a in Dmul(raw['D'],[r*p for r,p in zip(raw['R'],pj)])]
        amplitude=max(abs(a) for a in want);err=max(abs(T['P'][i][j]-want[i]) for i in range(n))
        ch.add(name+'_nonzero_control',amplitude>0)
        ch.small(name+'_original_current_relative',err/amplitude,'1e-4')
        currents[name]=dict(amplitude=mp.nstr(amplitude,30),relative_error=mp.nstr(err/amplitude,30))
    gdot=[]
    for i,q in enumerate(original['q']):
        w=q[7];a=T['Q'][i]
        gdot.append(raw['par']['b']*(w*w*(a[0]+a[2]+T['M'][2])/2+w*w*a[2]+2*w*a[4]))
    drift_error=max(abs(gdot[i]-baseline_out['g'][i]*(5*raw['H']-2*raw['HB'])/raw['rate'])/(1+abs(gdot[i])) for i in range(n))
    ch.small('computed_metric_frame_drift_not_imposed',drift_error,'1e-7')
    drift=raw['par']['b']*(mp.mpf(1)/500)**2*(1+max(abs(a[11]) for a in T['Q'])+abs(5*raw['H']-2*raw['HB']))
    row=max(abs(n*grad['Q'][i][10]-baseline_out['g'][i]*T['Q'][i][11]-raw['rate']*gdot[i]) for i in range(n))/drift
    ch.small('full_undivided_regulator_row',row,'1e-4')
    CE_scale=raw['par']['K_Q']*raw['rate']*max(abs(raw['H']),max(abs(q[11]) for q in T['Q']))
    node_speed=-T['Q'][0][4]/raw['wp'][0]
    CEsp=Dmul(raw['D'],baseline_out['CE'])[0];chisp=Dmul(raw['D'],baseline_out['chi'])[0]
    CEgrad=unpack(tape.grad(out['CE'][0],vs),n);chigrad=unpack(tape.grad(out['chi'][0],vs),n)
    CEdot=dot_chart(CEgrad,T)+node_speed*CEsp;chidot=dot_chart(chigrad,T)+node_speed*chisp
    ch.small('initial_node_energy_tangency',abs(CEdot)/CE_scale,'1e-4')
    ch.small('initial_node_regulator_tangency',abs(chidot),'1e-8')
    ch.small('initial_transverse_node_rates',max(abs(T['Q'][0][j]) for j in (3,5)),'1e-8')
    energy=dot_chart(grad,T)-grad['tau']
    ch.small('explicit_clock_energy_balance',abs(energy)/(1+abs(grad['tau'])),'1e-7')
    ch.small('explicit_matter_clock_term',abs(grad['tau']-raw['par']['beta']*raw['Qdust']/raw['rate'])/(1+abs(grad['tau'])),'1e-7')
    # Independent complex directional controls retain both V1 step sizes.
    dense=dict(Q=[[mp.mpf(((i+1)*(j+2))%7-3)/101 for j in range(12)] for i in range(n)],
               P=[[mp.mpf(((i+2)*(j+1))%11-5)/103 for j in range(10)] for i in range(n)],
               M=[mp.mpf(j+1)/107 for j in range(3)],PM=[-mp.mpf(j+1)/109 for j in range(3)],tau=mp.mpf(1)/113)
    node_steps=[]
    for hs in STEPS:
        step=mp.mpf(hs);probe=functional(shifted(X,dense,step),raw,ys)
        gdense=mp.im(probe['H'])/step;pred=dot_chart(grad,dense)
        ch.small('dense_all_variable_complex_gradient_'+hs,abs(gdense-pred)/(1+abs(pred)),'1e-7')
        pert=functional(shifted(X,T,step),raw,ys)
        ce=mp.im(pert['CE'][0])/step+node_speed*CEsp
        cc=mp.im(pert['chi'][0])/step+node_speed*chisp
        ch.small('node_complex_gradient_'+hs,abs(ce-CEdot)/(CE_scale+abs(ce)+abs(CEdot)),'1e-7')
        ch.small('chi_complex_gradient_'+hs,abs(cc-chidot),'1e-8');node_steps.append(ce)
    ch.small('two_step_node_derivative_agreement',abs(node_steps[0]-node_steps[1])/(CE_scale+abs(node_steps[0])+abs(node_steps[1])),'1e-7')
    crossmax=max([n*abs(cross['Q'][i][j]) for i in range(n) for j in range(10)]+[abs(v) for v in cross['M']])
    ch.add('omitted_two_form_cross_nonzero',crossmax>0,mp.nstr(crossmax,20))
    local_error=independent_local(ch,raw,ys,baseline_out)
    return dict(precision=precision,reference_error=mp.nstr(referr,30),currents=currents,
        coordinate_control_error=mp.nstr(coordinate_error,30),computed_drift_error=mp.nstr(drift_error,30),
        regulator_scaled=mp.nstr(row,30),node_energy_derivative=mp.nstr(CEdot,30),node_energy_scale=mp.nstr(CE_scale,30),
        node_energy_relative=mp.nstr(abs(CEdot)/CE_scale,30),node_chi_derivative=mp.nstr(chidot,30),node_speed=mp.nstr(node_speed,30),
        energy_balance=mp.nstr(energy,30),local_original_density_error=mp.nstr(local_error,30),
        minimum_local_dust=mp.nstr(min(p[14] for p in baseline_out['p']),30),
        force=[[mp.nstr(x,35) for x in row] for row in T['P']],mean_force=[mp.nstr(x,35) for x in T['PM']],
        complex_node_derivatives=[mp.nstr(x,30) for x in node_steps],
        physical_spectrum_computed=False,physical_window_established=False,state_adopted_or_evolved=False)

def engine_controls(ch):
    mp.mp.dps=100;t=Tape();x=t.var(mp.mpf(2)/7);y=t.var(mp.mpf(3)/5)
    f=x*x*sin(y)+exp(x/y)+sqrt(1+y*y)/x
    got=t.grad(f,[x,y]);fun=lambda a,b:a*a*mp.sin(b)+mp.exp(a/b)+mp.sqrt(1+b*b)/a
    want=[mp.diff(lambda a:fun(a,y.v),x.v),mp.diff(lambda b:fun(x.v,b),y.v)]
    ch.small('reverse_rules_independent_mpmath_diff',max(abs(a-b) for a,b in zip(got,want)),'1e-70')
    odd_tape=Tape();odd_x=odd_tape.var(mp.mpf(2)/7);odd_y=odd_tape.var(mp.mpf(3)/5)
    odd=odd_x/17+odd_y/25+odd_x*odd_y/33
    odd_grad=odd_tape.grad(odd,[odd_x,odd_y])
    odd_exact=[mp.mpf(1)/17+odd_y.v/33,mp.mpf(1)/25+odd_x.v/33]
    ch.small('odd_integer_division_keeps_arbitrary_precision',max(abs(a-b) for a,b in zip(odd_grad,odd_exact)),'1e-70')
    a,b,c,d,z=sy.symbols('dR pR dtheta ptheta theta')
    ch.zero('polar_exact_trigonometric_reduction',sy.trigsimp((a*b+c*d)*(sy.sin(z)**2+sy.cos(z)**2-1)))
    tt=Tape();zero=tt.var(mp.mpf(0));ch.small('C2_cusp_first_derivative_at_node',abs(tt.grad((zero*zero)**mp.mpf('1.5'),[zero])[0]),'1e-70')
    bad=False
    try:inv3([[mp.mpf(0)]*3 for _ in range(3)])
    except ZeroDivisionError:bad=True
    ch.add('singular_metric_not_defaulted',bad)
    A=[[mp.mpf(2),mp.mpf(1)/7,mp.mpf(1)/11],[mp.mpf(1)/7,mp.mpf(3),mp.mpf(1)/13],[mp.mpf(1)/11,mp.mpf(1)/13,mp.mpf(4)]]
    inv=inv3(A);ref=mp.matrix(A)**-1
    ch.small('cofactor_inverse_independent_mpmath_matrix',max(abs(inv[i][j]-ref[i,j]) for i in range(3) for j in range(3)),'1e-70')

def grid_job(task):
    case,point,initial,n,offset=task;ch=base.Checks();runs=[]
    try:
        for precision in (80,100):
            local=base.Checks();runs.append(precision_run(point,initial,n,offset,precision,local))
            nodal.reg.joint.merge_checks(ch,local.rows,str(precision)+'_')
        aa,bb=runs;forceA=[mp.mpf(x) for row in aa['force'] for x in row]+[mp.mpf(x) for x in aa['mean_force']]
        forceB=[mp.mpf(x) for row in bb['force'] for x in row]+[mp.mpf(x) for x in bb['mean_force']]
        discrepancy=max(abs(a-b)/(1+abs(a)+abs(b)) for a,b in zip(forceA,forceB))
        ch.small('80_100_digit_force_agreement',discrepancy,'1e-10')
        ceA,ceB=mp.mpf(aa['node_energy_derivative']),mp.mpf(bb['node_energy_derivative']);scale=mp.mpf(bb['node_energy_scale'])
        ch.small('80_100_digit_node_derivative_agreement',abs(ceA-ceB)/(scale+abs(ceA)+abs(ceB)),'1e-7')
    except Exception:ch.add('unexpected_grid_exception',False,traceback.format_exc())
    return (case,n,offset),dict(family=point['family'],eta=point['eta'],grid=n,node_orientation=offset,runs=runs),ch.rows

def calculate(workers):
    pins,before=sources();ch=base.Checks();engine_controls(ch)
    points=lift.READ(nodal.reg.JOINT+'independent.json');initial=lift.READ(lift.cop.CERTS)
    if len(points)!=9 or len(initial)!=9 or any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):raise ValueError('input case order')
    tasks=[(i,a,b,n,o) for i,(a,b) in enumerate(zip(points,initial)) for n in (17,25,33) for o in (0,1)];out={}
    progress('precision_grid_tasks',tasks=54,workers=min(workers,16))
    if workers==1:
        for task in tasks:
            r=grid_job(task);out[r[0]]=r;progress('grid_complete',key=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,16),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(grid_job,t):(t[0],t[3],t[4]) for t in tasks}
            for f in as_completed(jobs):
                r=f.result()
                if r[0]!=jobs[f] or r[0] in out:raise ValueError('grid identity')
                out[r[0]]=r;progress('grid_complete',key=r[0])
    records=[]
    for key in sorted(out):
        _,record,rows=out[key];records.append(record)
        nodal.reg.joint.merge_checks(ch,rows,'_'.join(map(str,key))+'_')
    _,after=sources();ch.add('sources_sidecars_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows);complete=len(records)==54 and all(len(r['runs'])==2 for r in records)
    summary=dict(validation='PASS_HIGH_PRECISION_INITIAL_FIRST_VARIATION_ONLY' if passed==len(ch.rows) and complete else 'FAIL_OR_UNRESOLVED_HIGH_PRECISION_FIRST_VARIATION',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='INITIAL_FIRST_VARIATION_'+('LOCALLY_VERIFIED' if passed==len(ch.rows) and complete else 'UNRESOLVED')+'_FULL_PHYSICAL_DOMAIN_OPEN',
        full_nodal_hierarchy_verified=False,physical_spectrum_computed=False,physical_window_established=False,
        full_initial_admission=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    form=dict(precision=[80,100],original_steps=list(STEPS),
        envelope='First differential only: dE0=sum(y*dP)-d(volume*L0) at fixed solved y; NOT a Hessian/off-base Hamiltonian',
        curvature='Flat first Ricci variation -D^2(delta hxx+delta hyy) retained at nodes; nonlinear Ricci remains necessary for future Hessian',
        momentum='Pdot=-H_Q-s*g_Q*Zdot, Qdot=H_P; all coupled variables/means/charges retained',
        physical_holds='Full nodal hierarchy/admission, function space, descriptor Hessian/background drift, physical modes/window, nonlinear control and matching remain unresolved')
    return {'summary.json':summary,'formulas.json':form,'independent.json':records}

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay')
    p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose output or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    meta=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:meta(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(nodal.v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode()
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay set drift')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or meta(f)!=before[name]:raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1

if __name__=='__main__':raise SystemExit(main())
