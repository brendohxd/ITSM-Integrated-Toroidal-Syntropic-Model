# A16.2: deterministic history map and direct channel inventory

15 November 2026. Conditional mathematical consequence of the registered
R4C1/B1 linear split, with bounded computational controls. This does not
replace the parent action, extend its physical domain, or identify a bath.

## Exact bridge from the existing split

Use q=(D,Vx), c=z-E_z q, O_z c=0 and L_d=M+Delta. The existing owner gives

    qdot=L_d q+R c,
    cdot=S q+J c.

Here c denotes the twenty-component constrained complement, not a new field;
the scalar reservoir amplitude in the underlying action is a different r.
Let U_J(t,s) solve partial_t U_J=J(t)U_J, U_J(s,s)=I in the original ambient
state space on the supported regular interval. Variation of constants gives

    c(t)=U_J(t,0)c(0)+integral_0^t U_J(t,s)S(s)q(s) ds,
    qdot(t)=L_d(t)q(t)+f_initial(t)+integral_0^t K(t,s)q(s) ds,
    f_initial(t)=R(t)U_J(t,0)c(0),
    K(t,s)=R(t)U_J(t,s)S(s).

The complement constraint moves with O_z(t). The inherited moving-map identities
support its transport in the full coupled solution; this is not a fixed-kernel
projection or a new unconstrained twenty-degree-of-freedom subsystem. U_J alone
must be used with the inherited compatibility conditions and S source.

All coefficient/basis/momentum drift is already in the parent operators.
For the evolving background this is a two-time kernel, not an assumed stationary
K(t-s), exponential relaxation or delta-function friction. A prepared c(0)=0
eliminates initial hidden forcing, not the history term. Zero q(0) permits later
response when hidden initial data are nonzero. Enlarging the retained state may
remove or change this memory representation; no irreducible memory is claimed.

## Direct support in the actual exported chart

The existing saved R has shape 2 by 20. Exact symbolic support inspection finds:

| Balanced chart group | Column indices | Direct R support |
| --- | --- | --- |
| Scalar metric coordinate and rate | 0,10 | Present |
| Tensor chart coordinates and rates | 1,2,11,12 | Absent in R |
| Longitudinal frame coordinate and rate | 3,13 | Present |
| Transverse frame coordinates and rates | 4,5,14,15 | Absent in R |
| Cartesian condensate amplitudes and rates | 6,7,16,17 | Present |
| Reservoir amplitude and rate | 8,18 | Present |
| Mixed force coordinate and rate | 9,19 | Present |

For example R[0,8]=-15 i a^2 r_dot/ell^2 in this registered chart. This is a
coefficient of an allowed complement vector, not a measured response to an
independently varied reservoir. It can vanish at special backgrounds such as
r_dot=0; generic export support is not a nonzero theorem at every state.

The force coordinate chi=p^2 Pi-i p psi_dot Vx already mixes force and frame.
The complement constraint and propagation J can mix input directions. Therefore
the table is a coordinate-support inventory, not invariant apportionment of
physical memory. Absent direct R entries alone prove no whole-system decoupling.
The coefficients were specialized to the original diagnostic action/family;
setting a coupling to zero in them would not reconstruct a different theory.

## Evidence and limits

[Frozen contract](RES001_A16_HISTORY_MAP_V1_CONTRACT_2026-11-15.md),
[input pins](RES001_A16_HISTORY_MAP_V1_INPUTS_2026-11-15.json), and
[executable](../../../Analysis/MasterTests/test_a16_history_map_v1.py).
[Receipt](../../../Analysis/MasterTests/outputs/a16_history_map_v1_20261115/receipt.json):
16/16 symbolic, rational and structural controls passed; a fresh-directory replay
is byte-identical. An exact determinant-one matrix P(t) supplies a genuinely
time-dependent noncommuting J=Pdot P^-1 and U=P(t)P(s)^-1. Controls retain source
feedback and hidden initial data and reject reversed endpoints and frozen drift.
A separate scalar integrating-factor control and actual R support checks pass.
These are same-assistant computational checks. The small matrix is an algebra
fixture, not a reduced ITSM simulation or error certificate for U_J.

The [original split owner](RES001_R4C1_G3N5_DUST_REMAINDER_REPORT_2026-10-11.md)
supplies the actual R/S/J equations. The
[finite-mode owner](RES001_R4C1_G3N5_DUST_FINITE_K_REPORT_2026-10-11.md),
sections Domain and Initial Data, owns the balanced coordinate definitions.
The [dust certificate](RES001_R4C1_G3N5_DUST_CERTIFIED_NUMERICAL_REPORT_2026-10-12.md)
and [allocation control](RES001_A16_SECTOR_SPLIT_V1_REPORT_2026-11-15.md)
remain unchanged. No fresh full-trajectory or inherited certificate replay is
claimed here. Physical kernel entries, approximation error and normalization
have not been computed by this executable.

## Interpretation and next deciding work

The existing equations already contain a deterministic mechanism by which
unretained field data affect later dust response. This is the formal memory of
a reduced description, not proof of a new fundamental organizing force. The
outstanding question is its physical identification and usefulness.

Next establish constraint-compatible, non-gauge input/source directions and
the operational retained observables before attributing effects to the reservoir.
Retain total stress, global charges and the original action. Pure coordinate
slots and deleted couplings cannot serve as physical interventions. Determine
whether adding the force or other retained variables closes the response, or
whether a useful residual history operator remains. Only then compute its
physical gain, time scales and controlled approximation on covered data.

No fluctuation-dissipation law, noise ensemble, entropy production, selected
structure, galaxy prediction, causal cutoff or MAT coefficient follows here.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1–G6 incomplete;
R-tau remains a separate unadopted comparison route.
