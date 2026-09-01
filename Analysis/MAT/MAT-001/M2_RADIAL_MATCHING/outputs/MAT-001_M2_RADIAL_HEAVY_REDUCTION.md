# MAT-001 M2 radial/heavy-mode reduction

**Calculation:** `PASS_CHEAP_SYMBOLIC_SCREEN`  
**Disposition:** `REJECT_MINIMAL_M2_CLASSES_SOFT_RESIDUE_NOT_DERIVED`  
**MAT-001:** `BLOCKED` · **V:** `NOT_COMPUTED` · **K_Q:** `NOT_DERIVED`

## Result

The live parent contains the finite-density condensate amplitude, but its
declared matter action couples to the separate force scalar and does not export
a radial-mode matter source in the live same-chart quadratic bundle. The live
M2 route therefore hits its first kill criterion: the required static radial
source is absent.

Two minimal controlled extensions were tested without empirical inputs.
Derivative mixing preserves a massless force mode but makes the induced soft
matter vertex vanish as momentum squared, leaving only a contact response.
Nonderivative mixing lifts the massless force mode. Tuning a counterterm to
restore it produces

`g_phys/sqrt(Z_phys) = -g_sigma*mu_mix/(sqrt(Z_sigma)*sqrt(Z_psi*Z_sigma*m_sigma_sq**2 + mu_mix**2))`,

which retains independent `mu_mix`, `g_sigma`, `Z_sigma`, `m_sigma_sq` and
`Z_psi`. A direct force-scalar matter vertex gives `g_psi/sqrt(Z_psi)`, which is
an input rather than a radial-mode prediction.

This rejects the tested minimal M2 action classes as a derivation of `V`. It
does not reject every possible symmetry-locked nonlinear completion.
