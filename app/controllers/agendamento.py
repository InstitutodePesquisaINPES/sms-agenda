import logging
from run import app
from fpdf import FPDF
from flask import Flask, render_template, make_response,send_from_directory

# from flask_weasyprint import HTML, render_pdf
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify,send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc, not_


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
            agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.servico_agendado.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtro == 'dataFiltro':       
            data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
            data_formatada = data_obj.strftime('%Y-%m-%d')
            
            agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado,Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)    
    else:
        agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

    return agendamentos

@app.route('/meusagendamentos') 
def meusagendamentos():
    try:
        agendamentos_filtrados = filtro()
        if agendamentos_filtrados.items:
           
            agendamentos_filtrados.items = [servico for servico in agendamentos_filtrados.items if servico.servico_agendado != "CARTÃO DO SUS"]
            
            return render_template('agendamentos.html', agendamentos=agendamentos_filtrados)
        else:
            
            flash('Nenhum resultado encontrado')
            return render_template('agendamentos.html', agendamentos=agendamentos_filtrados)
       
    except:
        flash('digite um valor de campo valido')
        return redirect(url_for('meusagendamentos'))
   


@app.route('/gerar_pdf/<int:id>', methods=['GET', 'POST'])
def gerar_pdf(id):
    agendamento = Agendamento.query.get(id)

    largura_pagina = 150
    altura_pagina = 148


    pdf = FPDF(format=(largura_pagina, altura_pagina))
    pdf.add_page()

   
    pdf.set_fill_color(227, 222, 129)  

    # Preencha o retângulo com a cor de fundo
    pdf.rect(0, 0, largura_pagina, altura_pagina, 'F')
    pdf.image(r'app\static\assets\images\prefeitura.jpeg', x=10, y=10, w=20)

    textoMedicamento = f"""LOCAL DO SERVIÇO: FACILITA SAÚDE
SENHA: {agendamento.senha}
SERVIÇO AGENDADO: {agendamento.servico_agendado}.
STATUS: {agendamento.status}
DATA AGENDADA: {agendamento.data_agendada}
HORA AGENDADA: {agendamento.horario_agendado}"""

    textoAgendamento = f"""LOCAL DO SERVIÇO: FACILITA SAÚDE
SENHA: {agendamento.senha}
SERVIÇO AGENDADO: {agendamento.servico_agendado}.
DATA AGENDADA: {agendamento.data_agendada}
HORA AGENDADA: {agendamento.horario_agendado}"""

    pdf.set_font("Courier", size=12)

    # Configurar alinhamento central para o título
    pdf.set_xy(10, 10)  # Defina as coordenadas iniciais para o título

   
    pdf.multi_cell(largura_pagina - 20, 10, "COMPROVANTE DE AGENDAMENTO", align='C')  # Largura ajustada para evitar margens

    # Configurar alinhamento à esquerda para o restante do texto
    pdf.set_xy(10, 30)  # Defina as coordenadas iniciais para o texto restante

    if agendamento.servico_agendado != "CARTÃO DO SUS":
        pdf.multi_cell(largura_pagina - 20, 10, textoAgendamento)  # Largura ajustada para evitar margens
    else:
        pdf.multi_cell(largura_pagina - 20, 10, textoMedicamento)  # Largura ajustada para evitar margens

    temp_file_path = "Comprovante de agendamento.pdf"
    pdf.output(temp_file_path)

    return send_file(temp_file_path, as_attachment=True)

@app.route('/gerar_pdf_logs', methods=['POST'])
def gerar_pdf_logs():

    

