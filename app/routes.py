from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SearchForm
from app.models import User, Flat, Flatcurrent
from app.scraping_scripts import runFlatSearch
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jakub S'}
    # Get user search criteria - hardcoded for the moment
    search_params = {
        'location': 'bemowo',
        'priceMin': '1',
        'priceMax': '500000',
        'pricePerM2min': '1',
        'pricePerM2max': '20000',
        'roomsNoSearch': '2',
        'flatSizeMin': '30',
        'flatSizeMax': '55',
        'market': 'wtorny'
    }
    flats = Flat.query.all()
    # return render_template('index.html', title='Strona Główna', user=user, search_params=search_params, offers=offers, flats=flats)
    return render_template('index.html', title='Strona Główna', user=user, search_params=search_params, flats=flats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Logowanie', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    search_paramsTemp = {}
    if form.validate_on_submit():
        search_paramsTemp["location"] = request.form["location"]
        search_paramsTemp["priceMin"] = request.form["priceMin"]
        search_paramsTemp["priceMax"] = request.form["priceMax"]
        search_paramsTemp["pricePerM2min"] = request.form["pricePerM2min"]
        search_paramsTemp["pricePerM2max"] = request.form["pricePerM2max"]
        search_paramsTemp["roomsNoSearch"] = request.form["roomsNoSearch"]
        search_paramsTemp["flatSizeMin"] = request.form["flatSizeMin"]
        search_paramsTemp["flatSizeMax"] = request.form["flatSizeMax"]
        search_paramsTemp["market"] = request.form["market"]
        search_params = json.dumps(search_paramsTemp)

        # # Clear current database:
        # Flatcurrent.delete()

        return redirect(url_for('search_results', search_params=search_params))
    return render_template('search_criteria.html', title='Wyszukiwanie', form=form)

@app.route('/testSearch')
def testSearch():
    # Get user search criteria - hardcoded for the moment
    search_params = {
        'location': 'bemowo',
        'priceMin': '1',
        'priceMax': '500000',
        'pricePerM2min': '1',
        'pricePerM2max': '20000',
        'roomsNoSearch': '2',
        'flatSizeMin': '30',
        'flatSizeMax': '55',
        'market': 'wtorny'
    }
    runFlatSearch.runFlatSearch(search_params)
    flats = Flat.query.all()
    flatsCurrent = Flatcurrent.query.all()
    return render_template('testSearch.html', title='Wyszukiwanie testowe', search_params=search_params, flats=flats, flatsCurrent=flatsCurrent)

@app.route('/search_results')
def search_results():

    search_paramsTemp1 = request.args.get('search_params')
    search_params = json.loads(search_paramsTemp1)
    runFlatSearch.runFlatSearch(search_params)
    flatsCurrent = Flatcurrent.query.all()
    return render_template('search_results.html', title='Wyniki wyszukiwania', search_params=json.loads(request.args.get('search_params')), flatsCurrent=flatsCurrent)from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SearchForm
from app.models import User, Flat, Flatcurrent
from app.scraping_scripts import runFlatSearch
import json
from threading import Thread

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jakub S'}
    # Get user search criteria - hardcoded for the moment
    search_params = {
        'location': 'bemowo',
        'priceMin': '1',
        'priceMax': '500000',
        'pricePerM2min': '1',
        'pricePerM2max': '20000',
        'roomsNoSearch': '2',
        'flatSizeMin': '30',
        'flatSizeMax': '55',
        'market': 'wtorny'
    }
    flats = Flat.query.all()
    # return render_template('index.html', title='Strona Główna', user=user, search_params=search_params, offers=offers, flats=flats)
    return render_template('index.html', title='Strona Główna', user=user, search_params=search_params, flats=flats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Logowanie', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    search_paramsTemp = {}
    if form.validate_on_submit():
        search_paramsTemp["location"] = request.form["location"]
        search_paramsTemp["priceMin"] = request.form["priceMin"]
        search_paramsTemp["priceMax"] = request.form["priceMax"]
        search_paramsTemp["pricePerM2min"] = request.form["pricePerM2min"]
        search_paramsTemp["pricePerM2max"] = request.form["pricePerM2max"]
        search_paramsTemp["roomsNoSearch"] = request.form["roomsNoSearch"]
        search_paramsTemp["flatSizeMin"] = request.form["flatSizeMin"]
        search_paramsTemp["flatSizeMax"] = request.form["flatSizeMax"]
        search_paramsTemp["market"] = request.form["market"]
        search_params = json.dumps(search_paramsTemp)

        # # Clear current database:
        # Flatcurrent.delete()

        return redirect(url_for('wait', search_params=search_params))
    return render_template('search_criteria.html', title='Wyszukiwanie', form=form)

@app.route('/testSearch')
def testSearch():
    # Get user search criteria - hardcoded for the moment
    search_params = {
        'location': 'bemowo',
        'priceMin': '1',
        'priceMax': '500000',
        'pricePerM2min': '1',
        'pricePerM2max': '20000',
        'roomsNoSearch': '2',
        'flatSizeMin': '30',
        'flatSizeMax': '55',
        'market': 'wtorny'
    }
    runFlatSearch.runFlatSearch(search_params)
    flats = Flat.query.all()
    flatsCurrent = Flatcurrent.query.all()
    return render_template('testSearch.html', title='Wyszukiwanie testowe', search_params=search_params, flats=flats, flatsCurrent=flatsCurrent)

@app.route('/search_results')
def search_results():

    # search_paramsTemp1 = request.args.get('search_params')
    search_params = json.loads(search_paramsTemp1)
    # runFlatSearch.runFlatSearch(search_params)
    flatsCurrent = Flatcurrent.query.all()
    return render_template('search_results.html', title='Wyniki wyszukiwania', search_params=json.loads(request.args.get('search_params')), flatsCurrent=flatsCurrent)

@app.route('/wait')
def wait():

    search_paramsTemp1 = request.args.get('search_params')
    search_params = json.loads(search_paramsTemp1)
    search_done = 0

    x = threading.Thread(target=thread_function, args=(1,))
x.start()
    while search_done == 0:
        return render_template('wait.html', title='Wyniki wyszukiwania', search_params=json.loads(request.args.get('search_params')))
        search_done = runFlatSearch.runFlatSearch(search_params)

    runFlatSearch.runFlatSearch(search_params)

    return redirect(url_for('search_results', search_params=search_params))
    # return render_template('search_results.html', title='Wyniki wyszukiwania', search_params=json.loads(request.args.get('search_params')), flatsCurrent=flatsCurrent)