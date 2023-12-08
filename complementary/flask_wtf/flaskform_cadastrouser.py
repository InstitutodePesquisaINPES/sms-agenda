from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length

class CadastroUsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('Cpf', validators=[DataRequired(), Length(min=11)])
    sus = StringField('Sus', validators=[DataRequired(), Length(min=15)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem coincidir')])
    senhanovamente = PasswordField('', [validators.DataRequired(), validators.Length(min=1, max=100)])
    submit = SubmitField('Cadastrar')
