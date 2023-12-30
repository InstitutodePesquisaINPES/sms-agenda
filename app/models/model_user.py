from run import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False) 
    nome = db.Column(db.String(255), nullable=False) 
    cpf = db.Column(db.String(14), nullable=False)
    sus = db.Column(db.String(19), nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome={self.nome}, user_type={self.user_type})>"

    def is_active(self): 

        return True  
    
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_agendada = db.Column(db.Date, nullable=False)
    horario_agendado = db.Column(db.Time, nullable=False)
    nome_cliente = db.Column(db.String(255), nullable=False)
    data_agendamento = db.Column(db.Date, nullable=False)
    senha = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(25), nullable=False)
    
    servico_agendado = db.Column(db.String(255), nullable=False)
    usuario = db.relationship('Usuario', backref='agendamentos')
    documentos = db.relationship('Documentos', backref='agendamento', cascade='all, delete-orphan')
    
class Horarios_disponiveis(db.Model):
    __tablename__ = 'horarios_disponiveis'
    id = db.Column(db.Integer , primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_pausa = db.Column(db.Time, nullable=False)
    tempo_pausa = db.Column(db.Time, nullable=False)
    hora_retomada = db.Column(db.Time, nullable=False)
    hora_final = db.Column(db.Time, nullable=False)
    # tempo_atendimento = db.Column(db.Time, nullable=False)
    
class Horario_Servico(db.Model):
    __tablename__ = 'horario_servico'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_servico = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_pausa = db.Column(db.Time, nullable=False) 
    hora_retomada = db.Column(db.Time, nullable=False)
    hora_final = db.Column(db.Time, nullable=False)
    tempo_atendimento = db.Column(db.Time, nullable=False)

class Servico(db.Model):
    __tablename__ = "servico"
    id = db.Column(db.Integer, primary_key=True)
    id_servico = db.Column(db.Integer, nullable=False)
    tempo_atendimento = db.Column(db.Time, nullable=False)
    
    
class Documentos(db.Model):
    __tablename__ = "documentos"
    id = db.Column(db.Integer, primary_key=True)
    id_agendamento = db.Column(db.Integer, db.ForeignKey('agendamentos.id'))
    caminho1 = db.Column(db.String(255), nullable=True)
    caminho2 = db.Column(db.String(255), nullable=True)
    caminho3 = db.Column(db.String(255), nullable=True)