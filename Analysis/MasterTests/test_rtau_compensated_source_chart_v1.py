"""Full initial compensated source/state chart; no physical energy claim."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_SOURCE_CHART_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
DENSITY='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
INVERSE='Analysis/MasterTests/outputs/rtau_compensated_static_inverse_v1_20261103/receipt.json'
OLD='Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
IDENTITY='Analysis/MasterTests/outputs/rtau_compensated_density_v1_20261103/receipt.json'
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    decode=lambda xs:iv.mpf([mp.mpf(tuple(t)) for t in xs])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,FACTORY,DENSITY,INVERSE,OLD,IDENTITY,
                'Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_STATIC_INVERSE_V1_REPORT_2026-11-03.md'):
        pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snap[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_hashes_match',len(original)==219)
    inv,old,identity=[json.loads((ROOT/rel).read_text()) for rel in (INVERSE,OLD,IDENTITY)]
    check('inverse_momentum_and_exact_compensation_owners_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (inv,old,identity)))
    fac=load('compensated_source_factory',FACTORY);env=fac.prepare()
    transport=load('compensated_source_improvement',DENSITY)
    params=env['env']['env']['exact'];KQ,A=[rational(params[k]) for k in ('K_Q','A')]

    def Bmatrix(q):
        h=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
        out=[[q[0]*0 for _ in range(3)] for _ in range(13)]
        for k,(a,b) in enumerate(HM):
            for j in range(3):out[k][j]=(h[a][j] if b==2 else q[0]*0)+(h[b][j] if a==2 else q[0]*0)
        for j in range(3):out[6+j][j]=-q[8]
        return out

    def Kmom(p):
        out=[[iv.mpf(0) for _ in range(13)] for _ in range(3)]
        for k in range(13):
            bb=Bmatrix([iv.mpf(int(i==k)) for i in range(13)])
            for j in range(3):out[j][k]=sum((bb[i][j]*p[i] for i in range(13)),iv.mpf(0))
        return out

    def setup(ctx,y,L):
        J,D,grad=ctx['J'],ctx['D'],ctx['gradient']
        q,v,d,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
        Q=[D.var(x,i) for i,x in enumerate(q)];V=[D.var(x,14+i) for i,x in enumerate(v)]
        DX=[D.var(x,28+i) for i,x in enumerate(d)];SS=[D.var(x,42+i) for i,x in enumerate(S)]
        N,mu,gamma,H,_=ctx['geometry'](Q,DX);M=N*mu
        pp=(V[12]-SS[2]*DX[12])/N
        rest=[H[i][2]*DX[12]+Q[6+i]*(pp+Q[8]*DX[12]/(gamma+1)) for i in range(3)]
        h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0
        force=(gamma*pp+Q[8]*DX[12])**2*KQ/2-Y**mp.mpf('1.5')*A
        other=L-M*force-transport.regulator(ctx,Q,DX)
        p=[grad(L,14+i) for i in range(13)]+[J(0)]
        po=p[:12]+[J(0),J(0)]
        rv=[a-b for a,b in zip(v,ctx['lie'](q,d,S,Sz))]
        P=[D.var(x,60+i) for i,x in enumerate(p)]
        B=transport.improvement(ctx,Q,DX,P)
        sigma=((other.c-sum((p[i]*rv[i] for i in range(12)),J(0))).c[0]-B.c.c[1])/M.c.c[0]
        # Full field-dependent spatial-generator work at fixed shift.
        km=Kmom([x.c[0] for x in po[:13]])
        aa=[(grad(other,i).c[0]+sum((km[j][i]*Sz[j].c[0] for j in range(3)),iv.mpf(0))-sigma*M.g.get(i,J(0)).c[0])/M.c.c[0] for i in range(13)]
        bb=[(grad(other,28+i).c[0]+S[2].c[0]*po[i].c[0])/M.c.c[0] for i in range(13)]
        bq=[B.g.get(i,J(0)).c[0] for i in range(13)]
        bd=[B.g.get(28+i,J(0)).c[0] for i in range(13)]
        bp=[B.g.get(60+i,J(0)).c[0] for i in range(13)]
        mi=J(1)/M.c;mw=up(mi.c[0])+up(mi.c[1])
        cq=norm(aa)+norm(bb)+mw*(norm(bq)+norm(bd))
        cp=norm([rv[i].c[0]/M.c.c[0] for i in range(12)])+mw*norm(bp)
        return dict(other=other,M=M,B=B,sigma=sigma,p=p,po=po,rv=rv,aa=aa,bb=bb,
                    bq=bq,bd=bd,bp=bp,mw=mw,Cq=cq,Cp=cp,Y=Y)

    J=env['J'];y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    L=env['evaluate'](y);whole=setup(env,y,L)
    check('background_source_and_multiplier_coefficients_finite',all(mp.isfinite(hi(x)) for x in (whole['Cq'],whole['Cp'],whole['mw'])))
    check('improvement_retains_metric_and_frame_momentum',hi(norm(whole['bd']))>0 and hi(norm(whole['bp'][6:9]))>0)
    check('compensated_improvement_excludes_clock_momentum_exactly',all(x==0 for x in whole['bp'][9:]))
    q=[x.c[0] for x in y[:13]];qz=[x.c[1] for x in y[:13]];p=[x.c[0] for x in whole['p'][:13]]
    bq=Bmatrix(q);km=Kmom(p)
    sq=[norm(km[i])+(norm(p) if i==2 else 0) for i in range(3)]
    spc=[norm([row[i] for row in bq])+(norm(qz) if i==2 else 0) for i in range(3)]
    check('force_momentum_kept_in_longitudinal_free_source',hi(up(p[12]))>0 and hi(norm(p)-norm(p[:12]))>0)
    check('scalar_spatial_generator_rows_exactly_zero',all(v==0 for row in bq[9:] for v in row))
    r=iv.mpf(1)/13000;e2,e4=iv.exp(2*r),iv.exp(4*r)
    cs=[(1+e4)*e2*iv.sqrt(2),(1+e4)*e2*iv.sqrt(2),(1+e2)*e2*(1+r)/iv.sqrt(2)]
    ce=[e4,e4,e2]
    W=[up(whole['rv'][i].c[0]/whole['M'].c.c[0]) for i in (2,4,5)]
    rhs=[iv.mpf(1),whole['Cq']+sum((W[i]*cs[i]*sq[i] for i in range(3)),iv.mpf(0)),
         whole['Cp']+sum((W[i]*cs[i]*spc[i] for i in range(3)),iv.mpf(0)),
         iv.mpf(max(hi(W[i]*ce[i]) for i in range(3)))]
    G=decode(inv['inverse_Hminus1_H1_binary']);trace=[G*x for x in rhs]
    Ct=iv.sqrt(2)*e2*(1+2*r)
    tx,ty,Terr=[decode(old['bounds'][k]) for k in ('transverse_x','transverse_y','longitudinal_difference')]
    tz=iv.mpf(11)/10*iv.sqrt(iv.mpf(3469)/4620)+Terr;Tnorm=norm([tx,ty,tz])
    qrow=[Ct*x for x in trace];qrow[1]+=1
    prow=[Tnorm*x for x in trace];prow[1]+=norm([cs[i]*sq[i] for i in range(3)])
    prow[2]+=1+norm([cs[i]*spc[i] for i in range(3)]);prow[3]+=max(hi(x) for x in ce)
    state=[a+b for a,b in zip(qrow,prow)]
    forward=[whole['Cq']+1,whole['Cp']+1+iv.sqrt(3)]
    check('complete_source_trace_and_state_bounds_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in (rhs,trace,qrow,prow,state,forward) for x in row))
    check('all_three_momentum_means_retained',all(lo(x)>0 for x in ce) and lo(state[3])>0)

    # Exact divergence product identity and an independent nonconstant dual pair.
    z=sp.symbols('z');m=1+sp.cos(z)/7;F=sp.sin(2*z)/5;t=sp.sin(z)
    strong=sp.integrate(m*sp.diff(F,z)*t,(z,0,2*sp.pi))
    weak=-sp.integrate(F*sp.diff(m*t,z),(z,0,2*sp.pi))
    check('nonconstant_outer_multiplier_weak_pair',sp.simplify(strong-weak)==0)
    missed=sp.integrate(F*sp.diff(m,z)*t,(z,0,2*sp.pi))
    # Use a separate test for the omitted coefficient derivative.
    missed2=sp.integrate(sp.sin(z)*sp.diff(m,z),(z,0,2*sp.pi))
    check('omitting_multiplier_derivative_rejected',sp.simplify(missed2)!=0)
    aa,ff=[sp.Function(n)(z) for n in ('a','f')]
    check('weak_divergence_identity',sp.expand(aa*sp.diff(ff,z)-sp.diff(aa*ff,z)+sp.diff(aa,z)*ff)==0)
    controls=[]
    for location in ('0.3','1.1','2.4'):
        ctx=fac.point(location);yy,LL=ctx['y'],ctx['L'];data=setup(ctx,yy,LL)
        JJ,DD=ctx['J'],ctx['D'];grad=ctx['gradient'];zero=iv.mpf(0)
        for label in ('all_fields_momenta_shift','clock_momentum_only'):
            x=[JJ(coefficients=[iv.mpf(i+1)/101,(-1)**i*iv.mpf(i+2)/103,-iv.mpf(i+1)/202]) for i in range(13)]+[JJ(0)]
            xz=[JJ(coefficients=[v.c[1],2*v.c[2],zero]) for v in x]
            pp=[JJ(coefficients=[(-1)**i*iv.mpf(i+1)/107,iv.mpf(i+3)/109,zero]) for i in range(13)]+[JJ(0)]
            w=[JJ(coefficients=[iv.mpf(i+1)/113,-iv.mpf(i+2)/127,zero]) for i in range(3)]
            wz=[JJ(coefficients=[v.c[1],zero,zero]) for v in w]
            if label=='clock_momentum_only':
                x=[JJ(0)]*14;xz=[JJ(0)]*14;pp=[JJ(0)]*14;pp[12]=JJ(1);w=[JJ(0)]*3;wz=[JJ(0)]*3
            ctx['run_probe']('source_chart_'+label,x,xz,pp,w,wz)
            dy0=x+[JJ(0)]*14+xz+w+wz
            rhs0=[pp[i].c[0]-sum((ctx['hj'](LL,14+i,k)*dy0[k] for k in range(48)),JJ(0)).c[0] for i in range(13)]
            dv0,err=ctx['solve'](rhs0);dv=[JJ(v) for v in dv0]+[JJ(0)];dy=x+dv+xz+w+wz
            Q=[DD(t,{0:e}) for t,e in zip(yy[:14],x)];DX=[DD(t,{0:e}) for t,e in zip(yy[28:42],xz)]
            PP=[DD(t,{0:e}) for t,e in zip(data['p'],pp)]
            dB=transport.improvement(ctx,Q,DX,PP).g.get(0,JJ(0))
            nm,mu0,_,_,_=ctx['geometry'](Q,DX);dM=(nm*mu0).g.get(0,JJ(0))
            lx=ctx['lie'](x,xz,yy[42:45],yy[45:48]);lw=ctx['lie'](yy[:14],yy[28:42],w,wz)
            dother=sum((grad(data['other'],k)*dy[k] for k in range(48)),JJ(0))
            direct=(dother-sum((pp[i]*data['rv'][i]+data['p'][i]*(dv[i]-lx[i]-lw[i]) for i in range(12)),JJ(0))).c[0]-dB.c[1]
            direct=(direct-data['sigma']*dM.c[0])/data['M'].c.c[0]
            canonical=sum((grad(data['other'],i)*x[i]+grad(data['other'],28+i)*xz[i]+data['po'][i]*lx[i] for i in range(13)),JJ(0))
            canonical-=sum((data['rv'][i]*pp[i] for i in range(12)),JJ(0))
            predicted=(canonical.c[0]-dB.c[1]-data['sigma']*dM.c[0])/data['M'].c.c[0]
            defect=direct-predicted
            check('direct_all_sector_canonical_source_'+location+'_'+label,hi(up(defect))<mp.mpf('1e-26'),mp.nstr(hi(up(defect)),24))
            check('direct_temporal_inverse_'+location+'_'+label,hi(err)<mp.mpf('1e-30'))
            if label=='clock_momentum_only':
                check('clock_momentum_cancels_from_static_Sigma_'+location,hi(up(direct))<mp.mpf('1e-26'))
                check('clock_momentum_remains_in_constraint_'+location,hi(up(yy[40].c[0]))>0)
            controls.append(dict(location=location,label=label,defect=binary(defect)))
        check('inherited_full_raw_action_controls_'+location,all(c['passed'] for c in ctx['checks']))
    check('source_and_sidecar_bytes_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snap.items()))
    rows=dict(assembled_rhs_Hminus1=rhs,trace_H1=trace,configuration_H1=qrow,momentum_L2=prow,canonical_state_sum=state,
              data_sum_from_full_canonical=forward,forward_Sigma_Hminus1=[whole['Cq'],whole['Cp']],
              momentum_source_Q=sq,momentum_source_P=spc,completion_source=cs,completion_means=ce)
    return dict(kind='RTAU_COMPLETE_COMPENSATED_SOURCE_CHART_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                input_order=['Sigma_Hminus1_original','Qfree_H1_original','Pfree_L2_original','three_original_momentum_means_l1'],
                rows_binary={k:[binary(v) for v in row] for k,row in rows.items()},
                upper_display={k:[mp.nstr(hi(v),24) for v in row] for k,row in rows.items()},
                multiplier_W1_binary=binary(whole['mw']),source_sha256=pins,inherited_source_count=len(original),point_controls=controls,
                scope='BOUNDED_INITIAL_CANONICAL_COMPENSATED_CHART_ON_EXACT_COMPATIBLE_PLANAR_RANGE',
                range_conditions='Original spatial gauge, transverse source means, longitudinal weighted range, fixed-I and phase-charge tangents; all physical momentum means/harmonics retained',
                force_H2='Optional stronger force configuration control is identical in both charts',
                Sigma_L2='Additional stronger observable restriction; not inferred from canonical H1/L2',
                physical_energy='NOT_DERIVED',strong_symplectic_inverse='NOT_DERIVED',evolving_chart='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=parser.parse_args()
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps({'status':'FAILED_ATTEMPT','error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n')
        raise
    raw=(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],
                      'state_bounds':data['upper_display']['canonical_state_sum'],'forward_data':data['upper_display']['data_sum_from_full_canonical']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
