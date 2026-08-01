# ITSM Selective Publishing Plan

**Status:** Working plan — **post–tier-1 referee reconstruction** (2026-08-01)  
**Branch authority:** `recovery/v12-core-architecture`  
**Master research plan:** `Theory/Core/ITSM_Master_Research_Plan.md`  
**Claim authority:** `Theory/Core/ITSM_Claim_Migration_Ledger.csv`  
**P1 authority:** `papers/P1-Scale-Matching-Reconstruction/` (reconstruction after Reject)  
**Naming table:** `papers/PAPERS_NAMING.md`  
**Manuscript authority:** `Manuscript/CoreRecovery/` (see `VERSION` for current freeze)

This document is the **binding claim firewall** for the staged paper program.  
Strategy (short, modular papers) is retained. **Headline claim strength is not.**  
For scientific identity, gate order, and the session checklist, use the master research plan first.

---

## 0. Executive change log (why this revision exists)

A tier-1 technical referee report **rejected** the prior P1 framing that claimed:

1. \(a_0=cH_0/2\pi\) from “circulation quantization,” and  
2. \(C_{\rm obs}=2/3\) from a transverse-projector trace ratio,

on a cubic flat \(T^3\) with \(L=c/H_0\).

**P1 was reconstructed** as a reconstruction / no-go note (see  
`papers/P1-Scale-Matching-Reconstruction/README.md`).  

**Papers 2–4 must never re-inflate the withdrawn claims**, even as “companion geometric inputs,” “established in Paper I,” or soft abstract wording.  
If a later paper needs a geometric derivation of \(a_0\) or \(C_{\rm obs}\), it must **close the reconstruction chain** (Sec.~0.2) and stand on its own math — not on citation of the old P1 title.

### 0.1 Hard ban list (global — all papers, all abstracts, all figures)

**Scope:** this list bans **abstract / manuscript packaging**, not research.
Underlying topics (wake, winding/SWNT *principle*, AQUAL-class IR, driven
anisotropy, PTA eigenmodes, honest SPARC pipelines) remain open under the
master plan’s Bucket B/C and identity pillars. Do not treat B1–B16 as a
research veto of untested routes.

These phrases and implications are **forbidden in papers** until a new manuscript closes the reconstruction chain and passes peer scrutiny:

| Ban ID | Forbidden claim | Why |
|--------|-----------------|-----|
| **B1** | \(a_0\) is *derived* from circulation quantization / Bohr–Sommerfeld on \(T^3\) | \(\kappa=cL\) is not \(h/m\) quantization |
| **B2** | Simultaneous \(L=c/H_0\), \(\Gamma=cL\), \(\omega=H_0\) as a consistent package | Internal kinematic contradiction if \(L\) is circumference |
| **B3** | “Distributing \(cH_0\) across \(2\pi\) topology” as a derivation | Chart-dependent; not coordinate-invariant |
| **B4** | Cubic \(E_1\) with \(L=c/H_0\) is COMPACT/Planck compatible or “marginally super-horizon” | Requires \(L\gtrsim\mathcal{O}(6)\,c/H_0\) order of magnitude |
| **B5** | Exact \(L_{\rm phys}(t)=c/H(t)\) under fixed comoving moduli in ordinary FLRW | Forces \(q=0\) (coasting); needs evolving moduli otherwise |
| **B6** | Hubble sphere \(c/H\) as “global causal domain / horizon” without qualification | Not generally a particle or event horizon |
| **B7** | \(\operatorname{Tr}(h)/\operatorname{Tr}(\gamma)=2/3\) *determines* \(C_{\rm obs}\) or is \(T^3\)-specific | Generic 3D identity; projector absent from weak-field action |
| **B8** | \(\Cobs=2/3\) as a geometric / universal local coupling | Matching assignment, not a Wilson calculation |
| **B9** | Simultaneous \(\azero=cH_0/2\pi\) *and* \(\Cobs=2/3\) as the empirical RAR/BTFR normalization | Predicts \(a_{0,\rm eff}=(4/9)\azero\); factor \(\sim 2.4\) off |
| **B10** | Doughnut / embedded \(\Ttwo\) figure labelled as flat \(\Tthree\) | Category error |
| **B11** | \(\mathcal{O}((r/L)^2)\) finite-size series as a derived error bar | Underived; topology is nonlocal (images, modes) |
| **B12** | Persistent free-field \(H_t/H_p=13/12\) or \(H_0=72.97\) as parameter-free prediction | Ledger Rejected (CBR-001); cycle counting Rejected |
| **B13** | NANOGrav fixed window \([1.08,\pi]\) nHz as *derived* | No eigenmode calculation |
| **B14** | JWST CO/Na I → bottom-light IMF as *derived* | Star-formation derivation Rejected |
| **B15** | SPARC \(p=0.62\); SPARC as independent cosmic \(H_0\) | Ledger Rejected |
| **B16** | “Zero free theoretical parameters” / “resolves all tensions” | Overclaim |

