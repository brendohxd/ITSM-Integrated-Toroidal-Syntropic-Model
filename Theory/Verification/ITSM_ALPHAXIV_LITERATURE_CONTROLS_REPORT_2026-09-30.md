# ITSM alphaXiv literature-controls report — 30 September 2026

## Result

**PASS — CONTROL ONLY (25/25 checks).**

The first-run receipt was reproduced byte for byte by a no-write replay. The
result independently supports two bounded statements:

1. after accounting for action and variable conventions, the uncoupled-dust
   density kinetic coefficient in Aoki et al. is exactly the R4C1 G3D
   coefficient \(K_D=a^5\rho_m/k^2\); and
2. the existing CBR-001 nonzero-mode conformal-scalar stress on a rectangular
   \(T^3\) agrees with both the formula in Negro et al. and an independent
   heat-kernel/Mellin implementation.

This result does **not** close a physics gate. It does not establish an
interacting EFT dictionary, full stability, a torus zero-mode state, dynamical
backreaction, observational viability, or publication readiness.

## Reproducibility record

- Contract:
  `Theory/Verification/ITSM_ALPHAXIV_LITERATURE_CONTROLS_CONTRACT_2026-09-30.md`
- Executable:
  `Analysis/LiteratureControls/test_itsm_alphaxiv_literature_controls.py`
- Frozen receipt:
  `Analysis/LiteratureControls/outputs/alphaxiv_controls_attempt_01/summary.json`
- Frozen formulas:
  `Analysis/LiteratureControls/outputs/alphaxiv_controls_attempt_01/formulas.json`
- Receipt SHA-256:
  `91815b117f747b86579b72d81441f912d27eed3efae7219b12c20a352b48d303`
- First run: 25/25 checks passed, exit code 0.
- No-write replay: receipt byte match `true`, no replay failures, exit code 0.

All local input hashes in the contract were verified by the executable before
the calculation. The source receipt and both JSON artifacts have matching
SHA-256 sidecars.

## Control A — Aoki et al. and the R4C1 density mode

### Exact normalization match

Aoki et al. write the scalar quadratic action without an overall factor of
\(1/2\), use \(X^T=(\delta_c/k,\zeta,\delta_m/k)\), and give

\[
 K_{11}=\frac{a^2M^2H^2}{2}
 \left(3\Omega_c+\alpha_{m2}-\bar\alpha_{m1}^{,2}\right).
\]

Writing the \(\delta_c\) term instead as
\(\tfrac12K_D\dot\delta_c^2\) gives

\[
 K_D^{\rm EFT}=\frac{2a^3K_{11}}{k^2}
 =\frac{a^5M^2H^2}{k^2}
 \left(3\Omega_c+\alpha_{m2}-\bar\alpha_{m1}^{,2}\right).
\]

In the uncoupled-dust limit,
\(3\Omega_c=\rho_c/(M^2H^2)\), so

\[
 K_D^{\rm EFT}=\frac{a^5\rho_c}{k^2}.
\]

The symbolic residual against the R4C1 G3D result was exactly zero. This is a
nontrivial convention and normalization control: the R4C1 coefficient has the
standard dust-density normalization found in an independently developed
coupled-dark-sector EFT.

### What does not follow

The exact uncoupled match does not identify the R4C1 interaction parameters
with \(\alpha_{m2}\) or \(\bar\alpha_{m1}\). Aoki et al. construct a broad
fluid EFT with energy- and momentum-transfer operators; R4C1 contains a
specific conformal matter coupling, amplitude/phase variables, an explicit
reservoir, and a higher-spatial-derivative regulator. Their field variables and
operator bases have not been matched.

Consequently, this report does not set
\(\alpha_{m2}=\bar\alpha_{m1}^{,2}\), import a small-scale no-ghost result into
R4C1, or establish all-scale kinetic and gradient stability.

### Exchange-structure comparison

The R4C1 variation report derives

\[
 \nabla_\mu T_m^{\mu\nu}=Q_{mp}^{\nu},\qquad
 \nabla_\mu T_P^{\mu\nu}=-Q_{mp}^{\nu}+Q_{\rm syn}^{\nu},\qquad
 \nabla_\mu T_R^{\mu\nu}=-Q_{\rm syn}^{\nu},
\]

with total conservation after summing sectors. This is structurally compatible
with the conservation bookkeeping required in a coupled-sector EFT, but it is
more specific than the Aoki operator basis and is not yet shown to be its
special case. The next legitimate comparison would require reducing the full
R4C1 action to the same perturbation variables and identifying each EFT
coefficient, including constraint and higher-derivative terms.

## Control B — Negro et al. and CBR-001

### Formula match

