# G3N5: coupled constraint-compatible linear IVP on a registered formal T3 domain

Date: 10 October 2026. Version 1; frozen before execution.
Approved bounded goal; Conditional; physics_pass=false; gate_effect=NONE;
review DEFERRED. This is not full nonlinear Master-Test-1 closure.

## Immutable inputs and actual scope

Use full v2 kernel summary 560e369d7795ed8e06d0c2c26350d3b412a53c577da82f0669e68f6ee04f5666,
independent comparison summary 2fb997e71b2fe24cc3aa8e458a26663c65165bcba068b3a12e40aedaae11d261,
B1 source 1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f,
and the previously checked 22-field background-matching inputs. Preserve all
transitive pins, sidecars, known absences and failed original G3/N3 attempts.

Compute the response to constraint-compatible initial perturbations under
the unchanged action, with no additional forcing or altered coupling.
All 22 unreduced equations remain the residual reference. Retain all x/y/z
derivatives before specializing to Fourier vectors. At Y=0 the nonanalytic
force has zero linear kernel; its retained unsmoothed second-order forcing
and infinite harmonic tail are not solved or removed by this linear IVP.

## Background, time and mode domain

Use precisely B1's MP2=1, MU2=2/3, c1=1/5, c2=1/10, c3=-1/5, c4=1/20,
K_Q=3, A=2/7, b=5/11, zeta=1/13, beta=2/5, g_r=3/7, m2=1,
lambda4=1/3, lambda6=1/5, Lambda=2, mr2=2, lambda_r=1/7, rho_Lambda=0.
Use its original initial data and positive H fixed only at t=0 by Friedmann.
No H reprojection or parameter retuning. Evolve the background only to supply
continuous coefficients for this new IVP and compare with retained B1 data.

Domain: t_E in [0,0.05]; coordinate periods 2*pi; integer mode vectors
(0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,2,3). Nonzero real fields include
the conjugate negative mode. This is a dimensionless formal benchmark, not a
physical torus size, action-derived EFT band or cosmological calibration.

## Gauge, auxiliaries and singular domains

Derive the active minus-Lie gauge transformations from the background:

```text
delta alpha=-chi_dot; delta S_i=partial_i chi/a-a xi_i_dot
delta M_ij=-2H chi delta_ij-partial_i xi_j-partial_j xi_i
delta V_i=partial_i chi/a
delta(du,dv,dr,Pi,T)=-(u_dot,v_dot,r_dot,psi_dot,C)*chi
delta Em=-epsilon_dot*chi; delta LambdaU=-lambda_dot*chi
delta nu=delta Z=0.
```

Check all 22 Euler equations on all four gauge families, including derivatives
of background coefficients. Exact initial checks use H0^2=3469/4620; numerical
checks use registered B1 points. Compare the Fourier Euler matrices directly
with those reconstructed from the full quadratic action and its a^3 measure.

Use T=0 only for C>0; E_Em then fixes alpha=-beta Pi. Retain E_LambdaU to
fix nu=0 and E_nu to recover LambdaU. Recover Em from E_alpha, and verify
its evolution in E_T rather than dropping the dust equation. For k!=0 use
k_i M_ij=0 as the spatial gauge. Eliminate shifts and Z only on invertible
auxiliary blocks; compare action-Schur and unreduced-Euler reductions.

The expected shift block is (k^2/a^2)[(MP2-MU2(c1+c3))*P_T/2
-MU2(c1+c2+c3)*P_L], with the Z block b. Record every inverse domain.
At k=0 do not divide by k: fix homogeneous shifts by translations, retain
all six metric components and solve Z=0 separately. Record the zero-mode
rank change and algebraic b=0, MU2=0, c1+c2+c3=0 and tensor-coefficient-zero
boundaries without claiming continuation or rejecting the entire action.
Coordinate counts and kinetic inertia are not a global physical DOF/stability proof.

## Frozen initial data and numerical acceptance

Let epsilon=1e-6 and N the reduced-coordinate count. For nonzero modes,
y_j=epsilon*((j+1)+i*(-1)^j)/(N+1) and
y_dot_j=epsilon*((-1)^j*(j+1)-i)/(N+1). Use real parts for k=0.
Recover every auxiliary from its equation. For the homogeneous mode adjust
only dv_dot initially so the linearized total U(1) charge variation is zero;
check that it stays zero. This is not nonlinear fixed-charge reduction.

- Exact checks: action/Euler equivalence, all initial gauge residuals,
  auxiliary block/inverse identities, and action/Euler reduced equations.
- Sampled gauge/operator residuals <=1e-10 after coefficient-scale normalization;
  a,C,rho_m>0 and reduced acceleration matrix condition number <1e10.
- Background/source-rate agreement and Friedmann residual <=1e-10; retained
  B1 coefficient-trajectory agreement <=1e-9; never rewrite B1 outputs.
- Response solvers DOP853 and Radau: rtol=1e-10, atol=1e-17; normalized
  solution discrepancy <=1e-7, scaled by max(epsilon, solution magnitudes).
- All 22 reconstructed analytic Euler residuals <=1e-9, normalized by the
  sum of separate operator-term norms with floor 1e-20, not by an additive 1.
- Independent five-point first/second differences on 65/129/257 samples:
  finest full-Euler normalized residual <=1e-5 and coarse/fine improvement >=4,
  unless both <=1e-10. Exclude two boundary samples per side.
- Homogeneous linearized charge drift/epsilon <=1e-8. Preserve the negative
  as well as positive kinetic eigenvalues; do not select a healthy-looking subset.

These are new diagnostic criteria, not replacements for any earlier failed
threshold. Preserve immutable outputs and exact read-only replay. A failed
assertion or missing input does not complete the goal merely by being reported.
Only a verified mathematical obstruction to the specified response may serve
as the approved alternative disposition; software failures cannot do so.

## Nonclaims and inherited holds

No nonlinear response, physical cutoff, global hyperbolicity, physical Hessian,
healthy continuous GR, weak-field matching or a0(z) follows automatically.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
Rule-9 DEFERRED, not cleared. No original source/receipt/frozen sidecar/action/
threshold, manuscript, PDF, vault, provider or runtime setting is changed.
No commit, push, upload or publication is included.
