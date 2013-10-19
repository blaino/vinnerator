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

        self.test1_output = {'first_mort': 0.0564,
                             'mezz': 0.000,
                             'calc_yield': 0.0298,
                             'amort_first_mort': -0.0083,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.078}

        # Same as test1 but cash_on_cash is 20%
        self.test2_input = deepcopy(self.test1_input)
        self.test2_input['cash_on_cash'] = 20
        self.test2_output = {'first_mort': 0.056428,
                             'mezz': 0.000,
                             'calc_yield': 0.050019,
                             'amort_first_mort': -0.006876,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.099571}


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
        self.run_scenario(self.test1_input, self.test1_output)

    def test_scenario_2(self):
        self.run_scenario(self.test2_input, self.test2_output)

    def run_scenario(self, input, output):
        c = CalcCapRate(input)
        r = c.iterate_computation()
        self.assertAlmostEqual(r['first_mort'], output['first_mort'], 4)
        self.assertAlmostEqual(r['mezz'], output['mezz'], 4)
        self.assertAlmostEqual(r['calc_yield'], output['calc_yield'], 4)
        self.assertAlmostEqual(r['amort_first_mort'], output['amort_first_mort'], 4)
        self.assertAlmostEqual(r['amort_mezz'], output['amort_mezz'], 4)
        self.assertAlmostEqual(r['appr'], output['appr'], 4)
        self.assertAlmostEqual(r['cap_rate'], output['cap_rate'], 4)


if __name__ == '__main__':
    unittest.main()











