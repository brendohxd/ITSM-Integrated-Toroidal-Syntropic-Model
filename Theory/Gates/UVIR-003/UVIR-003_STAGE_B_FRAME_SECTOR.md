# UVIR-003 — Stage B, frame (aether) sector: coupled mode speeds

Status: **partial progress — frame sector only, via verified literature
substitution**

Does not close UVIR-003 Stage B. Does not touch the force (`psi`) sector or
the condensate (`Phi`) coupling. Advances Stage B roadmap items 1, 2, 5 and 6
(`UVIR-003_STAGE_A_REPORT.md` Section 8) for the frame-metric subsystem in
isolation.

## Executive result

Stage A's decoupled-limit frame speeds,

\[
c_{U,T}^2=\frac{c_1}{c_{14}},\qquad c_{U,L}^2=\frac{c_{123}}{c_{14}},
\]

were derived in frozen Minkowski space with the metric held fixed — they
omit the metric's own dynamical response to the aether. The full coupled
Einstein-aether linearized-wave problem (metric perturbation `h_{mu nu}` and
aether perturbation `v^mu` together) has been solved in the literature
already cited by the Stage-A report itself: Jacobson and Mattingly
([arXiv:gr-qc/0007031](https://arxiv.org/abs/gr-qc/0007031)) established the
framework, and Eling, Jacobson and Mattingly
([arXiv:gr-qc/0410001](https://arxiv.org/abs/gr-qc/0410001), hereafter EJM)
tabulate the closed-form spin-0/1/2 mode speeds (their Table 1). Rather than
re-derive the full linearized field equations from scratch tonight — a
large, error-prone undertaking — this note verifies the precise sign and
normalization dictionary between the Stage-A action and EJM's, and then
substitutes EJM's published result through that verified dictionary.

**The operator-label and sign dictionary is the identity map**, but the
coefficient normalization is not automatically identical. The explicit
minus sign on the Stage-A `c4` term cancels the signature flip in EJM.
However, EJM place the aether operators under the Einstein-Hilbert prefactor
`M_P^2/2`, while Stage A declares an independent `M_U^2/2` prefactor.
The EJM coefficients are therefore `alpha_i=(M_U^2/M_P^2)c_i`; bare
equality holds only if `M_U=M_P`. Both parts of the map are now checked
symbolically.

Substituting, and checking that EJM's exact formulas reduce to Stage-A's own
decoupled ratios in the weak-metric-coupling limit (Section 2) — which they
do — gives three results Stage A did not have:

1. a spin-2 (pure gravitational-wave) speed, `1/(1-c13)`, absent from Stage
   A's decoupling limit entirely, since gravity doesn't respond to the
   aether there;
2. exact (not small-`c_i`-approximate) spin-0 and spin-1 speeds;
3. literature no-ghost, energy-positivity and light-cone conditions on
   `c1,c2,c3,c4` (Section 3), sharper than Stage A's necessary-only
   `c14,c1,c123>0`.

## 1. Convention dictionary (verified)

EJM's action (their eq. 1-2, signature `+---`, unit constraint `u^au_a=1`):

\[
S=\frac{-1}{16\pi G}\int d^4x\sqrt{-g}\Big(R+K^{ab}{}_{mn}\nabla_au^m\nabla_bu^n+\lambda(u^au_a-1)\Big),
\]
\[
K^{ab}{}_{mn}=c_1g^{ab}g_{mn}+c_2\delta^a_m\delta^b_n+c_3\delta^a_n\delta^b_m+c_4u^au^bg_{mn}.
\]

Stage A's frame action (`UVIR-003_STAGE_A_REPORT.md` Section 3.2, signature
`-+++`, unit constraint `U^\mu U_\mu=-1`):

\[
\mathcal L_U=-\frac{M_U^2}{2}\Big[c_1(\nabla_\mu U_\nu)(\nabla^\mu U^\nu)+c_2(\nabla_\mu U^\mu)^2+c_3(\nabla_\mu U_\nu)(\nabla^\nu U^\mu)-c_4a_\mu a^\mu\Big]+\frac\lambda2(U^\mu U_\mu+1).
\]

Christoffel symbols (hence covariant derivatives of matching index type) are
invariant under a global signature flip `g -> -g`, since
`Gamma ~ g^{-1} d(g)` picks up two sign flips that cancel. Using an
arbitrary symbolic `nabla_a u^m` object and tracking explicit metric factors
through all four terms directly (`uvir003_frame_sector_speeds.py`):

- the `c1`, `c2`, and `c3` contractions are each independently verified to
  be unchanged by the signature flip;
- the `c4` contraction is independently verified to carry one net metric
  sign and therefore flips.

Stage A's declared bracket already carries an explicit extra minus sign on
its `c4` term that EJM's does not. That extra sign exactly cancels the
signature-induced flip, so the **operator labels and signs map identically between the two
conventions** — confirmed by direct symbolic substitution, not asserted by
inspection.
The independent mass prefactors still require the separate coefficient
normalization `alpha_i=(M_U^2/M_P^2)c_i`.

## 2. Coupled mode speeds (EJM Table 1, substituted)

Using `alpha_i=(M_U^2/M_P^2)c_i`, `alpha13=alpha1+alpha3`,
`alpha14=alpha1+alpha4` and `alpha123=alpha1+alpha2+alpha3`:

\[
\boxed{s_{\rm tensor}^2=\frac1{1-\alpha_{13}}}
\qquad\text{(spin-2, purely gravitational)}
\]

\[
\boxed{s_{\rm vector}^2=
\frac{\alpha_1-\tfrac12\alpha_1^2+\tfrac12\alpha_3^2}
{\alpha_{14}(1-\alpha_{13})}}
\qquad\text{(spin-1, transverse aether-metric)}
\]

\[
\boxed{s_{\rm scalar}^2=
\frac{\alpha_{123}(2-\alpha_{14})}
{\alpha_{14}(1-\alpha_{13})(2+\alpha_{13}+3\alpha_2)}}
\qquad\text{(spin-0, longitudinal/trace)}
\]

**Consistency check against Stage A.** Scaling `c1,c2,c3,c4 -> eps*(c1,c2,c3,c4)`
uniformly and taking `eps -> 0+` (EJM's stated "`c_i` small compared to
unity" regime — verified in the script that all four coefficients must scale
together; scaling only `c1,c3` and leaving `c2,c4` fixed does not reduce
correctly, see `Theory/Gates/RECOVERY_SESSION_WORKLOG.md`, 2026-07-24):

\[
s_{\rm vector}^2\to\frac{c_1}{c_{14}}=c_{U,T}^2,
\qquad
s_{\rm scalar}^2\to\frac{c_{123}}{c_{14}}=c_{U,L}^2.
\]

Exact match to Stage A's decoupled-limit speeds. This is a nontrivial check:
it confirms Stage A's frozen-metric approximation is the correct
weak-metric-coupling limit of the full coupled system, not an unrelated or
inconsistent simplification.

## 3. Conditions on `alpha1,alpha2,alpha3,alpha4` (EJM, quoted)

No exponentially growing modes (real frequency for real wavevector), small-
`alpha_i` regime:

\[
c_1/c_{14}\ge0,\qquad c_{123}/c_{14}\ge0.
\]

Linearized energy positivity (exact, not small-`alpha_i`):

\[
\frac{2\alpha_1-\alpha_1^2+\alpha_3^2}{1-\alpha_{13}}>0
\quad\text{(vector)},\qquad
\alpha_{14}(2-\alpha_{14})>0\quad\text{(scalar/trace)}.
\]

All modes lie on the metric light cone iff
`alpha4=0, alpha3=-alpha1, alpha2=alpha1/(1-2alpha1)`.

These are strictly sharper than Stage A's own necessary-only conditions
(`c14,c1,c123>0`, Section 5 of the Stage-A report) — Stage A's conditions are
necessary for the decoupled-limit speeds to be real and non-negative, but
say nothing about the exact energy-positivity bounds above, nor about the
spin-2 sector at all.

## 4. Causality note (ties to `UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md`)

EJM's own discussion (Section 4.1 of their review) directly addresses the
causality question for this class of theory, and is worth quoting exactly
because it substantiates — with a citable primary source — the specific
mechanism behind Stage A's already-listed "not established: a covariant
regulator valid on accelerating or vortical frame backgrounds":

> "there is nothing wrong with local superluminal propagation in a
> Lorentz-violating theory, [Lim] pointed out that the vector field (in an
> inhomogeneous background) might tilt in such a way as to allow energy on
> such locally superluminal paths to flow around a closed spacetime curve."

EJM do not resolve this either way for the general theory ("It is not clear
to us that it is really necessary to impose this extra demand..."). This
means the open item is not merely academic caution on Stage A's part — it is
a live, specifically-identified mechanism (aether tilting on an inhomogeneous
background) in the literature this project already cites, and it is the same
mechanism that would need to be checked before the force-sector
superluminality found in the causality addendum could be called safe on
general (non-frozen) backgrounds.

## 5. What remains open

- the force sector (`psi`, `K_Q,A,gamma`) has not been coupled into this
  SVT decomposition at all — this note is frame-metric only;
- the condensate (`Phi`) sector and its current-alignment coupling to `U`
  are likewise untouched here;
- this result is a verified **literature substitution**, not an independent
  from-scratch linearized-Einstein-equation derivation on the ITSM side;
  a from-scratch check would be a valuable independent cross-check but was
  not attempted tonight, to avoid introducing a fresh, unverified
  multi-page tensor calculation without a second check on it;
- the accelerating/vortical (non-frozen) background case, where EJM's own
  causality caveat (Section 4 above) actually bites, is not covered by this
  linear-flat-background calculation any more than it was by Stage A.

## 6. Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_frame_sector_speeds.py
```

Expected footer:

```text
UVIR-003 Stage B frame-sector mode speeds: literature substitution VERIFIED
Consistency with Stage-A decoupled limit: CONSISTENT
STATUS: PARTIAL_PROGRESS_FRAME_SECTOR_ONLY
```
