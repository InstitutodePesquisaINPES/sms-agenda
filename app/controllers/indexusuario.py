from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app
from app.models.model_user import Servico, Horarios_disponiveis
from datetime import datetime, timedelta
from complementary.flask_wtf.flaskform_agendamento import *
from complementary.functions.functionsAgendamentos import *

servicos_card = {
    1:{'nome': 'ATENDIMENTO FARMACÊUTICO', 
       'sobre': 'Atendimento clínico farmacêutico e monitoramento de condição do paciente'},

    2:{'nome': 'MARCAÇÃO DE EXAMES', 
       'sobre': 'Central de Regulação e Procedimentos Especializados - CRPE'},

    3:{'nome': 'AUTORIZAÇÕES', 
       'sobre': 'Autorização de procedimentos ambulatoriais e hospitalares.'},

    4:{'nome': 'TRATAMENTO FORA DO DOMICÍLIO - TFD', 
       'sobre': 'Cadastro de pacientes para tratamento fora do domicílio'},
       
    5:{'nome': 'CARTÃO DO SUS', 
       'sobre': 'Emissão ou atualização do Cartão Nacional de Saúde.'},

    6:{'nome': 'CONSULTAR MEDICAMENTOS',
       'sobre': 'Consultar  medicamentos disponiveis'},
   
}


@app.route('/')
def indexuser():
   try:
      servico1 = servicos_card.get(1)
      servico2 = servicos_card.get(2)
      servico3 = servicos_card.get(3)
      servico4 = servicos_card.get(4)
      servico5 = servicos_card.get(5)
      servico6 = servicos_card.get(6)
   


      return render_template('index.html', servico1=servico1, servico2=servico2, servico3=servico3, servico4=servico4, servico5=servico5, servico6=servico6)
   except Exception as e:
         print(e)
         return render_template('errorPage.html')


@app.route('/allservices')
def allservices():
   try:
      servico1 = servicos_card.get(1)
      servico2 = servicos_card.get(2)
      servico3 = servicos_card.get(3)
      servico4 = servicos_card.get(4)
      servico5 = servicos_card.get(5) 
      servico6 = servicos_card.get(6)

      return render_template('allServices.html', servico1=servico1, servico2=servico2, servico3=servico3, servico4=servico4, servico5=servico5, servico6=servico6)
   except Exception as e:
        print(e)
        return render_template('errorPage.html')









