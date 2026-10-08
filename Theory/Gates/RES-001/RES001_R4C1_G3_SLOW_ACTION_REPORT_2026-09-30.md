# R4C1-G3A: signed formal slow action and symplectic audit

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / G3 family.
Review DEFERRED; gate effect NONE; physics_pass=false.

## Decision and affected use

The corrected action audit passes **28/28 local checks**. The leading
well-prepared slow branch has the signed kinetic coefficient

\[
 K_s=1-\frac{12}{\eta}=-\frac{12-\eta}{\eta}<0,
 \qquad 0<\eta\leq1.
\]

The independent canonical symplectic pullback agrees with this coefficient.
This is a result about the formal branch's action, not a choice of sign when
normalizing its equation of motion. A positive-energy certificate for this
branch is **not supported** by this calculation. Do not reverse the action's
overall sign to manufacture one.

The [G3E evolving reduction and GR density control](RES001_R4C1_G3_ZERO_EVOLUTION_REPORT_2026-09-30.md)
remain intact: the formal dust-only limit reconstructs the GR density modes
\(a\) and \(a^{-3/2}\). Those equation-level checks do not establish positive
energy or a healthy full GR limit. Conversely, this formal sign result alone
does not establish a stationary quantum ghost, an observational rejection,
or an all-action no-go.

## Registered scope and derivation

Follow the unchanged [frozen G3A contract](RES001_R4C1_G3_SLOW_ACTION_CONTRACT_2026-09-30.md),
G3S's full canonical matrices and G3E's evolving embeddings. The calculation
uses fixed comoving \(k\), the complete registered background flow, and the
domain \(0<\eta\leq1\), \(H>0\), \(a,C,\rho_m>0\), with S1's retained auxiliary
rank restrictions. It does not invert through \(\eta=0\), \(H=0\), \(k=0\),
or a rank-changing constraint boundary.

Start with the signed canonical action

\[
 L=\tfrac12\dot x^T\dot x+\dot x^TM_cx-\tfrac12x^TV_cx.
\]

Writing \(M_s=(M_c+M_c^T)/2\), \(G=M_c-M_c^T\), and
\(Q=V_c+\dot M_s\) gives the exact boundary relation

\[
 L=\tfrac12\bigl(\dot x^T\dot x+\dot x^TGx-x^TQx\bigr)
   +\frac{d}{dt}\left(\tfrac12x^TM_sx\right),
 \qquad Q+\tfrac12\dot G=W.
\]

Pull back to G3E's time-dependent embedding. Retain all three force orders
and the next propagating amplitudes until cancellation; do not insert the
slow equation before variation. The prospective positive powers of \(k\)
cancel, the dummy next amplitudes drop out of the constant coefficient, and
the leading action before its last boundary subtraction is

\[
 L_0=\tfrac12\dot X^2+\frac{6}{\eta}X\ddot X
       -\tfrac12K_s m_E X^2.
\]

Since \(\eta\) is time independent,

\[
 L_0=L_s+\frac{d}{dt}\left(\frac{6}{\eta}X\dot X\right),
 \qquad L_s=\tfrac12K_s(\dot X^2-m_E X^2).
\]

The mass coefficient agrees exactly with G3E:

\[
 m_E=-\frac{H^2}{4}-\frac{\dot H}{2}
     -\frac{\rho_m}{2M_c^2}
     +\beta(\ddot\psi+H\dot\psi)-\beta^2\dot\psi^2,
 \quad M_c^2=1-\eta/12,\quad\beta=2\eta^2/5.
\]

Here \(M_c^2\) is the background effective Planck coefficient, not the
mixing matrix \(M_c\). Variation gives
\(K_s(\ddot X+m_EX)=0\), with zero first-derivative coefficient. The negative
kinetic sign arises from the retained acceleration-linear term and its
integration by parts; discarding that term would produce an incorrect sign.

## Independent symplectic and Hamiltonian checks

Use the original momentum \(\pi=\dot x+M_cx\), not a velocity-only metric.
The slow equation is used only to construct the on-solution phase map.
With the declared convention \(\Omega=d x\wedge d\pi\), its leading
pullback in \((X,\dot X)\) is

\[
 \Omega_s=K_s\,dX\wedge d\dot X,
 \qquad [\Omega_s]=\begin{pmatrix}0&K_s\\-K_s&0\end{pmatrix}.
\]

The independent regular rational-event congruence and the full-action
boundary identity both hold exactly. Under the declared physical-amplitude
normalization \(X=\sqrt\eta\,\chi/k\), the \(\dot\chi^2\) coefficient is
\(-(12-\eta)/k^2\), still negative. This rescaling does not certify the
singular endpoint or remove its original rank change.

