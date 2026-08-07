# MAT-001 R5 pathway survey

**Date:** 2026-08-07

**Status:** `RESEARCH_CANDIDATE_ONLY`

**Executable algebra status:** `PASS_MAT001_R5_PATHWAY_ALGEBRA_RESEARCH_ONLY`

**Global status unchanged:** MAT-001 `BLOCKED`; (V) `NOT_COMPUTED`;
(K_Q) `NOT_DERIVED`; Stage 4A `CLOSED`

## 1. Purpose and evidence boundary

R5 proved that the currently declared action underdetermines
(V=C_m/\sqrt{K_Q}). This survey asks which microscopic parent-action route
could supply a real coefficient relation or a normalized residue. It does not
import a literature model into ITSM, validate a new degree of freedom, or
promote any gate.

Connected searches were used for discovery and adverse-evidence checks. Only
identified primary papers are retained as scientific anchors. Search summaries,
Notion planning text, and computer-algebra output are not treated as physical
evidence by themselves.

## 2. What the search rules out

### 2.1 Standard superfluid-dark-matter matter coupling is not a derivation

The original superfluid-dark-matter construction introduces the phonon-baryon
coupling with a dimensionless coefficient. The relativistic completion
discusses it as an unusual soft explicit breaking of the shift/U(1) symmetry
and offers possible origins, but does not derive the coefficient from the
phonon kinetic normalization.

Therefore this literature supports the R5 HOLD rather than closing it:

- [Berezhiani and Khoury, Phys. Rev. D 92, 103510 (2015)](https://doi.org/10.1103/PhysRevD.92.103510)
- [Berezhiani, Famaey and Khoury, JCAP 09 (2018) 021](https://doi.org/10.1088/1475-7516/2018/09/021)

### 2.2 A minimal symmetry-preserving density portal misses the static source

For the auxiliary-density parent

\[
 {\cal L}=nX-\frac{\lambda}{3}n^3-\eta n\rho_b,
\]

eliminating the positive branch gives

\[
 P_{\rm eff}=\frac{2}{3\sqrt{\lambda}}
 (X-\eta\rho_b)^{3/2}.
\]

This derives the three-halves structure, but a shift-symmetric phase enters
through derivatives in (X). Around (X=X_0-\dot\pi+\cdots), the portal has a
nonzero (\rho_b\dot\pi) vertex and no direct static (\rho_b\pi) source.
An explicit phase portal can supply (\rho_b\pi), but then its coefficient is
an independent soft-breaking parameter unless a further symmetry or threshold
calculation fixes it.

This is consistent with finite-density EFT matching methods in:

- [Joyce, Nicolis and Podo, JHEP 09 (2022) 066](https://doi.org/10.1007/JHEP09(2022)066)
- [Matchev, Smolinsky and Xue, arXiv:2108.07275](https://doi.org/10.48550/arXiv.2108.07275)

Those papers provide methods for integrating out a radial mode or matching a
probe/impurity interaction; neither is evidence that the declared ITSM static
matter residue is fixed.

## 3. First credible predictive fork: scale compensator plus superfluid

A conformal compensator can correlate normalization and matter coupling through
one decay scale. In the minimal toy chart (\psi=\sigma/f),

\[
 {\cal L}_{\rm kin}=\frac{f^2}{2}(\partial\psi)^2,
 \qquad
 {\cal L}_m=-\rho_b e^\psi,
\]

so (K_Q=f^2), (C_m=1), and

\[
 V=\frac{1}{f}.
\]

The same result appears in the canonical (\sigma) chart as (K_Q=1) and
(C_m=1/f). Unlike setting (K_Q=1) by convention in the existing action,
this relation follows from the candidate compensator construction.

Primary anchors establish that finite-density phonon-dilaton mixing is real and
that compensator matter couplings are controlled by a dilaton scale:

- [Argurio, Hoyos and Musso, Phys. Rev. D 102, 076011 (2020)](https://doi.org/10.1103/PhysRevD.102.076011)
- [Fuks, Goodsell and Kang, JHEP 10 (2020) 044](https://doi.org/10.1007/JHEP10(2020)044)

This is a candidate, not a closure. The finite-density theory has mixed
phonon/dilaton modes; the physical signed residue must be projected after the
full constraint and kinetic reduction. The fork also owes stability, cutoff,
screening, post-Newtonian and lensing tests. It may change the declared mode
count and therefore requires an explicit architecture decision.

## 4. Ranked pathway

1. **Close the minimal-portal obstruction.** Re-derive the absence of a static
   (\rho_b\pi) source in the exact ITSM phase chart, including ADM variables.
2. **Open one bounded parent-action fork.** Write a scale-compensator plus
   finite-density condensate action with a single declared scale (f), no
   coefficient inserted from the MOND target, and an explicit symmetry table.
3. **Perform the physical-mode calculation.** Integrate out nondynamical fields,
   diagonalize the scalar kinetic/gradient matrices, and compute the signed
   matter-to-mode pole residue. A symbolic (1/f) before mode projection is not
   sufficient.
4. **Apply hard rejection gates.** Reject the fork for an extra ghost, gradient
   instability, zero/strong-coupling singularity, unacceptable extra long-range
   mode, failed screening/local-gravity limits, or no overlap with the required
   galactic regime.
5. **Use scalar-tensor/scalaron models only as a control.** A symmetry-fixed
   universal coupling demonstrates that fixed residues are possible, but an
   unscreened galactic-range scalar is strongly constrained and would be a
   gravitational-architecture change, not a minimal ITSM repair.

## 5. Proposed next package: R5-P1

**Name:** `R5-P1_SCALE_COMPENSATOR_PARENT_FORK`

**Required artifacts:**

- one covariant parent action and field/units table;
- symmetry-breaking and degree-of-freedom ledger;
- homogeneous finite-density background equations;
- complete scalar quadratic action after constraints;
- kinetic/gradient eigenvalues and physical-mode map;
- signed matter residue (g_{\rm phys});
- cutoff and strong-coupling estimate;
- screening, PPN and lensing applicability statement;
- mutation tests that reject coefficient insertion and pre-projection matching.

**Decision rule:** advance only if the same healthy parameter domain derives or
rigorously bounds (g_{\rm phys}) without importing (C_{\rm obs}). Otherwise
freeze the fork as rejected and retain the R5 HOLD.

## 6. Connected-tool audit

| Connection | Use | Disposition |
|---|---|---|
| Scite and SciSpace | Primary-paper discovery and source-level adverse checks | Retained only through the identified papers/DOIs above |
| Wolfram | Independent elimination/series check for the density portal and compensator chart identity | Algebra cross-check only; repository script is authoritative for reproduction |
| Notion | Compared the route against internal finite-density/sextic planning | Planning context only; not peer-reviewed evidence |
| Slack | Searched for prior (K_Q/C_m) matching discussion | No relevant result found |
| Agora | Attempted broad research synthesis | Excluded: returned unrelated citations and cannot support physics claims |

## 7. Reproduction

```powershell
python -m py_compile Analysis/MAT/MAT-001/R5_PATHWAY/mat001_r5_pathway_algebra.py
python -B Analysis/MAT/MAT-001/R5_PATHWAY/mat001_r5_pathway_algebra.py --self-test-mutations
python -B Analysis/MAT/MAT-001/R5_PATHWAY/mat001_r5_pathway_algebra.py
```

Current output SHA-256:
`0ED92C61C2811A178B53AA85F4F3AF843DD4B1ECFD65D5EDD0BC4AC187FA5E99`.

The executable check rejects a standalone density portal as a static matching
route and advances the compensator construction only to a bounded research
fork. It does not close R5 or alter any global status.