**Enforcement:** before any abstract is frozen, grep the ban list concepts (quantization derivation, \(72.97\), \(13/12\) prediction, doughnut \(T^3\), \(C_{\rm proj}\Rightarrow C_{\rm obs}\), super-horizon \(c/H_0\)).

### 0.2 Reconstruction chain (required before *any* paper claims a geometric derivation of \(a_0\) or \(C_{\rm obs}\))

Copied from the referee / P1 §path. **All ten steps** must be closed in a dedicated derivation paper (not smuggled into P2–P4):

1. Condensate order parameter \(\Psi=\sqrt{n}\,e^{i\theta}\) (or relativistic analogue) with mass \(m\).  
2. Circulation from \(\nabla\theta\) and integer winding on \(T^3\).  
3. Precise definition of \(L\) (edge / geodesic / circumference) used consistently.  
4. Derived map from circulation \(\to\) acceleration scale (no chart-dependent \(2\pi\) ritual).  
5. Present-epoch-only matching **or** modulus action for \(L_{\rm phys}(t)\) without forcing \(q=0\).  
6. Correct \(T^3\) fundamental-domain schematic (never \(\Ttwo\) doughnut).  
7. Projector \(h^{ij}\) *in the action*; dynamics for \(n^i\); calculation of \(\Cobs\) independent of field normalization.  
8. Reconciliation of \(\Cobs^2 a_0\) with empirical RAR/BTFR.  
9. Compensated periodic nonlinear solution: ≥1 sphere + ≥1 disk.  
10. Direct confrontation with Planck/COMPACT cubic (and twisted) bounds.

Until then, the only honest product about \(a_0\) / \(2/3\) is the **P1 reconstruction note**.

### 0.3 What *may* still be said (whitelist)

| Statement | Allowed where | Caveat required |
|-----------|---------------|-----------------|
| Empirical coincidence \(2\pi a_0\sim cH_0\) | Any paper (motivation) | Not a derivation |
| \(a_0\equiv cH_0/2\pi\) as *present-epoch phenomenological* scale match | P1; optional *named postulate* in later papers | Never “derived from topology” |
| \(\Cobs=\Cm^{3/2}/\sqrt{\CIR}\) invariant | Any EFT / kinematics paper | Main solid positive result |
| Compensated sources / curl caution on compact \(T^3\) | P1, P4, theory notes | Does not fix \(\Cobs=2/3\) |
| Free rectangular \(T^3\) Casimir stress validated | **P2** | Not a universal cycle coefficient |
| Transient free-field passages near \(q=13/12\); no attractor | **P2** | Not a Hubble solution |
| Gate-level observational *program* (no fixed false predictions) | **P3** | Downstream of open gates |
| Kinematics under *explicit* nuisance model + declared \(\Cobs,a_0\) choices | **P4** | Must not claim geometric derivation or RAR-safe dual normalization |

---

## 1. Strategic judgment (still keep)

1. **One core claim per paper.**  
2. **Short manuscripts (6–12 pages).**  
3. **Public reproducibility** (GitHub + Zenodo).  
4. **Neutral language** — prefer “phenomenological matching,” “validated mechanism,” “negative free-field result,” “gate-dependent program.”  
5. **Robustness to partial failure** — P2 must stand if geometric \(a_0\) never returns; P1 no-gos must stand if Casimir never becomes cosmology.

