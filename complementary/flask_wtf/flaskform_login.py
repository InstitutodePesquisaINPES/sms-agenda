from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField, IntegerField
from wtforms.validators import Email, EqualTo, Length, InputRequired, NumberRange

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(message='Campo obrigatório'), Email()])

    senha = PasswordField('Senha', validators=[InputRequired(message='Campo obrigatório'), Length(min=8, max=50, message="A senha deve um minimo de 8 caracteres.")])                                        
    submit = SubmitField('Entrar')
class CadastroUsuarioForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(message='Campo obrigatório'), Email()])
    nome = StringField('Nome', validators=[InputRequired(message='Campo obrigatório'), Length(max=255)])
    cpf = StringField('Cpf', validators=[InputRequired(message='Campo obrigatório'), Length(min=14, max=14, message='Número do CPF deve ter 11 dígitos')])
    sus = StringField('Sus', validators=[InputRequired(message='Campo obrigatório'), Length(min=19, max=19, message='Número do SUS deve ter 15 dígitos')])
    telefone = StringField('Telefone', validators=[InputRequired(message='Campo obrigatório'), Length(max=255)])

    senha = PasswordField('Senha', validators=[InputRequired(message='Campo obrigatório'), Length(min=8, max=50, message="A senha deve um minimo de 8 caracteres e um maximo de 50 caracteres.")])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[InputRequired(message='Campo obrigatório'), EqualTo('senha', message='As senhas devem coincidir')])
    submit = SubmitField('Cadastrar')
