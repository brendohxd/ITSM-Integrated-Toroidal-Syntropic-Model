# CBR-001 Stage 3B — `13/12` reachability and stability

## Purpose

Stage 3B uses the validated Stage-3A Bianchi-I engine and Stage-2 Casimir
interpolation to test, without assuming the answer, whether

```text
q = H_t/H_p = 13/12
```

is unreachable, a transient crossing, a quasi-plateau, or a stable attractor.

`STATUS: PASS` means that the search, rejection rules, analytic identities,
constraints, continuity test, bracketed roots, and classifications were
executed successfully. It does not mean that the `13/12` hypothesis succeeded.

## Kinematic identity

With

```text
x = delta/H
H_p = H(1 - 2x/3)
H_t = H(1 + x/3),
```

the directional ratio is

```text
q = (1 + x/3)/(1 - 2x/3).
```

Consequently,

```text
q = 13/12  <=>  x = 3/38.
```

The script verifies this algebraically and numerically.

## Analytic small-source check

For the fixed-background approximation,

```text
x(N) = S [exp(-3N) - exp(-4N)].
```

Its maximum is

```text
max x = (27/256) S
N_at_max = ln(4/3).
```

Reaching `x=3/38` therefore requires

```text
S >= 128/171 = 0.748538...
```

which lies outside the strict small-perturbation regime. This estimate is used
as a diagnostic, not as a substitute for the nonlinear constrained evolution.

## Numerical search

The default initial shapes are

```text
r0 = 1.01, 1.05, 1.10, 1.25, 1.50, 2.0, 3.0, 4.0.
```

For each shape the solver scans 49 logarithmic amplitudes from `1e-6` to `10`
over `N=0..20`. When adjacent valid runs bracket the target, Brent root finding
solves

```text
max_N q(N; epsilon) - 13/12 = 0.
```

Runs are rejected if the total density becomes non-positive, either directional
Hubble rate becomes non-positive, the expanding Hamiltonian branch ceases to
exist, or the trajectory leaves the Stage-2 interpolation domain.

## Classification

- `NO_CROSSING`: the largest valid ratio remains below the target.
- `TRANSIENT_CROSSING`: the target is touched or crossed briefly.
- `QUASI_PLATEAU`: the ratio remains within 1% for at least one e-fold but fails
  the attractor requirements.
- `ATTRACTOR`: the ratio remains within 1% for at least five e-folds, nearby
  initial conditions converge, and the trajectory does not later decay toward
  unity.
- `INVALID`: a physical or numerical rejection condition is encountered.

Every bracketed candidate is perturbed one variable at a time using `r0` and
`epsilon` factors of `0.99` and `1.01`, plus initial shear shifts of
`+/-0.01(3/38)`. The changes in crossing time, maximum ratio, dwell time, and
late-time ratio are recorded.

## Asymptotic expectation

The free-field Casimir source redshifts as `a^-4`, while the homogeneous shear
is damped by `3H delta`. The minimal model is therefore expected to approach

```text
delta/H -> 0
H_t/H_p -> 1.
```

Stage 3B checks this directly at `N=20`. A tuned crossing followed by this
return to unity is not classified as an attractor.

## Interpreting the result

The report keeps four questions separate:

1. **Mathematical reachability:** can any valid amplitude reach `13/12`?
2. **Transient crossing:** is the target only crossed around a finite-time peak?
3. **Dynamical attraction:** do nearby states converge toward and remain at the
   target?
4. **Physically plausible amplitude:** is the required Casimir fraction still
   perturbatively small?

## Validated result

The default run completed with `STATUS: PASS`. Five initial shapes have a
bracketed amplitude at which the trajectory just reaches the target:

| `r0` | threshold `epsilon` | maximum Casimir fraction | result |
|---:|---:|---:|---|
| 1.10 | 2.55284 | 2.53573 | transient, nonperturbative |
| 1.25 | 1.33784 | 0.631824 | transient, nonperturbative |
| 1.50 | 0.675730 | 0.272886 | transient, nonperturbative |
| 2.00 | 0.277933 | 0.132980 | transient, nonperturbative |
| 3.00 | 0.0891822 | 0.0820713 | transient, marginal |

The tested `r0=1.01` and `1.05` cases do not cross within the valid amplitude
scan. The `r0=4` initial condition is invalid for this test because it starts at
the Stage-2 interpolation boundary and the sourced trajectory leaves that
domain.

- **Mathematical reachability:** yes for five of the eight tested initial
  shapes, after bracketed root finding rather than coarse-grid selection.
- **Transient crossing:** every reachable case is a tuned transient. Time
  within 1% of the target is only `0.27` to `0.30` e-folds.
- **Dynamical attraction:** no. Nearby runs may move above or below the target,
  and all valid candidates subsequently approach `q=1`; no `QUASI_PLATEAU` or
  `ATTRACTOR` occurs.
- **Physically plausible amplitude:** not demonstrated. No target-reaching
  candidate is perturbative under the stated Casimir-fraction criterion; four
  are nonperturbative and one is marginal.

At `N=20`, every valid threshold candidate satisfies `q=1` to approximately
`1e-15`, explicitly confirming the expected late-time decay to isotropy in the
minimal free-field model. The largest Hamiltonian and normalized continuity
residuals are `2.96e-16` and `4.39e-16`, respectively.
## Run

```powershell
conda activate itsm_env
python cbr001_stage3b_ratio_test.py
```

Outputs are written under `stage3b_outputs/`.
