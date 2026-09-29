# R4C1-C2: the conditional periodic response does not identify `A`

Date: 2026-09-29. Owner: Master Test 3 / conditional R4C1-v1.
The [C2 contract](RES001_R4C1_PERIODIC_IDENTIFIABILITY_CONTRACT_2026-09-29.md)
(SHA-256 `dd711d678c824e7f414b9170c164fc3cc101d880134df9d58012a5c0ddbf6d7a`)
was frozen before execution. C2 uses the unchanged action, C1 homogeneous
identifiability result, and T2P1 fixed-frame periodic contrast method.
The separate [source-pin addendum](RES001_R4C1_PERIODIC_IDENTIFIABILITY_PIN_ADDENDUM_2026-09-29.md)
(SHA-256 `637b4b48cd153551dfa98052e1beecace868b4bfd44f9ea38eb15cb0466c65e0`)
strengthened receipt provenance after the first local run, without changing
the action, equations, source, solver, grids or acceptance thresholds.
It introduces no observed acceleration, Hubble calibration or galaxy data.

**Decision:** Within the conditional static density-contrast reduction on
`T^3`, every positive `A` has a unique weak solution, and different `A`
values give different on-shell solutions for the same nonzero source.
The cubic-gradient energy decreases strictly as `A` increases. This
establishes a continuum *identifiability obstruction*: compact topology
and the pinned homogeneous/classical-linear data do not themselves
select the physical `A/K_Q^(3/2)` coupling. It does **not** prove a
coupled physical torus solution or derive `C_chi` or `a0`.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`, `canonical_Test3_pass=false`.

## 1. Exact result, distinct from finite-grid validation

Let `H^2_0(T^3)` be the real mean-zero Sobolev space on the cubic torus
of period `2*pi`; take the smooth nonzero, mean-zero density contrast
`delta_rho=(cos x+2 cos y+3 cos z)/50`. With `b=5/11>0`,
`beta=2/5>0`, and `A>=0`, the fixed-frame snapshot functional is

\[
 J_A[\psi]=\int_{T^3}\!\left[
 A|\nabla\psi|^3+\frac b2(\Delta\psi)^2
 +\beta\,\delta\rho\,\psi\right]d^3x.
\]

On mean-zero `H^2`, the Fourier/Poincare estimate controls its full
`H^2` norm by `||Delta psi||_2`. The linear source is bounded by that
norm, so the positive quadratic `b` term makes `J_A` coercive. The
nonnegative `|grad psi|^3` term is convex and finite because
`H^2(T^3)` embeds in `W^{1,3}(T^3)`. Weak lower semicontinuity and the
direct method give a minimizer. The `b||Delta psi||_2^2/2` term is
strictly convex on the mean-zero space, so the minimizer is unique.
No torus zero-mode inverse has been smuggled into this argument.

For every test field `phi` in that space, its weak Euler equation is

\[
 3A\int|\nabla\psi_A|\nabla\psi_A\cdot\nabla\phi
 +b\int\Delta\psi_A\Delta\phi
 +\beta\int\delta\rho\,\phi=0.
\]

Suppose `A_1 != A_2` had the same minimizer `psi`. Subtract the two
weak equations and choose `phi=psi`; then
`3(A_2-A_1) integral |grad psi|^3=0`. Thus `grad psi=0`, and the
mean-zero gauge gives `psi=0`. The remaining weak equation would imply
`delta_rho=0` (choose `phi=delta_rho`), contradicting the prescribed
source. Therefore `psi_{A_1} != psi_{A_2}`. This proof deliberately
excludes the zero-source case, for which `psi=0` for all `A`.

Define `P_A=int |grad psi_A|^3` and
`L(psi)=b||Delta psi||_2^2/2+beta<delta_rho,psi>`. If `A_2>A_1`,
uniqueness and distinctness give the two **strict** minimizer inequalities

\[
 A_1P_{A_1}+L(\psi_{A_1})
 < A_1P_{A_2}+L(\psi_{A_2}),\qquad
 A_2P_{A_2}+L(\psi_{A_2})
 < A_2P_{A_1}+L(\psi_{A_1}).
\]

Adding them yields `(A_2-A_1)(P_{A_2}-P_{A_1})<0`, hence
`P_{A_2}<P_{A_1}`. This is an integral ordering, **not** a theorem that
every pointwise acceleration component decreases with `A`.

The continuum argument is conventional mathematical reasoning supplied
here for review, not a proof-assistant certificate or independent
peer review. It applies to the conditional frozen metric/frame snapshot,
not the unresolved full Einstein/frame/dust/Euler system.

## 2. Registered finite-grid witness

With `A_B1=2/7`, C2 preregistered ratios `A/A_B1={1/4,1,4}` and reused
T2P1's `b`, `beta`, source, zero-mean gauge, solver and 17/25/33 grids.
The first [attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_c2_attempt_01/summary.json)
(SHA-256 `d84689e19df53d29a03cc3f2d0c510d5e54c0681a86090fa7cfbe4c78a5e4dfb`)
passed 107/107 local checks, but its executable did not itself rehash the
parent receipts' underlying source maps. It is preserved, not silently
overwritten or described as a physics failure. The
[attempt-02 receipt](../../../Analysis/MasterTests/outputs/r4c1_c2_attempt_02/summary.json)
(SHA-256 `f952675689274c4ccaf1d66004ce7e6c20783096d4c90ab932abd52495c5eef4`)
passes **107/107** with zero failed/unknown checks after verifying nine
direct pins and eleven unique transitive source paths before importing
the prior solver or reading B1 parameters. An independent live recheck
found no hash mismatch; the grid and check records are identical between
the two attempts. The parent source map explicitly pins the B1 script.

At `N=33`, the mean cubic-gradient values for increasing `A` are
`1.03298715284077e-4`, `8.58230005918213e-5`, and
`5.0664756669539e-5`. The adjacent decreases relative to the B1
value are `0.203625` and `0.409660`, well beyond the frozen `1e-4`
resolution margin. The adjacent zero-mean field RMS separations,
relative to the B1 field, are `0.0634922` and `0.1606040`.
The maximum normalized strong residual among the nine solves is
`3.258e-8`; the maximum registered weak residual is `2.547e-8`
(both thresholds `1e-5`). The largest 25-to-33 fundamental-cosine
relative change is `8.720e-9` (threshold `5e-3`). These are discrete
method checks, not continuum or physical-domain error bounds.

The zero-source control correctly returns the same zero stationary
solution for all `A`; the false equal-response claim for the nonzero
source is rejected. Keeping `K_Q`, `b`, `beta` and topology fixed changes
the invariant `A/K_Q^(3/2)`, so this sweep is not a field-chart
renaming. The [executable](../../../Analysis/MasterTests/test_03_r4c1_periodic_identifiability.py)
has SHA-256 `a641e5d6eb17cd4512bd91c483a23952e24de828bb6008eb8ccc12aee7c6d645`.
It imports only the pinned T2P1 definitions after verifying their bytes
and the parent source maps;
neither older receipt-producing `main()` is run or overwritten.

## 3. Scientific and governance boundary

C1 already showed the homogeneous equations and classical pre-constraint
quadratic action are `A`-independent on the aligned branch, while the
conditional spherical force normalization depends on `A`. C2 adds an
**on-shell** periodic, finite-`b`, nonspherical contrast example; it
does not manufacture a physical galaxy or a full `C_chi` map from that
example. It demonstrates why a background/topology-only matching claim
cannot determine the nonlinear spatial coefficient in this candidate.
An additional target-independent microscopic or nonlinear matching
condition might fix `A`; no such condition has been derived here.

The historical equation reconstruction remains incomplete. The analyst
has seen historical target context, so this is data-independent but
**not fresh analyst-blinded**. No coefficient among `1`, `2*pi`,
`1/(2*pi)`, or `sqrt(1-q_dec)/(2*pi)` is selected; there is no fifth
independently derived coefficient, `a0(z)` prediction, or justified
SPARC/bTFR/lensing ranking. The physical cutoff, full constrained IVP,
coupled weak-field law and projection factor also remain open.

Rule-9 review is deferred, not cleared. Its later review must check the
Sobolev/convexity hypotheses, the strict inequality argument, inherited
C1/T2P1 source chain, numerical-grid and solver boundaries, and the
distinction between an `A`-dependent conditional response and a unique
physical `C_chi`. Tests 1–3, MAT-001, UVIR-003, Stage 4A, the canonical
parent and publication holds are unchanged.
