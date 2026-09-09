# VOR/TOP phase and winding normalization specification

**Date:** 2026-09-05  
**Role:** Codex Role C — convention, provenance and gate specification  
**Status:** `FROZEN_SPEC_FOR_MAX_CALCULATION`  
**Physics pass:** `false`  
**Gate effect:** none; VOR-001 remains `OPEN_SCAFFOLD_ONLY`  
**Parent join:** prohibited until one common condensate parent is selected

## 1. Purpose

This document fixes the notation and invariant maps needed for an exact
winding calculation. It does not derive a force law, a matter pole residue,
an acceleration scale, a compactification scale or an observable.

The controlling separation is

```text
dimensionless phase
  != temporal Noether charge
  != spatial winding integer
  != canonical momentum circulation
  != observer-dependent three-velocity circulation
  != canonically normalized propagating mode
  != matter coupling or acceleration scale.
```

## 2. Units and field normalization

### 2.1 Natural-unit convention for the calculation

Unless a line is explicitly labelled SI, use

```text
hbar = c = 1,  metric signature (-,+,+,+),  [x^mu] = mass^-1.
```

For a canonical four-dimensional complex scalar,

```text
[Phi] = [rho] = mass,   [Theta] = 1,
[partial_mu Theta] = mass,   [lambda] = 1.
```

The polar definition is fixed as

\[
\Phi=\frac{\rho}{\sqrt{2}}e^{i\Theta},\qquad
\Theta\sim\Theta+2\pi.
\]

The exponential makes `Theta` dimensionless. A field redefinition
`varphi=f_Theta Theta` gives `varphi` mass dimension one only when
`[f_Theta]=mass`; its periodicity becomes `2*pi*f_Theta`. The rescaled field
must not be called a dimensionless phase.

### 2.2 SI restoration

The invariant phase holonomy is unchanged:

\[
\oint d\Theta=2\pi n.
\]

The canonical one-particle momentum covector is

\[
p_\mu=\hbar\nabla_\mu\Theta
\]

for a neutral condensate. Thus it is **momentum circulation**, not the
dimensionless phase integral, that carries a factor of `hbar`:

\[
\oint p_i\,dx^i=2\pi\hbar n=h n.
\]

Any restoration of `c` depends on whether a time coordinate is `t` or `ct` and
must be performed from the covariant action, not by dimensional guesswork.

## 3. Declared neutral parent class

The exact Max calculation must begin with one named member of

\[
S_\Phi=\int d^4x\sqrt{-g}\left[
-Z(s)g^{\mu\nu}(\nabla_\mu\Phi)^*(\nabla_\nu\Phi)-U(s)
\right],\qquad s=|\Phi|^2,
\]

with `Z(s)>0` on the tested branch. The canonical control is `Z=1`.
In polar variables,

\[
\mathcal L_\Phi=-\frac{Z}{2}(\nabla\rho)^2
-\frac{Z\rho^2}{2}(\nabla\Theta)^2-U(\rho^2/2).
\]

An amplitude-only portal such as the registered conformal matter metric
`S_m[chi,A^2(s/M_*^2)g]` preserves the global phase symmetry. It does not,
without reduction and matching, make winding a matter source or fix the
physical pole residue.

A charged condensate is a different calculation. It replaces the phase
gradient by a gauge-invariant covector, schematically
`hbar*dTheta-q*A`, and winding holonomy can mix with gauge flux. No charged
formula may be imported into the neutral baseline.

## 4. Noether current and charge

For a global `U(1)` variation, the current is proportional to

\[
j^\mu=\sigma\,Z\rho^2\nabla^\mu\Theta,
\]

where `sigma=+1` or `-1` records the chosen generator orientation. The Max
derivation must fix `sigma` directly from its declared transformation
convention and keep it unchanged.

For a unit future-directed observer `u^mu`, define the measured charge density
with an explicit orientation,

\[
n_Q=-u_\mu j^\mu,
\]

and choose the charge/background branch so `n_Q>0`. The conserved charge on a
compact spatial slice is

\[
Q_N=\int_{T^3}d^3x\sqrt{h}\,n_Q
\]

when the slice normal is the selected observer and no exchange breaks the
symmetry.

This temporal charge is not a spatial winding number. A background
`Theta=mu t` may carry charge with `n_i=0`; a static spatial winding may have
`Q_N=0`; a finite-density superflow can carry both.

