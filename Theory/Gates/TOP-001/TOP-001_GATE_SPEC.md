# TOP-001 — Gate specification (shape moduli and toroidal boundary conditions)

**Document type:** Open gate specification (research scaffold)
**Gate ID:** TOP-001
**Status:** `OPEN_SCAFFOLD_ONLY`
**Date:** 2026-08-03
**Branch:** `recovery/v12-core-architecture`
**Claim restoration:** **none** — no Derived topology or cosmology

---

## 0. Executive question

**Q0.** Can the retained **toroidal-shape identity** — compact flat spatial
slices with fundamental lengths $L_i$, optional twisted flat boundary
conditions, and **shape moduli** that are not automatic Wilson numbers — be
realized as a **consistent, energy-accounted sector** such that:

1. **topology** is cleanly separated from **metric** and **dynamical moduli**;
2. **fixed BC** are separated from **evolving** side lengths or shear;
3. **rectangular $T^3$** is separated from **twisted $E_2/E_3$** candidates
   (no automatic preference without energy/stability comparison);
4. **free Casimir stress** is separated from **driven / wake / reservoir /
   memory** stress;
5. **global geometry** is separated from **local Wilson coefficients** and
   **force laws**;
6. no free-field **$13/12$** attractor, **$H_0=72.97$**, topology-alone
   $a_0$, or $C_{\mathrm{obs}}=2/3$ packaging is restored?

**If yes:** produce a modulus action (or justified fixed-BC class), energy
accounting, and staged tests under declared domain.
**If no:** document falsifiers and demote or restrict the pillar with written
reason — **not** by recycling CBR-001 packaging failures.

---

## 1. Identity retained vs packaging rejected

### 1.1 Retained (Open identity)

| Element | Content |
|---------|---------|
| Compact flat $T^3$ | Periodic spatial identification; fundamental lengths $L_i>0$ |
| Shape moduli | Side lengths and ratios (e.g. biaxial $r=L_t/L_p$); **not** automatic invariants |
| Twisted flat BC | Master Plan **Open preference** for recirculating stabilisers vs pure cubic $E_1$ alone — **Conditional until compared** |
| Topology-dependent free stress | CBR-001: unequal lengths ⇒ anisotropic free Casimir pressure |
| Mode lattice | Discrete momenta set by $L_i$ and BC class |

### 1.2 Rejected packaging (do not re-import)

| Packaging | Disposition |
|-----------|-------------|
| Free-field persistent attractor $H_t/H_p=13/12$ | **Rejected** (CBR-001 / architecture §8) |
| Parameter-free $H_0=72.97$ from that attractor | **Rejected** |
| $a_0=cH_0/(2\pi)$ from topology alone | **Rejected** as TOP derivation; DSM is Conditional **elsewhere** if used |
| $C_{\mathrm{obs}}=2/3$ from dimension counting / projection | **Rejected** as TOP derivation |
| Automatic anisotropic stress from energy throughput alone | **Rejected** (architecture §3.9) |
| Automatic CMB / lensing / SPARC / NANOGrav from shape | **Forbidden** until COS/PERT/LEN/DISK etc. |
| Inserting $13/12$ into a modulus potential or constitutive coefficient | **Forbidden** |
| Twisted $E_2/E_3$ preferred without energy/stability comparison | **Forbidden** as Derived; Open research option only |

### 1.3 CBR-001 baseline (input, not re-derived here)

For free massless scalar on rectangular flat $T^3$:

- renormalized lattice Casimir stress is **anisotropic** when lengths unequal;
- free-field biaxial backreaction yields only **transient** passages near
  $H_t/H_p=13/12$; **no** quasi-plateau or attractor;
- topology-dependent anisotropic stress remains a **mechanism**, not a
  finished cosmology.

TOP-001 **must not** contradict this baseline by packaging. Driven persistence
is **CBR-002 / Open**, not free-field TOP.

---

## 2. Declared degrees of freedom

### 2.1 Global geometric moduli (TOP primary)

On a rectangular flat $T^3$ chart:

\[
L_i > 0,\qquad i=1,2,3,
\qquad
V = L_1 L_2 L_3,
\qquad
r_{ij} = L_i/L_j.
\]

Common reductions:

| Object | Type | Role |
|--------|------|------|
| $L_i$ | global moduli | fundamental circumferences |
| $V$ | composite | volume; often fixed in template scans |
| $r = L_t/L_p$ | biaxial shape | CBR-001 language; not a free attractor target |
| shear / off-diagonal flat moduli | optional | twisted or sheared flat metrics (Open) |

**Rule:** moduli are **not** local Wilson coefficients of $S_\psi$ or $S_\Phi$.

### 2.2 Topology and boundary-condition class

