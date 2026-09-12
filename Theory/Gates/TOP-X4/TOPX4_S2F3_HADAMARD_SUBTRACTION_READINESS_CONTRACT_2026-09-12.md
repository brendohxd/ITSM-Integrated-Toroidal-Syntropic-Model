# TOP-X4 `X4-S2F3` Hadamard/subtraction readiness contract

**Frozen:** 2026-09-12  
**Reasoning mode:** Max  
**Checkpoint class:** bounded Plan-11 subtraction scaffold and readiness audit  
**Authority effect:** none unless a later, separately reviewed gate says otherwise

## 1. Purpose and stop boundary

This contract freezes the next single TOP-X4 checkpoint after the exact
scalar/Dirac transport retry. The checkpoint may derive and test the universal
five-dimensional Hadamard and heat-kernel subtraction scaffold. It must also
audit whether the frozen `X4-S2F3` evidence pack supplies every operator and
state needed to use that scaffold.

The checkpoint does **not** compute a renormalized stress tensor. A successful
scaffold audit is compatible with, and expected to produce, a readiness
decision of `HOLD`. No mode integral, background update, Hessian, A4 task,
Ultra task, architecture claim or publication promotion is authorized.

## 2. Owning authorities

The executable must verify the checked-in SHA-256 sidecars for:

1. `TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md`;
2. `TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md`;
3. `TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md`;
4. the Plan-11 `PLAN.md`;
5. the finite-charge operator output whose scope stops before an evolving
   state, gravity constraints and the physical Hessian;
6. the failed dynamic-state output and its preserved low-mode evidence;
7. the exact-transport output that immediately owns this transition; and
8. the static determinant output whose Poisson `q=0` subtraction is bounded
   to the static zero-density control.

Any missing or mismatched authority receipt is a checkpoint failure.

## 3. Universal five-dimensional local scaffold

Use the Euclidean local operator convention

\[
 P=-\left(G^{AB}{\cal D}_A{\cal D}_B+E\right),\qquad
 \Omega_{AB}=[{\cal D}_A,{\cal D}_B].
\]

For a smooth five-dimensional manifold without boundary, write

\[
 \operatorname{Tr}e^{-sP}\sim
 \frac{1}{(4\pi s)^{5/2}}\int d^5x\sqrt{G}\,
 \operatorname{tr}\left[b_0+s b_1+s^2 b_2+O(s^3)\right],
\]

with

\[
 b_0=I,
 \qquad b_1=E+\frac16 RI,
\]

and

\[
\begin{aligned}
 b_2={}&\frac12E^2+\frac16RE+\frac1{12}\Omega_{AB}\Omega^{AB}\\
 &+I\left(\frac1{72}R^2-\frac1{180}R_{AB}R^{AB}
 +\frac1{180}R_{ABCD}R^{ABCD}\right)\\
 &+\frac16\Box E+\frac1{30}(\Box R)I.
\end{aligned}
\]

Here `b_0,b_1,b_2` are the DeWitt-indexed coefficients corresponding to
`a_0,a_2,a_4` in the common heat-kernel indexing. The distinction must be
recorded explicitly. Integrated total derivatives may be removed only after
the no-boundary/falloff assumptions are declared; they may not be silently
dropped from a local point-split stress calculation.

With a proper-time lower cutoff `s >= Lambda^-2`, the local five-dimensional
power structure is

\[
 \Gamma_{\rm even}^{\rm div}\propto
 \frac{1}{(4\pi)^{5/2}}\int d^5x\sqrt{G}\,\operatorname{tr}
 \left[\frac25\Lambda^5b_0+\frac23\Lambda^3b_1+2\Lambda b_2\right],
\]

up to the field-statistics and determinant prefactors. There is no bulk
logarithmic term for a smooth boundaryless five-dimensional operator of
Laplace type. This statement does not remove finite renormalization ambiguity.

## 4. Scalar Hadamard control

For one scalar operator `Box-m^2-xi R`, the required five-dimensional local
singular control is

\[
 G^F_{\rm sing}(x,x')=
 \frac{i}{16\sqrt{2}\pi^2}
 \frac{U(x,x')}{[\sigma(x,x')+i\epsilon]^{3/2}},
 \qquad U=U_0+U_1\sigma+U_2\sigma^2+O(\sigma^3).
\]

The coincidence controls are

\[
 u_0=1,
 \qquad u_1=-m^2-(\xi-1/6)R,
\]

\[
\begin{aligned}
 u_2={}&-\frac12m^4-(\xi-1/6)m^2R
 +\frac16(\xi-1/5)\Box R
 -\frac12(\xi-1/6)^2R^2\\
 &+\frac1{180}R_{AB}R^{AB}
 -\frac1{180}R_{ABCD}R^{ABCD}.
\end{aligned}
\]

The regular biscalar `W(x,x')` carries state dependence. Therefore, matching
the local `U` coefficients is necessary but not sufficient for a state or
stress-tensor claim. The scalar formula is a control only: it may not be
copied component by component into the interacting charged-scalar/`chi`
system without deriving that system's full matrix `E`, bundle connection and
parallel transport before the homogeneous ansatz.

## 5. Counterterm map boundary

For a free massive scalar, the purely gravitational dimension-five ambiguity
basis is represented by

\[
 m^5,\quad m^3R,\quad mR^2,\quad
 mR_{AB}R^{AB},\quad mR_{ABCD}R^{ABCD}.
\]

