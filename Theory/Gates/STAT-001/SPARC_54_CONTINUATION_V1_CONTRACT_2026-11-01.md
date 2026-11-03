# Targeted 54-galaxy continuation — 1 November 2026

Operator approved extending suitable failed cases from 10,000 to 20,000 steps.
All 54 failures receive one controlled extension; the original passing 121 are
not rerun. Diagnostics show 51 Rhat failures and 25 ESS failures (overlapping),
with maximum Rhat 1.63066; no assumption is made that longer sampling cures all.

Reuse the exact reviewed v3 target density, priors, input bytes, 64 walkers and
four independently seeded ensembles per galaxy. Restore positions, saved log
density and MT19937 state from step 10,000; verify the restored log density.
Run 10,000 additional steps on 16 processes and retain only new incremental
blocks in a fresh directory. Do not copy or overwrite parent chains. Parent
input hashes and selected evidence hashes are checked before launch.

Analyze concatenated 20,000-step histories, discarding the original first 2,000
only. Apply unchanged Rhat<1.01, estimated ESS>=400, retained length>=50*tau,
finite positive tau criteria. Preselected walker zero from each independent
ensemble remains the diagnostic convention; interacting walkers are not treated
as independent chains. Explicitly retain every continued case and failure.
The same adaptive selection is diagnostic follow-up, not a new blind test.

The routine continuation reuses the reviewed numerical calculation at Medium.
New model/likelihood derivations require a further High confirmation. No force
law, prior, sample cut, parent action or publication status changes here.

Output: `Analysis/STAT/STAT-001/outputs/sparc_54_continue_v1_20261101/`.
Producer: `Analysis/STAT/STAT-001/sparc_continue_54_v1.py`.
Original failed/successful chains, hashes and unrelated work remain preserved.
No automatic second extension, physical promotion, commit, push or publication.
