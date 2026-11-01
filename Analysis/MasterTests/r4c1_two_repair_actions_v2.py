"""Gauge-specific densities for two explicitly unadopted R4C1 repair candidates.

Covariant definitions live in the pinned candidate specification. Original
source files are never edited. Exact C2 work omits the norm-cubed term only
where the caller explicitly restores its nonzero-tilt derivatives.
"""
from __future__ import annotations
import ast, importlib.util
from pathlib import Path
from types import SimpleNamespace
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
ORIGINAL='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
QUADRATIC='Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'
WEAK='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
F_SLOTS=(0,1,3,9,10,11,12,13)
R_SLOTS=(0,1,3,6,7,8,9,10,11,12,13)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def make_body(route,physical=False):
    if route not in ('F-tau','R-tau'):raise ValueError('unknown candidate')
    tree=ast.parse((ROOT/ORIGINAL).read_text(encoding='utf-8-sig'))
    names={'dot','mv','tr','trans','mm','det3','inv3','tensor','geometry','body'}
    if physical:names|={'val','unary','sqrt','sin','cos','exp','Tape','Node'}
    tree.body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
    find=lambda name:next(n for n in body.body if isinstance(n,ast.Assign)
        and any(isinstance(v,ast.Name) and v.id==name for v in n.targets))
    if not physical:
        force=find('force')
        expected=ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body
        assert ast.dump(force.value)==ast.dump(expected)
        force.value=force.value.left
    if route=='R-tau':
        reg=find('reg')
        expected=ast.parse("par['b']*q[13]**2/2-par['b']*(dot(gz,mv(hp,gp))+q[13]*dot(acc,gp))",mode='eval').body
        assert ast.dump(reg.value)==ast.dump(expected)
        reg.value=ast.Constant(0)
    ast.fix_missing_locations(tree)
    scope={'mp':mp}
    if not physical:
        old=load('two_repair_exact_types',QUADRATIC)
        scope.update(sqrt=old.jsqrt,exp=old.jexp)
    exec(compile(tree,'<declared-two-repair-physical>' if physical else '<declared-two-repair-C2>', 'exec'),scope)
    return SimpleNamespace(**scope)

class ClockGaugeAction:
    def __init__(self,route,parameters,physical=False):
        self.route=route;self.par=parameters;self.physical=physical;self.body=make_body(route,physical)
        weak=load('two_repair_original_weak',WEAK)
        self.core=weak.WeakAction(self.body,parameters)

    def density(self,A):
        if len(A)!=56:raise ValueError('56 original ADM jet slots required')
        cast=mp.mpf if self.physical else s.Integer
        A=[cast(z) if type(z) is int else z for z in A]
        if A[46]!=0:raise ValueError('this backend requires the declared dust-clock gauge')
        if self.route=='F-tau':
            if any(z!=0 for z in A[6:9]+A[22:25]+A[38:41]):
                raise ValueError('F-tau has no independent spatial frame variables')
            return self.core.density(A)
        b=self.body;p=self.par
        q,v,d,S,N,Nz=A[:16],A[16:32],A[32:48],A[48:51],A[54],A[55]
        h=b.tensor(q);hi=b.inv3(h);vol=b.sqrt(b.det3(h))
        c=b.dot(q[6:9],b.mv(h,q[6:9]));gamma=b.sqrt(1+c)
        ps=(v[12]-S[2]*d[12])/N;zh=(v[13]-S[2]*d[13])/N
        # core has no spatial U-regulator, but its original temporal piece
        # remains explicit and must be removed, not silently inherited.
        temporal=-p['b']*zh*(c*ps+gamma*q[8]*d[12])
        reg_clock=p['b']*q[13]**2/2-p['b']*hi[2][2]*d[13]*d[12]
        reg_clock-=p['b']*q[13]*hi[2][2]*(Nz/N)*d[12]
        old,flow=self.core.density(A)
        return old+N*vol*(reg_clock-temporal),flow

def derivative_state(route,w,H,phase,x,ratio):
    slots=F_SLOTS if route=='F-tau' else R_SLOTS
    n=len(slots)
    if len(x)!=2*n+4:raise ValueError('wrong derivative jet count')
    if route=='F-tau' and w!=0:raise ValueError('tilt is not a field of F-tau')
    q=[1,0,0,1,0,1,0,w,0,1,0,1,0,x[-1],0,ratio(1,5)]
    vel=[0]*16;dz=[0]*16
    for j in (0,3,5):vel[j]=2*H
    vel[7]=-H*w;vel[10]=phase;vel[11]=ratio(1,4);vel[12]=ratio(1,5);vel[14]=1
    for i,j in enumerate(slots):vel[j]+=x[i];dz[j]=x[n+i]
    nz=-ratio(2,5)*dz[12]
    return q+vel+dz+[0,0,0]+list(x[2*n:2*n+3])+[1,nz]

