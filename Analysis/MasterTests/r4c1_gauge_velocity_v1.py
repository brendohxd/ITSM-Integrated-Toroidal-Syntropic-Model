"""Functional periodic gauge solve and paired coordinate-rate maps.

mean and primitive are the actual adapted-circle operators. primitive must
return a periodic zero-mean antiderivative; harmonics remain caller inputs.
"""
def solve(metric_rates,hxx,hyy,Abar,mean,primitive,harmonics=(0,0,0)):
 h=[hxx,hyy];constants=[];slopes=[];fields=[]
 for i in range(2):
  c=mean(lambda z:metric_rates[i](z)/h[i](z))/mean(lambda z:1/h[i](z))
  def slope(z,i=i,c=c):return (c-metric_rates[i](z))/h[i](z)
  base=primitive(slope);constants.append(c);slopes.append(slope)
  fields.append(lambda z,base=base,i=i:base(z)+harmonics[i])
 c=mean(metric_rates[2]);slope=lambda z:(c-metric_rates[2](z))/(2*Abar*Abar)
 base=primitive(slope);constants.append(c);slopes.append(slope);fields.append(lambda z:base(z)+harmonics[2])
 return dict(coordinate_velocity=fields,coordinate_gradient=slopes,modulus_rates=constants)

HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))
def lie_fields(q,d,w,wz):
 h=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
 out=[w[2]*d[k]+(sum(h[a][i]*wz[i] for i in range(3)) if b==2 else 0)+(sum(h[b][i]*wz[i] for i in range(3)) if a==2 else 0) for k,(a,b) in enumerate(HM)]
 out += [w[2]*d[6+i]-q[8]*wz[i] for i in range(3)]
 out += [w[2]*d[i] for i in range(9,14)]
 return out
def lie_momenta(p,pz,w,wz):
 T=[]
 for k in range(14):
  e=[0]*14;e[k]=1;T.append(lie_fields(e,[0]*14,[0]*3,wz))
 return [w[2]*pz[k]+wz[2]*p[k]-sum(T[k][i]*p[i] for i in range(14)) for k in range(14)]
def factors(J):
 field=[1,1,1/J,1,1/J,1/(J*J),1,1,J,1,1,1,1,1]
 return field,[1/(J*t) for t in field]
def coordinate_rates(q,d,p,pz,v,pdot,w,wz,J):
 f,g=factors(J);lq=lie_fields(q,d,[0,0,w],[0,0,wz]);lp=lie_momenta(p,pz,[0,0,w],[0,0,wz])
 return [a*(b-c) for a,b,c in zip(f,v,lq)],[a*(b-c) for a,b,c in zip(g,pdot,lp)]
def current_density_rate(I,Iz,Idot,w,wz,J):return (Idot-w*Iz-wz*I)/J
