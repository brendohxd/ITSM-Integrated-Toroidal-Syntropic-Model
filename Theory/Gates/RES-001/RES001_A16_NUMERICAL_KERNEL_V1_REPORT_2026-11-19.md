# A16.2: validated two-time kernels and pressure/history reconstruction

19 November 2026. High confirmed. Conditional unchanged original R4C1/B1.
Disposition: COMPLETE_SCOPED_NUMERICAL_KERNEL_AND_HISTORY_RECONSTRUCTION.
The wider A16.2 physical/reduction route remains OPEN.
physics_pass=false; gate_effect=NONE; Rule-9 review DEFERRED.

## Result and significance

The actual time-dependent retained and pressure kernels are now numerically
represented with uniform errors over 0<=s<=t<=0.05, for ell=4,8,16,32,64.
Using the certified full retained history, their integrals reproduce both the
combined scalar pressure and the eight retained-variable rates throughout
the interval. Hidden initial data and feedback are both included.

For the registered radial-rate seed, most endpoint pressure comes from the
evolving hidden initial state. Feedback is smaller but nonzero. Thus the
previous response can be accounted for by the existing coupled scalar state
and its causal history representation. This is not evidence for an additional
force, an irreversible bath, a new entropy law or a Campbell mechanism.

This is a reconstruction with a supplied retained history, not independent
retained-only Volterra evolution. That distinction is the next computational
test. No useful instantaneous approximation or short-memory limit follows.

## Calculation and error control

Use the frozen 8+4 split and actual matrices from the
[finite-state/history owner](RES001_A16_FINITE_STATE_HISTORY_V3_REPORT_2026-11-16.md):

    R_dot=A R+B h, h_dot=C R+D h, P=P_R R+P_h h.

The four hidden entries remain (delta u,delta v,proper_u_rate/p,
proper_v_rate/p), p=ell/a. R contains the area, longitudinal frame, reservoir,
force and their declared coordinate/proper rates. The original twenty-state
generator, reconstructed constraints, moving maps, rotating background and
momentum drift are retained. R-tau is separate and unadopted.

Compute U(t)=U_h(t,0) and V(t)=U_h(0,t) from

    U_dot=D U, V_dot=-V D, U(0)=V(0)=I.

Their derivative identity proves V U=I. No frozen exponential, transposed
forward propagator or numerically assumed inverse replaces V. The factors

    L(t)=B(t)U(t), Rh(t)=V(t)C(t), Lp(t)=P_h(t)U(t)

give K_R(t,s)=L(t)Rh(s) and K_P(t,s)=Lp(t)Rh(s). Fresh defect/background
bounds control U and V, and the factor-product error controls every point
of the full time triangle. Samples are additional controls, not the proof.

The original full radial-seed polynomials were reproduced exactly: initial
recipe, full coefficient-hash chain, maximum defect and amplitude all match
the earlier pressure certificate. Only after that match was its state error
reused. Fresh retained, pressure and retained-rate observations have their
own coefficient/background/rounding bounds.

The memory integral is evaluated tile by tile with indefinite polynomial
integration, including carried prefix intervals, highest-degree terms,
model remainders and rounding. The numerical memory law is

    I(t)=integral_0^t Rh(s)R(s) ds,
    P(t)=P_R(t)R(t)+Lp(t)[h0+I(t)],
    R_dot(t)=A(t)R(t)+L(t)[h0+I(t)].

No evolution is continually projected onto a desired graph. For this linear
seed R(0)=0 and h0=(0,0,1/ell,0). The supplied R history is obtained from
the full twenty-state evolution, not an independently evolved reduced model.

All numbers use the parent's registered formal units, fixed background and
unit radial-rate perturbation normalization. The following are conservative
continuous numerical-error displays, rounded upward:

| ell | Retained-kernel error | Pressure-kernel error | Reconstructed pressure error | Reconstructed retained-rate error |
| --- | ---: | ---: | ---: | ---: |
| 4 | <3.26e-37 | <6.35e-38 | <4.64e-36 | <6.16e-35 |
| 8 | <3.48e-37 | <5.88e-38 | <1.85e-35 | <1.41e-33 |
| 16 | <5.41e-37 | <8.72e-38 | <2.49e-34 | <2.65e-31 |
| 32 | <1.93e-36 | <3.06e-37 | <4.13e-33 | <5.91e-29 |
| 64 | <2.58e-35 | <4.09e-36 | <8.22e-32 | <1.42e-26 |

Every error passes the frozen absolute threshold 1e-8. Continuous nominal
pressure and rate differences from the reference are below 4e-43 and 4e-42,
respectively. These are numerical properties of fixed conditional equations,
not experimental uncertainties or precision of the underlying physical model.
The [error argument](RES001_A16_NUMERICAL_KERNEL_ERROR_ARGUMENT_V1_2026-11-19.md)
states the norms, factor inequalities and complete reconstruction error budget.

## What supplies the endpoint pressure?

