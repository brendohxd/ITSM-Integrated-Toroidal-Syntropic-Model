# R4C1-G3N3: coupled second-order regulator and dust equations

Date: 9 October 2026. Version 1 report; final executable v2.
Conditional; review DEFERRED; PROCEED_PROVISIONALLY within the declared chart.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Outcome and boundary

The complete second-order regulator equation and dust multiplier constraint
are derived for the inherited transverse (t,z) perturbation geometry, with
arbitrary second-order metric, shift, frame, psi and dust responses retained.
Final validation: 515/515 local checks, exact read-only replay. This supplies
actual coupled response equations, not a solved all-sector response or a
physical reduced Hessian. No full nonlinear uniqueness, cutoff, continuous
GR limit or canonical Test-1 closure follows.

The original 512/514 attempt is preserved. Two expression-identity assertions
were repaired in a separate version after independent exact residual checks;
the formulas and independent numerical-control artifacts are byte-identical
between attempts. No action, parameter, sample, tolerance or physical equation
was changed to obtain the final result.

## Retained chart and fields

The homogeneous cosmic-time chart has N=1 and tau_dot=C=exp(beta psi_0),
not tau=t. Write perturbations without a factorial convention:

```text
N=1+epsilon^2 alpha
h_ij=a^2(delta_ij+epsilon^2 M_ij)
N^i=(epsilon B delta_iy+epsilon^2 S_i)/a
v^i=(epsilon W delta_iy+epsilon^2 V_i)/a
gamma=sqrt(1+h_ij v^i v^j)
U^t=gamma/N; U^i=v^i-N^i gamma/N
psi=psi_0+epsilon^2 Pi; tau=tau_0+epsilon^2 T
z_aux=epsilon^2 Z.
```

All six independent M_ij, three S_i, three V_i, alpha, Pi and T are retained
until the required equations are expanded. The frame parametrization solves
its unit constraint; it does not replace independent U by a hypersurface-normal
field. The frame multiplier's remaining normal equation is not solved here.
B is arbitrary during derivation. Inserting the existing linear transverse
shift solution B=-eta W/(8-eta) leaves the derived regulator equation unchanged.
The second-order metric and other dynamical equations are not set to zero:
their response variables remain unsolved.

## Derived regulator equation

Let p=psi_0_dot and L=psi_0_ddot+2Hp. Direct construction of the ADM inverse,
connection, normalized frame, projector and covariant Delta gives

```text
Delta0=Delta1=0
Delta2 = Pi_zz/a^2 + (p/a) partial_z(V_z)
         + p W W_dot + L W^2
Z = -Delta2.
```

This retains the acceleration term in the frozen covariant definition of
Delta. The arbitrary second-order lapse, spatial metric and shift fields
cancel from this equation at the declared order. V_x and V_y also cancel
under the inherited (t,z) dependence. These cancellations are derived, not
assumed by freezing the metric. The two induced terms reproduce the S1
linear operator applied to second-order response; the direct transverse
terms reproduce G3V/G3N2. Each has mass dimension two.

Consequently, Z=-[p W W_dot+L W^2] is not the full solution unless the induced
operator Pi_zz/a^2+(p/a)partial_z(V_z) vanishes. That condition cannot be
assumed from a raw psi/z Hessian or a one-amplitude probe. This calculation
derives the equation; it does not determine Pi or V_z from the other sectors.

## Dust constraint and regulator action contribution

Expanding the dust multiplier equation before imposing it gives

```text
[C(psi)^2 (nabla tau)^2+C(psi)^4]_2
    =2C^4(alpha+beta Pi-T_dot/C)=0
alpha=T_dot/C-beta Pi.
```

Dust is not identified with U. Prematurely setting alpha=0 or tau=t loses
this response equation. No substitution setting the dust action to zero
before variation is used.

The regulator contribution at order epsilon^4, divided by background a^3
and using the frozen periodic/fixed-endpoint boundary convention, is

```text
Lreg4=b Z^2/2+b Z Delta2
Lreg4|Z=-Delta2 = -b(Delta2)^2/2.
```

This is only the regulator contribution, not the full quartic Schur action.
It includes the induced-field/direct-source cross terms. The exported
Fourier response derivatives below are regulator-only terms, not complete
metric/frame/condensate/reservoir/matter forcing.

## All generated even harmonics and the mean

For the parent's W=cos(chi)+(1/3)cos(3chi), chi=kz, and registered
W_dot=(1/4)cos(chi)-(1/8)cos(3chi), write
Pi=sum Pi_m cos(m chi), V_z=sum V_m sin(m chi), m=0,2,4,6.
The rates 1/4,-1/8 are reference-chart rates, not a derived physical frequency.
Restoring their rate unit omega_ref (numerically one in the receipt), the
direct source coefficients are:

| m | D_m for p W W_dot+L W^2 |
| --- | --- |
| 0 | 5 omega_ref p/48 + 5L/9 |
| 2 | 5 omega_ref p/48 + 5L/6 |
| 4 | -omega_ref p/48 + L/3 |
| 6 | -omega_ref p/48 + L/18 |

Every full coefficient obeys

```text
Delta2_m = D_m - (mk)^2 Pi_m/a^2 + (p mk/a) V_m
Z_m=-Delta2_m.
```

For m=0 the induced derivative terms vanish on the periodic torus, so
Z_0=-D_0. The zero mode is retained without dividing by k or a Laplacian.
The registered chart witnesses give mean Z_2 between 1.5452044480533577e-6
and 0.09945156155447882. These are reference-profile jets on inherited
background records, not newly solved on-shell waves or observational data.

