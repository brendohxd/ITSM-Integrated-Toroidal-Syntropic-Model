# R4C1 complete classical variation and conservation checkpoint

Date: 2026-09-25. Candidate: R4C1-v1, unchanged.
Status: `CONDITIONAL_CLASSICAL_VARIATION_PARENT_AND_BACKGROUND_HOLD`.
Owner: Master Test 1 / exploratory RES-001 R2. Gate effect: `NONE`.

Later continuation: [R4C1-B1](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md)
now supplies one finite-time interacting background control. It does not
establish physical stability, scale validity or healthy continuous GR
recovery. The variation results below retain their original scope.

## 1. Result and scope

The previously missing explicit frame and connection-dependent regulator
metric variations are now supplied below. Together with the scalar/dust
equations in the [first report](RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md),
they specify every classical Euler equation and sector stress of the frozen
candidate. Direct component variations and independently implemented exact
four-dimensional off-shell Ward probes give **162/162 local checks**.
All four total-conservation residuals are exactly zero in both registered
probes. Omitting the connection stress or the vector Ward terms is rejected.

The general tensor derivation, not a count of sampled zeros, supplies the
conservation argument. The finite probes check its implementation; they are
not a proof of all configurations, an independent referee review or a
solution of the field equations. The calculation is on the smooth timelike
frame / Y>0 chart. It does not smooth the frozen action at Y=0.

This advances **candidate-level classical action/source closure**, not
canonical Test-1 closure or microscopic derivation. An interacting physical
background, healthy continuous GR recovery, full constraint/stability
analysis, matter beyond dust and independent review remain open. Neither
K_Q nor the canonical matter-coupling invariant V has been computed.

## 2. General first-order variation: where the connection enters

Use the frozen (-+++) signature and independent covariant g_ab,
contravariant U^a, scalar fields and multipliers. For this section only,
V_a^b denotes nabla_a U^b, **not** the canonical MAT-001 matching invariant.
Treat g,U,V and scalar covariant gradients independently when taking the
following algebraic partial derivatives:

```
P_c^a = partial L_P / partial V_a^c,
F_c = partial L_P / partial U^c,
S^{mn} = 2 partial L_P / partial g_mn,
P^{ab} = P_c^a g^{cb}.
```

For symmetric tensors parentheses have unit-weight symmetrization. Since

```
delta V_a^c = nabla_a(delta U^c) + delta Gamma^c_ab U^b,
delta Gamma^c_ab = g^{cd}[nabla_a delta g_bd + nabla_b delta g_ad
                         - nabla_d delta g_ab]/2,
```

the coefficient of nabla_k delta g_mn is K^{k mn}/2, where

```
K^{k mn} = U^(m P^{k n)} + U^k P^{(mn)} - U^(m P^{n)k}.
```

After integration by parts with the frozen endpoint conditions,

```
E_Uc = F_c - nabla_a P_c^a,
T_P^{mn} = g^{mn} L_P + S^{mn} - nabla_k K^{k mn}.
```

This covariant-metric convention gives the same stress as
-2/sqrt(-g) times variation with respect to the inverse metric. The
connection improvement is essential, not an optional stress reassignment.
The first-order matter-sector surface variation is

```
Theta^k = P_c^k delta U^c + sum_f Pi_f^k delta f
          + K^{k mn} delta g_mn/2.
```

It vanishes for the frozen fixed endpoint fields/metric and periodic spatial
variations. Einstein-Hilbert uses its separately frozen GHY term. Eliminating
the auxiliary z requires retaining the induced boundary convention; the
present derivation uses the original first-order action throughout.

## 3. Explicit frame momentum and Euler derivative

The following abbreviations contain no new operators or free functions:

```
ell=sqrt(-U^2), n=U/ell, h^{ab}=g^{ab}+n^a n^b,
h^a_b=delta^a_b+n^a n_b, h_ab=g_ab+n_a n_b,
a_U^a=U^b V_b^a, theta_U=V_a^a,
p_a=partial_a psi, k_a=partial_a z,
Q=n.p, Q_z=n.k, J_n=n.J,
w_a=p_a+Q n_a, w_za=k_a+Q_z n_a, w_Ja=J_a+J_n n_a,
v^a=n^b V_b^a, D=n_a v^a, B=w_a v^a,
a^a=h^a_b v^b/ell.
```

