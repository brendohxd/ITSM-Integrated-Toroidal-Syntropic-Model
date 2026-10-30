# Quartic dust and phase: sampled initial tangency with physical normalization

28 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Finding and scope

On ten registered NONNODAL points of the unchanged R4C1 B1 eta=1/4,
e=1/500,k=40 quartic initial representative, the independently calculated
Hamiltonian physical dust-density derivative agrees with the varied dust-clock
current. The condensate phase-charge derivative also agrees with its U(1)
current. All fourteen coupled accelerations are retained.

The corrected V2 run passes256/256 exact-identity, numerical, independent
real/Taylor and rejection controls, with no failed or unknown rows. A fresh
two-worker replay of the four-worker run produces identical scientific bytes.
All156 pinned parent/current source artifacts and their digest values remain
unchanged. These controls are same-author numerical/exact checks, not
independent peer review or a continuum transport certificate.

This adds a reproducible initial consistency diagnostic. It does not establish
background admission, a nonlinear solution, constraint persistence, physical
modes, a physical validity interval or microscopic matching. In particular,
none of these samples is a matrix inversion at an alignment node.

## 1. Preserve and explain the failed first attempt

V1 failed216/236: the dust comparison failed at every point and both steps;
the phase, Hessian, Euler, real-differentiation and other controls passed.
The failure was an error in this diagnostic's normalization, not evidence
against the R4C1 action. V1's executable, contract, receipt and sidecars are
preserved, and a two-worker replay reproduces its failed receipt exactly.

The original density is L=sqrt(h)*L_scalar. Its conjugate momenta Pi_i,
proper Legendre energy E and lapse flux J are weight-one densities. The
lapse equation therefore is

    E+partial_z(J)+sqrt(h)*rho=0,
    E=sum_i Pi_i*normal_i-L,
    J=gamma*h_inverse[z,i]*Pi_Vi.

The scalar physical density equals the weight-one value when h=I. Their
time derivatives differ. Differentiation BEFORE imposing that initial metric
and hdot=2H*I gives

    rho_dot=-E_dot-partial_z(J_dot)-3H*rho.

V1 omitted the final volume-dilution term. The unvalidated working-algebra
note and V1 contract share that error; they are superseded only for this
normalization equation by the separate V2 addendum. No old file is rewritten.
The correction is derived from the determinant/lapse equation; it does not
assign rho_dot from the dust-current comparison target or alter its tolerance.

An interior example illustrates the distinction in the declared reference units:

    rho=0.20000000008408385235...,
    densitized_rho_dot=+0.00024999930040651192...,
    physical_rho_dot=-0.28914222110255939603... .

The last value agrees with the independently varied physical dust-current
requirement. Real differentiation of the physical quotient and exact symbolic
determinant/quotient identities verify the conversion separately.

## 2. Full generator and independently varied currents

Use the original normalized-frame fourteen-coordinate density, including its
temporal regulator. Reconstruct the new quartic periodic shift with12 sine
modes and64 quadrature nodes, including5*b*p*W*w^5*wprime. Compare with8
modes. Use the existing restricted-root point H,U,Ud,W without refitting.
Do not substitute the old quadratic shift, mean density or a slow graph.

At each point solve the complete velocity Hessian system for all14
accelerations. Differentiate E along that actual generator. For J_dot retain
the inverse-metric drift as well as the frame Euler derivative:

    J_dot=(gamma_dot-2H*gamma)*Pi_Vz
          +gamma*(L_qVz-partial_z(L_dVz)),
    gamma_dot=(H-Hbg)*w^2/gamma.

Varying the ORIGINAL dust multiplier gives the future homogeneous-clock
root tau_dot=C, C=exp(beta*psi), and pT=sqrt(h)*rho/C. Clock variation
requires pT_dot=partial_z(R*pT). Therefore the independently derived target is

    rho_dot_required=R*rho_z+(-3H+Rprime+beta*p)*rho.

The phase target follows from the canonical/alignment U(1) symmetry. On
the initial u=Rc,v=0,udot=0,vdot=D chart with zero phase gradients,

    pTheta=Rc*Pi_v,
    pTheta_dot_actual=Rc*Pi_v_dot-D*Pi_u,
    pTheta_dot_required=partial_z(R*pTheta).

The actual Pi_dot comes from the full Hessian-vector/acceleration generator,
not from assigning the current law. The directly differentiated spatial phase
current equals -R*pTheta on this slice. Exact checks cover global phase
invariance, its initial flux, the dust multiplier, future clock momentum,
on-shell scalar source, current dilution and the metric-density quotient.

## 3. Registered controls and errors

The points are pi/4,3pi/4 and each of pi/2,3pi/2 offset by+/-0.1 and
+/-0.01.110 decimal working digits, complex steps1e-20 and1e-26, frozen
normalized tolerance1e-18. The following are numerical residuals, NOT
outward continuum/root-error enclosures:

| Control | Largest normalized error |
| --- | ---: |
| Physical dust-current comparison | 9.53e-41 |
| Phase-charge comparison | 2.05e-51 |
| Acceleration agreement across steps | 1.01e-30 |
| Independent real/Taylor controls | 1.89e-40 |
| Shift differential-equation residual | 3.61e-76 |
|8/12-mode shift comparison | 1.83e-53 |

The two interior points have independent real energy/physical-density
differentiation and real/Taylor Euler checks for metric,Vy,psi,Z. Each
registered point rejects omission of the physical-volume dilution, inverse
metric flux drift or beta*p*rho term. The smallest induced normalized
mismatches respectively exceed0.2242,2.17e-11 and1.58e-4. These checks
detect those particular omissions; they do not prove all implementation
errors absent.

## 4. Reproduction, provenance and next requirement

Executables:
Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v1.py and
Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py.
V2 source SHA256:
2122f6892b9936c7d30ea581d4ed2cb1b90a0d4fec9f0019de3963057d49f9c6.

Receipts:
Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v1_attempt_01/summary.json
SHA256 bb1da6eefe1f0d769745498956ab1f3d100f83e0e5b64871c82135edd63b4c61;
Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v2_attempt_01/summary.json
SHA256 d9879aa6c6c5e13ef4a5a7c0a60a54127e6a8d09c6d209976c496ede566fa359.

Use --output with a fresh directory and --workers4 to compute; --replay
with the retained directory and --workers2 performs immutable comparison.
The option syntax is '--workers 4' or '--workers 2'. V1 correctly exits2
because its failed criteria remain; V2 exits0. Both print
READ_ONLY_REPLAY_EXACT on successful byte comparison. Logs remain ignored
under .local; no earlier scientific artifact, sidecar, manuscript or PDF changed.

Next derive actual all-three-component alignment-set jets and normalized-frame
Ward/ADM transport with vector and interface terms. A sampled initial balance
does not supply continuum identities, admissible evolved regularity or a
time interval. The earlier jerk weak-interface term remains mandatory where
it actually enters transport; no nodal division is justified by this run.

PROCEED_PROVISIONALLY for the stated sampled controls and exact identities.
HOLD_SUBSTANTIVE for continuum constraints, node persistence, actual background
admission, time evolution, physical modes/window/GR and identifying matching.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED. Review DEFERRED,
not cleared. No state/parent adoption, vault mutation, provider dispatch,
publication, commit/push or deployment.
