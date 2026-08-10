# ITSM scientific-integrity rules

These rules apply to every agent, script, document, manuscript, and status
surface in this repository.

1. Never invent a result, parameter value, citation, derivation, or validation.
2. Never derive a coefficient by fitting or inserting the value that the
   derivation is meant to predict.
3. Keep the claim classes `Derived`, `Conditional`, `Open`, and `Rejected`
   distinct. State uncertainty and blockers directly.
4. Declare units, field conventions, normalization, sign choices, assumptions,
   and the domain of validity for every substantive calculation.
5. Run contradiction checks across executable evidence, gate reports, the claim
   ledger, manuscript text, and public status surfaces before promotion.
6. A script-level `PASS_*` means only that the script's declared checks passed.
   It is not a physics pass unless the governing gate criteria are independently
   satisfied and the canonical status document is updated in the same change.
7. Read `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md` and
   `Theory/Core/ITSM_Active_Research_Status.md` before changing scientific
   claims. The Master Research Plan remains the workflow authority.
8. An upstream downgrade reopens every downstream conclusion that depends on
   it. No observational or publication claim survives silently.
9. Do not edit frozen manuscript releases. New release work requires an explicit
   release decision after all relevant scientific and reproducibility gates pass.
10. Preserve provenance. Quarantined work may be recovered only by a scoped,
    evidence-backed re-review; commit existence is not evidence of correctness.
