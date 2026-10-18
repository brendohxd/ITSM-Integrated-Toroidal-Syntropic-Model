"""Unreduced regulator nodes: necessary compatibility, not physical admission."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_REGULATOR_NODE_V1_CONTRACT_2026-10-17.md'
RET = 'Analysis/MasterTests/outputs/r4c1_fixed_charge_retarded_comparison_attempt_03/'
PLANAR = 'Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CANON = 'Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py'
PINS = {
    CONTRACT: '2bea03116cb22de56e91c48de5038945261c0ffc3a3bd1618b66b1cf9995d053',
    RET+'trajectories.json': '3e36b9594ec4f186fff610a291011b6344b23ba98645922dfd7ad78d242ee4b3',
    RET+'formulas.json': '8aef9982815d5a56804c330cff60e99b9c4111e59cd167182f4ad9da3a388e7c',
    PLANAR: '852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
    CANON: '4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada',
    'Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py': '7321e53304864f0832a3e5a6ce3fce5dc2d156d3fa12d29df267b93910730b3f',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py': '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/test_01_r4c1_fixed_charge_retarded_comparison_v3.py': 'f86276d8ab9b6d226eb9a47f68f0ada085b3e7300ff789406487129f8ee65b30',
    'Analysis/MasterTests/test_01_r4c1_initial_charge_completion_v4.py': 'af22270b76b72d29a04bdfba366464bcc2482ec5f2e41f5ffe66061fee7f4020',
    'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md': '4834ea7517fd0393015e1d94fa1c130d84e2796b0ae1667712c2b5cf4653692c',
    'Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md': '3019196b071b146a1e41cd055073ae02da2afa10b1cdb5ae49e0a63cf84a6eb6',
    'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V4_REPORT_2026-10-16.md': '6b81ceff4cde8c9d933259ac34fbdccb4bcf4118f188c734de8a2577613a6c36',
    'Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_REPORT_2026-10-17.md': '8c4496eacdb0d2447445e4a1949b683e033f042a7332c659701e2273d2bf23ea',
    'GEMINI.md': '5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
    'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md': 'd6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
    'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md': '3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
    'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md': '14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
}
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
          'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX = {n: i for i, n in enumerate(FIELDS)}
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENC = lambda data: (json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
NUM = lambda value: mp.mpf(str(value))
CX = lambda value: mp.mpc(NUM(value[0]), NUM(value[1]))
SHOW = lambda value: mp.nstr(value, 45)
CLEAN = lambda value: s.factor(s.cancel(s.expand(value)))


class Checks:
    def __init__(self):
        self.rows = []
        self.names = set()

    def add(self, name, passed, value=None, criterion='exact'):
        if name in self.names:
            raise ValueError('duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name, passed=bool(passed), value=value, criterion=criterion))

    def zero(self, name, residual):
        values = list(residual) if isinstance(residual, (list, tuple, s.MatrixBase)) else [residual]
        bad = [str(v) for e in values if (v := CLEAN(e)) != 0]
        self.add(name, not bad, bad)

    def small(self, name, value, tolerance):
        self.add(name, mp.isfinite(value) and value <= mp.mpf(tolerance), SHOW(value), '<='+tolerance)


def sources():
    pins = dict(PINS)
    pins[SELF] = SHA((ROOT/SELF).read_bytes())
    metadata = {}
    for name, expected in pins.items():
        path = ROOT/name
        if SHA(path.read_bytes()) != expected:
            raise ValueError('source hash drift '+name)
        sidecar = Path(str(path)+'.sha256')
        if sidecar.read_text().split()[0].lower() != expected:
            raise ValueError('source sidecar mismatch '+name)
        for item in (path, sidecar):
            data = item.read_bytes()
            metadata[item.relative_to(ROOT).as_posix()] = dict(
                sha256=SHA(data), bytes=len(data), mtime_ns=item.stat().st_mtime_ns)
    return pins, metadata


def symbolic(ch):
    print('DERIVE_UNREDUCED_NODE_AND_TRANSPORT', flush=True)
    b, Z, theta, p, K, divV = s.symbols('b Z theta p K divV', real=True)
    n = s.Matrix(s.symbols('n0:4', real=True))
    acc = s.Matrix(s.symbols('acc0:4', real=True))
    grad = s.Matrix(s.symbols('q0:4', real=True))
    zg = s.Matrix(s.symbols('zg0:4', real=True))
    hp = s.Matrix(4, 4, lambda i,j: s.Symbol('hp'+str(i)+str(j), real=True))
    hess = s.Matrix(4, 4, lambda i,j: s.Symbol('H'+str(min(i,j))+str(max(i,j)), real=True))
    # Differentiate the original first-order density before using product identities.
    Lreg = b*Z**2/2 - b*(zg.T*hp*grad)[0] - b*Z*(acc.T*grad)[0]
    momentum = s.Matrix([s.diff(Lreg, x) for x in zg])
    dLZ = s.diff(Lreg, Z)
    div_hp = theta*n+acc
    div_momentum = -b*((div_hp.T*grad)[0]+sum(hp[i,j]*hess[i,j] for i in range(4) for j in range(4)))
    euler = CLEAN((dLZ-div_momentum)/b)
    candidate = Z+sum(hp[i,j]*hess[i,j] for i in range(4) for j in range(4))+theta*(n.T*grad)[0]
    ch.zero('Euler_Z_from_original_density_not_adjoint', euler-candidate)
    ch.zero('regulator_momentum_original', momentum+b*hp*grad)
    ch.add('reject_omitting_acceleration_changes_Euler_Z',
           CLEAN((dLZ+b*(acc.T*grad)[0]-div_momentum)/b-candidate) != 0)
    # Independent product-rule proof of div(hp)=theta*n+acc, tensorial with metric compatibility.
    B = s.Matrix(4,4,lambda i,j: s.Symbol('B'+str(i)+str(j), real=True))
    div_nn = s.Matrix([sum(B[a,a]*n[j]+n[a]*B[a,j] for a in range(4)) for j in range(4)])
    ch.zero('all4_covariant_projector_divergences',
            div_nn-s.trace(B)*n-B.T*n)
    # At V=0: Qij=Dij psi-Kij*p, theta=K+divV, while hp00=hp0i=0.
    lap = s.Symbol('lap_psi', real=True)
    aligned = CLEAN(Z+lap-K*p+(K+divV)*p)
    ch.zero('aligned_constraint_retains_spatial_divergence', aligned-(Z+lap+p*divV))
    ch.add('reject_setting_frame_divergence_zero_at_node', CLEAN(aligned-(Z+lap)) != 0)
    pp, vv, vq, KQ, A, zs = s.symbols('p V2 Vq KQ A Zhat', real=True)
    gam = s.sqrt(1+vv)
    # Everything outside the temporal/cusp/regulator force has no psi velocity.
    original_force = KQ*(gam*pp+vq)**2/2-A*(vv*pp**2+2*gam*vq*pp+s.Symbol('q2'))**s.Rational(3,2)-b*zs*(vv*pp+gam*vq)
    pm = s.diff(original_force, pp)
    ch.zero('aligned_original_force_temporal_momentum', pm.subs({vv:0,vq:0})-KQ*pp)
    ch.zero('aligned_regulator_primary_momentum', s.diff(original_force,zs).subs({vv:0,vq:0}))
    # Metric variation of the scalar Laplacian in normal coordinates at a point.
    N = s.Symbol('N', real=True)
    Ng = s.symbols('N0:3', real=True)
    kg = [[[s.Symbol('dK'+str(a)+str(min(i,j))+str(max(i,j)), real=True)
            for j in range(3)] for i in range(3)] for a in range(3)]
    km = s.Matrix(3,3,lambda i,j:s.Symbol('K'+str(min(i,j))+str(max(i,j)), real=True))
    H = s.Matrix(3,3,lambda i,j:s.Symbol('Q'+str(min(i,j))+str(max(i,j)), real=True))
    q = s.Matrix(s.symbols('q1:4', real=True))
    dh = 2*N*km
    dg = [s.Matrix(3,3,lambda i,j:2*Ng[a]*km[i,j]+2*N*kg[a][i][j]) for a in range(3)]
    delta_gamma = [[[sum(int(k==l)*(dg[i][l,j]+dg[j][l,i]-dg[l][i,j]) for l in range(3))/2
                    for j in range(3)] for i in range(3)] for k in range(3)]
    direct_delta_lap = -sum(dh[i,j]*H[i,j] for i in range(3) for j in range(3))-sum(delta_gamma[k][i][i]*q[k] for i in range(3) for k in range(3))
    drift = -2*N*sum(km[i,j]*H[i,j] for i in range(3) for j in range(3))-sum(
        (2*sum(Ng[i]*km[i,j]+N*kg[i][i][j] for i in range(3))
         -Ng[j]*s.trace(km)-N*sum(kg[j][i][i] for i in range(3)))*q[j] for j in range(3))
    ch.zero('all3D_metric_Laplacian_drift', direct_delta_lap-drift)
    ch.add('reject_freezing_metric_in_transport', CLEAN(drift) != 0)
    # A zero value does not kill div(D_t V). Persistent fixed node example.
    t,z = s.symbols('t z', real=True)
    Vz = (1+t)*z
    ch.zero('persistent_node_V_value', Vz.subs(z,0))
    ch.zero('persistent_node_DtV_value', s.diff(Vz,t).subs(z,0))
    ch.zero('persistent_node_divergence_drift_nonzero', s.diff(Vz,t,z).subs(z,0)-1)
    psi_hat = z**2+t*z+1
    lapse = 1+z+z**2
    ch.add('reject_dropping_nonuniform_lapse_from_Delta_Np',
           CLEAN(s.diff(lapse*psi_hat,z,2)-lapse*s.diff(psi_hat,z,2)) != 0)
    chi = z-t
    ch.zero('moving_node_tangent_transport', s.diff(chi,t)+s.diff(chi,z))
    ch.add('reject_fixed_node_transport_for_moving_surface', s.diff(chi,t) != 0)
    # Twice Hadamard integral identity, with F(0)=F'(0)=0, controls F/sigma^2.
    sig,u = s.symbols('sigma u', real=True)
    aa = s.symbols('a2:7', real=True)
    F = sum(aa[j-2]*sig**j for j in range(2,7))
    integral = s.integrate((1-u)*s.diff(F,sig,2).subs(sig,u*sig), (u,0,1))
    ch.zero('twice_Hadamard_remainder_identity', F-sig**2*integral)
    ch.zero('Hadamard_explicit_constant_one_half', s.integrate(1-u,(u,0,1))-s.Rational(1,2))
    ch.add('reject_nonzero_numerator_value',
           s.limit(1/sig**2,sig,0,dir='+') is s.oo)
    # The following is deliberately a rejection, not oo-oo arithmetic.
    ch.add('reject_only_primary_value_without_first_normal_jet',
           s.limit(sig/sig**2,sig,0,dir='+') is s.oo)
    ch.add('reject_C2_numerator_implies_C1_quotient',
           s.limit(s.diff(sig**2*s.Abs(sig)/sig**2,sig),sig,0,dir='+')
           != s.limit(s.diff(sig**2*s.Abs(sig)/sig**2,sig),sig,0,dir='-'))
    e,w,ph,A0,b0 = s.symbols('e w p A b', positive=True)
    pcusp = -3*A0*(e*w*sig)**3*ph**2  # positive sigma chart; opposite chart uses |sigma|.
    delta_z = CLEAN(pcusp/(b0*(e*w*sig)**2))
    ch.zero('cusp_momentum_cubic_induces_linear_Zhat_shift', delta_z+3*A0*e*w*sig*ph**2/b0)
    eta = s.Symbol('eta', positive=True)
    coeff = CLEAN((3*A0/b0*ph**2).subs({A0:2*eta**s.Rational(3,2)/7,b0:5*eta/11,ph:eta/5}))
    ch.zero('registered_cusp_shift_coefficient', coeff-s.Rational(66,875)*eta**s.Rational(5,2))
    d = s.Symbol('dim_psi')
    ch.zero('node_operator_dimensions', (d+1)+1-(d+2))
    ch.zero('cusp_momentum_dimensions', (1-3*d)+(d+1)+(d+1)-(3-d))
    ch.zero('cusp_Zhat_shift_dimensions', (3-d)-(-2*d)-(d+3))
    return dict(
        Euler_Z='E_Z/b = Z + hp^{ab} nabla_a nabla_b psi + theta*(n.grad psi)',
        general_ADM='Z+V2*Q00+2*gamma*Vi*Q0i+(h^ij+ViVj)*Qij+theta*(gamma*p+Vi*Di psi)',
        Hessian_projection=dict(Q00='D_t p/N - D^i lnN D_i psi',
            Q0i='D_i p-K_i^j D_j psi', Qij='D_iD_j psi-Kij*p'),
        aligned_constraint='chi=Z+Delta_h psi+p*D_i V^i=0; pZ=0; Ppsi=K_Q*p',
        transport='D_t chi=D_t Z+Delta_h(N*p)-2N*K^ij*D_iD_j psi-(2D_i(NK^ij)-D^j(NK))*D_j psi+(D_t p)*divV+p*div(D_t V) at V=0',
        moving_worldsheet='For T=D_t+r^i D_i tangent to Sigma, require T chi=D_t chi+r^i D_i chi=0; do not assert D_t Sigma=0',
        local_quotient_theorem={
            'assumptions':'simple signed profile coordinate sigma; V=sigma W; W2>=c>0 continuous; each numerator F is C2 in sigma with F(0)=F_normal(0)=0 and |F_normalnormal|<=M',
            'identity':'F/sigma^2=integral_0^1 (1-u) F_normalnormal(u*sigma) du',
            'psi_bound':'|psi_hat|<=Mpsi/(2*c)',
            'Z_bound':'|Zhat|<=MZ/(2*|b|*c)',
            'numerators':'Fpsi=PZ/b+gamma*V.Dpsi; FZ=Ppsi-ell_prime.y-f_prime; use complete action coefficients',
            'necessity':'A bounded quotient with C1 F requires both normal jets to vanish; with C2 F the quotient has a continuous extension',
            'exclusions':['not sufficient full constraint admission','no C1 quotient follows from C2 numerator','no uniform e,w,eta or b=0 limit','degenerate zeros not covered'],
        },
        cusp_momentum='Ppsi_cusp=-3A sqrt(Y)*(V2*p+gamma*V.Dpsi)',
        homogeneous_initial_cusp_shift='Omitting Ppsi_cusp at fixed other complete momenta changes Zhat by -(3A/b)*|e*w*cos(kz)|*|p|p, provided the regular inverse applies',
        registered_coefficient=str(coeff),
        archive_node_formula='chi2=Z0-2ReZ2+8k^2/a^2 RePi2+4k*p/a ImVz2',
        archive_transport_formula='chi2_dot=Zd0-2ReZd2+8k^2/a^2 RePid2-16Hk^2/a^2 RePi2+4k/a*(p ImVzd2+(pdd-Hp) ImVz2)',
        interpretation='Necessary local compatibility and sampled quadratic archive checks only; not full nonlinear physical reduction',
    )


def independent(ch):
    print('INDEPENDENT_ORIGINAL_DENSITY_AND_MOMENTA', flush=True)
    spec = importlib.util.spec_from_file_location('r4c1_node_original_canonical', ROOT/CANON)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    records = []
    for seed in (0,1):
        c = old.mp_geometry(seed)
        covH = mp.matrix([[mp.mpf((i+j+seed)%7-2)/37 for j in range(4)] for i in range(4)])
        n,gi,Dn = c['n'],c['gi'],c['DN']
        grad = c['coord_grad']['psi']
        hp = gi+n*n.T
        theta = sum(Dn[i,i] for i in range(4))
        acc = Dn.T*n
        divhp = mp.matrix([sum(Dn[a,a]*n[j]+n[a]*Dn[a,j] for a in range(4)) for j in range(4)])
        direct = c['Z']-(acc.T*grad)[0]+(divhp.T*grad)[0]+sum(hp[i,j]*covH[i,j] for i in range(4) for j in range(4))
        ell = mp.matrix([1/c['N']]+[-x/c['N'] for x in c['S']])
        Q00 = (ell.T*covH*ell)[0]
        Q0 = mp.matrix([sum(ell[a]*covH[a,i+1] for a in range(4)) for i in range(3)])
        spatialH = mp.matrix([[covH[i+1,j+1] for j in range(3)] for i in range(3)])
        v2 = (c['V'].T*c['h']*c['V'])[0]
        pred = c['Z']+v2*Q00+2*c['gamma']*(c['V'].T*Q0)[0]+sum(
            (c['hi'][i,j]+c['V'][i]*c['V'][j])*spatialH[i,j] for i in range(3) for j in range(3))+theta*(n.T*grad)[0]
        err = abs(direct-pred)/max(1,abs(direct),abs(pred))
        ch.small('coordinate_regulator_projection_'+str(seed),err,'1e-50')
        ch.add('reject_missing_acceleration_'+str(seed),abs((acc.T*grad)[0])>mp.mpf('1e-50'))
        ch.add('reject_missing_expansion_'+str(seed),abs(theta*(n.T*grad)[0])>mp.mpf('1e-50'))
        y = mp.matrix([c['K'][i,j] for i,j in old.HM]+list(c['X'])+[c['proper'][n] for n in ('u','v','r')])
        for family in old.FAMILIES:
            for eta in old.ETAS:
                par = old.parameters(family,eta,'mp')
                tag = str(seed)+'_'+family+'_'+str(eta)
                ps,zs = c['proper']['psi'],c['proper']['Z']
                ref = lambda v,pp=ps,zz=zs,pars=par:old.mp_body(c,pars,v,pp,zz)
                expected = -3*par['A']*mp.sqrt((grad.T*hp*grad)[0])*(
                    v2*ps+c['gamma']*(c['V'].T*c['spatial']['psi'])[0])
                noA = {**par,'A':mp.mpf(0)}
                pc = mp.diff(lambda pp:ref(y,pp),ps)-mp.diff(lambda pp:ref(y,pp,pars=noA),ps)
                errp = abs(pc-expected)/max(1,abs(pc),abs(expected))
                ch.small('full_density_cusp_momentum_'+tag,errp,'1e-50')
                ca = {**c,'V':mp.matrix([0,0,0]),'gamma':mp.mpf(1)}
                p_align = mp.diff(lambda pp:old.mp_body(ca,par,y,pp,zs),ps)
                z_align = mp.diff(lambda zz:old.mp_body(ca,par,y,ps,zz),zs)
                ch.small('aligned_full_momentum_'+tag,abs(p_align-par['K_Q']*ps),'1e-50')
                ch.small('aligned_full_Z_momentum_'+tag,abs(z_align),'1e-50')
                records.append(dict(tag=tag,regulator_projection_error=SHOW(err),cusp_momentum_error=SHOW(errp)))
        # Homogeneous initial force gradient; exact finite-amplitude cusp omission.
        par = old.parameters(old.FAMILIES[0],old.ETAS[0],'mp')
        for esign in (-1,1):
            ee = mp.mpf(esign)/1000
            for sigma in (mp.mpf(1)/2,-mp.mpf(1)/3):
                cc = dict(c)
                cc['V'] = mp.matrix([0,ee*sigma/mp.sqrt(c['h'][1,1]),0])
                cc['gamma'] = mp.sqrt(1+ee**2*sigma**2)
                cc['spatial'] = {**c['spatial'],'psi':mp.matrix([0,0,0])}
                ps = mp.mpf(1)/20
                body = lambda zz:mp.diff(lambda pp:old.mp_body(cc,par,y,pp,zz),ps)
                pc = -3*par['A']*abs(ee*sigma)**3*abs(ps)*ps
                shift = -3*par['A']/par['b']*abs(ee*sigma)*abs(ps)*ps
                delta = body(zs+shift)-(body(zs)-pc)
                ch.small('full_coupled_cusp_omission_shift_'+str(seed)+'_'+str(esign)+'_'+SHOW(sigma),abs(delta),'1e-50')
    return records


def archived(ch):
    print('ALL18_ARCHIVED_RUNS_ALL72_FULL_EVENTS', flush=True)
    runs = json.loads((ROOT/(RET+'trajectories.json')).read_bytes())['runs']
    expected = {(f,e,m) for f in ('archived_G3','new_B1_frame','new_hierarchical')
                for e in ('1/4','1/64','1/1024') for m in ('Radau','DOP853')}
    ch.add('all18_registered_run_identities',len(runs)==18 and {
        (r['family'],r['eta_exact'],r['method']) for r in runs} == expected)
    records = []
    global_max = {k:mp.mpf(0) for k in ('chi','transport','frame_node','shift_node')}
    alltimes = set()
    for ir,run in enumerate(runs):
        tag = str(ir)+'_'+run['family']+'_'+run['eta_exact']+'_'+run['method']
        eta = s.Rational(run['eta_exact'])
        eta = mp.mpf(int(eta.p))/int(eta.q)
        KQ,beta = 3*eta,2*eta**2/5
        k = NUM(run['k'])
        ch.add(tag+'_all4_saved_events_k40',len(run['events'])==4 and k==40)
        rows = []
        maxima = dict.fromkeys(global_max,mp.mpf(0))
        for ev in run['events']:
            a,H,R,ud,v,vd,r,rd,psi,p,rho,tau,w,wd = map(NUM,ev['background_and_first_wave'])
            pdd = -3*H*p-beta*rho/KQ
            q0 = list(map(CX,ev['full_response']['mean']['response']))
            q2 = list(map(CX,ev['full_response']['second']['response']))
            d0 = list(map(CX,ev['full_response']['mean']['velocity']))
            d2 = list(map(CX,ev['full_response']['second']['velocity']))
            if not all(len(x)==22 for x in (q0,q2,d0,d2)):
                raise ValueError('archive field order/length drift')
            node = lambda name:q0[IX[name]]-2*q2[IX[name]].real
            dz = lambda name:4*k*q2[IX[name]].imag
            ddz = lambda name:8*k*k*q2[IX[name]].real
            zd,lp,dvterm = d0[IX['Z']]-2*d2[IX['Z']].real,8*k*k/a**2*d2[IX['Pi']].real,4*k/a*p*d2[IX['Vz']].imag
            geom = -16*H*k*k/a**2*q2[IX['Pi']].real
            bg = 4*k/a*(pdd-H*p)*q2[IX['Vz']].imag
            terms = [node('Z'),ddz('Pi')/a**2,p*dz('Vz')/a]
            dtterms = [zd,lp,dvterm,geom,bg]
            chi = sum(terms)
            transport = sum(dtterms)
            residuals = dict(chi=abs(chi)/(1+sum(map(abs,terms))),
                transport=abs(transport)/(1+sum(map(abs,dtterms))),
                frame_node=max(abs(node(n)) for n in ('Vx','Vy','Vz')),
                shift_node=abs(node('Sz')))
            for name,val in residuals.items():
                maxima[name]=max(maxima[name],val)
                global_max[name]=max(global_max[name],val)
            alltimes.add(str(ev['time']))
            rows.append(dict(time=ev['time'],background_psi_acceleration=SHOW(pdd),
                chi=SHOW(chi),transport=SHOW(transport),
                chi_terms=list(map(SHOW,terms)),transport_terms=list(map(SHOW,dtterms)),
                frame_nodes={n:SHOW(node(n)) for n in ('Vx','Vy','Vz')},
                normal_shift_node=SHOW(node('Sz')),
                residuals={n:SHOW(val) for n,val in residuals.items()}))
        for name,val in maxima.items():
            ch.small(tag+'_'+name+'_all_saved_events',val,'1e-10')
        records.append(dict(tag=tag,family=run['family'],eta=run['eta_exact'],method=run['method'],
            maxima={n:SHOW(val) for n,val in maxima.items()},events=rows))
    ch.add('all72_saved_events_retained',sum(len(r['events']) for r in records)==72)
    return dict(runs=records,maximum_residuals={n:SHOW(v) for n,v in global_max.items()},
        sampled_times=sorted(alltimes,key=mp.mpf),scope='Quadratic nodal coefficients at four stored full-response times only; not all-order alignment or continuous-time admission')


def calculate():
    mp.mp.dps = 80
    pins,before = sources()
    ch = Checks()
    formula = symbolic(ch)
    independent_rows = independent(ch)
    archive = archived(ch)
    _,after = sources()
    ch.add('all_source_bytes_sidecars_and_metadata_unchanged',before==after)
    ok = all(r['passed'] for r in ch.rows)
    summary = dict(validation='PASS_NECESSARY_NODE_COMPATIBILITY_CONTROLS_ONLY' if ok else 'FAIL_NODE_IDENTITIES_OR_ARCHIVED_CONTROLS',
        passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,
        source_sha256=pins,source_metadata=before,physics_pass=False,gate_effect='NONE',
        Rule9_cleared=False,review_status='DEFERRED',stage2_complete=False,stage3_entered=False,
        finite_amplitude_initial_data_admitted=False,general_3D_constraint_closure_proved=False,
        physical_ghost_classification='NOT_ESTABLISHED',physical_family_GO=[],
        status='NECESSARY_STRATUM_COMPATIBILITY_ONLY_FULL_NONLINEAR_REDUCTION_OPEN',
        missing_required_physics=['full constraint algebra/reduction across rank-changing strata',
            'constraint-admissible finite-amplitude initial data and persistence',
            'physical Hessian/Cauchy/energy domain, nonlinear remainder and physical validity window',
            'healthy GR and identifying matter-residue/nonlinear-force matching inputs'])
    return {'summary.json':summary,'formulas.json':formula,'independent.json':independent_rows,'archive_nodes.json':archive}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--replay')
    args = parser.parse_args()
    if bool(args.output)==bool(args.replay):
        parser.error('choose exactly one fresh output or read-only replay')
    dest = (ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):
        raise ValueError('receipt directory outside scientific outputs')
    if args.output:
        dest.mkdir(parents=True,exist_ok=False)
    original = {p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    results = calculate()
    payloads = {name:ENC(obj) for name,obj in results.items()}
    for name,data in list(payloads.items()):
        payloads[name+'.sha256']=(SHA(data)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(original)!=set(payloads):
            raise ValueError('replay file-set mismatch')
        for name,data in payloads.items():
            path = dest/name
            if path.read_bytes()!=data or (SHA(path.read_bytes()),path.stat().st_size,path.stat().st_mtime_ns)!=original[name]:
                raise ValueError('replay changed bytes/metadata '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,data in payloads.items():
            with (dest/name).open('xb') as stream:
                stream.write(data)
    summary = results['summary.json']
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','physics_pass','stage2_complete','status')}),flush=True)
    return 0 if summary['passed']==summary['total'] else 1


if __name__=='__main__':
    raise SystemExit(main())
