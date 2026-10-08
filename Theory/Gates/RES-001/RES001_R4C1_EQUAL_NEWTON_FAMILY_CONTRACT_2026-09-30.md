# R4C1-G3: equal-Newton family and tensor/background preflight

Date: 2026-09-30. Status: `FROZEN_CONDITIONAL_PREFLIGHT`.
Owner: Master Test 1 / unchanged R4C1-v1 action.
This separately registered family follows G2's permitted `alpha_13!=0`
diagnostic route. It changes candidate parameters and initial data only as
specified below; it does not replace B1, G1, S1 or their outputs. No observed
`a0`, fitted `H0`, galaxy datum or numerical gravity bound enters.
`physics_pass=false`, `gate_effect=NONE`, `review_status=DEFERRED`,
`Rule9_cleared=false`, `canonical_Test1_pass=false`.

## Inputs and calculation boundary

Pin the action (`81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`),
G1 report (`b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404`),
S1 report (`0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b`),
G2 addendum (`a8966e9bff26f8514fb466f5f9be67acab6fb0340760148e1d3c642e3a14a3d1`),
and B1 executable (`1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`).
Verify the B1 executable's own source pins before using its pure `physics`
and `rhs` functions. Do not invoke old receipt-writing `main()` functions.
The full variation executable it imports remains pinned to
`aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0`.

The tensor calculation uses the on-shell zero-scalar, zero-exchange,
zero-density Minkowski frame control: `beta=g_r=0`, `u=v=r=0`, constant
`psi`, `rho_Lambda=0`, `U=partial_t`, signature `-+++`. With lapse one,
shift zero and one cross polarization,
`gamma_xy=gamma_yx=epsilon q(t,z)`, `gamma_xx=gamma_yy=gamma_zz=1`,
derive the quadratic density directly from exact spatial curvature and
ADM extrinsic curvature of this metric. Include EH/GHY and all frame
invariants. For the aligned unit frame, the frame invariants reduce to
`c_13 K_ij K^ij+c_2 K^2`, with acceleration zero. Periodic spatial
variations and fixed temporal endpoints allow the stated total derivative.
The tensor representation has no linear scalar/vector constraint mixing on
this isotropic vacuum control. This does not certify interacting B1 tensors.

Check that, up to `M_P^2 partial_z(q partial_z q)`, the quadratic density is
`[(M_P^2-M_U^2 c_13) qdot^2-M_P^2 qz^2]/4`.
Thus test the control's tensor speed `c_tensor^2=1/(1-alpha_13)`.
Independently retain G1's metric-shift-reduced transverse coefficients
`K_V=M_U^2 c_14` and
`G_V=M_U^2 c_1+M_U^4 c_13^2/[2(M_P^2-M_U^2 c_13)]`.
Any omission or reversed sign of the tensor frame term must be detected at
the nonzero-`alpha_13` point. A speed ratio at a zero kinetic endpoint is
not an endpoint propagating mode.

## Frozen family

Let `eta` be a parameter labelling separate solutions, constant during each
integration. Use `eta=(1,1/4,1/16,1/64,1/256,1/1024)` and B1's reference
units, `M_P^2=1`, unchanged scalar/reservoir potential parameters and
`rho_Lambda=0`. At `eta=1` retain B1 `c_1=1/5`, `c_4=1/20`, set
`c_2=-7/48`, `c_3=-1/80`, and use `M_U^2=(2/3)eta`. These give

```text
alpha_13=eta/8, alpha_14=eta/6, alpha_2=-7 eta/72,
alpha_L=eta/36, alpha_theta=-eta/6,
M_c^2=1-eta/12, M_t^2=1-eta/8,
G_cos/G_static=1.
```

Scale `zeta,K_Q,b,g_r` by `eta` from B1; scale `A` by `eta^(3/2)` and
`beta` by `eta^2`. This keeps `A/K_Q^(3/2)` and `b/K_Q` constant rather
than inheriting G1's divergent canonical cubic coefficient. It is an
explicit alternate limit prescription fixed before execution, not a
derived microscopic matching or a change to G1's scaling.

Use B1's initial vector `(a,H,u,udot,v,vdot,r,rdot,psi,psidot,rho_m,tau)`
with `u,vdot,r,rdot` multiplied by `sqrt(eta)` and `psidot` by `eta`.
Keep initial `a=1`, `rho_m=1/5`, `udot=v=psi=tau=0`; recompute `H>0`
from this family's own Friedmann constraint after these scalings. Initial
conserved charge equals `eta`, not a fixed nonzero charge. At `eta=0`
compare only to the separately defined Einstein-dust control; do not invert
vanishing kinetic/auxiliary blocks or evaluate `beta/K_Q` there.

## Numerical decision rules frozen before the new executable

For every positive `eta`, evolve B1's general homogeneous equations on
`[0,4]` with both DOP853 and Radau, `rtol=1e-11`, `atol=1e-13`, dense
output and 801 common points. Require completion, finite sampled fields,
`a,H,rho_m>0`, and normalized Friedmann residual, charge drift and dust
integral drift each below `1e-8` using B1's existing normalizations.
Require maximum DOP853/Radau state disagreement
`max|y_D-y_R|/(1+|y_D|)<1e-8`.
For the `eta=1` member also use B1's independent finite-difference sector
and spatial-metric balances on 201,401,801 points: finest residuals below
`1e-7`, and balance-error improvement at least four, or both endpoint
balance errors below `1e-9`.

Compare `a,H,rho_m` to exact Einstein-dust on the same grid with G1's
`max|member-GR|/(1+|GR|)` norm. Require decreasing sampled errors and a
last factor-four refinement ratio strictly between two and six. Record any
failure with the fixed family and thresholds intact. Evaluate S1's
inherited kinetic-square weights and G1's transverse coefficients on this
family; positive weights are a scoped no-ghost check, not a fresh complete
constraint derivation, gradient, causality, all-sector or EFT result.

## Output and interpretation

Write only a new numbered attempt directory, refusing an existing target.
Retain both-method sampled trajectories as deterministic NumPy data,
machine-readable exact formulas/checks, input/runtime/output hashes and
sidecars. Allow an in-memory replay without replacing earlier output.
The executable must reject a source-pin mutation before creating outputs.

Record any finite-time convergence, equal-Newton or positive-kinetic result
as conditional. If tensor propagation differs from the matter light cone
at finite `eta`, report it explicitly; do not infer either GR or an
observational exclusion from equal Newton constants. If kinetic rank
degenerates as `eta->0`, retain healthy continuous GR recovery as open;
neither an all-path no-go nor a physical scattering cutoff follows from
the coefficient limit alone. Tests 1–3, MAT-001, UVIR-003, `K_Q`, `V`,
Stage 4A, TOP-X4 and publication statuses retain their owning holds.
