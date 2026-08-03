# VOR-001 — Gate specification (SWNT principle → complex condensate on \(T^3\))

**Document type:** Open gate specification (research scaffold)
**Gate ID:** VOR-001
**Status:** `OPEN_SCAFFOLD_ONLY`
**Date:** 2026-08-03
**Branch:** `recovery/v12-core-architecture`
**Claim restoration:** **none** — founding intuition only; no Derived physics claimed

---

## 0. Executive question

**Q0.** Can the retained Phase-2 **SWNT principle** — ordered structure through
**winding**, **circulation**, **resonance**, and **finite-density** ordering —
be realized as a **consistent, energy-accounted sector** of a **complex
condensate** \(\Phi\) on **compact \(T^3\)** (or twisted flat BC), with:

1. local phase dynamics cleanly separated from global winding sectors;
2. topological integers separated from Wilson coefficients;
3. boundary conditions separated from force laws;
4. defect cores (\(\rho=0\)) separated from smooth circulation;
5. no automatic packaging into \(a_0\), \(\Cobs\), cosmology, or lensing?

**If yes:** produce actions, energy accounting, and staged tests that pass under
declared domain (later Derived/Conditional upgrades).
**If no:** document falsifiers and demote or retire the pillar with written
reason — **not** by recycling old packaging failures.

---

## 1. Principle retained vs programme rejected

### 1.1 Retained (Open identity)

| Element | Content |
|---------|---------|
| Winding | Quantized phase holonomy on non-contractible cycles of \(T^3\) |
| Circulation | Line integral of superfluid / condensate velocity around loops |
| Resonance | Preference for ordered spectral / geometric alignments (to be *defined*, not assumed as PTA band) |
| Finite density | Homogeneous \(\rho_0\neq 0\) background admitting phonons and defects |

### 1.2 Rejected packaging (do not re-import)

| Historical packaging | Disposition |
|----------------------|-------------|
| Lunar SWNT proxy / impossible field strengths as “proof” | **REJECTED_PACKAGING** (Bucket A/B) |
| Topology alone / circulation quantizes \(a_0\) | **Rejected as derivation**; \(a_0\sim cH_0\) only as **named DSM** elsewhere if used |
| \(a_0\equiv cH_0/2\pi\) as circulation quantum | **Rejected** as VOR derivation path |
| \(C=2/3\) or \(\Cobs=2/3\) from vortex geometry | **Rejected** unless independently rederived in MAT/UVIR |
| Free-field Casimir \(13/12\) attractor | **Rejected** (CBR-001 baseline; not VOR) |
| Fixed NANOGrav \([1.08,\pi]\) nHz from \(a_0\) units | **Rejected** packaging; eigenmodes later Open under PERT/VOR only if derived |
| Automatic lensing / SPARC / \(H_0\) claims from winding | **Forbidden** |

---

## 2. Declared degrees of freedom

### 2.1 Field content (candidate)

Complex order parameter (architecture §3.2):

\[
\Phi = \frac{\rho}{\sqrt{2}}\, e^{i\Theta},
\qquad
\rho\ge 0,\quad \Theta\sim\Theta+2\pi.
\]

Optional decompositions:

| Object | Type | Role |
|--------|------|------|
| \(\rho(x)\) | local field | amplitude; \(\rho=0\) at defect cores |
| \(\vartheta(x)\) | local field | fluctuation phase about a background |
| \(\mu\) | chemical potential / charge-setting | finite-density selection (mechanism Open) |
| \(U^\mu\) | plenum frame (separate sector) | **not** identified with \(\partial\Theta\) without parent action |
| \(\psi\) | IR force phonon (UVIR) | **not** a VOR DOF |

### 2.2 Global / topological sectors (not local fields)

On rectangular \(T^3\) with side lengths \(L_i>0\):

\[
\oint_{\gamma_i} d\Theta = 2\pi n_i,
\qquad
\mathbf{n}=(n_1,n_2,n_3)\in\mathbb{Z}^3.
\]

| Object | Type | Notes |
|--------|------|-------|
| \(\mathbf{n}\) | topological integers | invariant under continuous local deformations with \(\rho>0\) |
| Homotopy class of maps \(T^3\to S^1\) | sector label | winding sector |
| Defect worldlines / vortex filaments | singular loci | \(\rho=0\); linking with \(\mathbf{n}\) via Stokes-type relations |

**Rule:** \(\mathbf{n}\) is **never** a free Wilson coefficient. Coefficients live in
\(S_\Phi[\rho,\Theta;\text{params}]\); integers label **sectors** of the configuration space.

### 2.3 Smooth circulation vs defects

