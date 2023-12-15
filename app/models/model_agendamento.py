from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_agendada = db.Column(db.Date, nullable=False)
    horario_agendado = db.Column(db.Time, nullable=False)
    nome_cliente = db.Column(db.String(255), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    senha = db.Column(db.String(10), nullable=False)

from app.models.model_user import Usuario
Agendamento.usuario = db.relationship('Usuario', backref='agendamentos')