For the nonzero modes of a conformally coupled massless scalar, Negro et al.
obtain the topological energy density and directional stress with the same
lattice tensors used in CBR-001. Their de Sitter prefactor obeys
\(H^4\eta^4=a^{-4}\), so using physical lengths \(aL_i\) reduces their
nonzero-mode expression to

\[
 \rho=-\frac{1}{2\pi^2}\sum_{\mathbf n\ne0}R_{\mathbf n}^{-4},
 \qquad
 p_i=\frac{1}{2\pi^2}\sum_{\mathbf n\ne0}
 \frac{R_{\mathbf n}^2-4L_i^2n_i^2}{R_{\mathbf n}^6}.
\]

These are exactly the CBR-001 Stage-1 formulas.

### Independent numerical benchmark

The new control did not reuse the CBR direct lattice sum to compute its
reference value. It evaluated the Epstein sum through a Mellin integral of a
product of Jacobi theta functions, used the Poisson transformation at small
integration parameter, and recovered pressures from derivatives of the total
energy. It then compared those values with the registered symmetric-cutoff
CBR extrapolation.

| \((L_1,L_2,L_3)\) | heat-kernel \(\rho\) | direct-extrapolated \(\rho\) | relative \(\rho\) discrepancy | maximum normalized \(p_i\) discrepancy | relative trace residual |
|---|---:|---:|---:|---:|---:|
| \((1,1,1)\) | -0.837536910696079 | -0.837535892991725 | \(1.2151\times10^{-6}\) | \(4.0504\times10^{-7}\) | \(5.6064\times10^{-12}\) |
| \((1,1.25,1.25)\) | -0.478867349309024 | -0.478866775070187 | \(1.1992\times10^{-6}\) | \(6.4556\times10^{-7}\) | \(2.9599\times10^{-12}\) |
| \((1,1,2)\) | -0.436226667105586 | -0.436226197110306 | \(1.0774\times10^{-6}\) | \(5.4256\times10^{-7}\) | \(4.0071\times10^{-12}\) |
| \((0.8,1.1,1.4)\) | -0.751973137782145 | -0.751972287882301 | \(1.1302\times10^{-6}\) | \(7.4199\times10^{-7}\) | \(2.2378\times10^{-12}\) |

The cube equation of state, permutation covariance, and
\(L_i\mapsto1.7L_i\) scaling all passed their frozen \(5\times10^{-5}\)
tolerances. The approximately \(10^{-6}\) offset between methods is consistent
with the finite-cutoff extrapolation being the less precise member of the pair;
it is well below the predeclared acceptance bounds.

### Zero-mode and backreaction boundary

Negro et al. retain a state-dependent, isotropic zero-mode contribution. The
control excludes that term from both sides. Therefore it verifies the
nonzero-mode topological stress but does not choose or derive the physical
zero-mode state.

The paper studies perturbative metric backreaction about an isotropic de
Sitter background. CBR-001 Stage 1 is a static stress solver. Agreement of the
stress tensors does not by itself establish a self-consistent anisotropic
semiclassical solution, renormalized state evolution, or TOP-X4's physical
Hessian.

## Manuscript consequence

The two controls support a combined R4C1 theory-paper programme rather than a
standalone claim that ITSM is already complete. The defensible core is:

1. a fully declared conditional action and its sector-by-sector exchange
   identities;
2. finite-charge and background reductions, with assumptions exposed;
3. the canonical dust-density normalization, now independently controlled;
4. coefficient non-identifiability and compact-domain compatibility limits;
5. explicit separation of established results, conditional ansatzes, and open
   stability or matching work; and
6. external comparison with coupled-fluid EFT and compact-space quantum stress
   calculations.

The separate P2 Casimir paper remains the correct home for the full rectangular
\(T^3\) stress scan and any future backreaction analysis. The R4C1 paper may
cite this control as a topology-sector consistency check, but should not absorb
P2's numerical programme.

## Required next work

1. Derive an explicit R4C1-to-fluid-EFT perturbation dictionary, including
   lapse/shift constraints and the higher-spatial-derivative regulator.
2. Determine whether the interacting correction to \(K_D\) is positive over a
   registered domain; the uncoupled equality alone is insufficient.
3. Treat the torus zero mode as a declared state-selection problem and test its
   effect separately from the nonzero-mode stress.
4. Extend the Casimir control to a declared background evolution only after the
   renormalized semiclassical source and approximation order are frozen.
5. Obtain deferred independent review before canonical promotion or public
   claims of physical closure.

## Sources

- Aoki et al., *Effective field theory of coupled dark energy and dark matter*,
  [arXiv:2504.17293v2](https://arxiv.org/abs/2504.17293v2).
- Negro et al., *Quantum Signatures of Cosmic Topology: How Casimir
  Backreaction Transmits Isotropy Violation*,
  [arXiv:2603.12319](https://arxiv.org/abs/2603.12319).
