# M4 actual causal metric response: shear-sign repair

5 November 2026. Supersedes the V1 source/kernel's shift-source sign and V1
causal response's shift reconstruction. Original files, hashes and receipts
remain preserved. Full M4 and its physical pole/residue requirement remain open.

## Independent failure and cause

The first causal-response executable produced 14/16 checks. Canonical/Euler
solvers agreed, but the isotropic-source traceless metric check failed on both
registered modes. This is a substantive convention error, not numerical noise,
a threshold to loosen, a new ghost or a defect of the parent theory.

The original parent raw quadratic action contains

    -2M Sigma R_dot+2MH alpha Sigma-rho_dot Sigma delta_rho.

Direct ADM extrinsic-curvature expansion and the amplitude spatial advection
term give the opposite signs for the actual shift divergence. Consequently

    Sigma_parent=-D_i N^i=-Delta beta/a^2=+q^2 beta.

The V1 source export assigned Sigma_parent=+D_i N^i. Correcting the metric
convention therefore requires BOTH

    matter source h=(-delta_e,-j/q^2), beta=+Sigma_parent/q^2.

The original parent action, internal quadratic blocks, Fourier conventions,
Ward equations, background parameters, pressure probe and all acceptance
thresholds are unchanged. In particular Phi=alpha+dot beta and Psi=-R-H beta
are unchanged. The corrected source is derived from the original metric
variation, not selected to make two solvers agree.

The two-constraint nonzero-mode block, actual one-constraint homogeneous
block and their distinction remain as in the preceding source report.
Only the new corrected source/response versions may be reused for physical
nonzero-mode forcing. The old V1 source sign and metric-response results are
HOLD_SUBSTANTIVE for that use. U5 and its local DOF result are unaffected.

## Exact response retained

All canonical A,B, retarded Green and observation-map derivations in the V1
response report remain, with H_r's j entry changed to -q^-2 and beta rows
changed to +q^-2 times the parent Sigma rows. Source contact, derivative source,
volume/time dependence and lapse/shift source dressing remain included.
Independent checks compare canonical DOP853 refinement with second-order
Euler RK45 AND the traceless metric equation, on the frozen conserved probe.
Numerical differences remain diagnostics, not rigorous continuum error bounds.

This is a causal finite-mode metric response of a declared EFT parent.
The physical pole/adiabatic window is not yet demonstrated; coefficient
evolution prevents treating a naive globally frozen Fourier kernel as the
actual response. J/a0 remain free inputs. No live Track-A V is computed.

V2 source preflight also records an indentation-generation error, preserved
before execution; V3 corrects that implementation detail without a change
to the scientific equations or controls. The paired source and response V3
executables are the usable versions. Verification records identify their
fresh receipt paths, results and immutable replays separately.

No old action or failed artifact overwritten. Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; full M4 INCOMPLETE. No provider/vault/publication/Git action.