| Object | Type | Notes |
|--------|------|-------|
| Manifold class | discrete choice | rectangular $T^3$; twisted flat $E_2/E_3$-type candidates |
| Identification maps | global BC data | fixed vs time-dependent |
| Homology cycles $\gamma_i$ | topological | interface to VOR winding $\oint d\Theta=2\pi n_i$ |

### 2.3 Local / field content (not owned by TOP)

| Object | Owner | TOP role |
|--------|-------|----------|
| $g_{\mu\nu}$ | GR / background | TOP supplies BC and moduli, not EH dynamics alone |
| $\Phi=\rho e^{i\Theta}/\sqrt{2}$ | UVIR / VOR | lives on manifold TOP declares |
| $\psi$ force phonon | UVIR / MAT | **not** a TOP DOF |
| Wake $W$ | WAK-001 | **not** a TOP DOF |
| Reservoir $T_R^{\mu\nu}$ | reservoir sector | couples later; not free Casimir |

### 2.4 Nonlocal / sector quantities

| Object | Type | Notes |
|--------|------|-------|
| Free Casimir $\Pi_{\mathrm{Cas}}(a,r)$ | nonlocal functional of shape | CBR-001; radiation-like scale factor in tested model |
| Driven anisotropic stress | constitutive | CBR-002; requires declared action |
| Mode spectrum $\{k_{\mathbf{n}}\}$ | discrete set | template: $k_i = 2\pi n_i/L_i$ (periodic scalar) |

---

## 3. Candidate routes

Routes are **research options**, not Derived rankings.

### Route T1 — Fixed rectangular $T^3$ BC (parameterized geometry)

- Fix $L_i$ (or fix $V$ and scan shape ratios)
- Compute mode lattices, free Casimir diagnostics (via CBR tools), compensated
  Poisson hygiene
- **Pros:** matches CBR-001 / P2; lowest packaging risk
- **Cons:** no dynamical explanation of observed shape

### Route T2 — Dynamical shape moduli with effective potential

- $S_{\mathrm{mod}}[L_i]$ or $S_{\mathrm{mod}}[r]$ with kinetic term + potential
- Potential from Casimir, condensate, or other **declared** sectors
- **Pros:** Master Plan “action + energy accounting”
- **Cons:** easy to smuggle $13/12$ into $V(r)$; forbidden

### Route T3 — Minisuperspace cosmology with shape (biaxial/triaxial)

- Scale factor $a(t)$ + shape $r(t)$ as in CBR-001 backreaction language
- **Pros:** direct interface to free-field negative result and driven follow-ons
- **Cons:** not full COS-001; must not claim CMB

### Route T4 — Twisted flat manifolds ($E_2/E_3$-class)

- Nontrivial holonomy / shift identification; recirculating stabiliser preference
- **Pros:** Master Plan identity preference
- **Cons:** **must** energy/stability-compare to rectangular $T^3$ before preference is Derived

### Route T5 — Joint TOP+VOR bundle geometry

- $\Phi$ as section on manifold with moduli; winding sectors on cycles
- **Pros:** clean interface
- **Cons:** requires VOR staged work; TOP still owns $L_i$

**Scaffold default for first calculations:** **T1** templates + CBR-001 as
external baseline; T2/T3 only after firewall review of any potential.

---

## 4. Energy, constraint, stability, covariance requirements

| ID | Requirement | Stage |
|----|-------------|-------|
| **E1** | Moduli (if dynamical) have a declared Lagrangian density or minisuperspace action | S2 |
| **E2** | Energy of free Casimir / vacuum stress defined only under renormalization scheme already validated for that BC class | S1–S2 |
| **E3** | No unbounded-below modulus potential at fixed volume without physical cutoff statement | S2 |
| **E4** | Fixed-volume or fixed-charge constraints stated when used (template: fixed $V$) | S0–S1 |
| **E5** | Covariance: moduli as geometric data compatible with spatial diffeomorphisms / residual torus automorphisms | S2 |
| **E6** | Stability: Hessian of effective potential (or mode frequencies) positive in declared domain, or HOLD with obstruction | S2–S3 |
| **E7** | Total conservation when coupled: TOP stress enters $T^{\mu\nu}$ with exchange terms named (CRA) | S4+ |

**Out of early stages:** full relativistic completion of dynamical twisted moduli on FRW.

---

## 5. Interfaces

### 5.1 VOR-001

- TOP declares manifold + $L_i$ + BC class.
- VOR places winding $\mathbf{n}\in\mathbb{Z}^3$ and defects on that manifold.
- Neither gate derives force-law coefficients from the other by packaging.

### 5.2 CBR-001 / CBR-002

- **CBR-001:** free rectangular $T^3$ Casimir + free backreaction baseline
  (anisotropy yes; persistent $13/12$ no).
- **CBR-002:** driven anisotropic stress only after reservoir, shape, and wake
  sectors are derived (Recovery Plan). TOP supplies shape sector **inputs**,
  not the driven constitutive law.

