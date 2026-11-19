# A16.2: adding the force pair does not close the initial dust state

15 November 2026. Conditional result for the original registered R4C1/B1
linear export at its initial background and ell=4,8,16,32,64. No new action,
background, physical domain or thermodynamic state is adopted.

## Actual retained maps and closure criterion

Let x be the original twenty-component first-order chart state, xdot=L x.
Use the parent's actual dust map O x=(D,Vx). Reconstruct Pi from row 16 of
the original full 22-field map, and lapse alpha from row 0. Pi is exactly
chart coordinate 9; its coordinate-time derivative is state coordinate 19.
The additional normalized-frame temporal perturbation is

    P_n=delta(n^mu partial_mu psi)=Pi_dot-psi_dot*alpha.

The background is homogeneous and n is the unit frame used in the original
action; the linear spatial-frame term has no background spatial scalar
gradient to contract. This is not the mixed balancing variable chi or an
identification with the independent unconstrained multiplier/frame variation.
Pi and these reconstructed maps use the parent's fixed gauge. No new
gauge-invariant observable construction is asserted.

For A x equal to either the dust pair or (D,Vx,Pi,P_n), define

    B=A_dot+A L.

All observation-map derivatives use the actual background flow, including
lapse reconstruction and psi_dot drift. An instantaneous linear closure
requires a matrix C with B=C A. Equivalently ker A is contained in ker B,
or rank(stack(A,B))=rank(A). This tests permitted information loss in the
declared chart; these ranks do not count new physical degrees of freedom.

## Exact initial result

| Retained variables | Rank A | Rank stacked A,B | Initial closure |
| --- | ---: | ---: | --- |
| D,Vx | 2 | 4 | Fails |
| D,Vx,Pi,P_n | 4 | 6 | Fails |

Every registered nonzero mode gives these exact algebraic ranks. For each
case an independently substituted nullspace witness d obeys A d=0 but B d
is nonzero. Thus identical retained initial values do not determine identical
retained initial rates in this full linear chart. Adding the force pair is
insufficient; at least two further independent row combinations are needed
to determine this first rate. It is not proved that adding two variables
would close their own subsequent evolution or supply a minimal complete state.

The exported witnesses at all five modes have support only on original slots
0 and 7 (the first metric chart coordinate and Cartesian condensate dv).
There is no initial reservoir coordinate/rate in slots 8,18. At ell=4, one
unnormalized witness has d0=i sqrt(4006695)/56 and d7=10 i. Its enlarged
retained rate difference is (75/2,0,0,30 i). These numbers depend on arbitrary
direction normalization; they are not measured gains, physical amplitudes
or observational predictions. The conjugate negative Fourier mode restores
real perturbations. No real-field obstruction follows from complex storage.

This is a chart-level initial witness, not a new certified finite-time seed,
an invariant causal intervention on a single sector, or a proof of canonical
physical admission. In particular it does not demonstrate a reservoir-only
memory mechanism: the exhibited ambiguity already involves other variables.
Initial lapse is zero for this witness because Pi_dot=P_n=0 and psi_dot is
nonzero, but physical state interpretation still inherits the parent gauge
and constraint qualifications.

## Verification and preservation

[Contract](RES001_A16_ENLARGED_STATE_V1_CONTRACT_2026-11-15.md) and
[input hashes](RES001_A16_ENLARGED_STATE_V1_INPUTS_2026-11-15.json) were frozen
before execution. The [executable](../../../Analysis/MasterTests/test_a16_enlarged_state_v1.py)
uses exact algebraic fields, not floating singular-value thresholds.
[Receipt](../../../Analysis/MasterTests/outputs/a16_enlarged_state_v1_20261115/receipt.json):
32/32 controls and byte-identical fresh-directory replay. Rank/nullspace
agreement, exact witness substitution, row independence, actual Pi/rate map,
and nonzero lapse/coefficient drift retention are checked. These are
same-assistant computational controls, not external scientific review.

The initial background is the existing a=C=u=r=1, u_dot=v=0, v_dot=1,
r_dot=1/4, psi_dot=rho_m=1/5, H=sqrt(3469/4620). The action/export is
unchanged. No arbitrary reservoir or force coupling is removed. Original
source files, hashes, sidecars and previous failures are preserved.

## Consequence and next task

The [history map](RES001_A16_HISTORY_MAP_V1_REPORT_2026-11-15.md) remains a
supported deterministic reduction identity. This new result rejects one
specific proposal to remove the hidden-state dependence by retaining only
the force pair in addition to dust. It does not prove irreducible memory:
an appropriately enlarged instantaneous state can still be sufficient.

Next identify the additional constrained row combinations and their physical
meaning, keeping the reconstructed metric/condensate response and original
global restrictions. Assess whether a usable retained state closes under its
own dynamics or leaves a controlled history operator. Physical source/gauge
interpretation must precede reservoir attribution. An evolution or kernel
error estimate for new seed directions needs its own justified extension;
the old four-column dust certificate is not automatically transferred.

No organizing-force law, dissipative bath, entropy production, matched force
coefficient or all-domain stability result follows. Review DEFERRED;
physics_pass=false; gate_effect=NONE. G1–G6 and MAT matching remain incomplete.
