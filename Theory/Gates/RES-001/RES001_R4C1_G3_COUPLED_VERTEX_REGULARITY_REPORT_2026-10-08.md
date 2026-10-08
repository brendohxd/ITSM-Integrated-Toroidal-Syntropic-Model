# R4C1-G3V: coupled transverse constraints and cubic-vertex regularity

Date: 8 October 2026. Owning scope: conditional R4C1-v1 / G3 / Master Test 1.
Parent-authored local derivation. Review **DEFERRED**; claim **Conditional**;
`physics_pass=false`, `Rule9_cleared=false`, `gate_effect=NONE`.

## Result and scientific disposition

The finite-density metric-shift constraint was restored and solved in the
pure transverse spin-1 sector. The unchanged force operator leaves a
nonzero even cubic-amplitude functional on this constrained direction.
Its left and right third derivatives disagree. Consequently the full
ordinary trilinear Taylor vertex required by the proposed ordinary
cubic/quartic exchange-diagram calculation does not exist on this
homogeneous G3 background.

**379/379 local checks pass**; nonmutating replay reproduces all four JSON
artifacts byte-for-byte. The 216 registered chart events all have a
nonzero transverse cusp. These are verification of a bounded obstruction,
not a physical stability or cutoff pass.

The bounded G3V prerequisite test is complete. Full finite-density
scattering and physical EFT-cutoff work remain **HOLD_SUBSTANTIVE**.
Whether G3I's fixed-metric amplitude survives the interacting background
is **NOT_DETERMINED**. No full finite-density amplitude is supplied.

The nonanalyticity of the unchanged operator was already identified in
the older UVIR Track-A work. The new result is its explicit pullback after
the G3 transverse metric/dust constraints, the interacting quadratic
coefficients, and its evaluation on the pinned G3 trajectories.
This does not establish a no-go for classical evolution, a nonanalytic
perturbative prescription, quantum completion, another background, or
all candidate actions.

## Frozen scope, geometry and auxiliary constraints

The contract was frozen after analytic planning and before executable
covariance/constraint checks and numerical sampling. No action parameter,
grid, tolerance, old receipt or failed assertion was changed.

Use signature (-+++), flat FRW, spatial metric gamma_ij=a^2 delta_ij,
a physical transverse shift B_y(t,z), and physical frame tilt w_y(t,z).
For amplitude epsilon and lapse N, the exact chart is

```text
g_00 = -N^2 + epsilon^2 B^2
g_0y = epsilon a B
U^0 = sqrt(1+epsilon^2 w^2)/N
U^y = epsilon [w-B sqrt(1+epsilon^2 w^2)/N]/a
h^mu nu = g^mu nu + U^mu U^nu .
```

The exact inverse, unit norm, projector orthogonality and idempotence were
checked. The frame multiplier is eliminated by the exact unit
parametrization. Homogeneous canonical scalar and irrotational-dust
actions have no transverse shift source, as verified directly from
their inverse-metric contractions.

Scalar and tensor linear perturbations vanish in this pure spin-1
direction by the isotropic decomposition. At first order delta_tau and
delta_psi vanish. With C=exp(beta psi) and tau_dot=C, the dust multiplier
constraint is C^4(1-1/N^2)=0, whose linear coefficient is
2 C^4 delta_N; hence delta_N=0. This retains the dust constraint rather
than freezing a dynamical metric without checking it.

The transverse shift has no time derivative and is eliminated at
nonzero spatial mode. The scalar auxiliary rank witness is inherited
from S1 in its declared matrix normalization:

```text
det A_scalar = C^8 M_U^2 b k^2 c_123
c_123(G3) = 1/24 .
```

Its positive numerical values certify nonsingularity in the sampled
nonzero-mode chart, not a physical kinetic or stability criterion.
No new complete scalar J2/J3 solution or homogeneous nonlinear
auxiliary reduction is claimed.

## Full interacting spin-1 quadratic block

All four frame invariants were contracted with the metric connection
through second order, including a_dot=a H. Before integration by parts,
the proper frame density is

