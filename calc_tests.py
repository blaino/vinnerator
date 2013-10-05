from calc import CalcCapRate
import unittest
from copy import deepcopy


class CalcTestCase(unittest.TestCase):

    def setUp(self):
        self.test1_input = {'cash_on_cash': 10,
                            'target_ltv': 80,
                            'transfer_cost': 2,
                            'transfer_buyer_share': 50,
                            'recordation_cost': 5,
                            'recordation_buyer_share': 50,
                            'finance': 1,
                            'interest': 6,
                            'amort': 30,
                            'mezz_rate': 8,
                            'mezz_interest_only': True,
                            'mezz_secured': False,
                            'mezz_amort': 30,
                            'apprec_depr': 0,
                            'holding_period': 5}
        self.test1_cap_rate = .078

        # Same as test1 but cash_on_cash is 20%
        self.test2_input = deepcopy(self.test1_input)
        self.test2_input['cash_on_cash'] = 20
        self.test2_cap_rate = .0996

    def test_init_scenario_1(self):
        c = CalcCapRate(self.test1_input)
        self.assertEqual(c.cash_on_cash, 0.10)
        self.assertEqual(c.interest, 0.06)
        self.assertEqual(c.holding_period, 5)
        self.assertAlmostEqual(c.first_mort, 0.78, 2)
        self.assertAlmostEqual(c.equity, 0.22, 2)
        self.assertAlmostEqual(c.const, 0.0719, 2)
        self.assertAlmostEqual(c.per_loan_repaid, 0.0695, 2)
        self.assertAlmostEqual(c.mezz_const, 0.08, 2)
        self.assertAlmostEqual(c.per_mezz_loan_repaid, 0.0, 2)

    def test_scenario_1(self):
        self.run_scenario(self.test1_input, self.test1_cap_rate)

    def test_scenario_2(self):
        self.run_scenario(self.test2_input, self.test2_cap_rate)

    def run_scenario(self, input, output):
        c = CalcCapRate(input)
        result = c.iterate_computation()
        cap_rate = result['cap_rate']

        self.assertAlmostEqual(cap_rate, output, 4)


if __name__ == '__main__':
    unittest.main()











