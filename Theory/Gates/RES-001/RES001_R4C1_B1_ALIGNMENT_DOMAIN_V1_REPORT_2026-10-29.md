# B1: aligned linear control does not clear the unrestricted dust-clock domain

29 October 2026. Conditional G4 diagnostic. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding

Arbitrarily small homogeneous transverse tilts can satisfy the original dust
and scalar charges, unit constraint and lapse/momentum constraints, and admit
local homogeneous solutions of the unchanged action. On their dust-clock
slices, actual nonzero-mode gauge/shift reduction leaves a kinetic form with
inertia **(10 positive, 1 negative, 0 zero)** for every
0<|w|<=1/500. At exact alignment the auxiliary is algebraic and its elimination
leaves the earlier positive ten-field block.

This is a substantive obstruction to extrapolating the successful aligned
linear certificate into an **unrestricted positive-kinetic dust-clock
neighbourhood allowing these tilt variations**. It is not a revision of that
certificate: the original aligned solution, propagator and evidence remain
unchanged and valid in their stated scope.

The result is not a foliation-independent quantum-ghost diagnosis, a physical
cutoff, a finite-frequency instability rate, an all-background/action no-go,
or rejection of ITSM/T3. Admissibility of a restricted physical Cauchy domain
remains essential. The diagnostic varies the homogeneous frame harmonic and
does not establish membership in an ensemble separately fixing that harmonic
to zero. It does not replace the vortical G1 preparation or solve its domain.

## Charge-preserving diagnostic initial data

The [contract](RES001_R4C1_B1_ALIGNMENT_DOMAIN_V1_CONTRACT_2026-10-29.md) was
frozen before calculation. Use the old B1 coefficients and original action,
not the later eta=1/4 B1-frame map. At the initial event set h=I, a=C=1,
(u,v,r)=(1,0,1), (u_dot,r_dot,psi_dot)=(0,1/4,1/5), Z=Z_dot=0,
tau_dot=1 and rho=1/5. Introduce V_y=w, V_x=V_z=0 and
coordinate V_y_dot=-Hw, so the physical tilt derivative initially vanishes.
This does not impose a constant future tilt or a future FLRW metric.

Direct original-density differentiation gives the normalized U(1) charge
(1-w^2/13)v_dot. Holding its registered value 1 fixes

$$\dot v=\frac{1}{1-w^2/13}.$$

The original clock charge remains 1/5 per unit coordinate volume. The
unfixed-lapse equation is

$$C_H(w)H^2=E(w),\qquad C_H=33/10+13w^2/60,$$

$$E(w)=\frac{3469}{1400}-\frac12+
\frac{1}{2(1-w^2/13)}+\frac{3w^2}{50}-\frac{4|w|^3}{875}.$$

The norm-cubed contribution is retained in this equation. Select the positive
root H=sqrt(E/C_H). Outward-rounded bounds over the whole declared interval
give 0.75086549 < H^2 < 0.75086604. Both charges and H^2 are invariant under
w -> -w, and H^2(0)=3469/4620. The lapse equation determines H; neither an
observational target nor a changed dust density selects it.

All spatial fields and momenta are homogeneous, so every spatial derivative
in the original canonical momentum constraint vanishes. Constant-shift
variations also vanish directly. No diagonal metric equation is discarded:
all six homogeneous metric variables, three frame variables, three Cartesian
scalars, psi and Z retain independent accelerations after this initial event.

## Local homogeneous admission, with its precise limitation

Use the already derived positive dust branch and fixed clock charge I=1/5.
Its homogeneous Routh contribution is -I N C(psi), not a premature deletion
of the dust action. The remaining homogeneous action has fourteen coordinate
velocities and the original unit-frame branch. The independent normal-frame
equation determines its multiplier as in the pinned canonical reduction.

Let R12 be the temporal Hessian complement excluding psi and Z. Direct
calculation gives

$$\det R_{12}=\frac{11(w^2-13)(w^2+5)^2(2w^2+3)}
 {539136000(1+w^2)},$$

$$\det M_{14}=-b^2w^4\det R_{12},\qquad b=5/11.$$

R12 is uniformly nonzero on |w|<=1/500; M14 is nonzero at each w != 0.
The physical projected gradient is Y=w^2/25>0 at each such point. The full
homogeneous Euler system is consequently a smooth ordinary differential
equation in a neighbourhood of that point, with positive metric determinant,
future unit frame and positive dust. Standard local ODE existence applies.
The full accelerations, including anisotropic metric response, are available;
the earlier aligned FRW evolution equations are not reused for this tilted
solution.

The unfixed lapse derivative is checked to equal minus the homogeneous
canonical energy. The autonomous Routh equations preserve that energy, so
its initially satisfied lapse constraint persists. Spatial momentum
constraints remain identically zero by homogeneity. Dust charge is fixed by
Routh reduction; the unchanged U(1) symmetry preserves the scalar charge.
Positive dust follows locally from I>0, C>0 and positive spatial volume.
This establishes **pointwise local homogeneous admission**, not a lifetime
uniform as w -> 0 and not a [0,0.05] tilted propagator theorem. M14 becomes
singular at alignment. These are diagnostic neighbouring data, not an adopted
cosmology, new parent, or a continuation of G1's spatial profile and means.

