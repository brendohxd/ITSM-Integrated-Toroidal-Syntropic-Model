# R4C1 first action-and-current checkpoint

Date: 2026-09-25. Status: `CONDITIONAL_FIRST_VARIATION_CHECKPOINT_PARENT_HOLD`.
Owner: Master Test 1 / exploratory RES-001 R2 lane. Gate effect: `NONE`.

Later checkpoint: the [complete classical variation report](RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md)
supplies the frame/regulator stresses and four-dimensional Ward checks that
were still missing at this first checkpoint. Physical background, healthy
continuous GR recovery and canonical-gate holds remain open. The equations
and measured results below retain their original checkpoint scope.

## 1. Outcome and exact boundary

The separately approved [R4C1-v1 action](RES001_R4C1_ACTION_FREEZE_2026-09-25.md)
now has explicit scalar, dust and auxiliary equations, matter/reservoir
interface currents, and an alignment-corrected conserved condensate current.
The executable returns **119/119 exact checks**, including deliberately wrong
alternatives rejected by exact nonzero witnesses. Counts include dimensional
and provenance-related controls; they are not 119 independent physical tests.

This is progress beyond the earlier disconnected canonical-scalar witness:
R4C1 retains the current recovery frame, current alignment, conditional force
action and selected projected regulator. It supplies a concrete reversible
reservoir and an explicit pressureless dust realization. These new choices
remain conditional. No full Einstein/frame variation, coupled physical
Hessian, interacting on-shell cosmology, microscopic matching or independent
Rule-9 review is certified. **Master Test 1 has not passed.**

## 2. Convention and scalar variations

Use the frozen (-+++) chart and define E_f=(sqrt(-g))^-1 delta S/delta f.
Let s=u^2+v^2, C^mu=h^{mu nu}J_nu, and V_s=dV/ds. All derivatives below
are covariant. The portal is W=g_r s r^2/4 and belongs to the plenum stress.

The two condensate momenta and equations are

```
Pi_u^mu = -nabla^mu u - zeta v C^mu,
Pi_v^mu = -nabla^mu v + zeta u C^mu,

E_u = Box u - 2u V_s - g_r u r^2/2
      + zeta [2 C^mu partial_mu v + v nabla_mu C^mu] = 0,
E_v = Box v - 2v V_s - g_r v r^2/2
      - zeta [2 C^mu partial_mu u + u nabla_mu C^mu] = 0,
E_r = Box r - V_R'(r) - g_r s r/2 = 0.
```

Their momenta, equations and U(1) identity are differentiated from the action
with arbitrary local h and first derivatives of h. This covers the scalar
identity on a varying frame; it does not solve the frame's own equation.

For dust, C=exp(beta psi), X_tau=(nabla tau)^2, and

```
E_tau = nabla_mu(epsilon C^2 nabla^mu tau) = 0,
E_epsilon = -(C^2 X_tau + C^4)/2 = 0.
```

On that constraint X_tau=-C^2. The physical dust stress has trace
T_m=-epsilon C^4. The off-shell trace must be used before the multiplier
equation; substituting the constraint into the action before variation would
incorrectly make its Lagrangian zero.

The first-order force action gives

```
Pi_psi^mu = K_Q Q n^mu - 3 A sqrt(Y) h^{mu nu} partial_nu psi
            - b h^{mu nu} partial_nu z - b z a^mu,
Pi_z^mu = -b h^{mu nu} partial_nu psi,
E_z = b(z + Delta psi) = 0,
E_psi = -nabla_mu Pi_psi^mu + beta T_m = 0.
```

For b>0, eliminate z=-Delta psi. The resulting equation is

```
E_psi = -nabla_mu[K_Q Q n^mu - 3 A sqrt(Y) h^{mu nu} partial_nu psi]
        - b Delta_dagger Delta psi + beta T_m = 0,
Delta_dagger z = nabla_mu(h^{mu nu} partial_nu z + z a^mu).
```

The formal adjoint is with respect to sqrt(-g) d4x and the frozen boundary
conditions. It is not generally Delta itself. At b=0 the auxiliary decouples;
do not divide by b or infer an unchanged constraint rank.

## 3. Charge conservation is not energy throughput

Under delta u=-v alpha, delta v=u alpha, the action-derived current is

