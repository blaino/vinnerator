import os
from flask import Flask, send_from_directory, \
    request, session, redirect, url_for, abort, render_template, flash
from flask.ext.mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from calc import CalcCapRate


# initialization
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/vinnerator_db"
# Need to: export DATABASE_URL="postgresql://localhost/vinnerator_db for following to work:"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['USERNAME'] = "admin"
app.config['PASSWORD'] = "password"
app.config['TESTING'] = False
app.config['DEBUG'] = True
app.secret_key = ')\xd4\xa0\xbf@\xce\x81tol\xdbrae\xd0\xc6\x0b#\xf1\xc5\x11@\xdd\xcc'
app.config['secret_key'] = ')\xd4\xa0\xbf@\xce\x81tol\xdbrae\xd0\xc6\x0b#\xf1\xc5\x11@\xdd\xcc'
app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/show_scenarios'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_POST_REGISTER_VIEW'] = '/show_scenarios'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db = SQLAlchemy(app)
mail = Mail(app)
app.extensions['mail'] = mail


# Models

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


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    cash_on_cash = db.Column(db.Float, unique=False)
    target_ltv = db.Column(db.Float, unique=False)
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
    apprec_depr = db.Column(db.Float, unique=False)
    holding_period = db.Column(db.Float, unique=False)

    cap_rate = db.Column(db.Float, unique=False)

    def __init__(self, title, cash_on_cash, target_ltv, transfer_cost,
                 transfer_buyer_share, recordation_cost, recordation_buyer_share,
                 finance, interest, amort, mezz_rate, mezz_interest_only,
                 mezz_secured, mezz_amort, apprec_depr, holding_period):
        self.title = title
        self.cash_on_cash = cash_on_cash
        self.target_ltv = target_ltv
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
        self.apprec_depr = apprec_depr
        self.holding_period = holding_period


    def __repr__(self):
        return '<Title %r>' % self.title


def init_db():
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    scenario = Scenario("default",  # title
                        10,  # cash_on_cash
                        80,  # target_ltv
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
                        0,  # apprec_depr
                        5)  # holding_period
    db.session.add(scenario)
    db.session.commit()


# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/paymentform')
@login_required
def paymentform():
    return render_template('paymentform.html')


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')


@app.route('/basic')
@app.route('/basic/<index>')
@login_required
def basic(index=0):
    index = int(index)
    try:
        scenarios = Scenario.query.all()
        c = CalcCapRate(scenarios[index].__dict__)
        result = c.iterate_computation()
        # Convert to percentages for output
        result.update((i, j*100) for i, j in result.items())
    except:
        scenarios = []
        result = {}
    return render_template('basic.html',
                           scenarios=scenarios,
                           result=result,
                           index=index)


@app.route('/show_scenarios')
@app.route('/show_scenarios/<index>')
@login_required
def show_scenarios(index=0):
    try:
        scenarios = Scenario.query.all()
        if index != 0:
            index = int(index)
        else:
            index = len(scenarios) - 1

        c = CalcCapRate(scenarios[index].__dict__)
        result = c.iterate_computation()
        # Convert to percentages for output
        result.update((i, j*100) for i, j in result.items())
    except:
        scenarios = []
        result = {}
    return render_template('show_scenarios.html',
                           scenarios=scenarios,
                           result=result,
                           index=index)


@app.route('/delete/<index>')
@login_required
def delete(index):
    index = int(index)
    print index
    try:
        scenarios = Scenario.query.all()
        db.session.delete(scenarios[index])
        db.session.commit()
    except:
        print "Could not delete scenario %d" % index
    print "about to redirect"
    return redirect(url_for('show_scenarios'))


@app.route('/add', methods=['POST'])
@login_required
def add_scenario():
    if not session.get('logged_in'):
        abort(401)
    print request
    scenario = Scenario(request.form['title'],
                        float(request.form['cash_on_cash']),
                        float(request.form['target_ltv']),
                        float(request.form['transfer_cost']),
                        float(request.form['transfer_buyer_share']),
                        float(request.form['recordation_cost']),
                        float(request.form['recordation_buyer_share']),
                        float(request.form['finance']),
                        float(request.form['interest']),
                        float(request.form['amort']),
                        float(request.form['mezz_rate']),
                        request.form['mezz_interest_only'],
                        request.form['mezz_secured'],
                        float(request.form['mezz_amort']),
                        float(request.form['apprec_depr']),
                        float(request.form['holding_period']))
    c = CalcCapRate(scenario.__dict__)
    result = c.iterate_computation()
    cap_rate = result['cap_rate']
    print "===cap rate: " + str(cap_rate)
    scenario.cap_rate = cap_rate

    db.session.add(scenario)
    db.session.commit()
    flash('New scenario was successfully posted')
    return redirect(url_for('show_scenarios'))


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
