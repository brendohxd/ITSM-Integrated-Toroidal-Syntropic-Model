# G3N5: action-derived dust observables and weighted slow-sector evolution

Date: 11 October 2026 (Australia/Perth). Version 1.
Disposition: CONDITIONAL_FORMAL_SLOW_DUST_CANONICAL_WEIGHTED_ENTRY_CHECKED.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Result and scope

The same formal slow branch that has velocity-action coefficient K=-11/6
admits an action-derived, time-dependent canonical dust-density formulation
with positive momentum Hessian and a negative growth potential. Its complete
Hamiltonian is still indefinite. This is a constructive interpretation of the
checked leading slow sector, not a physical no-ghost or stability certificate.

The unchanged R4C1/B1 action, dust clock, normalized frame, full constraint
reconstruction and registered parameters are retained. The domain is
k=(ell,0,0), ell>0, coordinate periods 2*pi, conjugate negative modes and
t_E in [0,0.05]. On the formal T3, ell is an integer. No physical torus size,
EFT window, new dust-charge restriction or observational target is inserted.
All quantities below use the registered dimensionless B1 normalization.

The ordinary wave-scale zero-speed Jordan defect and negative spatial trace
energy from the [parent nonzero report](RES001_R4C1_G3N5_NONZERO_CHARACTERISTIC_REPORT_2026-10-11.md)
remain. The present calculation does not establish a full finite-k remainder
estimate or a well-posed all-direction mixed-order system.

## Frozen authority and reproducibility

- [Pre-execution contract](RES001_R4C1_G3N5_SLOW_DUST_WEIGHTED_CONTRACT_2026-10-11.md):
  SHA-256 e01cb28d59c0244ad17a0cdf08579c64acbde4d1010efcbc06f4b756a95b2e4c.
- [Frozen executable v1](../../../Analysis/MasterTests/test_01_r4c1_g3n5_slow_dust_weighted_v1.py):
  SHA-256 283179bbec79e2f5e80f77edf3cc2c85f68f5fcf6b3a1a516403c66de9721d5f.
- [Attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01/summary.json):
  SHA-256 fe81f337ba6a7bd5a2783fc2e8a99b617ec08dd119673844f11edf30d53b1208.
  PASS_LOCAL_CHECKS, 79/79; no failed or unknown current checks.
- Exact read-only replay recomputes and byte-compares all five JSON outputs
  and matching sidecars. It passed. The 395 unique source/evidence/sidecar
  files in the replay audit retained SHA-256, size and UTC last-write ticks.
  The main calculation separately preserves 385 input/sidecar files.

Supporting artifacts: [matrices](../../../Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01/matrices.json),
[formulas](../../../Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01/formulas.json),
[transfer](../../../Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01/transfer.json),
and [diagnostics](../../../Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01/diagnostics.json).

