from calc import CalcCapRate
import unittest
from copy import deepcopy


class CalcTestCase(unittest.TestCase):

    def setUp(self):
        self.test1_input = {'cash_on_cash': 10,
                            'target_ltv': 80,
                            'mezz_debt': 0,
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
                            'income_appr': 0,
                            'apprec_depr': 0,
                            'holding_period': 5}

        self.test1_output = {'first_mort': 0.0564,
                             'mezz': 0.000,
                             'calc_yield': 0.0298,
                             'amort_first_mort': -0.0083,
                             'amort_mezz': 0.000,
                             'appr': 0.000,
                             'cap_rate': 0.078,
                             'sinking_fund_factor': .1518,
                             'appr_depr_factor': 0.000,
                             'op_cap_rate': 0.07955}

        self.test021814_input = {'cash_on_cash': 8,
                                 'target_ltv': 85,
                                 'mezz_debt': 7.5,
                                 'transfer_cost': 2,
                                 'transfer_buyer_share': 50,
                                 'recordation_cost': 5,
                                 'recordation_buyer_share': 50,
                                 'finance': 1,
                                 'interest': 4.5,
                                 'amort': 30,
                                 'mezz_rate': 5,
                                 'mezz_interest_only': False,
                                 'mezz_secured': True,
                                 'mezz_amort': 30,
                                 'income_appr': 5,
                                 'apprec_depr': 5,
                                 'holding_period': 5}

        self.test021814_output = {'first_mort': 0.0495,
                                  'mezz': 0.0047,
                                  'calc_yield': 0.0183,
                                  'amort_first_mort': -0.0094,
                                  'amort_mezz': -0.0008,
                                  'appr': -0.0009,
                                  'cap_rate': 0.0628431,
                                  'sinking_fund_factor': .129819,
                                  'appr': -0.0009451,
                                  'op_cap_rate': 0.0642,
                                  'j_factor': 0.43973279,
                                  'cash_flow_growth': 0.0014,
                                  'irr': 0.21758509,
                                  'over_hold': 0.095,
                                  'debt_cov_first_y1': 1.2410,
                                  'debt_cov_first_oh': 1.2683,
                                  'debt_cov_mezz_y1': 1.1329,
                                  'debt_cov_mezz_oh': 1.1579}

    def test_basic_ingest_scenario_1(self):
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

    def run_scenario(self, input, output):
        c = CalcCapRate(input)
        r = c.iterate_computation()
        self.assertAlmostEqual(r['first_mort'], output['first_mort'], 3)
        self.assertAlmostEqual(r['mezz'], output['mezz'], 4)
        self.assertAlmostEqual(r['appr'], output['appr'], 4)
        self.assertAlmostEqual(r['amort_first_mort'], output['amort_first_mort'], 3)
        self.assertAlmostEqual(r['amort_mezz'], output['amort_mezz'], 4)
        self.assertAlmostEqual(r['cash_flow_growth'], output['cash_flow_growth'], 4)
        self.assertAlmostEqual(r['calc_yield'], output['calc_yield'], 3)
        self.assertAlmostEqual(r['irr'], output['irr'], 3)
        self.assertAlmostEqual(r['sinking_fund_factor'], output['sinking_fund_factor'], 4)
        self.assertAlmostEqual(r['cap_rate'], output['cap_rate'], 4)
        self.assertAlmostEqual(r['op_cap_rate'], output['op_cap_rate'], 4)
        self.assertAlmostEqual(r['over_hold'], output['over_hold'], 3)
        self.assertAlmostEqual(r['debt_cov_first_y1'], output['debt_cov_first_y1'], 3)
        self.assertAlmostEqual(r['debt_cov_first_oh'], output['debt_cov_first_oh'], 3)
        self.assertAlmostEqual(r['debt_cov_mezz_y1'], output['debt_cov_mezz_y1'], 3)
        self.assertAlmostEqual(r['debt_cov_mezz_oh'], output['debt_cov_mezz_oh'], 3)
        self.assertAlmostEqual(r['j_factor'], output['j_factor'], 3)
        return r

    def test_scenario_020814(self):
        self.run_scenario(self.test021814_input, self.test021814_output)

if __name__ == '__main__':
    unittest.main()
