# TOP-X4 `X4-S2F3` Plan-11 Hadamard/subtraction readiness receipt

**Executed:** 2026-09-12  
**Checkpoint status:** `PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS`  
**Readiness decision:** `HOLD`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Binding result

The preregistered executable completed all `20/20` bounded scaffold and
fail-closed inventory checks. It establishes a consistent local
five-dimensional Hadamard/heat-kernel subtraction scaffold and identifies the
specific missing `X4-S2F3` inputs. It does **not** establish a full Hadamard
state or authorize a renormalized stress calculation.

The output remains explicit:

```text
readiness_decision=HOLD
hadamard_stress_ready=false
physics_pass=false
gate_effect=NONE
```

## 2. Execution receipt

Command:

```powershell
python Analysis\TOP\TOP-X4\topx4_s2f3_hadamard_subtraction_readiness.py
```

Recorded output:

```text
PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS
checks=20/20
readiness_decision=HOLD
hadamard_stress_ready=false
physics_pass=false
gate_effect=NONE
sha256=a36658292ee7986f2be8828222e1a2a05cd7991da824a949a5eaf749aa58a1d2
```

Artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `topx4_s2f3_hadamard_subtraction_readiness.py` | `e90c6b813f00ed1ccd0a7f181def6e5a3c7c7208957953d3abfa4aa7571510e6` |
| `topx4_s2f3_hadamard_subtraction_readiness_summary.json` | `a36658292ee7986f2be8828222e1a2a05cd7991da824a949a5eaf749aa58a1d2` |

The executable verified the sidecars of all nine registered authority/input
artifacts before evaluating the scaffold.

Three final clean CLI replays produced the same output hash
`a36658292ee7986f2be8828222e1a2a05cd7991da824a949a5eaf749aa58a1d2`.

## 3. What the calculation establishes

The bounded checks independently recover:

- the scalar `D=5` singular power `3/2` and propagator normalization
  `i/(16*sqrt(2)*pi^2)`;
- the required scalar expansion through `U_0`, `U_1` and `U_2`, including the
  registered coincidence coefficients;
- the general matrix Laplace-type `b_0,b_1,b_2` map, with the convention
  `P=-(D^2+E)` and the explicit `E`, `Omega_AB Omega^AB`, `R^2`, Ricci-squared
  and Riemann-squared terms;
- the distinction between DeWitt `b_0,b_1,b_2` and heat-kernel
  `a_0,a_2,a_4` indexing;
- proper-time power terms proportional to `Lambda^5`, `Lambda^3` and
  `Lambda`, all of five-dimensional Lagrangian dimension;
- the five independent pure-gravity local operators `1`, `R`, `R^2`,
  `R_AB R^AB` and `R_ABCD R^ABCD`;
- absence of a bulk logarithmic term for the smooth boundaryless `D=5`
  Laplace-type control, without erasing finite renormalization ambiguity;
- absence of internal boundary/fixed-point heat-kernel terms for the smooth
  unorbifolded circle; and
- the strict boundary that Poisson removal of the decompactified `q=0` image
  isolates a static topology-dependent Casimir term but does not renormalize
  evolving state-dependent stress.

All six registered bad mutations were rejected: adding a five-dimensional
bulk logarithm, omitting Riemann-squared, promoting `q=0` subtraction to full
stress renormalization, calling finite-order transport Hadamard, omitting the
graviton ghost/Jacobian sector, and omitting the matrix bundle terms.

## 4. Binding readiness inventory

| Required completion item | Recorded status | Current evidence boundary |
|---|---|---|
| Covariant charged-scalar/`chi` matrix second variation | `NOT_COMPLETED` | Existing operator is the constant-background principal operator before gravity constraints |
| Scalar matrix Hadamard state | `NOT_COMPLETED` | Existing data are instantaneous positive-Hamiltonian data plus exact finite-order transport |
| Dirac Hadamard two-point function | `NOT_COMPLETED` | Existing Dirac state is a first-order projector plus exact unitary transport |
| Curved finite-charge graviton and ghost/Jacobian operators | `NOT_COMPLETED` | Existing gravity result is only a flat zero-density five-polarization count |
| Parity-odd phase, anomaly and quantized counterterms | `NOT_COMPLETED` | Explicitly retained as unaudited by the exact-transport result |
| Gravitational and matter counterterm normalizations | `NOT_COMPLETED` | Covariant five-dimensional subtraction remains `NOT_DERIVED` |

The interacting scalar counterterm map cannot be inferred from the
pure-gravity basis alone. It depends on the model-specific matrix
`tr(E)`, `tr(E^2)`, `tr(Omega_AB Omega^AB)` and local derivative terms obtained
from the off-shell covariant second variation.

Likewise, squaring the Dirac operator can organize the parity-even determinant
magnitude, but it discards the parity-odd phase. A curved graviton determinant
also requires a gauge-fixed Hessian and the associated ghost/Jacobian and
zero-mode prescriptions; the saved flat degree count is not that calculation.

## 5. Primary-source audit

The five-dimensional scalar singular structure, its state-dependent regular
part and the independent curvature-squared counterterms follow the explicit
`D=5` construction of Decanini and Folacci,
[arXiv:gr-qc/0512118](https://arxiv.org/abs/gr-qc/0512118).

The general Laplace-type coefficient formulas and the requirement to include
connections, endomorphisms and gauge/ghost operators follow Vassilevich,
[arXiv:hep-th/0306138](https://arxiv.org/abs/hep-th/0306138).

The finite-order versus Hadamard distinction is bounded by Hollands,
[arXiv:gr-qc/9906076](https://arxiv.org/abs/gr-qc/9906076), and by the general
adiabatic-state framework of Junker and Schrohe,
[arXiv:math-ph/0109010](https://arxiv.org/abs/math-ph/0109010). Relevant
pseudodifferential constructions are given for scalar fields by Gerard and
Wrochna, [arXiv:1209.2604](https://arxiv.org/abs/1209.2604), and for Dirac
fields by Gerard and Stoskopf,
[arXiv:2108.11630](https://arxiv.org/abs/2108.11630).

The cited Dirac constructions are structural controls only: their stated
hypotheses are four- or even-dimensional. They do not certify the required
five-dimensional spinor state, whose dimension-appropriate construction
remains open.

These sources constrain the scaffold; they are not independent Rule-9 reviews
of this repository calculation.

## 6. Decision and next admissible checkpoint

The universal scaffold passes, but stress readiness is held. The next
single-gate calculation is the off-shell covariant matrix second variation of
the two real components of `Phi` coupled to `chi`, derived before the
homogeneous or fixed-charge ansatz. It must expose the model-specific
Laplace-type connection, `E` and `Omega` data and enumerate the resulting
matter counterterm structures.

Spinor Hadamard construction, the graviton/ghost determinant, the parity-odd
phase and counterterm normalization remain separate receipted prerequisites.
No stress integral, self-consistent background, physical Hessian, A4, Ultra,
gate promotion or publication change follows from this receipt.

Rule-9 status remains `THREE_WAY_CLEARANCE_NOT_MET` with zero completed
independent reports for this checkpoint.
