# ITSM PKM1 broad-route decision — metric-hosted condensate foliation

**Date:** 2026-08-25  
**Branch:** `recovery/v12-core-architecture`  
**Decision:** `ADVANCE_ONE_FULL_PARENT_HAMILTONIAN_TEST_ONLY`  
**Route status:** `OPEN_RESEARCH_CANDIDATE`; new action class, not the live action  
**Physics pass:** `false`  
**Commit/push/publication:** not performed

## 1. Outcome

The broader search found a real mechanism-level partial resolution, but not a
complete ITSM theory.

Move the low-acceleration response from a separately matter-coupled force
scalar into the metric constraint associated with the condensate-defined time
foliation. Ordinary matter then couples universally to one metric. Within this
candidate IR action there is no independent direct coupling `C_m`, so the live
separate-field residue `C_m/sqrt(K_Q)` is bypassed rather than guessed.

The unresolved burden has moved, not disappeared:

1. the function `J(Y)`, its coefficient and `a0` are not derived from the
   finite-density condensate;
2. the exact fractional-power response forces a critical or otherwise
   non-analytic zero-gradient sector;
3. the complete amplitude–phase–metric constraint algebra, Hamiltonian,
   characteristics, high-acceleration join and global winding domain remain
   open.

The correct disposition is therefore one bounded parent-action Hamiltonian
test. No observational fitting or gate migration is authorized.

## 2. Authority and scope re-anchor

The decision was made after rereading the binding scientific-integrity rules,
Core Identity Briefing, Core Architecture, Master Research Plan, Tier-1 route
programme, G0 report, post-G0 plan, RG1 decision, RG1-to-P2 checkpoint, live
dashboard, MAT force-hosting/R5 decisions and the M2/M4/U2 outputs.

The binding baseline remains:

- UVIR-003: `IN_PROGRESS`, `HOLD_TIER1_CLOSURE`, `physics_pass=false`;
- MAT-001: `BLOCKED`, `V NOT_COMPUTED`, `K_Q NOT_DERIVED`;
- M2 minimal radial/heavy classes: rejected as a residue derivation;
- U2: frozen at A0–A2 for incomplete action/domain/DOF;
- S0: not a complete local-gravity route;
- no local-gravity, lensing, disk, SPARC, cosmology or publication stage open.

PKM1 changes the force host. It cannot inherit credit from the rejected M2,
frozen U2 or live separate-`psi` action.

## 3. Candidate action class

On a smooth finite-density phase chart,

`Phi=(rho/sqrt(2)) exp(i Theta)`,

define

`U_mu=-nabla_mu Theta/sqrt(-nabla_Theta^2)`,

`Q=sqrt(-nabla_Theta^2)/mu_Theta`,

`a_mu=U^nu nabla_nu U_mu`, and `Y=a_mu a^mu`.

The controlled IR candidate is

`S=(M_P^2/2) integral sqrt(-g)[R-2 J(Y)+2 K(Q)] + S_m[Psi_m,g]`.

This makes three deliberate architecture changes:

1. the preferred vector is derived from the condensate phase rather than kept
   as an independent aether;
2. the lapse/metric potential becomes the weak-force host rather than a
   separate `psi` field;
3. matter remains minimally and universally coupled to `g_mu_nu`.

Those changes avoid the present double-counting and direct-residue problems,
but they require a new architecture decision before canonical adoption.
Finite density, amplitude zeros, winding, compact `T^3` boundary conditions
and the reservoir remain part of ITSM; they are not supplied by the displayed
IR action.

## 4. Conditional stationary weak-field result

For the deliberately selected control

`mu(y)=(y+y^2+y^3)/(1+y+y^2+y^3)`, with
`y=|grad Phi_N|/a0`,

the constructed primitive

`J=a0^2[ln(1+y)-ln(1+y^2)/2-atan(y)]`

satisfies

- `1+J_Y=mu` exactly;
- `J=-Y+(2/(3a0))Y^(3/2)+...` and `mu~y` as `y->0+`;
- `mu->1` and `J->-pi a0^2/2` at high acceleration;
- positive transverse and radial static ellipticity eigenvalues for every
  `y>0`.

