# Three-family homogeneous charge/energy domain continuation: V1

Date: 13 October 2026. Frozen before execution.
Owner: Master Test 1 / RES-001 / approved unchanged-action Stage 2.
This is a necessary physical-constraint/ensemble calculation, not replacement
of the full dust -> GR/domain -> matched numerical weak-field objective.
Stage 2 physical GO remains unproved; Stage 3 is not entered.

## Authority and existing results

Keep the R4C1 action and all three registered families/scalings. Reuse, without
rerunning, the completed B1 mean-mode canonical report (11 October) and the
three-family retarded cubic V2 result (13 October). The former establishes an
admissible negative homogeneous direction in the varying-dust-charge ensemble;
the fixed-dust comparator is a different ensemble, not a gauge repair.
The latter supplies immutable prepared trajectories, not a physical EFT band.

Do not transplant B1-specialized matrices into the new families. Use the
unspecialized 22-field action Hessian and the generic planar WWR functional;
vary/derive generic currents and momentum coefficients before specialization.
No new parent, prepared-data adjustment, charge restriction, model/provider,
dependency/runtime setup, manuscript/PDF, vault, commit/push or publication.

## Question and registered data

Determine which global conserved-charge ensemble the existing prepared waves
actually occupy as their amplitude e varies. Do not assume either second-order
charge correction vanishes. Do not impose fixed dust momentum to remove a sign.
Determine the generic homogeneous momentum/clock domains and their singular
endpoints, retaining the negative direction and its exact scope.

Use all 18 stored cases: G3, B1-frame and hierarchical; eta=1/4,1/64,1/1024;
k=40; DOP853 and Radau; t in [0,1/20]. Reconstruct all 21 stored time nodes and
check the archived initial/interior/final/linear-zero full-field controls.
Reconstruction keeps all 22 field labels, source offsets, inverse and basis
drift, constraints and source derivatives. No ODE integrations are repeated.
The first spatial angle k*z is not the complex scalar's internal U(1) angle.

## Currents derived from the unchanged action

Derive the internal rotation current by direct differentiation of the scalar
and alignment density, with delta u=-v delta angle, delta v=u delta angle.
J_mu=v partial_mu u-u partial_mu v. Independently compare with

```text
j_U1^mu = sqrt(-g) [g^(mu nu)+zeta*(u^2+v^2)*h^(mu nu)] J_nu,
p_tau^mu = -sqrt(-g)*epsilon*C^2*g^(mu nu)*partial_nu tau.
```

Keep lapse, density and the normalized frame/projector unfixed during this
variation. Prove the internal-rotation and dust-shift Noether identities before
using background equations. No division by the Cartesian radius is permitted
in the currents; any polar canonical chart requires radius>0 explicitly.
Only integrate the periodic spatial divergence away after deriving it.

For the registered transverse standing wave, first spatial metric/scalar/dust
responses vanish, while second-order mean fields are present. Let vol=a^3,
j=u*v_dot-v*u_dot, radius2=u^2+v^2, trM=Mxx+Myy+Mzz. The expected quadratic
mean coefficients, to be derived and independently checked, are

```text
Q2 = vol*[u*dv_dot+du*v_dot-v*du_dot-dv*u_dot
          +(trM/2-alpha)*j-zeta*radius2*j*W^2/2],
P_tau2 = vol*C^3*Em
       +(vol*rho_m/C)*[trM/2-alpha+2*beta*Pi+T_dot/C].
```

Here W is the time-dependent amplitude of cos(k*z), with mean cos^2=1/2.
Use all mean fields in these formulas. Mean-zero 2k pieces and periodic
divergences must be rejected only with exact Fourier/order arguments, not by
dropping the mean equation. In dust-clock gauge T=T_dot=0 and alpha=-beta Pi,
the dust bracket becomes trM/2+3 beta Pi. C is the background C in these
quadratic coefficients. The directional cusp cannot be converted to a Taylor
cubic; prove its order does not enter these particular second-order currents.

For the prescribed zero free response coordinates/velocities at the initial
event, derive (do not fit) Q2(0)=-eta^3/26 in the declared reference units.
The initial dust correction is determined by the full lapse/constraint source;
do not preset its value, sign or scaling. A nonzero correction identifies
different amplitude-dependent global charge sectors, not charge nonconservation
within an individual solution. Charges are per unit coordinate volume;
integrated values multiply by (2*pi)^3. Coefficients normalized to the initial
frame residue divide by f2=eta/6; this is not microscopic matching.

