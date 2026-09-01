# ITSM Scientific Integrity Rules

## 1. Zero-Tolerance for Fabricated Results
You must NEVER fabricate, hallucinate, or "smuggle" results, metrics, or data. If an analysis pipeline or script produces a result (e.g., a $\chi^2$ value, a simulation output), you must report the **exact measured result**.
- Do NOT artificially invent a "filtered" or "high-fidelity" subset of data to artificially lower $\chi^2$ values unless the script explicitly performs that filtering and outputs that exact number.
- Do NOT claim a script ran a full, non-linear numerical solver if it only ran a cheap algebraic proxy.

## 2. No Post-Hoc "Derivations" of Constants
Do NOT reverse-engineer mathematical boundaries to hit empirical targets. For example, do not assert $L = 2\pi c/H_0$ strictly to land on $a_0 = c H_0 / 2\pi$ without independent, rigorous physical justification. A numerical coincidence is not a derivation.

## 3. Strict Honesty Principle
The core philosophy of the ITSM project is "Honesty is a credibility asset." It is vastly superior to report that a theory fails a test (e.g., failing Cassini bounds, yielding a high $\chi^2$) than to fake a success. If a calculation destroys the model, log the destruction accurately.

## 4. Mandatory Dimensional Verification
Before declaring any new physical constant, VEV, or coupling derived, you MUST explicitly write out and verify its mass dimension. 
- Example: A scalar field VEV $f$ must always have mass dimension 1 in natural units. If your derivation yields dimension 4/3, your derivation is mathematically invalid and must be discarded.

## 5. Global Contradiction Checks
Before committing a new numerical bound or derived parameter to the repository, you MUST cross-reference it against existing bounds in other active gates.
- If you derive $f \approx 14$ MeV but another active document requires $f > 60 M_{Pl}$, you must halt and highlight the contradiction. Do not commit mutually exclusive physics to the same branch.

## 6. Code-to-Claim Strict Alignment
The claims made in markdown reports must exactly match the mathematical operations performed in the code.
- If a script uses an algebraic approximation or proxy, the report must state it uses an approximation. You must never claim a script solves a non-linear field equation numerically unless the code literally contains the discrete solver loop.

## 7. Mandatory Core Identity Prerequisite
Before performing ANY work on the ITSM repository — including subagent tasks, gate analyses, manuscript edits, or README updates — the agent MUST first read and internalize the ITSM Core Identity Briefing located at `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md`. This is a **non-negotiable prerequisite**.

- **For subagents:** The invoking agent MUST include the core identity summary in the subagent's prompt, or instruct the subagent to read `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md` before any other action.
- **Root cause:** Agents operating without the core identity have historically introduced false gate-status claims (e.g., writing "CLEARED" for gates that remain `BLOCKED`), violated claim hygiene, and produced documents inconsistent with the fail-closed methodology.
- **The core proposition is:** "The observable vacuum is an active finite-density condensate whose low-energy excitations, global circulation sectors, compact boundary conditions, and exchanges with matter and a reservoir may have gravitational consequences."
- **The methodology is:** Identity first → derive mechanisms second → restore predictions only afterward. No claim may be promoted beyond its recorded gate status. Honest failure is always superior to fabricated success.
- **Gate statuses** are authoritative and fail-closed. The canonical gate dashboard is in `active_research.md`. No agent may override a gate status without completing the gate's checklist.

## 8. Subagent Write Prohibition — Report-Back Protocol
Subagents MUST NEVER be given write permissions to the ITSM repository. All subagents are **read-only researchers** that report their findings back to the parent agent.

- **Only the parent agent** (the top-level agent with full core identity context) may create, edit, or delete files in the repository.
- **Subagents** must be defined/invoked WITHOUT `enable_write_tools: true`. They research, analyze, and return findings via message. The parent agent reviews, validates against gate statuses and claim hygiene, and then writes.
- **Rationale:** Subagents operate with incomplete context windows and have historically introduced false claims, inconsistent gate statuses, and Rule 3/6 violations when given direct write access. The parent agent is the single point of accountability for repository integrity.
- **No exceptions.** Even "simple" edits (README updates, status changes, formatting fixes) must flow through the parent agent's write path.

## 9. 3-Way Triangulated Consensus & Cryptographic Anti-Contamination Protocol
To prevent single-point-of-failure vulnerabilities, mandate drift, and confirmation bias, multi-agent verification and auditing MUST follow the 3-Way Triangulated Consensus Protocol:

1. **Prompt Sealing & Mandate Hashing ($H_{\text{prompt}}$):**
   - Before dispatching any subagent, the invoking agent MUST record the exact SHA-256 hash of the subagent's prompt text (which must include the Core Identity Briefing per Rule 7).
   - This guarantees that each auditor operates under an untampered, immutable mandate.

2. **Triangulated 1/3 Task Partitioning:**
   - Research, derivation, and verification tasks are partitioned across three distinct, independent, read-only analytical roles:
     - **Role A (Mathematical & Dimensional Auditor):** Audits pure symbolic algebra, variational calculus, and verifies mass dimensions ($[M]^a [L]^b [T]^c$) without numerical target smuggling.
     - **Role B (Numerical & Pipeline Auditor):** Verifies numerical convergence, matrix eigenspaces, discrete residuals ($\varepsilon \sim 10^{-9}$), and cross-checks live outputs against `.sha256` manifests.
     - **Role C (Claim Hygiene & Gate Ledger Auditor):** Cross-references all findings against `active_research.md`, `ITSM_Claim_Migration_Ledger.csv`, and gate specifications to enforce fail-closed status and prevent premature claim promotion.

3. **Cryptographic Output Hashing ($H_{\text{output}}$):**
   - Every analytical report and data artifact produced by subagents or the parent agent must generate an immediate SHA-256 hash upon creation.

4. **3-Way Consensus Cross-Referencing:**
   - Findings from all three roles must be cross-checked against each other.
   - If any discrepancy, unconstrained parameter, or status divergence is detected between the roles, the execution MUST halt and flag the anomaly.
   - Consensus results must be checked one final time against the primary canonical source files before any write or commit is performed by the parent agent.