\[
j^\mu=-v\Pi_u^\mu+u\Pi_v^\mu
     =J^\mu+\zeta s h^{\mu\nu}J_\nu,
\qquad \nabla_\mu j^\mu=vE_u-uE_v.
\]

Thus the portal preserves U(1): on the condensate equations, div j=0.
The bare current J is generally **not** the full Noether current once the
alignment interaction is present. In a homogeneous comoving frame the
alignment contribution vanishes, recovering charge density s dot(Theta) and
its zero-source FRW dilution law. This limiting agreement must not be
extrapolated to inhomogeneous current transport.

A concrete local subsystem check uses a rest frame and spatial jets u=x,
v=x^2 at x=1, solving the two time accelerations from E_u=E_v=0. Then

```
div(zeta s C) = -10 zeta,
div J = +10 zeta,
div j = 0.
```

This is a condensate-on-shell local jet, not a solved Einstein/frame
background or a global periodic profile. The general identity is covariant
and compatible with periodic fields on T3. The current is polynomial in
u,v and their first derivatives and is regular at amplitude zeros.

R4C1 therefore has S_N=0 for its full Noether charge, despite permitting
nonzero energy exchange. No positive entropy production or charge creation
has been established. It cannot yet substantiate an irreversible syntropic
mechanism merely by naming its reservoir current Q_syn.

## 4. Varied stresses and interface currents

Define T_{a,mu nu}=-2(sqrt(-g))^-1 delta S_a/delta g^{mu nu}, holding the
independent **contravariant** U fixed. Direct scalar metric variation gives

```
T_m,mu nu = epsilon C^2 partial_mu tau partial_nu tau + g_mu nu L_m,
T_R,mu nu = partial_mu r partial_nu r + g_mu nu L_R,
T_Phi+W,mu nu = partial_mu u partial_nu u + partial_mu v partial_nu v
              + g_mu nu[-((nabla u)^2+(nabla v)^2)/2 - V - W].
```

In particular, partial L_m/partial psi=beta T_m follows from the varied
conformal action, not an assumed exchange equation. Differentiating the first
two stress tensors gives the off-shell identities

```
nabla_mu T_m^{mu nu} = E_tau nabla^nu tau
                    + E_epsilon nabla^nu epsilon + beta T_m nabla^nu psi,
nabla_mu T_R^{mu nu} = E_r nabla^nu r + W_r nabla^nu r.
```

Consequently, on those fields' equations, the baseline-split interface
currents are

\[
Q_{mp}^\nu=\beta T_m\nabla^\nu\psi,\qquad
Q_{syn}^\nu=-W_r\nabla^\nu r=-\frac{g_r}{2}s r\nabla^\nu r.
\]

Both have mass dimension five. Their exact zero-coupling branches agree with
their limits; neither divides by charge, density or coupling. They remain
finite on the frozen finite-field chart, including s=0. For example,
u=1,v=0,r=1,g_r=2,dot(r)=3 gives Q_syn^0=3 in the local natural-unit chart.
It is an exchange witness, not a calibrated rate or cosmological solution.

If fraction eta of -W is instead assigned to L_R,

```
T_R -> T_R - eta W g,       T_P -> T_P + eta W g,
Q_syn -> Q_syn + eta nabla W.
```

The total action/stress is unchanged, but the named transfer current is
split-dependent. Do not treat a split-dependent current as a unique
observable without fixing the convention.

### Frame-normalization terms already checked

Because n=U/sqrt(-U^2), varying the metric at fixed U changes n. Let
J_n=n^mu J_mu and p_mu=partial_mu psi. Then

```
T_align,mu nu = zeta[J_mu J_nu - J_n^2 n_mu n_nu] + g_mu nu L_align,
T_QY,mu nu = K_Q Q^2 n_mu n_nu
            + 3 A sqrt(Y)[p_mu p_nu - Q^2 n_mu n_nu] + g_mu nu L_QY.
```

Direct variation in all ten independent inverse-metric directions checks
these expressions at a boosted timelike frame. J remains symbolic; the
force check uses a declared exact nonzero-gradient jet. This does not prove
the connection-dependent frame/regulator stress, nor a metric Hessian.
Omitting the normalization term fails the alignment test.

### Total conservation: precise remaining obligation

