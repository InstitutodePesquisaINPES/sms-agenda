from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class AgendamentoForm(FlaskForm): 
    
    data_agendamento = DateField('Data do Agendamento', format='%Y-%m-%d', validators=[DataRequired()])
    id_usuario = DateField('ID do usuário')
    data_agendada = DateField('Data Agendada', validators=[DataRequired()])
    horario = TimeField('Horário do Agendamento', format='%H:%M', validators=[DataRequired()])
    nome_cliente = StringField('Nome do Cliente', validators=[DataRequired()])
    submit = SubmitField('Agendar')
