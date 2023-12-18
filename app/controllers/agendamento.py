import logging
from run import app
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

from app.models.model_agendamento import *
from app.controllers.googleCloud import *
from complementary.flask_wtf.flaskform_login import *
from complementary.flask_wtf.flaskform_agendamento import * 
from complementary.functions.functionsAgendamentos import *

from datetime import datetime, timedelta
from werkzeug.utils import secure_filename #import de mexer com arquivos

def filtro(dado):
    pesquisarBarra = request.args.get('pesquisarBarra')
    filtro = request.args.get('filtro')
    agendamentos = []  # Definir uma lista vazia como valor padrão
    
    if pesquisarBarra:
        if filtro == 'nomeFiltro':
            agendamentos = Agendamento.query.filter(Agendamento.nome_cliente.ilike(f"%{pesquisarBarra}%")).all()
        elif filtro == 'dataFiltro':
            agendamentos = Agendamento.query.filter(Agendamento.data_agendada.ilike(f"%{pesquisarBarra}%")).all()
        elif filtro == 'horarioFiltro':
            agendamentos = Agendamento.query.filter(Agendamento.horario_agendado.ilike(f"%{pesquisarBarra}%")).all()
    else:
        agendamentos = dado.items

    return agendamentos

@app.route('/meusagendamentos') 
def meusagendamentos():
    id_usuario_logado = session.get('id_usuario_logado')
    page = int(request.args.get('page', 1))
    registros_por_pagina = 10   
    
    agendamentos = Agendamento.query.filter(Agendamento.id_usuario==id_usuario_logado).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
    agendamentos = filtro(agendamentos)


    return render_template('agendamentos.html', agendamentos=agendamentos)

@app.route('/editar/<int:id_usuario>', methods=['GET', 'POST'])
def editar(id_usuario):
    novo_agendamento = Agendamento.query.get(id_usuario)
    print(f'ID do Usuário: {id_usuario}')
    print(f'Objeto de Agendamento: {novo_agendamento}')


    print('editando...')
    if novo_agendamento:
        print('asdasd',request.form.get('data_agendamento'))
        #pegando os inputs para substituir no html
        novo_agendamento.nome_cliente = request.form.get('nome_cliente')
        novo_agendamento.data_agendada =  request.form.get('data_agendamento')
        novo_agendamento.horario_agendado = request.form.get('horario_agendado')
       
        db.session.commit()
    else:
        print('dsfj')

    return redirect(url_for('meusagendamentos'))

        
# Agendamento #
logging.basicConfig(level=logging.DEBUG)

servicos = {
    1:{'id': 1, 'categoria': 'FARMÁCIA', 'nome': 'ATENDIMENTO FARMACÊUTICO', 
       'descricao': 'Distribuição de medicamentos, orientação farmacêutica e monitoramento de condição glicemica', 
       'documentos': ['Receita', 'Carteira de Identidade', 'Cartão do SUS', 'CPF']},

    2:{'id': 2,'categoria': 'EXAMES', 'nome': 'MARCAÇÃO DE EXAMES', 
       'descricao': '(CRPEE) – Regulação/autorização de Tomografias, Ressonâncias, Cintilografias, Biópsias/estudo anatomopatológico, Colonoscopias, Videolaringoscopias, exames pré-operatórios da ortopedia e consultas e/ou procedimentos destinados ao tratamento oncológico, tratamento de cardiopatias graves, tratamento de Insuficiência Renal Crônica e tratamento de doenças imunossupressoras.', 
       'documentos': 'Documentos do serviço B'},

    3:{'id': 3,'categoria': 'AUTORIZAÇÕES', 'nome': 'AUTORIZAÇÃO DE PROCEDIMENTOS', 
       'descricao': 'AIH/APAC – processos de Autorização de Internação Hospitalar (AIH) ou Autorização de Procedimentos Ambulatoriais (APAC), previamente emitida por cirurgião.', 
       'documentos': 'Documentos do serviço C'},

    4:{'id': 4,'categoria': 'TRATAMENTOS', 'nome': 'TRATAMENTO FORA DO DOMICÍLIO - TFD', 
       'descricao': 'Cadastro de agendamentos que necessitam de atendimentos/procedimentos via TFD (tratamento fora do domicílio), quando não estão disponíveis na rede de saúde do município, com laudo já emitido previamente por profissional médico da rede assistencial pública de Vitória da Conquista.',
       'documentos': 'Documentos do serviço D'},

    5:{'id': 5,'categoria': 'SUS', 'nome': 'CARTÃO DO SUS', 
       'descricao': 'Emissão ou atualização do Cartão Nacional de Saúde - SUS.', 
       'documentos': 'Documentos do serviço E'}
}
@app.route('/servico/<int:servico_id>')
def userservicos(servico_id):
    info_servico = servicos.get(servico_id)
    return render_template('userservicos.html', info_servico=info_servico) 

