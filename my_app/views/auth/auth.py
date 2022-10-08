import email
import functools
# Importacion para ejecutar funciones de forma asíncrona
import threading
from flask import(
    render_template as render, Blueprint, flash, g, redirect, request, session, url_for
)

import base64
from werkzeug.security import generate_password_hash, check_password_hash

from my_app.utilities import send_email

# Importar SQLAlchemy del archivo __init__.py
from my_app import db

# Importar los modelos
from my_app.models.auth.user import User

# Importar los formularios
from my_app.forms.auth.register import RegisterForm
from my_app.forms.auth.login import LoginForm
from my_app.forms.auth.recover_password import RecoverPasswordForm
from my_app.forms.auth.reset_password import ResetPasswordForm


auth = Blueprint('auth', __name__, url_prefix= '/auth')

# Registrar Usuario
@auth.route('/register', methods=["GET", "POST"])
def register():
    # se cargar el formulario
    form = RegisterForm(request.form)
    error = None
    titulo = "Registrar - Quickly"  
    # si se accede por el metodo post y si no contiene errores 
    if request.method == 'POST' and form.validate():
        # se cargan los datos enviados desde el html
        user_name = form.user_name.data
        email = form.email.data
        password = form.password.data
        titulo = "Verificar correo - Quickly"
        # buscamos q no exista un usuario con el mismo nombre y/o email
        user = User.get_by_email_or_user_name(email, user_name)
        if user is not None:
            error = f'El nombre {user_name} o el email {email} ya está siendo utilizado por otro usuario'
        else:
            # cargamos el modelo User y se lo asignamos a la variable user
            user = User(user_name, email, False, generate_password_hash(password))
            # guardamos 
            db.session.add(user)
            db.session.commit()
            # obtenemos el id asignado a ese usuario en la base de datos
            id = user.id
            # encriptamos el id del usuario para asignarlo a la url q se adjuntara en el correo para activar la cuenta            
            id_bytes = str(id).encode('ascii')
            id_base64_bytes = base64.b64encode(id_bytes)
            id_base64 = id_base64_bytes.decode('ascii') 
            threading_emails = threading.Thread(target=send_email, args=("Activar cuenta Quickly", user, id_base64, 'activate_account'))
            threading_emails.start()
            return render('auth/verify_email.html', titulo=titulo, email=email)
        flash(error, 'error')
        return render('auth/register.html', titulo=titulo, form=form)
    else:
        return render('auth/register.html', titulo=titulo, form=form)

# Iniciar Session
@auth.route('/login', methods=["GET", "POST"])
def login():    
    form = LoginForm()
    titulo = "Iniciar sesion - Quickly"
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        error = None
        user = User.get_by_email(email)
        if user == None:
            error = "El correo electrónico no existe"
        elif user.active == False:
            error = "La cuenta no esta activa, revisa tu buzón de correos y activa la cuenta"
        elif not check_password_hash(user.password, password):
            error = "Contraseña incorrecta"
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('inbox.index'))
        flash(error, 'error')
        return render('auth/login.html', titulo=titulo, form=form)
    else:            
        return render('auth/login.html', titulo=titulo, form=form)


# Activar Cuenta
@auth.route('/activate_account')
def activate_account():        
    parametro = request.args.get('userId')    
    if parametro:
        id_base64_bytes = parametro.encode('ascii')
        id_bytes = base64.b64decode(id_base64_bytes)
        id_user = id_bytes.decode('ascii')
        
        user = User.get_by_id(id_user)
        if user is not None:
            user.active = True
            db.session.commit()
            return redirect(url_for('auth.login'))               
        else:
            return redirect('/not_found')
    else:
        return redirect('/not_found')


# Recuperar contraseña
@auth.route('/recover_password', methods=["GET", "POST"])
def recover_password():    
    form = RecoverPasswordForm()
    email = form.email.data
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.get_by_email_or_user_name(email, '')
        if user is not None:
            id = user.id
            id_bytes = str(id).encode('ascii')
            id_base64_bytes = base64.b64encode(id_bytes)
            id_base64 = id_base64_bytes.decode('ascii') 
            threading_emails = threading.Thread(target=send_email, args=("Restablecer contraseña de la cuenta Quickly", user, id_base64, 'recover_password'))
            threading_emails.start()
            flash(f"Hemos enviado un enlace a su dirección de correo electrónico: {email}, siga el enlace que se encuentra dentro para restablecer su contraseña de Quickly.")            
        else:
            flash(f"El correo {email} no existe", 'error')    
            
    titulo="Restablecer contraseña - Quickly"        
    return render('auth/recover_password.html', titulo=titulo, form=form)



# Cambiar contraseña
@auth.route('/reset_password', methods=["GET", "POST"])
def reset_password():    
    parametro = request.args.get('userId')
    form = ResetPasswordForm()
    titulo="Cambiar contraseña - Quickly"
    print(parametro)
    if request.method == 'POST' and form.validate(): 
        password = form.password.data
          
        if parametro:
            id_base64_bytes = parametro.encode('ascii')
            id_bytes = base64.b64decode(id_base64_bytes)
            id_user = id_bytes.decode('ascii')
            print(id_user)
            user = User.get_by_id(id_user)

            if user is not None:                
                user.password = generate_password_hash(password)
                db.session.commit()
                flash(f"La contraseña se restablecio correctamente")
                return redirect(url_for('auth.login'))
            else:
                flash(f"Error de autenticacion 160", 'error')        
        else:
            if g.user is None:
                flash(f"Error de autenticacion", 'error')                
            else:
                user = User.get_by_id(g.user.id)
                user.password = generate_password_hash(password)
                db.session.commit()
                session.clear()
                flash(f"La contraseña se restablecio correctamente")
                return redirect(url_for('auth.login'))
            
    return render('auth/reset_password.html', titulo=titulo, form=form)




# Verificar usuario logueado
@auth.before_app_request
def load_logged_in_user():
    # Obtener id de usuario logueado
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        # se puede usar solo get pero para traer errores se usa get_or_404 
        # se obtiene el usuario logueado
        g.user = User.query.get_or_404(user_id)


# Cerrar Session
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

# Para restringir las vistas q necesiten de inicio de session
def login_required(view):
    # este decorador verifica si esta logueado para retornar al login
    @functools.wraps(view)
    # **kwargs Argumentos indefinidos por nombre
    def wrapped_view(**kwargs):
        # si g no contienen ningun usuario pailas nos vamos para el login 
        if g.user is None:
            return redirect(url_for('auth.login'))
        # De lo contrario retorna la vista
        return view(**kwargs)
    return wrapped_view