"""Bounded tests for the bundled BBN table adapter.

These tests validate table schema handling and the CAMB interface. They are
software/data controls only; they do not test an ITSM early-time action,
plenum mapping, transfer current, or cosmological likelihood.
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

try:
    import camb
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    import camb

from camb import bbn

TABLE_NAMES = (
    "PArthENoPE_880.2_standard.dat",
    "PArthENoPE_880.2_marcucci.dat",
    "PRIMAT_Yp_DH_Error.dat",
    "PRIMAT_Yp_DH_ErrorMC_2021.dat",
    "PRIMAT_Yp_DH_ErrorMC_2024.dat",
)
CONTROL_OMBH2 = 0.02237
CONTROL_DELTAN = 0.0


class BBNTableTest(unittest.TestCase):
    def test_all_bundled_tables_load_with_default_axis_names(self):
        table_dir = Path(bbn.__file__).parent

        for table_name in TABLE_NAMES:
            with self.subTest(table=table_name):
                table_path = table_dir / table_name
                self.assertTrue(table_path.is_file())
                predictor = bbn.BBN_table_interpolator(table_name)

                self.assertEqual(predictor.function_of, ("ombh2", "DeltaN"))
                self.assertIn(predictor.axis_columns[0].casefold(), {"ombh2"})
                self.assertEqual(predictor.axis_columns[1], "DeltaN")
                self.assertGreaterEqual(len(predictor.ombh2s), 2)
                self.assertGreaterEqual(len(predictor.deltans), 2)
                self.assertTrue(np.all(np.diff(predictor.ombh2s) > 0))
                self.assertTrue(np.all(np.diff(predictor.deltans) > 0))
                self.assertGreaterEqual(CONTROL_OMBH2, predictor.ombh2s[0])
                self.assertLessEqual(CONTROL_OMBH2, predictor.ombh2s[-1])
                self.assertGreaterEqual(CONTROL_DELTAN, predictor.deltans[0])
                self.assertLessEqual(CONTROL_DELTAN, predictor.deltans[-1])

                y_p = predictor.Y_p(CONTROL_OMBH2, CONTROL_DELTAN)
                y_he = predictor.Y_He(CONTROL_OMBH2, CONTROL_DELTAN)
                d_h = predictor.DH(CONTROL_OMBH2, CONTROL_DELTAN)
                self.assertTrue(np.isfinite(y_p) and 0.0 < y_p < 1.0)
                self.assertTrue(np.isfinite(y_he) and 0.0 < y_he < 1.0)
                self.assertTrue(np.isfinite(d_h) and d_h > 0.0)
                self.assertAlmostEqual(y_he, bbn.ypBBN_to_yhe(y_p), places=15)

    def test_primat_2024_case_difference_is_schema_only(self):
        table_name = "PRIMAT_Yp_DH_ErrorMC_2024.dat"
        automatic = bbn.BBN_table_interpolator(table_name)
        explicit_case = bbn.BBN_table_interpolator(table_name, function_of=("Ombh2", "DeltaN"))
        explicit_lower = bbn.BBN_table_interpolator(table_name, function_of=("ombh2", "DeltaN"))

        self.assertEqual(automatic.axis_columns, ("Ombh2", "DeltaN"))
        self.assertEqual(explicit_case.axis_columns, automatic.axis_columns)
        self.assertEqual(explicit_lower.axis_columns, automatic.axis_columns)
        for observable in ("Yp^BBN", "D/H", "sig(Yp^BBN)", "sig(D/H)"):
            with self.subTest(observable=observable):
                automatic_value = automatic.get(observable, CONTROL_OMBH2, CONTROL_DELTAN)
                explicit_value = explicit_case.get(observable, CONTROL_OMBH2, CONTROL_DELTAN)
                lower_value = explicit_lower.get(observable, CONTROL_OMBH2, CONTROL_DELTAN)
                self.assertEqual(automatic_value, explicit_value)
                self.assertEqual(automatic_value, lower_value)

    def test_invalid_axis_requests_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly two"):
            bbn.BBN_table_interpolator(function_of=("ombh2",))
        with self.assertRaisesRegex(ValueError, "not found"):
            bbn.BBN_table_interpolator(function_of=("missing_axis", "DeltaN"))

    def test_ambiguous_case_insensitive_axis_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            bbn._resolve_column_index(["ombh2", "Ombh2", "DeltaN"], "OMBH2", "synthetic.dat")

    def test_header_data_width_mismatch_fails_closed(self):
        table_name = "PRIMAT_Yp_DH_ErrorMC_2024.dat"
        with patch.object(bbn.np, "loadtxt", return_value=np.zeros((1, 3))):
            with self.assertRaisesRegex(ValueError, "schema mismatch"):
                bbn.BBN_table_interpolator(table_name)

    def test_camb_consumes_mass_fraction_from_bbn_predictor(self):
        predictor = bbn.BBN_table_interpolator("PRIMAT_Yp_DH_ErrorMC_2024.dat")
        pars = camb.CAMBparams()
        pars.set_cosmology(
            H0=67.7,
            ombh2=CONTROL_OMBH2,
            omch2=0.12,
            bbn_predictor=predictor,
        )

        self.assertAlmostEqual(pars.YHe, predictor.Y_He(CONTROL_OMBH2, 0.0), places=14)
        self.assertAlmostEqual(pars.get_Y_p(), predictor.Y_p(CONTROL_OMBH2, 0.0), places=14)


if __name__ == "__main__":
    unittest.main()