## Independent density drift and generator identities

The retained reconstruction helper assigns Em_dot from the dust Euler row.
That value must NOT be used to prove conservation of the dust momentum: doing
so would test the assigned equation against itself. Derive Em as an explicit
affine function of the mean state from the lapse constraint, including its
complete source. Differentiate that graph with the actual reduced evolution
and all coefficient/source drift. Compare this independent Em_dot with the
Euler-assigned value, and retain any disagreement as a substantive result.
Never replace a needed auxiliary derivative with zero or a row assignment
without a separate kinematic check.

For each charge write Q2=L_Q(t)z+o_Q(t), P_tau2=L_P(t)z+o_P(t), where
z_dot=Gz+g is the full mean evolution. Derive and check both the homogeneous
rows L_dot+L*G and the forced terms L*g+o_dot. Exact current/source identities
use the varied generic action and declared on-shell background/first-wave
equations. Numerics verify the same identities on the registered data.
Do not continually project onto a slow graph or invent a new constraint map.

## Homogeneous momentum and clock domains

Derive the lapse-unfixed aligned homogeneous Legendre constraint with generic
M_cos2, K_Q, potential, C and the full angular charge. Fixing complex charge
uses the alignment-dependent Routh coefficient
vol*radius2*(1-zeta*radius2*boost_squared)/N, not a phase-only shortcut.
Retain its boost curvature. Unit/normal, density, regulator and clock constraints
must precede any physical momentum-sign interpretation.

Use the full unspecialized action kernel to verify the mean physical kinetic
congruence in the volume/five-shear/three-boost/Cartesian-scalar/psi basis.
Derive, rather than assume, its coefficients, normal-block inverse domain,
and the dust-clock volume momentum coefficient. The force-psi clock is not
the complex U(1) angle. On its positive-momentum branch, retain the mixed
volume/dust-momentum subblock and radicand domain. Carry all three families
through every resulting domain test. Do not invert eta=0, zero radius,
zero density, zero clock or a singular auxiliary/normal block.

A homogeneous negative canonical direction is not automatically a local
propagating ghost. A fixed-dust comparator remains explicitly different from
the original prepared ensemble. This milestone does not prove the complete
quadratic potential positive, a conserved perturbation energy, a Cauchy domain,
quartic frequency window, physical cutoff or healthy uniform GR recovery.

## Checks, acceptance and preservation

- Exact independent variational/tensor currents and Noether identities;
  formal second-order mean coefficients; generic momentum congruence and
  regular/singular clock/normal domains before family substitution.
- Exact Fourier averaging and sign/unit controls; rejection of omitted
  alignment, mean volume/density, conformal weight, source or coefficient drift.
- Numerical conservation and independent derivative/row/source controls use
  1e-7 normalized tolerance, with cancellation scales and both absolute and
  eta^3-relative U(1) discrepancies reported. A large absolute floor cannot be
  presented as precision on the tiny eta^3 correction. Initial exact-recipe
  identity is kept distinct from numerical propagation error.
- Two-method checks on both conserved coefficients, and independent unexpanded
  current controls of the second-order coefficient. Finite controls must carry
  their higher-order remainder, not demand exact finite-step polynomial equality.
- Fresh non-overwriting receipts, new versioned executable, immediate sidecars,
  exact read-only replay and owning report. Preserve the existing V2 six-artifact
  bytes, old failures, all originals/sidecars and unrelated dirty work.

Acceptance is an explicit, reproducible determination of the registered charge
ensemble, independent constraint-density drift and homogeneous momentum-domain
implications within the declared scope. A failed conservation/drift identity
requires an exact disposition; original passed receipts are never rewritten.
Partial algebra or numerical agreement alone is not physical Stage-2 GO.

Register R9-MT1-THREE-FAMILY-CHARGE-DOMAIN-V1 with MEAN-MODE-ENERGY,
RETARDED-CUBIC, PLANAR-WWR, GR-FAMILY-SURVEY, TIME/RESPONSE/ODD-TAIL and all
transitive review debt. Review DEFERRED; Rule9_cleared=false; physics_pass=false;
gate_effect=NONE. Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
canonical K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Full native goal ACTIVE/incomplete. Matching and observational prediction are
not entered, no family is selected using a desired acceleration coefficient.
