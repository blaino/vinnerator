from calc import CalcCapRate
import unittest


class CalcTestCase(unittest.TestCase):

    def setUp(self):
        self.test1_input = {'cash_on_cash': 10,
                            'target_ltv': 80,
                            'transfer': {'cost': 2, 'buyer_share': 50},
                            'recordation': {'cost': 5, 'buyer_share': 50},
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

    def tearDown(self):
        pass

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
        c = CalcCapRate(self.test1_input)
        print ""

        print "irr: %.7f" % c.irr
        cap_rate = c.compute_cap_rate()
        print "cap_rate: %.7f" % cap_rate

        print "irr: %.7f" % c.irr
        cap_rate = c.compute_cap_rate()
        print "cap_rate: %.7f" % cap_rate

        print "irr: %.7f" % c.irr
        cap_rate = c.compute_cap_rate()
        print "cap_rate: %.7f" % cap_rate


        self.assertAlmostEqual(cap_rate, self.test1_cap_rate, 4)


if __name__ == '__main__':
    unittest.main()











