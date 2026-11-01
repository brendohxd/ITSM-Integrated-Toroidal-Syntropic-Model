"""Full-metric auxiliary jets and mixed time tangent with explicit inputs."""
import mpmath as mp

def tensor(x):return [[x[0],x[1],x[2]],[x[1],x[3],x[4]],[x[2],x[4],x[5]]]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def trace(a):return sum(a[i][i] for i in range(3))
def coefficient(ctx,q,d):
 _,_,_,hi,_=ctx['geometry'](q,d);dh=tensor(d)
 C=hi[2][2]*trace(mul(hi,dh))/2-mul(mul(hi,dh),hi)[2][2]
 return hi,C
def laplacian(ctx,q,d,psi4):
 J=ctx['J'];hi,C=coefficient(ctx,q,d)
 psi2=J(coefficients=[d[12].c[1],2*d[12].c[2],psi4/2])
 return hi[2][2]*psi2+C*d[12]
def apply(ctx,q,d,psi4,v,dq,dd,dpsi4,dv):
 J=ctx['J'];D=ctx['D'];zero=mp.iv.mpf(0)
 def dz(x):return J(coefficients=[x.c[1],2*x.c[2],zero])
 qq=[D(x,{0:t,1:e},{(0,1):et}) for x,t,e,et in zip(q,v,dq,dv)]
 ddd=[D(x,{0:dz(t),1:e},{(0,1):dz(et)}) for x,t,e,et in zip(d,v,dd,dv)]
 hi,C=coefficient(ctx,qq,ddd)
 psi2=D(J(coefficients=[d[12].c[1],2*d[12].c[2],psi4/2]),
         {0:J(2*v[12].c[2]),1:J(coefficients=[dd[12].c[1],2*dd[12].c[2],dpsi4/2])},
         {(0,1):J(2*dv[12].c[2])})
 lap=hi[2][2]*psi2+C*ddd[12]
 return dict(Z=-lap.c,delta_Z=-lap.g.get(1,J(0)),Zdot=-lap.g.get(0,J(0)).c[0],delta_Zdot=-lap.h.get((0,1),J(0)).c[0],time_spatial_jet='NOT_RETURNED')
def independent_time_value(ctx,q,d,v):
 J=ctx['J'];hi,C=coefficient(ctx,q,d);dh=tensor(d);ht=tensor(v)
 dht=tensor([J(coefficients=[t.c[1],2*t.c[2],mp.iv.mpf(0)]) for t in v])
 hit=[[-x for x in row] for row in mul(mul(hi,ht),hi)]
 tr=trace(mul(hi,dh))/2
 trt=(trace(mul(hit,dh))+trace(mul(hi,dht)))/2
 Ct=hit[2][2]*tr+hi[2][2]*trt-mul(mul(hit,dh),hi)[2][2]-mul(mul(hi,dht),hi)[2][2]-mul(mul(hi,dh),hit)[2][2]
 return -(hit[2][2].c[0]*d[12].c[1]+hi[2][2].c[0]*2*v[12].c[2]+Ct.c[0]*d[12].c[0]+C.c[0]*v[12].c[1])
