# MAT-001 Tier-1 Remediation Addendum ? 2026-08-07

**Status:** ACTIVE ? fail-closed remediation

**Authority:** Subordinate to `Theory/Core/ITSM_Master_Research_Plan.md`,
`ITSM_Core_Architecture.md`, and `ITSM_Core_Recovery_Plan.md`

**Frozen releases:** alpha.11 and alpha.12 remain immutable

**Gate status:** UVIR-003 `IN_PROGRESS`; MAT-001 `BLOCKED`; $V$
`NOT_COMPUTED`; $K_Q$ `NOT_DERIVED`; Stage 4A `CLOSED`

## Purpose and quarantine

Repair the post-alpha.12 MAT evidence chain under a Tier-1 physics standard.
This is an execution addendum, not a competing research plan. The August 6 MAT
chain from the same-chart free-sector export through RR2/H7 is provisional
until the items below are resolved. A script-level pass certifies only its named
calculation; it cannot unlock MAT, UVIR, Stage 4A, or downstream claims.

## R1 ? ADM-to-J2 convention bridge

The declared sectors are

\[
L_{\rm ADM,z}=+z^T(M_xx+M_v\dot x)+\frac12z^TC_{\rm ADM}z,
\]

\[
L_{\rm J2,z}=-x^TBz-\frac12z^TC_{\rm J2}z.
\]

Their static terms agree only for

\[
B=-M_x^T,\qquad C_{\rm J2}=-C_{\rm ADM}.
\]

Correct the prior $B=+M_x^T$ export, add exact symbolic reconstruction checks,
regenerate the evidence, and trace every consumer. The nonzero $M_v\dot x$
block remains an obstruction and must not be erased.

**Exit:** byte-reproducible output; exact reconstruction; dependency cone
regenerated or marked stale; gate status unchanged.

## R2 ? H1.3 source-provenance audit

The current audit assigns `derives_numeric_* = False` in its own inventory and
then tests those assigned fields. Replace that circular inventory with parsed
source evidence where machine-readable and a file-and-line provenance table
where semantic review is required.

**Exit:** absence is source-supported; injected valid derivations are detected;
unreadable or unclassified sources fail closed.

## R3 ? Covariant parent matter action

The Track-A interaction $L_{\rm int}=-C_m\rho_b\psi$ is a Conditional reduced
ansatz. Its $h=(0,0)$ result is not a covariant matter-source derivation.
Specify one covariant matter action, matter variables, metric signature,
field/unit chart and conservation law. Derive lapse and shift sources by ADM
variation in the same chart as the free sector.

**Exit:** action provenance and covariance recorded; $d,h$ obtained by
variation; constraint/Bianchi consistency checked; any zero follows from the
action or a declared controlled limit.

## R4 ? Signed residue contract

Maintain signed finite $C_m$ through canonical normalization and projected
source matching. Magnitude-only diagnostics may be supplementary but cannot
satisfy a signed matching contract.

**Exit:** sign transformations are explicit; zero, non-finite, negative and
sign-flipped mutation cases behave according to the declared contract.

## Execution order

1. Repair R1 and regenerate its dependency cone.
2. Replace R2 with a source-backed audit.
3. Freeze the covariant action and conventions for R3.
4. Switch to High reasoning for the R3 variation and ADM reduction.
5. Apply R4 to the resulting canonical vertex and residue chain.
6. Run an independent Tier-1 review of the repaired bundle.
7. Only then reconsider the MAT-001 checklist.

TOP, VOR, WAK and reservoir/$Q_{\rm syn}$ work may continue in parallel as
Conditional/Open research, but cannot bypass this remediation.

## Evidence control

For each item record the source equation and convention, affected dependency
cone, reproduction command, runtime environment, deterministic rerun, negative
tests, status changes or non-changes, and reviewer disposition (`PASS_SCOPED`,
`HOLD`, or `FAIL`). No alpha freeze is justified by inventory growth alone.

## External evidence channels ? 2026-08-07

Scite and SciSpace searches identify four distinct comparison classes. These
are research anchors, not support for an ITSM claim:

