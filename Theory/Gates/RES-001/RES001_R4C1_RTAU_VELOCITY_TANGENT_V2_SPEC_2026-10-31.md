# Velocity tangent V2: separate background departure and root uncertainty

V1 is preserved with 20/21 checks. Its extra precheck incorrectly required
the TOTAL departure of the prepared rate vector from the homogeneous
reference to be <0.001. The prepared longitudinal shift has derivative
amplitude about 0.0034. This is not the certified root uncertainty, which
is <1.139e-5 in the original continuation coordinates. The failed precheck
was not a requirement of the frozen contract and is not a physical failure.

Do not alter V1 or replace its measured total departure. V2 retains that
same total bound in every operator/energy inequality and only requires
that bound to be finite. Separately derive the propagation of the certified
root uncertainty into the rate vector. Apply the retained <0.001 check to
that uncertainty, with explicit derivatives of all rate components.

Let r=1.139e-5 bound each S, S_z, H and omega correction, l bound |lambda_z|,
and Nmin bound N below. Bounds for the changes in Wbar components are:

- two diagonal transverse rates: r*(1+l)/Nmin;
- two off-diagonal rates: r/(sqrt(2)*Nmin);
- longitudinal diagonal rate: r*(2+l)/Nmin;
- frame i: r*(|V_i|+|V_i'|+l*|V_i|+|V_z|)/Nmin;
- u/r/psi: r*|field_z|/Nmin;
- v: r*(1+|v_z|)/Nmin.

Their Euclidean sum-of-squares bound is the new root-rate uncertainty
control. The original total operator difference <0.01, right-inverse <1.01,
positive energy lower bound >0.01, full-action derivative tolerances and
all scientific equations/constraints are unchanged. This does not certify
the incorrect V1 total-departure precheck; its failure remains explicit.
The scope is planar velocity functions, both parities and all circle
harmonics, at fixed prepared spatial fields. No full symplectic, general
three-dimensional perturbation or evolving admission follows.
