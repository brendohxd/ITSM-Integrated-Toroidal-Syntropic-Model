# R4C1-G3F: finite-k full-system check of the prepared slow plane

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / G3 family.
Review DEFERRED; gate effect NONE; physics_pass=false.
Replay verification: all three artifacts recomputed byte-identically.

## Decision and scope

The registered calculation passes **106/106 local checks**. Eighteen
full-system integrations (nine eta/k cases, two methods) all complete. The
prepared full solutions approach the truncated G3E slow approximation under
both k doublings at each tested eta. The largest approximation error at
k=80 is **0.188274%** over the registered interval t in [0,1], below the
preregistered 5% diagnostic target.

The initial finite-k symplectic coefficient is negative in the declared
ordered slow basis for all nine cases, approaches G3A's K_s=1-12/eta, and
is transported by the actual full equations with worst relative drift
2.711e-12. This supplies finite-time numerical support for the formal slow
branch; it is not merely a frozen-coefficient or reduced-ODE check.

Here "full system" means G3S's coupled six-scalar canonical ODE after S1's
constraint reduction in its registered nonsingular chart. It does **not**
mean every gravity, matter, quantum, anomaly or renormalization sector is
complete. These dimensionless k values have not been placed inside a
derived physical EFT window. Arbitrary fast-wave data, uniform eta->0
control and a full PDE/remainder theorem remain open.

A symplectic coefficient in an ordered solution basis is not by itself a
basis-independent positive-frequency norm or an energy signature. The
[G3A action result](RES001_R4C1_G3_SLOW_ACTION_REPORT_2026-09-30.md) retains its
negative kinetic coefficient for the frame-based slow coordinate X. A
physical dust-density coordinate may mix X with its momentum; its action
and energy interpretation require an explicit transformation, not a sign
choice. No physical quantum ghost, positive-energy theorem or all-action
no-go is claimed here. The GR density-growth control remains intact.

## Frozen protocol and exact identities

The unchanged [G3F contract](RES001_R4C1_G3_FINITE_K_CONTRACT_2026-09-30.md)
was frozen before calculation. Use eta=(1,1/4,1/16), k=(20,40,80), fixed
comoving k, and 101 equally spaced samples on [0,1]. This is a declared
subset of G3's six-member family, not coverage of the full eta interval.

For phase vector y=(x,xdot), the full canonical system is

\[
 \dot y=A y,\quad
 A=\begin{pmatrix}0&I\\-W&-G\end{pmatrix},\qquad
 J=\begin{pmatrix}G&I\\-I&0\end{pmatrix}.
\]

The exact source identity W-W^T=Gdot implies

\[
 \dot J+A^TJ+JA=0.
\]

This identity is verified symbolically with the full background flow. It
implies preservation of Y^T J Y for actual full solutions Y; it does not
assert conservation of a time-dependent cosmological Hamiltonian.

Use the G3E exported position embedding E_q through its retained force
orders and leading propagating order. Set the uncomputed next propagating
amplitudes to zero, explicitly retaining this truncation as a limitation.
With B=[[0,1],[-m_E,0]], construct

\[
 E_v=\dot E_q+E_qB,\qquad E=\binom{E_q}{E_v}.
\]

The position defect vanishes identically. The lower embedding defect is
\(-W E_q-G E_v-\dot E_v-E_vB\), evaluated with full coefficient derivatives.
Both initial full columns are E(0,k), representing (X,Xdot)=(1,0),(0,1).
The comparison is against E(t,k)F_s(t), where F_s solves the evolving slow
2x2 equation, not a frozen mass equation.

Backgrounds are independently integrated by DOP853 and Radau at
rtol=1e-11, atol=1e-13. Both perturbation methods then share the DOP853 dense
background to isolate their numerical comparison. The slow reference uses
the same tighter tolerances. Full columns use rtol=1e-9, atol=1e-11, with
the exact row-major linear Jacobian A tensor I_2 supplied to Radau. No old
receipt-producing main() is called; only the pinned pure background RHS.

## Entire registered grid

Approximation error below is max_t ||Y-E F_s||_F/(1+||E F_s||_F), maximized
over both solvers. Omega_0 is the initial coefficient in the declared
ordered basis. Defect is max_t ||lower defect||_F/(1+||E||_F). These are
chart-dependent diagnostics, not observational likelihoods.