For m>0 an algebraic choice Pi_m=a^2 D_m/(mk)^2,V_m=0 changes Z_m to zero.
This illustrates why the direct source alone does not fix the nonzero-mode
response; it is not asserted to solve the other field equations. With average
weight c_0=1,c_m=1/2 for m>0, the regulator-only response derivatives are

```text
d<Lreg4>/dPi_m = b c_m (mk)^2 Delta2_m/a^2
d<Lreg4>/dV_m  = -b c_m p mk Delta2_m/a.
```

All 216 inherited charts retain the four direct source coefficients, which
agree with G3N2 to normalized error <=8.327e-17. The finite harmonic set is
not claimed invariant under the full nonanalytic field evolution.

## Independent controls and transparent repair

Two generic off-shell jets retain nonzero second-order lapse, all spatial
metric components, shifts, frame responses, Pi and dust gradients. The
unexpanded calculation uses exact unit normalization and 50-digit mpmath.
It independently compares the Hessian-trace/theta and projected-divergence/
acceleration definitions of Delta; discrepancies are <=3.852e-52.

Even second differences at epsilon=1e-3,5e-4,2.5e-4 decrease at the expected
order. Final largest normalized Delta2 discrepancy is 2.434e-9 and dust
constraint discrepancy 9.761e-9, below the unchanged 1e-5 acceptance bound.
These are independent implementation paths, not reviewers, a full domain
proof or increased precision for inherited binary64 trajectories.

Attempt 01 (v1) failed two assertions, explicitly retained:

- reject_direct_source_as_full_Z_solution used structural expression equality.
  Its independently evaluated exact residual is zero, while b times the
  induced operator is generically nonzero. v2 checks that residual directly.
- all_direct_harmonics_exact_reconstruction retained the unevaluated identity
  4cos(2chi)^3+6cos(2chi)^2-3cos(2chi)-3cos(4chi)-cos(6chi)-3.
  Independent Chebyshev-polynomial expansion proves it is exactly zero.
  v2 expands the trigonometric polynomial before the zero-residual check.

v1 and its sidecar/failed output remain untouched. v2 also pins the failed
receipt and exports both failed assertions. Diff inspection finds only the
two assertion repairs, version/output labels and failure-provenance additions.
Both formulas.json and independent.json are byte-identical across attempts.

## Reproduction and provenance

Contract SHA-256 525c4ac96d08574912a49c31e7e64df597a1e13e34bffbc483ad36a23c9a9530.
v1 executable SHA-256 991c6234e46fab15c8de5a32907d3f7964e2c88b8182566961d3474b79909c8b.
Final v2 executable SHA-256 937c9e2130ce17c7ef671471e02f9ff81c63e84de5d191ed10bd87c7fe3f1a20.

Final directory: Analysis/MasterTests/outputs/r4c1_g3n3_attempt_02.

| Artifact | SHA-256 |
| --- | --- |
| summary.json | ee6683f0b99a087f009e29c653e719fb86647242182c58beea7f44b5e9998871 |
| formulas.json | 919dcbf41470a9bd693cf7b83a929dbb6a975f01d7e24d5c3089510a17b15328 |
| response.json | 3839631db2de20063028e509ef415a05275b9dcd15740345f4e363a232409a9e |
| independent.json | 1b7fb79da21892f188f789b7c7e3f7bfd6692f00bd4ee0a21ad968bd803e0a01 |

Preserved failed summary: r4c1_g3n3_attempt_01/summary.json, SHA-256
d4f6abf7b98bde67f1e4ce12534fc0fd8fb608cf5d4616d94fe6e9efaa3ec8a4.

```text
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3n3_second_order_regulator_v2.py
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3n3_second_order_regulator_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3n3_attempt_02
```

Both exit zero. Replay compares every output/sidecar byte, and independent
before/after snapshots verify unchanged hashes, lengths and last-write times
for all eight final output/sidecar files. All 112 source pins and 109 available
sidecars match before and after calculation. The three inherited absent
sidecars and original G3 balance failure are preserved, not rewritten.

Private logs, not release/commit artifacts:
attempt 01 .local/itsm-context/output-738321fb2849490b92310fc77c83730d.txt,
SHA-256 a1dba3be0b95341e0a1d15eae48b933dde65f4a34b56167278a0f3bbbe77e1a2;
attempt 02 .local/itsm-context/output-bc0defeb4b1d4952ae5bbef2d137d8e8.txt,
SHA-256 0fe518c5fa154b02549bf4401d59fa586e5ec25126787c3a653f7fbe4d7153b1;
replay .local/itsm-context/output-cce162f953ec45bc9da391ecc40053d1.txt,
SHA-256 45c9f8e2d851d14c37f19cc37034f17e3caedae08977dec1fe5e1fa730756ce8.

## Next substantive calculation and unchanged holds

Assemble the remaining second-order metric/frame/condensate/reservoir/matter
sources and solve for compatible response and initial data. Keep homogeneous
constraints separate from nonzero-mode Schur inverses. Retain the absolute-
cubic force, including its nonanalytic vector forcing and further harmonics;
do not replace it with an ordinary third Taylor vertex or assume a finite-mode
invariant PDE. These equations are inputs to that calculation, not its result.
Physical Cauchy/DAE domain, all-sector stability, cutoff and GR continuity
remain open. Tests 2-3 and canonical MAT matching retain their dependencies.

Inherit R9-MT1-G3N2, R9-MT1-S1 and full scientific/review debt. Rule-9 review
alone is DEFERRED; unsupported physical uses remain blocked substantively.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action change, manuscript/PDF edit, vault mutation, provider dispatch,
commit, push, canonical promotion or publication. Native full goal ACTIVE
and incomplete, not redefined around this smaller completed calculation.
