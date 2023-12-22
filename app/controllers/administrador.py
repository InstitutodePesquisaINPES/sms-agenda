from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
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

@app.route('/api/obter_tempo_atendimento', methods=['GET', 'POST'])
def obter_tempo_atendimento():
    try:
        dados_json = request.get_json()
        print(dados_json)
        id_servico = dados_json.get('servico_id')
        print(id_servico)
        servico_temp = Servico.query.filter_by(id_servico = id_servico).first()
        print(servico_temp)
        tempo_atendimento = servico_temp.tempo_atendimento.isoformat()
        print(tempo_atendimento)
        return jsonify({'tempo_atendimento': tempo_atendimento})
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@app.route('/autenticarConfig1', methods=['POST'])
@login_required
def autenticarConfig1(): #config de funcionamento da agencia
    hora_inicio = request.form['hora_inicio']
    if len(hora_inicio) != 8:
        hora_inicio = hora_inicio + ":00"
    hora_pausa = request.form['hora_pausa']
    if len(hora_pausa) != 8:
        hora_pausa = hora_pausa + ":00"
    hora_retomada = request.form['hora_retomada']
    if len(hora_retomada) != 8:
        hora_retomada = hora_retomada + ":00"
    hora_final = request.form['hora_final']
    if len(hora_final) != 8:
        hora_final = hora_final + ":00"
    
    try:
        update = db.session.query(Horarios_disponiveis).filter_by(id=1).update({
            'hora_inicio': hora_inicio,
            'hora_pausa': hora_pausa,
            'hora_retomada': hora_retomada,
            'hora_final': hora_final
        })
        db.session.commit()
    except Exception as e:
        return render_template('errorPage.html', mensagem_erro=e)
    
    
    
    return redirect(url_for('configUnidade'))

@app.route('/autenticarConfig2', methods=['POST'])
@login_required
def autenticarConfig2(): #config de tempo_atendimento
    print(request.form)
    servico_id = request.form['servicoSelect']
    novo_horario = request.form['tempo_atendimento']
    novo_horario = novo_horario + ":00"

    try:
        update = db.session.query(Servico).filter_by(id_servico=servico_id).update({'tempo_atendimento': novo_horario})
        db.session.commit()
    except Exception as e:
        return render_template('errorPage.html', mensagem_erro=e)
    return redirect(url_for('configUnidade'))