### 5.3 WAK-001

- Wake/memory stress is **not** free Casimir and **not** shape moduli kinetic energy.
- Joint anisotropic sources require separately declared actions.

### 5.4 Reservoir / $Q_{\rm syn}$

- Open-system exchange may compensate observable-subsystem stress.
- Energy injection **alone** does not imply directional stress (architecture).
- Reservoir is **not** a substitute for $S_{\mathrm{mod}}$.

### 5.5 UVIR / MAT / force

- Mode lattices may enter phonon/Green calculations as BC data.
- Force Wilson coefficients ($C_{\mathrm{IR}}$, $K_Q$, …) are **not** TOP outputs.

---

## 6. Staged tests (with negative controls)

### Stage S0 — Vocabulary and separation (this scaffold)

| ID | Test | Pass criterion |
|----|------|----------------|
| S0.1 | DOF table: topology / moduli / fields / Wilson | Written and non-conflating |
| S0.2 | Claim firewall | Rejected packaging enumerated |
| S0.3 | Route catalogue | ≥3 routes with pros/cons |
| S0.4 | Optional template | Fixed-volume shape quantities; `physics_pass: false`; refinement + negative controls |

### Stage S1 — Fixed rectangular $T^3$ geometry (math)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S1.1 | Mode lattice $k_{\mathbf{n}}=2\pi\sqrt{\sum(n_i/L_i)^2}$ | **PASS** if implemented under periodic BC |
| S1.2 | Fixed-volume shape scan invariants | **PASS** if $V$ held fixed; ratios vary |
| S1.3 | Negative control: cubic $L_1=L_2=L_3$ | **PASS** if directional mode anisotropy diagnostic vanishes |
| S1.4 | No $13/12$ insertion | **FAIL** if target ratio hard-coded into potential/template as “attractor” |
| S1.5 | Full-triaxial log-shape chart (two independent coords) | **PASS** template: `PASS_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE` (see `TOP-001_STAGE_S1_TRIAXIAL.md`); biaxial scaffold retained separately |
| S1.6 | Axis-permutation covariance of directional moments | **PASS** if moments transform under $L_i$ permutations; $A$ invariant |
| S1.7 | Modular-basis redundancy $B\sim BM$, $M\in SL(3,\mathbb Z)$ | **PASS** template: exact direct/reciprocal/winding reindexing, Gram covariance and volume invariance; physical deformation kept separate (see `TOP-001_STAGE_S1M_MODULAR_BASIS.md`) |
| S1.8 | Physical-cutoff modular spectrum | **PASS** template: certified-complete $\ell=m^T(B^{-1}B^{-T})m$ cutoff gives identical exact spectra and degeneracies; identical raw label boxes fail the negative control (see `TOP-001_STAGE_S1M_PHYSICAL_CUTOFF_SPECTRUM.md`) |

### Stage S2 — Free Casimir / vacuum stress interface

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S2.1 | Point to CBR-001 validated pipeline as baseline | **PASS** if cited without re-packaging attractor |
| S2.2 | Reproduce anisotropy qualitative statement for unequal $L_i$ | **PASS** via CBR tools or equivalent; not required to re-run full lattice in TOP toy |
| S2.3 | Negative control: free backreaction has no persistent $13/12$ | **PASS** if architecture/CBR baseline retained |

### Stage S3 — Dynamical moduli (only if Route T2/T3 chosen)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S3.1 | Write $S_{\mathrm{mod}}$ without forbidden targets | **PASS** if no $13/12$, $H_0$, $a_0$ in potential by hand |
| S3.2 | Energy accounting + stability Hessian | **PASS** / **HOLD** |
| S3.3 | Negative control: freeze moduli → recover fixed-BC sector | **PASS** if limit exists |

### Stage S4 — Twisted BC comparison (Route T4)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S4.1 | Define twisted identification maps | **PASS** if charts declared |
| S4.2 | Energy/stability comparison vs rectangular $T^3$ | **PASS** only with comparison; **FAIL** if preference asserted without it |

### Stage S5 — Coupling audits

| ID | Test | Notes |
|----|------|-------|
| S5.1 | VOR winding on TOP cycles | Joint interface |
| S5.2 | WAK/reservoir stress ≠ free Casimir | Separation audit |
| S5.3 | No force-law smuggling | UVIR/MAT firewall |

---

## 7. Falsifiers

| ID | Falsifier |
|----|-----------|
| F1 | Only viable “results” restore free-field $13/12$ attractor or $H_0=72.97$ |
| F2 | Moduli continuously identified with local Wilson coefficients of $\psi$ without matching |
| F3 | Dynamical modulus potential unbounded below with no cutoff and no HOLD |
| F4 | Twisted preference claimed without energy/stability comparison |
| F5 | Directional stress inferred from energy injection alone |
| F6 | Topology-alone derivation of $a_0$ or $C_{\mathrm{obs}}$ presented as TOP-Derived |

