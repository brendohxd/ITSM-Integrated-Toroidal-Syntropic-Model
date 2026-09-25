"""R4C1-S1: full nonzero-mode scalar constraints on the registered B1 branch.

Classical, spatially flat gauge (H!=0), no observational or full stability claim.
The unit frame is parametrized exactly; lapse, shift, dust multiplier and
regulator are retained until their quadratic constraint equations are solved.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
import sympy as s

from test_01_r4c1_interacting_background import PARAMS, NAMES, integrate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Analysis/MasterTests/outputs'
STEM = 'test_01_r4c1_scalar_constraints'
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':
        '81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
    'Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_CONTRACT_2026-09-25.md':
        '78da952e4a9faa7c4f3381b5cbe181416e74e142cdbb5904780801cc21ac94e6',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':
        '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/test_01_r4c1_full_variation.py':
        'aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_summary.json':
        'e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv':
        '0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa',
}

e = s.Symbol('perturbation_order')
a, C = s.symbols('a C', positive=True)
H, k = s.symbols('H k', real=True)
MP, MU, c1, c2, c3, c4, KQ, b, zeta, beta = s.symbols(
    'MP2 MU2 c1 c2 c3 c4 K_Q b zeta beta', real=True)
alpha, shift, w = s.symbols('alpha shift w', real=True)
at, ax, st, sx, wt, wx = s.symbols('alpha_t alpha_x shift_t shift_x w_t w_x', real=True)
u,v,r,ud,vd,rd,pd,rho = s.symbols('u v r u_dot v_dot r_dot psi_dot rho_m',real=True)
du,dv,dr,dp,dtau = s.symbols('du dv dr dpsi dtau',real=True)
dut,dvt,drt,dpt,dtaut = s.symbols('du_t dv_t dr_t dpsi_t dtau_t',real=True)
dux,dvx,drx,dpx,dtaux = s.symbols('du_x dv_x dr_x dpsi_x dtau_x',real=True)
de,z,zx = s.symbols('depsilon z z_x',real=True)
q = s.Matrix([du,dv,dr,dp,dtau,w])
qd = s.Matrix([dut,dvt,drt,dpt,dtaut,wt])
aux = s.Matrix([alpha,shift,de,z])
m2,l4,l6,Lambda,mr2,lr,gr = s.symbols('m2 lambda4 lambda6 Lambda mr2 lambda_r gr',real=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    path.with_name(path.name+'.sha256').write_text(sha(path)+'  '+path.name+'\n',encoding='ascii')


class Audit:
    def __init__(self):
        self.checks=[]

    def exact(self,name,value):
        if isinstance(value,s.MatrixBase):
            residual=[s.factor(x) for x in value]
            ok=all(x==0 for x in residual)
            evidence='zero_matrix' if ok else str(residual)
        else:
            residual=s.factor(value)
            ok=residual==0
            evidence=str(residual)
        self.checks.append(dict(name=name,passed=bool(ok),residual=evidence))

    def test(self,name,ok,value=None,criterion=None):
        self.checks.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))


def tr(expr):
    """Polynomial jet through degree two. No Taylor regularization of |q|^3."""
    poly=s.Poly(s.expand(expr),e)
    return s.Add(*(coeff*e**powers[0] for powers,coeff in poly.terms() if powers[0]<=2))


def order(expr,n):
    return s.expand(expr).coeff(e,n)


def derivative(expr,index):
    if index==0:
        return s.diff(expr,a)*a*H+sum(s.diff(expr,x)*dx for x,dx in
                ((alpha,at),(shift,st),(w,wt)))
    if index==1:
        return sum(s.diff(expr,x)*dx for x,dx in ((alpha,ax),(shift,sx),(w,wx)))
    return s.Integer(0)


def geometry(audit):
    g=s.diag(-1-2*e*alpha+e**2*(a*a*shift**2-alpha**2),a*a,a*a,a*a)
    g[0,1]=g[1,0]=e*a*a*shift
    gi=s.diag(-1+2*e*alpha-3*e**2*alpha**2,a**-2-e**2*shift**2,a**-2,a**-2)
    gi[0,1]=gi[1,0]=e*shift-2*e**2*alpha*shift
    U=s.Matrix([1-e*alpha+e**2*(alpha**2+w*w/2),
                e*(w/a-shift)+e**2*alpha*shift,0,0])
    audit.exact('inverse_metric_through_order_two',(g*gi-s.eye(4)).applyfunc(tr))
    audit.exact('unit_frame_through_order_two',tr((U.T*g*U)[0]+1))
    wrong=s.Matrix([1-e*alpha+e**2*alpha**2,e*(w/a-shift)+e**2*alpha*shift,0,0])
    audit.test('reject_missing_unit_boost_normalization',order((wrong.T*g*wrong)[0]+1,2)==w*w)
    gamma=[[[tr(sum(gi[c,j]*(derivative(g[j,bb],aa)+derivative(g[j,aa],bb)
                    -derivative(g[aa,bb],j)) for j in range(4))/2)
             for bb in range(4)] for aa in range(4)] for c in range(4)]
    D=s.Matrix(4,4,lambda aa,bb:tr(derivative(U[bb],aa)
                +sum(gamma[bb][aa][cc]*U[cc] for cc in range(4))))
    acc=[tr(sum(U[j]*D[j,i] for j in range(4))) for i in range(4)]
    I1=tr(sum(tr(gi[aa,bb]*g[cc,dd])*tr(D[aa,cc]*D[bb,dd])
              for aa in range(4) for bb in range(4) for cc in range(4) for dd in range(4)
              if gi[aa,bb]!=0 and g[cc,dd]!=0))
    I2=tr(s.trace(D)**2)
    I3=tr(sum(D[i,j]*D[j,i] for i in range(4) for j in range(4)))
    I4=tr(sum(g[i,j]*tr(acc[i]*acc[j]) for i in range(4) for j in range(4) if g[i,j]!=0))
    LU=tr(-MU*(c1*I1+c2*I2+c3*I3-c4*I4)*(1+e*alpha)/2)
    frame=order(LU,2)
    audit.exact('frame_background_action',order(LU,0)+3*MU*(c1+3*c2+c3)*H*H/2)
    audit.exact('no_lapse_velocity',s.diff(frame,at))
    audit.exact('no_shift_velocity',s.diff(frame,st))
    audit.exact('fixed_metric_flat_frame_control',frame.subs({H:0,alpha:0,ax:0,at:0,
                    shift:0,st:0,sx:0})-MU*((c1+c4)*wt**2-(c1+c2+c3)*wx**2/a**2)/2)
    h=(gi+U*U.T).applyfunc(tr)
    pdd,pxt,pxx=s.symbols('psi_ddot dpsi_xt dpsi_xx',real=True)
    grad=s.Matrix([pd+e*dpt,e*dpx,0,0])
    second=s.zeros(4); second[0,0]=pdd
    second[0,1]=second[1,0]=e*pxt; second[1,1]=e*pxx
    Q=tr((U.T*grad)[0])
    Delta=tr(sum(h[i,j]*tr(second[i,j]-sum(gamma[c][i][j]*grad[c] for c in range(4)))
             for i in range(4) for j in range(4))+s.trace(D)*Q)
    audit.exact('Delta_background',order(Delta,0))
    delta=order(Delta,1)
    audit.exact('Delta_covariant_first_variation',delta-pxx/a**2-pd*wx/a)
    audit.test('reject_omitted_frame_in_Delta',s.factor(delta-pxx/a**2)==pd*wx/a)
    force=order(tr(KQ*(1+e*alpha)*tr(Q*Q)/2),2)
    force_expected=KQ*(dpt*dpt-2*alpha*pd*dpt+alpha*alpha*pd*pd+pd*pd*w*w
                     -2*pd*shift*dpx+2*pd*w*dpx/a)/2
    audit.exact('force_direct_covariant_expansion',force-force_expected)
    J=s.Matrix([(v+e*dv)*(ud+e*dut)-(u+e*du)*(vd+e*dvt),
                 e*(v*dux-u*dvx)+e*e*(dv*dux-du*dvx),0,0])
    align=order(tr(-zeta*(1+e*alpha)*(J.T*h*J)[0]/2),2)
    audit.exact('alignment_direct_covariant_expansion',align+zeta*((v*dux-u*dvx)/a+(v*ud-u*vd)*w)**2/2)
    Y=tr((grad.T*h*grad)[0])
    audit.exact('projected_gradient_zero_background',order(Y,0))
    audit.exact('projected_gradient_zero_linear',order(Y,1))
    audit.exact('projected_gradient_quadratic_square',order(Y,2)-(dpx/a+pd*w)**2)
    # Y^(3/2)=|epsilon|^3 |dpsi_x/a+psi_dot*w|^3+o(epsilon^3).
    audit.test('cubic_force_has_no_quadratic_term',order(Y,0)==0 and order(Y,1)==0)
    reg=order(tr((1+e*alpha)*(b*e*e*z*z/2-b*(s.Matrix([0,e*zx,0,0]).T*h*grad)[0]
              -b*e*z*sum(acc[i]*grad[i] for i in range(4)))),2)
    audit.exact('regulator_direct_first_derivative_density',reg-(b*z*z/2-b*zx*(dpx/a**2+pd*w/a)))
    return frame,force,align,delta,pxx


def fourier(expr):
    co,si=s.symbols('cos_basis sin_basis')
    mapping={x:s.sqrt(2)*co*x for x in list(q[:5,0])+list(qd[:5,0])+[alpha,de,z]}
    mapping.update({x:s.sqrt(2)*si*x for x in [w,wt,shift]})
    mapping.update({gx:-s.sqrt(2)*k*si*x for gx,x in zip(
        [dux,dvx,drx,dpx,dtaux,ax],[du,dv,dr,dp,dtau,alpha])})
    mapping.update({wx:s.sqrt(2)*k*co*w,sx:s.sqrt(2)*k*co*shift})
    poly=s.Poly(s.expand(expr.subs(mapping,simultaneous=True)),co,si)
    moments={(2,0):s.Rational(1,2),(0,2):s.Rational(1,2),(1,1):0}
    if any(powers not in moments for powers,coeff in poly.terms() if coeff!=0):
        raise ValueError('Not a homogeneous quadratic Fourier density')
    return s.expand(sum(coeff*moments[powers] for powers,coeff in poly.terms() if coeff!=0))


def scalar_blocks(audit,frame,force,align):
    kin=0
    for dotf,dotq,gradq in [(ud,dut,dux),(vd,dvt,dvx),(rd,drt,drx)]:
        exact=tr((dotf+e*dotq-e*e*shift*gradq)**2*(1-e*alpha+e*e*alpha*alpha)/2
                 -(1+e*alpha)*e*e*gradq*gradq/(2*a*a))
        expected=dotq**2/2-alpha*dotf*dotq+alpha**2*dotf**2/2-dotf*shift*gradq-gradq**2/(2*a*a)
        audit.exact('canonical_density_'+str(dotf),order(exact,2)-expected)
        kin+=order(exact,2)
    radius=u*u+v*v
    pot=m2*radius/2+l4*radius**2/8+l6*radius**3/(24*Lambda**2)+mr2*r*r/2+lr*r**4/4+gr*radius*r*r/4
    fields=s.Matrix([u,v,r]); changes=s.Matrix([du,dv,dr])
    potential=-(changes.T*s.hessian(pot,fields)*changes)[0]/2-alpha*sum(s.diff(pot,f)*df for f,df in zip(fields,changes))
    direct=order(tr(-(1+e*alpha)*pot.subs({u:u+e*du,v:v+e*dv,r:r+e*dr},simultaneous=True)),2)
    audit.exact('potential_direct_expansion',potential-direct)
    C2=C*C*(1+2*e*beta*dp+2*e*e*beta**2*dp*dp)
    C4=C**4*(1+4*e*beta*dp+8*e*e*beta**2*dp*dp)
    dust=order(tr((rho/C**4+e*de)*(tr(C2*tr((C+e*dtaut-e*e*shift*dtaux)**2)
                 *(1-e*alpha+e*e*alpha**2))-(1+e*alpha)*C2*e*e*dtaux**2/a**2
                 -(1+e*alpha)*C4)/2),2)
    expected=rho*((dtaut/C)**2+4*beta*dp*dtaut/C-2*alpha*dtaut/C+alpha**2
            -6*beta**2*dp**2-6*alpha*beta*dp-2*shift*dtaux/C-dtaux**2/(a*a*C*C))/2
    expected+=de*C**3*(dtaut-C*alpha-beta*C*dp)
    audit.exact('dust_direct_expansion',dust-expected)
    audit.exact('dust_multiplier_constraint',s.diff(dust,de)-C**3*(dtaut-C*alpha-beta*C*dp))
    eh=order(tr(MP*(-3*H*H+2*H*e*sx)*(1-e*alpha+e*e*alpha*alpha)),2)
    audit.exact('ADM_EH_quadratic',eh+3*MP*H*H*alpha**2+2*MP*H*alpha*sx)
    modes=fourier(eh+frame+kin+potential+force+align+dust)
    delta_mode=-k*k*dp/a**2+pd*k*w/a
    regulator=b*z*z/2+b*z*delta_mode
    audit.exact('regulator_auxiliary_elimination',regulator.subs(z,-delta_mode)+b*delta_mode**2/2)
    audit.test('reject_wrong_regulator_sign',s.factor((regulator.subs(z,-delta_mode)-b*delta_mode**2/2))!=0)
    return modes+regulator,delta_mode


def reduction(audit,L):
    x=s.Matrix(list(qd)+list(q))
    allvars=s.Matrix(list(x)+list(aux))
    pre=s.hessian(L,allvars)
    B=pre[12:,12:]
    F=pre[:12,12:]
    P=pre[:12,:12]
    det=s.factor(B.det())
    print('Auxiliary determinant: '+str(det),flush=True)
    # Dust multiplier -> lapse, regulator -> z, shift -> shift; finally lapse
    # equation determines dust multiplier. No constraint is discarded.
    av=dtaut/C-beta*dp
    L1=s.expand(L.subs(alpha,av))
    zv=s.solve(s.diff(L1,z),z)[0]
    L2=s.expand(L1.subs(z,zv))
    sv=s.solve(s.diff(L2,shift),shift)[0]
    dev=s.solve(s.diff(L,alpha),de)[0].subs({alpha:av,z:zv,shift:sv},simultaneous=True)
    solutions=s.Matrix([av,s.factor(sv),s.factor(dev),s.factor(zv)])
    for i,var in enumerate(aux):
        audit.exact('auxiliary_equation_'+str(var),s.diff(L,var).subs(dict(zip(aux,solutions)),simultaneous=True))
    # Sparse rational inverse only on the displayed nonsingular domain.
    inv=B.inv()
    solution_schur=-inv*F.T*x
    audit.exact('constraint_solutions_vs_Schur',solutions-solution_schur)
    R=(P-F*inv*F.T).applyfunc(s.factor)
    direct=s.hessian(s.expand(L2.subs(shift,sv)),x)
    audit.exact('reduced_direct_vs_Schur',direct-R)
    for i in range(12):
        audit.exact('retained_variation_chain_rule_'+str(i),
            s.diff(L,x[i]).subs(dict(zip(aux,solutions)),simultaneous=True)-(R*x)[i])
    KK=R[:6,:6]; MM=R[:6,6:]; VV=-R[6:,6:]
    audit.exact('kinetic_symmetric',KK-KK.T)
    audit.exact('potential_symmetric',VV-VV.T)
    frozen_metric=s.hessian(L.subs({alpha:0,shift:0,de:0,z:0}),qd)
    audit.test('reject_metric_frozen_Hessian_as_reduced',any(s.factor(t)!=0 for t in KK-frozen_metric))
    # B determinant is an exact rank-domain condition, not a positivity test.
    audit.exact('auxiliary_determinant_factorization',det-C**8*MU*b*k*k*(c1+c2+c3))
    return pre,B,R,KK,MM,VV,solutions,det


def exact_frame_numeric(epsilon,jets,params):
    """Independent unexpanded metric/connection calculation, real finite jets."""
    aa,hh=jets['a'],jets['H']
    nn=1+epsilon*jets['alpha']; sh=epsilon*jets['shift']; ww=epsilon*jets['w']
    nt=epsilon*jets['alpha_t']; nx=epsilon*jets['alpha_x']
    sht=epsilon*jets['shift_t']; shx=epsilon*jets['shift_x']
    wwt=epsilon*jets['w_t']; wwx=epsilon*jets['w_x']
    gg=np.diag([-nn*nn+aa*aa*sh*sh,aa*aa,aa*aa,aa*aa])
    gg[0,1]=gg[1,0]=aa*aa*sh
    inv=np.linalg.inv(gg)
    dg=np.zeros((4,4,4))
    dg[0,0,0]=-2*nn*nt+2*aa*aa*hh*sh*sh+2*aa*aa*sh*sht
    dg[1,0,0]=-2*nn*nx+2*aa*aa*sh*shx
    dg[0,0,1]=dg[0,1,0]=aa*aa*(2*hh*sh+sht)
    dg[1,0,1]=dg[1,1,0]=aa*aa*shx
    for i in (1,2,3): dg[0,i,i]=2*aa*aa*hh
    gam=np.einsum('cj,jab->cab',inv,
         np.transpose(dg,(1,0,2))+np.transpose(dg,(1,2,0))-dg)/2
    boost=np.sqrt(1+ww*ww)
    U=np.array([boost/nn,ww/aa-sh*boost/nn,0.,0.])
    dU=np.zeros((4,4))
    for j,wn,nj,sj in ((0,wwt,nt,sht),(1,wwx,nx,shx)):
        dU[j,0]=ww*wn/(boost*nn)-boost*nj/(nn*nn)
        dU[j,1]=wn/aa-(ww*hh/aa if j==0 else 0)-sj*U[0]-sh*dU[j,0]
    D=dU+np.einsum('bac,c->ab',gam,U)
    acc=U@D
    invariants=[np.einsum('ab,cd,ac,bd',inv,gg,D,D),np.trace(D)**2,
                np.einsum('ab,ba',D,D),acc@gg@acc]
    return -params['MU2']*nn*(params['c1']*invariants[0]+params['c2']*invariants[1]
               +params['c3']*invariants[2]-params['c4']*invariants[3])/2


def finite_difference_check(audit,frame):
    jets=dict(a=1.3,H=.4,alpha=.17,shift=-.23,w=.31,alpha_t=.19,alpha_x=-.29,
              shift_t=-.11,shift_x=.37,w_t=-.41,w_x=.43)
    symbols=[a,H,alpha,shift,w,at,ax,st,sx,wt,wx,MU,c1,c2,c3,c4]
    values=[jets[str(x)] for x in symbols[:11]]+[PARAMS[x] for x in ('MU2','c1','c2','c3','c4')]
    expected=float(frame.subs(dict(zip(symbols,values))))
    zero=exact_frame_numeric(0.,jets,PARAMS)
    errors=[]; estimates=[]
    for step in (1e-3,5e-4,2.5e-4):
        estimate=(exact_frame_numeric(step,jets,PARAMS)+exact_frame_numeric(-step,jets,PARAMS)-2*zero)/(2*step*step)
        estimates.append(estimate); errors.append(abs(estimate-expected)/max(1.,abs(expected)))
    audit.test('independent_frame_second_difference',errors[-1]<1e-5 and all(
        errors[i+1]<errors[i] or max(errors[i+1],errors[i])<1e-8 for i in range(2)),
        dict(expected=expected,estimates=estimates,errors=errors),
        'finest <1e-5 and decreasing; sub-1e-8 numerical plateau accepted and recorded')


def matrix_strings(mat):
    return [[str(mat[i,j]) for j in range(mat.cols)] for i in range(mat.rows)]


def kinetic_certificate(audit,KK):
    """Post-sampling analytic strengthening; no change to registered criteria."""
    ct=c1+3*c2+c3; c123=c1+c2+c3; c14=c1+c4
    Mcos=MP+MU*ct/2; Mtensor=MP-MU*(c1+c3)
    D=s.factor(4*H*H*Mcos*Mtensor/(MU*c123))
    squares=sum((dq-fdot*dtaut/C)**2 for dq,fdot in ((dut,ud),(dvt,vd),(drt,rd)))
    squares+=KQ*(dpt-pd*dtaut/C)**2+MU*c14*(wt-k*dtaut/(a*C))**2+D*(dtaut/C)**2
    audit.exact('kinetic_completed_squares_identity',(qd.T*KK*qd)[0]-squares)
    # The canonical 4x4 block is diag(1,1,1,K_Q). Avoid an expensive generic
    # symbolic 6x6 determinant; its exact block determinant is only 2x2.
    reduced2=(KK[4:,4:]-KK[4:,:4]*s.diag(1,1,1,1/KQ)*KK[:4,4:]).applyfunc(s.factor)
    determinant=KQ*(reduced2[0,0]*reduced2[1,1]-reduced2[0,1]*reduced2[1,0])
    audit.exact('kinetic_determinant_identity',determinant-KQ*MU*c14*D/C**2)
    benchmark={MP:1,MU:s.Rational(2,3),c1:s.Rational(1,5),c2:s.Rational(1,10),
               c3:-s.Rational(1,5),c4:s.Rational(1,20),KQ:3}
    audit.exact('B1_final_square_coefficient',D.subs(benchmark)-66*H*H)
    weights=[s.Integer(1),s.Integer(1),s.Integer(1),KQ,MU*c14,D/H**2]
    values=[x.subs(benchmark) for x in weights]
    audit.test('B1_square_weights_positive',all(x>0 for x in values),list(map(str,values)))
    return dict(identity='qdot.T K qdot = '+str(squares),final_square_coefficient=str(D),
        determinant=str(s.factor(KQ*MU*c14*D/C**2)),
        B1_weights=list(map(str,values)),B1_final_weight='66*H^2',
        sufficient_domain='K_Q>0; MU2*(c1+c4)>0; M_cos2*(MP2-MU2*(c1+c3))/(MU2*(c1+c2+c3))>0; a,C finite positive; H!=0; k!=0; b!=0',
        conclusion='Exact positive scalar kinetic form at B1 coefficients in the regular chart; not full dynamical stability',
        timing='Analytic strengthening after first registered sample run; thresholds and action unchanged')


def numerical(audit,pre,B,R,KK):
    csvpath=ROOT/'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv'
    data=np.genfromtxt(csvpath,delimiter=',',names=True)
    times=data['t']; reference=np.vstack([data[name] for name in NAMES])
    solution=integrate(PARAMS,'Radau',1e-11,1e-13)
    if not solution.success:
        audit.test('independent_background_integration',False,solution.message)
        return {},[]
    alternate=solution.sol(times)
    diff=float(np.max(np.abs(alternate-reference)/(1+np.abs(reference))))
    audit.test('independent_background_integration',solution.success and diff<1e-7,diff,'<1e-7')
    args=[a,H,u,ud,v,vd,r,rd,pd,rho,C,k]
    params={MP:1,MU:s.Rational(2,3),c1:s.Rational(1,5),c2:s.Rational(1,10),
            c3:-s.Rational(1,5),c4:s.Rational(1,20),KQ:3,b:s.Rational(5,11),
            zeta:s.Rational(1,13),beta:s.Rational(2,5),m2:1,l4:s.Rational(1,3),
            l6:s.Rational(1,5),Lambda:2,mr2:2,lr:s.Rational(1,7),gr:s.Rational(3,7)}
    fpre=s.lambdify(args,pre.subs(params),'numpy',cse=True)
    fred=s.lambdify(args,R.subs(params),'numpy',cse=True)
    # The exact parameters are the frozen B1 values, not a fitted surrogate.
    for symbol,key in ((MP,'MP2'),(MU,'MU2'),(KQ,'K'),(Lambda,'cutoff'),(l4,'l4'),(l6,'l6'),(lr,'lr')):
        audit.test('parameter_identity_'+key,float(params[symbol])==PARAMS[key])
    max_sym=max_schur=max_eigen_diff=0.; rows=[]
    min_eig=float('inf'); max_cond=0.; inertia_counts={}; unresolved=0
    domain_ok=bool(np.all(reference[0]>0) and np.all(reference[1]>0) and np.all(reference[10]>0))
    for n in (1,2,4,8):
        for it,tt in enumerate(times):
            records=[]
            for tag,trajectory in (('pinned',reference),('Radau',alternate)):
                aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi,psi_d,rm,tau=trajectory[:,it]
                arguments=[aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi_d,rm,np.exp(PARAMS['beta']*psi),2*np.pi*n]
                pm=np.asarray(fpre(*arguments),dtype=float)
                rmtrx=np.asarray(fred(*arguments),dtype=float)
                auxm=pm[12:,12:]
                schur=pm[:12,:12]-pm[:12,12:]@np.linalg.solve(auxm,pm[12:,:12])
                kk=rmtrx[:6,:6]
                max_sym=max(max_sym,float(np.max(abs(kk-kk.T))/(1+np.max(abs(kk)))))
                max_schur=max(max_schur,float(np.max(abs(rmtrx-schur))/(1+np.max(abs(rmtrx)))))
                eig=np.linalg.eigvalsh((kk+kk.T)/2)
                threshold=1e-9*max(1.,float(np.max(abs(eig))))
                inertia=(int(np.sum(eig>threshold)),int(np.sum(eig<-threshold)),int(np.sum(abs(eig)<=threshold)))
                condition=float(np.linalg.cond(auxm))
                record=dict(trajectory=tag,t=float(tt),n=n,k_physical=float(2*np.pi*n/aa),
                            kinetic_eigenvalues=eig.tolist(),inertia_positive_negative_unresolved=list(inertia),
                            auxiliary_condition=condition)
                records.append(record)
                max_cond=max(max_cond,condition);min_eig=min(min_eig,float(eig[0]))
                key=','.join(map(str,inertia)); inertia_counts[key]=inertia_counts.get(key,0)+1
                unresolved+=inertia[2]
            eig0=np.array(records[0]['kinetic_eigenvalues'])
            eig1=np.array(records[1]['kinetic_eigenvalues'])
            eigen_difference=float(np.max(abs(eig0-eig1))/(1+np.max(abs(eig0))))
            max_eigen_diff=max(max_eigen_diff,eigen_difference)
            rows.extend(records)
    audit.test('sampled_chart_domain',domain_ok,dict(min_a=float(reference[0].min()),min_H=float(reference[1].min()),min_density=float(reference[10].min())))
    audit.test('numeric_kinetic_symmetry',max_sym<1e-9,max_sym,'relative <1e-9')
    audit.test('numeric_Schur_agreement',max_schur<1e-9,max_schur,'relative <1e-9')
    audit.test('independent_background_kinetic_agreement',max_eigen_diff<1e-7,max_eigen_diff,'relative <1e-7')
    return dict(sample_pairs=len(rows)//2,matrices_evaluated=len(rows),inertia_counts=inertia_counts,
        min_kinetic_eigenvalue=min_eig,max_auxiliary_condition=max_cond,unresolved_eigenvalue_count=unresolved,
        max_relative_eigenvalue_difference=max_eigen_diff,background_difference=diff),rows


def main():
    audit=Audit()
    observed={path:sha(ROOT/path) for path in PINS}
    for path,digest in PINS.items(): audit.test('source_pin_'+path,observed[path]==digest,observed[path])
    if not all(c['passed'] for c in audit.checks):
        write_json(OUT/(STEM+'_summary.json'),dict(validation='FAIL_SOURCE_PIN',checks=audit.checks))
        return 1
    print('Deriving covariant geometry and densities...',flush=True)
    frame,force,align,delta,pxx=geometry(audit)
    L,delta_mode=scalar_blocks(audit,frame,force,align)
    print('Solving retained constraints...',flush=True)
    pre,B,R,KK,MM,VV,solutions,det=reduction(audit,L)
    finite_difference_check(audit,frame)
    certificate=kinetic_certificate(audit,KK)
    print('Evaluating pinned and independently integrated backgrounds...',flush=True)
    samples,rows=numerical(audit,pre,B,R,KK)
    formula_path=OUT/(STEM+'_matrices.json')
    write_json(formula_path,dict(schema='r4c1-scalar-matrices-v1',q=list(map(str,q)),qdot=list(map(str,qd)),
        auxiliaries=list(map(str,aux)),preconstraint_order=list(map(str,list(qd)+list(q)+list(aux))),
        convention='spatial average L2/a^3 = qdot.K.qdot/2 + qdot.M.q - q.V.q/2',
        preconstraint_hessian=matrix_strings(pre),auxiliary_hessian=matrix_strings(B),
        auxiliary_determinant=str(det),auxiliary_solutions=list(map(str,solutions)),
        K=matrix_strings(KK),M=matrix_strings(MM),V=matrix_strings(VV),
        kinetic_certificate=certificate,
        frame_density_before_fourier=str(s.factor(frame)),quadratic_density=str(L),
        linear_Delta_psi=str(delta),Fourier_Delta_psi=str(delta_mode),
        chart_domain='a>0,C>0,H!=0,k!=0; MU2*b*(c1+c2+c3)!=0',
        units='Frozen B1 reference units; raw mixed-field eigenvalue magnitudes are chart-dependent'))
    sample_path=OUT/(STEM+'_samples.json');write_json(sample_path,rows)
    passed=sum(c['passed'] for c in audit.checks)
    valid=passed==len(audit.checks)
    negative=any(row['inertia_positive_negative_unresolved'][1]>0 for row in rows)
    unresolved=not rows or any(row['inertia_positive_negative_unresolved'][2]>0 for row in rows)
    outcome=('UNVALIDATED' if not valid else 'NEGATIVE_REDUCED_KINETIC_MODE_DETECTED' if negative else
             'KINETIC_INERTIA_UNRESOLVED' if unresolved else 'NO_NEGATIVE_KINETIC_MODE_ON_REGISTERED_SAMPLES')
    result=dict(schema='r4c1-scalar-constraints-v1',validation='PASS' if valid else 'FAIL',
        passed=passed,total=len(audit.checks),status=outcome,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',Rule9_cleared=False,research_execution='PROCEED_PROVISIONALLY',
        inherited_unreviewed_inputs=['R9-MT1-VARIATION','R9-MT1-B1'],
        scope='Classical finite-k scalar reduction on expanding B1; no gradient/mass/hyperbolicity/EFT certification',
        canonical=dict(MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED'),
        inputs=observed,executable_sha256=sha(Path(__file__)),
        artifacts={str(path.relative_to(ROOT)):sha(path) for path in (formula_path,sample_path)},
        versions=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__,scipy=scipy.__version__),
        samples=samples,checks=audit.checks,
        analytic_kinetic_certificate=certificate,
        remaining=['homogeneous k=0 constrained sector','gradient/mass and characteristic analysis',
            'time evolution and robustness beyond sampled domain','all-sector stability and EFT hierarchy',
            'deferred independent review; not a block on bounded research'])
    write_json(OUT/(STEM+'_summary.json'),result)
    Path(__file__).with_name(Path(__file__).name+'.sha256').write_text(sha(Path(__file__))+'  '+Path(__file__).name+'\n',encoding='ascii')
    print(json.dumps(dict(validation=result['validation'],passed=passed,total=len(audit.checks),status=outcome,samples=samples)))
    return 0 if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
