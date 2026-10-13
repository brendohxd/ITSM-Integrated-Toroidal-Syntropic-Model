# MAT-001 RM1: radial matter-mass portal screen

Date: 13 October 2026. Candidate/result ID: `MAT001-RM1-v1`.
Status: **Conditional, separate scalar/probe matching control**.
Authority: operator instruction to proceed with the bounded mechanism screen
following `MAT001_PHYSICAL_MATCHING_ROUTE_DECISION_2026-10-13.md`.
This contract is frozen before its executable. It does not replace R4C1 or
adopt a new canonical parent.

## Purpose

Test whether deriving a matter source from a condensate-dependent particle mass
gives a nonzero soft coupling to the condensate's gapless phase mode, without
inserting an independent direct phase-source coefficient. This is a new
source/pole calculation for the declared control, not a replay of UVIR-001's
already negative spatial cubic-law test or the existing M2 toy mixing tests.

## Declared action, domain and assumptions

Use signature `(-+++)`, `c=hbar=1`. The covariant scalar action is

```text
S_scalar = integral sqrt(-g) [
    -1/2 (grad rho)^2 -1/2 rho^2 (grad Theta)^2 - V(rho)]
V(rho) = m^2 rho^2/2 + lambda4 rho^4/8
         + lambda6 rho^6/(24 Lambda^2)
Phi = rho exp(i Theta)/sqrt(2).
S_probe = -sum_a integral y_a rho(x_a) ds_g.
```

For the calculation choose the external flat metric on `I x T3`, spatial
period L and zero spatial winding. The homogeneous background is scalar-only,
`rho=rho0>0`, `Theta=mu t`, with `mu>0`. Specify positive conserved charge
density `n_Q` independently of observational force targets and solve
`V'(rho0)=mu^2 rho0`, `n_Q=mu rho0^2`. No homogeneous probe background is
included. Use `m^2>=0`, `lambda4>=0`, `lambda6>0`, `Lambda>0`, `y_a>0` and
strict positive amplitude curvature `M_rho^2=V''(rho0)-mu^2`.

The chosen mass law `m_a(rho)=y_a rho` is an explicit portal assumption.
Its source is derived by varying that action. It is U(1) invariant on the
nonzero-amplitude branch, but it is not uniquely required by that symmetry,
not a microscopic derivation of baryon mass, and not a Standard-Model or
ultraviolet completion. The sextic scalar term also belongs to an EFT.
No Yukawa loop, anomaly, reservoir or matter-number dynamics is claimed.

Prescribed nonrelativistic probes provide an infinitesimal density source
`rho_b=sum_a n_a y_a rho0`, keeping particle number densities fixed when
varying rho. Prescribed worldlines and fixed metric are probe-limit choices;
full gravitational/Euler consistency is outside this screen. Linearize in
the source about its absence. For nonzero Fourier modes the contrast has
zero spatial mean. Treat the uniform source separately at fixed total charge.

Mass dimensions: `[rho]=[rho0]=[mu]=[m]=[Lambda]=1`, `[Theta]=[y_a]=0`,
`[lambda4]=[lambda6]=0`, `[n_Q]=3`, `[rho_b]=4`, `[M_rho^2]=2`, `[L]=-1`.
Fixed endpoint scalar variations or compactly supported time variations and
periodic spatial variations specify the local quadratic calculation.

## Required calculation and checks

1. Expand the declared scalar action to quadratic order around the stationary
   background, using `h=rho-rho0` and `p=rho0 (Theta-mu t)` as fields. Derive
   the amplitude-phase mixing coefficient and background equations directly.
2. Vary the probe mass action and derive its signed radial and phase source
   coefficients. Verify that varying the independent positive y does not
   insert a new fractional mass-response coefficient.
3. Derive the full two-field frequency kernel for nonzero `k=2 pi |n|/L`,
   `n!=0`, with Fourier convention `exp(-i omega t+i k.x)`. Retain the term
   linear in frequency. Find both dispersion branches and the radial-to-source
   and fractional-mass-to-source responses exactly.
4. Compute the simple-pole weights in `z=omega^2`. Distinguish signed vertex,
   vertex square, and static response. Check source covariance under a
   nonorthogonal field change and verify pole normalization using the
   frequency derivative of the mixed kernel, not Euclidean eigenvectors.
5. Determine the nonzero-mode static limit and the formal soft-momentum
   behavior of the gapless pole weight/vertex. The soft limit is an analytic
   diagnostic (or a sequence of larger tori), not an inverse of the fixed
   torus zero mode. Derive the fixed-charge uniform susceptibility separately.
6. Show the scalar quadratic Hamiltonian's sign/domain. Test at least three
   rational parameter cases for roots, residues and response reconstruction
   with high precision. Numerical cases are algebra diagnostics, not matched
   physical parameter sets. Rejection tests must catch the lost mixing term,
   direct phase source, magnitude-only signed vertex, wrong static kernel,
   wrong charge ensemble and promotion of an assumed source to canonical V.

## Decision rule and exclusions

For this portal to provide the desired gapless static matter coupling, the
soft phase-mode vertex must be finite and nonzero, and its static response
must actually contain the corresponding long-range pole. If either condition
fails, reject **this candidate as the missing gapless static-source mechanism**.
Do not conclude that all mass portals, finite-range radial forces, other
parents, or ITSM itself are excluded.

A selected amplitude and a parameterized radial source do not supply a
numerical canonical V: the scalar parameters and independent charge/state
still need physical determination. No full metric/frame constraints,
characteristics, nonlinear spatial matching, physical cutoff, lensing or
galactic prediction is performed. Retain the UVIR-001 negative spatial result.
The `M_rho^2=0`, `rho0=0`, `mu=0` boundaries must not be admitted by dividing
the interior formulas; report their different rank/domain when used as controls.

Review status DEFERRED, not cleared. Inherit the route decision and its MAT
R4/R5/M2/M4 dependencies, and UVIR-001 for the scalar action/domain only.
`research_execution=PROCEED_PROVISIONALLY` for this conditional screen;
numerical canonical matching remains `HOLD_SUBSTANTIVE`.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, `Stage4A=CLOSED`, canonical Tests 1-3 `HOLD_SUBSTANTIVE`.

Input source versions:

- Route decision: SHA-256
  `00e784bc797600fd4e8c31192026f5c2c7977b66d39f4b5faeddce71ef46b4ac`.
- UVIR-001 gate report: SHA-256
  `850d4e6616a136088936bbdbbb809f0443b508117cbe0140ebb05eca79aaf630`;
  scalar action/background and mode sections used, not canonical acceptance.
- R4 signed-source contract: SHA-256
  `63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386`.

Primary methodological reference (not the origin of the chosen mass portal):
[Joyce, Nicolis, Podo and Santoni, JHEP 09 (2022) 066,
arXiv:2204.03678](https://arxiv.org/abs/2204.03678). Their work supplies
finite-density EFT matching context; this screen is its own tree-level
action variation and computes no one-loop matching.
