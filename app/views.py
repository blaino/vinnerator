import os
import re
from app import app, db
from flask import send_from_directory, \
    request, redirect, url_for, render_template, flash
from flask.ext.security import login_required, current_user
from calc import CalcCapRate
from app.models import Scenario
from forms import ScenarioForm
from postmark import PMMail


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = "Name: " + request.form['name']
    email = "Email: " + request.form['email']
    body = "Message: " + request.form['message']
    text_body = name + '\n' + email + '\n' + body

    message = PMMail(api_key=os.environ.get('POSTMARK_API_KEY'),
                     subject="Contact Message from Capulator",
                     sender="andrew@capulator.com",
                     to="blaine.m.nelson@gmail.com",
                     text_body=text_body,
                     tag="hello")

    message.send()
    return render_template('thanks.html')


@app.route('/basic')
def basic():
    scenario = default_scenario()
    c = CalcCapRate(scenario.__dict__)
    result = c.iterate_computation()
    # Convert to percentages for output
    result.update((i, j*100) for i, j in result.items())
    form = ScenarioForm(request.form)
    return render_template('basic.html',
                           form=form,
                           scenario=scenario,
                           result=result)


@app.route('/basic_calc', methods=['POST'])
def basic_calc():
    scenario = Scenario("basic",  # title
                        float(request.form['cash_on_cash']),
                        float(request.form['target_ltv']),
                        0,  # mezz_debt
                        0,  # transfer_cost
                        50,  # transfer_buyer_share
                        0,  # recordation_cost
                        50,  # recordation_buyer_share
                        0,  # finance
                        float(request.form['interest']),
                        float(request.form['amort']),
                        8,  # mezz_rate
                        False,  # mezz_interest_only
                        False,  # mezz_secured
                        30,  # mezz_amort
                        0,  # income_appr
                        0,  # apprec_depr
                        5)  # holding_period

    form = ScenarioForm(obj=scenario)
    form.title.data = "basic"  # For some reason, not picking this up from scenario

    if form.validate():
        c = CalcCapRate(scenario.__dict__)
        result = c.iterate_computation()
        # Convert to percentages for output
        result.update((i, j*100) for i, j in result.items())
        cap_rate = result['cap_rate']
        scenario.cap_rate = cap_rate
        return render_template('basic.html',
                               form=form,
                               scenario=scenario,
                               result=result)
    else:
        print "Not Validated."
        print form.errors
        return redirect(url_for('basic'))


@app.route('/show_scenarios')
@app.route('/show_scenarios/<db_id>')
@login_required
def show_scenarios(db_id=0):
    index = 0
    s_map = []
    db_id = int(db_id)
    user_id = current_user.id
    result = {}
    scenarios = []
    try:
        scenarios = Scenario.query.filter_by(user_id=user_id).all()
    except:
        print "Couldn't find any scenarios in db, so adding default scenario"
        scenario = default_scenario()
        scenarios.append(scenario)
        db.session.add(scenario)
        db.session.commit()

    s_len = len(scenarios)
    if s_len == 0:
        #print "Appending default scenario"
        scenarios.append(default_scenario())
    elif db_id > 0:
        #print "db_id: %s" % db_id
        s_map = [(scenarios[i].id, i) for i in range(s_len)]
        index = [s[1] for s in s_map if s[0] == db_id][0]
    else:
        index = s_len - 1
    c = CalcCapRate(scenarios[index].__dict__)
    result = c.iterate_computation()
    # Convert to percentages for output
    result.update((i, j*100) for i, j in result.items())

    form = ScenarioForm(request.form)
    return render_template('show_scenarios.html',
                           form=form,
                           scenarios=scenarios,
                           result=result,
                           index=index)


