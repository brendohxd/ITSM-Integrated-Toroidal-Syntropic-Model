# R4C1-G3DF: finite-k dust-density diagnostics on the prepared plane

Date: 2026-10-08. Owner: Master Test 1 / conditional R4C1-v1 / G3.
**182/182 local checks pass; zero failed or unknown.** Three new artifacts
replay byte-for-byte. Review DEFERRED; Rule9_cleared=false; physics_pass=false;
gate_effect=NONE. Canonical Tests 1-3 remain HOLD_SUBSTANTIVE.

## Result and scope

The leading G3D dust-density dynamics accurately approximate the actual
density and its derivative on G3F's prepared finite-k solution planes, after
matching their actual initial density phase. All sampled kinetic weights on
these planes are positive. Every registered k doubling decreases the density
phase error; the worst normalized phase error at k=80 is 3.95813e-6
(0.000395813% in the specified norm), below the frozen 5% diagnostic target.

This is a new physical-variable projection of **18 archived full scalar
integrations**, not 18 new integrations. It covers eta=(1,1/4,1/16),
k=(20,40,80), t in [0,1], and 101 equally spaced samples. It does not prove a
physical EFT window, a universal density-only closure, arbitrary fast-wave
control, continuous-time bounds, all-sector stability or healthy full GR.

G3D was separately replayed and registered as R9-MT1-G3D: 172/172 local checks
and byte-identical artifacts. Its 30 September report was not changed.

## Physical reconstruction and reference

Use S1's generic auxiliary solutions with unchanged G3 parameters and the
G3S canonical map in its inherited spatially flat gauge (H!=0):

```text
q = R x,  qdot = Rdot x + R xdot,
D = (C^4 delta_epsilon + 4 beta rho_m delta_psi)/rho_m,
A = [[0,I],[-W,-G]],  J = [[G,I],[-I,0]],
L0 z = D,  L1 = dot(L0)+L0 A,  L2 = dot(L1)+L1 A.
```

Every coefficient derivative uses the full G3S background flow at fixed
comoving k. Six exact checks verify dust normalization, the regulator
constraint, density linearity, the large-k density phase map, its determinant
and the inherited leading generator. No density equation, Poisson law or
observational coefficient was inserted into the full reconstruction.

The physical embedding is E_phys=E_G3F sqrt(eta)/k. Exactly,

```text
lim_(k->infinity) [L0;L1] E_phys = T_G3D,
det(T_G3D) = -(12-eta)/(a^5 rho_m),
Dddot + (2H+beta psi_dot) Ddot - rho_m/(2 Mc2) D = 0,
Mc2 = 1-eta/12,  K_D = a^5 rho_m/k^2.
```

For archived full columns Y_phys, let N=([L0;L1](0)E_phys(0))^-1 and
F_full=[L0;L1]Y_phys N. Thus F_full(0)=I. The leading reference is
F_lead=T(t)F_slow(t)T(0)^-1. This changes the basis of the same prepared
plane; it does not change its span or fit a density history. An independent
integration of the leading dust equation from I agrees with this reference
to at most 1.93192e-11 normalized.

Initial finite-k reconstruction is not silently identified with the leading
map: its normalized discrepancy is exported separately below. The largest
initial mismatch is 0.0327478 at eta=1,k=20; even eta=1,k=80 has 0.00211486.
The much smaller matched-phase evolution error must not be presented as an
unmatched raw-observable error or measured fractional astrophysical accuracy.

## Registered grid

Errors are maxima over both full-system solvers and the 101 times.
Phase error is ||F_full-F_lead||_F/(1+||F_lead||_F).
Initial mismatch uses max_ij |map_full-map_lead|/(1+|map_lead|).
K error is max |K_plane/K_D-1|. These normalizations differ.

| eta | k | Matched density phase error | Raw initial map mismatch | Relative K error |
|---:|---:|---:|---:|---:|
| 1 | 20 | 5.50864e-5 | 3.27478e-2 | 7.70641e-4 |
| 1 | 40 | 1.35665e-5 | 8.40493e-3 | 1.92955e-4 |
| 1 | 80 | 3.38384e-6 | 2.11486e-3 | 4.82571e-5 |
| 1/4 | 20 | 6.33105e-5 | 2.12513e-3 | 7.64318e-4 |
| 1/4 | 40 | 1.58307e-5 | 5.42279e-4 | 1.91144e-4 |
| 1/4 | 80 | 3.95813e-6 | 1.36257e-4 | 4.77901e-5 |
| 1/16 | 20 | 6.00165e-5 | 6.85678e-4 | 7.53392e-4 |
| 1/16 | 40 | 1.50136e-5 | 1.71486e-4 | 1.88443e-4 |
| 1/16 | 80 | 3.75396e-6 | 4.28755e-5 | 4.71166e-5 |

Under doubling, phase-error ratios range from 0.246277 to 0.250159.
This is sampled behavior on three wavenumbers, not a proved convergence
exponent. Worst density-row error at k=80 is 2.46358e-6; derivative-row error
is 5.02598e-6. Worst density-method discrepancy over the grid is 2.58829e-12.

