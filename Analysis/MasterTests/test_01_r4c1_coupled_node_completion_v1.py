"""Certified restricted coupled mean/node system; not full initial admission."""
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
PARENT = 'Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_CONTRACT_2026-10-18.md'
PROOF = 'Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/proof.json'
CERTS = 'Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01/certificates.json'
NORMAL = 'Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02/normalization.json'
PREV = 'Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01/formulas.json'
PLANAR = 'Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA = lambda raw: hashlib.sha256(raw).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
READ = lambda name: json.loads((ROOT/name).read_bytes())
if SHA((ROOT/PARENT).read_bytes()) != 'd994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a':
    raise ValueError('parent source drift before import')
spec = importlib.util.spec_from_file_location('initial_surface_utilities', ROOT/PARENT)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
iv = mp.iv
PINS = dict(base.PINS)
PINS.update({
    PARENT: 'd994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a',
    CONTRACT: 'b63c9f3106d5b86c080a63c30b6fdb8ff188bdc08069c286b97d95b52966381a',
    PROOF: 'b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b',
    CERTS: '7c3465014fd85d7a98b905eed721c907f2f7764ccefadf856680ecf068d7127a',
    NORMAL: '447192694f9d65cd7791cfe93444dfe9a7d2566dfc99f453f590ae00825c668f',
    'Analysis/MasterTests/test_01_r4c1_node_acceleration_v2.py': '1e77ba8e8fc9d09d3e7e4a3a556405fa45dd5ce0dbf89580ff7ae2df106a9a7c',
    'Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md': '4e81b770bcf5ad3b999ce34af37326803c1f73aba852b21f1d0bafb75c2a5f96',
    'Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_PREFLIGHT_ADDENDUM_2026-10-18.md': '255484635f5a6f665ce65484cb665d640951e8b7400f482c4289a8ca99cfb0eb',
    'Theory/Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_REPORT_2026-10-18.md': '7fc348b923e55a8807fe597897fbbd1af20e1d5969260f7f31efa4c2dfc58d87',
    'Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02/summary.json': '825e3e39624d4533bcfb0e9db115cbc4695794f300d1f69b31463710f2c38804',
})


def sources():
    pins = dict(PINS)
    pins[SELF] = SHA((ROOT/SELF).read_bytes())
    metadata = {}
    for name, digest in pins.items():
        path = ROOT/name
        if SHA(path.read_bytes()) != digest:
            raise ValueError('source drift '+name)
        side = Path(str(path)+'.sha256')
        if side.read_text().split()[0].lower() != digest:
            raise ValueError('source sidecar drift '+name)
        for p in (path, side):
            metadata[p.relative_to(ROOT).as_posix()] = dict(
                sha256=SHA(p.read_bytes()), bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns)
    return pins, metadata


