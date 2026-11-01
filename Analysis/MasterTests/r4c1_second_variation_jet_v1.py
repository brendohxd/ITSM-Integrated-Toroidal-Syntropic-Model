"""Sparse second variations over a caller-supplied scalar/spatial-jet algebra.

Hessian entries are derivatives, not Taylor coefficients. No runtime dispatch.
"""
class Second:
 parents=()  # Existing spatial Jet must defer mixed arithmetic to this level.
 scalar=staticmethod(lambda x:x)
 exponential=staticmethod(lambda x:x.exp())
 def __init__(self,c=0,g=None,h=None):
  self.c=self.scalar(c);self.g=g or {};self.h=h or {}
 @classmethod
 def cast(cls,x):return x if isinstance(x,cls) else cls(x)
 @classmethod
 def var(cls,c,i):return cls(c,{i:cls.scalar(1)})
 def __add__(self,x):
  x=self.cast(x)
  def add(a,b):
   out=a.copy()
   for k,v in b.items():out[k]=out.get(k,self.scalar(0))+v
   return {k:v for k,v in out.items() if v!=0}
  return type(self)(self.c+x.c,add(self.g,x.g),add(self.h,x.h))
 __radd__=__add__
 def __neg__(self):return type(self)(-self.c,{k:-v for k,v in self.g.items()},{k:-v for k,v in self.h.items()})
 def __sub__(self,x):return self+-self.cast(x)
 def __rsub__(self,x):return self.cast(x)+-self
 def __mul__(self,x):
  x=self.cast(x);g={};h={};zero=self.scalar(0)
  for i in self.g.keys()|x.g.keys():g[i]=self.g.get(i,zero)*x.c+x.g.get(i,zero)*self.c
  for k in self.h.keys()|x.h.keys():h[k]=self.h.get(k,zero)*x.c+x.h.get(k,zero)*self.c
  for i,a in self.g.items():
   for j,b in x.g.items():
    k=(min(i,j),max(i,j));h[k]=h.get(k,zero)+(2 if i==j else 1)*a*b
  return type(self)(self.c*x.c,{k:v for k,v in g.items() if v!=0},{k:v for k,v in h.items() if v!=0})
 __rmul__=__mul__
 def unary(self,value,first,second):
  h={k:first*v for k,v in self.h.items()};keys=sorted(self.g)
  for ai,i in enumerate(keys):
   for j in keys[ai:]:
    k=(i,j);h[k]=h.get(k,self.scalar(0))+second*self.g[i]*self.g[j]
  return type(self)(value,{k:first*v for k,v in self.g.items()},{k:v for k,v in h.items() if v!=0})
 def __pow__(self,p):
  if p==0:return type(self)(1)
  if p==1:return self
  # Avoid 0**negative in derivatives of polynomial powers at a zero value.
  first=p*self.c**(p-1)
  second=self.scalar(2) if p==2 else p*(p-1)*self.c**(p-2)
  return self.unary(self.c**p,first,second)
 def __truediv__(self,x):return self*self.cast(x)**(-1)
 def __rtruediv__(self,x):return self.cast(x)*self**(-1)
 def __eq__(self,x):
  try:x=self.cast(x);return self.c==x.c and self.g==x.g and self.h==x.h
  except (TypeError,ValueError):return False
 def __bool__(self):return not self==0
 def exp(self):
  v=self.exponential(self.c);return self.unary(v,v,v)
