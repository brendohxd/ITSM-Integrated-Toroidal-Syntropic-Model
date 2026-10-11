# G3N5 homogeneous canonical-energy and charge-sector audit

Date: 11 October 2026 (Australia/Perth). Version 1.
Status: CONDITIONAL_HOMOGENEOUS_CANONICAL_CHARGE_SECTORS_CHECKED.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Outcome and scope

The retained normalized mean metric-trace coefficient -11/20=-0.55 is not
removed by the checked local constraints or by fixing the complex U(1)
charge alone. An admissible negative homogeneous canonical direction
survives in the original varying-dust-charge ensemble, in both the dust
and force-psi clocks. A separate fixed-complex-and-dust-charge sector has
a positive homogeneous momentum Hessian on the stated regular B1 domain.
That extra global charge restriction changes the ensemble; it is not a
gauge removal or a repair of the original result.

This completes the bounded [approved goal](../../Core/ITSM_G3N5_MEAN_MODE_ENERGY_GOAL_PLAN_2026-10-11.md),
not the full physical stability, propagating-ghost, EFT/GR or Tests 1-3 programme.
The [frozen acceptance contract](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_CONTRACT_2026-10-11.md)
and [prior linear response report](RES001_R4C1_G3N5_CONSTRAINT_RESPONSE_REPORT_2026-10-10.md)
remain unchanged. Scope is the frozen R4C1/B1 action, k=0, t_E in [0,0.05],
coordinate periods 2*pi. Momenta and charges below are per coordinate-cell
volume; integrated charges multiply by (2*pi)^3. B1 q=1 and P_tau=1/5.
Registered K=3 and the other dimensionless action parameters are controls,
not a derivation of canonical microscopic K_Q or a physical calibration.

## Evidence and reproducibility

| Calculation | Local checks | Replay |
| --- | --- | --- |
| Full 22-field constraints, two clocks, charge sectors and finite witnesses, v4 | 124/124 | exact read-only replay |
| Separate unfixed-lapse homogeneous Legendre calculation, v1 | 12/12 | exact read-only replay |
| Independent complete charge-sector momentum-block comparison, v4 | 18/18 | exact read-only replay |

These are local calculations by this agent, not an independent external
review panel. No failed or unknown current checks remain. Review stays
DEFERRED, with inherited dependencies retained.

Current [canonical receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_mean_mode_energy_attempt_04/summary.json)
SHA-256: bdda5069e8650b2bcdb5cb897978c493f480443e7ad254479c20502c6fac5c93.
[Independent comparison receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_homogeneous_hamiltonian_compare_attempt_01/summary.json)
SHA-256: 36e395b5a9b973cde655fe580a7b985553d4ad6aa25d667631fc55a310b511ba.
The unfixed-action-only receipt is
[retained separately](../../../Analysis/MasterTests/outputs/r4c1_g3n5_homogeneous_hamiltonian_attempt_01/summary.json),
SHA-256 e006ea322f1eea94fbba9c425d84c832eb578e9ec33164595eee3e8c3b4dfd04.

Frozen [main v4 source](../../../Analysis/MasterTests/test_01_r4c1_g3n5_mean_mode_energy_v4.py)
SHA-256: 4b56c1f89406dba379f790b1f1a0cea66ee9ed570717ac201925f9d219d5e469.
Frozen [comparison v4 source](../../../Analysis/MasterTests/test_01_r4c1_g3n5_homogeneous_hamiltonian_v4.py)
SHA-256: 8c5c4cfded924f74dd2907568872a7e68f4d3d59ad53707c6baf810cbbd18ed6.
The comparison's four scientific functions are AST-identical to its v1/v2/v3
versions; only parent/output metadata and source pins differ.

The main receipt verifies 168 dependency pins and 165 available sidecars
before and after calculation. The three inherited UVIR sidecar absences are
explicitly retained. All 1,172 exported nonzero coefficients pass exact
structural serialization roundtrip. Complete generic matrices are retained in
[canonical.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_mean_mode_energy_attempt_04/canonical.json)
and [charge_sectors.json](../../../Analysis/MasterTests/outputs/r4c1_g3n5_mean_mode_energy_attempt_04/charge_sectors.json).
The latter supplies all A/R/K blocks; the Legendre formula below specifies
their complete quadratic Hamiltonians, not just a kinetic-sign summary.

## Momenta, constraint chain and symplectic reduction

For the retained 22-coordinate action, with v=a^3,

L2 = v*(q^T A q/2 + q_dot^T R q + q_dot^T K q_dot/2),
p = v*(K q_dot + R q).

The velocity block has fifteen variables and seven primary null momenta:
alpha, Sx, Sy, Sz, Em, Z and LambdaU. On the invertible dynamic block,

q_dot_dyn = K_dyn^(-1)*(p_dyn/v - R_dyn*q),
Hqq = v*(R_dyn^T*K_dyn^(-1)*R_dyn - A),
Hqp = -R_dyn^T*K_dyn^(-1), Hpp = K_dyn^(-1)/v.

