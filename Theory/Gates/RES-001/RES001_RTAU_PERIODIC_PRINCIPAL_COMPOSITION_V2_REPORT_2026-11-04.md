# Periodic principal composition with all mean terms retained

4 November 2026. Conditional component of the
[prepared coupled-energy contract](RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md),
following the [20-direction mixed assembly](RES001_RTAU_MIXED_PRINCIPAL_ASSEMBLY_V1_REPORT_2026-11-04.md).
R-tau remains an UNADOPTED comparator. Original R4C1 and G1-G6 are unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE.

## Result and precise scope

The registered variable-coefficient principal differential operator now has
an exact periodic composition identity and a bounded L2 remainder for its
normal-form change. The change is invertible on the ENTIRE original
periodic complex L2 space and preserves every component mean. No Fourier
cutoff, low-mode deletion or truncation of generated tails is used.

This advances beyond the preceding frozen-symbol remainder. It does not
identify the principal differential operator with the actual full physical
generator. The material-frame remainder from exact constraint/auxiliary/
Green reconstruction, restored physical-time advection, T_dot, H_dot,
moving gauge/range/charge conditions and all global partners remain OPEN.
The actual background time tube and full coupled evolution inequality are
not established by this result.

Whole initial-root constants, in the existing original-coordinate norm,
include

    ||S||_2,infinity <0.601920,
    ||S_z||_2,infinity <0.058385,
    ||T||L2->L2 <1.601920,
    ||T^-1||L2->L2 <2.512053,
    ||R_composition||L2->L2 <26.438228,
    1.7010957e-8*||Y20||L2^2 <= E0(T*Y20)
                                <=1.1753917e7*||Y20||L2^2.

The constants are conservative bounds, not measured rates, a physical
cutoff, a validity window or a useful finite-time error estimate. All 20
ordinary/force directions remain. Mean preservation does not imply that
arbitrary tuples satisfy the original weighted range and fixed-charge
conditions; those conditions must be transported through the invertible
change on their actual compatible domain.

## Exact periodic operator algebra

On the registered 2*pi coordinate circle use the normalized coordinate
L2 norm, D=partial_z, the original coordinate mean M and

    P=D^-1*(I-M), DP=PD=I-M, ||P||L2->L2=1.

P acts componentwise and is the ORIGINAL periodic primitive. It is not a
new proper-volume or adapted-coordinate mean prescription. Put

    G=-A*D^2-i*B*D,
    Gdiag=-A*D^2-i*Bdiag*D,
    B+[S,A]=Bdiag.

A is the previous order-two fast block, and B the full mixed first block.
The material-frame principal coefficients retain their spatial dependence.
Common material advection is not silently discarded from the real system;
it still must be restored in the physical-time energy calculation.

Use the LEFT-primitive change

    T=I+i*P*S.

Its principal symbol is I+S/k, but multiplication and P do not commute.
This is a new operator realization of the earlier principal normal form,
not a claim that its previous frozen matrix remainder already covered
variable coefficients. Since ||S||infinity<1, the Neumann operator inverse
exists globally, with the bounds above. Moreover

    mean(T*u)=mean(u)

for every u. The change preserves means and retains all input modes, even
though varying coefficients mix Fourier components. It is not modewise
diagonalization.

Let F=S*A and H=S*B. Integration by parts with the original periodic
primitive gives the exact identities

    P*F*D^2=F*D-F_z+2*M*F_z+P*F_zz,
    P*H*D=H-M*H-P*H_z.

In particular the factor 2 in the first mean term is necessary. Here
M*F_z is the finite-rank operator u -> mean(F_z*u); it is not multiplication
by a mean coefficient. Substituting into T*G-Gdiag*T yields

    Rpre = i*F_z+i*A*S_z+H-Bdiag*S
           -2i*M*F_z-i*P*F_zz-M*H-P*H_z+Bdiag*M*S,
    T*G*T^-1=Gdiag+Rpre*T^-1.

All matrix multiplication orders are retained. In normalized L2 the mean
operator has norm one. Thus, for Rmul=i*F_z+i*A*S_z+H-Bdiag*S,

    ||Rpre|| <= ||Rmul||+2||F_z||+||F_zz||
                         +||H||+||H_z||+||Bdiag||*||S||,
    ||Rpre|| <10.524554,
    ||Rpre*T^-1|| <26.438228.

The same identity also justifies the natural mixed derivative domains for
this principal operator. S is C1 with its certified derivative bound.
The ordinary<-fast entries map H2 fast data into at least H1 ordinary data
through P; the fast<-ordinary entries map H1 ordinary data into H2 fast
data. Density has a zero cross row/column and stays at its declared L2
order. For the inverse, the component equations first yield fast H1 from
L2 data, then ordinary H1, then fast H2. This is a domain argument for this
registered principal change; it does not establish the physical constraint
domain's time preservation or its global symplectic normalization.

## Certified coefficient derivatives

