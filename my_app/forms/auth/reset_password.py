from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetPasswordForm(FlaskForm):    
    password = PasswordField('Nueva contraseña', validators=[DataRequired('Este campo es requerido'), EqualTo('confirm', message='Las contraseñas deben coincidir'), Length(min=8, message='Minimo 8 caracteres')])        
    confirm = PasswordField('Confirmar la contraseña')
    