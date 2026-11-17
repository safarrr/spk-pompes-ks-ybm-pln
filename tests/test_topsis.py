import math
import unittest

from topsis import analyze, calculate, load_data


class TestTopsis(unittest.TestCase):
    def test_cost_and_benefit_manual_ideal_extremes(self):
        result = calculate([[1, 4], [2, 2]], [.6, .4], ["cost", "benefit"])
        self.assertEqual(result["scores"], [1, 0])
        self.assertAlmostEqual(result["normalized"][0][0], 1 / math.sqrt(5))
        self.assertAlmostEqual(result["normalized"][0][1], 4 / math.sqrt(20))
        self.assertAlmostEqual(result["positive"][0], .6 / math.sqrt(5))
        self.assertEqual(result["ranks"], [1, 2])

    def test_single_cost_analytic_middle(self):
        result = calculate([[0], [2], [4]], [1], ["cost"])
        self.assertEqual(result["scores"], [1, .5, 0])

    def test_weight_scale_invariance(self):
        a = calculate([[1, 2], [2, 1]], [.3, .7], ["cost", "benefit"])
        b = calculate([[1, 2], [2, 1]], [30, 70], ["cost", "benefit"])
        self.assertEqual(a["scores"], b["scores"])

    def test_zero_column_and_all_identical(self):
        result = calculate([[0, 5], [0, 5]], [1, 1], ["cost", "benefit"])
        self.assertEqual(result["normalized"][0][0], 0)
        self.assertEqual(result["scores"], [.5, .5])
        self.assertEqual(result["ranks"], [1, 1])

    def test_competition_ties(self):
        result = calculate([[0], [0], [3]], [1], ["cost"])
        self.assertEqual(result["ranks"], [1, 1, 3])
        self.assertEqual(result["order"], [0, 1, 2])

    def test_invalid_weights(self):
        for weights in [[0], [-1], [math.nan], [math.inf], [True]]:
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                calculate([[1]], weights, ["cost"])

    def test_nominal_income_is_used_as_cost(self):
        rows = load_data()
        result = analyze(rows)
        self.assertEqual(result["matrix"][0][0], rows[0]["Penghasilan (Rp)"])
        self.assertNotEqual(result["matrix"][0][0], rows[0]["C1 (Penghasilan)"])
        self.assertEqual(result["types"][0], "cost")
        self.assertEqual(result["positive"][0], min(row[0] for row in result["weighted"]))
        self.assertTrue(all(row[4] == 0 for row in result["plus_sq"]))
        self.assertTrue(all(row[4] == 0 for row in result["minus_sq"]))


if __name__ == "__main__":
    unittest.main()
