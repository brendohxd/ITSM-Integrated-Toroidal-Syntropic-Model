# R4C1-G3S: coupled scalar characteristics of the equal-Newton family

Date: 2026-09-30. Owner: Master Test 1 / conditional R4C1-v1.
Disposition: `CONDITIONAL_G3_SCALAR_SYMBOL_ZERO_BRANCH_AND_EFT_OPEN`.
Local validation: 25/25, zero failed/unknown local checks.
`physics_pass=false`, canonical Tests 1–3 remain `HOLD_SUBSTANTIVE`;
`Rule9_cleared=false`, review DEFERRED, gate effect NONE.

## Result and scope

G3's equal-static/cosmological-Newton family retains positive scalar kinetic
weights and real nonzero leading scalar frequencies in the regular expanding
nonzero-mode chart. Its frame-related scalar speed squared is
`4/[3(8-eta)]`, equal to `4/21` at eta=1. This is derived from the **coupled**
metric/frame/dust/force action, not substituted from a vacuum comparator.

The double zero-speed root remains defective for every finite registered
eta. The family therefore does **not** resolve that principal-chart
well-posedness question. Full physical EFT validity, singular/zero-mode
treatment, mixed-regularity evolution estimates on this new family and a
healthy continuous GR limit remain open. A negative entry of the slow
potential is not itself a gradient-instability verdict: gyroscopic mixing
changes the physical characteristic polynomial.

The [contract](RES001_R4C1_EQUAL_NEWTON_SCALAR_CONTRACT_2026-09-30.md)
was frozen before calculation. This is the unchanged action and previously
declared [G3 family](RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md),
not a retuned B1 result. No observed acceleration, Hubble calibration or
galaxy target entered.

## 1. Retained constraints and time-dependent normalization

Use S1's generic symbolic preconstraint Hessian and reduced K,M,V export.
Its coefficients remain symbolic; S2's B1-specialized evaluated matrices
are not reused. Substitute G3 coefficients with symbolic 0<eta<=1 and
derive the new on-shell background flow from the same action equations.
In particular `M_c^2=1-eta/12`, `K_Q=3 eta`,
`psi_ddot=-3H psi_dot-(2 eta/15)rho_m` and
`rho_mdot=(-3H+(2 eta^2/5)psi_dot)rho_m`.

Let q=(delta u,delta v,delta r,delta psi,delta tau,w). With
`J[:,4]=(udot,vdot,rdot,psidot,C,k/a)` and all other identity columns,
the exact transformed kinetic weights are

```text
J^T K J = diag(1,1,1,3 eta,D,eta/6),
D = 144 H^2 (1-eta/12)(1-eta/8)/eta.
```

They are positive for 0<eta<=1 and H!=0. Require finite positive a,C,
H>0,k!=0, b>0 and the nonzero S1 auxiliary determinant. Neither eta=0
nor another rank-changing surface is inverted. Natural units and mixed
field dimensions remain those of the action/S1; raw magnitudes are not
observationally normalized eigenvalues.

Normalize the full volume-weighted action with
`R=J diag(1,1,1,1/sqrt(3 eta),1/sqrt(D),sqrt(6/eta))/a^(3/2)`.
The exact identities are

```text
a^3 R^T K R = I,
M_c = a^3 (R^T K Rdot + R^T M R),
V_c = a^3 (R^T V R - Rdot^T K Rdot
                 - Rdot^T M R - R^T M^T Rdot),
G = M_c-M_c^T, W = V_c+M_cdot,
xddot + G xdot + W x = 0.
```

Here M_c is the canonical mixing matrix, distinct from the background
coefficient M_c^2. Direct transformation of the retained Euler equations
agrees exactly, including Rdot/Rddot; V_c is symmetric, G antisymmetric,
and `W-W^T=Gdot`. Omitting canonical derivatives, M_cdot or the cubic
fast/slow elimination changes the result and is rejected by local checks.

## 2. Exact coupled physical-momentum symbol

Take every time derivative at fixed comoving k, then set k=a*p. The full
canonical W is degree four in physical momentum; its highest block has
rank one with coefficient `5/33` in x_psi. Thus the formal fast branch is
`omega_fast^2=(5/33)p^4+o(p^4)`. This is not a finite relativistic-cone
or scattering-cutoff proof.

Eliminate that block asymptotically with the product of **both** p^3 cross
blocks divided by its p^4 coefficient. In slow order
(x_u,x_v,x_r,x_T,x_W), put `d=(8-eta)(12-eta)>0`. The resulting potential
coefficient L_2 has condensate block

```text
[[1+eta v^2/13, -eta u v/13],
 [-eta u v/13, 1+eta u^2/13]],
```

and remaining diagonal entries `1, -4 eta/(3d), 0`, with no other entries.
The only nonzero leading gyroscopic entries are
`(G_1)_TW=-4/sqrt(d)`, `(G_1)_WT=4/sqrt(d)`.
The **full** five-dimensional determinant for nu=lambda/p is

```text
det(nu^2 I+nu G_1+L_2)
 = nu^2 (nu^2+1)^2
        [nu^2+1+eta(u^2+v^2)/13]
        [nu^2+4/(3(8-eta))].
```

