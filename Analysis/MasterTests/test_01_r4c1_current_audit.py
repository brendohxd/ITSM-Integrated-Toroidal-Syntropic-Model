"""R4C1-v1 first variational checkpoint; NOT a complete Test-1 physics pass.

Exact SymPy local jets, with independent directional metric variations and
curved-background regulator controls. No cosmological fit or provider calls.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md"
FROZEN_SHA = "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3"
OUT = ROOT / "Analysis/MasterTests/outputs/test_01_r4c1_current_summary.json"
SOURCE_SHA = {
    "Theory/Gates/UVIR-001/UVIR-001_GATE_REPORT.md":
        "850d4e6616a136088936bbdbbb809f0443b508117cbe0140ebb05eca79aaf630",
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_A_REPORT.md":
        "f73004c07e031672669d5cb3f098fadcd487cc6ab21ea30546e951ad1ee7033b",
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md":
        "c2a5c82f285dc04adcfffed4ba5c562661ddca98c4d045802ffb6e88bfeefd68",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self):
        self.checks = []
        self.expressions = {}

    def equal(self, name, expression):
        value = s.simplify(s.expand(expression))
        self.checks.append({"name": name, "passed": value == 0,
                            "expected": "zero", "residual": str(value)})

    def reject(self, name, expression):
        value = s.simplify(s.expand(expression))
        variables = sorted(value.free_symbols, key=str)
        witness = {}
        result = value
        # An exact nonzero witness, not 'simplify did not return zero'.
        for offset in range(1, 5):
            witness = {v: s.Integer((i + offset) % 5 + 1)
                       for i, v in enumerate(variables)}
            result = s.simplify(value.subs(witness))
            if result.is_zero is False:
                break
        self.checks.append({"name": name, "passed": result.is_zero is False,
                            "expected": "exact_nonzero_witness",
                            "residual": str(value), "witness_result": str(result),
                            "witness": {str(k): str(v) for k, v in witness.items()}})


def scalar_currents(a):
    u, v, r, psi, tau, eps = fields = s.symbols("u v r psi tau epsilon", real=True)
    beta, zeta, gr, eta = s.symbols("beta zeta g_r eta", real=True)
    m2, l4, l6, cutoff, mr2, lr = s.symbols("m2 lambda4 lambda6 Lambda mr2 lambda_r", positive=True)
    metric = s.diag(-1, 1, 1, 1)
    grad = {f: s.Matrix(s.symbols(f"d_{f}_0:4", real=True)) for f in fields}
    hess = {f: s.Matrix(4, 4, lambda i, j: s.Symbol(f"H_{f}_{min(i,j)}{max(i,j)}", real=True))
            for f in fields}
    h = s.Matrix(4, 4, lambda i, j: s.Symbol(f"h{min(i,j)}{max(i,j)}", real=True))
    hvars = sorted(set(h), key=str)
    # h derivatives retained: the charge identity is not a constant-frame-only test.
    dh = {f: s.symbols(f"d_{f}_0:4", real=True) for f in hvars}

    def d(expr, mu):
        return s.expand(sum(s.diff(expr, f) * grad[f][mu] + sum(
            s.diff(expr, grad[f][i]) * hess[f][i, mu] for i in range(4)) for f in fields)
            + sum(s.diff(expr, f) * dh[f][mu] for f in hvars))

    def div(vec):
        return sum(d(vec[i], i) for i in range(4))

    def dot(f, g):
        return (grad[f].T * metric * grad[g])[0]

    def box(f):
        return s.trace(metric * hess[f])

    def el(L, f):
        return s.diff(L, f) - div(s.Matrix([s.diff(L, p) for p in grad[f]]))

    radius2 = u*u + v*v
    VP = m2*radius2/2 + l4*radius2**2/8 + l6*radius2**3/(24*cutoff**2)
    VR = mr2*r*r/2 + lr*r**4/4
    W = gr*radius2*r*r/4
    Jlow = v*grad[u] - u*grad[v]
    Cvec = h*Jlow
    La = -zeta*(Jlow.T*h*Jlow)[0]/2
    Lphi = -(dot(u, u)+dot(v, v))/2 - VP - W + La
    pu = s.Matrix([s.diff(Lphi, p) for p in grad[u]])
    pv = s.Matrix([s.diff(Lphi, p) for p in grad[v]])
    fullj = -v*pu + u*pv
    expectedj = metric*Jlow + zeta*radius2*Cvec
    for mu in range(4):
        a.equal(f"full_U1_current_component_{mu}", fullj[mu]-expectedj[mu])
        a.equal(f"u_momentum_{mu}", pu[mu]+(metric*grad[u])[mu]+zeta*v*Cvec[mu])
        a.equal(f"v_momentum_{mu}", pv[mu]+(metric*grad[v])[mu]-zeta*u*Cvec[mu])
    Eu, Ev = el(Lphi, u), el(Lphi, v)
    a.equal("u_EL_including_alignment", Eu - (box(u)-s.diff(VP+W, u)
            + zeta*(2*(Cvec.T*grad[v])[0]+v*div(Cvec))))
    a.equal("v_EL_including_alignment", Ev - (box(v)-s.diff(VP+W, v)
            - zeta*(2*(Cvec.T*grad[u])[0]+u*div(Cvec))))
    a.equal("inhomogeneous_frame_U1_Ward", div(fullj)-v*Eu+u*Ev)
    a.equal("portal_U1_invariance", -v*s.diff(W,u)+u*s.diff(W,v))
    # A physical rest-frame projector supplies a concrete rejection domain.
    rest = {h[i,j]: int(i == j and i > 0) for i in range(4) for j in range(i,4)}
    rest.update({q: 0 for value in dh.values() for q in value})
    missingj = (div(metric*Jlow)-v*Eu+u*Ev).subs(rest)
    a.reject("bare_J_charge_law_rejected", missingj)
    a.reject("wrong_alignment_current_sign_rejected",
             (div(metric*Jlow-zeta*radius2*Cvec)-v*Eu+u*Ev).subs(rest))
    # Condensate-on-shell jet at x=1 for spatial profiles u=x, v=x^2.
    # Solve the two time accelerations from Eu=Ev=0, rather than claiming
    # those static profiles themselves solve the equations. Frame/metric
    # equations are not solved by this local subsystem counterexample.
    time_acc = {hess[u][0,0]:s.expand(Eu+hess[u][0,0]).subs(rest),
                hess[v][0,0]:s.expand(Ev+hess[v][0,0]).subs(rest)}
    jet = {q:0 for f in fields for q in grad[f]}
    jet.update({q:0 for f in fields for q in set(hess[f])})
    jet.update({u:1,v:1,grad[u][1]:1,grad[v][1]:2,hess[v][1,1]:2})
    a.equal("on_scalar_shell_u_equation",Eu.subs(rest).subs(time_acc).subs(jet))
    a.equal("on_scalar_shell_v_equation",Ev.subs(rest).subs(time_acc).subs(jet))
    a.equal("on_scalar_shell_full_charge_jet",div(fullj).subs(rest).subs(time_acc).subs(jet))
    a.equal("on_scalar_shell_bare_charge_defect",div(metric*Jlow).subs(time_acc).subs(jet)-10*zeta)
    a.equal("charge_regular_at_amplitude_zero",
            sum(c.subs({u:0,v:0})**2 for c in fullj))

    conf = s.exp(beta*psi)
    Lm = -eps*(conf**2*dot(tau,tau)+conf**4)/2
    Tm = eps*conf**2*(metric*grad[tau])*(metric*grad[tau]).T + metric*Lm
    trace = s.trace(metric*Tm)
    Etau, Eeps = el(Lm,tau), s.diff(Lm,eps)
    a.equal("dust_EL", Etau-div(eps*conf**2*metric*grad[tau]))
    a.equal("dust_multiplier_constraint", Eeps+(conf**2*dot(tau,tau)+conf**4)/2)
    a.equal("matter_trace_variation", s.diff(Lm,psi)-beta*trace)
    a.reject("wrong_matter_source_sign_rejected", s.diff(Lm,psi)+beta*trace)
    a.equal("dust_trace_on_constraint", s.expand(trace).subs(
        grad[tau][0]**2, conf**2+sum(grad[tau][i]**2 for i in range(1,4)))+eps*conf**4)

    LR = -dot(r,r)/2-VR
    TR = (metric*grad[r])*(metric*grad[r]).T+metric*LR
    Er = el(LR-W,r)
    a.equal("reservoir_EL", Er-box(r)+s.diff(VR+W,r))
    Qmp = beta*trace*metric*grad[psi]
    Qsyn = -s.diff(W,r)*metric*grad[r]
    for nu in range(4):
        divm = sum(d(Tm[mu,nu],mu) for mu in range(4))
        divr = sum(d(TR[mu,nu],mu) for mu in range(4))
        a.equal(f"matter_Ward_with_multiplier_{nu}",
                divm-Etau*(metric*grad[tau])[nu]-Eeps*(metric*grad[eps])[nu]-Qmp[nu])
        a.equal(f"reservoir_Ward_{nu}", divr-Er*(metric*grad[r])[nu]+Qsyn[nu])
        a.equal(f"portal_reallocation_{nu}",
                sum(d((TR-eta*metric*W)[mu,nu]-TR[mu,nu],mu) for mu in range(4))
                +eta*metric[nu,nu]*d(W,nu))
        a.equal(f"Qsyn_zero_branch_limit_{nu}", s.limit(Qsyn[nu],gr,0)-Qsyn[nu].subs(gr,0))
        a.equal(f"Qmp_zero_branch_limit_{nu}", s.limit(Qmp[nu],beta,0)-Qmp[nu].subs(beta,0))
        a.equal(f"Qsyn_regular_at_zero_charge_{nu}", Qsyn[nu].subs({u:0,v:0}))
    a.reject("wrong_reservoir_source_sign_rejected",
             sum(d(TR[mu,0],mu) for mu in range(4))-Er*(metric*grad[r])[0]-Qsyn[0])
    # Nonzero transfer at a finite exact field jet: charge symmetry still exact.
    a.equal("nonzero_energy_exchange_witness", Qsyn[0].subs(
        {u:1,v:0,r:1,gr:2,grad[r][0]:3})-3)
    a.expressions.update({"j_full": "J^mu + zeta (u^2+v^2) h^{mu nu} J_nu",
        "Q_mp": "beta T_m grad^nu psi", "Q_syn": "-g_r (u^2+v^2) r grad^nu r / 2",
        "S_N": "0 for the full Noether charge; not an irreversible source",
        "Q_syn_reassigned": "Q_syn + eta grad^nu W",
        "bare_J_rejection_residual": str(s.factor(missingj))})


def metric_blocks(a):
    """Direct inverse-metric variations, fixed contravariant U, boosted frame.

    This checks algebraic alignment and Q/Y stresses, NOT the connection-
    dependent U/regulator stress or a physical metric/constraint Hessian.
    """
    eta = s.diag(-1,1,1,1)
    U = s.Matrix([s.Rational(5,3),s.Rational(4,3),0,0])
    J = s.Matrix(s.symbols("j0:4", real=True))
    p = s.Matrix([2,3,5,7])
    zeta, K, A = s.symbols("zeta K A", positive=True)
    q = s.Symbol("metric_perturbation", real=True)
    nlow = eta*U
    h0 = eta+U*U.T
    a.equal("unit_frame", (U.T*eta*U)[0]+1)
    a.equal("projector_annihilates_frame", sum(v*v for v in h0*nlow))
    a.equal("projector_idempotent", sum(v*v for v in h0*eta*h0-h0))
    Jn = (U.T*J)[0]
    Q = (U.T*p)[0]
    Y = (p.T*h0*p)[0]
    La0 = -zeta*(J.T*h0*J)[0]/2
    Lf0 = K*Q**2/2-A*Y**s.Rational(3,2)
    Ta = zeta*(J*J.T-Jn**2*nlow*nlow.T)+eta*La0
    Tf = K*Q**2*nlow*nlow.T+3*A*s.sqrt(Y)*(p*p.T-Q**2*nlow*nlow.T)+eta*Lf0
    for i in range(4):
        for j in range(i,4):
            D = s.zeros(4)
            D[i,j] = D[j,i] = 1
            inv = eta+q*D
            cov = inv.inv()
            ell2 = -(U.T*cov*U)[0]
            h = inv+U*U.T/ell2
            La = -zeta*(J.T*h*J)[0]/2
            q2 = (U.T*p)[0]**2/ell2
            yf = (p.T*h*p)[0]
            Lf = K*q2/2-A*yf**s.Rational(3,2)
            metric_trace = s.trace(eta*D)
            a.equal(f"alignment_metric_direction_{i}{j}",
                    -2*s.diff(La,q).subs(q,0)+metric_trace*La0-s.trace(Ta*D))
            a.equal(f"force_QY_metric_direction_{i}{j}",
                    -2*s.diff(Lf,q).subs(q,0)+metric_trace*Lf0-s.trace(Tf*D))
    a.reject("ignoring_normalization_in_alignment_stress_rejected", -zeta*Jn**2*nlow[0]**2)


def regulator_controls(a):
    # Differentiate the frozen first-order force action before eliminating z.
    # Background n,h,a may vary; no constant-frame simplification is used in
    # these momentum/auxiliary identities. Their derivatives enter div(Pi).
    pn = s.Matrix(s.symbols("n0:4", real=True))
    pg = s.Matrix(s.symbols("dpsi0:4", real=True))
    zg = s.Matrix(s.symbols("dz0:4", real=True))
    av = s.Matrix(s.symbols("acc0:4", real=True))
    hp = s.Matrix(4,4,lambda i,j:s.Symbol(f"hp{min(i,j)}{max(i,j)}", real=True))
    Kp, Ap, bp, zp = s.symbols("Kp Ap bp zp", positive=True)
    qp = (pn.T*pg)[0]
    yp = (pg.T*hp*pg)[0]
    Lp = Kp*qp**2/2-Ap*yp**s.Rational(3,2)+bp*zp**2/2
    Lp -= bp*(zg.T*hp*pg)[0]+bp*zp*(av.T*pg)[0]
    expected_pi = Kp*qp*pn-3*Ap*s.sqrt(yp)*hp*pg-bp*hp*zg-bp*zp*av
    for mu in range(4):
        a.equal(f"force_momentum_{mu}",s.diff(Lp,pg[mu])-expected_pi[mu])
        a.equal(f"auxiliary_momentum_{mu}",s.diff(Lp,zg[mu])+bp*(hp*pg)[mu])
    div_h_grad_psi = s.Symbol("div_h_grad_psi", real=True)
    Delta = div_h_grad_psi-(av.T*pg)[0]
    a.equal("auxiliary_EL_variable_frame",
            s.diff(Lp,zp)+bp*div_h_grad_psi-bp*(zp+Delta))
    scale, adot = s.symbols("a adot", positive=True)
    p = s.symbols("p0:4", real=True)
    hh = s.Matrix(4,4,lambda i,j:s.Symbol(f"psi{min(i,j)}{max(i,j)}"))
    g = s.diag(-1,scale**2,scale**2,scale**2)
    inv = g.inv()

    def dg(i,j,k):
        return s.diff(g[i,j],scale)*adot if k == 0 else 0

    christ = [[[sum(inv[l,k]*(dg(k,j,i)+dg(k,i,j)-dg(i,j,k))/2
                           for k in range(4)) for j in range(4)] for i in range(4)] for l in range(4)]
    n = s.Matrix([1,0,0,0])
    h = inv+n*n.T
    theta = sum(christ[mu][mu][0] for mu in range(4))
    projected_hessian = sum(h[i,j]*(hh[i,j]-sum(christ[k][i][j]*p[k] for k in range(4)))
                            for i in range(4) for j in range(4))
    leaf = sum(hh[i,i] for i in range(1,4))/scale**2
    a.equal("FRW_Delta_intrinsic_laplacian", projected_hessian+theta*p[0]-leaf)
    a.reject("FRW_omitted_theta_Q_rejected", projected_hessian-leaf)

    x = s.Symbol("x", real=True)
    N, f, z = [s.Function(name, positive=True)(x) for name in ("N","f","z")]
    acc = s.diff(N,x)/N
    divergence = s.diff(N*s.diff(f,x),x)/N
    a.equal("accelerated_lapse_Delta", divergence-acc*s.diff(f,x)-s.diff(f,x,2))
    # Formal adjoint under measure N dx, derived by two integrations by parts.
    adjoint = s.diff(N*z,x,2)/N
    conservative_adjoint = s.diff(N*(s.diff(z,x)+acc*z),x)/N
    a.equal("accelerated_lapse_formal_adjoint", adjoint-conservative_adjoint)
    kk = s.Symbol("kappa", positive=True)
    nonzero = (adjoint-s.diff(N*s.diff(z,x),x)/N).subs(
        {N:s.exp(kk*x),z:s.exp(x)}).doit().subs(x,0)
    a.reject("omitted_adjoint_acceleration_rejected", nonzero)
    b, Z, delta = s.symbols("b z Delta", real=True)
    integrated = b*Z**2/2+b*Z*delta
    a.equal("auxiliary_EL", s.diff(integrated,Z)-b*(Z+delta))
    a.equal("auxiliary_elimination_sign", integrated.subs(Z,-delta)+b*delta**2/2)
    a.reject("wrong_auxiliary_elimination_sign_rejected", integrated.subs(Z,delta)+b*delta**2/2)
    a.equal("auxiliary_b_zero_endpoint", integrated.subs(b,0))
    omega, wave, K = s.symbols("omega k K", positive=True)
    # E_psi=-K psi_tt-b psi_xxxx for a constant rest frame, no matter.
    a.equal("rest_frame_regulator_dispersion_sign",
            (K*omega**2-b*wave**4).subs(omega**2,b*wave**4/K))
    a.expressions["E_psi"] = "-div(K_Q Q n - 3 A sqrt(Y) h.dpsi) - b Delta_dagger Delta psi + beta T_m"
    a.expressions["Delta_dagger_z"] = "div(h.grad z + z a)"


def dimensions_and_gr(a):
    # Independent dimension ledger for every distinct action operator.
    dims = {"EH":2+2, "vacuum":4, "scalar_kinetic":2*(1+1), "mass_potential":2+2,
            "quartic":4, "sextic":6-2, "frame_two_derivative":2+2,
            "frame_constraint":4, "alignment":-2+2*(1+1+1),
            "Q_squared":2+2, "Y_three_halves":s.Rational(3,2)*2+1,
            "reg_z_squared":2*2, "reg_grad_z_grad_psi":3+1,
            "reg_z_a_grad_psi":2+1+1, "dust":4+2*(1-1),
            "reservoir_portal":2+2}
    for name,value in dims.items():
        a.equal(f"action_dimension_{name}",value-4)
    a.equal("matter_current_dimension",0+4+1-5)
    a.equal("reservoir_current_dimension",2+1+2-5)
    a.equal("Noether_current_dimension", -2+2+3-3)
    extra_kinetic = s.Symbol("r_dot", real=True)**2/2
    a.reject("zero_exchange_pure_GR_claim_rejected",extra_kinetic)
    # This coefficient-level endpoint is a degeneracy control, not a smooth
    # physical limit or an integration of a finite-density background.
    MU2,zeta,K,A,b,u,v,r = s.symbols("MU2 zeta K A b u v r")
    IU,IA,IQ,IY,IZ,V2,V4,V6,VR2,VR4 = s.symbols("IU IA IQ IY IZ V2 V4 V6 VR2 VR4")
    # Scalar gradient terms vanish on identically zero fields, not just a node.
    extra = MU2*IU+zeta*IA+K*IQ+A*IY+b*IZ+V2*(u*u+v*v)+V4*(u*u+v*v)**2
    extra += V6*(u*u+v*v)**3+VR2*r*r+VR4*r**4
    a.equal("algebraic_GR_extra_action_endpoint",extra.subs(
        {MU2:0,zeta:0,K:0,A:0,b:0,u:0,v:0,r:0}))


def main():
    a = Audit()
    # A changed frozen input is a provenance failure, not permission to
    # silently bless changed physics by recomputing hashes.
    pins = {str(FREEZE.relative_to(ROOT)).replace('\\','/'):FROZEN_SHA, **SOURCE_SHA}
    actual = {}
    for rel,expected in pins.items():
        actual[rel] = digest(ROOT/rel)
        if actual[rel] != expected:
            raise RuntimeError(f"FROZEN_INPUT_HASH_MISMATCH: {rel}")
    scalar_currents(a)
    metric_blocks(a)
    regulator_controls(a)
    dimensions_and_gr(a)
    passed = sum(c["passed"] for c in a.checks)
    record = {
        "candidate":"R4C1-v1", "validation":"PASS" if passed == len(a.checks) else "FAIL",
        "status":"CONDITIONAL_FIRST_VARIATION_CHECKPOINT_PARENT_HOLD",
        "passed":passed, "total":len(a.checks), "checks":a.checks,
        "expressions":a.expressions, "source_sha256":actual,
        "script_sha256":digest(Path(__file__)),
        "runtime":{"python":platform.python_version(),"sympy":s.__version__},
        "coverage":{"candidate_scalar_and_dust_currents":"exact symbolic local jets",
            "algebraic_metric_blocks":"10 independent metric directions at a boosted timelike frame",
            "regulator":"FRW and accelerated static lapse controls, not general principal-symbol proof",
            "GR":"algebraic endpoint only; no healthy continuous-limit proof"},
        "holds":["full U and connection-dependent regulator metric variation",
            "all-sector vector Ward identity and constraints",
            "finite-density on-shell background and stability",
            "healthy continuous GR recovery",
            "matter beyond irrotational pre-caustic dust",
            "microscopic or irreversible reservoir mechanism",
            "independent Rule-9 review"],
        "canonical_test_01_action_input_complete":False, "canonical_source_vector_derived":False,
        "full_metric_frame_variation_verified":False, "physics_pass":False,"gate_effect":"NONE",
        "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED",
        "V":"NOT_COMPUTED","Stage4A":"CLOSED","Rule9":"NOT_CLEARED",
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    OUT.with_suffix(OUT.suffix+".sha256").write_text(f"{digest(OUT)}  {OUT.name}\n",encoding="ascii")
    print(json.dumps({k:record[k] for k in ("candidate","validation","passed","total","physics_pass","status")}))
    for check in a.checks:
        if not check["passed"]:
            print(json.dumps(check))
    return 0 if passed == len(a.checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
