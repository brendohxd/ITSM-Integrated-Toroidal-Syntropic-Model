#!/usr/bin/env python3
"""BBN-001: reproducible BBN table and CAMB bridge control.

This is a software/data control, not an ITSM cosmology prediction. It checks
that the bundled BBN tables have a rectangular, readable schema; that the
PRIMAT 2024 ``Ombh2`` spelling is handled without an undocumented workaround;
and that CAMB consumes the resulting helium mass fraction. It deliberately
does not provide an early-plenum background, an action-derived ``Q^mu`` or a
BBN likelihood.
"""

import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy

REPO_ROOT = Path(__file__).resolve().parents[3]
SOLVER_ROOT = REPO_ROOT / "CAMB_ITSM_Solver"
sys.path.insert(0, str(SOLVER_ROOT))

import camb  # noqa: E402
from camb import bbn  # noqa: E402

TABLE_NAMES = (
    "PArthENoPE_880.2_standard.dat",
    "PArthENoPE_880.2_marcucci.dat",
    "PRIMAT_Yp_DH_Error.dat",
    "PRIMAT_Yp_DH_ErrorMC_2021.dat",
    "PRIMAT_Yp_DH_ErrorMC_2024.dat",
)
CONTROL_OMBH2 = 0.02237
CONTROL_DELTAN = 0.0
PRIMAT_2024 = "PRIMAT_Yp_DH_ErrorMC_2024.dat"
COMMON_OBSERVABLES = ("Yp^BBN", "D/H")


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition, message):
    if not condition:
        raise RuntimeError(message)


def _control_values(predictor):
    y_p = float(predictor.Y_p(CONTROL_OMBH2, CONTROL_DELTAN))
    y_he = float(predictor.Y_He(CONTROL_OMBH2, CONTROL_DELTAN))
    d_h = float(predictor.DH(CONTROL_OMBH2, CONTROL_DELTAN))
    _require(np.isfinite(y_p) and 0.0 < y_p < 1.0, "Y_p control is not finite or physical-range bounded")
    _require(np.isfinite(y_he) and 0.0 < y_he < 1.0, "Y_He control is not finite or physical-range bounded")
    _require(np.isfinite(d_h) and d_h > 0.0, "D/H control is not finite and positive")
    converted_y_he = float(bbn.ypBBN_to_yhe(y_p))
    _require(np.isclose(y_he, converted_y_he, rtol=0.0, atol=1e-14), "Y_p to Y_He conversion is inconsistent")
    return {
        "Y_p_nucleon_fraction": y_p,
        "Y_He_mass_fraction": y_he,
        "D/H": d_h,
        "Y_He_from_Y_p_check": converted_y_he,
    }


def _table_result(table_name):
    table_path = SOLVER_ROOT / "camb" / table_name
    _require(table_path.is_file(), f"Missing bundled BBN table: {table_name}")
    predictor = bbn.BBN_table_interpolator(table_name)
    _require(len(predictor.ombh2s) >= 2, f"Insufficient ombh2 axis values in {table_name}")
    _require(len(predictor.deltans) >= 2, f"Insufficient DeltaN axis values in {table_name}")
    _require(np.all(np.diff(predictor.ombh2s) > 0), f"ombh2 axis is not strictly increasing in {table_name}")
    _require(np.all(np.diff(predictor.deltans) > 0), f"DeltaN axis is not strictly increasing in {table_name}")
    _require(
        predictor.ombh2s[0] <= CONTROL_OMBH2 <= predictor.ombh2s[-1],
        f"Control ombh2 is outside the table domain for {table_name}",
    )
    _require(
        predictor.deltans[0] <= CONTROL_DELTAN <= predictor.deltans[-1],
        f"Control DeltaN is outside the table domain for {table_name}",
    )
    for observable in COMMON_OBSERVABLES:
        _require(observable in predictor.interpolators, f"Missing {observable} column in {table_name}")

    return {
        "table": table_name,
        "sha256": _sha256(table_path),
        "header_columns": list(predictor.table_columns),
        "requested_function_of": list(predictor.function_of),
        "resolved_axis_columns": list(predictor.axis_columns),
        "grid_shape": {
            "ombh2": len(predictor.ombh2s),
            "DeltaN": len(predictor.deltans),
            "rows": len(predictor.ombh2s) * len(predictor.deltans),
        },
        "domain": {
            "ombh2": [float(predictor.ombh2s[0]), float(predictor.ombh2s[-1])],
            "DeltaN": [float(predictor.deltans[0]), float(predictor.deltans[-1])],
        },
        "control_point": {
            "ombh2": CONTROL_OMBH2,
            "DeltaN": CONTROL_DELTAN,
        },
        "outputs": _control_values(predictor),
    }


def _schema_equivalence_check():
    automatic = bbn.BBN_table_interpolator(PRIMAT_2024)
    explicit_case = bbn.BBN_table_interpolator(PRIMAT_2024, function_of=("Ombh2", "DeltaN"))
    explicit_lower = bbn.BBN_table_interpolator(PRIMAT_2024, function_of=("ombh2", "DeltaN"))
    _require(automatic.axis_columns == ("Ombh2", "DeltaN"), "PRIMAT 2024 axis spelling was not preserved")
    comparisons = {}
    for observable in COMMON_OBSERVABLES:
        automatic_value = float(automatic.get(observable, CONTROL_OMBH2, CONTROL_DELTAN))
        case_value = float(explicit_case.get(observable, CONTROL_OMBH2, CONTROL_DELTAN))
        lower_value = float(explicit_lower.get(observable, CONTROL_OMBH2, CONTROL_DELTAN))
        _require(automatic_value == case_value == lower_value, f"Schema path changed {observable}")
        comparisons[observable] = {
            "automatic": automatic_value,
            "explicit_table_spelling": case_value,
            "explicit_default_spelling": lower_value,
            "equal": True,
        }
    return {
        "table": PRIMAT_2024,
        "automatic_default_axis_request": ["ombh2", "DeltaN"],
        "actual_table_axis": ["Ombh2", "DeltaN"],
        "former_workaround": ["Ombh2", "DeltaN"],
        "comparisons": comparisons,
        "interpretation": "Schema compatibility only; no numerical or physical transformation is applied.",
    }


