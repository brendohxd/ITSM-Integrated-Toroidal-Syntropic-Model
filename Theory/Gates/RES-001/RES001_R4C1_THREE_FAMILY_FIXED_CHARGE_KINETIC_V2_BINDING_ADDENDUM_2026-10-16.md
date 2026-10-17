# Fixed-charge kinetic V2: exact compact determinant binding

16 October 2026. Frozen before V2 execution.
Inherit the 15 October scope contract and 16 October V1 numerical addendum
without changing any domain, numerical criterion, field, ensemble or physics.

V1 source SHA-256:
9d7c58ac068aec7f3546c2e9a45ed91feabfd05baf6663e3953c93ca3ec7cbbb.
Attempt 01 was interrupted before receipts after about seven minutes.
Attempt 02 repeated the unchanged source with a private calculation-neutral
stack log, then was interrupted when the stack identified automatic
Matrix.det() simplification of the final mixed 2x2 Hessian as the bottleneck.
No scientific assertion failure or acceptance is inferred from either run.

V2 replaces only that determinant evaluation with the full exact identity

```text
h = -pd*sqrt(A*px^2-B*P_tau+D),
det Hessian_(px,P_tau)(h) = -pd^2*A*B^2/[4*(A*px^2-B*P_tau+D)^2].
```

Compute its two-by-two Hessian by differentiation and the determinant by
explicit multiplication/subtraction. Bind the radicand to the physical
homogeneous Hamiltonian using

```text
A = 3*K/(2*M),
B = 2*K*volume*C,
D = -K*(pR^2+pr^2)-2*K*volume^2*potential_and_angular_energy_density.
```

All spectator momenta/energy terms remain in D. This is an algebraic compression,
not their removal or a specialized background substitution. The final physical
determinant remains -3*pd^2*C^2*K/[8*M*(F_rest-C*P_tau)^2] on the positive
radicand branch. Verify both the generic identity and full radicand binding.

Retain every other V1 check, including the independently differentiated full
11-momentum Hessian, evolving polar/boundary calculation, 378 untouched saved
background nodes, nine finite full-Hessian controls and immutable replay.
Seal the new source and this addendum before executing into a fresh directory.

Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Full potential, physical stability/window, cutoff, GR and matching remain open.
The two ensembles and prior retarded warning are unchanged. No source/sidecar
replacement, provider change, publication, commit or push.
