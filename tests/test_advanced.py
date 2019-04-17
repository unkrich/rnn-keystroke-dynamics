# -*- coding: utf-8 -*-

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    # def test_absolute_truth_and_meaning(self):
    #     assert True

class ModelDataTestSuite(unittest.TestCase):
    """Advanced test cases."""

    # def test_absolute_truth_and_meaning(self):
    #     assert True

    def test_model_creation(self):
    	assert False

	def test_model_get_training(self):
		assert False

	def test_model_get_testing(self):
		assert False



if __name__ == '__main__':
    unittest.main()