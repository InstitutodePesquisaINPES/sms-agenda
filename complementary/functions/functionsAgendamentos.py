import uuid
from flask import Request
from PyPDF2 import PdfMerger
from PIL import Image
from app.models.model_user import *
from werkzeug.utils import secure_filename #import de mexer com arquivos
import os
import time
from run import app
from datetime import datetime


from app.controllers.googleCloud import *
from complementary.servicos.servicos_data import *


def paraMinutos(hora):
    emMinutos = hora.hour * 60 + hora.minute
    return emMinutos

def calculaHoras(id_servico): # puxa do banco a quantidade de horas de cada horario de atendimento (intevalo de tempo), util na api do calendario
    servicos = servicos_data_function()

    dia_atual = datetime.today().date()
    numero_dia_atual = dia_atual.day

    print(numero_dia_atual)

    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    # horario1 = Horarios_disponiveis.query.filter_by(id=1).first()
    horario1 = Horario_Servico.query.filter_by(id_servico = id_servico).first()
    
    
    servico = servicos.get(int(id_servico))
    
    # Certifique-se de que `hora_inicio` e `hora_pausa` sejam objetos time
    hora_inicio = horario1.hora_inicio
    hora_pausa = horario1.hora_pausa
    # tempo_pausa = horario1.tempo_pausa
    hora_retomada = horario1.hora_retomada
    hora_final = horario1.hora_final

    # tempo_atendimento = servico['tempo_atendimento']
    # tempo_atendimento = datetime.strptime(tempo_atendimento, "%H:%M:%S")
    

    tempo_atendimento = horario1.tempo_atendimento

    # Converta os objetos time para representações numéricas (por exemplo, minutos)
    minutos_inicio = paraMinutos(hora_inicio)
    minutos_pausa = paraMinutos(hora_pausa)
    # minutos_pausados = paraMinutos(tempo_pausa)
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
 
def calculaHorarios(id_servico, dia):

    servicos = servicos_data_function()
    servico = servicos.get(int(id_servico))

    dia_atual = datetime.today().date()
    numero_dia_atual = dia_atual.day

    # e `hora_inicio` e `hora_pausa` são campos no seu modelo
    # horario1 = Horarios_disponiveis.query.filter_by(id=1).first()
    horario1 = Horario_Servico.query.filter_by(id_servico = id_servico, dia_semana = dia).first()

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
    tempo_atendimento = horario1.tempo_atendimento
    minutos_atendimento = paraMinutos(tempo_atendimento)


    # Calcula a diferença entre os minutos
    manhaMinutos = minutos_pausa - minutos_inicio
    tardeMinutos = minutos_final - minutos_retomada

    # quantia de horarios para cada turno
    horarios_manha = manhaMinutos / minutos_atendimento
    horarios_tarde = tardeMinutos / minutos_atendimento
                    #0                    #1                    #2                     #3                #4
    return [int(horarios_manha), int(horarios_tarde), int(minutos_atendimento), int(minutos_inicio), int(minutos_retomada)]

def numero_do_dia_da_semana(data_str):
    # Converter a string da data para um objeto datetime
    data = datetime.strptime(data_str, "%Y-%m-%d").date()
    
    # Obter o número do dia da semana (domingo = 0, segunda-feira = 1, ..., sábado = 6)
    numero_dia_da_semana = data.weekday()
    
    return numero_dia_da_semana

def listaHorarios(id_servico, dia):
    tempo = 0
    horarios = calculaHorarios(int(id_servico), dia)
    print(horarios)
    lista_horarios = []
    
    tempo = horarios[3] # tempo que inicia a manha
    horas, minutos_restantes = divmod(tempo, 60)
    tempo_format = "{:02d}:{:02d}".format(horas, minutos_restantes)
    
    tempo2 = horarios[4] # tempo que inicia a tarde
    horas, minutos_restantes = divmod(tempo2, 60)
    tempo2_format = "{:02d}:{:02d}".format(horas, minutos_restantes)
    
    lista_horarios.append(tempo_format)
    
    for i in range(horarios[0]):
        if i != 0:
            tempo = tempo + horarios[2]
            tempoh = tempo // 60
            tempom = tempo % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)
    
    lista_horarios.append(tempo2_format)

    for i in range(horarios[1]):
        if i != 0:
            tempo2 = tempo2 + horarios[2]
            tempoh = tempo2 // 60
            tempom = tempo2 % 60
            tempo_formatado = "{:02}:{:02}".format(tempoh, tempom)
            lista_horarios.append(tempo_formatado)

    return lista_horarios


def converter_para_pdf(documento, nome_da_pasta, nome_do_arquivo):
    # Garante que o nome da pasta é seguro
    nome_da_pasta = secure_filename(nome_da_pasta)

    # Cria o caminho completo para a pasta de upload
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], nome_da_pasta)
    os.makedirs(upload_path, exist_ok=True)

    # Define o caminho de destino para o arquivo PDF resultante
    destino = os.path.join(upload_path, secure_filename(nome_do_arquivo + '.pdf'))

    # Define o caminho para o arquivo temporário PDF
    temp_pdf_path = os.path.join(upload_path, "temp.pdf")

  
        

    # Converte a imagem para PDF se for uma imagem
    if documento.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        Image.open(documento).save(temp_pdf_path, 'PDF', resolution=100.0)
    
    # Se for um PDF, salva diretamente
    elif documento.filename.lower().endswith('.pdf'):
        temp_pdf_path = os.path.join(upload_path, secure_filename(documento.filename))
        documento.save(temp_pdf_path)
    else:
        raise ValueError("Tipo de arquivo não suportado.")

    # Cria um objeto PdfMerger para mesclar os PDFs
    pdf_merger = PdfMerger()
    pdf_merger.append(temp_pdf_path)

    # Escreve o resultado no arquivo de destino
    with open(destino, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)

    

    return destino

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

def gerarSenha(nome_do_servico, horario, id_servico, dia):
    if ' ' in nome_do_servico:
        doisPrimeiros = ''.join(word[0] for word in nome_do_servico.split())
    else:
        doisPrimeiros = nome_do_servico[:2]

    lista_de_horas = listaHorarios(id_servico, dia)

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
    
    


    
