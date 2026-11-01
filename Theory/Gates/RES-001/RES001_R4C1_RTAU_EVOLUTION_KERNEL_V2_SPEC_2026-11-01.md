# Evolution composition V2 — sparse zero derivative handling

Routine implementation correction under the physical-norm V1 contract;
the new physical-norm derivation remains NOT_STARTED.

V1's all-field composition reached the pure-shift integration probe, where
the direct density helper indexed reg.g[1] although its first configuration
tangent is exactly zero. Sparse Second derivatives omit zero entries.
Preserve the V1 module, driver and new failure record. No completed V1
integration receipt or scientific physical-domain result is claimed.

Density-time helper V2 uses J(0) for absent sparse derivative entries in
all returned time/mixed derivative values, including reg.g[1]. The kernel
V2 selects that helper. No equation, nonzero derivative, input or tolerance
changes. Earlier general nonzero-tangent density V1 results remain intact;
they did not exercise this absent-entry branch.

Retain the independent frozen general-probe density/current comparison and
pure canonical shift/dual-density response at1e-28. Add the zero canonical
direction as a necessary linear-operator boundary check. Exact replay and
source preservation remain required. Do not claim a global compatible
domain, physical norm or finite-time evolution from this implementation.
Review DEFERRED; physics_pass=false; R-tau unadopted; goal incomplete.
