# UVIR-003 Stage B — local adiabatic observable normalization

Date: 2026-08-01

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (2026-08-01 run: narrow \(\sigma=0.02\) rel.\ dev.\ \(\sim 2.5\times 10^{-4}\))

Subgate:
`PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

## Purpose

Replace the unspoken assumption “local kernel = cosmological S-matrix element”
with an explicit, auditable **packet-averaged local observable proxy**.

## Definition

On the admitted external ratios \(\{q_i/H\}\) from the tetrahedral four-leg
summary, with centre \(q_0\) and width \(\sigma\) in \(\ln(q/q_0)\),

\[
O[\sigma]
=
\frac{\sum_i w_i K(q_i)}{\sum_i w_i},
\qquad
w_i=\exp\Bigl(-\frac{(\ln(q_i/q_0))^2}{2\sigma^2}\Bigr).
\]

\(K(q)\) is the residue-normalized local combined four-leg kernel (exchange +
reduced contact) for a fixed mode pair.

## Pass criteria (this subgate)

1. Finite positive weights on the admitted sample.
2. Narrow \(\sigma\): \(O\to K(q_0)\) within declared relative tolerance.
3. \(\mathrm{Im}\,O\) negligible when each \(K_i\) is real within tolerance.

## Explicit non-claims

- Not an S-matrix element.
- Not a cross section.
- Not an optical-theorem / partial-wave unitarity bound.
- Not a physical EFT cutoff.
- Not MAT-001.

## Reproduction

```powershell
conda activate itsm_env
cd Analysis\UVIR\UVIR-003
python uvir003_local_adiabatic_observable_norm.py
```

Depends on:
`outputs/uvir003_local_four_leg_kernel_summary.json`
(with `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL`).

## Next

1. Optional denser homogeneous-edge deformation scan.  
2. Promote proxy toward a true in-in correlator on the FRW trajectory.  
3. Nonzero-gradient `|grad(pi)|^3`.  
4. Declared unitarity criterion only after the above.
