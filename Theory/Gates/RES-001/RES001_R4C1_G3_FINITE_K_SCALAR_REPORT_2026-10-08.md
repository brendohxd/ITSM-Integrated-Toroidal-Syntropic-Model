# R4C1-G3K: coupled finite-k scalar operator and clock-domain report

Date: 8 October 2026. Owner: conditional R4C1-v1 / G3T / Master Test 1.
Parent-authored local derivation. Conditional; PROCEED_PROVISIONALLY;
review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Outcome and scope

**744/744 registered local checks pass.** The complete closed scalar
sector for propagation along the tilt axis has been derived from the
unchanged covariant action, retaining its longitudinal shift constraint
and the time derivatives of all evolving coefficients. There are 120
sampled finite-k operators and eight short perturbation evolutions on
the sealed G3T backgrounds. All five final artifacts replay byte-for-byte.

The aligned limit recovers S1/G3S's six positive kinetic weights and an
algebraic regulator. At nonzero tilt the regulator contributes a velocity
pair with opposite signs in the dust clock. The shift elimination has an
exact rank boundary at w^2=1/5; that boundary is evaluated without division.

The sampled operators also retain positive real frozen exponents.
Neither their signs nor the dust-clock kinetic inertia establish a
physical ghost, a physical instability, a viable domain, or an
action-derived EFT cutoff. A healthy fixed-frame scalar control retains
the same clock issue. Physical characteristic/Cauchy analysis remains
a substantive required input.

This is the axisymmetric scalar sector with k parallel to the tilt,
on G3T's local reduced homogeneous candidates. It is not an
arbitrary-direction tensor/vector spectrum, a complete off-ansatz
four-dimensional background audit, a global I x T3 Cauchy theorem,
or a scattering calculation. G3V's zero-gradient cubic-vertex obstruction
remains; a valid quadratic Hessian does not supply the missing Taylor vertex.

## Action, constraints and independent checks

Use the original R4C1-v1 potential, canonical condensate/reservoir terms,
alignment term, force term and first-order regulator. All six sealed G3
parameter sets are inputs, including their assumed K_Q values. They do
not derive the outstanding canonical K_Q. Reference scale factors are
a_parallel=exp(alpha+2 sigma), a_perp=exp(alpha-sigma).

The scalar metric and normalized frame are

```text
gamma_xx = a_parallel^2
gamma_yy = gamma_zz = a_perp^2 exp(2 xi)
g00 = -N^2+B^2, g0x = a_parallel B
U0 = sqrt(1+w^2)/N
Ux = [w-B sqrt(1+w^2)/N]/a_parallel .
```

The longitudinal spatial diffeomorphism removes the radial metric
perturbation only at k!=0. The dust clock uses tau=t. The independent
coordinates after the algebraic dust-clock reduction are
q=(xi,w,u,v,r,psi,z); B is the physical longitudinal shift and has no
time derivative. Background xi, B and all spatial gradients vanish;
the other background fields and velocities are the evolving G3T ones.

The exact first-derivative scalar action uses

```text
gamma = sqrt(1+w^2), V = a_parallel a_perp^2 exp(2xi)
e0 f = (f_dot-B f_x/a_parallel)/N
e1 f = f_x/a_parallel
d0 = e0 w/gamma + N_x/(N a_parallel)
d1 = e1 w/gamma + (H_parallel-B_x/a_parallel)/N
F0 = (H_perp+xi_dot-B xi_x/a_parallel)/N
F1 = xi_x/a_parallel
nF = gamma F0+w F1

I1 = -d0^2+d1^2+2 nF^2
I2 = (w d0+gamma d1+2 nF)^2
I3 = (w d0+gamma d1)^2+2 nF^2
I4 = (gamma d0+w d1)^2

Q_f = gamma e0 f+w e1 f
S_f = w e0 f+gamma e1 f
Y = S_psi^2, Y_J = S_J^2
L_reg/(N V) = b z^2/2 - b S_z S_psi
              - b z (gamma d0+w d1) S_psi .
```

On the registered positive-gradient patch S_psi>0 the exact force
term is -A S_psi^3. The aligned zero-gradient control uses only the
valid C2 Hessian of the absolute-cube action.

Direct four-dimensional connection contractions verify the normalized
frame, projector, all four invariants, projected gradient, acceleration
projection and absence of B_dot. An independent spatial connection
gives R3=-(4 xi_xx+6 xi_x^2)/a_parallel^2. After the explicit periodic
spatial boundary transformation, the Einstein ADM/GHY density is