| Regime | Condition | Circulation |
|--------|-----------|-------------|
| Smooth superflow | \(\rho>0\) everywhere on \(T^3\) | \(\mathbf{v}\propto\nabla\Theta\); winding still \(\mathbf{n}\in\mathbb{Z}^3\) |
| Defectful | \(\rho=0\) on cores | vorticity supported on cores; phase multi-valued |

Both regimes are **in scope for research**; neither automatically sources \(\psi\).

### 2.4 Twisted boundary conditions (TOP interface)

Twisted / shift-identified flat 3-manifolds (architecture preference for
recirculating stabilisers) are **TOP-001 territory** for moduli and
identification maps. VOR-001 may *use* a declared BC class as input:

| BC class | VOR use | Forbidden inference |
|----------|---------|---------------------|
| Periodic rectangular \(T^3\) | baseline holonomy lattice | force law |
| Twisted \(E_2/E_3\)-type | Conditional extension | automatic \(a_0\) or \(C\) |

---

## 3. Candidate mathematical routes (Open — not ranked as Derived)

Routes are **research options**. Choosing one is Conditional until tests pass.

### Route V1 — Madelung / superfluid hydrodynamics on \(T^3\)

- Madelung transform of a complex Klein–Gordon or Gross–Pitaevskii-type action
- Continuity + Euler with equation of state from \(V(\rho)\)
- **Pros:** clear circulation quanta \(2\pi n_i\); defect language
- **Cons:** nonrelativistic limits; matching to UVIR \(\psi\) is separate

### Route V2 — Relativistic complex scalar + finite-density background

- \(S_\Phi[\Phi,g]\) with \(U(1)\) symmetry; chemical potential or charge density
- UVIR-001 already showed **one** candidate does **not** produce spatial
  \(Y^{3/2}\) — VOR must **not** reverse that without new calculation
- **Pros:** covariant; interfaces UVIR condensate history
- **Cons:** force sector still independent (UVIR-002 split)

### Route V3 — Effective vortex filament / Ginzburg–Landau defect gas

- Core size \(\xi\), tension \(T_v\), interaction kernels on \(T^3\)
- Resonance as collective-mode spectrum of filament networks
- **Pros:** direct SWNT-principle language
- **Cons:** easy to overclaim cosmology from string network lore

### Route V4 — Spectral / Bloch resonance on compact manifold

- Laplace–Beltrami / Bogoliubov spectrum on \(T^3\) with background superflow
- “Resonance” = avoided crossings / commensurate winding–geometry ratios
- **Pros:** falsifiable numerics without packaging
- **Cons:** does not by itself supply energy-positive dynamics

### Route V5 — Twisted-bundle condensate (joint TOP+VOR)

- \(\Phi\) as section of a flat line bundle with holonomy; twisted BC
- **Pros:** aligns with Master Plan toroidal identity preference
- **Cons:** requires TOP-001 moduli action for full energy accounting

**Scaffold default for staged tests:** **V1 + V2 interface notes**, with V3/V4
as optional extensions. No route is mandatory.

---

## 4. Energy and stability requirements

Any candidate action \(S_\Phi\) (or effective defect energy \(E[\mathbf{n},\rho]\))
must eventually address:

| Requirement | Statement | Stage |
|-------------|-----------|-------|
| **E1 Finite density** | Homogeneous \(\rho_0\neq 0\) with \(V_{\mathrm{eff}}''(\rho_0)>0\) (architecture) | S1 |
| **E2 Positive energy of fluctuations** | Quadratic action about background has correct sign kinetic structure in declared frame | S2 |
| **E3 Sector energy** | Energy of winding sector \(\mathbf{n}\) well-defined mod gauge; extensive or topological tension stated | S2–S3 |
| **E4 Defect core energy** | Finite core energy density; no runaway collapse without cutoff \(\xi\) | S3 |
| **E5 No free lunch** | Total stress + exchange with other sectors conserves (CRA) when coupled | S4+ |
| **E6 Causal structure** | Characteristics / sound speed declared for hydro or relativistic modes | S2 |

**Out of Stage 0–1 scope:** full coupled UVIR+VOR stability on FRW.

---

## 5. Dependencies

### 5.1 Soft dependencies (scaffold may proceed)

| Dependency | Why soft |
|------------|----------|
| UVIR-003 full PASS | VOR is parallel identity track; force \(\psi\) not required for pure \(\Phi\) topology |
| MAT-001 | Only for matter-coupled vortex or force-from-winding claims |
| TOP-001 action | Needed for dynamical \(L_i\); fixed-\(L_i\) math templates OK first |

### 5.2 Hard dependencies (for later *Derived* VOR claims)

