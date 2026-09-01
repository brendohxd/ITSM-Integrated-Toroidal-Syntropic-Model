# PKM1 A2-A6 bounded obstruction audit

**Calculation:** `PASS_SCOPED_A2_A6_AUDIT`  
**Disposition:** `ADVANCE_PKM1_TO_FULL_PARENT_HAMILTONIAN_ONLY`  
**Physics pass:** `false`

## What survives

In the smooth timelike phase chart, `Theta=mu_Theta t` gives `Q=1/N` and
`a_i=D_i ln N`. The candidate action therefore contains spatial derivatives
of the lapse but no lapse or shift velocities. This is consistent with a
khronometric constrained scalar, although it is not the full Dirac count.

The particular nonlinear product `J_Y a_i a_j` starts at second perturbative
order around a zero-acceleration background, so that term cannot by itself
source linear traceless slip. This is not a proof that the complete ITSM
parent has equal metric potentials: the khronon, susceptibility, amplitude and
constraint contributions remain uncomputed. The metric-hosted
modified-Poisson equation retains universal source normalization. A generic
`K(Q)` supplies an additional static Helmholtz term; exact AQUAL requires
`K_QQ(1)=0` or a controlled local regime where that term is negligible.

## New obstruction

A stable algebraic heavy mode with energy affine in `Y` cannot generate the
required deep energy. At its stable stationary point,

`F''(Y)=-(b')^2/(U''+b''Y) <= 0`,

whereas `F_target=C Y^(3/2)` has

`F_target''=3 C/(4 sqrt(Y)) > 0`.

Thus a simple radial/heavy integrate-out cannot microscopically produce PKM1's
convex deep operator. A viable parent must use non-affine coupling, a
constrained or propagating polarization sector, nonlocal dynamics, or treat
`J` as fundamental controlled EFT data.

## Constructive non-affine control

The scoped obstruction can be evaded algebraically. For `s>0`, the constructed
static energy

`F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3`

has `s_star=sqrt(Y)/a0`, positive curvature `2 a0 sqrt(Y)`, and exactly

`F_eff(Y)=(2/3)Y^(3/2)/a0`.

This was built from the desired operator and is **not** a microscopic
derivation. It identifies a narrower possibility to test: a non-affine,
critically soft susceptibility or constrained polarization. Both `s_star` and
its stiffness vanish at `Y=0`, so the constraint rank, Hamiltonian and strong
coupling at that boundary are the decisive risks. It cannot be identified with
the stable gapped condensate radial mode rejected by M2.

The naive canonical cubic scale is `Lambda_0=sqrt(a0 M_P)`, but this is not a
physical cutoff until the full constrained amplitude is calculated.

## Decision

PKM1 is the only survivor among the broad controls explicitly screened here
because it bypasses the independent direct matter residue. It advances only to
one explicit parent-action Hamiltonian calculation, using the non-affine
susceptibility as a hostile constructive control. The live action and every
gate status remain unchanged.