Reintegrated backgrounds agree between DOP853/Radau to 4.03574e-12 and with
the archived G3 trajectory to 1.17410e-12, passing the frozen 1e-10/1e-8
targets. Their tolerances are rtol=1e-11,atol=1e-13, as in G3F. The archived
full perturbation tolerances remain rtol=1e-9,atol=1e-11.

## Density chart, symplectic weight and effective generator

On the actual evolved prepared plane, with Z=Y_phys N, compute

```text
Omega0 = (E_phys(0)N)^T J(0) (E_phys(0)N),
K_plane = Omega0[0,1]/det(F_full),
B_plane = ([L1;L2] Z) F_full^-1 = [[0,1],[-M_plane,-Gamma_plane]].
```

Every sampled chart has det(F_full)>0 and is regular: the smallest determinant
is 0.211316 and largest condition number 6.03721 (<1e8).
The minimum sampled K_plane is 3.1248492e-5. Its ratio to leading K_D lies in
[0.99922936,0.99997550]. Full two-form transport and the density-coordinate
pullback agree to at most 2.71064e-12 relative. The generator's first-row error
is 1.11022e-16 normalized.

The sampled generator also remains close to G3D: largest normalized friction
and mass discrepancies are 2.69268e-4 and 5.57515e-4 over the grid; at k=80
they are at most 1.67414e-5 and 3.50253e-5. These were reported diagnostics,
not additional frozen pass thresholds. Friction lies in [0.469308,1.979263]
and mass in [-0.109709,-0.0113760].

The pullback supplies a two-dimensional symplectic density weight and
generator on this chosen moving solution family. It is not an independently
proved off-shell universal reduction of the full action. Coefficients can
depend on the preparation and full solution history. Even a corresponding
quadratic density Hamiltonian would have an indefinite potential when
M_plane<0; positive kinetic weight does not imply positive-definite energy.
No stationary quantum norm or all-sector stability follows.

## Provenance, replay and implementation disposition

The [contract](RES001_R4C1_G3_FINITE_K_DENSITY_CONTRACT_2026-10-08.md)
was frozen before the new density projections and numerical sign/error
sampling. Its SHA-256 is
`26ecfebc6d7792c0a5d6e065b8512f803d5ddd6e6316d01300d83ad7ef2769ce`.

- [Executable](../../../Analysis/MasterTests/test_01_r4c1_g3_finite_k_density.py):
  `95a0274d486b6ceaf816c8e361dcb012ceef73522c83b27cb98ce61741c4619d`.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_g3df_attempt_01/summary.json):
  `877b6f630a6692965656005fc823a2141b21daac4d32461f77e28dd12905a5a3`.
- [Formulas](../../../Analysis/MasterTests/outputs/r4c1_g3df_attempt_01/formulas.json):
  `f51ca9aca5f0ad2ea1dcc067f07cac65fbab3cf22808419c27cca5008ca206c9`.
- [Density transfers and sampled generators](../../../Analysis/MasterTests/outputs/r4c1_g3df_attempt_01/density_transfers.json):
  `43eac96fe2df2d8e6369304553d3e7cd9aec21d54ecbde660933885fba8ed12f`.
- Inherited archived G3F columns:
  `2a7df2c3ca35f5d438f54520241c880692c9804d03f3bf1bf696cf183345bccc`.

All 53 unique direct/transitive source pins match. Artifact sidecars match.
Replay recomputes all three artifacts without writes and reproduces their
bytes. Existing output directories are refused. No older receipt-producing
main() was invoked. Replay command:

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_finite_k_density.py --replay
```

The initial implementation was interrupted before scientific output creation
because global rational simplification was slow. Its source is preserved as
`test_01_r4c1_g3_finite_k_density_v1.py`, SHA-256
`2970b1a1b7fe8821ce228de3522828b24dbfebfe11b4c841e56dd6efeab48940`.
The completed implementation extracts the linear density coefficients before
canonical substitution and retains the exact second-derivative expression
without global expansion/factorization. It changes no action, grid, threshold
or initialization. The interrupted run supplied no numerical verdict. Native
file writes were used after the patch tool failed to create files; no existing
scientific file was lost. Peripheral process diagnostics failed or were
unavailable and supplied no scientific evidence. Local logs remain ignored.

## Disposition and next discriminating work

Register R9-MT1-G3DF. PROCEED_PROVISIONALLY applies to these prepared,
sampled finite-k density diagnostics; claim Conditional, review DEFERRED.
Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A/G3F/G3D
and their scope/deferred-review dependencies. No substantive failure within
this bounded grid. This does not clear the inherited full-theory holds.

The next obligation is the **action-derived interaction scale and physical
validity domain**: identify a controlled range with background scales below
k/a and k/a below the relevant cutoff, and test all retained sectors there.
The numerical chart wavenumbers have no demonstrated admissibility yet.
Continuous-time estimates and fast-data dependence remain separate needs;
101 samples can miss high-frequency extrema. The eta=0 auxiliary rank change,
tensor/frame and healthy complete-parent requirements remain open.

Nonlinear periodic/weak-field response and blind acceleration-coefficient
matching follow only once their parent/domain prerequisites survive. Current
results supply no SPARC force law or observational MCMC likelihood.
Canonical Tests 1-3 HOLD_SUBSTANTIVE. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged. No memory
mutation, provider dispatch, PDF edit, commit, push, promotion or publication.