Equivalently, a cutoff treatment requires independent local coefficients for
`1`, `R`, `R^2`, `R_AB R^AB` and `R_ABCD R^ABCD`. In five dimensions the last
curvature-squared term cannot be removed by treating the four-dimensional
Euler density as topological.

This gravitational basis is not the complete `X4-S2F3` counterterm map. The
off-shell charged-scalar/`chi` matrix endomorphism contributes through
`tr(E)`, `tr(E^2)` and, if nontrivial, `tr(Omega_AB Omega^AB)`. Those terms must
be expanded against the frozen masses, quartics, portal and background fields
to identify every matter counterterm and normalization condition. The map is
`NOT_DERIVED` until that covariant second variation exists.

The smooth unorbifolded circle has no fixed points or internal boundary and
therefore no boundary or brane heat-kernel coefficients. Falloff in the
noncompact directions remains an explicit assumption. Poisson removal of the
decompactified `q=0` image isolates the finite topology-dependent static
Casimir term; it is not a substitute for local covariant subtraction of an
evolving, state-dependent stress tensor.

## 6. Field-by-field completion inventory

Stress readiness requires all of the following in compatible conventions:

1. the full covariant matrix second-variation operator for the two real
   components of `Phi` coupled to `chi`, derived before the homogeneous and
   fixed-charge reductions;
2. matrix/bundle Hadamard coefficients or an equivalent infinite-order
   pseudodifferential/adiabatic state construction for the scalar sector;
3. the five-dimensional Dirac operator, its parity-even squared Laplace-type
   operator and a spinor Hadamard two-point function;
4. a gauge-fixed graviton Hessian on the finite-charge curved background,
   including the Faddeev-Popov/Jacobian operators and zero-mode prescription;
5. the parity-odd phase/global-anomaly and quantized-counterterm audit, which
   is not encoded by the squared Dirac operator; and
6. normalization conditions for every gravitational and matter counterterm,
   followed by regulator-, scale-, state-order- and resolution-stability
   checks.

Exact symplectic scalar transport and a first-order Dirac projector do not by
themselves establish the Hadamard wavefront condition. A flat-background
count of five physical graviton polarizations is not a curved gauge-fixed
graviton determinant.

## 7. Preregistered executable checks

The script must independently test:

1. all authority and input sidecars;
2. the `D=5` singular exponent and normalization;
3. the required `U_0,U_1,U_2` depth and scalar coincidence coefficients;
4. the absence of a bulk logarithmic heat-kernel divergence on the smooth
   boundaryless five-dimensional control;
5. the general `b_0,b_1,b_2` coefficient map, including `E`, `Omega` and both
   independent Ricci/Riemann contractions;
6. the `Lambda^5,Lambda^3,Lambda` proper-time powers and dimensions;
7. the five independent pure-gravity local terms and their dimensions;
8. the boundary between static `q=0` subtraction and local state-dependent
   stress renormalization;
9. the exact-transport output's declared finite-order and non-Hadamard status;
10. the current field-by-field completion inventory; and
11. an observational-target firewall.

At least five rejecting mutations must be included: add a five-dimensional
bulk logarithm, omit `R_ABCD R^ABCD`, treat `q=0` subtraction as full stress
renormalization, promote a finite-order state to Hadamard, and omit the
graviton ghost/Jacobian sector.

## 8. Decision rule

The bounded status may be

`PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS`

only if every universal/scaffold check and every fail-closed inventory check
passes. That status means the audit correctly identifies the usable local
structure and the missing prerequisites. It must be accompanied by:

- `calculation_status=PASS`;
- `hadamard_stress_ready=false`;
- `renormalized_stress=NOT_COMPUTED`;
- `physics_pass=false`;
- `gate_effect=NONE`;
- no advance to a semiclassical background, Hessian, A4 or Ultra; and
- `THREE_WAY_CLEARANCE_NOT_MET` until genuinely independent reports exist.

Any algebraic, dimensional, receipt, mutation or firewall failure produces
`FAIL_HADAMARD_SUBTRACTION_READINESS_CHECKPOINT`. Even a scaffold pass cannot
change any canonical scientific claim.

## 9. Primary-source controls

- Decanini and Folacci, *Hadamard renormalization of the stress-energy tensor
  for a quantized scalar field in a general spacetime of arbitrary dimension*,
  arXiv:gr-qc/0512118.
- Vassilevich, *Heat kernel expansion: user's manual*,
  arXiv:hep-th/0306138.
- Hollands, *The Hadamard Condition for Dirac Fields and Adiabatic States on
  Robertson-Walker Spacetimes*, arXiv:gr-qc/9906076.
- Junker and Schrohe, *Adiabatic vacuum states on general spacetime manifolds*,
  arXiv:math-ph/0109010.
- Gerard and Wrochna, *Construction of Hadamard states by pseudo-differential
  calculus*, arXiv:1209.2604.
- Gerard and Stoskopf, *Hadamard states for quantized Dirac fields on
  Lorentzian manifolds of bounded geometry*, arXiv:2108.11630.

The cited Dirac papers provide structural microlocal and pseudodifferential
controls, but their stated constructions are four- or even-dimensional. They
do not by themselves supply the required five-dimensional `X4-S2F3` spinor
Hadamard state. A dimension-appropriate derivation or justified extension
remains part of the open Dirac prerequisite.
