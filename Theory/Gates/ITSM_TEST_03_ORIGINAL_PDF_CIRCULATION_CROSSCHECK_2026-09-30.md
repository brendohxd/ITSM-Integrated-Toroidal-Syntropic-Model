# Test 3: original-PDF v7.2 / v11.1.1 circulation cross-check

Date: 2026-09-30. Branch: `recovery/v12-core-architecture`.
Status: `SOURCE_LEVEL_REJECTION_OF_DISPLAYED_CHAIN`; `physics_pass=false`,
`canonical_Test3_pass=false`, `Test2_physics_pass=false`, `gate_effect=NONE`,
`Rule9_cleared=false`, `review_status=DEFERRED`. The analyst is **not blind**
to the historical target. No observed `a0`, SPARC, bTFR or lensing value was
used to select a coefficient.

## Primary sources and provenance boundary

Both manuscript PDFs underlying the archived Markdown transcriptions were
located in the adjacent private `MISC ITSM` archive and read in full (8 and
34 pages, respectively); the critical equations were also visually inspected
on rendered pages. Neither PDF was edited. The filenames, archived extraction
paths, and PDF metadata support their version identity, but no independent
publisher-signed hash authenticates them. The v11.1.1 TeX is a corroborating
source, not proof that a particular PDF was built byte-for-byte from it.

| Original source | SHA-256 | Pinpoints |
|---|---|---|
| `MISC ITSM/📝 Drafts/2026-04/ITSM_V7.2_Relativistic_Field_Equations.pdf` | `ec37735cb3523acc48c8a4768093c5a517217703337a843a235df9a5b2def70d` | pp. 2-3: `T^3`, circulation, action and paired divergence; pp. 5-7: growth, wake and appendices |
| `MISC ITSM/💾 Backups/ITSM_Backup_20260627_184507/Manuscript/ITSM_Core_Cosmology_v11.1.1.pdf` | `25678f36450a9df9482a14c798f0eae143dc1cf04652251bd930257a9ed799ee` | p. 5: circulation, two-scale quantum; p. 7: equality claim; pp. 11-12: weak-field reduction |
| Same backup's `ITSM_Core_Cosmology_v11.1.1.tex` | `c94557b5cc1ad07b467d7a1b617932f10fbbf7a9550d5dec85e885b96dfb3d5c` | lines 165-188 and 245-251 reproduce the relevant equations/claims |

The earlier [transcription-only audit](ITSM_TEST_03_EARLY_COEFFICIENT_LINEAGE_AUDIT_2026-09-30.md)
and [historical-chain addendum](ITSM_TEST_03_HISTORICAL_CHAIN_ADDENDUM_2026-09-25.md)
correctly marked the original PDF **unverified at the time**. This addendum
supersedes that *provenance limitation for v7.2 and v11.1.1 only*. It does not
establish completeness of the full manuscript lineage, verify other originals,
or upgrade the historical theory's claims.

## What v7.2 contributed, and what v11.1.1 changed

The operator recalls v7.2 being chosen after a historical search for work
lost along the way. The original PDF supports treating it as an important
**starting document**: it introduces explicit spatial `T^3` language and
contains candidate growth, wake-density, gravitational-slip and exponential
rotation-curve formulae. v11.1.1 retains the `T^3` and matter/plenum-exchange
programme, but its specific force action and some observational claims change;
the named v7.2 formulae are not reproduced as such. The historical choice of
a starting point is not a signed scientific gate decision. The earlier v7.1
EFE/lensing route, separately flagged in the master research plan, must not
be overlooked by a v7.2-only recovery.

| Thread | v7.2 original PDF | v11.1.1 original PDF | Current use |
|---|---|---|---|
| Topology | `T^3` explicit, p. 2 | retained and stronger uniqueness claims, pp. 3-4 | `T^3` remains the current postulate; flatness alone does not select it |
| `a0` | `kappa=c^2/H0`, `ell=c/H0`, then `kappa/(2 pi ell)=cH0/(2 pi)`, pp. 2-3 | the same chain, p. 5 | **Rejected as displayed algebra**, not a rejection of winding research |
| Matter/plenum exchange | paired divergences `Q^nu`, p. 3; no source-generating matter interaction varied | adds `Q^nu=kappa Theta u^nu`, p. 9; no complete action-level origin | Test 1 remains open; Bianchi balance is necessary but not sufficient |
| Weak-field | interpolation and an appendix exponential comparator, pp. 4, 6 | Born-Infeld-type plenum action and claimed square-root reduction, pp. 8, 11-12 | Test 2 remains open; see exact check below |
| Other seeds | growth power law, wake-density formula, slip and SPARC protocols, pp. 5-7 | more elaborate cosmology/cluster claims, but not those specific displayed formulae | candidates for fresh derivation only; no observational validation inherited |

### A. The original-PDF coefficient chain is not an acceleration derivation