## 5. Relativistic flow and nonrelativistic velocity are separate maps

### 5.1 Relativistic phase-gradient map

On a branch where the neutral phase gradient is timelike,

\[
X=-\nabla_\mu\Theta\nabla^\mu\Theta>0,
\qquad
u_\mu=-\frac{\nabla_\mu\Theta}{\sqrt X}
\]

is a candidate irrotational four-velocity orientation. The local chemical
potential or enthalpy scale is proportional to `hbar*sqrt(X)` after units are
restored. A spatial three-velocity is obtained only after projection into a
declared observer/slicing; it is not universally `grad(Theta)`.

Relativistic circulation quantizes the canonical momentum/chemical-potential
one-form. Dividing by a mass or enthalpy scale to obtain a velocity circulation
is model- and state-dependent.

### 5.2 Nonrelativistic Gross-Pitaevskii limit

Only after a controlled nonrelativistic reduction with constituent mass `m`
may one write

\[
\mathbf v=\frac{\hbar}{m}\boldsymbol\nabla\Theta,
\qquad
\oint\mathbf v\cdot d\boldsymbol\ell
=\frac{2\pi\hbar}{m}n=\frac{h}{m}n.
\]

The factor `hbar/m` comes from the nonrelativistic parent and its particle-mass
normalization. Neither `m`, an enthalpy, nor a matter coupling can be supplied
by topology. Therefore the velocity-circulation formula may not be used in a
relativistic condensate calculation until that limit has been derived.

## 6. Compact geometry convention

Use coordinate periods `ell_i` and a spatial metric `h_ij` as the primary
objects. For a rectangular static chart one may choose

```text
x^i in [0, ell_i),   h_ij=delta_ij,
```

and then the proper noncontractible cycle lengths are `L_i=ell_i`.
In a general chart,

\[
L_i=\oint_{\gamma_i}\sqrt{h_{jk}\,dx^jdx^k}
\]

and coordinate period is not automatically proper length.

For the rectangular baseline,

\[
\Theta_{\mathbf n}=2\pi\sum_i\frac{n_i x^i}{L_i},
\qquad
k_i=\frac{2\pi n_i}{L_i},
\qquad
|k|_h^2=h^{ij}k_i k_j.
\]

Each `L_i` is the proper length of a noncontractible `S^1` cycle—equivalently
its circumference in this intrinsic description. It is not an embedded torus
radius, a diameter, a Hubble radius, or automatically `2*pi` times another
physical scale.

Under a change of cycle basis in `GL(3,Z)`, the components of `n_i`, the
period/basis matrix and reciprocal covectors must transform together. The
invariant energy depends on their contracted norm; a component value or a
chosen basis is not an observable.

## 7. Winding energy and amplitude relaxation

For the canonical static control with constant amplitude,

\[
E_{\rm grad}=\frac{V_{T^3}}{2}\rho^2|k|_h^2.
\]

For

\[
U(\rho)=\frac{\lambda}{4}(\rho^2-v^2)^2,
\qquad \omega^2=|k|_h^2,
\]

the constant-amplitude stationary branches are

\[
\rho_0^2=v^2-\frac{\omega^2}{\lambda}
\quad (\omega^2<\lambda v^2),
\]

and the restored configuration `rho_0=0` above threshold. On the broken branch,

\[
\Delta e_{\mathbf n}
=\frac12v^2\omega^2-\frac{\omega^4}{4\lambda}.
\]

At the preregistered S2-T02 point `lambda=100`, `omega=1`, `v=1`, the relative
deviation from the fixed-amplitude S1 energy is

\[
\frac{\omega^2}{2\lambda v^2}=\frac1{200}=0.5\%,
\]

so the `<0.1%` criterion fails. This failure is binding; the prior substitution
`lambda=100000` did not test the registered point.

When `rho=0`, the phase and its map into `S^1` are undefined. The restored
configuration is therefore not a protected smooth-winding sector; it is a
route by which the winding label can be lost. Statements that T03–T06 survive
must be restricted to the broken branch, with the collapse/unwinding boundary
reported separately.

The fixed-chemical-potential and fixed-conserved-charge ensembles need not
give the same equilibrium. The selected ensemble and boundary terms are part
of the parent definition, not nuisance conventions.