Differentiate the same action-derived matrices, retaining all shift and
material-advection terms. In particular

    (Kshift^-1)_z=-Kshift^-1*Kshift_z*Kshift^-1,
    (Mordinary^-1)_z=-Mordinary^-1*Mordinary_z*Mordinary^-1.

The raw shift/velocity/gradient block derivatives come from the immutable
first spatial Hessian export. The exact differentiated Ward identity fixes
the longitudinal column without interval dependency loss. Dshift+S*Cshift
and its derivative remain in the shift response. No root-error radius is
differentiated and no background coefficient is assumed spatially constant.

Only special second derivatives are needed in this operator ordering:

- F=S*A has only the ordinary<-fast block -Bof. Its nonzero coefficient is
  i*d*s/(2a^2) in the two metric momentum rows, so F_zz follows from the
  analytic metric/clock profiles.
- Bfast_z requires m_zz. For m=(mu/N)*f_pp, derive f_pp from the full force.
  With p normal clock velocity, cv=V.h.V, w=Vz and
  Y=cv*p^2+2*gamma*w*p*s+(kappa+w^2)*s^2, it is

      f_pp=K_Q*gamma^2
             -3*Aforce*(cv*sqrt(Y)+(cv*p+gamma*w*s)^2/sqrt(Y)).

  The positive-Y branch is checked before any fractional power. Spatial
  order-two Taylor jets use the original certified root and existing higher
  root certificate. The mass and first derivative are checked against the
  original Hessian enclosures. No full Hessian is rerun.

Outward bounds include

    ||B_z||infinity <14.760497,
    ||F_z||infinity <0.000052604,
    ||F_zz||infinity <0.000094162,
    |m_zz| <0.045762.

These calculations do not supply the time derivatives of those coefficients.

## Spatial energy-adjoint terms

The diagonal principal system's spatial energy terms are also bounded.
For the ordinary sector, differentiate the same complement energy and the
stationary coordinate zeta=z-b*C^-1*x. The inverse derivative is retained,
including the exact reference normalization factor sqrt(99/2) relating the
reference energy norm to coordinate norm. Conservative results are

    ||Hordinary_z||infinity <1.655114e10,
    ||(Hordinary*(-i*Aordinary))_z||infinity <1.061336e11.

These large constants are interval/triangle bounds, not measured growth
or evidence of instability. They do not certify useful accuracy on the
target [0,0.05]. They should not be converted into an asserted physical
evolution result by freezing time coefficients.

For the force pair, the previously proved order-two/order-one formal
cancellations leave the spatial zero-order form

    (Hfast*Afast)_zz-(Bfast_differential^T*Hfast)_z,

whose norm is below 0.008407. The required second force mass derivative is
included. Neither this number nor the ordinary spatial bound includes
H_dot, T_dot or the actual generator's unassembled terms.

The global energy equivalence in this report follows directly by applying
the pointwise diagonal energy bounds to T*Y and using

    (1-||S||)*||Y|| <= ||T*Y|| <= (1+||S||)*||Y||.

It is an equivalence of norms for the periodic principal change, not a
complete physical energy evolution inequality.

## Controls, failure preservation and disposition

Executable `Analysis/MasterTests/test_rtau_periodic_principal_composition_v2.py`;
[frozen V2 criteria](RES001_RTAU_PERIODIC_PRINCIPAL_COMPOSITION_V2_SPEC_2026-11-04.md).
Receipt `Analysis/MasterTests/outputs/rtau_periodic_principal_composition_v2_20261104/receipt.json`.
SHA256:

    d3f2fe4cc893109596883f69155622e1e8e7c93300a40eb0ed8774988d922a8a

18/18 bounded controls and byte-identical replay COMPLETE. Independent
exact Fourier-polynomial controls use noncommuting varying matrices, retain
every convolution tail and detect deletion of the finite-rank mean terms.
They also verify both periodic primitive identities and mean preservation.
The force f_pp formula has a separate exact symbolic differentiation
control. Current spatial derivative enclosures remain source-pinned.

V1's failed source/specification/failure record are preserved. Its ordinary
interval v*v multiplication lost square nonnegativity on crossing-zero
gradient intervals, giving a spurious negative Y enclosure and invalid
fractional-power arithmetic. V2 uses the existing jet's v**2 operation and
stops strictly before fractional powers unless Y>0. No equation, physical
branch condition, domain, tolerance or acceptance was weakened.

All 219 original input pins and 292 receipt source pins remain unchanged;
snapshotted sidecars/timestamps were preserved. These are same-author
controls; independent Rule-9 review remains DEFERRED.

NEXT: derive the actual material-frame generator minus this registered
principal operator with the exact compatible Green/constraint/auxiliary
and gauge reconstruction. Restore physical-time advection in its energy
identity, then bound T_dot, H_dot, moving range and global charge/harmonic
partners. A genuine background-domain tube is still needed before any
finite-time admission. Full energy and original G1-G6 remain incomplete.
The domain-first goal remains ACTIVE. No action adoption, matching input,
paper/site promotion, vault write/sync, dispatch or Git/publication occurred.
