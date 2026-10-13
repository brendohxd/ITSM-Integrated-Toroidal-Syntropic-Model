# MAT-001 RM1: a radial mass source does not supply a soft static phase coupling

13 October 2026. Result ID `MAT001-RM1-v1`. Claim **Conditional / scoped negative**.
Contract: [RM1 frozen action and decision rule](MAT001_RM1_RADIAL_MASS_SCREEN_CONTRACT_2026-10-13.md),
SHA `b27acb9fcd40e2591f96a10d7ffa8911d940bb784d0124b9785ad83e1ad0e375`.
Owner: MAT-001 matching mechanism screen, following the
[physical matching route decision](MAT001_PHYSICAL_MATCHING_ROUTE_DECISION_2026-10-13.md).

## Result

The declared mass portal `m_a(rho)=y_a rho` gives a genuine radial source whose
fractional coupling is `-1/rho0`. In the exact two-field amplitude/phase
quadratic control, however, the gapless phase-mode coupling tends to zero at
soft momentum. Its static response contains no massless phase pole.
The route therefore fails the frozen requirement of a finite nonzero soft
static matter coupling to that gapless mode.

Decision: `REJECT_RM1_AS_NONZERO_SOFT_GAPLESS_STATIC_SOURCE`.
This does not reject finite-range radial forces, every mass portal, a different
parent, or ITSM. The selected portal is an assumption, not a derivation of
baryon mass. All results are at tree level in a flat scalar/probe control,
not the coupled R4C1 gravitational spectrum or a canonical matter match.

## 1. What was actually varied

The [contract](MAT001_RM1_RADIAL_MASS_SCREEN_CONTRACT_2026-10-13.md) declares

```text
L_scalar = -1/2 (grad rho)^2 -1/2 rho^2 (grad Theta)^2 - V(rho)
V = m^2 rho^2/2 + lambda4 rho^4/8 + lambda6 rho^6/(24 Lambda^2)
S_probe = -sum_a integral y_a rho ds_g.
```

The external spacetime is flat `I x T3`, with zero spatial winding. There is
no homogeneous probe density. Background charge is specified independently,
`n_Q=mu rho0^2>0`, with `V'(rho0)=mu^2 rho0`. In the strict interior,
`rho0,mu,Lambda>0`, `m^2,lambda4>=0`, `lambda6>0` and

```text
M2 := M_rho^2 = V''(rho0)-mu^2
             = lambda4 rho0^2 + lambda6 rho0^4/Lambda^2 > 0.
```

The particle-mass law is U(1) invariant on this amplitude branch. No unique
symmetry derivation of it, Standard-Model mass generation, Yukawa matching,
loop computation, reservoir action, metric variation or probe Euler dynamics
is claimed. It is a concrete local source assumption whose variation is tested.

Set `h=rho-rho0`, `p=rho0 (Theta-mu t)`. The expansion before imposing field
equations gives a linear endpoint derivative and the quadratic action

```text
L2 = (h_dot^2-|grad h|^2-M2 h^2)/2
     +(p_dot^2-|grad p|^2)/2 + 2 mu h p_dot
     -rho_b h/rho0.
```

The last term follows at fixed probe number from the declared mass law, using
`rho_b=sum_a n_a y_a rho0`. Its fractional coefficient is independent of
the positive `y_a`. There is no direct `rho_b p` source. The calculated
mixing `2 mu h p_dot` is fixed by the scalar kinetic action and background.

## 2. Exact mixed poles and matter response

For a nonzero torus mode `k=2 pi |n|/L`, use `exp(-i omega t+i k.x)` and
`z=omega^2`, `q=k^2`, `H=M2+4 mu^2`. The quadratic action kernel is

```text
D = [[z-q-M2, -2 i mu omega], [2 i mu omega, z-q]]
Delta = det D = (z-q-M2)(z-q)-4 mu^2 z
z_- = q+H/2 -sqrt(H^2+16 mu^2 q)/2
z_+ = q+H/2 +sqrt(H^2+16 mu^2 q)/2.
```

Both squared frequencies are strictly positive for `q>0` in this scalar
interior. Their product is `q(q+M2)>0`, their sum is positive and their
discriminant is positive. The scalar quadratic Hamiltonian is

```text
H2 = p_h^2/2 +(p_phase-2 mu h)^2/2
     +(|grad h|^2+|grad p|^2+M2 h^2)/2,
p_h=h_dot; p_phase=p_dot+2 mu h.
```

This establishes the sign/domain of this limited scalar control only. It
provides no gravity/frame/constraint/quantum or physical-frequency-band verdict.

The fractional probe-mass response is

