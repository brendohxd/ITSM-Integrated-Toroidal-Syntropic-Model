# R-tau: a computer-assisted periodic initial-constraint existence certificate

31 October 2026. Claim Conditional; independent review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains an unadopted comparison action.

## Result and precise scope

The quantitative defect/contraction inequalities pass. Together with the
function-space and symmetry argument below, they give a computer-assisted
existence/uniqueness certificate for a nearby exact periodic solution of the
declared clock-gauge lapse/momentum/auxiliary constraints and inherited
clock/U(1) charge equations. Density is positive throughout the correction
ball. This is a nontrivial prepared INITIAL slice for the R-tau comparator.

It is NOT a time-evolving on-shell background, nonlinear Cauchy theorem,
full Dirac/physical-mode clearance, reduced interaction calculation, physical
cutoff/window, microscopic match or publication clearance. The original
unchanged R4C1 action and its failed alignment restrictions are not repaired
by this result. No canonical parent is selected.

The [owning periodic-preparation contract](RES001_R4C1_RTAU_PERIODIC_PREPARATION_V1_CONTRACT_2026-10-31.md)
now has a declared-scope continuum constraint certificate, rather than only
finite-grid agreement. The wider G1-G6 programme remains incomplete.
Follow the [inverse contract](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_CONTRACT_2026-10-31.md),
[execution specification](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_SPEC_2026-10-31.md)
and [independent-control specification](RES001_R4C1_RTAU_PERIODIC_INVERSE_AUDIT_V1_SPEC_2026-10-31.md).

## Data, equations and explicit centre

The prescribed metric, condensate, reservoir, force, frame and velocity
profiles remain exactly those frozen before the numerical solve at
epsilon=1/1000. All three frame components are present. H and omega are
the two free continuation parameters, with inherited normalized charge
targets 1/5 and 1; no acceleration or observational target is inserted.

The original numerical candidate and its exact binary coefficients are
preserved. The new explicit symmetry centre keeps cosine coefficients of
Sx/Sy and sine coefficients of Sz. The other numerical coefficients are
recorded as a correction, not silently removed from the evidence. Their
componentwise C2 displacement bound is

    Delta < 1.513e-12.

This is obtained from the sum of n^2 times each removed coefficient's
absolute exact binary value. The new coefficients and exact interval bound
are exported in the receipt. H and omega are unchanged at the centre.
The displacement is included in the defect estimate below.

Use X=(Sx,Sy,Sz,H,omega) and the full equations

    F(X)=(L_S-d_z(L_Sz), I_clock-1/5, Q_U1-1),
    I_clock=average((L_N-beta*psi_z*L_Nz)/C),
    Q_U1=average(u*pi_v-v*pi_u).

The clock integral uses exact periodic integration by parts of the lapse
Euler flux. Local matter reconstruction is rho=(L_N-d_z(L_Nz))/sqrt(h).
Positive clock lapse and exact Z=-Delta_h(psi) are retained. The old bare
local dust continuity equation is not substituted for the new clock exchange.

## Complete function spaces and momentum compatibility

Take periodic real C2 shifts with Sx/Sy even and mean zero, Sz odd. The
two other unknowns are real constants. Use product norm

    ||delta X||=max_i(||delta S_i||C2,|delta H|,|delta omega|),
    ||S||C2=max(||S||infinity,||S_z||infinity,||S_zz||infinity).

The codomain uses C0 component supremum norms and absolute charge defects.
These are fixed mathematical control-unit norms, not a physical frequency
cutoff or a new microscopic normalization. The C2 product space is complete.
All harmonics allowed by the exact symmetry are present in the correction
space; the proof is not confined to the numerical grid's Fourier cutoff.

The symmetry is supported by the frozen action and initial profiles.
Scalars, conformal metric and their velocities are even under z reflection;
Vx,Vy and their velocities are even, Vz and its velocity are odd. N and Z
are even. The action's tensor contractions, potentials, regulator and force
norm are reflection invariant; there is no parity-odd contraction in this
declared classical action. Each term in its ADM density preserves these
transformation rules. Consequently E_Sz is odd. Planar shift VALUES Sx/Sy
do not enter the density (only their spatial derivatives do), so E_Sx/E_Sy
are full spatial divergences. Their integrated residuals vanish on the
circle; the odd longitudinal residual also has exactly zero mean.

