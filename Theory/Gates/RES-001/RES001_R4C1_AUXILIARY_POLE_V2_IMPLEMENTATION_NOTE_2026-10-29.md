# Auxiliary pole V2: canonicalize exact rational expressions before the node guard

29 October 2026. Under the unchanged AUXILIARY_POLE_V1_CONTRACT.
Conditional; review DEFERRED; physics_pass=false; gate_effect=NONE.

V1 is preserved with its source, digest and failed receipt:
Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v1_attempt_01/summary.json,
SHA256 c3b1eb0d99a7d46739e340d4c3678bf2c6947c973811958c88a635c97590b906.
77/78 checks passed. The failure is exactly
all_normalized_source_denominators_removable. V1 correctly retains its
auxiliary_partition_pole_certified=false result; no earlier claim is edited.

The guard inspected the raw representation of jpos(w)/w. Its denominator
at w=0 is zero before cancelling its exact common factor. Exact SymPy
cancellation gives denominator275520000 at the node and limit9/560000;
the original-minus-cancelled expression is identically zero. This is the
parent's already known scalar cusp quotient, not a new physical singularity.

V2 first cancels every normalized rational expression exactly, checks that
ALL original-minus-cancelled functions vanish, then applies the same nonzero
node-denominator guard. No equation, source term, radius, envelope, coefficient,
Cauchy majorant, tolerance or pole acceptance inequality is changed. V2 pins
the unchanged V1 source/failed receipt and this note and uses a fresh output
directory. Both versions and all historical sidecars remain immutable.

This implementation repair does not by itself establish a pole, physical
clearance or an exclusion of weak solutions. The complete V2 proof checks,
source identity, inherited bounds and immutable replay must separately pass.