```text
R(z,q) := delta ln(m_a)/rho_b = (z-q)/(rho0^2 Delta)
       = W_-/(z-z_-) + W_+/(z-z_+),
W_- = (q-z_-)/(rho0^2 (z_+-z_-))
W_+ = (z_+-q)/(rho0^2 (z_+-z_-)).
```

For `q>0`, both weights are positive and sum to `1/rho0^2`. They are squared
source vertices in the `z=omega^2` pole convention, not signed vertices.
With the radial-component-positive eigenmode orientation and the declared
negative source, `g_j=-sqrt(W_j)`. No conclusion about a universal gravitational
force sign is extracted from these scalar exchange weights.

The kernel contains terms linear in frequency. An ordinary Euclidean mode
norm would give the wrong residue. At a positive-frequency simple pole,
take `u=(1,i d)`, `d=(q+M2-z_j)/(2 mu sqrt(z_j))`. Its pole normalization is

```text
N_j = u^dagger (partial D/partial z) u
    = 1+d^2+2 mu d/sqrt(z_j)
    = (partial Delta/partial z)/(z_j-q),
W_j = 1/(rho0^2 N_j).
```

The identity is checked exactly on shell by polynomial remainder, and in
nine high-precision numerical cases. These formulas are for `mu>0,q>0`,
simple positive-frequency poles. The zero mode is treated separately below.

## 3. Soft static limit and the contact term

The exact soft behavior is

```text
c_s^2 = M2/H
z_- = c_s^2 k^2 + O(k^4)
W_- = [4 mu^2/(rho0^2 H^2)] k^2 + O(k^4)
g_- = -[2 mu/(rho0 H)] |k| + O(|k|^3).
```

Thus the nonzero-momentum phase pole exists, but its matter vertex vanishes
in the soft limit. The nonzero-mode static response is exactly

```text
R(0,k^2) = -1/[rho0^2 (k^2+M2)].
```

It has the radial finite-range denominator, not a static gapless phase pole.
In a fixed finite torus the allowed nonzero modes are discrete; the soft
limit above is analytic or a sequence of increasing tori. No inverse of the
fixed torus zero mode is used. Very small positive M2 can produce a long
radial range; this result does not rule out such a finite-range model, select
its parameters, or give it the missing nonlinear spatial law.

At energies/momenta small relative to the strict radial-curvature scale, the
leading heavy-amplitude derivative expansion yields

```text
Z_phase = 1+4 mu^2/M2
L_eff = Z_phase p_dot^2/2 -|grad p|^2/2
        -2 mu rho_b p_dot/(rho0 M2)
        +rho_b^2/(2 rho0^2 M2) + higher derivatives.
```

The phase source is derivative, and a time-independent prescribed density
does not supply its direct static source. The contact term is essential to
the static response. The canonical phase is `sqrt(Z_phase) p`; its
derivative-source vertex squared on shell agrees with the soft pole weight.
This expansion is not asserted outside its low-energy domain.

## 4. Fixed-charge mean mode

The unexpanded U(1) current is `n_Q=rho^2 Theta_dot`, and its linearization is

```text
delta n_Q = rho0 (p_dot+2 mu h) = rho0 p_phase.
```

For the uniform mode at fixed total charge, impose `p_phase=0` before solving.
The radial equation has curvature `H=M2+4 mu^2`; its uniform static response is

```text
R_uniform,fixed_charge = -1/[rho0^2 (M2+4 mu^2)].
```

This differs from the soft limit of nonzero spatial modes, whose local charge
can redistribute while their mean charge vanishes. The fixed-chemical-potential
uniform susceptibility would instead have M2 in its denominator. They answer
different physical questions and must not be exchanged. At `M2=0` the strict
curvature premise fails; at `rho0=0` the polar/source chart fails. Neither is
an admitted cure obtained by dividing an interior formula at its boundary.

## 5. Verification and new information

The [executable](../../../Analysis/MAT/MAT-001/RM1_RADIAL_MASS/mat001_rm1_radial_mass_screen.py)
SHA is `ddd844f263a09642d3b84a27463f3195e088c75cd794fded8022cc0f1d47a857`.
The [attempt-01 receipt](../../../Analysis/MAT/MAT-001/RM1_RADIAL_MASS/outputs/rm1_attempt_01/summary.json)
SHA is `10ca6ede9976acad66d2119295021f8f260895dc08ceffcdaac31656eb11969d`.

Actual result: **106/106 local checks**, zero failed or unknown; three rational
background parameter sets, each at three nonzero integer torus wave numbers.
The 80-decimal numerical diagnostics compare exact dispersion roots with an
independently constructed first-order Hamiltonian matrix, pole weights with
the frequency-derivative norm, and the spectral sum with the direct response.
Maximum absolute discrepancies across the nine cases:

| Diagnostic | Measured maximum |
|---|---:|
| Hamiltonian frequency comparison | `9.27713419e-80` |
| Pole-weight normalization | `4.216879177e-81` |
| Direct/spectral response reconstruction | `4.216879177e-81` |

These are arithmetic comparisons for assumed scalar/probe parameters. They
are not physical parameter matches or independent scientific review. All eight
receipt source pins were rehashed separately, with no mismatches. A fresh run
into ignored `.local/itsm-context/rm1_replay_2026_10_13/` reproduced the receipt
and sidecar byte-for-byte, leaving both attempt-01 files' sizes and timestamps
unchanged. Original attempt-01 receipt: 20365 bytes.

Expression-level negative controls detect a dropped amplitude-phase mixing
term, an added direct phase source, a lost radial propagator numerator, wrong
charge ensemble, untransported source, substituted bare soft vertex and
reversed anchored source. Numerical controls reject Euclidean normalization;
a separate metadata mutation rejects `physics_pass=true`.

Additional exact pole-norm/current QA output remains private:
`.local/itsm-context/output-464527b2fa7446f8937db122a07d999c.txt`, SHA
`b5014f1e4381b3ca9d8696e6890dc8e6fd084812e48c831bca15d55a803ccad9`.
Its pole-norm identity is independently reproducible by substituting the
displayed d into N and dividing the numerator of
`N-Delta_z/(z-q)` by the polynomial Delta: the remainder is exactly zero.

Reproduce using a **new** output directory; existing attempts are protected:

```powershell
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MAT/MAT-001/RM1_RADIAL_MASS/mat001_rm1_radial_mass_screen.py --out .local/itsm-context/rm1_new_replay
```

The earlier UVIR-001 spatial-law rejection and M2 minimal-mixing rejections
remain prior results. This calculation adds the source obtained from the
declared radial mass law, exact mixed source poles, signed orientation,
contact term, frequency-derivative normalization and fixed-charge mean-mode
response. It does not count those old rejections as newly performed tests.

The primary [Joyce et al. matching paper](https://arxiv.org/abs/2204.03678)
provides context for integrating out finite-density amplitude modes and
matching EFT parameters to specified parent parameters. It is not evidence
for this chosen portal or the numerical ITSM coupling. Only that narrow
methodological context was checked; its one-loop work was not reproduced.

## 6. Implication for the missing ITSM coupling

This control connects a matter mass to the amplitude and expresses its radial
source in terms of the same field. It still leaves the background charge and
potential scales as independent physical inputs, and it fails the desired
gapless static source. Assigning the bare amplitude vertex `1/rho0` to the
phase would discard the exact mixed-mode projection.

A succeeding proposal must have an admissible soft force mode with a nonzero
static source overlap and independently identifying normalization/coupling
information. A U(1)-preserving amplitude-only source in this canonical
condensate does not provide it. The separate force field of the recovery
architecture therefore still needs its own explicit microscopic bridge and
matter-source matching. Any alternative phase symmetry breaking must declare
its operator, charge/current consequences and coefficient origin; adding a
free direct phase source would merely change the input problem.

No canonical numerical V, K_Q, nonlinear force coefficient, healthy full GR
limit, physical cutoff, Stage-3 prediction or MAT/UVIR gate closure follows.
Next permitted research: use this scoped negative result to screen a distinctly
specified source mechanism; maintain the separate unchanged-action R4C1 domain
investigation. No automatic parent adoption or TOP-X4 pivot is made.

## 7. Governance and review dependencies

Research execution `PROCEED_PROVISIONALLY` for the scoped negative and further
diagnostics; review `DEFERRED`; `Rule9_cleared=false`. Inherit the route
decision, MAT R4/R5/M2/M4 and UVIR-001 for the premises actually used. The
R4C1 fixed-charge report is background status only, not an equation input.
The negative result cannot be reused as a positive source match.

```text
numerical_canonical_matching=HOLD_SUBSTANTIVE
canonical_Tests_1_3=HOLD_SUBSTANTIVE
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
K_Q=NOT_DERIVED
V=NOT_COMPUTED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
review_status=DEFERRED
Rule9_cleared=false
```

The ITSM memory workflow supplied authority/continuity guidance; live pinned
source documents and the new local calculation supply the scientific evidence.
No memory mutation, model dispatch, manuscript/publication change, commit or
push is included. New scientific artifacts and an append-only living review
entry are the intended write scope; optimizer logs and replay remain private.
