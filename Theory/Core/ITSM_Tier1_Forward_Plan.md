# ITSM tier-1 forward plan (hurdles 1–7)

**Branch:** `recovery/v12-core-architecture`  
**Opened:** 2026-08-06  
**Standard:** physics tier-1 / peer-review bar  
**Authority:** Master Research Plan; Stage 5 `HOLD_TIER1_CLOSURE`; dual-status discipline  

**Rule:** Lane A (Derived) never uses Lane B (Conditional) outputs as substitutes.  
Conditional work may run in parallel for methods only.

---

## Current baseline (do not re-litigate)

| Item | Status |
|---|---|
| Manuscript | α.11 frozen Tier-1 hold |
| UVIR Stage 5 | `HOLD_TIER1_CLOSURE` |
| \(V\) / \(K_Q\) | `NOT_COMPUTED` / `NOT_DERIVED` |
| MAT PASS | forbidden |
| Stage 4A | closed |
| Track-A Conditional kit | form-complete (host, \(S_{\rm int}\), \(d,h\), symbolic \(K\), join map) |
| \(K_Q\) dig | no ready numeric path |
| Conditional branch | open dual-status only |

---

## Plan overview

| Step | Hurdle | Goal | Exit when… | Depends on |
|---|---|---|---|---|
| **H0** | Process hygiene | All evidence on remote branch | clean tree, push current audits | — |
| **H1** | No Derived \(K_Q\) / absolute \(C_m\) | Parent-action or residue path that can supply absolute coefficients | numeric \(C_m\) and \(K_Q\), **or** numeric residue \(V\), **or** documented incompleteness of a named parent action | H0 |
| **H2** | Chart-fixed vs invariant | Prove redefinition safety of the matched object | invariant identity under \(\psi\to s\psi\) (and documented chart) | H1 form |
| **H3** | Stage 4A lock | Reopen only under matched invariant | Stage 4A reopen contract all true; causality + cutoff re-eval recorded | H1+H2 Derived |
| **H4** | M2 IR control | Relevant IR complex-quartet control or permanent exclude-with-scope | M2 tier1_met or permanent exclude audited as not claimed | H3 domain |
| **H5** | M7 / MAT packaging | MAT PASS only after UVIR tier-1 + checklist | `mat001_pass` only with Derived \(V\)/`C_{\rm obs}` path + ledger | H1–H4, Stage 5 PASS |
| **H6** | Sector joins | Matter + free-force + multi-sector only if declared | join status explicit; no silent free-sector≡Track-A | parallel to H1–H3 |
| **H7** | Process hygiene (ongoing) | Dual-status docs, queue, SHA sidecars, no path leaks | every checkpoint dual-run + docs in same commit | every step |

**H0 is immediate hygiene; H7 is continuous. Science critical path is H1 → H2 → H3 → H4 → H5. H6 is parallel fail-closed join work.**

---

## H0 — Process hygiene (start now)

**Do**
- Commit and push: Track-A join readiness, tier-1 peer-review readiness, plan file, queue/README updates.
- Ensure remote is the evidence root for peer review.

**Exit:** `git status` clean; origin tip includes latest audits.

---

## H1 — Derived \(K_Q\) / absolute \(C_m\) (or residue \(V\))

**Problem:** Track-A has form \(d=(-C_m)\) and symbolic \(K_Q\); dig found no ready numeric path.

**Selected Derived route (primary):**  
**Parent-action matching** — one parent kinetic \(Z_\phi\) and coupling \(g_\phi\) with declared map to Track-A \(\pi\), inducing  
\(C_m=g_\phi/f_\phi\), \(K_Q=Z_\phi/f_\phi^2\), \(V=g_\phi/\sqrt{Z_\phi}\).

**Backup Derived route:**  
**Direct residue** — compute on-shell invariant vertex residual without quoting bare \(K_Q\) (R2 identity), if parent dynamics allow.

**Forbidden as Derived:** R1 \(k_Q\sim 1\), R3 incomplete residue, Conditional samples, free-sector paste.

### H1 work packages

| ID | Task | Deliverable |
|---|---|---|
| H1.1 | Declare selected parent-action chart and map to Track-A | Executable declaration + gate note |
| H1.2 | Inventory repo for any \(Z_\phi,g_\phi,f_\phi\) or equivalent exports | Fail-closed inventory (expected: incomplete) |
| H1.3 | Attempt derivation or bound from declared \(S_\Phi+S_{\rm int}\) sources | **DONE (incomplete):** `PASS_MAT001_PARENT_ACTION_H13_INCOMPLETE_SOURCES_AUDITED` — no \(Z_\phi/g_\phi\) from declared sources |
| H1.4 | Freeze missing micro inputs as research requirements RR1–RR5 | **DONE** in H1.3 output + this plan; keep OPEN until micro matching exists |

**Exit (success):** Derived \(V\) or \((C_m,K_Q)\) with provenance SHA.  
**Exit (honest fail):** `INCOMPLETE_PARENT_ACTION_MATCHING` with non-empty missing list — **met by H1.3**.

### Frozen research requirements (from H1.3)

