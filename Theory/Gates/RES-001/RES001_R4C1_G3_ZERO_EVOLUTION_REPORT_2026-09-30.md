# R4C1-G3E: evolving slow branch and reconstructed GR dust control

Date: 2026-09-30. Owner: Master Test 1 / conditional R4C1-v1 / G3.
Local evolution validation 83/83; separate post-run GR control 9/9.
No failed/unknown local checks. Review DEFERRED; Rule9_cleared=false.
physics_pass=false, gate_effect=NONE. Canonical Tests 1–3 HOLD_SUBSTANTIVE.

## Result and exclusions

Coefficient derivatives change G3Z's frozen frequency interpretation. The
formal evolving low-frequency branch has **zero first-derivative coefficient**
in its canonical coordinate. Its leading dust-density/velocity reconstruction
is rank two. A separately labelled post-run dust-only coefficient-limit
control reproduces `Dddot+2H Ddot-(rho_m/2)D=0` in MP2=1 reference units,
and hence the GR dust growing/decaying modes `D~a` and `D~a^(-3/2)`.

This is useful classical **linear slow-sector GR consistency**, not healthy
full-theory GR recovery. The reduction selects a formal well-prepared
low-frequency branch: arbitrary fast-wave initial data, full PDE remainder
estimates, mixed-regularity evolution, homogeneous/singular modes and a
physical EFT window are not proved. Neither the original Jordan obstruction
nor tensor-cone, interaction/cutoff or canonical parent holds is cleared.
No observed acceleration coefficient is supplied.

The [G3E contract](RES001_R4C1_G3_ZERO_EVOLUTION_CONTRACT_2026-09-30.md)
was frozen before calculation. The GR control is explicitly **post-run**,
not preregistered. All earlier action, background and frequency records
remain intact, including G3's original 112/113 failure.

## 1. Differential reduction at fixed comoving k

Use G3S's full canonical `xddot+G xdot+W x=0`, its transformation R and
the new G3 background flow. Let x_W=X(t), the four propagating coordinates
start at Y_i/k, and the force coordinate at F1/k+F2/k^2+F3/k^3. Retain
dummy next-order propagating amplitudes Z_i/k^2 throughout the calculation.

The force equations at k^3,k^2,k^1 determine F1,F2,F3. Higher-power
propagating residuals cancel; their leading k equations determine Y_i.
Time differentiation of the solved coefficients includes a(t), H(t), all
field/background derivatives and hence the p(t)=k/a(t) drift. The W equations
at positive k powers cancel, and the O(1) equation loses every dummy Z_i.
The retained-field differential reduction, not lambda->d/dt substitution,
therefore gives

```text
-(12-eta)/eta * [Xddot + m_E(t) X] = 0,
m_E = -H^2/4 - Hdot/2 - rho_m/(2 M_c^2)
      + beta (psi_ddot+H psi_dot) - beta^2 psi_dot^2,
M_c^2 = 1-eta/12, beta=2 eta^2/5,
Hdot = -(udot^2+vdot^2+rdot^2+3 eta psi_dot^2+rho_m)/(2 M_c^2),
psi_ddot = -3H psi_dot-(2 eta/15)rho_m.
```

The compact mass form is a post-run exact algebraic simplification checked
independently against the unsimplified exported coefficient. All quantities
use the registered MP2=1 reference units; they are not observational units.
Holding the elimination coefficients fixed before differentiation instead
reproduces G3Z's inner pencil exactly. Thus the previous frequency audit
was not overwritten or found algebraically false: it answers a different,
fixed-event question. Omission of coefficient derivatives fails this new
evolving reduction and is explicitly rejected.

The prefactor is negative for 0<eta<=1. Normalizing an ODE by it is not a
physical energy/ghost-sign assessment. The reduced action/Hamiltonian and
its slow/fast symplectic interpretation must be derived before claiming
positive energy of this branch. S1/G3S's positive full kinetic certificate
is retained at its scope; it alone does not settle the new low-frequency
effective energy question. No sign was discarded to claim stability.

## 2. Matter and frame reconstructed from the constraints

Reconstruct q=R x and qdot with the full background derivative; only then
substitute the reduced Xddot equation. Use S1's generic auxiliary solutions
with G3 parameters, not B1's evaluated lapse, shift or density formulas.
Dust normalization and `z=-delta Delta_psi` vanish exactly after substitution.
Density follows from `delta rho_m=C^4 delta epsilon+4 beta rho_m delta psi`.

Choose the physical-amplitude chart `X=sqrt(eta)*chi/k`. Eta is constant
on each member, so this does not change the time equation. It is a declared
normalization for the slow density response, not a claim of uniform energy.
The leading maps for D=delta rho_m/rho_m and V=k*v_d, where v_d is the dust
tilt relative to the ADM normal, are