# Abre o arquivo em modo de leitura ('r')
    with open('log.txt', 'r') as logs:
    # Lê o conteúdo do arquivo e armazena na variável
        log = logs.read()
    # Crie um objeto FPDF
        pdf = FPDF()
        pdf.add_page()

        # Adicione o título
        pdf.set_font("Courier", size=14)
        pdf.cell(200, 10, txt="Logs do Sistema", ln=True, align='C')

        # Adicione os logs
        pdf.set_font("Courier", size=6)
    
        pdf.multi_cell(0, 3, txt=log)

        # Salve o arquivo PDF temporário
        temp_file_path = "logs.pdf"
        pdf.output(temp_file_path)

    # Envie o arquivo PDF como resposta
    return send_file(temp_file_path, as_attachment=True)

   


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    try:
        user_type_usuario_logado = session.get('user_type_usuario_logado')
        usuario_logado = session.get('usuario_logado')
        cpf_usuario_logado = session.get('cpf_usuario_logado')
        novo_agendamento = Agendamento.query.get(id)
        novo_agendamento.servico_agendado = request.form.get('serviço_admin')
        novo_agendamento.data_agendada =  request.form.get('data_agendamento_admin')
        novo_agendamento.horario_agendado = request.form.get('horario_admin')
        if novo_agendamento.servico_agendado == 'CARTÃO DO SUS':
           
            if request.form.get('status_admin') :
                 novo_agendamento.status = request.form.get('status_admin')
                 documento = request.files.get('documentos_upados[]')
                 converter_para_pdf_editar(novo_agendamento.data_agendada, novo_agendamento.horario_agendado, documento, request.form.get('data_agendamento_admin'), request.form.get('horario_admin'))
            else:
                novo_agendamento.status = 'analise'
        else:
            pass
        print(request.form.get('horario_admin'),request.form.get('status_admin'))
        

        # Adicione validações para campos obrigatórios
        if novo_agendamento.servico_agendado is None or novo_agendamento.status is None:
            raise ValueError('Os campos serviço e status são obrigatórios.')

        descricao_log = f'''Registro de edição: 
        - id: {novo_agendamento.id}
        - id_usuario: {novo_agendamento.id_usuario}
        - nome_cliente: {novo_agendamento.nome_cliente}
        - data_agendada: {novo_agendamento.data_agendada}
        - horario_agendado: {novo_agendamento.horario_agendado}
        - senha: {novo_agendamento.senha}
        - status: {novo_agendamento.status}
        - servico_agendado: {novo_agendamento.servico_agendado}
        - documentos: {novo_agendamento.documentos}
        - Usuario editor: 
            - usuario_logado: {usuario_logado}
            - cpf_usuario_logado: {cpf_usuario_logado}
            - user_type_usuario_logado: {user_type_usuario_logado}
    ------------------------------------------------------------------
    '''

        db.session.commit()
        registrar_log(descricao_log)
        flash('Edição feita com sucesso')
        if user_type_usuario_logado == 'usuario':
            if novo_agendamento.servico_agendado == 'CARTÃO DO SUS':
                
                return redirect(url_for('consultarMedicamento'))
            else:
                
                return redirect(url_for('meusagendamentos'))
        elif user_type_usuario_logado in ['servidor', 'administrador']:
            if novo_agendamento.servico_agendado == 'CARTÃO DO SUS':
                
                return redirect(url_for('consultarMedicamento'))
            else:  
                    
                return redirect(url_for('areaServidor'))

    except:
        flash('Por favor, altere um serviço ou um status para concluir a edição. Essas informações são obrigatórias')
        # Realize os redirecionamentos com base no tipo de serviço e tipo de usuário
        if user_type_usuario_logado == 'usuario':
            if novo_agendamento.servico_agendado == 'CARTÃO DO SUS':
                
                return redirect(url_for('consultarMedicamento'))
            else:
                
                return redirect(url_for('meusagendamentos'))
        elif user_type_usuario_logado in ['servidor', 'administrador']:
            if novo_agendamento.servico_agendado == 'CARTÃO DO SUS':
                
                return redirect(url_for('consultarMedicamento'))
            else:  
                   
                return redirect(url_for('areaServidor'))

    


def registrar_log(descricao):
    with open('log.txt', 'a') as f:
        dataAlteraçao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = f'{dataAlteraçao} - {descricao}\n'
        f.write(log)


def deletar_docs(filename, data, horario):
    instancia_usuario_solicitante = Agendamento.query.filter_by(id=filename).first()
    cpf = instancia_usuario_solicitante.usuario.cpf
    cpf_formatado = cpf.replace(".", "").replace("-", "")
    horario_formatado = horario[:-2]

    nome_arquivo = f'{data}{horario_formatado}.pdf'
    print(nome_arquivo, cpf_formatado,data,horario_formatado)
    # Construa o caminho completo
    caminho_completo = os.path.join(app.root_path, 'uploads', cpf_formatado, nome_arquivo)

    for arquivo in os.listdir(os.path.dirname(caminho_completo)):
        caminho_arquivo = os.path.join(os.path.dirname(caminho_completo), arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)
        except Exception as e:
            print(f'Erro ao excluir o arquivo {caminho_arquivo}: {e}')

    return "Arquivos deletados com sucesso!"

