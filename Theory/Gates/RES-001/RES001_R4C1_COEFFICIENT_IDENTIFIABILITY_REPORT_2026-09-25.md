# R4C1-C1: a physical coefficient remains invisible to background matching

Date: 2026-09-25. Owner: Master Test 3; conditional Test-2 consequence.
Action R4C1-v1 unchanged. Gate effect NONE. Executable checks: 63/63.

**Disposition:** `CLASSICAL_BACKGROUND_AND_LINEAR_DATA_DO_NOT_IDENTIFY_SPATIAL_FORCE_COEFFICIENT`.
This is a structural nonidentifiability result for the specified classical
branch, not a rejection of every parent or an observational exclusion.

## 1. Question and result

Within the [frozen action](RES001_R4C1_ACTION_FREEZE_2026-09-25.md), change
only the positive coefficient A of -A Y^(3/2). Keep K_Q, beta, the frame,
reservoir, potentials, initial conditions and T3 periods fixed. The
[C1 contract](RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_CONTRACT_2026-09-25.md)
was frozen before the executable; no observed acceleration enters execution.

On the homogeneous, spatially aligned branch:

- The complete background equations and their solutions do not depend on A.
- Their classical pre-constraint quadratic action also does not depend on A.
- The normalized nonlinear spatial operator does depend on A. The variation
  is not a field-coordinate change, a boundary term or a change of topology.

Consequently these background/linear data alone cannot uniquely match that
operator to the cosmological expansion. An additional microscopic or
nonlinear physical condition is required. Selecting a desired C_chi and
solving backward for A is parameter assignment, not prediction.

The matching implication is distinct from the previous static reference-a0
rescaling redundancy: here the canonically normalized action genuinely
changes. No claim is made that all these parameter choices have a healthy
EFT, or that the full galaxy response has been calculated.

## 2. Direct covariant check, not absence from a parameter list

The action defines n=U/sqrt(-U^2), h^{mu nu}=g^{mu nu}+n^mu n^nu and
Y=h^{mu nu} partial_mu psi partial_nu psi. For a homogeneous psi and
aligned timelike n, the projected spatial gradient vanishes and Y=0.

The executable evaluates the full normalized-projector variation on a
homogeneous metric with arbitrary positive lapse, scale factor and off-unit
timelike length. It checks the A derivative of every component of the
Lagrangian blocks, frame algebraic equation, connection momentum, algebraic
metric variation and connection-stress tensor. All vanish exactly. The
cubic force flux -3 A sqrt(Y) h^{mu nu} partial_nu psi also vanishes.
The covariant first variations are finite; no coupling division is used.
An unnormalized-projector mutation fails the corresponding test.

Both B1 interface currents retain their established form:

\[
Q_{mp}^{\nu}=\beta T_m\nabla^\nu\psi,\qquad
Q_{syn}^{\nu}=-\frac{g_r s r}{2}\nabla^\nu r.
\]

They remain nonzero during the interacting control, but contain no A at
fixed fields. The conserved charge likewise supplies no A matching equation.
This is consistent with the full variation and background derivations; it
is not inferred only from the numerical ODE ignoring a parameter.

## 3. Why linear stability equations cannot supply the missing coefficient

In a local orthonormal spatial frame write the projected gradient as q and
f(q)=A|q|^3. For q nonzero,

\[
\partial_i f=3A|q|q_i,\qquad
\partial_i\partial_j f=3A\left(|q|\delta_{ij}+\frac{q_iq_j}{|q|}\right).
\]

The Hessian eigenvalues are 6A|q| along q and 3A|q| transversely. Its
operator norm tends to zero from every direction. Thus f is C2 with zero
gradient and Hessian at q=0. Along a line its two third derivatives are
+6A and -6A, so it is not C3 there. A singular derivative with respect to
the intermediate scalar Y is not a divergent physical field-space Hessian.

The normalized timelike chart and local spatial frame are smooth. Applying
the chain rule to q(fields), and including the volume element, therefore
gives no term of order zero, one or two from this operator around q=0.
This includes metric, frame and force perturbations. Replacing the operator
by A|q|^2 would give a nonzero quadratic Hessian and is rejected as a mutation.

