# tqpy : A compact, scalable, statistical analysis and reporting library built
# on top of pandas, used to assist in Yahoo! Traffic Quality investigations.
#
# Author : Rashad Alston <ralston@yahoo-inc.com>
# Python : 3.5.1
#
# License: BSD 3 Clause
#
# *************************************************************************

import unittest

import sys
sys.path.append("/Users/ralston/Desktop/Projects/tqpy")
import tqpy.visualizer as tqv
import tqpy.functions as tqf
import tqpy.reporter as tqr
import pandas as pd


class TestStringMethods(unittest.TestCase):

    def test_tqf_load_data(self):
        df = tqf.load_data("data/mb_test_data_small.csv", low_memory=False)
        self.assertIsInstance(df, pd.DataFrame)
        return df.columns.values

    def test_tqf_clean_names(self):
        df = tqf.load_data("data/mb_test_data_small.csv", low_memory=False)
        self.assertCountEqual(self.test_tqf_load_data(), df.columns.values, msg="Arrays are equal.")

if __name__ == '__main__':
    unittest.main()
