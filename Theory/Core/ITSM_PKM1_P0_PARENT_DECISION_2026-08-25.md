# ITSM PKM1-P0 finite-density parent decision

**Date:** 2026-08-25
**Branch:** `recovery/v12-core-architecture`
**Decision:** `HOLD_PKM1_P0_B_STABILITY_FIRST_CONTROL_ONLY_P0_A_REJECTED`
**Physics pass:** `false`
**Canonical-action change:** none
**Commit/push/publication:** not performed

## 1. Executive decision

The bounded PKM1 parent calculation produced three distinct results that must
not be collapsed into one `PASS` label.

1. **The interpolation used in the first PKM1 screen is rejected.** It passes
   static modified-Poisson ellipticity, but its independent radial khronon
   kinetic Hessian changes sign at finite acceleration.
2. **The metric-hosted parent action class is not rejected.** A
   stability-first `J(Y)` comparator has a regular four-degree-of-freedom
   Dirac count and a positive two-scalar kinetic matrix on an on-shell
   finite-charge FRW branch, including at zero spatial acceleration.
3. **The route is not solved.** The same canonical condensate necessarily
   supplies a positive lapse susceptibility and hence a Helmholtz term. Exact
   AQUAL is not a prediction of the tested parent. A local AQUAL regime is
   possible only if an unverified parameter window exists. The surviving
   `J(Y)` is fundamental EFT data, not an ITSM derivation.

The correct route status is therefore global `HOLD`, with one stability-first
control retained for the next falsification test. MAT-001, UVIR-003 and every
downstream gate remain unchanged.

## 2. Authority and non-inheritance

This decision is governed by the Core Identity Briefing, Tier-1 Route Test
Programme, live gate records and the earlier PKM1 broad-route decision. It
preserves the ITSM identity: a finite-density complex condensate, phase and
amplitude dynamics, compact topology, circulation sectors and possible
reservoir exchange remain part of the framework.

No result from Lambda-CDM, another khronon theory or an independent-aether
model was inserted as an ITSM premise. External theories are precedents and
null/comparator classes only. The retained FRW branch is derived from the
canonical ITSM condensate equations; it is not a Lambda-CDM background.

This document supersedes the earlier PKM1 screen only where that screen treated
its designed fast-transition interpolation as a viable global control. The
earlier static existence and source-normalization algebra remains a scoped
calculation, but it did not test the khronon kinetic Hessian.

## 3. Frozen local parent

On the smooth timelike phase chart

`Phi=(rho/sqrt(2)) exp(i Theta)`, `Z=-nabla_Theta^2>0`,

define

`U_mu=-nabla_mu Theta/sqrt(Z)`,

`a_mu=U^nu nabla_nu U_mu`, and `Y=a_mu a^mu`.

The P0 parent is

`S_P0=integral sqrt(-g) { (M_P^2/2)[R-2J(Y)]`

`       -(nabla rho)^2/2-rho^2(nabla Theta)^2/2-V(rho) }`

`       +S_m[Psi_m,g]`,

with the canonical mass-quartic-sextic condensate potential.

The phase defines the foliation once. There is no independent aether, no
separate force scalar, no direct `psi T` vertex and no appended freely chosen
`K(Q)`. Ordinary matter is minimally and universally coupled to the single
metric.

`J(Y)` is explicitly labelled **fundamental controlled IR EFT data**. P0 does
not derive it, its normalization or `a0` from the condensate potential,
topology, circulation or observations.

## 4. Rejection of the inherited P0-A interpolation

The first route screen used

`mu_A=(y+y^2+y^3)/(1+y+y^2+y^3)`,

where `y=sqrt(Y)/a0` and `1+J_Y=mu_A`.

It has positive static ellipticity eigenvalues. That is not sufficient for
the phase-defined khronon. The transverse and radial kinetic-Hessian
conditions are

`J_Y<0`,

`J_Y+2YJ_YY<0`.

Direct differentiation gives

`J_Y+2YJ_YY=(2y^3+y^2-1)/(1+y+y^2+y^3)^2`.

The numerator has one positive root,

`y_critical=0.657298106138376...`.

