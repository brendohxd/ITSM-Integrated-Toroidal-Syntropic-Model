# CBR-001 Stage 3A — validated cosmological backreaction

## Scope

Stage 3A treats the verified rectangular-`T^3` Casimir tensor as a small
perturbation on a positive de Sitter background. It does not evolve a universe
sourced only by the negative Casimir density.

> Stage 3A does not test or establish the ITSM 13/12 ratio. It validates the
> cosmological backreaction engine required for that later test.

## Geometry and variables

The biaxial Bianchi-I metric is

```text
ds^2 = -dt^2 + a_p(t)^2 dx^2 + a_t(t)^2 (dy^2 + dz^2).
```

The directional and mean expansion rates are

```text
H_p = dot(a_p)/a_p
H_t = dot(a_t)/a_t
H   = (H_p + 2 H_t)/3
delta = H_t - H_p
r = a_t/a_p
```

with

```text
dot(r) = r delta
a = (a_p a_t^2)^(1/3)
a_p = a r^(-2/3)
a_t = a r^(1/3).
```

The solver uses `N = ln(a)` as its independent variable and evolves `ln(r)`
and `delta`. It reconstructs

```text
H_p = H - 2 delta/3
H_t = H + delta/3.
```

## Casimir source

The input is `stage2_outputs/cbr001_stage2_scan.csv`. At fixed mean scale,

```text
u(r) = r^(8/3) rho_hat(r).
```

A shape-preserving PCHIP interpolates the fixed-volume pressure anisotropy
`Delta p = r^(8/3)(p_t_hat-p_p_hat)`. Integrating

```text
d u/d ln(r) = -(2/3) Delta p
```

and anchoring it at the cubic data point produces a thermodynamically
consistent source without oscillatory splines. The directional pressures are
reconstructed using

```text
p_p + 2 p_t = rho
p_t - p_p = Delta p.
```

The physical scaling is

```text
rho_C, p_p,C, p_t,C proportional to a^(-4).
```

The factor `hbar*c/L_*^4` is absorbed into the dimensionless perturbation
amplitude `epsilon`.

## Background and equations

Dimensionless conventions are

```text
H_bg = 1
kappa = 1
rho_bg = 3.
```

The equations are

```text
dot(delta) + 3 H delta = kappa epsilon (p_t,C - p_p,C)
dot(r) = r delta
dot(a) = H a
3 H^2 - delta^2/3 = kappa (rho_bg + epsilon rho_C).
```

`H` is always taken from the positive expanding branch of the Hamiltonian
constraint; it is not integrated independently.

## Run matrix

The default run covers `N=0..10` with

```text
r0 = 0.5, 1.0, 2.0
epsilon = 0, 1e-8, 1e-6, 1e-4.
```

Run it from this directory with:

```powershell
conda activate itsm_env
python cbr001_stage3_backreaction.py
```

## Validation

The solver checks:

1. The `epsilon=0` de Sitter control remains at `H=1`, `delta=0`, and fixed
   `r`.
2. The cubic `r0=1` control remains isotropic for every amplitude.
3. The normalized Hamiltonian residual remains below `1e-9`.
4. The normalized Casimir continuity residual remains below `1e-7`.
5. The `epsilon=1e-8` solutions reproduce the fixed-background analytic shear
   and accumulated shape benchmarks to relative error below `1e-5`.
6. Tighter ODE tolerances reproduce selected `epsilon=1e-4` runs to relative
   difference below `1e-6`.

## Outputs

The run creates:

- `stage3_outputs/cbr001_stage3_runs.csv`
- `stage3_outputs/cbr001_stage3_summary.json`
- `stage3_outputs/cbr001_stage3_shape.png`
- `stage3_outputs/cbr001_stage3_shear.png`
- `stage3_outputs/cbr001_stage3_hubble_ratio.png`
