import json
import os
from flask import Flask, request
from google.cloud import storage
from run import app


# Obtém o caminho relativo para o arquivo JSON de chave de serviço
chave_servico_path = os.path.join(os.path.dirname(__file__), 'sms-agenda-407918-9625fe9ffc72.json')

# Carrega as informações da chave de serviço
with open(chave_servico_path, 'r') as json_file:
    chave_servico_info = json.load(json_file)

# Configurações do Google Cloud Storage
bucket_name = 'user-agenda-documents-sms'
client = storage.Client.from_service_account_json(chave_servico_path)
bucket = client.get_bucket(bucket_name)

@app.route('/upload', methods=['POST'])
def upload():
    if 'documento' not in request.files:
        return 'Nenhum documento enviado', 400

    documento = request.files['documento']

    # Gere um nome de arquivo único ou utilize algum identificador do seu banco de dados
    nome_arquivo = 'documento_unico.jpg'

    # Fazer upload para o Google Cloud Storage
    blob = bucket.blob(nome_arquivo)
    blob.upload_from_file(documento)

    # Salvar a URL do documento ou outras informações no seu banco de dados
    # ...

    return 'Upload bem-sucedido'


@app.route('/download/<nome_arquivo>', methods=['GET'])
def download(nome_arquivo):
    # Recuperar o documento do Google Cloud Storage
    blob = bucket.blob(nome_arquivo)

    # Verificar se o arquivo existe
    if not blob.exists():
        return 'Documento não encontrado', 404

    # Fazer o download do documento
    documento = blob.download_as_text()  # Ou use blob.download_to_filename('local_file_path') para baixar como arquivo

    # Faça o que precisar com o documento (por exemplo, enviar como resposta)
    # ...

    return 'Download bem-sucedido'