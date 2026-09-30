# Test 3: later coefficient lineage and the v12 excitation-gap equality

Date: 2026-09-30. Branch: `recovery/v12-core-architecture`.
Status: `SOURCE_LEVEL_LINEAGE_AUDIT_ONLY`; `physics_pass=false`,
`canonical_Test3_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`. No observed acceleration or fitted Hubble value was
used to select a coefficient. The analyst knows the historical target and is
not blind. This note changes no manuscript, original archive, sidecar, gate
report, or prior result.

## Scope and pinned evidence

This extends the [early-lineage audit](ITSM_TEST_03_EARLY_COEFFICIENT_LINEAGE_AUDIT_2026-09-30.md)
and [original-PDF v7.2/v11.1.1 comparison](ITSM_TEST_03_ORIGINAL_PDF_CIRCULATION_CROSSCHECK_2026-09-30.md)
to selected *later* texts. It is an equation-level check of the pinpoints
below, **not** a review of every one of the inventory's 444 text sources,
original PDFs for every version, or an independent blinded derivation.
Historical `source.md` entries remain transcriptions rather than authenticated
original manuscripts.

| Source, current raw SHA-256 | Inspected lines | Relevant statement |
|---|---:|---|
| `Theory/History/FullArchive/manuscripts/15_v7.21-2026-03-16/source.md` — `bf8cd8a88fc4e41a3889c8a7ac127522b6d4b1184ca5cc811b1a678eba1776e2` | 57-63 | Repeats `kappa/ell/(2*pi)=cH0/(2*pi)` after the same `kappa`, `ell` definitions. |
| `Theory/History/FullArchive/manuscripts/17_v8.0.7-2026-03-20/source.md` — `ff0c51f049a1554838e0125b48d40c53c847d21595fdcfba9f8ba527fd770996` | 49-55, 85 | Repeats the invalid ratio, relabels it `a0(z)`, and supplies no action-derived `H(z)` in the inspected extraction. |
| `Manuscript/ITSM_Core_Cosmology_v11.4.1.md` — `63a86883af23935bd3ff0904f7300291732b9051073d57aa03bb9a62e146bf7c` | 153-161 | Explicitly moves away from the loose `kappa/ell` argument and calls the `2*pi` assignment a *strict geometric postulate*. Its Markdown extraction drops some displayed equations; it is not treated as a complete original equation source. |
| `Manuscript/ITSM_Core_Cosmology_v12.0.tex` — `578afdb543039e69828c836d7b8578bf0d12a0e12f71216ad911738ff79188b6` | 206-211, 233-237 | States the same postulate, and separately prints the topological-gap equality tested below. The [core identity](../Core/ITSM_CORE_IDENTITY_BRIEFING.md) lists this as the official v12.0 core manuscript, but the current gate ledger outranks legacy Derived language. |
| `papers/P1-Scale-Matching-Reconstruction/main.tex` — `5597cb6eeeb5b70c6264eb606c78f95319ace9c31dd2ea4fd58cc1a27228b1d4` | 198-268, 483-505 | Already distinguishes genuine phase-winding quantization from `cL`, rejects the geometric `2*pi` derivation and retains `a0=cH0/(2*pi)` only as a present-epoch phenomenological postulate. |

The existing [lexical inventory](../../Analysis/MasterTests/outputs/acceleration_history_inventory.json)
records 444 text sources, 274 unique byte contents, 170 sources with `a0`
token hits and 1,860 hit windows. Those are **search counts**, not 1,860
derivations or certified complete historical coverage; PDFs/Word files were
not parsed by that inventory. Its reported `physics_pass=false` is retained.

## A separate exact v12 algebra check

The current v12.0 TeX at line 233 defines `R_H=c/H0`. Lines 235-236 print

```text
Delta E_topo ≈ hbar*c/R_H = hbar*H0/(2*pi).
```

For nonzero `H0`, direct substitution instead gives

```text
hbar*c/(c/H0) = hbar*H0,
[hbar*c/R_H] / [hbar*H0/(2*pi)] = 2*pi.
```

The printed last equality would require `R_H=2*pi*c/H0`, contrary to its
declared `R_H=c/H0`. This is a **factor-of-`2*pi` algebra inconsistency in
that displayed gap equation**, not a numerical measurement of a gap and not
a general no-go for topological excitation spectra. An independently
specified mode spectrum and physical period might yield some `2*pi` factor,
but the printed chain does not establish it. The inconsistency is distinct
from the already rejected v7.2/v11.1.1 `kappa/ell` acceleration equality.

The v11.4/v12 section's own word *postulate* is the crucial classification:
even if its printed value has acceleration units, naming a topological
angular range does not derive a matter-force coefficient. The later P1 note
already records the coordinate and circulation objections. The conditional
R4C1-C1 report supplies a further physical nonidentifiability control:
at fixed `T^3` and homogeneous/linear data, varying its independent
`-A Y^(3/2)` coupling changes the conditional force scale.

## Hash-only companion provenance boundary

The current `Manuscript/ITSM_Core_Cosmology_v12.0.tex.sha256` contains only
`a9b1b5cdb9e70bf20eeaf2eb28668183623ade56a2484a67c4f1c6f1ab85ba61`.
It has no target basename and **does not equal** the current TeX byte digest
`578afdb543039e69828c836d7b8578bf0d12a0e12f71216ad911738ff79188b6`.
Both files have no tracked working-tree modifications; `git log -1 --` places
their last touch in the same `7da0e9a` commit of 2026-08-30. The separate
[legacy pair audit](../Verification/ITSM_LEGACY_SHA256_PAIR_AUDIT_2026-09-30.md)
counts 18 mismatches **only among conventional `digest  basename` pairs**
and expressly leaves 96 other formats unclassified. This hash-only case is
outside that count; it is not a newly discovered nineteenth *conventional*
pair, nor evidence of when, why, or by whom the bytes diverged. The current
TeX content is cited above by its computed raw-byte SHA-256 and Git history,
**not** as validated by the hash-only companion. Both originals are preserved.

## Decision

The inspected lineage offers no independently action-derived `C_chi`:
v7.21/v8 repeat the speed-versus-acceleration error; v11.4/v12 explicitly
replace it with a postulate; and P1 already treats that value as conditional.
The newly checked v12 gap equality has its own `2*pi` mismatch. This does
not certify that *every* historical equation was found, reject a future
microscopic matching route, or make the present analyst blind. Complete
historical source coverage, action/force closure, a unique target-independent
coefficient and held-out comparison remain required. Master Tests 1-3,
MAT-001, UVIR-003, Stage 4A and publication holds remain unchanged;
`K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, and Rule-9 review is deferred, not cleared.
