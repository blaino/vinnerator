from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import TextField, DecimalField, IntegerField, BooleanField, validators

class MyForm(Form):
    name = TextField('name', validators=[DataRequired()])
    level = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])


class ScenarioForm(Form):
    title = TextField('title', validators=[DataRequired()])
    #title = TextField('title')
    cash_on_cash = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    target_ltv = DecimalField('target_ltv', [validators.NumberRange(min=0, max=100)])
    mezz_debt = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    transfer_cost = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    transfer_buyer_share = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    recordation_cost = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    recordation_buyer_share = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    finance = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    interest = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    amort = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    mezz_rate = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])

    # mezz_interest_only = BooleanField('cash_on_cash', [validators.Required()])
    # mezz_secured = BooleanField('mezz_secured', [validators.Required()])
    mezz_interest_only = BooleanField('cash_on_cash')
    mezz_secured = BooleanField('mezz_secured')

    mezz_amort = DecimalField('mezz_amort', [validators.NumberRange(min=0, max=100)])
    apprec_depr = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    holding_period = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])