The radial Hessian is negative below this value and positive above it. Because
the physical Lagrangian kinetic eigenvalue is proportional to
`-(J_Y+2YJ_YY)`, it changes sign at a finite claimed background. A
lower-order lapse term cannot conceal this loss of principal kinetic sign.

**Disposition:** `REJECT_P0_A_FINITE_Y_RADIAL_KHRONON_KINETIC_SIGN_CHANGE`.

This is a failure of the selected interpolation, not a no-go theorem over all
metric-hosted parents.

## 5. Stability-first P0-B control

The hostile comparator

`mu_B=y/(1+y)`,

`J_B=-2a0^2[y-ln(1+y)]`

satisfies

`1+J_Y=mu_B`,

`J_Y=-1/(1+y)`,

`J_Y+2YJ_YY=-1/(1+y)^2`.

Thus both khronon kinetic eigenvalues have the correct sign for every finite
`y>0`. Its static eigenvalues are also positive:

`lambda_T=mu_B=y/(1+y)`,

`lambda_R=mu_B+y mu_B'=y(y+2)/(1+y)^2`.

At low acceleration,

`J_B=-Y+(2/(3a0))Y^(3/2)+...`,

and at high acceleration `mu_B->1` and `J_B/Y->0`. The field-equation
correction becomes subleading, although `J_B` itself does not approach a
constant.

**Disposition:** retain P0-B as a stability-first EFT existence control only.
It is not selected as the ITSM interpolation and has not passed PPN or data.

## 6. New pure-J high-acceleration tradeoff

Let

`delta(y)=1-mu(y)=-J_Y>0`.

Radial khronon kinetic positivity requires

`J_Y+2YJ_YY=-[delta+y delta']<=0`,

or equivalently

`(y delta)'>=0`.

After any finite `y0` for which `delta(y0)>0`, this implies

`delta(y)>=y0 delta(y0)/y`.

Therefore a globally stable pure-`J(Y)` parent cannot approach `mu=1` faster
than a `1/y` tail. Since

`dJ/dy=-2a0^2 y delta`,

the same condition forbids `J` from approaching a finite constant.

This is a mathematical tradeoff inside the pure-J action class. It is not by
itself a Solar-System exclusion: the PPN, ephemeris and strong-coupling test
has not yet been run. It does show why a fast static interpolation cannot be
accepted without independently checking its khronon kinetic Hessian.

## 7. Same-action lapse susceptibility

In uniform-phase gauge `Theta=mu_Theta t`,

`Q=sqrt(Z)/mu_Theta=1/N`.

The canonical phase term is already

`rho^2 mu_Theta^2 Q^2/2`.

In the notation

`(M_P^2/2)[R-2J(Y)+2K(Q)]`,

this is

`K_cond(rho,Q)=rho^2 mu_Theta^2 Q^2/(2M_P^2)`.

At fixed amplitude,

`K_QQ(1)=rho_0^2 mu^2/M_P^2>0`.

A direct Schur complement of the original amplitude-lapse action gives, after
stable Thomas-Fermi radial relaxation,

`K_QQ(1)=rho_0^2 mu^2(1+4mu^2/M_rho^2)/M_P^2`

`       =rho_0^2 mu^2/(M_P^2 c_s^2)>0`,

where

`c_s^2=M_rho^2/(M_rho^2+4mu^2)`.

Thus the relaxed radial response enhances the fixed-amplitude result by
`1/c_s^2`; it does not tune it away. The weak static equation contains

`m_K^2=K_QQ(1)/2`.

Exact AQUAL would require the finite density, charge or stable radial
susceptibility assumptions to fail, or a new operator to cancel the result.
No such cancellation is present in P0.

### Conditional local window

For a local wavenumber `k` and the relevant static ellipticity eigenvalue
`lambda_stat`, the Helmholtz term is negligible only if

`m_K^2/(lambda_stat k^2)<<1`.

Thomas-Fermi radial elimination simultaneously requires

`k^2<<M_rho^2`.

An overlap can exist only if

`m_K^2/(lambda_stat M_rho^2)<<1`.

Writing the charge-enthalpy fraction as

`f_h=rho_0^2 mu^2/(3M_P^2H^2)`,

the locality ratio at `k~1/R` is

`m_K^2 R^2/lambda_stat`

`=(3 f_h/(2c_s^2 lambda_stat))(H R)^2`.

