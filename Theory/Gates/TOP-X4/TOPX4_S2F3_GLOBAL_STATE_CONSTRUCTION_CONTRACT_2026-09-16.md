# TOP-X4 X4-S2F3 global scalar-matrix state construction contract (2026-09-16)

## 1. Purpose and authority

This contract freezes the next single gate after the local scalar-matrix
Hadamard-parametrix checkpoint. It asks whether the registered evolving
rank-three scalar system admits a globally admissible state construction on
the frozen finite-charge background.

The local `U_0`--`U_2` result remains valid but local. The prior branchwise
fourth-order WKB failure remains rejected, and the exact scalar/Dirac
transport retry remains finite-order evidence. Neither result is superseded
by this contract.

This task may use an all-order adiabatic/pseudodifferential construction, with
a Borel-summed symbol or an equivalent theorem-backed realization. It must
not promote a finite-order numerical fit, an instantaneous vacuum, or an
exactly transported low-mode basis to a Hadamard state without proving the
microlocal boundary.

The contract is subordinate to:

- `Theory/Core/Reasoning_Mode_Plans/11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md`;
- `Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md`;
- `Theory/Gates/TOP-X4/TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md`;
- `Theory/Gates/TOP-X4/TOPX4_S2F3_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CONTRACT_2026-09-12.md`;
- the failed dynamic-state and finite-order exact-transport receipts.

## 2. Frozen input and scope

The calculation must use the registered A1 zero-winding background on
`t in [0,1]`, with the declared five-dimensional metric

`ds^2=-dt^2+a(t)^2 d vec{x}^2+b(t)^2 dy^2`,

the complex condensate split into radial/phase variables, and the real
`chi` spectator. The scalar bundle is rank three: the charged real pair plus
`chi`. The registered mode labels and authority sidecars must be read from
the predecessor receipts, not copied into a new unstated background.

The frozen operator convention is

`P=-Box I_3+H = -(D^2+E)`, with `E=-H`.

In Cartesian bundle variables the connection is zero. A phase-aligned basis
may use `A_A=J partial_A Theta`, but its curvature must remain zero on a
smooth patch and its first-derivative mixing must be retained. A basis change
is not a new physical interaction.

The task is limited to the scalar state. It does not include the Dirac
Hadamard two-point function, curved graviton/ghost/Jacobian operators,
parity/anomaly phase, counterterm normalization, determinant, stress tensor,
semiclassical background, physical Hessian, A4 or Ultra.

## 3. Admissible construction routes

Exactly one route must be declared before execution:

### Route A — all-order pseudodifferential projection

Construct positive/negative frequency pseudodifferential projections for the
first-order scalar Hamiltonian system. The symbol recursion must be defined
to arbitrary order, with the principal symbol, subprincipal transport,
remainder class and smoothing low-mode patch stated explicitly. The exact
evolution of the projection must define a bisolution on the full registered
globally hyperbolic slab.

### Route B — all-order adiabatic/Borel construction

Construct the coupled matrix adiabatic symbols to arbitrary order from the
exact time-dependent operator, show that the formal series has a smooth
Borel realization, and use exact evolution to obtain the two-point function.
Any finite-order truncation is a diagnostic of the declared recursion only;
it is not itself the final state.

An implementation may compare the two routes, but it may not silently mix
their state definitions or use the prior scalar WKB branch as a replacement
for either route.

## 4. Required state conditions

For the resulting bidistribution `Lambda` the executable and its owning
receipt must establish:

1. `P_x Lambda=0` and `P_y Lambda=0` on the slab, with a stated treatment of
   the Cauchy surface and the bundle connection;
2. the scalar commutator/CCR and the required symmetry condition;
3. positivity as a quadratic form on compactly supported test sections,
   including the low-mode patch;
4. the Hadamard wavefront condition in the five-dimensional geometry;
5. agreement with the local `U_0`--`U_2` singular data and the corrected
   `E=-H` convention;
6. arbitrary-order ultraviolet remainder control, or a theorem-backed
   pseudodifferential construction whose remainder is smoothing; and
7. independence of the result from Cartesian versus phase-aligned bundle
   coordinates, including the pure-gauge connection transport.

