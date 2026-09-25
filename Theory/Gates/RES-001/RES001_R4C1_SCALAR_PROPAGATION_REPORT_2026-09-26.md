# R4C1-S2: scalar propagation and finite-time evolution

Date: 2026-09-26. Conditional R4C1-v1/B1 candidate. Master Test 1.
Validation: 56/56 implementation checks, zero failed/unknown checks.
Status: SCALAR_PROPAGATION_SUPPORTED_ZERO_BRANCH_WELLPOSEDNESS_OPEN.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Decision

The full time-dependent scalar equations have been constructed from S1 and
integrated by two independent numerical methods for the four registered torus
modes. The formal high-frequency propagating branches have real leading
frequencies. This is not a complete stability, causality or well-posedness pass:

- The remaining zero-speed branch has a defective leading symbol: a double
  zero root with only one independent eigenvector in the stated scaled chart.
- The condensate phase branch has speed squared 1+(u^2+v^2)/13, exceeding the
  matter-metric light speed when the condensate is nonzero.
- The force branch has quartic dispersion. Its unlimited formal high-frequency
  extrapolation is not a relativistic finite-cone or EFT-validity certificate.
- Finite low-frequency growth and finite-time amplification remain; these
  are not classified as a ghost or UV gradient instability just by their size.

These are substantive scientific limits. Review-only delay does not block
using the equations for the next diagnostic. No modification of the frozen
action, B1 parameters, sample domain or acceptance thresholds was made.

Owning [contract](RES001_R4C1_SCALAR_PROPAGATION_CONTRACT_2026-09-26.md);
upstream [S1 report](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md).

## 1. Time-dependent canonical action

Starting with S1's reduced K,M,V, set T=delta tau/C and

\[
 X_f=\delta f-\dot{\bar f}T\quad(f=u,v,r,\psi),
 \qquad W_f=w-(k/a)T.
\]

The intermediate coordinates y=(X_u,X_v,X_r,X_psi,T,W_f) have kinetic
diagonal (1,1,1,3,66H^2,1/6). With H>0 define

\[
 x=a^{3/2}\,\mathrm{diag}(1,1,1,\sqrt3,\sqrt{66}H,1/\sqrt6)y,
 \qquad q=R(t,k)x.
\]

The entire action, including its volume factor, becomes

\[
 L^{(2)}=\tfrac12\dot x^T\dot x+\dot x^T M_c x
                         -\tfrac12x^TV_cx,
\]
\[
 M_c=a^3(R^TK\dot R+R^TMR),
\]
\[
 V_c=a^3(R^TVR-\dot R^TK\dot R-\dot R^TMR-R^TM^T\dot R).
\]

The equations are xddot+G xdot+W_c x=0, where G=M_c-M_c^T and
W_c=V_c+Mcdot. They satisfy G^T=-G and W_c-W_c^T=Gdot. Direct transformation
of the original S1 equations, including Rdot and Rddot, gives the same result.
All background derivatives use the unchanged B1 equations. Thus this is not
a frozen-coordinate substitution or an eigenvalue test on V_c alone.

The scalar chart still excludes H=0 and k=0 and inherits the S1 auxiliary
rank restrictions. Singular branches are not crossed by an inverse.

## 2. Corrected short-wavelength calculation

Set physical p=k/a only after taking derivatives at fixed comoving k.
The highest spatial block has rank one and coefficient 5/33 in the normalized
force coordinate, giving

\[
 \omega_\mathrm{fast}^2=\frac5{33}p^4+o(p^4).
\]

For the remaining five modes, eliminate this fast block asymptotically,
including the product of both p^3 cross blocks divided by its p^4 coefficient.
Crucially, Mcdot contributes at order p^2. In the normalized T coordinate,

\[
 (M_c)_{TT}\big|_{p^2}=-\frac{p^2}{30H},
\]
\[
 (\dot M_c)_{TT}\big|_{p^2}
 =\frac{22H^2-15\dot\psi^2-5\dot r^2-5\rho_m-5\dot u^2-5\dot v^2}
        {330H^2}p^2.
\]

It changes the slow principal TT entry to -1/33. Dropping this contribution
gave an erroneous time-dependent frame speed in the first implementation.
The real evolution equations already included it; only that first symbol
diagnostic omitted it. The archived failed result is not accepted evidence.

In slow-coordinate order (x_u,x_v,x_r,x_T,x_W), the leading potential is

\[
 L_2=\begin{pmatrix}
 1+v^2/13&-uv/13&0&0&0\\
 -uv/13&1+u^2/13&0&0&0\\
 0&0&1&0&0\\
 0&0&0&-1/33&0\\
 0&0&0&0&0
 \end{pmatrix},
\]

and the only nonzero leading gyro entries are
(G_1)_{TW}=-2/sqrt(11), (G_1)_{WT}=2/sqrt(11).
The frequency/growth pencil, not L_2 alone, determines the branches.
For nu=lambda/p, where a mode varies locally as exp(lambda*t),