| ID | Requirement | Status |
|---|---|---|
| RR1 | Complete parent action with both \(Z_\phi\) kinetic and \(g_\phi\) vertex | OPEN |
| RR2 | Derive/bound \(Z_\phi,g_\phi\) or compute residue \(V\) directly | OPEN |
| RR3 | Verify \(f_\phi\) map into Track-A \(\pi\) chart | OPEN_CONDITIONAL_MAP_ONLY |
| RR4 | Alternate: \(S_\Phi\) → \(Z_\psi,\rho_\Phi\) (R3 incomplete) | OPEN_R3_INCOMPLETE |
| RR5 | Never promote \(C_m=C_{\rm IR}\), \(C_{\rm obs}\sim1\), \(k_Q\sim1\) to Derived | ACTIVE_FIREWALL |

**H1 gate for H2–H5:** blocked until RR1–RR3 close (or residue \(V\) path succeeds).

---

## H2 — Matched invariant (redefinition-safe)

**Problem:** Chart-fixed \(I_{a_0}\) is not enough for M3.

**Do**
- Once H1 supplies coefficients or residue, prove \(V\) (or \(Aq/K_Q\)) invariant under \(\psi\to s\psi\).
- Document the field/unit chart explicitly (already partially in unit-chart contract).
- Reject any “match” that depends on arbitrary \(\psi\) normalization alone.

**Exit:** executable identity checks green; invariant named in Stage 4A input contract.

---

## H3 — Stage 4A reopen under matched invariant

**Problem:** Stage 4 is permanent Conditional on M3/M6 until matched reopen.

**Do (only after H1+H2 Derived)**
1. Reopen Stage 4A under the matched invariant.
2. Re-evaluate causality (M3) with that invariant.
3. Re-evaluate physical cutoff / unitarity path (M6) with that invariant.
4. Keep optical theorem out of UVIR PASS unless separately claimed.

**Exit:** Stage 4A reopen contract conditions true; new Stage 4A evidence JSON; Stage 4A status not silently flipped without evidence.

**Hurdle if blocked:** force covariant completion / \(Y^{3/2}\) may still limit multi-sector claims — record scope.

---

## H4 — M2 IR control

**Problem:** High-\(q\) domain is partial; relevant IR complex-quartet HOLD remains.

**Do**
- Either derive control of the relevant IR response in the claim domain, **or**
- Permanent exclude list: “not claimed for tier-1 stability” with machine audit (already partial in weak-coupling domain).

**Exit:** M2 `tier1_met: true` **or** documented permanent exclude such that tier-1 claim domain does not require that IR slice.

**Do not** claim full stability while IR HOLD is unresolved and still inside the claim domain.

---

## H5 — M7 / MAT packaging firewall

**Problem:** Pressure to issue MAT PASS after form kit.

**Do**
- Keep `allows_MAT001_PASS: false` until: UVIR tier-1 closed (or Master Plan handoff explicitly allows MAT-only Derived — currently not for full PASS), Derived \(V\)/`C_{\rm obs}` path, checklist complete.
- Claim ledger + Selective Publishing ban-list update only on real PASS.
- Dual-status: Conditional DISK/STAT allowed under explicit labels.

**Exit:** either honest MAT PASS with full checklist, or continued BLOCKED with clear handoff note.

---

## H6 — Sector joins (parallel, fail closed)

**Problem:** Matter-only static channel form-ready; free-force J2 is velocity-quadratic; full multi-sector J2 not assembled.

**Do**
- Keep operational channel = matter-only static Track-A for Conditional/form work.
- Optional: extended projection identity for velocity-mixed constraints (declare extension, do not erase residual).
- Optional: multi-sector ADM join only after force completion declarations.

**Exit:** join statuses remain accurate; no free-sector≡Track-A without map.

---

## H7 — Continuous process hygiene

Every checkpoint:
- dual-run byte-identical JSON + SHA sidecar  
- no absolute paths  
- claim firewall  
- gate note + worklog + changelog + queue  
- dual-status wording in README/site if status changes  
- no frozen manuscript overwrite  

---

## Lane B (parallel, never substitutes H1–H5)

| Allowed | Forbidden |
|---|---|
| Conditional dual-status samples | Packaging as Derived \(V\)/`K_Q` |
| DISK/STAT methods under Conditional \(C_{\rm obs}\) | Claiming MAT PASS |
| Paper presentation / site | α.12 freeze as UVIR closed |
| Identity scaffolds (TOP/VOR/WAK/RES) | Using them to unlock M3/M6 |

---

## Immediate execution order (this sprint)

1. **H0** — commit/push outstanding audits + this plan.  
2. **H1.1–H1.2** — parent-action matching declaration + repo inventory (start now).  
3. **H1.3** — derivation attempt or incompleteness PASS.  
4. Stop at H1 exit; do not open H3 without Derived invariant.  
5. H6/H7 continuous; H2 bundled with H1 success path.

---

## Success metrics

| Metric | Target |
|---|---|
| Peer-review survivability | Deny-list never violated in committed claims |
| Derived progress | One invariant with provenance, or named incompleteness |
| Hold integrity | Stage 4A closed until contract met |
| Dual status | Conditional branch samples never appear as Derived in summaries |

---

## Explicit non-goals for this plan

- Inventing numeric \(K_Q\) or \(V\)  
- Reopening Stage 4A from Conditional tables  
- Full multi-sector completion before parent matching  
- Cosmology / SPARC / \(H_0\) packaging from MAT form kit  
