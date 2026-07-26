# UVIR-003 - Stage B three-dimensional khronon quartic audit

Date: 2026-07-26
Branch: `recovery/v12-core-architecture`
Status: **quartic flat-decoupling basis passed; complete physical 2-to-2 amplitude held**

## Executive result

The normalized hypersurface-orthogonal aether field has now been expanded
through fourth order in

```text
T = t + pi,
U_mu = -partial_mu T / sqrt[-(partial T)^2].
```

The calculation:

1. derives the complete three-dimensional flat-decoupling quartic basis;
2. reproduces the previous quadratic and cubic actions exactly;
3. contains 96 expanded quartic monomials;
4. reduces exactly to an independently generated one-dimensional quartic
   action;
5. derives the elastic centre-of-mass contact angular form;
6. proves that the elastic `t` and `u` cubic-exchange vertices vanish;
7. identifies the `s` channel as the non-invertible homogeneous khronon gauge
   orbit.

This is a passed interaction-readiness subgate. It is not a physical
strong-coupling result and does not close UVIR-003.

## Exact elastic contact result

For unit external spatial momentum, define

```text
c123 = c1 + c2 + c3,
c14  = c1 + c4,
x    = cos(theta).
```

After imposing the linear on-shell relation

```text
omega^2 = (c123/c14) |k|^2,
```

the quartic contact coefficient is

```text
C4(theta) =
  4 [c123^2/c14 - (2 c123 - c14) cos^2(theta)].
```

Its unweighted angular average is

```text
<C4> =
  4 [c123^2/c14 - (2 c123 - c14)/3].
```

This is the contact contribution only. It is not a partial-wave amplitude or
a unitarity cutoff because the gauge-regular exchange completion is missing.

## Exact elastic exchange result

Use all-incoming elastic centre-of-mass momenta. For a static `t`-channel
transfer, write the outgoing unit direction as `(y,0,x)`. The polarized cubic
vertex factorizes as

```text
V3,t proportional to x^2 + y^2 - 1.
```

The unit-vector identity `x^2+y^2=1` therefore makes the elastic `t`-channel
vertex vanish exactly. The `u` channel follows by crossing. The numerical
exchange values at representative angles are zero up to floating-point
roundoff, and the script asserts the exact symbolic identity.

The `s` channel is different. In centre-of-mass kinematics its internal
spatial momentum is zero:

```text
q_s = (-2 omega, 0).
```

The flat khronon inverse propagator is

```text
D_pi(q) =
  M_U^2 c14 |q|^2 [q_0^2 - c_s^2 |q|^2].
```

It vanishes at `|q|=0`, even when the internal frequency is nonzero. This is
the homogeneous preferred-time gauge orbit found independently by the low-`q`
ADM audit. Inverting it or simply dropping the channel would not define a
physical amplitude.

The flat-decoupling elastic result is therefore:

```text
contact = finite,
t/u exchange = zero exactly,
s exchange = homogeneous gauge mode, not invertible.
```

## Quartic constraint order

Let the quadratic algebraic constraint block be

```text
L2 = L2,phys + z^T J1 + z^T C z/2,
z = z1 + z2 + ...,
z1 = -C^(-1) J1.
```

At quartic order, the derivative of the cubic action supplies a quadratic
constraint source `J2`. The second-order solution is

```text
z2 = -C^(-1) J2.
```

Combining the quadratic and cubic contributions gives the Schur complement

```text
Lred^(4) =
  L4[x,z1] - J2^T C^(-1) J2/2.
```

Thus second-order lapse and shift information is genuinely required for the
reduced quartic action, although the solution can be incorporated directly
through this Schur-complement term. Third-order constraint solutions cancel
at quartic order.

## Scientific boundary

The physical interaction scale still requires:

1. the full evolving-FRW cubic vertex evaluated on first-order constraints;
2. the full evolving-FRW quartic vertex and second-order constraint Schur
   complement;
3. projection onto the regular physical scalar eigenmodes;
4. a gauge-regular exchange-plus-contact `2-to-2` amplitude;
5. the appropriate Lorentz-violating phase-space and partial-wave unitarity
   normalization.

Until those steps are complete:

```text
COMPLETE_PHYSICAL_2_TO_2_AMPLITUDE = NOT_YET_DERIVED
PHYSICAL_STRONG_COUPLING_SCALE = NOT_YET_DERIVED
UVIR-003 = IN_PROGRESS
MAT-001 = BLOCKED
```

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_3d_quartic.py
```

Output:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_aether_stueckelberg_3d_quartic_summary.json`

Expected footer:

```text
UVIR-003 three-dimensional khronon quartic basis: VERIFIED
Expanded quartic monomials: 96
Independent one-dimensional reduction: VERIFIED
Elastic COM quartic contact angular form: VERIFIED
Elastic COM t/u cubic exchange: VANISHES_EXACTLY
Quartic second-order constraint Schur complement: VERIFIED
COM s-channel: HOMOGENEOUS_GAUGE_MODE_NOT_INVERTIBLE
Complete physical 2-to-2 amplitude: NOT_YET_DERIVED
Physical strong-coupling scale: NOT_YET_DERIVED
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_QUARTIC_BASIS_WITH_2_TO_2_GAUGE_HOLD
```
