# R4C1-G3D: physical density phase/action map and singular-domain audit

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / formal G3 slow branch.
Review DEFERRED; gate effect NONE. Frozen before executable validation and
new numerical sign sampling. Analytic expectations arise during planning
from the frozen G3E maps; this is not a claim of preregistration before
analytic reasoning or a new observational test.

Owning report: [G3F finite-k comparison](RES001_R4C1_G3_FINITE_K_REPORT_2026-09-30.md).
G3A retains K_X=1-12/eta<0; G3F validates the prepared approximation on a
bounded grid but does not identify a physical energy/norm. Derive the
physical dust-density coordinate's action without changing either result.

## Registered calculation and evidence rules

1. Use only the frozen G3E physical density map and G3S background flow,
   with X=sqrt(eta)*chi/k and k,eta constant in time. The physical leading
   density contrast is D=f chi+g chidot; its coefficients are the exported
   density row times sqrt(eta). Retain the inherited signed coefficient
   kappa=eta*K_X/k^2, mass m_E, and the exact original slow action.
2. Differentiate D with the full background flow and slow generator
   B=[[0,1],[-m_E,0]]. Derive T:(chi,chidot)->(D,Ddot), det(T), and its
   singular domains. Distinguish this determinant from G3E's different
   density/comoving-velocity determinant. Verify or reject the analytic
   expectations gdot=-f and Ddot=(sqrt(6)/a^(5/2))*chi. Never invert across
   a vanishing determinant or an inherited rank-changing boundary.
3. Obtain the transformed generator (Tdot+T B) T^-1, using the adjugate
   and explicit determinant. Compare the derived friction and mass with
   2H+beta*psidot and -rho_m/(2Mc2), where beta=2eta^2/5, Mc2=1-eta/12.
   Obtain K_D=kappa/det(T) from the symplectic form, not from an arbitrary
   integrating factor. Verify or reject K_D=a^5 rho_m/k^2 and
   K_D_dot/K_D=friction. Record all failures and sign discrepancies.
4. Prove action equivalence in FIRST-ORDER phase space. Treat chi and its
   momentum as independent off-shell variables. Build the time-dependent
   generating boundary term from the difference of canonical one-forms,
   and verify both its phase gradient and its explicit time derivative in
   the Hamiltonian identity. Do not insert the slow equation into a
   second-order off-shell action or reverse its overall sign. Verify the
   new second-order Euler equation by algebraic momentum elimination.
5. Distinguish positive density kinetic weight from a positive-definite
   Hamiltonian, stationary quantum norm and full physical energy theorem.
   Report the sign of the density mass/potential and its energy balance.
   Check the formal GR dust coefficient control: eta->0, no transfer,
   rho_m=3H^2, Hdot=-3H^2/2 in the MP2=1 chart. Recover the standard dust
   growth equation and its a,a^(-3/2) modes without claiming a rank-regular
   full-theory eta=0 limit or a physical EFT window.
6. Sample ALL six frozen G3 eta values and both archived background
   methods at t=(0,.5,1,2,3,4), with k=(20,40,80): 216 registered coefficient
   events. Check density-map rank, signed kinetic, transformed friction,
   mass, first-order action identities and normalization. Record the full
   grid and maxima. These chart parameters are not measured wavelengths.

All exact and numerical checks must be retained, including failures. Pin
direct/inherited sources, refuse existing output directories and support
nonmutating byte-identity replay. Memory is retrieval only; no vault mutation,
source/receipt overwrite, PDF work, model dispatch, commit or publication.

Domain: 0<eta<=1, a,C,rho_m,H>0, k>0 and S1's inherited auxiliary rank
conditions. The formal dust coefficient limit is not an inverse through
eta=0. The canonical full GR limit, physical cutoff, all-sector stability
and Tests 2/3 closure remain independent requirements.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A/G3F and
their scope/review debt. Canonical Tests 1-3 HOLD_SUBSTANTIVE; physics_pass=false,
Rule9_cleared=false, review DEFERRED, gate_effect=NONE. MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED;
TOP-X4 unchanged.
