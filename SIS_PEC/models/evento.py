#MODELO EVENTO

from datetime import datetime
from SIS_PEC import db

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    lugar = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, author, title, body, lugar) -> None:
        self.author = author
        self.title = title
        self.body = body
        self.lugar = lugar

    def __repr__(self) -> str:
        return f'Evento: {self.title}'