The result is about A-dependence, not a computation of the other quadratic
blocks or a proof they are healthy. Any regular linear constraint reduction
inherits this independence. A singular block requires its own analysis;
one cannot invert it or infer a reduced spectrum here. Nonlinear backgrounds
and quantum corrections may depend on A. No radiative stability is claimed.

## 4. Physical distinction and periodic topology

Under a positive field-chart change psi_new=sigma psi and z_new=sigma z,

\[
K_{Q,\mathrm{new}}=K_Q/\sigma^2,\quad A_{\mathrm{new}}=A/\sigma^3,
\quad b_{\mathrm{new}}=b/\sigma^2,\quad\beta_{\mathrm{new}}=\beta/\sigma.
\]

The invariant couplings are A/K_Q^(3/2), b/K_Q and beta/sqrt(K_Q).
Changing A alone changes the first invariant with the others held fixed;
it cannot be undone by that chart freedom. The auxiliary regulator terms
transform consistently with z_new=sigma z.

For a fixed periodic probe psi=d cos(kx), d>0 and k=2 pi |n|/L, n nonzero,
the mean static force energy density on flat T3 is

\[
\overline{\mathcal E}_{\psi}
=\frac{4A d^3 k^3}{3\pi}+\frac{b d^2 k^4}{4}.
\]

The first term changes with A at unchanged period, mode number, amplitude,
K_Q and matter coupling. Its nonzero integral cannot be a periodic surface
term. This explicitly tests T3 compatibility, but is an off-shell probe,
not a self-consistent matter/metric solution. Mode quantization has not
supplied a value for the operator coefficient.

## 5. Conditional weak-field normalization, with regulator kept explicit

In the local static, frozen-frame reduction, with positive beta and weak
matter potentials, the force action is

\[
\mathcal L_{\mathrm{stat}}=-A|\nabla\psi|^3
-\frac b2(\Delta\psi)^2-\beta\rho\psi.
\]

Direct variation gives

\[
3A\nabla\cdot(|\nabla\psi|\nabla\psi)-b\Delta^2\psi=\beta\rho.
\]

For spherical q=d psi/dR>0, regular central flux and an enclosed source M,

