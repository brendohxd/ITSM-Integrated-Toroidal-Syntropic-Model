"""Actual initial cross-normal-form time drift from generic material blocks."""
import argparse
import ast
import copy
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_NORMAL_FORM_TIME_DRIFT_V1_CONTRACT_2026-11-14.md'
SPEC=GATE+'RES001_RTAU_MATERIAL_BLOCK_TIME_EXPORT_V1_SPEC_2026-11-14.md'
PARENT=OUT+'rtau_physical_advection_composition_v1_20261114/receipt.json'
PERIODIC=OUT+'rtau_periodic_principal_composition_v2_20261104/receipt.json'
MIXED=OUT+'rtau_mixed_principal_assembly_v1_20261104/receipt.json'
NORMAL=OUT+'rtau_strong_density_normal_form_v2_20261103/receipt.json'
SETUP='Analysis/MasterTests/test_rtau_ordinary_strong_graph_v1.py'
ORD=[0,1,3,6,7,8,9,10,11]


def load(rel,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def frozen_blocks():
    """Reuse the old certified matrix inverse construction, not an experiment."""
    old=load(SETUP,'normal_form_time_frozen_blocks')
    parents={k:read(v) for k,v in old.PARENTS.items()}
    tree=ast.parse((ROOT/SETUP).read_text())
    fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
    target=lambda n,k:isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==k for t in n.targets)
    start=next(i for i,n in enumerate(fn.body) if target(n,'z'))
    stop=next(i for i,n in enumerate(fn.body) if target(n,'ii'))
    fn.name='frozen';fn.body=fn.body[start:stop]+[ast.Return(ast.Call(ast.Name('locals',ast.Load()),[],[]))]
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    env=dict(mp=mp,iv=iv,parents=parents,principal=parents['principal'],ROOT=ROOT,
             FACTORY=old.FACTORY,SLOTS=ORD,importlib=importlib,lo=lo,hi=hi,
             ab=lambda x:max(abs(lo(x)),abs(hi(x))),
             decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x]),check=lambda n,ok,*args:assertion(ok,n))
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-material-block-values>', 'exec'),env)
    return env['frozen']()


def assertion(ok,name):
    assert bool(ok),name


