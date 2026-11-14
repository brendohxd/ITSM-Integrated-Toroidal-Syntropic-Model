# Generic material-block time derivative export

This implements the frozen normal-form time-drift contract, at confirmed
High. Only the ordinary principal subblocks needed by the registered cross
normal form are exported. The full action Hessian is not rerun.

## Structural independence before specialization

In the pinned unspecialized body, ADM K, frame B and canonical gu are linear
in first derivatives, with coefficients depending on q and N only. ADM,
frame, alignment and canonical kinetic sectors are quadratic in those
linear forms. The weak spatial-curvature density is quadratic in metric
gradients plus lapse-gradient times a linear metric-gradient flux. With
N=exp(-beta psi), Nz=-beta N psi_z, this remains degree two in derivatives.
Their second derivatives with respect to ordinary velocities, ordinary
gradients and shift gradients consequently depend on q only.

The potential and dust terms have no such derivative arguments. The
full nonlinear force depends on q, proper psi velocity and psi_z, but has
no ordinary velocity, ordinary gradient or shift-gradient argument. The
combined R-tau regulator likewise contains q, Z, Z_z, psi_z and Nz only.
Neither contributes to these selected ordinary principal blocks. This
is a sector-by-sector statement about the actual action, not an empirical
observation of small coefficient variations.

At a general scalar longitudinal shift S the unreduced principal blocks
obey, by the displayed material derivative in the weak action,

    A(S)=A0, B(S)=B0-S A0,
    Cshift(S)=C0, Dshift(S)=D0-S C0, Kshift(S)=K0.

Thus the material Schur coefficient B_R and Dshift+S Cshift are independent
of S. Their S_t contributions cancel before any derivative is dropped.
Evaluate the selected action subblocks at S=0 and any convenient ordinary
derivative values; the structural result makes their values and q-directional
time derivatives identical to the actual material coefficients.

Use generic metric/frame variables and the true registered q_t in an outer
first-time jet; seed only the nine ordinary velocities, nine ordinary
gradients and three shift gradients for second variation. Export A0,B0,C0,
D0,K0 and first time derivatives. Compare zero-shift values to the old raw
enclosures after their exact material correction; interval consistency is
not the proof of the identities above. Use the preserved inverse enclosures
and inverse derivative identities, rather than a new unproved inversion.

## Force and auxiliary coefficients

Compute mu, gamma and h^zz from the full metric before specializing.
Use the full force with independent proper p and s=psi_z. Its momentum is
pi_psi=mu f_p. In the ordinary slots,

    Tq_i=mu_i f_p+mu f_pqi,
    Qaux_i=-s (h^zz (log mu)_i+(h^zz)_i),
    aq_i=b N mu Qaux_i.

Retain the certified p_t, actual s_t and all q_t in their time jets, including
the metric, frame, scalar and lapse/volume variations. Generic coefficient
variation precedes evaluating the conformal initial metric and its known
conformal first tangent. No future conformality is imposed.

For the fixed ordinary complement, leading gradient map L, velocity V and
shift-gradient response W, the reverse block can be written

    B_fo,first=-kappa aphi Tq L+i Qaux V-i kappa s W_z
               -vphi Qaux L,
    B_fo,second=0.

Here W_z labels the longitudinal row of the shift-gradient response, not a
new spatial derivative. This expression follows from the full auxiliary
variation, clock Legendre identity and Qaux B_gauge=kappa s e_z. It agrees
with the earlier registered conformal-slice expression, but retains generic
metric derivatives for its time rate. The forward block is i aq in the
ordinary momentum rows. Differentiate both blocks and A_fast^-1 by exact
product rules. Keep the existing original-coordinate primitive fixed.

Acceptance: a finite numerical whole-initial-root C_t and T_t T^-1 bound,
all blocks identified with the preserved construction, independent inverse/
material/Legendre controls and omitted-rate rejection, fresh receipts and
exact replay. Missing or inconsistent evidence leaves the task incomplete.
No root-error-radius differentiation, higher-time-jet assertion, new action,
cutoff, external dispatch, vault mutation, publication or Git delivery.
H_t and the actual compatible evolution/time tube remain open.
R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
