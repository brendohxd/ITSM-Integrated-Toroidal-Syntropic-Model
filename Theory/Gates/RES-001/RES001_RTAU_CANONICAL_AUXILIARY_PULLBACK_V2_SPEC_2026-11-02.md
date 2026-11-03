# V2 correction: coordinate measure and derivative factors

Preserve the V1 producer/specification/receipt. Its reported canonical
composition constants were not justified: they omitted L2 measure conversion
and the H1 derivative factor for pulling a coordinate velocity back. No claim
that the original bound is false on every actual vector is made; it is withdrawn
as a certified estimate. The target density, action and norm criteria are unchanged.

Use zeta_z=J, j<=J<=u, J_z/J=lambda_z, |lambda_z|<=r.
The source-to-adapted L2 map has multiplier bound F*sqrt(u), not F alone.
For Sx=xi_x(zeta), derivative_z Sx=J*xi_x,zeta; similarly y.
For Sz=xi_z(zeta)/J,

    derivative_z Sz=xi_z,zeta-(lambda_z/J)*xi_z.

The integration measure is dz=d_zeta/J. The component H1 operator matrices
are diag(1,J) transversely and [[1/J,0],[-lambda_z/J,1]] longitudinally.
Their common bound, including measure, is

    Cback=j^(-1/2)*(max(1,u,1/j)+r/j).

It bounds the diagonal part by its maximum and the lower off-diagonal part
by r/j, so is conservative for all components on the actual circle. Replace
F by F*sqrt(u) and Cback by this expression throughout the V1 composition.
The mean-free gauge solve and harmonic inputs remain as before. Add exact
chain-rule/Jacobian identities and outward checks of both component matrix
bounds. Do not change the auxiliary variation or infer a finite-time theorem.

New receipt retains supersession_scope=initial bound correction only. V1 raw
outputs, sources and failure interpretation remain available for provenance.
