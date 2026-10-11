# R4C1-G3N2: transverse multimode entry disposition

Date: 9 October 2026. Version 1. Owning Test-1 continuation after G3K-C2.
Conditional; review DEFERRED; PROCEED_PROVISIONALLY for supported uses only.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Outcome

The frozen executable passes 1542/1542 local checks and exact read-only replay.
For the retained G3V transverse waves, the first-order metric-shift constraint
does not remove vorticity. These waves do not admit a local U-orthogonal clock
where the computed Frobenius three-form is nonzero. The finite-amplitude raw
psi/z multimode velocity block is also not uniformly algebraic in z: its rank
is eight at nonzero amplitude and four at alignment, and its inverse has a
nonzero amplitude^-4 leading z/z block.

These findings reject the naive intrinsic-preferred-leaf and uniformly
algebraic-regulator extensions of G3N1. They do not reject the covariant
definition of Delta, establish a physical ghost, solve the full nonlinear
constraint reduction, or prove an all-action/all-clock/classical no-go.
G3N1's frozen-amplitude ODE result is preserved within its original scope.

## Frozen evidence and execution

Contract: [G3N2 entry contract](RES001_R4C1_G3N2_TRANSVERSE_MULTIMODE_ENTRY_CONTRACT_2026-10-09.md),
SHA-256 43878a67d4002e32e3dc70e318659cd65e11699433eee7d7e2b3e5f7a29504db.
Executable: Analysis/MasterTests/test_01_r4c1_g3n2_transverse_multimode_entry_v1.py,
SHA-256 a5a9c4d0414224dbb30ac3bb7d454d3749ca2ec04028de424738a54c4f251198.

New immutable output directory: Analysis/MasterTests/outputs/r4c1_g3n2_attempt_01.

| Artifact | SHA-256 |
| --- | --- |
| summary.json | 7f0fee4b79104cb43dab3b712b851c1de253d683fe870e920bb2d80e18789252 |
| formulas.json | f898a66f3581782386cdf5960c9ea9dfdd0522508a42d7366abeaa8f3ba939b6 |
| samples.json | f175c5047bb90574708e6c61c3d8f27aac59cf5b13ae0becc0b77682549f98c1 |

Execution, using the existing itsm_env interpreter and optimizer:

```text
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_g3n2_transverse_multimode_entry_v1.py
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_g3n2_transverse_multimode_entry_v1.py --replay Analysis/MasterTests/outputs/r4c1_g3n2_attempt_01
```

Both return exit code 0. Replay recomputes the calculation and compares every
JSON and sidecar byte. Separately comparing all six output files before and
after replay confirms identical hashes, lengths and last-write timestamps.
No existing pinned scientific file or sidecar is changed by the calculation.

Original run private log: .local/itsm-context/output-776fd5c78e0d47d2bf0f7a8d86daf7a7.txt,
SHA-256 33014f1667e6ee89743cdaf455029f1acfd59151aa57008a19918c82b6fd54a1.
Replay private log: .local/itsm-context/output-03d1c0cddc8b4a5e90f9c404f19e0e5f.txt,
SHA-256 bc1093e84ee4ef702fdf7363322f21f7b0b0e52be35e3aa669395b43c3287521.
Private logs are not release artifacts and must not be committed.

## Actual transverse chart and constraints

Retain the G3V cosmic-time chart, not C2's dust-time coordinate chart:

```text
g_tt=-N^2+B_y^2; g_ty=a B_y; g_ii=a^2
U=(gamma/N,0,(w_y-B_y gamma/N)/a,0), gamma=sqrt(1+w_y^2)
N=1 on the archived homogeneous trajectory; tau_dot=C, not tau=t
B_y=sigma w_y at first order, sigma=-eta/(8-eta)
```

The first-order nonzero-mode transverse shift constraint and its zero
homogeneous integration mode are retained. This is not a solved nonlinear
scalar/tensor/frame/dust constraint system. All 216 archived G3V chart records
are used without a new background integration, parameter fit or trajectory
selection. Parameters remain the declared G3 family, including assumed
K_Q=3 eta in its unit chart, not a canonical first-principles K_Q determination.

## Local foliation obstruction

For arbitrary w_y(t,z) and B_y(t,z), direct metric contraction gives

```text
theta=U_flat=(-N gamma+B_y w_y)dt+a w_y dy
coefficient_dt_dy_dz(theta wedge dtheta)
    =a[N partial_z(w_y)/gamma+w_y^2 partial_z(B_y)].
```

Substitution of w_y=epsilon W and B_y=epsilon sigma W gives

```text
a epsilon partial_z(W)
    [N/sqrt(1+epsilon^2 W^2)+sigma epsilon^2 W^2]
    =a N epsilon partial_z(W)+higher orders.
```