The executable retains every field until constrained. Its eight second-class
constraints are p_Em/density consistency, p_Z/Z, and the four-link
p_LambdaU/nu/normal-consistency/multiplier-fixation chain. Coefficients are

h_Em = v*C^8/rho_m,
h_nu = -330/(31*v),
h_LambdaU = -v*h_nu.

The exact Poisson determinant is h_Em^2*v^2*h_nu^4, nonzero on
v>0, C>0, rho_m>0. The pullback graph satisfies all eight constraints and
T^T*J44*T=J36. Five first-class constraints remain: the lapse primary and
time secondary, plus three homogeneous shift primaries. The secondary's
consistency includes its explicit B1 derivative. Its coefficients of p_T
and p_Pi are C and psi_dot respectively, fixing the clock domains.

Each time gauge gives thirteen canonical pairs with the standard reduced
symplectic form. This is a local homogeneous chart count, not a global
physical degree-of-freedom theorem. Fixing complex charge and quotienting
its global angle gives twelve pairs; additionally fixing dust momentum
and quotienting its global origin gives the separate eleven-pair control.

## Two clocks and the time-dependent canonical map

Dust clock: T=0, alpha=-beta*Pi, C>0.
Second clock: Pi=0, alpha=T_dot/C, psi_dot>0.
The second clock is the existing force field psi, NOT the complex U(1) angle.

For the derived configuration map q_psi=D*q_dust, the pulled-back actions
obey K_pull=K_dust and differ by the quadratic boundary generator
W=v*(R_pull-R_dust), with W=W^T and
v*(A_pull-A_dust)=dW/dt. The momentum map is

S = [[D,0],[D^(-T)*W,D^(-T)]],
S^T*J*S=J,
J*H_psi*S - S*J*H_dust - dS/dt = 0.

Both the unfixed-complex and fixed-complex constructions pass the full
identity exactly on the specified background constraint. The nonzero
time generator must not be omitted. The reduced quadratic Hamiltonian is
time dependent: dH2/dt=partial_t H2 along its canonical evolution. No
conserved perturbation-energy theorem is inferred. The full unfixed-action
dust-clock Hamiltonian below also has the explicitly checked C_background
energy-balance term.

An analytic interval comparison gives
psi_dot >= -3469/210000 + exp(-sqrt(4006695)/15400)/5
=0.1591037670864998; the saved minimum is 0.174825737177346.
The nonzero charge gives R^2 >= 700*exp(-sqrt(4006695)/7700)/3469.
These bounds use the registered positive-density B1 solution, nonnegative
potential and H_dot<=0; they do not follow from positive samples alone.
Zero radius, zero clock, zero density or singular alignment-coefficient
domains are excluded rather than inverted.

## Full complex charge and Routh reduction

For the homogeneous scalar radius R and boost squared B, the alignment
term changes the angular coefficient to

A_theta = v*R^2*(1-zeta*R^2*B)/N,
q = A_theta*theta_dot,
L_Routh,theta = -N*q^2/[2*v*R^2*(1-zeta*R^2*B)].

Its quadratic boost contribution -N*zeta*q^2*B/(2*v) is retained.
The Cartesian/polar canonical one-form, quadratic charge curvature and
nonlinear polar-map boundary terms are checked; delta-q=0 alone was not
used as a substitute for the full fixed-charge reduction. The cyclic
angle is quotiented only after Routh reduction.

The [v3 orbit addendum](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_V3_ORBIT_ADDENDUM_2026-10-11.md)
uses the exact instantaneous section u=R, v_scalar=0, u_dot=R_dot,
v_scalar_dot=q/(a^3*R), R>0, AFTER original Cartesian derivatives.
It is not a physical zero-angle or zero-angular-velocity trajectory.
Constant-rotation radius, kinetic, current, potential and canonical-one-form
identities pass exactly. Generic coefficient exports remain intact.
All reduced A/R/K, clock D/S/W and both Hamiltonian coefficients agree
between original and section evaluations on every untouched saved point:
largest normalized discrepancy 2.8422e-14, versus the unchanged 1e-10 bound.

## Canonical meaning of the negative direction

Let x=ln(v), MC=11/10 and K=3. The separately organized unfixed-lapse action is

L = -MC*v*x_dot^2/(3*N)
    + v*(R_dot^2+r_dot^2+K*psi_dot^2+R^2*theta_dot^2)/(2*N)
    - N*v*V + v*epsilon*(C^2*tau_dot^2/N-N*C^4)/2.

Its directly derived momenta are p_x=-2*MC*v*x_dot/(3*N),
p_R=v*R_dot/N, p_r=v*r_dot/N, p_psi=v*K*psi_dot/N,
P_tau=v*epsilon*C^2*tau_dot/N and q=v*R^2*theta_dot/N
on the aligned zero-boost witness. Positive dust density is
epsilon=P_tau/(v*C^3), rho_m=C*P_tau/v.
On the aligned isotropic witness, the exact full-action constraint is

h_other + C*P_tau = 0,
h_other = -3*p_x^2/(4*MC*v) + p_R^2/(2*v) + p_r^2/(2*v)
          + p_psi^2/(2*K*v) + q^2/(2*v*R^2) + v*V
          (aligned isotropic witness; shear/boost coordinates and momenta zero).

