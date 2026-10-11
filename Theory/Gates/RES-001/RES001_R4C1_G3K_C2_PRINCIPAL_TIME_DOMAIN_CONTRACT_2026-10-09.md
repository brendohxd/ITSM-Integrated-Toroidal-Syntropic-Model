# R4C1-G3K-C2: coupled dust-time principal-domain contract

Date: 9 October 2026. Version 1. Test-1 continuation after G3K-C1.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Question and decision rule

Test the necessary strong-hyperbolicity condition for the unchanged coupled
closed scalar axis sector in the actual global periodic dust-time chart.
Do not replace this coupled calculation by the healthy fixed-frame comparator.
Do not select only healthy-looking roots or discard the regulator auxiliary.

Form the principal quadratic characteristic matrix from the frozen action,
retaining the shift before its regular-domain reduction. Use a conventional
first-order / Fourier reduction of the second-order scalar equations, with
q and its first derivatives. Strong hyperbolicity in this reduction requires
real characteristic speeds and a complete, uniformly controlled eigenbasis.
A repeated speed with algebraic multiplicity greater than geometric
multiplicity rejects this unrestricted strong-hyperbolic dust-time use.

This is not automatically an all-norm nonlinear ill-posedness theorem,
physical ghost theorem, action-wide no-go or exclusion of a separately
justified finite-band EFT. A failed conventional reduction must not be
silently replaced by different derivative weights, mode selection, an altered
action or an invented cutoff. Such alternatives require their own derivation.

The mathematical criterion follows Gundlach and Martin-Garcia,
https://arxiv.org/pdf/gr-qc/0506037, sections I-II and V: the reduction must
be specified rather than importing an unrelated theorem wholesale.

## Frozen sources and chart

G3K-C1 report SHA-256:
ccab89c81f331cc7fc0288e998cf190311119b5f1c3717bd48d32752b32aee7c.
C1 attempt_02 summary and samples SHA-256 respectively:
39818742f14afe951780c20425b206128b11bf8007e3b84efd5743979e3262e7;
339373b084ba6b73c2eda87b58c215564afb86dab1ea55dbe3b68267e88c4cff.
G3K executable SHA-256:
05f3c588d8424a9d7f65c69624b483394144da5ae242c75c54f238ef895e37de.
G3K attempt_02 formulas, matrices and samples SHA-256 respectively:
b369f337b38fd29c8d6c16b4fed6bf787069089c682c9c639c38224e161bf8d5;
48cdb08629a4b1a252c62de632b7cf82d97e8f7b554c93a14376ef7c93ba3989;
69102fff332222f34684151e08a218fd92c6ae7a5153fd49d5900cf9e4b430d5.
Verify all inherited C1/G3K source pins and all available sidecars. Preserve
the three declared absent sidecars and all inherited failed assertions.

q=(xi,w,u,v,r,psi,z), radial metric gauge and positive dust clock tau=t.
The previously varied dust multiplier/lapse equations give N=exp(-beta psi)
and solve rho_m; no additional lapse constraint is invented or discarded.
Work on all 24 initial states and 16 saved method-tagged jets: 40 records,
32 eta/initial-tilt/time coordinates. Do not count paired solvers as distinct
physical backgrounds. No background, field, parameter or mode is refitted.

## Principal construction and retained constraints

Differentiate the frozen scalar action in (q_dot,q_x,B_x) before evaluating
the background. Independently verify H_BB=H_Bq=H_B,q_dot=0 there, and
the absence of a B velocity. Retain the unreduced 8-by-8 symbol for (q,B).

For q proportional to exp[i(k x-omega t)], c=omega/k, define
Q8(c)=[c^2 H_dd-c(H_dx+H_xd)+H_xx, -c H_d,Bx+H_x,Bx;
       -c H_Bx,d+H_Bx,x, H_Bx,Bx].
Use proper-coordinate speed nu=a_parallel*c/N and the nonsingular shift
variable B=N b_shift. Normalize by a_parallel^2/(N V), V=a_parallel*a_perp^2.
On the regular shift domain, form its Schur complement Q7(nu).
Do not invert k=0, w=0, or the exact w^2=1/5 shift boundary. At the latter,
check only the unreduced symbol and retain continuation as an open obligation.

Write Q7=nu^2 Tbar-nu Rbar+Sbar. Derive its conventional companion matrix
C14=[0,I;-Tbar^-1 Sbar,Tbar^-1 Rbar] on the regular invertible-kinetic domain.
Show directly that its eigenvectors at speed nu correspond to ker Q7(nu).
This keeps the constraint reduction and the precise strong-hyperbolicity
criterion auditable. Tbar signs alone are not a ghost classification.

## Regulator and multiplicity tests

Derive, without assuming it, the principal z row/column and its psi mixing.
Test whether it contains only -b*(w*nu-sqrt(1+w^2))^2 and a zero z diagonal.
If that structure holds, expand the determinant by those rows/columns to
derive its characteristic factor and multiplicity; do not infer multiplicity
from numerically split nearly-repeated roots.

At nu_star=sqrt(1+w^2)/w, derive the remaining five-field and six-field
minors and kinetic determinant under the exact registered G3 family.
Verify exact nonzero minors at all 24 rational initial eta/tilt pairs.
For the 16 archived jets evaluate the derived expressions as well as the
full numerical symbol. If a minor vanishes or a rank is unresolved, preserve
that case as unknown/failed rather than assuming the generic result.

Numerical symbol identities and archive-leading-coefficient matches:
normalized error <=1e-10. Use field congruence based on the inherited kinetic
scales before rank tests; require smallest nonzero singular value divided
by largest >=1e-8 to claim the six-field rank. Show the one explicit null
direction and companion kernel relation with normalized residual <=1e-10.
Retain all ten other characteristic roots plus all algebraic copies of the
regulator speed. Full polynomial eigenpair residual <=1e-7. No reality or
health pass requirement is imposed on those diagnostic roots.

Recover leading W/k and V/k^2 coefficients from the sealed k=(20,40,80)
matrices only after establishing their polynomial orders analytically.
Match them to the independently differentiated action. Coefficient time
derivatives are lower principal order; do not erase them from the parent
finite-frequency problem or call a principal test its full evolving solution.

## Controls, evidence and disposition

Retain the healthy fixed-frame quartic comparator as a method control only.
Check its tilted-clock principal multiplicity separately and its preferred
frame dispersion; a comparator defect must not be called a ghost in that
healthy preferred-frame model. Retain the aligned w=0 control as a distinct
mixed-order/auxiliary formulation, not a divided limit of C14.

Report exact algebra, every failure/unknown, conditioning margins, all roots,
inherited failures, source/receipt hashes and an exact read-only replay.
Use new versioned files and refuse an existing output directory. Do not
modify original action, sources, parent receipts, thresholds or parameters.

If the coupled principal matrix is defective, reject its unrestricted
strong-hyperbolic global dust-time use under this contract. Keep physical
finite-band/cutoff and alternative-formulation questions open; do not label
an inadmissible time chart as the action's physical ghost spectrum.
Carry direct/transitive review/scientific debt as DEFERRED. Tests 1-3
HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No manuscript/PDF edit, vault mutation, provider dispatch, commit, push,
promotion or publication is authorized by this checkpoint.
