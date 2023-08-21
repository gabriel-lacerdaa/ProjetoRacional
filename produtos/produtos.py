from flask import request, render_template, redirect, url_for, session, Blueprint
from models.model import Produtos
from extensions import db

produtos_blueprint = Blueprint("produtos", __name__)

# @produtos_blueprint.route('/')
# def index():
#     if ("user" in session) and (session["user"] is not None):
#         produtos = Produtos.query.order_by(Produtos.id)
#         return render_template("produtos.html", produtos=produtos, titulo='Produtos')
#     else:
#         return redirect(url_for('login', proxima=url_for('index')))


@produtos_blueprint.route('/edit')
def edit():
    id = request.args.get("id")
    produto = Produtos.query.filter_by(id=id).first()
    return render_template('produtos_edit.html', produto=produto, titulo='Editar produto')

@produtos_blueprint.route('/delete')
def delete():
    id = request.args.get("id")
    Produtos.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@produtos_blueprint.route('/salvar', methods=['POST'])
def salvar():
    produto = Produtos.query.filter_by(id=request.form["id"]).first()
    produto.nome = request.form["produto"]
    produto.descricao = request.form["descricao"]
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('index'))

@produtos_blueprint.route('/produto/novo')
def novoProduto():
    return render_template('novo.html')

@produtos_blueprint.route('/produto/novo/salvar', methods=['POST'])
def newProduct():
    nome = request.form["nome"]
    descricao  = request.form["descricao"]
    produto = Produtos(nome=nome, descricao=descricao)
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('index'))