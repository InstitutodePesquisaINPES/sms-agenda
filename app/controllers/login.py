from run import app
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models.User import User
from app.models.model_user import *
from app.models.model_agendamento import *
from complementary.flask_wtf.flaskform_login import *
from complementary.flask_wtf.flaskform_agendamento import *
import pandas as pd


from complementary.functions.login import tipo_user

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():

   proxima = request.args.get('proxima')
   form_login = LoginForm()

   return render_template('login.html', form_login= form_login, proxima=proxima)


@app.route('/autenticarlogin', methods=['POST'])
def autenticarlogin():
        form_login = LoginForm(request.form)


        nome = form_login.nome.data
        senha = form_login.senha.data


        user = Usuario.query.filter_by(nome=nome, senha=senha).first()

        if user:
            session['usuario_logado'] = nome
            session['id_usuario_logado'] = user.id
            session['cpf_usuario_logado'] = user.cpf      
            login_user(user)
            flash('Login realizado!')
            proxima_pagina = url_for('indexuser')
            return redirect(proxima_pagina) 
        else:
            flash('Falha no login. Verifique suas credenciais.', 'danger')
            return redirect(url_for('login'))



""""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = None

        for u in users_db.values():
            if u.username == username and u.password == password:
                user = u
                break

        if user:
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            
            return tipo_user(user)
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')

    return render_template('login.html')
    """

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('usuario_logado', None)    
    
    flash('Logout bem-sucedido!', 'success')
    return redirect(url_for('indexuser'))

    