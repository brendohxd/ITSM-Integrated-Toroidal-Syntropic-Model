# PKM1-P0 independent reproduction and mutation audit

**Calculation:** `PASS_INDEPENDENT_REPRODUCTION`
**Physics pass:** `false`
**Route:** `HOLD_PKM1_P0_B_STABILITY_FIRST_CONTROL_ONLY_P0_A_REJECTED`

The decisive results were reproduced without importing the primary script:

- P0-A's radial Hessian is
  `(2y^3+y^2-1)/(1+y+y^2+y^3)^2` and changes sign at
  `y=0.657298106138376`;
- P0-B has `J_Y=-1/(1+y)` and
  `J_Y+2YJ_YY=-1/(1+y)^2`;
- a direct Schur complement of the original `rho,N` action gives
  `M_P^2 K_QQ=rho^2 mu^2(1+4mu^2/M_rho^2)`;
- direct lapse/shift elimination gives
  `det K=(rho^2 mu^2+C_J q^2)/H^2`, including a positive strict-`q=0`
  determinant on the finite-charge branch.

Four claim-changing mutations were detected: replacing the khronon Hessian
with static ellipticity, reversing the sign of `J`, forcing `K_QQ=0`, and
deleting the finite charge at `q=0`.

All five files in the primary SHA-256 manifest match their recorded hashes.
This is an independent algebra/reproducibility pass, not a physics pass.
