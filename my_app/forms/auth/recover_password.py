from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class RecoverPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Este campo es requerido'), Email('Dirección de correo electrónico no válida')])
   