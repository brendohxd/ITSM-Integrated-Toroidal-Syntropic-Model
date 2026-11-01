# R-tau physical-norm execution specification V1

Frozen before the numerical/symbolic implementation for the physical-norm
contract. This is an ansatz to test, not a claim of a successful estimate.
Use the exact characteristics V3 receipt and its common old-B1 background.
No action or physical input is changed.

## Variables and proposed estimate

Use the local scalar helicity coordinates q=(Gamma,v_z,delta u,delta v,
delta r,delta psi), Gamma=(gamma_xx+gamma_yy)/2, and kappa=k/a.
The density delta rho is the NEW full lapse reconstruction. Reduce its
coefficients modulo the conserved Friedmann constraint only; never drop a
new perturbation constraint or impose a desired mode relation.

Test the twelve independent variables

    Y=(sigma,kappa*v_z,kappa*delta u,kappa*delta v,kappa*delta r,
       kappa^2*delta psi,Pi_Gamma,Pi_vz,Pi_u,Pi_v,Pi_r,delta psi_dot),
    sigma=delta rho+K_Q*p*(delta psi_dot+beta*p*delta psi), p=psi_dot.

The second term in sigma is the linear perturbation of the force sector's
timelike kinetic energy in the clock gauge. It cancels no mode: delta rho
must be recoverable. Pi=(q_dot+M_scalar^{-1}*B_scalar*q) for the first FIVE
scalar components; these are normalized canonical momenta from the action.
The force component uses its physical normal velocity instead. Justify and
check each distinction, actual invertibility and natural-norm equivalence.
Do not infer a numerical physical scale from the control's field units.

Compute G_Y=(T_dot+T*G)*T^{-1} on the actual background, including kappa_dot.
Extract A2=lim G_Y/kappa^2 and A1=lim (G_Y-kappa^2*A2)/kappa.
Preserve any unexpected higher powers, failed cancellations or instabilities.

Test a positive energy whose ordinary trace/frame part is built from

    D=Pi_Gamma-i*(kappa*v_z)/198,
    X=(kappa*v_z)+18*i*D,
    |D|^2+|X|^2/3+|Pi_vz|^2.

Use |sigma|^2, the canonical condensate spatial-gradient form, ordinary
reservoir gradient/velocity energies, and b*|kappa^2*delta psi|^2+
K_Q*|delta psi_dot|^2. These proposed coefficients must annihilate the
unbounded Hermitian parts exactly; otherwise preserve the failure. Do not
fit a norm to finite-mode eigenvalues after the test.

For each independently decoupled tensor/vector helicity use its actual
canonical momentum and squared speed derived from the action. Retain the
homogeneous mode separately, with all six metric amplitudes and both charge
levels, not the singular k=0 limit of T.

## Domain, constants, and controls

Try the explicit background box a in [1/2,2], rho in [1/20,2], and absolute
value at most 2 for H,u,v,r,u_dot,v_dot,r_dot,p,psi. Prove a short-time
background inclusion from the actual initial data by an explicit flow bound;
do not assume the whole proposed box lies on shell. Candidate target is
[0,1/200]; shorten with a documented reason if the bound requires it.

For kappa>=1/2 derive an explicit entrywise remainder bound from rational
coefficient majorants and positive denominators. Report constants even if
very loose. Prove coercivity, bounded reconstruction and an energy inequality
with actual coefficient drift, or preserve the precise obstruction. This is
a control-unit linear estimate, not a physical UV cutoff/window or nonlinear
Cauchy theorem. Do not extrapolate through density/clock/caustic/rank boundaries.

Independent controls: real/complex physical reconstruction at k=1,7,40;
exact generator conjugacy including T_dot; numerical actual-drift differences
at steps 1e-14 and 1e-22, 120 digits, normalized error <1000*step^2;
exact positive-form identities and failed omitted-drift control. Fresh
receipt, sealed source, immutable replay, input bytes/mtimes retained.
Preserve failed attempts in new versions; no weakened tolerance or action.

Review DEFERRED; physics_pass=false; gate_effect=NONE. All full physical
window, nonlinear admission, realistic matter, GR/local and matching holds
remain independent. Neither comparison action is adopted.