This shows why the nonzero term need not automatically be fatal on a local
sub-Hubble patch. It also shows exactly which same-action parameters must be
derived before that claim is available. No physical ITSM window has yet been
established.

## 8. ADM/Dirac result

The exact unitary-gauge ADM action is

`S_P0=integral dt d^3x N sqrt(h) {`

` (M_P^2/2)[R3+K_ijK^ij-K^2-2J(Y)]`

` +(dot rho-N^iD_i rho)^2/(2N^2)`

` -D_i rho D^i rho/2+rho^2mu_Theta^2/(2N^2)-V }+S_m`.

The nonzero momenta are

`pi^ij=(M_P^2/2)sqrt(h)(K^ij-h^ijK)`,

`p_rho=sqrt(h)(dot rho-N^iD_i rho)/N`.

The primary constraints are `p_N=0` and `p_i=0`. The Hamiltonian is

`H=integral [N H0+N^iH_i+M_P^2N sqrt(h)J(Y)`

`            -sqrt(h)rho^2mu_Theta^2/(2N)]`.

The lapse secondary is

`C_N=H0+M_P^2sqrt(h)(J-2YJ_Y)`

`    -D_i[2M_P^2sqrt(h)J_YD^iN/N]`

`    +sqrt(h)rho^2mu_Theta^2/(2N^2)`.

In the smooth unitary chart, the six shift/momentum constraints are first
class and generate spatial diffeomorphisms. The pair `(p_N,C_N)` is second
class. With 11 unitary-gauge configuration variables,

`N_DOF=(22-2*6-2)/2=4`:

- two tensor modes;
- one phase/khronon scalar;
- one amplitude scalar.

For P0-B at generic finite `Y>0`, the transverse and radial principal
constraint eigenvalues are nonzero. At `Y=0`, `J_Y=-1` and the homogeneous
lapse bracket also contains `-rho^2mu^2`. The finite-charge parent therefore
does **not** inherit the engineered auxiliary control's zero-gradient
constraint-rank loss.

This is a local Dirac result on `rho>0`, `Z>0`. It does not cross defect cores
or non-timelike phase regions.

## 9. Background result

### Stationary Minkowski

For a stationary homogeneous finite-density condensate,

`epsilon=rho_0^2mu^2/2+V`,

`p=rho_0^2mu^2/2-V`,

so

`epsilon+p=rho_0^2mu^2>0`.

A cosmological constant shifts `epsilon` and `p` oppositely and cannot cancel
their sum. Exact stationary finite-density Minkowski space is therefore not an
on-shell P0 background. It would require loss of finite charge or a new
counterstress/reservoir sector.

### Evolving flat FRW

At homogeneous `Y=0`, `J(0)=0` and the retained equations are

`3M_P^2H^2=(rho_dot^2+rho^2mu^2)/2+V`,

`-2M_P^2 H_dot=rho_dot^2+rho^2mu^2`,

`rho_ddot+3Hrho_dot-rho mu^2+V_rho=0`,

`d(a^3rho^2mu)/dt=0`.

A deterministic dimensionless existence branch was integrated from these
equations. Its maximum relative diagnostics were:

- Friedmann residual: `2.40033115205762e-10`;
- charge drift: `2.22044604925031e-16`;
- continuity residual: `1.44366881110785e-15`.

These numbers validate the integration only. They are not a cosmological fit
or evidence for an observed ITSM background.

## 10. Reduced FRW scalar Hamiltonian information

In uniform-phase gauge, the retained scalar coordinates are

`x=(R,delta_rho)`.

Eliminating lapse and scalar shift from the independently reconstructed ADM
quadratic action gives

`K=[[((rho_dot^2+rho^2mu^2)+C_Jq^2)/H^2,-rho_dot/H],`

`   [-rho_dot/H,1]]`,

where `C_J=-2M_P^2J_Y(0)=2M_P^2` for P0-B. Its determinant is

`det K=(rho^2mu^2+C_Jq^2)/H^2>0`.

At strict `q=0`,

`det K=rho^2mu^2/H^2>0`.

The constraint determinant is

`det C=-4M_P^4H^2`,

