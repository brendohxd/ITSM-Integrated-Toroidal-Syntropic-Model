# MAT-001 R4 signed residue contract

**Date:** 2026-08-07

**Scoped status:** `PASS_MAT001_R4_SIGNED_RESIDUE_CONTRACT_SCOPED`

**Global status unchanged:** MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`; `V` `NOT_COMPUTED`; `K_Q` `NOT_DERIVED`; Stage 4A `CLOSED`.

**Authority:** Implements R4 of `MAT-001_TIER1_REMEDIATION_ADDENDUM_2026-08-07.md`. This is a sign-and-orientation contract for symbolic matching, not a numerical matter-sector match.

## 1. Fixed convention

The reduced source convention is

\[
 L_{\rm src}=\rho_b\,c_{\rm eff}^{T}x,
 \qquad c_{\rm eff}=d-BC^{-1}h.
\]

For the R3 conformal matter action in the normalized comoving weak-field limit,

\[
 d=(-C_m),\qquad h=(0,0),\qquad c_{\rm eff}=(-C_m).
\]

For a physical mode `u` with positive kinetic norm,

\[
 g_{\rm can}=\frac{c_{\rm eff}^{T}u}{\sqrt{u^{T}Ku}}.
\]

With the one-field orientation anchor `u_psi=+1`,

\[
 g_{\rm can}=-\frac{C_m}{\sqrt{K_Q}}=-V_{\rm signed},
 \qquad V_{\rm signed}=\frac{C_m}{\sqrt{K_Q}}.
\]

The minus sign belongs to the declared source convention. It is not removable by taking an absolute value.

## 2. Admissible domain

A signed matching candidate must satisfy

- `C_m` real, finite and nonzero;
- `K_Q` real, finite and strictly positive;
- every constraint matrix used in the Schur reduction invertible in the declared domain;
- a named physical-mode orientation transported through every basis change.

Both signs of `C_m` are admissible. Zero is not an identified nonzero matter-force residue and therefore cannot satisfy this matching contract. A decoupled mode may have zero projection, but that is a negative matching result rather than a value of the required nonzero residue.

## 3. Basis and orientation behavior

For an orientation-preserving one-field rescaling `psi_prime=s psi` with `s>0`,

\[
 K_Q' = K_Q/s^2,\qquad C_m'=C_m/s,
 \qquad V_{\rm signed}'=V_{\rm signed}.
\]

For a general field-basis map `x=R y`, the source is a covector and the mode is a vector:

\[
 K_y=R^T K R,\qquad c_y=R^T c,\qquad u_y=R^{-1}u.
\]

The projected signed coupling is invariant when all three objects are transported consistently. Eigenvectors have an arbitrary algebraic sign, so the physical orientation must be anchored. Under an actual orientation reversal `u -> -u`,

\[
 g_{\rm can}\rightarrow-g_{\rm can}.
\]

Therefore `abs(g_can)` and `V^2` erase information required by the signed contract. They may be reported only as supplementary magnitude diagnostics.

## 4. Executable controls

The repaired chain enforces the contract at four levels:

1. J1 rejects zero/nonfinite coefficients, admits either nonzero sign, and verifies orientation reversal of `g_phi/sqrt(Z_phi)`.
2. J2 transports `K`, `c_eff` and `u` covariantly, and verifies `g(-u)=-g(u)`.
3. `S_INT_DH_EXPORT` exports signed `g_can=-C_m/sqrt(K_Q)` and rejects sign-flipped or magnitude-only substitutions.
4. Track-A and RR2 retain the signed source through the projected pathway and carry the `u_psi=+1` orientation anchor.

Mutation cases cover sign reversal, magnitude-only replacement, zero/nonfinite coefficients, omitted constraint dressing and inconsistent basis transport.

## 5. Scientific boundary

This scoped PASS means the symbolic evidence chain no longer loses the sign of the matter residue. It does not determine `C_m`, derive a numerical `K_Q`, compute numerical `V`, establish a microscopic UV completion, prove stability, or reopen Stage 4A. Those remain independent open gates.

## 6. Reproduction

Run the local symbolic exporters from the repository root, then verify each JSON against its adjacent SHA-256 sidecar. The consolidated remediation runner is:

```powershell
python -B Analysis/MAT/MAT-001/REMEDIATION/mat001_tier1_remediation_runner.py
```

A successful run must still end with `MAT=BLOCKED`, `V=NOT_COMPUTED`, `K_Q=NOT_DERIVED`, and `Stage4A=CLOSED`.
