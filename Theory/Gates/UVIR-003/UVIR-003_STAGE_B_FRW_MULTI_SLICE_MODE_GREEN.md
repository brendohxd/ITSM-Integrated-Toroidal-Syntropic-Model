# UVIR-003 Stage B — FRW multi-slice kernel + mode-projected Green

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (proxy assembly; full in-in still not computed)

Subgate:
`PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

## Purpose

Advance the declared FRW in-in path by:

1. Sampling the local four-leg kernel across **multiple FRW slices** in the
   controlled high-$q$ domain (not only the initial freeze).
2. Replacing scalar endpoint $T_{\mathrm{gain}}$ with a **causal
   mode-projected two-time Green proxy** built from the existing high-$q$
   transfer singular-value history.

## Definitions

### Multi-slice kernel

For fixed-comoving high-$q$ labels $q_0/H|_{\mathrm{init}}\in\{10,100\}$,

\[
\frac{q_{\mathrm{phys}}(t)}{H(t)}
=
\frac{q_0}{H_0}\,\frac{H_0 a_0}{H(t)\,a(t)},
\]

and

\[
K_{\mathrm{nn}}(t)
=
\text{nearest-neighbour }
\bigl(\texttt{exchange\_plus\_reduced\_contact}\bigr)
\text{ at channel } q_{\mathrm{phys}}/H.
\]

### Mode-projected two-time Green proxy

On the high-$q$ support of the primary transfer mode ($q_0/H=100$):

\[
G_{\mathrm{mp}}(t_{\mathrm{out}},t_{\mathrm{in}})
=
\begin{cases}
K_{\mathrm{nn}}(t_{\mathrm{in}})\,
\dfrac{\mathrm{SV}(t_{\mathrm{out}})}{\mathrm{SV}(t_{\mathrm{in}})}
& t_{\mathrm{out}}\ge t_{\mathrm{in}}\\[0.6em]
0 & t_{\mathrm{out}} < t_{\mathrm{in}}
\end{cases}
\]

where $\mathrm{SV}$ is the largest endpoint-normalized singular value of the
gauge-invariant fixed-comoving transfer integrator.

At equal times, $\mathrm{SV}$ ratio $=1$, so the Green diagonal recovers
the local multi-slice kernel.

## Pass criteria (this subgate)

1. FRW branch + local four-leg kernel + packet proxy prior PASS available.  
2. ≥ 6 high-$q$ multi-slice kernel hits finite.  
3. Causal Green grid finite; diagonal matches local $K$.  
4. Scientific boundary written (no S-matrix / unitarity / MAT unlock).

## Non-claims

- Not nested interaction-picture in-in integrals.  
- Not optical theorem / unitarity.  
- Not $|\nabla\pi|^3$ (still held).  
- Not MAT-001.

## Reproduction

```powershell
conda activate itsm_env
cd Analysis\UVIR\UVIR-003
python uvir003_frw_multi_slice_mode_green.py
# expect: PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN
```

Outputs:

- `outputs/uvir003_frw_multi_slice_mode_green_summary.json`
- `outputs/uvir003_frw_multi_slice_kernel.csv`
- `outputs/uvir003_frw_mode_projected_green.csv`

## Next (remaining alpha.10)

1. Nonzero-gradient $|\nabla\pi|^3$ sector on a declared background.  
2. Optional: recompute multi-slice kernels at FRW-local backgrounds (not NN).  
3. Only then a *declared* perturbative-unitarity / EFT-validity criterion.