Keep all four frame invariants. Writing M=M_U^2, their contribution and the
regulator contribution to P are

```
P_frame,c^a = -M[c1 g^{ab}g_cd V_b^d + c2 theta_U delta_c^a
                + c3 V_c^a - c4 U^a a_Uc],
P_reg,c^a = -(b z/ell) n^a w_c,
P = P_frame + P_reg.
```

The algebraic U derivatives, at fixed g and V, are

```
F_frame,c = M c4 V_c^a a_Ua + lambda_U U_c,
F_align,c = -(zeta J_n/ell) w_Jc,
F_QY,c = [(K_Q-3 A sqrt(Y))Q/ell] w_c,
F_reg,c = -(b/ell)(Q w_zc + Q_z w_c)
          -(b z/ell^2)[n_c B + h^a_c V_a^d w_d
                       + w_c D + Q h_dc v^d],
F = F_frame + F_align + F_QY + F_reg.
```

These include the normalization derivative
partial n^a/partial U^c=h^a_c/ell. The multiplier equation is
E_lambda=(U^2+1)/2=0; it is imposed after variation. No null-frame extension
or replacement of U by a normalized condensate current has been made.

Dimensions: [P]=3, [F]=[E_U]=4, [K]=3. Every term in the stress has dimension
four, and its divergence and every Ward term have dimension five in the
frozen dimensionless-psi chart.

## 4. Explicit metric algebraic blocks and full stress

Write S_i^{mn}=2 partial L_i/partial g_mn at fixed U,V and scalar covariant
gradients. Define V^{ma}=g^{mb}V_b^a. Then

```
S_frame^{mn} = M c1[V^{ma}V^{nb}g_ab - g^{ab}V_a^m V_b^n]
               + M c4 a_U^m a_U^n + lambda_U U^m U^n,

S_align^{mn} = zeta[J^m J^n - J_n^2 n^m n^n],

S_QY^{mn} = K_Q Q^2 n^m n^n
            + 3 A sqrt(Y)[p^m p^n - Q^2 n^m n^n],

S_reg^{mn} = 2b k^(m p^{n)} - 2b Q Q_z n^m n^n
             -(2b z/ell)[(B+Q D)n^m n^n + Q v^(m n^{n)}].
```

Here J_n is the scalar contraction defined above; it is not a free tensor
index in J_n^2. The c2 and c3 invariants have no explicit metric derivative
at fixed V_a^b; their stress contributions enter through L_frame and K(P).
They have not been dropped from the action or Einstein equations.

Assemble the complete plenum stress, with the portal assigned to L_P:

```
T_P^{mn} = g^{mn} L_P + nabla^m u nabla^n u + nabla^m v nabla^n v
           + S_frame^{mn} + S_align^{mn} + S_QY^{mn} + S_reg^{mn}
           - nabla_k K^{k mn}.
```

The reservoir and dust stresses are those explicitly varied in the first
report. The metric equation is

```
M_P^2 G^{mn} + rho_Lambda g^{mn} = T_P^{mn}+T_R^{mn}+T_m^{mn}.
```

The scalar momenta/Euler equations from the first report, E_U=0 above,
E_lambda=0, and this metric equation complete the classical variational
ledger. No unspecified frame/regulator stress remains in this candidate's
equations. This does not supply a solution or a renormalized quantum stress.

## 5. Conservation from action variation, not Bianchi assignment

For compactly supported infinitesimal diffeomorphisms use
delta g_mn=2 nabla_(m xi_n), delta U^a=xi^b nabla_b U^a-U^b nabla_b xi^a,
and delta f=xi^b partial_b f for every scalar, including multipliers.
Substituting the variations above and integrating the xi derivative gives

```
nabla_mu T^mu_nu = sum_f E_f partial_nu f
                 + E_Ua nabla_nu U^a + nabla_mu(U^mu E_U nu).
```

Thus the vector terms must be retained off shell. Treating U as a scalar
collection in this identity is incorrect. For the plenum sector, include
its external reservoir derivative E_r^P=-W_r; its force equation is
E_psi^P=E_psi-beta T_m. For the reservoir and matter sectors use their
explicitly varied equations and stresses. Only after setting all total
field equations to zero do the three identities reduce to

