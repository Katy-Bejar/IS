import functools
from os import error
from flask import(
    render_template, Blueprint, flash, g, redirect, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from SIS_PEC.models.user import Usuario

from SIS_PEC import db

auth = Blueprint('auth', __name__, url_prefix='/administrador')

#Registrar un usuario 
@auth.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Usuario(username, generate_password_hash(password))

        error = None
        if not username:
            error = 'Se requiere nombre de usuario'
        elif not password:
            error = 'Se requiere contraseña'
        
        user_name = Usuario.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
        flash(error)
        
    return render_template('administrador/register.html')

#Iniciar Sesión
@auth.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        
        user = Usuario.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('evento.index'))
        
        flash(error)
        
    return render_template('administrador/login.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get_or_404(user_id)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('evento.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
