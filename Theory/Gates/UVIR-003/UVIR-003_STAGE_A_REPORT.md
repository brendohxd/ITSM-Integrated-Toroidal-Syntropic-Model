# UVIR-003 — Preferred-frame action and stability gate, Stage A

Stage-A status: **PASS**

Full UVIR-003 status: **IN PROGRESS**

Architecture decision: **independent dynamical `U^mu` with condensate-current alignment**

Regulator status: **conditional pass in the flat decoupling limit**

MAT-001: **BLOCKED**

## Executive result

The literature identified for UVIR-003 supplies a valid methodology, but it
also forces a sharper architecture decision than the initial action template
made. The preferred frame cannot simultaneously be

1. defined algebraically by the condensate current, and
2. varied as an independent Einstein-aether field

without double-counting its degrees of freedom.

Stage A chooses an independent, constrained unit timelike vector `U^mu`. It is
coupled to the condensate through a positive alignment energy rather than an
algebraic identity. This permits the complete four-operator two-derivative
Einstein-aether basis and preserves the option of relative condensate/frame
dynamics.

For the resulting decoupled flat-background sectors, the calculation derives:

\[
c_{14}>0,\qquad c_1>0,\qquad c_{123}>0
\]

as necessary frame-sector conditions in the convention declared below, and

\[
K_Q>0,\qquad A>0,\qquad \gamma>0
\]

as necessary conditions for the regulated force scalar.

The proposed higher-spatial-derivative term changes the zero-gradient force
dispersion from a missing spatial operator to

\[
\omega^2=\frac{\gamma}{K_QM_*^2}k^4.
\]

It therefore passes the limited zero-gradient test for a frozen Minkowski
metric and constant frame. This is not yet a strong-coupling proof, a covariant
constraint analysis, or evidence that the regulator is technically natural.
The full gate remains open.

## 1. Primary-source methodology

The source chain has five distinct jobs.

### 1.1 Two-sector motivation

