# M4 P0-B: physical pole/domain disposition

5 November 2026. Unchanged PKM1-P0-B control; High explicitly retained.
The usable implementation is `m4_pole_domain_v2.py`, with fresh receipt
`Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/m4_pole_domain_v2_20261105/receipt.json`.
The exact retarded metric response already calculated remains valid in its
declared linear-control scope. A controlled physical pole/residue has NOT
been established. This calculation identifies why taking larger momentum
alone does not supply the missing slow-frequency/background hierarchy.

## Parent and scope

Use the corrected V3 source/shift convention in
[the sign-repair owner](MAT001_M4_P0B_SHEAR_SOURCE_REPAIR_V2_REPORT_2026-11-05.md):
`Sigma=+q^2 beta`, source constraint vector `(-delta_e,-j/q^2)`.
No parent coefficient, source, potential, background initial data, acceptance
tolerance or original scientific hash was changed. Set `M=M_P^2`, `C_J=2M`.

The exact asymptotic statements below concern one initial event on the
expanding FRW solution, with `rho_dot=0`, `V_rho=rho mu^2`, positive
`M,H,rho,mu`, and nonzero physical harmonic `q`. The nonnegative-potential
assumption is used explicitly in the bound. Equilibrium is imposed AFTER
time differentiation; it is not imposed on subsequent evolution.
This is not a result for all backgrounds, all actions, or nonlinear evolution.
The genuine homogeneous scalar and harmonic-vector sectors retain their
separate constraints; they are not obtained by sending nonzero q to zero.

## Completing the local quadratic calculation

The exported reduced action has fields `x=(R,delta_rho)` and measure `a^3`:

    L/a^3 = x_dot^T K x_dot/2 + x_dot^T D x + x^T F x/2.

Write `D_s=(D+D^T)/2`, `D_a=(D-D^T)/2`. Integration by parts gives

    F_e = F - dot D_s - 3H D_s,
    O = K d_t^2 + (dot K+3H K+2D_a)d_t
                  + (dot D_a+3H D_a-F_e).

At the registered event, retaining the background equations gives exactly

    K = diag((rho^2 mu^2+2M q^2)/H^2, 1),
    2D_a = [[0,-2rho mu^2/H],[2rho mu^2/H,0]],
    F_e = [[-rho^2 mu^2 q^2/H^2, mu^4 rho^3/(2M H^2)],
           [ mu^4 rho^3/(2M H^2), mu^2-V_rhorho-q^2]].

The derivative terms alter the leading q^2 curvature entry. Reading the
original `F` as a physical mass matrix is therefore incorrect.

For a full evolving canonical normalization use `x=T y`, where

    kappa=(rho^2 mu^2+2M q^2)/H^2,
    T=a^(-3/2) [[1/sqrt(kappa),0],
               [rho_dot/(H sqrt(kappa)),1]].

Exactly, `a^3 T^T K T=I` on the background constraint. Define

    E_c=a^3(T^T K dot T+T^T D T),
    F_c,raw=a^3(dot T^T K dot T+dot T^T D T
                +T^T D^T dot T+T^T F T),
    F_c=F_c,raw-d_t(E_c+E_c^T)/2,  G=E_c-E_c^T.

Then the EXACT transformed evolution equation is

    y_ddot + G y_dot + (dot G/2-F_c)y = transformed_source.

For the already derived external-source terms the right-hand side is exactly
`a^3 T^T(s_x-dot s_v-3H s_v)`. Thus normalization does not remove derivative
sources, the Ward conditions or the lapse/shift source-contact terms in the
separate metric observation map.

All derivatives of T, measure, mixing and constraints are retained. The
receipt exports the full event matrices, including `dot G`. The conservative
local diagnostic `det(-omega^2 I-i omega G-F_c)` additionally freezes those
coefficients and omits `dot G/2`; it is not the exact retarded Green function.
Neither this prescription nor freezing the unnormalized fields establishes
a physical pole without error control for the evolution being approximated.

## Exact large-momentum limits

Keeping finite amplitude mixing, the unnormalized conservative diagnostic
has a slow root tending to

    omega_raw,slow^2 = rho^2 mu^2/(2M).

For the normalized conservative diagnostic,

    omega_c,slow^2 = -H^2/4 + 13rho^2 mu^2/(4M)
                            -rho^4 mu^4/(2M^2 H^2),
    omega_c,fast/q -> 1.

These limits follow from the full two-by-two determinants, not radial
elimination. Their differing slow limits are of background order. They
illustrate why freezing and an evolving field redefinition cannot be freely
interchanged when background terms are comparable to the proposed frequency.