- action-level superfluid phonons and baryon coupling: Berezhiani and Khoury,
  [Phys. Rev. D 92, 103510](https://doi.org/10.1103/PhysRevD.92.103510), and
  Berezhiani, Famaey and Khoury,
  [JCAP 09 (2018) 021](https://doi.org/10.1088/1475-7516/2018/09/021);
- analyticity/causality obstruction for derivative EFTs: Adams et al.,
  [JHEP 10 (2006) 014](https://doi.org/10.1088/1126-6708/2006/10/014);
- finite-density positivity beyond Lorentz-invariant vacuum assumptions:
  Creminelli, Janssen and Senatore,
  [JHEP 09 (2022) 201](https://doi.org/10.1007/JHEP09(2022)201), plus
  Chandrasekaran, Remmen and Shahbazi-Moghaddam,
  [JHEP 11 (2018) 015](https://doi.org/10.1007/JHEP11(2018)015);
- compact-topology observational bounds: Planck
  [2013 XXVI](https://doi.org/10.1051/0004-6361/201321546) and
  [2015 XVIII](https://doi.org/10.1051/0004-6361/201525829).

Wolfram independently reduced the generic ADM-to-J2 sign-bridge residual to
zero. This is an external algebra check, not repository authority. Notion
confirmed the same action gap and gate ordering but lagged the Git freeze.
Slack contained no ITSM records. Agora returned generic prose with unrelated
sources and is excluded from the physics evidence set.

## Automation work packages

| ID | Automated control | Fail-closed output |
|---|---|---|
| AUTO-00 | Run syntax checks, mutation suite, normal export twice under distinct `PYTHONHASHSEED` values | Any unequal digest fails R1 |
| AUTO-01 | Build a declared dependency graph from script input defaults, evidence `source` fields, JSON paths and checksum sidecars | Unknown or cyclic dependency is `HOLD` |
| AUTO-02 | Regenerate the R1 dependency cone in topological order and verify every sidecar | Missing/stale consumer is `HOLD` |
| AUTO-03 | Replace H1.3 booleans with source parsers plus file/line semantic attestations | Unreadable/unclassified source is `HOLD` |
| AUTO-04 | Maintain a DOI manifest with query, retrieval date, relevance and correction/retraction checks | Literature cannot directly set a physics PASS |
| AUTO-05 | Generate a convention sheet for the R3 covariant action: signature, fields, dimensions, variations, ADM chart and boundary terms | Any undeclared convention blocks variation |
| AUTO-06 | After High-reasoning derivation, run symbolic reconstruction, constraint, sign-flip and dimensional mutations | MAT remains BLOCKED on any failure |

Connector searches are deliberately not placed in CI: they are mutable external
services. CI should consume a reviewed DOI/evidence manifest and deterministic
local fixtures. A human-reviewed refresh may update that manifest, with source
dates and changed citation status recorded explicitly.

## Progress record

- R1 convention corrected: $B=-M_x^T$, $C_{\rm J2}=-C_{\rm ADM}$.
- Wolfram generic-matrix residual: zero.
- Mutation suite and two distinct Python hash seeds produce byte-identical JSON:
  `33FCD3A4AB8F8531E611DFACDD91CCB7598CF9ADE49A8279A87B5EB954D4A469`.
- Reproduction runner:
  `python -B Analysis/MAT/MAT-001/REMEDIATION/mat001_r1_remediation_runner.py`.
- The reversed RR2 dependency on the later RR2?H7 package was removed. The
  package now consumes the RR2 attempt as upstream evidence, giving the
  provenance direction RR1 ? RR2 ? RR2?H7 package.
- Direct and transitive evidence outputs were regenerated. All retain
  `MAT-001 BLOCKED`, $V$ `NOT_COMPUTED`, $K_Q$ `NOT_DERIVED`, and Stage 4A
  `CLOSED`.
- AUTO-03 completed: H1.3 no longer assigns and tests its own
  `derives_numeric_* = False` fields. It classifies attestations parsed from all
  declared sources; unreadable, unclassified, contradictory, or unbacked input
  fails closed.
- The H1.1-H1.2 inventory is now restricted to an explicit upstream source set, and H1.3 no longer hashes the Master Research Plan. This removes downstream-governance feedback from the derivation graph.
- H1.3 evidence mutations for a derivation claim and a lost source backing both
  invalidate the absence predicate. Normal status remains
  `PASS_MAT001_PARENT_ACTION_H13_INCOMPLETE_SOURCES_AUDITED`, with digest
  `C43E84A180D8F9C9DDA8BE1DAA3DCA8FFE3E83D67329B15066C698DEF0835013`.
- RR1, RR2 and the bounded RR2-H7 package were regenerated from the new H1.3
  digest. No MAT, UVIR, $V$, $K_Q$, or Stage 4A status was promoted.
## R3-R4 close-out record

- R3 selected the universal conformal matter action
  `S_m[Psi_m,A(psi)^2 g]`, with
  `A=exp[C_m(psi-psi_star)]` in natural units. The subtraction definition of
  `S_int` prevents double counting against the minimally coupled matter sector.
- Exact point-particle ADM variation derives the lapse and shift response. The
  normalized comoving linear limit gives `d=(-C_m)` and `h=(0,0)`; the full
  expression retains the mixed lapse vertex and a nonzero moving-matter shift
  vertex. Therefore `h=0` is a controlled background limit, not a global
  identity.
- The matter Ward identity is recorded as
  `nabla_mu T_m^{mu}{}_nu = alpha T_m nabla_nu psi`; for dust at the
  normalization point this gives `Q_m->psi_nu=-C_m rho_m nabla_nu psi` in the
  declared sign convention.
- R3 mutations detect a flipped exchange sign, deletion of the mixed lapse
  response and an invalid global `h=0` claim. Scoped R3 digest:
  `99F712392F0DD42820D760FDAA7D1CDAEA1E301D04D610D5C4B49C663377F676`.
- An independent Wolfram Language reduction returned zero exact lapse/shift
  residuals, the controlled derivatives `(-C_m m,0,0,-C_m m,0)`, and the
  expected nonzero moving shift coefficient. This is an algebra cross-check,
  not repository authority.
- R4 now retains signed real nonzero matter coefficients. J1 rejects zero,
  admits either sign and anchors the parent/IR field orientation. J2 verifies
  `g_can(-u)=-g_can(u)` under physical-mode reversal. The source convention is
  `g_can=-C_m/sqrt(K_Q)=-V_signed` for `u_psi=+1`.
- Magnitude-only matching is explicitly inadmissible: `abs(g_can)` and `V^2`
  may supplement exchange diagnostics but cannot satisfy a signed vertex or
  residue contract. Sign-flip and magnitude-only mutations pass throughout
  `S_INT_DH_EXPORT`, Track-A and RR2.
- The consolidated runner
  `python -B Analysis/MAT/MAT-001/REMEDIATION/mat001_tier1_remediation_runner.py`
  completed all 21 ordered outputs at the R1--R4 close-out, ran every available mutation suite,
  verified each JSON/SHA-256 pair, and ended with
  `MAT=BLOCKED | V=NOT_COMPUTED | K_Q=NOT_DERIVED | Stage4A=CLOSED`.
- Final bounded-package digest:
  `D036D164892492AC3692E5186515781F8591B95341875D00E6AF8B39F5FFEC15`.
  Tier-1 readiness remains `NOT_MET`, with hold digest
  `43FB26DD0A6063368B34ACBE438E82F3B1F0440B3BE0F92AB2FD31E4AE1A644E`.
## R5 microscopic matching decision

- R5 is the post-R1--R4 MAT remediation item, not the pre-existing UVIR-003
  Conditional AQUAL route R5.
- The executable action-level identifiability audit proves
  `V=C_m/sqrt(K_Q)` is invariant under positive field rescaling, while the
  declared R3 matter action and Track-A force action provide no relation
  between their independent `C_m` and `K_Q` Wilson coefficients.
- For every `kappa>0` and nonzero signed `V_target`, the family
  `K_Q=kappa`, `C_m=V_target*sqrt(kappa)` is admitted by the action form.
  Hence the current action class does not select or bound `V`.
- `K_Q=1`, `C_m=C_IR`, fixed `C_obs`, the Conditional UVIR route-R5 anchor,
  and the symbolic RR2 identity all fail to provide Derived closure.
- Scoped status: `PASS_MAT001_R5_IDENTIFIABILITY_AUDIT_HOLD`.
  Matching verdict: `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`.
- R5 digest:
  `20B6A0BD506755DCFB8933668C8F2DC99B90C8BC4917DF8982BB9F59C0C50F24`.
- The research-only R5 pathway survey rejects a minimal shift-symmetric density portal as a standalone static-force source and advances a scale-compensator/superfluid parent only to bounded fork R5-P1.
- The consolidated runner now verifies 22 ordered outputs across R1--R5 and
  retains `MAT=BLOCKED | V=NOT_COMPUTED | K_Q=NOT_DERIVED | Stage4A=CLOSED`.

The hold can be lifted only by a named microscopic calculation of
`g_phi/sqrt(Z_phi)`, a live normalized signed matter-mode residue, or an
independently justified relation with enough physical input to fix or bound
`V`. Another inventory or normalization convention is not an admissible next
step.
