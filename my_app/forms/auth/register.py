from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    user_name = StringField('Nombre usuario', validators=[DataRequired('Este campo es requerido'), Length(max=64, message='Maximo 64 caracteres')])
    email = StringField('Correo electrónico', validators=[DataRequired('Este campo es requerido'), Email('Dirección de correo electrónico no válida')])
    password = PasswordField('Contraseña', validators=[DataRequired('Este campo es requerido'), EqualTo('confirm', message='Las contraseñas deben coincidir'), Length(min=8, message='Minimo 8 caracteres')])        
    confirm = PasswordField('Repita la contraseña')
    privacy_policy = BooleanField('Estoy de acuerdo con', validators=[DataRequired('Debe aceptar la política de privacidad y términos')])    
    