| eta | k | Minimum k/a | Full-column error | Omega_0 | Normalized defect |
| --- | --- | --- | --- | --- | --- |
| 1 | 20 | 9.32456 | 0.0165236751 | -10.8571760 | 0.4286198133 |
| 1 | 40 | 18.64912 | 0.0063021101 | -10.9633821 | 0.2920017284 |
| 1 | 80 | 37.29823 | 0.0018827337 | -10.9907885 | 0.1665142501 |
| 1/4 | 20 | 13.23207 | 0.0040748032 | -46.9643100 | 0.0854963718 |
| 1/4 | 40 | 26.46414 | 0.0017945579 | -46.9909736 | 0.0734094614 |
| 1/4 | 80 | 52.92828 | 0.0006742438 | -46.9977369 | 0.0544924699 |
| 1/16 | 20 | 15.11723 | 0.0011067694 | -190.9806098 | 0.0227880074 |
| 1/16 | 40 | 30.23445 | 0.0005399258 | -190.9951367 | 0.0219002853 |
| 1/16 | 80 | 60.46890 | 0.0002504375 | -190.9987832 | 0.0201707824 |

The corresponding formal symplectic coefficients are -11, -47 and -191.
At k=80, their relative initial discrepancies are respectively
8.37407e-4, 4.81510e-5 and 6.37075e-6. Both doublings reduce these errors.

Worst background method discrepancy is 4.036e-12; worst full-column method
discrepancy is 1.07501e-8, below the registered 1e-7 target. Worst relative
symplectic transport drift is 2.711e-12. The maximum separately reported
slow-coordinate/velocity error at k=80 is 7.08843e-4 (0.0708843%).

The normalized pointwise embedding defect is not uniformly tiny: it reaches
0.42862 at eta=1,k=20, and is still 0.16651 at eta=1,k=80. Small integrated
solution errors do not turn this into a rigorous operator/PDE remainder
bound. There is no registered pass threshold for this defect; report it
alongside, not behind, the finite-time approximation successes.

## Provenance and reproduction

| Artifact | SHA-256 |
| --- | --- |
| Frozen contract | `75050556086b27f794b2378ac389f6bb864ae03e4441c395ff5fc64538b1cd55` |
| Executable | `24ef13486d8477cb021dc4931d6e64c6d6fcc8fa52a330c106515c4507624504` |
| Attempt 01 summary | `3c3241a44e43b986971c8c340643b6b9c87ca97c803347cb9da5c0a934fa05e1` |
| Position/velocity embedding | `c235d8c9f81314f01ade15dddd215263fc22754efa6caee485d793f85e432300` |
| Full/reference columns | `2a7df2c3ca35f5d438f54520241c880692c9804d03f3bf1bf696cf183345bccc` |

The columns array has shape (3,3,3,101,12,2), with axes eta,k,run,time,
phase component,initial column. Runs are DOP853, Radau and the truncated
slow reference. The receipt includes the full grid, solver evaluations,
endpoint columns, all checks, runtime versions and source pins. Existing
outputs are refused; replay recomputes and compares all artifacts without
writing. No registered failure was dropped or threshold changed.
The completed replay exits zero with the same 106/106 validation and all
artifact hashes unchanged.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_finite_k.py --replay
```

## Disposition and next requirement

PROCEED_PROVISIONALLY applies to the specified finite-time, well-prepared
full-scalar comparison and symplectic-transport diagnostics. They strengthen
the approximation evidence beyond the previous formal large-k derivation.
They do not derive a physical EFT cutoff or justify energy/norm claims.
The next action-interpretation requirement is an explicit physical
dust-density phase/action map, including its invertibility and any singular
domain; do not infer a dust ghost from the frame-based X coefficient.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A and their
scope/review debt. Canonical Tests 1-3 HOLD_SUBSTANTIVE; claim CONDITIONAL,
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage 4A CLOSED; TOP-X4 unchanged. No PDF edit, provider dispatch, commit,
push or publication occurred. Prior sources, receipts and hashes remain
unchanged; local command logs remain ignored.
