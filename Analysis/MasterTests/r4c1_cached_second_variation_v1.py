"""Cached C2 second differentials for the full constrained planar functional."""
from __future__ import annotations
import hashlib,importlib.util
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py'
PSHA='99a71aa721140a59c0e27af4632e4c52c9ae30138a8ae9af53b690b5c2cee157'
if hashlib.sha256((ROOT/PARENT).read_bytes()).hexdigest()!=PSHA:raise ValueError('descriptor source drift')
spec=importlib.util.spec_from_file_location('frozen_coupled_descriptor',ROOT/PARENT)
dc=importlib.util.module_from_spec(spec);spec.loader.exec_module(dc)
pv=dc.pv
dot,mv,mm,trans,mean=pv.dot,pv.mv,pv.mm,pv.trans,pv.mean
tensor,inv3,det3,sqrt,Dmul=pv.tensor,pv.inv3,pv.det3,pv.sqrt,pv.Dmul

def value(x):return x.v if isinstance(x,N2) else x

class Tape2:
    def __init__(self):self.nodes=[];self.cusps=[];self.prepared=False
    def var(self,x):return N2(self,x,(),())
    def gradient(self,root,variables):
        for n in self.nodes:n.bar=mp.mpf(0)
        if isinstance(root,N2):
            root.bar=mp.mpf(1)
            for n in reversed(self.nodes):
                if n.bar:
                    for a,w in n.parents:
                        if w:a.bar+=n.bar*w
        return [n.bar for n in variables]
    def prepare(self,root,variables):
        # A vanishing primitive alone does not justify the composite C2 limit.
        for y in self.cusps:
            g=self.gradient(y,variables)
            if max(abs(x) for x in g)>mp.mpf('1e-60'):
                raise ValueError('nonstationary Y^(3/2) is not C2 at zero')
        self.variables=variables;self.first=self.gradient(root,variables);self.prepared=True
    def action(self,direction):
        if not self.prepared or len(direction)!=len(self.variables):raise ValueError('unprepared/mismatched Hessian direction')
        for n in self.nodes:n.d=mp.mpf(0);n.db=mp.mpf(0)
        for n,z in zip(self.variables,direction):n.d=z
        for n in self.nodes:
            if n.parents:n.d=sum(w*a.d for a,w in n.parents if w and a.d)
        for n in reversed(self.nodes):
            if n.db:
                for a,w in n.parents:
                    if w:a.db+=n.db*w
            if n.bar:
                for a,b,w in n.second:
                    if w and b.d:a.db+=n.bar*w*b.d
        return [n.db for n in self.variables]

class N2:
    __slots__=('t','v','parents','second','bar','d','db')
    def __init__(self,t,v,parents,second):
        self.t=t;self.v=v;self.parents=parents;self.second=second
        self.bar=self.d=self.db=mp.mpf(0);t.nodes.append(self)
    def __add__(self,b):
        if not isinstance(b,N2) and b==0:return self
        return N2(self.t,self.v+value(b),((self,mp.mpf(1)),)+(((b,mp.mpf(1)),) if isinstance(b,N2) else ()),())
    __radd__=__add__
    def __neg__(self):return N2(self.t,-self.v,((self,mp.mpf(-1)),),())
    def __sub__(self,b):return mp.mpf(0) if b is self else self+(-b)
    def __rsub__(self,b):return b+(-self)
    def __mul__(self,b):
        if not isinstance(b,N2) and b==0:return mp.mpf(0)
        parents=((self,value(b)),)+(((b,self.v),) if isinstance(b,N2) else ())
        second=((self,b,mp.mpf(1)),(b,self,mp.mpf(1))) if isinstance(b,N2) else ()
        return N2(self.t,self.v*value(b),parents,second)
    __rmul__=__mul__
    def __truediv__(self,b):
        z=value(b);one=mp.mpf(1)
        parents=((self,one/z),)+(((b,-self.v/z**2),) if isinstance(b,N2) else ())
        second=((self,b,-one/z**2),(b,self,-one/z**2),(b,b,2*self.v/z**3)) if isinstance(b,N2) else ()
        return N2(self.t,self.v/z,parents,second)
    def __rtruediv__(self,b):return N2(self.t,b/self.v,((self,-b/self.v**2),),((self,self,2*b/self.v**3),))
    def __pow__(self,p):
        if isinstance(p,N2):raise TypeError('variable exponent')
        if p==0:return mp.mpf(1)
        if p==1:return self
        if self.v==0 and p>1:
            d=mp.mpf(0)
            if p<2:self.t.cusps.append(self);dd=mp.mpf(0)
            else:dd=mp.mpf(2) if p==2 else mp.mpf(0)
        else:d=p*self.v**(p-1);dd=p*(p-1)*self.v**(p-2)
        return N2(self.t,self.v**p,((self,d),),((self,self,dd),))

def unary(fn,df,ddf,x):
    return N2(x.t,fn(x.v),((x,df(x.v)),),((x,x,ddf(x.v)),)) if isinstance(x,N2) else fn(x)
