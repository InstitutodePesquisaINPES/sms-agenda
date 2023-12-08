from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nome = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(),  validators.Length(min=1, max=100)])
    user_type = SelectField('Tipo de Usuário', choices=[('administrador', 'Administrador'), ('servidor', 'Servidor'), ('usuario', 'Usuário')], validators=[DataRequired()])
    submit = SubmitField('Entrar')
