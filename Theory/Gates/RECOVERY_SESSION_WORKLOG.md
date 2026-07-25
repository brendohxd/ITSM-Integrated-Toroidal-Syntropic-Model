# Recovery branch session worklog

Append-only log of tactical decisions during autonomous work sessions on the
v12 core recovery program: routes tried, routes abandoned or overwritten, and
why. Purpose: nothing gets silently dropped or replaced without a record the
user can review later. Every entry stays even if a later entry supersedes it —
do not delete or rewrite past entries; add a new one that references the old.

Format per entry: date, gate, what changed, why, what (if anything) was
abandoned or superseded.

---

## 2026-07-24 — UVIR-003 causality addendum opened

Gate: UVIR-003 (Stage A)

Started a causality check on the Stage-A regulated force dispersion relation
in response to the user's request to build on the recovery branch using the
historical archive as a source of routes, specifically following up on the
archive's flagged `c_s^2~1.11` superluminality concern. Produced:
`Theory/Gates/UVIR-003/UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md`,
`Analysis/UVIR/UVIR-003/uvir003_causality_check.py`, one new row in
`Theory/Core/ITSM_Claim_Migration_Ledger.csv`.

Finding: dispersion is superluminal both at long wavelength (`k->0`, if
background gradient `q` exceeds `K_Q/(3A(1+cos^2 theta))`) and at short
wavelength (`k->infinity`, unbounded, for every positive `K_Q,A,gamma`).
Nothing abandoned — this is new work, not a revision.

## 2026-07-24 — Correction: long-wavelength check is not closeable "once K_Q is fixed"

Gate: UVIR-003 (Stage A causality addendum)

**What changed:** the addendum's original Section 1 and its recommendation
said the long-wavelength superluminality question "does not require the
Stage B strong-coupling calculation to resolve" and was "closeable now, in
principle, once K_Q is fixed relative to A" — implying fixing K_Q was a free
normalization choice. Checked this against `Theory/Core/ITSM_Core_Architecture.md`
Section 3.4/4/5 directly rather than trusting the earlier framing.

**Why it changed:** Core Architecture normalizes the force scalar via
`Y = h^{mu nu} nabla_mu psi nabla_nu psi / a0^2` and gives
`L_IR = -(2 C_IR/3) M_P^2 a0^2 Y^(3/2)`, which fixes `A = C_IR/(12 pi G a0)`
in Stage A's unnormalized convention (verified this reduces to the Stage-A
`A` exactly, using `M_P^2=1/(8 pi G)`). `C_IR` at least has a tentative
candidate value (the `2/3` geometric-projection matching hypothesis, itself
only Conditional per the ledger). But `K_Q` — the coefficient of the `Q^2`
term, `Q=U^mu nabla_mu psi` — appears **nowhere else** in the architecture:
not in the static weak-field Lagrangian (Section 5, which drops time
derivatives entirely), not in any matching relation, not even as a
tentative guess. A field redefinition `psi -> psi/sqrt(K_Q)` can always
absorb `K_Q`'s literal numerical value into redefinitions of `A`, `gamma`,
and the background `q` — so "fixing K_Q" in isolation is not a meaningful,
free choice; what actually needs deriving is the physical, redefinition-
invariant combination `3Aq(1+cos^2 theta)/K_Q` in psi's true physical
normalization, and that requires an independent matching condition for
`K_Q` that presently does not exist anywhere in the theory (most likely
this has to come from the same UV-completion / matter-coupling work that
MAT-001 is supposed to do for `C_IR`, `C_m` — MAT-001 is itself blocked on
UVIR-003).

**What this supersedes:** the claim in
`UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md` that the long-wavelength check
"does not wait on a strong-coupling calculation" and is closeable "once K_Q
is fixed relative to A" is corrected below (Section 1 rewritten in place,
with this worklog entry as the record of the original, weaker claim and why
it was wrong). The two-regime structure of the finding (long-wavelength vs
short-wavelength) is NOT abandoned — it still stands and is still correct;
only the claim about how easily the long-wavelength half closes is revised.
Ledger row for this claim also updated to match.

## 2026-07-24 — Aether-sector mode speeds via literature substitution (Stage B, frame only)

Gate: UVIR-003 (Stage B, frame/aether sector only — force sector not touched)

