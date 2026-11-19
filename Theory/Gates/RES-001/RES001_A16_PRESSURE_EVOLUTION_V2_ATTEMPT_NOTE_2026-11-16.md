# A16.2 pressure evolution V2 failed control

16 November 2026. Completed 83/88 checks. The only five failures were
negative_seed_symmetry, one per mode. IV.center floors the dyadic midpoint;
rounding is not odd, so opposite trajectories need not have identical point
centers, amplitudes or defect bounds. The scientific trajectory, pressure
error inequalities and independent original-chart ODE comparisons all passed.
V2 remains a failed receipt and must not be relabeled PASS. V3 retains the
propagation and certifies the sign-reversed endpoint discrepancy using the
sum of the actual defects and an outward Gronwall bound, rather than exact
point equality. Preserve all V2 files and sidecars.
