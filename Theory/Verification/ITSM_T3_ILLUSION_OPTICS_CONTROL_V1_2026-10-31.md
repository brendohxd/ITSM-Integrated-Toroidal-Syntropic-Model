# T3 illusion: exact light-propagation control and mechanism input boundary

Date: 31 October 2026 (Australia/Perth).
Result: T3-OPTICS-STATIC-CONTROL-V1. Claim: Conditional.
review_status=DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Question and authority

The operator requested an explicit light-propagation calculation for the T3
illusion hypothesis. This is a parallel methods control under sections 1 and 4
of `Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md`, not an action-derived
ITSM prediction or a replacement for the active R4C1 programme.

The paper assessed is `papers/T3-Illusion/ITSM_T3_Illusion_v0.6.1.tex`, SHA256
667be8ba7e8e7839c5df19141428397b9c38ce932d6371841f2e638da321faef.
It proposes topological images and additional shear-plane/dome explanations.
This control separates those mechanisms by adding no vacuum optical effect.

## Frozen control assumptions and exact solution

Assume, rather than derive, a static rectangular spatial quotient with

    ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2,
    x_i ~ x_i + n_i L_i, n_i integer, L_i > 0.

The reference length Lref sets units; set c=1 and Lx=Ly=Lz=1.
Times are in Lref/c, positions in Lref. These are not seconds or observed
cosmological lengths. There is no cosmological expansion in this control.
Observer o=(0.5,0.5,0.5), source s=(0.68,0.61,0.57). Both are static.
The source emits continuously over the lookback interval [0,1.6]. No source
evolution, atmosphere, opaque Earth, luminosity, detector or selection model
is supplied. The source is distinct from the observer modulo the lattice.

For reception at t=0, every image has

    d_n = s-o + (n_x Lx,n_y Ly,n_z Lz),
    r_n = |d_n|,  N_n = d_n/r_n,
    t_emit = -r_n/c,
    t(lambda) = -lambda/c, x(lambda) = o + lambda N_n,
    0 <= lambda <= r_n.

Only 0<r_n<=1.6 is retained. These are exact geodesics, not numerical ODE
integration: the covering-space Christoffel symbols vanish. Quotient face
crossing is a coordinate identification with identity tangent transport,
not bending at a wall. The stationary orthonormal tetrad is
e_(0)=c^-1 partial_t and e_(i)=partial_i. The future arrival tangent is
proportional to (1/c,-N_n), so the observed source direction is +N_n.
Static emitter and observer have frequency ratio one in this metric.

For each coordinate the necessary interval
(-depth-delta_i)/L_i <= n_i <= (depth-delta_i)/L_i
provides a complete finite enumeration. The spherical distance criterion
then removes images outside the past cone. No arbitrary winding cap is used.

## Executed result

Executable: `Analysis/Lensing/T3Illusion/t3_null_control_v1.py`.
Receipt: `Analysis/Lensing/T3Illusion/outputs/static_t3_v1/summary.json`.
Executable SHA256: 9b626278a3c0df5f0f578967fec9af645c6b50784e23818aa159f5732dc08e39.
Receipt SHA256: 00e8e935909cdaff201c868756d0637a4aacf127b9c32abca58d5036cfb0ac05.

The assumed source has 19 geometric images inside the prescribed past cone.
Their lookbacks range from 0.2222611077089287 to 1.5966840639274884 Lref/c.
These are different emission events; image number is not a detection count.
All angles and lookbacks are in `images.csv`; `sky.svg` is a longitude/latitude
map, not a physically calibrated sky or an equal-area projection.

Eight methods checks passed, with no failed or unknown checks: independent
oversized lattice enumeration, null normalization, quotient endpoints,
translation through cell faces, the finite-depth large-cell Euclidean limit,
multiple emission lookbacks, straight covering-space paths, and supplementary
directional probes. Maximum null residual was 2.2204460492503131e-16;
maximum integer-period endpoint residual was 1.1102230246251565e-16.
The check count does not establish physical validity of the assumed metric.

