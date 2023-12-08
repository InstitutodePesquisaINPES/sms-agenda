from flask_login import current_user
from flask import render_template, redirect, url_for


def tipo_user(user):
    if current_user.user_type == 'administrador':
        return redirect(url_for('areaAdmin'))
    elif current_user.user_type == 'servidor':
        return redirect(url_for('areaServidor'))
    elif current_user.user_type == 'usuario':
        return redirect(url_for('areaUser'))
    else:
        return redirect(url_for('login'))