## 8. Canonical local mode is not the phase angle

For a static canonical background with no mixing, the phase quadratic term is
schematically

\[
\frac12 Z(\rho_0)\rho_0^2(\partial\vartheta)^2,
\]

suggesting a local normalization
`q_phase=sqrt(Z(rho_0))*rho_0*vartheta`. On a finite-density time-dependent or
winding background, amplitude, phase, lapse, shift, metric and any extra frame
field can mix. The true physical mode and its residue must be obtained only
after constraint reduction and kinetic diagonalization.

Accordingly,

```text
f_Theta = sqrt(Z)*rho_0
```

is at most a fixed-background coefficient. It is not automatically `K_Q`,
`1/V`, a decay constant, a gravitational coupling or an acceleration scale.

## 9. Claim firewall

The following inferences fail this specification:

- `n_i`, `2*pi`, a cycle count or a coordinate angle used as a Wilson
  coefficient;
- `L_i=c/H`, `L_i=2*pi*c/H` or any observed acceleration inserted before the
  parent determines the physical scale;
- `a0=cH/(2*pi)` labelled a circulation derivation;
- `C_obs=2/3`, `13/12`, a PTA band or a matter coupling inferred from the
  number of compact directions;
- `U^mu` identified with the phase gradient while also retained as an
  independent field in the same parent;
- a fixed-amplitude winding energy presented as on-shell after the amplitude
  equation has shifted the background;
- the restored `rho=0` branch presented as a protected smooth-winding sector;
- a nonrelativistic velocity formula used in a relativistic parent without a
  controlled limit.

## 10. Max calculation specification

### X5-A — common-parent declaration

1. Select exactly one neutral relativistic complex-parent action and one
   finite-density ensemble.
2. State `Z(s)`, `U(s)`, all dimensions, boundary terms and whether the matter
   portal is RCP-I1-T, RCP-I1-C or absent for the control.
3. State whether any frame field is derived from `Theta` or independent; never
   both without an explicit constraint.

### X5-B — background and topological sectors

1. Solve the homogeneous zero-winding finite-density branch without
   observational inputs.
2. Add the rectangular-`T^3` winding covector and solve amplitude relaxation
   in both fixed-charge and fixed-chemical-potential ensembles, or justify one.
3. Locate broken/restored branches, Hessian signs and the point where winding
   protection is lost through `rho=0`.

### X5-C — invariant current, circulation and stress

1. Derive the Noether current from the action and fix its sign convention.
2. Derive the canonical momentum circulation and, separately, any controlled
   nonrelativistic velocity circulation.
3. Vary the action with respect to the rectangular metric/moduli to obtain
   energy and directional stresses; do not infer stress from cycle counting.
4. Verify reflection, permutation/modular reindexing, zero-winding, isotropic
   and decompactification limits.

### X5-D — local stability and parent interface

1. Expand amplitude and phase fluctuations about each surviving nonzero
   winding branch.
2. At fixed metric, diagonalize their kinetic and gradient matrices and report
   ghosts, gradient instabilities and mode speeds.
3. Record every metric/constraint term deferred to Ultra; no fixed-background
   mode may be called the final physical matter-coupled mode.
4. Test whether the selected M2/M3-U1 portal changes charge conservation or
   supplies a phase source. If it is amplitude-only, record the negative
   result explicitly.

## 11. Pass, hold and fail criteria

| Outcome | Criterion |
|---|---|
| `PASS_BOUNDED_WINDING_CONTROL` | One declared parent and ensemble; on-shell finite-density winding branches; exact current/circulation/stress; positive fixed-background local modes; invariant limits pass; no observable matching claim |
| `HOLD_FOR_ULTRA_CONSTRAINT_REDUCTION` | Fixed-background winding sector survives but metric/lapse/shift mixing is required to identify physical modes or residues |
| `FAIL_PARENT_BRANCH` | No stable nonzero-density branch, ghost/gradient failure, energy unbounded below, or all tested windings collapse through `rho=0` in the claimed domain |
| `FAIL_CLAIM_FIREWALL` | Topological integer, `2*pi`, compact length or a target observable is used to supply a missing coupling/scale |

No result from this calculation changes MAT-001, UVIR-003, SCR-001, LEN-001,
DISK-001 or a cosmology gate without a later signed parent-interface decision.