@app.route('/agendar/<int:servico_id>')
def agendar(servico_id):
    horasDisp = listaHorarios() # lista de horários com vagas
    form_agendamento = AgendamentoForm()
    info_servico = servicos.get(servico_id)

    return render_template('formAgendamento.html', horasDisp=horasDisp, form_agendamento=form_agendamento, info_servico=info_servico)

@app.route('/api/agendamentos_por_dia')
def agendamentos_por_dia():
    # Obtém a data de hoje
    hoje = datetime.now().date()
 
    # Obtém a data daqui a 30 dias
    data_30_dias_frente = hoje + timedelta(days=30)

    # Query para contar o número de agendamentos por dia
    resultados = db.session.query(func.count(Agendamento.id), Agendamento.data_agendada).\
        filter(Agendamento.data_agendada.between(hoje, data_30_dias_frente)).\
        group_by(Agendamento.data_agendada).all()
    
    # Lista para armazenar os dias
    dias_list = []

    # Itera sobre os resultados da consulta
    for count, data_agendada in resultados: 
        # Extrai o dia e adiciona à lista de dias
        if count == calculaHoras():
            dias_list.append(data_agendada.day)

    return jsonify(dias_list)

@app.route('/api/horarios_disponiveis', methods=['GET', 'POST'])
def horas_disponiveis():
    try:
        data_selecionada_str = request.json.get('data_selecionada')
        data_selecionada = datetime.strptime(data_selecionada_str, '%Y-%m-%d').date()
        print(data_selecionada_str, data_selecionada)
         

        # Consulta todos os horários já agendados para a data fornecida
        horarios_agendados = [agendamento.horario_agendado.strftime('%H:%M') for agendamento in Agendamento.query.filter_by(data_agendada=data_selecionada_str).all()]

        # Sua lista de horários disponíveis
        horas_disp = listaHorarios()  # Substitua com seus próprios horários

        # Filtra os horários disponíveis removendo aqueles que já foram agendados
        horarios_disponiveis = [hora for hora in horas_disp if hora not in horarios_agendados]

        return jsonify({'horarios_disponiveis': horarios_disponiveis})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

@app.route('/autenticaragendamento', methods=['POST'])
@login_required
def autenticaragendamento():
    documentos = request.files.getlist('documentos_upados[]')

    cpf_usuario = session['cpf_usuario_logado']
    
    lista_documentos = upar_documentos(documentos, cpf_usuario)

    try:
        if request.method == 'POST':
            data_atual = datetime.now().date().strftime('%Y-%m-%d')
            data_agendamento = data_atual
            id_usuario = session['id_usuario_logado']
            nome_cliente = session['usuario_logado']
            data_agendada = request.form['data_agendada']
            horario_agendado = request.form['hora_ipt']

            nome_do_servico = request.form['nome_do_servico']

            senha = gerarSenha(nome_do_servico, horario_agendado)
            print(senha)
            novo_agendamento = Agendamento(id_usuario=id_usuario, nome_cliente=nome_cliente, data_agendada=data_agendada, horario_agendado=horario_agendado, data_agendamento=data_agendamento, senha=senha)

            db.session.add(novo_agendamento)
            db.session.commit()

            lista_documentos_uuid = upa_pro_GCloud(documentos, cpf_usuario)

            id_agendamento = (
                db.session.query(Agendamento.id).filter(Agendamento.data_agendada == data_agendada).filter(Agendamento.horario_agendado == horario_agendado).filter(Agendamento.id_usuario == id_usuario).first()
            )

            print(id_agendamento)
            id_formatado = id_agendamento[0]

            caminho1 = ""
            caminho2 = ""
            caminho3 = ""

            for indice, item in enumerate(lista_documentos_uuid):
                if item and indice == 0:
                   caminho1 = item
                if item and indice == 1:
                   caminho2 = item
                if item and indice == 2:
                   caminho3 = item

            novo_caminho = Documentos(id_agendamento=id_formatado, caminho1=caminho1, caminho2=caminho2, caminho3=caminho3)

            db.session.add(novo_caminho)
            db.session.commit()


            return redirect(url_for('meusagendamentos'))

    except SQLAlchemyError as e:
        # Se ocorrer um erro no banco de dados, você pode lançar uma mensagem de erro
        # Aqui, você pode redirecionar para uma página de erro ou renderizar um template com a mensagem de erro
        db.session.rollback()  # Desfaz qualquer alteração pendente no banco de dados
        mensagem_erro = f"Erro ao adicionar agendamento: {str(e)}"
        # Aqui você pode redirecionar para uma página de erro ou renderizar um template com a mensagem de erro
        return render_template('errorPage.html', mensagem_erro=mensagem_erro)

    return render_template('outra_pagina.html')