# R4C1-G3T: tilted homogeneous background and regulator-clock report

Date: 8 October 2026. Owner: conditional R4C1-v1 / G3 / Master Test 1.
Parent-authored local derivation. Claim Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Outcome and exact boundary

**268/268 local checks pass.** All four result artifacts replay
byte-for-byte. The unchanged action admits 24 constraint-compatible
initial states in a tilted, axisymmetric homogeneous reduction. Eight
short reduced evolutions remain on the smooth Y>0 patch with positive
dust density and conserved energy/charge within the frozen bounds.

This supplies a local homogeneous candidate background for further
nonzero-projected-gradient work. It does not replace G3's isotropic
background or remove G3V's zero-gradient Taylor-vertex obstruction.

The regulator's z velocity mixes with the force-field velocity when the
frame is tilted. The full dust-clock velocity Hessian has six positive
and two negative eigenvalues at every registered initial state.
One negative direction already belongs to the gravitational volume
block. The regulator/force pair contributes one positive and one
negative direction in this clock.

**That is not a physical ghost theorem.** An explicitly healthy
preferred-frame scalar control produces the same higher-time-derivative
feature when expressed in a tilted clock. The new result requires a
preferred Cauchy-domain and finite-k physical-spectrum calculation;
it does not authorize discarding z or calling the tilted background healthy.
Full scattering, physical cutoff, healthy GR and canonical Tests 1-3 remain
HOLD_SUBSTANTIVE.

The on-shell statements below concern the reduced homogeneous equations,
their lapse/dust constraints and short local IVP. No complete off-ansatz
four-dimensional metric/frame variation or finite-k constraint audit
is claimed by this minisuperspace calculation.

## Unchanged action, chart and reduction

Use R4C1-v1 with its original independent unit frame, dimensionless psi,
conformal irrotational dust, reservoir and first-order regulator.
All six archived G3 parameter sets are inputs. In particular their K_Q
values are not a derivation of the outstanding canonical K_Q.

The metric has equal transverse scale factors:

```text
a_parallel = exp(alpha+2 sigma)
a_perp = exp(alpha-sigma)
V = exp(3 alpha)
H_parallel = alpha_dot+2 sigma_dot
H_perp = alpha_dot-sigma_dot
gamma = sqrt(1+w^2)

g00 = -N^2+B^2, g0x = a_parallel B
U0 = gamma/N
Ux = (w-B gamma/N)/a_parallel .
```

N is retained until the lapse and dust equations are derived. The direct
connection includes B, B_dot and N_dot. Norm, inverse, projector and all
four frame invariants were verified exactly. Their homogeneous
first-order action has no B/B_dot/N_dot dependence. In this physical-unit
chart, the shift variation also changes the coordinate frame component:
its original momentum equation is linked to the frame equation.
It is not an independent discarded matter momentum source.

The symmetry argument retains translations and transverse reflection/
interchange symmetry; omitted transverse frame and off-diagonal spatial
components have no source within that sector. Transfer of these results
to a general inhomogeneous background still requires the full field audit.

Writing dots in the coordinate clock, the exact frame invariants are

```text
N^2 I1 = -w_dot^2/(1+w^2) + H_parallel^2
         +2 H_perp^2(1+w^2)
N^2 I2 = [w w_dot/gamma+gamma(H_parallel+2 H_perp)]^2
N^2 I3 = w^2 w_dot^2/(1+w^2)
         +(1+w^2)(H_parallel^2+2 H_perp^2)
         +2 H_parallel w w_dot
N^2 I4 = (w_dot+H_parallel w)^2

Q = gamma psi_dot/N
Y = w^2 psi_dot^2/N^2
a0 = w(w_dot+H_parallel w)/N^2
Delta psi = [w^2(psi_ddot-N_dot psi_dot/N)
             +w w_dot psi_dot+2 H_perp w^2 psi_dot]/N^2 .
```

