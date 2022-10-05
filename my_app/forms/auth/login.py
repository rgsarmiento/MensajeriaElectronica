from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    #user_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired('Este campo es requerido'), Email('Dirección de correo electrónico no válida')])
    password = PasswordField('Password', validators=[DataRequired('Este campo es requerido'), Length(min=8, message='Minimo 8 caracteres')])        
    