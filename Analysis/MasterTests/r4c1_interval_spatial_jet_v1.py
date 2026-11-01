"""Fourth-order spatial Taylor jets with outward interval coefficients."""
import math
import mpmath as mp
iv=mp.iv
ORDER=4
class Jet:
 def __init__(self,value=0,coefficients=None):
  self.c=list(coefficients) if coefficients is not None else [iv.mpf(value)]+[iv.mpf(0) for _ in range(ORDER)]
 @staticmethod
 def cast(x):return x if isinstance(x,Jet) else Jet(x)
 @staticmethod
 def variable(x):return Jet(coefficients=[iv.mpf(x),iv.mpf(1),iv.mpf(0),iv.mpf(0),iv.mpf(0)])
 def __add__(self,x):
  x=self.cast(x);return Jet(coefficients=[a+b for a,b in zip(self.c,x.c)])
 __radd__=__add__
 def __neg__(self):return Jet(coefficients=[-x for x in self.c])
 def __sub__(self,x):return self+-self.cast(x)
 def __rsub__(self,x):return self.cast(x)+-self
 def __mul__(self,x):
  x=self.cast(x);return Jet(coefficients=[sum((self.c[j]*x.c[n-j] for j in range(n+1)),iv.mpf(0)) for n in range(ORDER+1)])
 __rmul__=__mul__
 def __pow__(self,p):
  if isinstance(p,Jet):
   assert all(z==0 for z in p.c[1:]);p=p.c[0]
  if p==0:return Jet(1)
  for n in range(1,9):
   if p==n:
    out=Jet(1)
    for _ in range(n):out=out*self
    return out
  a=self.c[0];q=Jet(coefficients=[iv.mpf(0)]+[v/a for v in self.c[1:]])
  total=Jet(1);term=Jet(1);binom=iv.mpf(1)
  for n in range(1,ORDER+1):
   term=term*q;binom=binom*(iv.mpf(p)-n+1)/n;total=total+term*Jet(binom)
  return total*Jet(a**iv.mpf(p))
 def __truediv__(self,x):return self*self.cast(x)**(-1)
 def __rtruediv__(self,x):return self.cast(x)*self**(-1)
 def __eq__(self,x):
  try:x=self.cast(x);return all(a==b for a,b in zip(self.c,x.c))
  except (TypeError,ValueError):return False
 def __bool__(self):return not self==0
def exp(x):
 x=Jet.cast(x);d=Jet(coefficients=[iv.mpf(0)]+x.c[1:]);out=Jet(1);term=Jet(1)
 for n in range(1,ORDER+1):term=term*d/n;out=out+term
 return Jet(iv.exp(x.c[0]))*out
def trig(x,cosine=False):
 x=Jet.cast(x);d=Jet(coefficients=[iv.mpf(0)]+x.c[1:]);term=Jet(1);out=Jet(0)
 funcs=(iv.cos,lambda z:-iv.sin(z),lambda z:-iv.cos(z),iv.sin) if cosine else (iv.sin,iv.cos,lambda z:-iv.sin(z),lambda z:-iv.cos(z))
 for n in range(ORDER+1):
  if n:term=term*d/n
  out=out+Jet(funcs[n%4](x.c[0]))*term
 return out
class Adapter:
 def mpf(self,x=0):
  if isinstance(x,str) and x in ('.5','0.5','1.5'):return mp.mpf(x)
  return Jet.cast(x)
 def exp(self,x):return exp(x)
 def sin(self,x):return trig(x)
 def cos(self,x):return trig(x,True)
 def sqrt(self,x):return Jet.cast(x)**mp.mpf('.5')
def endpoints(x):return [list(x._mpi_[0]),list(x._mpi_[1])]
def upper(x):return mp.mpf(x._mpi_[1])
def lower(x):return mp.mpf(x._mpi_[0])
def abs_upper(x):return max(abs(lower(x)),abs(upper(x)))