Diffeomorphism invariance supplies the structural Ward identity for a
contravariant vector and scalar fields f:

```
nabla_mu T^mu_nu = sum_f E_f partial_nu f
                 + E_Ua nabla_nu U^a + nabla_mu(U^mu E_U nu).
```

Include multiplier fields among f. Applying this to S_P also includes its
explicit r derivative -W_r, and E_psi^P=E_psi-beta T_m. If **all** plenum
equations, including the varied U and constraint equations, hold, the
identity gives div T_P=-Q_mp+Q_syn and the three balances sum to zero.
This is the formal action-based argument, not a completed independent
all-sector conservation test. The explicit connection-dependent T_U and
T_reg and their vector Ward residual remain to be generated and checked.
No Bianchi-only assignment has been counted as that missing verification.

## 5. Regulator and GR controls

Christoffels computed from flat-FRW g=diag(-1,a^2,a^2,a^2) give

```
h^{mu nu} nabla_mu nabla_nu psi = a^-2 partial_i^2 psi - 3H dot(psi),
theta Q = 3H dot(psi),
Delta psi = a^-2 partial_i^2 psi.
```

Omitting theta Q therefore fails on an evolving slice. For the accelerated
static lapse metric ds^2=-N(x)^2 dt^2+dx^2+dy^2+dz^2, n=N^-1 partial_t,
a^x=N'/N, and fields depending only on x,

```
Delta f = f'',
Delta_dagger z = (N z)''/N.
```

The acceleration term in the divergence representation is necessary. The
first-order auxiliary sign yields -b(Delta psi)^2/2, reproducing the
constant-frame force dispersion omega^2=b k^4/K_Q. These checks are not a
proof of stability, hyperbolicity or a healthy arbitrary-frame spectrum.

At beta=g_r=0, an uncoupled reservoir with nonzero dot(r) still carries
positive energy. This rejects 'zero exchange = pure GR'. The frozen
coefficient-level endpoint removes all additional kinetic sectors, sets the
extra scalar fields identically to zero, and leaves Einstein-dust plus a
cosmological constant. This changes the frame/auxiliary dynamics and is
**not** a demonstrated healthy continuous GR limit at finite density.

## 6. Reproduction, correction history, and next gate

```
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_current_audit.py
python -B Scripts/itsm_context.py receipt Analysis/MasterTests/outputs/test_01_r4c1_current_summary.json
```

Verified interpreter: C:/Users/brend/anaconda3/envs/itsm_env/python.exe;
Python 3.13.9, SymPy 1.14.0. Substitute that interpreter for both occurrences
of python where the shell alias is unavailable.

- Freeze SHA256: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
- Script SHA256: `625c6e1b32818719ba0f12ff93b37ea680e6955f9f60f37784f99a45e7f3d740`.
- Receipt SHA256: `71a43573a28d03d3ee01b51e1d77c6ba2739ce212d1596662362f53bcbe0fcc2`.

An in-memory changed-freeze-hash probe raises FROZEN_INPUT_HASH_MISMATCH
before writing a receipt; the existing receipt hash remains unchanged.
Source files themselves were not modified for this probe.

During test strengthening, a 117-check run failed the new local bare-charge
assertion (residual 20 zeta). Its expected sign had incorrectly been -10
zeta. Differentiating zeta s J^x=-zeta(x^4+x^6) fixes that expected divergence
to +10 zeta when div j=0. The frozen action and Noether identity were unchanged.
The final 119 checks additionally verify both solved scalar equations at that
jet. The failed-run output is preserved in ignored local optimizer logs;
this correction history prevents silently presenting an uninterrupted pass.

**Next bounded task:** explicit off-shell U, lambda_U and connection-dependent
regulator metric variation for this frozen action, followed by all-sector
Ward residual checks. Then test a nonzero-charge interacting background and
the GR/constraint limit. Pressure/radiation matter, stability, microscopic
matching and independent review remain separate requirements. Historical
coefficient work stays parked at the user's direction.

The ITSM memory skill was used for continuity and provenance discipline, not
as scientific evidence; the live files and exact calculations govern this
report. No paid reviewers were dispatched, and this is not peer review.

`physics_pass=false`, `Rule9=NOT_CLEARED`, `gate_effect=NONE`.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED. TOP-X4, frozen manuscripts and published artifacts unchanged.
