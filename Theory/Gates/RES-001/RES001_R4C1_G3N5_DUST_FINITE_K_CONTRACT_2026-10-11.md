# G3N5: full finite-mode dust/slow comparison contract

Date: 11 October 2026 (Australia/Perth). Version 1; freeze before execution.
Conditional research; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.
Review DEFERRED. Operator authorization: the next bounded diagnostic after
the action-derived weighted-dust entry, not canonical promotion/publication.

## Frozen authority and domain

Reuse the unchanged 22-field R4C1/B1 quadratic action, dust clock, normalized
frame, all constraints and registered parameters. Owning weighted-dust report
SHA-256: da03bc19d9414f5b78f3c7bb6257e602f6721769a96b5268d885ba36ebf1f1ff.
Weighted-dust receipt SHA-256:
fe81f337ba6a7bd5a2783fc2e8a99b617ec08dd119673844f11edf30d53b1208.
Nonzero canonical receipt SHA-256:
610b8b58037d60c694093b045a55745df0f39858b829447ac18d7d2e2bf88020.

Use coordinate periods 2*pi; k=(ell,0,0), ell in {4,8,16,32,64}; retain
negative conjugate modes and both real quadratures. The fixed window is
t_E in [0,0.05], with 257 comparison times. Use the saved 70-digit degree-40
B1 background and slow transfer, evaluated in binary64 for the new numerical
IVPs. Register that rounding; do not call an old receipt-writing main.
Physical torus size, physical EFT cutoff and an observational cosmology are
not supplied. Retain all ten complex chart coordinates and twenty first-order
states; unexcited coordinates are initial data, not deletion of sectors.

## Derivation and registered initial data

1. Rebuild the generic positive-x chart from the frozen action and independent
   Euler export. Verify its E0,E1,E2 against saved A,R,K with background and
   volume derivatives retained. Reconstruct actual dust density/current and
   all auxiliaries, including Em and LambdaU, from those equations.
2. Let x=(y,y_dot). Derive its full linear generator L and actual observable
   O*x=(D,Vx), D=delta_rho/(i*p*rho_m), p=ell/a. The slow comparison generator
   is the already derived M=[[H,1],[6*rho_m/11,-H-2*psi_dot/5]].
3. Lift the saved formal slow fields to x through their explicit evolving
   maps and p_dot=-H*p. Call this 20x2 lift G, parameterized by (Vx,Vx_dot).
   Define the instantaneous observable-normalized diagnostic graph
   E=G*(O*G)^(-1). Check its rank and regularity. This is a choice of initial
   data and a diagnostic graph, NOT an imposed restriction during evolution.
4. Slow initial columns are E(0)*(1,0) and E(0)*(0,1), so both full and leading
   dust systems start with the same actual observables. Let Phi be the frozen
   leading weighted transfer; compare O*x_full against Phi for these columns.
5. Complementary probes use independent scaled Pi-position and Pi-velocity
   coordinate vectors. Subtract their E*O component at the initial time only,
   then normalize each in the declared balanced norm. They have initially
   zero actual dust signal. They are complementary seeds, not certified pure
   fast eigenmodes. Retain the complete subsequent evolution and report the
   dust signal they generate; do not call it spontaneous instability.

Use an explicitly invertible, time-dependent numerical balancing map B.
In the parent's SO(2) coordinates (h,TT+,TTx,Vx,Vy,Vz,du,dv,dr,Pi), its position
coordinates are (p*h,p*TT+,p*TTx,Vx,Vy,Vz,p*du,p*dv,p*dr,chi), where
chi=p^2*Pi-i*p*psi_dot*Vx. Its velocity coordinates are the time derivatives
of these positions divided respectively by (p,p,p,p,p,p,p,p,p,p^2).
Integrate z=B*x with L_z=(B_dot+B*L)*B^(-1). Retain B_dot. This norm is a
numerical/diagnostic mixed-order norm, not a canonical energy or a proved
full-system well-posedness norm. Do not hide the prior indefinite energy.

## Numerical controls and decision rules

Run DOP853 and Radau at rtol=1e-10, atol=1e-12, plus a refined DOP853 run at
rtol=2e-12, atol=2e-14. All must complete the fixed window. Use the full real
representation of complex matrices; sparse exact linear Jacobians may be
used. Require normalized balanced-state and dust-observable disagreements
<=2e-7, coefficient-background residual/agreement <=1e-10, analytic normalized
all-22 Euler residual <=1e-9 and initial observable matching <=1e-11.

Independently differentiate reconstructed full fields at T/4,T/2,3*T/4 with
the fixed fourth-order five-point first/second derivative stencils. Use
omega_control=1+p+sqrt(5/33)*p^2 at the initial point and
h=min(T/16,0.2/omega_control), then h/2. Require fine normalized all-22 Euler
residual <=1e-5 and refinement >=4, or both residuals <=1e-8. Report every
failure; do not change steps, tolerances or action based on the result.

For slow columns report the maximum induced infinity-norm discrepancy
e_ell=max_t ||O*x_full-Phi||_inf / max(1,max_t||Phi||_inf). Also report
observable equation defect (O_dot+O*L-M*O)*x, balanced distance from E*O*x,
complementary-seed dust transfer and all solver discrepancies.

The PREDECLARED finite-sample support criterion is e_64<=0.01,
e_64<=e_32, and e_8>=4*e_64. Record the boolean separately from software and
identity validation: a trustworthy negative comparison is still a completed
diagnostic. List the raw errors and ratios, not just its classification.
This operational criterion is not a theorem, physical cutoff, universal
asymptotic rate, arbitrary-initial-data bound or publication clearance.

Exact identities must vanish, optionally modulo the explicit B1 Friedmann
constraint where required by background on-shell redundancy. Verify negative
Fourier conjugation, both quadratures, complete reconstruction and balancing
generator. Reject an omitted p drift or B_dot if a required identity changes.

## Preservation and unchanged holds

Freeze this contract and the versioned executable with matching sidecars
before first execution. Verify inherited source pins and hash/size/mtime_ns
before and after. Fresh outputs refuse existing destinations; exact read-only
replay recomputes and byte-compares every new artifact and sidecar. Preserve
all historical failed receipts and the three inherited absent UVIR sidecars.
No action, old source, old sidecar, failure or threshold is overwritten.

The original K=-11/6, ordinary-wave Jordan defect, negative spatial trace
energy and indefinite density Hamiltonian remain recorded. Physical
stability/ghost/causality, a full finite-k uniform remainder estimate,
all-direction evolution, nonlinear source, healthy GR, G_eff/PPN and
microscopic/weak-field/coefficient matching remain unverified unless a
separate owning calculation establishes them.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Rule-9 DEFERRED is not clearance and does not alone block provisional research.
Only new research files and append-only owning queue/review entries are in
scope. No manuscript/PDF, vault/provider/runtime/model change, paid dispatch,
commit, push, deployment, submission or canonical promotion is authorized.
