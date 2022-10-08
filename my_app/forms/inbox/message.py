from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    users = SelectMultipleField('Para: ', validate_choice = False, validators=[DataRequired('Este campo es requerido')])
    subject = StringField('Asunto: ', validators=[DataRequired('Este campo es requerido'), Length(max=100, message='Maximo 200 caracteres')])
    message = HiddenField('mensaje', validators=[DataRequired('Este campo es requerido')])
