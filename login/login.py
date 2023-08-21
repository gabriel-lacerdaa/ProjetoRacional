from flask import render_template, request, session, redirect, url_for, send_from_directory, Blueprint
from models.model import Usuarios
from flask_bcrypt import check_password_hash

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route('/login')
def login():
    if ("user" in session) and (session["user"] is not None):
        return redirect(url_for('index'))
    proxima_pagina = request.args.get("proxima")
    return render_template('login.html', proxima_url=proxima_pagina)

@login_blueprint.route('/autenticar', methods=["POST"])  
def logar():
    usuario = request.form["username"]
    senha = request.form["password"]
    proxima_url = request.form["proxima_url"]
    usuario = Usuarios.query.filter_by(nome=usuario).first()
    if usuario:
        if check_password_hash(usuario.senha, senha):
            session["user"] = usuario.nome
            return redirect(proxima_url)
    return redirect(url_for('login', proxima=proxima_url))

@login_blueprint.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('index'))