An independent interval decomposition at t=0.05 gives the following rounded
real Fourier coefficients. Exact rational intervals are in the audit receipt.

| ell | Total pressure | Direct retained contribution | Hidden initial-state contribution | History feedback contribution |
| --- | ---: | ---: | ---: | ---: |
| 4 | -0.12140444 | -0.00003419 | -0.12192615 | +0.00055590 |
| 8 | -0.11670015 | -0.00003338 | -0.11721272 | +0.00054595 |
| 16 | -0.09870212 | -0.00003025 | -0.09917913 | +0.00050726 |
| 32 | -0.03881950 | -0.00001922 | -0.03916979 | +0.00036951 |
| 64 | +0.06056458 | +0.00000607 | +0.06052505 | +0.00003347 |

The endpoint feedback contribution is about 0.06--0.95 percent of the total
pressure magnitude across these five cases. This is not a uniform relative
error estimate: the ell=64 pressure crosses zero, and deleting terms would
also change an independently evolved retained trajectory. No small-feedback
or memoryless model is certified here. The positive ell=64 endpoint is already
present in its hidden initial-state term; feedback is not its sole source.
These signs refer to Fourier coefficients in the selected phase/chart, not
pressure everywhere in physical space or total cosmological pressure.

## Verification and reproducible artifacts

The main calculation passes 115/115 controls. Its independent audit passes
217/217 using exact rational box arithmetic, separately reconstructed field
maps/background derivatives, explicit exponential tail inequalities, lossless
archive checks and endpoint interval decomposition. It does not import the
production numerical solver or its dyadic arithmetic implementation.
These are same-assistant computational checks, not independent peer review.

Independent DOP853 evolution of the actual background and forward/right-inverse
fundamentals checks 45 retarded time pairs per mode. Worst kernel-entry
disagreement is <5.69e-13; the sampled U V identity residual is <2.23e-16.
Those floating-point comparisons do not establish the continuous bounds.

The main package and audit replay byte-identically, including all five curve
archives, mode receipts, global receipts and sidecars. All 26 final artifact/
preservation checks pass. All 721 original source hashes and their main-run
pre/post timestamps remain unchanged. Five mode calculations ran as local
processes; no model/provider dispatch or runtime reconfiguration occurred.

Each ell directory contains curves.json.gz: deterministic gzip (mtime=0)
of exact nominal polynomial coefficients, not just their hashes. At local
tile coordinate tau=(t-tile*T/steps)/(T/steps), evaluate each real/imaginary
coefficient list as sum(integer_n*tau^n)/dyadic_scale. The factor arrays L,
Rh and Lp reproduce the nominal kernels by matrix multiplication at t and s;
the global induced-infinity errors are in each receipt. Reference and memory
response curves are also retained. The five compressed archives total about
13.19 MiB. Lossless coefficients and sealed errors allow evaluation away from
the diagnostic sample grid without rerunning the differential equations.

The first independent-audit attempt stopped because its rational evaluator
lacked a constant sqrt(2) branch used by the existing balancing map. V2 adds
320-bit rational root enclosures checked by exact integer-square inequalities.
The main computation and its equations were unchanged. The failed source,
manifest and private-log identification are preserved in the
[attempt note](RES001_A16_NUMERICAL_KERNEL_AUDIT_V1_ATTEMPT_NOTE_2026-11-19.md).

- [Frozen contract](RES001_A16_NUMERICAL_KERNEL_V1_CONTRACT_2026-11-19.md).
- [721-input manifest](RES001_A16_NUMERICAL_KERNEL_V1_INPUTS_2026-11-19.json).
- [Main executable](../../../Analysis/MasterTests/test_a16_numerical_kernel_v1.py).
- [Main receipt](../../../Analysis/MasterTests/outputs/a16_numerical_kernel_v1_20261119/receipt.json), SHA256 `4065e4d716b767c63b7866830d576469ca3a1ff5f386f14f6ee69c8a6c0b462d`.
- [Independent audit](../../../Analysis/MasterTests/outputs/a16_numerical_kernel_audit_v2_20261119/receipt.json), SHA256 `8f6fc1725a9bc2cb8f9e69b0c1f308b3ca73400c73f662ed776c022c36e4a83f`.
- [Replay verification](../../../Analysis/MasterTests/outputs/a16_numerical_kernel_v1_verification_20261119/receipt.json).

Next: independently evolve the eight retained variables with the validated
Volterra operator and hidden initial forcing, prove its quadrature/evolution
error and compare the full coupled response. Only then assess useful reduced
approximations over the registered domain, retaining zero crossings and
separate absolute/relative errors. A16.5 time-scale separation remains open.

Physical-health, nonlinear/interacting-window, thermodynamic-state, organizing-
mechanism and matching obligations remain with their live owners. No MAT/GR
clearance, acceleration prediction or publication promotion follows. No paper,
PDF, site, external review, bulk vault sync, commit, push or deployment changed.
