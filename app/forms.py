from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class SearchForm(FlaskForm):
    location = SelectField('Dzielnica', validators=[DataRequired()], choices=[('bemowo', 'Bemowo'), ('bielany', 'Bielany'), ('ochota', 'Ochota'), ('wola', 'Wola')])
    roomsNoSearch = SelectField('Liczba pokoi', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    flatSizeMin = DecimalField('Powierzchnia min', places=0)
    flatSizeMax = DecimalField('Powierzchnia max', places=0)
    priceMin = DecimalField('Cena min', places=0)
    priceMax = DecimalField('Cena max', places=0)
    pricePerM2min = DecimalField('Cena/m2 min', places=0)
    pricePerM2max = DecimalField('Cena/m2 max', places=0)
    market = SelectField('Rynek', choices=[('wtorny', 'Wtórny'), ('pierwotny', 'Pierwotny')])
    source = SelectMultipleField('Oferty z', choices=[('gratka', 'Gratka.pl'), ('gumtree', 'Gumtree.pl'), ('domiporta', 'Domiporta.pl'), ('nierOnline', 'Nieruchomości-Online.pl'), ('olx', 'OLX.pl'), ('sprzedajemy', 'Sprzedajemy.pl')])
    submit = SubmitField('Szukaj')