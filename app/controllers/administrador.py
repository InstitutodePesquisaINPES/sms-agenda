from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app
from app.models.model_user import *

@app.route('/areaAdmin')
@login_required
def areaAdmin():
    return render_template('areaAdmin.html')

@app.route('/configUnidade')
@login_required
def configUnidade():
    horarios = Horarios_disponiveis.query.filter_by(id=1).first()
    hora1 = "09:00:00"

    return render_template('configUnidade.html', horarios=horarios, hora1=hora1)

@app.route('/configAtendimento')
@login_required
def configAtendimento():
    return render_template('configAtendimento.html')


