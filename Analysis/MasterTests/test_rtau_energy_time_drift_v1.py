"""Initial time drift of the registered diagonal and pulled-back energies."""
import argparse
import ast
import copy
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
import test_rtau_normal_form_time_drift_v1 as time_owner
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_ENERGY_TIME_DRIFT_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_normal_form_time_drift_v1_20261114/receipt.json'
ORDINARY=OUT+'rtau_ordinary_ward_energy_v4_20261104/receipt.json'
PERIODIC=OUT+'rtau_periodic_principal_composition_v2_20261104/receipt.json'
NORMAL=OUT+'rtau_strong_density_normal_form_v2_20261103/receipt.json'
TIME_SOURCE='Analysis/MasterTests/test_rtau_normal_form_time_drift_v1.py'
ORD=time_owner.ORD


def exact_controls():
    t=sp.symbols('t',real=True)
    C=sp.Matrix([[2+t,1+2*t],[3-t,4+t]])
    b=sp.Matrix([[1+t,2-t]])
    ell=b*C.inv()
    zero=lambda m:all(sp.cancel(v)==0 for v in m)
    inverse_rate=(b.diff(t)-ell*C.diff(t))*C.inv()
    c=1+t/7
    F=sp.eye(4);F[1,1]=1/c;F[2,1]=1/(2*c);F[3,1]=-1/(3*c)
    J=sp.eye(4);J[1,2]=-ell[0];J[1,3]=-ell[1]
    HC=sp.Matrix([[2+t,sp.Rational(1,5)+t/11],[sp.Rational(1,5)+t/11,3-t]])
    seed=sp.diag(1,1,HC)
    H=F.T*J.T*seed*J*F
    rate=(F.diff(t).T*J.T*seed*J*F+F.T*J.diff(t).T*seed*J*F
          +F.T*J.T*seed.diff(t)*J*F+F.T*J.T*seed*J.diff(t)*F
          +F.T*J.T*seed*J*F.diff(t))
    u=sp.Matrix([1,2,3,4])
    return dict(exact_stationary_row_time_identity=zero(ell.diff(t)-inverse_rate),
                exact_full_energy_factor_derivative=zero((H.diff(t)-rate).subs(t,0)),
                exact_nonzero_zero_sector_energy_rate=zero(((u.T*H*u).diff(t)-u.T*rate*u).subs(t,0)),
                omitted_stationary_row_rate_rejected=not zero(J.diff(t).subs(t,0)),
                omitted_chart_rate_rejected=not zero(F.diff(t).subs(t,0)),
                omitted_complement_energy_rate_rejected=not zero(HC.diff(t)),
                noncommuting_energy_fixture=C.subs(t,0)*HC.subs(t,0)!=HC.subs(t,0)*C.subs(t,0))


