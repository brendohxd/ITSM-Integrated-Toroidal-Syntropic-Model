# G3N5 sharper prepared-dust upper bound: replay-pending checkpoint

Date: 11 October 2026. Version 1. Owner: Master Test 1 / stage 1 / B1.
Result: CONDITIONAL_UPPER_BOUND_TIGHTENED. First execution 73/73 local checks.
Exact read-only replay is RUNNING at this checkpoint, not claimed passed.
Full dust milestone OPEN; physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED.

## Outcome and acceptance gap

For ORIGINAL prepared data, all 20 coupled states and actual dust observables,
the new coefficient in the previously derived inequality

```text
||W_full(t)-Phi(t) W0||_infinity <= C2(t) ||W0||_infinity / ell^2
```

is C2(1/20)=767652.5840961253 (display). The old coefficient remains intact
at 168549167.52104756. This is about 219.564-fold tighter without changed
physical evolution, initial conditions, action parameters or fitted constants.
It remains much too conservative for useful small-error certification.

| ell | Newly reconstructed absolute error | New endpoint upper bound |
|---:|---:|---:|
| 16 | 0.0004418373158664446 | 2998.6429066254896 |
| 32 | 0.00011046044682905265 | 749.6607266563724 |
| 64 | 0.00002759425428122686 | 187.4151816640931 |

The actual errors still decrease with momentum, but this numerical trend and
a smaller upper constant do not prove the sharp/actual order. These are upper
bounds, not measured growth, instability, or physical errors of these sizes.
The stored archive is byte-identical. Reconstruction displays differ from the
older reconstruction by roughly 1e-14 floating evaluation roundoff; no archived
trajectory or original receipt has been recalibrated or rewritten.

The high-mode inverse domain is ell>=15, t in [0,1/20], on the registered
rotating B1 Friedmann shell with a,C,rho_m>0 and J=1. Modes 4,8 remain in the
archive and retain their separately certified full-propagator bounds; T2 is
not used below its domain. This coordinate-inverse condition is NOT a physical
EFT momentum/frequency window, and does not authorize high-ell phenomenology.

## Structural improvement, not removal of physical couplings

Let D be the Pf/Po diagonal compression with Pf selecting 9,19. Since Q and
Q_dot commute with Pf, the energy form of D(A_w) is exactly the compression
of the COMPLETE A_w energy form. It inherits the full mu<60 energy bound.
This replaces the old large comparison exponent, not actual coupled evolution.

Use the unchanged T2=I+V/ell^2, retaining V_dot. The off-block V permits

```text
T2^-1 = (I-V/ell^2)(I-V^2/ell^4)^-1.
```

Separate even/odd Neumann bounds control diagonal deviation and off coupling.
The resulting diagonal comparison exponent is gamma=45.374056156265 (display),
rather than the earlier 133.0416882568903. The actual full y propagator is
still bounded by 3 exp(30 dt), and the complete fast response stays in the
variation-of-constants integral. All inverse restrictions are interval-derived.

In addition, reconstruct R2 through R5 from the complete A_c,H_j,H_j_dot,M
and bound their EXACT matrices on the preserved shell. This replaces the old
product-of-norm source majorant; it does not delete any forcing term. Exact
identities reject omitted V_dot, fast cross terms and nonzero residual source.

The new coefficient, with the same original mismatch/observation constants,
is explicitly

```text
C2(t)=(3/2)[K_O{3 exp(30t)(C_other+2 K_W K_source t)
                +3 kappa t exp(gamma t) C_fast}
            +3 K_Of exp(30t) C_fast+K_observation exp(21t/10)].
```

All rational constants and complete residual matrices are exported in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_dust_sharper_attempt_01/formulas.json).
No value was selected using the archived errors. This still compares to the
LEADING dust generator M. The separately verified formal N_obs correction
has not been substituted into this theorem: its full corrected-system
remainder is a distinct remaining obligation.

## Controls, preservation and remaining work

Independent numerical transformed-generator residuals are below 2.3e-16;
direct/Laurent source identities below 1.7e-14. All-five-mode actual-observation
and 22-field reconstruction differences are below 1.8e-14. Full diagonal
energy, perturbation and coupling samples at t=0,1/40,1/20 lie within their
whole-interval constants. All original 257 times/four columns are retained;
original complementary nonmonotonic responses are untouched. Samples check
implementation; the exact identities and interval inequalities supply the bound.
The original -11/6 term, ordinary-wave Jordan defect and indefinite physical
Hamiltonian are not removed or reclassified. Q is a transfer norm, not that
physical Hamiltonian or a positivity proof.

489 pinned input/source/available-sidecar files preserved hash/size/mtime.
Original failed attempts and missing inherited sidecars remain declared.
First-run computation is TERMINAL; exact replay runs on a separate known
handle. No replay result or completed full milestone is inferred from silence.

Next requirements remain: finish replay, extend/control the full corrected
lift for N_obs with original mismatch and retained fast/wave forcing, prove or
reject actual order, and obtain useful accuracy within the declared domain.
The private fast-time leading candidate cancels exactly and cannot establish
sharpness. A nonzero formal N_obs alone also does not establish sharpness.

## Frozen evidence

[Contract](RES001_R4C1_G3N5_SHARPER_DUST_BOUND_CONTRACT_2026-10-11.md):
b9759219cc782514194af5e45798337062c16a483f28bfeb04371e44d63d6823.
[Executable](../../../Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_sharper_v1.py):
c5db997e9dfef8b4276ced6c1fc5a21ac25872b1c4ec343de453b5d29e0ce3c5.
[Summary](../../../Analysis/MasterTests/outputs/r4c1_g3n5_prepared_dust_sharper_attempt_01/summary.json):
34d6f2504c82bf3264fd4625947fa66dc28f533c5c3501115e492898175f22e8.
Formula hash: e3278b7ad861582afad1bf1c1602d964c1e0476280fb8d9199323b8d667b83df.
Diagnostics hash: 306789bf9fe63abbeaba17d62a3b7935cad4dc3f0ab464fe532b9c39d9955d22.
[Formal actual-observable correction](RES001_R4C1_G3N5_OBSERVABLE_CORRECTION_REPORT_2026-10-11.md)
has separate 29/29 checks and completed exact replay, not a corrected-system bound.

Stage 1 and the full native goal remain incomplete. Stage 2 action-selection
stop/physical-window gap and stage 3 matching gap are unchanged. Tests 1-3
HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED. Reviews remain DEFERRED.
The memory skill separates conditional local evidence from canonical promotion;
current source/receipts are authority. No vault mutation, provider/model dispatch,
publication, submission, commit/push, manuscript/PDF or deployment change.