Drop from style rules: marketing phrases like “geometric origin” and “zero-parameter under postulates” unless the reconstruction chain is closed.

---

## 2. Claim hygiene filter

| Label | Meaning |
|-------|---------|
| **Derived** | Checked result from declared assumptions; may headline. |
| **Phenomenological** | Named encoding of data / coincidence; may headline only as postulate. |
| **Conditional** | Requires named extra assumption; name it in abstract. |
| **Open** | Research program only. |
| **Rejected / Withdrawn** | Ban list (Sec.~0.1); historical only. |
| **Excluded** | Logically or observationally incompatible with concurrent assumptions. |

### Status table (post-referee)

| Claim | Status | Papers |
|-------|--------|--------|
| \(2\pi a_0\sim cH_0\) coincidence | Fact | All (motivation) |
| \(a_0\equiv cH_0/2\pi\) present-epoch | Phenomenological | P1; optional named use in P4 |
| Circulation \(\Rightarrow a_0\) | Withdrawn | **None** |
| Cubic \(E_1\), \(L=c/H_0\) vs Planck | Excluded | **None** as viable model |
| Fixed-moduli \(L\propto c/H(t)\) | Incompatible | **None** without moduli theory |
| Trace \(2/3\) DOF count | Derived (generic) | P1 only as identity |
| Trace \(\Rightarrow\Cobs\) | Withdrawn | **None** |
| \(\Cobs\) invariant | Derived | P1, P4, EFT notes |
| \(\Cobs=2/3\) + \(a_0=cH_0/2\pi\) as RAR | Excluded | **None** |
| Free Casimir anisotropic stress | Derived (CBR-001) | **P2** |
| Persistent free-field \(13/12\) | Rejected | **None** as prediction |
| Transient \(q\approx 13/12\) crossings | Derived diagnostic | **P2** |
| \(H_0=72.97\) zero-parameter | Rejected | **None** |
| NANOGrav \([1.08,\pi]\) derived | Rejected | **None** until VOR-001 |
| JWST IMF derivation | Rejected | **None** until ASTRO-001 |
| SPARC \(p=0.62\), SPARC-\(H_0\) | Rejected | **None** |

---

## 3. Paper sequence (updated)

| # | Working name | Core claim (allowed) | Readiness | Length | Venues |
|---|--------------|----------------------|-----------|--------|--------|
| **P1** | Scale-matching reconstruction | Prior geometric story fails; \(\Cobs\) invariant + compact-source hygiene survive; \(a_0\equiv cH_0/2\pi\) only as present-epoch phenomenology | **Draft complete** (reconstructed) | ~5–8 pp | CQG / PRD Notes / arXiv first |
| **P2** | Rectangular \(T^3\) Casimir + free-field backreaction | Validated anisotropic free-scalar stress; **no** free-field persistent \(H_t/H_p=13/12\) attractor | **Draftable now** | 8–12 pp | PRD, JCAP, CQG |
| **P3** | Gate-structured observational program | Falsifiers *conditional* on closed gates; no fixed nHz/IMF numbers | Outline now | 7–9 pp | later |
| **P4** | Kinematics under declared inputs | Fits with **explicit** \(a_0\), \(\Cobs\) choices; honest BIC; no dual-normalization claim | After DISK-001 + STAT-001 | 8–12 pp | MNRAS, ApJ |

### Why this sequence still works

- **P1** is no longer “citation capital for two invariants.” It is **citation capital for intellectual honesty and the \(\Cobs\) invariant** — and a firewall document later papers must cite when they *avoid* overclaim.  
- **P2** does **not** depend on P1’s withdrawn derivations. It must not cite P1 as establishing geometric \(a_0\) or \(C_{\rm proj}\). Cite P1 only for claim hygiene / topology schematic standards if needed.  
- **P3–P4** remain downstream of gates; ban list applies in full.

---

## 4. Paper-by-paper claim firewalls

### 4.1 P1 — Reconstruction (current)

**Path:** `papers/P1-Scale-Matching-Reconstruction/`

**Allowed headline:** neither \(a_0\) nor \(2/3\) is yet a geometric derivation on cubic \(T^3\); \(\Cobs\) invariant is derived; compact compensated sources.

