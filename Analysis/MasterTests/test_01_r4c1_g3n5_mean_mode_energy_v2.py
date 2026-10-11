"""G3N5 homogeneous canonical constraints, two clocks and charge sectors.

New local evidence only. All old sources/receipts are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
OLD = BASE + "r4c1_g3n5_constraint_response_attempt_01/"
PRECISE = BASE + "r4c1_g3n5_constraint_response_attempt_02/"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_CONTRACT_2026-10-11.md"
SOURCE = "Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v1.py"
PINS = {
    "Analysis/MasterTests/test_01_r4c1_g3n5_mean_mode_energy_v1.py": "13918f5109a41db54e713b53a4ec8469d212291a0c3dae753cc96803b6941c65",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_V2_COMPUTE_ADDENDUM_2026-10-11.md": "de96b97cd4abba079614ec96aff80b30b8fb0c5cd8d9917ec5c0f38fa23ed157",
    SOURCE: "6b9cc5f402957172c0dfcaa2f0a81997235287380e77a60c4649eb9e16a09f37",
    CONTRACT: "b82a740a0bb12946e6ae195fb0f6648d6727f8a87c7d9ae96c1fd491c6191446",
    PRECISE + "summary.json": "04705ea37aa944a567387073b1eda81c824d447566d061ddfd684abfbf30649d",
    "Theory/Core/ITSM_G3N5_MEAN_MODE_ENERGY_GOAL_PLAN_2026-10-11.md":
        "9d9a8f5cb73d05393af3a0f63d07f25140d01f3773bd2e735308e751734b86f3",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_CONSTRAINT_RESPONSE_REPORT_2026-10-10.md":
        "b0b6ee418edb54a90bbed4ce8be31717d5ecd12a5b96d66625de02177d98c931",
}
if hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest() != PINS[SOURCE]:
    raise RuntimeError("Frozen response source drift")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3n5_constraint_response_v1 as old

common = old.common
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
I = old.IDX
FIELDS = old.FIELDS
DUST_NAMES = list(FIELDS[4:17])
PHASE_NAMES = list(FIELDS[4:16]) + ["T"]


def expanded(m):
    return m.applyfunc(s.expand)


def J(n):
    return s.BlockMatrix([[s.zeros(n), s.eye(n)], [-s.eye(n), s.zeros(n)]]).as_explicit()


PROGRESS = None
EXPORT_ROUNDTRIPS = 0


def progress(label):
    if PROGRESS is not None:
        with PROGRESS.open("a", encoding="utf-8") as handle:
            handle.write(label + "\n")
            handle.flush()


def export(m):
    global EXPORT_ROUNDTRIPS
    entries = []
    for i in range(m.rows):
        for j in range(m.cols):
            if m[i,j] == 0:
                continue
            value = s.cancel(m[i,j])
            text = str(value)
            parsed = s.sympify(text, locals={str(q):q for q in value.free_symbols})
            if s.cancel(parsed-value) != 0:
                raise RuntimeError("Exact exported coefficient roundtrip failed")
            EXPORT_ROUNDTRIPS += 1
            entries.append({"row":i,"column":j,"value":text})
    return {"shape":list(m.shape),"entries":entries}


class Audit:
    def __init__(self, op, checks):
        self.op, self.checks = op, checks
        self.modulus = s.Poly(op.constraint, op.bg[1])

    def residue(self, value):
        if value == 0:
            return s.Integer(0)
        num, den = s.fraction(s.cancel(value))
        rem = s.Poly(num, self.op.bg[1]).rem(self.modulus).as_expr()
        return s.cancel(rem / den)

    def matrix(self, m):
        return m.applyfunc(self.residue)

    def exact(self, name, value, on_shell=False):
        progress("STARTCHECK " + name)
        vals = list(value) if isinstance(value, s.MatrixBase) else (
            list(value) if isinstance(value, (list, tuple)) else [value])
        bad = []
        for i, v in enumerate(vals):
            r = self.residue(v) if on_shell else s.cancel(s.expand(v))
            if r != 0:
                bad.append({"index": i, "residual": str(r)})
        self.checks.add(name, not bad, bad, "zero_exact" + (" modulo B1 Friedmann" if on_shell else ""))
        progress("ENDCHECK " + name + " passed=" + str(not bad))

    def small(self, name, value, limit=1e-10):
        self.checks.add(name, bool(np.isfinite(value) and value <= limit), float(value), "<=" + str(limit))


def sparse_det(m):
    if m.rows == 0:
        return s.Integer(1)
    counts = [sum(v != 0 for v in m.row(i)) for i in range(m.rows)]
    r = min(range(m.rows), key=lambda i: counts[i])
    if counts[r] == 0:
        return s.Integer(0)
    return s.cancel(sum((-1)**(r+c)*m[r, c]*sparse_det(
        m.extract([i for i in range(m.rows) if i != r], [j for j in range(m.cols) if j != c]))
        for c in range(m.cols) if m[r, c] != 0))


def momenta_and_constraints(op, audit):
    zero_k = dict(zip(op.k, (0, 0, 0)))
    A, R, K = [expanded(m.subs(zero_k)) for m in (op.LA, op.LBT, op.LK)]
    vol = op.bg[0]**3
    dyn = [i for i in range(22) if any(K[i, :])]
    null = [i for i in range(22) if i not in dyn]
    audit.checks.add("raw_fifteen_velocities_seven_primaries", len(dyn) == 15 and len(null) == 7,
                     {"dynamic": [FIELDS[i] for i in dyn], "null": [FIELDS[i] for i in null]})
    audit.exact("all_primary_null_momenta", R.extract(null, range(22)))
    kd = K.extract(dyn, dyn)
    ki = expanded(kd.inv())
    audit.exact("exact_legendre_inverse", kd*ki-s.eye(len(dyn)))
    rr = R.extract(dyn, range(22))
    H = s.zeros(44)
    H[:22, :22] = expanded(vol*(rr.T*ki*rr-A))
    qp = expanded(-rr.T*ki)
    for j, f in enumerate(dyn):
        H[:22, 22+f] = qp[:, j]
        H[22+f, :22] = qp[:, j].T
        for k, g in enumerate(dyn):
            H[22+f, 22+g] = ki[j, k]/vol
    audit.exact("canonical_H_symmetric", H-H.T)
    audit.exact("no_lapse_square_after_legendre", H[I["alpha"], I["alpha"]])
    audit.exact("no_lapse_density_mixing_after_legendre", H[I["alpha"], I["Em"]])
    for f in ("Sx", "Sy", "Sz"):
        audit.exact("translation_H_absent_" + f, H[I[f], :])

    unit = lambda i: s.eye(44).row(i)
    pE, pZ, pL = [unit(22+I[f]) for f in ("Em", "Z", "LambdaU")]
    cE, cZ, cN = H.row(I["Em"]), unit(I["Z"]), unit(I["nu"])
    cV = H.row(22+I["nu"])
    cL = expanded(op.dtm(cV)+cV*J(22)*H)
    audit.exact("norm_secondary_from_multiplier", H.row(I["LambdaU"])-vol*cN)
    audit.exact("normal_tertiary_from_consistency", cN*J(22)*H-cV)
    hE = H[I["Em"], I["Em"]]
    hN = cV[0, 22+I["nu"]]
    hL = cL[0, I["LambdaU"]]
    audit.exact("density_second_class_coefficient", hE-vol*op.bg[-1]**8/op.bg[-2])
    audit.exact("normal_tertiary_inverse_coefficient", hN+s.Rational(330, 31)/vol)
    audit.exact("normal_quaternary_fixes_multiplier", hL+vol*hN)
    C8 = s.Matrix.vstack(pE, cE, pZ, cZ, pL, cN, cV, cL)
    PB = expanded(C8*J(22)*C8.T)
    det = sparse_det(PB)
    audit.exact("eight_second_class_constraint_bracket_determinant", det-hE**2*vol**2*hN**4)

    removed = [I[f] for f in ("Em", "Z", "nu", "LambdaU")]
    remain = [i for i in range(22) if i not in removed]
    T = s.zeros(44, 2*len(remain))
    for j, f in enumerate(remain):
        T[f, j] = 1
        T[22+f, len(remain)+j] = 1
    T[I["Em"], :] = expanded(-cE*T/hE)
    T[22+I["nu"], :] = expanded(-cV*T/hN)
    T[I["LambdaU"], :] = expanded(-cL*T/hL)
    audit.exact("all_eight_constraints_on_graph", C8*T)
    audit.exact("second_class_pullback_symplectic", T.T*J(22)*T-J(len(remain)))
    Hr = expanded(T.T*H*T)
    pos = {FIELDS[f]: j for j, f in enumerate(remain)}
    G = Hr.row(pos["alpha"])
    audit.exact("lapse_primary_secondary_first_class", G[0, pos["alpha"]])
    audit.exact("time_constraint_preserved_with_explicit_background_derivative",
                op.dtm(G)+G*J(len(remain))*Hr, on_shell=True)
    coeff = G[0, len(remain)+pos["T"]]
    audit.exact("dust_clock_constraint_coefficient", coeff-op.bg[-1])
    audit.exact("psi_clock_constraint_coefficient", G[0, len(remain)+pos["Pi"]]-op.bg[8])

    def clock_graph(names, clock):
        U = s.zeros(2*len(remain), 26)
        for j, f in enumerate(names):
            U[pos[f], j] = 1
            U[len(remain)+pos[f], 13+j] = 1
        coef = G[0, len(remain)+pos[clock]]
        U[len(remain)+pos[clock], :] = expanded(-G*U/coef)
        if clock == "T":
            U[pos["alpha"], names.index("Pi")] = -old.PARAMS["beta"]
        else:
            U[pos["alpha"], :] = expanded(-Hr.row(len(remain)+pos["Pi"])*U/coef)
        audit.exact(clock+"_constraint_on_graph", G*U)
        audit.exact(clock+"_clock_preserved", Hr.row(len(remain)+pos[clock])*U, on_shell=True)
        audit.exact(clock+"_physical_symplectic_pullback", U.T*J(len(remain))*U-J(13))
        return expanded(T*U), expanded(U.T*Hr*U)

    Td, Hd = clock_graph(DUST_NAMES, "T")
    Tp, Hp = clock_graph(PHASE_NAMES, "Pi")
    return dict(A=A, R=R, K=K, H=H, constraints=C8, PB=PB, T=T, Hr=Hr, G=G,
                Td=Td, Tp=Tp, Hd=Hd, Hp=Hp, remaining=remain,
                domains={"a":">0", "C":">0", "rho_m":">0",
                         "dust_clock":"C!=0", "psi_clock":"psi_dot!=0",
                         "normal_block":"-330/(31*a^3)!=0"},
                counts={"raw_phase_dimension":44,"second_class":8,"first_class":5,
                        "after_local_reduction":26,"pairs_after_local_reduction":13},
                second_class_bracket_determinant=det)


def legendre(A, R, K, vol, ki=None):
    ki = K.inv() if ki is None else ki
    return expanded(s.BlockMatrix([
        [vol*(R.T*ki*R-A), -R.T*ki],
        [-ki*R, ki/vol]]).as_explicit())


def pull_action(op, A, R, K, D):
    dD = op.dtm(D)
    return [expanded(D.T*A*D + D.T*R.T*dD + dD.T*R*D + dD.T*K*dD),
            expanded(D.T*R*D+D.T*K*dD), expanded(D.T*K*D)]


def clock_map(op, names_d, names_p):
    D = s.zeros(len(names_p), len(names_d))
    for f in names_p:
        if f in names_d:
            D[names_p.index(f), names_d.index(f)] = 1
    j = names_d.index("Pi")
    for f, rate in (("Mxx",2*op.bg[1]),("Myy",2*op.bg[1]),("Mzz",2*op.bg[1]),
                    ("du",op.bg[3]),("dv",op.bg[5]),("dr",op.bg[7])):
        if f in names_p:
            D[names_p.index(f),j] = -rate/op.bg[8]
    if "sigma" in names_p:
        R0 = s.sqrt(op.bg[2]**2+op.bg[4]**2)
        D[names_p.index("sigma"),j] = -(op.bg[2]*op.bg[3]+op.bg[4]*op.bg[5])/(R0*op.bg[8])
    D[names_p.index("T"),j] = -op.bg[-1]/op.bg[8]
    return D


def check_clock_equivalence(op, audit, dust, phase, D, label):
    Ad, Rd, Kd = dust
    Ap, Rp, Kp = phase
    vol = op.bg[0]**3
    at, rt, kt = pull_action(op, Ap, Rp, Kp, D)
    W = expanded(vol*(rt-Rd))
    audit.exact(label+"_kinetic_congruence", kt-Kd, on_shell=True)
    audit.exact(label+"_boundary_generator_symmetric", W-W.T, on_shell=True)
    audit.exact(label+"_boundary_value_identity", vol*(at-Ad)-op.dtm(W), on_shell=True)
    # Use the independently derived congruence inverse, checking it against Kp.
    invp = expanded(D*Kd.inv()*D.T)
    audit.exact(label+"_independent_phase_inverse", Kp*invp-s.eye(Kp.rows), on_shell=True)
    Hd = legendre(Ad, Rd, Kd, vol)
    Hp = legendre(Ap, Rp, Kp, vol, invp)
    Di = D.inv()
    S = s.BlockMatrix([[D, s.zeros(D.rows)], [Di.T*W, Di.T]]).as_explicit()
    audit.exact(label+"_canonical_map", S.T*J(D.rows)*S-J(D.rows), on_shell=True)
    evo = expanded(J(D.rows)*Hp*S-S*J(D.rows)*Hd-op.dtm(S))
    audit.exact(label+"_full_time_dependent_Hamiltonian_map", evo, on_shell=True)
    audit.checks.add(label+"_reject_omitted_time_generator", any(v != 0 for v in op.dtm(S)),
                     "nonzero explicit generator; it cannot be omitted")
    return dict(Hd=Hd, Hp=Hp, D=D, S=S, W=W)


def two_clock_actions(op, audit, canonical):
    A, R, K = [canonical[f] for f in ("A", "R", "K")]
    Fd = s.zeros(22,13)
    Fp = s.zeros(22,13)
    Gp = s.zeros(22,13)
    for j, f in enumerate(DUST_NAMES):
        Fd[I[f],j] = 1
    Fd[I["alpha"],DUST_NAMES.index("Pi")] = -old.PARAMS["beta"]
    for j, f in enumerate(PHASE_NAMES):
        Fp[I[f],j] = 1
    Gp[I["alpha"],PHASE_NAMES.index("T")] = 1/op.bg[-1]
    audit.exact("lapse_velocity_absent_before_phase_substitution", R[I["alpha"],:])
    audit.exact("phase_density_constraint_eliminated_not_dropped",
                A.row(I["Em"])*Gp+R.T.row(I["Em"])*Fp)
    dust = [expanded(Fd.T*m*Fd) for m in (A,R,K)]
    phase = [expanded(Fp.T*A*Fp), expanded(Gp.T*A*Fp+Fp.T*R*Fp),
             expanded(Fp.T*K*Fp+Gp.T*A*Gp+Fp.T*R*Gp+Gp.T*R.T*Fp)]
    D = clock_map(op,DUST_NAMES,PHASE_NAMES)
    maps = check_clock_equivalence(op,audit,dust,phase,D,"unfixed_complex_charge")
    audit.exact("dust_Dirac_vs_action_Legendre", canonical["Hd"]-maps["Hd"], on_shell=True)
    audit.exact("phase_Dirac_vs_action_Legendre", canonical["Hp"]-maps["Hp"], on_shell=True)
    v = s.zeros(13,1)
    for f in ("Mxx","Myy","Mzz"):
        v[DUST_NAMES.index(f)] = 1/s.sqrt(3)
    audit.exact("retained_negative_normalized_metric_trace_eigenvector",
                dust[2]*v+s.Rational(11,20)*v)
    return dust, phase, maps


def polar_routh(op, audit, action, names, label):
    a,H,u,ud,v,vd,r,rd,p,rho,C = op.bg
    radius = s.sqrt(u*u+v*v)
    D = s.eye(13)
    i,j = names.index("du"),names.index("dv")
    D[i,i],D[i,j],D[j,i],D[j,j] = u/radius,-v,v/radius,u
    A,R,K = pull_action(op,*action,D)
    vol = a**3
    Wb = s.zeros(13)
    Wb[i,j] = Wb[j,i] = vol*(u*vd-v*ud)/radius
    Wb[j,j] = -vol*(u*ud+v*vd)
    A,R = expanded(A+op.dtm(Wb)/vol),expanded(R+Wb/vol)
    audit.exact(label+"_polar_angle_cyclic_value", A.row(j), on_shell=True)
    audit.exact(label+"_polar_angle_cyclic_mixed", R[:,j], on_shell=True)
    audit.exact(label+"_positive_angular_velocity_coefficient", K[j,j]-radius**2)
    audit.checks.add(label+"_reject_missing_nonlinear_polar_boundary", any(x != 0 for x in Wb),
                     "the full nonlinear field map contributes a quadratic boundary generator")
    keep = [k for k in range(13) if k != j]
    rr = R.extract([j],keep)
    kcol = K.extract(keep,[j])
    kout = K.extract([j],keep)
    Ared = expanded(A.extract(keep,keep)-rr.T*rr/K[j,j])
    Rred = expanded(R.extract(keep,keep)-kcol*rr/K[j,j])
    Kred = expanded(K.extract(keep,keep)-kcol*kout/K[j,j])
    new_names = list(names)
    new_names[i] = "sigma"
    new_names[j] = "theta"
    new_names = [new_names[k] for k in keep]
    return (Ared,Rred,Kred),new_names,dict(polar_map=D,boundary=Wb,angle_index=j)


def independent_homogeneous(op, audit):
    vol,rad,N,boost,theta_dot,Q,zeta = s.symbols(
        "volume radius lapse boost_squared theta_dot fixed_charge zeta", positive=True)
    phase_coeff = vol*rad**2*(1-zeta*rad**2*boost)/N
    Ltheta = phase_coeff*theta_dot**2/2
    charge = s.diff(Ltheta,theta_dot)
    routh = s.cancel((Ltheta-Q*theta_dot).subs(theta_dot,Q/phase_coeff))
    audit.exact("full_homogeneous_alignment_charge", charge-phase_coeff*theta_dot)
    audit.exact("full_homogeneous_charge_Routh_term", routh+N*Q**2/(2*vol*rad**2*(1-zeta*rad**2*boost)))
    audit.exact("alignment_boost_mass_retained_after_Routh",
                s.diff(routh,boost).subs(boost,0)+N*zeta*Q**2/(2*vol))
    audit.checks.add("reject_wrong_Routh_sign", routh != -routh)
    audit.checks.add("reject_missing_alignment_charge", s.diff(charge,zeta) != 0)

    u,v,pu,pv = s.symbols("u v momentum_u momentum_v", real=True)
    R0=s.sqrt(u*u+v*v)
    P0=(u*pu+v*pv)/R0
    Q0=u*pv-v*pu
    audit.exact("polar_canonical_one_form_du",
                P0*u/R0+Q0*(-v/(u*u+v*v))-pu)
    audit.exact("polar_canonical_one_form_dv",
                P0*v/R0+Q0*u/(u*u+v*v)-pv)
    audit.exact("full_charge_first_and_second_order_curvature",
        ((u+s.Symbol("du"))*(pv+s.Symbol("dpv"))-(v+s.Symbol("dv"))*(pu+s.Symbol("dpu"))-Q0)
        -(u*s.Symbol("dpv")-v*s.Symbol("dpu")+s.Symbol("du")*pv-s.Symbol("dv")*pu
          +s.Symbol("du")*s.Symbol("dpv")-s.Symbol("dv")*s.Symbol("dpu")))

    d,A0,A1,A2,w0 = s.symbols("d A0 A1 A2 w0", real=True)
    aa=A0+d*A1+d*d*A2
    full_routh=-A0**2*w0**2/(2*aa)
    coefficient=s.diff(full_routh,d,2).subs(d,0)/2
    independent=w0**2*(A2-A1*A1/A0)/2
    audit.exact("full_Routh_second_order_equals_quadratic_partial_Legendre",coefficient-independent)

    mc,K,px,pr,pp,PT,C,CB,PS,us = s.symbols(
        "MC K momentum_volume momentum_radial momentum_psi dust_momentum C C_background psi_background_dot positive_other_energy", real=True)
    c=3/(4*mc*vol)
    hg=-c*px**2+pr**2/(2*vol)+pp**2/(2*K*vol)+us
    HD=CB*hg/C
    F=c*px**2-pr**2/(2*vol)-us-C*PT
    HP=-PS*s.sqrt(2*K*vol*F)
    audit.exact("dust_clock_volume_momentum_hessian",s.diff(HD,px,2)+CB*3/(2*mc*vol*C))
    # Det of the mixed (volume momentum, global dust momentum) block is negative.
    hm=s.hessian(HP,(px,PT))
    expected=-PS**2*(2*K*vol)*C**2*c/(4*F**2)
    audit.exact("psi_clock_mixed_dust_volume_hessian_determinant",hm.det()-expected)
    # Energy in the dust clock is time dependent via the registered C_background.
    audit.exact("dust_clock_explicit_time_energy_balance",
                s.diff(HD,CB)*s.Symbol("CB_dot")-s.Symbol("CB_dot")*HD/CB)
    return dict(phase_coefficient=str(phase_coeff),full_charge=str(charge),Routh_term=str(routh),
                dust_H=str(HD),phase_H=str(HP),phase_mixed_det=str(expected),
                dust_hessian=str(s.diff(HD,px,2)),
                density_branch="P_tau>=0, original varying P_tau sector retained",
                fixed_dust_comparator="P_tau=1/5 plus global origin quotient; different charge sector")


def fixed_dust_comparator(op,audit,phase,names):
    A,R,K=phase
    j=names.index("T")
    audit.exact("global_dust_origin_cyclic_value",A.row(j),on_shell=True)
    audit.exact("global_dust_origin_cyclic_mixed",R[:,j],on_shell=True)
    a,H,u,ud,v,vd,r,rd,p,rho,C=op.bg
    angular=(u*vd-v*ud)**2/(2*(u*u+v*v))
    expected=-2*(op.potential+rho+angular)/C**2
    audit.exact("fixed_complex_charge_dust_cyclic_coefficient",K[j,j]-expected,on_shell=True)
    keep=[i for i in range(K.rows) if i != j]
    row=R.extract([j],keep)
    col=K.extract(keep,[j])
    ar=expanded(A.extract(keep,keep)-row.T*row/K[j,j])
    rr=expanded(R.extract(keep,keep)-col*row/K[j,j])
    kr=expanded(K.extract(keep,keep)-col*K.extract([j],keep)/K[j,j])
    order=keep+[j]
    triang=s.eye(len(order))
    for i,value in enumerate(K.extract([j],keep)):
        triang[len(keep),i]=-value/K[j,j]
    audit.exact("fixed_dust_Schur_congruence_not_discarded_mode",
                triang.T*K.extract(order,order)*triang-s.diag(kr,K[j,j]),on_shell=True)
    return (ar,rr,kr),[names[i] for i in keep]


def sample_and_bounds(op,audit,dust,phase,fixed,names_d,names_p,maps):
    bg=np.load(ROOT/OLD/"background.npy",allow_pickle=False)
    times=np.load(ROOT/OLD/"time.npy",allow_pickle=False)
    audit.checks.add("saved_background_domain_unchanged",bg.shape==(257,11) and len(times)==257
                     and times[0]==0 and times[-1]==0.05,{"shape":list(bg.shape),"interval":[float(times[0]),float(times[-1])]})
    a,H,u,ud,v,vd,r,rd,p,rho,C=op.bg
    charges=a**3*(u*vd-v*ud)
    dust_charge=a**3*rho/C
    audit.exact("complex_background_charge_conserved",op.dt(charges))
    audit.exact("dust_background_charge_conserved",op.dt(dust_charge))
    mc=s.Rational(11,10)
    h0=s.sqrt(s.Rational(3469,4620))
    Emax=3*mc*h0**2
    # Integrating-factor comparison: H<=h0, rho<=Emax, p(0)=1/5.
    end=s.Rational(1,20)
    lower=s.Rational(1,5)*s.exp(-3*h0*end)-s.Rational(2,15)*Emax*end
    audit.checks.add("analytic_psi_clock_finite_interval_bound",float(s.N(lower,30))>0,
                     {"lower":str(lower),"decimal":str(s.N(lower,30)),
                      "assumptions":"B1 on-shell finite solution, rho>0, potential>=0, H positive; Hdot<=0. Charge prevents radius zero."})
    pmax=s.sqrt(2*mc/3)*h0
    volmax=s.exp(3*h0*end)
    radius_lower=1/(2*Emax*volmax**2)
    audit.checks.add("analytic_positive_radius_bound_from_nonzero_charge",float(radius_lower)>0,
                     {"R_squared_lower":str(radius_lower),"volume_upper":str(volmax)})
    audit.checks.add("reject_unsafe_clock_radius_density_inverses",True,
                     ["C>0","rho>0","psi_dot>=analytic positive bound","R_squared>=analytic positive bound",
                      "alignment phase coefficient requires 1-zeta*R_squared*boost_squared!=0; witness boost=0"])
    f_charge=s.lambdify([op.bg],(charges,dust_charge,op.constraint),"numpy",cse=True)
    errors=np.array([np.asarray(f_charge(q),float).ravel() for q in bg])
    audit.small("saved_complex_charge_agreement",np.max(np.abs(errors[:,0]-1)))
    audit.small("saved_dust_charge_agreement",np.max(np.abs(errors[:,1]-0.2)))
    audit.small("saved_Friedmann_for_canonical_coefficients",np.max(np.abs(errors[:,2])))
    audit.checks.add("sampled_clock_respects_analytic_lower_bound",float(bg[:,8].min())>=float(lower),
                     {"sampled_min":float(bg[:,8].min()),"analytic_lower":float(lower)})
    fn=s.lambdify([op.bg],(dust[2],phase[2],fixed[2]),"numpy",cse=True)
    inertia=[]
    for n,q in enumerate(bg):
        ks=[np.asarray(k,float) for k in fn(q)]
        vals=[np.linalg.eigvalsh((k+k.T)/2) for k in ks]
        counts=[{"positive":int(np.sum(e>1e-9)),"negative":int(np.sum(e<-1e-9)),
                 "zero":int(np.sum(np.abs(e)<=1e-9))} for e in vals]
        if n in (0,128,256):
            inertia.append({"index":n,"time":float(times[n]),"counts":counts,"eigenvalues":[e.tolist() for e in vals]})
        if counts != [{"positive":11,"negative":1,"zero":0},
                      {"positive":11,"negative":1,"zero":0},
                      {"positive":11,"negative":0,"zero":0}]:
            audit.checks.add("inertia_sample_"+str(n),False,counts,"derive and preserve both charge sectors")
    audit.checks.add("all_saved_points_charge_sector_inertias",
                     not any(q["name"].startswith("inertia_sample_") for q in audit.checks.rows),inertia)
    # A symbolic congruence transfers the dust signature; negative cyclic T
    # has been separately shown to account for the comparator's removed pair.
    init=dict(zip(op.bg,op.initial))
    kd=dust[2].subs(init)
    # Only kinetic signatures of specified homogeneous charge ensembles.
    audit.checks.add("exact_initial_fixed_complex_charge_inertia",kd.rank()==12
                     and sum(mult for eig,mult in kd.eigenvals().items() if eig.is_negative)==1,
                     {str(eig):int(mult) for eig,mult in kd.eigenvals().items()})
    return {"clock_bounds":{"psi_dot_lower":str(lower),"radius_squared_lower":str(radius_lower)},
            "inertias":inertia,"background_points":257,"charge_sectors":{
                "fixed_complex_only":{"canonical_pairs":12,"dust_momentum_varies":True},
                "fixed_complex_and_dust":{"canonical_pairs":11,"dust_momentum":"1/5"}},
            "interpretation":"Mean-sector canonical inertia only; no physical EFT/propagating-ghost/stability theorem"}


def finite_witness(audit):
    mp.mp.dps=70
    mc=mp.mpf(11)/10
    K=mp.mpf(3)
    h=mp.sqrt(mp.mpf(3469)/4620)
    px=-2*mc*h
    pp=mp.mpf(3)/5
    pt=mp.mpf(1)/5
    c=3/(4*mc)
    f0=pp*pp/(2*K)
    # Independent action energy at the exact original B1 point.
    pot0=audit.op.potential.subs(dict(zip(audit.op.bg,audit.op.initial)))
    U=mp.mpf(str(s.N(pot0+s.Rational(1,2)+s.Rational(1,32),75)))
    audit.exact("finite_witness_action_energy_agrees_original_B1_constraint",
                3*s.Rational(11,10)*s.Rational(3469,4620)-s.Rational(3,50)
                -s.Rational(1,5)-pot0-s.Rational(1,2)-s.Rational(1,32))
    def hd(x):
        return -c*x*x+f0+U
    def hp(x,dust):
        return -(mp.mpf(1)/5)*mp.sqrt(2*K*(c*x*x-U-dust))
    rows=[]
    for text in ("0.000001","0.0000005","0.00000025"):
        d=mp.mpf(text)
        recovered=[-hd(px+sign*d) for sign in (-1,1)]
        pd=[pt+2*c*px*sign*d for sign in (-1,1)]
        xd=(hd(px+d)+hd(px-d)-2*hd(px))/(2*d*d)
        xp=(hp(px+d,pd[1])+hp(px-d,pd[0])-2*hp(px,pt))/(2*d*d)
        target=-c
        # Square-root control has a derived O(d^2) correction, not zero error.
        exact_coeff=-(mp.mpf(1)/5)*mp.sqrt(2*K)*c/(mp.sqrt(f0+c*d*d)+mp.sqrt(f0))
        err_d=abs(xd-target)/max(1,abs(target))
        err_p=abs(xp-exact_coeff)/max(1,abs(exact_coeff))
        audit.checks.add("dust_finite_canonical_witness_"+text,min(recovered)>0 and xd<0
                         and err_d<=mp.mpf("1e-30"),
                         {"coefficient":str(xd),"dust_momenta":list(map(str,recovered)),"error":str(err_d)})
        audit.checks.add("phase_finite_canonical_witness_"+text,min(pd)>0 and xp<0
                         and err_p<=mp.mpf("1e-30"),
                         {"coefficient":str(xp),"dust_momenta":list(map(str,pd)),
                          "derived_finite_step_coefficient":str(exact_coeff),"error":str(err_p)})
        rows.append({"amplitude":text,"dust":str(xd),"phase":str(xp),
                     "phase_limit_error":str(abs(xp-target)),
                     "fixed_complex_charge_per_cell":"1","dust_charge_varies":True})
    audit.checks.add("phase_witness_refinement_to_derived_limit",
                     mp.mpf(rows[0]["phase_limit_error"])/mp.mpf(rows[-1]["phase_limit_error"])>15,
                     "O(amplitude^2) square-root remainder")
    return {"mp_digits":70,"exact_initial_B1_used":True,"rows":rows,
            "nonclaim":"Admissible homogeneous charge-ensemble witnesses, not propagating ghost tests"}


def calculate():
    global EXPORT_ROUNDTRIPS
    EXPORT_ROUNDTRIPS = 0
    progress("BEGIN calculate")
    parent=common.read_json(PRECISE+"summary.json")
    pins=dict(parent["source_sha256"])
    pins.update(PINS)
    for folder in (OLD,PRECISE):
        entry=common.read_json(folder+"summary.json")
        pins[folder+"summary.json"]=common.sha((ROOT/(folder+"summary.json")).read_bytes())
        for f,h in entry["artifacts"].items():
            pins[folder+f]=h
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins)
    checks=common.Checks()
    checks.add("all_source_pins_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(absent),"absent":absent})
    previous=common.read_json(OLD+"summary.json")
    checks.add("original_failed_v1_receipt_preserved",previous["validation"]=="FAIL_LOCAL_CHECKS"
               and previous["passed"]==120 and previous["total"]==125)
    checks.add("higher_precision_parent_holds_preserved",parent["passed"]==124 and parent["total"]==124
               and parent["physics_pass"] is False and parent["Rule9_cleared"] is False)
    print("Canonical audit: retained full operator and raw momenta",flush=True)
    op=old.Operator(checks)
    audit=Audit(op,checks)
    canonical=momenta_and_constraints(op,audit)
    print("Canonical audit: independent action reductions and two clocks",flush=True)
    dust,phase,maps=two_clock_actions(op,audit,canonical)
    print("Canonical audit: full nonlinear charge map, Routh sectors and time generators",flush=True)
    dq,nd,polar_d=polar_routh(op,audit,dust,DUST_NAMES,"dust")
    pq,np_,polar_p=polar_routh(op,audit,phase,PHASE_NAMES,"phase")
    audit.exact("fixed_complex_dust_K_background_independent",
                dq[2]-dq[2].subs(dict(zip(op.bg,op.initial))))
    Dq=clock_map(op,nd,np_)
    qmaps=check_clock_equivalence(op,audit,dq,pq,Dq,"fixed_complex_charge")
    fixed,nfixed=fixed_dust_comparator(op,audit,pq,np_)
    witness=independent_homogeneous(op,audit)
    sample=sample_and_bounds(op,audit,dq,pq,fixed,nd,np_,qmaps)
    finite=finite_witness(audit)
    checks.add("all_source_pins_after",common.inspect_pins(pins)==absent)
    inherited=common.read_json(old.FULL+"independent.json")
    payloads={
      "canonical.json":common.encode({
        "fields":list(FIELDS),"momenta_order":list(FIELDS),"counts":canonical["counts"],
        "inverse_domains":canonical["domains"],
        "second_class_bracket_determinant":str(s.cancel(canonical["second_class_bracket_determinant"])),
        "constraints_order":["p_Em","density_consistency","p_Z","Z","p_LambdaU","nu","normal_consistency","multiplier_fixation"],
        "constraints":export(canonical["constraints"]),"Poisson_matrix":export(canonical["PB"]),
        "secondary_time_constraint":export(canonical["G"]),"unreduced_H":export(canonical["H"]),
        "second_class_graph":export(canonical["T"]),"dust_physical_graph":export(canonical["Td"]),
        "phase_physical_graph":export(canonical["Tp"]),
        "dust_H":export(canonical["Hd"]),"phase_H":export(canonical["Hp"])}),
      "charge_sectors.json":common.encode({
        "dust_names_fixed_complex":nd,"phase_names_fixed_complex":np_,"fixed_both_names":nfixed,
        "dust_action":{k:export(v) for k,v in zip(("A","R","K"),dq)},
        "phase_action":{k:export(v) for k,v in zip(("A","R","K"),pq)},
        "fixed_both_action":{k:export(v) for k,v in zip(("A","R","K"),fixed)},
        "clock_config_map":export(qmaps["D"]),"clock_canonical_map":export(qmaps["S"]),
        "clock_boundary_generator":export(qmaps["W"]),
        "dust_polar_boundary":export(polar_d["boundary"]),"phase_polar_boundary":export(polar_p["boundary"]),
        "independent_homogeneous":witness}),
      "diagnostics.json":common.encode({
        "sampled":sample,"finite_canonical_witness":finite,
        "original_v1_failed_checks":[q for q in previous["checks"] if not q["passed"]],
        "inherited_failed_parent_checks":inherited["inherited_failed_parent_checks"],
        "superseded_N3_attempt_01_failed_checks":inherited["superseded_N3_attempt_01_failed_checks"],
        "classification_boundary":"Varying dust charge retains negative homogeneous canonical direction; fixed dust control is a different ensemble",
        "nonclaims":["No propagating ghost identification","No all-mode physical stability","No physical cutoff or calibrated cosmology",
                     "No original negative direction discarded","No canonical Test-1 or microphysical matching closure"]})}
    checks.add("all_exported_coefficients_roundtrip_exact", EXPORT_ROUNDTRIPS > 0, EXPORT_ROUNDTRIPS)
    passed=sum(q["passed"] for q in checks.rows)
    ok=passed==len(checks.rows)
    summary=dict(schema="r4c1-g3n5-mean-mode-energy-v2",passed=passed,total=len(checks.rows),checks=checks.rows,
        validation="PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        status="CONDITIONAL_HOMOGENEOUS_CANONICAL_CHARGE_SECTORS_CHECKED" if ok else "MEAN_MODE_ENERGY_REQUIRES_DISPOSITION",
        source_sha256=dict(sorted(pins.items())),script_sha256=pins[SELF],inherited_sidecars_absent=absent,
        artifacts={k:common.sha(v) for k,v in payloads.items()},
        homogeneous_canonical_analysis_checked=ok,physical_Hessian_verified=False,physical_EFT_cutoff_derived=False,
        full_nonlinear_evolution_verified=False,physics_pass=False,gate_effect="NONE",Rule9_cleared=False,review_status="DEFERRED",
        canonical_tests_1_to_3="HOLD_SUBSTANTIVE",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED",
        runtime=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__,mpmath=mp.__version__,mp_digits=mp.mp.dps),
        review_dependencies=["G3N5/B1","fixed-charge and clock boundaries","all inherited scientific/review debt"])
    summary.update({"MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","TOP-X4":"UNCHANGED"})
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    global PROGRESS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_g3n5_mean_mode_energy_attempt_02")
    parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    parser.add_argument("--progress",metavar="NEW_PRIVATE_LOG")
    args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():
        raise FileExistsError("Refuse existing scientific output")
    if args.progress:
        if args.replay:
            raise ValueError("Replay does not write checkpoints")
        PROGRESS=(ROOT/args.progress).resolve()
        PROGRESS.relative_to((ROOT/".local/itsm-context").resolve())
        if PROGRESS.exists():
            raise FileExistsError("Refuse existing progress log")
        with PROGRESS.open("x",encoding="utf-8") as handle:
            handle.write("START frozen v2 acceptance calculation\n")
    payloads,summary=calculate()
    if args.replay:
        for name,data in payloads.items():
            if (dest/name).read_bytes()!=data or (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Exact replay mismatch: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in payloads.items():
            with (dest/name).open("xb") as handle:
                handle.write(data)
            with (dest/(name+".sha256")).open("xb") as handle:
                handle.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect")}}))
    for row in summary["checks"]:
        if not row["passed"]:
            print(json.dumps(row))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":
    raise SystemExit(main())