```text
L_frame,2 = (M_U^2/2) [
 (c1+c4) w_dot^2 - c1 w_z^2/a^2
 +(c1+c3) w_z B_z/a^2 -(c1+c3) B_z^2/(2a^2)
 +2(c4-3c2-c3) H w w_dot
 +(c4-2c1-9c2-3c3) H^2 w^2 ] .
```

The Einstein ADM bulk term, with the inherited fixed-boundary/GHY
convention, contributes M_P^2 B_z^2/(4a^2). The temporal-force and
current-alignment terms contribute
(K_Q psi_dot^2-zeta J0^2)w^2/2, where J0=v u_dot-u v_dot.
The regulator has zero background and first-order variations in this
sector. Other homogeneous scalar/dust blocks give no additional
transverse quadratic source.

The stationary solution and reduced principal coefficients are

```text
B_z = -M_U^2(c1+c3) w_z/[M_P^2-M_U^2(c1+c3)]

K_vector = M_U^2(c1+c4)
G_vector = M_U^2 c1
         + M_U^4(c1+c3)^2/[2(M_P^2-M_U^2(c1+c3))] .
```

Here M_U^4 means (M_U^2)^2. The archived G3 family uses M_P=1 reference
units, M_U^2=2 eta/3, c1=1/5, c2=-7/48, c3=-1/80, c4=1/20,
K_Q=3 eta, zeta=eta/13, b=5 eta/11 and A=2 eta^(3/2)/7.
Thus

```text
f^2 = K_vector = eta/6
M_tensor^2 = 1-eta/8
c_vector^2 = 4/5 + 3 eta/[8(8-eta)] .
```

Restoring units gives f^2=eta M_P^2/6. The flat, zero-background
quadratic result agrees with the metric-shift reduced vacuum control.
The interacting background mass is not that vacuum result.

Including the background flow when differentiating coefficients gives

```text
w_ddot + 3 H w_dot + [c_vector^2 k^2/a^2 + m_w^2] w = 0
m_w^2 = 2(H_dot+H^2)-18 psi_dot^2+6 J0^2/13

X = a^(3/2) f w
X_ddot + [c_vector^2 k^2/a^2 + m_X^2] X = 0
m_X^2 = H_dot/2-H^2/4-18 psi_dot^2+6 J0^2/13 .
```

The exported fields `vector_mass_w` and `canonical_X_mass` are these
mass-squared coefficients, not their square roots. The on-shell flow is

```text
M_cosm^2 = 1-eta/12
H_dot = -(u_dot^2+v_dot^2+r_dot^2+K_Q psi_dot^2+rho_m)/(2 M_cosm^2)
psi_ddot = -3 H psi_dot-beta rho_m/K_Q .
```

Positive sampled kinetic and gradient coefficients do not establish full
stability. The sampled m_X^2 values are negative, while the declared
local frozen frequencies squared at k=20,40,80 are positive.
Neither sign alone is a full time-dependent or all-sector stability result.

## Exact force cusp and stationary elimination

For homogeneous psi, the exact covariant projector gives

```text
Y = epsilon^2 psi_dot^2 w^2/N^2
sqrt(-g) L_force,nonanalytic = -a^3 A |epsilon psi_dot w|^3/N^2 .
```

The shift cancels from Y. For w=W cos(kz), the spatially averaged
leading force term is

```text
-a^3 A |psi_dot|^3 |epsilon W|^3 * 4/(3 pi) .
```

The leading cubic coefficient is independent of the first-order lapse
and shift, and the first-order dust/regulator auxiliaries vanish in
this direction. Its lapse prefactor cannot change this leading order.

For regular local auxiliary elimination, an order-epsilon^2 correction
to an auxiliary enters the cubic action multiplied by the first-order
constraint equation. That equation vanishes on the linear solution.
The actual transverse-shift contraction
B_z,2 (partial L_2/partial B_z)|B_z,1=0 was verified explicitly.
The same stationary argument requires the declared local nonzero-mode
rank and an order-epsilon^2 continuation; it is not a construction of
the full nonlinear auxiliary solution or its zero-mode sector.
Under this stated scope, regular elimination cannot cancel this
leading nonanalytic coefficient with analytic cubic terms.

In local physical canonical V=f w and comoving X=a^(3/2) f w, define

