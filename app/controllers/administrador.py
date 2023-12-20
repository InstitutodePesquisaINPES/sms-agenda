from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app
from app.models.model_user import *
from complementary.servicos.servicos_data import *

@app.route('/areaAdmin')
@login_required
def areaAdmin():
    return render_template('areaAdmin.html')

@app.route('/configUnidade')
@login_required
def configUnidade():
    horarios = Horarios_disponiveis.query.filter_by(id=1).first()
    servicos = servicos_data_function()

    return render_template('configUnidade.html', horarios=horarios, servicos=servicos)


@app.route('/autenticarConfig2', methods=['POST'])
@login_required
def autenticarConfig2(): #config de tempo_atendimento
    print(request.form)
    servico_id = request.form['servicoSelect']
    novo_horario = request.form['tempo_atendimento']
    novo_horario = novo_horario + ":00"

    muda_tempo_atendimento(servico_id, novo_horario)
    
    return render_template('configUnidade.html')