def symbolic(ch):
    print('BUILD_COUPLED_SYSTEM_AND_H_U_INVERSE_SENSITIVITIES', flush=True)
    names = ('MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 vz vz1 vz2 R q p '
             'Z Zd Z1 Z2 D rd pot k alpha xi zc zdc rs qs CC SS eeabs rh qh ru qu')
    u = {n: s.Symbol(n, real=True) for n in names.split()}
    u['p'] = s.Symbol('p', positive=True)
    parse = lambda text: s.sympify(text, locals=u)
    H, U, al, x = [u[n] for n in ('H', 'zc', 'alpha', 'xi')]
    proof, norm = READ(PROOF), READ(NORMAL)
    pn = [parse(text) for text in proof['polynomial_pieces']]
    scaled = sum(al**j*p for j, p in enumerate(pn))
    Q = lambda f: (2*x-1)*f-2*x*(1-x)*s.diff(f, x)
    ch.zero('exact_shift_affine_in_H_U', [s.diff(scaled, H, 2), s.diff(scaled, U, 2),
                                          s.diff(scaled, H, U)])
    residual = s.Poly(parse(proof['residual_numerator']), al, x)
    terms = residual.terms()
    ch.add('actual_residual_powers_retained', [list(p) for p, c in terms] == proof['residual_powers'])
    ch.add('normalized_residual_has_positive_powers', min(p[0] for p, c in terms) >= 4)
    coefficients = [c for p, c in terms]
    reval = base.Eval(coefficients+[s.diff(c, H) for c in coefficients]+[s.diff(c, U) for c in coefficients])
    peval = base.Eval([scaled, Q(scaled), s.diff(scaled, H), Q(s.diff(scaled, H)),
                       s.diff(scaled, U), Q(s.diff(scaled, U))])
    analytic = parse(norm['normalized_energy_analytic'])
    delta = analytic-2*u['A']*u['p']**3*u['eeabs']*u['CC']**3
    dH = s.diff(delta, H)+s.diff(delta, u['rs'])*u['rh']+s.diff(delta, u['qs'])*u['qh']
    dU = s.diff(delta, U)+s.diff(delta, u['rs'])*u['ru']+s.diff(delta, u['qs'])*u['qu']
    ee = s.Symbol('e_exact', real=True)
    C, S, k = u['CC'], u['SS'], u['k']
    sub = {u['vz']:ee*C, u['vz1']:-k*ee*S, u['vz2']:-k*k*ee*C,
           u['R']:ee**2*u['rs'], u['q']:ee**2*u['qs'], u['Z']:U*ee**2*C*C,
           u['Zd']:u['zdc']*ee**2*C*C, u['Z1']:-2*k*U*ee**2*C*S,
           u['Z2']:-2*k*k*U*ee**2*(2*C*C-1)}
    num, den = s.fraction(parse(READ(PREV)['lapse_flux_divergence']))
    np, dp = s.Poly(s.expand(num.subs(sub)), ee), s.Poly(s.expand(den.subs(sub)), ee)
    ch.zero('local_flux_removable_constant_and_linear', [np.coeff_monomial(1), np.coeff_monomial(ee)])
    ch.add('local_flux_even_amplitude_powers', all(p[0]%2 == 0 for p, c in np.terms()+dp.terms()))
    flux = sum(c*al**(p[0]//2-1) for p, c in np.terms() if p[0]>=2)/sum(c*al**(p[0]//2) for p, c in dp.terms())
    node_flux = parse(norm['normalized_node_flux'])
    ch.zero('normalized_local_flux_at_node', flux.subs({C:0,S:1,u['rs']:0})-node_flux)
    ch.zero('node_flux_has_no_H_U_sensitivity', [s.diff(node_flux,H),s.diff(node_flux,U)])
    E0, mean_delta, node_delta, node_J, rho0, qnode = s.symbols('E0 mean_delta node_delta node_J rho0 qnode')
    K, beta, bb, kk, pp, HB = [u[n] for n in ('K_Q','beta','b','k','p','H0')]
    rho_node = -E0-al*node_delta-al*node_J
    F = E0+al*mean_delta+rho0
    G = (K+2*bb*kk**2*al)*U-K*HB*pp-K*pp*al*qnode-beta*rho_node
    Uref = HB*pp+beta*rho0/K
    DD = 2*bb*U*kk**2-K*pp*qnode-beta*(mean_delta-node_delta-node_J)
    ch.zero('preconditioned_node_equation_identity', G-beta*F-K*(U-Uref)-al*DD)
    dims = {E0:4,mean_delta:4,node_delta:4,node_J:4,rho0:4,qnode:1,
            K:2,beta:0,bb:0,kk:1,pp:1,HB:1,U:2,al:0}
    ds = [sum(dims[a]*power for a,power in term.as_powers_dict().items() if a in dims)
          for expression in (F,G,DD) for term in s.Add.make_args(s.expand(expression))]
    ch.add('coupled_equations_mass_dimension_four',all(d==4 for d in ds),[int(d) for d in ds])
    formulas = dict(
        equations=['F=Ebase+alpha*<Edelta>+rho0', 'B=G-beta*F=K_Q*(U-U0)+alpha*D',
                   'D=2*b*U*k^2-K_Q*p*qnode_scaled-beta*(<Edelta>-Edelta_node-flux_node_scaled)'],
        jacobian=['F_H=-6*M*H+alpha*<d_H Edelta>', 'F_U=alpha*<d_U Edelta>',
                  'B_H=alpha*d_H D', 'B_U=K_Q+alpha*d_U D'],
        existence_uniqueness='Strict opposite F faces, opposite B faces, F_H<0, and B_U-B_H*F_U/F_H>0 on the fixed rectangle give a unique root of this restricted system by solving H(U), then the monotone B(H(U),U).',
        residual_powers=[list(p) for p,c in terms],
        normalized_error_proof='For residual=B*N(alpha,x)/(1+alpha*x), divide its actual terms alpha^n by alpha: |residual|/alpha<=sum |coef|*amax^(n-1)/2. Coercivity constants are independent of H,U. Apply the same bound to exact H/U inverse sensitivities; no old U0-only error constant is reused.',
        correction_proof='At the coupled root (U-U0)/alpha=-D/K_Q; hence |Z-Zold|<=sup|D/K_Q|*alpha^2. At alpha=0 this describes the continued limiting system, not physical identification of U on the aligned stratum.',
        normalized_local_flux=str(flux), energy_total_H_derivative=str(dH), energy_total_U_derivative=str(dU),
        exclusions=['regulator velocity higher completion','higher/rank-changing consistency and persistence',
                    'full initial admission or temporal nonlinear IVP','physical Hessian/domain/window and healthy GR','genuine identifying matching inputs'])
    return u, dict(poly=peval, residual=reval, terms=terms,
                   energy=base.Eval([delta,dH,dU,flux]), analytic=base.Eval([analytic]),
                   node_flux=base.Eval([node_flux])), formulas


def unpack(record):
    a, b = record['exact_binary_endpoints']
    return iv.mpf([mp.mpf(tuple(a)), mp.mpf(tuple(b))])


def make_case(item, fn):
    es = s.Symbol('eta')
    et = base.interval_s(s.Rational(item['eta']))
    raw = READ(PLANAR)['families'][item['family']]['parameter_map']
    v = {n:base.interval_s(s.sympify(t,locals={'eta':es}).subs(es,s.Rational(item['eta']))) for n,t in raw.items()}
    rc = iv.sqrt(et)
    v.update(Rc=rc,D=rc,rd=rc/4,p=et/5,k=iv.mpf(40),H0=unpack(item['H_background']),
             zdc=unpack(item['regulator_velocity_coefficient']),alpha=unpack(item['amplitude_squared_range']),
             eeabs=iv.mpf([0,base.hi(unpack(item['amplitude_absolute_max']))]),rho=iv.mpf(1)/5,
             pot=3*et/2+et**2*(iv.mpf(1)/24+iv.mpf(1)/28)+et**3*(iv.mpf(1)/480+iv.mpf(3)/28))
    U0 = unpack(item['regulator_coefficient'])
    Hlo, Hhi = 49*v['H0']/50, 51*v['H0']/50
    Ulo, Uhi = 49*U0/50, 51*U0/50
    Hall, Uall = iv.mpf([base.lo(Hlo),base.hi(Hhi)]), iv.mpf([base.lo(Ulo),base.hi(Uhi)])
    amax = base.upper(v['alpha'])
    s0 = v['c1']+v['c2']+v['c3']
    Tmax = abs(v['c4'])+abs(v['c1'])+abs(v['c2']+v['c3'])*amax
    kap = s0-amax*(2*abs(v['c2'])+Tmax)/4
    coerce, pmin = base.lower(v['MU2']*kap), base.lower(v['MU2']*s0)
    wmax = base.upper(v['MU2']*v['k']**2*amax*(2*abs(v['c2'])+Tmax))
    dtmin = v['MP2']-v['MU2']*abs(v['c1']+v['c3'])-2*v['MU2']*amax*(abs(v['c3'])+abs(v['c4'])*(1+amax))
    v.update(M=v['MP2']+v['MU2']*(v['c1']+3*v['c2']+v['c3'])/2)
    assert all(base.lo(x)>0 for x in (coerce,pmin,dtmin,v['M'],v['K_Q'],U0))
    vals = dict(v,H=Hall,zc=Uall)
    coeffs = fn['residual'].interval(vals)
    nt = len(fn['terms'])
    errors = []
    for group in range(3):
        r = iv.mpf(0)
        for (powers, expr), coeff in zip(fn['terms'],coeffs[group*nt:(group+1)*nt]):
            r += base.upper(abs(coeff))*amax**(powers[0]-1)/2
        r = base.upper(r)
        length = iv.mpf(2)/v['k']
        re = base.upper(length*r/(2*v['k']*coerce))
        qe = base.upper(length*(wmax*re+r)/pmin)
        errors.append((re,qe,r))
    return dict(family=item['family'],eta=item['eta'],values=v,U0=U0,Hlo=Hlo,Hhi=Hhi,
                Ulo=Ulo,Uhi=Uhi,Hall=Hall,Uall=Uall,errors=errors,
                constants=dict(coercivity=base.pack(coerce),Pmin=base.pack(pmin),Wmax=base.pack(wmax),
                               transverse_denominator_lower=base.pack(dtmin)))


def state(c, H, U, C, S, fn):
    v = dict(c['values'],H=H,zc=U,xi=C*C,CC=C,SS=S)
    pp = fn['poly'].interval(v)
    for j,(rn,qn) in enumerate((('rs','qs'),('rh','qh'),('ru','qu'))):
        v[rn] = C*S*pp[2*j]+base.box(c['errors'][j][0])
        v[qn] = v['k']*pp[2*j+1]+base.box(c['errors'][j][1])
        if base.lo(C)==base.hi(C)==0:
            v[rn] = iv.mpf(0)
    v['D'] = v['Rc']/(1-v['zeta']*v['Rc']**2*v['alpha']/2)
    return v


def enclose(c,H,U,n,fn):
    mean = [iv.mpf(0) for _ in range(3)]
    density_floor = None
    v0 = c['values']
    Dphase = v0['Rc']/(1-v0['zeta']*v0['Rc']**2*v0['alpha']/2)
    ebase = -3*v0['M']*H**2+(v0['K_Q']*v0['p']**2+Dphase**2+v0['rd']**2)/2+v0['pot']
    for j in range(n):
        theta = iv.mpf([base.lo(iv.pi*j/(2*n)),base.hi(iv.pi*(j+1)/(2*n))])
        v = state(c,H,U,iv.cos(theta),iv.sin(theta),fn)
        ed,eh,eu,flux = fn['energy'].interval(v)
        for i,x in enumerate((ed,eh,eu)):
            mean[i] += x/n
        low = base.lo(-ebase-v0['alpha']*(ed+flux))
        density_floor = low if density_floor is None else min(density_floor,low)
    vn = state(c,H,U,iv.mpf(0),iv.mpf(1),fn)
    node = fn['energy'].interval(vn)
    fnode = fn['node_flux'].interval(vn)[0]
    drho = mean[0]-node[0]-fnode
    defect = 2*v0['b']*U*v0['k']**2-v0['K_Q']*v0['p']*vn['qs']-v0['beta']*drho
    dh = -v0['K_Q']*v0['p']*vn['qh']-v0['beta']*(mean[1]-node[1])
    du = 2*v0['b']*v0['k']**2-v0['K_Q']*v0['p']*vn['qu']-v0['beta']*(mean[2]-node[2])
    return dict(F=ebase+v0['alpha']*mean[0]+v0['rho'],
                B=v0['K_Q']*(U-c['U0'])+v0['alpha']*defect,
                FH=-6*v0['M']*H+v0['alpha']*mean[1],FU=v0['alpha']*mean[2],
                BH=v0['alpha']*dh,BU=v0['K_Q']+v0['alpha']*du,
                defect=defect,density=base.point(density_floor))


def certify(c,fn,ch):
    print('CERTIFY_COUPLED_ROOT '+c['family']+' eta='+c['eta'],flush=True)
    attempts = []
    success = False
    for n in (16,32,64,128,256):
        core = enclose(c,c['Hall'],c['Uall'],n,fn)
        faces = [enclose(c,H,U,n,fn) for H,U in
                 ((c['Hlo'],c['Uall']),(c['Hhi'],c['Uall']),
                  (c['Hall'],c['Ulo']),(c['Hall'],c['Uhi']))]
        signs = dict(mean_lower_face=base.lo(faces[0]['F'])>0,mean_upper_face=base.hi(faces[1]['F'])<0,
                     node_lower_face=base.hi(faces[2]['B'])<0,node_upper_face=base.lo(faces[3]['B'])>0,
                     mean_H_derivative=base.hi(core['FH'])<0,positive_density=base.lo(core['density'])>0)
        schur = core['BU']-core['BH']*core['FU']/core['FH'] if signs['mean_H_derivative'] else iv.mpf([-mp.inf,mp.inf])
        signs['coupled_unique_root_derivative'] = base.lo(schur)>0
        attempt = dict(boxes=n,criteria=signs,mean_lower_face=base.pack(faces[0]['F']),
                       mean_upper_face=base.pack(faces[1]['F']),node_lower_face=base.pack(faces[2]['B']),
                       node_upper_face=base.pack(faces[3]['B']),derivatives={k:base.pack(core[k]) for k in ('FH','FU','BH','BU')},
                       monotone_node_derivative=base.pack(schur),density_floor=base.pack(core['density']),
                       normalized_defect=base.pack(core['defect']),
                       regulator_coefficient_correction_over_e_squared=base.pack(-core['defect']/c['values']['K_Q']))
        attempts.append(attempt)
        if all(signs.values()):
            success = True
            break
    for name,ok in signs.items():
        ch.add(name+'_'+c['family']+'_'+c['eta'],ok,criterion='strict outward inequality on fixed full H/U/amplitude rectangle')
    return dict(family=c['family'],eta=c['eta'],status='CERTIFIED_RESTRICTED_COUPLED_MEAN_NODE_ROOT' if success else 'UNRESOLVED_BY_FIXED_BOUNDS',
                attempts=attempts,H_bracket=base.pack(c['Hall']),U_bracket=base.pack(c['Uall']),
                U_reference=base.pack(c['U0']),constants=c['constants'],
                normalized_inverse_errors=[dict(field=base.pack(r),gradient=base.pack(q),residual=base.pack(t)) for r,q,t in c['errors']],
                full_initial_admission=False,state_adopted_or_evolved=False)


def point_system(c,H,U,fn):
    v0 = {k:base.midpoint(v) for k,v in c['values'].items()}
    v0.update(alpha=mp.mpf(1)/250000,eeabs=mp.mpf(1)/500,H=H,zc=U)
    v0['D'] = v0['Rc']/(1-v0['zeta']*v0['Rc']**2*v0['alpha']/2)
    def at(C,S):
        v = dict(v0,CC=C,SS=S,xi=C*C)
        pp = fn['poly'].numeric(v)
        for j,(rn,qn) in enumerate((('rs','qs'),('rh','qh'),('ru','qu'))):
            v[rn],v[qn] = C*S*pp[2*j],v['k']*pp[2*j+1]
        return v
    mean = [mp.mpf(0) for _ in range(3)]
    for j in range(64):
        theta = 2*mp.pi*j/64
        v = at(mp.cos(theta),mp.sin(theta))
        ev = fn['energy'].numeric(v)
        mean[0] += fn['analytic'].numeric(v)[0]/64
        mean[1] += ev[1]/64
        mean[2] += ev[2]/64
    mean[0] -= 8*v0['A']*v0['p']**3*v0['eeabs']/(3*mp.pi)
    vn = at(mp.mpf(0),mp.mpf(1))
    node = fn['energy'].numeric(vn)
    fl = fn['node_flux'].numeric(vn)[0]
    dd = 2*v0['b']*U*v0['k']**2-v0['K_Q']*v0['p']*vn['qs']-v0['beta']*(mean[0]-node[0]-fl)
    dh = -v0['K_Q']*v0['p']*vn['qh']-v0['beta']*(mean[1]-node[1])
    du = 2*v0['b']*v0['k']**2-v0['K_Q']*v0['p']*vn['qu']-v0['beta']*(mean[2]-node[2])
    ebase = -3*v0['M']*H**2+(v0['K_Q']*v0['p']**2+v0['D']**2+v0['rd']**2)/2+v0['pot']
    F = ebase+v0['alpha']*mean[0]+v0['rho']
    B = v0['K_Q']*(U-base.midpoint(c['U0']))+v0['alpha']*dd
    jac = mp.matrix([[-6*v0['M']*H+v0['alpha']*mean[1],v0['alpha']*mean[2]],
                     [v0['alpha']*dh,v0['K_Q']+v0['alpha']*du]])
    return mp.matrix([F,B]),jac,at


def galerkin(c,H,U,modes):
    v = {k:base.midpoint(value) for k,value in c['values'].items()}
    ee,k = mp.mpf(1)/500,v['k']
    mat,rhs = mp.matrix(modes),mp.matrix(modes,1)
    for j in range(64):
        theta = 2*mp.pi*j/64
        w,wp,wpp = ee*mp.cos(theta),-k*ee*mp.sin(theta),-k*k*ee*mp.cos(theta)
        P = v['MU2']*(v['c1']+v['c2']+v['c3'])*(1+w*w)
        T = v['c4']+(v['c1']-(v['c2']+v['c3'])*w*w)/(1+w*w)
        W = -v['MU2']*((v['c2']+T)*wp*wp+v['c2']*w*wpp)
        A0 = v['c1']+2*v['c2']+v['c4']+(v['c2']-v['c3']+v['c4'])*w*w
        AH = 3*v['c1']+5*v['c2']+v['c3']+2*v['c4']+(2*v['c1']+4*v['c2']+2*v['c4'])*w*w
        force = v['MU2']*w*wp/(1+w*w)*(v['H0']*A0-H*AH)+3*v['b']*v['p']*U*w**3*wp
        sn = [mp.sin(2*(i+1)*theta) for i in range(modes)]
        ds = [2*(i+1)*k*mp.cos(2*(i+1)*theta) for i in range(modes)]
        for a in range(modes):
            rhs[a] += force*sn[a]/64
            for b in range(modes):
                mat[a,b] += (P*ds[a]*ds[b]+W*sn[a]*sn[b])/64
    coeff = mp.lu_solve(mat,rhs)
    return lambda theta: (sum(coeff[i]*mp.sin(2*(i+1)*theta) for i in range(modes)),
                          sum(coeff[i]*2*(i+1)*k*mp.cos(2*(i+1)*theta) for i in range(modes)))


def independent(c,fn,ch):
    print('POINT_ROOT_AND_INDEPENDENT_GALERKIN '+c['family']+' eta='+c['eta'],flush=True)
    H,U = base.midpoint(c['values']['H0']),base.midpoint(c['U0'])
    for step in range(20):
        residual,jac,at = point_system(c,H,U,fn)
        if max(abs(x) for x in residual) <= mp.mpf('1e-60'):
            break
        update = mp.lu_solve(jac,residual)
        H,U = H-update[0],U-update[1]
    residual,jac,at = point_system(c,H,U,fn)
    ch.small('approximate_joint_root_'+c['family']+'_'+c['eta'],max(abs(x) for x in residual),'1e-60')
    ch.add('approximate_root_inside_frozen_rectangle_'+c['family']+'_'+c['eta'],
           base.lo(c['Hall'])<=H<=base.hi(c['Hall']) and base.lo(c['Uall'])<=U<=base.hi(c['Uall']))
    g8,g12 = galerkin(c,H,U,8),galerkin(c,H,U,12)
    errs,polyerrs = [],[]
    for theta in (mp.mpf(0),mp.pi/7,mp.pi/2):
        a,b = g8(theta),g12(theta)
        errs.extend(abs(x-y)/(1+abs(x)+abs(y)) for x,y in zip(a,b))
        v = at(mp.cos(theta),mp.sin(theta))
        polyerrs.append([base.SHOW(abs(b[0]-v['alpha']*v['rs'])),base.SHOW(abs(b[1]-v['alpha']*v['qs']))])
    ch.small('independent_shift_8_12_'+c['family']+'_'+c['eta'],max(errs),'1e-30')
    return dict(family=c['family'],eta=c['eta'],H=base.SHOW(H),U=base.SHOW(U),
                relative_U_change=base.SHOW(U/base.midpoint(c['U0'])-1),newton_steps=step+1,
                root_residual=base.SHOW(max(abs(x) for x in residual)),
                galerkin_8_12_normalized_difference=base.SHOW(max(errs)),
                galerkin_vs_polynomial_absolute_differences=polyerrs,
                interpretation='Approximate quadrature/Galerkin diagnostics; exact existence and error control come from the interval/residual proof, not agreement.')


def calculate():
    mp.mp.dps,iv.dps = 110,80
    pins,before = sources()
    ch = base.Checks()
    base.interval_prerequisites(ch)
    u,fn,formulas = symbolic(ch)
    cases,controls = [],[]
    for item in READ(CERTS):
        c = make_case(item,fn)
        cases.append(certify(c,fn,ch))
        controls.append(independent(c,fn,ch))
    _,after = sources()
    ch.add('all_source_bytes_sidecars_metadata_preserved',before==after)
    ok = all(row['passed'] for row in ch.rows)
    count = sum(row['status']=='CERTIFIED_RESTRICTED_COUPLED_MEAN_NODE_ROOT' for row in cases)
    summary = dict(validation='PASS_RESTRICTED_COUPLED_NODE_COMPLETION_ONLY' if ok and count==9 else 'FAIL_OR_UNRESOLVED_COUPLED_NODE_COMPLETION',
                   passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows,
                   certified_cases=count,source_sha256=pins,source_metadata=before,
                   full_initial_admission=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
                   physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                   status='RESTRICTED_MEAN_NODE_PAIR_ONLY_HIGHER_COMPLETION_AND_EVOLUTION_OPEN',
                   missing_required_physics=formulas['exclusions'])
    return {'summary.json':summary,'formulas.json':formulas,'certificates.json':cases,'independent.json':controls}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output')
    p.add_argument('--replay')
    args = p.parse_args()
    if bool(args.output)==bool(args.replay):
        p.error('choose one fresh output or read-only replay')
    dest = (ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):
        raise ValueError('outside output root')
    if args.output:
        dest.mkdir(parents=True,exist_ok=False)
    old = {q.name:(SHA(q.read_bytes()),q.stat().st_size,q.stat().st_mtime_ns) for q in dest.iterdir()} if args.replay else None
    data = calculate()
    payload = {n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):
        payload[name+'.sha256'] = (SHA(raw)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(old)!=set(payload):
            raise ValueError('replay file-set mismatch')
        for name,raw in payload.items():
            q = dest/name
            if q.read_bytes()!=raw:
                raise ValueError('recomputed bytes differ '+name)
            if (SHA(q.read_bytes()),q.stat().st_size,q.stat().st_mtime_ns)!=old[name]:
                raise ValueError('original metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as stream:
                stream.write(raw)
    su = data['summary.json']
    print(json.dumps({k:su[k] for k in ('validation','passed','total','certified_cases','status')}),flush=True)
    return 0 if su['passed']==su['total'] and su['certified_cases']==9 else 1


if __name__=='__main__':
    raise SystemExit(main())
