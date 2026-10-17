# Coupled cusp tail V2: complex kinetic reduction correction

17 October 2026. Frozen before V2 execution. Unchanged action, families,
backgrounds, 27 source rows, constraints, mean preparation and V1 acceptance.
Conditional; review DEFERRED, physics_pass=false, gate_effect=NONE.

V1 source SHA 86d554486d6d88beebbfa9ef2fd7b8da72c366ad11443440541c91153b48a07d
and failed attempt01 summary SHA
cf7c7ecfb63ddf738833b7392b57074edf40c5047b30710c10d134063619692a remain unchanged.
The first case stopped at the complete acceleration identity, with residual
-78961/1152 in flattened entries 0,2,20,22. Local outcome 13/17; no accepted
coupled bound or physical conclusion followed.

The new implementation incorrectly used V.T in its kinetic Schur complement.
For the complex Fourier constraint map, the action requires

~~~text
K = F^dagger LK F - V^dagger D_inverse V,  V=U^dagger LB F.
~~~

F and U in this chart are real, but V contains imaginary spatial coefficients.
V2 corrects the conjugation, and explicitly checks Hermiticity and a nonzero
wrong-transpose rejection witness in the nonzero sector. It does not repair
or change the parent generic action or independent numeric reducer.

Inherit all V1 requirements. Keep every tolerance, source, background box,
mode, failed result and field. No parameter fit, wave projection, branch
deletion, softened check or scientific status change is authorized. V2 has
its own frozen source, fresh attempt02 directory, pins, report and immutable
replay. A subsequent obstruction must remain explicit and block dependent use.