## Actual nonzero-mode reduction and interaction

On these same initial events keep the original clock/dust variation before
elimination. For a nonzero perturbation wave k in z, transverse to V_y,
delta tau=0 fixes delta N=-beta delta psi and its spatial gradient. The lapse
equation determines the density perturbation. Use the three spatial metric
gauges and eliminate all three shifts from their actual derivative block.
The determinant after removing the common k^6 factor is

$$\det D_S=-\frac{(1+w^2)(w^4+5w^2+15)}{900},$$

nonzero throughout the declared interval. No scalar/regulator direction is
deleted by hand. This is a new calculation with old B1 coefficients and the
charge-preserving data above, not substitution into the later B1-frame pencil.

The complete nine-field complement B9, excluding psi,Z, has positive exact
LDL pivots over the interval. Its full matrices and pivots are exported.
There is no time-kinetic coupling of psi to this complement at these events.
The remaining two-field temporal form is exactly

$$\frac12f(w)\dot\psi^2-bw^2\dot\psi\dot Z,
\qquad f=3(1+w^2)-\frac{12}{35}|w|^3>0.$$

The true finite-tilt norm-cubed Hessian supplies the last term in f. Completing
the square gives

$$\frac f2\left(\dot\psi-\frac{bw^2}{f}\dot Z\right)^2
-\frac{b^2w^4}{2f}\dot Z^2.$$

The negative Schur coefficient is strict for every nonzero w in the domain;
its magnitude divided by w^4 lies between 0.06887024 and 0.06887053 in the
declared control units. At |w|=1e-3 the coefficient is approximately
-6.88705e-14. This is a dimensioned kinetic coefficient in the specified field
convention, not an eigenfrequency, scattering amplitude or cutoff.

The original canonical regulator momentum already has
P_Z=-b[V^2 psi_hat+gamma V^i D_i psi]. On the homogeneous ray it is
-bw^2 psi_dot. The interaction -b |delta V|^2 delta psi_dot delta Z_dot
is invisible to the exactly aligned quadratic action but activates the extra
velocity pairing away from alignment. A magnitude-normalized Z variable has
scale b w^2/sqrt(f), which vanishes at alignment. The time-kinetic sign and
rank change cannot be removed by a nonsingular real field redefinition in
this fixed clock reduction. Its physical-domain interpretation is still
separate from this algebra.

In particular negative kinetic inertia on these slices is not itself a proof
of an exponentially growing finite-k observable or a quantum ghost in every
possible admissible slicing. A different Cauchy formulation, a restricted
initial domain or a justified low-energy prescription must be demonstrated,
not inferred by deleting this direction. Local Frobenius or a coordinate
boost alone also does not supply a global periodic preferred-time slicing:
at the initial event n_flat has a uniform nonzero dy component w. If it were
F dT with F>0 and a globally single-valued periodic T, integrating
T_y=w/F around the y circle would have a nonzero fixed sign, contradicting
periodicity. This is a global caveat for this harmonic diagnostic; it does
not reject every alternative formulation or a separately fixed harmonic
ensemble.

## Verification and research decision

The [versioned executable](../../../Analysis/MasterTests/test_01_r4c1_b1_alignment_domain_v1.py)
passes 53/53 checks. The [fresh receipt](../../../Analysis/MasterTests/outputs/r4c1_b1_alignment_domain_v1_attempt_01/summary.json)
SHA-256 is `5ce2ecbf65f1a1b1d3f0e38dc6a02413a9bcefa36a1e93e24b9aeb090e36be1b`.
Its full read-only recomputing replay is byte-identical, exit 0. All twenty-five
direct inputs and their twenty-five sidecars retain bytes and modification
times through calculation/replay. The successful aligned propagator and
earlier warnings are not changed or superseded.

Independent automatic differentiation of the unmodified physical density,
with A retained, checks the whole 25x25 derivative block and 14x14 homogeneous
mass at both w signs, complex steps 1e-20 and 1e-26, and 120 digits. The largest
derivative-block discrepancy at the smaller step is below 5.358e-50;
homogeneous-mass discrepancies are below 2e-121. Original lapse, dust/scalar
charge and homogeneous shift checks also pass. Exact identities and interval
sign bounds support the stated domain; numerical controls and same-author
replay are not external peer review.

The unrestricted positive-kinetic dust-clock route allowing this diagnostic
curve is obstructed. Do not label the aligned linear certificate a nonlinear
healthy neighbourhood or physical window. The next question is whether the
unchanged action supplies an invariant/admissible restricted low-energy or
Cauchy domain with controlled interactions, or whether an operator action/domain
decision is required. No mode exclusion, future boundary law, cutoff or new
parent is adopted here. The physical frequency scale and admissibility of any
excluded branch require further coupled analysis and matching information.

G1-G6 INCOMPLETE; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED.
The old B1 GR/normalization holds and the vortical G1 on-shell/domain problem
remain. Review DEFERRED; no vault, manuscript/PDF/site, provider, commit/push
or action/state adoption.
