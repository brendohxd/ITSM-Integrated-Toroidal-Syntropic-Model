# TOP-X4 `X4-S2F3` scoped curved Dirac-operator contract

**Date:** 2026-09-16  
**Status:** `SCOPED_OPERATOR_CHECKPOINT`  
**Scope:** Hamiltonian-form curved 5D Dirac operator on the registered
homogeneous metric  
**Gate effect:** none  
**Physics pass:** false

## 1. Purpose and boundary

This contract freezes the next resolvable operator input for the `X4-S2F3`
retry. It derives the Hamiltonian-form neutral-spectator Dirac operator on

\[
 ds^2=-N(t)^2dt^2+a(t)^2d\mathbf{x}^2+b(t)^2dy^2,
 \qquad y\sim y+2\pi,
\]

including the torsion-free homogeneous spin connection, the volume-rescaling
term, the Hermitian Hamiltonian Clifford representation and the periodic KK
dispersion relation.

It does **not** construct a finite-charge background, a spinor Hadamard state,
a state-dependent determinant, a parity-odd phase, an anomaly calculation,
quantized counterterms, a renormalized stress tensor or a physical Hessian.

## 2. Declared operator

For the coframe

\[
 e^{\hat 0}=Ndt,\qquad e^{\hat i}=a,dx^i,\qquad e^{\hat 4}=b\,dy,
\]

the torsion-free connection has

\[
 \omega^{\hat i}{}_{\hat0}=H_a e^{\hat i},
 \qquad
 \omega^{\hat4}{}_{\hat0}=H_b e^{\hat4},
 \qquad
 \Theta=3H_a+H_b.
\]

After the declared rescaling

\[
 \Psi_c=(a^3b)^{1/2}\Psi,
\]

the neutral periodic spectator mode with observed momentum `k_obs` and KK
integer `n` is represented in Hamiltonian form by

\[
 H_D=N\left(\alpha_{\rm obs}\frac{k_{\rm obs}}{a}
 +\alpha_y\frac{n}{b}+\beta m_F\right),
 \qquad n\in\mathbb Z,
\]

with five Hermitian matrices that square to the identity and mutually
anticommute. Therefore

\[
 H_D^2=N^2\left[\left(\frac{k_{\rm obs}}a\right)^2
 +\left(\frac nb\right)^2+m_F^2\right]I_4.
\]

The spectator is neutral under the condensate: no direct `rho`, `chi` or
`mu` shift is inserted into `H_D`. Any dependence on the evolving background
enters through the metric and the later state construction.

## 3. Required checks

The executable reports the 13 checks in two explicit classes. The first two
are contract/provenance checks; the remaining 11 are operator and rejection
checks. A missing sidecar or contract token fails closed as
`ERROR_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT`, but it is not represented
as an operator-mathematics failure.

The operator class must verify:

1. the diagonal coframe and inverse reconstruct the registered metric;
2. the Hamiltonian Clifford matrices are Hermitian and satisfy the exact
   anticommutation algebra;
3. the torsion-free spin connection and half-log-volume derivative agree;
4. the Hamiltonian squares to the lapse-scaled KK dispersion relation;
5. the periodic integer KK spectrum has the expected positive/negative pairs;
6. the wrong spin-connection sign, antiperiodic half-shift and direct scalar
   chemical-potential shift are rejected.

## 4. Binding status

The admissible successful result is:

```text
PASS_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_SCOPED_HOLD_QUANTUM_CLOSURE
contract_checks=2/2
operator_checks=11/11
operator_status=DERIVED_HAMILTONIAN_FORM_ON_REGISTERED_HOMOGENEOUS_METRIC
covariant_completion=SCOPED_ONLY_NOT_FULL
physics_pass=false
gate_effect=NONE
```

The uncomputed full-completion fields remain `NOT_DERIVED` or
`NOT_CONSTRUCTED` at the parent gate; this scoped receipt does not overwrite
those statuses.

This is an operator-geometry prerequisite only. It does not advance the
finite-charge determinant, parity/anomaly, counterterm, stress, Hessian,
`X4-D2`, MAT, UVIR, BBN, Rule 9 or publication gates.

## 5. Reproduction

```powershell
python -B Analysis/TOP/TOP-X4/topx4_s2f3_curved_dirac_operator_checkpoint.py
```

The deterministic output is
`Analysis/TOP/TOP-X4/outputs/topx4_s2f3_curved_dirac_operator_summary.json`.
