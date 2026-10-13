# Concept-led website update — 14 October 2026

Operator request: update itsm-cosmology.com carefully, with a clear concept,
vision and aim, without making governance the primary reader experience.
This is a website presentation update, not a scientific gate promotion.

## Reading structure

- Home introduces the active-vacuum proposal, defines Integrated / Toroidal /
  Syntropic, explains the aims and gives three plain-language progress items.
- Vision explains the hypothesis, intended tests and success criteria.
- The model explains the ingredients before offering a collapsible technical
  action inventory. T³ means three periodic spatial identifications, not an
  embedded doughnut; existing background art is explicitly illustrative.
- Progress summarizes the bounded dust milestone, the unresolved physical
  validity/GR window and the missing identifying matching inputs.
- Papers links the current P1/P2 v0.2.0-rc3, thermodynamics
  v0.7.1-conditional-draft and R4C1 v0.1.1-conditional-draft PDFs. Working and
  authority core PDFs remain distinct; unavailable legacy P3/P4 PDF links are
  removed. Draft availability is not journal or publication clearance.
- Evidence retains the technical claim matrix and exact canonical holds.
- Reproduce leads with a named-revision integrity check and a read-only replay,
  rather than commands that could regenerate historical output directories.

Primary navigation is Vision / The model / Progress / Papers / Evidence.
Reproduction, source and contact links remain available in the footer.

## Evidence basis and unchanged scientific boundary

The public progress summary uses the
[13 October research checkpoint](../Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-13.md),
the linked owning reports, core identity and current research dashboard.
Bounded linear prepared-dust research acceptance is not canonical dust
clearance. No family is admitted to a physical GO domain. Numerical Stage 3
has not been entered. RM1/ST1/ST2 are separate declared mechanism controls.

K_Q=NOT_DERIVED; V=NOT_COMPUTED; MAT-001=BLOCKED;
UVIR-003=IN_PROGRESS; Stage4A=CLOSED; physics_pass=false; gate_effect=NONE.
Rule-9 remains DEFERRED and Rule9_cleared=false. No new independent review,
microscopic parent selection, observational fit or paper submission occurred.

Original manuscripts, scientific scripts, receipts and sidecars are untouched.
The previous 1,061-file/441-source-pin checkpoint passed a fresh WORKTREE
integrity check. Historical website content remains in Git history; the dated
13 October docs README and sealed research manifest are not rewritten.

## Website verification

- `python -B Scripts/site/check_public_site.py`: PASS_WEBSITE_SOURCE_ONLY;
  seven pages, 207 references, six public PDF targets, no failures.
- The checker verifies local assets/fragments, publication of repository file
  targets, retained PDF naming, navigation, basic document structure, private
  path exclusion, manifest JSON and the explicit canonical boundaries.
- `node --check docs/sw.js`: exit 0.
- Browser QA: all seven pages checked at the normal desktop viewport and a
  390-by-844 phone-sized override; no document-level horizontal overflow.
- Desktop and mobile home/paper layouts visually inspected. The model's native
  technical disclosure expands and displays its action. Browser error log empty.
- Removed initial content-fade animation for immediately readable text and
  strengthened mobile background contrast after inspecting the preview.
- The stylesheet query and service-worker cache are versioned for this update;
  cache cleanup is restricted to older ITSM cache names.
- `git diff --check`: exit 0. Website text normalization is separate from the
  untouched sealed scientific evidence.

Preview serves only public `docs/` on 127.0.0.1, not the repository or vault.
No firewall, DNS, credentials, hosting platform or audience changes are made.

## Publishing and rollback

The existing `.github/workflows/pages.yml` is manual-dispatch GitHub Pages,
uploading only `docs/` from the selected revision. An ordinary push does not
deploy the website. Publication requires dispatch of the website commit and
verification of the successful run and live content.

This source note records preparation and checks; it is not itself a deployment
success receipt. Deployment confirmation is supplied by the workflow result
and the live verification at handoff.

Previous successful Pages run: 36184635013, source commit
`8a292769433b3743c17fa2239423a20c8ea39b32`. The pre-update repository base is
`fb5a5c0abe07c5a48de8be6f612b65c8d1f39721`. Git history preserves both rollback
references. No automatic rollback, amend, force-push or workflow change.