Thus all three momentum mean equations are satisfied in this preparation
class, not dropped from a nonzero-mode solve. Constant transverse shifts
are coordinate gauge; the odd longitudinal shift already has zero mean.
This is a choice of symmetry-supported initial data, not continuous
projection of a time-evolving solution or a health claim for all data.
The separate future evolution problem retains the physical degrees of freedom.

## Reference inverse and full derivative enclosure

The homogeneous reference is

    L0_shift=-K0*d_z^2, K0=diag(1/2,1/2,-1/15),
    L0_charge=[[a,-1],[0,1]], a=(33/5)*sqrt(3469/4620).

The principal block comes from the freshly derived action Hessian, and the
charge block is checked against the same action at the homogeneous control.
The negative constraint pivot is not treated as positive coercivity.

The periodic zero-mean first-derivative Green kernel has L1 norm pi/2.
Composing it twice gives an inverse C0-to-C2 shift bound
15*pi^2/4<38. It preserves the specified parity and mean conditions.
For comparing the old numerical centre outside the exact symmetry class,
the same kernels define a bounded extension: its second derivative projects
out the forcing mean, with norm at most two, still below pi^2/4. This
extension is used only in the displacement estimate; the final F on the
symmetry class has exactly zero momentum mean as established above.

Enclose DF-L0 on the ENTIRE radius r=1/1000 ball. With local Hessian blocks
A=L_SS, B=L_S,Sz, C=L_Sz,Sz, its shift action is

    (A-(B^T)_z)*delta S+(B-B^T-C_z)*delta S_z-C*delta S_zz.

H/omega couplings and both charge rows are included. Charge derivative flux
coefficients are integrated by parts before the supremum bound is taken.
First-order spatial interval jets enclose coefficient derivatives and the
unknown function/first/second derivative ranges over every covering cell.

For the analytic SUMMAND the action is quadratic in S,S_z,H,omega on the
fixed profiles: Einstein/frame kinetic terms, scalar normal velocities,
alignment and K_Q force are quadratic; the potentials and clock-spatial
regulator do not introduce higher powers of these unknowns. Exact unit
polarization therefore extracts the shift derivative; symmetric unit
polarization extracts the charge-integrand derivative on the interval ball.
There is no finite-step derivative approximation in these enclosures.

The full norm-cubed force is retained separately. For q the exact boosted
rest gradient and q_S its longitudinal shift-value derivative, the verified
domain bounds give |q|<=2e-4 and |q_S|<=2e-8. The cusp contributions obey

    ||D_S E_S,cusp|| <= 6*A*N*sqrt(h)*|q|*|q_S|^2 <1e-17,
    ||D_S I_cusp|| <= 6*A*sqrt(h)/C*|q_S|
                       *(|q|^2+|psi_normal|*|q|*|V|) <1e-12,
    |rho_cusp| <= A*(|q|^3+3*|psi_normal|*|q|^2*|V|) <1e-10.

These follow from the norm gradient/Hessian inequalities and Cauchy-Schwarz.
They hold continuously at a zero rest gradient as well. No fictitious
analytic third amplitude derivative or A=0 action is adopted. In this ball
the packet in fact also stays away from that zero: its positive transverse
frame component and bounded normal velocity supply a positive rest-gradient
component. General amplitude nonanalyticity at the aligned background remains.

## Actual constants and Banach argument

The unpreconditioned analytic-plus-cusp derivative-defect row bounds are

| Row | Upper bound |
|---|---|
| Sx | 0.000369225 |
| Sy | 0.000388918 |
| Sz | 0.002124878 |
| Clock charge | 0.320392 |
| U(1) charge | 0.005601372 |