Consequently the nonzero linear branch speed squares are
`1,1,1+eta(u^2+v^2)/13,4/[3(8-eta)]`. On this domain the last lies in
`(1/6,4/21]`. The condensate phase branch is wider than the conformal
matter-metric cone wherever the condensate is nonzero. This is a cone
comparison, not an automatic instability, causal-curve or observational
exclusion claim. No p value here has been shown to lie inside a physical
EFT window.

## 3. Surviving zero branch and endpoint caution

The first-order slow generator `[[0,I],[-L_2,-G_1]]` has a zero root of
algebraic multiplicity two and geometric multiplicity one. This exact rank
test is part of the registered run; absence of positive real **nonzero
leading** roots cannot replace its missing complete eigenbasis.

A separate **post-run analytic interpretation** makes the defect explicit.
Restrict the generator to (x_T,x_W,xdot_T,xdot_W). Its eigenvector and
generalized eigenvector can be chosen as

```text
h=(0,1,0,0), j=(-3 sqrt(d)/eta,0,0,1),
A h=0, A j=h.
```

Direct substitution and a separate in-memory SymPy check give zero
residuals. This identifies the coordinate-level Jordan chain; it is not a
new physical-variable regularity theorem. Its displayed normalized chain
coefficient diverges as eta approaches zero. The *formal canonical-symbol*
endpoint instead has a two-dimensional zero kernel, but R and the original
auxiliary constraint reduction are singular there. That formal change of
kernel does not establish a continuous physical GR/EFT limit. S3/S4's B1
regularity/evolution analyses cannot simply be adopted with different
coefficients.

## 4. Registered numerical cross-checks

Use all six G3 eta values, both stored DOP853/Radau backgrounds and
t=(0,.5,1,2,3,4): 72 time/family/method cases. There are 288 preconstraint
Schur comparisons for n=(1,2,4,8) and 288 full-frequency pencils for
p=(20,40,80,160), not that many independent physics gates.

- Maximum normalized new-flow/pure-RHS discrepancy: `1.092e-16`.
- Maximum normalized kinetic Schur discrepancy: `8.871e-16`.
- Maximum full-frequency pencil residual: `6.420e-13`.
- Maximum p=160 propagating-coefficient discrepancy: `1.11724e-4`, below
  the frozen 0.05 diagnostic-reach criterion.
- No positive real leading rate above the registered 1e-6 numerical
  threshold appears. The exact factorization gives the nonzero branches;
  the defective zero sector still requires subleading/evolution analysis.

Finite-frequency instantaneous positive real exponents are retained in
the receipt, not deleted or labelled stable. The largest recorded is
`1.07601839888` in reference units at eta=1,t=0,p=160 (Radau background).
These roots have not been physically classified as dust/Jeans, transient
or instability contributions by this calculation. A sampled frozen-time
pencil is not an evolving-mode or uniform-function-space bound.

The original G3 background receipt remains 112/113 with its failed
801-point balance check. Its separately frozen refinement remains the
authority for finer-grid balances. Neither was overwritten or reclassified
by G3S; its preserved failure is explicitly recorded in the new receipt.

## 5. Provenance, review debt and next discriminating calculation

- Contract SHA-256: `92fc34dd19f2bc5de077703b0e7a8b209c14fdf1ae66674bc1f8176d8e4be1c5`.
- [Executable](../../../Analysis/MasterTests/test_01_r4c1_equal_newton_scalar.py):
  `eb5d8c41938d346a294aa03f713ea10655b939234dab7935f4a0ee9f774553f9`.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/summary.json):
  `550caae54b03b490a5388ecd363ad0f9ff0d8d4891021d2eb1c366871d54378a`.
- [Canonical matrix/symbol export](../../../Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/matrices.json):
  `1877c4b4412e37b15ed6297d099ff12302c59cdad929858085b97178eae47355`.

The receipt verifies direct and inherited source pins before calculation;
the deliberately false-pin control is rejected before output creation.
Python 3.13.9, NumPy 2.4.6, SciPy 1.17.1 and SymPy 1.14.0 are recorded.
New attempts refuse existing directories. Reproduction uses
`C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B
Analysis/MasterTests/test_01_r4c1_equal_newton_scalar.py --replay`, which
recomputes without writes. No older receipt-producing main() is invoked.
The independent replay run returned exit 0 and reproduced both the receipt
and canonical matrix export byte-for-byte; their hashes above are unchanged.

Review debt inherits R9-MT1-VARIATION/B1/G1/S1/S2/G2/G3. Independent review
must check the generic S1 formula reuse, new coefficient/flow substitution,
canonical derivative identities, both cubic cross blocks, full determinant,
zero-root chart interpretation and distinction between formal and physical
momenta. `PROCEED_PROVISIONALLY` applies to this scoped symbol/accuracy
result, with `substantive_blocker=NONE_WITHIN_STATED_SCOPE`: the exact
operator identities and compatible source integrity are locally checked.
Canonical Tests 1–3 remain `HOLD_SUBSTANTIVE`.

Next: evaluate the new family's subleading zero sector and finite-time
mixed-regularity evolution, and derive canonical frame interactions plus a
constraint-compatible physical validity range. Do not substitute B1's
uniform bound or a coefficient scale for that work. The healthy GR,
nonlinear weak-field and blind coefficient obligations remain unresolved.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged. No PDF edit, provider dispatch, commit,
push, canonical promotion or publication occurred.