Reproduce:

    python -B Scripts/itsm_context.py run -- python -B Analysis/Lensing/T3Illusion/t3_null_control_v1.py
    python -B Scripts/itsm_context.py receipt Analysis/Lensing/T3Illusion/outputs/static_t3_v1/summary.json

## Interpretation and rejection boundaries

Repeated images follow conditionally from this assumed periodic geometry and
sufficient emission age. They are a standard topological consequence, not a
distinctive new ITSM effect. Fixed source/observer coordinates produce fixed
image directions, not daily circular motion.

There is no angular wall or physical dome in this metric: every unit direction
defines a complete null ray on the quotient. This conclusion follows from the
analytic metric and covering map, not from the finite source catalog or the
26 directional probes. The light-cone depth is an emission-age restriction,
not a material boundary. Thus static translation-only T3 periodicity alone is
insufficient to supply the proposed dome mechanism. No inference about all
possible curved, dynamical or photon-coupled ITSM models follows.

The model does not include a planet, so it cannot explain an Earth horizon.
Spatial topology and the curvature/visibility of an opaque surface must be
treated separately. No claim about observed horizon shape is validated here.

For this fixed idealized geometry and continuously emitting source, the listed
directions and relative lookbacks are quantitative predictions. A future
observational test must first freeze actual lengths, orientation, source
identification/history and detection completeness. Inconsistent image
directions/delays, or missing detectable images under that complete forward
model, could reject that specified configuration. The present artificial
catalog is not itself an observational test and does not fix those inputs.

## Required next physical inputs

Before adding a claimed vacuum optical effect, supply:

1. A named action/route and admissible spacetime solution g_mu_nu, with units,
   topology scale, boundary conditions and stated validity domain.
2. A photon action. Either declare minimally coupled Maxwell propagation or
   derive a different optical characteristic equation from explicit couplings.
   Condensate acoustic characteristics cannot be substituted for photon rays.
3. A solved vacuum structure/shear profile and its metric or electromagnetic
   response. A drawn shear surface or chosen refractive index is an imposed
   toy input until that connection is derived.
4. Observer tetrad/motion, sources and ordinary foreground/occultation controls.
5. A frozen observable and exclusion criterion against the same-source control:
   angular deflection, time delay, image morphology or spectral signature.

The existing `Analysis/Lensing/LEN-001/len001_gravitational_lensing_solver.py`
inserts an acceleration interpolation and an algebraic mass-to-deflection
relation; its array of lensing/dynamical mass ratios is explicitly set to one.
It does not supply the needed metric ray integration. It was inspected, not
executed or changed. Its historical physics_pass flag is not authority for
this control, consistent with the live LEN-001 OPEN disposition.

## Dependencies and inherited holds

No R-tau or F-tau candidate action, perturbation estimate or background is
used as a photon metric here. The control therefore does not inherit their
calculation-specific review debt or treat either comparator as adopted.
The T3 addendum's periodic-mode/metric distinction is respected, but its
conditional matter force equations are not inputs to these rays.

Independent review is DEFERRED; this calculation is same-author local work.
Within the stated exact geometric methods scope, research may
PROCEED_PROVISIONALLY. Physical use of the illusion mechanism is
HOLD_SUBSTANTIVE for the missing metric/coupling/profile/calibration inputs.
LEN-001 OPEN; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED;
UVIR-003 IN_PROGRESS; canonical Tests 1-3 HOLD_SUBSTANTIVE.
No canonical promotion, publication readiness, manuscript revision, commit,
push or provider dispatch is performed.

## External context checked

Planck Collaboration, *Planck 2013 results. XXVI. Background geometry and
topology of the Universe*, https://doi.org/10.1051/0004-6361/201321546:
the quotient/covering-space construction is established cosmic-topology
methodology. No observational limit from this source is used to calibrate the
illustrative unit cell or to claim present-day observational viability.