def _response_sanity_check():
    predictor = bbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat")
    baseline = _control_values(predictor)
    faster_expansion = _control_values_for_delta(predictor, 1.0)
    _require(
        faster_expansion["Y_He_mass_fraction"] > baseline["Y_He_mass_fraction"],
        "DeltaN response control did not increase Y_He",
    )
    _require(
        faster_expansion["D/H"] > baseline["D/H"],
        "DeltaN response control did not increase D/H",
    )
    return {
        "table": "PArthENoPE_880.2_standard.dat",
        "baseline_DeltaN": baseline,
        "DeltaN_plus_1": faster_expansion,
        "interpretation": "Interpolation response sanity check, not an ITSM expansion-history result.",
    }


def _control_values_for_delta(predictor, delta_neff):
    y_p = float(predictor.Y_p(CONTROL_OMBH2, delta_neff))
    y_he = float(predictor.Y_He(CONTROL_OMBH2, delta_neff))
    d_h = float(predictor.DH(CONTROL_OMBH2, delta_neff))
    _require(np.isfinite(y_p) and np.isfinite(y_he) and np.isfinite(d_h), "DeltaN response is not finite")
    return {
        "Y_p_nucleon_fraction": y_p,
        "Y_He_mass_fraction": y_he,
        "D/H": d_h,
    }


def _camb_bridge_check():
    predictor = bbn.BBN_table_interpolator(PRIMAT_2024)
    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=67.7,
        ombh2=CONTROL_OMBH2,
        omch2=0.12,
        bbn_predictor=predictor,
    )
    data = camb.CAMBdata()
    data.Params = pars
    data.calc_background(pars)
    expected_y_he = float(predictor.Y_He(CONTROL_OMBH2, 0.0))
    expected_y_p = float(predictor.Y_p(CONTROL_OMBH2, 0.0))
    _require(np.isclose(pars.YHe, expected_y_he, rtol=0.0, atol=1e-14), "CAMB YHe bridge mismatch")
    _require(np.isclose(pars.get_Y_p(), expected_y_p, rtol=0.0, atol=1e-14), "CAMB Y_p bridge mismatch")
    return {
        "table": PRIMAT_2024,
        "H0": 67.7,
        "ombh2": CONTROL_OMBH2,
        "omch2": 0.12,
        "CAMB_YHe": float(pars.YHe),
        "CAMB_Y_p_nucleon_fraction": float(pars.get_Y_p()),
        "bridge_check": True,
    }


def run_control():
    table_results = [_table_result(table_name) for table_name in TABLE_NAMES]
    return {
        "record_type": "BOUNDED_BBN_CONTROL_RECEIPT",
        "gate": "BBN-001",
        "status": "CONTROL_ONLY",
        "physics_pass": False,
        "gate_effect": "NONE",
        "publication_status": "NOT_A_PHYSICS_CLAIM",
        "scope": (
            "Bundled BBN table schema, interpolation, and CAMB bridge only. "
            "No ITSM early-time action, plenum density, Q^mu, G_eff(z), or likelihood is implemented."
        ),
        "frozen_inputs": {
            "ombh2": CONTROL_OMBH2,
            "DeltaN": CONTROL_DELTAN,
            "common_observables": list(COMMON_OBSERVABLES),
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "camb": camb.__version__,
        },
        "table_results": table_results,
        "schema_equivalence": _schema_equivalence_check(),
        "response_sanity": _response_sanity_check(),
        "camb_bridge": _camb_bridge_check(),
        "review_state": {
            "independent_reproduction": "NOT_COMPLETED",
            "three_way_consensus": "NOT_MET",
            "external_BBN_likelihood": "NOT_IMPLEMENTED",
            "ITSM_mapping": "NOT_DERIVED",
        },
        "limitations": [
            "The bundled tables encode external BBN calculations; this receipt does not reproduce their nuclear network.",
            "DeltaN is a control coordinate here, not an action-derived ITSM transfer or plenum parameter.",
            "Y_p is a helium nucleon fraction; Y_He is the mass fraction passed to CAMB.",
            "No BBN, empirical-helium, Planck, DESI, or posterior likelihood is evaluated.",
            "No gate or publication status changes follow from this receipt.",
        ],
    }


def main():
    result = run_control()
    result["script_sha256"] = _sha256(Path(__file__))
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "bbn001_control_summary.json"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    digest = _sha256(output_path)
    (output_dir / "bbn001_control_summary.json.sha256").write_text(f"{digest}  {output_path.name}\n", encoding="utf-8")
    print("BBN-001 bounded control complete")
    print(f"Status: {result['status']}")
    print(f"Tables checked: {len(result['table_results'])}")
    print(f"CAMB bridge: {result['camb_bridge']['bridge_check']}")
    print(f"SHA-256: {digest}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