**Must not claim:** anything on the ban list as a positive derivation.

**Citation role for later papers:**  
> “Claim hygiene and withdrawn geometric shortcuts are recorded in [P1]; the present work does not rely on those shortcuts.”

---

### 4.2 P2 — Casimir stress (highest-priority next draft)

**Core claim (one sentence):**  
For a free massless scalar on a *rectangular* flat \(T^3\), renormalized lattice Casimir stress is anisotropic and validated; free-field biaxial backreaction produces only *transient* passages near \(H_t/H_p=13/12\), with no quasi-plateau or attractor.

#### P2 must include

- Epstein / lattice \(\rho_{\rm Cas}\), \(p_i\); validation table (CBR-001 Stages 1–2).  
- Biaxial shear system + Stage 3B ratio test.  
- Explicit historical box: cycle-counting \(13/12\) and \(H_0=72.97\) are **not** predictions of this paper.  
- Correct \(T^3\) fundamental-domain / rectangular schematic (**B10**).  
- Distinguish rectangular moduli (shape-dependent stress) from cubic \(E_1\) CMB bounds (**do not** claim the simulated box is Planck-safe cosmology).

#### P2 must not

| Forbidden in P2 | Ban |
|-----------------|-----|
| “Uses geometric \(a_0\) from Paper I” | B1–B3 |
| “Same topology that derives MOND scale” | B1, B4 |
| “Parameter-free Hubble resolution” | B12 |
| \(H_t=(13/12)H_p\Rightarrow 72.97\) as theory prediction | B12 |
| “Super-horizon cubic cell \(L=c/H_0\)” | B4 |
| “Dynamic scale matching justifies the lattice size” | B5 |
| Cite projector \(2/3\) as related physics | B7–B9 |
| Doughnut figure | B10 |

#### P2 companion citation (safe)

> Companion work [P1] records that present-epoch scale matching and projector counting are *not* geometric derivations of galactic dynamics; the Casimir calculation below is independent of those proposals and does not restore them.

#### P2 abstract seed (firewall-safe)

> Compact spatial topology can source anisotropic vacuum stress. For a free massless scalar on a rectangular flat three-torus we validate a renormalized lattice Casimir energy density and directional pressures. Coupled to biaxial expansion, free-field backreaction produces only transient passages near the historically proposed ratio \(H_t/H_p=13/12\), with no quasi-plateau or late-time attractor. Persistent anisotropic expansion cannot be attributed to free Casimir stress alone. We do not claim a resolution of the Hubble tension, a derivation of the galactic acceleration scale, or a completed cubic cosmology.

#### P2 drafting checklist

- [x] Skeleton `papers/P2-Rectangular-T3-Casimir/main.tex` (draft scaffold 2026-08-01)  
- [x] Port `06_topology_casimir.tex` + CBR-001 STAGE docs  
- [x] Freeze Stage 1–3B checksums into paper appendix (`CBR001_CHECKSUMS.md`)  
- [x] **Abstract ban-list review (Sec.~0.1)** (draft abstract uses whitelist wording)  
- [x] No cross-cite of withdrawn P1 geometric story as positive input  
- [x] Limitations: free scalar only; rectangular moduli; de Sitter testbed; CBR-002 open  
- [x] Cover letter draft  
- [x] Hostile internal read (`HOSTILE_READ.md`) + minor tex fixes  
- [ ] Optional external co-read  
- [ ] Submit / arXiv only after author final freeze of digests + PDF

---

### 4.3 P3 — Observational program (deferred full draft)

**Core claim:** gate-structured program; failure modes once observables are *derived*.

#### P3 must not

| Forbidden | Ban / gate |
|-----------|------------|
| Fixed NANOGrav \([1.08,\pi]\) nHz as ITSM prediction | B13 / VOR-001 |
| Scalar polarization as guaranteed near-term PTA result without response calculation | B13 |
| JWST CO/Na I suppression as model-level falsifier from Jeans/IMF bridge | B14 |
| “Independent of acceleration formula” while still quoting withdrawn \(a_0\) derivation | B1 |
| Bullet Cluster quantitative stall as established | ledger |
| “Falsifies the \(T^3\) superfluid premise” tied to fixed nHz window | B13 |

