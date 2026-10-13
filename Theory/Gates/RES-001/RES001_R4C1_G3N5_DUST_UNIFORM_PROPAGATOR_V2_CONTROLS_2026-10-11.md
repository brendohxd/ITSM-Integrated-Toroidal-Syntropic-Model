# G3N5 uniform propagator v2: correct rotating background

Date: 11 October 2026. Frozen before v2 execution. Supplements the original
oscillatory-bound contract without altering any original source or receipt.

Attempt 01 is FAILED, 67/72: all five background-box checks fail. Its
zero-background-velocity enclosure is incompatible with the registered
v_dot(0)=1 and r_dot(0)=1/4 and conserved angular charge J=1. The displayed
2.80 amplification bound and affirmative proof flag in that FAILED receipt
are not evidence for the actual B1 trajectory. Do not provisionally reuse
that bound. The original source, controls, outputs and sidecars stay intact.

V2 may reuse the general, unspecialized exact maps from attempt 01 ONLY
after independently checking the full 20-state transformed generator,
inverses and Q-skew identities again. The five failed checks were downstream
of the general map export. No initial data, action or parameter changes.
Do not set v or v_dot to zero in the new estimate or its derivatives.

Verify the saved initial state against
(a,u,u_dot,v,v_dot,r,r_dot,psi_dot,rho_m,C)=(1,1,0,0,1,1,1/4,1/5,1/5,1).
H0^2=3469/4620, E0=3469/1400 and J=a^3(u v_dot-v u_dot)=1.

Retain the earlier certified a,H,psi_dot,rho_m,C bounds on T=1/20.
Let r_max=1+T/4, s_max=1+T^2,
F=1+s_max/6+s_max^2/80+3*r_max^2/14,
F_r=r_max*(2+r_max^2/7+3*s_max/14).
Bootstrap the damped polynomial equations to certify
1-F*T^2/2<=u<=1, -F*T<=u_dot<=0,
0<=v<=T, 1-(3+T*F)*T<=v_dot<=1,
1<=r<=r_max, 1/4-(3/4+F_r)*T<=r_dot<=1/4.
Check that the lower velocity bounds remain positive. These inequalities
prevent first exit from the bootstrap box; they are not sampled fits.
Retain all complex scalar perturbations and the nonzero angular charge.

Q contains the full 2x2 complex-scalar block I+[(v,-u)^T(v,-u)]/13.
For the energy estimate use a fixed diagonal lower metric D: all entries 1
except D00=1/3, D44=D55=4/5, D99=5/33. Prove Q>=D>0.
Bound the Hermitian energy derivative with D^(-1/2) rather than incorrectly
treating Q as diagonal. Its rational interval row bounds give E_dot<=mu E
when mu>=0; no inferred physical Hamiltonian positivity follows.

Keep the v1 predeclared 1e-9 generator/inverse/energy and 1e-10 field/domain
control thresholds, all five modes, all four columns and all 22 fields.
Fresh receipts and exact read-only replay are mandatory. V1 failure remains
visible in the new receipt and report. The prepared dust remainder/order,
physical EFT domain, canonical parent holds and deferred review remain open.
