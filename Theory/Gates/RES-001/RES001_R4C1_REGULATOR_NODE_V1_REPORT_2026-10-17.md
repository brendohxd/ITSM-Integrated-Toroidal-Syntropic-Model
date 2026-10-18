# R4C1 regulator nodes: necessary compatibility, not physical admission

17 October 2026. Unchanged-action Stage 2. Local checks 187/187 PASS;
complete fresh read-only replay exact, exit zero. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding and meaning

The singular regular-branch inverse does not by itself reject the registered
wave. At alignment, the original regulator equation supplies a different
necessary constraint. Its value and transport are consistent with every
stored quadratic full-response sample: 18 runs, four events each, both
methods and all three registered families/eta values. No sample is discarded.
This is not a proof of persistence, arbitrary-3D constraint closure, or
admission of complete finite-amplitude initial data.

The calculation also identifies a concrete canonical-lifting pitfall.
Omitting the action's cubic cusp momentum can cause an order-|e| error in the
reconstructed regulator velocity near the profile zero. The archive stores
velocities, not a cusp-omitting canonical state; it has not been corrected or
accused of this error. An exact momentum lift must use the complete action.

## 1. Original regulator equation, before alignment

The [contract](RES001_R4C1_REGULATOR_NODE_V1_CONTRACT_2026-10-17.md) retains
normalized n=U/sqrt(-U^2) and independent unit variation. With
hp^{ab}=g^{ab}+n^a n^b, acc^a=n^b nabla_b n^a and theta=nabla_a n^a,
the original first-order regulator density is

    L_reg = b Z^2/2 - b grad Z . hp . grad psi - b Z acc . grad psi.

Direct Euler variation, not an assumed self-adjoint operator, gives

    E_Z/b = Z + nabla_a(hp^{ab} grad_b psi) - acc . grad psi
          = Z + hp^{ab} nabla_a nabla_b psi + theta (n.grad psi).

The second equality follows by the product rule and metric compatibility:
div hp = theta n + acc. Omitting the acceleration term leaves an extra
acc.grad psi. The generally different formal adjoint is not substituted.
Division by b requires the declared b!=0 branch.

Write n=gamma ell+V in the ADM normal/spatial basis, gamma^2=1+V^2, with
p=(partial_t psi-L_S psi)/N and Kij=(partial_t hij-L_S hij)/(2N).
The scalar Hessian components follow by differentiating p=ell.grad psi,
nabla_i ell=K_i^j e_j and nabla_ell ell=D ln N:

    Q00 = D_t p/N - D^i ln N D_i psi,
    Q0i = D_i p - K_i^j D_j psi,
    Qij = D_iD_j psi - Kij p.

Consequently

    E_Z/b = Z + V^2 Q00 + 2 gamma V^i Q0i
              + (h^{ij}+V^i V^j) Qij + theta (gamma p+V^i D_i psi).

All spatial directions and metric/frame jets remain. Independent general-
coordinate controls compare the original Euler contraction to this ADM
projection at 80 digits, normalized tolerance 1e-50.

## 2. The aligned constraint and necessary transport

At a point V=0, theta=K+D_i V^i. The K p terms cancel, leaving

    chi = Z + Delta_h psi + p D_i V^i = 0,
    p_Z = 0;   P_psi = p_psi/sqrt(h) = K_Q p.

The frame VALUE vanishing does not set its spatial derivatives to zero.
The aligned scalar momentum follows from the complete original force density;
cusp and regulator temporal contributions vanish at that point. This
stratum-local observation is not a global Dirac or propagating-mode count.

Let D_t=partial_t-L_S. Varying the inverse metric and Levi-Civita connection
gives the exact scalar Laplacian identity

    D_t(Delta_h psi) = Delta_h(D_t psi)
      - 2N K^{ij} D_iD_j psi
      - [2D_i(N K^{ij})-D^j(N K)]D_j psi.

The executable checks it in spatial normal coordinates, retaining all three
directions and arbitrary lapse/K gradients. Also

    D_t(div V) = div(D_t V) + V^i D_i(N K).

Thus at V=0,

    D_t chi = D_t Z + Delta_h(N p)
      - 2N K^{ij}D_iD_j psi
      - [2D_i(N K^{ij})-D^j(N K)]D_j psi
      + (D_t p)div V + p div(D_t V).