#### P3 may

- List **theoretical** near-term falsifiers (UVIR-003, MAT-001, CBR-002, DISK-001) from CoreRecovery `10_falsifiability.tex`.  
- Describe *methodology* for PTA polarization separation *if* eigenmodes exist.  
- Treat \(\Upsilon\to 0.01\) optimizer behaviour as a **diagnostic**, not a spectral prediction.  
- Cite P1 for claim-hygiene standards.

#### P3 trigger to full draft

At least one of: VOR-001 derived spectrum with units; ASTRO-001 viable star-formation model; or a published upper limit that *maps cleanly* onto a derived ITSM template.

---

### 4.4 P4 — SPARC kinematics (optional, gated)

**Core claim:** under *declared* inputs \((a_0,\Cobs)\) and a solved or controlled disk approximation, compare to SPARC with honest noise / BIC.

#### P4 absolute rules

1. **Declare** \(a_0\) and \(\Cobs\) as inputs (phenomenological or fitted).  
2. **Never** claim both \(a_0=cH_0/2\pi\) and \(\Cobs=2/3\) as the empirical RAR normalization (**B9**).  
   - If \(a_0=cH_0/2\pi\), then \(\Cobs\simeq 1\) (or report \(a_{0,\rm eff}=\Cobs^2 a_0\)).  
   - If \(\Cobs=2/3\), then either fit \(a_0\) or set \(a_0=(9/4)a_{0,\rm emp}\).  
3. No **B1** language (“topologically fixed \(a_0\)”). Prefer “phenomenological \(a_0\)” or “input scale.”  
4. No **B15** (\(p=0.62\), SPARC measures cosmic \(H_0\)).  
5. DISK-001 before claiming morphology-independent coupling.  
6. STAT-001 matched pipeline before any global \(p\)-value.

#### P4 tone (fixed)

> Competitive once scatter and disk geometry are modelled; primary virtue is absence of *halo* free parameters under *declared* inputs — not global zero parameters or geometric derivation.

---

## 5. Cross-paper architecture

### 5.1 Companion-citation language (safe default)

> Companion papers address (i) claim hygiene and the failure of prior geometric shortcuts for \(a_0\) and \(C_{\rm obs}\) [P1], (ii) free-field Casimir stress and free-field backreaction limits on rectangular \(T^3\) [P2], and (iii) a gate-structured observational program [P3]. None of these papers claims a completed multi-tension cosmology. Archives: GitHub / Zenodo DOI …

### 5.2 Forbidden companion-citation language

Do **not** write:

- “Using the geometric invariants established in Paper I …”  
- “With \(a_0\) and \(C_{\rm proj}\) fixed by topology as in Paper I …”  
- “Building on the zero-parameter \(H_0\) prediction of Paper II …” (unless CBR-002+ genuinely delivers and is peer-accepted)

### 5.3 Shared assets

| Asset | Path |
|-------|------|
| Claim ledger | `Theory/Core/ITSM_Claim_Migration_Ledger.csv` |
| Recovery plan / gates | `Theory/Core/ITSM_Core_Recovery_Plan.md` |
| P1 reconstruction | `papers/P1-Scale-Matching-Reconstruction/` |
| CBR-001 | `Analysis/Casimir/CBR-001/` |
| Correct \(T^3\) figure script | `Scripts/itsm_t3_fundamental_domain.py` |
| **Do not use as \(T^3\)** | `Scripts/itsm_3d_toroidal_manifold.py` (doughnut = \(\Ttwo\)) |
| Legacy v11 synthesis | Provenance only; not claim authority |

### 5.4 Style rules (every paper)

1. Abstract ≤ strongest claim status on the post-referee table.  
2. **Ban-list review** before freeze (Sec.~0.1).  
3. Explicit Limitations section.  
4. Historical v11 numbers only under “withdrawn / historical.”  
5. Physical vs comoving \(L\) labelled every time.  
6. Cubic vs rectangular vs twisted stated every time topology appears.  
7. `hyperref` with `hidelinks` (or equivalent) for submission PDFs.  
8. No “resolves all tensions.”

### 5.5 Code availability block

