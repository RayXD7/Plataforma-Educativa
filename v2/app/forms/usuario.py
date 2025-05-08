from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(min=6, max=120)])