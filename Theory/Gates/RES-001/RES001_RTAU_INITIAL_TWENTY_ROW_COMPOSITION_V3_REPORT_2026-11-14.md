# Conditional initial twenty-row remainder estimate

The [frozen contract](RES001_RTAU_INITIAL_TWENTY_ROW_COMPOSITION_V1_CONTRACT_2026-11-14.md)
joins the previously calculated ordinary, force and corrected-density
rows in their actual common state. The result is an initial operator
comparison on compatible jets, not a finite-time evolution theorem.

## Actual state, operator and domain

Use the original periodic coordinate z, D=partial_z and the actual
canonical state from the
[state-map owner](RES001_RTAU_DENSITY_STATE_MAP_V1_REPORT_2026-11-14.md):

    Y20=(w,Q8,P9,zeta,xi),
    Q8=-i D phi, phi=R delta q_O, P9=delta p_O,
    O=(0,1,3,6,7,8,9,10,11), zeta=delta Z, xi=delta pi_psi,
    w=delta Sigma-c P xi-alpha D chi.

R is the constant eight-by-nine complement projection. The actual metric
trace is reconstructed by the corrected constraint inverse; its leading
trace graph is not imposed as an exact constraint. Configuration means,
metric moduli, force mean, eliminated momentum means and harmonic velocity
are retained. The original weighted range, total-I and U1 tangents remain
conditions on admissible inputs.

On the inherited smooth compatible Euler/constraint/auxiliary initial
jets, the five row identities give

    Y_t-S D Y = -A2(z) D^2 Y-i A1(z) D Y+R_init(Y,globals).

A2 and A1 are exactly the registered mixed principal matrices of
`rtau_mixed_principal_assembly_v1_20261104/receipt.json`. The displayed
coefficients act on the left. This is their original Fourier convention
k=-i D, not a divergence-form substitution. Coefficient derivatives are
retained in the remainder or already explicit first-order force entries.
Physical-time advection S D stays explicit.

This statement is conditional on exact compatible initial jets within
the certified prepared root enclosure. The finite numerical centre is
not declared an exact on-shell background. The estimate does not admit
arbitrary twenty-component tuples. A bounded remainder extends only to
the controlling-norm closure of this inherited initial domain; no
extension of the principal generator's domain or its preservation follows.

## Exact row identification

| State rows | Identity and completed numerical owner |
| --- | --- |
| w, row 0 | Actual material corrected-density source R_w, density V4 and subsequent physical-map/state-map calculations. The principal row is zero; the source is retained. |
| Q8, rows 1--8 | Ordinary velocity V2 followed by Q_t-S D Q=-i R V D Y-i R V_z Y-i D R R_v-i S_z R D delta q. The last three terms are bounded; R_v is H1. |
| P9, rows 9--17 | Ordinary momentum V3: negative derivative of the material Schur flux, its coefficient derivative and flux remainder, local reactions, S_z delta p and paired gauge response. The auxiliary-gradient coupling in metric rows 0,3 remains principal. |
| zeta, row 18 | Force-pair V2: -kappa a_phi D^2 xi-g D xi-v D zeta+Jrow D Y18+R_zeta. The complete reverse ordinary coupling is retained. |
| xi, row 19 | Force-pair V2: d D^2 zeta+(d_z-beta d s)D zeta-v D xi+R_xi. Regulator and lapse-gradient terms remain. |

The ordinary matrices are identified by the existing action-derived
Legendre/shift-Schur and canonical flux identities. In their notation,
with leading ordinary configuration-gradient map L and velocity V,

    A1_Q=R V,
    A1_P=-i B_R^T V+G_R L,
    F_lead=B_R^T V+i G_R L.

Consequently -i A1_P D Y=-F_lead D Y. Differentiating the
variable-coefficient flux adds -(F_lead)_z Y to the remainder. The ordinary
owner bounds that derivative along with the H1 flux remainder; it does
not assume a derivative of an arbitrary L2 momentum is bounded. Both
zero-speed directions of the inherited ordinary construction remain in
the full state, alongside both force directions. No slow projection or
spectral reclassification has been introduced.

The force self-block maps to

    A2_fast=[[0,kappa a_phi],[-d,0]],
    A1_fast=[[-i v,-i g],[i(d_z-beta d s),-i v]].

These yield the signs in the retained physical equations above. The
separate physical-rho observable has nonzero derivative terms and the
[138337 U remainder estimate](RES001_RTAU_PHYSICAL_DENSITY_REMAINDER_V2_REPORT_2026-11-14.md).
It is not an additional state row and is not substituted for w.

## Quantitative all-mode estimate

All five component bounds use the same nine inputs and original periodic
Sobolev convention. Let c_wj,c_Qj,c_Pj,c_Zj,c_xij denote their recorded
input-column coefficients. The conservative stacked estimate uses

    C_j=sqrt(c_wj^2+8 c_Qj^2+9 c_Pj^2+c_Zj^2+c_xij^2),
    ||R_init||L2 <=sum_j C_j U_j <=226066 U,

where U=sum_j U_j is the same original strong/global norm as the physical
density owner. Dimension factors 8 and 9 remain even where a parent bounds
the entire row group: the implied per-row bound suffices, so this
aggregation does not need a stronger interpretation of its norm estimate.
The maximum binary interval upper endpoint is approximately
226065.794133283. Decimal displays do not replace the binary certificate.

Using the actual state map,

    U<=5||Y20||2+sqrt(2)|mean(phi)|+Cmod|metric_moduli|
       +|mean(chi)|+sqrt(3)|eta|+|harmonic_velocity|,
    Cmod=exp(4/13000)sqrt(1+4/13000^2).

The remainder's state coefficient is therefore below 1130329, with the
remaining finite-dimensional weights recorded individually. These are
conservative initial bounds, not observed growth rates, a physical cutoff
or useful finite-time accuracy estimates.

## Evidence and remaining requirements

The [V3 executable](../../../Analysis/MasterTests/test_rtau_initial_twenty_row_composition_v3.py)
verified 424 pinned inputs and nineteen controls and replayed byte for
byte. Its [receipt](../../../Analysis/MasterTests/outputs/rtau_initial_twenty_row_composition_v3_20261114/receipt.json)
contains row ownership, all nine coefficient columns, the full state
ordering and explicit holds. Variable periodic and noncommuting matrix
controls verify the physical derivative signs, flux and gradient product
rules and detect omitted coefficient/material drift. Existing action
identities supply the row coefficients; the fixture does not replace them.

V1 stopped on a parent metadata-schema distinction. V2 then stopped
because a version substitution unintentionally renamed the unchanged
contract path. Both implementation failures, sources and sidecars are
preserved. V3 corrects those wrapper errors without changing the equations,
parents, norm or acceptance criteria.

This completes a conditional initial twenty-row remainder composition.
The full actual-generator contract remains incomplete: the periodic
normal-form time derivative, coupled energy time derivative, compatible
domain persistence and an actual background/evolution time tube are still
open. Their required background coefficient rates must be derived, not
obtained by differentiating interval error radii or assuming future
conformality. No time integral of these initial constants is justified.

Next: derive the initial time drift of the registered mixed principal
normal form, identifying any genuinely missing background jets, then
continue domain/energy control where supported. This result neither
adopts R-tau nor clears interactions, matching or numerical weak-field
predictions. Review DEFERRED; physics_pass=false; gate_effect=NONE.