```text
D = sqrt(6)(eta-12)/(a^(5/2)rho_m)
    * [(H/12-eta^2 psi_dot/15)chi - chidot/6],
V = -sqrt(6)/(H a^(3/2))
    * [(H/2+2 eta^2 psi_dot/5)chi + chidot].
```

The map from (chi,chidot) to (D,V) has determinant
`(12-eta)/(a^4 rho_m)>0` on the stated domain. This removes the displayed
1/sqrt(eta) amplitude singularity from these observables, not the original
canonical/auxiliary rank change at eta=0. Leading reconstructed lapse and
regulator vanish; subleading metric/force perturbations are not asserted
zero. No Poisson law, dust source or density history was inserted to obtain D.

## 3. Separate post-run Einstein-dust consistency control

Along G3's declared family, nonmatter background energies and exchange tend
to zero as eta->0. For the formal coefficient control set those scalar
velocities to zero, rho_m=3H^2 and Hdot=-3H^2/2. Without inverting the
endpoint's original constraint block, the projected equations/maps give

```text
chiddot - H^2 chi = 0,
D = sqrt(6)/(3a^(5/2)H^2) * (2chidot-Hchi).
```

Differentiating this actual exported density map using the Einstein-dust
flow gives exactly `Dddot+2H Ddot-(3H^2/2)D=0`. Canonical solutions
chi~a^2 and chi~a^(-1/2) map to D~a and D~a^(-3/2), respectively.
Nine exact checks verify the compact mass, map determinant, boundary mass,
map provenance, density equation and both mode pairs. This is not a
target-data calibration, all-sector stability proof or new canonical action.

## 4. Finite-time accuracy and limits

For each of the six unchanged eta values, integrate the slow fundamental
matrix together with its background over [0,4], with both DOP853 and Radau,
rtol=1e-11,atol=1e-13 and 101 times. All twelve integrations finish with
finite values. Maximum normalized discrepancies are:

- Background versus pinned G3 trajectory: `1.68318e-11` (<1e-8).
- Two-method slow transfer: `1.98021e-12` (<1e-7).
- Determinant/Liouville identity: `7.80376e-13` (<1e-7).

Because the first-derivative coefficient is zero, the slow transfer
determinant is one. Maximum sampled canonical-chart amplification ranges
from about 3.715 (eta=1) to 4.588 (eta=1/1024). These are bounded finite-time
reduced-branch accuracy diagnostics, not proof of physical stability,
uniformity at arbitrary k/eta, or convergence of a full PDE solution to the
slow asymptotic. No arbitrary fast-wave initial data were suppressed and
then described as full evolution.

## 5. Provenance and next action

- Contract: `d1d64c216465956424589f95c940116bc198f5670552297b7e611894bcd385fa`.
- [Evolution executable](../../../Analysis/MasterTests/test_01_r4c1_g3_zero_evolution.py):
  `31e753b1f4cf965e4998e3acb035b646252d1b5615db75ea3331b1e3ba76d059`.
- [Evolution receipt](../../../Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/summary.json):
  `1f13df62495f3a39198b697a7387f14086338306a8a5e24462b1e873800f1b5a`.
- [Formulas](../../../Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/formulas.json):
  `f634e510fd6e04f51f0c2c6cc1f43d284b0b0c9e5d9c44d4a3b4de9d8a35e87f`.
- [Transfers](../../../Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/transfer.json):
  `981043dc0572f4d0ddd1d2165e77c488f607ac5746fe121a63e2db4172fb2a5c`.
- [Post-run GR executable](../../../Analysis/MasterTests/test_01_r4c1_g3_gr_density_control.py):
  `9facf8174099b2b53efe77ffc10d46c3035f3c5ea7964df84b0ecb6897953f8b`.
- [Post-run GR receipt](../../../Analysis/MasterTests/outputs/r4c1_g3e_gr_attempt_01/summary.json):
  `813353365311041ba341c96ec5949520e927df06f69bde8e5be19227930a5d28`.

All direct/inherited inputs are hash-verified. Both executable --replay runs
reproduce every artifact byte-for-byte without writes; new attempts refuse
existing targets. No older receipt-producing main() was invoked. One
supplemental one-line Python check had a syntax error before execution;
the corrected calculation and separate nine-check control are retained.
That command error did not change a scientific source or receipt.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z. Review debt remains
deferred for the hierarchy, time derivatives, reconstruction, GR boundary,
normalization and reduced-energy interpretation. PROCEED_PROVISIONALLY and
NONE_WITHIN_STATED_SCOPE apply to the verified formal slow reduction and
the separately scoped GR density control, not a positive-energy/full-IVP
claim. Independent review and all missing physics still govern promotion.

Next discriminating obligation: derive the slow/fast action and symplectic
energy signs, and test how the full finite-k system approaches this branch
with controlled initial-data/remainder estimates inside a physical validity
range. Canonical interactions/cutoff, singular modes, healthy full GR,
nonlinear weak-field derivation and blind coefficient matching remain open.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged. No PDF edit, provider dispatch, commit,
push, canonical promotion or publication occurred.