If D_t is tangent to a persistent alignment worldsheet, this must vanish
there. More generally, for a tangent T=D_t+r^i D_i require

    T chi = D_t chi + r^i D_i chi = 0.

For coordinate worldsheet velocity c^i, r^i=c^i+S^i. Tangency and persistence
must be demonstrated, not assumed. The retained example Vz=(1+t)z has both
V and its time derivative zero at z=0 but div(D_t V)=1. Separate controls
reject deletion of nonuniform lapse, metric drift or moving-node advection.

## 3. What a continuous inverse extension actually requires

This is a conditional local theorem, not admission of the preparation.
Let sigma be a simple signed normal coordinate for a proposed alignment
surface and suppose the FULL frame factors as V=sigma W with W^2>=c>0.
On the neighboring regular unit/dust/Legendre-complement branch define

    F_psi = P_Z/b + gamma V.Dpsi,
    F_Z = P_psi - ell_prime.y - f_prime,
    psi_hat = -F_psi/(sigma^2 W^2),
    Z_hat   = -F_Z/(b sigma^2 W^2).

The ell, y and f are the complete coupled coefficients in the
[canonical report](RES001_R4C1_FINITE_TILT_CANONICAL_V2_REPORT_2026-10-17.md).
First establish F_psi compatibility, then regularity of the reconstructed
quantities entering F_Z; do not assume it. The complement and unit/dust
branches must remain regular up to the proposed surface wherever invoked.

For either numerator F, assume C2 normal regularity, F(0)=F_normal(0)=0
and |F_normalnormal|<=M in a tubular neighborhood. Twice applying the
fundamental theorem of calculus gives

    F(sigma)/sigma^2
      = integral_0^1 (1-u) F_normalnormal(u sigma) du.

The quotient extends continuously and

    |psi_hat| <= M_psi/(2c),
    |Z_hat|   <= M_Z/(2|b|c).

This statement holds along each normal line. A jointly continuous extension
also requires F_normalnormal and W^2 jointly continuous in the tangential
variables; pointwise normal regularity alone does not guarantee it.

Conversely, bounded F/sigma^2 with C1 F forces both normal jets to vanish:
F(0)=0 by continuity and F_normal(0)=lim F(sigma)/sigma=0. A momentum VALUE
condition alone is insufficient. Polynomial checks exercise the integral
identity; the C2 theorem follows from this integral proof, not extrapolation
of polynomial tests.

C2 numerator regularity does not imply a C1 quotient: F=sigma^2|sigma|
has quotient |sigma|. No nonexistent ordinary third cusp derivative is used.
The constants are explicit CONDITIONAL bounds; their hypotheses are not
certified for an exact nonlinear wave. In the leading transverse profile
W^2=e^2 w(t)^2, the lower bound degenerates as e or w tends to zero.
No uniform amplitude, eta, b=0 or joint-zero limit follows.

## 4. Action-specific cusp momentum warning

At fixed configuration the original cusp contributes

    P_psi,cusp = -3 A sqrt(Y) [V^2 p + gamma V.Dpsi].

It contributes no other velocity momentum: Y depends on configuration and
the psi velocity, not metric/frame/Cartesian velocities. On the initial
homogeneous force profile, V^2=e^2 w^2 cos^2(kz),

    P_psi,cusp = -3 A |e w cos(kz)|^3 |p|p.

Hold the other COMPLETE momenta and configuration fixed on the regular
inverse branch. If that contribution is omitted from P_psi, then

    delta Z_hat = -(3A/b)|e w cos(kz)| |p|p.

The cubic momentum defect becomes a linear-in-|e| velocity defect, with a
|cos(kz)| cusp. For registered p=eta/5, A=2 eta^(3/2)/7, b=5 eta/11
and w(0)=1 its coefficient is (66/875) eta^(5/2). This follows from the
action, not an observational target. It warns against an incomplete canonical
lift, not a changed action or an invented correction to the archive.
Eight finite-amplitude complete-density controls, with nontrivial coupled
velocities and both amplitude/profile signs, verify the shift at 1e-50.

## 5. Archived quadratic nodal controls