As an independent geometry/frame control, the velocity Hessian agrees
with Eq. 7 of [Carruthers and Jacobson](https://arxiv.org/pdf/1011.6466)
after w=sinh(theta), sigma=-sigma_plus and the stated action/coupling
normalization mapping. Their vacuum stability results are not imported.

Define U_pot as the original scalar/reservoir/portal potential plus vacuum
density, J=v u_dot-u v_dot, and T as

```text
T_geometry = -3 M_P^2(alpha_dot^2-sigma_dot^2)
             -M_U^2[c1 N^2 I1+c2 N^2 I2+c3 N^2 I3-c4 N^2 I4]/2

T = T_geometry
    +(u_dot^2+v_dot^2+r_dot^2+K_Q(1+w^2)psi_dot^2
      -zeta w^2 J^2)/2
    -b w^2 z_dot psi_dot
    -b z w(w_dot+H_parallel w)psi_dot .

L_homogeneous = V[T/N - A |w psi_dot|^3/N^2
                  +N(b z^2/2-U_pot)] .
```

The Einstein term uses the inherited ADM/GHY boundary convention.
The executable uses the smooth branch w>0, psi_dot>0, retaining the exact
absolute-cube action there. Domain exit is rejected, not continued with
an unjustified analytic branch.

Before gauge fixing, the dust multiplier gives tau_dot=N C,
C=exp(beta psi). The lapse equation determines

```text
rho_m = epsilon C^4
      = -T/N^2 + 2 A |w psi_dot|^3/N^3 + b z^2/2-U_pot .
```

In the dust clock tau=t, N=1/C. Eliminating only N and epsilon gives the
eight coordinates q=(alpha,sigma,w,u,v,r,psi,z). The exact reduced energy
and alignment-corrected charge are

```text
E = -V rho_m/C
Q_U1 = V C [1-zeta w^2(u^2+v^2)] (u v_dot-v u_dot) .
```

The dust integral is therefore retained by reduced energy conservation.
At w=0, the action reduces to the original aligned G3 background action.
The tilted initial current differs from the old current because of the
alignment factor; equal initial field/velocity values do not imply equal
physical charge across the two backgrounds.

## Regulator equation, rank and the clock issue

The original first-order regulator equation was derived directly:

```text
dL/dz - d/dt(dL/dz_dot) = b N V (z+Delta psi) = 0 .
```

For nonzero tilt, this includes psi_ddot and z is not an algebraic
first-order auxiliary of the dust-clock action. Eliminating z in the bulk
instead gives -b N V (Delta psi)^2/2. Its psi_ddot-squared coefficient and
highest-time-derivative Hessian are

```text
coefficient = -b V w^4/(2 N^3)
H_highest = -b V w^4/N^3 .
```

For the first-order eight-coordinate velocity Hessian, the psi/z block is

```text
S = [[kappa, m], [m, 0]]
m = -b V w^2/N
kappa = (V/N)[K_Q(1+w^2)-6 A w^3 psi_dot/N]
det S = -m^2 .
```

Let R exclude psi,z. z_dot couples to no remaining velocity. Thus
S_inverse[psi,psi]=0 and the block Schur correction vanishes exactly:

```text
det H = -m^2 det R
inertia(H) = inertia(R) + (one positive, one negative) .
```

The proper geometry/frame determinant for G3 in M_P=1 reference units is

```text
det G = -eta(eta-12)[3 eta w^2+3 eta-20 w^2-24]/[48(1+w^2)] .
```

It is nonzero on the registered eta/tilt grid. At all 24 initial states,
R has inertia (5 positive, 1 negative, 0 zero), and H has
(6 positive, 2 negative, 0 zero). Numerical eigenvalue magnitudes and
condition numbers use the declared reference units and coordinate
normalizations; they are not canonical physical residues or masses.
The largest numerical condition number was 5.8688841142e9.

## Healthy fixed-frame control

Take a separate flat, fixed-frame scalar with K_Q,b>0, A=0:

```text
L_control = K_Q (n.partial pi)^2/2 - b (Delta pi)^2/2 .
```

Its preferred-frame Hamiltonian is positive and it has the ordinary
preferred-time dispersion K_Q Omega^2=b P^4. For a constant tilted frame,
define T=gamma t-w x and X=gamma x-w t. A mode labelled by dust-coordinate
omega,k has

```text
Omega = gamma omega-w k
P = gamma k-w omega
D = K_Q Omega^2-b P^4 .
```

At dust k=0, besides the zero root, the same dispersion gives

```text
omega^2 = K_Q gamma^2/(b w^4)
Omega = gamma omega
P = -w omega .
```

The nonzero roots are high preferred-momentum points of the same
preferred-frame field. They are not evidence for an additional independent
preferred-frame particle. At these roots, the preferred group-speed
magnitude is 2 gamma/|w|; on the opposing propagation branch, the map
between preferred and dust spatial momentum has a turning point at

```text
|P_turn| = sqrt(K_Q/b) gamma/(2 |w|) .
```

This control shows why an unrestricted tilted-slice initial-value
interpretation or a dust-time pole residue can misclassify a spatial
regulator. It does not prove that the full R4C1 theory has a suitable
preferred Cauchy foliation, healthy vortical sector or a physical cutoff.
The Hamiltonian-instability criterion also requires the relevant
nondegenerate physical time/constraint system, not just a coordinate
coefficient; see [Woodard's review](https://arxiv.org/abs/1506.02210)
for that general criterion. No theorem from that review is used to
declare this model physically inconsistent.

## Initial data and short local solutions

The frozen initial grid is eta=(1,1/4,1/16,1/64,1/256,1/1024) and
w=(1/2,1/4,1/8,1/16). Alpha=sigma=0 and
sigma_dot=w_dot=z_dot=0. The archived u,v,r,psi, their initial velocities,
and positive rho_m are retained.

Set z=w^2[H psi_dot+beta rho_m/K_Q] and solve the full lapse equation
for the expanding H root nearest the old aligned value. Both roots are
stored. This matches the old psi acceleration at the initial jet after
conversion to the dust clock:

```text
psi_ddot_initial = -3 H psi_dot-beta rho_m/K_Q-beta psi_dot^2 .
```

Every initial state has nonzero Y, a rank-eight Hessian and a solution
of all eight reduced Euler-Lagrange equations. Smooth coefficients and
nonsingular Hessian supply a local regular mechanical IVP in this patch.
This is a conditional homogeneous-sector local statement, not a full PDE
existence/uniqueness theorem.

| Initial-jet witness | Largest normalized residual |
| --- | ---: |
| Lapse constraint | 8.09538e-16 |
| Eight reduced equations | 1.59423e-16 |
| Matched psi acceleration | 1.37715e-16 |
| Energy/charge derivative | 6.32827e-15 |

Initial Y ranges from 1.4901161194e-10 to 1.0e-2. These values are
reference-unit background data, not galaxy accelerations.

For eta=(1,1/1024), w=(1/4,1/16), both DOP853 and Radau integrated all
16 position/velocity components over dust time [0,1e-3], at 51 samples,
rtol=1e-10 and atol=1e-12.

| Short-IVP witness | Recorded value |
| --- | ---: |
| Largest normalized energy drift | 2.68304e-15 |
| Largest normalized charge drift | 4.45159e-16 |
| Largest normalized cross-method state difference | 4.78867e-12 |
| Minimum evolved w | 0.06249999871 |
| Minimum evolved psi_dot | 1.9513447453e-4 |
| Minimum evolved rho_m | 0.1994451555 |

All eight runs succeed with finite states and positive w, psi_dot and
rho_m. The tiny time interval does not establish long-time stability,
alignment, an attractor, a nonempty physical EFT window or a healthy GR limit.

The independent direct-covariant action agrees with the reduced action at
the frozen diagnostic jets. A finite-difference velocity-Hessian check
has normalized maximum errors 2.04228e-9, 6.83264e-9 and 1.95174e-8
at h=1e-4,5e-5,2.5e-5. The error grows as the floating-point step shrinks
but remains below the frozen finest-step 1e-5 bound. All values are retained.

## Preserved failed check and correction

Attempt 01 remains FAIL_LOCAL_CHECKS at 265/266. Its symbolic
`rotation_noether_source` assertion applied a rotation only to the field
coordinates. Current alignment also depends on their velocities, so that
coordinate-only expression is not the full U(1) symmetry generator.
The preserved nonzero expression is

```text
w^2 zeta (u u_dot+v v_dot)(u v_dot-u_dot v) V C .
```

The corrected check includes both coordinate and velocity rotations:

```text
u L_v-v L_u+u_dot L_vdot-v_dot L_udot = 0 .
```

Two direct regulator-equation/highest-derivative checks were also added.
No action, background equation, input parameter, frozen tolerance or grid
was changed. Initial-data and trajectory artifacts are byte-identical
between attempts 01 and 02. The failed source, receipt and log are preserved.
The separate inherited original G3 112/113 derivative failure remains intact.

## Reproducibility and provenance

[Contract](RES001_R4C1_G3_TILTED_BACKGROUND_CONTRACT_2026-10-08.md):
SHA-256 508252d61dcdc73c28d9c568e4b80769aa1a3c88bb68cfc1a3306ccac078f9ac.

[Corrected script](../../../Analysis/MasterTests/test_01_r4c1_g3_tilted_background.py):
SHA-256 408320a076b4dabcfd01e4ec95d1cd7c7fcb788998012f85b64cc9f86916931b.

[Preserved first script](../../../Analysis/MasterTests/test_01_r4c1_g3_tilted_background_v1.py):
SHA-256 1fced9abc0e9b05f8aac86b27ed185bdfb41a531be12236cf8bf0b8387edaaf1.
Failed receipt SHA-256
aa9e434fff0cdb9975dbd120abf94080b0adeb5fddb74fbcb741a0ad3d5e264e.

Successful outputs: Analysis/MasterTests/outputs/r4c1_g3t_attempt_02.

| Artifact | SHA-256 |
| --- | --- |
| summary.json | 386120a3d38819127341cdd2db6dec9741471783a19beab2d4d7f6c1eca073b6 |
| formulas.json | d00499457b8468203cbdd91c985ddbd502e1f8489eb813bfa75780113d8f3597 |
| initial_data.json | c1b80b7c8cd1fd74e07fe797214a56f6c14f32f0416bb3966f6371cf4a85d243 |
| trajectories.npy | 470bdd1212e45fb3334e549003a6d6233f26f396043924c2ccb9b20bf13c18cd |

All 69 unique direct/transitive scientific source pins and artifact
sidecars were verified. The versioned G3V source is used as provenance;
the unversioned G3V file was not edited. No old receipt-writing main ran.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_tilted_background.py --output-dir Analysis/MasterTests/outputs/r4c1_g3t_attempt_02
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_tilted_background.py --output-dir Analysis/MasterTests/outputs/r4c1_g3t_attempt_02 --replay
```

Both successful commands exit 0; replay writes nothing and reproduces
all four payloads. The first command refuses existing output paths.
Full runtime versions are in the receipt.

Ignored logs retained under .local/itsm-context:

- First failed run: output-279f41e9f5d74e9cb18586cd50264a13.txt;
  SHA-256 a58244ce5500531a0be90ed32491d931c215ee7579d0536c9db459c9856bfe4a.
- Corrected run: output-72a551e23f0d4066948c14332139dd40.txt;
  SHA-256 352db8080216d1f0f9085032594fc9311d834e611504147a9464296e65aed933.
- Replay: output-43b4bdfdac1c454b8ba4c07e55d162f4.txt;
  SHA-256 cb518274841144b13c4a4d74dea5525626f96bd014df7b4337bc3cb693017d12.
- Integrity/statistics: output-d89fd638b9b24d6eb7f5660ec7b8e702.txt;
  SHA-256 9ccde5afe85547930cd286d50b26c371b1915ad2419ac169101e7d2dcc48b911.

The private memory packet ctx_9d4a86cc900a663c938c6d07 was used for
continuity only, with items chk_57a11159f38512994de40eff,
chk_4c4f556cdea69d5eeaa4ec9f and chk_ef45ba68ea1ce7c4e48da922 pointing
to the G3V report, contract and integrity addendum. All scientific evidence
was checked against live files. No model-mediated memory mutation occurred.

## Remaining work and parent holds

The next required calculation is the coupled finite-k constrained
principal symbol on this tilted, evolving background, expressed in a
declared admissible local time foliation. It must track preferred-frame
momenta and frequencies, retain the regulator, and distinguish coordinate
turning/extra roots from physical negative-energy modes.
A physical cutoff and overlap with background/perturbation scales still
need derivation before any scattering result can be assigned an EFT window.
Global preferred-leaf/Cauchy admissibility on I x T3 is not verified here.

Register R9-MT1-G3T inherits G3V/G3I/G3DF/G3D/G3F/G3A/G3E/G3Z/G3S/G3,
G2/G1/B1/S1/S2/S3/variation, applicable PD1 and Track-A scope/review debt.
Pending review alone does not block provisional research. The missing
physical-domain and full-spectrum inputs remain substantive blockers.

MAT-001=BLOCKED; UVIR-003=IN_PROGRESS; K_Q=NOT_DERIVED; V=NOT_COMPUTED;
Stage4A=CLOSED; TOP-X4 unchanged. Canonical Tests 1-3 HOLD_SUBSTANTIVE.
No ITSM SPARC prediction/likelihood, parameter/action change, manuscript/
PDF edit, provider dispatch, commit, push, promotion or publication.
