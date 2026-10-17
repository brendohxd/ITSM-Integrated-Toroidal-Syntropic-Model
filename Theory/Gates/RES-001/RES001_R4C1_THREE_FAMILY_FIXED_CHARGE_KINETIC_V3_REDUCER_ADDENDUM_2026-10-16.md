# Fixed-charge kinetic V3: complete Friedmann polynomial reduction

16 October 2026. Frozen before V3 execution.
Inherit V1 scope/numerical criteria and V2 compact determinant binding unchanged.
V2 completed 79/80 exact/local checks. Its numerical controls were correctly
skipped after the independent inverse-Hessian identity failed. Keep its source,
receipts and sidecars untouched; no V2 acceptance is claimed.

All four nonzero residuals of that check contain the exact factor

```text
6*M*H^2-K*pd^2-Rdot^2-2*U-rdot^2.
```

The independent reducer used expand(expr).subs(H**2,hsq), which does not fully
reduce odd powers such as H**3. V3 instead clears denominators and takes the
numerator's exact polynomial remainder in H modulo

```text
6*M*H^2-(K*pd^2+Rdot^2+rdot^2+2*U).
```

The generic 22-field compiler already uses this polynomial-remainder method.
V3 verifies the independent reducer explicitly on H^3-H*hsq and H^4-hsq^2,
and verifies that the constraint is nonzero away from its declared shell.
No background value, kinetic formula, Hessian, charge, sign convention or
tolerance changes. Raw archived constraint residuals remain retained and
controlled by the already registered exact W-U correction.

Pin V2's source and failed receipt manifest, seal the V3 source, and execute
into a fresh directory. Preserve both interrupted attempts and the 79/80 result.
Retain all 378 archived-node and nine independent finite-Hessian controls.

Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
No full stability/window, cutoff, conserved energy, healthy GR or matching
claim. No provider change, publication, commit or push.
