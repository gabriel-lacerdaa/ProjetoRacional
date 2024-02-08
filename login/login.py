from flask import render_template, request, session, redirect, url_for, Blueprint, flash
from models.model import Funcionarios
from flask_bcrypt import check_password_hash
from helpers import FormularioLogin

login_blueprint = Blueprint("login", __name__, template_folder='templates')

@login_blueprint.route('/')
def login():
    if ("user" in session) and (session["user"] is not None):
        return redirect(url_for('produtos.allProducts'))
    proxima_pagina = request.args.get("proxima")
    if not proxima_pagina:
        proxima_pagina = url_for('produtos.allProducts')
    form = FormularioLogin()
    return render_template('login.html', form=form, proxima_url=proxima_pagina)

@login_blueprint.route('/autenticar', methods=["POST"])  
def logar():
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    proxima_url = request.form["proxima_url"]
    usuario = Funcionarios.query.filter_by(nome=usuario).first()
    if usuario:
        if check_password_hash(usuario.senha, senha):
            session["user"] = usuario.nome
            session["isAdmin"] = usuario.admin
            return redirect(proxima_url)
    flash('Usuário ou senha inválidos')
    return redirect(url_for('login.login', proxima=proxima_url))

@login_blueprint.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('login.login'))