For \(P_X=K_s\dot X\),

\[
 H_s=\frac{P_X^2}{2K_s}+\frac{K_sm_E X^2}{2},
 \qquad \left.\frac{dH_s}{dt}\right|_{\rm EOM}
       =\frac{K_s\dot m_E X^2}{2}.
\]

This is a time-dependent reduced Hamiltonian, not a conserved global
cosmological energy. Its frozen Hessian in \((P_X,X)\) is
\(\operatorname{diag}(1/K_s,K_sm_E)\). The registered 72 background samples
(six eta values, two integration methods, six times) all have negative
\(K_s\). Sixteen have a negative-definite instantaneous Hessian; 56 have an
indefinite one; none is degenerate. The sampled mass range is
\([-0.1262487767769776,0.08068669640296501]\), and the maximum normalized
action/Euler coefficient discrepancy is \(2.695\times10^{-16}\).

These instantaneous signatures are not conserved-energy or stationary
positive-frequency pole classifications. Positive full six-field velocity
weights alone do not supply the missing slow-branch energy theorem.

## Failed and interrupted attempts: preserved, not overwritten

1. Attempt 01 / v1 passed 14/26 checks and failed 12. Its use of
   `expand(expr).coeff(k,n)` did not normalize denominators containing powers
   of k. The alleged coefficients still depended on k; its K=1 extraction
   therefore was invalid. Its static status label is **not** a validated
   physics conclusion. Preserve its receipt, formulas and exact v1 source.
2. Attempt 02 / v2 normalized the entire rational action at once. That
   simplification was interrupted for runtime cost before any receipt or
   output directory was created. No mathematical or physics verdict follows
   from the interruption. Preserve its exact source.
3. Attempt 03 / v3 normalizes each expanded term's denominator, extracts
   polynomial powers, groups equal Laurent powers, then simplifies the
   required coefficients. It rejects non-Laurent denominators, k-dependent
   coefficients and unchecked growing powers. No action, parameter,
   background, target, tolerance or prior receipt was changed. The retained
   symplectic calculation independently checks the corrected kinetic sign.

## Provenance and reproduction

| Artifact | SHA-256 |
| --- | --- |
| Frozen contract | `f6a35a4ade82c8d925b44d6984164eb761e50015936623b0683e071516f62a43` |
| Current v3 executable | `64e59e69851734cd24a4abbd31d7b02b17490395b1d841b1a0f06bd246681b90` |
| Retained v1 executable | `c7b36994f7e4cf778104d68c9d263a5d59ed460103f24f6d43ef0ab9887f65df` |
| Retained v2 executable | `ab7e4598ddb2780e1134e53364c3fa196c0016b66ff27056965c0ec876005954` |
| Failed attempt 01 summary | `eb39cd319866eff4993e7719d873076e395581db7993339debfb106ed84d7914` |
| Failed attempt 01 formulas | `be892d1443e8c56b0edfbb086180f4e7b87950b8fd62c63e54796b24377572e2` |
| Passed attempt 03 summary | `3c46b9834c6805c0ae46aeb0ff6226ec2abf814db873abc1d8fc104b8eacab72` |
| Passed attempt 03 formulas | `f4b7a2e69c7a51ebf33d25b94e03a60f7ca2680fecb481e42d4258cf9219ace6` |

The executable verifies direct and transitive G3E source pins before
calculation, refuses existing output directories and supports nonmutating
replay. The retained v1 executable reproduces the failed attempt with an
explicit output-directory argument. Local command logs remain ignored.

Both replays completed with **byte-identical summary and formula artifacts**.
Attempt 03 exits zero with 28/28 checks. Attempt 01 intentionally exits one
with its original 14/26 failed validation; replay identity does not convert
that failed attempt into a passed result. Attempt 02 has no receipt to replay.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_slow_action.py --replay
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_slow_action_v1.py --replay --output-dir Analysis/MasterTests/outputs/r4c1_g3a_attempt_01
```

## Remaining substantive holds

Provisional reuse is confined to the formal action, symplectic, boundary,
coefficient and sampled instantaneous-Hessian results above. A controlled
finite-k remainder, a physical EFT cutoff/window, full constraint/energy
interpretation, arbitrary fast-wave data, a stationary physical-pole test
where applicable, and healthy continuous GR remain unverified. Those are
substantive requirements, not Rule-9-only blockers. The new sign evidence
must accompany any dependent positive-energy or healthy-limit claim.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E and their scoped
review debt. Canonical Tests 1-3 HOLD_SUBSTANTIVE; claim CONDITIONAL,
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage 4A CLOSED; TOP-X4 unchanged. No PDF edit, provider dispatch, commit,
push or publication occurred in this audit.
