# Quantitative inverse V1 execution specification

Freeze before execution. Use 32 covering cells, 40-digit outward intervals,
first-order spatial jets for derivative coefficients and radius 1/1000.
Use an explicit reflection center from the numerical 33-node coefficients:
Sx/Sy keep cosines; Sz keeps sines. Record exact removed-coefficient C2
majorant, preserve the original and carry that displacement into eta.

Extract the analytic A=0 summand's shift derivative at zero values of all
eight unknowns (S,S_z,H,omega) by exact unit polarization; its gradient is
affine in these unknowns. For the charge-integrand derivative, use symmetric
unit polarization over the entire interval correction ball; integrands have
degree at most two in those unknowns. Include the spatial derivative of
charge-flux coefficients after integration by parts. This is polynomial
identity extraction, not a finite-step approximation of the full cusp.

Bound the retained cusp analytically in local shift derivative, clock-charge
derivative and density. Check sufficient domain bounds before using them:
N,C,volume in [0.99,1.01], |V|<=1e-4, both coordinate and orthonormal
|grad psi|<=1e-4, |S_z-value|<=0.01, |psi_normal|<=0.3. Then the rest-gradient
norm is <=2e-4 and its shift derivative <=2e-8. Verify derived upper bounds
6*A*N*volume*|q|*|q_S|^2<1e-17,
6*A*volume/C*|q_S|*(|q|^2+|psi_normal|*|q|*|V|)<1e-12,
and A*(|q|^3+3*|psi_normal|*|q|^2*|V|)<1e-10.
These bounds cover the full cusp; no A=0 action is adopted.

Compute componentwise analytic derivative-defect row bounds on the whole
ball. Precondition shift rows with 38, H row with (I_row+Q_row)/a_lower,
omega row with Q_row. Use the interval residual V3's exact binary endpoints
for eta; add (1+q)*center_displacement. Require q<1 and eta+q*r<r.
Check positive density over every correction-ball cell, including cusp bound.
Record all failed inequalities unchanged; no existence claim if any required
bound or symmetry/mean compatibility justification is missing.

Validate the homogeneous charge block and principal reference against the
action, interval jet rules and full derivative coefficients. Fresh source,
receipt, exact replay; preserve all earlier files. A successful computer-
assisted certificate remains Conditional with independent review DEFERRED.
physics_pass=false; no nonlinear evolution or physical-window claim.
