# TOP-001 Stage S1.7 / S1M — Modular basis-equivalence audit

**Date:** 2026-08-05
**Branch:** `recovery/v12-core-architecture`
**Status:** `OPEN_SCAFFOLD_ONLY`
**Subgate:** `PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE`
**physics_pass:** **false**

## Purpose

Determine which apparent torus shears are only changes of the integer lattice
basis and therefore describe the same fixed flat \(T^3\). This is a quotient
and redundancy guardrail for later TOP work, not evidence that a sheared torus
is dynamically preferred.

Let the columns of \(B\) be a direct-lattice basis,

\[
  \Lambda(B)=\{B\mathbf n:\mathbf n\in\mathbb Z^3\}.
\]

For \(M\in SL(3,\mathbb Z)\), define \(B'=BM\). Because \(M\) is an
invertible integer map of \(\mathbb Z^3\), \(B\) and \(B'\) generate exactly
the same lattice. The required label maps are

\[
 \mathbf n'=M^{-1}\mathbf n,
 \qquad
 \mathbf m'=M^T\mathbf m,
 \qquad
 \mathbf w'=M^T\mathbf w.
\]

They preserve direct-lattice points, reciprocal wavevectors and winding
covectors exactly:

\[
 B'\mathbf n'=B\mathbf n,
 \qquad
 2\pi B'^{-T}\mathbf m'=2\pi B^{-T}\mathbf m,
 \qquad
 2\pi B'^{-T}\mathbf w'=2\pi B^{-T}\mathbf w.
\]

The coordinate Gram matrix changes covariantly,
\(G'=M^TGM\), while the fundamental volume is unchanged.

## Executable record

```powershell
python Analysis\TOP\TOP-001\top001_s1m_modular_basis_equivalence_audit.py
# expect: PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE
# physics_pass: False
```

Outputs:

```text
Analysis/TOP/TOP-001/outputs/top001_s1m_modular_basis_equivalence_summary.json
Analysis/TOP/TOP-001/outputs/top001_s1m_modular_basis_equivalence_summary.sha256
```

Accepted deterministic SHA-256:

```text
112051eb62e28683a15e981b5bf29a9d7a58f40e461d915ba9846fdb4461fde0
```

## Checks

The audit runs 11 checks:

1. all declared maps are in \(SL(3,\mathbb Z)\);
2. exact direct-lattice reindexing;
3. exact reciprocal-mode reindexing;
4. exact winding-covector reindexing;
5. Gram-matrix covariance;
6. fundamental-volume invariance;
7. paired Laplacian-eigenvalue invariance;
8. negative control for an untransformed reciprocal label;
9. separation from an explicit volume-preserving ambient deformation;
10. fail-closed rejection of malformed or out-of-domain maps; and
11. claim-firewall packaging flags remain false.

## Cutoff caution

A raw cubical label cutoff such as \(|m_i|\leq N\) is coordinate dependent.
Under a modular map, labels must be transformed with \(M^T\), or a physical
eigenvalue cutoff must be used. Comparing identical raw label boxes in two
bases can create a false difference even though the underlying spectrum is
the same.

## Physical-deformation separation

The audit separately applies a left-acting, volume-preserving ambient map
\(B_{\rm physical}=FB\) with
\(F=\operatorname{diag}(2,1,1/2)\). A sampled reciprocal norm changes. This
is a genuine metric/shape deformation in the declared ambient frame, not an
integer relabelling \(B\mapsto BM\).

## Scientific boundary

- No preferred modular shear or numerical pattern is inferred.
- No physical significance is assigned to the illustrated labels \(1,4,7\).
- No modulus action, energy minimum, Hessian, stability or backreaction is
  computed.
- No Casimir tensor or twisted \(E_2/E_3\) comparison is performed.
- No \(13/12\), \(H_0\), \(a_0\), \(C_{\rm obs}\), or cosmological result is
  produced.

This closes only an exact fixed-boundary basis identity. TOP-001 remains
`OPEN_SCAFFOLD_ONLY`; a later physical comparison must work on inequivalent
moduli after quotienting by the modular redundancy.
