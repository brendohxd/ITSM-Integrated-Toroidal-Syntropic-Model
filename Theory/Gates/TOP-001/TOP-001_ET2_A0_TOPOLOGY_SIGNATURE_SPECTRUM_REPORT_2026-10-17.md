# TOP-001 ET2-A0 topology, signature, and spectrum report

- **Date:** 2026-10-17
- **Route:** `TOP-001 / ET2-A0`
- **Result:** `PASS_TOP001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTROL_HOLD_LORENTZIAN_COMPLETION`
- **Checks:** `22/22 PASS`, `0 FAIL`, `0 UNKNOWN`
- **Physics pass:** `false`
- **Gate effect:** `NONE`
- **Canonical T3 replaced:** `false`
- **Rule-9:** `DEFERRED`; `Rule9_cleared=false`; provisional research may proceed

## Executive result

Yes: compact Euclidean time opens a mathematically distinct and potentially
useful branch, but it does not collapse the existing options into one model.
The exact result is:

- `S1_tau x T2` is a `T3` as an **abstract Euclidean manifold**.
- Euclidean signature alone does not close time: `R_tau x T2` remains compact
  rank two and is not `T3` until `tau` is explicitly identified periodically.
- With periodic bosonic boundary conditions, it has exactly the same
  rectangular mode formula as a Euclidean `T3` with circumferences
  `(beta,L1,L2)`.
- It is not thereby the same physical model as the canonical spatial `T3`.
  One cycle has a temporal role, and the spin structure, thermal boundary
  conditions, Wick rotation, and Lorentzian continuation remain additional
  physics.
- `R_t x T2` is instead a 2+1-dimensional Lorentzian spacetime. Ordinary time
  is noncompact and is not a third torus circle.
- If the intended model is 3+1-dimensional, the T2 branch requires another
  noncompact spatial coordinate: `R_t x R_z x T2`. Its finite-temperature
  Euclidean form is `S1_tau x R_z x T2 = R_z x T3`: the **compact factor** is
  `T3`, while the full four-dimensional manifold is not a compact `T3`.
- `S1_t x T2` is also abstractly `T3`, but for the direct-product Lorentzian
  metric its timelike circle is itself a closed timelike curve. Adding `R_z`
  does not remove that curve. Those branches are held, not adopted.
- `S1_tau x T3` is abstractly Euclidean `T4`; TOP-X4 is different again:
  `R_t x T3_obs x S1_y`, a five-dimensional Lorentzian spacetime whose four
  compact cycles are spatial/internal.

This resolves the naming ambiguity while preserving the scientific question:
the Euclidean-time `T3` branch deserves a controlled action-and-continuation
test, not automatic replacement of the current canonical branch.

## Branch ledger

| Branch | Product | What the dimension means | Compact rank | Result |
|---|---|---|---:|---|
| canonical | `R_t x T3` | 3+1 Lorentzian | 3 | current canonical branch; unchanged |
| ET2 | `S1_tau x T2` | 3D Euclidean | 3 | abstract `T3`; candidate methods branch |
| LT2 | `R_t x T2` | 2+1 Lorentzian | 2 | not `T3` |
| E0T2 | `R_tau x T2` | 3D Euclidean | 2 | noncompact Euclidean time; not `T3` |
| CYL-T2 | `R_t x R_z x T2` | 3+1 Lorentzian | 2 | four-dimensional, but not compact `T3` |
| E-CYL-T2 | `S1_tau x R_z x T2` | 4D Euclidean | 3 | compact factor `T3`; full manifold `R_z x T3` |
| PLT2 | `S1_t x T2` | 2+1 Lorentzian | 3 | direct-product CTC hold |
| PL-CYL-T2 | `S1_t x R_z x T2` | 3+1 Lorentzian | 3 | same direct-product CTC hold |
| ET3 | `S1_tau x T3` | 4D Euclidean | 4 | abstract `T4` |
| TOP-X4 | `R_t x T3_obs x S1_y` | 4+1 Lorentzian | 4 | existing extra-spatial/internal-circle fork |

## Exact controls

### Topology and winding bookkeeping

The ET2 branch obeys

```text
S1_tau x T2 = (S1)^3 = T3,
pi_1 = H_1 = Z^3,
b_k = [1,3,3,1],
chi = 1 - 3 + 3 - 1 = 0.
```

The three integer windings therefore exist topologically, but the audit does
not identify their physical roles: one winds Euclidean time and two wind
space.

The separate `R_tau x T2` check confirms that Wick rotation changes signature
but does not by itself change compactness. Periodic identification is an extra
model/state condition.

### Periodic spectrum identity

The audit used exact rational circumferences

```text
(beta,L1,L2) = (5/3,7/4,11/6)
```

and all `343` labels in `[-3,3]^3`. Removing the common factor `(2*pi)^2`,