```text
C_local = A |psi_dot|^3/f^3
C_X = C_local/a^(3/2)
C_local(G3, M_P=1) = (12 sqrt(6)/7) |psi_dot|^3 .
```

The periodic-average coefficient for X additionally includes 4/(3 pi).
For F(epsilon)=-C |epsilon|^3 and C>0,

```text
F'''(0+) = -6C
F'''(0-) = +6C .
```

No common third derivative exists. A symmetric odd finite difference
vanishes by evenness and would be a false regularity test. In contrast
with G3I's analytic frame-only interaction, this particular cusp
coefficient does not diverge merely from canonical normalization:
A/f^3 is eta-independent in reference units, and it decreases as
|psi_dot|^3 when the trajectory's psi_dot decreases.

A=0 or psi_dot=0 removes this transverse term. The latter does not
certify the full action is C3: at psi_dot=0, a retained force-gradient
direction delta_psi=epsilon Pi cos(kz), U equal to the ADM normal,
has Y=epsilon^2 (partial_z delta_psi/epsilon)^2/a^2, independent of
lapse/shift. Its averaged leading term is
-A |epsilon k Pi|^3 4/(3 pi). This is the separate S1 force-gradient
direction, not an assertion that the full scalar constraint solution
has been newly assembled.

The action remains C2 in these local projected-gradient directions.
The obstruction concerns ordinary third-order Taylor vertices; it
does not negate the existing classical background/linear evolution.

## Direct regulator term and its limit

The exact connection/projector calculation gives

```text
Delta_0 = Delta_1 = 0
Delta_2 = psi_dot w w_dot+(psi_ddot+2 H psi_dot) w^2
z_2 = -Delta_2
L_regulator,4,direct = -b Delta_2^2/2 .
```

This is a direct quartic term from eliminating the regulator auxiliary
in the transverse chart. It is not the complete quartic constrained
action, the scalar/metric J2 source, or the full quartic Schur complement.

## Numerical evidence and independent controls

Only pinned archived trajectories were used. No new background
integration or tolerance refinement was performed. The grid is
eta=(1,1/4,1/16,1/64,1/256,1/1024), both archived methods,
t=(0,.5,1,2,3,4) and k=(20,40,80): 216 chart events.

All 216 have a nonzero cusp. Across the grid:

- Minimum K_vector: 1.6276041667e-4.
- Minimum inherited scalar auxiliary determinant: 4.8165369515e-6.
- Minimum transverse-shift Fourier Hessian: 7.4929657274.
- C_local range: 1.1346638317e-14 to 3.3593002187e-2.

These are finite samples in reference units, not observed galaxy scales,
uniform continuum bounds, or a physical EFT window.

| eta | c_vector^2 | max C_local | min local frozen frequency squared |
| --- | ---: | ---: | ---: |
| 1 | 0.853571429 | 3.35930022e-2 | 14.5967333 |
| 1/4 | 0.812096774 | 5.24890659e-4 | 44.4140574 |
| 1/16 | 0.802952756 | 8.20141655e-6 | 71.8035164 |
| 1/64 | 0.800733855 | 1.28147134e-7 | 85.6709282 |
| 1/256 | 0.800183195 | 2.00229896e-9 | 90.2264038 |
| 1/1024 | 0.800045782 | 3.12859213e-11 | 91.4611307 |

An independent numerical evaluator used the unexpanded metric,
connection and projector at the contract's diagnostic jets. These jets
are algebraic controls, not an on-shell background trajectory.
For h=(1e-3,5e-4,2.5e-4), both signs and multiples h,2h,3h were retained.
At the finest h:

- Frame quadratic coefficient absolute error: 6.8175477199e-12.
- Delta_2 coefficient absolute error: 4.0209344535e-11.
- Right/left force third differences divided by C:
  -5.9999995012 and +5.9999995012.
- Error from the exact normalized third differences: 4.9878645214e-7.
- Projector/Y errors remained below 1e-12 at every recorded h.

The third-difference error is not monotonically decreasing at this
floating-point scale; it remains below the frozen 1e-5 finest-step
criterion. The independent frame check satisfies the declared
decreasing-error-or-small-error criterion. All errors and signs remain
in the artifacts.

