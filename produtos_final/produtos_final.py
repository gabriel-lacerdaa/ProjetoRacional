from flask import request, render_template, redirect, url_for, session, Blueprint, flash
from models.model import Produtos, Fitas, Frascos, Cliches
from extensions import db
from helpers import FormularioProdutoFinal
from utils import listaParaSelectPeloNome, listaParaSelectPelaDescricao

produtos_blueprint = Blueprint("produtos", __name__, template_folder="templates")

@produtos_blueprint.route('/produtos_final')
def index():
    # if ("user" in session) and (session["user"] is not None):
    produtos = Produtos.query.order_by(Produtos.id)
    return render_template("produtos.html", produtos=produtos, titulo='Produtos')
    # else:
    #     return redirect(url_for('login', proxima=url_for('index')))


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
    return redirect(url_for('produtos.index'))

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
    fitas = Fitas.query.order_by(Fitas.id)
    frascos = Frascos.query.order_by(Frascos.id)
    cliches = Cliches.query.order_by(Cliches.id)
    form = FormularioProdutoFinal()
    form.frasco_id.choices = listaParaSelectPeloNome(frascos, "--Escolha um Frasco--")
    form.fita_id.choices = listaParaSelectPelaDescricao(fitas, "--Escolha uma Fita--")
    form.cliche_id.choices = listaParaSelectPelaDescricao(cliches, "--Escolha um Cliche--")
    return render_template('produto_novo.html', form=form, titulo="Novo Produto")

@produtos_blueprint.route('/produto/novo/salvar', methods=['POST'])
def newProduct():
    form = FormularioProdutoFinal(request.form)
    produto = Produtos.query.filter_by(codigo=form.codigo.data).first()
    print(produto)
    if produto:
        flash(f"O Produto com o codigo {produto.codigo} já está cadastrado")
        return redirect(url_for('produtos.novoProduto'))
    if form.fita_id.data == 0 or form.frasco_id.data == 0 or form.cliche_id.data == 0:
        flash('É necessário informar um Frasco, Fita e Clichê para inserir um novo Produto!!')
        return redirect(url_for('produtos.novoProduto'))
    produto = Produtos(nome=form.nome.data, codigo=form.codigo.data, fita_id=form.fita_id.data, 
                       frasco_id=form.frasco_id.data, cliche_id=form.cliche_id.data)
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produtos.index'))