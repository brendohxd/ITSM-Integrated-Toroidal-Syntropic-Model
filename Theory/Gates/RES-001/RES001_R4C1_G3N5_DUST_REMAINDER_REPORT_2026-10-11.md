# G3N5: exact dust split, graph correction, finite-mode bounds

Date: 11 October 2026. Owner: Master Test 1 / conditional R4C1/B1.
Local result: **78/78**, zero failed/unknown registered checks, exact
read-only scientific replay. **The analytic dust milestone remains OPEN.**
The certified finite-mode majorants below are too loose to establish a
useful accuracy estimate or uniform high-momentum convergence.
Review DEFERRED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.

## 1. New result and scope

Starting from the unchanged [finite-mode archive](RES001_R4C1_G3N5_DUST_FINITE_K_REPORT_2026-10-11.md),
retain the full 20-state generator and all 22 reconstructed original fields.
For z=B x, define O_z=O B_inverse, E_z=B G (O G)^(-1), W=O_z z,
r=z-E_z W. The entire complement is retained; O_z r=0 initially and along
the exact split. This is not continuous projection of evolution onto G.

The exact factored equations are

```text
F = O_z_dot + O_z A_z,     Delta = F E_z - M,
R = F - M O_z,
S = A_z E_z - E_z_dot - E_z(M+Delta),
J = A_z - E_z F,
W_dot = (M+Delta) W + R r,
r_dot = S W + J r,
M = [[H,1],[6 rho_m/11,-H-(2/5) psi_dot]].
```

The 2x2 adjugate identity, lift factorization, differentiated inverse and
feedback-before-inverse identities verify normalization and moving-kernel
tangency without huge denominator expansions. Archive recomposition uses
the factored S/J, with worst normalized residual 1.672672874329736e-15.
The five original modes and all four prepared/complementary columns are
retained. Nonmonotonic complementary transfer in the old archive is unchanged.

The instantaneous graph correction has no order-one or inverse-p term:

```text
Delta = D2(t)/p^2 + D4(t)/p^4 + higher terms,  p=ell/a>0.
```

Exact D2, D4 and the rational tail are exported in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_remainder_attempt_01/formulas.json).
This is a correction on the declared evolving graph, NOT a closed effective
slow generator after complementary feedback. R and S are nonzero. Dropping
R r is not justified by this expansion. Momentum drift and B_dot remain.

## 2. Certified bounds and the unresolved estimate

B1G's exact energy/constraint theorem gives rational background enclosures
on [0,1/20], independently of sampled extrema:
a in [1,20/19], H in [3/4,1], rho_m in [17/100,1/5],
psi_dot in [1/6,1/5], C in [1,250/249]. u,r are in [71/80,89/80],
v in [-9/80,9/80], and scalar/reservoir velocities in [-9/4,9/4].
The energy argument and short-time positivity bootstrap are checked.
Only the graph determinant certificate is reduced by the conserved
Friedmann relation; no v_dot division or rewriting of parent matrices occurs.
Exact rational interval arithmetic certifies nonzero graph determinant
and matrix majorants for ell=4,8,16,32,64 over the WHOLE interval.

In the frozen reference-unit infinity norm, set
m>=||M||, d>=||Delta||, c>=||R||, s>=||S||, j>=||J||,
Lambda=max(m+d+c,s+j). For prepared W0 norm 1, r0=0,

```text
||W(t)-Phi(t) W0|| <= (d t+c s t^2/2) exp(Lambda t).
```

For complementary W0=0, r0 norm 1, ||W(t)||<=c t exp(Lambda t).
This follows from a nonnegative two-block majorant and variation of constants.
All constants are explicit rational numbers in
[diagnostics.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_remainder_attempt_01/diagnostics.json).
Exact expressions are certificates; rounded logarithms below are displays.

| ell | log10 of displayed prepared bound at t=0.05 |
|---:|---:|
| 4 | 347.6269791995195 |
| 8 | 65.63855157360047 |
| 16 | 96.45102540001255 |
| 32 | 313.63721642775926 |
| 64 | 1189.5811167465122 |

These are extremely conservative UPPER bounds, not measured growth rates,
physical instability or proof that the observed slow approximation fails.
Their growth with momentum discards oscillatory cancellation. The missing
result is a complementary propagator/fast-forcing estimate uniform in p,
including generated complementary response. Thus the actual full-dust
convergence order remains NOT_PROVED; the observed inverse-square trend
in the original finite sample is not promoted to a theorem. The independent
GR/domain assessment may proceed under the approved plan.

## 3. Receipt, precision, preserved history

- [Contract](RES001_R4C1_G3N5_DUST_REMAINDER_CONTRACT_2026-10-11.md):
  8c9ae0331a826c583f26e969dc61697d6e71345b16e1448be1940b3b3ecfa21c.
- [Executable v6](../../../Analysis/MasterTests/test_01_r4c1_g3n5_dust_remainder_v6.py):
  efef4d8cc501fbbf7f62f2c9e60d12a5dceab8c24f0caaa73b3136e952eba913.
- [Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_dust_remainder_attempt_01/summary.json):
  0da2e0166bb30f3f15cbbda980cc90ee9cefd30bd3aeb602f816dc6d3da621cd.
- Formulas: ccdfab337bd9e5922125d077f2c41e0859ca4fe46ebff3c4cad27abaa2cfbdd5.
- Diagnostics: 864bddad18f1969894ad253f627b36467502cb989fa87e22d08ed77e00d54537.

Reproduction: Python in itsm_env, -B, executable v6; --replay followed by
Analysis/MasterTests/outputs/r4c1_g3n5_dust_remainder_attempt_01 performs
exact scientific byte/sidecar comparison without modifying receipts.
Rational/SymPy algebra and interval enclosures are distinct from binary64
archive checks using the saved 70-digit degree-40 background coefficients.
No new high-precision IVP, arbitrary-data theorem or physical norm is claimed.

429 input/source/available-sidecar files preserve hashes, sizes and mtimes
through calculation. Sources v1-v3 were interrupted at symbolic bottlenecks
without mathematical verdicts. v4 had a NameError in a stale expanded-S
check, before receipt creation. v5 finished numerical/bound checks but its
expanded-denominator export was interrupted. All source versions and original
sidecars remain; private logs/progress records stay local. v6 preserves
factored scalar expressions in the existing matrix wire shape; acceptance
thresholds, physics and archive data were not changed.

Inherited failed receipts, three absent UVIR sidecars, the -11/6 original
slow coefficient, ordinary-wave Jordan defect and indefinite complete
density Hamiltonian remain. No physical ghost, Cauchy, cutoff or GR clearance.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Review dependencies: R9-MT1-G3N5-DUST-REMAINDER, finite-mode/weighted/nonzero
G3N5, B1G and inherited operator/action review, all DEFERRED.
