# R4C1-S2: scalar propagation and finite-time evolution

Date: 2026-09-26. FROZEN_BEFORE_EXECUTABLE. Owner: Master Test 1.
Conditional R4C1-v1 action and B1 coefficients unchanged. Gate effect NONE.

## Inputs and purpose

Use S1's constraint-reduced scalar action, not a metric-frozen proxy. Determine
its formal short-wavelength propagation branches and evolve its linear modes
on the registered background. Separate kinetic, gradient, finite-time growth,
well-posedness and EFT applicability; a positive kinetic matrix does not settle
the other questions. No target data or coefficient fitting.

Pins:

- S1 matrices: `27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a`.
- S1 receipt: `10bdc2ac1faeb30203cd75f5015ab41e64dd19b6cef37193f6987baf85bfc033`.
- S1 executable: `977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed`.
- S1 report: `0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b`.
- B1 executable: `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
- B1 trajectory: `0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa`.

Verify the pinned receipts' transitive source/artifact hashes before use.
Review is DEFERRED; inherit R9-MT1-S1, R9-MT1-B1 and R9-MT1-VARIATION.
Proceed provisionally without reviewer dispatch. Do not certify publication.

## Time-dependent chart, not a frozen-coordinate shortcut

For nonzero k=2*pi*n and expanding H>0, let T=delta tau/C and define

```
X_u=delta u-u_dot*T; X_v=delta v-v_dot*T; X_r=delta r-r_dot*T;
X_psi=delta psi-psi_dot*T; W=w-(k/a)*T.
```

Construct q=J(t,k)y, y=(X_u,X_v,X_r,X_psi,T,W), including Jdot and Jddot.
First recover the S1 kinetic diagonal (1,1,1,K_Q,D,M_U^2*c14), D=66H^2
at B1 coefficients. Then define x=a^(3/2)*sqrt(K_diagonal)*y, so the
entire time-dependent action has unit kinetic matrix. Keep all derivatives
of this transformation; freezing it before differentiation can corrupt
leading spatial terms. Use exact B1 background equations for these derivatives.

Export normalized action matrices Mc,Vc in
L2=xdot^2/2+xdot^T Mc x-x^T Vc x/2 and EOM
xddot+G xdot+Wc x=0, G=Mc-Mc^T, Wc=Vc+Mcdot.
Check G antisymmetry, Wc-Wc^T=Gdot, and equivalence to the original S1
equations under the time-dependent transformation. A symmetric part of Mc
may be removed only with its associated time-derivative term.

## Formal short-wavelength branch analysis

Extract polynomial powers of physical p=k/a after all time derivatives.
Determine the highest spatial order, its rank and sign. Do not use Vc
eigenvalues alone as physical frequencies. Retain the gyroscopic -i*omega*G
terms when constructing the frequency pencil.

If there is a single positive p^4 branch, derive its leading omega^2/p^4.
Eliminate that fast branch asymptotically for omega=O(p), retaining any p^3
cross terms through their Schur correction. Solve the remaining leading
frequency pencil, including G's leading spatial powers. Count zero branches
explicitly; a zero sound speed is not a positive-speed or strong-hyperbolicity
certificate. Report negative/complex leading roots as such, without retuning.

Use t=(0,0.5,1,2,3,4) for independent numeric symbol checks at
p=(20,40,80,160). These continuous p values test the local symbol only,
not four additional torus trajectories. Compare analytic leading coefficients
with numeric branches; expected asymptotic behavior must be demonstrated,
not asserted from a single wavelength. Tolerances: algebraic identities exact;
normalized pencil residuals <1e-8; final propagating-branch leading coefficient
discrepancy <0.05, or record NONASYMPTOTIC/UNRESOLVED without relaxing the bound.
Zero branches need separate subleading interpretation rather than relative
error against zero. Do not infer physical access to p->infinity without an EFT.

As a labelled frame-sector comparator only, the Einstein-aether Minkowski
spin-0 speed is alpha123*(2-alpha14)/[alpha14*(1-alpha13)*(2+alpha13+3*alpha2)],
where alpha_i=M_U^2*c_i/M_P^2; see Oost, Mukohyama and Wang (2018), eq. (3.4),
https://arxiv.org/html/1802.04303v2. The coupled B1 answer must be derived;
this comparator is neither an input substituted for it nor an observational
fit. The H=0 spatially flat gauge is invalid and is not used as its derivation.

## Finite-time transfer and validation

Evolve the full 12x12 fundamental matrix of (x,xdot) for n=(1,2,4,8) on
[0,4], starting with identity. Use DOP853 rtol=1e-9, atol=1e-11 and Radau
rtol=1e-9, atol=1e-11, with 101 output times. Background: dense B1 DOP853
integration rtol=1e-12, atol=1e-14; compare to the pinned background to 1e-8.
No projection, artificial damping or eigenvalue clipping.

Require solver success and finite values. Compare the two transfer matrices
with max abs(difference)/(1+max abs(reference)), threshold 1e-5. Record
symplectic conservation in canonical variables (x,pi=xdot+Mc*x), normalized
by 1+||F||^2, threshold 1e-6. A failed accuracy criterion means UNVALIDATED,
not a repaired scientific outcome. If computationally infeasible, report the
actual remaining modes/methods rather than shrinking the registered domain.

Report endpoint and maximal sampled singular-value amplification in this
explicit reference chart. This norm is not a coordinate-invariant energy or
Lyapunov exponent: a stable high-frequency oscillator can have a large
unweighted (x,xdot) norm. Do not declare an instability solely from it.
Do not label a finite low-frequency gravitational growth rate a UV gradient
instability; use its scale dependence and the leading pencil.

Checks must reject omission of Jdot/Jddot and omission of the p^3 Schur term
if present. Verify the transformed EOM independently from the original S1
K,M,V formula. Preserve any disagreement. Export formulas, numerical symbol
diagnostics and transfer summaries with hashes and exact interpretation.

## Remaining boundary

Even a favorable result is limited to the classical scalar branch on B1.
The k=0 constraints, singular parameter/gauge surfaces, all-sector evolution,
nonlinear caustics, uniform well-posedness, EFT scale hierarchy, physical
weak-field matching, GR recovery and independent review remain separate.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; Rule9_cleared=false; physics_pass=false. No commit/push.
