# A16.2: matched current and geometry expose a scalar-pressure ambiguity

16 November 2026. High retained. Conditional initial-point result in the
unchanged registered R4C1/B1 linear export. No new physical source, bath,
equation of state or parent action is adopted.

## Stricter preparation

Use the reconstructed twelve-value scalar state from the
[scalar-state owner](RES001_A16_SCALAR_STATE_V1_REPORT_2026-11-16.md).
For a reservoir configuration direction or normalized-frame reservoir-rate
direction, compare two initial protocols:

1. compensate using condensate phase configuration and normalized phase rate;
2. compensate using phase configuration and condensate modulus-squared value.

The declared two-by-two solves enforce N_tau=F_tau=0. Both protocols also
have D=Vx=Pi=P_n=0 and zero transverse area and area rate. All unspecified
scalar-state values are zero, including the initial Vx coordinate rate and
normalized condensate modulus-squared rate. The other reservoir value is
zero; the designated reservoir direction is the same in both protocols.
These are specific infinitesimal preparations, not every possible compensation.

Reconstruction verifies that lapse and shift vanish initially. The scalar
spatial metric and its initial area rate agree; no tensor/transverse seed is
introduced. Original nonzero-mode constraints and fixed gauge are inherited.
The flux is the actual normalized coordinate flux of the conserved dust clock
current, not the frame variable Vx used as a proxy in the earlier experiment.

## Initial outcome

At ell=4,8,16,32,64, both protocols now give zero initial D_dot and N_tau_dot.
The earlier density-rate difference disappears after proper current and
geometry matching. The frame-rate difference is also zero, consistent with
the explicitly unexcited Vx-rate state value. It is not a new prediction of
universal preparation-independent frame acceleration.

The coordinate current-flux rate and transverse-area acceleration still differ.
Those outputs retain their original clock/chart definitions; neither is here
identified with an invariant measured force or a newly constructed curvature
observable. The same reservoir input does not determine them independently
of how the condensate compensates its energy and momentum.

## Independent scalar-stress audit

The background's declared combined canonical u,v,r potential is

    U=s/2+s^2/24+s^3/480+r^2+r^4/28+3s r^2/28, s=u^2+v^2.

At u=r=1, v=u_dot=0, v_dot=1, r_dot=1/4 and zero lapse,

    delta K=delta v_dot+delta r_dot/4,
    delta U=(2341/1680)delta u+(33/14)delta r,
    delta rho_scalar=delta K+delta U,
    delta p_scalar=delta K-delta U.

An independent script evaluates these expressions from the stored original
twenty-state directions, rather than inferring pressure from the acceleration.
Both protocols have zero combined scalar energy perturbation and zero initial
scalar momentum perturbation. They have different pressure because their
kinetic/potential perturbations compensate differently.

| Reservoir direction | Pressure difference: protocol 1 minus 2 | Area-acceleration difference |
| --- | --- | --- |
| Configuration | -77253/28147 | 70230/28147 |
| Normalized-frame rate | -2341/8042 | 11705/44231 |

These direction-normalized values are not measured amplitudes or a physical
acceleration scale. Both differences are the same at all five registered
modes. In each case the coupled exported geometry obeys exactly

    Delta area_ddot=-(10/11)Delta p_scalar,
    Delta area_ddot=2 i ell Delta F_tau_dot.

The coefficient uses the registered B1 cosmological gravitational factor
11/10, whose background constraint is (33/10)H^2=energy. It was not fitted
to these differences and is not a universal Newton/matching coefficient.
The geometric relation is checked only for these initial protocol differences.

The audited pressure is the combined canonical scalar-plus-potential stress,
not an independently defined reservoir pressure or the full stress tensor in
an arbitrary state. Including the complete declared scalar potential prevents
moving the portal energy between named sectors from changing this combined
quantity. The initial linear scalar pressure here is isotropic; no directional
stress, toroidal attractor or persistent anisotropy mechanism is established.

## Scientific implication

For these allowed linear preparations, matched matter transport, initial
geometry and scalar energy do not determine the pressure. The existing
action already encodes that missing state information. This is a concrete
reason why a reduced law based only on an exchange current or density cannot
stand in for the complete scalar dynamics.

It identifies a constitutive/state-description obligation, not a new force:
which retained variables or preparation determine the relevant stress response?
A reduced memory kernel could encode discarded stress information, but no
irreducibility, thermal state, dissipation, entropy production or organizing
effect follows from the existence of different reversible preparations.

## Verification and preservation

[Matched-current contract](RES001_A16_MATCHED_CURRENT_V1_CONTRACT_2026-11-16.md),
[input pins](RES001_A16_MATCHED_CURRENT_V1_INPUTS_2026-11-16.json),
[executable](../../../Analysis/MasterTests/test_a16_matched_current_v1.py),
[receipt](../../../Analysis/MasterTests/outputs/a16_matched_current_v1_20261116/receipt.json):
182/182 symbolic/current/reconstruction/preparation controls.

[Scalar-stress audit contract](RES001_A16_SCALAR_PRESSURE_V1_CONTRACT_2026-11-16.md),
[audit pins](RES001_A16_SCALAR_PRESSURE_V1_INPUTS_2026-11-16.json),
[audit executable](../../../Analysis/MasterTests/test_a16_scalar_pressure_v1.py),
[audit receipt](../../../Analysis/MasterTests/outputs/a16_scalar_pressure_v1_20261116/receipt.json):
61/61 independent potential-derivative, scalar energy/momentum and response
consistency controls. Both receipts have byte-identical fresh-directory replays.
These are same-assistant computational checks, not external scientific review.
Original sources, hashes, sidecars, earlier protocols and their outcomes remain
unchanged. The old four-column finite-time certificate is not transferred.

## Next supported question

Define an operational stress/state closure or quantify how response depends
on admissible preparations. Compare only physical quantities whose observer,
geometry and compensation conditions are explicit. A time-dependent pressure
or memory claim needs new controlled evolution/error estimates for the chosen
directions; do not infer persistence from these initial acceleration identities.
No additional parent, prescribed source, empirical calibration or thermal bath
may be inserted silently to remove this state freedom.

Review DEFERRED; physics_pass=false; gate_effect=NONE. Physical domain/energy,
G1–G6 and MAT matching remain open; R-tau is a separate unadopted comparator.