@app.route('/deletar/<int:id>/<filename>/<data>/<horario>', methods=['GET', 'POST'])
def deletar(id, filename, data,horario):
    user_type_usuario_logado = session.get('user_type_usuario_logado')
    usuario_logado = session.get('usuario_logado')
    cpf_usuario_logado = session.get('cpf_usuario_logado')

    documento = Documentos.query.filter_by(id_agendamento=id).all()
    if documento:
        for doc in documento:
            db.session.delete(doc)
    


    agendamento = Agendamento.query.get(id)
    descricao_log = descricao_log = f'''Registro excluído: 
    - id: {agendamento.id}
    - id_usuario: {agendamento.id_usuario}
    - nome_cliente: {agendamento.nome_cliente}
    - data_agendada: {agendamento.data_agendada}
    - horario_agendado: {agendamento.horario_agendado}
    - senha: {agendamento.senha}
    - status: {agendamento.status}
    - servico_agendado: {agendamento.servico_agendado}
    - documentos: {agendamento.documentos}
    - Usuario editor: 
        - usuario_logado: {usuario_logado}
        - cpf_usuario_logado: {cpf_usuario_logado}
        - user_type_usuario_logado: {user_type_usuario_logado}
------------------------------------------------------------------
'''

    
    if user_type_usuario_logado == 'usuario' :
        if agendamento.servico_agendado == 'CARTÃO DO SUS':
            db.session.delete(agendamento)
            db.session.commit()
            deletar_docs(filename, data,horario)
            registrar_log(descricao_log)
            return redirect(url_for('consultarMedicamento'))
        else:
            db.session.delete(agendamento)
            db.session.commit()
            deletar_docs(filename, data,horario)
            registrar_log(descricao_log)
            return redirect(url_for('meusagendamentos'))
        
    elif user_type_usuario_logado == 'servidor' or  user_type_usuario_logado == 'administrador':
        if agendamento.servico_agendado == 'CARTÃO DO SUS':
            db.session.delete(agendamento)
            db.session.commit()
            deletar_docs(filename, data,horario)
            registrar_log(descricao_log)
            return redirect(url_for('consultarMedicamento'))
        else:  
            db.session.delete(agendamento)
            db.session.commit()
            deletar_docs(filename, data,horario)
            registrar_log(descricao_log)   
            return redirect(url_for('areaServidor'))

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
    print(id_servico)
    print(info_servico)

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
    
    print(resultados)
    
    horario1 = Horario_Servico.query.filter_by(id_servico = 1, dia_semana = 4).first()
    print(horario1)
    
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
        
        numero_dia = numero_do_dia_da_semana(data_selecionada_str) + 1
        
        print('num: ', numero_dia)

        servico_id = dados_json.get('servico')
        
        
        # Sua lista de horários disponíveis
        horas_disp = listaHorarios(servico_id, numero_dia)

        horarios_agendados = [agendamento.horario_agendado.strftime('%H:%M') for agendamento in Agendamento.query.filter_by(data_agendada=data_selecionada).all()]
        
        data_atual = datetime.now()
        
        # Filtra os horários disponíveis removendo aqueles que já foram agendados
        horarios_disponiveis = [hora for hora in horas_disp
                         if datetime.combine(data_selecionada, datetime.strptime(hora, '%H:%M').time()) > data_atual and hora not in horarios_agendados]

        return jsonify({'horarios_disponiveis': horarios_disponiveis})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/uploads/<filename>/<data>/<horario>')
def servir_arquivo(filename, data, horario):
    instancia_usuario_solicitante = Agendamento.query.filter_by(id=filename).first()
    cpf = instancia_usuario_solicitante.usuario.cpf
    cpf_formatado = cpf.replace(".", "").replace("-", "")
    horario_formatado = horario[:-2]

    nome_arquivo = f'{data}{horario_formatado}.pdf'
    print(nome_arquivo, cpf_formatado,data,horario_formatado)
    # Construa o caminho completo
    caminho_completo = os.path.join(app.root_path, 'uploads', cpf_formatado, nome_arquivo)

    return send_from_directory(os.path.dirname(caminho_completo), os.path.basename(caminho_completo))
