
from operator import pos
from flask import(
    render_template, Blueprint, flash, g, redirect, request, url_for
)

from werkzeug.exceptions import abort

from myblog.models.post import Evento
from myblog.models.user import Usuario

from myblog.views.auth import login_required

from myblog import db

evento = Blueprint('evento', __name__)

#Obtner un ususario
def get_user(id):
    user = Usuario.query.get_or_404(id)
    return user

@evento.route("/")
def index():
    posts = Evento.query.all()
    posts = list(reversed(posts))
    db.session.commit()
    return render_template('evento/index.html', posts = posts, get_user=get_user)

#Registrar un post 
@evento.route('/evento/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Evento(g.user.id, title, body)

        error = None
        if not title:
            error = 'Se requiere un título'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('evento.index'))
        
        flash(error)
        
    return render_template('evento/create.html')

def get_post(id, check_author=True):
    post = Evento.query.get(id)

    if post is None:
        abort(404, f'Id {id} de la publicación no existe.')

    if check_author and post.author != g.user.id:
        abort(404)
    
    return post

#Update post 
@evento.route('/evento/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    post = get_post(id) 

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        error = None
        if not post.title:
            error = 'Se requiere un título'
        
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('evento.index'))
        
        flash(error)
        
    return render_template('evento/update.html', post=post)

#Eliminar un post
@evento.route('/evento/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('evento.index'))