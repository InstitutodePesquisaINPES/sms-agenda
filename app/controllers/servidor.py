from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from run import app

@app.route('/areaServidor')
def areaServidor():
    return render_template('areaServidor.html')