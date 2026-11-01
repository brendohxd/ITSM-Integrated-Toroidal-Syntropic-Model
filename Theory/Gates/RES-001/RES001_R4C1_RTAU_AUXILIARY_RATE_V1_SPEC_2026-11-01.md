# Prepared auxiliary spatial/time closure V1

High confirmed; freeze before execution under prepared evolution V1.
For arbitrary positive spatial metric define
C=hInv_zz*tr(hInv*h_z)/2-(hInv*h_z*hInv)_zz and
Delta psi=hInv_zz*psi_zz+C*psi_z. Retain all six metric components.
Return Z and delta Z through second spatial order and the VALUE of Zdot
and delta Zdot. Inputs include explicit background/perturbed psi fourth
derivatives, metric third jets and field-rate second jets. Missing higher
time-spatial jets are not returned as physical zero values.

Compute mixed field/time differentiation with the frozen second-variation
algebra. Independently check the time row using hInv_dot=-hInv*hdot*hInv
and its metric coefficient derivatives. Use symmetric tangent steps1e-12
and1e-16 with tolerances1e-20 and1e-28. Compare the actual prepared Z and
its first time tangent with their owning profiles at1e-28. Reject omissions
of metric-time terms and psi_dot,zz. These are caller-supplied canonical
rate controls, not a completed gauge/current or physical evolution solve.
Fresh receipts, exact replay and original hashes are required. Review
DEFERRED; physics_pass=false; full evolution and physical norm remain open.
