# ITSM alphaXiv literature-controls contract — 30 September 2026

## Scope and status

This contract freezes two bounded literature controls before their executable is
created:

1. compare the R4C1 dust-density kinetic normalization and exchange structure
   with Aoki et al., *Effective field theory of coupled dark energy and dark
   matter*, arXiv:2504.17293v2; and
2. independently benchmark the existing rectangular-\(T^3\) conformal-scalar
   Casimir stress against Negro et al., *Quantum Signatures of Cosmic Topology:
   How Casimir Backreaction Transmits Isotropy Violation*, arXiv:2603.12319.

This is a literature and implementation control, not a gate-closing calculation.
It may support provisional research under the deferred Rule-9 policy. It cannot
promote R4C1, CBR-001, TOP-X4, UVIR-003, or any manuscript to Derived or
publication-ready status.

## Frozen local inputs

| Input | SHA-256 |
|---|---|
| `Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md` | `3019196b071b146a1e41cd055073ae02da2afa10b1cdb5ae49e0a63cf84a6eb6` |
| `Theory/Gates/RES-001/RES001_R4C1_G3_DENSITY_ACTION_REPORT_2026-09-30.md` | `8a1c2245fc02307c5e70c7b4c1064872e82464c4c411d3095e97575c730b1876` |
| `Analysis/Casimir/CBR-001/casimir_t3_lattice.py` | `5f0515fab37cdfc0de837bcbc36011260815c5275dc6755a3226144811f04b87` |
| `Analysis/Casimir/CBR-001/README.md` | `6b5122e9b59c671fd0f88e4c990b344cc2d9569e01279516363a7135ba633b65` |

Any hash mismatch is a provenance failure for this attempt. It is not repaired
silently.

## Control A — coupled-dark-sector density normalization

Aoki et al. write their scalar quadratic action without an overall \(1/2\),
with variable ordering

\[
  X^T=(\delta_c/k,\zeta,\delta_m/k),
\]

and, in their notation,

\[
 K_{11}=\frac{a^2M^2H^2}{2}
 \left(3\Omega_c+\alpha_{m2}-\bar\alpha_{m1}^{,2}\right).
\]

For uncoupled dust, \(3\Omega_c=\rho_c/(M^2H^2)\). Converting the
\(\delta_c/k\) term to the standard convention
\(\tfrac12K_D\dot\delta_c^2\) therefore predicts

\[
  K_D^{\rm EFT}=\frac{2a^3K_{11}}{k^2}
  =\frac{a^5\rho_c}{k^2},
\]

which is the R4C1 G3D dust-density normalization. The executable shall check
this identity symbolically and exactly.

The interacting EFT expression shall also be recorded as

\[
  K_D^{\rm EFT}=\frac{a^5M^2H^2}{k^2}
  \left(3\Omega_c+\alpha_{m2}-\bar\alpha_{m1}^{,2}\right),
\]

but no mapping from the R4C1 fields or couplings to the Aoki EFT coefficients is
assumed. In particular, the control must not infer
\(\alpha_{m2}=\bar\alpha_{m1}^{,2}\), transfer the paper's small-scale
no-ghost conditions to the full R4C1 system, or treat agreement in the
uncoupled normalization as validation of R4C1 interactions.

The accompanying report shall compare the exchange structures qualitatively:
R4C1 has the covariant identities
\(\nabla_\mu T_m^{\mu\nu}=Q_{mp}^{\nu}\),
\(\nabla_\mu T_P^{\mu\nu}=-Q_{mp}^{\nu}+Q_{\rm syn}^{\nu}\), and
\(\nabla_\mu T_R^{\mu\nu}=-Q_{\rm syn}^{\nu}\), whereas the paper supplies a
general fluid-EFT operator basis. This comparison is a structural control, not
an operator dictionary.

## Control B — independent rectangular-\(T^3\) Casimir benchmark

For the nonzero modes of a conformally coupled massless scalar, Negro et al.
give a topological stress whose static physical-length specialization is

\[
 \rho=-\frac{1}{2\pi^2}\sum_{\mathbf n\ne0}R_{\mathbf n}^{-4},
 \qquad
 p_i=\frac{1}{2\pi^2}\sum_{\mathbf n\ne0}
 \frac{R_{\mathbf n}^2-4L_i^2n_i^2}{R_{\mathbf n}^6},
\]

where \(R_{\mathbf n}^2=\sum_iL_i^2n_i^2\). These are the formulas implemented
by CBR-001. The paper's state-dependent isotropic zero-mode term is excluded
from this benchmark and must be reported explicitly as an unresolved state
choice rather than silently set to a derived physical value.

The independent evaluator shall compute

\[
 S_4=\sum_{\mathbf n\ne0}R_{\mathbf n}^{-4}
 =\int_0^\infty t\left[
 \prod_i\vartheta_3(0,e^{-L_i^2t})-1\right]dt
\]

using Jacobi/Poisson transformation at small \(t\), adaptive quadrature, and no
call to the repository's direct lattice sum for this value. Pressures shall be
obtained independently from the energy derivative

\[
 p_i=-\frac{L_i}{V}\frac{\partial (V\rho)}{\partial L_i}
\]

using central differences plus one Richardson extrapolation. These results are
then compared with the existing direct-lattice extrapolation.

### Frozen geometries

The dimensionless side lengths are:

1. \((1,1,1)\);
2. \((1,1.25,1.25)\);
3. \((1,1,2)\); and
4. \((0.8,1.1,1.4)\).

The existing direct evaluator shall use symmetric cutoffs
\(N=(20,30,40,60,80,120)\) and its registered \(1/N^2\) extrapolation.

### Frozen acceptance tests

For every geometry:

- the relative energy-density discrepancy between the two methods must be at
  most \(2\times10^{-4}\);
- each pressure discrepancy, normalized by
  \(\max(|p_i^{\rm heat}|,|\rho^{\rm heat}|,10^{-14})\), must be at most
  \(5\times10^{-4}\);
- the heat-kernel stress trace \(|-\rho+\sum_ip_i|/|\rho|\) must be at most
  \(5\times10^{-5}\);
- the cube pressures must be mutually equal to relative tolerance
  \(5\times10^{-5}\) and satisfy \(p_i=\rho/3\) to that tolerance;
- permuting the side lengths must permute the pressure components while leaving
  \(\rho\) invariant to relative tolerance \(5\times10^{-5}\); and
- scaling all lengths by \(\lambda=1.7\) must scale \(\rho\) and every \(p_i\)
  by \(\lambda^{-4}\) to relative tolerance \(5\times10^{-5}\).

Quadrature warnings, non-finite values, a failed input hash, a failed symbolic
identity, or any failed acceptance test make the control fail closed.

## Receipt and replay requirements

The first execution shall create a new attempt directory and shall refuse to
overwrite it. It shall write deterministic JSON receipts with SHA-256
sidecars. Replay shall recompute the result in memory and compare exact JSON
bytes and hashes without rewriting the first-run receipt. The receipt must
retain individual checks, tolerances, raw values, provenance, exclusions, and
the explicit conclusion that the result is a control only.

## Claim boundary

A passing result would establish only:

1. exact agreement of the uncoupled dust-density normalization after convention
   conversion;
2. agreement of the existing CBR-001 nonzero-mode conformal-scalar formulas
   with an independent heat-kernel/Mellin implementation and the cited paper;
   and
3. a reproducible basis for a combined R4C1 manuscript outline.

It would not establish the R4C1 interaction dictionary, full kinetic or
gradient stability, zero-mode state selection, renormalized backreaction on an
anisotropic dynamical background, action-level force matching, observational
viability, or publication readiness.
