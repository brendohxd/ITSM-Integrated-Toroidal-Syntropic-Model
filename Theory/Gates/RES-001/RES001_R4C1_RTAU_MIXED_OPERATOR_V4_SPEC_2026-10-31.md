# Mixed operator V4: original-density clock-gauge control

V3 reached the original-density point control and stopped at the existing
backend's dust-clock guard. The control wrapped tau_z=0 in a differentiation
node, even though the 48-slot pullback fixes that quantity and its Jacobian
row is identically zero. The backend correctly rejects that node as an
unfixed clock gradient. V4 leaves tau_z as its fixed primitive zero and
computes original derivatives for the other 55 slots. The unused tau_z
gradient slot is a zero placeholder, not a claimed covariant derivative.

Every unpulled derivative used by the 48-slot chain rule remains computed,
including independent lapse and lapse-gradient derivatives. No Jacobian
column, allowed metric/frame/force variation, acceptance threshold or
scientific equation changes. Preserve all three failed sources/records.
All full physical/symplectic/evolution holds remain.
