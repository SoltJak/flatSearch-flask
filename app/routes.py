from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, SearchForm
from app.models import User, Flat
from app.scraping_scripts import runFlatSearch

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jakobsen'}
    search_params = {
        'district': 'Bemowo',
        'rooms_no': '3',
        'price_max': '600000',
        'priceM2_max': '9000'
    }
    offers = [
        {
            'location': 'Bemowo',
            'rooms_no': '2',
            'price': '529000zł',
            'priceM2': '10580zł',
            'link': 'https://www.olx.pl/oferta/warszawa-bemowo-kossutha-3-pok-loggia-ogrodek-metro-CID3-IDDBV0o.html'
        },
        {
            'location': 'Wola',
            'rooms_no': '3',
            'price': '429000zł',
            'priceM2': '8250zł',
            'link': 'https://www.otodom.pl/oferta/rozkladowe-9-pietro-z-pieknym-widokiem-metro-ID45xYV.html'
        }
    ]
    flats = Flat.query.all()
    return render_template('index.html', title='Strona Główna', user=user, search_params=search_params, offers=offers, flats=flats)

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
    if form.validate_on_submit():
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))
        return redirect(url_for('search_criteria'))
    return render_template('search_criteria.html', title='Wyszukiwanie', form=form)

@app.route('/testSearch')
def testSearch():
    # Get user search criteria - hardcoded for the moment
    search_params = {
        'location': 'bemowo',
        'priceMin': '1',
        'priceMax': '450000',
        'pricePerM2min': '1',
        'pricePerM2max': '10000',
        'roomsNoSearch': '2',
        'flatSizeMin': '30',
        'flatSizeMax': '55',
        'market': 'wtorny'
    }
    runFlatSearch.runFlatSearch(search_params)
    flats = Flat.query.all()
    return render_template('testSearch.html', title='Wyszukiwanie testowe', search_params=search_params, flats=flats)