If theta=-mu dT for a local real U-orthogonal clock, theta wedge dtheta must
vanish. The nonzero leading coefficient therefore excludes that clock for
these allowed nonconstant transverse waves. Regular response starting at
second order cannot cancel a nonzero first-order coefficient. This does not
exclude another time choice or justify replacing independent U by a
hypersurface-normal field.

For W=cos(chi)+rho cos(3chi), chi=kz, the exact derivative-square average is
(1+9 rho^2)/2>0. The main witness uses rho=1/3, epsilon=1e-3 and includes
profile zeros. The sufficient bracket bound at N=1 is

```text
1/sqrt(1+epsilon^2(1+|rho|)^2)
    -|sigma| epsilon^2(1+|rho|)^2 > 0.
```

Its minimum over the 216 charts is 0.9999988571440422. Independent direct
metric/U contraction with complex-step differentiation agrees with the
symbolic three-form to normalized error <=2.221e-16. Grid witnesses supplement
the exact derivative norm and bracket argument; they are not the proof alone.
These reference profiles do not determine a physical torus size or EFT band.

## Raw regulator block, not a physical spectrum

In the orthonormal average basis e=(1,sqrt(2)cos(2chi),sqrt(2)cos(4chi),
sqrt(2)cos(6chi)), define G_mn=<W^2 e_m e_n>. Exact Fourier convolution and
independent quadratures retain all four modes and rho=0,-1/3,1/3,1 controls.
G is positive definite: a nonzero finite Fourier polynomial cannot vanish on
an entire open interval on which W is nonzero. Exact leading principal
minors are positive for all four registered controls.

The action-derived raw mixed time term is -b a^3 w_y^2 z_dot psi_dot/N.
With the direct absolute-cubic force contribution retained, its block is

```text
H_raw=[Apsi,C;C^T,0], C=-(b a^3/N) epsilon^2 G
det(H_raw)=det(C)^2=(b a^3/N)^8 epsilon^16 det(G)^2
H_raw^-1=[0,(C^T)^-1;C^-1,-C^-1 Apsi (C^T)^-1]
epsilon^4 (H_raw^-1)_zz -> -K_Q/(a^3 b^2/N) G^-2 != 0.
```

At zero amplitude the separate raw rank is four; no zero-amplitude inverse
is attempted. Exact congruence of the finite-amplitude block gives a raw
4-positive/4-negative signature. It is not a physical ghost classification:
the complete metric/frame/matter constraints and physical degree reduction
have not been solved. A singular amplitude-dependent numerical rescaling is
not a regular endpoint field transformation.

The 144 raw-block probes use twelve archived eta/time charts, four profiles
and three amplitudes. All use the frozen threshold <=1e-10. Largest normalized
inverse-formula error is 5.901e-49; determinant-ratio error 9.128e-46. The
largest scaled inverse-limit discrepancy is 1.249e-5 and each obeys its
individual <=10 epsilon^2 criterion. Unexpanded-action central differences
at three declared velocity step sizes give discrepancies <=2.089e-39.
These high-precision arithmetic checks use 50-digit mpmath; they do not
increase the precision of inherited binary64 trajectories or certify a
unit-independent physical conditioning margin for mixed-dimension variables.

## Direct auxiliary response and unresolved coupled response

Retain the direct parent source

```text
Delta2_direct=psi_dot W W_dot+(psi_ddot+2H psi_dot)W^2
z2_direct=-Delta2_direct.
```

For the registered two-harmonic W and W_dot profiles it contains harmonics
0,2,4,6, all exported and independently reconstructed on every chart. This
is not the complete auxiliary solution: induced psi, scalar metric,
longitudinal-frame and matter responses contribute at the same order. It
does not provide a complete J2, quartic Schur pullback or invariant finite-mode
PDE closure. Absolute |W|^3 is never substituted by signed W^3.

Next substantive obligation: assemble the coupled nonlinear constraint and
evolution response, starting with the complete second-order regulator
equation and its scalar/frame/metric response. Keep other admissible time
formulations open. A finite-band alternative needs its own action-level
physical cutoff and domain; a comparator band or the potential's cutoff=2
does not provide them.

## Provenance, inherited failures and unchanged holds

All 104 source pins and 101 available sidecars match before and after
recalculation. Three inherited sidecars are absent, not fabricated:

- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONZERO_GRADIENT_FORCE_LOCAL.md
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md

The original G3 balance failure is preserved: eta1_independent_fd_balances,
1.1005635230674148e-7 against <1e-7, in the 112/113 receipt. No threshold,
parent failed assertion, frozen action or original scientific hash is repaired
into a pass. Inherit R9-MT1-G3N1, R9-MT1-G3V, R9-MT1-G3K-C2 and their full
scientific/review dependencies. Review alone is deferred; the failed extension
assumptions cannot be deferred into healthy field evolution.

Unchanged: Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action change, manuscript/PDF edit, vault mutation, provider dispatch,
commit, push, canonical promotion or publication. The native full Tests 1-3
goal remains ACTIVE and incomplete; this checkpoint is not its completion.
