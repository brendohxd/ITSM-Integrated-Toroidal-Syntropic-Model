# Cheap-screen route activation — U3, M4, U5–U7

**Date:** 2026-09-04  
**Document ID:** `ITSM-RT-2026-009`  
**Branch:** `recovery/v12-core-architecture`  
**Decision:** `ACTIVATE_CHEAP_SCREENS_ONLY`  
**Expensive lane:** unchanged PKM1 A0–A6 parent test  
**Physics pass:** `false`  
**Commit/push/publication:** not authorized by this file  
**Authority:** subordinate to `GEMINI.md`, `active_research.md`, the Core
Identity Briefing, `ITSM_Ban_List_Reassessment_and_Frontier_Policy.md`
(corrected 2026-09-01), `ITSM_Tier1_Route_Test_Programme.md`, and
`ITSM_PKM1_BROAD_ROUTE_DECISION_2026-08-25.md`

> [!CAUTION]
> This activation does not compute \(V\), derive \(K_Q\), reopen Stage 4A,
> clear MAT-001 or UVIR-003, import \(a_0\), or touch SPARC. A cheap-screen
> `PASS_*` is bounded evidence, not a gate pass.

## 1. Why now

The 2026-09-01 frontier policy separates a **research topic** from a **banned
claim formulation**. Track-B (U3) and direct residue (M4) were already in the
route catalogue as Open alternatives if Track-A/PKM1 stalls. They were not
activated as cheap screens after the 25 August PKM1-P0 hold.

PKM1 remains the only expensive microscopic lane. These screens run in
parallel, share kill criteria A0–A2 (U3/M4/U5/U7) or A0–A2 only (U6), and
cannot borrow a coefficient from PKM1 or from each other.

## 2. Binding baseline (unchanged)

| Item | Status |
|---|---|
| MAT-001 | `BLOCKED` |
| UVIR-003 | `IN_PROGRESS` |
| \(V\) | `NOT_COMPUTED` |
| \(K_Q\) | `NOT_DERIVED` |
| PKM1 | `OPEN_RESEARCH_CANDIDATE`; P0-A rejected; P0-B `HOLD` |
| SPARC / DISK / STAT / COS | methods/comparator only |
| \(a_0=cH_0/2\pi\) | not derived |

## 3. Lane discipline

| Lane | Route IDs | Allowed work | Forbidden |
|---|---|---|---|
| Expensive | PKM1 A0–A6 | Parent Hamiltonian, Dirac count, characteristics, cutoff, source response | Phenomenology, SPARC, publication |
| Cheap screen | U3, M4, U5, U6, U7 | Named operator, DOF/rank, IR-law delta, residue identity or no-go | New live action, gate promotion, imported MOND/\(a_0\) |

At most one additional expensive microscopic route may be opened later, and
only after a cheap screen produces a signed architecture decision. U6 is not
that route until A0–A2 survive.

## 4. U3 — Track-B analytic completion (cheap control)