# rota para autenticar o agendamento     
@app.route('/autenticaragendamento', methods=['POST'])
@login_required
def autenticaragendamento():
    documento = request.files.get('documentos_upados[]')

    cpf_usuario = session['cpf_usuario_logado']
    
    

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

            numero_dia = numero_do_dia_da_semana(data_agendada) + 1
            senha = gerarSenha(nome_do_servico, horario_agendado, id_servico, numero_dia)

            if nome_do_servico == "CARTÃO DO SUS":
                status = 'analise'
                
                novo_agendamento = Agendamento(id_usuario=id_usuario, nome_cliente=nome_cliente, servico_agendado=nome_do_servico, data_agendada=data_agendada, horario_agendado=horario_agendado, data_agendamento=data_agendamento, senha=senha,status=status)

                data_formatada = data_agendada.replace("-", "")
                horario_formatado = horario_agendado.replace(":", "")
                cpf_usuario_formatado = cpf_usuario.replace(".","").replace("-","")
                
                nome_arquivo = f"{data_formatada}{horario_formatado}"
                
                print(cpf_usuario_formatado,nome_arquivo)
                try:
                    converter_para_pdf(documento, str(cpf_usuario_formatado), nome_arquivo)
                except ValueError:
                    flash('Insira um documento com extensão válida: .jpeg - .jpg - .pdf')
                   
                    return redirect(url_for('allservices'))
                
                db.session.add(novo_agendamento)
                db.session.commit()
                
                    

            
                return redirect(url_for('consultarMedicamento')) 
            
            status = ''
                
            novo_agendamento = Agendamento(id_usuario=id_usuario, nome_cliente=nome_cliente, servico_agendado=nome_do_servico, data_agendada=data_agendada, horario_agendado=horario_agendado, data_agendamento=data_agendamento, senha=senha,status=status)

            db.session.add(novo_agendamento)
            db.session.commit()


            return redirect(url_for('meusagendamentos'))
            

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
            

    except Exception:
        flash('Ocorreu um erro. Por favor, tente novamente.')
        return redirect(url_for('indexuser'))

def filtroAll():
    id_usuario_logado = session.get('id_usuario_logado')
    page = int(request.args.get('page', 1))
    registros_por_pagina = 10

    
    pesquisarBarra = request.args.get('pesquisarBarra')
    filtro = request.args.get('filtro')
    if pesquisarBarra:
        if filtro == 'servicoFiltro':
           
            agendamentos = Agendamento.query.filter(Agendamento.servico_agendado.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtro == 'dataFiltro':       
            data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
            data_formatada = data_obj.strftime('%Y-%m-%d')
            
            agendamentos = Agendamento.query.filter(Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
        elif filtro == 'usuarioFiltro':       
          
            
            agendamentos = Agendamento.query.filter(Agendamento.nome_cliente.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False) 
    else:
        agendamentos = Agendamento.query.order_by(Agendamento.data_agendada).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)


    return agendamentos

@app.route('/areaServidor') 
def areaServidor():
    try:
        agendamentos_filtrados = filtroAll()

        if agendamentos_filtrados.items:
            agendamentos_filtrados.items = [servico for servico in agendamentos_filtrados.items if servico.servico_agendado != "CARTÃO DO SUS"]
            
            return render_template('areaServidor.html', agendamentos=agendamentos_filtrados)
        else:
            
            flash('Nenhum resultado encontrado')
            return render_template('areaServidor.html', agendamentos=agendamentos_filtrados)
    except:
        flash('digite um valor de campo valido')
        return redirect(url_for('areaServidor'))
   

def filtroConsultarMedicamento():
    id_usuario_logado = session.get('id_usuario_logado')
    user_type_usuario_logado = session.get('user_type_usuario_logado')
    page = int(request.args.get('page', 1))
    registros_por_pagina = 10

    
    pesquisarBarra = request.args.get('pesquisarBarra')
    filtroStatus = request.args.get('filtroStatus')
    filtroPesquisa = request.args.get('filtroPesquisa')
    
    if user_type_usuario_logado == "usuario":  
        
        if filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'todosFiltro':
           
            
            agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "aprovado").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtroStatus == 'retificadosFiltro'  and filtroPesquisa == 'todosFiltro':       
            agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "retificado").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtroStatus == 'analiseFiltro'  and filtroPesquisa == 'todosFiltro':       
            agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "analise").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
        
        else:
           
            if pesquisarBarra:
                if filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'senhaFiltro':
                
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "aprovado",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

                elif filtroStatus == 'retificadosFiltro'  and filtroPesquisa == 'senhaFiltro':       
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "retificado",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                
                elif filtroStatus == 'analiseFiltro'  and filtroPesquisa == 'senhaFiltro':       
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "analise",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                
                elif filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "aprovado",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                
                elif filtroStatus == 'retificadosFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "retificado",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                
                elif filtroStatus == 'analiseFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "analise",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                else:
                    flash('por favor preencha os dois campos de filtro')
                    agendamentos  = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "analise", Agendamento.servico_agendado == "CARTÃO DO SUS").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
            
            else:
                    
                    agendamentos  = Agendamento.query.filter(Agendamento.id_usuario == id_usuario_logado, Agendamento.status == "analise", Agendamento.servico_agendado == "CARTÃO DO SUS").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
