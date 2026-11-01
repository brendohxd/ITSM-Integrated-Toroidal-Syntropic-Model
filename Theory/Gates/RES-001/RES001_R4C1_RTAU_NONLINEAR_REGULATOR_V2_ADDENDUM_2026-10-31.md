# Nonlinear regulator V2: exact periodic boundary identity

V1 terminated with MemoryError in SymPy's general integration of the
derivative of exp(epsilon*f)*epsilon*k*g_theta. Its sealed executable and
private traceback remain preserved; no scientific receipt was produced.

V2 applies the fundamental theorem directly to that already-known flux:
F(2*pi)-F(0). Both fields are smooth periodic trigonometric functions, so
this is the exact same integral, not a numerical approximation or weakened
check. All actions, coefficients, remainder bounds and tolerances remain
unchanged. An additional zero-leading-force ray control retains its exact
higher-order residue rather than interpreting zero cubic order as no force.

The physical-density decomposition controls use independent local off-shell
jets with nonzero metric, frame, condensate and reservoir entries. Only the
force summand is compared between full and A=0 decompositions. Those jets
are not claimed to be an on-shell periodic solution. The separate analytic
regulator packet is periodic and retains its actual weighted mean flux.

Full lapse/shift/matter solve, constraint/principal persistence and canonical
coupled interactions remain incomplete. Review DEFERRED; physics_pass=false.
