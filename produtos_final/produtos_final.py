from flask import request, render_template, redirect, url_for, session, Blueprint, flash
from models.model import Produtos, Fitas, Frascos, Cliches
from extensions import db
from helpers import FormularioProdutoFinal
from utils import listaDeFitasParaSelect, listaDeClichesParaSelect, listaDeFrascoParaSelect

produtos_blueprint = Blueprint("produtos", __name__, template_folder="templates")

@produtos_blueprint.route('/produtos_final')
def allProducts():
    # if ("user" in session) and (session["user"] is not None):
    produtos = Produtos.query.order_by(Produtos.id)
    return render_template("produtos.html", produtos=produtos, titulo='Produtos')
    # else:
    #     return redirect(url_for('login', proxima=url_for('index')))


@produtos_blueprint.route('/produtos/editar')
def edit():
    form = FormularioProdutoFinal()
    id = request.args.get("id")
    produto = Produtos.query.filter_by(id=id).first()
    form.process(obj=produto)
    frasco = Frascos.query.filter_by(id=produto.frasco_id).first()
    fita = Fitas.query.filter_by(id=produto.fita_id).first()
    cliche = Cliches.query.filter_by(id=produto.cliche_id).first()
    form.frasco_id.choices = listaDeFrascoParaSelect(f'{frasco.nome} / {frasco.cor}', frasco.id)
    form.fita_id.choices = listaDeFitasParaSelect( f'{fita.descricao} / {fita.tamanho_corte_mm}(mm)', fita.id)
    form.cliche_id.choices = listaDeClichesParaSelect(f'{cliche.codigo_interno} / {cliche.descricao}', cliche.id)
    return render_template('produtos_edit.html', form=form, titulo='Editar produto', id=id, erro=request.args.get('erro'))


@produtos_blueprint.route('/produtos/editar/salvar', methods=['POST'])
def salvarEdicao():
    erro=None
    form=FormularioProdutoFinal(request.form)
    produto = Produtos.query.filter_by(id=request.form["id"]).first()
    produto.codigo = form.codigo.data
    produto.nome = form.nome.data
    produto.frasco_id = form.frasco_id.data
    produto.fita_id = form.fita_id.data
    produto.cliche_id = form.cliche_id.data
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produtos.allProducts'))


@produtos_blueprint.route('/delete')
def delete():
    try:
        id = request.args.get("id")
        Produtos.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        erro=True
        flash('Ocorreu um erro ao tentar deletar o produto. Tente novamente em alguns minutos!')
        return redirect(url_for('produtos.allProducts', erro=erro))
    flash('Produto deletado com sucesso!')
    return redirect(url_for('produtos.allProducts'))


@produtos_blueprint.route('/produto/novo')
def novoProduto():
    form = FormularioProdutoFinal()
    form.frasco_id.choices = listaDeFrascoParaSelect("--Escolha um Frasco--")
    form.fita_id.choices = listaDeFitasParaSelect("--Escolha uma Fita--")
    form.cliche_id.choices = listaDeClichesParaSelect("--Escolha um Cliche--")
    return render_template('produto_novo.html', form=form, titulo="Novo Produto", erro=request.args.get('erro'))


@produtos_blueprint.route('/produto/novo/salvar', methods=['POST'])
def newProduct():
    form = FormularioProdutoFinal(request.form)
    produto = Produtos.query.filter_by(codigo=form.codigo.data).first()
    if produto:
        flash(f"O Produto com o codigo {produto.codigo} já está cadastrado")
        return redirect(url_for('produtos.novoProduto'))
    if form.fita_id.data == 0 or form.frasco_id.data == 0 or form.cliche_id.data == 0:
        flash('É necessário informar um Frasco, Fita e Clichê para inserir um novo Produto!!')
        erro=True
        return redirect(url_for('produtos.novoProduto', erro=erro))
    produto = Produtos(nome=form.nome.data, codigo=form.codigo.data, fita_id=form.fita_id.data, 
                       frasco_id=form.frasco_id.data, cliche_id=form.cliche_id.data)
    db.session.add(produto)
    db.session.commit()
    return redirect(url_for('produtos.allProducts'))