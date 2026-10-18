# TOP-001 ET2-A0 topology, signature, and spectrum control contract

- **Date frozen:** 2026-10-17
- **Route:** `TOP-001 / ET2-A0`
- **Class:** mathematical-template control only
- **Owning gate:** `TOP-001` (`OPEN_SCAFFOLD_ONLY`)
- **Canonical effect:** none
- **Physics pass:** false by construction

## 1. Question

Test, without changing the canonical ITSM geometry, whether a two-torus plus a
time-like coordinate can be usefully separated into the following distinct
possibilities:

1. ordinary Lorentzian time, `R_t x T2`;
2. noncompact, zero-temperature **Euclidean** time, `R_tau x T2`;
3. finite-temperature or otherwise compact **Euclidean** time,
   `S1_tau x T2`;
4. compact **Lorentzian** time, `S1_t x T2`;
5. 3+1-dimensional cylinders `R_t x R_z x T2`,
   `S1_tau x R_z x T2`, and `S1_t x R_z x T2`;
6. the current canonical branch, `R_t x T3`;
7. finite-temperature Euclideanization of the canonical branch,
   `S1_tau x T3`; and
8. the existing TOP-X4 branch, `R_t x T3_obs x S1_y`.

The control must answer the naming question exactly while keeping topology,
metric signature, coordinate role, field boundary conditions, and total
dimension separate.

## 2. Frozen branch ledger

| Branch | Product | Signature | Total dimension | Compact torus rank | Frozen interpretation |
|---|---|---:|---:|---:|---|
| canonical | `R_t x T3` | Lorentzian `(-+++)` | 4 | 3 | noncompact time plus three compact spatial cycles |
| ET2 | `S1_tau x T2` | Euclidean `(+++)` | 3 | 3 | abstractly `T3`, but one circle is Euclidean time |
| LT2 | `R_t x T2` | Lorentzian `(-++)` | 3 | 2 | 2+1-dimensional spacetime; not `T3` |
| E0T2 | `R_tau x T2` | Euclidean `(+++)` | 3 | 2 | Euclidean signature with noncompact time; not `T3` |
| CYL-T2 | `R_t x R_z x T2` | Lorentzian `(-+++)` | 4 | 2 | 3+1-dimensional spacetime with only two compact spatial cycles |
| E-CYL-T2 | `S1_tau x R_z x T2` | Euclidean `(++++)` | 4 | 3 | 4D Euclidean space with compact factor `T3`, not a wholly compact `T3` |
| PLT2 | `S1_t x T2` | Lorentzian `(-++)` | 3 | 3 | abstractly `T3`, but contains a compact timelike circle |
| PL-CYL-T2 | `S1_t x R_z x T2` | Lorentzian `(-+++)` | 4 | 3 | 3+1-dimensional compact-time cylinder with the same direct-product CTC hold |
| ET3 | `S1_tau x T3` | Euclidean `(++++)` | 4 | 4 | finite-temperature Euclidean canonical branch; abstractly `T4` |
| TOP-X4 | `R_t x T3_obs x S1_y` | Lorentzian `(-++++)` | 5 | 4 | noncompact time plus four compact spatial/internal cycles |

The route label `TOP-X4` is not being redefined as “four-dimensional
spacetime.” Here it denotes the already frozen extra-circle route.

Euclidean signature alone does not compact time: `R_tau` becomes `S1_tau`
only after imposing a periodic identification such as finite-temperature KMS
boundary conditions. In a 3+1-dimensional T2 cylinder, the compact Euclidean
factor can be `T3` while the full manifold remains `R_z x T3`.

## 3. Exact identities under test

### 3.1 Topology

For `T^n=(S1)^n`,

```text
pi_1(T^n) = Z^n,
b_k(T^n) = C(n,k),
chi(T^n) = sum_k (-1)^k b_k = 0  for n >= 1.
```

Therefore `S1_tau x T2` is `T3` as an abstract manifold and has Betti numbers
`[1,3,3,1]`. This identity does not identify the Euclidean-time circle with a
spatial circle in a physical model.

