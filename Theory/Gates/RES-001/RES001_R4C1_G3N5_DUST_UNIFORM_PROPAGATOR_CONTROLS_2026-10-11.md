# G3N5 uniform propagator: numerical controls before receipt execution

Date: 11 October 2026. Version 1. Supplements the oscillatory-bound contract.
The exact normal-form construction was inspected in private exploratory files;
no fresh physical prediction, blind derivation or independent review is claimed.

Use C=diag(1,...,p at index 13,...,1), retaining C_dot; all other positions
are the old balanced 20-state coordinates. The fast transformation is
T_f=I+U/ell with U^3=g U, g=-22 a^2/375. Its exact inverse is
I-U/[ell(1-g/ell^2)]+U^2/[ell^2(1-g/ell^2)]. The wave transformation T_w
and positive evolution metric Q are exported in the fresh receipt.

Prove the complete transformed generator, both Q-skew principal blocks,
the inverse identities and positivity on the whole declared domain. Bound
the exact residual with rational interval arithmetic, including Q_dot and
all coordinate derivatives. No sampled maximum supplies the bound constant.
The uniform bound is for ell>=4, not a physical EFT momentum cutoff.

The improved background enclosure uses the unchanged registered initial
u=r=1, u_dot=r_dot=v=v_dot=0. The ODE preserves v=v_dot=0, while perturbations
in both complex scalar directions are retained. On the existing positive-H
short interval, u_dot and r_dot stay nonpositive. Set
F_u=1+1/6+1/80+3/14 and F_r=33/14. Then
1-F_u*T^2/2<=u<=1, -F_u*T<=u_dot<=0,
1-F_r*T^2/2<=r<=1, -F_r*T<=r_dot<=0, T=1/20.
These enclosures follow from the damped equations and positivity bootstrap;
they are not adjustments to the actual background or observed extrema.
Retain the earlier certified a,H,psi_dot,rho_m,C enclosures.

Controls retain all five archived modes, all four columns and 22 reconstructed
fields. Check each archived column's transformed Q-norm amplification against
the analytic exp(mu*t/2) bound, allowing 1e-9 for binary64 archive evaluation
only. Exact symbolic generator reconstruction is mandatory; additionally
check direct versus factored numeric generator at t=0,1/40,1/20 with normalized
residual <=1e-9. These are numerical controls, not the analytic proof.
Check positive definiteness, archive domain membership, negative-mode conjugate
energy equality and all inverse reconstructions with the existing 1e-9 limit.
Do not delete any state, project evolution, overwrite an archive, or impose
the leading dust flow on the full generator.

Outputs: formulas.json, diagnostics.json, summary.json, with new sidecars and
exact read-only replay. A successful propagator certificate alone does not
prove the prepared dust error's order. Report that remainder as OPEN unless
its retained forcing, initial mismatch and observable error are controlled.
Retain physics_pass=false, gate_effect=NONE and deferred review and parent holds.
