from flask import(
    render_template as render, Blueprint, flash, g, redirect, request, url_for
)

# Importar los modelos
from my_app.models.auth.user import User

# Importar SQLAlchemy del archivo __init__.py
from my_app import db
from my_app.views.auth.auth import login_required

inbox = Blueprint('inbox', __name__)

@inbox.route("/")
@login_required
def index():
    user = User.get_by_id(1)
    avatar_name = user.user_name[0:2].upper()
    return render("inbox/index.html", avatar_name=avatar_name)

