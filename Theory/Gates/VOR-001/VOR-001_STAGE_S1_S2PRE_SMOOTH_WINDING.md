# VOR-001 S1 and S2-pre - finite density and smooth winding

**Date:** 2026-08-04
**Gate status:** `OPEN_SCAFFOLD_ONLY`
**Result:** `PASS_VOR001_S1_AND_S2PRE_MATH_TEMPLATE_ONLY`
**Physics pass:** `false`
**Hold:** `HOLD_PARENT_ACTION_LOCAL_FLUCTUATIONS_AND_DEFECT_SECTOR`

## Question

Can the dimensionless complex `U(1)` toy energy used by the VOR scaffold
support a stable nonzero-density minimum and numerically controlled smooth
integer-winding sectors on a fixed rectangular `T^3`?

The tested energy is

```text
E = integral d^3x [
      |grad rho|^2 / 2
      + rho^2 |grad theta|^2 / 2
      + lambda (rho^2-v^2)^2 / 4
    ].
```

This is a mathematical template. It is not adopted as the UVIR condensate
action and does not restore any historical SWNT packaging.

## S1 finite-density result

At `rho0=v` with `lambda>0` and `v>0`,

```text
V'(v)  = 0,
V''(v) = 2 lambda v^2 > 0.
```

The homogeneous zero-winding configuration has zero template energy for both
`theta=0` and a constant shifted phase. This is the expected global `U(1)`
shift control within the fixed-background toy.

The calculation contains no force-field operator or observable normalization.
It therefore does not reverse UVIR-001, derive a spatial `Y^(3/2)` operator,
or connect winding to `a0`.

## S2 smooth-winding pre-screen

For constant `rho=v`,

```text
theta = 2 pi (n1 x/L1 + n2 y/L2 + n3 z/L3),
n_i in Z.
```

The continuum energy is

```text
E_cont = v^2 V_T3 / 2
         * sum_i (2 pi n_i/L_i)^2.
```

The executable uses second-order periodic central differences applied to
`exp(i theta)`. Its exact discrete energy is therefore

```text
E_disc = v^2 V_T3 / 2
         * sum_i [sin(2 pi n_i/N)/(L_i/N)]^2.
```

Keeping these two formulas separate is essential. The abandoned draft
incorrectly tested `E_disc` against `E_cont` with tolerances smaller than the
known discretization error. The corrected audit verifies the discrete formula
at machine precision and independently measures convergence toward the
continuum result.

## Verified controls

All thirteen aggregate checks pass:

1. stable finite-density minimum;
2. homogeneous global-phase shift control;
3. no force operator or packaging parameter;
4. integer winding sectors;
5. numerical energy agrees with the exact discrete formula;
6. positive energy for every tested nontrivial sector;
7. `E(n)=E(-n)`;
8. axis-permutation covariance on an isotropic box;
9. zero winding recovers the homogeneous background;
10. energy increases across the selected winding-norm sequence;
11. second-order convergence to the continuum energy;
12. malformed and under-resolved inputs are rejected; and
13. the result remains explicitly non-physical.

For `n=(1,0,0)` at `N=(16,32,64)`, the continuum relative errors decrease
monotonically with observed order close to two. The `N=64` relative error is
below `0.004`, matching the declared second-order scheme.

## Reproduction

Run:

```powershell
python Analysis\VOR\VOR-001\vor001_stage_s1_energy_audit.py
```

The deterministic summary is
`Analysis/VOR/VOR-001/outputs/vor001_stage_s1_energy_audit_summary.json`.
Its SHA-256 after two consecutive runs was
`7A2590C15F3920FECA02836FAE8B1F37E9CA121CEFB4723D54624360C55D2ADD`.

## Scientific boundary

This establishes only that the declared fixed-background dimensionless toy
has a stable finite-density minimum and correctly accounted smooth winding
energies. It does not establish:

- the parent ITSM condensate action;
- stability of local amplitude/phase fluctuations on a winding background;
- a defect core or vortex-filament solution;
- a resonance spectrum or ordering mechanism;
- an `a0`, force, cosmology, lensing, PTA, SPARC or `13/12` result; or
- `PASS_VOR001_RESEARCH`.

## Next action

Derive the sector split from one declared parent condensate action and expand
the local amplitude and phase fluctuations about a nonzero winding sector.
Defect cores remain S3 work. “Resonance” must receive an operational
definition before any S4 spectrum is calculated.