**Catalogue home:** `ITSM_Tier1_Route_Test_Programme.md` §7.1 U3;
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md`.

**Question.** Can a declared smooth completion of \(Y^{3/2}\) support a
homogeneous force-sector 2-to-2 calculation without pretending it is still
the exact deep-IR square-root branch?

**Declared controls (not live IR):**

- B1: \(F_{B1}(Y)=(Y+\sigma^2)^{3/2}-\sigma^3\). Analytic; generates a linear
  \(Y\) term; **changes** the exact square-root branch. Adverse control.
- B2: \(F_{B2}(Y)=(Y+\sigma^2)^{3/2}-\sigma^3-(3/2)\sigma Y\). Analytic; no
  canonical \(Y\) term; leading zero-background interaction quartic in
  spatial gradients. Homogeneous-amplitude control.

\(\sigma>0\) is an explicit crossover. It is not derived from the condensate.

**Cheap-screen deliverable.**

1. A0: identity map — Track-B is a force-operator completion, not a new
   condensate, not PKM1, not AQUAL.
2. A1: write \(F_{B1}\) and \(F_{B2}\) with dimensions, \(\sigma\) provenance
   (`CONTROL_SCALE_NOT_DERIVED`), and the exact IR-law replacement.
3. A2: DOF unchanged from the declared Track-A force host unless an extra
   field is introduced; if one is, stop.
4. State whether a homogeneous 2-to-2 exists for B2, and that B1 is not the
   live deep-IR law.

**Pass (screen only):** both controls written, IR-law delta explicit, no
chart smuggling of \(\sigma\to a_0\).

**Kill / freeze:** smoothing used to manufacture vertices while claiming the
exact \(Y^{3/2}\) law; \(\sigma\) fitted to SPARC or \(a_0\); Track-B adopted
as canonical IR without an architecture decision.

**Must not claim:** cutoff, optical theorem, MAT residue, or UVIR closure.

## 5. M4 — direct on-shell residue (cheap identity)

**Catalogue home:** programme §7.2 M4; H1.3 parent-action audit
`Theory/Gates/MAT-001/MAT-001_PARENT_ACTION_H13.md`
(`INCOMPLETE_NO_Z_phi_g_phi_FROM_DECLARED_SOURCES`).

**Question.** On a frozen parent or control, is there a field-redefinition
invariant matter-to-physical-mode pole residue that does **not** assign bare
\(K_Q\)?

**Declared targets, in order:**

1. Live Track-A chart as declared. Honest expected result: incomplete, same
   as H1.3, unless a new off-shell source appears. Do not invent \(Z_\phi\).
2. PKM1-P0-B stability-first **control**
   \(\mu=y/(1+y)\), \(J=-2a_0^2[y-\ln(1+y)]\). Residue, if any, is
   control-chart data. \(a_0\) here is an input of the designed \(J\), not a
   derivation.

**Cheap-screen deliverable.**

1. A0: residue identity vs bare \(C_m/\sqrt{K_Q}\).
2. A1: named action/control and matter vertex.
3. A2: constraints eliminated before the pole is read.
4. Signed residue or a reproducible incompleteness/no-go.

**Pass (screen only):** invariant residue computed **or** incompleteness
reproduced with the missing source named.

**Kill / freeze:** chart-dependent number called observable; pre-projection
\(1/f\) called \(V\); \(K_Q\) assigned by hand; SPARC used to normalize.

**Must not claim:** MAT-001 pass, \(V\) computed, Stage 4A reopen.

## 6. U5 — covariant phase-space rewrite of frozen PKM1-P0

**New method route.** Same parent as
`ITSM_PKM1_P0_PARENT_DECISION_2026-08-25.md`. No new field content.

**Question.** Does the P0 Dirac/ADM rank survive a covariant phase-space /
presymplectic rewrite that does not use a 3+1 split to invent constraints?

**Cheap-screen deliverable.** Presymplectic current from the frozen P0
Lagrangian; on-shell DOF count; comparison with the existing ADM count;
statement whether any rank loss is split-artefact or parent-sick.

**Pass (screen only):** both counts written and compared.

**Kill / freeze:** new kinetic term inserted to “fix” rank; MOND operator
imported into the symplectic potential.

## 7. U6 — Cartan / teleparallel host screen

**New action-class screen, not an expensive lane.**

**Question.** If the PKM1 identity (condensate phase defines the preferred
foliation; matter couples to one metric/tetrad) is hosted by a tetrad plus
Weitzenböck/teleparallel connection instead of a metric kinetic \(J(Y)\),
does A0–A2 stay healthy?

**Cheap-screen deliverable.** A0 identity map (torsion as host, not a new
fifth force); A1 covariant action or an explicit declaration that none exists
yet; A2 DOF vs GR + condensate. Stop at A2.

**Pass (screen only):** host written or incompleteness named.

**Kill / freeze:** torsion used as a slogan without an action; Einstein–Cartan
spin-torsion mixed in without spin sources; second expensive parent opened
without a signed decision.

U6 may become an expensive lane only after this screen and a new dated
decision. It does not replace PKM1.

## 8. U7 — truncated \(T^3\) Fourier / difference parent

**New method route** on the P0-B control, circle-first.

**Question.** On a periodic 3-torus with a finite Fourier or second-difference
operator, is the P0-B constraint/kinetic rank visible before the continuum
variational derivative is taken?

**Cheap-screen deliverable.** Mode truncation \(N\) declared; difference or
spectral kinetic block; rank vs \(N\); continuum comparison. No galactic
source fit.

**Pass (screen only):** rank table for at least two truncations.

**Kill / freeze:** \(L=c/H\) or \(2\pi\) inserted to hit \(a_0\); winding
count used as a coupling; continuum limit claimed from one mode.

## 9. Shared firewall

- Identity first: five pillars remain condensate, excitations, \(T^3\),
  circulation, reservoir. A screen that silently drops one is A0-fail.
- No imported \(a_0\), \(C_{\rm obs}\), \(H_0\), \(13/12\), SPARC \(\chi^2\).
- Designed \(J(Y)\) stays labelled designed.
- Cheap-screen output cannot unlock SCR, LEN, DISK, STAT, COS, or
  publication.
- Log every start/stop in `Theory/Gates/RECOVERY_SESSION_WORKLOG.md`.
- Rule 9 consensus cannot overrule a failed parent checklist.

## 10. Execution order

1. Keep PKM1 A0–A6 as the expensive job.
2. Run U5 first (method rewrite of the frozen parent; cheapest information
   on whether the hold is 3+1 bookkeeping).
3. Run M4 on P0-B in parallel with U5 (residue identity).
4. Run U3 B1/B2 as UVIR operator controls, not as a MAT parent.
5. Run U7 only if U5 still shows a continuum-rank obstruction.
6. Run U6 only as A0–A2 if the metric host itself is the named obstruction.

## 11. Status this file does not change

MAT-001 `BLOCKED`. UVIR-003 `IN_PROGRESS`. PKM1 P0-B `HOLD`. No canonical
action replacement. No website, manuscript, or Zenodo update.
