# -*- coding: utf-8 -*-

from .context import data_helpers as dh
from .context import keycodes as k

import numpy as np

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    # def test_absolute_truth_and_meaning(self):
    #     assert True

class DataHelperTestSuite(unittest.TestCase):
    """Data Helper test cases."""

    # read_from_file_to_arr tests
    def test_read_from_file_to_arr_short(self):
        test_file = './data/test/test_1.txt' # "1|2|3|4|5"
        expected_result = ['2', '3', '4', '5']
        self.assertEqual(dh.read_from_file_to_arr(test_file), expected_result)

    def test_read_from_file_to_arr_long(self):
        test_file = './data/test/test_2.txt' # "1|2|3|4|5"
        expected_result = ['66,332,71,66', '108,659,59,76', '105,241,157,73', '110,148,93,78', '100,83,89,68', '32,1240,87,32', '119,196,84,87', '111,186,58,79', '117,625,64,85', '108,1144,55,76', '100,86,112,68', '32,251,88,32', '101,197,124,69', '113,236,76,81', '117,445,67,85', '97,110,60,65', '108,151,76,76', '32,154,92,32', '119,218,78,87', '104,577,72,72', '105,308,55,73', '108,199,70,76', '101,64,88,69', '32,2785,92,32', '111,1999,92,79', '104,134,140,72', '32,160,156,32', '109,199,116,77', '114,128,172,82', '32,128,116,32', '100,305,96,68', '111,138,89,79', '32,68,104,32', '115,414,80,83', '116,314,56,84', '121,152,84,89', '108,113,100,76', '101,134,88,69', '46,656,84,190', '32,128,104,32', '76,281,64,76', '97,140,96,65', '105,120,139,73', '110,92,109,78', '32,100,100,32', '108,500,73,76', '101,60,52,69', '100,170,97,68', '32,80,96,32', '97,229,96,65', '110,124,106,78', '100,116,108,68', '32,68,112,32', '102,453,100,70', '97,373,130,65', '99,120,104,67', '116,222,104,84', '32,1046,80,32', '110,285,108,78', '111,215,152,79', '110,160,96,78', '101,92,88,69', '46,846,105,190', '32,88,96,32']
        self.assertEqual(dh.read_from_file_to_arr(test_file), expected_result)

    # keycode_obj test
    def test_most_keycodes_accounted_for(self):
        test_file = './data/keystrokes/participant_1.txt'
        data = dh.read_from_file_to_arr(test_file)
        expected_result = len(data)

        num_keystrokes_in_obj = 0
        for keystroke in data:
            if int(keystroke.split(',')[3]) in k.keycode_obj:
                num_keystrokes_in_obj += 1

        # At least 90% of keys are used
        self.assertGreater(num_keystrokes_in_obj / expected_result, 0.9)

    # encodings generation test
    def test_encoding_generation_single(self):
        data = ['x,x,x,68']
        result = dh.generate_encodings(data)

        self.assertEqual(np.sum(result), 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 32)
        self.assertEqual(result[0][3], 1)

    # def test_encoding_generation_multiple(self):

    # encoding concatenation test
    def test_encoding_concatenation_single(self):
        firstConcat = np.zeros(32)
        firstConcat[0] = 1
        secondConcat = np.zeros(32)
        secondConcat[4] = 1

        result = dh.concatenate_encodings([firstConcat, secondConcat])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[0][32 + 4], 1)
        self.assertEqual(np.sum(result[0]), 2)

    # def test_encoding_concatenation_single(self):

    def test_ks_seek_press(self):
        data = "32,251,88,32"
        expected_seek, expected_press = dh.ks_seek_press(data)
        self.assertEqual(expected_seek, 251)
        self.assertEqual(expected_press, 88)

    def test_calc_between_ks_timings(self):
        assert False

    def test_generate_digraph_vectors(self):
        assert False

    def test_clean_data(self):
        assert False


if __name__ == '__main__':
    unittest.main()