For a regular expansion

`K(Q)=K_0+(K_QQ(1)/2)(Q-1)^2+...`,

the stationary weak-field variation gives

`div[mu(|grad Phi_N|/a0) grad Phi_N]+m_K^2 Phi_N=4 pi G rho_b`,

where `m_K^2=K_QQ(1)/2` in the displayed convention. Exact AQUAL requires
`m_K=0`, or a declared local regime in which the Helmholtz term is negligible.
In that subcase, spherical deep acceleration gives

`g=sqrt(a0 g_N)`.

This establishes an action-level existence and source-normalization result for
the displayed **designed** function and static-`K` subcase. It is not a
derivation of `J`, `K`, MOND or `a0` from ITSM microphysics. Coefficient one
follows from the chosen low-`y` normalization together with universal metric
sourcing; it was not recovered blindly from topology or circulation.

## 5. Microscopic obstruction and constructive evasion

### 5.1 Stable affine heavy modes do not work

For a stable algebraic heavy variable entering the static energy affinely in
`Y`,

`F(Y)=M_P^2 Y + min_chi[U(chi)+b(chi)Y]`,

the stationary-point envelope obeys

`F''(Y)=-(b')^2/(U''+b''Y) <= 0`.

The required deep energy is convex:

`d^2[C Y^(3/2)]/dY^2=3C/(4 sqrt(Y))>0`.

Therefore the already-rejected simple radial/heavy route cannot generate this
operator through a stable affine coupling.

### 5.2 A non-affine auxiliary representation exists

For `s>0`, construct

`F(Y,s)=Y^2/(2 a0^2 s)+(a0^2/6)s^3`.

Then

`s_star=sqrt(Y)/a0`,

`d^2F/ds^2|_star=2 a0 sqrt(Y)>0`,

and

`F_eff(Y)=(2/3)Y^(3/2)/a0`.

This exactly evades the affine-heavy convexity obstruction. It was engineered
from the desired operator, so it is a hostile constructive control, not a
microscopic explanation.

Because there is no `dot(s)`, the local constraints are `p_s=0` and
`dF/ds=0`, with bracket

`{p_s,C_s}=-2 a0 sqrt(Y)`.

For every `Y>0` the pair is second class and the susceptibility contributes no
local propagating degree of freedom. At `Y=0`, however, `s_star`, its stiffness
and the constraint bracket all vanish. The strict positive-`s` chart ends and
the constraint rank changes.

This boundary is structural. If a parent is analytic near `Y=0` and its heavy
Hessian is nonsingular, the implicit function theorem gives an analytic
integer-power effective action. It cannot yield an exact `Y^(3/2)` term.
PKM1 must therefore contain a critical, singular, gapless, nonlocal or
explicitly non-analytic ingredient, or operate only on a controlled
nonzero-gradient domain.

The constructed block is also deep-regime only: `F_eff/Y` diverges at large
`Y`, so it does not provide the GR join.

## 6. External precedent and non-inheritance rule