The wavefront and positivity claims must be attached to the actual coupled
matrix state, not inferred from scalar component plots or from a decreasing
finite-order mixing envelope. A finite mode grid cannot establish a global
microlocal statement by itself.

## 5. Required numerical and algebraic controls

The bounded executable must independently check:

1. every predecessor authority hash and the preserved negative dynamic-state
   result;
2. smooth finite background interpolation and the registered hyperbolicity
   domain;
3. the matrix canonical equations and exact bisolution residuals;
4. positivity and CCR residuals on the primary and resolution-witness grids;
5. the declared all-order symbol/adiabatic recursion at every implemented
   order, with a separate residual rather than a claim of infinite-order
   convergence from extrapolation;
6. the smoothing character of the low-mode patch and its absence from the
   high-frequency wavefront argument;
7. covariance under a constant orthogonal bundle basis change and the
   phase-aligned pure-gauge transport;
8. agreement with the local parametrix at the singular orders already
   registered;
9. deterministic output, relative paths, sidecar hashes and byte-identical
   reruns; and
10. all status and downstream firewalls below.

At least these rejecting mutations are mandatory:

1. set `E=+H`;
2. declare the exact finite-order transport retry to be Hadamard;
3. omit the matrix connection or its phase-derivative mixing;
4. copy independent scalar component states into the interacting matrix;
5. omit the low-mode positivity check;
6. replace the wavefront argument with a finite grid or UV trend alone;
7. treat a static `q=0` subtraction as the evolving state-dependent stress;
8. claim determinant, stress or physical-Hessian closure from the state alone;
9. import an observational target, `H_0`, `a_0`, `K_Q` or `V`; and
10. manufacture Rule-9 clearance from this local calculation.

## 6. Decision rule and stop boundary

The only status that may open this gate is

`PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN`

and only if all seven state conditions, all registered controls, the
all-order/smoothing argument and the rejecting mutations pass. Even then the
receipt must retain:

- `physics_pass=false` and `gate_effect=NONE`;
- Dirac, gravity/ghost, parity/anomaly and counterterm normalization as open;
- determinant and renormalized stress as `NOT_COMPUTED`;
- physical Hessian, radion stabilization, A4 and Ultra as closed;
- `THREE_WAY_CLEARANCE_NOT_MET` until independent reports exist.

If the construction is not executed, or if any state condition is not
established, the result must be

`HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED`

with no gate effect. A failed construction must preserve the prior WKB
failure and finite-order transport pass as separate evidence; it must not
rewrite either receipt.

No stress tensor, determinant, semiclassical background or physical Hessian
may be calculated from an unverified state. No downstream MAT, UVIR, COS,
publication or architecture status follows from this contract.

## 7. Primary formal basis

- Gerard and Wrochna, *Construction of Hadamard states by pseudodifferential
  calculus*, [arXiv:1209.2604](https://arxiv.org/abs/1209.2604).
- Sahlmann and Verch, *Passivity and microlocal spectrum condition*,
  [arXiv:math-ph/0008029](https://arxiv.org/abs/math-ph/0008029), for
  vector-bundle-valued field scope.
- Hollands, *The Hadamard Condition for Dirac Fields and Adiabatic States on
  Robertson-Walker Spacetimes*, [arXiv:gr-qc/9906076](https://arxiv.org/abs/gr-qc/9906076),
  for the separate spinor-state boundary.

These sources constrain the construction method. They are not independent
Rule-9 reviews of the repository-specific X4 calculation.

## 8. Execution disposition (2026-09-16)

The theorem-backed Route-A construction is now recorded in
`Analysis/TOP/TOP-X4/topx4_s2f3_global_state_construction.py` and its JSON
receipt. It instantiates the smooth normally hyperbolic rank-three operator,
the arbitrary-order formal symbol, the Borel/smoothing realization, a
positive finite-rank low-mode patch, exact full-matrix Cauchy evolution and
constant bundle-basis covariance. The construction checkpoint passes its
registered controls and returns
`PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN`.

This is a theorem-backed scalar-state construction checkpoint, not a physics
or publication pass. Dirac, graviton/ghost, parity/anomaly, counterterm
normalization, determinant, renormalized stress, physical Hessian, Rule-9 and
all downstream gate effects remain closed.
