import logging
from run import app
from flask import Flask, render_template, make_response

# from flask_weasyprint import HTML, render_pdf
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


from app.models.User import *
from app.controllers.googleCloud import *
from complementary.flask_wtf.flaskform_login import *
from complementary.flask_wtf.flaskform_agendamento import * 
from complementary.functions.functionsAgendamentos import *

from complementary.servicos.servicos_data import *
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename #import de mexer com arquivos

servicos = servicos_data_function() # objeto com dados dos serviços

def filtro():
    id_usuario_logado = session.get('id_usuario_logado')
    page = int(request.args.get('page', 1))
    registros_por_pagina = 10

    
    pesquisarBarra = request.args.get('pesquisarBarra')
    filtro = request.args.get('filtro')
    if pesquisarBarra:
        if filtro == 'servicoFiltro':
            agendamentos = Agendamento.query.filter(Agendamento.servico_agendado.ilike(f"%{pesquisarBarra}%")).all()

        elif filtro == 'dataFiltro':       
            data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
            data_formatada = data_obj.strftime('%Y-%m-%d')
            
            agendamentos = Agendamento.query.filter(Agendamento.data_agendada.ilike(f"%{data_formatada}%")).all()    
    else:
        agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

    return agendamentos

@app.route('/meusagendamentos') 
def meusagendamentos():
    try:
        agendamentos_filtrados = filtro()
    except:
        flash('digite um valor de campo valido')
        return redirect(url_for('meusagendamentos'))
   
    return render_template('agendamentos.html', agendamentos=agendamentos_filtrados)


# @app.route('/gerar_pdf/<int:id>', methods=['GET', 'POST'])
# def gerar_pdf(id):
#     agendamento = Agendamento.query.get(id)

#     # Verifica se o agendamento foi encontrado
#     if agendamento is None:
#         return "Agendamento não encontrado", 404

#     # Renderiza o template HTML
#     html = render_template('comprovante_agendamento.html', agendamento=agendamento)

#     # Converte o HTML para PDF usando o Flask-WeasyPrint
#     pdf = render_pdf(HTML(string=html))

#     # Cria uma resposta Flask
#     response = make_response(pdf)

#     # Define os cabeçalhos apropriados para PDF
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=Facilita_comprovante_de_agendamento.pdf'

#     return response
    


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
   
    return redirect(url_for('meusagendamentos'))

@app.route('/deletar/<int:id>', methods=['GET', 'POST'])
def deletar(id):
    documento = Documentos.query.filter_by(id_agendamento=id).all()
    if documento:
        for doc in documento:
            db.session.delete(doc)

        agendamento = Agendamento.query.get(id)
        db.session.delete(agendamento)

        db.session.commit()
    
    return redirect(url_for('meusagendamentos'))

# rota do card de informações do serviço, recebe um id e busca os dados no objeto
@app.route('/servico/<int:servico_id>')
def userservicos(servico_id):
    info_servico = servicos.get(servico_id)
    return render_template('userservicos.html', info_servico=info_servico) 

# rota do formulario de agendamento, recebe um id, e busca os dados do serviço, para agendar.
@app.route('/agendar/<int:servico_id>')
@login_required
def agendar(servico_id):
    
    form_agendamento = AgendamentoForm()
    info_servico = servicos.get(servico_id)

    return render_template('formAgendamento.html', form_agendamento=form_agendamento, info_servico=info_servico)

# API de buscar quantidade de agendamentos em um único dia, acessada pelo js e retorna a lista dos dias disponiveis.
@app.route('/api/agendamentos_por_dia', methods=['GET', 'POST'])
def agendamentos_por_dia():
    id_servico = request.json.get('servico_id')
    info_servico = servicos.get(int(id_servico))

    # Obtém a data de hoje
    hoje = datetime.now().date()

    # Número de dias a serem adicionados (regra de negócio de dias minimos)
    dias_a_frente = info_servico['dias_minimos']
    

    # nova data com regra de negocio de dias minimos
    nova_data = hoje + timedelta(days=dias_a_frente)
    print(nova_data)
 
    # Obtém a data daqui a 30 dias
    data_30_dias_frente = nova_data + timedelta(days=30)
    print(data_30_dias_frente)
    

    # Query para contar o número de agendamentos por dia
    resultados = db.session.query(func.count(Agendamento.id), Agendamento.data_agendada).\
        filter(Agendamento.data_agendada.between(nova_data, data_30_dias_frente)).\
        group_by(Agendamento.data_agendada).all()
    

    
    # Lista para armazenar os dias
    # dias_list = [(nova_data - timedelta(days=i)).day for i in range(dias_a_frente)]
    dias_list = []
    for i in range(dias_a_frente + 1):
        prox_data = hoje + timedelta(days=i)
        dias_list.append(str(prox_data.strftime('%Y-%m-%d')))

    # função que calcula quantos horarios pode ter agendado em um unico dia
    qntHorarios = calculaHoras(id_servico)
    

    # Itera sobre os resultados da consulta
    for count, data_agendada in resultados:
        # Extrai o dia e adiciona à lista de dias
        qntHorarios = calculaHoras(id_servico)
        
        if count == qntHorarios: # se count(quantidade de horarios agendadas, for igual ao maximo de horarios que pode ter nesse dia)
            print(data_agendada.day)
            dias_list.append(str(data_agendada)) # esse dia não estará disponivel
 
    print(dias_list)

    
    return jsonify({'dias_list': dias_list})

