from flask import Flask, render_template as render
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cargar configuraciones
app.config.from_object('config.DevelopmenConfig')

# variables para el uso de SQLAlchemy
db = SQLAlchemy(app)

#importar vistas
from my_app.views.auth import auth
app.register_blueprint(auth)


#ejecutar todos los querys
db.create_all()


def page_400(error):
    return render('404.html'), 404