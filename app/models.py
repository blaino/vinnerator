from app import app, db
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    scenarios = db.relationship('Scenario',
                                backref=db.backref('user', lazy='joined'),
                                lazy='dynamic')


# Setup Flsak-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    cash_on_cash = db.Column(db.Float, unique=False)
    target_ltv = db.Column(db.Float, unique=False)
    mezz_debt = db.Column(db.Float, unique=False)
    transfer_cost = db.Column(db.Float, unique=False)
    transfer_buyer_share = db.Column(db.Float, unique=False)
    recordation_cost = db.Column(db.Float, unique=False)
    recordation_buyer_share = db.Column(db.Float, unique=False)
    finance = db.Column(db.Float, unique=False)
    interest = db.Column(db.Float, unique=False)
    amort = db.Column(db.Float, unique=False)
    mezz_rate = db.Column(db.Float, unique=False)
    mezz_interest_only = db.Column(db.Boolean, unique=False)
    mezz_secured = db.Column(db.Boolean, unique=False)
    mezz_amort = db.Column(db.Float, unique=False)
    income_appr = db.Column(db.Float, unique=False)
    apprec_depr = db.Column(db.Float, unique=False)
    holding_period = db.Column(db.Float, unique=False)

    cap_rate = db.Column(db.Float, unique=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title='empty', cash_on_cash=0, target_ltv=0, mezz_debt=0,
                 transfer_cost=0, transfer_buyer_share=0, recordation_cost=0,
                 recordation_buyer_share=0, finance=0, interest=0, amort=0, mezz_rate=0,
                 mezz_interest_only=False, mezz_secured=False, mezz_amort=0,
                 income_appr=0, apprec_depr=0,
                 holding_period=0, user_id=0):
        self.title = title
        self.cash_on_cash = cash_on_cash
        self.target_ltv = target_ltv
        self.mezz_debt = mezz_debt
        self.transfer_cost = transfer_cost
        self.transfer_buyer_share = transfer_buyer_share
        self.recordation_cost = recordation_cost
        self.recordation_buyer_share = recordation_buyer_share
        self.finance = finance
        self.interest = interest
        self.amort = amort
        self.mezz_rate = mezz_rate
        self.mezz_interest_only = mezz_interest_only
        self.mezz_secured = mezz_secured
        self.mezz_amort = mezz_amort
        self.income_appr = income_appr
        self.apprec_depr = apprec_depr
        self.holding_period = holding_period
        self.user_id = user_id

    def __repr__(self):
        return '<Title %r>' % self.title


def init_db():
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db.session.commit()
    users = User.query.all()
    user_id = users[0].id
    scenario = Scenario("default",  # title
                        10,  # cash_on_cash
                        80,  # target_ltv
                        0,  # mezz_debt
                        2,  # transfer_cost
                        50,  # transfer_buyer_share
                        5,  # recordation_cost
                        50,  # recordation_buyer_share
                        1,  # finance
                        6,  # interest
                        30,  # amort
                        8,  # mezz_rate
                        True,  # mezz_interest_only
                        False,  # mezz_secured
                        30,  # mezz_amort
                        0,  # income_appr
                        0,  # apprec_depr
                        5,  # holding_period
                        user_id)
    db.session.add(scenario)
    db.session.commit()


def tear_down_db():
    db.session.remove()
    db.drop_all()
