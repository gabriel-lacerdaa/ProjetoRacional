from flask import render_template, request, session, redirect, url_for
from app import app, db
from model import Usuarios, Produtos
from flask_bcrypt import check_password_hash



@app.route('/')
def index():
    # if ("user" in session) and (session["user"] is not None):
        produtos = Produtos.query.order_by(Produtos.id)
        return render_template("produtos.html", produtos=produtos, titulo='Produtos')
    # else:
    #     return redirect(url_for('login', proxima=url_for('index')))

@app.route('/login')
def login():
    if ("user" in session) and (session["user"] is not None):
        return redirect(url_for('index'))
    proxima_pagina = request.args.get("proxima")
    return render_template('login.html', proxima_url=proxima_pagina)

@app.route('/autenticar', methods=["POST"])  
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

@app.route('/logout')
def logout():
    session["user"] = None
    return redirect(url_for('index'))

@app.route('/edit')
def edit():
    id = request.args.get("id")
    produto = Produtos.query.filter_by(id=id).first()
    return render_template('produtos_edit.html', produto=produto, titulo='Editar produto')

@app.route('/delete')
def delete():
    id = request.args.get("id")
    Produtos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/salvar', methods=['POST'])
def salvar():
    produto = Produtos.query.filter_by(id=request.form["id"]).first()
    produto.nome = request.form["produto"]
    produto.descricao = request.form["descricao"]
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/produto/novo')
def novoProduto():
    return render_template('novo.html')

@app.route('/produto/novo/salvar', methods=['POST'])
def newProduct():
    nome = request.form["nome"]
    descricao  = request.form["descricao"]
    produto = Produtos(nome=nome, descricao=descricao)
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('index'))
    