| Claim type | Requires |
|------------|----------|
| Dynamical shape–winding coupling | TOP-001 moduli action |
| Matter-sourced defects | MAT-001 or declared Conditional coupling |
| Observable PTA / CMB from resonance | PERT/COS + energy-positive spectrum; **not** unit assignment to \(a_0\) |
| Force-law coefficient from winding | Explicit matching gate; **default forbidden** without new derivation |

### 5.3 Explicit non-dependencies (anti-packaging)

VOR-001 **does not depend on** and **must not import as inputs**:

- lunar SWNT calibrations;
- \(H_0=72.97\), \(13/12\), dual RAR \((a_0=cH_0/2\pi,\,C=2/3)\);
- historical SPARC \(p=0.62\).

---

## 6. Staged tests

### Stage S0 — Vocabulary and separation audit (this scaffold)

| ID | Test | Pass criterion |
|----|------|----------------|
| S0.1 | DOF table written | Local vs global vs topological vs Wilson params listed |
| S0.2 | Claim firewall present | Rejected packaging enumerated |
| S0.3 | Route catalogue | ≥3 mathematical routes with pros/cons |
| S0.4 | Optional toy | If present: template-only + negative controls |

**S0 status:** satisfied by this document package when files exist on disk.

### Stage S1 — Homogeneous finite-density background (math)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S1.1 | Effective potential admits \(\rho_0\neq 0\) | **PASS** if \(V_{\mathrm{eff}}'=0\), \(V_{\mathrm{eff}}''>0\) under named \(V\) |
| S1.2 | Goldstone / phonon existence at \(\mathbf{n}=\mathbf{0}\) | **PASS** if gapless phase mode under \(U(1)\) |
| S1.3 | No smuggled force operator | **FAIL** if \(Y^{3/2}\) asserted without UVIR-class calculation |

### Stage S2 — Winding sectors without defects (smooth superflow)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S2.1 | Phase holonomy \(\oint_{\gamma_i}d\Theta=2\pi n_i\) | **PASS** if implemented and gauge-checked |
| S2.2 | Energy \(E(\mathbf{n})\) for fixed \(L_i\) | **PASS** if computed from declared action; **HOLD** if only dimensional estimate |
| S2.3 | Local \(\vartheta\) dynamics decoupled from \(\mathbf{n}\) at linear level | **PASS** if sector–fluctuation split documented |
| S2.4 | Negative control: \(\mathbf{n}=\mathbf{0}\) | **PASS** if recovers homogeneous background energy |

### Stage S3 — Defect cores

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S3.1 | Core solution \(\rho\to 0\) with finite energy per length | **PASS** / **HOLD** if only 2D toy |
| S3.2 | Linking of core vorticity with winding | **PASS** if Stokes/ Ampere relation holds numerically |
| S3.3 | Negative control: forced \(\rho\ge\rho_{\min}>0\) | **PASS** if singular vorticity disappears |

### Stage S4 — Resonance (definition required first)

| ID | Test | Pass / Hold / Fail |
|----|------|---------------------|
| S4.0 | Define “resonance” operationally (spectral / geometric / driven) | **PASS** only after definition frozen |
| S4.1 | Spectrum computation on \(T^3\) with background \(\mathbf{n}\) | **PASS** under declared operator |
| S4.2 | Negative control: no preferred PTA interval without units derivation | **FAIL** packaging if interval asserted from \(a_0\) alone |

### Stage S5 — Interface audits (not full closure)

| ID | Test | Notes |
|----|------|-------|
| S5.1 | TOP moduli fixed vs dynamical | Joint with TOP-001 |
| S5.2 | No double-counting \(U^\mu\) vs \(\partial\Theta\) | Architecture constraint |
| S5.3 | Coupling to \(\psi\) only via declared \(S_{\mathrm{int}}\) | MAT/UVIR |

---

## 7. Falsifiers

A candidate VOR construction **fails** (or must be demoted) if, under its
own declared premises:

| ID | Falsifier |
|----|-----------|
| F1 | No finite-density stable branch with \(\rho_0\neq 0\) for the chosen \(V\) |
| F2 | Winding integers continuously tunable (not \(\mathbb{Z}\)) without singular cores or topology change |
| F3 | Energy unbounded below in a winding sector at fixed charge/chemical potential |
| F4 | Local phase dynamics cannot be separated from \(\mathbf{n}\) even as an idealization (complete obstruction) |
| F5 | Only viable “predictions” recycle rejected packaging (lunar, \(13/12\), dual RAR, unit-assigned PTA band) |
| F6 | Force-law coefficients claimed from holonomy without a matching calculation |