Separately, the complete quadratic B1 operator retains all five shear and
three boost momentum directions, with positive terms 2*p_shear^2/v and
3*p_boost^2/v in the stated normalized basis. Their coordinate/mixed
couplings remain in the generic exported matrices. This displayed aligned
constraint is not a nonlinear Hamiltonian formula for arbitrary boosted or
anisotropic backgrounds.

Dust clock: H_d=(C_background/C)*h_other.
Force-psi clock, positive momentum branch:
H_psi=-psi_dot_background*sqrt(2*K*v*(-h_rest-C*P_tau)),
where h_rest=h_other-p_psi^2/(2*K*v).
Setting shear/boost values to zero for an explicit witness does not drop
them from the audit: the complete 12-by-12 dust kinetic block, all 144
original force-clock momentum-inverse identities and all 121 fixed-both
identities are independently checked.

The trace chart Mxx=Myy=Mzz=2*delta-x/3 has K_x=-2*MC/3=-11/15.
This maps to the retained Frobenius-normalized trace eigenvalue -11/20.
Consequently H_d,p_xp_x=-3*C_background/(2*MC*v*C)<0.
In the force-psi chart the (p_x,P_tau) momentum subblock has

det = -2*c*C^2/(K*v*psi_dot^2)<0, c=3/(4*MC*v),

at the regular B1 background. Thus the original homogeneous sign survives
the checked local constraints and the second clock. Its admissible witness
changes the separately conserved global dust momentum: it is not a gauge
direction. This conclusion is not a local propagating-ghost identification.

The distinct fixed-P_tau=1/5 control has
Hpp=-2*B+4*(B*p)*(B*p)^T/(K*v*psi_dot^2), with the Lorentzian B specified
in the comparison artifact. The constraint gives p^T*B*p=F+U,
F=K*v*psi_dot^2/2>0 and U=v*(V+rho_m+angular_energy)>0.
Congruence to the timelike momentum rest frame is positive definite.
This proves the stated homogeneous momentum control, not positivity of
the full quadratic potential, characteristic stability or a physical EFT band.

At every saved point the fixed-complex-only kinetic inertia is 11 positive,
1 negative, 0 zero in BOTH clocks. The separate fixed-both inertia is
11 positive, 0 negative, 0 zero. Eigenvalues and negative cyclic dust
coefficient are retained, including the Schur-congruence removal identity.

## Admissible finite witnesses and numerical controls

At the exact B1 initial event, 70-digit evaluations use both signs of
amplitudes 1e-6, 5e-7 and 2.5e-7, fixed complex q=1, and positive recovered
dust momenta/densities. The dust-clock central quadratic coefficient is
-15/22. The force-clock witness approaches the same limit with the
derived O(amplitude^2) square-root remainder; it is not falsely tested as
an exact finite-step polynomial. Finest normalized numerical errors are
5.410e-58 and 5.269e-58, below the original 1e-30 bound.
The two finite families need not have the same second-order dust-momentum
correction; each satisfies its own constraint/clock construction.

Saved charge errors are <=1.540e-13 (complex) and <=3.942e-14 (dust);
Friedmann discrepancy <=2.201e-13. These remain below the original 1e-10
criterion. No physical observational fit or microscopic input follows.

## Attempt history, preservation and remaining work

Main v1/v2/v3 were deliberately interrupted for symbolic-computation
bottlenecks; each ended without a scientific acceptance receipt. Preserve
their frozen sources/sidecars and private checkpoint history. They are
neither accepted results nor physics failures. The
[v2](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_V2_COMPUTE_ADDENDUM_2026-10-11.md),
[v3](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_V3_ORBIT_ADDENDUM_2026-10-11.md) and
[v4](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_V4_COMPUTE_ADDENDUM_2026-10-11.md)
addenda record the computational changes. V4 expands the same two-by-two
determinant directly, and projects factors before the charged Hamiltonian
product; original Cartesian derivatives still precede projection.

The main and comparison fourteen-file output/sidecar set is unchanged in
hash, byte size and UTC last-write timestamp after exact replay. All 317
original baseline files/sidecars are unchanged. Original binary64 linear
response v1 stays FAIL_LOCAL_CHECKS, 120/125, with five failed refinement
checks. The earlier 70-digit linear-response v2's 124/124 is a DIFFERENT
checkpoint from the current canonical 124/124. Original G3/N3 failures and
three inherited missing sidecars are not cleared.

The bounded canonical disposition is complete, conditional and review-deferred.
Next substantive lane: constrained nonzero-mode characteristics, gradient/ghost
domains and a physically justified cutoff/window; retain homogeneous and
singular-domain boundaries. Separately, unsmoothed nonlinear response,
healthy continuous GR, G_eff/PPN, weak-field and microscopic matching remain.
No general no-go for ITSM or global stability/energy theorem is claimed.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No original hash/negative eigenvalue/failure is replaced; no manuscript/PDF,
vault/runtime/provider/model change, commit, push, upload or publication.
Queue/register updates are append-only with their old byte prefixes preserved.
