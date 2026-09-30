# Local independent-review preparation: Master Tests 1-3

This workflow prepares exact evidence and mandates. It does not run a model,
assign a reviewer, claim independence, clear Rule 9, or promote any gate.
The full scientific requirement table remains in
`Theory/Gates/ITSM_TESTS_01_03_DERIVATION_DISPOSITION_2026-09-25.md`, section 6.2.

**25 September operator decision:** all Rule-9 reviews are now DEFERRED until
the operator resumes them. Apply the
[continuation policy](../Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md) and
[register](../Theory/Verification/ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md).
Locally supported work proceeds provisionally when review is its only
outstanding prerequisite. Record downstream review dependencies and keep
substantive scientific holds. Do not make panel setup a prerequisite for
ordinary research or ask again for dispatch merely to keep work moving.

**Later S1-S3 results, 25-26 September:** R9-MT1-S1, S2 and S3 are recorded
in the deferred register.
The existing preparation roster and earlier sealed snapshot contain the ten
pre-S1 receipts, not the new scalar-constraint, propagation or zero-branch artifacts.
They must not be represented as S1-S3 review. Before a future S1-S3-inclusive
review, extend the explicit roster and mandates, verify dependencies and
seal a new snapshot. This deferred packaging task does not block research.
S2 review must retain the failed attempt-01 archive and audit the corrected
Mcdot principal contribution, not just count the final passing checks.
S3 review must inspect the extra derivative requirement and distinguish its
frozen-sector graph estimate from a full coupled initial-value theorem.

## Prepare and verify

From the recovery-branch root, using the itsm_env interpreter (or its full
path if the shell alias is unavailable):

```powershell
python -B Scripts/itsm_context.py run -- python -B Scripts/tests/test_master_tests_review_packet.py
python -B Scripts/itsm_context.py run -- python -B Theory/Verification/prepare_master_tests_review.py
python -B Scripts/itsm_context.py run -- python -B Theory/Verification/prepare_master_tests_review.py --verify .local/itsm-review/master-tests-PACKET_ID --expected-manifest-sha256 TRUSTED_FULL_HASH
```

Replace PACKET_ID and TRUSTED_FULL_HASH with the actual preparation output;
they are placeholders, not commands to run verbatim. Verification is read-only.
Preparation writes only under ignored `.local/itsm-review/`. The tool checks
that this output root is ignored before writing. No Relay runtime, provider
credentials, network, model session, or automatic dispatch is used.

The explicit roster includes mandatory governance, the frozen R4C1 action,
pre-S1 owning contracts, the ten pre-S1 symbolic/numerical receipts,
their transitive source pins, the B1 trajectory, current reports, claim
ledger, execution queue and affected working manuscript sources. Scientific
artifacts require matching sidecars. Older governance/operator sources without
sidecars are explicitly labelled and hashed, never represented as signed.
Receipt checks are counted as pass/fail/unknown without hiding failures.

Prompt text includes the complete Core Identity, GEMINI rules and deferred
review policy; Role A's
Frame prompt additionally includes the complete action. Exact prompt bytes
are hashed before any prospective dispatch. Snapshot files preserve source
bytes and existing sidecars. The final manifest hashes all payload files and
is written last, followed by its own hash. A deterministic rebuild reuses
identical bytes; different existing bytes are never overwritten. Changed
sources require a new snapshot. Existing snapshots are not deleted.

An internally matching sidecar is not an authentication signature: compare
the complete manifest hash against the trusted preparation/approval record,
especially before dispatch. The verify command checks both snapshot integrity
and freshness against current source bytes and captured sidecars.

## Roles, sequencing and read-only operations

| Mandate | Permitted phase | Required output |
|---|---|---|
| A Frame: independent mathematics/dimensions | Phase 1 only, before author results | Independent derivation or precise insufficiency; exposure record |
| A Compare | Only after A Frame output is saved and hashed | Attributed differences against phase-2 evidence; preserve initial report |
| B: numerical/pipeline | Phase 2, without A/C reports initially | Independently checked residuals, convergence, pins, negative controls and executable coverage |
| C: claims/gates | Phase 2, without A/B reports initially | Requirement-level coverage and discrepancies against the authoritative ledger |

All three initial reports must be sealed before cross-role comparison.
Resolve disagreements against primary sources. A substantive discrepancy or
missing parameter needed for a proposed claim holds that affected use;
symbolic/conditional work can keep a parameter explicit. An absent review
does not impose an execution hold. The parent alone writes repository changes,
including provisional work under the deferred-review policy. A reviewer may
recommend a disposition, but cannot itself enact one.

Reviewers must not run receipt-writing main() entry points in the worktree
or snapshot. Role B can evaluate inspected pure functions/in-memory runs
using Python -B. A replay requiring file writes must be requested from the
parent and run in an isolated scratch copy, with resulting logs/data returned
and hashed. Never grant direct repository mutation just to make a review run.

The directory/mandate split is organizational, **not an enforced sandbox**.
Before dispatch, verify that each chosen runner has read-only permissions,
appropriate phase access and no inherited author/other-reviewer session.
Do not infer those guarantees from the prompt, provider name or CLI presence.
Any extra prompt text or changed source requires a new exact seal.

## Blinding and provenance limits

The complete mandatory GEMINI file already contains an example acceleration
relation. The preparation tool therefore records `target_unprimed=false`,
`independently_verified=false` and `phase_boundary_enforced=false`.
Do not weaken or omit governance to manufacture a blind label. A fresh
session is not proof of no prior exposure or independent scientific judgment.
No observed a0 or target dataset is supplied as a computational input, but
reviewers must disclose their own prior/accidental exposure. The intended
Frame-versus-Compare separation does not retroactively blind this author.

For each output, the parent must preserve reviewer/provider/model/session,
exact mandate and evidence hashes, source-access/exposure record, actual
permission constraints, findings and immediate output SHA256. Unknown fields
remain unknown. Model agreement is not journal peer review. Historical
coefficient reconstruction is still parked, not complete; prior TOP-X4/BBN
certificates are not substitutes for this review.

## Authority and current boundary

Each newly prepared snapshot initializes its own roles NOT_ASSIGNED and
dispatch NOT_PERFORMED. It does not erase earlier partial review records.
New snapshots record review_status=DEFERRED and the provisional continuation
policy, with Rule9 NOT_CLEARED, physics_pass=false and gate_effect=NONE.
Current Tests 1-3 still have substantive scientific requirements open;
review-only delay does not by itself make a completed local task incomplete.
No commit, push or publication is implied. Private packet contents and logs
must not be committed or sent to a provider without the normal authority.

When the operator resumes review, verify existing provider/model and
quota/credit authority against the proposed current snapshot and runtime;
request only missing authority. No dispatch is performed by this workflow.
Review may assess the current positive and negative results;
it cannot create the missing microscopic matching that would fix the free
physical coefficient, the full weak-field solution, or a healthy parent.
