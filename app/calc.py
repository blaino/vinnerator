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

    def compute_cap_rate(self):
        r = {}

        r['sinking_fund_factor'] = self.irr / ((1 + self.irr) ** self.holding_period - 1)
        r['appr_depr_factor'] = 0 - self.apprec_depr * r['sinking_fund_factor']
        r['first_mort'] = self.first_mort * self.const
        r['mezz'] = self.mezz_debt * self.mezz_const
        r['calc_yield'] = self.equity * self.irr
        r['amort_first_mort'] = (- (self.first_mort * self.per_loan_repaid * r['sinking_fund_factor'])
                                  )
        r['amort_mezz'] = - ((self.mezz_debt * self.per_mezz_loan_repaid * r['sinking_fund_factor'])
                            )
        r['appr'] = r['appr_depr_factor']

        self.irr = (self.cash_on_cash * self.equity - r['amort_first_mort'] -
                    r['amort_mezz'] - r['appr']) / self.equity
        r['irr'] = self.irr

        r['cap_rate'] = (r['first_mort'] + r['mezz'] + r['calc_yield'] +
                         r['amort_first_mort'] + r['amort_mezz'] + r['appr'])

        r['op_cap_rate'] = self.compute_offer_price_cap_rate(r)

        total = r['calc_yield'] + r['amort_first_mort'] + r['amort_mezz'] + r['appr']
        r['yield_per'] = total / r['calc_yield']
        r['amort_first_mort_per'] = 0 - r['amort_first_mort'] / r['calc_yield']
        r['amort_mezz_per'] = 0 - r['amort_mezz'] / r['calc_yield']
        r['appr_per'] = 0 - r['appr'] / r['calc_yield']

        return r

    def iterate_computation(self):
        delta = 999
        old = self.compute_cap_rate()
        epsilon = .000001
        while abs(delta) > epsilon:  # really should be checking delta on IRR, but works
            new = self.compute_cap_rate()
            delta = new['cap_rate'] - old['cap_rate']
            old = new
        new['j_factor'] = ((self.holding_period /
                            (1 - (1 + self.irr) ** (- self.holding_period)) - 1 / self.irr) *
                           new['sinking_fund_factor'])

        new = self.apply_jfactor(new)

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
        new['first_mort'] = new['first_mort'] / income_correction
        new['mezz'] = new['mezz'] / income_correction
        new['calc_yield'] = new['calc_yield'] / income_correction
        new['amort_first_mort'] = new['amort_first_mort'] / income_correction
        new['amort_mezz'] = new['amort_mezz'] / income_correction
        new['appr'] = new['appr'] / income_correction
        new['cap_rate'] = (new['first_mort'] + new['mezz'] + new['calc_yield'] +
                           new['amort_first_mort'] + new['amort_mezz'] + new['appr'])
        new['op_cap_rate'] = self.compute_offer_price_cap_rate(new)
        return new

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