```text
M_P^2 N V [
 xi_x^2/a_parallel^2
 +2(N_x/N)xi_x/a_parallel^2
 -2 Kx F0-F0^2 ],   Kx=(H_parallel-B_x/a_parallel)/N .

L_Einstein_raw-L_Einstein_first
 = partial_x[-2 M_P^2 N V xi_x/a_parallel^2] .
```

In particular, the shift/curvature-velocity coupling is retained.
Freezing the metric before its constraint reduction would lose the
aligned S1/G3S kinetic result.

Before selecting the clock, the dust term is

```text
L_dust = V epsilon (C^2 tau_dot^2/N-N C^4)/2
C = exp(beta psi) .
```

The multiplier yields tau_dot=N C on its positive branch; tau=t gives
N=C^-1. The lapse equation solves the dust density:
rho_m=epsilon C^4=(delta L_pre/delta N)/V.
Here delta L_pre/delta N denotes the lapse variational derivative,
including spatial derivatives. It is not an extra discarded metric
constraint. The dust contribution to the psi equation on this shell is
-beta N (delta L_pre/delta N), exactly the lapse chain term in the
reduced action. These multiplier, lapse and psi identities are checked
before substitution. G3T's homogeneous density and conserved dust
integral remain inherited; no separate inhomogeneous positive-density
or all-amplitude claim is made.

At xi=.07, xi_dot=-.11, zero gradients and shift, all 24 registered
initial states also reproduce G3T's homogeneous action under
alpha=alpha_bg+2xi/3, sigma=sigma_bg-xi/3. Maximum normalized action
difference is 2.844969e-16.

The independent numerical benchmark constructs the defining metric,
connection, projector and action directly, then removes the stated
spatial boundary. Its action agrees within the frozen 1e-12 bound.
Central differences of all 23 jet variables give normalized Hessian
errors 6.967814e-9, 2.143337e-8 and 1.165882e-7 at
h=(1e-4,5e-5,2.5e-5). The finest error satisfies 1e-5. The increasing
roundoff floor is retained; this is a bounded independent witness,
not an extrapolation or convergence theorem.

## Fourier reduction and evolving operator

The exact Hessian is formed in (q,q_dot,q_x,B,B_x), then evaluated on
the evolving homogeneous background. With partial_x -> i k, define

```text
T = H_dd
W = H_dq+i k H_dx
Vmat = H_qq+i k(H_qx-H_xq)+k^2 H_xx
F = H_Bd-i k H_Bx,d
G = H_Bq+i k H_B,x-i k H_Bx,q+k^2 H_Bx,x
A_B = H_BB+k^2 H_Bx,Bx .

B = -(F q_dot+G q)/A_B
Tred = T-F_dagger F/A_B
Wred = W-F_dagger G/A_B
Vred = Vmat-G_dagger G/A_B .
```

The comma notation distinguishes a Hessian row associated with B_x
from a row associated with B and a column associated with q_x.
All coefficients and their derivatives are exported. Derivatives use
the actual G3T background flow at fixed comoving k, including scale
factors, field velocities and accelerations. The resulting equation is

```text
Tred q_ddot
 +(Tred_dot+Wred-Wred_dagger) q_dot
 +(Wred_dot-Vred) q = 0 .
```

The reconstructed B and B_dot satisfy the unreduced field and shift
equations in every sampled check. Maximum normalized reconstructed
residual over the 120 generic test events is 3.377924e-14.

An instantaneous 14-dimensional first-order generator retains these
coefficient derivatives before its eigenproblem is frozen. A static
congruence conditions that instantaneous calculation; it does not
represent a time-dependent canonical transformation. Perturbation
integration uses the raw, evolving coefficients.

For generic couplings, c123=c1+c2+c3 and c14=c1+c4,

```text
H_Bx,Bx = -M_U^2 V [c123-(c14-c123) w^2]/(N a_parallel^2).

G3: A_B = -eta V (1-5 w^2) k^2/(36 N a_parallel^2).
```

k=0 is a separate gauge/constraint sector and is never inverted.
w^2=1/5 is an exact zero of A_B and is checked without elimination.
Its two sign regions are both retained. A zero of this Schur denominator
does not alone establish a singularity of the unreduced physical system;
an alternative constraint chart or principal-symbol analysis is required
at the boundary.

## Aligned check and tilted kinetic signs

At w=w_dot=z=z_dot=0 and H_parallel=H_perp,

```text
Tred = V C diag(Dbar,eta/6,1,1,1,3 eta,0)
Dbar = 144(1-eta/12)(1-eta/8)/eta .
```

