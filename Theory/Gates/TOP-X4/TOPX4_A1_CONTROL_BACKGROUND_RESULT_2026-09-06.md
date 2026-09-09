# TOP-X4 / KK-001 A1 control-background result

**Date:** 2026-09-06  
**Status:** `PASS_TOPX4_A1_CONTROL_BACKGROUND_ONLY`  
**Decision:** `X4-D1 PASS_CONTROL_PARENT_ONLY`; Max A2/A3 control analysis may begin  
**Physics pass:** false  
**Gate effect:** none

## Question tested

Does the frozen `X4-I1C` five-dimensional Einstein--complex-scalar--real-
scalar control possess a finite-charge on-shell homogeneous background, with
the registered equations following independently from the action and metric?

## Frozen interpretation

- The extra cycle is spatial/internal and has dynamical radius `b(t)`.
- The condensate carries a global `U(1)` charge; finite density is a state, not
  a chemical-potential term inserted into the covariant action.
- `chi` is a bulk real-scalar matter proxy. It is not Standard Model matter and
  cannot establish universal coupling or the equivalence principle.
- The tested background has zero winding and `chi=0`. Consequently, the portal
  is present off shell but inactive on this background.

## Exact executions

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a1_symbolic_audit.py
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a1_background_control.py
```

The symbolic audit passed 9/9 exact checks. It constructed the Einstein tensor
directly from the five-dimensional metric and varied the lapse, scale factors,
radial field, phase and matter proxy independently of the numerical right-hand
side. Every simplified residual was exactly zero.

The numerical background control passed 7/7 registered checks over the
dimensionless interval `0 <= t <= 1` with 401 output points:

- maximum Hamiltonian-constraint residual:
  `9.410250356722827e-13` against `1e-8`;
- maximum global-charge relative drift:
  `1.7201795543542175e-12` against `1e-9`;
- maximum analytic stress-continuity residual:
  `4.996003610813204e-16` against `1e-10`;
- minimum tested field values: `a=1`, `b=1`,
  `rho=0.6995359234543251`;
- no non-finite value, zero-radius crossing or forbidden observational target
  was encountered.

Independent reruns were byte-identical. Output hashes are:

- background JSON:
  `17270d7c7a71401bb7e283139c82d28a188d6fef555348bf42647feacb112b43`;
- symbolic-audit JSON:
  `11a43a73f0caf82210dbe81c9a783d86dbecde6ff9635984302b7483dbcb58de`.

## What passed

The frozen control is internally consistent at the covariant-action and
homogeneous-background level. The tested finite-charge solution is on shell,
and the zero-portal theory is a literal nested `g5=0` limit.

## What did not pass

This is not a physical ITSM pass. In particular, it does not establish:

- perturbative ghost/gradient/tachyon health;
- a fixed or metastable compactification radius;
- a Standard Model matter embedding or universal matter response;
- active energy transfer, a derived nonzero `Q^mu`, `K_Q` or `V`;
- a nonlinear screening law, lensing relation or acceleration scale;
- observational viability or replacement of canonical `T3`.

Because the tested `chi=0` background does not activate the portal, A4 cannot
inherit a nonzero-transfer result from this pass.

## Decision

`X4-D1` is recorded as `PASS_CONTROL_PARENT_ONLY`. The next bounded task is the
Max A2/A3 analysis of the exact frozen action: complete KK/radion reduction,
quadratic signs and poles, EFT hierarchy, zero-charge/small-circle/
decompactification limits, and radion stabilization. No canonical manuscript
revision is authorized before those tests survive.