```
div T_m = Q_mp,   div T_P = -Q_mp+Q_syn,   div T_R = -Q_syn,
Q_mp^nu = beta T_m nabla^nu psi,
Q_syn^nu = -g_r (u^2+v^2) r nabla^nu r/2.
```

Their sum is conserved. This derives the conservation structure from the
frozen action and all field variations. It does not infer an arbitrary
reservoir vector from the contracted Bianchi identity. The interaction-split
dependence, regular zero-coupling currents and separate zero-source Noether
charge equation from the first checkpoint are unchanged.

## 6. Executable evidence and limitations

The [pre-execution contract](RES001_R4C1_FULL_VARIATION_CHECK_CONTRACT_2026-09-25.md)
fixes the tests, domains, rational probe coefficients and seeds. The action
was not altered after observing results.

- Direct SymPy differentiation checks 16 frame-derivative directions, four
  frame directions and ten symmetric metric directions for each of four
  sectors, with symbolic couplings and nonunit timelike frame.
- The connection-variation identity is checked with arbitrary independent
  symmetric metric-derivative symbols, including their 40 coefficients.
- A separate rational Taylor algebra is checked against independent SymPy
  inverse, square-root, fractional-power and exponential expansions plus
  mixed differentiation. The full matrix inverse is checked through all
  retained Taylor coefficients.
- Dense four-dimensional field/metric Taylor polynomials through degree
  three use registered seeds 4101 and 4102. Nonzero metric derivatives and
  connection terms are retained; no FRW, static or one-coordinate ansatz is
  imposed. Both frames have U^2=-4 intentionally: the Ward identity is tested
  **off** the unit constraint, retaining its multiplier residual. Y=9 and the
  dust time gradient is timelike at the point.
- Matter, reservoir, plenum and total Ward residuals vanish in all four
  components for both probes. Omitting connection stress gives nonzero
  squared residual norms, including 1933849646336473/78586200000000 for
  seed 4101. Wrong stress sign and omitted vector Ward terms also fail.

The 162 checks include related component and arithmetic controls, not 162
independent experiments. The exact local probes are compatible with smooth
local charts on T3 but are not global periodic solutions. They do not select
initial data or demonstrate stable time evolution. The general ledger and
finite checks still require independent review. The previous zero-gradient
first-variation control remains separate; no higher Taylor expansion at
Y=0 is claimed here.

Run using the known working Python interpreter:

```
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_full_variation.py
python -B Scripts/itsm_context.py receipt Analysis/MasterTests/outputs/test_01_r4c1_full_variation_summary.json
```

Verified runtime: C:/Users/brend/anaconda3/envs/itsm_env/python.exe;
Python 3.13.9 and SymPy 1.14.0. Substitute that interpreter for both python
commands if the shell alias is unavailable. Source pins reject changed
frozen inputs before execution. A second run reproduces the receipt byte for
byte; an in-memory pin-mismatch probe rejects without replacing that receipt.

SHA256:

- Contract: `ad553a06fcec073cc176a68ef3f6b1bb77b5506d0ba5006606ff56ab595318db`.
- Executable: `aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0`.
- Receipt: `a91ad85caa748b77b888f69aede80c2dce5322dcdef4f1b77cf61f5a93a4e156`.

## 7. Requirement-level continuation

The missing explicit classical variation item is advanced for R4C1. The
next physics test is an interacting, finite-charge on-shell background with
its independent constraint and exchange residuals, followed by the
registered GR-limit and constraint/stability checks. The algebraic GR
endpoint previously exhibited is not automatically a healthy continuous
limit of such a solution. The classical neutral reservoir preserves U(1)
and does not establish irreversible syntropic production.

Tests 2 and 3 retain their previous dispositions: conditional spherical
weak-field behavior is not a universal pointwise law on T3; static coefficient
normalization is not a blind action-derived a0 prediction. No matching
constant, expansion history or observational fit is supplied by this Ward
audit. Historical reconstruction remains parked at the user's direction.

The complete Tests 1-3 goal remains active and incomplete. The ITSM memory
skill kept provenance and canonical status separate; unavailable live memory
tools were not treated as a source of new scientific evidence. No paid
reviewers were dispatched or self-certification called Rule-9 clearance.

`physics_pass=false`, `gate_effect=NONE`, `Rule9=NOT_CLEARED`.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED. TOP-X4 and published/frozen artifacts unchanged.