Use the unchanged FIXED-CHARGE-RETARDED-V3 archive, all three families,
eta=1/4,1/64,1/1024 and Radau/DOP853. Each run stores FOUR full-response
events (72 total): endpoints, t=0.025, and its family/method-dependent event
near t=0.0444. The separate 21-point grid is not 21 full-response events.

For q(z)=q0+2Re(q2 exp(2ikz)), at every leading node cos(kz)=0,

    q_node = q0-2Re(q2),
    (partial_z q)_node = 4k Im(q2),
    (partial_z^2 q)_node = 8k^2 Re(q2).

This identity covers every leading node; repeated nodes are not independent
tests. The original frame convention is V^i=Vi/a. With background
p_dot=-3Hp-beta rho/K_Q, the second-order expressions are

    chi2 = Z0-2Re Z2 + (8k^2/a^2)Re Pi2 + (4kp/a)Im Vz2,
    chi2_dot = Zd0-2Re Zd2
      + (8k^2/a^2)Re Pid2 - (16Hk^2/a^2)Re Pi2
      + (4k/a)[p Im Vzd2+(p_dot-Hp)Im Vz2].

The frame and normal shift at each node are checked from archived fields,
not zeroed by fiat; mean, second harmonic, regulator and velocity terms remain.
The inherited normalized binary64 tolerance is 1e-10.

| Quantity | Maximum across all stored events |
|---|---:|
| chi2 normalized residual | 8.009306556193205e-17 |
| chi2_dot normalized residual | 2.000000000000000e-15 |
| reconstructed quadratic frame node | 3.35245349892283e-17 |
| reconstructed quadratic normal shift node | 1.8082949432832462e-18 |

These are sampled finite-order results, NOT continuous-time certificates,
exact all-order alignment, a full constraint solve or nonlinear error bounds.
No response or preparation is overwritten.

## Verification and remaining acceptance

All 187 checks pass. The executable pins 18 sources and verifies all 36
source/sidecar metadata records unchanged. Fresh exact read-only replay
recomputes four JSON outputs and preserves all eight payload/sidecar bytes,
sizes and mtimes. Both executions terminate exit zero. Independent numerical
implementations are same-author controls, not independent peer review.

Next is full finite-amplitude constraint admission/persistence and arbitrary-
3D reduction, using these necessary node conditions rather than extending the
singular inverse. The physical reduced Hessian, Cauchy/energy domain, nonlinear
remainder, physical validity window and healthy GR remain open. Matching
still does not identify either required normalization.

Stage1 complete only in registered linear prepared-dust scope; Stage2
INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. No family GO, physical ghost/healthy verdict or prediction.

R9-MT1-REGULATOR-NODE-V1 is DEFERRED, not cleared. It inherits canonical,
constraint, G3N5, generic-family and transitive review debt. Provisional reuse
is limited to these necessary compatibility formulas and stated controls.
No vault mutation, manuscript/PDF/site edit, commit/push, publication,
submission, model/provider dispatch, runtime or action change is included.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| Contract | 2bea03116cb22de56e91c48de5038945261c0ffc3a3bd1618b66b1cf9995d053 |
| Executable | 7126d03a3b3a3a525bf1ce4c8b31c8541901f9d7c45ad82c288db71cc97cfa25 |
| summary.json | d50fbea1300bfa65d36dce8f3c6bf64bf77a48695b094382db2bb1c63b1d1353 |
| formulas.json | 4645438782fedd5fb4a6637edcb2d599d90ea87747c010d6e3c5a8071eca87bb |
| independent.json | 1fcc4ca681e918ebe31280f00faad8848cdd35272ba3d3935fbffe690315c645 |
| archive_nodes.json | 9f867c7d6699103d428b000e883e0f70027caeca95d65ef84b9149f0927ec847 |

Executable: Analysis/MasterTests/test_01_r4c1_regulator_node_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_regulator_node_attempt_01.

    python -B Analysis/MasterTests/test_01_r4c1_regulator_node_v1.py --replay Analysis/MasterTests/outputs/r4c1_regulator_node_attempt_01

New calculations require a new nonexistent output directory. Original sources,
receipts, failures and hashes remain untouched. Only mutable execution/review
indexes receive a guarded append and new index digests.
