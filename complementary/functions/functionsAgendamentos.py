import uuid
from flask import Request
from app.models.model_user import *
from werkzeug.utils import secure_filename #import de mexer com arquivos
import os
from run import app
from datetime import datetime
from app.controllers.googleCloud import *
from complementary.servicos.servicos_data import *


def paraMinutos(hora):
    emMinutos = hora.hour * 60 + hora.minute
    return emMinutos

def calculaHoras(id_servico): # puxa do banco a quantidade de horas de cada horario de atendimento (intevalo de tempo), util na api do calendario
    servicos = servicos_data_function()

    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    horario1 = Horarios_disponiveis.query.filter_by(id=1).first()
    
    servico = servicos.get(int(id_servico))
    
    # Certifique-se de que `hora_inicio` e `hora_pausa` sejam objetos time
    hora_inicio = horario1.hora_inicio
    hora_pausa = horario1.hora_pausa
    tempo_pausa = horario1.tempo_pausa
    hora_retomada = horario1.hora_retomada
    hora_final = horario1.hora_final

    # tempo_atendimento = servico['tempo_atendimento']
    # tempo_atendimento = datetime.strptime(tempo_atendimento, "%H:%M:%S")
    
    servico_temp = Servico.query.filter_by(id_servico = id_servico).first()
    tempo_atendimento = servico_temp.tempo_atendimento

    # Converta os objetos time para representações numéricas (por exemplo, minutos)
    minutos_inicio = paraMinutos(hora_inicio)
    minutos_pausa = paraMinutos(hora_pausa)
    minutos_pausados = paraMinutos(tempo_pausa)
    minutos_retomada = paraMinutos(hora_retomada)
    minutos_final = paraMinutos(hora_final)
    minutos_atendimento = paraMinutos(tempo_atendimento)

    # Calcula a diferença entre os minutos
    manhaMinutos = minutos_pausa - minutos_inicio
    tardeMinutos = minutos_final - minutos_retomada

    qntManha = manhaMinutos / minutos_atendimento
    qntTarde = tardeMinutos / minutos_atendimento

    # Se necessário, manipule diferença_em_minutos de acordo com suas necessidades
    return qntManha + qntTarde #retorna 2 em cada

    # soma do return da 4, usar um count com filtro por dia, para saber quantos agendamentos tem no dia pra saber se ta disponivel 
 
def calculaHorarios(id_servico):

    servicos = servicos_data_function()
    servico = servicos.get(int(id_servico))

    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    horario1 = Horarios_disponiveis.query.filter_by(id=1).first()

    # manha
    hora_inicio = horario1.hora_inicio
    hora_pausa = horario1.hora_pausa
    
    # tarde
    hora_retomada = horario1.hora_retomada
    hora_final = horario1.hora_final

    # manha em minutos
    minutos_inicio = paraMinutos(hora_inicio)
    minutos_pausa = paraMinutos(hora_pausa)

    # tarde em minutos
    minutos_retomada = paraMinutos(hora_retomada)
    minutos_final = paraMinutos(hora_final)

    # tempo de duração de cada atendimento 
    servico_temp = Servico.query.filter_by(id_servico = id_servico).first()
    tempo_atendimento = servico_temp.tempo_atendimento
    minutos_atendimento = paraMinutos(tempo_atendimento)


    # Calcula a diferença entre os minutos
    manhaMinutos = minutos_pausa - minutos_inicio
    tardeMinutos = minutos_final - minutos_retomada

    # quantia de horarios para cada turno
    horarios_manha = manhaMinutos / minutos_atendimento
    horarios_tarde = tardeMinutos / minutos_atendimento
                    #0                    #1                    #2                     #3                #4
    return [int(horarios_manha), int(horarios_tarde), int(minutos_atendimento), int(minutos_inicio), int(minutos_retomada)]