# API de horarios por dia selecionada, envia a data pelo js e retorna os horarios disponiveis do dia especifico
@app.route('/api/horarios_disponiveis', methods=['GET', 'POST'])
def horas_disponiveis():
    try:
        dados_json = request.get_json()
        
        data_selecionada_str = dados_json.get('data_selecionada')
        data_selecionada = datetime.strptime(data_selecionada_str, '%Y-%m-%d').date()
        

        servico_id = dados_json.get('servico')
        
        
        # Sua lista de horários disponíveis
        horas_disp = listaHorarios(servico_id)

        horarios_agendados = [agendamento.horario_agendado.strftime('%H:%M') for agendamento in Agendamento.query.filter_by(data_agendada=data_selecionada).all()]
        
        data_atual = datetime.now()
        
        # Filtra os horários disponíveis removendo aqueles que já foram agendados
        horarios_disponiveis = [hora for hora in horas_disp
                         if datetime.combine(data_selecionada, datetime.strptime(hora, '%H:%M').time()) > data_atual and hora not in horarios_agendados]

        return jsonify({'horarios_disponiveis': horarios_disponiveis})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
# rota para autenticar o agendamento     
@app.route('/autenticaragendamento', methods=['POST'])
@login_required
def autenticaragendamento():
    documentos = request.files.getlist('documentos_upados[]')

    cpf_usuario = session['cpf_usuario_logado']
    
    lista_documentos = upar_documentos(documentos, cpf_usuario) # salvar documentos agendados na pasta raíz

    try:
        if request.method == 'POST':
            data_atual = datetime.now().date().strftime('%Y-%m-%d')
            data_agendamento = data_atual
            id_usuario = session['id_usuario_logado']
            nome_cliente = session['usuario_logado']
            data_agendada = request.form['data_agendada']
            horario_agendado = request.form['hora_ipt']
            id_servico = request.form['id_servico']

            nome_do_servico = request.form['nome_do_servico']

            senha = gerarSenha(nome_do_servico, horario_agendado, id_servico)
            print(senha)
            novo_agendamento = Agendamento(id_usuario=id_usuario, nome_cliente=nome_cliente, servico_agendado=nome_do_servico, data_agendada=data_agendada, horario_agendado=horario_agendado, data_agendamento=data_agendamento, senha=senha)

            db.session.add(novo_agendamento)
            db.session.commit()

            #|----------- Função de enviar para api do GCloud Suspensa, os métodos estão comentados abaixo ------------|#

            # lista_documentos_uuid = upa_pro_GCloud(documentos, cpf_usuario)

            # id_agendamento = (
            #     db.session.query(Agendamento.id).filter(Agendamento.data_agendada == data_agendada).filter(Agendamento.horario_agendado == horario_agendado).filter(Agendamento.id_usuario == id_usuario).first()
            # )

            
            # id_formatado = id_agendamento[0]

            # caminho1 = ""
            # caminho2 = ""
            # caminho3 = ""

            # for indice, item in enumerate(lista_documentos_uuid):
            #     if item and indice == 0:
            #        caminho1 = item
            #     if item and indice == 1:
            #        caminho2 = item
            #     if item and indice == 2:
            #        caminho3 = item

            # novo_caminho = Documentos(id_agendamento=id_formatado, caminho1=caminho1, caminho2=caminho2, caminho3=caminho3)

            # db.session.add(novo_caminho)
            # db.session.commit()


            return redirect(url_for('meusagendamentos'))

    except SQLAlchemyError as e:
        # Se ocorrer um erro no banco de dados, você pode lançar uma mensagem de erro
        # Aqui, você pode redirecionar para uma página de erro ou renderizar um template com a mensagem de erro
        db.session.rollback()  # Desfaz qualquer alteração pendente no banco de dados
        mensagem_erro = f"Erro ao adicionar agendamento: {str(e)}"
        # Aqui você pode redirecionar para uma página de erro ou renderizar um template com a mensagem de erro
        return render_template('errorPage.html', mensagem_erro=mensagem_erro)

    return render_template('outra_pagina.html')