Let `X=rho^2 mu^2/(M H^2)`. Friedmann at this event gives
`3M H^2=rho^2 mu^2/2+V`, hence `0<X<=6` if `V>=0`. Then

    omega_c,slow^2/H^2 = -1/4+13X/4-X^2/2
                       = 161/32-(X-13/4)^2/2 <= 161/32.

Where that diagnostic root is oscillatory, `omega_c,slow/H <= 2.2431`.
Also `|mu_dot/mu|=3H`, so

    |mu_dot/mu|/omega_c,slow >= 3sqrt(32/161) > 1.

The usual sufficient hierarchy in which all background rates are small
compared with the slow frequency is not obtained by increasing q. This
is a scoped obstruction to that high-q justification, NOT a theorem excluding
every possible approximation, exact time-dependent solution or physical
regime on P0-B. Correlated background evolution requires its own controlled
analysis; a failed sufficient adiabatic criterion is not an instability proof.

The slow branch cannot simply be replaced by the fast amplitude root. At
the event the exact source-free metric reconstruction gives

    Psi = (1+rho^2 mu^2/(2M q^2)) R_dot/H
          -rho mu^2 delta_rho/(M q^2).

For the formal normalized slow eigenvector `y=(1,O(q^-3))`,

    q Psi -> [-i omega-H/2-rho^2 mu^2/(2M H)]/sqrt(2M).

Thus the slow branch has nonzero metric overlap. This overlap is a diagnostic,
not a signed physical residue. The fast mode may also couple; its own physical
domain and residue require analysis and cannot certify the slow-force result.

The earlier fixed-metric phase expression agrees with the raw formal plateau,
but its radial-elimination assumption was `q^2 << M_rho^2`. Here
`M_rho^2=V_rhorho-mu^2=11/20` initially. None of the five nonzero benchmark
harmonics has that hierarchy at a=1. The old expression explicitly called its
literal infinite-q limit a scaling diagnostic. The present calculation keeps
the amplitude; it does not upgrade that older approximation's validity.

## Numerical diagnostics and verification

Frozen benchmark: `M=1`, polynomial potential and charge as in the preceding
response, `a=rho=1`, `rho_dot=0`, `mu^2=101/80`, `H^2=287/720`.
All q here are in that control's units, not an observational scale or an
assertion that arbitrarily large q lies below an interacting cutoff.

| q | Local normalized slow omega^2 | Local normalized fast omega^2 | 3H/omega_slow |
|---|---:|---:|---:|
| 1 | -0.23546643 | 5.35135952 | No oscillatory slow root |
| 4 | 1.88148432 | 16.84981829 | 1.38084729 |
| 16 | 1.99959963 | 256.61264889 | 1.33944360 |
| 64 | 2.00387520 | 4096.60077904 | 1.33801388 |
| 256 | 2.00413035 | 65536.60004865 | 1.33792871 |

At q=1 the unnormalized diagnostic instead has positive slow omega^2,
0.02884772. Both come from the same evolving equations. Preserve that
difference: it prevents interpreting the normalized negative diagnostic as
a demonstrated ghost, tachyonic physical pole or model exclusion. Positive
roots at the other modes likewise do not establish stability or a cutoff.

The usable V2 executable passes 32/32 controls and byte-identical replay:
exact integration-by-parts and transformed Euler identities; mixed-mode
asymptotics; the completed-square bound; actual metric overlap; direct numeric
Schur reduction of the uneliminated constraint system at five modes; and an
independent background-flow finite-difference check of normalized derivatives
at q=1,4,16 using two step sizes. The latter scaled differences are below
6e-10. They test implementation agreement, not rigorous continuum errors.

V1 was interrupted during symbolic expression swell before producing a
receipt; its executable remains preserved. V2 uses an explicit two-by-two
determinant to avoid that swell, aligns the independent factorization with
the declared whitening chart, and preserves the negative q=1 diagnostic
rather than assuming all local roots are oscillatory. No numerical acceptance
tolerance was relaxed. Private interrupted-run notes remain under `.local`.

## Disposition and handoff

- This bounded pole/domain TEST is complete: there is no demonstrated
  controlled slow-force pole from the proposed high-q hierarchy at this event.
- Full physical M4 remains INCOMPLETE. A physical signed residue, interacting
  cutoff and a controlled finite-domain approximation to the actual retarded
  response are still required. No missing residue is replaced by a bare field
  coefficient. J/a0 remain declared free control inputs; live Track-A V is not
  computed and MAT-001 is not promoted.
- Continue the independently authorized unfinished U3 B1/B2 analytic controls.
  They do not require pretending the P0-B pole is solved or adopting a new
  parent. Preserve P0-B's larger physical-window task in the backlog.

Rule-9 DEFERRED. `physics_pass=false`, `gate_effect=NONE`. No publication,
commit/push, external provider dispatch, runtime reconfiguration or vault write.
