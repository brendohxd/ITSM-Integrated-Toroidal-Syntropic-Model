# A16.2: reconstructed scalar state closes the registered initial response

16 November 2026. High retained by operator. Conditional R4C1/B1 linear
control; no new action, field, bath, background or physical gate is adopted.

## Result

The original twenty-state system admits an exact symbolic decomposition
into twelve scalar chart components and eight tensor/transverse components.
Both cross blocks of the full generator vanish in this decomposition. This
checks the complete exported linear generator, not merely a principal symbol.
The dust observation map and the reconstructed scalar-state map annihilate
the tensor/transverse block.

The twelve scalar components can be expressed as six reconstructed field
configurations and six rates:

| Configuration | Definition in the existing fixed chart | Rate used |
| --- | --- | --- |
| Transverse area | (M_yy+M_zz)/2, the linear transverse log-area perturbation | Coordinate-time rate |
| Longitudinal frame | Original reconstructed Vx | Coordinate-time rate, not a claimed invariant frame acceleration |
| Condensate modulus squared | delta s=2u delta u+2v delta v | delta s_dot-s_dot alpha |
| Condensate phase | delta theta=(u delta v-v delta u)/(u^2+v^2) | delta theta_dot-theta_dot alpha |
| Reservoir field | delta r | delta r_dot-r_dot alpha |
| Force field | Pi | Pi_dot-psi_dot alpha |

The scalar rates refer to the parent's normalized frame on the homogeneous
background. Lapse and actual background/observation-map drift are retained.
The phase map requires s=u^2+v^2 nonzero and is a local linear phase chart;
it neither removes winding sectors nor defines a global phase branch.
Here s is the condensate modulus squared, not its Noether number density,
a statistical entropy or a thermodynamic state variable by identification.

## Initial inversion and generator

Let E embed the original scalar coordinates and their rates into the
twenty-state chart. Let Q reconstruct the twelve values above. At the
registered initial background, for every ell=4,8,16,32,64:

    rank(Q E)=12, det(Q E)=4,
    rank(stack(Q E,(Q_dot+Q L)E))=12.

The executable computes the exact inverse and initial transformed generator

    G_scalar=(Q_dot+Q L) E (Q E)^-1,
    O_dust_scalar=O E (Q E)^-1.

Exact recomposition recovers both the full scalar rate and original dust
map. The receipt exports each initial generator and dust map. No numerical
rank thresholds, dropped source direction or fitted coefficient is used.
The determinant is a chart-dependent result of the stated variables and
normalizations, not a new physical invariant or universal coefficient.

At ell=4 the density-contrast row depends on most of these coupled values,
including reservoir field and its proper rate; the velocity observation is
the reconstructed longitudinal-frame channel. Changing a reservoir value
while holding all other scalar-state values fixed therefore need not hold
the dust density fixed. A matched-dust comparison needs an explicit compatible
compensation/source prescription, not deletion of a coupling or a raw slot.

## Meaning for the memory route

The lower-dimensional dust/force/rate descriptions previously tested were
not sufficient states for this same linear control. This field-based scalar
description is sufficient at the tested initial points. Thus those earlier
failures do not prove irreducible memory or demand a new fundamental force.
They are consistent with information being hidden by the chosen reduction.

The exact two-time history representation remains available when fields are
eliminated. Whether a smaller history law is useful, has controlled errors,
or corresponds to an irreversible reservoir remains a different question.
This is not a thermal coarse graining, a fluctuation-dissipation calculation,
an entropy-production law, or a structure-selection mechanism.

## Evidence and limits

[Frozen contract](RES001_A16_SCALAR_STATE_V1_CONTRACT_2026-11-16.md),
[input pins](RES001_A16_SCALAR_STATE_V1_INPUTS_2026-11-16.json),
[executable](../../../Analysis/MasterTests/test_a16_scalar_state_v1.py),
[receipt](../../../Analysis/MasterTests/outputs/a16_scalar_state_v1_20261116/receipt.json).
32/32 controls pass; fresh-directory replay is byte-identical.

Checks include the constant SO(2) decomposition and both exact cross blocks,
reconstructed map and rate annihilation on the omitted block, an independent
two-by-two modulus/phase inverse with determinant two, field/area/frame
identities, lapse and time drift, initial Friedmann constraint, and exact
generator/inverse/dust recomposition at each mode. These are same-assistant
computational controls, not external scientific review. Original sources,
hashes and previous failures remain unchanged.

The symbolic block split holds wherever its original coefficient expressions
are regular. The reconstructed field-map inversion and generators are checked
at the specified initial points only. No uniform inverse bound, finite-time
error control for new states, nonlinear domain preservation or global phase
map is established. Zero mode, endpoints, physical gauge/source admission,
positive kinetic/energy properties and interacting window remain separate.
The older B1 and R4C1 stability qualifications are not removed by an invertible
change of variables. Twelve scalar chart values do not certify twelve healthy
physical degrees of freedom.

## Next supported work

Use the reconstructed state and exact dust map to specify a compatible
paired-state/source comparison. Identify which measured or operationally
defined values are held fixed, how constraints require compensation, and
whether the comparison isolates reservoir response or only a coupled scalar
response. Retain global charges and the original action. Finite-time or
kernel-gain claims require the corresponding new error/domain control.
The microscopic reservoir/state/coarse-graining and organizing-mechanism
questions remain Open, alongside matching and G1–G6.

Review DEFERRED; physics_pass=false; gate_effect=NONE. R-tau remains a separate
unadopted comparator. No canonical promotion or publication readiness follows.