Both PDFs define `kappa=c^2/H0` and `ell=c/H0`, with circulation dimensions
`[kappa]=L^2/T` and `[ell]=L`. Therefore

```text
kappa/(2*pi*ell) = (c^2/H0)/(2*pi*c/H0) = c/(2*pi),
```

which has dimensions of **speed**. Their next displayed member,
`cH0/(2*pi)`, has dimensions of **acceleration**. The intermediate printed
`c^2/(2*pi*ell)` silently substitutes `c^2` for the defined `c^2/H0`.
The missing factor is `H0`. Replacing the historical equation with a new
relation may be a research route, but is not a repair derivable from these
pages. A period convention or cycle count alone cannot supply a physical
force coupling or fix `C_chi`.

### B. v11.1.1's two-scale circulation statements conflict

On p. 5, v11.1.1 states `kappa_OF=h/m`, `kappa_cosmo=c^2/H0`, and a ratio
`n=kappa_cosmo/kappa_OF≈10^10` for `m≈10^-22 eV/c^2`. On p. 7 it instead
sets `kappa_OF=kappa_cosmo`, implying `n=1` and a different mass
`m=hH0/c^2`. These cannot both be the same selected model point.

With **illustrative** `H0=70 km s^-1 Mpc^-1`, SI `c` and `h`, and the stated
`m=10^-22 eV/c^2` (interpreting the manuscript's `eV` mass in natural units),
the declared formulae give:

```text
kappa_OF       = 3.71695e24 m^2/s,
kappa_cosmo    = 3.96181e34 m^2/s,
kappa_cosmo/kappa_OF = 1.06588e10,
mass required for equality = 9.38195e-33 eV/c^2.
```

Thus its dimensionless ratio is approximately consistent **only if the two
quanta remain distinct**. Its separately printed magnitudes `10^-3 m^2/s`
and `10^39 m^2/s` are not SI evaluations of the stated formulae; their
ratio would be `10^42`, not `10^10`. No observed `a0` enters this check.

### C. The later weak-field action does not close the claimed bridge

v11.1.1 pp. 11-12 gives, for `q=|grad phi|>0`, `X=q^2/2`,

```text
L_X/M_P^2 = 1 + 1/[3 sqrt(1+q^2/(2 a0^2))],
(L_X/M_P^2) q = g_bar.
```

The bracket lies strictly between `1` and `4/3` for finite `q>0`, with
`4/3` as `q→0`. Hence `3 g_bar/4 < q < g_bar`, and in the low-gradient
limit `q=(3/4)g_bar+o(g_bar)`. The displayed equation cannot yield the next
line's `q≈sqrt(g_bar/a0)`: its source/response is linear, not quadratic, in
that limit. This is an algebraic check of the printed reduction only; it does
not rule out a different action or matching sector producing a square-root
law. The parent [core identity](../Core/ITSM_CORE_IDENTITY_BRIEFING.md)
already records UVIR-001 as `CLOSED NEGATIVE` for the direct Born-Infeld
route. No new Test-2 gate status is asserted here.

## Reproduction and decision boundary

`Analysis/MasterTests/test_03_original_pdf_comparison.py` (SHA-256
`769bf9976a15a407851a57e10185d63b23ba9ad61da7bb61ce7dc4a68278d855`)
is an **in-memory, stdout-only** replay. Run it with `--v72-pdf` and
`--v111-pdf` pointing to the two originals above. It first checks their exact
SHA-256 bytes, then independently evaluates the manually transcribed algebra,
limits and illustrative SI conversion. It does not parse PDF equations,
write/overwrite a receipt, edit a sidecar, or create a blind analyst.
The 2026-09-30 run returned `local_validation=PASS`, `13/13` checks,
`source_integrity_verified=true`, **`physics_pass=false`**,
`C_chi=NOT_DERIVED`, `Test2_physics_pass=false`, and `gate_effect=NONE`.
A negative-control run with the two PDF arguments swapped reported
`source_integrity_verified=false` and stopped before the algebra checks.

The v7.2 manuscript is retained as a historically valuable candidate map,
not as a Derived parent. The *displayed* v7.2/v11.1.1 coefficient chain,
v11.1.1 simultaneous `n≈10^10` and `n=1` claims, and v11.1.1 displayed
Born-Infeld weak-field square-root inference are **Rejected as written**.
This does not reject `T^3`, microscopic winding, or an alternate action-level
matching route. Before Test 3 can pass, the full historical equation inventory,
an independently blinded derivation of a unique `C_chi`, an action-derived
background `H(z)`/`q_dec(z)`, and only then held-out observational tests are
still required. Test 1 and Test 2 action/matter-coupling prerequisites remain
substantive blockers. Master Tests 1-3, MAT-001, UVIR-003, Stage 4A and
publication statuses are unchanged; deferred Rule-9 review is not clearance.