def calculate():
    mp.mp.dps,mp.iv.dps=100,60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    ab=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    parent=read(PARENT);ordinary=read(ORDINARY);periodic=read(PERIODIC);normal=read(NORMAL)
    pins=dict(parent['source_pins'])
    for rel in (CONTRACT,PARENT,ORDINARY,PERIODIC,NORMAL,TIME_SOURCE,Path(__file__).relative_to(ROOT).as_posix()):
        p=ROOT/rel;h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for d in (parent,ordinary,periodic,normal) for c in d['checks'])
    checks=exact_controls()
    old=time_owner.frozen_blocks();ctx=factory.prepare();mp.mp.dps,mp.iv.dps=100,60
    J,D=ctx['J'],ctx['D']
    y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q,vel,grad=y[:14],y[14:28],y[28:42]
    time=lambda v,d:J(coefficients=[v,d,iv.mpf(0)])
    qtime=[time(x.c[0],v.c[0]) for x,v in zip(q,vel)]
    N0=ctx['geometry'](q,grad)[0];p0=(vel[12]-y[44]*grad[12])/N0
    Ntime=ctx['geometry'](qtime,[J(0)]*14)[0]
    s=time(grad[12].c[0],vel[12].c[1])
    args=qtime+[J(0)]*14+[J(0)]*14+[J(0)]*6
    args[26]=Ntime*p0.c[0];args[40]=s
    ds=[28+i for i in ORD]
    variables=[D.var(v,i) if i in ds else D(v) for i,v in enumerate(args)]
    clock=ctx['env'];result=clock['density'](clock['lifted'](variables))[0]
    hh=lambda i,j:result.h.get(tuple(sorted((i,j))),J(0))
    Gjets=[[hh(i,j) for j in ds] for i in ds]
    raw=old['hh'];shift=old['shift']
    overlaps=lambda a,b:max(lo(a),lo(b))<=min(hi(a),hi(b))
    expected=[[raw(i,j)+shift*(raw(i,14+j-28)+raw(14+i-28,j))+shift**2*raw(14+i-28,14+j-28) for j in ds] for i in ds]
    checks['generic_material_gradient_values_consistent_with_export']=all(overlaps(x.c[0],v) for row,srow in zip(Gjets,expected) for x,v in zip(row,srow))

    # Reuse the already checked first-time-jet arithmetic class.
    tree=ast.parse((ROOT/TIME_SOURCE).read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    pair=copy.deepcopy(next(n for n in fn.body if isinstance(n,ast.ClassDef) and n.name=='Pair'))
    env={'iv':iv}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[pair],type_ignores=[])),'<frozen-first-time-pair>', 'exec'),env)
    Pair=env['Pair']
    def conj(x):
        return Pair(iv.mpc(x.v.real,-x.v.imag),iv.mpc(x.t.real,-x.t.imag))
    mat=lambda n,m:[[Pair() for _ in range(m)] for _ in range(n)]
    tr=lambda a:[list(row) for row in zip(*a)]
    dag=lambda a:[[conj(x) for x in row] for row in tr(a)]
    mul=lambda a,b:[[sum((a[i][k]*b[k][j] for k in range(len(b))),Pair()) for j in range(len(b[0]))] for i in range(len(a))]
    add=lambda a,b,sign=1:[[x+y*sign for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    scale=lambda a,c:[[x*c for x in row] for row in a]
    fromjet=lambda x:Pair(x.c[0],x.c[1])
    exports=parent['material_blocks_value_time_binary']
    A,B,C,Drel,K=[[[Pair(decode(x[0]),decode(x[1])) for x in row] for row in exports[k]] for k in ('A','B','Cshift','Drel','Kshift')]
    G=[[fromjet(x) for x in row] for row in Gjets]
    mm,ms=old['mul'],old['scale']
    KIt=ms(mm(mm(old['KI'],[[x.t for x in row] for row in K]),old['KI']),-1)
    KI=[[Pair(v,d) for v,d in zip(row,drow)] for row,drow in zip(old['KI'],KIt)]
    MP=add(A,mul(mul(C,KI),tr(C)),-1)
    BPraw=add(B,mul(mul(C,KI),tr(Drel)),-1)
    GPraw=add(G,mul(mul(Drel,KI),tr(Drel)),-1)
    MI0=ms(old['add'](old['MI'],old['tr'](old['MI'])),iv.mpf(1)/2)
    MIt=ms(mm(mm(old['MI'],[[x.t for x in row] for row in MP]),old['MI']),-1)
    MI=[[Pair(v,d) for v,d in zip(row,drow)] for row,drow in zip(MI0,MIt)]
    BP0=[row[:] for row in old['BR']];GP0=ms(old['add'](old['GR'],old['tr'](old['GR'])),iv.mpf(1)/2)
    for i in range(9):
        BP0[i][5]=iv.mpf(int(i in (0,2)))/(2*old['coefficient'])
        GP0[i][5]=GP0[5][i]=iv.mpf(0)
    BP=[[Pair(v,x.t) for v,x in zip(row,trow)] for row,trow in zip(BP0,BPraw)]
    GP=[[Pair(v,x.t) for v,x in zip(row,trow)] for row,trow in zip(GP0,GPraw)]

    # Reuse the full-force time-jet expressions without rerunning the ordinary
    # action export or the cross-normal-form experiment.
    target=lambda n,k:isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id==k for v in n.targets)
    first=next(i for i,n in enumerate(fn.body) if target(n,'Q'))
    last=next(i for i,n in enumerate(fn.body) if target(n,'cj'))
    force_env=dict(ctx=ctx,J=J,D=D,qtime=qtime,p0=p0,s=s,mp=mp,iv=iv,
                   hi=hi,lo=lo,ab=ab,decode=decode,data={'normal':normal},checks=checks,ORD=ORD)
    exec(compile(ast.fix_missing_locations(ast.Module(body=copy.deepcopy(fn.body[first:last+1]),type_ignores=[])),'<frozen-generic-force-time-jets>','exec'),force_env)
    cj,mj,kj,Nj,mu,b=[force_env[k] for k in ('cj','mj','kj','Nj','mu','b')]
    c=fromjet(cj);ii=Pair(iv.mpc(0,1))
    E=sp.zeros(9,8);E[0,0]=1;E[2,0]=-1;E[1,1]=1
    R=sp.zeros(8,9);R[0,0]=sp.Rational(1,2);R[0,2]=-sp.Rational(1,2);R[1,1]=1
    for j in range(2,8):E[j+1,j]=R[j,j+1]=1
    Rp=[[Pair(iv.mpf(int(R[i,j].p))/int(R[i,j].q)) for j in range(9)] for i in range(8)]
    qkeep=[0,1,2,3,5,6,7]
    XC,PC=mat(9,16),mat(9,16)
    for j,slot in enumerate(qkeep):
        for i in range(9):XC[i][j]=Pair(int(E[i,slot]))
    for i in range(9):PC[i][7+i]=Pair(1)
    XC[0][12]=XC[2][12]=ii*c
    KC=add(PC,scale(mul(BP,XC),ii),-1)
    VC=mul(MI,KC);PDC=add(scale(mul(tr(BP),VC),-ii),mul(GP,XC));QDC=mul(Rp,VC)
    bc=[[ii*x/(2*c) for x in VC[5]]]
    CC=[QDC[i] for i in qkeep]+[[PDC[i][j]-(bc[0][j] if i in (0,2) else 0) for j in range(16)] for i in range(9)]
    HC=add(mul(mul(dag(KC),MI),KC),mul(mul(dag(XC),GP),XC),-1)
    def compatible(z,enc):return all(overlaps(getattr(z,part),decode(enc[part])) for part in ('real','imag'))
    checks['complement_energy_values_match_preserved_owner']=all(compatible(x.v,e) for row,srow in zip(HC,ordinary['energy_complement_binary']) for x,e in zip(row,srow))
    checks['complement_generator_values_match_preserved_owner']=all(compatible(x.v,e) for row,srow in zip(CC,ordinary['generator_complement_binary']) for x,e in zip(row,srow))
    checks['stationary_row_values_match_preserved_owner']=all(compatible(x.v,e) for x,e in zip(bc[0],ordinary['zero_to_complement_row_binary']))
    magnitude=lambda z:iv.sqrt(ab(z.real)**2+ab(z.imag)**2)
    norm=lambda rows:iv.sqrt(sum((magnitude(x)**2 for row in rows for x in row),iv.mpf(0)))
    derivatives=lambda a:[[x.t for x in row] for row in a]
    cinv=decode(ordinary['bounds']['normalized_complement_inverse_bound_binary'])*iv.sqrt(iv.mpf(99)/2)
    ell=decode(ordinary['ordinary_norm_constants']['zero_charge_row_norm_upper_binary'])
    bt=norm(derivatives(bc));ct=norm(derivatives(CC));hct=norm(derivatives(HC))
    ellt=(bt+ell*ct)*cinv
    cmin=iv.mpf(lo(c.v));fnorm=iv.sqrt(17+3/(4*cmin**2))
    ft=iv.sqrt(3)*ab(c.t)/(2*cmin**2)
    eh=iv.mpf(max(mp.mpf(1),hi(decode(ordinary['bounds']['action_energy_upper_binary']))))
    pieces=dict(chart_time=2*fnorm*ft*(1+ell)**2*eh,
                stationary_row_time=2*fnorm**2*(1+ell)*ellt*eh,
                complement_energy_time=fnorm**2*(1+ell)**2*hct)
    hordt=sum(pieces.values(),iv.mpf(0))
    fast1=Nj*mu.c*b;fast2=1/mj
    hfastt=iv.mpf(max(hi(ab(fast1.c[1])),hi(ab(fast2.c[1]))))
    diagonal=iv.mpf(max(hi(hordt),hi(hfastt)))
    H0=iv.mpf(max(hi(decode(ordinary['ordinary_norm_constants']['energy_upper_binary'])),hi(fast1.c[0]),hi(fast2.c[0])))
    T0=decode(periodic['values_binary']['global_T_norm'])
    Tt=decode(parent['bounds_binary']['T_time'])
    pulled=T0*T0*diagonal+2*T0*H0*Tt
    bounds=dict(complement_generator_time=ct,complement_energy_time=hct,stationary_drive_time=bt,
                complement_inverse=cinv,stationary_row=ell,stationary_row_time=ellt,
                chart=fnorm,chart_time=ft,seed_energy=eh,ordinary_energy_time=hordt,
                fast_energy_time=hfastt,diagonal_energy_time=diagonal,
                diagonal_energy=H0,pulled_back_energy_time=pulled)
    checks.update(both_zero_speed_directions_retained=len(CC)==16 and qkeep==[0,1,2,3,5,6,7] and len(Rp)==8,
                  complete_ordinary_energy_derivative_has_three_parts=len(pieces)==3,
                  time_chart_and_stationary_parts_not_zero=hi(pieces['chart_time'])>0 and hi(pieces['stationary_row_time'])>0,
                  finite_positive_initial_energy_time_bounds=all(lo(v)>=0 and mp.isfinite(hi(v)) for v in bounds.values()),
                  immutable_sources_and_sidecars=all((digest(f),f.stat().st_mtime_ns)==v for f,v in snap.items()))
    assert all(checks.values()),checks
    encode=lambda z:dict(real=binary(z.real),imag=binary(z.imag))
    return dict(kind='RTAU_INITIAL_ENERGY_TIME_DRIFT_V1',source_pins=pins,pinned_files=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                gradient_block_value_time_binary=[[[binary(x.c[0]),binary(x.c[1])] for x in row] for row in Gjets],
                complement_energy_time_binary=[[encode(x.t) for x in row] for row in HC],
                complement_generator_time_binary=[[encode(x.t) for x in row] for row in CC],
                stationary_drive_time_binary=[[encode(x.t) for x in row] for row in bc],
                fast_energy_value_time_binary=[[binary(x.c[0]),binary(x.c[1])] for x in (fast1,fast2)],
                contribution_bounds_binary={k:binary(v) for k,v in pieces.items()},
                bounds_binary={k:binary(v) for k,v in bounds.items()},
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                energy_definition='Hdiag=diag(Hordinary,d/kappa,aphi); Horiginal=T^dagger Hdiag T',
                scope='CONDITIONAL_INITIAL_CONTROLLING_ENERGY_TIME_DERIVATIVE_ONLY',
                full_coupled_energy_inequality='OPEN',finite_partner_rate_assembly='OPEN',
                domain_persistence='OPEN',background_time_tube='OPEN',
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Byte-identical energy-time replay')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=False)
        with a.output.open('xb') as f:f.write(raw)
        print('Initial controlling-energy time derivative verified')


if __name__=='__main__':main()