which is nonzero on the expanding branch. A scan of 1,952 matrix samples found
zero negative and zero numerical-zero kinetic eigenvalues; the minimum scanned
strict-`q=0` determinant was `0.679755144943642` in the selected dimensionless
existence example.

This establishes a positive kinetic Hamiltonian block, not a globally
positive conserved Hamiltonian on time-dependent FRW. The local equation
generator retained background and volume-factor derivatives; its eigenvalues
remain diagnostics, not invariant global instability rates.

After radial elimination in a controlled fixed-metric patch, the phase mode
has

`omega^2=(rho_0^2 k^2/2)`

`        /[rho_0^2/(2c_s^2)+M_P^2k^2/mu^2]`.

It reduces to `omega^2=c_s^2k^2` at low momentum and receives a positive
`k^2`-dependent time kinetic term from `J`. Its formal `omega/k->0` UV scaling
cannot be promoted beyond the Thomas-Fermi domain `k^2<<M_rho^2`.

## 11. A0-A6 classification

| Stage | Result | Classification |
|---|---|---|
| A0 identity/domain | Smooth finite-density phase defines one foliation on `rho>0`, `Z>0`; cores and winding charts open | `CONDITIONAL_PASS_LOCAL_CHART` |
| A1 action | One explicit local covariant parent; no phase/aether/force duplication; `J` fundamental | `PASS_ACTION_DECLARATION`, microscopic origin open |
| A2 symmetry/DOF | Four local DOF; no finite-charge `Y=0` rank loss; P0-A radial sign failure | `PASS_P0_B_LOCAL_COUNT`; `REJECT_P0_A` |
| A3 static/local limit | Universal source retained; exact AQUAL blocked by positive same-action `m_K^2`; local window conditional | `HOLD_PARAMETER_WINDOW` |
| A4 stability | P0-B Hessians and FRW kinetic block positive; nonlinear zero-gradient cutoff and stationary galactic Hamiltonian open | `PARTIAL_PASS_QUADRATIC`, global `HOLD` |
| A5 observables | PPN, Shapiro, lensing, GW, compact objects and data not run | `NOT_RUN` |
| A6 UV/completion | `J`, `a0`, radiative stability, cutoff, topology and reservoir not derived | `HOLD` |

## 12. Reproducibility

Primary calculation:

- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md`
- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/itsm_pkm1_finite_density_parent_hamiltonian.py`
- generated JSON, Markdown, FRW CSV and SHA-256 manifest under `outputs/`.

Independent reproduction:

- `Analysis/MAT/MAT-001/PKM1_METRIC_HOST/itsm_pkm1_p0_independent_reproduction.py`
- generated JSON, Markdown and SHA-256 manifest under `outputs/`.

The independent script does not import the primary calculation. It separately
reproduces the P0-A sign change, P0-B Hessians, original-action radial Schur
complement and direct ADM constraint elimination. It also rejects four
claim-changing mutations and verifies all five primary manifest hashes.

Both calculations reproduce byte-identical outputs on repeated runs.

## 13. Exact next decision test

Do **not** proceed to SPARC or phenomenological fitting. The next cheapest
dependency-clearing test is a bounded P0 high-acceleration/locality
falsification:

1. combine the pure-J stable-tail inequality with the repository's
   Solar-System, PPN, Shapiro and GW requirements;
2. derive the permitted asymptotic tail and any unavoidable anomalous
   acceleration without fitting galaxy targets;
3. intersect that domain with
   `m_K^2/(lambda_stat k^2)<<1`, `k^2<<M_rho^2` and the physical EFT cutoff;
4. require one nonempty parameter domain from the same action;
5. if the intersection is empty, reject pure P0 and only then consider a
   separately declared extrinsic-curvature completion with its own DOF,
   PPN/GW and strong-coupling audit.

This test is more upstream than a full galactic solver: it can kill the pure
P0 route before expensive local-gravity work.

## 14. Gate firewall

- MAT-001 remains `BLOCKED`;
- UVIR-003 remains `IN_PROGRESS`;
- live-route `V` remains `NOT_COMPUTED`;
- live-route `K_Q` remains `NOT_DERIVED`;
- `a0` and its coefficient remain underived;
- the live separate-`psi` action remains a frozen control;
- no canonical action, local-gravity, lensing, disk, SPARC, cosmology or
  publication gate is opened.
