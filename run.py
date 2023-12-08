from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from app.models.User import User


from flask_sqlalchemy import SQLAlchemy 
from flask_wtf.csrf import CSRFProtect
import os
from flask_wtf.csrf import CSRFProtect

import pandas as pd


from complementary.functions.login import tipo_user


app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
app.config.from_pyfile('config.py')
csrf = CSRFProtect(app)
db = SQLAlchemy(app)



from app.controllers.login import *      

from app.controllers.administrador import *
from app.controllers.cadastrouser import *
from app.controllers.servidor import *
from app.controllers.indexusuario import *
from app.controllers.agendamento import *
from app.models.model_user import *
from app.models.model_agendamento import *


if __name__ == '__main__':
    app.run(debug=True)
#