The full regulator velocity row vanishes; its algebraic Hessian
diagonal is b V/C>0. Thus z can be eliminated algebraically in this
control and the previous six positive S1/G3S weights are recovered.

The inherited dust-clock/radial-gauge mapping is
delta_tau_old=-C xi/H_proper,
delta_f_old=delta_f_new-f_dot xi/H_proper for f=(u,v,r,psi),
and w_old=w_new-k xi/(a_parallel H_proper) in the old real
cosine/sine convention. Substitution in the old completed squares
cancels their field/clock mixings and gives the Dbar weight.
The executable verifies the complete resulting kinetic matrix exactly.

For nonzero tilt, Tred_psi,z=-b V C w^2 and Tred_z,z=0.
The regulator contributes one positive and one negative direction
rather than an algebraic first-order auxiliary. The registered
inertias are:

| Initial tilt label | Events | Positive | Negative | Zero | Sign of A_B |
| --- | ---: | ---: | ---: | ---: | --- |
| 1/16 | 42 | 6 | 1 | 0 | negative |
| 1/8 | 18 | 6 | 1 | 0 | negative |
| 1/4 | 42 | 6 | 1 | 0 | negative |
| 1/2 | 18 | 5 | 2 | 0 | positive |

For evolved cases the labels identify the initial tilt; the actual
evolving tilt is used in every coefficient. All 120 velocity matrices
have rank seven away from the registered shift boundary.

These are dust-clock quadratic signs in the stated coordinate/action
chart. No physical energy-residue or ghost classification is inferred.

## Numerical roots and short evolution

Initial states: 24 sealed G3T cases, k=(20,40,80), giving 72 operators.
Evolved states: the four saved G3T eta/tilt cases, both archived methods,
t=(.0005,.001), the same k, giving 48 more. No background was
re-integrated, refitted or selected to change the result.

All 14 complex roots are retained for every event, with no positivity
or absence-of-growth pass requirement. Maximum normalized eigenpair
residual is 2.079381e-13. Every sampled event has a positive maximum
real exponent. Across all events those maxima span 18.11965 to
855.92190 in the stated reference coordinate-time units; at tilt 1/4
they span 51.89491 to 112.32767.

The 24 shared evolved-jet method comparisons retain both coefficient
and optimally matched complete root-set discrepancies:

- Maximum normalized coefficient difference: 1.355080e-11.
- Maximum matched normalized root difference: 1.974807e-13.
- Maximum matched absolute root difference: 4.192564e-12.

These are instantaneous roots of a time-dependent operator. They
do not establish sustained physical growth, nor can a kinetic sign
or a mode be dropped to manufacture a healthy spectrum.

Each root is also mapped as a formal covector diagnostic:

```text
omega_proper = i lambda/N, p_proper = k/a_parallel
Omega = gamma omega_proper-w p_proper
P = gamma p_proper-w omega_proper .
```

For complex lambda, Omega and P are complex. This mapping is not
a real preferred-energy particle identification or an EFT pole test.

Perturbations at eta=(1,1/1024), initial tilt=1/4, k=(20,80) use
both DOP853 and Radau over [0,.001], 51 samples, rtol=1e-10,
atol=1e-12. Both perturbation methods use the same sealed DOP853
background, interpolated by a cubic Hermite spline with slopes from
the exact G3T flow. The background interpolation/flow discrepancy
is at most 5.028313e-8, within the registered 1e-6 bound. It remains
a numerical interpolation, not an exact continuous trajectory.

All eight runs succeed. Maximum paired normalized state difference
is 1.070979e-10. Maximum reconstructed perturbation field residual is
2.500576e-15; maximum shift-equation residual is 6.806212e-17.
The unit-normalized initial perturbation has delta_psi=1 with the
other fields and velocities zero. Restoring the declared physical
amplitude 1e-12 gives maximum |delta S_psi|/S_psi=1.689501e-6,
below .01; the smooth-gradient patch is retained for this short IVP.

No long-time, finite-amplitude, uniform PDE, nonlinear stability,
or continuum momentum-band claim follows from these integrations.

## Healthy comparator and open physical domain

The separate fixed-frame preferred-time comparator has

```text
Omega^2 = c_psi^2 P^2+d P^4
c_psi^2 = 6 A sqrt(Y)/K_Q > 0, d=b/K_Q>0.
```

Its tilted proper-clock k=0 roots obey
omega^2=(gamma^2-c_psi^2 w^2)/(d w^4), and its frequency-momentum
map turns where
v^2(c_psi^2+2 d P^2)^2=c_psi^2+d P^2, v=w/gamma.
All 24 registered comparator substitutions satisfy their dispersion
and turning checks. This verifies that higher-time roots in a tilted
clock need a domain/foliation interpretation. The comparator cannot
replace the coupled scalar spectrum or derive its cutoff.

