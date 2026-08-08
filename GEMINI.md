# ITSM Scientific Integrity Rules

## 1. Zero-Tolerance for Fabricated Results
You must NEVER fabricate, hallucinate, or "smuggle" results, metrics, or data. If an analysis pipeline or script produces a result (e.g., a $\chi^2$ value, a simulation output), you must report the **exact measured result**.
- Do NOT artificially invent a "filtered" or "high-fidelity" subset of data to artificially lower $\chi^2$ values unless the script explicitly performs that filtering and outputs that exact number.
- Do NOT claim a script ran a full, non-linear numerical solver if it only ran a cheap algebraic proxy.

## 2. No Post-Hoc "Derivations" of Constants
Do NOT reverse-engineer mathematical boundaries to hit empirical targets. For example, do not assert $L = 2\pi c/H_0$ strictly to land on $a_0 = c H_0 / 2\pi$ without independent, rigorous physical justification. A numerical coincidence is not a derivation.
- Always check the **dimensional consistency** of any derived vacuum expectation values (VEV) or constants (e.g., $f$ must have mass dimension 1).
- If an action underdetermines a parameter, report it as underdetermined. Do not force a fake resolution to close a gate.

## 3. Strict Honesty Principle
The core philosophy of the ITSM project is "Honesty is a credibility asset." It is vastly superior to report that a theory fails a test (e.g., failing Cassini bounds, yielding a high $\chi^2$) than to fake a success. If a calculation destroys the model, log the destruction accurately.
