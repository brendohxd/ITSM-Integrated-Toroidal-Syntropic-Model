# UVIR-003 Stage B — FRW in-in observable path (declared)

Date: 2026-08-02

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (path declared; full diagrams not computed)

Subgate:
`PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

## Purpose

Promote the **local adiabatic packet proxy** toward an FRW-aware observable
without pretending a cosmological S-matrix exists.

## Declared skeleton

\[
G_{\mathrm{proxy}}(t_{\mathrm{out}},t_{\mathrm{in}};\sigma)
=
O[\sigma]\,T_{\mathrm{gain}}(q_{\mathrm{high}})
\]

- \(O[\sigma]\): local Gaussian packet average of the frozen four-leg kernel
  (`PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION`).
- \(T_{\mathrm{gain}}\): endpoint normalized phase-space gain on a **controlled
  high-\(q\)** fixed-comoving transfer sample (infrared transfer may remain
  `HOLD` and is not used here).

## Pass criteria

1. Verified FRW representative branch available.  
2. Packet proxy summary PASS.  
3. At least one high-\(q\) converged transfer sample.  
4. Explicit scientific boundary written to JSON.

## Non-claims

- Not nested in-in time integrals.  
- Not a cross section or optical-theorem check.  
- Not MAT-001.  
- Not unitarity.

## Reproduction

```powershell
conda activate itsm_env
cd Analysis\UVIR\UVIR-003
# dependencies (already PASS on this branch):
#   uvir003_local_four_leg_kernel.py
#   uvir003_local_adiabatic_observable_norm.py
#   prior FRW + transfer outputs
python uvir003_frw_in_in_observable_path.py
```

## Next

1. Multi-slice local kernel / response on admitted high-\(q\) FRW points.  
2. Replace scalar \(T_{\mathrm{gain}}\) with mode-projected two-time Green’s function.  
3. Nonzero-gradient \(|\nabla\pi|^3\).  
4. Declared unitarity criterion only after the above.
