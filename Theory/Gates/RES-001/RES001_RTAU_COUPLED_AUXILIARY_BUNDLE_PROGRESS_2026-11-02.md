# Coupled observable-norm bundle: auxiliary and canonical rate map

High confirmed for this continuing bundle. This report records substantive
component progress, not completion of the coupled norm/generator contract.
R-tau remains unadopted; physical_norm=NOT_DERIVED; physics_pass=false;
gate_effect=NONE; review DEFERRED. Original G1–G6 remain incomplete.

## Full metric and velocity variation

The complete auxiliary relation was varied in all six metric entries and
their time velocities, retaining determinant/inverse terms and scalar force
variation. Writing mu=sqrt(det h), H=h^-1, c=mu Hzz, k=delta h, l=delta h_t,
the tensor coefficient of delta c is

    D=mu*(-H[:,z] H[z,:]+Hzz*H/2).

Its time variation includes both l and the evolving background metric. The
divergence formulation permits integration by parts before estimating the
rough velocities: no derivative of l is needed for this component's H-2 bound.
The earlier strong point evaluator's l-through-third-derivative requirement
therefore must not be mistaken for a necessary physical phase-space condition.

On the actual original initial background, with full-matrix Frobenius metric
norms and coordinate Bessel H-2, conservative upward-rounded constants give

    ||delta Z_t||H-2 <= 1.000770 ||delta psi_t||L2
                     +3.468336 ||delta psi_z||L2
                     +0.001010 ||delta h||L2,F
                     +0.000227441 ||delta h_t||L2,F.

These include the whole circle and certified H/root correction, rather than
only the numerical centre. Gaussian/observational matching or new physical
scale input is not involved. The two-tensor time-variation identity is an
actual coupled observable calculation, not a fixed-coefficient scalar test.

Specification: `RES001_RTAU_COUPLED_AUXILIARY_VARIATION_V1_SPEC_2026-11-02.md`.
Producer: `Analysis/MasterTests/test_rtau_coupled_auxiliary_variation_v1.py`.
Receipt: `Analysis/MasterTests/outputs/rtau_coupled_auxiliary_variation_v1_20261102/receipt.json`.
**7/7 exact controls**, immutable replay byte-identical. Controls independently
differentiate the strong full-metric Laplace-Beltrami coefficients, retain all
six metric perturbations, check Lie transport with tensor-index terms and a
constant metric mode, and reject omission of independent metric velocity.
Local rational fixtures check identities; analytic profile bounds and outward
interval arithmetic establish the actual initial constants.

## Initial canonical and gauge-rate composition

The full scalar-observable estimate was then composed with the already
certified initial Legendre inverse and periodic gauge-velocity map. The actual
global Hessian supplies L_vq/L_vd block bounds. Their auxiliary Z/Z_z columns
are exactly absent under the owning sparse convention, not discarded as small.
The signed/indefinite constraint direction is not interpreted as positive
physical kinetic energy.

Define Q0=||delta q||L2, Q1=||partial_z delta q||L2 and P0=||delta p||L2
for all thirteen nonauxiliary canonical slots in the original coordinate.
For compatible initial canonical data and the declared linear coordinate-rate
construction, with Hc the retained adapted harmonic coordinate-velocity norm,
the corrected conservative estimate is

    ||delta Z_t||H-2 <= 24.084505 P0 +58.858560 Q0
                       +5.604964 Q1 +0.000554257 Hc.

This is a coordinate control bound on an initial observable-rate map. It is
not a positive physical Hamiltonian norm or a transported evolution theorem.
Physical metric-modulus rates remain constants in the periodic solve; the
harmonic coordinate inputs are retained separately, not confused with those
physical modes or with physical clock evolution.

### Preserved correction

The V1 composition omitted the L2 measure conversion and pulled-back H1
derivative factors. Its constants are withdrawn as certified bounds. The V1
source, specification, raw receipt and interpretation-hold record remain intact.
V2 uses source factor sqrt(J_upper) and

    Cback=J_lower^(-1/2)*
          (max(1,J_upper,1/J_lower)+r/J_lower), r=1/13000.

The exact identity derivative_z[xi_z(zeta)/J]=xi_z,zeta-lambda_z*xi_z/J
and transverse derivative_z xi=J*xi_zeta supply these factors with
dz=d_zeta/J. No action, input, posterior, diagnostic threshold or norm target
was changed by this correction. All original scientific evidence is preserved.

V2 specification: `RES001_RTAU_CANONICAL_AUXILIARY_PULLBACK_V2_SPEC_2026-11-02.md`.
Producer: `Analysis/MasterTests/test_rtau_canonical_auxiliary_pullback_v2.py`.
Receipt: `Analysis/MasterTests/outputs/rtau_canonical_auxiliary_pullback_v2_20261102/receipt.json`.
**10/10 controls**, exact immutable replay. These include the exact sparse
auxiliary-column check, slot-to-full-matrix Frobenius conversion, Lie estimate
and coordinate chain rule. Functional Legendre/gauge estimates are inherited
from their owning continuum proofs, not inferred from finite fixtures.
All 219 inherited source hashes still match after execution.

## Remaining deciding work in the same bundle

1. Relate this initial canonical control topology to the physical observables
   and the nonlocal density/trace/weighted-momentum graph. The order-minus-two
   symplectic density block and every cross/modulus block remain essential.
2. The weak auxiliary-rate bound does not control strong auxiliary energy or
   establish physical admissibility of arbitrary H1/L2 data. Force H2-type
   observables and the actual matter/density regularities still need analysis.
3. Retain the longitudinal source-range condition, global I/Q tangents,
   means, physical clock flow, gauge/chart derivatives and moving inverse.
4. Derive a closed generator estimate with zero-speed/quartic/subleading
   coupling, and a genuine background tube before any finite-time claim.

No coupled norm, [0,.05] theorem, interaction window, microscopic match or
theory-fixed acceleration prediction has been established. No manuscript/site
claim changes are warranted. High acknowledgement remains valid for continuing
this bundle; no repeated setting approval is needed at this component receipt.
No commit, push, publication, model dispatch or vault mutation occurred.
