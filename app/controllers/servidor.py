import logging
from run import app
from flask import Flask, render_template, make_response

# from flask_weasyprint import HTML, render_pdf
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc


from app.models.User import *
from app.controllers.googleCloud import *
from complementary.flask_wtf.flaskform_login import *
from complementary.flask_wtf.flaskform_agendamento import * 
from complementary.functions.functionsAgendamentos import *

from complementary.servicos.servicos_data import *
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename #import de mexer com arquivos


