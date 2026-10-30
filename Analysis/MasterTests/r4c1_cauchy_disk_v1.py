"""Exact rational outward complex-disk majorant for an analytic action summand.

Centers are real rationals; radii bound complex deviations. Radius rounding is
outward to a dyadic grid. This is not a physical cutoff or evolution solver.
"""
from fractions import Fraction as F
from math import isqrt

BITS=80
operations=0
inverse_margins=[]
sqrt_margins=[]


def fraction(x):
    if isinstance(x,F):return x
    if isinstance(x,int):return F(x)
    if hasattr(x,'_mpf_'):
        sign,man,exp,_=x._mpf_
        return F((-1 if sign else 1)*man)*(F(2)**exp)
    if hasattr(x,'p') and hasattr(x,'q'):return F(int(x.p),int(x.q))
    raise TypeError('non-exact disk operand '+repr(type(x)))


def outward(x,bits=BITS):
    x=fraction(x);scale=1<<bits
    return F(-((-x.numerator*scale)//x.denominator),scale)


class Disk:
    __slots__=('c','r')
    def __init__(self,center=0,radius=0):
        self.c=fraction(center);self.r=outward(radius)
        if self.r<0:raise ValueError('negative radius')
    @staticmethod
    def cast(x):return x if isinstance(x,Disk) else Disk(x)
    def __add__(self,x):
        global operations
        operations+=1;x=self.cast(x);return Disk(self.c+x.c,self.r+x.r)
    __radd__=__add__
    def __neg__(self):return Disk(-self.c,self.r)
    def __sub__(self,x):return self+-self.cast(x)
    def __rsub__(self,x):return self.cast(x)+-self
    def __mul__(self,x):
        global operations
        operations+=1;x=self.cast(x)
        return Disk(self.c*x.c,abs(self.c)*x.r+abs(x.c)*self.r+self.r*x.r)
    __rmul__=__mul__
    def inverse(self):
        global operations
        operations+=1;margin=abs(self.c)-self.r
        if margin<=0:raise ValueError('complex disk inverse crosses zero')
        inverse_margins.append(margin)
        return Disk(1/self.c,self.r/(abs(self.c)*margin))
    def __truediv__(self,x):return self*self.cast(x).inverse()
    def __rtruediv__(self,x):return self.cast(x)*self.inverse()
    def sqrt(self):
        global operations
        operations+=1
        if self.c<=self.r:raise ValueError('sqrt disk not in positive half-plane')
        a,b=isqrt(self.c.numerator),isqrt(self.c.denominator)
        if a*a!=self.c.numerator or b*b!=self.c.denominator:
            raise ValueError('sqrt center not an exact rational square')
        center=F(a,b);sqrt_margins.append(self.c-self.r)
        # |sqrt(z)-sqrt(c)|=|z-c|/|sqrt(z)+sqrt(c)| <= r/sqrt(c).
        return Disk(center,self.r/center)
    def __pow__(self,e):
        e=fraction(e)
        if e==F(1,2):return self.sqrt()
        if e.denominator!=1:raise ValueError('unverified analytic power '+str(e))
        n=e.numerator
        if n<0:return (self.inverse())**(-n)
        out=Disk(1);base=self
        while n:
            if n&1:out=out*base
            n//=2
            if n:base=base*base
        return out
    def __eq__(self,x):
        x=self.cast(x);return self.c==x.c and self.r==x.r
    def upper(self):return abs(self.c)+self.r


def reset():
    global operations
    operations=0;inverse_margins.clear();sqrt_margins.clear()


def initial_polydisc():
    delta=F(1,1000);q=[Disk(0,delta) for _ in range(14)]
    for i in (0,3,5):q[i]=Disk(1,delta)
    for i in (9,11):q[i]=Disk(F(1,2),delta)
    q[7]=Disk(0,F(1,1000)+delta);q[13]=Disk(0,F(1,1000)+delta)
    return q+[Disk(0,2+delta) for _ in range(14)]+[Disk(0,1+delta) for _ in range(14)]+[Disk(0,1+delta) for _ in range(6)]


def summary(value):
    bound=value.upper();integer=-((-bound.numerator)//bound.denominator)
    return dict(radius_bits=BITS,operations=operations,center=str(value.c),radius=str(value.r),
                absolute_upper=str(bound),integer_upper=integer,
                inverse_checks=len(inverse_margins),sqrt_checks=len(sqrt_margins),
                minimum_inverse_margin=str(min(inverse_margins)),minimum_sqrt_margin=str(min(sqrt_margins)))
