"""Compose the actual initial differentiated trace source in nine input norms."""

import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_TRACE_SOURCE_COMPOSITION_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_free_momentum_source_rate_v1_20261114/receipt.json'
PARENTS={
 'lift':'rtau_momentum_rate_lift_v2_20261104',
 'force':'rtau_strong_force_coordinate_v3_20261104',
 'weak':'rtau_weak_canonical_rate_v2_20261103',
 'gauge':'rtau_gauge_mean_trace_rate_v2_20261109',
 'density':'rtau_actual_corrected_density_v4_20261105',
 'drift':'rtau_free_coefficient_drift_v1_20261113',
 'weights':'rtau_source_weight_rates_v1_20261113',
 'rate':'rtau_rate_input_multipliers_v1_20261114',
 'trace_drift':'rtau_trace_momentum_drift_v2_20261109',
 'green':'rtau_trace_green_rate_v3_20261109'}


def exact_controls():
    t=sp.symbols('t')
    A,B,Q,T,f,q,p,b,M,w=[sp.Function(k)(t) for k in ('A','B','Q','T','f','q','p','b','M','w')]
    fullq=q+Q*f
    fullp=p+T*f+b
    L=A*Q+B*T
    source=sp.diff(M*w,t)-sp.diff(A,t)*fullq-sp.diff(B,t)*fullp
    source-=A*(sp.diff(q,t)+sp.diff(Q,t)*f)
    source-=B*(sp.diff(p,t)+sp.diff(T,t)*f+sp.diff(b,t))
    current=A*fullq+B*fullp-M*w
    return dict(exact_differentiated_reconstruction=sp.expand(sp.diff(current,t)-(L*sp.diff(f,t)-source))==0,
                moving_trace_shape_required=sp.diff(Q,t)*f!=0,
                moving_normalized_source_required=sp.diff(b,t)!=0,
                measure_rate_required=sp.diff(M,t)*w!=0)


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    ab=lambda x:max(abs(lo(x)),abs(hi(x)))
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    parent=read(PARENT)
    pins=dict(parent['source_pins'])
    paths={k:OUT+v+'/receipt.json' for k,v in PARENTS.items()}
    for rel in (CONTRACT,PARENT,*paths.values()):
        path=ROOT/rel
        h=Path(str(path)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        path=ROOT/rel
        assert digest(path)==h,rel
        for p in (path,Path(str(path)+'.sha256')):
            if p.exists():snap[p]=(digest(p),p.stat().st_mtime_ns)
    data={k:read(p) for k,p in paths.items()}
    assert all(c['passed'] for d in (parent,*data.values()) for c in d['checks'])
    lift,force,weak,gauge,density=[data[k] for k in ('lift','force','weak','gauge','density')]
    order=density['input_order']
    assert len(order)==9 and order[-1]=='harmonic_coordinate_velocity_adapted'
    base=[iv.mpf(0)]*9
    unit=lambda j:[iv.mpf(int(i==j)) for i in range(9)]
    vector=lambda xs:list(map(decode,xs))
    def nine(xs):
        row=vector(xs)
        assert len(row)==8
        return row+[iv.mpf(0)]
    Q=nine(lift['constants_binary']['full_configuration_H1'])
    P=nine(lift['constants_binary']['full_momentum_L2'])
    F=nine(force['constants_binary']['force_H2_inverse'])
    trace=nine(force['constants_binary']['trace_H1_after_force_inverse'])
    gbound={k:vector(v) for k,v in gauge['bounds_binary'].items()}
    shift=gbound['corrective_shift_H1']
    direct=gbound['direct_trace_rate_L2']
    def weakrow(key):
        c=vector(weak['coefficients_binary'][key])
        assert len(c)==4
        return [c[0]*p+c[1]*q+c[2]*f+c[3]*s for p,q,f,s in zip(P,Q,F,shift)]
    qt=weakrow('field_rate_L2')
    pt=weakrow('ordinary_momentum_rate_Hminus1')
    xi_t=weakrow('force_momentum_rate_Hminus2')
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J=ctx['J']
    y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    h,h_t=y[0],y[14]
    shape_H1=iv.sqrt(2)*(iv.mpf(ab(h.c[0]))+iv.mpf(ab(h.c[1])))
    shape_L2=iv.sqrt(2)*iv.mpf(ab(h.c[0]))
    shape_t_L2=iv.sqrt(2)*iv.mpf(ab(h_t.c[0]))
    qfree=[q+shape_H1*f for q,f in zip(Q,trace)]
    qfree_t=[v+shape_L2*d+shape_t_L2*f for v,d,f in zip(qt,direct,trace)]
    # Free canonical momenta are selected original slots, a norm-one projection.
    pfree=P
    pfree_t=pt
    eta=[unit(i) for i in (5,6,7)]
    eta_t=[gbound['eliminated_momentum_mean_'+i+'_rate'] for i in ('x','y','z')]
    weights={k:decode(v) for k,v in data['weights']['bounds_binary'].items()}
    drift={k:decode(v) for k,v in data['drift']['bounds_binary'].items()}
    rate={k:decode(v) for k,v in data['rate']['bounds_binary'].items()}
    Sd=iv.mpf(ab(y[44].c[0]))+iv.mpf(ab(y[44].c[1]))
    rw=vector(density['bounds_binary']['initial_original_coordinate_density_source_L2'])
    assert len(rw)==9
    w_t=[r+Sd*u for r,u in zip(rw,unit(0))]
    terms={
       'weighted_density_rate':[weights['measure_multiplier_Hminus1']*v for v in w_t],
       'measure_drift':[weights['measure_time_rate_sup']*u for u in unit(0)],
       'ordinary_configuration_coefficient_drift':[drift['ordinary_configuration_drift_H1_to_Hminus1']*q for q in Q],
       'ordinary_momentum_coefficient_drift':[drift['ordinary_momentum_drift_L2_to_Hminus1']*p for p in P],
       'clock_configuration_coefficient_drift':[weights['Malpha_time_sup']*f for f in F],
       'clock_momentum_coefficient_drift':[weights['Mc_time_sup']*p for p in P],
       'ordinary_free_configuration_rate':[rate['configuration_L2_to_Hminus2']*q for q in qfree_t],
       'clock_free_configuration_rate':[weights['Malpha_D_chi_rate_L2_to_Hminus1']*q for q in qfree_t],
       'moving_trace_shape':[rate['configuration_L2_to_Hminus2']*shape_t_L2*f for f in trace],
       'ordinary_free_momentum_rate':[rate['momentum_Hminus1_to_Hminus2']*p for p in pfree_t],
       'clock_free_momentum_rate':[weights['Mc_P_xi_rate_Hminus2_to_Hminus1']*p for p in xi_t],
    }
    td= data['trace_drift']['bounds_binary']
    columns=data['rate']['column_bounds_binary']['U']
    moving_T=iv.mpf(0)
    for name,slot in zip(('x','y','longitudinal'),(2,4,5)):
        moving_T+=decode(columns[slot][0])*decode(td['Tdot_'+name+'_L2_to_L2'])
    terms['moving_trace_momentum_lift']=[moving_T*f for f in trace]
    bdot_rows=[vector(r) for r in parent['normalized_momentum_rate_Hminus1_binary']]
    common=[qfree,pfree,qfree_t,pfree_t,xi_t]
    bdot_current=[iv.mpf(0)]*9
    for i,slot in enumerate((2,4,5)):
        coeff=decode(columns[slot][0])+decode(columns[slot][1])
        for k in range(9):
            bdot=sum((bdot_rows[i][j]*row[k] for j,row in enumerate(common)),iv.mpf(0))
            bdot+=bdot_rows[i][5]*eta[i][k]+bdot_rows[i][6]*eta_t[i][k]
            bdot_current[k]+=coeff*bdot
    terms['moving_free_momentum_source']=bdot_current
    total=[sum((r[k] for r in terms.values()),iv.mpf(0)) for k in range(9)]
    G=decode(data['green']['bounds_binary']['G_Hminus2_to_L2'])
    inverse=[G*t for t in total]
    # Independent exact-rational summation of the displayed component endpoints.
    rational=lambda x:sp.Rational(mp.mpf(x)._mpf_[1])*sp.Rational(2)**mp.mpf(x)._mpf_[2]*(-1 if mp.mpf(x)._mpf_[0] else 1)
    checks=exact_controls()
    checks.update(all_nine_inputs_retained=len(total)==len(order)==9,
                  independent_rational_sum_enclosed=all(rational(hi(total[k]))>=sum(rational(hi(row[k])) for row in terms.values()) for k in range(9)),
                  harmonic_velocity_reaches_actual_source=hi(total[-1])>0,
                  all_three_dynamical_means_reach_source=all(hi(terms['moving_free_momentum_source'][k])>0 for k in (5,6,7)),
                  all_source_and_rate_bounds_finite_positive=all(lo(x)>0 and mp.isfinite(hi(x)) for x in total+inverse+direct),
                  original_sources_and_sidecars_preserved=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_TRACE_SOURCE_COMPOSITION_V1',source_sha256=digest(Path(__file__)),source_pins=pins,pinned_sources=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],input_order=order,
                component_Hminus2_binary={k:[binary(x) for x in r] for k,r in terms.items()},
                source_Hminus2_binary=[binary(x) for x in total],trace_rate_from_inverse_L2_binary=[binary(x) for x in inverse],
                independent_direct_trace_rate_L2_binary=[binary(x) for x in direct],
                upper_display=dict(source=[mp.nstr(hi(x),24) for x in total],inverse_trace_rate=[mp.nstr(hi(x),24) for x in inverse],direct_trace_rate=[mp.nstr(hi(x),24) for x in direct]),
                scope='CONDITIONAL_EXACT_COMPATIBLE_INITIAL_JET_SOURCE_COMPOSITION',
                finite_centre_euler_solution='OPEN',full_coupled_energy='OPEN',review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path)
    group.add_argument('--replay',type=Path)
    args=parser.parse_args()
    payload=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if args.replay:
        assert args.replay.read_bytes()==payload
        print('Byte-identical read-only replay')
    else:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(payload)
        print('Initial differentiated trace-source composition controls complete')


if __name__=='__main__':main()