[Mistele](https://arxiv.org/abs/2009.03003) identifies the conflict that occurs
when one phonon both carries a substantial equilibrium superfluid density and
mediates the long-range MOND-like force. The proposed two-field split supports
the UVIR-002 division of labor. It does not derive the ITSM force operator.

### 1.2 Full coupled perturbation method

[Skordis and Zlosnik](https://arxiv.org/abs/2007.00082) provide a relativistic
metric-vector-scalar precedent and report a quadratic action without ghost
instabilities. Their detailed
[Minkowski stability analysis](https://arxiv.org/abs/2109.13287) eliminates
constraints with Hamiltonian methods and exposes a nonpropagating mode whose
Hamiltonian can be unbounded in a low-momentum range. The direct lesson is that
signs read from a frozen force scalar are necessary but never sufficient.

### 1.3 Preferred-frame operator basis

[Jacobson and Mattingly](https://arxiv.org/abs/gr-qc/0007031) and the
[Einstein-aether review](https://arxiv.org/abs/gr-qc/0410001) supply the
generally covariant unit-vector framework. The early restricted derivative
action developed gradient singularities, which is a concrete warning against
removing symmetry-allowed frame operators before the stability calculation.

Modern black-hole perturbation analyses use an aether-orthogonal frame and
derive kinetic matrices, propagation speeds and no-ghost conditions for the
coupled modes
([arXiv:2407.00287](https://arxiv.org/abs/2407.00287),
[arXiv:2107.08061](https://arxiv.org/abs/2107.08061)). These are downstream
applications, but their decomposition principle is relevant to the full
UVIR-003 calculation.

### 1.4 Strong-coupling warning

[Blas, Pujolas and Sibiryakov](https://arxiv.org/abs/1007.3503) show that
projectability and the available preferred-frame operators decide whether the
scalar mode is unstable, strongly coupled or healthy. UVIR-003 therefore begins
with the complete two-derivative frame basis instead of a one-contraction toy
action.

### 1.5 Candidate zero-gradient regulator

[Motohashi and Mukohyama](https://arxiv.org/abs/1912.00378) show in a different
degenerate scalar-tensor setting that controlled higher-spatial-derivative
detuning can produce

\[
\omega^2=\alpha k^4/M^2
\]

and restore weak coupling about a timelike-gradient background. This is a
mechanism to test, not a proof that the same result carries over to the
nonanalytic ITSM cubic sector.

The relativistic/nonrelativistic distinction remains guarded by the review of
[Favero and Bernardo](https://arxiv.org/abs/2410.18214). Static `p=3` Laplacian
regularity literature such as
[Durastanti](https://arxiv.org/abs/1805.05136) belongs primarily to the static
PDE problem and cannot replace a dynamical stability analysis.

## 2. The frame decision

The condensate Noether current is

\[
J_\Phi^\mu
=i\left(\Phi^*\nabla^\mu\Phi
-\Phi\nabla^\mu\Phi^*\right).
\]

On a timelike nonzero-current branch one may define

\[
\widehat U^\mu
=\frac{J_\Phi^\mu}
{\sqrt{-J_{\Phi\nu}J_\Phi^\nu}}.
\]

That construction is valid as a derived velocity in the condensate sector.
However, substituting it into a kinetic action containing `nabla U` produces
higher-derivative operators of `Phi`; it does not create an independent vector
degree of freedom. Varying both `Phi` and an ostensibly independent `U` while
also imposing `U=U_hat[Phi]` would be redundant unless a precise constrained
parent action were supplied.

Stage A therefore adopts:

> `U^mu` is an independent unit timelike field. The condensate current is
> dynamically aligned with it but is not identical to it.

This is a provisional microscopic choice. It expands the ITSM field content and
must earn that cost through the full stability and phenomenology gates.

## 3. Declared Stage-A action

Use signature `(-,+,+,+)` and

\[
S_A=S_{\rm EH}+S_\Phi+S_U+S_{\rm align}+S_\psi+S_m.
\]

The reservoir is irrelevant to the local Minkowski Stage-A calculation and is
not deleted from the complete architecture. This is a controlled truncation,
not yet a complete `Phi`-`U`-`psi` mixing census. Apart from current alignment
and the appearances of `U` in `Q`, `Y` and `Delta_U`, additional mixing
operators are deferred to Stage B and must be classified by the declared
`U(1)`, force-field shift, parity and derivative assumptions.

### 3.1 Condensate

`S_Phi` is the finite-density complex condensate sector already audited in
UVIR-001. It retains the density, amplitude, circulation and defect roles. It
is not assigned the spatial cubic force operator.

### 3.2 Independent unit frame

Define

\[
a_\mu=U^\nu\nabla_\nu U_\mu
\]

and

\[
\begin{aligned}
\mathcal L_U=-\frac{M_U^2}{2}\big[&
c_1(\nabla_\mu U_\nu)(\nabla^\mu U^\nu)
+c_2(\nabla_\mu U^\mu)^2\\
&+c_3(\nabla_\mu U_\nu)(\nabla^\nu U^\mu)
-c_4a_\mu a^\mu\big]
+\frac{\lambda}{2}(U^\mu U_\mu+1).
\end{aligned}
\]

All four two-derivative contractions are retained. Sign conventions for the
`c_i` differ across the literature; every condition in this report refers to
the displayed action.

### 3.3 Current alignment

Let

\[
h_{\mu\nu}=g_{\mu\nu}+U_\mu U_\nu
\]

and use

\[
\mathcal L_{\rm align}
=-\frac{\zeta}{2}h_{\mu\nu}J_\Phi^\mu J_\Phi^\nu,
\qquad \zeta>0,
\]

where `zeta` carries the dimensions required by the normalization of `J_Phi`.
This term penalizes current transverse to the frame without imposing equality
as an algebraic constraint.

### 3.4 Force sector

Use unnormalized invariants

\[
\mathcal Q=U^\mu\nabla_\mu\psi,
\qquad
\mathcal Y=h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi.
\]

The Stage-A force action is

\[
\mathcal L_\psi
=\frac{K_Q}{2}\mathcal Q^2
-A\mathcal Y^{3/2}
-\frac{\gamma}{2M_*^2}(\Delta_U\psi)^2.
\]

For the existing weak-field normalization,

\[
A=\frac{C_{\rm IR}}{12\pi G a_0}.
\]

`Delta_U` denotes the spatial Laplacian in the constant, hypersurface-orthogonal
Stage-A frame. Its generally covariant completion on a frame with acceleration,
shear or vorticity is not yet fixed. Calling the displayed term fully covariant
outside this restricted background would be premature.

No canonical `-B Y/2` term is inserted. Such a term would dominate the cubic
as `Y -> 0` and destroy the intended asymptotic square-root branch. Explaining
why it is absent or suppressed is part of the technical-naturalness burden.

## 4. Alignment calculation

In flat spacetime write, to the required order,

\[
U^\mu=(\sqrt{1+\mathbf u^2},\mathbf u),
\qquad
J_\Phi^\mu=(n,\mathbf j).
\]

Then

\[
h_{\mu\nu}J_\Phi^\mu J_\Phi^\nu
=J_\Phi^2+(U\cdot J_\Phi)^2
=|\mathbf j-n\mathbf u|^2+\mathcal O(3).
\]

Therefore `zeta>0` gives positive energy for relative current. It aligns the
two sectors while preserving an independent relative mode. The coupled
relative-mode eigenfrequency is not calculated until the condensate and aether
constraints are included together.

## 5. Frozen-metric frame calculation

Set

\[
g_{\mu\nu}=\eta_{\mu\nu},
\qquad U^\mu=(1,\mathbf u)+\mathcal O(u^2).
\]

The unit constraint removes the linear `u^0` perturbation. Define

\[
c_{14}=c_1+c_4,
\qquad
c_{123}=c_1+c_2+c_3.
\]

The quadratic decoupled frame action has time coefficient

\[
M_U^2c_{14},
\]

transverse spatial coefficient

\[
M_U^2c_1,
\]

and longitudinal spatial coefficient

\[
M_U^2c_{123}.
\]

Thus necessary flat-decoupling conditions are

\[
\boxed{c_{14}>0,\qquad c_1>0,\qquad c_{123}>0.}
\]

The corresponding decoupled speeds are

\[
c_{U,T}^2=\frac{c_1}{c_{14}},
\qquad
c_{U,L}^2=\frac{c_{123}}{c_{14}}.
\]

These are not the full Einstein-aether propagation speeds. Metric mixing
changes the kinetic and gradient matrices and introduces the spin-2 sector.
Observational restrictions such as the gravitational-wave speed constraint are
also outside this necessary-condition audit.

## 6. Regulated force calculation

Let a local galactic background have

\[
\nabla\bar\psi=\mathbf v,
\qquad |\mathbf v|=q.
\]

For the cubic spatial energy

\[
E=A|\mathbf v+\nabla\pi|^3,
\]

choose `v=(q,0,0)`. Its gradient Hessian is

\[
H_{ij}=\operatorname{diag}(6Aq,3Aq,3Aq).
\]

For a Fourier wavevector making angle `theta` with `v`, the regulated
decoupled dispersion is

\[
\boxed{
\omega^2
=\frac{1}{K_Q}\left[
3Aq(1+\cos^2\theta)k^2
+\frac{\gamma}{M_*^2}k^4
\right].
}
\]

At nonzero `q`, the cubic background produces a positive anisotropic `k^2`
term for `K_Q,A>0`. The higher-spatial-derivative term dominates above

\[
k_\times^2
=\frac{3Aq(1+\cos^2\theta)M_*^2}{\gamma}.
\]

At zero gradient,

\[
\boxed{
q=0:
\qquad
\omega^2=\frac{\gamma}{K_QM_*^2}k^4.
}
\]

The necessary decoupling conditions are therefore

\[
\boxed{K_Q>0,\qquad A>0,\qquad\gamma>0.}
\]

Because the regulator contains spatial rather than higher time derivatives in
the declared frame, the flat force equation remains second order in time. This
does not prove that a chosen covariant completion preserves the constraint
structure on general backgrounds.

## 7. What Stage A establishes

### Derived within the declared decoupling limit

- an independent frame and a derived current velocity cannot be treated as the
  same variable without a parent constraint construction;
- the alignment term has positive relative-current energy for `zeta>0`;
- the full two-derivative frame basis reduces to the stated necessary sign
  combinations in frozen Minkowski space;
- the cubic force Hessian is positive at nonzero gradient for `A>0`;
- the proposed regulator supplies a positive `k^4` dispersion at zero gradient
  for `K_Q,gamma>0`;
- deliberately unhealthy parameter choices fail the automated sign checks.

### Not established

- the full propagating degree-of-freedom count after gravity and all constraints;
- positivity of the reduced coupled Hamiltonian;
- absence of the low-momentum nonpropagating problem found in related theories;
- a strong-coupling scale for the nonanalytic cubic plus `k^4` system;
- radiative stability of the missing canonical `Y` operator;
- a covariant regulator valid on accelerating or vortical frame backgrounds;
- compatibility with finite-density condensate sound modes;
- observationally viable aether coefficients;
- screening, matter coupling or lensing.

Accordingly, Stage A passes while UVIR-003 remains open.

## 8. Next calculation: Stage B

Stage B must use an aether-orthogonal ADM decomposition around

\[
g_{\mu\nu}=\eta_{\mu\nu},
\qquad
\Phi=\frac{\rho_0+\delta\rho}{\sqrt2}
e^{i(\mu t+\vartheta)},
\qquad
U^\mu=(1,0,0,0),
\qquad
\bar\psi=\mathrm{constant}.
\]

It must then:

1. decompose metric, aether, condensate and force perturbations into scalar,
   vector and tensor sectors;
2. impose the unit-vector constraint;
3. identify lapse, shift and multiplier variables;
4. integrate out every nondynamical variable before inspecting signs;
5. derive the reduced scalar, vector and tensor kinetic matrices;
6. calculate all dispersion relations, including the `k^4` force branch;
7. test the Hamiltonian eigenvalues through `k -> 0`;
8. repeat on a nonzero-gradient force background, where rotational symmetry is
   reduced and frame/force mixing appears;
9. perform power counting and derive the actual strong-coupling scale.

Only after those checks can UVIR-003 decide whether the action passes, fails or
requires a constrained redesign. MAT-001 remains blocked.

## 9. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_stage_a.py
```

Expected footer:

```text
UVIR-003 Stage-A validation: PASS
Architecture: INDEPENDENT_DYNAMICAL_U_WITH_CURRENT_ALIGNMENT
k4 regulator: CONDITIONAL_PASS_IN_FLAT_DECOUPLING_LIMIT
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS
```

Machine-readable outputs are under `Analysis/UVIR/UVIR-003/outputs/`.
