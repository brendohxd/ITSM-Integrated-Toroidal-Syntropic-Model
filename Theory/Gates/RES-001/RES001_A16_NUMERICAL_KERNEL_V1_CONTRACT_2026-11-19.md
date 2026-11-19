# A16.2 validated numerical kernel contract V1

19 November 2026. High confirmed. Unchanged conditional original R4C1/B1.

Evaluate the actual retained and pressure kernels over 0<=s<=t<=1/20 for
ell=4,8,16,32,64, retaining the registered background, constraints, moving
maps, proper-rate conventions, momentum drift and hidden initial data.
Use the frozen 8+4 matrices from the finite-state/history owner.

Construct forward U(t)=U_h(t,0) and inverse V(t)=U_h(0,t) with their distinct
equations U_dot=D U and V_dot=-V D. Never replace the inverse with a transpose
or a frozen exponential. Validate their defects and background uncertainty
with explicit constants. Derivative identities establish V U=I exactly.

Represent the full two-time kernels by separable, piecewise polynomial factors:

    L=B U, R=V C, Lp=P_h U,
    K_ret(t,s)=L(t)R(s), K_pressure(t,s)=Lp(t)R(s).

Keep polynomial truncation, rounding, fundamental-matrix errors and all
background/observation-map errors. Acceptance requires a uniform absolute
induced-infinity error <1e-8 on the full time triangle, not only at samples.
Export reproducible exact dyadic polynomial coefficients and error budgets;
deterministic lossless compression is allowed. Do not archive only hashes.

Replay the existing radial seed's full twenty-state polynomials and verify
their chain, defects, amplitude and initial recipe against the prior certificate
before reusing its state error. Construct fresh retained-history, pressure and
retained-rate observations with their own bounds. Integrate the polynomial
convolution including all quadrature/truncation/rounding errors and hidden
initial forcing. Compare reconstructed pressure and retained rates throughout
the interval, requiring both absolute reconstruction errors and continuous
nominal differences from the reference to be <1e-8.

The supplied retained history is from the certified full coupled trajectory.
This tests numerical kernels and history reconstruction; independent
retained-only Volterra evolution is not certified by this comparison.

Controls include exact pressure-map recomposition, zero/inverse identities,
noncommuting propagator and right-inverse orientation tests, polynomial
integration with retained remainder, independent DOP853 kernel comparisons,
independent error-budget audit and fresh byte-identical replay. Preserve
all original inputs, hashes, sidecars, failed attempts and unrelated edits.
Use fresh receipt directories; scientific source/contract/manifest frozen
before execution. Update route A16.2 and the deferred-review register.

No thermal/dissipative interpretation, short-memory approximation, new
mechanism, healthy coupled-mode or nonlinear validity window, action change,
MAT/GR/acceleration matching, publication or canonical promotion follows.
physics_pass=false; gate_effect=NONE; Rule-9 DEFERRED. No provider dispatch,
bulk vault mutation, commit/push, deployment or paper/PDF edit.
