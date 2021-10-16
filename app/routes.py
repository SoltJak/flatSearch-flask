from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SearchForm
from app.models import User, Flat, Flatcurrent
from app.scraping_scripts import runFlatSearch
import json
import random, string

def get_random_string(length):
# get random string pf length 20 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    searchString = ''.join(random.choice(characters) for i in range(length))
    return searchString

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
    searchString = get_random_string(10)
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
        search_paramsTemp["source"] = request.form.getlist("source")
        search_paramsTemp["searchCode"] = searchString 
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
    # flatsCurrent = Flatcurrent.query.all()
    # print(flatsCurrent[0].roomsNo)
    flatsCurrent = Flat.query.all()
    print('Pierwsze: ' + str(flatsCurrent[0]) + ', ORAZ: ' + str(flatsCurrent[-1]))
    flatsCurrent = Flat.query.filter(Flat.searchCode == search_params['searchCode']).all()
    print('Search code: ' + search_params['searchCode'])
    print('Wybrane: ' + str(flatsCurrent[0]) + ', ORAZ: ' + str(flatsCurrent[-1]))
    return render_template('search_results.html', title='Wyniki wyszukiwania', search_params=json.loads(request.args.get('search_params')), flatsCurrent=flatsCurrent)