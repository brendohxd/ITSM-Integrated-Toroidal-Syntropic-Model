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