Reproduce from the repository root with the known working environment:

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Analysis/MasterTests/test_01_r4c1_g3n5_slow_dust_weighted_v1.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_slow_dust_weighted_attempt_01
```

Fresh-output mode refuses an existing destination. Replay does not overwrite
the frozen source, contract, receipts, sidecars or inherited failed attempts.
These are same-agent local derivations and numerical cross-checks, not
independent external Rule-9 review.

## 1. Dust density and conserved-current reconstruction

Write beta=2/5, volume v=a^3, rho=rho_m and p=ell/a. At fixed comoving ell,
p_dot=-H*p; rho_dot=(-3*H+beta*psi_dot)*rho and C_dot=beta*psi_dot*C.
Keep the existing T=0, alpha=-beta*Pi, nu=0 clock/constraint solution.

Variation of the dust action gives the actual Einstein-frame density and
Noether momentum/current, independently checked against the unreduced
canonical momentum and full dust Euler/continuity identity:

```text
delta_rho = C^4*Em + 4*beta*rho*Pi
P_tau = a^3*rho/C                         (constant on the background)
delta_P_tau = a^3*C^3*Em + P_tau*(tr(M)/2 + 3*beta*Pi)
coordinate_flux_i = -P_tau*S_i/a
```

Define delta=delta_rho/rho and D=delta/(i*p). The leading map from the formal
slow velocity Vx and its derivative agrees with the separately reconstructed
charge-density map D_tau=delta_P_tau/(i*p*P_tau):

```text
D = (11/(6*rho)) * [Vx_dot + (H+beta*psi_dot)*Vx]
D_tau = D                                (leading slow order only)
Sx = Vx                                  (leading slow order only)
det[(Vx,Vx_dot) -> (D,Vx)] = -11/(6*rho)
```

The two-observable map has rank two on rho>0. Equality of the density and
charge maps is derived, not assumed; it is not an equality of the full finite-k
perturbations. In this clock the dust is ADM-comoving, and Vx is the relative
frame velocity. The construction is singular at rho=0 or k=0; it neither
replaces the separately treated homogeneous sector nor fixes a new charge.

## 2. Independent continuity and slow-action equations

The action route and full dust-current route yield the same formal leading
two-state flow:

```text
D_dot  = H*D + Vx
Vx_dot = (6*rho/11)*D - (H+beta*psi_dot)*Vx
M_weighted = [[H,1],[6*rho/11,-H-2*psi_dot/5]]
```

Restoring the fixed-ell p drift gives the actual density-contrast equation:

```text
delta_ddot + (2*H+beta*psi_dot)*delta_dot - (6*rho/11)*delta = 0
```

This is not an inserted cosmological growth target. The coefficient 6/11
belongs to this registered dimensionless branch; it is not a calibrated
G_eff, PPN result, weak-field matching or healthy continuous full-GR limit.

## 3. Canonical transformation: kinetic sign versus complete energy

The original formal velocity action retains K=-11/6 and
R=-121*H/30-11*psi_dot/15. Its canonical momentum is
p_V=v*(K*Vx_dot+R*Vx). Set r=R-K*(H+beta*psi_dot)=-11*H/5.
For each real Fourier quadrature the transformation is

```text
(D,P_D) = S*(Vx,p_V)
S = [[-11*H/(5*rho),-1/(v*rho)],[v*rho,0]]
P_D = v*rho*Vx
S^T*J*S = J
omega_weighted = v*rho*dD wedge dVx
F1(Vx,D,t) = -(11/10)*v*H*Vx^2 - v*rho*Vx*D
p_V = partial_Vx F1; P_D = -partial_D F1
H_D = H_old + partial_t F1                (in the new variables)
```

The generator is independently checked, including background derivatives.
It gives the complete weighted-density Hamiltonian

```text
H_D = P_D^2/(2*v*rho) + H*D*P_D - (3*v*rho^2/11)*D^2
Hessian_D = [[-6*v*rho^2/11,H],[H,1/(v*rho)]]
det(Hessian_D) = -H^2-6*rho/11 < 0
```

For complex Fourier amplitudes, (delta,P_delta)=B*(D,P_D), with
B=diag(i*p,i/p). B^dagger*J*B=J; equivalently the real-quadrature map is
symplectic. Its time-dependent dilation generator, using p_dot=-H*p,
cancels the mixed H term. With conjugate modes retained, the result per
normalized real quadrature is represented by

```text
H_delta = (p^2/(2*v*rho))*|P_delta|^2
          - (3*v*rho^2/(11*p^2))*|delta|^2
det(Hessian_delta) = -6*rho/11 < 0
L_delta = (v*rho/(2*p^2))*|delta_dot|^2
          + (3*v*rho^2/(11*p^2))*|delta|^2
