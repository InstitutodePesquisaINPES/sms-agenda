from run import app, db
from flask import render_template, url_for, session, request, redirect,flash
from complementary.flask_wtf.flaskform_login import CadastroUsuarioForm
from app.models.model_user import Usuario
from sqlalchemy import or_

@app.route('/cadastrouser')
def cadastrouser():
    proxima = request.args.get('proxima')
    form_cadastrouser = CadastroUsuarioForm() 

    return render_template('cadastrouser.html', proxima=proxima, form_cadastrouser=form_cadastrouser)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    form_cadastrouser = CadastroUsuarioForm()

    if form_cadastrouser.validate_on_submit():
        user = Usuario.query.filter(
            or_(Usuario.cpf == form_cadastrouser.cpf.data,
                Usuario.nome == form_cadastrouser.email.data)).first()
        if user:
            flash('Usuario já cadastrado no sistema', 'negado')
            return redirect(url_for('cadastrouser'))

        novo_usuario = Usuario(
            email=form_cadastrouser.email.data,
            nome=form_cadastrouser.nome.data,
            cpf=form_cadastrouser.cpf.data,
            sus=form_cadastrouser.sus.data,
            senha=form_cadastrouser.senha.data,
            user_type="usuario"
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'successo')
        return redirect(url_for('indexuser'))
    
    flash('Usuário não cadastrado! reveja os campos', 'negado')
    return render_template('cadastrouser.html', form_cadastrouser=form_cadastrouser)