################
    elif user_type_usuario_logado == "servidor" or user_type_usuario_logado == "administrador":
         
        if filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'todosFiltro':
           
            
            agendamentos = Agendamento.query.filter( Agendamento.status == "aprovado").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtroStatus == 'retificadosFiltro'  and filtroPesquisa == 'todosFiltro':       
            agendamentos = Agendamento.query.filter( Agendamento.status == "retificado").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)

        elif filtroStatus == 'analiseFiltro'  and filtroPesquisa == 'todosFiltro':       
            agendamentos = Agendamento.query.filter( Agendamento.status == "analise").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
        
        else:
           
            if pesquisarBarra:
                if filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'senhaFiltro':  
                    agendamentos = Agendamento.query.filter( Agendamento.status == "aprovado",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                elif filtroStatus == 'retificadosFiltro'  and filtroPesquisa == 'senhaFiltro':       
                    agendamentos = Agendamento.query.filter( Agendamento.status == "retificado",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                elif filtroStatus == 'analiseFiltro'  and filtroPesquisa == 'senhaFiltro':       
                    agendamentos = Agendamento.query.filter( Agendamento.status == "analise",  Agendamento.senha.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)


                elif filtroStatus == 'aprovadosFiltro'  and filtroPesquisa == 'usuarioFiltro':       
                    agendamentos = Agendamento.query.filter( Agendamento.status == "analise",  Agendamento.nome_cliente.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                elif filtroStatus == 'retificadosFiltro'  and filtroPesquisa == 'usuarioFiltro':       
                    agendamentos = Agendamento.query.filter( Agendamento.status == "analise",  Agendamento.nome_cliente.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                elif filtroStatus == 'analiseFiltro'  and filtroPesquisa == 'usuarioFiltro':       
                    agendamentos = Agendamento.query.filter( Agendamento.status == "analise",  Agendamento.nome_cliente.ilike(f"%{pesquisarBarra}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                

                elif filtroStatus == 'aprovadosFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter( Agendamento.status == "aprovado",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)   
                elif filtroStatus == 'retificadosFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter( Agendamento.status == "retificado",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)              
                elif filtroStatus == 'analiseFiltro' and filtroPesquisa == 'dataFiltro':       
                    data_obj = datetime.strptime(pesquisarBarra, '%d/%m/%Y')
                    data_formatada = data_obj.strftime('%Y-%m-%d')
                    agendamentos = Agendamento.query.filter( Agendamento.status == "analise",  Agendamento.data_agendada.ilike(f"%{data_formatada}%")).order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
                
                else:
                    flash('por favor preencha os dois campos de filtro')
                    agendamentos  = Agendamento.query.filter( Agendamento.status == "analise", Agendamento.servico_agendado == "CARTÃO DO SUS").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
            
            else:
                    
                    agendamentos  = Agendamento.query.filter( Agendamento.status == "analise", Agendamento.servico_agendado == "CARTÃO DO SUS").order_by(Agendamento.data_agendada).paginate(page=page, per_page=registros_por_pagina, error_out=False)
    
    return agendamentos

@app.route('/consultarMedicamento') 
def consultarMedicamento():
    try:
        agendamentos_filtrados = filtroConsultarMedicamento()
        if agendamentos_filtrados.items:
            agendamentos_filtrados.items = [servico for servico in agendamentos_filtrados.items if servico.servico_agendado == "CARTÃO DO SUS"]
            
            return render_template('consultarMedicamento.html', agendamentos=agendamentos_filtrados)
        else:
            
            flash('Nenhum resultado encontrado')
            return render_template('consultarMedicamento.html', agendamentos=agendamentos_filtrados)
       
    except:
        flash('digite um valor de campo valido')
        return redirect(url_for('consultarMedicamento'))