import os
from app import app, db
from flask import send_from_directory, \
    request, redirect, url_for, render_template, flash
from flask.ext.security import login_required, current_user
from calc import CalcCapRate
from app.models import Scenario


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


@app.route('/basic')
def basic():
    print "In basic route"
    scenario = default_scenario()
    c = CalcCapRate(scenario.__dict__)
    result = c.iterate_computation()
    # Convert to percentages for output
    result.update((i, j*100) for i, j in result.items())
    return render_template('basic.html',
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
                        0,  # apprec_depr
                        5)  # holding_period

    c = CalcCapRate(scenario.__dict__)
    result = c.iterate_computation()
    # Convert to percentages for output
    result.update((i, j*100) for i, j in result.items())
    cap_rate = result['cap_rate']
    scenario.cap_rate = cap_rate
    return render_template('basic.html',
                           scenario=scenario,
                           result=result)


@app.route('/show_scenarios')
@app.route('/show_scenarios/<index>')
@login_required
def show_scenarios(index=0):
    try:
        user_id = current_user.id
        scenarios = Scenario.query.filter_by(user_id=user_id).all()
        if len(scenarios) == 0:
            scenarios.append(default_scenario())
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
    try:
        scenarios = Scenario.query.all()
        db.session.delete(scenarios[index])
        db.session.commit()
    except:
        print "Could not delete scenario %d" % index
    return redirect(url_for('show_scenarios'))


@app.route('/add', methods=['POST'])
@login_required
def add_scenario():
    scenario = Scenario(request.form['title'],
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
                        float(request.form['mezz_rate']),
                        request.form['mezz_interest_only'],
                        request.form['mezz_secured'],
                        float(request.form['mezz_amort']),
                        float(request.form['apprec_depr']),
                        float(request.form['holding_period']),
                        current_user.id)
    c = CalcCapRate(scenario.__dict__)
    result = c.iterate_computation()
    cap_rate = result['cap_rate']
    print "===cap rate: " + str(cap_rate)
    scenario.cap_rate = cap_rate

    db.session.add(scenario)
    db.session.commit()
    flash('New scenario was successfully posted', 'alert alert-info')
    return redirect(url_for('show_scenarios'))


def default_scenario():
    return Scenario("default",  # title
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
                    False,  # mezz_interest_only
                    False,  # mezz_secured
                    30,  # mezz_amort
                    0,  # apprec_depr
                    5)  # holding_period
















