# V3: retain arbitrary precision in integer-division adjoints

20 October 2026. Supplement the unchanged V1/V2 scientific contracts.

V2 returned 2922/2922 under its frozen checks. A subsequent independent
constant-division probe found that the reverse-mode rule's `1/z`, with integer
z, first creates a Python binary64 number. In particular x/17 differentiates
with an approximately 8.16e-19 absolute error instead of full mpmath precision.
Passing those checks therefore did not establish the intended 80/100-digit
derivative accuracy. Preserve V2, all its passing receipts and this limitation;
do not relabel it as a scientific rejection or silently rewrite its source.

V3 changes ONLY that reciprocal to `mp.mpf(1)/z`, adds an independent odd-
integer-division derivative check (<=1e-70 at 100 decimals), and updates source
pins to retain V2 source/contract/receipts. All other numerical function and
class-method ASTs must remain identical. Equations, initial recipes, charges,
two step sizes, 80/100-digit calculations, all54 registered grids, precision
agreement and scientific tolerances are unchanged. No target is inserted.

Freeze the versioned V3 source after AST comparison and before execution;
fresh attempt03, complete fresh read-only replay and external byte/size/mtime
guards. V1 remains the exact-replayed 833/880 failure. V2 remains the 2922/2922
passing first attempt with an identified derivative-precision limitation;
its full immutable replay is not claimed here. Do not repeat its expensive
run merely to demonstrate the already identified conversion.

The V2 stationary envelope remains a FIRST-DIFFERENTIAL evaluator, never a
physical Hessian or off-base evolution Hamiltonian. Passing the corrected
initial tests still leaves nodal hierarchy/admission, full descriptor
Hessian/background drift, function space, persistence, physical interaction/
frequency window and matching open. Rule9 DEFERRED; physics_pass=false;
gate_effect=NONE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED. No state adoption,
action change, model/provider/global-runtime change, vault mutation,
manuscript/site edit, publication, commit or push.
