# Prepared evolution local composition kernel V2

1 November 2026. Routine implementation, not a new physical-norm derivation.
Review DEFERRED; physics_pass=false; gate_effect=NONE; R-tau unadopted.

## Implemented scope

The [kernel](../../../Analysis/MasterTests/r4c1_prepared_evolution_kernel_v2.py)
composes the previously derived canonical velocity/momentum, full-metric
auxiliary, clock-current and direct canonical-density time rows. It accepts
thirteen nonauxiliary canonical field/momentum perturbation jets, explicit
background/tangent force fourth derivatives and caller-supplied shift jets.
The auxiliary value and its time value are reconstructed, rather than
supplied as an independent kinetic degree of freedom.

Nonauxiliary field rates have second spatial jets. Auxiliary time rate is
returned only as a value; momentum-rate spatial derivatives are returned
only for metric/frame rows where they were actually computed. No scalar or
auxiliary higher time-spatial rates are fabricated. The nonzero background
and general-probe density/current Ward residuals remain visible in output.

This is a LOCAL point kernel. It neither solves a global periodic gauge
or constraint problem nor certifies that arbitrary supplied jets are
compatible physical data. Global I/Q conditions, weighted longitudinal
range, harmonic/modulus data and evolving operator domains remain caller/
analysis requirements. The full first item of the
[physical-norm contract](RES001_R4C1_RTAU_PHYSICAL_NORM_V1_CONTRACT_2026-11-01.md)
is therefore incomplete; a global compatible evolution operator is not
claimed merely from this composition.

## Sparse-zero implementation defect and repair

The first integration driver reached a pure-shift probe, where the density
helper accessed reg.g[1]. The configuration tangent is exactly zero in
that probe, so the sparse derivative algebra correctly omits that entry.
The lookup raised KeyError:1; it did not produce an incorrect physical
prediction. Its [failure record](../../../Analysis/MasterTests/outputs/r4c1_rtau_evolution_kernel_v1_attempt_01/failure.json)
and all V1 sources remain sealed.

[Density helper V2](../../../Analysis/MasterTests/r4c1_density_time_transport_v2.py)
uses the existing J(0) convention for absent sparse time/tangent derivatives.
Kernel V2 selects that helper. The equations, nonzero derivatives, inputs
and1e-28 local tolerance are unchanged. This sparse-zero code path is
distinct from the unresolved physical zero-speed characteristic branch.
The earlier full nonzero-tangent density result remains valid in its scope;
it did not exercise this absent-entry boundary.

## Verification

[Integration executable V2](../../../Analysis/MasterTests/test_01_r4c1_rtau_evolution_kernel_v2.py):10/10.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_evolution_kernel_v2_attempt_01/summary.json)
SHA256 7b1ae5d9052cd5b210f65d6106712ed51ca91fd8f32dc69497ec11724ad8eec7.
Immutable replay COMPLETE, native session7960 terminal exit0, byte-identical.
The experiment checks422 inherited/current source and sidecar byte/mtime
pairs. No live calculation remains; do not repeat this unchanged replay.

Controls compare the composed all-field background/tangent Ward residuals
with the independently frozen raw-density/current calculation. A pure shift
is compared with the full canonical Lie field and dual momentum-density
response, retaining the density Jacobian and current advection. The exactly
zero canonical direction produces zero composed rates. These test integration
boundaries; they are not a new physical stability/evolution certificate.

## Next required work

The physical derivative counts, mixed norm, zero-speed/quartic/background
coupling, moving compatible inverse and quantitative domain/time estimates
remain NOT_DERIVED. The next hard calculation follows the frozen physical-
norm contract and203-input manifest, augmented by this implementation and
its preserved failure/repair. The fresh High-confirmation request supersedes
the previous return-to-Medium request; no model/setting change is inferred.

The current local results do not change matching inputs or P1/P2,
Thermodynamics or original R4C1 claims. Global composition, nonlinear
persistence, transverse modes, interactions/window, GR/local compatibility
and G1-G6 remain incomplete. Same-author replay is not external review.
No action adoption, provider dispatch, vault mutation, publication, commit,
push or deployment.
