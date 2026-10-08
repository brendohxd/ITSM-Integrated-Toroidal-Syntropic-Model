# R4C1-G3Z: finite-rate inner pencil of the zero-speed sector

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / G3 family.
Local validation 19/19; no failed/unknown local checks. Review DEFERRED.
`physics_pass=false`, `Rule9_cleared=false`, `gate_effect=NONE`.
Canonical Tests 1–3 remain `HOLD_SUBSTANTIVE`.

## Decision and scope

The full canonical equations give a nonsingular quadratic **finite-rate
inner pencil** for G3S's two zero-speed roots at each fixed regular
coefficient event. Their leading zero-speed Jordan block does not by itself
imply rates diverging with momentum. At the sampled events, the full-pencil
roots approach the derived inner roots as momentum increases.

This is a frozen-event asymptotic, not a time-dependent evolution equation
for density perturbations. Positive real instantaneous canonical rates
remain. They are not classified here as Jeans growth, transient growth or a
physical instability; a time-dependent rescaling can change instantaneous
rates. Neither the equal-order Jordan obstruction nor the physical-EFT and
healthy-GR holds is cleared.

The [contract](RES001_R4C1_G3_ZERO_INNER_CONTRACT_2026-09-30.md) was frozen
before calculation. Use the unchanged [G3S full canonical matrices](../../../Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/matrices.json),
not B1's evaluated symbol or graph-norm estimate. All statements require
0<eta<=1,H>0,a,C>0,k!=0 and S1's nonzero auxiliary rank domain. No eta=0
inverse, added pressure, action retuning or observational input is used.

## Derivation and exact checks

Form `P(lambda,p)=lambda^2 I+lambda G(p)+W(p)` from G3S, whose background
and canonical derivatives were taken at fixed comoving k before p=k/a.
The force block begins at p^4 with coefficient 5/33. Its inverse through
p^-6 is retained, including its p^2 denominator term; that term contributes
at O(1) after multiplication by both cubic cross blocks. Omitting it changes
the result and is explicitly rejected.

Eliminate the force block, then scale both rows and columns of the five
remaining coordinates (u,v,r,T,W) by (1/p,1/p,1/p,1/p,1). Every prospective
divergent entry cancels exactly. The four propagating coordinates have the
G3S principal block, independent of lambda, with determinant

```text
-4 eta [1+eta(u^2+v^2)/13] / [3(8-eta)(12-eta)].
```

It is nonzero on the declared real-field domain. Their Schur complement
gives

```text
S_Z(lambda) = -(12-eta)/eta * [lambda^2 + c1_Z lambda + c0_Z],
c1_Z = -12H/(12-eta).
```

Its lambda^2 coefficient never vanishes there. The negative overall pencil
factor is not a physical kinetic/ghost classification; S1/G3S's retained
six-field kinetic certificate remains positive in its stated chart.

A separately labelled **post-run algebraic simplification**, using the
pinned background Hdot equation, writes the constant coefficient as

```text
c0_Z = -(36-eta) H^2/[4(12-eta)]
       -(24-eta) Hdot/[2(12-eta)]
       -6 rho_m/(12-eta) -(beta psi_dot)^2,
beta = 2 eta^2/5,
Hdot = -6(udot^2+vdot^2+rdot^2+3 eta psi_dot^2+rho_m)/(12-eta).
```

These are the registered M_P^2=1 reference units, not an observational
normalization. The original unsimplified coefficients and scaled matrix
are retained in the pencil export. In-memory SymPy confirms the compact
identity exactly. Its first supplementary parse used same-named symbols
with different assumptions and did not simplify to zero; using the
export's actual symbols yielded zero, without changing any source/equation.

An independent exact rational Schur calculation reproduces the finite
scaled matrix at fixed lambda. Its rational coefficient jet checks algebra,
not a claimed on-shell G3 background point; physical sampling below instead
uses both pinned G3 on-shell trajectories. No sampled coefficient event
replaces the symbolic identities.

## Recorded numerical evidence

There are 72 time/family/method cases: six eta values, both stored methods,
and t=(0,.5,1,2,3,4), with p=(20,40,80,160). Full 12-root pencils were
recomputed from the pinned matrices and matched the earlier recorded roots
with zero normalized discrepancy in this runtime. Matching uses the two
inner roots against all twelve roots; it does not discard the other modes.

- Maximum p=160 normalized inner-root discrepancy: `0.00551758805`, below
  the frozen 0.05 diagnostic-reach criterion.
- The smallest absolute lambda^2 prefactor is 11.
- The largest inner real rate is `1.07627486565`; the minimum real part
  across all inner roots is `-0.171317387196`, in reference units.
- Sixteen cases have complex-conjugate inner roots. Real nonzero **leading
  wave frequencies** in G3S did not assert that these finite inner rates
  must also be real or stable.

At eta=1,t=0, the inner roots are `(1.07627486565,-0.0407504431125)`.
The full pair at p=160 is `(1.07601839888,-0.0350080109040)`; maximum
matching errors at p=20,40,80,160 are about .3580,.08853,.02208,.005518.
The larger lower-momentum discrepancies are retained, not promoted into
the asymptotic regime. The eta=1/1024 initial inner pair is approximately
`(0.388242,-0.128734)` and also converges across those diagnostic momenta.

Since c1_Z<0 for H>0, the inner roots' sum is positive; at least one has
positive real part in this instantaneous canonical pencil. This is a
precise rate statement, not a coordinate-invariant physical-instability
verdict. A formal Einstein-dust coefficient boundary gives c0_Z=-3H^2/4
and instantaneous roots `(3H/2,-H/2)`, but the original canonical/constraint
map is singular at eta=0. This boundary does not prove GR recovery.

## Provenance, exclusions and next step

- Contract: `47723c96936643b6be19d22e00a4f98bc3f4208cb409e61c255e041b7ce725e5`.
- [Executable](../../../Analysis/MasterTests/test_01_r4c1_g3_zero_inner.py):
  `db77ef15784eb73d8b9eefc6e2f07d39b330b5061c0248189138be9cc2441bdd`.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_g3z_attempt_01/summary.json):
  `60d9de53f95592512e094ffc60c81a781ab8f9b33a8afa93dbf53943efbb34bf`.
- [Pencil export](../../../Analysis/MasterTests/outputs/r4c1_g3z_attempt_01/pencil.json):
  `abb6a23cba1f80b0a02bf76d1bb47153bd745be55e83c44e9bd8183f9a9d5bb4`.

Direct/inherited hashes are checked before computation. New numbered outputs
refuse existing directories. Replay using
`C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B
Analysis/MasterTests/test_01_r4c1_g3_zero_inner.py --replay` returns exit 0
and reproduces both artifacts byte-for-byte. No older main() was invoked,
and G3's original 112/113 failed receipt remains unchanged.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S. Review must examine the
series order, all Schur couplings, canonical-versus-physical rates, source
compatibility and distinction between a fixed-event limit and evolution.
`PROCEED_PROVISIONALLY`, `substantive_blocker=NONE_WITHIN_STATED_SCOPE`
applies only to these locally verified frequency asymptotics. Evolution,
full IVP, physical cutoff and healthy GR remain substantive holds.

Next: derive the **time-dependent** reduced zero-sector equations and
reconstruction in dust/frame variables, keeping derivatives of eliminated
coefficients and p(t). Substituting lambda->d/dt in this frozen pencil is
not that derivation. Then test the coupled mixed-regularity evolution and
canonical interaction/validity range. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged. No PDF
work, provider dispatch, commit, push or publication occurred.