[Blanchet and Marsat (2011)](https://arxiv.org/abs/1107.5264) provide the
metric-hosted preferred-foliation precedent, including a stationary MOND limit
and GR-like lensing structure. [Flanagan (2023)](https://arxiv.org/abs/2302.14846)
finds a consistent nonrelativistic limit and stability for certain symmetric
stationary low-acceleration backgrounds, while also finding order-one
nonstationary corrections in general.

[Blanchet and Skordis (2024)](https://arxiv.org/abs/2404.06584) give the exact
`R-2J(Y)+2K(Q)` covariant action with universally coupled matter and document
both its attractions and its open burdens: the arbitrary `J` function, a
nonpropagating scalar at quadratic order, a long-wavelength Jeans-type
Hamiltonian problem and a naive `sqrt(a0 M_P)` strong-coupling scale.

These papers establish that the route class is technically serious. They do
not prove that identifying the khronon with the ITSM condensate phase is
globally consistent, that the auxiliary block is microscopic, or that ITSM
inherits their PPN, lensing, stability or cosmology results.

## 7. Bounded route comparison

| Screened route | Result | Disposition |
|---|---|---|
| Live separate-`psi` action | Independent normalized matter residue remains uncomputed | Frozen control |
| Minimal radial/heavy M2 | No live radial source; tested extensions retain free combinations or lift the massless force | Rejected within tested classes |
| Helical two-scalar locking | Residue remains `g_sigma*kappa/sqrt(Z_psi+Z_sigma*kappa^2)` and the matter vertex breaks the locking shift unless matter transforms | Reject as residue solution |
| Minimal healthy vector direct-force control | Equal-sign universal charges repel | Reject only this simple control; no general vector-tensor no-go claimed |
| PKM1 metric host | Universal metric source; designed-`J` modified-Poisson reduction, with exact AQUAL only in the static-`K` null/local limit; local auxiliary pair healthy for `Y>0` | Advance one parent Hamiltonian test; global HOLD |

PKM1 is the only survivor among the controls actually screened. This is not an
exhaustive theorem over all possible modified-gravity or condensate parents.

## 8. Exact next calculation

The next task is one bounded A0–A6 parent test, before phenomenology:

1. Declare one covariant parent
   `S_parent=S_EH+S_cond[rho,Theta,g]+S_pol[s,rho,Theta,g]+S_m[Psi_m,g]`.
   `U_mu` must be derived once from `Theta`; no independent aether or appended
   `psi` may be silently retained.
2. Derive both `J(Y)` and `K(Q)` by controlled elimination or label either one
   as fundamental EFT data. Do not append the canonical condensate phase
   kinetic term and `K(Q)` as two descriptions of the same degree of freedom.
3. Supply a global high-acceleration join that tends to GR without inserting
   observational targets.
4. Perform the complete ADM/Dirac count for `rho`, `Theta`, `s`, lapse, shift
   and spatial metric on `Y>0`, then repeat at `Y=0`. Track every primary,
   secondary, first-class and second-class constraint and its rank.
5. Solve every retained background equation on Minkowski, FRW and a declared
   nonzero-gradient galactic patch.
6. Derive the reduced Hamiltonian, characteristic matrix, front speeds,
   Jeans band, zero-gradient join, cutoff and radiative-stability domain.
7. Compute the invariant matter-to-physical-mode source response from the full
   metric constraint. Minimal coupling removes a bare `C_m`; it does not waive
   the on-shell pole/residue and sign audit.
8. Only if A0–A6 survive, begin PPN, Shapiro delay, lensing, GW, compact-object
   and topology/winding compatibility tests.

### Kill criteria

Reject or freeze PKM1 if any of the following occurs:

- an extra ghost/Ostrogradsky mode or negative physical Hamiltonian;
- an uncontrolled constraint-rank change or strong coupling at `Y=0`;
- no domain overlapping galactic gradients below the physical cutoff;
- loss of a globally admissible timelike phase foliation in the claimed
  winding sector;
- a coefficient or `a0` justified only by the desired acceleration law;
- failure of the high-acceleration GR/PPN/GW limit;
- instability or order-one nonstationary corrections in the intended domain.

## 9. Gate firewall

This decision creates no canonical-action replacement and no parent-gate
promotion:

- MAT-001 remains `BLOCKED`;
- UVIR-003 remains `IN_PROGRESS`;
- `V` remains `NOT_COMPUTED` in the live route;
- `K_Q` remains `NOT_DERIVED` in the live route;
- `a0` and `C_chi` remain underived;
- local gravity, lensing, disks, SPARC, cosmology and publication remain
  closed behind their recorded dependencies.

PKM1 may replace the old force-host architecture only after a separate signed
architecture decision backed by the full parent calculation.

## 10. Reproducible evidence

- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/itsm_pkm1_metric_hosted_khronon_screen.py`
- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/itsm_pkm1_a2_a6_obstruction_audit.py`
- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/itsm_pkm1_auxiliary_constraint_rank.py`
- generated JSON, Markdown reports and SHA-256 manifests under the route's
  `outputs/` directory.

The first two reports are scoped existence/obstruction audits. The third is a
local Dirac sub-block. None is the full parent Hamiltonian or a physics pass.
