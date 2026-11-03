# Prepared initial coefficient calculation V1 specification

Frozen after owner inspection, before executing the new inequalities.
Use epsilon=1/1000, r=epsilon/13, lambda=r cos z,
L=lambda_t=H+epsilon cos(2z)/31. H is its stored exact binary numerical centre
plus/minus the certified 1139/100000000 correction. No decimal centre rounding.
The prescribed metric is h=exp(2lambda)I and h_t=2Lh at this instant only.

Original-coordinate coefficients:

    a=exp(-2lambda), b=a lambda_z,
    a_z=-2a lambda_z, a_zz=a(4lambda_z^2-2lambda_zz),
    b_z=a(lambda_zz-2lambda_z^2),
    a_t=-2La, b_t=a(L_z-2Llambda_z).

Set E=exp(2r), M=max|H|+epsilon/31 and D=2epsilon/31. Whole-circle bounds:
a0<=E, a1<=2Er, a2<=E(4r^2+2r), b0<=Er, b1<=E(r+2r^2),
at0<=2EM, bt0<=E(D+2Mr). Thus K_v<=E(1+8r+6r^2).

Prepared coordinate: retain Abar=<exp(lambda)>, J=exp(lambda)/Abar,
m=H+epsilon R2/31, w_z=L-m-lambda_z w. Read certified J_lower, w_upper and
w_z_upper from the existing gauge receipt. Abar is not assigned 1: averaging
exp(lambda)>=1+lambda gives 1<=Abar<=exp(r), hence exp(-2r)<=Abar^-2<=1.

    a_new=Abar^-2, a_new,zeta=a_new,zeta,zeta=0 initially,
    b_new=2 a_new lambda_z/J,
    b_new,zeta=2 a_new(lambda_zz-lambda_z^2)/J^2,
    a_new,t=-2m a_new,
    b_new,t=2 a_new/J*(L_z-w_z lambda_z-w lambda_zz-2m lambda_z).

These time formulas follow from the actual transformed diagonal metric and
velocity; they do not differentiate an assumed invariant conformal family.
With certified j=J_lower,W=sup|w|,P=sup|w_z|, bound |m|<=M and
b0_new<=2r/j, b1_new<=2(r+r^2)/j^2, at0_new<=2M,
bt0_new<=2/j*(D+Pr+Wr+2Mr), K_v_new<=1+2r/j+2(r+r^2)/j^2.

Record volume bounds original [exp(-3r),exp(3r)] and prepared
[exp(-2r),exp(3r)]. They prove L2 measure comparisons, not full physical H2
or weak symplectic equivalence. General metric velocity perturbations, evolving
maps and coefficient persistence remain separate, unproved requirements.

Use 60-digit outward mpmath intervals; export exact interval endpoints for
all upper bounds. Independent exact controls use the previously validated
full-metric auxiliary implementation on rational smooth metric/velocity jets
and compare a_t,b_t with the formulas above. In the prepared fixture require
nonzero w and w_z and reject omitting their transport terms or m. Rational
fixtures validate identities, not the analytic whole-circle/root-ball bound.
Acceptance requires both identities and finite positive certified constants,
then immutable replay and unchanged inherited input hashes. No arbitrary
acceptance cutoff on constant magnitude is imposed. No finite-time estimate,
coupled norm or physical clearance follows from initial coefficients alone.