def exact_controls():
    t,S=sp.symbols('t S')
    A=sp.Matrix([[2+t,sp.Rational(1,7)+t/11],[sp.Rational(1,7)+t/11,3+2*t]])
    C=sp.Matrix([[1+t,sp.Rational(1,3)],[sp.Rational(1,5),2-t]])
    K=sp.Matrix([[4+t,sp.Rational(1,13)],[sp.Rational(1,13),5-t]])
    B=sp.Matrix([[2+t,3],[1,4-t]])
    D=sp.Matrix([[1,2+t],[3-t,1]])
    KI=K.inv();M=A-C*KI*C.T
    corrected=B-S*A-C*KI*(D-S*C).T+S*M
    reference=B-C*KI*D.T
    zero=lambda x:all(sp.cancel(v)==0 for v in x)
    inv=sp.Matrix([[2+t,1+2*t],[3-t,4+t]])
    reciprocal=inv.inv()
    OF=sp.Matrix([[1+t,2],[3,1-t]])
    forward=-OF*reciprocal
    forward_t=-OF.diff(t)*reciprocal+OF*reciprocal*inv.diff(t)*reciprocal
    # Generic metric directional rates are evaluated before a conformal slice.
    h=sp.Matrix([[2+t,sp.Rational(1,5)+t/7],[sp.Rational(1,5)+t/7,3+2*t]])
    hj=h.subs(t,0);ht=h.diff(t)
    det=h.det()
    q,ga,p,s,w,k,Aforce,Kforce=sp.symbols('q gamma p s w k A K',positive=True)
    cv=ga**2-1
    Y=cv*p*p+2*ga*w*p*s+(k+w*w)*s*s
    force=Kforce*(ga*p+w*s)**2/2-Aforce*Y**sp.Rational(3,2)
    fpp=sp.diff(force,p,2)
    clock_defect=sp.diff(fpp,p).subs({ga:sp.sqrt(5)/2,w:0,s:0,p:sp.Rational(1,5),k:1})
    return dict(exact_material_shift_cancellation=zero(corrected-reference),
                exact_material_shift_rate_cancellation=zero(sp.diff(corrected-reference,S)),
                exact_inverse_time_derivative=zero(reciprocal.diff(t)+reciprocal*inv.diff(t)*reciprocal),
                exact_noncommuting_forward_block_product=zero(forward.diff(t)-forward_t),
                omitted_inverse_rate_rejected=not zero((OF*reciprocal*inv.diff(t)*reciprocal).subs(t,0)),
                exact_generic_metric_inverse_rate=zero(h.inv().diff(t).subs(t,0)+hj.inv()*ht*hj.inv()),
                exact_generic_volume_log_rate=sp.cancel(sp.diff(det,t).subs(t,0)/det.subs(t,0)-(hj.inv()*ht).trace())==0,
                omitted_normal_clock_rate_rejected=sp.simplify(clock_defect)!=0)


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    ab=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    parent=read(PARENT);data={k:read(p) for k,p in [('periodic',PERIODIC),('mixed',MIXED),('normal',NORMAL)]}
    pins=dict(parent['source_pins'])
    for rel in (CONTRACT,SPEC,PARENT,PERIODIC,MIXED,NORMAL,SETUP,Path(__file__).relative_to(ROOT).as_posix()):
        p=ROOT/rel;h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for d in (parent,*data.values()) for c in d['checks'])
    checks=exact_controls()
    old=frozen_blocks();ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J,D=ctx['J'],ctx['D']
    y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q,vel,grad=y[:14],y[14:28],y[28:42]
    time=lambda v,d:J(coefficients=[v,d,iv.mpf(0)])
    qtime=[time(x.c[0],v.c[0]) for x,v in zip(q,vel)]
    N0=ctx['geometry'](q,grad)[0]
    p0=(vel[12]-y[44]*grad[12])/N0
    # Ordinary principal Hessians are independent of these derivative values.
    # Keep the nonlinear force on its actual positive-Y branch nevertheless.
    Ntime=ctx['geometry'](qtime,[J(0)]*14)[0]
    s=time(grad[12].c[0],vel[12].c[1])
    args=qtime+[J(0)]*14+[J(0)]*14+[J(0)]*6
    args[26]=Ntime*p0.c[0];args[40]=s
    active=[14+i for i in ORD]+[28+i for i in ORD]+[45,46,47]
    variables=[D.var(v,i) if i in active else D(v) for i,v in enumerate(args)]
    clock=ctx['env']
    result=clock['density'](clock['lifted'](variables))[0]
    hh=lambda i,j:result.h.get(tuple(sorted((i,j))),J(0))
    vs,ds,ws=[14+i for i in ORD],[28+i for i in ORD],[45,46,47]
    # Values are at zero shift: B0 and D0 are material raw blocks.
    exports={k:[[hh(i,j) for j in cols] for i in rows] for k,rows,cols in
             [('A',vs,vs),('B',vs,ds),('Cshift',vs,ws),('Drel',ds,ws),('Kshift',ws,ws)]}
    def overlaps(a,b):return max(lo(a),lo(b))<=min(hi(a),hi(b))
    raw=old['hh'];shift=old['shift']
    expected={
        'A':[[raw(i,j) for j in vs] for i in vs],
        'B':[[raw(i,j)+shift*raw(i,14+(j-28)) for j in ds] for i in vs],
        'Cshift':old['C'],
        'Drel':old['add'](old['D'],old['scale'](old['C'],shift)),
        'Kshift':[[raw(i,j) for j in ws] for i in ws],
    }
    checks['material_block_values_consistent_with_original_export']=all(overlaps(x.c[0],v) for k,a in exports.items() for row,srow in zip(a,expected[k]) for x,v in zip(row,srow))

    class Pair:
        def __init__(self,v=0,t=0):
            cast=lambda x:x if hasattr(x,'_mpi_') or hasattr(x,'_mpci_') else iv.mpf(x)
            self.v,self.t=cast(v),cast(t)
        @classmethod
        def cast(cls,x):return x if isinstance(x,cls) else cls(x)
        def __add__(self,x):
            x=self.cast(x);return Pair(self.v+x.v,self.t+x.t)
        __radd__=__add__
        def __neg__(self):return Pair(-self.v,-self.t)
        def __sub__(self,x):return self+-self.cast(x)
        def __rsub__(self,x):return self.cast(x)+-self
        def __mul__(self,x):
            x=self.cast(x);return Pair(self.v*x.v,self.t*x.v+self.v*x.t)
        __rmul__=__mul__
        def __truediv__(self,x):
            x=self.cast(x);value=self.v/x.v;return Pair(value,(self.t-value*x.t)/x.v)
        def __rtruediv__(self,x):return self.cast(x)/self

    mat=lambda n,m:[[Pair() for _ in range(m)] for _ in range(n)]
    tr=lambda a:[list(r) for r in zip(*a)]
    mul=lambda a,b:[[sum((a[i][k]*b[k][j] for k in range(len(b))),Pair()) for j in range(len(b[0]))] for i in range(len(a))]
    add=lambda a,b,sign=1:[[x+y*sign for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    scale=lambda a,c:[[x*c for x in row] for row in a]
    fromjet=lambda x:Pair(x.c[0],x.c[1])
    A,B,C,Drel,K=[[[fromjet(x) for x in row] for row in exports[k]] for k in ('A','B','Cshift','Drel','Kshift')]
    oldmul=old['mul'];oldscale=old['scale']
    Kt=[[x.t for x in row] for row in K]
    KIt=oldscale(oldmul(oldmul(old['KI'],Kt),old['KI']),-1)
    KI=[[Pair(v,d) for v,d in zip(row,drow)] for row,drow in zip(old['KI'],KIt)]
    MP=add(A,mul(mul(C,KI),tr(C)),-1)
    BPraw=add(B,mul(mul(C,KI),tr(Drel)),-1)
    MIt=oldscale(oldmul(oldmul(old['MI'],[[x.t for x in row] for row in MP]),old['MI']),-1)
    MI0=oldscale(old['add'](old['MI'],old['tr'](old['MI'])),iv.mpf(1)/2)
    MI=[[Pair(v,d) for v,d in zip(row,drow)] for row,drow in zip(MI0,MIt)]
    BP0=[row[:] for row in old['BR']]
    for i in range(9):BP0[i][5]=iv.mpf(int(i in (0,2)))/(2*old['coefficient'])
    BP=[[Pair(v,x.t) for v,x in zip(row,trow)] for row,trow in zip(BP0,BPraw)]

    # Generic metric/force differentials are independent of the selected
    # principal AD variables; all their actual initial time rates are retained.
    Q=[D.var(x,i) for i,x in enumerate(qtime)]
    ND,mu,gam,Hinv,_=ctx['geometry'](Q,[D(0)]*14)
    p_rate=ab(decode(data['normal']['bounds_binary']['normal_p_time']))
    pn=time(p0.c[0],iv.mpf([-hi(p_rate),hi(p_rate)]))
    pd,sd=D.var(pn,100),D.var(s,101)
    h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
    rest=[Hinv[i][2]*sd+Q[6+i]*(pd+Q[8]*sd/(gam+1)) for i in range(3)]
    YY=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
    YY+=2*sum((h[i][j]*rest[i]*rest[j] for i in range(3) for j in range(i+1,3)),D(0))
    checks['generic_force_positive_Y']=lo(YY.c.c[0])>0
    assert checks['generic_force_positive_Y']
    pars=ctx['env']['env']['exact']
    rat=lambda q:iv.mpf(int(q.p))/int(q.q)
    KQ,Aforce,b=[rat(pars[k]) for k in ('K_Q','A','b')]
    force=(gam*pd+Q[8]*sd)**2*KQ/2-YY**mp.mpf('1.5')*Aforce
    fp=force.g[100];fpp=force.h[100,100];fps=force.h[100,101]
    checks['actual_force_temporal_mass_positive']=lo(fpp.c[0])>0
    assert checks['actual_force_temporal_mass_positive']
    kj=Hinv[2][2].c;Nj=ND.c;mj=mu.c*fpp/Nj
    qaux=[-(kj*mu.g.get(i,J(0))/mu.c+Hinv[2][2].g.get(i,J(0)))*s for i in ORD]
    tq=[mu.g.get(i,J(0))*fp+mu.c*force.h.get(tuple(sorted((100,i))),J(0)) for i in ORD]
    aq=[x*Nj*mu.c*b for x in qaux]
    cj=gam.c/(qtime[0]**mp.mpf('.5'))
    kappa,aphi,sj,cjP=[fromjet(x) for x in (kj,1/mj,s,cj)]
    vp=fromjet(Nj*fps/fpp)
    dj=Nj*mu.c*kj*b;dp=fromjet(dj)
    ii=Pair(iv.mpc(0,1))
    E=sp.zeros(9,8);E[0,0]=1;E[2,0]=-1;E[1,1]=1
    for j in range(2,8):E[j+1,j]=1
    L,Pmom=mat(9,18),mat(9,18)
    for i in range(9):
        for j in range(8):L[i][1+j]=Pair(int(E[i,j]))
        Pmom[i][9+i]=Pair(1)
    L[0][14]=L[2][14]=ii*cjP
    V=mul(MI,add(Pmom,scale(mul(BP,L),ii),-1))
    W=scale(mul(KI,add(mul(tr(C),V),scale(mul(tr(Drel),L),ii))),-1)
    Qaux=[[fromjet(x) for x in qaux]];Tq=[[fromjet(x) for x in tq]]
    qv,ql,tx=mul(Qaux,V)[0],mul(Qaux,L)[0],mul(Tq,L)[0]
    FO=[[-kappa*aphi*tx[j]+ii*qv[j]-ii*kappa*sj*W[2][j]-vp*ql[j] for j in range(18)],mat(1,18)[0]]
    OF=mat(18,2)
    for i,x in enumerate(aq):OF[9+i][0]=ii*fromjet(x)
    Ainv=[[Pair(),-1/dp],[1/(kappa*aphi),Pair()]]
    Cof=scale(mul(OF,Ainv),-1);Cfo=mul(Ainv,FO)
    cross=mat(20,20)
    for i in range(18):
        for j in range(2):cross[i][18+j]=Cof[i][j]
    for i in range(2):
        for j in range(18):cross[18+i][j]=Cfo[i][j]
    stored=data['mixed']['cross_normal_form_matrix_binary']
    def compatible(z,enc):
        return all(overlaps(getattr(z,part),decode(enc[part])) for part in ('real','imag'))
    checks['generic_cross_values_consistent_with_registered_normal_form']=all(compatible(x.v,e) for row,srow in zip(cross,stored) for x,e in zip(row,srow))
    def magnitude(z):return iv.sqrt(ab(z.real)**2+ab(z.imag)**2)
    derivatives=[x.t for row in cross for x in row]
    Ctime=iv.sqrt(sum((magnitude(x)**2 for x in derivatives),iv.mpf(0)))
    inverse=decode(data['periodic']['values_binary']['global_T_inverse_norm'])
    transformed=Ctime*inverse
    zero=lambda x:x.real==0 and x.imag==0
    checks.update(original_density_row_and_column_time_drift_zero=all(zero(x.t) for x in cross[0]) and all(zero(row[0].t) for row in cross),
                  both_cross_directions_retained=any(not zero(x.t) for row in Cof for x in row) and any(not zero(x.t) for row in Cfo for x in row),
                  actual_clock_rate_uncertainty_retained=hi(p_rate)>0,
                  finite_initial_time_drift=all(lo(v)>=0 and mp.isfinite(hi(v)) for v in (Ctime,transformed)),
                  immutable_sources_and_sidecars=all((digest(f),f.stat().st_mtime_ns)==v for f,v in snap.items()))
    assert all(checks.values()),checks
    encode=lambda z:dict(real=binary(z.real),imag=binary(z.imag))
    export=lambda jets:[[[binary(x.c[0]),binary(x.c[1])] for x in row] for row in jets]
    return dict(kind='RTAU_INITIAL_NORMAL_FORM_TIME_DRIFT_V1',source_pins=pins,pinned_files=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                material_blocks_value_time_binary={k:export(a) for k,a in exports.items()},
                cross_matrix_time_binary=[[encode(x.t) for x in row] for row in cross],
                bounds_binary=dict(C_time=binary(Ctime),T_time=binary(Ctime),T_time_times_inverse=binary(transformed),normal_p_time=binary(p_rate)),
                upper_display=dict(C_time=mp.nstr(hi(Ctime),30),T_time_times_inverse=mp.nstr(hi(transformed),30)),
                operator_identity='T_t=i*P*C_t at fixed original coordinate',
                scope='CONDITIONAL_INITIAL_NORMAL_FORM_TIME_DRIFT_ONLY',
                energy_time_derivative='OPEN',domain_persistence='OPEN',background_time_tube='OPEN',
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Byte-identical normal-form time-drift replay')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=False)
        with a.output.open('xb') as f:f.write(raw)
        print('Initial normal-form time drift verified')


if __name__=='__main__':main()
