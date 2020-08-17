from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')

class SearchForm(FlaskForm):
    district = SelectField('Dzielnica', validators=[DataRequired()], choices=[('bemowo', 'Bemowo'), ('bielany', 'Bielany'), ('ochota', 'Ochota'), ('wola', 'Wola')])
    roomsNo = SelectField('Liczba pokoi', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    sizeMin = DecimalField('Powierzchnia min', places=0)
    sizeMax = DecimalField('Powierzchnia max', places=0)
    priceMin = DecimalField('Cena min', places=0)
    priceMax = DecimalField('Cena max', places=0)
    priceM2Min = DecimalField('Cena/m2 min', places=0)
    priceM2Max = DecimalField('Cena/m2 max', places=0)
    submit = SubmitField('Szukaj')