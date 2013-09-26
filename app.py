import os
from flask import Flask, send_from_directory, \
    request, session, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

# initialization
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/vinnerator_db"
# Need to: export DATABASE_URL="postgresql://localhost/vinnerator_db for following to work:"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['USERNAME'] = "admin"
app.config['PASSWORD'] = "password"
app.config['TESTING'] = True
app.secret_key = ')\xd4\xa0\xbf@\xce\x81tol\xdbrae\xd0\xc6\x0b#\xf1\xc5\x11@\xdd\xcc'
db = SQLAlchemy(app)


class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, default='Default title')
    text = db.Column(db.String(120), unique=True)

    cash_on_cash = db.Column(db.Float, unique=True)
    target_ltv = db.Column(db.Float, unique=True)
    transfer_cost = db.Column(db.Float, unique=True)
    transfer_buyer_share = db.Column(db.Float, unique=True)
    recordation_cost = db.Column(db.Float, unique=True)
    recordation_buyer_share = db.Column(db.Float, unique=True)
    finance = db.Column(db.Float, unique=True)
    interest = db.Column(db.Float, unique=True)
    amort = db.Column(db.Float, unique=True)
    mezz_rate = db.Column(db.Float, unique=True)
    mezz_interest_only = db.Column(db.Boolean, unique=True)
    mezz_secured = db.Column(db.Boolean, unique=True)
    mezz_amort = db.Column(db.Float, unique=True)
    apprec_depr = db.Column(db.Float, unique=True)
    holding_period = db.Column(db.Float, unique=True)

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Title %r>' % self.title


def init_db():
    db.create_all()


# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/paymentform')
def paymentform():
    return render_template('paymentform.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/show_scenarios')
def show_scenarios():
    if Scenario:
        scenarios = Scenario.query.all()
        print "Scenarios: " + str(scenarios)
    else:
        print "Scenario doesn't exist"
        scenarios = []
    return render_template('show_scenarios.html', scenarios=scenarios)


@app.route('/add', methods=['POST'])
def add_scenario():
    if not session.get('logged_in'):
        abort(401)
    scenario = Scenario(request.form['title'], request.form['text'])
    db.session.add(scenario)
    db.session.commit()
    flash('New scenario was successfully posted')
    return redirect(url_for('show_scenarios'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_scenarios'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

