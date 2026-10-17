"""Exact low-rank repair of the complete R4C1 fast-map inverse.

The rejected cubic construction is preserved. This executable starts from the
unspecialized action and uses a two-by-two Schur complement, not that inverse.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import re

import numpy as np
import sympy as s

import test_01_r4c1_three_family_weighted_evolution_v4 as old

ev = old.ev
ROOT, BASE = old.ROOT, old.BASE
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_LOW_RANK_INVERSE_V1_CONTRACT_2026-10-17.md'
REJECT = 'Theory/Gates/RES-001/RES001_R4C1_WEIGHTED_EVOLUTION_CUBIC_REJECTION_REPORT_2026-10-17.md'
REJECT_BASE = BASE + 'r4c1_weighted_cubic_rejection_attempt_01/'
CLEAN, ON, NORM = old.CLEAN, old.ON, old.NORM
Checks = old.Checks
CASES = [(f, s.Rational(e)) for f in
         ('archived_G3', 'new_B1_frame', 'new_hierarchical')
         for e in ('1/4', '1/64', '1/1024')]


def inputs():
    pins, absent, _, generic, prior, time = old.inputs()
    pins.update({
        REJECT: 'd2b88d18c74ed5a5557bdae7dc41cbc941826f27d38ca1790b9c690d3e90c5ba',
        REJECT_BASE+'summary.json': 'aa3092b89e861a85a004552a74273574aec5df538bcb3f293e3c676f88c3e621',
        REJECT_BASE+'cubic_residual.json': '64083e1895a85d7bdf24dc411dbf46605a7ee1a4690ce09882a47e2e342dc4ed',
        REJECT_BASE+'formulas.json': '7637a4013838428d62b94bf854c6443713e82f5144901edb147a145f3c9278e3',
        CONTRACT: ev.SHA((ROOT/CONTRACT).read_bytes()),
        SELF: ev.SHA((ROOT/SELF).read_bytes()),
    })
    paths = []
    for name, digest in pins.items():
        p = ROOT/name
        if ev.SHA(p.read_bytes()) != digest:
            raise RuntimeError('Frozen input drift: '+name)
        paths.append(p)
        side = Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower() != digest:
                raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        elif name not in absent:
            raise RuntimeError('Required sidecar absent: '+name)

    def snapshot():
        return [(p.relative_to(ROOT).as_posix(), ev.SHA(p.read_bytes()),
                 p.stat().st_size, p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    return pins, absent, snapshot, generic, prior, time


class Derivation:
    def __init__(self, ch, family, eta):
        self.family, self.eta = family, eta
        print('ACTION', family, str(eta), flush=True)
        wire = ev.READ(old.PARENT+'formulas.json')
        texts = ' '.join(q for key in ('A', 'R', 'K')
                         for row in wire[key]['entries'] for q in row)
        names = set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*', texts))-{'I', 'sqrt'}
        names.update(('eta', 'rho', 'p'))
        x = {n: s.Symbol(n, positive=True) if n in ('a', 'ell', 'eta', 'p', 'C')
             else s.Symbol(n, real=True) for n in names}
        mapping = ev.READ(ev.PLANAR)['families'][family]['parameter_map']
        fixed = {n: s.sympify(q).subs(s.Symbol('eta'), eta)
                 for n, q in mapping.items() if n in x}
        fixed.update(m2=s.Integer(1), lambda4=s.Rational(1,3),
                     lambda6=s.Rational(1,5), Lambda=s.Integer(2),
                     mr2=s.Integer(2), lambda_r=s.Rational(1,7),
                     rho_Lambda=s.Integer(0), g_r=3*eta/7)
        self.parameter_map = {n: str(v) for n, v in fixed.items()}
        x.update(fixed)
        self.x = x
        loc = {**x, 'I': s.I, 'sqrt': s.sqrt}
        load = lambda key: s.Matrix([[s.sympify(q, locals=loc) for q in row]
                                    for row in wire[key]['entries']])
        O = load('SO2_map')
        self.O20 = s.diag(O, O)
        a, ell = x['a'], x['ell']
        H,u,ud,v,vd,r,rd,pd,rho,C = (x[n] for n in
            ('H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho','C'))
        MP, MU = x['MP2'], x['MU2']
        f2 = MU*(x['c1']+x['c4'])
        MC = MP+MU*(x['c1']+3*x['c2']+x['c3'])/2
        rad = u*u+v*v
        V = (x['m2']*rad/2+x['lambda4']*rad**2/8
             +x['lambda6']*rad**3/(24*x['Lambda']**2)
             +x['mr2']*r*r/2+x['lambda_r']*r**4/4
             +x['g_r']*rad*r*r/4+x['rho_Lambda'])
        kin = ud*ud+vd*vd+rd*rd+x['K_Q']*pd*pd
        self.bg = s.Matrix([a,H,u,ud,v,vd,r,rd,pd,rho,C])
        self.rates = s.Matrix([
            a*H, -(kin+rho)/(2*MC),
            ud, -3*H*ud-s.diff(V,u), vd, -3*H*vd-s.diff(V,v),
            rd, -3*H*rd-s.diff(V,r),
            -3*H*pd-x['beta']*rho/x['K_Q'],
            (-3*H+x['beta']*pd)*rho, x['beta']*pd*C])
        self.dt = lambda m: m.applyfunc(lambda q: CLEAN(sum(
            s.diff(q,z)*rate for z,rate in zip(self.bg,self.rates)
            if z in q.free_symbols)))
        self.V, self.energy, self.MC = V, kin/2+V+rho, MC
        self.constraint = 3*MC*H*H-self.energy
        ch.exact('background_energy_balance',
                 self.dt(s.Matrix([self.energy]))[0]+3*H*(kin+rho))
        ch.exact('background_constraint_balance',
                 self.dt(s.Matrix([self.constraint]))[0])
        ch.exact('background_dust_charge',
                 self.dt(s.Matrix([a**3*rho/C]))[0])
        A,R,K = [ON((O.T*load(key)*O).subs(x['epsilon0'],rho/C**4))
                 for key in ('A','R','K')]
        Ki = s.diag(*(1/K[i,i] for i in range(10)))
        ch.exact('complete_kinetic_inverse', K*Ki-s.eye(10))
        G = s.zeros(20)
        G[:10,10:] = s.eye(10)
        G[10:,:10] = ON(Ki*(A-self.dt(R)-3*H*R))
        G[10:,10:] = ON(Ki*(R.conjugate().T-R-self.dt(K)-3*H*K))
        self.G = G
        B, Bi = s.eye(20), s.eye(20)
        for i in range(10):
            if i not in (3,9):
                B[i,i], Bi[i,i] = ell/a, a/ell
        B[9,9], B[9,3] = ell**2/a**2, -s.I*ell*pd/a
        Bi[9,9], Bi[9,3] = a*a/ell**2, s.I*a*pd/ell
        B[19,13], Bi[19,13] = -s.I*a*pd/ell, s.I*a*pd/ell
        ch.exact('balance_inverse_both_orders',
                 list(B*Bi-s.eye(20))+list(Bi*B-s.eye(20)))
        self.B,self.Bi,self.Bd = B,Bi,self.dt(B)
        self.blocks = old.laurent(ON((self.Bd+B*G)*Bi),ell)
        ch.add('all_balance_powers_retained',
               set(self.blocks).issubset({-2,-1,0,1,2}), sorted(self.blocks))
        F,L = self.blocks[2],self.blocks[1]
        fast = (9,19)
        rest = [i for i in range(20) if i not in fast]
        Ff = F.extract(fast,fast)
        ch.exact('dispersive_block',Ff-s.Matrix(
            [[0,1/a**2],[-x['b']/(x['K_Q']*a*a),0]]))
        remainder_F = F.copy()
        for i in fast:
            for j in fast:
                remainder_F[i,j] = 0
        ch.exact('only_degree_two_dispersive_pair',remainder_F)
        off,Ld,U = s.zeros(20),L.copy(),s.zeros(20)
        for ii in rest:
            for jj in fast:
                off[ii,jj],Ld[ii,jj] = L[ii,jj],0
                off[jj,ii],Ld[jj,ii] = L[jj,ii],0
        upper = ON(off.extract(rest,fast)*Ff.inv())
        lower = ON(-Ff.inv()*off.extract(fast,rest))
        for i,ii in enumerate(rest):
            for j,jj in enumerate(fast):
                U[ii,jj],U[jj,ii] = upper[i,j],lower[j,i]
        U = ON(U)
        self.U,self.Ud = U,self.dt(U)
        self.g = CLEAN(s.trace(U*U)/2)
        ch.exact('fast_cross_commutator',F*U-U*F+off)
        ch.exact('negative_g_binding',self.g+a*a*x['beta']**2*f2/x['b'])

        # Exact 18+2 Schur inverse, including nilpotent cross terms.
        print('SCHUR inverse',family,str(eta),flush=True)
        q = s.Symbol('inverse_ell',positive=True)
        S = ON(lower*upper)
        D = s.eye(2)-q*q*S
        den = CLEAN(D.det())
        adj = s.Matrix([[D[1,1],-D[0,1]],[-D[1,0],D[0,0]]])
        P = s.zeros(20)
        tl = ON(den*s.eye(18)+q*q*upper*adj*lower)
        tr,bl = ON(-q*upper*adj),ON(-q*adj*lower)
        for i,ii in enumerate(rest):
            for j,jj in enumerate(rest):
                P[ii,jj] = tl[i,j]
            for j,jj in enumerate(fast):
                P[ii,jj],P[jj,ii] = tr[i,j],bl[j,i]
        for i,ii in enumerate(fast):
            for j,jj in enumerate(fast):
                P[ii,jj] = adj[i,j]
        P = ON(P)
        ch.exact('Schur_two_dimensional_adjugate',D*adj-den*s.eye(2))
        ch.exact('full_inverse_left',(s.eye(20)+q*U)*P-den*s.eye(20))
        ch.exact('full_inverse_right',P*(s.eye(20)+q*U)-den*s.eye(20))
        ch.exact('Schur_determinant_rank_one',S.det())
        ch.exact('complete_denominator',den-(1-self.g*q*q))
        ch.exact('fifth_degree_annihilator',U**5-self.g*U**3)
        self.cubic_residual = ON(U**3-self.g*U)
        ch.add('old_cubic_defect_retained',
               any(z!=0 for z in self.cubic_residual))
        self.inverse_coeff = old.laurent(P,q)
        ch.add('inverse_numerator_is_finite_polynomial',
               all(0<=j<=4 for j in self.inverse_coeff),
               sorted(self.inverse_coeff))
        self.den = den.subs(q,1/ell)
        self.den_q = den
        self.q = q
        self.S = S
        self.P = P
        cs,ct,cv = [s.sympify(wire[n],locals=loc)
                    for n in ('scalar_c2','tensor_c2','vector_c2')]
        kh = K[0,0]
        d = s.I*MP/(s.sqrt(2)*f2)
        c = s.I*MP/(s.sqrt(2)*kh*cs)
        e = CLEAN(-a*Ld[10,3]/cs)
        Tw,Ti = s.eye(20),s.eye(20)
        Tw[13,:] = s.eye(20)[13,:]+d*s.eye(20)[0,:]
        Tw[0,:] = s.eye(20)[0,:]+c*Tw[13,:]+e*s.eye(20)[3,:]
        Ti[0,:] = s.eye(20)[0,:]-c*s.eye(20)[13,:]-e*s.eye(20)[3,:]
        Ti[13,:] = s.eye(20)[13,:]-d*Ti[0,:]
        Gm = s.Matrix([[1+x['zeta']*v*v,-x['zeta']*u*v,0],
                       [-x['zeta']*u*v,1+x['zeta']*u*u,0],[0,0,1]])
        shift = ON(-a*Gm.inv()*Ld.extract([16,17,18],[3]))
        for i in range(3):
            Tw[6+i,3],Ti[6+i,3] = shift[i],-shift[i]
        self.Tw,self.Ti = Tw,Ti = ON(Tw),ON(Ti)
        self.Twd = self.dt(Tw)
        ch.exact('wave_inverse_both_orders',
                 list(Tw*Ti-s.eye(20))+list(Ti*Tw-s.eye(20)))
        self.F,self.L = ON(Tw*F*Ti),ON(Tw*Ld*Ti)
        Q = s.eye(20)
        Q[0,0],Q[1,1],Q[2,2] = cs,ct,ct
        Q[4,4],Q[5,5],Q[9,9] = cv,cv,x['b']/x['K_Q']
        Q[6:9,6:9] = Gm
        self.Q,self.Qd = Q,self.dt(Q)
        ch.exact('dispersive_positive_power_Q_skew',
                 Q*self.F+self.F.conjugate().T*Q)
        ch.exact('wave_positive_power_Q_skew',
                 Q*self.L+self.L.conjugate().T*Q)
        rank = s.zeros(20)
        rank[6:8,6:8] = x['zeta']*s.Matrix([v,-u])*s.Matrix([[v,-u]])
        diag = Q-rank
        ch.exact('Q_positive_diagonal_plus_positive_rank_one',
                 diag-s.diag(*diag.diagonal()))
        ch.add('positive_rank_one_coefficient',x['zeta']>0,str(x['zeta']))
        ch.add('Q_coercivity_one_tenth',
               all(CLEAN(v-s.Rational(1,10))>0 for v in diag.diagonal()),
               list(map(str,diag.diagonal())))
        ch.add('denominator_at_least_one',
               CLEAN(self.g/(-a*a))>0,str(CLEAN(self.g/(-a*a))))

        # Full generator identity, with no continual slow-graph projection.
        print('GENERATOR complete coefficients',family,str(eta),flush=True)
        M0,M1,M2 = [self.blocks.get(k,s.zeros(20)) for k in (0,-1,-2)]
        ns = [ON(L*U-U*Ld+M0),ON(M0*U+M1-self.Ud),
              ON(M1*U+M2),ON(M2*U)]
        pre = {}
        def add_to(out,k,m):
            out[k] = out.get(k,s.zeros(20))+m
        for k,m in self.blocks.items():
            add_to(pre,k,m)
            add_to(pre,k-1,m*U)
        add_to(pre,-1,-self.Ud)
        diff = dict(pre)
        for k,m in ((2,-F),(1,-Ld-U*F),(0,-U*Ld)):
            add_to(diff,k,m)
        for k,m in diff.items():
            ch.exact('preinverse_remainder_power_'+str(k),
                     m-(ns[-k] if -3<=k<=0 else s.zeros(20)))
        raw = [ON(sum((Pj*ns[j-k] for k,Pj in self.inverse_coeff.items()
                       if 0<=j-k<4),s.zeros(20)))
               for j in range(8)]
        direct = {}
        for j,Pj in self.inverse_coeff.items():
            for k,m in pre.items():
                add_to(direct,k-j,Pj*m)
        den_coeff = old.laurent(s.Matrix([[den]]),q)
        for j,dj in den_coeff.items():
            add_to(direct,2-j,-dj[0,0]*F)
            add_to(direct,1-j,-dj[0,0]*Ld)
        for k in sorted(set(direct)|set(range(-7,1))):
            ch.exact('complete_transformed_generator_power_'+str(k),
                     direct.get(k,s.zeros(20))-
                     (raw[-k] if -7<=k<=0 else s.zeros(20)))
        self.N = [ON(Tw*n*Ti) for n in raw]
        self.drift = ON(self.Twd*Ti)
        self.S0 = ON(self.Qd+Q*self.drift+self.drift.conjugate().T*Q)
        self.Sj = [ON(Q*n+n.conjugate().T*Q) for n in self.N]
        ch.add('full_remainder_retained',any(z!=0 for n in self.N for z in n))
        ch.add('quartic_pair_retained',self.F[9,19]!=0 and self.F[19,9]!=0)

    def numeric(self,ch,generic,prior,time):
        mats = [self.B,self.Bi,self.Bd,self.U,self.Ud,self.Tw,self.Ti,
                self.Twd,self.Q,self.Qd,self.F,self.L,self.drift,
                *[self.inverse_coeff.get(i,s.zeros(20)) for i in range(5)],
                *self.N]
        symbols = sorted(set().union(*(m.free_symbols for m in mats)),key=str)
        fn = s.lambdify([symbols],mats+[s.Matrix([[self.g]])],'numpy',cse=True)
        red = time.EvolvingReduction(prior,generic)
        O = np.asarray(self.O20,complex)
        p = generic.bg.PARAMS.copy()
        for n,q in ev.READ(ev.PLANAR)['families'][self.family]['parameter_map'].items():
            p['K' if n=='K_Q' else n] = float(s.sympify(q).subs(s.Symbol('eta'),self.eta))
        p['gr'] = float(3*self.eta/7)
        maxima = {k:0. for k in ('generator','energy_derivative','inverse',
                                 'dense_inverse','auxiliary')}
        witness = {k:0. for k in ('balance_drift','fast_drift','wave_drift',
                                  'extra_inverse','remainder')}
        records = []
        runs = ev.READ(old.parent.PARENT+'trajectories.json')['runs']
        for ir,run in enumerate(runs):
            if run['family']!=self.family or s.Rational(run['eta_exact'])!=self.eta:
                continue
            for it,stored in enumerate(run['first_order_states']):
                b = np.asarray(stored[:12],float)
                raw = dict(zip(red.op.kernel.order,red.op.kernel.values(b,p)))
                raw['rho'] = b[10]
                for mode in (4,80):
                    raw['ell'] = mode
                    vals = [np.asarray(m,complex) for m in fn([raw[str(z)] for z in symbols])]
                    B,Bi,Bd,U,Ud,Tw,Ti,Twd,Q,Qd,F,L,drift = vals[:13]
                    Pc,Ns = vals[13:18],vals[18:26]
                    gg = float(vals[26][0,0].real)
                    den = 1-gg/mode**2
                    tf = np.eye(20)+U/mode
                    tfi = sum((m/mode**j for j,m in enumerate(Pc)),np.zeros((20,20),complex))/den
                    dense = np.linalg.inv(tf)
                    inv = max(NORM(tf@tfi-np.eye(20)),NORM(tfi@tf-np.eye(20)))
                    dinv = NORM(tfi-dense)/(1+NORM(tfi)+NORM(dense))
                    data = red.at(b,p,mode,np.zeros(22),np.zeros(4))
                    G = data['G']
                    ac = (Bd+B@O.conj().T@G@O)@Bi
                    exact = (Twd+Tw@tfi@(ac@tf-Ud/mode))@Ti
                    residual = drift+sum((n/mode**j for j,n in enumerate(Ns)),
                                          np.zeros((20,20),complex))/den
                    factored = mode**2*F+mode*L+residual
                    ge = NORM(exact-factored)/(1+NORM(exact)+NORM(factored))
                    M = Tw@tfi@B@O.conj().T
                    Md = (Twd@tfi@B-Tw@tfi@(Ud/mode)@tfi@B+Tw@tfi@Bd)@O.conj().T
                    P = M.conj().T@Q@M
                    Pd = Md.conj().T@Q@M+M.conj().T@Qd@M+M.conj().T@Q@Md
                    lhs = Pd+G.conj().T@P+P@G
                    rhs = M.conj().T@(Qd+factored.conj().T@Q+Q@factored)@M
                    ee = NORM(lhs-rhs)/(1+NORM(lhs)+NORM(rhs))
                    rec = red.reconstruct(data,np.linspace(.01,.2,20)*(1+.1j),p)
                    for key,value in dict(generator=ge,energy_derivative=ee,
                            inverse=inv,dense_inverse=dinv,auxiliary=rec['error']).items():
                        maxima[key] = max(maxima[key],value)
                    old_inv = np.eye(20)-U/(mode*den)+U@U/(mode**2*den)
                    for key,value in dict(
                            balance_drift=NORM(Tw@tfi@Bd@Bi@tf@Ti)/(1+NORM(exact)),
                            fast_drift=NORM(Tw@tfi@(Ud/mode)@Ti)/(1+NORM(exact)),
                            wave_drift=NORM(drift)/(1+NORM(exact)),
                            extra_inverse=NORM(tfi-old_inv),
                            remainder=NORM(residual)/(1+NORM(exact))).items():
                        witness[key] = max(witness[key],value)
                    records.append(dict(run=ir,node=it,ell=mode,generator=ge,
                        energy_derivative=ee,inverse=inv,dense_inverse=dinv,
                        auxiliary=rec['error'],Q_min_eigenvalue=float(
                            np.linalg.eigvalsh(Q).min())))
        for name,value in maxima.items():
            ch.small('independent_all_nodes_'+name,value,1e-9)
        for name,value in witness.items():
            ch.add('reject_omitted_'+name,value>1e-12,value,'>1e-12')
        ch.add('all_84_case_action_controls',len(records)==84,len(records))
        return dict(records=records,maxima=maxima,rejection_witnesses=witness,
                    independent_full_action_reducer=True,new_integrations=False)

    def bounds(self,ch):
        # This method is allowed only after exact and numeric prerequisites.
        x = self.x
        a,H,u,ud,v,vd,r,rd,pd,rho,C = self.bg
        eta = self.eta
        initial = {a:1,u:s.sqrt(eta),ud:0,v:0,vd:s.sqrt(eta),
                   r:s.sqrt(eta),rd:s.sqrt(eta)/4,pd:eta/5,rho:s.Rational(1,5),C:1}
        E0 = CLEAN(self.energy.subs(initial))
        ch.add('initial_energy_between_zero_and_one',0<E0<1,str(E0))
        ch.add('initial_H_between_quarter_and_one',
               s.Rational(1,16)<E0/(3*self.MC)<1,str(E0/(3*self.MC)))
        ch.exact('actual_clock_source_scaling',x['beta']/x['K_Q']-2*eta/15)
        ch.exact('actual_dust_coupling_scaling',x['beta']-2*eta**2/5)
        ch.exact('H_differential_comparison',
                 self.rates[1]+3*H*H-(self.V+rho/2+self.constraint)/self.MC)
        ch.add('potential_nonnegative',
               all(coef.is_nonnegative and all(k%2==0 for k in powers)
                   for powers,coef in s.Poly(self.V,u,v,r).terms()))
        ch.add('positive_clock_bootstrap',
               s.Rational(1,5)-s.Rational(2,15)*s.Rational(20,19)**3/20
               >s.Rational(20,19)**3/10)
        ch.add('clock_positive_H_lower_comparison',
               s.Rational(1,4)/(1+3*s.Rational(1,4)/20)>s.Rational(1,5))
        ch.add('rho_lower_bootstrap',s.Rational(1,5)*s.Rational(19,20)**3>s.Rational(1,6))
        ch.add('rho_upper_bootstrap',s.Rational(1,5)*s.Rational(250,249)<s.Rational(1,4))
        ch.add('C_upper_bootstrap',s.Rational(16000,15999)<s.Rational(250,249))
        box = {a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(1,5),s.Integer(1)),
               **{z:(s.Integer(-2),s.Integer(2)) for z in (u,ud,v,vd,r,rd)},
               pd:(eta/10,eta/5),rho:(s.Rational(1,6),s.Rational(1,4)),
               C:(s.Integer(1),s.Rational(250,249))}
        bx = old.RationalBox(box)
        matrices = [self.S0,*self.Sj]
        rows = []
        for i in range(20):
            rows.append(CLEAN(10*(sum(bx.absolute(matrices[0][i,j]) for j in range(20))
                +sum(sum(bx.absolute(matrices[k+1][i,j]) for j in range(20))/4**k
                     for k in range(len(self.Sj))))))
        mu = max([s.Integer(0),*rows])
        ch.add('outward_rational_energy_constant',
               all(q.is_Rational for q in rows) and mu>=0)
        return dict(mu_exact=str(mu),mu_display=float(mu),rows_exact=list(map(str,rows)),
            endpoint_log_amplification_upper=float(mu/40),Q_lower='I/10',
            ell_min=4,time_domain='0<=s<=t<=1/20',
            inequality='sqrt(E(t))<=exp(mu*(t-s)/2)*sqrt(E(s))',
            E='w^dagger Q(t) w',background_box={str(z):list(map(str,b)) for z,b in box.items()},
            initial_energy_exact=str(E0),
            proof='On shell E_dot=-3H(kinetic+rho), V>=0, positive dust. E0<1; '
                  'H_dot>=-3H^2 gives H>1/5, H<=H0<1, 1<=a<=exp(1/20)<=20/19. '
                  'Positive mass terms and kinetic energy bound all fields/velocities by 2. '
                  'a^3*psi_dot=eta/5-(2eta/15)*integral(a^3*rho); a^3*rho<=(20/19)^3 '
                  'gives eta/10<psi_dot<=eta/5 through t=1/20 by bootstrap. '
                  'C_dot/C=beta*psi_dot<=1/800, so 1<=C<=exp(1/16000)<=16000/15999<250/249. '
                  'Dust charge gives rho=C/(5a^3) in (1/6,1/4). '
                  'Exact positive-power Q-skew identities remove ell^2 and ell terms. '
                  'The full Schur denominator>=1, Q>=I/10; outward rational row sums '
                  'bound every complete Hermitian remainder coefficient, giving E_dot<=mu E.',
            physical_energy_positive=False,physical_window=False)

    def export(self):
        matrices = dict(B=self.B,B_inverse=self.Bi,B_dot=self.Bd,U=self.U,
            U_dot=self.Ud,Schur_product=self.S,inverse_numerator=self.P,
            cubic_defect=self.cubic_residual,Tw=self.Tw,Tw_inverse=self.Ti,
            Tw_dot=self.Twd,Q=self.Q,Q_dot=self.Qd,F=self.F,L=self.L,drift=self.drift,
            **{'inverse_coefficient_'+str(j):m for j,m in self.inverse_coeff.items()},
            **{'N'+str(j):n for j,n in enumerate(self.N)})
        return dict(family=self.family,eta_exact=str(self.eta),parameter_map=self.parameter_map,
            matrices={n:old.parent.MAT(m) for n,m in matrices.items()},
            g=str(self.g),inverse_ell_symbol=str(self.q),denominator=str(self.den),
            annihilating_polynomial='U^5-g*U^3=0; no minimal-degree claim',
            state='w=Tw*(I+U/ell)^(-1)*B*SO2^dagger*(y,y_dot)',
            generator='ell^2 F+ell L+drift+sum_{j=0}^7 N_j/ell^j /(1-g/ell^2)',
            all_twenty_states=True,zero_mode_excluded=True)


def calculate(emit_case):
    pins,absent,snapshot,generic,prior,time = inputs()
    before = snapshot()
    checks,cases = [],[]
    for index,(family,eta) in enumerate(CASES):
        ch = Checks()
        der = Derivation(ch,family,eta)
        good = lambda: all(row['passed'] for row in ch.rows)
        numbers = der.numeric(ch,generic,prior,time) if good() else dict(
            skipped='Exact inverse/generator prerequisite failed')
        bounds = der.bounds(ch) if good() else dict(
            skipped='Exact/independent numerical prerequisite failed')
        record = dict(index=index,family=family,eta_exact=str(eta),
                      accepted=good(),checks=ch.rows,bounds=bounds,
                      formulas=der.export(),numerics=numbers)
        emit_case('case_'+str(index).zfill(2)+'.json',ev.ENCODE(record))
        cases.append(dict(index=index,family=family,eta_exact=str(eta),
                          accepted=good(),mu_exact=bounds.get('mu_exact'),
                          action_probes=len(numbers.get('records',[]))))
        for row in ch.rows:
            checks.append(dict(row, name=family+'|'+str(eta)+'|'+row['name']))
        print('CASE_COMPLETE',index,good(),bounds.get('mu_display'),flush=True)
        if not good():
            break
    ch = Checks()
    ch.add('all_nine_exact_cases_present',len(cases)==9,len(cases))
    ch.add('all_756_independent_full_action_probes',
           sum(c['action_probes'] for c in cases)==756,
           sum(c['action_probes'] for c in cases))
    ch.add('source_hash_size_mtime_preserved',before==snapshot())
    checks.extend(ch.rows)
    passed = sum(row['passed'] for row in checks)
    complete = passed==len(checks) and len(cases)==9
    return dict(schema='r4c1-low-rank-inverse-v1',
        validation='PASS_LOCAL_LINEAR_ESTIMATE' if complete else 'FAIL_LOCAL_LINEAR_ESTIMATE',
        status='EXACT_SCHUR_INVERSE_FULL_GENERATOR_WEIGHTED_LINEAR_ESTIMATE' if complete
               else 'INVERSE_OR_WEIGHTED_ESTIMATE_UNRESOLVED',
        passed=passed,total=len(checks),checks=checks,cases=cases,
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,claim_status='Conditional',
        weighted_linear_estimate_verified=complete,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',Rule9_cleared=False,
        canonical_energy_positive=False,physical_window_admitted=False,
        full_nonlinear_fixed_charge_admission=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
        Stage4A='CLOSED',TOP_X4='UNCHANGED',native_goal_active=True,
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        review_dependencies=['THREE-FAMILY-FINITE-K-V3','WEIGHTED-CUBIC-REJECTION-V1',
            'CUSP3-EVOLUTION-V1','THREE-FAMILY-FIXED-CHARGE-KINETIC-V3',
            'GENERIC-KERNEL/EVOLVING-REDUCTION','all transitive debt'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_low_rank_inverse_attempt_01')
    ap.add_argument('--replay')
    args = ap.parse_args()
    dest = (ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():
            raise FileNotFoundError('Replay absent')
        before = [(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                  for p in sorted(dest.iterdir())]
    elif dest.exists():
        raise FileExistsError('Refuse overwrite of existing evidence')
    else:
        dest.mkdir(parents=True)
    artifacts = {}
    def emit(name,body):
        digest = ev.SHA(body)
        side = (digest+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:
                raise RuntimeError('Read-only replay drift: '+name)
        else:
            with (dest/name).open('xb') as f:
                f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:
                f.write(side)
        artifacts[name] = digest
    try:
        summary = calculate(emit)
        summary['artifacts'] = dict(artifacts)
        emit('summary.json',ev.ENCODE(summary))
    except BaseException as exc:
        if not args.replay:
            emit('interrupted.json',ev.ENCODE(dict(
                validation='INTERRUPTED_NO_ACCEPTED_ESTIMATE',
                error_type=type(exc).__name__,error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        after = [(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                 for p in sorted(dest.iterdir())]
        if before!=after:
            raise RuntimeError('Replay changed artifact metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:summary[k] for k in
        ('validation','passed','total','status','physics_pass')}),flush=True)
    for row in summary['checks']:
        if not row['passed']:
            print(json.dumps(row),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__ == '__main__':
    raise SystemExit(main())
