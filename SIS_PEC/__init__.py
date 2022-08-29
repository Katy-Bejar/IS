from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Cargar las configuraciones
app.config.from_object('config.DevelopmentConfig') #configuracion de la BD
db = SQLAlchemy(app)

#Importar vistas 
from SIS_PEC.controllers.auth import auth
app.register_blueprint(auth)

from SIS_PEC.controllers.evento import evento
app.register_blueprint(evento)
app.add_url_rule('/', endpoint='index')

db.create_all()