from email import message
from flask import(
    render_template as render, Blueprint, flash, g, redirect, request, url_for
)

# Importar los modelos
from my_app.models.auth.user import User
from my_app.models.inbox.message import Message

# Importar formularios

from my_app.forms.inbox.message import MessageForm

# Importar SQLAlchemy del archivo __init__.py
from my_app import db
from my_app.views.auth.auth import login_required

inbox = Blueprint('inbox', __name__)

@inbox.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = MessageForm()       
    form.users.choices=[(s.id, s.user_name+" "+s.email) for s in (User.get_all_except_me(g.user.id))] 
    user = User.get_by_id(g.user.id)
    avatar_name = user.user_name[0:2].upper()
    error = None

    if request.method == 'POST':
        if form.users.data and form.message.data != '<p><br></p>' and form.subject.data:

            for user in form.users.data:
                message = Message(g.user.id, user, form.subject.data, form.message.data, 0)
                
                db.session.add(message)
                db.session.commit()

            flash('Mensaje enviado correctamente')
            return redirect(url_for('inbox.index'))        
        else:
            error= "Los campos de: para, asunto y mensaje son  obligatorios para el envio de mensajes"
    if error is not None:
        flash(error, 'error')

    received_messages_new =Message.get_all_received_new(g.user.id)    
    sent_messages = Message.get_all_sent(g.user.id)
    received_messages = Message.get_all_received(g.user.id)

    return render("inbox/index.html", to_html=Message.to_html, user_get_by_id=User.get_by_id, avatar_name=avatar_name, received_messages=received_messages, sent_messages=sent_messages, received_messages_new=received_messages_new, form=form)

@inbox.route("/update")
@login_required
def update():
    parametro = request.args.get('messageId')
    if parametro:                
        message = Message.get_by_id(parametro)
        if message is not None:
            message.status = 1
            db.session.commit()
            return redirect(url_for('inbox.index'))            
        