def listaHorarios(id_servico):
    tempo = 0
    horarios = calculaHorarios(int(id_servico))
    lista_horarios = []
    tempo = horarios[3] # tempo que inicia a manha
    tempo2 = horarios[4] # tempo que inicia a tarde
    lista_horarios.append("0{}:00".format(int(tempo / 60)))
    for i in range(horarios[0]):
        if i != 0:
            tempo = tempo + horarios[2]
            tempoh = tempo // 60
            tempom = tempo % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)
    
    lista_horarios.append("{}:00".format(int(tempo2 / 60)))

    for i in range(horarios[1]):
        if i != 0:
            tempo2 = tempo2 + horarios[2]
            tempoh = tempo2 // 60
            tempom = tempo2 % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)

    return lista_horarios


def upar_documentos(documentos, nome_da_pasta):
    lista_documentos = []

    # Certifique-se de que o nome da pasta é seguro
    nome_da_pasta = secure_filename(nome_da_pasta)

    # Crie o caminho completo do diretório de upload
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_da_pasta)

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    for documento in documentos:
        
        # Verificar se é um arquivo seguro
        if documento.filename != '':
            
            # Gerar um nome de arquivo seguro usando secure_filename
            filename = secure_filename(documento.filename)

            # Salvar o arquivo na pasta de uploads
            destino = os.path.join(upload_path, filename)

            documento.save(destino)

            # Adicionar o caminho do arquivo à lista
            lista_documentos.append(destino)


    return lista_documentos

def gerarSenhaDemandas():
    
    texto_original = ""  # Substitua isso pela sua string original
    letras_substituicao_ano = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letras_substituicao_mes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']


    # Obtenha o ano atual
    ano_atual = datetime.now().year
    mes_atual =  datetime.now().month




    # Calcule o índice da letra de substituição com base no ano
    indice_letra_substituicao_ano = ano_atual % len(letras_substituicao_ano)
    indice_letra_substituicaoa_mes = mes_atual % len(letras_substituicao_mes)

    # Substitua a letra na string original
    letra_codigo_ano = texto_original[:indice_letra_substituicao_ano] + letras_substituicao_ano[indice_letra_substituicao_ano] + texto_original[indice_letra_substituicao_ano + 1:]
    letra_codigo_mes = texto_original[:indice_letra_substituicaoa_mes] + letras_substituicao_mes[indice_letra_substituicaoa_mes] + texto_original[indice_letra_substituicaoa_mes + 1:]

    return letra_codigo_ano, letra_codigo_mes, texto_original

def gerarSenha(nome_do_servico, horario, id_servico):
    if ' ' in nome_do_servico:
        doisPrimeiros = ''.join(word[0] for word in nome_do_servico.split())
    else:
        doisPrimeiros = nome_do_servico[:2]

    lista_de_horas = listaHorarios(id_servico)

    indiceHora = lista_de_horas.index(horario) + 1 if horario in lista_de_horas else 0

    senha = f"{doisPrimeiros}_{indiceHora}"

    return senha

def upa_pro_GCloud(documentos, cpf_usuario):
    lista_documentos_uuid = []
    for indice, documento in enumerate(documentos):
        try:
            print(documento)

            # Gere um nome de arquivo único ou utilize algum identificador do seu banco de dados
            id = str(uuid.uuid4())
            nome_arquivo = cpf_usuario + '/' + cpf_usuario + '_' + id + '.jpg'
            lista_documentos_uuid.append(id)

            prefixo = cpf_usuario + '/'
            blobs = list(bucket.list_blobs(prefix=prefixo))
                
            if not blobs:
                # Se a pasta não existe, crie-a
                bucket.blob(prefixo).upload_from_string('')

            # Posicione o cursor no início do arquivo
            documento.seek(0)

            # Fazer upload para o Google Cloud Storage
            blob = bucket.blob(nome_arquivo)
            blob.upload_from_file(documento)

        except Exception as e:
            print(f"Ocorreu um erro durante o upload do documento: {e}")

    return lista_documentos_uuid 

def obter_horario_atual():
    # Obtém o horário atual
    horario_atual = datetime.now().strftime("%H:%M")
    return horario_atual



    


    
