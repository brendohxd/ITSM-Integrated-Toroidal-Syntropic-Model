"""Canonical density and its direct time tangent on the auxiliary surface."""
import mpmath as mp

def regulator(ctx,q,d):
 n,vol,_,hi,_=ctx['geometry'](q,d);b=ctx['b'];beta=ctx['beta']
 return b*n*vol*(q[13]*q[13]/2-hi[2][2]*d[13]*d[12]+beta*q[13]*hi[2][2]*d[12]*d[12])

def improvement(ctx,q,d,p):
 n,_,gamma,hi,f=ctx['geometry'](q,d)
 return n*(gamma*sum(hi[i][2]*p[6+i] for i in range(3))-f/2)

def evaluate(ctx,dq,dd,dp,dv,dS,dSz,pdot,delta_pdot,Zdot,delta_Zdot):
 J=ctx['J'];D=ctx['D'];grad=ctx['gradient'];hj=ctx['hj'];lie=ctx['lie']
 q=ctx['q'];d=ctx['d'];v=ctx['v'];p=ctx['pi'];S=ctx['S'];Sz=ctx['Sz'];L=ctx['L']
 dz=lambda t:J(coefficients=[t.c[1],2*t.c[2],mp.iv.mpf(0)])
 v=v[:13]+[J(Zdot)];dv=dv[:13]+[J(delta_Zdot)]
 dy=dq+dv+dd+dS+dSz
 RG=regulator(ctx,[D.var(x,i) for i,x in enumerate(q)],[D.var(x,28+i) for i,x in enumerate(d)])
 L0=L-RG
 def tangent(xs,ys):return [D(x,{0:y}) for x,y in zip(xs,ys)]
 def mixed(xs,ts,es,ets):return [D(x,{0:t,1:e},{(0,1):et}) for x,t,e,et in zip(xs,ts,es,ets)]
 Q=tangent(q,dq);V=tangent(v,dv);P=tangent(p,dp);PD=tangent(pdot,delta_pdot)
 SS=tangent(S,dS);SZ=tangent(Sz,dSz);DD=tangent(d,dd)
 VD=tangent([dz(x) for x in v],[dz(x) for x in dv])
 RV=[a-b for a,b in zip(V,lie(Q,DD,SS,SZ))];LV=lie(V,VD,SS,SZ)
 time=D(J(0))
 for i in range(14):
  tq=sum((hj(L0,i,k)*dy[k] for k in range(48)),J(0));td=sum((hj(L0,28+i,k)*dy[k] for k in range(48)),J(0))
  lq=D(grad(L0,i),{0:tq});ld=D(grad(L0,28+i),{0:td})
  time+=lq*V[i]+ld*VD[i]-PD[i]*RV[i]+P[i]*LV[i]
 QM=mixed(q,v,dq,dv);DM=mixed(d,[dz(x) for x in v],dd,[dz(x) for x in dv]);PM=mixed(p,pdot,dp,delta_pdot)
 B=improvement(ctx,QM,DM,PM)
 n,vol,_,_,_=ctx['geometry'](QM,DM);reg=-ctx['b']*n*vol*QM[13]*QM[13]/2
 rv=[a-b for a,b in zip(v,lie(q,d,S,Sz))]
 hat=L0.c-sum((p[i]*rv[i] for i in range(14)),J(0))
 dhat=sum((grad(L0,k)*dy[k] for k in range(48)),J(0))-sum((dp[i]*rv[i]+p[i]*RV[i].g.get(0,J(0)) for i in range(14)),J(0))
 base=hat+reg.c;delta=dhat+reg.g.get(1,J(0));dB=B.g.get(1,J(0))
 I=J(coefficients=[base.c[0]-B.c.c[1],base.c[1]-2*B.c.c[2],mp.iv.mpf(0)])
 deltaI=J(coefficients=[delta.c[0]-dB.c[1],delta.c[1]-2*dB.c[2],mp.iv.mpf(0)])
 return dict(density=I,delta_density=deltaI,density_rate=time.c.c[0]-B.g[0].c[1]+reg.g[0].c[0],
  delta_density_rate=time.g[0].c[0]-B.h[0,1].c[1]+reg.h[0,1].c[0],
  delta_improvement=dB,delta_regulator_density=reg.g[1],delta_regulator_time=reg.h[0,1].c[0],higher_time_spatial_rates='NOT_RETURNED')
