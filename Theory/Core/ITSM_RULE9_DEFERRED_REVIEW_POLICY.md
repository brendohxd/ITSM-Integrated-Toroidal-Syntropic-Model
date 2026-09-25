# Rule-9 deferred review and research continuation

Effective: 25 September 2026. Authority: the operator's explicit instruction
to defer all Rule-9 issues to later review and continue work whenever review
is the only blocker. This is an execution-policy change, not a scientific
finding or a clearance certificate.

## Scope and precedence

All outstanding Rule-9 reviews, including incomplete panels and pending
cross-role comparisons, are `DEFERRED` until the operator resumes review.
This applies to current and future results in every ITSM workstream during
the deferral. It supersedes older instructions that stop research or parent
writes solely because Rule-9 review is absent. Existing scientific decisions,
contracts, rejections, claim classifications and publication requirements
remain authoritative for their scientific content.

Keep historical receipts, mandates and partial reviewer outputs intact.
Their `NOT_CLEARED`, `NOT_COMPLETED` or similar fields remain accurate as
clearance records. Record the current scheduling decision separately as
`review_status=DEFERRED`; never rewrite those fields to manufacture clearance.
Do not launch/retry reviewers or ask for a panel merely to continue research
while this instruction is active. Local calculations and evidence preparation
can continue. Review can be resumed later without discarding partial reports.

## Decision for the proposed next step

Assess the exact result and use, rather than the entire programme in one step.

| Current evidence for the proposed use | Research execution |
|---|---|
| Required local derivation/checks are recorded, source integrity is established, assumptions/domain are explicit, and the only remaining requirement is independent review | `PROCEED_PROVISIONALLY`; record review debt and continue |
| A required equation, input, convergence result, stability condition or other substantive prerequisite is absent, failed or disputed | `HOLD_SUBSTANTIVE` for the use that requires it; continue diagnostics or an explicitly scoped conditional calculation aimed at resolving it |
| Scope, evidence or dependency compatibility has not been assessed | `ASSESS_SCOPE`; perform that local assessment, without requesting a review panel merely to do it |

A check count alone cannot establish eligibility. Read the owning report,
inspect failed/unknown checks, verify the evidence used, and state why the
proposed calculation is supported within the exact scope. A bounded negative
result may guide subsequent research; it cannot be reused as a positive
solution. An unconstrained parameter can remain symbolic where the task
permits it, but it cannot be supplied as a determined numerical prediction.

`PROCEED_PROVISIONALLY` is an execution status. It does not replace the
scientific claim labels Derived, Conditional, Open or Rejected, change a
receipt's `physics_pass`, close a gate, or certify Tier-1 readiness.

## Minimal record and dependency inheritance

Record the following alongside the result in the
[deferred-review register](../Verification/ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md)
or its owning report, and link it from the register. Do this as part of the
work; creating a new process or waiting for a reviewer is not an entry gate.

- Stable result ID, owning report, exact evidence hashes and calculation scope.
- Local validation and any substantive blockers for the proposed use; write
  `NONE_WITHIN_STATED_SCOPE` only with a reason, not because a script says PASS.
- Assumptions, domain restrictions, excluded uses and the next permitted step.
- Upstream provisional result IDs/hashes, plus unresolved questions for review.
- `review_status=DEFERRED`, `Rule9_cleared=false`, execution status and the
  existing scientific claim/gate status.

Downstream work inherits every unresolved review dependency it actually uses.
It remains provisional even if its own local checks pass. Record both direct
and inherited dependencies in the downstream report, with source hashes.
Changing an input, equation, scope or receipt requires a new version/record;
preserve the previous evidence and reassess affected dependent uses.
If a substantive flaw is found, mark affected descendants for reassessment
and stop relying on the invalid result. Keep independent work moving.

## Later review and admission

When the operator resumes review, select a coherent batch from the register,
reseal current source versions, and apply GEMINI Rule 9's independent roles,
prompt/output hashes and cross-role comparison. Prior packets remain
historical evidence and must not be silently refreshed. Record disagreements
and their resolution; review consensus alone does not supply missing physics.

Review-only delay does not prevent authoring code, notes, manuscripts or
conditional diagnostics within the approved task. Final scientific gate
closure, new canonical Derived promotion and claims of publication readiness
still require their full scientific checklists and applicable review. Actual
commit, push, publication and provider actions retain their own authority.
Do not treat the review backlog alone as proof that an otherwise completed
local task must remain unfinished; report local completion and review status
separately.

## Current application

The register applies this rule to the Master Tests 1-3 results and records the
older TOP-X4/BBN review batch as deferred. Other review-only holds are covered
by this policy immediately; add their scoped record when they are next used.
No exhaustive migration of old documents is required before research resumes.
Specific scientific dispositions and current priorities belong in the
register and dashboard, rather than in this general scheduling policy.