```

The density kinetic weight v*rho/p^2 is positive, but the complete Hamiltonian
remains a saddle, with a negative growth/Jeans-type potential. A
time-dependent canonical Hamiltonian is not an invariant positive-energy
certificate. Neither the original K=-11/6 nor the adverse parent energy is
deleted. Omitting the canonical generator or p drift gives a nonzero rejected
identity. This reformulation is not gauge removal or a full physical ghost
verdict in either direction.

## 4. Analytic leading-sector bound and numerical controls

For the registered B1 background M_c=11/10, its potential is nonnegative
(positive coefficients and even powers). The Friedmann constraint implies
H_dot<=0 and H_dot+3*H^2=(potential+rho/2)/M_c>=0. Let
T=0.05, H0=sqrt(3469/4620), Pmax=sqrt(11/5)*H0. Then

```text
H0/(1+3*H0*T) <= H <= H0
|psi_dot| <= Pmax
rho_min = 0.2*exp[-(3*H0+beta*Pmax)*T]
rho_max = 0.2*exp[beta*Pmax*T]
1 <= a <= exp(H0*T)
exp(-beta*Pmax*T) <= C <= exp(beta*Pmax*T)
Lambda = max(H0+1, (6/11)*rho_max+H0+beta*Pmax)
```

On a smooth background obeying these identities,
norm(W)=max(|D|,|Vx|)=max(|delta|/p,|Vx|) satisfies the Gronwall bound
norm(W(t))<=exp(Lambda*t)*norm(W(0)). It is mode-independent for the formal
leading two-state system only. Lambda=1.8665251299678508838 and the endpoint
amplification bound is 1.0978198477060288. The sampled transfer infinity-norm
maximum is 1.0935735825836057, below that analytic bound.

The density has one derivative weight relative to Vx. A bound in this norm
does not establish the equal-regularity ordinary wave formulation, arbitrary
fast-wave initial data or the omitted finite-k remainder. The distinction
between derivative-weighted evolution norms and strong hyperbolicity is
discussed in [Gundlach and Martin-Garcia's second-order analysis](https://arxiv.org/html/gr-qc/0506037v1).
Their results are not used as a theorem for this full mixed p^2/p^4 system.

Verification uses the frozen 70-digit degree-40 B1 background and slow
transfer, with 257 saved sample points and degree-32 comparison:

- True Taylor transfer residual: 1.9531951885866e-42 (limit 1e-20).
- Degree-32/40 transfer discrepancy: 3.0458127983265e-36 (limit 1e-20).
- Liouville det(Phi_weighted)*C=1 residual: 1.3276277923018e-44 (limit 1e-20).
- Original binary64 background agreement: 1.0845238916636e-13 (limit 1e-10).
- Independent DOP853/Radau transfer discrepancy: 3.405054016525355e-13
  (rtol 1e-11, atol 1e-13; agreement limit 1e-8).

Analytic-domain samples allow 1e-60 for 70-digit decimal rounding only; this
does not enlarge the analytic domain or replace its proof. The 79 checks
include 20 inherited exact full-action/Euler checks, independent unreduced
dust momentum/continuity reconstruction, canonical generators, Fourier
phases, retained energy signs, domain bounds and serialization/source pins.

## Preservation, inherited work and next route

All historical failed attempts remain intact, including nonzero main v1
103/106, separate principal v1 7/9, binary64 response 120/125 and older G3/N3
failures. The three inherited missing UVIR sidecars remain declared. The
earlier [G3E zero-evolution report](RES001_R4C1_G3_ZERO_EVOLUTION_REPORT_2026-09-30.md)
uses a different parameter family/coordinate; its controls are lineage, not
a B1 GR limit or a replacement for this calculation.

Next bounded route: compare the full finite-k constrained evolution and its
actual dust observables with this derived slow system on the same B1 window.
Register modes, constraint-preserving initial data, accuracy controls and
rejection tests before execution; quantify fast-mode contamination and
slow-remainder error without discarding modes or changing the action. A
finite sample cannot by itself prove a uniform physical validity window.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Physical cutoff/causality, all-direction evolution, complete energy/ghost
interpretation, nonlinear source closure, healthy full GR, G_eff/PPN and
microscopic/coefficient/weak-field matching remain substantive requirements.
Rule-9 review alone does not block provisional research in the checked scope,
but deferred review is not clearance or publication readiness.

Only new research files and append-only queue/register entries are added;
only those two mutable index sidecars are refreshed. No manuscript/PDF,
vault/provider/runtime/model change, commit, push, deployment, submission or
canonical promotion is included.