@app.route('/delete/<db_id>')
@login_required
def delete(db_id):
    if db_id != 'None':  # It's 'None' for the default scenario
        db_id = int(db_id)
        try:
            scenarios = Scenario.query.all()
            s_map = [(scenarios[i].id, i) for i in range(len(scenarios))]
            index = [s[1] for s in s_map if s[0] == db_id][0]
            db.session.delete(scenarios[index])
            db.session.commit()
        except:
            print "Could not delete scenario %d" % db_id
    return redirect(url_for('show_scenarios'))


def to_boolean(yesno):
    ''' Not validating here, just converting'''
    if re.match('[Yy].{0,2}', yesno):
        return True
    else:
        return False


def check_title(input_title):
    try:
        user_id = current_user.id
        scenarios = Scenario.query.filter_by(user_id=user_id).all()
    except:
        scenarios = []
    match = [s.title for s in scenarios if s.title == input_title]
    if match:
        last_index = 0
        m = re.search('(.*)\<(.*)\>', input_title)
        if m:  # If this name has already been used more than once
            input_title = m.group(1)
        last_index = get_last_scenario(scenarios, input_title)
        return "%s<%d>" % (input_title, last_index+1)
    else:
        return input_title


def get_last_scenario(scenarios, title_text):
    """
    Gets the last rev of a scenario.  Say there's x<1>, x<2>, x<13>.  Returns 13
    """
    matches = [s.title for s in scenarios if re.search(title_text + '<', s.title)]
    indices = [int(re.search('(.*)\<(.*)\>', m).group(2)) for m in matches]
    if indices:
        return max(indices)
    else:
        return 0


@app.route('/add', methods=['POST'])
@login_required
def add_scenario():
    checked_title = check_title(request.form['title'])
    if float(request.form['mezz_debt']) > 0:
        is_intr_only = to_boolean(request.form['mezz_interest_only'])
        is_secured = to_boolean(request.form['mezz_secured'])
        mezz_rate = float(request.form['mezz_rate'])
        mezz_amort = float(request.form['mezz_amort'])
    else:
        is_intr_only = to_boolean('no')
        is_secured = to_boolean('no')
        mezz_rate = 1
        mezz_amort = 1
    scenario = Scenario(checked_title,
                        float(request.form['cash_on_cash']),
                        float(request.form['target_ltv']),
                        float(request.form['mezz_debt']),
                        float(request.form['transfer_cost']),
                        float(request.form['transfer_buyer_share']),
                        float(request.form['recordation_cost']),
                        float(request.form['recordation_buyer_share']),
                        float(request.form['finance']),
                        float(request.form['interest']),
                        float(request.form['amort']),
                        mezz_rate,
                        is_intr_only,
                        is_secured,
                        mezz_amort,
                        float(request.form['income_appr']),
                        float(request.form['apprec_depr']),
                        float(request.form['holding_period']),
                        current_user.id)

    form = ScenarioForm(obj=scenario)

    if form.validate():
        c = CalcCapRate(scenario.__dict__)
        result = c.iterate_computation()
        cap_rate = result['cap_rate']
        #print "===cap rate: " + str(cap_rate)
        scenario.cap_rate = cap_rate

        db.session.add(scenario)
        db.session.commit()
        #flash('New scenario was successfully posted', 'alert alert-info')
        return redirect(url_for('show_scenarios') + '#results-column')
    else:
        print "Advanced calc input not validated."
        print form.errors
        return redirect(url_for('show_scenarios'))


def default_scenario():
    return Scenario("default",  # title
                    10.0,  # cash_on_cash
                    80.0,  # target_ltv
                    0.0,  # mezz_debt
                    2.0,  # transfer_cost
                    50.0,  # transfer_buyer_share
                    5.0,  # recordation_cost
                    50.0,  # recordation_buyer_share
                    1.0,  # finance
                    6.0,  # interest
                    30.0,  # amort
                    8.0,  # mezz_rate
                    False,  # mezz_secured
                    False,  # mezz_interest_only
                    30.0,  # mezz_amort
                    0.0,  # income_appr
                    0.0,  # apprec_depr
                    5.0)  # holding_period
