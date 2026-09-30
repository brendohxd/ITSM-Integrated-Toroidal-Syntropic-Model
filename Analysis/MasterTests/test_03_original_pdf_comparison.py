"""Fail-closed algebra/units replay for the original v7.2 and v11.1.1 PDFs.

Equations are manually transcribed from the identified PDF pages; this script
hash-checks the PDF bytes but does not claim to parse equations from a PDF.
It writes no files and does not select C_chi from observational a0 data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path

import sympy as s


EXPECTED_PDF_SHA256 = {
    "v7.2": "ec37735cb3523acc48c8a4768093c5a517217703337a843a235df9a5b2def70d",
    "v11.1.1": "25678f36450a9df9482a14c798f0eae143dc1cf04652251bd930257a9ed799ee",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v72-pdf", type=Path, required=True)
    parser.add_argument("--v111-pdf", type=Path, required=True)
    args = parser.parse_args()

    paths = {"v7.2": args.v72_pdf, "v11.1.1": args.v111_pdf}
    actual_hashes = {name: digest(path) for name, path in paths.items()}
    integrity = all(actual_hashes[name] == expected for name, expected in EXPECTED_PDF_SHA256.items())
    if not integrity:
        print(json.dumps({"source_integrity_verified": False, "actual_pdf_sha256": actual_hashes,
                          "expected_pdf_sha256": EXPECTED_PDF_SHA256, "physics_pass": False}, indent=2))
        return 2

    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})

    c, H, h, m, a, q = s.symbols("c H h m a q", positive=True)
    ell = c / H
    kappa_cosmo = c**2 / H
    kappa_of = h / m
    literal_a0 = s.simplify(kappa_cosmo / (2 * s.pi * ell))
    displayed_a0 = c * H / (2 * s.pi)
    check("literal_v7_and_v11_chain_is_speed", s.simplify(literal_a0 - c / (2 * s.pi)) == 0)
    check("displayed_a0_is_not_literal_chain", s.simplify(literal_a0 - displayed_a0) != 0)
    check("missing_factor_is_H", s.simplify(displayed_a0 / literal_a0 - H) == 0)
    ratio = s.simplify(kappa_cosmo / kappa_of)
    check("two_scale_ratio_formula", ratio == m * c**2 / (h * H))
    equality_mass = s.solve(s.Eq(kappa_cosmo, kappa_of), m)[0]
    check("equality_requires_different_mass", s.simplify(equality_mass - h * H / c**2) == 0)

    # v11.1.1 PDF pp. 11-12, Eqs. (37)-(39), with X=q^2/2 and q=|grad phi|.
    lx_over_mp2 = 1 + 1 / (3 * s.sqrt(1 + q**2 / (2 * a**2)))
    flux = q * lx_over_mp2
    check("weak_field_lx_zero_limit", s.limit(lx_over_mp2, q, 0, dir="+") == s.Rational(4, 3))
    check("weak_field_lx_large_limit", s.limit(lx_over_mp2, q, s.oo) == 1)
    check("weak_field_flux_linear_at_zero", s.limit(flux / q, q, 0, dir="+") == s.Rational(4, 3))
    check("weak_field_flux_not_quadratic_at_zero", s.limit(flux / q**2, q, 0, dir="+") == s.oo)

    # Numerical consistency uses only the manuscript's illustrative H0=70 and
    # m=10^-22 eV/c^2, not measured a0. SI constants and IAU Mpc conversion.
    c_si = Decimal("299792458")
    h_si = Decimal("6.62607015e-34")
    mpc_si = Decimal("3.0856775814913673e22")
    h0_si = Decimal("70000") / mpc_si
    m_si = Decimal("1e-22") * Decimal("1.78266192e-36")
    macro_si = c_si**2 / h0_si
    micro_si = h_si / m_si
    ratio_si = macro_si / micro_si
    equality_mass_ev = (h_si * h0_si / c_si**2) / Decimal("1.78266192e-36")
    check("stated_mass_implies_distinct_quanta", Decimal("1e10") < ratio_si < Decimal("1.2e10"))
    check("printed_micro_magnitude_not_SI_value", micro_si / Decimal("1e-3") > Decimal("1e20"))
    check("printed_macro_magnitude_not_SI_value", Decimal("1e39") / macro_si > Decimal("1e4"))
    check("printed_magnitudes_ratio_is_1e42_not_1e10",
          Decimal("1e39") / Decimal("1e-3") == Decimal("1e42"))

    passed = all(row["passed"] for row in checks)
    payload = {
        "test": 3,
        "scope": "original_pdf_source_hash_and_declared_equation_replay",
        "equation_extraction": "manual reading of v7.2 pp. 2-3 and v11.1.1 pp. 5, 7, 11-12",
        "source_integrity_verified": True,
        "pdf_sha256": actual_hashes,
        "checks": checks,
        "local_validation": "PASS" if passed else "FAIL",
        "derived_values": {
            "literal_kappa_over_2pi_ell": str(literal_a0),
            "displayed_a0": str(displayed_a0),
            "kappa_cosmo_m2_per_s": str(macro_si),
            "kappa_of_m2_per_s": str(micro_si),
            "kappa_ratio": str(ratio_si),
            "mass_for_quantum_equality_eV_per_c2": str(equality_mass_ev),
            "weak_field_lx_over_mp2": str(lx_over_mp2),
        },
        "observed_a0_used": False,
        "analyst_blinded": False,
        "C_chi": "NOT_DERIVED",
        "physics_pass": False,
        "canonical_Test3_pass": False,
        "Test2_physics_pass": False,
        "gate_effect": "NONE",
        "Rule9_cleared": False,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
