"""Actual initial strong-density constraint lift; full generator remains open."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_CONSTRAINT_LIFT_V2_SPEC_2026-11-04.md'
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_ACTUAL_GENERATOR_REMAINDER_V1_CONTRACT_2026-11-04.md'
INPUTS='Theory/Gates/RES-001/RES001_RTAU_ACTUAL_GENERATOR_REMAINDER_V1_INPUTS_2026-11-04.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
BASE='Analysis/MasterTests/outputs/'
PARENTS={
 'weak':BASE+'rtau_weak_graph_v1_20261103/receipt.json',
 'inverse':BASE+'r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json',
 'normal1':BASE+'rtau_strong_density_normal_form_v1_20261103/receipt.json',
 'normal2':BASE+'rtau_strong_density_normal_form_v2_20261103/receipt.json',
}
FREE_P=[0,1,3,6,7,8,9,10,11,12]
ELIM=[2,4,5]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    contains=lambda x:lo(x)<=0<=hi(x)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    inputs=json.loads((ROOT/INPUTS).read_text());pins=dict(inputs['inherited_source_sha256'])
    for rel,want in inputs['direct_owner_sha256'].items():
        assert rel not in pins or pins[rel]==want,rel
        pins[rel]=want
    parents={k:json.loads((ROOT/v).read_text()) for k,v in PARENTS.items()}
    for rel in [SPEC,CONTRACT,INPUTS,FACTORY,'Analysis/MasterTests/test_rtau_strong_constraint_lift_v1.py','Theory/Gates/RES-001/RES001_RTAU_STRONG_CONSTRAINT_LIFT_V1_SPEC_2026-11-04.md','Analysis/MasterTests/outputs/rtau_strong_constraint_lift_v1_20261104/failure.json',*PARENTS.values(),Path(__file__).resolve().relative_to(ROOT).as_posix()]:pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel,want in pins.items():
        p=ROOT/rel;assert sha(p)==want,rel
        for item in (p,Path(str(p)+'.sha256')):
            if item.exists():snapshot[item]=(sha(item),item.stat().st_mtime_ns)
    check('292_inherited_pins_and_219_original_sources_preserved',inputs['inherited_source_count']==292 and inputs['original_source_count']==219)
    check('parent_controls_pass_only_in_their_registered_scopes',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in parents.values()))
    spec=importlib.util.spec_from_file_location('strong_constraint_first_variation_factory',ROOT/FACTORY)
    fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
    J,D=env['J'],env['D']
    # Same action evaluator, first differential only. No Hessian is generated.
    def first_mul(self,other):
        other=self.cast(other);zero=self.scalar(0)
        g={i:self.g.get(i,zero)*other.c+other.g.get(i,zero)*self.c for i in self.g.keys()|other.g.keys()}
        return type(self)(self.c*other.c,{i:v for i,v in g.items() if v!=0})
    def first_unary(self,value,first,second):
        return type(self)(value,{i:first*v for i,v in self.g.items() if v!=0})
    D.__mul__=first_mul;D.__rmul__=first_mul;D.unary=first_unary
    theta=J.variable(iv.mpf(2)/5);x=D.var(theta,0);y=D.var(1+theta**2,1)
    f=(x*y).exp()*(x*x+y**3)+(1+x*x)**mp.mpf('.5')+1/(2+y)
    sx,sy,t=sp.symbols('x y t',real=True)
    exact=sp.exp(sx*sy)*(sx*sx+sy**3)+sp.sqrt(1+sx*sx)+1/(2+sy)
    for index,symbol in enumerate((sx,sy)):
        expr=sp.diff(exact,symbol).subs({sx:t,sy:1+t*t})
        for order in (0,1):
            target=iv.mpf(str(sp.N(sp.diff(expr,t,order).subs(t,sp.Rational(2,5)),85)))
            check('first_differential_spatial_control_'+str(index)+'_'+str(order),hi(up(f.g[index].c[order]-target))<mp.mpf('1e-48'))
    check('first_only_engine_has_no_Hessian',not f.h)
    n=sp.symbols('n',integer=True,positive=True)
    current_nonzero=sp.Rational(553,400);current_mean=-sp.Rational(2263,8400);density0=sp.Rational(1,5)
    physical_nonzero=current_nonzero-density0;physical_mean=current_mean-density0
    check('physical_density_reference_keeps_true_negative_mean',physical_mean==-sp.Rational(3943,8400) and physical_nonzero==sp.Rational(473,400))
    check('reference_all_nonzero_modes_Hminus1_H1',sp.simplify(n*n+physical_nonzero-(1+n*n))==physical_nonzero-1 and physical_nonzero>1)
    check('fixed_current_density_is_not_fixed_physical_density',physical_mean!=current_mean and physical_nonzero!=current_nonzero)
    z=sp.symbols('z');A,a1,k,l,p,r,g=[sp.Function(v)(z) for v in ('A','a1','k','l','p','r','g')]
    ff=sp.Function('f')(z);C=A*l
    original=A*(sp.diff(g,z)+sp.diff(l*p,z))+a1*(g+l*p)+k*ff-sp.diff(C*p,z)-r
    desired=A*sp.diff(g,z)+a1*g+k*ff+(a1-sp.diff(A,z))*l*p-r
    check('variable_coefficient_gradient_remainder_identity',sp.expand(original-desired)==0)
    check('removed_frame_momentum_derivative_rejected',sp.diff(C*p,z)!=0)
    # Exact periodic Fourier antiderivative controls, including a nonzero mean.
    testp=2+sp.cos(z)+sp.sin(2*z);primitive=sp.sin(z)-sp.cos(2*z)/2
    check('primitive_retains_original_mean_partner',sp.expand(sp.diff(primitive,z)-(testp-2))==0)
    aa=2+sp.sin(z)/7;qq=sp.cos(z)+sp.sin(3*z)/5
    check('variable_coefficient_primitive_commutator_retained',sp.simplify(sp.diff(aa*primitive,z)-aa*(testp-2)-sp.diff(aa,z)*primitive)==0)
    b=iv.mpf(5)/11;beta=iv.mpf(2)/5;rad=iv.mpf(1)/13000
    c_bound=decode(parents['normal1']['bounds_binary']['coefficient'])
    alpha_bound=decode(parents['normal2']['bounds_binary']['alpha'])
    weak_error=decode(parents['weak']['constants_binary']['H1_Hminus1_operator_perturbation'])
    oldA={key:decode(v) for key,v in parents['inverse']['whole_root_trace_coefficients'].items()}
    old_bounds={key:decode(v) for key,v in parents['inverse']['bounds'].items()}
    h0=iv.sqrt(iv.mpf(3469)/4620);pi0=-iv.mpf(11)/10*h0
    Ti=[old_bounds['transverse_x'],old_bounds['transverse_y'],up(pi0)+old_bounds['longitudinal_difference']]
    source_factor=[(1+iv.exp(4*rad))*iv.exp(2*rad)*iv.sqrt(2)]*2+[(1+iv.exp(2*rad))*iv.exp(2*rad)*(1+rad)/iv.sqrt(2)]
    mean_factor=[iv.exp(4*rad),iv.exp(4*rad),iv.exp(2*rad)]
    reference_green=iv.mpf(8400)/3943
    records=[];bounds=[]
    # Equal coordinate cells cover the full circle; each carries the complete
    # original certified root uncertainty, not independent point solutions.
    for cell in range(16):
        zz=iv.mpf([lo(2*iv.pi*cell/16),hi(2*iv.pi*(cell+1)/16)])
        yy,_=env['state'](J.variable(zz),True,[0,0,0])
        L=env['evaluate'](yy);assert not L.h
        q,d,v,S,Sz=yy[:14],yy[28:42],yy[14:28],yy[42:45],yy[45:48]
        grad=env['gradient'];mom=[grad(L,14+i) for i in range(14)]
        Q=[D.var(x,i) for i,x in enumerate(q)];DX=[D.var(x,28+i) for i,x in enumerate(d)];PM=[D.var(x,100+i) for i,x in enumerate(mom)]
        N,mu,gamma,H,flux=env['geometry'](Q,DX)
        Fj=sum((N*gamma*H[i][2]*PM[6+i] for i in range(3)),D(0))-N*flux/2-N*mu*Q[13]*H[2][2]*DX[12]*b
        N,mu,gamma,H=N.c,mu.c,gamma.c,[[x.c for x in row] for row in H]
        material=[x-y for x,y in zip(v,env['lie'](q,d,S,Sz))]
        def partial(i):return Fj.g.get(i,J(0))
        q0=[];q1=[];q2=[]
        for i in range(14):
            basis=[J(int(i==j)) for j in range(14)]
            indexterm=sum((mom[j]*a for j,a in enumerate(env['lie'](basis,[J(0)]*14,[J(0)]*3,Sz))),J(0))
            q0.append(grad(L,i).c[0]+indexterm.c[0]-partial(i).c[1])
            q1.append(grad(L,28+i).c[0]+S[2].c[0]*mom[i].c[0]-partial(i).c[0]-partial(28+i).c[1])
            q2.append(-partial(28+i).c[0])
        aval=iv.sqrt(q[0].c[0]);A2=-N.c[0]*aval;A2z=-(N*q[0]**mp.mpf('.5')).c[1]
        C=N*gamma/q[0];lead=-gamma/(q[0]**mp.mpf('1.5'))
        I=L.c.c[0]-sum((mom[i].c[0]*material[i].c[0] for i in range(13)),iv.mpf(0))-Fj.c.c[1]
        M=(N*mu).c[0]
        # Exact conformal-initial identities from the inherited action graph.
        expected=[iv.mpf(0)]*14;expected[0]=expected[3]=-N.c[0]/(2*aval);expected[12]=b*N.c[0]*aval*q[13].c[0]
        check('action_principal_density_coefficients_cell_'+str(cell),all(contains(x-y) for x,y in zip(q2,expected)))
        check('action_canonical_momentum_improvement_cell_'+str(cell),all(contains(partial(100+i).c[0]-(C.c[0] if i==8 else 0)) for i in range(13)))
        # q_free has zero transverse trace. Its canonical metric moduli are
        # included, and the force coordinate is controlled separately in H2.
        logM=[iv.mpf(0)]*12
        for i in (0,3,5):logM[i]=1/(2*q[0].c[0])
        rq=norm([I*logM[i]-q0[i] for i in range(12)])+norm(q1[:12])
        rf=up(-beta*I-q0[12])+up(M)*alpha_bound/2+up(q1[12])/2+up(q2[12])
        rp=norm([material[i].c[0] for i in FREE_P])+up(M)*c_bound
        rbase=[up(M),rq,rp,rf]+[iv.mpf(0)]*3
        srows=[]
        for j in range(3):
            B=[iv.mpf(0)]*14
            # Columns of B at the conformal initial background.
            B[(2,4,5)[j]]=q[0].c[0]*(2 if j==2 else 1)
            B[6+j]=-q[8].c[0]
            # dB^T*p is a linear field coefficient, directly from the same Lie.
            K=[]
            for i in range(12):
                basis=[J(int(i==k)) for k in range(14)]
                basis_sz=[J(int(j==k)) for k in range(3)]
                response=env['lie'](basis,[J(0)]*14,[J(0)]*3,basis_sz)
                K.append(sum((mom[k].c[0]*response[k].c[0] for k in range(13)),iv.mpf(0)))
            sQ=norm(K);sP=norm([B[i] for i in FREE_P]);sF=iv.mpf(0)
            if j==2:
                sP+=norm([x.c[0] for x in d[:13]])
                sQ+=norm([x.c[0] for x in mom[:12]])
                sF+=up(mom[12].c[0])/2
            srows.append([iv.mpf(0),sQ,sP,sF]+[iv.mpf(0)]*3)
        sMaps=[]
        for j,row in enumerate(srows):
            result=[source_factor[j]*x for x in row];result[4+j]+=mean_factor[j];sMaps.append(result)
        rtotal=[rbase[k]+sum((up(material[i].c[0])*sMaps[j][k] for j,i in enumerate(ELIM)),iv.mpf(0)) for k in range(7)]
        rho_error=up(I-iv.mpf(1)/5);physical_error=weak_error+rho_error
        contraction=reference_green*physical_error
        check('physical_density_Green_Neumann_margin_cell_'+str(cell),hi(contraction)<1,mp.nstr(hi(contraction),24))
        assert hi(contraction)<1,'Physical-density inverse not proved; retain this failure'
        green=reference_green/(1-contraction)
        rhs=list(rtotal);rhs[2]+=up(C.c[0])
        fbound=[green*x for x in rhs]
        pbound=[[Ti[j]*fbound[k]+sMaps[j][k] for k in range(7)] for j in range(3)]
        Kbound=up(oldA['A0']-I)+sum((up(material[i].c[0])*Ti[j] for j,i in enumerate(ELIM)),iv.mpf(0))
        A1bound=up(oldA['A1'])
        # A2 is strictly negative: inverse norm uses its absolute LOWER bound.
        Ai=1/iv.mpf(min(abs(lo(A2)),abs(hi(A2))))
        assert hi(A2)<0
        gl2=list(fbound);gl2[2]+=up(lead.c[0])
        gz=[Ai*(rtotal[k]+A1bound*gl2[k]+Kbound*fbound[k]) for k in range(7)]
        gz[2]+=Ai*up((A2z-oldA['A1'])*lead.c[0])
        gbound=[a+b for a,b in zip(gl2,gz)]
        metric=[iv.exp(2*rad)*(1+2*rad)*g+iv.exp(2*rad)*(4*rad+4*rad*rad)*f for g,f in zip(gbound,fbound)]
        vals={'trace_H1':fbound,'eliminated_px_L2':pbound[0],'eliminated_py_L2':pbound[1],'eliminated_pz_L2':pbound[2],'trace_gradient_principal_remainder_H1':gbound,'metric_gradient_principal_remainder_H1':metric}
        check('all_strong_lift_and_smoothing_constants_finite_cell_'+str(cell),all(mp.isfinite(hi(x)) and lo(x)>=0 for row in vals.values() for x in row))
        records.append(dict(cell=cell,z=binary(zz),current_density=binary(I),physical_density_error=binary(rho_error),Neumann_contraction=binary(contraction),Green_bound=binary(green),leading_lift=binary(lead.c[0]),leading_lift_z=binary(lead.c[1])))
        bounds.append(vals)
    combined={key:[iv.mpf(max(hi(cell[key][j]) for cell in bounds)) for j in range(7)] for key in bounds[0]}
    check('original_sources_sidecars_and_timestamps_unchanged',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
    return dict(kind='RTAU_STRONG_CONSTRAINT_LIFT_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
      source_sha256=pins,original_source_count=219,inherited_source_count=292,
      input_order=['corrected_density_L2','free_ordinary_configuration_H1_including_moduli','free_canonical_momentum_L2_including_xi','force_configuration_H2','eliminated_momentum_mean_x','eliminated_momentum_mean_y','eliminated_momentum_mean_z'],
      constants_binary={k:[binary(x) for x in row] for k,row in combined.items()},upper_display={k:[mp.nstr(hi(x),26) for x in row] for k,row in combined.items()},cells=records,
      reference_physical_density_nonzero_mass=str(physical_nonzero),reference_physical_density_mean_mass=str(physical_mean),
      all_modes_and_means_retained=True,physical_density_measure_retained=True,compatible_range='Original transverse means, longitudinal weighted range and independent I/U1 charge tangents REQUIRED',
      scope='INITIAL_COMPATIBLE_PHYSICAL_DENSITY_CONSTRAINT_RECONSTRUCTION_AND_ONE_DERIVATIVE_PRINCIPAL_LIFT_REMAINDER_ONLY',
      full_actual_generator_remainder='NOT_BOUNDED',moving_Green_and_gauge_rates='NOT_ASSEMBLED',full_prepared_coupled_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
      review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')

def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    if args.output:assert not args.output.parent.exists(),'Fresh receipt directory required'
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            p=args.output.parent/'failure.json';raw=(json.dumps({'error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n').encode();p.write_bytes(raw);Path(str(p)+'.sha256').write_text(sha(p)+'\n')
        raise
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'kind':data['kind'],'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],'scope':data['scope'],'physics_pass':False}))
    if data['passed']!=data['total']:raise SystemExit(1)

if __name__=='__main__':main()
