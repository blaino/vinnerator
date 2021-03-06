from __future__ import division


class CalcCapRate():

    def __init__(self, s):
        self.cash_on_cash = s['cash_on_cash'] / 100
        self.target_ltv = s['target_ltv'] / 100
        self.mezz_debt = s['mezz_debt'] / 100
        self.transfer_cost = s['transfer_cost'] / 100
        self.transfer_buyer_share = s['transfer_buyer_share'] / 100
        self.recordation_cost = s['recordation_cost']
        self.recordation_buyer_share = s['recordation_buyer_share'] / 100
        self.finance = s['finance'] / 100
        self.interest = s['interest'] / 100
        self.amort = s['amort']
        self.mezz_rate = s['mezz_rate'] / 100
        self.mezz_interest_only = s['mezz_interest_only']
        self.mezz_secured = s['mezz_secured']
        self.mezz_amort = s['mezz_amort']
        self.income_appr = s['income_appr'] / 100
        self.apprec_depr = s['apprec_depr'] / 100
        self.holding_period = s['holding_period']
        self.sales_costs = 2 / 100


        self.first_mort = (self.target_ltv /
                           (1 + self.transfer_cost * self.transfer_buyer_share +
                            self.recordation_cost * self.recordation_buyer_share
                            / 1000 * self.target_ltv + self.finance * self.target_ltv))
        self.equity = 1 - self.first_mort - self.mezz_debt
        self.const = self.interest / 12 / (1 - (1 / (1 + self.interest / 12) ** (self.amort * 12))) * 12
        self.per_loan_repaid = ((self.const - self.interest) /
                                (self.interest / 12 / (1 - (1 / (1 + self.interest / 12) **
                                                            (self.holding_period * 12))) * 12 - self.interest))
        if (self.mezz_interest_only):
            self.mezz_const = self.mezz_rate
        else:
            self.mezz_const = (self.mezz_rate / 12 / (1 - (1 / (1 + self.mezz_rate / 12) **
                                                           (self.mezz_amort * 12))) * 12)

        if (self.mezz_rate > 0):
            self.per_mezz_loan_repaid = ((self.mezz_const - self.mezz_rate) /
                                         (self.mezz_rate / 12 / (1 - (1 / (1 + self.mezz_rate / 12) **
                                                                      (self.holding_period * 12))) * 12 - self.mezz_rate))
        else:
            self.per_mezz_loan_repaid = 0

        self.irr = 0.10  # Initial seed
        self.formula = 0.10  # Initial seed

    def compute_cap_rate(self):
        r = {}

        r['cash_on_cash'] = self.cash_on_cash
        r['sinking_fund_factor'] = self.irr / ((1 + self.irr) ** self.holding_period - 1)

        r['first_mort'] = self.first_mort * self.const
        r['mezz'] = self.mezz_debt * self.mezz_const
        #r['calc_yield'] = self.equity * self.irr
        r['calc_yield'] = self.equity * self.cash_on_cash
        r['amort_first_mort'] = (- (self.first_mort * self.per_loan_repaid * r['sinking_fund_factor'])
                                  )
        r['amort_mezz'] = - ((self.mezz_debt * self.per_mezz_loan_repaid * r['sinking_fund_factor'])
                            )

        if self.mezz_secured:
            mezzx = self.recordation_cost * self.recordation_buyer_share / 1000 * self.mezz_debt
        else:
            mezzx = 0

        r['appr'] = (-(1 + self.apprec_depr - self.sales_costs * (1 + self.apprec_depr) -
                       (1 + self.transfer_cost * self.transfer_buyer_share +
                        self.recordation_cost * self.recordation_buyer_share / 1000 *
                        self.target_ltv + self.finance * self.target_ltv + self.finance *
                        self.mezz_debt + mezzx)) *
                      (r['sinking_fund_factor'] /
                       (1 + self.transfer_cost * self.transfer_buyer_share / 1000 *
                        self.target_ltv + self.finance * self.target_ltv + self.finance *
                        self.mezz_debt + mezzx)))

        r['j_factor'] = ((self.holding_period /
                          (1 - (1 + self.irr) ** (- self.holding_period)) - 1 / self.irr) *
                         r['sinking_fund_factor'])
        r = self.apply_jfactor(r)

        self.irr = ((self.cash_on_cash * self.equity + self.income_appr *
                     r['j_factor'] * r['cap_rate'] -
                     (1 + self.income_appr * r['j_factor']) *
                     (r['amort_first_mort'] + r['amort_mezz'] + r['appr']))
                    / self.equity)

        r['irr'] = self.irr

        r = self.calc_output_percents(r)

        return r

    def iterate_computation(self):
        delta = 999
        old = self.compute_cap_rate()
        epsilon = .000000001
        while abs(delta) > epsilon:  # really should be checking delta on IRR, but works
            new = self.compute_cap_rate()
            delta = new['cap_rate'] - old['cap_rate']
            old = new
            print "old, new: %s, %s" % (old['cap_rate'], new['cap_rate'])
        return new

    def apply_jfactor(self, new):
        '''
        When comparing capulator to the spreadsheet the application of
        the jfactor can be confusing.  It's ambiguous in the
        spreadsheet whether or not you should iterate on jfactor in
        addition to iterating on IRR, but the intent is to only
        iterate on IRR.  Andrew's intent: jfactor is a correction
        applied after the IRR iteration has settled down.
        '''
        income_correction = (1 + self.income_appr * new['j_factor'])
        self.formula = ((self.first_mort * self.const + self.mezz_debt * self.mezz_const +
                         self.cash_on_cash * self.equity + new['j_factor'] * self.formula) /
                        income_correction)
        new['first_mort'] = new['first_mort'] / income_correction
        new['mezz'] = new['mezz'] / income_correction
        new['amort_first_mort'] = new['amort_first_mort'] / income_correction
        new['amort_mezz'] = new['amort_mezz'] / income_correction
        new['appr'] = new['appr'] / income_correction
        new['calc_yield'] = (new['calc_yield'] / income_correction -
                             (new['amort_first_mort'] + new['amort_mezz'] + new['appr']))
        new['cash_flow_growth'] = ((self.income_appr * new['j_factor'] *
                                    (self.first_mort * self.const + self.mezz_debt *
                                     self.mezz_const + self.cash_on_cash * self.equity +
                                     self.income_appr * new['j_factor'] * self.formula) /
                                    income_correction**2))
        new['cap_rate'] = (new['first_mort'] + new['mezz'] + new['calc_yield'] +
                           new['amort_first_mort'] + new['amort_mezz'] + new['appr'] +
                           new['cash_flow_growth'])
        new['op_cap_rate'] = self.compute_offer_price_cap_rate(new)

        new['over_hold'] = ((1 + self.income_appr * new['j_factor']) *
                            (new['calc_yield'] + new['cash_flow_growth'] + new['amort_first_mort'] +
                             new['amort_mezz'] + new['appr']) / self.equity)

        new['unleveraged_irr'] = 9999
        new['debt_cov_first_y1'] = (1 / ((self.first_mort * self.const) / new['cap_rate']))
        new['debt_cov_first_oh'] = (1 / ((self.first_mort * self.const) / new['cap_rate']) *
                                    (1 + self.income_appr * new['j_factor']))
        new['debt_cov_mezz_y1'] = (1 / ((self.first_mort * self.const + self.mezz_debt * self.mezz_const) /
                                        new['cap_rate']))
        new['debt_cov_mezz_oh'] = (1 / ((self.first_mort * self.const + self.mezz_debt * self.mezz_const) /
                                        new['cap_rate']) * (1 + self.income_appr * new['j_factor']))
        return new

    def calc_output_percents(self, r):
        r['loan_paydown_per'] = ((- r['amort_first_mort']) /
                                 (r['calc_yield'] + r['cash_flow_growth']))
        r['loan_paydown_mezz_per'] = ((- r['amort_mezz']) /
                                      (r['calc_yield'] + r['cash_flow_growth']))
        r['base_cash_flow_per'] = ((r['calc_yield'] + r['amort_first_mort'] +
                                    + r['amort_mezz'] + r['appr']) /
                                   (r['calc_yield'] + r['cash_flow_growth']))
        r['cash_flow_growth_per'] = (r['cash_flow_growth'] /
                                     (r['calc_yield'] + r['cash_flow_growth']))
        r['gain_on_sale_per'] = (- (r['appr'] / (r['calc_yield'] + r['cash_flow_growth'])))
        return r

    def compute_offer_price_cap_rate(self, r):
        def calc_secured_factor():
            if self.mezz_secured == True:
                return self.recordation_cost * self.transfer_buyer_share / 1000 * self.mezz_debt
            else:
                return 0
        return r['cap_rate'] * (
            1 + self.transfer_cost * self.transfer_buyer_share +
            self.recordation_cost * self.transfer_buyer_share / 1000 * self.first_mort +
            self.finance * self.first_mort + self.finance * self.mezz_debt +
            calc_secured_factor())
