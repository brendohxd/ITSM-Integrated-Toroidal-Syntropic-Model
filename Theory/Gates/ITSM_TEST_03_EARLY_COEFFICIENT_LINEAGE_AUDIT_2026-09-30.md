# Test 3: early acceleration-coefficient lineage audit

Date: 2026-09-30. Branch: `recovery/v12-core-architecture`.
Status: `HISTORICAL_TRANSCRIPTION_AUDIT_ONLY`; `physics_pass=false`,
`canonical_Test3_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`. No observed `a0` was used to select a coefficient.
The analyst has already seen the historical target and is **not blinded**.

## Scope and provenance

This is a critical-path audit of the *available Markdown transcriptions*,
not a verification of the original PDFs or a complete audit of every later
manuscript. The [master test programme](../Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md)
(SHA-256 `81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b`)
requires historical reconstruction, an independently derived `C_chi`, then
held-out observational comparison. The current [core identity](../Core/ITSM_CORE_IDENTITY_BRIEFING.md)
(SHA-256 `d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa`)
defines spatial `T^3`, not a two-dimensional doughnut picture.

| Available source transcription | SHA-256 | Relevant lines |
|---|---|---:|
| `Theory/History/FullArchive/manuscripts/01_original-dossier-2026-02-18/source.md` | `1038f4190af7bee815c2844fd5eb03b9c17e9063375cb0f0cfd0dda4d487e419` | 1-10, 22-27 |
| `Theory/History/FullArchive/manuscripts/02_v1v2v3-2026-03/v1_source.md` | `29749f54f9efcd6c8fb4733fe0c8d8449872cb6d20117655b6a8ed1026dad6f8` | 39-55 |
| `Theory/History/FullArchive/manuscripts/05_v3.6.2-2026-03-09/source.md` | `c87cc1dfcc2055afe50b87dcc50a6305da1a8de2e8b9d0ff1e6f71ecf52948a2` | 50-56 |
| `Theory/History/FullArchive/manuscripts/07_v5-line-2026-03-09/v5_source.md` | `c7a980ff17951290c0b1966ffbf5bfa1a4480fa29268a8f3c348ebecaec193fa` | 56-65 |
| `Theory/History/FullArchive/manuscripts/08_v5.7-v6.0-2026-03-09/v5.7_source.md` | `64cbc4a97169f84f60a8d665b0c71f2ce1fdd9e06d78001725e481dee52db50f` | 57-63 |
| `Theory/History/FullArchive/manuscripts/09_v6.1-v7.2-2026-03-09/v7.2_source.md` | `6069e4959dc8038d14de3c6489a7cc87f4d7acc53ed323443a63966e48730aa1` | 55-65 |

The dossier transcription names an original two-page PDF and prints that
PDF's claimed hash. The original PDF was **not** found in the repository's
historical manuscript directory during this audit. The printed PDF hash is
therefore a provenance lead, not a verified byte match. The same limitation
applies to the later original PDF versions represented by transcriptions.

## What the historical equations actually establish

1. The original dossier's code sets `H0=70*1000/3.086e22`, `chi=2*pi`,
   and then `a0=c*H0/chi`. This is an **input assignment** of `chi`, not a
   derivation from an action or periodic boundary-value problem. v1 calls
   `chi=2*pi` a toroidal geometry coefficient and repeats
   `a0=cH0/(2*pi)`; it does not add an independent matching equation.
2. v3.6.2 explicitly describes a `T^2=S^1 x S^1` universe and argues that
   a full angular circuit enforces the divisor `2*pi`. That argument is not
   a derivation on the current `T^3` manifold. Neither the number of cycles
   nor their angular coordinate convention fixes a force coefficient without
   a dynamical coupling and length/acceleration map. A historical `2*pi`
   angular factor must not be conflated with the separate, still-unproved
   `2/3` matter-force projection.
3. v5 instead prints `a0=2*pi*(cH0) ~ 1.33e-10 m/s^2`, describing `2*pi`
   as a **multiplier**. Multiplication and division differ by exactly
   `4*pi^2`. With the dossier's *declared illustrative* `H0=70 km/s/Mpc`
   and `c=3e8 m/s`, they give respectively `4.27566077287e-9` and
   `1.08303752590e-10 m/s^2`. v5 does not state an `H0` beside that
   printed value, so the arithmetic comparison is conditional on reusing
   the earlier value; it nevertheless shows that the printed number is
   **not** the value of its displayed multiplier under that declared input.
   The printed `1.33e-10` would algebraically imply
   `H0=2.17744121776 km/s/Mpc` under the multiplier, or
   `85.9619337036 km/s/Mpc` under the divisor. These are *inferred inputs*,
   not measurements or coefficient-selection evidence.
4. v5.7 restores the divisor `a0=cH0/(2*pi)` while retaining the `T^2`
   circulation explanation. This is a textual change of formula, not a
   derivation of why the divisor rather than multiplier follows from the
   current action.
5. v7.2 tries to supply an intermediate circulation chain. As transcribed,
   it defines `ell=c/H0` and `kappa=c^2/H0`, then writes
   `a0=(kappa/ell)/(2*pi)=cH0/(2*pi)`. But exact substitution gives
   `kappa/ell=c`, a **speed**, whereas `cH0` is an **acceleration**. Their
   ratio is `H0`, with dimensions of inverse time. The displayed equality
   is rejected as transcribed; an extra physical relation would be needed.
   This agrees with the earlier [historical-chain addendum](ITSM_TEST_03_HISTORICAL_CHAIN_ADDENDUM_2026-09-25.md),
   SHA-256 `0005426a448f2ff783de4e6d49bbff82c392a99c3614fdceceba4fb83bb9cd4e`.

These are **source-level classifications**, not a statistical test. No
observed acceleration value was used to rank `1`, `2*pi`, `1/(2*pi)`, or
`sqrt(1-q_dec)/(2*pi)`. The [R4C1-C1 coefficient report](RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md)
(SHA-256 `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a`)
independently shows that its homogeneous and classical linear data leave
the nonlinear force coefficient `A` free. The historical texts do not
remove that action-level degeneracy. `C_chi=NOT_DERIVED`; `a0(z)` remains
unpredicted; the Test-4 projection factor and physical Test-2 law remain
open.

## Rejection and completion boundary

Rejected **as available transcriptions**: an original-dossier first-
principles derivation merely from assigning `chi=2*pi`; v5's multiplier
with the earlier `H0=70` numerical packaging; and v7.2's printed
circulation-to-acceleration equality. This does **not** reject every
possible microscopic matching route, establish the original PDFs' exact
contents, or complete the full history. Later variants, source aliases,
original binary archives and independent blind review still need explicit
coverage. The current analyst cannot retroactively become blind to the
known coefficient. No SPARC, bTFR or lensing comparison may be used to
choose the theory coefficient before an action-derived prediction exists.

Master Tests 1-3, MAT-001, UVIR-003, Stage 4A and publication statuses are
unchanged. Pending Rule-9 review may be deferred for provisional research,
but it is not cleared and does not cure the substantive missing derivation.