**Non-falsifier:** UVIR-003 still IN PROGRESS; VOR-001 still OPEN scaffold.

---

## 8. PASS / HOLD / FAIL criteria

### 8.1 Scaffold pass (current target)

**PASS_SCAFFOLD** when:

- README + this GATE_SPEC exist;
- separations and claim firewall are explicit;
- staged tests S0–S5 written with negative controls;
- no Derived cosmological/topology packaging asserted.

### 8.2 Research pass (future — not claimed now)

Toward Master Plan TOP/VOR/WAK pass (*actions + energy accounting*):

- declared fixed-BC class **or** $S_{\mathrm{mod}}$ with E1–E6 addressed in domain;
- CBR-001 baseline respected;
- written scientific boundary;
- ledger/Master Plan updates only when programme integrates (out of scaffold scope).

### 8.3 HOLD

Structural obstruction (incomplete twisted class, renormalization scheme gap)
without falsifying compact-$T^3$ identity.

### 8.4 FAIL

Falsifier F1–F6 under named premises, or gate used only to re-package rejected claims.

---

## 9. Claim firewall (mandatory)

### 9.1 Allowed *now*

| Class | Examples |
|-------|----------|
| **Open** | “Shape moduli may have an action; twisted BC remain candidates.” |
| **Conditional** | “Under fixed $V$, periodic BC and the tested symmetric truncation, $D$ vanishes at the cubic point and is nonzero for the scanned non-cubic chart points.” |
| **Template-only** | Fixed-volume geometric scans with `physics_pass: false` |
| **Baseline citation** | CBR-001 free-field anisotropy without attractor |

### 9.2 Forbidden *now*

| Forbidden | Reason |
|-----------|--------|
| Persistent free-field $13/12$ | CBR-001 Rejected |
| $H_0=72.97$ parameter-free | Rejected packaging |
| $a_0$ from topology alone | Rejected as TOP derivation |
| $C_{\mathrm{obs}}=2/3$ from geometry counting | Rejected as TOP derivation |
| Automatic cosmology / lensing / SPARC / PTA | Upstream gates missing |
| $13/12$ in modulus potential | Forbidden insertion |
| Twisted preferred without comparison | Open only |

### 9.3 Reviewer checklist

- [ ] Topology vs metric vs moduli distinguished
- [ ] Fixed BC vs dynamical $L_i$ distinguished
- [ ] Rectangular vs twisted distinguished
- [ ] Free Casimir vs driven/wake/reservoir distinguished
- [ ] Geometry vs Wilson/force distinguished
- [ ] Template vs physics distinguished
- [ ] No $13/12$ / $H_0=72.97$ / dual RAR packaging

---

## 10. Suggested calculation order

1. Freeze rectangular $T^3$, fixed $V$, scan shape ratios (S1 template).
2. Quotient modular-basis relabellings and validate spectra with a physical cutoff before treating a shear chart as a physical modulus (S1.7-S1.8).
3. Cite/use CBR-001 for free stress baseline (S2); do not re-open attractor.
4. Only then draft $S_{\mathrm{mod}}$ (S3) if dynamical route chosen.
5. Twisted comparison (S4) before any identity preference upgrade.
6. Joint VOR/WAK/reservoir audits (S5) before CBR-002 packaging.

---

## 11. Optional mathematical template

```text
Analysis/TOP/TOP-001/top001_shape_template_audit.py
Analysis/TOP/TOP-001/README.md
```

Label: **mathematical-template-only**.
Scope: fixed-volume rectangular-torus shape diagnostics and free scalar mode
lattice anisotropy measures; refinement + negative controls;
`physics_pass: false`.
**Does not** pass TOP-001 research gate; **does not** recompute CBR-001 Casimir.

---

## 12. Unresolved decisions (independent review)

| ID | Decision |
|----|----------|
| U1 | Stay on fixed-BC (T1) through first research pass, or prioritize dynamical moduli (T2/T3)? |
| U2 | Primary shape chart: biaxial $r$ only vs full triaxial $L_i$? |
| U3 | When to open twisted $E_2/E_3$ comparison (S4)? |
| U4 | Which sectors may source $V_{\mathrm{mod}}$ (Casimir only / condensate / none yet)? |
| U5 | Fixed comoving volume vs dynamical volume in minisuperspace? |
| U6 | Programme integration: Master Plan / ledger update only after review? |

---

## 13. Document control

| Version | Date | Note |
|---------|------|------|
| 0.2 | 2026-08-03 | Independent template review: domain guards, four malformed-input controls, 1% refinement guardrail, and chart-scoped wording |
| 0.1 | 2026-08-03 | Initial Open scaffold; research only; no claim restoration |