**Non-falsifier:** UVIR-003 still IN PROGRESS — does not kill VOR scaffold.

---

## 8. Pass / Hold / Fail criteria (gate-level)

### 8.1 Scaffold pass (current target)

**PASS_SCAFFOLD** when:

- README + this GATE_SPEC exist;
- separations of §0/§2 and claim firewall §9 are explicit;
- staged test plan S0–S5 is written;
- no Derived cosmological/force claims are asserted.

### 8.2 Research pass (future — not claimed now)

Master Plan wording for TOP/VOR/WAK: *actions + energy accounting for
moduli / winding / wake.*

**PASS_VOR001_RESEARCH** (future) would require at minimum:

- declared \(S_\Phi\) or effective defect energy with E1–E4 addressed in domain;
- S2 winding-sector calculation with negative controls;
- written scientific boundary;
- ledger update **only when programme integrates** (out of scope for this scaffold authoring).

### 8.3 Hold

**HOLD** when a structural obstruction is identified (e.g. complex mode
mixing, incomplete BC class) without falsifying the principle itself.

### 8.4 Fail

**FAIL** when a falsifier F1–F6 triggers under named premises, or when the
gate is used only to re-package rejected claims.

---

## 9. Claim firewall (mandatory language)

### 9.1 Allowed claim classes under VOR-001 *now*

| Class | Examples |
|-------|----------|
| **Open** | “Winding on \(T^3\) is a candidate ordering mechanism.” |
| **Conditional** | “Under GP action \(X\) and BC \(Y\), \(E(\mathbf{n})\propto\|\mathbf{n}\|^2\).” |
| **Template-only** | Toy numerics labelled non-physical |

### 9.2 Forbidden claims under VOR-001 *now*

| Forbidden | Reason |
|-----------|--------|
| Derived \(a_0\) from circulation quanta | Master Plan: not topology-alone; DSM is Conditional elsewhere |
| Derived \(\Cobs\) or \(C=2/3\) from vortices | MAT/UVIR matching |
| \(13/12\) or \(H_0=72.97\) | Rejected packaging |
| Lunar SWNT validation | Rejected packaging |
| PTA interval from \(a_0\) unit assignment | Rejected packaging |
| Lensing / Bullet Cluster from winding sketch | Needs LEN/SCR + energy accounting |
| “SWNT principle proven” | Scaffold ≠ proof |

### 9.3 Separation checklist (reviewer paste)

- [ ] Local \(\vartheta\) vs global \(\mathbf{n}\) distinguished
- [ ] \(\mathbf{n}\in\mathbb{Z}^3\) vs Wilson parameters distinguished
- [ ] BC class vs \(\psi\) force law distinguished
- [ ] \(\rho=0\) cores vs smooth \(\rho>0\) circulation distinguished
- [ ] Founding intuition vs Derived status distinguished
- [ ] No dual RAR defaults
- [ ] No automatic cosmology

---

## 10. Suggested calculation order (when research resumes)

1. Fix BC: rectangular \(T^3\), fixed \(L_i\) (TOP dynamical later).
2. Pick Route V1 or V2 toy action; run S1 finite density.
3. Smooth winding sectors S2 + negative control \(\mathbf{n}=0\).
4. Single straight defect S3 on \(T^2\times S^1\) reduction if 3D hard.
5. Define resonance S4.0 before any spectrum packaging.
6. Only then consider TOP joint S5 or MAT coupling.

---

## 11. Optional mathematical template

See:

```text
Analysis/VOR/VOR-001/vor001_winding_template_audit.py
Analysis/VOR/VOR-001/README.md
```

Label: **mathematical-template-only**.
Negative controls: trivial winding; forced smooth \(\rho\); random non-integer
“fake holonomy” rejected.
Under-resolved winding at the sampling boundary is rejected before estimation.
**Does not** pass VOR-001 research gate.

---

## 12. Unresolved decisions (for independent review)

| ID | Decision |
|----|----------|
| U1 | Primary route V1 vs V2 vs V3 for first research pass? |
| U2 | Fixed \(L_i\) forever in VOR, or early joint TOP-001? |
| U3 | Is “resonance” spectral, geometric, or driven (S4.0)? |
| U4 | Chemical potential vs fixed charge for finite density? |
| U5 | When (if ever) to allow Conditional coupling \(\Phi\)–\(\psi\)? |
| U6 | Programme integration: update Master Plan / ledger only after review? |

---

## 13. Document control

| Version | Date | Note |
|---------|------|------|
| 0.1 | 2026-08-03 | Initial Open scaffold; research only; no claim restoration |
| 0.2 | 2026-08-03 | Independent review: explicit grid-domain validation and under-resolved-winding negative control |
