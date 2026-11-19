# A16.2: condensate radial-rate information determines the remaining pressure rate

16 November 2026. High retained. Conditional initial-point result in the
original R4C1/B1 linear control. No new action, field, reservoir, state or
thermodynamic law is adopted.

## What is held fixed

The tested original scalar chart has twelve state values. The following ten
reconstructed quantities are fixed when comparing perturbations:

1. conserved dust clock-current density and coordinate flux;
2. transverse metric area and its coordinate rate;
3. longitudinal frame Vx;
4. force field Pi and its normalized-frame temporal perturbation P_n;
5. reservoir field and its normalized-frame rate;
6. combined canonical u,v,r scalar energy perturbation, including the complete
   declared scalar potential.

The list groups ten independent rows. The fixed coordinate/observer convention
is the parent's clock/spatial gauge; no new gauge-invariant measurement protocol
or isolated-sector source is claimed.

We then also fix the combined scalar pressure and ask whether its normalized-
frame rate is determined. All maps and their background/lapse drift are retained.

## Exact result

| Retained information | Initial rank |
| --- | ---: |
| Ten held rows above | 10 |
| Held rows plus scalar pressure | 11 |
| Also include the pressure rate | 12 |
| Instead add normalized condensate modulus-squared rate | 12 |

The same result holds at ell=4,8,16,32,64. With the first eleven rows fixed,
there is exactly one scalar-chart null direction. It is the Cartesian radial
velocity perturbation delta u_dot at the registered u=1,v=u_dot=0 point.
The phase is rotating (v_dot=1); the radial rate is zero in the background,
not every scalar velocity.

Let s=u^2+v^2 and sigma=delta(n^mu partial_mu s), the normalized-frame
modulus-squared rate perturbation. For differences preserving the first
eleven quantities, the exact pressure-rate dependence is

    Delta pressure_rate=-(2341/1680) Delta sigma.

The quotient coefficient is computed from the full allowed nullspace, not
fitted from a selected pair. An exact row factorization using all twelve named
values reconstructs the pressure-rate row on the entire original scalar chart
at each tested initial point. The full coefficient row is in the receipt.
This is conditional on the other held quantities; pressure and sigma alone
are not asserted to form an autonomous two-variable model.

## Physical explanation and independent check

The original potential is

    U=s/2+s^2/24+s^3/480+r^2+r^4/28+3s r^2/28.

At the registered initial point U_u=2341/1680. A unit original delta u_dot
direction preserves all eleven held values. Its sigma is 2 and its scalar
pressure rate is -2 U_u. This separately checks the nullspace quotient against
the canonical kinetic/potential dynamics. With zero background radial velocity,
that radial-rate perturbation is invisible to the first-order instantaneous
energy and pressure, but it changes their later response to the radial force.

This identifies state information already carried by the condensate. It does
not require introducing a new fundamental force, interpreting the radial rate
as quantum information, or assuming equal entropy cancellation. Integrating
out such a state can produce a reduced history dependence; whether doing so
is controlled or useful still requires a domain/time-scale calculation.

The coefficient is specific to this action, background, normalization and
held quantities. It is not a general equation of state, Wilson coefficient,
universal acceleration scale or microscopic matching value. In particular this
dynamic-pressure result does not repair a rejected static radial mass portal
or supply the missing MAT soft-force residue.

## Method and evidence

[Frozen contract](RES001_A16_PRESSURE_STATE_V1_CONTRACT_2026-11-16.md),
[input pins](RES001_A16_PRESSURE_STATE_V1_INPUTS_2026-11-16.json),
[executable](../../../Analysis/MasterTests/test_a16_pressure_state_v1.py),
[receipt](../../../Analysis/MasterTests/outputs/a16_pressure_state_v1_20261116/receipt.json).
37/37 controls pass and fresh-directory replay is byte-identical.

The script reconstructs canonical scalar energy and pressure from the full
field map and the parent potential. The pressure-rate perturbation is
P_dot+P L-alpha p_background_dot, not just a frozen pressure row times L.
Rank/nullspace substitution, complete-state pressure-rate factorization,
proper-time correction, actual coefficient drift and an explicit independent
canonical radial direction are checked. These are same-assistant computational
checks, not independent peer review. Original sources, hashes, sidecars and
previous failed attempts remain unchanged.

The [matched-current pressure comparison](RES001_A16_MATCHED_CURRENT_V1_REPORT_2026-11-16.md)
and [reconstructed scalar state](RES001_A16_SCALAR_STATE_V1_REPORT_2026-11-16.md)
retain their original scopes. The scalar pressure is combined canonical scalar
plus potential stress, not a separately identified reservoir pressure or the
full stress tensor of an arbitrary state. At this linear homogeneous point
it is isotropic; no driven anisotropy or stable structure is demonstrated.

## Scope and next task

The registered point has s=1 and zero radial background rate, which matters
to the pure radial null direction and numerical coefficient. No extension to
other backgrounds, zero mode, nonlinear perturbations or finite-time map
persistence is made. Initial chart invertibility and state sufficiency do not
establish positive physical energy, stability, a causal interaction window or
an irreversible bath. There is no finite-time certificate for this new radial
initial direction yet.

Next derive controlled short-time scalar pressure/geometry response for the
specified radial-rate direction, or establish a justified restriction/domain
that prevents its use. Keep the full coupled system, clock-current and global
restrictions. The old four-column certificate is not automatically transferred.
Only then assess a useful reduced stress/history law and the time scales on
which radial information could be eliminated.

Review DEFERRED; physics_pass=false; gate_effect=NONE. G1–G6 and MAT matching
remain incomplete; R-tau is a separate unadopted comparator. No thermodynamic
entropy sign, organizing force or publication readiness follows.