\[
 \det(\nu^2I+\nu G_1+L_2)
 =\nu^2(\nu^2+1)^2
    \left(\nu^2+1+\frac{u^2+v^2}{13}\right)
    \left(\nu^2+\frac13\right).
\]

Consequently the four nonzero linear branches have speed squares
1,1,1+(u^2+v^2)/13,1/3. The negative TT entry alone is NOT a negative
frequency-square conclusion: its coupling through G_1 is essential.

The derived 1/3 frame-related coefficient agrees with the isolated
Einstein-aether Minkowski comparator evaluated at alpha_i=M_U^2*c_i/M_P^2,
not at bare c_i. The comparator is equation (3.4) of
[Oost, Mukohyama and Wang (2018)](https://arxiv.org/html/1802.04303v2).
No observational bounds from that paper were applied, and no H=0 gauge limit
was used as the derivation of the coupled B1 result.

## 3. Zero branch, propagation cones and limits

The zero root has algebraic multiplicity two but geometric multiplicity one
in the leading first-order matrix [[0,I],[-L_2,-G_1]]. Thus diagonalizability
of that principal system fails. The absence of a positive real leading
eigenvalue is not enough to establish a uniform evolution estimate.

This branch must be tracked into the original dust/frame constrained fields
and appropriate spatial regularity norms. The coordinate transformation
contains k, so a conclusion about every physical formulation or function
space cannot be inferred merely by declaring this chart definitive. Neither
an all-formulation no-go nor strong hyperbolicity is claimed here. The
leading generalized eigenvector and subleading dynamics remain the next
bounded well-posedness calculation. No pressure or damping term is added.

The wider formal condensate cone and quartic force dispersion also need a
preferred-time/causality and cutoff analysis. Faster phase/group propagation
than the matter cone is not by itself a demonstrated closed causal curve,
but it cannot be called ordinary relativistic luminal closure. All formulae
use the B1 reference units; its EFT hierarchy remains unestablished.

## 4. Numerical evidence and interpretation

The local-symbol check uses six times and physical p=(20,40,80,160); those p
values are not additional torus trajectories. At the largest p the maximum
relative discrepancy from the derived propagating coefficients is
0.0001011508696051752, below the frozen 0.05 bound. The first implementation's
0.08008268218651664 discrepancy is preserved, not silently relabelled as a pass.

The full 12x12 transfer matrix for (x,xdot) was evolved over [0,4] at 101 output
times for k=2*pi*n, with DOP853 and Radau at the frozen tolerances. All eight
integrations finish with finite values. Canonical symplectic checks use
pi=xdot+M_c*x and the correctly transformed initial canonical identity.

| n | Two-method normalized discrepancy | Maximum normalized symplectic residual | Maximum sampled chart amplification |
|---|---:|---:|---:|
| 1 | 6.64e-10 | 1.65e-10 | 20.576 |
| 2 | 2.76e-9 | 8.52e-11 | 57.174 |
| 4 | 1.54e-8 | 5.05e-11 | 222.498 |
| 8 | 7.29e-8 | 2.60e-11 | 887.311 |

The discrepancy threshold is 1e-5; the normalized symplectic threshold is
1e-6. These are accuracy checks, not observational or stability likelihoods.
The norm of (x,xdot) is chart dependent and unweighted by frequency: even a
stable oscillator can have a large value. No instability verdict follows
from the last column. The instantaneous finite-frequency generator also has
positive real exponents of order unity or smaller at the sampled times;
these are not the leading rate proportional to p or p^2. Their dust/Jeans,
background and transient interpretation is still open.

The receipt field formal_UV_growth_detected tests **exponential** leading
growth. Its false value does not exclude polynomial growth of the defective
zero branch or imply a well-posedness theorem.

## 5. Reproduction and preserved correction history

```
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_scalar_propagation.py
```

The [current receipt](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_summary.json)
pins its executable, S1 sources, matrix/symbol/transfer artifacts and all checks.
Its SHA-256 is
56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735.

Attempt 01's 49/52 failed receipt, original executable and all four artifacts
with sidecars remain in
`Analysis/MasterTests/outputs/r4c1_s2_attempt_01/`. Its receipt hash is
9d5c84aa198cf942795bd96e1bd9c723be10fc490682c85c4b3ef160fa232e76.
Three equality checks required exact normalization of unevaluated 0*sqrt(n);
no numeric tolerance was substituted. The separate leading-symbol omission
was a genuine implementation error and was corrected with new rejection
and characteristic-polynomial checks. It did not alter S1 or the integrated
equations. The failed attempt's execution flag is not authority to reuse its
failed findings. The later scoped register/report govern current use.

The old review packet contains neither S1 nor S2 and is not their review.
Inherit R9-MT1-S1/B1/VARIATION; register R9-MT1-S2 as DEFERRED. These formulas
may be used provisionally for the zero-branch and physical-domain diagnostics.
Claims of strong hyperbolicity, causality, full stability, a healthy GR limit,
physical weak-field matching or coefficient determination are not supported.

Next gate: a frozen zero-branch well-posedness/regularity diagnostic, retaining
the exact candidate action and testing the original constrained variables.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED. No reviewer dispatch, parameter retuning, commit or push.