### 3.2 Periodic bosonic spectrum

For circumferences `(beta,L1,L2)` and periodic fields, remove the common
factor `(2*pi)^2` and compare

```text
lambda_ET2(n_tau,n1,n2)
  = n_tau^2/beta^2 + n1^2/L1^2 + n2^2/L2^2
  = lambda_T3(n0,n1,n2)
```

under `n0=n_tau`. The equality must hold exactly with rational arithmetic on
the frozen cube `[-3,3]^3`.

For `S1_tau x R_z x T2`, the additional noncompact momentum contributes the
same `k_z^2` term to both representations. The compact-sector equality must
therefore remain exact for the frozen rational `k_z` samples, without
misidentifying the full manifold as a compact `T3`.

Two negative controls are mandatory:

- deleting the Matsubara term must be detected whenever `n_tau != 0`;
- replacing periodic Euclidean-time boundary conditions by thermal fermionic
  anti-periodicity, `n_tau -> n_tau+1/2`, must break the labelwise periodic
  spectrum equality and remove the temporal zero mode.

Thus equal product topology is insufficient to fix the physical spectrum;
spin structure and boundary conditions remain independent inputs.

### 3.3 Compact Lorentzian time

For the direct-product metric on `S1_t x T2`, the curve with fixed spatial
coordinates and one winding around `S1_t` is closed and has timelike tangent.
The branch therefore carries an explicit closed-timelike-curve hold. No claim
about a non-product chronology-protected construction is made.

### 3.4 First-shell dimension control

For an isotropic periodic `T^n`, the integer vectors of squared norm one have
degeneracy `2n`. The expected values are `T2=4`, `T3=6`, and `T4=8`.

## 4. Dependency receipt

The audit must verify the current SHA-256 receipts for the governing identity,
gate, programme, Rule-9 policy, active-research pointer, TOP-X4 route plan, and
the existing TOP-X4 A0 JSON. It must also verify that the TOP-X4 A0 result is a
14/14 mathematical control with `physics_pass=false`, `gate_effect=NONE`, and
`canonical_t3_replaced=false`.

## 5. Claim firewall

The calculation must not import or fit `a0`, `H0`, SPARC data, a target `2*pi`
coefficient, or a target reservoir current. It must emit no derived physical
claims.

Passing this contract establishes only:

- the abstract-manifold identity `S1_tau x T2 ~= T3`;
- exact periodic-boson mode-spectrum equivalence for the frozen rectangular
  lengths and labels;
- explicit failure of that equivalence when the required temporal term or
  boundary condition is changed;
- exact dimension, compact-rank, homology, and first-shell bookkeeping; and
- the direct-product compact-Lorentzian-time CTC obstruction.

It does **not** establish:

- Lorentzian continuation or a causal propagator;
- reflection positivity, KMS consistency, or a valid thermal state;
- an ITSM Euclidean condensate action, saddle, stress tensor, or Hessian;
- any mapping between Euclidean winding and an observed current;
- equivalence to the canonical spatial `T3` model as physics;
- radion or modulus stabilization;
- `K_Q`, `V`, `a0`, `H0`, or any observational prediction; or
- a TOP-001 gate transition, canonical promotion, or publication readiness.

## 6. Pass and hold rule

All exact checks must pass for the receipt status

```text
PASS_TOP001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTROL_HOLD_LORENTZIAN_COMPLETION
```

Even on that pass:

```text
calculation_status = PASS
physics_pass = false
gate_effect = NONE
canonical_t3_replaced = false
claim_status = Open
review_status = DEFERRED
Rule9_cleared = false
research_execution = PROCEED_PROVISIONALLY
```

The next admissible step is a separately frozen Euclidean condensate-action
and continuation contract covering Wick rotation, KMS/spin structure,
reflection positivity, causal/retarded continuation, stress tensor, and the
relationship—if any—between temporal and spatial winding. Until then,
Lorentzian completion remains a substantive hold.
