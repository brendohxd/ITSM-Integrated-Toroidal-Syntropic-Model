"""Full metric action current; value/first spatial coefficient only."""
import mpmath as mp
def tensor(q):return [[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def dz(ctx,x):
 J=ctx['J'];D=ctx['D']
 def first(t):return J(coefficients=[t.c[1],2*t.c[2],mp.iv.mpf(0)])
 if isinstance(x,D):return D(first(x.c),{i:first(t) for i,t in x.g.items()},{i:first(t) for i,t in x.h.items()})
 return first(x)
def flux(ctx,q,d,v,S,Sz):
 n,vol,_,hi,_=ctx['geometry'](q,d)
 # Independent frame variables elsewhere in the action remain untouched;
 # this R-tau regulator uses the declared clock normal.
 lie=ctx['lie'](q,d,S,Sz);K=tensor([(v[i]-lie[i])/(2*n) for i in range(6)])
 trace=sum(hi[i][j]*K[j][i] for i in range(3) for j in range(3));up=mm(mm(hi,K),hi)
 p=(v[12]-S[2]*d[12])/n;pz=dz(ctx,p)
 return [ctx['b']*n*n*vol*(q[13]*hi[i][2]*pz+q[13]*(trace*hi[i][2]-2*up[i][2])*d[12]-p*hi[i][2]*d[13]) for i in range(3)]
def linearized(ctx,q,d,v,S,Sz,dq,dd,dv,dS,dSz,I,deltaI):
 D=ctx['D'];J=ctx['J']
 def lift(xs,ys):return [D(x,{0:y}) for x,y in zip(xs,ys)]
 F=flux(ctx,lift(q,dq),lift(d,dd),lift(v,dv),lift(S,dS),lift(Sz,dSz))
 df=[t.g.get(0,J(0)) for t in F]
 rate=(S[2]*deltaI+I*dS[2]+df[2]).c[1]
 return dict(background_flux=[t.c for t in F],delta_flux=df,density_rate=rate,higher_spatial_rates='NOT_RETURNED')