The original coarse G3 derivative assertion remains failed at 112/113.
It was checked and preserved, not relabelled. Its later refinement and
the inherited Friedmann/dust/charge witnesses retain their original
scopes and holds. There were no new implementation or assertion
failures in this G3V run.

## Reproducibility and integrity

Script:
[local calculation](../../../Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity.py),
SHA-256 `875aefe980e4b78a1173a69bbd129d81a7dc4b2b0872c0a16774bc7c177bfe8b`.

Contract:
[frozen scope](RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_CONTRACT_2026-10-08.md),
SHA-256 `53940518eeff7ca46fb5a9373db6e4637360eeedaeffcba6044af5cc580ac3ac`.

Output directory:
`Analysis/MasterTests/outputs/r4c1_g3v_attempt_01`.

| Artifact | SHA-256 |
| --- | --- |
| summary.json | 07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae |
| formulas.json | 1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358 |
| samples.json | 93288f37a919d22f59a397ab8ffb732f8386d23ee561469be2bebea489af3d03 |
| independent.json | cedcd8344d45933029d542c761324c3775b16864e8d123e7f6b5a8fa52fe9981 |

All 62 unique direct/transitive scientific source pins were verified,
including the G3I/G3DF chain, scalar-constraint witness, action freeze
and older Track-A force report. The script and artifact sidecars match.
Full pin paths/hashes are in the receipt.

Runtime: Python 3.13.9, NumPy 2.4.6, SymPy 1.14.0, in the existing
itsm_env interpreter. Commands from the repository root:

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity.py
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity.py --replay
```

Both exited 0. Replay checks equality of all four generated payloads
without writing them. The first command refuses an existing output
directory; use replay or a separately numbered attempt.

Ignored first-run log:
`.local/itsm-context/output-530fff8ebf1a49179e2a8d40d3e1ea7b.txt`,
SHA-256 `ffe534cd1f73005add6f4d5066bc9a8ea16ff18c82d5df85c51f159e40bf2a37`.
Ignored replay log:
`.local/itsm-context/output-5a0310a756dd44afb68a9069d21671d1.txt`,
SHA-256 `d8c962a09844a32e24ea750f2ab59d2cff651b49ecd44f8c13e961263650b504`.
Ignored integrity/sampling log:
`.local/itsm-context/output-c9ecb6010ba74a128dd62bbdbbe31078.txt`,
SHA-256 `01747eb1eda0748510d2f35f3fe884de3a56dd47f69fadd09eba1d7a2e0aaee8`.

## Remaining work and inherited holds

An explicit prescription for the nonanalytic interaction is
**NOT_SUPPLIED**. Ordinary Taylor diagrams cannot silently drop the
force term, smooth its origin or replace its even cubic functional by
a multilinear coupling. The older Track-A route instead expands at a
nonzero projected-gradient background. Any use of that route must
first establish its on-shell background and domain and distinguish it
from homogeneous G3; changing the background is not a continuation
of the same G3 amplitude without additional proof.

Full J2/J3 assembly, complete quartic Schur reduction, finite-density
physical eigenstate amplitudes, infrared exchange treatment,
higher-derivative/loop matching and a physical validity window remain
open. G3I's p_probe retains its fixed-metric conditional scope only.

Register R9-MT1-G3V inherits G3I/G3DF/G3D/G3F/G3A/G3E/G3Z/G3S/G3,
G2/G1/B1/S1/S2/S3/variation, applicable PD1 and Track-A review debt,
and all transitive parent restrictions. Execution PROCEED_PROVISIONALLY;
review DEFERRED. Pending review alone does not block this research.

Canonical Tests 1-3 remain HOLD_SUBSTANTIVE. MAT-001=BLOCKED;
UVIR-003=IN_PROGRESS; K_Q=NOT_DERIVED; V=NOT_COMPUTED;
Stage4A=CLOSED; TOP-X4 unchanged. The numerical family parameter K_Q
above is an input, not a derivation of the outstanding canonical K_Q.
No ITSM SPARC prediction or likelihood is produced.

Existing dirty work and earlier scientific artifacts are preserved.
No manuscript/PDF edit, parameter/action change, memory mutation,
provider dispatch, commit, push, canonical promotion or publication.