The next required research is a constraint-chart and preferred-Cauchy
analysis of the coupled characteristic problem, including the
w^2=1/5 boundary and admissible momentum/frequency conditions.
Transfer to arbitrary directions, tensor/vector sectors and global
I x T3 leaves remains separate required work. An action-derived
physical cutoff and physical scattering are still absent; the present
calculation does not authorize a SPARC force prediction or likelihood.

## Attempts, evidence and replay

Attempt 01 is preserved with 713/713 local checks, not a failed
physics calculation. Its script is archived byte-for-byte as
[version 1](../../../Analysis/MasterTests/test_01_r4c1_g3_finite_k_scalar_v1.py),
SHA-256 7b4133cc48d093ca0bfc926893083dc2b59bbe107550835dae6da26de526dee0.
Inspection found missing explicit audit coverage/exports required
by the frozen contract: dust-shell identities, homogeneous action
mapping and paired root-set discrepancies, plus the aligned z
algebraic check. Attempt 02 completes those records with 31 additional
checks. No action, parameter, grid, threshold or numerical operator
was changed. The formulas, coefficient matrices and perturbation
trajectories are byte-identical between the two attempts.

The final [executable](../../../Analysis/MasterTests/test_01_r4c1_g3_finite_k_scalar.py)
SHA-256 is 05f3c588d8424a9d7f65c69624b483394144da5ae242c75c54f238ef895e37de.
The [frozen contract](RES001_R4C1_G3_FINITE_K_SCALAR_CONTRACT_2026-10-08.md)
SHA-256 is eaefd9650e265512a516cf9770e67e8b6e3297e7ab0de2ab095b4c6d448366f9.

Final directory:
Analysis/MasterTests/outputs/r4c1_g3k_attempt_02/

| Artifact | SHA-256 |
| --- | --- |
| summary.json | 131e175a3d1a6979a7c3a68a6f5d84a21b533ce01a7850066fcfde5800d2d6ab |
| formulas.json | b369f337b38fd29c8d6c16b4fed6bf787069089c682c9c639c38224e161bf8d5 |
| samples.json | 69102fff332222f34684151e08a218fd92c6ae7a5153fd49d5900cf9e4b430d5 |
| matrices.npy | 48cdb08629a4b1a252c62de632b7cf82d97e8f7b554c93a14376ef7c93ba3989 |
| linear_trajectories.npy | 746dcdae9d9d3b8da334523f60de69150b8c49941f8ad256e3f60e56e0ebc4d4 |

matrices.npy has shape (120,5,7,7), in the order
Tred,Wred,Vred,Tred_dot,Wred_dot. linear_trajectories.npy has shape
(8,15,51), containing time, seven fields and seven velocities.
samples.json retains all roots, inertias, method matches, independent
Hessian errors, homogeneous checks, comparator controls and IVP statistics.
summary.json retains all individual checks, required holds and source pins.

All 75 unique direct/transitive scientific source pins match current
bytes without overlapping hash conflicts. Current executable and all
artifact sidecars also match. Runtime: Python 3.13.9, NumPy 2.4.6,
SymPy 1.14.0, SciPy 1.17.1. Nonmutating byte-identity replay uses

```text
C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B
 Scripts/itsm_context.py run --
 C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B
 Analysis/MasterTests/test_01_r4c1_g3_finite_k_scalar.py
 --output-dir Analysis/MasterTests/outputs/r4c1_g3k_attempt_02 --replay
```

The line breaks above are display wrapping; pass the arguments as a
single command. Existing result directories are refused for mutation.
Exact local command logs and supplemental integrity checks remain in
ignored .local/itsm-context; they are not publication artifacts.

## Disposition and inherited dependencies

Register R9-MT1-G3K. Inherit G3T/G3V/G3I/G3DF/G3D/G3F/G3A/G3E/G3Z/
G3S/G3, G2/G1/B1/S1/S2/S3/variation, applicable PD1 and Track-A
scientific/review debt. The separate G3V cross-check and G3N1 records
are preserved; this calculation does not absorb or supersede them.

Conditional; PROCEED_PROVISIONALLY; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Canonical Tests 1-3, physical scattering/cutoff and healthy GR remain
HOLD_SUBSTANTIVE. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
Review deferral permits bounded provisional research; it clears
neither physics failures nor required missing inputs.
