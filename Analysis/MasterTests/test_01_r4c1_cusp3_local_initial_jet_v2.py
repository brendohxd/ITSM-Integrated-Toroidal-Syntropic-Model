"""Initial |e|^3 local constraints and sourced jets, not nonlinear evolution."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

import mpmath as mp
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
PARENT = BASE+'r4c1_initial_charge_completion_attempt_04/'
RET = BASE+'r4c1_fixed_charge_retarded_comparison_attempt_03/'
KERNEL = BASE+'r4c1_g3n5_attempt_02/kernel.json'
PLANAR = BASE+'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
FORCE = BASE+'r4c1_g3n4_force_attempt_01/formulas.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_LOCAL_INITIAL_JET_V1_CONTRACT_2026-10-16.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
SHA = lambda b:hashlib.sha256(b).hexdigest()
READ = lambda p:json.loads((ROOT/p).read_bytes())
ENCODE = lambda o:(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CLEAN = lambda e:s.factor(s.cancel(s.expand(e)))
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
          'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX = {n:i for i,n in enumerate(FIELDS)}
CONSTRAINTS = ('alpha','Sx','Sy','Sz','Em','Z','LambdaU')
AUX = ('Sx','Sy','Sz','Z')
HARMONICS = (0,1,2,4,8,16)
FROZEN = {
    'Analysis/MasterTests/test_01_r4c1_cusp3_local_initial_jet_v1.py':
        '5a3c28c15f1ef4efda084c497c2b64c62ffe3fa943301fa405031d97d93dc39c',
    BASE+'r4c1_cusp3_local_initial_jet_attempt_01/interrupted.json':
        'db000032b56fb49a358c5f574a1ca37a1a6da3a80499ce59be0c4aaf7b10d1f0',
    'Theory/Gates/RES-001/RES001_R4C1_CUSP3_LOCAL_INITIAL_JET_V2_SOLVER_ADDENDUM_2026-10-16.md':
        '8ccea7063cfe2c642d140164cc6a9cdfbc7f7955f85a929899534a9afa5a33fe',
    CONTRACT:'27ce42cb55f9f7316ec9b94bde2626989ec67192d2990e6c289b97b902a1d24f',
    PARENT+'summary.json':'8e16a7c05b5f9ce9054b6f37726f715abccb2b78ab45507a8e97e7552e5cfa01',
    'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V4_REPORT_2026-10-16.md':
        '6b81ceff4cde8c9d933259ac34fbdccb4bcf4118f188c734de8a2577613a6c36',
}


class Checks:
    def __init__(self):self.rows=[];self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names:raise ValueError('Duplicate check '+name)
        self.names.add(name);self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def exact(self,name,expr):
        vals=list(expr) if isinstance(expr,(list,tuple,s.MatrixBase)) else [expr]
        bad=[dict(index=i,residual=str(r)) for i,e in enumerate(vals) if (r:=CLEAN(e))!=0]
        self.add(name,not bad,bad,'zero_exact')
    def small(self,name,value,tol):self.add(name,abs(value)<=tol,float(abs(value)),'<= '+str(tol))


def inputs():
    parent=READ(PARENT+'summary.json')
    pins=dict(parent['source_sha256'])
    pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins.update(FROZEN);pins[SELF]=SHA((ROOT/SELF).read_bytes())
    absent=parent['inherited_sidecars_absent'];paths=[]
    for name,expected in pins.items():
        p=ROOT/name
        if SHA(p.read_bytes())!=expected:raise RuntimeError('Frozen source drift: '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=expected:raise RuntimeError('Frozen sidecar differs: '+name)
            paths.append(side)
        elif name not in absent:raise RuntimeError('Required sidecar absent: '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_gr_family_survey_v2 as generic
    import test_01_r4c1_three_family_response_entry_v2 as prior
    import test_01_r4c1_three_family_time_response_v2 as time
    return pins,absent,snapshot,generic,prior,time


class Compiler:
    def __init__(self,ch):
        print('Bind generic WWR and force sources before family substitution',flush=True)
        planar=READ(PLANAR);kernel=READ(KERNEL);force=READ(FORCE)
        texts=list(planar['Euler_sources_before_shift'].values())+[r['value'] for r in kernel['entries']]
        names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts)))
        names.update('A psi_ddot bk co si absolute_co w2 w3 q hm'.split())
        for n in list(names):
            if n=='B' or n.startswith('B_'):names.add('W'+n[1:])
        names.update(('W','W_t','W_tt','W_tz','B','B_t','B_tt','B_tz'))
        self.x=x={n:s.Symbol(n,real=True) for n in names}
        x['psi_dot']=s.Symbol('psi_dot',positive=True)
        a,H,pd,A,bk,co,si,t=(x[n] for n in ('a','H','psi_dot','A','bk','co','si','absolute_co'))
        f2=x['MU2']*(x['c1']+x['c4']);MT=x['MP2']-x['MU2']*(x['c1']+x['c3'])
        MC=x['MP2']+x['MU2']*(x['c1']+3*x['c2']+x['c3'])/2
        sigma=-x['MU2']*(x['c1']+x['c3'])/MT
        shift={x[n]:sigma*x['W'+n[1:]] for n in names if n=='B' or n.startswith('B_')}
        self.src={n:s.sympify(planar['Euler_sources_before_shift'][n],locals=x).xreplace(shift) for n in FIELDS}
        ch.add('complete_generic22_field_order',tuple(planar['field_order'])==FIELDS)
        ch.exact('bind_generic_first_shift',s.sympify(planar['first_transverse_shift'],locals=x)-sigma)
        fsy={n:s.Symbol(n,real=True) for n in ('A','e','p','W','H','pdd','Wt')}
        force0={n:s.sympify(force['Euler_sources'][n],locals={**fsy,'Abs':s.Abs}).subs(
            {fsy['A']:A,fsy['e']:1,fsy['p']:pd,fsy['W']:1,fsy['H']:H,fsy['pdd']:x['psi_ddot'],fsy['Wt']:0}) for n in FIELDS}
        self.direct=s.zeros(22,3)
        for n in FIELDS:
            if force['directional_degree'][n]==3:self.direct[IX[n],1]=force0[n]
        D=CLEAN(force0['Vy']/f2)
        ch.exact('lower_order_cusp_acceleration_from_action_source',D+3*A*pd**3/f2)
        first={x['W']:co,x['W_t']:0,x['W_tt']:x['w2']*co,
               x['W_z']:-bk*si,x['W_zz']:-bk**2*co,x['W_tz']:0}
        for n in names:
            if n.startswith('W_') and 'x' in n:first[x[n]]=0
        def at(expr):return s.expand(expr.xreplace(first))
        def decompose(expr,label):
            poly=s.Poly(s.cancel(expr/t),co,si)
            ch.add(label+'_supported_trig_monomials',all(i+j==2 for (i,j),v in poly.terms() if v!=0))
            c20=poly.coeff_monomial(co**2);c11=poly.coeff_monomial(co*si);c02=poly.coeff_monomial(si**2)
            ch.exact(label+'_complete_trig_identity',expr-t*(c20*co**2+c11*co*si+c02*si**2))
            return s.Matrix([[CLEAN(c02),CLEAN(c20-c02),CLEAN(-c11/(3*bk))]])
        self.full=self.direct.copy();self.mixed=s.zeros(22,3);self.drift=s.zeros(4,3)
        for n in FIELDS:
            expr=self.src[n]
            wave=[x[q] for q in names if q=='W' or q.startswith('W_')]
            ch.add('generic_'+n+'_quadratic_source_jet_degree',expr==0 or s.Poly(expr,*wave).total_degree()==2)
            mixed=at(s.diff(expr,x['W_tt']))*D*co*t
            self.mixed[IX[n],:]=decompose(mixed,n+'_mixed')
            self.full[IX[n],:]+=self.mixed[IX[n],:]
        def derivative_mix(n):
            expr=self.src[n]
            return at(s.diff(expr,x['W_t']))*D*co*t+at(s.diff(expr,x['W_tz']))*(-2*bk*D*t*si)
        for j,n in enumerate(AUX):self.drift[j,:]=decompose(derivative_mix(n),n+'_aux_dt')
        alpha_dt=decompose(derivative_mix('alpha'),'alpha_dt')+s.Matrix([[0,6*A*pd**2*x['psi_ddot'],0]])
        for n in CONSTRAINTS:
            ch.exact(n+'_source_no_lower_order_acceleration',s.diff(self.src[n],x['W_tt']))
        ch.exact('full_source_only_abs_cosine_cubed',list(self.full[:,0])+list(self.full[:,2]))
        ch.exact('initial_longitudinal_and_boost_sources_zero',list(self.full[IX['Sz'],:])+list(self.full[IX['Vz'],:]))
        temporal=-alpha_dt-3*H*self.full[IX['alpha'],:]
        for n in ('Mxx','Myy','Mzz'):temporal+=2*H*self.full[IX[n],:]
        for n,rate in (('du','u_dot'),('dv','v_dot'),('dr','r_dot'),('Pi','psi_dot')):
            temporal+=x[rate]*self.full[IX[n],:]
        longitudinal=a*self.drift[2,:]+s.Matrix([[0,0,2*self.full[IX['Mzz'],1]]])
        ch.exact('complete_temporal_source_Ward',temporal)
        ch.exact('complete_longitudinal_source_Ward',longitudinal)
        omitted_temporal=-s.Matrix([[0,6*A*pd**2*x['psi_ddot'],0]])-3*H*self.direct[IX['alpha'],:]
        for n in ('Mxx','Myy','Mzz'):omitted_temporal+=2*H*self.direct[IX[n],:]
        omitted_temporal+=pd*self.direct[IX['Pi'],:]
        omitted_longitudinal=s.Matrix([[0,0,2*self.direct[IX['Mzz'],1]]])
        ch.exact('omitted_mixed_temporal_Ward_witness',omitted_temporal-s.Matrix([[0,-3*H*A*pd**3,0]]))
        ch.exact('omitted_mixed_longitudinal_Ward_witness',omitted_longitudinal-s.Matrix([[0,0,-A*pd**3]]))
        ch.add('reject_omitted_mixed_acceleration',CLEAN(omitted_temporal[1])!=0 and CLEAN(omitted_longitudinal[2])!=0)
        ch.add('reject_omitted_auxiliary_source_drift',any(CLEAN(v)!=0 for v in self.drift))

        print('Prove seven initial constraint rows, including arbitrary nonzero harmonic',flush=True)
        LA,LB,LBT,LK=[s.zeros(22) for _ in range(4)]
        q=x['q'];weights=(s.Integer(1),0,0,0,s.I*q)
        ch.add('kernel_full110_jet_order',kernel['jet_order']==[n+suffix for suffix in ('','_t','_x','_y','_z') for n in FIELDS])
        for rec in kernel['entries']:
            bi,i=divmod(rec['row'],22);bj,j=divmod(rec['column'],22)
            val=s.sympify(rec['value'],locals=x)
            if bi!=1 and bj!=1:LA[i,j]+=s.conjugate(weights[bi])*val*weights[bj]
            elif bi!=1:LB[i,j]+=s.conjugate(weights[bi])*val
            elif bj!=1:LBT[i,j]+=val*weights[bj]
            else:LK[i,j]+=val
        h0=4/(3*s.pi);g0=2/s.pi;hm=x['hm']
        self.xdot=CLEAN(-A*pd**3*h0/(MC*H))
        qmean=s.zeros(22,1);vmean=s.zeros(22,1)
        for n in ('Mxx','Myy','Mzz'):vmean[IX[n]]=2*self.xdot/3
        qnonzero=s.zeros(22,1);qnonzero[IX['Em']]=2*A*pd**3*hm/x['C']**4
        source_mean=self.full*s.Matrix([g0,h0,0])
        source_nonzero=self.full*s.Matrix([0,hm,s.I*q*hm])
        for n in CONSTRAINTS:
            i=IX[n]
            ch.exact(n+'_no_primitive_velocity_or_acceleration',list(LBT.row(i))+list(LK.row(i)))
            ch.exact(n+'_mean_constraint',(LA.subs(q,0)*qmean+LB.subs(q,0)*vmean+source_mean)[i])
            ch.exact(n+'_arbitrary_nonzero_harmonic_constraint',(LA*qnonzero+source_nonzero)[i])
        m=s.Symbol('integer_harmonic',integer=True,nonnegative=True)
        quad_formula=(-1)**m/(4*s.pi)*(3/(1-2*m)+3/(1+2*m)-1/(3-2*m)-1/(3+2*m))
        fourier=12*(-1)**m/(s.pi*(4*m*m-1)*(4*m*m-9))
        ch.exact('all_integer_fourier_coefficients_from_product_to_sum',quad_formula-fourier)
        ch.exact('zero_mode_mean_not_dropped',fourier.subs(m,0)-h0)
        node=s.Symbol('node',real=True)
        for degree in range(3):
            ch.exact('cosine_node_C2_matching_derivative_'+str(degree),
                     s.limit(s.diff(node**3,node,degree),node,0,dir='+')-
                     s.limit(s.diff(-node**3,node,degree),node,0,dir='-'))
        ch.add('reject_ordinary_analytic_cubic_at_node',s.diff(node**3,node,3)!=s.diff(-node**3,node,3))
        expressions=list(self.full)+list(self.drift)+[self.xdot]
        self.order=sorted({str(q) for e in expressions for q in e.free_symbols})
        ch.add('initial_source_no_unbound_first_acceleration',not ({'w2','w3','co','si','absolute_co'} & set(self.order)))
        self.fun=s.lambdify([[x[n] for n in self.order]],expressions,'numpy',cse=True)
        self.export=dict(basis=['abs(cos(kz))','abs(cos(kz))^3','d_z abs(cos(kz))^3'],
            full_source={n:list(map(str,self.full[IX[n],:])) for n in FIELDS},
            mixed_source={n:list(map(str,self.mixed[IX[n],:])) for n in FIELDS},
            auxiliary_source_dt={n:list(map(str,self.drift[j,:])) for j,n in enumerate(AUX)},
            lower_cusp_acceleration_coefficient=str(D),mean_xdot_counter=str(self.xdot),
            even_fourier_coefficient=str(fourier),constraint_rows=list(CONSTRAINTS),
            omitted_mixed_temporal_Ward=list(map(str,omitted_temporal)),
            omitted_mixed_longitudinal_Ward=list(map(str,omitted_longitudinal)),
            pointwise_density='2*A*psi_dot^3/C^4*(abs(cos(kz))^3-4/(3*pi))',
            proof_scope='All source harmonics for seven initial constraints; finite probes only for full22 jets')


def spectral(ch):
    mp.mp.dps=80;values={}
    for m in HARMONICS:
        exact=12*(-1)**m/(mp.pi*(4*m*m-1)*(4*m*m-9))
        actual=mp.quad(lambda t:abs(mp.cos(t))**3*mp.cos(2*m*t),
                       [0,mp.pi/2,mp.pi,3*mp.pi/2,2*mp.pi])/(2*mp.pi)
        ch.small('independent_full_period_quadrature_m'+str(m),actual-exact,mp.mpf('1e-50'))
        values[m]=float(exact)
    return values


def direct_solve(data,out,state,source_dt,red,q):
    """Unreduced original22 equations plus differentiated auxiliary constraints."""
    EA,EB,ED,F,U=(data[n] for n in ('EA','EB','ED','F','U'))
    n=len(data['dyn']);m=len(data['aux']);y,yd=state[:n],state[n:]
    LA,LB,_,_=red.blocks(data['raw'],q)
    dLA,dLB,_,_=red.blocks(data['coefficient_dt'],q)
    Y=U.conj().T@LA@F;V=U.conj().T@LB@F
    Yd=U.conj().T@dLA@F;Vd=U.conj().T@dLB@F
    D=U.conj().T@LA@U;Dd=U.conj().T@dLA@U
    sd=np.array([source_dt[AUX.index(label)] for label in data['aux']],complex)
    em,lm=IX['Em'],IX['LambdaU']
    top=np.column_stack((ED@F,EA@U,EB@U,EA[:,em],EA[:,lm],EB[:,em]))
    bottom=np.hstack((V,Dd,D,np.zeros((m,3),complex)))
    matrix=np.vstack((top,bottom))
    rhs=np.r_[-(EA@F@y+EB@F@yd+data['S']),-(Yd@y+(Y+Vd)@yd+sd)]
    target=np.r_[out['ydd'],U.conj().T@out['q'],U.conj().T@out['qd'],out['q'][em],out['q'][lm],out['qd'][em]]
    scale=np.maximum(np.max(abs(matrix),axis=1),1e-30)
    mat=matrix/scale[:,None];r=rhs/scale
    cols=np.maximum(np.max(abs(mat),axis=0),1e-30);mat=mat/cols
    cv=lambda z:mp.mpc(repr(float(complex(z).real)),repr(float(complex(z).imag)))
    mm=mp.matrix([[cv(z) for z in row] for row in mat]);rr=mp.matrix([cv(z) for z in r])
    solution=mp.lu_solve(mm.H*mm,mm.H*rr)
    solution=np.array([complex(solution[j])/cols[j] for j in range(len(target))])
    residual=np.linalg.norm(matrix@solution-rhs,np.inf)/(np.linalg.norm(matrix,np.inf)*np.linalg.norm(solution,np.inf)+np.linalg.norm(rhs,np.inf)+1e-30)
    comparison=np.linalg.norm(solution-target,np.inf)/(np.linalg.norm(solution,np.inf)+np.linalg.norm(target,np.inf)+1e-30)
    u=U.conj().T@out['q'];ud=U.conj().T@out['qd']
    terms=(V@out['ydd'],Dd@u,D@ud,Yd@y,(Y+Vd)@yd,sd)
    drift=np.linalg.norm(sum(terms),np.inf)/(sum(np.linalg.norm(t,np.inf) for t in terms)+1e-30)
    return dict(independent_residual=float(residual),independent_comparison=float(comparison),auxiliary_drift_residual=float(drift))


def numeric(ch,compiler,generic,prior,time):
    fourier=spectral(ch);red=time.EvolvingReduction(prior,generic)
    for imaginary in (False,True):
        witness=mp.matrix([[0,mp.j if imaginary else 1],[1,0],[0,0]])
        expected=mp.matrix([2,1]);rhs=witness*expected
        actual=mp.lu_solve(witness.H*witness,witness.H*rhs)
        ch.small('independent_zero_diagonal_solver_control_'+str(imaginary),mp.norm(actual-expected),mp.mpf('1e-50'))
        ch.small('independent_original_row_solver_control_'+str(imaginary),mp.norm(witness*actual-rhs),mp.mpf('1e-50'))
    planar=READ(PLANAR);runs=READ(RET+'trajectories.json')['runs'];records=[]
    ch.add('all18_archived_events_retained',len(runs)==18)
    for ir,run in enumerate(runs):
        eta=float(s.Rational(run['eta_exact']));p=generic.bg.PARAMS.copy()
        for n,expr in planar['families'][run['family']]['parameter_map'].items():
            p['K' if n=='K_Q' else n]=float(s.sympify(expr).subs(s.Symbol('eta'),s.Rational(run['eta_exact'])))
        p['gr']=3*eta/7
        bg=np.array(run['events'][0]['background_and_first_wave'][:12],float)
        a,H,R,_,_,_,_,_,_,pd,rho,_=bg
        MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        MT=p['MP2']-p['MU2']*(p['c1']+p['c3']);f2=p['MU2']*(p['c1']+p['c4'])
        cL=p['MU2']*(p['c1']+p['c2']+p['c3']);C=np.exp(p['beta']*bg[8])
        domain=min(a,H,R,rho,MC,MT,f2,p['K'],p['b'],pd,eta)>0 and cL!=0
        ch.add(str(ir)+'_regular_initial_chart',domain)
        if not domain:raise ValueError('Refuse singular initial chart')
        raw=dict(zip(red.op.kernel.order,red.op.kernel.values(bg,p)))
        raw.update(p,psi_ddot=generic.bg.rhs(0,bg,p)[9],bk=40)
        vals=np.asarray(compiler.fun([raw[n] for n in compiler.order]),complex)
        full=vals[:66].reshape(22,3);sd=vals[66:78].reshape(4,3);xdot=vals[-1]
        print(json.dumps(dict(stage='INITIAL_CUSP3_JETS',family=run['family'],eta=run['eta_exact'],archived_method=run['method'])),flush=True)
        for m in HARMONICS:
            q=2*m*40;hm=fourier[m];gm=2*(-1)**m/(np.pi*(1-4*m*m))
            basis=np.array([gm,hm,1j*q*hm]);source=full@basis;source_dt=sd@basis
            data=red.at(bg,p,q,source,source_dt)
            state=np.zeros(2*len(data['dyn']),complex)
            if m==0:
                for n in ('Mxx','Myy','Mzz'):state[len(data['dyn'])+data['dyn'].index(n)]=2*xdot/3
            out=red.reconstruct(data,state,p)
            label=str(ir)+'_m'+str(m)
            ch.small(label+'_all22_equations',out['error'],1e-9)
            control=direct_solve(data,out,state,source_dt,red,q)
            ch.small(label+'_auxiliary_constraint_time_derivative',control['auxiliary_drift_residual'],1e-9)
            ch.small(label+'_unreduced80digit_residual',control['independent_residual'],1e-9)
            ch.small(label+'_unreduced80digit_comparison',control['independent_comparison'],1e-7)
            expected_density=0 if m==0 else 2*p['A']*pd**3*hm/C**4
            ch.small(label+'_pointwise_density_coefficient',abs(out['q'][IX['Em']]-expected_density)/(1+abs(expected_density)),1e-10)
            records.append(dict(family=run['family'],eta_exact=run['eta_exact'],archived_method=run['method'],
                harmonic=m,momentum=q,full22_residual=out['error'],**control,
                source=time.serial(source),auxiliary_source_dt=time.serial(source_dt),
                q=time.serial(out['q']),qd=time.serial(out['qd']),qdd=time.serial(out['qdd']),
                physical_acceleration=time.serial(out['ydd']),free_initial_state=time.serial(state),
                coordinate_order=list(data['dyn']),auxiliary_order=list(data['aux']),
                reduced_kinetic_condition=float(np.linalg.cond(data['K']))))
    return dict(initial_jets=records,probe_count=len(records),source_harmonics_not_truncated=True,
                full_infinite_mode_acceleration_bound=False,finite_time_evolution=False)


def calculate():
    pins,absent,snapshot,generic,prior,time=inputs();before=snapshot();ch=Checks()
    compiler=Compiler(ch)
    numerics=numeric(ch,compiler,generic,prior,time) if all(r['passed'] for r in ch.rows) else dict(skipped='Exact prerequisite failure')
    ch.add('all_source_sidecar_metadata_preserved',before==snapshot())
    scope=dict(claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,
        physics_pass=False,gate_effect='NONE',initial_cusp_order_only=True,
        complete_nonlinear_admission=False,physical_window_admitted=False,stage2_complete=False,
        stage3_entered=False,old_preparation_changed=False,retarded_warning_unchanged=True,
        Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',
        V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        remaining=['All-order initial constraints and controlled remainder','Full infinite-mode jet control and unprojected finite-time evolution',
            'Constrained finite-k energy/quartic characteristics and physical interaction window',
            'Tensor/local gravity/healthy GR and genuine matter plus nonlinear-force matching'])
    verification=dict(passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows)
    verification['validation']='PASS' if verification['passed']==verification['total'] else 'FAIL'
    bodies={'formulas.json':ENCODE(compiler.export),'initial_jets.json':ENCODE(numerics),
            'scope.json':ENCODE(scope),'verification.json':ENCODE(verification)}
    summary=dict(schema='r4c1-cusp3-local-initial-jet-v2',**verification,**scope,
        status=('CONDITIONAL_CUSP3_INITIAL_COMPATIBILITY_ONLY' if verification['validation']=='PASS' else 'LOCAL_INITIAL_JET_UNRESOLVED'),
        artifacts={n:SHA(b) for n,b in bodies.items()},source_sha256=dict(sorted(pins.items())),
        source_metadata_preserved=len(before),inherited_sidecars_absent=absent,
        runtime=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__,numpy=np.__version__),
        review_id='R9-MT1-CUSP3-LOCAL-INITIAL-JET-V1',
        review_dependencies=['INITIAL-CHARGE-COMPLETION-V4','THREE-FAMILY-FIXED-CHARGE-KINETIC-V3',
          'FIXED-CHARGE-RETARDED-V3','CHARGE-DOMAIN-V5','G3N4-FORCE-COVERAGE','GENERIC-WWR/EVOLVING-REDUCTION','all transitive debt'])
    bodies['summary.json']=ENCODE(summary)
    return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_cusp3_local_initial_jet_attempt_02')
    parser.add_argument('--replay');args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing scientific output')
    before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())] if args.replay else None
    bodies,summary=calculate()
    if args.replay:
        for name,b in bodies.items():
            if (dest/name).read_bytes()!=b or (dest/(name+'.sha256')).read_bytes()!=(SHA(b)+'  '+name+'\n').encode():
                raise RuntimeError('Read-only replay differs: '+name)
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay metadata changed')
        action='READ_ONLY_REPLAY_EXACT'
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,b in bodies.items():
            with (dest/name).open('xb') as f:f.write(b)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((SHA(b)+'  '+name+'\n').encode())
        action='NEW_RECEIPTS_WRITTEN'
    print(json.dumps(dict(action=action,**{n:summary[n] for n in ('validation','passed','total','status','physics_pass')})),flush=True)
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row),flush=True)
    return 0 if summary['validation']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
