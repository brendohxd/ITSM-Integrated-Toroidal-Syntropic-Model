# TOP-X4 X4-S2F3 Plan-11 Exact-Transport Retry Checkpoint

**Date:** 2026-09-12  
**Branch:** `recovery/v12-core-architecture`  
**Candidate:** `X4-S2F3`  
**Result:** `PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN`  
**Checks:** `18/18`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## Decision

The separately frozen retry passes its bounded exact-transport scope. The
registered A1 background supports positive-Hamiltonian charged-scalar Cauchy
data, exact symplectic transport of the charged and real-scalar modes, and
exact unitary transport of a distinct first-order Dirac superadiabatic
projector state.

This result does not reclassify the prior
`FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT`. The three low-mode fourth-order
WKB failures remain negative evidence. The retry uses a different prescription
for those modes—positive-Hamiltonian data at the original `t=0` Cauchy surface
followed by exact transport, with no scalar WKB iterate.

The pass establishes neither a full Hadamard state nor a renormalized stress
tensor. It does not advance to the semiclassical background or physical
Hessian.

## Charged and real-scalar result

For `z=(v,p)^T`, the implemented quadratic Hamiltonian is

`H_2=1/2 (p-mu*J*v)^T(p-mu*J*v)+1/2 v^T K v=1/2 z^T G z`,

with `G=[[K+mu^2 I,mu J],[-mu J,I]]` and exact generator
`A_s=Omega G`. The two negative-imaginary eigenmodes at `t=0` are normalized
to `iF^dagger Omega F=I`, `F^T Omega F=0`, and transported by
`S_dot=A_s S`.

The bounded primary-grid evidence is:

- minimum registered `K` eigenvalue: `0.891283303349327`;
- minimum registered scalar Hamiltonian eigenvalue: `0.4828799025122714`;
- maximum scalar symplectic residual: `2.694307068596595e-9`;
- maximum scalar mode-normalization residual: `4.87428921321968e-10`;
- maximum scalar isotropy residual: `2.378506009181205e-11`;
- maximum real-scalar Wronskian residual: `3.872481224576063e-10`.

All registered modes remain finite, including charged-minus `(k,n)=(1,0)`
and `(1,1)` and chi `(1,0)`, which failed the prior branchwise `W^(4)`
positivity check. This exact-transport success is not a retroactive WKB pass.

For every `n in {0,1,2,4}`, the final instantaneous-basis scalar mixing
decreases strictly along `k_obs=8,16,32`. The maximum value on that trend grid
is `9.398247120850417e-4` for the coupled charged modes and
`4.5859324007961806e-4` for chi. Three finite momenta establish only the
registered UV trend, not infinite-order adiabatic convergence.

## Separate Dirac-state result

After `Psi_c=(a^3 b)^(1/2)Psi`, the code independently uses

`H_D=alpha_1*k_obs/a+alpha_4*n/b+beta*m_F`,

with four-component 5D spinors, `N_F=3`, periodic `n`, and the equal-mass
dimensionless control `m_F=1`. The five Hermitian Clifford matrices have zero
measured algebra residual.

From `P=(I+H_D/omega)/2`, the retry constructs

`P_1=-(i/(2omega))[P_dot,P]`, `S=[P_1,P]`, and
`P_ad1=exp(S)P exp(-S)`.

Every retracted projector is Hermitian, idempotent and rank two within the
registered `1e-12` tolerance. The first-order construction reduces the local
initial-surface invariance defect for every mode; the largest corrected-to-
zeroth-order ratio is `0.1956287111447811`, below the frozen `0.25` bound.
Exact evolution preserves the two-state inner-product matrix to maximum
residual `7.059952142327541e-10`.

Final negative-energy leakage decreases strictly along `k_obs=8,16,32` for
every registered `n`; its maximum on that trend grid is
`4.297309419954153e-6`. The projector is first order, not infinite order, so
this does not establish a Dirac Hadamard state. The distinction is consistent
with the iterative spinor construction of Barbero et al.,
[`arXiv:1805.05107`](https://arxiv.org/abs/1805.05107), and the infinite-order
Hadamard boundary described by Hollands,
[`gr-qc/9906076`](https://arxiv.org/abs/gr-qc/9906076).

## Controls and reproducibility

- The previous failed output and its three low-mode failures are checked as
  immutable inputs.
- Constant-background charged-scalar, chi and Dirac controls give mixing or
  leakage below `1e-10`.
- Wrong scalar symplectic sign and broken Dirac Clifford sign mutations are
  rejected.
- Neither the prior scalar-WKB executable nor the static determinant solver is
  imported as the transport calculation.
- No observational target or absolute mass enters the executable.
- Primary 801-point and witness 401-point envelope difference:
  `4.4959119760434874e-10`, below `2e-5`.
- Three final clean CLI replays produced byte-identical JSON. A superseded
  pre-finalization artifact differed in the listed solver residuals by at most
  `4.2e-12`; no check, bound or decision changed.

## Artifact integrity

| Artifact | SHA-256 |
|---|---|
| `Theory/Gates/TOP-X4/TOPX4_S2F3_EXACT_TRANSPORT_RETRY_CONTRACT_2026-09-12.md` | `0cba0d6b36135e2cc3d1bd85462625e6090f47c1eec3327ff48558666a5ad9c8` |
| `Analysis/TOP/TOP-X4/topx4_s2f3_exact_transport_retry_checkpoint.py` | `b381df5bd94b253ae78cc434f225d0014f3e96b5859a638a7787f26363089644` |
| `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_exact_transport_retry_summary.json` | `de3426c753e55da8b55a5f0151bc875b5060c4bf3d7fbae75ab044c93273a1d6` |

All ten frozen authority sidecars matched in the executable receipt.

## Scientific boundary and next admissible work

The state data remain finite-order candidates. In particular:

- the scalar state is instantaneous positive-Hamiltonian data, not an
  infinite-order matrix adiabatic or pseudodifferential construction;
- the Dirac state is first order, not an infinite-order spinor state;
- the registered UV trends are not a proof of the Hadamard wavefront-set
  condition;
- no covariant five-dimensional subtraction or local counterterm map is
  derived;
- no stress integral, KK sum, semiclassical background, constrained Hessian,
  parity-odd determinant phase or anomaly audit is performed.

The next admissible calculation is therefore a separately frozen matrix and
spinor high-order/Hadamard construction plus the covariant five-dimensional
subtraction/counterterm map. It must precede any renormalized stress integral.
Initial-state singularities in coupled systems require explicit control rather
than naive instantaneous diagonalization; see Baacke and Kevlishvili,
[`arXiv:0910.1128`](https://arxiv.org/abs/0910.1128).

`physics_pass=false`, `gate_effect=NONE`,
`advance_to_semiclassical_background=false`, `advance_to_hessian=false`,
`advance_to_a4=false`, and `advance_to_ultra=false`. Rule-9 three-way
independent clearance remains unmet; no independent reports were completed
for this retry.
