"""Registered R4C1-B1 finite-charge interacting FRW control on T3.

Full tensor variation cross-check + unfixed-lapse variation + independent
numerical constraint/charge/dust and finite-difference energy audits.
This is not calibrated cosmology, a stability proof or canonical closure.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

from test_01_r4c1_full_variation import (
    frame_blocks, connection_tensor, matadd, scale, mm, mv, dot, outer,
)

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_CONTRACT_2026-09-25.md":
        "3d5f164529ee2621aaa41bd08f8ba0a1ad2e4b866591f5aa4475f188fdf99a59",
    "Analysis/MasterTests/test_01_r4c1_full_variation.py":
        "aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0",
}
OUT = ROOT / "Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_summary.json"
CSV = OUT.with_name("test_01_r4c1_interacting_background_trajectory.csv")
PARAMS = dict(MP2=1., MU2=2/3, c1=1/5, c2=1/10, c3=-1/5, c4=1/20,
              K=3., A=2/7, b=5/11, zeta=1/13, beta=2/5, gr=3/7,
              m2=1., l4=1/3, l6=1/5, cutoff=2., mr2=2., lr=1/7, vacuum=0.)
NAMES = ('a','H','u','ud','v','vd','r','rd','psi','psid','rho_m','tau')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self):
        self.checks = []

    def exact(self,name,expr):
        value = s.simplify(expr)
        self.checks.append(dict(name=name,passed=bool(value==0),residual=str(value),expected="zero_exact"))

    def numeric(self,name,passed,value=None,criterion=None):
        self.checks.append(dict(name=name,passed=bool(passed),value=value,criterion=criterion))


def symbolic_background(audit):
    t = s.symbols('t',real=True)
    a = s.Function('a',positive=True)(t)
    u,v,r,psi,tau,eps = [s.Function(name,real=True)(t)
                       for name in ('u','v','r','psi','tau','epsilon')]
    N = s.Function('N',positive=True)(t)
    H,Hd = s.symbols('H Hdot',real=True)
    lam = s.symbols('lambda_U',real=True)
    coeff = {key:s.Symbol(key,real=True) for key in ('M','c1','c2','c3','c4','K','A','b','zz')}
    M,c1,c2,c3,K = [coeff[x] for x in ('M','c1','c2','c3','K')]
    MP2,beta,gr,m2,l4,l6,cutoff,mr2,lr,vac = s.symbols(
        'MP2 beta gr m2 lambda4 lambda6 Lambda mr2 lambda_r rho_Lambda',real=True)
    ct = c1+3*c2+c3
    MC = MP2+M*ct/2
    subH = {s.diff(a,t,2):a*(Hd+H**2),s.diff(a,t):a*H}
    g = s.diag(-1,a*a,a*a,a*a).tolist()
    gi = s.diag(-1,a**-2,a**-2,a**-2).tolist()
    U = [s.Integer(1),s.Integer(0),s.Integer(0),s.Integer(0)]

    def d(x,i):
        return s.diff(x,t) if i==0 else 0

    gamma = [[[sum(gi[c][e]*(d(g[e][b],aa)+d(g[e][aa],b)-d(g[aa][b],e))/2
                        for e in range(4)) for b in range(4)] for aa in range(4)] for c in range(4)]
    V = [[d(U[b],aa)+sum(gamma[b][aa][cc]*U[cc] for cc in range(4))
          for b in range(4)] for aa in range(4)]
    p = [s.diff(psi,t),0,0,0]
    J = [v*s.diff(u,t)-u*s.diff(v,t),0,0,0]
    # Substitute homogeneous fields into the already varied tensors. The
    # Y=0 first-variation limit is finite; no derivative of sqrt(Y) is taken.
    blocks = frame_blocks(g,gi,U,V,J,p,[0,0,0,0],s.Integer(0),lam,coeff)
    P = blocks['P']
    divP = [sum(d(P[aa][b],aa)+sum(gamma[aa][aa][cc]*P[cc][b]
                 -gamma[cc][aa][b]*P[aa][cc] for cc in range(4)) for aa in range(4)) for b in range(4)]
    EU = [s.simplify(blocks['F'][b]-divP[b]) for b in range(4)]
    lam_solution = s.simplify(EU[0]+lam)
    lam_expected = 3*M*c2*Hd-3*M*(c1+c3)*H**2
    audit.exact('full_frame_multiplier',lam_solution.subs(subH)-lam_expected)
    audit.exact('full_frame_time_equation',EU[0].subs(lam,lam_solution))
    for i in range(1,4):
        audit.exact(f'full_frame_spatial_equation_{i}',EU[i])
    CC = connection_tensor(U,P,gi)
    divCC = [[sum(d(CC[aa][m][n],aa)+sum(gamma[aa][aa][cc]*CC[cc][m][n]
        +gamma[m][aa][cc]*CC[aa][cc][n]+gamma[n][aa][cc]*CC[aa][m][cc]
        for cc in range(4)) for aa in range(4)) for n in range(4)] for m in range(4)]
    Tframe = matadd(scale(blocks['Ls'][0],gi),blocks['B2s'][0],scale(-1,divCC))
    rhoU = s.simplify(Tframe[0][0].subs(lam,lam_solution).subs(subH))
    pressureU = s.simplify((a*a*Tframe[1][1]).subs(lam,lam_solution).subs(subH))
    audit.exact('full_frame_energy_density',rhoU+3*M*ct*H**2/2)
    audit.exact('full_frame_pressure',pressureU-M*ct*(2*Hd+3*H**2)/2)
    audit.exact('frame_energy_balance',s.diff(-3*M*ct*s.Function('HH')(t)**2/2,t).subs(
        {s.diff(s.Function('HH')(t),t):Hd,s.Function('HH')(t):H})+3*H*(rhoU+pressureU))
    for i in range(1,4):
        audit.exact(f'frame_isotropic_pressure_{i}',
                    (a*a*Tframe[i][i]).subs(lam,lam_solution).subs(subH)-pressureU)
    for sector in (1,3):
        audit.exact(f'homogeneous_sector_{sector}_action',blocks['Ls'][sector])
        audit.exact(f'homogeneous_sector_{sector}_algebraic_stress',
                    sum(x*x for row in blocks['B2s'][sector] for x in row))
    Tforce = matadd(scale(blocks['Ls'][2],gi),blocks['B2s'][2])
    audit.exact('full_force_energy_density',Tforce[0][0]-K*s.diff(psi,t)**2/2)
    audit.exact('full_force_pressure',a*a*Tforce[1][1]-K*s.diff(psi,t)**2/2)
    theta = sum(gamma[mu][mu][0] for mu in range(4))
    Delta = sum(blocks['h'][i][j]*(d(p[j],i)-sum(gamma[k][i][j]*p[k] for k in range(4)))
                for i in range(4) for j in range(4))+theta*p[0]
    audit.exact('homogeneous_auxiliary_Delta_equation',Delta)

    radius = u*u+v*v
    pot_phi = m2*radius/2+l4*radius**2/8+l6*radius**3/(24*cutoff**2)
    pot_r = mr2*r*r/2+lr*r**4/4
    W = gr*radius*r*r/4
    pot = pot_phi+pot_r+W+vac
    kin2 = sum(s.diff(f,t)**2 for f in (u,v,r))+K*s.diff(psi,t)**2
    C = s.exp(beta*psi)
    Ldust = a**3*eps*(C**2*s.diff(tau,t)**2/N-N*C**4)/2
    L = -3*MC*a*s.diff(a,t)**2/N+a**3*kin2/(2*N)-N*a**3*pot+Ldust

    def gauge(expr):
        return s.simplify(expr.subs(N,1).doit().subs(s.diff(tau,t),C).subs(subH))

    def euler(f):
        return s.diff(L,f)-s.diff(s.diff(L,s.diff(f,t)),t)

    lapse = gauge(s.diff(L,N)/a**3)
    audit.exact('lapse_Friedmann_before_gauge',lapse-(3*MC*H**2-kin2/2-pot-eps*C**4))
    audit.exact('scale_factor_before_gauge',gauge(euler(a)/(3*a*a))-(MC*(2*Hd+3*H**2)+kin2/2-pot))
    for f in (u,v,r):
        audit.exact(f'scalar_EL_{str(f.func)}',gauge(euler(f)/a**3)+s.diff(f,t,2)+3*H*s.diff(f,t)+s.diff(pot,f))
    audit.exact('force_EL_with_matter',gauge(euler(psi)/a**3)+K*(s.diff(psi,t,2)+3*H*s.diff(psi,t))+beta*eps*C**4)
    audit.exact('dust_constraint',gauge(s.diff(L,eps)))
    # Substitute tau_dot before differentiating the explicit first-order
    # matter momentum, preserving all chain-rule terms of the constraint.
    dust_momentum = s.diff(Ldust,s.diff(tau,t)).subs(s.diff(tau,t),N*C)
    audit.exact('dust_current_equation',dust_momentum-a**3*eps*C**3)
    rdensity = s.Function('rho_m')(t)
    dust_deriv = s.diff(dust_momentum.subs(eps,rdensity/C**4),t)
    audit.exact('dust_energy_transfer',dust_deriv*C/a**3-(
        s.diff(rdensity,t)+3*s.diff(a,t)/a*rdensity-beta*rdensity*s.diff(psi,t)))
    # Full-metric 00 and reduced lapse formulations must agree.
    audit.exact('full_metric_reduced_constraint_agree',
        3*MP2*H**2-(kin2/2+pot+eps*C**4+rhoU)-(3*MC*H**2-kin2/2-pot-eps*C**4))
    dd_u = -3*H*s.diff(u,t)-s.diff(pot,u)
    dd_v = -3*H*s.diff(v,t)-s.diff(pot,v)
    Qcharge = a**3*(u*s.diff(v,t)-v*s.diff(u,t))
    audit.exact('charge_from_two_scalar_equations',s.diff(Qcharge,t).subs(
        {s.diff(u,t,2):dd_u,s.diff(v,t,2):dd_v,s.diff(a,t):a*H}))
    return {'lambda_U':str(lam_expected),'rho_U':str(rhoU),'p_U':str(pressureU),
            'M_cos_squared':str(MC),'all_equations':'classical homogeneous restriction of frozen R4C1',
            'Y_zero_scope':'homogeneous first variations only; no higher Taylor vertex'}


def effective_mass(p):
    return p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2


def physics(y,p):
    aa,H,u,ud,v,vd,r,rd,psi,psid,rm,tau = y
    radius = u*u+v*v
    VP = p['m2']*radius/2+p['l4']*radius**2/8+p['l6']*radius**3/(24*p['cutoff']**2)
    VR = p['mr2']*r*r/2+p['lr']*r**4/4
    W = p['gr']*radius*r*r/4
    kin = ud*ud+vd*vd+rd*rd+p['K']*psid*psid
    energy = kin/2+VP+VR+W+rm+p['vacuum']
    hdot = -(kin+rm)/(2*effective_mass(p))
    ct = p['c1']+3*p['c2']+p['c3']
    rhoU = -1.5*p['MU2']*ct*H*H
    pU = p['MU2']*ct*(hdot+1.5*H*H)
    rhoP = (ud*ud+vd*vd+p['K']*psid*psid)/2+VP+W+rhoU
    presP = (ud*ud+vd*vd+p['K']*psid*psid)/2-VP-W+pU
    rhoR = rd*rd/2+VR
    presR = rd*rd/2-VR
    constraint = 3*effective_mass(p)*H*H-energy
    return dict(radius=radius,VP=VP,VR=VR,W=W,kin=kin,energy=energy,hdot=hdot,
        rhoU=rhoU,pU=pU,rhoP=rhoP,pP=presP,rhoR=rhoR,pR=presR,
        Qmp=p['beta']*rm*psid,Qsyn=p['gr']*radius*r*rd/2,
        charge=aa**3*(u*vd-v*ud),dust_integral=aa**3*rm*np.exp(-p['beta']*psi),
        constraint=constraint,constraint_norm=np.abs(constraint)/(1+np.abs(3*effective_mass(p)*H*H)+np.abs(energy)),
        lambda_U=3*p['MU2']*p['c2']*hdot-3*p['MU2']*(p['c1']+p['c3'])*H*H)


def initial(p,bad_H=False):
    y = np.array([1.,0.,1.,0.,0.,1.,1.,.25,0.,.2,.2,0.])
    y[1] = np.sqrt(physics(y,p)['energy']/(3*effective_mass(p)))
    if bad_H:
        y[1] *= 1.001
    return y


def rhs(t,y,p,wrong_portal=False):
    aa,H,u,ud,v,vd,r,rd,psi,psid,rm,tau = y
    rad = u*u+v*v
    mass = p['m2']+p['l4']*rad/2+p['l6']*rad*rad/(4*p['cutoff']**2)+p['gr']*r*r/2
    rforce = p['mr2']*r+p['lr']*r**3+( -1 if wrong_portal else 1)*p['gr']*rad*r/2
    kin = ud*ud+vd*vd+rd*rd+p['K']*psid*psid
    return [aa*H,-(kin+rm)/(2*effective_mass(p)),ud,-3*H*ud-mass*u,
            vd,-3*H*vd-mass*v,rd,-3*H*rd-rforce,psid,
            -3*H*psid-p['beta']*rm/p['K'],(-3*H+p['beta']*psid)*rm,np.exp(p['beta']*psi)]


def integrate(p,method,rtol,atol,bad_H=False,wrong_portal=False):
    return solve_ivp(lambda t,y:rhs(t,y,p,wrong_portal), (0.,4.),initial(p,bad_H),
                     method=method,rtol=rtol,atol=atol,dense_output=True)


def summarize_solution(solution,p):
    grid = np.linspace(0.,4.,801)
    y = solution.sol(grid)
    data = physics(y,p)
    return {'success':bool(solution.success and solution.t[-1]==4.),'message':solution.message,
        'nfev':solution.nfev,'njev':solution.njev,
        'all_finite':bool(np.all(np.isfinite(y))),
        'min_a':float(y[0].min()),'min_H':float(y[1].min()),'min_rho_m':float(y[10].min()),
        'min_radius_squared':float(data['radius'].min()),
        'max_normalized_Friedmann':float(data['constraint_norm'].max()),
        'max_charge_drift':float(np.max(np.abs(data['charge']-data['charge'][0]))/max(1.,abs(data['charge'][0]))),
        'max_dust_integral_drift':float(np.max(np.abs(data['dust_integral']-data['dust_integral'][0]))/max(1.,abs(data['dust_integral'][0]))),
        'max_abs_Qmp':float(np.max(np.abs(data['Qmp']))),'max_abs_Qsyn':float(np.max(np.abs(data['Qsyn']))),
        'min_Qsyn':float(np.min(data['Qsyn'])),'max_Qsyn':float(np.max(data['Qsyn'])),
        'initial_state':dict(zip(NAMES,map(float,y[:,0]))),
        'final_state':dict(zip(NAMES,map(float,y[:,-1]))),
        'final_charge':float(data['charge'][-1]),'final_dust_integral':float(data['dust_integral'][-1])}


def difference5(values,dt):
    return (-values[4:]+8*values[3:-1]-8*values[1:-3]+values[:-4])/(12*dt)


def finite_difference_balances(solution,p,count):
    grid = np.linspace(0.,4.,count)
    y = solution.sol(grid)
    data = physics(y,p)
    sl = slice(2,-2)
    H = y[1,sl]
    hdot_fd = difference5(y[1],grid[1]-grid[0])
    # Full frame pressure uses an independent finite difference of H, not
    # Raychaudhuri supplied by the integration RHS.
    pUfd = p['MU2']*(p['c1']+3*p['c2']+p['c3'])*(hdot_fd+1.5*H*H)
    pP = data['pP'][sl]-data['pU'][sl]+pUfd
    sources = {'P':-data['Qmp'][sl]+data['Qsyn'][sl], 'R':-data['Qsyn'][sl], 'm':data['Qmp'][sl]}
    densities = {'P':data['rhoP'],'R':data['rhoR'],'m':y[10]}
    pressures = {'P':pP,'R':data['pR'][sl],'m':np.zeros(count-4)}
    measured = {}
    for name,density in densities.items():
        deriv = difference5(density,grid[1]-grid[0])
        expansion = 3*H*(density[sl]+pressures[name])
        residual = deriv+expansion-sources[name]
        norm = np.abs(residual)/(1+np.abs(deriv)+np.abs(expansion)+np.abs(sources[name]))
        measured[name] = float(np.max(norm))
    pressure_total = pP+data['pR'][sl]-p['vacuum']
    metric_lhs = p['MP2']*(2*hdot_fd+3*H*H)
    acceleration = np.abs(metric_lhs+pressure_total)/(1+np.abs(metric_lhs)+np.abs(pressure_total))
    return {'points':count,'dt':float(grid[1]-grid[0]),'balance_maxima':measured,
            'maximum':max(measured.values()),'full_spatial_metric_fd_residual':float(acceleration.max())}


def main():
    for path,expected in PINS.items():
        if sha(ROOT/path)!=expected:
            raise RuntimeError(f'FROZEN_INPUT_HASH_MISMATCH: {path}')
    audit = Audit()
    symbolic = symbolic_background(audit)
    print('Full tensor and unfixed-lapse background equations checked',flush=True)
    runs = {'coarse':integrate(PARAMS,'DOP853',1e-8,1e-10),
            'fine':integrate(PARAMS,'DOP853',1e-11,1e-13),
            'Radau':integrate(PARAMS,'Radau',1e-11,1e-13)}
    summaries = {name:summarize_solution(sol,PARAMS) for name,sol in runs.items()}
    for name,result in summaries.items():
        audit.numeric(f'{name}_completed',result['success'],result['message'],'t=4 successfully reached')
        audit.numeric(f'{name}_sampled_domain',result['all_finite'] and min(result[k] for k in ('min_a','min_H','min_rho_m'))>0
                      and result['min_radius_squared']>1e-6,
                      {k:result[k] for k in ('min_a','min_H','min_rho_m','min_radius_squared')},'finite; a,H,rho_m>0; s>1e-6')
    for key in ('max_normalized_Friedmann','max_charge_drift','max_dust_integral_drift'):
        audit.numeric(f'fine_{key}',summaries['fine'][key]<1e-8,summaries['fine'][key],'<1e-8')
    grid = np.linspace(0.,4.,801)
    yf = runs['fine'].sol(grid)
    differences = {name:float(np.max(np.abs(yf-runs[name].sol(grid))/(1+np.abs(yf)))) for name in ('coarse','Radau')}
    for name,limit in (('coarse',1e-6),('Radau',1e-8)):
        audit.numeric(f'{name}_fine_agreement',differences[name]<limit,differences[name],f'<{limit}')
    coarse,fine = [summaries[name]['max_normalized_Friedmann'] for name in ('coarse','fine')]
    audit.numeric('constraint_tolerance_improvement',fine<coarse or max(fine,coarse)<1e-12,
                  {'coarse':coarse,'fine':fine},'fine<coarse or both<1e-12')
    balances = [finite_difference_balances(runs['fine'],PARAMS,n) for n in (201,401,801)]
    audit.numeric('independent_fd_balances',balances[-1]['maximum']<1e-7,balances[-1]['maximum'],'<1e-7')
    improvement = balances[0]['maximum']/max(balances[-1]['maximum'],np.finfo(float).tiny)
    audit.numeric('independent_fd_refinement',improvement>=4 or max(balances[0]['maximum'],balances[-1]['maximum'])<1e-9,
                  improvement,'>=4 or endpoint residuals both<1e-9')
    for key in ('max_abs_Qmp','max_abs_Qsyn'):
        audit.numeric(f'nonzero_{key}',summaries['fine'][key]>1e-5,summaries['fine'][key],'>1e-5')
    zero_params = {**PARAMS,'beta':0.,'gr':0.}
    zero = summarize_solution(integrate(zero_params,'DOP853',1e-11,1e-13),zero_params)
    audit.numeric('zero_exchange_control',zero['success'] and zero['max_abs_Qmp']==zero['max_abs_Qsyn']==0,
                  {k:zero[k] for k in ('max_abs_Qmp','max_abs_Qsyn','max_normalized_Friedmann')},'completed; both currents exactly zero')
    wrong = {
        'wrong_initial_H':summarize_solution(integrate(PARAMS,'DOP853',1e-11,1e-13,bad_H=True),PARAMS),
        'wrong_reservoir_force':summarize_solution(integrate(PARAMS,'DOP853',1e-11,1e-13,wrong_portal=True),PARAMS),
    }
    for name,result in wrong.items():
        audit.numeric(f'{name}_rejected',result['success'] and result['max_normalized_Friedmann']>1e-5,
                      result['max_normalized_Friedmann'],'completed deliberate mutant has residual>1e-5')
    CSV.parent.mkdir(parents=True,exist_ok=True)
    data = physics(yf,PARAMS)
    extras = ('charge','dust_integral','rhoP','rhoR','rhoU','Qmp','Qsyn','constraint','lambda_U')
    with CSV.open('w',newline='',encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(('t',)+NAMES+extras)
        for i,t in enumerate(grid):
            writer.writerow([format(float(x),'.17g') for x in [t,*yf[:,i],*[data[k][i] for k in extras]]])
    CSV.with_suffix(CSV.suffix+'.sha256').write_text(f'{sha(CSV)}  {CSV.name}\n',encoding='ascii')
    passed = sum(check['passed'] for check in audit.checks)
    record = {'candidate':'R4C1-v1','control':'R4C1-B1','validation':'PASS' if passed==len(audit.checks) else 'FAIL',
        'passed':passed,'total':len(audit.checks),'checks':audit.checks,'symbolic':symbolic,'parameters':PARAMS,
        'M_cos_squared':effective_mass(PARAMS),'runs':summaries,'method_differences':differences,
        'finite_difference_balances':balances,'zero_exchange_control':zero,'negative_controls':wrong,
        'source_sha256':PINS,'script_sha256':sha(Path(__file__)),
        'trajectory':str(CSV.relative_to(ROOT)).replace('\\','/'),'trajectory_sha256':sha(CSV),
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__},
        'status':'CONDITIONAL_INTERACTING_BACKGROUND_CONTROL_PARENT_HOLD',
        'scope':'classical finite-time homogeneous zero-winding T3 control; not calibrated or stability-verified',
        'healthy_continuous_GR_limit_verified':False,'physical_Hessian_verified':False,
        'microscopic_matching_verified':False,'irreversible_syntropic_production_derived':False,
        'canonical_Test1_pass':False,'physics_pass':False,'gate_effect':'NONE','Rule9':'NOT_CLEARED',
        'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','K_Q':'NOT_DERIVED','V':'NOT_COMPUTED','Stage4A':'CLOSED'}
    OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    OUT.with_suffix(OUT.suffix+'.sha256').write_text(f'{sha(OUT)}  {OUT.name}\n',encoding='ascii')
    print(json.dumps({k:record[k] for k in ('validation','passed','total','status','physics_pass')}))
    print(json.dumps({'fine':{k:summaries['fine'][k] for k in ('max_normalized_Friedmann','max_charge_drift','max_dust_integral_drift','max_abs_Qmp','max_abs_Qsyn')},
                      'method_differences':differences,'finite_difference_balances':balances}))
    for check in audit.checks:
        if not check['passed']:
            print(json.dumps(check))
    return 0 if passed==len(audit.checks) else 1


if __name__=='__main__':
    raise SystemExit(main())
