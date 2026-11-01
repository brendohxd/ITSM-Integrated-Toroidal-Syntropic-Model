# Direct canonical-density time transport V1

Freeze before execution at acknowledged High. Continue current transport
V2 and the prepared-evolution contract, without changing the action.

On the auxiliary secondary surface split L=L_nonreg+L_reg. The density is

    I=L_nonreg-p*(v-Lie_S q)-partial_z B0-b*N*sqrt(h)*Z^2/2,
    B0=N*gamma*h^{iz}*p_Vi-N*curvature_flux/2,
    Z=-Delta_h psi.

The regulator expression follows by cancellation with the lapse improvement,
not by dropping its flux. For the time derivative use the exact Legendre
cancellation of accelerations:

    partial_t[L_nonreg-p*(v-Lie_S q)]
      =L_nonreg,q*v+L_nonreg,d*v_z-pdot*(v-Lie_S q)+p*Lie_S v.

Shift-time terms cancel locally; no physical Sdot=0 prescription is made.
Differentiate B0 in time and space with metric/frame canonical rates, and
differentiate the on-secondary regulator density with the reconstructed
Zdot. Obtain the first perturbation using the full action Hessian and
mixed time/tangent differentiation; no full action third variation or
unsupported spatial Zdot derivative is needed.

At z=0.3,1.1,2.4, use the inherited all-field canonical probe and explicit
fourth force derivative. Compare the direct graph density to the raw lapse
improvement, and its direct time/tangent rates to the explicit current.
Retain the finite-centre momentum defect:

    I_dot-partial_z(S*I+mathcalFz)=partial_z(N^2*h^{iz}*C_i),
    delta R=partial_z(N^2*h^{iz}*delta C_i+delta(N^2*h^{iz})*C_i).

Freeze tolerance1e-28. The earlier current V2 receipt must pass all46 checks.
Check paired current-density coordinate transport with the existing J,w;
reject deleting regulator density, lapse improvement or coordinate drift
when their discrepancy is nonzero. Do not assume point centres solve the
constraints exactly. Do not equate these local controls with a uniform
physical norm, a semigroup, finite-time persistence or action adoption.
Preserve all sources/failures, fresh receipt and exact immutable replay.
Review DEFERRED; physics_pass=false; goal incomplete; no publication/push.
