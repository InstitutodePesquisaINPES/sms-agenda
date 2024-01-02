from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app
from app.models.model_user import *
from complementary.servicos.servicos_data import *

# painel de configurações da unidade de atendimento
@app.route('/configUnidade')
@login_required
def configUnidade():
    horarios = Horario_Servico.query.filter_by(id=1).first()
    servicos = servicos_data_function() # objeto dos serviços
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

    return render_template('configUnidade.html', horarios=horarios, servicos=servicos, dias=dias)

@app.route('/api/obter_horario_e_tempo_atendimento', methods=['GET', 'POST'])
def obter_horario_e_tempo_atendimento():
    try:
        dados_json = request.get_json()

        id_servico = dados_json.get('servico_id')
        dia_semana = dados_json.get('dia_semana')
        print('id: ', id_servico)
        print('dia: ', dia_semana )

        servico_temp = Horario_Servico.query.filter_by(id_servico = id_servico, dia_semana = dia_semana).first()

        hora_inicio = servico_temp.hora_inicio.isoformat()
        hora_pausa = servico_temp.hora_pausa.isoformat()
        hora_retomada = servico_temp.hora_retomada.isoformat()
        hora_final = servico_temp.hora_final.isoformat()
        tempo_atendimento = servico_temp.tempo_atendimento.isoformat()

        return jsonify({
                        'hora_inicio': hora_inicio,
                        'hora_pausa': hora_pausa,
                        'hora_retomada': hora_retomada,
                        'hora_final': hora_final,
                        'tempo_atendimento': tempo_atendimento
                        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@app.route('/autenticar_novas_configuracoes', methods=['POST'])
@login_required
def autenticar_novas_configuracoes():
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
    tempo_atendimento = request.form['tempo_atendimento']
    if len(tempo_atendimento) != 8:
        tempo_atendimento = tempo_atendimento + ":00"

    servico_id = request.form['servicoSelect1'] 

    try:
        horario = db.session.query(Horario_Servico).get(servico_id)
        
        horario.hora_inicio = hora_inicio
        horario.hora_pausa = hora_pausa
        horario.hora_retomada = hora_retomada
        horario.hora_final = hora_final
        horario.tempo_atendimento = tempo_atendimento
        
        db.session.commit()
        
    except Exception as e:
        return render_template('errorPage.html', mensagem_erro=e) 
    
    return redirect(url_for('configUnidade'))    
    
