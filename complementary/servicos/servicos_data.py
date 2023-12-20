servicos = {
         1:{'id': 1, 'categoria': 'FARMÁCIA', 'nome': 'ATENDIMENTO FARMACÊUTICO', 
            'descricao': 'Distribuição de medicamentos, orientação farmacêutica e monitoramento de condição glicemica', 
            'documentos': ['Receita', 'Carteira de Identidade', 'Cartão do SUS', 'CPF'], 'tempo_atendimento': '00:20:00'},

         2:{'id': 2,'categoria': 'EXAMES', 'nome': 'MARCAÇÃO DE EXAMES', 
            'descricao': '(CRPEE) – Regulação/autorização de Tomografias, Ressonâncias, Cintilografias, Biópsias/estudo anatomopatológico, Colonoscopias, Videolaringoscopias, exames pré-operatórios da ortopedia e consultas e/ou procedimentos destinados ao tratamento oncológico, tratamento de cardiopatias graves, tratamento de Insuficiência Renal Crônica e tratamento de doenças imunossupressoras.', 
            'documentos': 'Documentos do serviço B', 'tempo_atendimento': '00:30:00'},

         3:{'id': 3,'categoria': 'AUTORIZAÇÕES', 'nome': 'AUTORIZAÇÃO DE PROCEDIMENTOS', 
            'descricao': 'AIH/APAC – processos de Autorização de Internação Hospitalar (AIH) ou Autorização de Procedimentos Ambulatoriais (APAC), previamente emitida por cirurgião.', 
            'documentos': 'Documentos do serviço C', 'tempo_atendimento': '00:10:00'},

         4:{'id': 4,'categoria': 'TRATAMENTOS', 'nome': 'TRATAMENTO FORA DO DOMICÍLIO - TFD', 
            'descricao': 'Cadastro de agendamentos que necessitam de atendimentos/procedimentos via TFD (tratamento fora do domicílio), quando não estão disponíveis na rede de saúde do município, com laudo já emitido previamente por profissional médico da rede assistencial pública de Vitória da Conquista.',
            'documentos': 'Documentos do serviço D', 'tempo_atendimento': '00:05:00'},

         5:{'id': 5,'categoria': 'SUS', 'nome': 'CARTÃO DO SUS', 
            'descricao': 'Emissão ou atualização do Cartão Nacional de Saúde - SUS.', 
            'documentos': 'Documentos do serviço E', 'tempo_atendimento': '00:40:00'}
      }
   
def servicos_data_function():
   return servicos

def muda_tempo_atendimento(id_servico, novo_horario):
   if id_servico in servicos:
      servicos[id_servico]['tempo_atendimento'] = novo_horario
      
        