# R-tau norm V2: two-dimensional trace certificate correction

31 October 2026. V1 executable and 57/58 receipt remain frozen:
Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v1_attempt_01/summary.json,
SHA256 68cd6d2bc808ff9a5c4c3f1bd56bbdcebd3e950ff6791020019107add7b5586e.

The only failed check asked whether the TRACE OF ALL THREE coordinates of
H3 was below 110. H3 is a two-dimensional positive block plus the independent
unit Pi_vz coordinate. Its full trace is 4327993/39204, greater than 110;
the two-dimensional trace is 4288789/39204, less than 110. The independent
unit coordinate also has eigenvalue less than 110. Thus the original upper
bound 110 and lower bound 1/330 follow from the intended TWO-DIMENSIONAL
trace and determinant 1/3. No eigenvalue or physical branch is discarded.

V2 corrects that exact certificate's matrix slice, records both traces and
preserves the threshold 110. The energy form, variables, actual operator,
background/time/momentum domains, remainder bounds, norm-equivalence bounds,
growth constants and all numerical tolerances are unchanged. Compare the
scientific exports between V1 and V2 explicitly. This is not a physical
failure repaired by weakening an acceptance criterion.

The independent conformal homogeneous sign is not involved in this correction.
All substantive nonlinear/window/matching and unadopted-parent boundaries
remain. Review DEFERRED; physics_pass=false; gate_effect=NONE.