def sin(x):return unary(mp.sin,mp.cos,lambda a:-mp.sin(a),x)
def cos(x):return unary(mp.cos,lambda a:-mp.sin(a),lambda a:-mp.cos(a),x)
def exp(x):return unary(mp.exp,mp.exp,mp.exp,x)

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

def state(X):return pv.flatten(X)[:-1]
def unstate(x,n):return pv.unpack(list(x)+[mp.mpf(0)],n)

def augmented(X,ys,raw):
    out=restore(X,raw);q,p,dq=out['q'],out['p'],out['dq'];R3=dc.ricci(q,raw['D']);E=[];F=[]
    for i in range(raw['n']):
        h,hi,DV,vol,gam=pv.geometry(q[i],dq[i]);Pi=[2*x for x in p[i][:6]]+p[i][6:12]
        e=dot(Pi,ys[i])-vol*pv.body(q[i],dq[i],ys[i],X['Q'][i][11],raw['par'],R3[i])
        e+=p[i][14]*sqrt(exp(raw['par']['beta']*q[i][12])**2+hi[2][2]*dq[i][14]**2)
        E.append(e);F.append(gam*dot(hi[2],p[i][6:9]))
    ds=Dmul(raw['D'],[1/x[11] for x in X['Q']])
    return mean([e/x[11]-f*d for e,x,f,d in zip(E,X['Q'],F,ds)])

class CachedHessian:
    def __init__(self,raw,X,y0):
        self.raw=raw;self.X=X;self.n=raw['n'];self.y0=y0;self.t=Tape2()
        xs=[self.t.var(x) for x in state(X)];ys=[self.t.var(y) for row in y0 for y in row]
        self.vars=xs+ys;Y=unstate(xs,self.n);yy=[ys[12*i:12*(i+1)] for i in range(self.n)]
        root=augmented(Y,yy,raw);self.t.prepare(root,self.vars)
        self.N=len(xs);self.value=value(root);self.first=self.t.first[:self.N]
        self.stationarity=max(abs(x) for x in self.t.first[self.N:]);self.inverses=[]
        out=pv.restore(X,raw)
        for i in range(self.n):
            vol=pv.geometry(out['q'][i],out['dq'][i])[3]
            neg_Fyy=mp.matrix(raw['Rs'][i])*vol/(self.n*X['Q'][i][11])
            self.inverses.append([list(row) for row in (neg_Fyy**-1).tolist()])
        self.last_stationarity=mp.mpf(0)
    def action(self,v):
        a=self.t.action(state(v)+[mp.mpf(0)]*(12*self.n));hx=a[:self.N];hy=a[self.N:]
        dy=[x for i in range(self.n) for x in mv(self.inverses[i],hy[12*i:12*(i+1)])]
        b=self.t.action([mp.mpf(0)]*self.N+dy)
        self.last_stationarity=max(abs(x+y)/(1+abs(x)+abs(y)) for x,y in zip(hy,b[self.N:]))
        return unstate([x+y for x,y in zip(hx,b[:self.N])],self.n)

def engine_controls(ch):
    mp.mp.dps=100;t=Tape2();x=t.var(mp.mpf(2)/7);y=t.var(mp.mpf(3)/5)
    f=x*x*sin(y)+exp(x/y)+sqrt(1+y*y)/x+x/17+y/25
    t.prepare(f,[x,y]);v=[mp.mpf(1)/11,-mp.mpf(2)/13];got=t.action(v)
    fn=lambda a,b:a*a*mp.sin(b)+mp.exp(a/b)+mp.sqrt(1+b*b)/a+a/17+b/25
    H=mp.matrix([[mp.diff(lambda a:fn(a,y.v),x.v,2),mp.diff(lambda a:mp.diff(lambda b:fn(a,b),y.v),x.v)],
                 [mp.diff(lambda b:mp.diff(lambda a:fn(a,b),x.v),y.v),mp.diff(lambda b:fn(x.v,b),y.v,2)]])
    want=list(H*mp.matrix(v));ch.small('cached_second_rules_independent_mpmath',max(abs(a-b) for a,b in zip(got,want)),'1e-70')
    tt=Tape2();a=tt.var(mp.mpf(0));b=tt.var(mp.mpf(0));f=(a*a+b*b)**mp.mpf('1.5');tt.prepare(f,[a,b])
    ch.small('C2_composite_node_Hessian_limit',max(abs(x) for x in tt.action([mp.mpf(1),mp.mpf(2)])),'1e-70')
    bad=False
    try:
        u=Tape2();z=u.var(mp.mpf(0));u.prepare(z**mp.mpf('1.5'),[z])
    except ValueError:bad=True
    ch.add('nonstationary_fractional_primitive_rejected',bad)
    n,s,m=mp.mpf(17),mp.mpf(3)/7,mp.mpf(5)/11
    q=Tape2();p=q.var(mp.mpf(2)/13);yy=q.var(p.v/m);root=(p*yy-m*yy*yy/2)/(n*s);q.prepare(root,[p,yy])
    first=q.action([mp.mpf(1),mp.mpf(0)]);dy=n*s*first[1]/m;second=q.action([mp.mpf(0),dy])
    ch.small('Legendre_Schur_retains_n_s_factor',abs(first[0]+second[0]-1/(n*s*m)),'1e-70')
