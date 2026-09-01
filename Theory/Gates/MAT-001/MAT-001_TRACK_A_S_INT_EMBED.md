# MAT-001 Track-A $S_{\rm int}$ embed and $d,h$ export

**Status:** `PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL`  
**Host:** `R2_TRACK_A_FORCE_PHONON` · `SELECTED_CONDITIONAL`  
**$S_{\rm int}$:** `EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST`  
**Track-A $d,h$:** `EXPORTED_CONDITIONAL_ON_TRACK_A_HOST`  
**Free-sector $d,h$:** `NOT_EXPORTED`  
**MAT-001:** **BLOCKED**  
**V:** **NOT_COMPUTED**  
**$K_Q$:** **NOT_DERIVED**  
**Stage 4A:** **CLOSED**  
**Physics pass:** `false`

## Purpose

Select Track-A as the Conditional live force host, embed the declared matter
interaction on that host, and export matter-channel source covectors without
claiming numeric matching or free-sector identification.

## Host and map

- Force field: $\psi=\psi_{\rm bar}+\pi$ (Track-A gauge)
- Conditional map: IR $\psi$ is the Track-A force phonon (force role only)
- **Not** free-sector $(R,\delta\rho,\vartheta)$
- **Not** a completed join with full $g+U+\Phi+$alignment

## Interaction and export

\[
S_{\rm int}\supset\int(-C_m\rho_b\psi),\qquad
L_{\rm int,\pi}=-C_m\rho_b\pi.
\]

| Object | Track-A host export |
|---|---|
| dynamical $x$ | $(\pi)$ |
| constraints $z$ | $(\delta N,\beta)$ recorded |
| $d$ | $(-C_m)$ |
| $h$ | $(0,0)$ |
| time-kinetic $K$ template | $K_Q$ (symbolic) |
| $\lvert g_{\rm can}\rvert$ form | $C_m/\sqrt{K_Q}=V$ (form only) |

Free-force Track-A constraint sources quadratic in $\dot\pi$ are **not**
matter $d,h$; joining free-force $B,C$ with matter sources remains later.

## Decision

Matter channel $d,h$ now exist on a selected Conditional force host. Numeric
$V$ is still forbidden until $K_Q$ (or an invariant residue) is derived.
MAT remains blocked; Stage 4A stays closed.

## Reproduction

```text
python -B Analysis/MAT/MAT-001/TRACK_A_S_INT/mat001_track_a_s_int_embed_audit.py
```

```text
STATUS: PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL
SHA-256: EB4D07370A7FD007C68051FFD0A10E03BB0770AE957826128283C25C90E519C8
```

## Serial next

Derive $K_Q$ (or the invariant on-shell residue) on this host under explicit
Conditional scope, **or** join free-force $B,C$ / free-sector ADM only under
a declared multi-sector chart.
