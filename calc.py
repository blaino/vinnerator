from __future__ import division


class CalcCapRate():

    def __init__(self, s):
        self.cash_on_cash = s['cash_on_cash'] / 100
        self.target_ltv = s['target_ltv'] / 100
        self.transfer_cost = s['transfer']['cost'] / 100
        self.transfer_buyer_share = s['transfer']['buyer_share'] / 100
        self.recordation_cost = s['recordation']['cost']
        self.recordation_buyer_share = s['recordation']['buyer_share'] / 100
        self.finance = s['finance'] / 100
        self.interest = s['interest'] / 100
        self.amort = s['amort']
        self.mezz_rate = s['mezz_rate'] / 100
        self.mezz_interest_only = s['mezz_interest_only']
        self.mezz_secured = s['mezz_secured']
        self.mezz_amort = s['mezz_amort']
        self.apprec_depr = s['apprec_depr'] / 100
        self.holding_period = s['holding_period']


        self.first_mort = (self.target_ltv /
                           (1 + self.transfer_cost * self.transfer_buyer_share +
                            self.recordation_cost * self.recordation_buyer_share
                            / 1000 * self.target_ltv + self.finance * self.target_ltv))
        self.mezz_debt = 0
        self.equity = 1 - self.first_mort - self.mezz_debt
        self.const = self.interest / 12 / (1 - (1 / (1 + self.interest / 12) ** (self.amort * 12))) * 12
        self.per_loan_repaid = ((self.const - self.interest) /
                                (self.interest / 12 / (1 - (1 / (1 + self.interest / 12) **
                                                            (self.holding_period * 12))) * 12 - self.interest))
        if (self.mezz_interest_only):
            self.mezz_const = self.mezz_rate
        else:
            self.mezz_const = (self.mezz_rate / 12 / (1 - (1 / (1 + self.mezz_rate / 12) **
                                                           (self.mezz.amort * 12))) * 12)

        self.per_mezz_loan_repaid = ((self.mezz_const - self.mezz_rate) /
                                     (self.mezz_rate /12 / (1 - (1 / (1 + self.mezz_rate / 12) **
                                                                 (self.holding_period * 12))) * 12 - self.mezz_rate))
        self.irr = 0.10  # Initial seed
        self.sinking_fund_factor = self.irr / ((1 + self.irr) ** self.holding_period - 1)
        self.appr_depr_factor = self.apprec_depr * self.sinking_fund_factor

    def compute_cap_rate(self):
        print "irr: %.7f" % self.irr
        first_mort = self.first_mort * self.const
        mezz = self.mezz_debt * self.mezz_const
        calc_yield = self.equity * self.irr
        amort_first_mort = - (self.first_mort * self.per_loan_repaid * self.sinking_fund_factor)
        amort_mezz = - (self.mezz_debt * self.per_mezz_loan_repaid * self.sinking_fund_factor)
        appr = self.appr_depr_factor
        self.irr = (self.cash_on_cash * self.equity - amort_first_mort - amort_mezz-appr) / self.equity
        cap_rate = first_mort + mezz + calc_yield + amort_first_mort + amort_mezz + appr
        print "cap_rate: %.7f" % cap_rate
        return cap_rate

    def iterate_computation(self):
        cap_rate = self.compute_cap_rate()
        cap_rate = self.compute_cap_rate()
        cap_rate = self.compute_cap_rate()
        return cap_rate

    def compute_offer_prices_cap_rate():
        pass

















