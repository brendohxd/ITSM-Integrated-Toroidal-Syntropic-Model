"""Exact dyadic outward-rounded intervals and polynomial remainder arithmetic.

Endpoints are integers divided by 2**256. No binary floating-point endpoint
calculation. The implementation is deliberately limited to operations needed
by the registered finite-mode rational ODE; unsupported operations are refused.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt, comb

BITS=256
SCALE=1 << BITS


def ceildiv(n, d):
    if d <= 0:
        raise ValueError('ceildiv requires positive denominator')
    return -((-n)//d)


def upprod(a,b):
    if a<0 or b<0:
        raise ValueError('Nonnegative radii required')
    return ceildiv(a*b,SCALE)


class IV:
    __slots__=('lo','hi')

    def __init__(self,lo,hi=None):
        self.lo=int(lo)
        self.hi=int(lo if hi is None else hi)
        if self.lo>self.hi:
            raise ValueError('Inverted enclosure')

    @classmethod
    def rational(cls,n,d=1):
        n,d=int(n),int(d)
        if d==0:raise ZeroDivisionError('Zero rational denominator')
        if d<0:n,d=-n,-d
        return cls(n*SCALE//d,ceildiv(n*SCALE,d))

    @classmethod
    def fraction(cls,q):
        q=Fraction(q)
        return cls.rational(q.numerator,q.denominator)

    @classmethod
    def coerce(cls,q):
        if isinstance(q,IV):return q
        if isinstance(q,(int,Fraction)):return cls.fraction(q)
        raise TypeError('Refuse floating-point interval input')

    def __add__(self,q):
        q=self.coerce(q)
        return IV(self.lo+q.lo,self.hi+q.hi)

    __radd__=__add__

    def __neg__(self):return IV(-self.hi,-self.lo)

    def __sub__(self,q):return self+-self.coerce(q)

    def __rsub__(self,q):return self.coerce(q)+-self

    def __mul__(self,q):
        q=self.coerce(q)
        if self.lo==self.hi:
            a,b=self.lo*q.lo,self.lo*q.hi
            lo,hi=min(a,b),max(a,b)
        elif q.lo==q.hi:
            a,b=q.lo*self.lo,q.lo*self.hi
            lo,hi=min(a,b),max(a,b)
        else:
            values=(self.lo*q.lo,self.lo*q.hi,self.hi*q.lo,self.hi*q.hi)
            lo,hi=min(values),max(values)
        return IV(lo//SCALE,ceildiv(hi,SCALE))

    __rmul__=__mul__

    def inverse(self):
        if self.lo<=0<=self.hi:
            raise ZeroDivisionError('Interval denominator includes zero')
        # Reciprocal is decreasing on either connected nonzero real interval.
        def low(x):
            n,d=SCALE*SCALE,x
            if d<0:n,d=-n,-d
            return n//d
        def high(x):
            n,d=SCALE*SCALE,x
            if d<0:n,d=-n,-d
            return ceildiv(n,d)
        return IV(low(self.hi),high(self.lo))

    def __truediv__(self,q):return self*self.coerce(q).inverse()

    def __rtruediv__(self,q):return self.coerce(q)*self.inverse()

    def scale(self,n,d=1):
        n,d=int(n),int(d)
        if d==0:raise ZeroDivisionError('Zero scale denominator')
        if d<0:n,d=-n,-d
        x,y=self.lo*n,self.hi*n
        return IV(min(x,y)//d,ceildiv(max(x,y),d))

    def sqrt(self):
        if self.lo<0:raise ValueError('Negative square-root interval')
        lo=isqrt(self.lo*SCALE)
        upper=self.hi*SCALE
        hi=isqrt(upper)
        if hi*hi<upper:hi+=1
        return IV(lo,hi)

    def power(self,n):
        if not isinstance(n,int):raise TypeError('Integer power required')
        if n<0:return self.inverse().power(-n)
        answer=ONE
        base=self
        while n:
            if n&1:answer=answer*base
            n//=2
            if n:base=base*base
        return answer

    def square(self):
        low=0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi)
        high=max(self.lo*self.lo,self.hi*self.hi)
        return IV(low//SCALE,ceildiv(high,SCALE))

    def center(self):return IV((self.lo+self.hi)//2)

    def abs_upper(self):return max(abs(self.lo),abs(self.hi))

    def abs_lower(self):
        return 0 if self.lo<=0<=self.hi else min(abs(self.lo),abs(self.hi))

    def contains(self,q):
        q=Fraction(q)
        return self.lo*q.denominator<=q.numerator*SCALE<=self.hi*q.denominator

    def is_zero(self):return self.lo==self.hi==0

    def encode(self):return [str(self.lo),str(self.hi)]


ZERO=IV(0)
ONE=IV(SCALE)
UNIT=IV(0,SCALE)


def convolution(a,b,degree=None):
    degree=len(a)+len(b)-2 if degree is None else degree
    out=[ZERO]*(degree+1)
    for i,x in enumerate(a):
        if x.is_zero():continue
        for j,y in enumerate(b[:max(0,degree-i+1)]):
            if not y.is_zero():out[i+j]=out[i+j]+x*y
    return out


class TM:
    """Coefficient enclosures plus an absolute symmetric remainder on [0,1]."""
    __slots__=('coeff','radius','degree')

    def __init__(self,coeff,radius=0):
        self.coeff=tuple(IV.coerce(x) for x in coeff)
        self.degree=len(self.coeff)-1
        self.radius=int(radius)
        if self.degree<0 or self.radius<0:raise ValueError('Invalid Taylor model')

    @classmethod
    def constant(cls,value,degree):
        return cls([IV.coerce(value)]+[ZERO]*degree)

    def coerce(self,x):
        if isinstance(x,TM):
            if x.degree!=self.degree:raise ValueError('Mixed polynomial degrees')
            return x
        return TM.constant(x,self.degree)

    def __add__(self,q):
        q=self.coerce(q)
        return TM([a+b for a,b in zip(self.coeff,q.coeff)],self.radius+q.radius)

    __radd__=__add__

    def __neg__(self):return TM([-x for x in self.coeff],self.radius)

    def __sub__(self,q):return self+-self.coerce(q)

    def __rsub__(self,q):return self.coerce(q)+-self

    def polynomial_sup(self):return sum(x.abs_upper() for x in self.coeff)

    def sup(self):return self.polynomial_sup()+self.radius

    def range(self):
        out=ZERO
        for x in reversed(self.coeff):out=out*UNIT+x
        return out+IV(-self.radius,self.radius)

    def __mul__(self,q):
        q=self.coerce(q)
        product=convolution(self.coeff,q.coeff)
        tail=sum(x.abs_upper() for x in product[self.degree+1:])
        tail+=upprod(self.polynomial_sup(),q.radius)
        tail+=upprod(q.polynomial_sup(),self.radius)
        tail+=upprod(self.radius,q.radius)
        return TM(product[:self.degree+1],tail)

    __rmul__=__mul__

    def inverse(self):
        den=self.range().abs_lower()
        if den<=0:raise ZeroDivisionError('Taylor denominator includes zero')
        p0=self.coeff[0]
        v=[p0.inverse().center()]
        for k in range(1,self.degree+1):
            value=sum((self.coeff[j]*v[k-j] for j in range(1,k+1)),ZERO)
            v.append((-value/p0).center())
        prod=convolution(self.coeff,v)
        prod[0]=prod[0]-ONE
        numerator=sum(x.abs_upper() for x in prod)
        numerator+=upprod(self.radius,sum(x.abs_upper() for x in v))
        return TM(v,ceildiv(numerator*SCALE,den))

    def __truediv__(self,q):return self*self.coerce(q).inverse()

    def power(self,n):
        if not isinstance(n,int):raise TypeError('Integer power required')
        if n<0:return self.inverse().power(-n)
        answer=TM.constant(ONE,self.degree)
        base=self
        while n:
            if n&1:answer=answer*base
            n//=2
            if n:base=base*base
        return answer

    def restrict(self,tile,steps,degree):
        if steps<=0 or steps&(steps-1):raise ValueError('Dyadic tile count required')
        if not 0<=tile<steps:raise ValueError('Tile outside domain')
        if not 0<=degree<=self.degree:raise ValueError('Restriction degree mismatch')
        bits=steps.bit_length()-1
        out=[]
        for k in range(self.degree+1):
            lo=hi=0
            for j in range(k,self.degree+1):
                numerator=comb(j,k)*tile**(j-k)
                if numerator==0:continue
                denominator=1 << (bits*j)
                value=self.coeff[j].scale(numerator,denominator)
                lo+=value.lo;hi+=value.hi
            out.append(IV(lo,hi))
        return TM(out[:degree+1],self.radius+sum(x.abs_upper() for x in out[degree+1:]))

    def at(self,n=1,d=1):
        x=IV.rational(n,d)
        out=ZERO
        for value in reversed(self.coeff):out=out*x+value
        return out+IV(-self.radius,self.radius)

    def derivative(self,scale):
        if self.radius:raise ValueError('Cannot differentiate an unproved remainder')
        scale=Fraction(scale)
        return TM([self.coeff[k+1].scale((k+1)*scale.denominator,scale.numerator)
                   for k in range(self.degree)]+[ZERO])

    def encode(self):
        return dict(coefficients=[x.encode() for x in self.coeff],radius=str(self.radius))


def exp_upper(q):
    """Positive rational exponential majorant, with geometric Taylor tail."""
    q=IV.coerce(q)
    if q.lo<0:raise ValueError('Nonnegative exponent required')
    x=IV(q.hi)
    term=total=ONE
    for k in range(1,161):
        term=(term*x).scale(1,k)
        total=total+term
    ratio=x.scale(1,162)
    if ratio.hi>=SCALE:raise ValueError('Exponential proof tail not contractive')
    next_term=(term*x).scale(1,161)
    tail=next_term/(ONE-ratio)
    return total.hi+tail.hi


def upper_fraction(value):return str(Fraction(int(value),SCALE))


def display(value):return float(Fraction(int(value),SCALE))