\[
4\pi R^2\left[3Aq^2-b\frac{d}{dR}\left(q'+\frac{2q}{R}\right)\right]
=\beta M(<R).
\]

Only when the regulator is subleading does the exterior leading expression
become

\[
q_0=\frac{D}{R},\qquad D=\sqrt{\frac{\beta M}{12\pi A}},\qquad
g_\psi=\beta q_0.
\]

Substituting this profile into the full integrated flux gives regulator
contribution 2bD/R, compared with cubic contribution 3AD^2. The required
small ratio is 2b/(3ADR), not a ratio to the vanishing exterior divergence
of the leading cubic flux. Thus finite b was not silently set to zero.
Weak potential, negligible time/frame response, controlled metric
backreaction, R small relative to the cosmological/box scales and a
compensated local source are additional assumptions. No common domain
satisfying them has yet been proved for B1. A global isolated positive
source on empty T3 is not admitted.

Writing g_bar=G_static M/R^2 gives the conditional dynamic scale

\[
\boxed{a_{\mathrm{dyn}}\equiv\frac{g_\psi^2}{g_{\mathrm{bar}}}
=\frac{\beta^3}{12\pi G_{\mathrm{static}}A}}.
\]

G_static must not be silently replaced by bare G; the
[G1 audit](RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md) distinguished them.
In natural units [G_static]=-2 and [A]=1, so [a_dyn]=1 as required.
For the proposed notation g_psi=C_proj sqrt(g_bar a0), this fixes only
a_dyn=C_proj^2 a0. C_proj remains unknown, not 2/3 by assumption.

The underlying nonlinear-Poisson variational form has the familiar
nonrelativistic precedent in [Bekenstein and Milgrom (1984), section II](https://articles.adsabs.harvard.edu/pdf/1984ApJ...286....7B).
That precedent is not an ITSM coefficient derivation. The present numerical
normalization comes from the displayed R4C1 action, not a literature fit.

## 6. Registered background comparison and target-assignment rejection

The three DOP853 controls use unchanged B1 inputs except A, on [0,4] with
rtol=1e-11, atol=1e-13 and 801 samples. Each completes with finite states.

| A/A_B1 | Maximum normalized state/current difference | A/K_Q^(3/2) ratio | Conditional force-amplitude ratio | Conditional a_dyn ratio |
|---:|---:|---:|---:|---:|
| 1/4 | 0 / 0 | 1/4 | 2 | 4 |
| 1 | 0 / 0 | 1 | 1 | 1 |
| 4 | 0 / 0 | 4 | 1/2 | 1/4 |

All sampled state arrays are exactly equal. Each has maximum normalized
Friedmann residual 3.408907498308431e-12, charge drift
1.8791856959410325e-11 and dust-integral drift 2.8703150967146485e-12.
The positive sensitivity control K_Q -> 4 K_Q changes the trajectory by
0.01656658471876225 in the same normalized state norm. Repeating an identical
ODE is a degeneracy control, not independent integrator validation. The
covariant and field-space arguments establish the structural result.

The homogeneous Einstein-frame H(t), its derivative and the fields are
identical across A. Conversion to the same conformal matter frame cannot
remove this degeneracy: its scale factor C a and proper time d tau=C dt
also use identical C=exp(beta psi). This is not a calibrated H0 prediction.

In the conditional static normalization, holding H and C_proj fixed gives
C_chi=a_dyn/(C_proj^2 H) proportional to 1/A (c=1). Any specified positive
target C_* can be imposed by assigning

\[
A_* =\frac{\beta^3}{12\pi G_{\mathrm{static}}C_{\mathrm{proj}}^2 H C_*}.
\]

The executable checks this inverse assignment for the four registered
comparators 1, 2 pi, 1/(2 pi), and sqrt(1-q_dec)/(2 pi) with q_dec<1.
It selects none. The real positive domain of the fourth comparator is
explicit; its boundary or a complex value is not silently continued.
There is no independently derived fifth coefficient to compare and no
observational ranking. A required redshift law a0(z) also remains unproved:
the physical local/background matching and projection factor are missing.

## 7. Reproduction and scientific disposition

```powershell
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_03_r4c1_coefficient_identifiability.py
```

Use the full itsm_env interpreter path for both python arguments if needed.

- Contract SHA256: `29f54fbef62d6a2b2a5d29d772633a87694a9ed1d05f7b00244833b88075465d`.
- Executable SHA256: `ae5e6c363a22b2a3d2fc88f0aaf19f946b1d07d3c06cf9c55696f418a5392d45`.
- Receipt: `Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json`.
- Receipt SHA256: `49b10df599d6158f02ae6e55febe054f5b6fe2e3a2b53ee70daf7196f44d2fcf`.

The first implementation passed 60 checks; three further exact checks made
the spherical regulator flux and its approximation condition explicit.
No input, threshold, or coefficient was retuned. The final 63-check receipt
is reproduced byte for byte, and each of its five deliberately altered
expected dependency hashes is rejected before receipt overwrite.

This rejects the inference that the R4C1 homogeneous background plus its
classical linear equations uniquely predict the nonlinear force coefficient.
It does not reject every value of A, every viable parent, or the possibility
of matching from further microscopic/nonlinear physics. A condition that
only identifies an allowed interval of A would still not derive a unique
number; it must break this physical degeneracy without inserting a target.

The analyst has already seen historical and observational context. This is
target-independent algebra, not fresh analyst blinding or independent peer
review. Historical reconstruction remains parked. Tests 1-3 and the full
goal remain incomplete; no conditional result is promoted to canonical
Derived status. The ITSM provenance discipline preserves that distinction.

MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; Rule9 NOT_CLEARED; physics_pass=false; gate_effect=NONE.
No TOP-X4 change, paid reviewer dispatch, commit, push or publication.
