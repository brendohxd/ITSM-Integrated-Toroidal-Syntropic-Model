# VOR-001 S2b — Parent \(S_\Phi\) template (hardened, not UVIR condensate)

**Branch:** `recovery/v12-core-architecture`<br>
**Status:** `OPEN_SCAFFOLD_ONLY`<br>
**physics_pass:** **false**<br>
**Hold:** `HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED`<br>
**Subgate (template only):** `PASS_VOR001_S2B_PARENT_ACTION_TEMPLATE_DECLARED`<br>

## Exact action convention

\[
\Phi = \frac{\rho}{\sqrt{2}}\,e^{i\Theta},\qquad
|\Phi|=\frac{\rho}{\sqrt{2}},\qquad
\rho=\sqrt{2}\,|\Phi|.
\]

Flat fixed-background template (\(D_\mu=\partial_\mu\); **no** aether):

\[
\mathcal L = -g^{\mu\nu}(\partial_\mu\Phi)^\ast(\partial_\nu\Phi) - V(|\Phi|).
\]

Potential (two equivalent writings; machine-checked equality):

\[
V_\rho(\rho)=\frac{\lambda}{4}(\rho^2-v^2)^2,\qquad
V_{|\Phi|}(|\Phi|)=\lambda\Bigl(|\Phi|^2-\frac{v^2}{2}\Bigr)^2.
\]

Polar kinetic decomposition:

\[
|\nabla\Phi|^2 = \tfrac12|\nabla\rho|^2 + \tfrac{\rho^2}{2}|\nabla\Theta|^2.
\]

Static spatial energy density = S1 toy integrand.

## Machine-checked identities

- \(V_{|\Phi|}(\rho/\sqrt{2})=V_\rho(\rho)\) (no factor-of-two ambiguity)
- Polar kinetic decomposition
- Static reduction to S1 toy energy
- Stationary minimum at \(\rho=v\)
- Amplitude mass \(m^2=V''(v)=2\lambda v^2\)
- Massless Goldstone (potential independent of \(\Theta\))
- Quadratic Hamiltonian with consistent phase convention
  \(H_\Theta=p_\Theta^2/(2v^2)+(v^2/2)|\nabla\Theta|^2\)
- Imported S2 amplitude mass equals declared \(2\lambda v^2\) (not mere positivity)

## Negative controls (must raise)

`lambda<=0`, `v<=0`, non-finite parameters, inconsistent normalization, missing/malformed S2 input.

## Reproduce

```powershell
python Analysis\VOR\VOR-001\vor001_s2b_parent_action_template.py
# expect: PASS_VOR001_S2B_PARENT_ACTION_TEMPLATE_DECLARED
# physics_pass: False
# HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED
```

## Explicit non-claims / holds

- **Not** the ITSM UVIR condensate action
- No UVIR validation; no aether/frame coupling
- No defects, resonance, SWNT numbers, \(a_0\), \(\Cobs\), PTA, force claims
- No VOR research-gate PASS
