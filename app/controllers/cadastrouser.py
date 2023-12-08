from run import app, db
from flask import render_template, url_for, session, request, redirect
from complementary.flask_wtf.flaskform_cadastrouser import *
from app.models.model_user import Usuario

@app.route('/cadastrouser')
def cadastrouser():
    proxima = request.args.get('proxima')
    form_cadastrouser = CadastroUsuarioForm() 

    return render_template('cadastrouser.html', proxima=proxima, form_cadastrouser=form_cadastrouser)



 
@app.route('/cadastrar', methods=['POST'])
def cadastrar():

    form_cadastrouser = CadastroUsuarioForm(request.form)

    user = Usuario.query.filter_by(nome=form_cadastrouser.nome.data).first()

  
    
    if user:
        session['error_message5'] = 'O email em questão ja se encontra cadastrado no sistema, por favor insira outro para efetuar o cadastro '
        return redirect(url_for('cadastrouser'))
    
       
    
    if form_cadastrouser.senha.data ==  form_cadastrouser.senhanovamente.data:
        novo_usuario = Usuario(
            nome = form_cadastrouser.nome.data,
            cpf = form_cadastrouser.cpf.data,
            sus = form_cadastrouser.sus.data,    
            senha = form_cadastrouser.senha.data,
            user_type = "usuario"
        )

        db.session.add(novo_usuario)
        db.session.commit()
        session['error_message5'] = 'Usuario cadastrado com sucesso'
    else:
        session['error_message5'] = 'Por favor, verifique se as senhas digitadas coecidem '
        return redirect(url_for('cadastrouser'))
    
    return redirect(url_for('login'))