```
Code and data availability. Pipelines and the claim-migration ledger are
archived at https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
and Zenodo DOI 10.5281/zenodo.18808348. Withdrawn geometric shortcuts are
documented in the P1 reconstruction note; live numerical claims must cite
their gate or pipeline explicitly.
```

---

## 6. Journal and submission tactics

| Paper | Primary framing | Avoid |
|-------|-----------------|-------|
| P1 | Reconstruction / EFT hygiene / no-gos | “Geometric origin of \(a_0\)” title |
| P2 | Mechanism + negative free-field cosmology result | Letters demanding miracle \(H_0\) |
| P3 | Methods / program paper after gates | Premature ApJL with fixed nHz |
| P4 | Empirical methods + model comparison | “Validates dark-matter-free cosmology” |

**arXiv:** P1 `gr-qc`; P2 `gr-qc` + `hep-th`/`astro-ph.CO`; P3–P4 as appropriate later.

---

## 7. Master timeline (revised)

```
Now          P1 reconstruction frozen as claim firewall
Month 0–2    Draft + submit P2 (Casimir); ban-list review mandatory
Month 2–6    UVIR-003 / MAT-001 / CBR-002 / DISK-001 gates
Month 6+     Reassess P3 only if a derived observable exists
Later        P4 only after DISK-001 + STAT-001 + RAR-normalization honesty
Indefinite   Full multi-scale synthesis only after reconstruction chain
             or permanent abandonment of geometric a0/C_obs claims
```

**Do not** wait for P1 journal acceptance to start P2: P2 is independent and higher integrity as a numerical paper.

---

## 8. Contingencies

| Event | Response |
|-------|----------|
| Referee asks P2 to use “Paper I geometric \(a_0\)” | Refuse; cite P1 reconstruction / ban list |
| Pressure to restore \(H_0=72.97\) in P2 abstract | Refuse; offer CBR-002 roadmap |
| CBR-002 later finds driven attractor | New paper **P2b**, not silent P2 correction |
| Reconstruction chain closes | New paper **P1b** (derivation); update this plan; un-ban only with explicit checklist |
| Someone reintroduces doughnut \(T^3\) figure | Block release; regenerate from `itsm_t3_fundamental_domain.py` |
| P4 draft uses both \(\Cobs=2/3\) and \(a_0=cH_0/2\pi\) as RAR | Reject draft until **B9** fixed |

---

## 9. Pre-submission ban-list checklist (copy into every paper repo)

```
[ ] No circulation-quantization derivation of a0
[ ] No (L, Γ=cL, ω=H0) consistency claim
[ ] No cubic E1 L=c/H0 as Planck-safe
[ ] No L_phys(t)=c/H(t) without moduli dynamics
[ ] No c/H as causal horizon without citation/qualification
[ ] No Tr(h)/Tr(γ)=2/3 ⇒ C_obs
[ ] No C_obs=2/3 as universal geometric coupling
[ ] No dual a0=cH0/2π + C_obs=2/3 as empirical RAR
[ ] No doughnut labelled T3
[ ] No underived O((r/L)^2) as error bar
[ ] No 13/12 or 72.97 as live prediction
[ ] No [1.08,π] nHz as derived prediction
[ ] No JWST IMF derivation as model falsifier
[ ] No SPARC p=0.62 or SPARC-H0 cosmology
[ ] No “zero free parameters” / “all tensions”
[ ] Companion cites do not re-inflate P1 geometric story
```

---

## 10. Document control

| Version | Date | Note |
|---------|------|------|
| 0.1 | 2026-08-01 | Initial selective plan vs v12 ledger |
| 0.2 | 2026-08-01 | **Post-referee firewall:** ban list B1–B16; P1 reconstruction; P2–P4 cannot re-inflate withdrawn geometric claims |
| 0.3 | 2026-08-01 | Clarified: B1–B16 ban **paper packaging only**, not research routes / identity pillars (see master plan) |

**Authority order when conflicts arise:**  
For **paper wording:** (1) Sec.~0 ban list of this document → (2) claim ledger → (3) P1 reconstruction.  
For **what research may pursue:** master research plan identity + buckets first (untested routes stay Open).