```text
n_tau^2/beta^2 + n1^2/L1^2 + n2^2/L2^2
```

matched the rectangular periodic `T3` expression exactly, with zero
mismatches.

For the 3+1-dimensional Euclidean cylinder, the audit added the common
noncompact term `k_z^2` at three exact rational samples. All `1,029`
`(k_z,n_tau,n1,n2)` sample pairs matched. This preserves the compact-sector
identity while retaining the full manifold as `R_z x T3`.

This is an isospectrality statement for the frozen free periodic operator. It
is not an action, interaction, state, or Lorentzian equivalence result.

### Negative controls

Two deliberate changes were detected:

1. Deleting the Matsubara term produced a mismatch for all `294` labels with
   `n_tau != 0`.
2. Thermal fermionic anti-periodicity, `n_tau -> n_tau+1/2`, produced zero
   labelwise equalities against the periodic spectrum across all `343` tested
   labels and removed the temporal zero mode.

These controls show why topology alone cannot select the physical spectrum.

### Dimensional shell check

The isotropic first-shell degeneracies were recovered exactly:

```text
T2: 4,  T3: 6,  T4: 8.
```

### Lorentzian-time obstruction

On the direct products `S1_t x T2` and `S1_t x R_z x T2`, hold every spatial
coordinate fixed and wind once around `S1_t`. The curve closes by periodicity
and has unit-speed tangent norm `-1`. It is therefore a closed timelike curve.
The result is limited to these direct-product metrics and does not claim a
theorem about every possible non-product construction.

## TOP-X4 relationship

The prior TOP-X4 A0 receipt was rechecked byte-for-byte:

```text
status = PASS_TOPX4_A0_KINEMATIC_AND_DIMENSIONAL_CONTROL
checks = 14/14
physics_pass = false
gate_effect = NONE
canonical_t3_replaced = false
sha256 = 0559b5a699f140f5690a73a3d6f8eeeeb77188cdf59d3551359736d5293fa3e7
```

Its exact `T4 = T3 + KK circle` spectrum check passes, but TOP-X4 represents
an extra compact spatial/internal circle alongside noncompact Lorentzian time.
It is one member of the broader possibility set, not the same construction as
compact Euclidean time.

## Scientific holds

The control does not supply:

- a frozen Euclidean ITSM condensate action or saddle;
- reflection positivity or a valid KMS/spin-structure completion;
- a justified Wick rotation or causal/retarded Lorentzian continuation;
- a stress tensor, physical Hessian, or stability result;
- an admissible compact-Lorentzian-time model beyond the demonstrated CTC
  obstruction;
- a derived map from temporal winding to an observed current;
- `K_Q`, `V`, `a0`, `H0`, SPARC fits, or any observational prediction; or
- a gate transition, canonical promotion, or publication readiness.

Accordingly, `physics_pass=false` and `gate_effect=NONE` remain mandatory.

## Recommended next bounded test

Freeze a separate ET2 action-and-continuation contract before doing any fit or
phenomenology. It should require, in order:

1. one explicit Euclidean condensate action on `S1_tau x T2`, including field
   content, temporal/spatial boundary conditions, and all circumference/modulus
   conventions;
2. a stated interpretation of `beta`—thermal inverse temperature, regulator,
   or geometric cycle—and rejection tests that distinguish those cases;
3. reflection-positivity and quadratic-operator checks around a frozen saddle;
4. an explicit Wick-rotation/analytic-continuation prescription and retarded
   pole test;
5. KMS and fermionic spin-structure checks where matter is present;
6. stress-tensor and physical-Hessian calculations; and
7. only after those pass, a comparison with the canonical `R_t x T3` and
   TOP-X4 branches.

Until that contract passes, ET2 is a promising mathematical route, not a
solution to the open ITSM physics gates.

## Reproducibility receipt

Artifacts:

- contract:
  `Theory/Gates/TOP-001/TOP-001_ET2_A0_TOPOLOGY_SIGNATURE_SPECTRUM_CONTRACT_2026-10-17.md`
- deterministic audit:
  `Analysis/TOP/TOP-001/top001_et2_a0_topology_signature_spectrum_audit.py`
- machine receipt:
  `Analysis/TOP/TOP-001/outputs/top001_et2_a0_topology_signature_spectrum_summary.json`

SHA-256 values at execution:

```text
3c4782f287a9a1eed518eaed9c9ecac8067bfeb90c60f6d1733ec20881413480  contract
b402e247effa4a4c7bde912efefb41031dd5f6389597863f4d565717223f7f1d  audit script
52cd474d418b6ee7d0393d1f0af150acaa1a061045613631caa31cdd3ac18585  JSON receipt
```

The ITSM context receipt recognized the schema and reported `22 passed`,
`0 failed`, and `0 unknown`; the JSON sidecar matched.
