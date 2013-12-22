from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import TextField, DecimalField, IntegerField, BooleanField, validators


class MyForm(Form):
    name = TextField('name', validators=[DataRequired()])
    level = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])


class ScenarioForm(Form):
    title = TextField('title', validators=[DataRequired()])
    cash_on_cash = DecimalField('cash_on_cash', [validators.NumberRange(min=0, max=100)])
    target_ltv = DecimalField('target_ltv', [validators.NumberRange(min=0, max=100)])
    mezz_debt = DecimalField('mezz_debt', [validators.NumberRange(min=0, max=100)])
    transfer_cost = DecimalField('transfer_cost', [validators.NumberRange(min=0, max=100)])
    transfer_buyer_share = DecimalField('transfer_buyer_share', [validators.NumberRange(min=0, max=100)])
    recordation_cost = DecimalField('recordation_cost', [validators.NumberRange(min=0, max=100)])
    recordation_buyer_share = DecimalField('recordation_buyer_share', [validators.NumberRange(min=0, max=100)])
    finance = DecimalField('finance', [validators.NumberRange(min=0, max=100)])
    interest = DecimalField('interest', [validators.NumberRange(min=0, max=100)])
    amort = DecimalField('amort', [validators.NumberRange(min=0, max=100)])

    mezz_rate = DecimalField('mezz_rate', [validators.NumberRange(min=0, max=100)])
    mezz_interest_only = BooleanField('mezz_interest_only')
    mezz_secured = BooleanField('mezz_secured')
    mezz_amort = DecimalField('mezz_amort', [validators.NumberRange(min=0, max=100)])

    apprec_depr = DecimalField('apprec_depr', [validators.NumberRange(min=0, max=100)])
    holding_period = DecimalField('holding_period', [validators.NumberRange(min=0, max=100)])