Precondition componentwise, using 38 for shift rows, (I_row+Q_row)/a_lower
for H and Q_row for omega. The scalar charge inverse is not replaced by
the much larger wave inverse. The resulting full product-norm bound is

    ||L0^{-1}*(DF-L0)|| <= q < 0.080746.

Use the earlier WHOLE-CIRCLE interval residual and charge defects. Include
the centre displacement as eta<=eta_original+(1+q)*Delta. The exact binary
interval calculations give conservative displays

    eta < 1.046775e-5,
    r-eta-q*r > 0.0009087869,
    rho > 0.14850 throughout the entire ball.

Hence T(X)=X-L0^{-1}F(X) has derivative norm at most q<1 and maps the
closed ball strictly into itself. The prescribed field profiles are smooth,
the local constraint principal block remains nonsingular, and the complete
force map is C1 on the ball; the full residual/charge map is well-defined
from the stated C2 space to C0/scalars. The symmetry and mean argument above
makes T a self-map of that complete function space. Banach's contraction
theorem yields an exact root X_star, unique WITHIN THIS BALL AND CLASS.

The root correction obeys

    ||X_star-X_centre|| <= eta/(1-q) < 1.139e-5.

This is a continuum argument covering all allowed harmonics. It does not
assert global uniqueness outside the ball or a separately measured Fourier
l1 tail. The root satisfies momentum constraints and both charge targets;
rho reconstruction satisfies the lapse equation, the positive lapse solves
the dust multiplier, the exact Z reduction supplies its auxiliary equation,
and the frame unit relation is retained in its actual parameterization.
No omitted mean or negative constraint direction is used as a propagating
positivity assumption. No all-sector Dirac/Hessian clearance is inferred.

## Reproducibility and independent relevant controls

- [Primary executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_periodic_inverse_v1.py),
  [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_v1_attempt_01/summary.json):
  11/11; SHA256 9c22269a9e40c331fd9c72ad72e44e9f67705524193293e2a11adc9f131827b9.
- [Additional audit](../../../Analysis/MasterTests/audit_01_r4c1_rtau_periodic_inverse_v1.py),
  [receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_periodic_inverse_audit_v1_attempt_01/summary.json):
  15/15; SHA256 a1ef2a03fcd26a561ce9843cd72106f57ed37530f0ca625ddfbdbb47bf787a52.
- BOTH complete recomputing read-only replays are byte-identical. Every
  exported cell derivative interval is additionally finite/ordered and each
  cell density lower endpoint is positive. Exact binary endpoints and the
  explicit parity-centre coefficients remain in the primary receipt.
- Independent full physical-action re-evaluation on shifted 65-node data,
  using two centered parameter steps in five unit product-norm directions,
  gave observed preconditioned derivative defects below 0.004879. These
  controls use the original full density and a different derivative assembly;
  they do not replace the interval proof or constitute external peer review.
- Source/sidecar bytes and mtimes are retained, including original numerical
  data, failed interval implementations and prior scoped failures. No test
  tolerance, candidate coefficient or action was changed to force acceptance.

The mathematical interpretation remains Conditional pending independent
review of the argument, outward arithmetic and implementation. Passing
counts alone are not the reason for the existence conclusion: the explicit
function-space, compatibility, derivative, defect and domain inequalities are.

## What follows, and what does not

This completes the declared-scope periodic INITIAL-CONSTRAINT preparation
milestone for the unadopted R-tau comparator. Next derive the actual reduced
quadratic/symplectic and principal evolution on this prepared inhomogeneous
data with its certified correction uncertainty, then supported nonlinear
evolution/interactions. Do not import the homogeneous propagator or assume
linear norm bounds prove that new physical problem.

No time-dependent on-shell solution, nonlinear Cauchy/domain persistence,
full reduced interaction functional, physical frequency/momentum window,
microscopic clock choice, realistic matter, GR/local compatibility or
identifying K_Q/nonlinear-force match is supplied. Original G1-G6 remain
INCOMPLETE; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED. F-tau's
gradient failure and original R4C1 results remain unchanged. No canonical
action adoption, manuscript/site edit, publication, provider dispatch,
vault mutation or commit/push. Native goal ACTIVE.