Fetched the Eling-Jacobson-Mattingly Einstein-aether review (arXiv:gr-qc/0410001,
already cited in `UVIR-003_STAGE_A_REPORT.md` Section 1.3) to get literature-
verified coupled metric+aether mode speeds (spin-0/1/2), rather than trust
memory of the formulas — the Stage-A report itself warns sign/normalization
conventions differ across papers. Confirmed via an explicit sympy check
(`Analysis/UVIR/UVIR-003/uvir003_frame_sector_speeds.py`) that Stage-A's
`c1,c2,c3,c4` map identically (no relabeling) to EJM's, because the frame
action's declared extra minus sign on the `c4` term exactly cancels the sign
flip induced by the signature difference (mostly-minus vs mostly-plus).

**Bug caught before trusting the result:** the first version of the
consistency check (verifying EJM's exact formulas reduce to Stage-A's
decoupled `c1/c14`, `c123/c14` ratios in the weak-metric-coupling limit)
scaled only `c1,c3 -> eps*c1,eps*c3` while leaving `c2,c4` at O(1). This
failed the assertion (correctly — the script raised rather than silently
passing). EJM's text specifies the reduction holds "for c_i small compared
to unity" — i.e. all four `c_i` scaled together. Fixed by scaling
`c1,c2,c3,c4 -> eps*(...)` uniformly; the corrected limit passes and matches
Stage A's decoupled speeds exactly. Nothing about the underlying physics
claim was wrong — the bug was in how the limit was taken to check it. Logged
here per the instruction to record tactic changes, even ones this small,
so a later reviewer doesn't have to guess whether the first failing run
indicated a real problem with the substitution itself.

## 2026-07-24 — Force-sector longitudinal IR NDA estimate

Gate: UVIR-003 (Stage B item 9, partial)

Estimated one NDA derivative scale for the force sector's nonanalytic cubic
operator, following the method precedent already set by
`UVIR-001_GATE_REPORT.md` Section 7 (canonical-normalize, read the scale off
the cubic vertex). Initially considered doing this fully — all three spatial
directions plus the k^4-dominated regime above `k_cross` — but the
anisotropic Hessian (diag(6Aq,3Aq,3Aq)) makes a fully rigorous coordinate
rescaling delicate (the volume element and field normalization mix under an
anisotropic spatial rescaling in a way that isn't a quick generalization of
UVIR-001's single-scalar-invariant case), and the k^4-dominated regime has
different (Lifshitz, z=2) scaling entirely.

**Decision:** scoped down to the longitudinal direction only (largest
quadratic coefficient, most conservative choice) and the k^2-dominated
regime below `k_cross`, explicitly excluding the transverse directions and
the Lifshitz regime rather than force an estimate that would silently paper
over those complications. Result:
`Lambda_NDA,long^(IR) ~ K_Q^(3/4)/sqrt(A)`
(`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_STRONG_COUPLING.md`). This is a
time-normalized longitudinal derivative scale, not a completed physical EFT
cutoff. It is blocked numerically on the same missing `K_Q` matching condition
as the causality addendum's long-wavelength check; transverse normalization,
Lifshitz power counting, and the physical cutoff remain open.

## 2026-07-24 — Conditional K_Q estimate (speculative, escalates priority)

Gate: UVIR-003 (causality addendum, extension)

While looking for any existing handle on `K_Q` (which the causality addendum
found has no matching condition anywhere), found that
`UVIR-002_ROUTE_SELECTION.md` declares the temporal invariant as
`Q=U^mu nabla_mu psi/a0` (a0-normalized, same pattern as Core Architecture's
`Y` normalization). Constructed a candidate matching hypothesis by direct
analogy to how `A=C_IR/(12 pi G a0)` was fixed (same `M_P^2*a0^2`
dimensional-necessity prefactor), giving `K_Q ~ k_Q * M_P^2`. This is
explicitly NOT a derivation — no document states or implies this prefactor
choice for the temporal sector — but is a defensible dimensional analogy
given `M_P` and `a0` are the only scales the architecture declares.

Substituting `k_Q~1` (unjustified NDA guess) and `C_IR~2/3` (already only
Conditional per the ledger) gives `q_cross ~ 0.375-0.75 * a0` — i.e. the
long-wavelength causality threshold would sit *below* `a0`, inside rather
than outside the theory's core physical regime. Verified symbolically and
numerically (`uvir003_conditional_kq_estimate.py`).

**Explicitly not claiming this is a finding about the theory** — three
unconfirmed premises are stacked. Logging this prominently because it
changes the practical priority of the open `K_Q` item: it is not safely
deferrable bookkeeping, since the naive expected values land at or past the
causality edge rather than comfortably away from it. If a future pass
derives `K_Q` properly and finds `q_cross >> a0`, this speculative estimate
should be marked superseded here, not deleted — record why the naive
estimate was wrong once the real answer exists.
