#CONTROLLER EVENTO

from operator import pos
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

from werkzeug.exceptions import abort

from SIS_PEC.models.evento import Evento
from SIS_PEC.models.user import Usuario

from SIS_PEC.controllers.auth import login_required

from SIS_PEC import db

evento = Blueprint('evento', __name__)

#Obtner un ususario
def get_user(id):
    user = Usuario.query.get_or_404(id)
    return user

@evento.route("/")
def index():
    eventos = Evento.query.all()
    eventos = list(reversed(eventos))
    db.session.commit()
    return render_template('evento/index.html', eventos = eventos, get_user=get_user)

#Registrar un evento 
@evento.route('/evento/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        place = request.form.get('place')

        evento = Evento(g.user.id, title, body, place)

        error = None
        if not title:
            error = 'Se requiere un título'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(evento)
            db.session.commit()
            return redirect(url_for('evento.index'))
        
        flash(error)
        
    return render_template('evento/create.html')

def get_post(id, check_author=True):
    evento = Evento.query.get(id)

    if evento is None:
        abort(404, f'Id {id} de la publicación no existe.')

    if check_author and evento.author != g.user.id:
        abort(404)
    
    return evento



#Update evento 
@evento.route('/evento/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    evento = get_post(id) 

    if request.method == 'POST':
        evento.title = request.form.get('title')
        evento.body = request.form.get('body')
        evento.place = request.form.get('place')

        error = None
        if not evento.title:
            error = 'Se requiere un título'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(evento)
            db.session.commit()
            return redirect(url_for('evento.index'))
        
        flash(error)
        
    return render_template('evento/update.html', evento=evento)

#Eliminar un evento
@evento.route('/evento/delete/<int:id>')
@login_required
def delete(id):
    evento = get_post(id)
    db.session.delete(evento)
    db.session.commit()

    return redirect(url_for('evento.index'))
