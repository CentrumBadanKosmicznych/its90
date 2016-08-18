# -*- coding: utf-8 -*-
"""
@author: pgrudzinski
"""

import unittest
from its90 import prt
import numpy as np


class TestReferenceFunction(unittest.TestCase):

    def setUp(self):
        self.wr_range = np.linspace(0.216, 4.286, 10000)
        self.temp_range = np.linspace(-189.3442+273.15, 961.78+273.15, 10000)

    def test_reference_function_integrity(self):
        self.assertTrue(
            np.allclose(
                self.wr_range,
                prt.T_90(prt.W_r(self.wr_range)),
                rtol=0,
                atol=2e-4
            )
        )

class TestCalculation(unittest.TestCase):

    def setUp(self):
        self.sample_prt = {
            'R_TPW': 99.9968,
            'a4': -1.951465e-2,
            'b4': -1.742478e-4,
            'a': -1.949075e-2,
            'b': -2.148739e-4,
        }
        self.sample_data = np.recfromcsv('sample_cal.csv', delimiter='\t')

    def test_resistance(self):
        test_prt = prt.prt(**self.sample_prt)
        self.assertTrue(
            np.allclose(
                self.sample_data['resistance'],
                test_prt.resistance(self.sample_data['temperature']),
                rtol=0,
                atol=2e-4
            )
        )

    def test_temperature(self):
        test_prt = prt.prt(**self.sample_prt)
        self.assertTrue(
            np.allclose(
                self.sample_data['temperature'],
                test_prt.temperature(self.sample_data['resistance']),
                rtol=0,
                atol=2e-4
            )
        )

if __name__ == '__main__':
    unittest.main()