from flask import Blueprint, request, url_for, redirect, render_template, flash
from models.model import Pedidos, Produtos
from extensions import db
from helpers import FormularioPedido
from utils import montarListaDeProdutos

pedidos_blueprint = Blueprint('pedidos', __name__, template_folder='templates')

@pedidos_blueprint.route('/pedidos')
def allOrders():
    pedidos = db.session.query(Pedidos.id, Pedidos.numero_nfe,\
                               Produtos.nome, Pedidos.quantidade, Pedidos.data_do_pedido) \
                                .join(Produtos).all()
    return render_template('pedidos.html', pedidos=pedidos, erro=request.args.get('erro'))


@pedidos_blueprint.route('/pedidos/novo')
def newOrder():
    form = FormularioPedido()
    form.id_produto.choices = montarListaDeProdutos('--Escolha um Produto--', 0)
    return render_template('novo_pedido.html', form=form)


@pedidos_blueprint.route('/pedidos/novo/salvar', methods=['post'])
def saveOrder():
    try:
        form = FormularioPedido(request.form)
        if form.id_produto.data == 0:
            flash('Para inserir um pedido é necessário escolher um produto!')
            return redirect(url_for('pedidos.allOrders', erro=True))
        newOrder = Pedidos(id_produto=form.id_produto.data, numero_nfe=form.numero_nfe.data, data_do_pedido=form.data_do_pedido.data,
                        quantidade=form.quantidade.data)
        
        db.session.add(newOrder)
        db.session.commit()

        return redirect(url_for('pedidos.allOrders'))    
    except Exception as e:
        flash(f'Erro ao salvar pedido: {e}')
        return redirect(url_for('pedidos.allOrders', erro=True))   


@pedidos_blueprint.route('/pedidos/deletar')
def deleteOrder():
    try:
        id = request.args.get('id')
        Pedidos.query.filter_by(id=id).delete()
        db.session.commit()

        flash('Pedido deletado com sucesso!')
        return redirect(url_for('pedidos.allOrders'))
    except:
        flash('Erro ao deletar pedido!')
        return redirect(url_for('pedidos.allOrders', erro=True))
    

@pedidos_blueprint.route('/pedidos/editar')
def editOrder():
    id = request.args.get('id')
    pedido = Pedidos.query.filter_by(id=id).first()
    produto = Produtos.query.filter_by(id=pedido.id_produto).first()
    form = FormularioPedido()
    form.process(obj=pedido)
    form.id_produto.choices = montarListaDeProdutos(f'{produto.nome} / {produto.codigo}', produto.id,)
    return render_template('edit_pedido.html', form=form, id=id)


@pedidos_blueprint.route('/pedidos/editar/salvar', methods=['POSt'])
def saveEditOrder():
    try:
        form = FormularioPedido(request.form)
        pedido = Pedidos.query.filter_by(id=request.args.get('id')).first()
        pedido.numero_nfe = form.numero_nfe.data
        pedido.id_produto = form.id_produto.data
        pedido.quantidade = form.quantidade.data
        pedido.data_do_pedido = form.data_do_pedido.data
        db.session.add(pedido)
        db.session.commit()
        return redirect(url_for('pedidos.allOrders'))
    except Exception as e:
        flash(f'Erro ao salvar edição do Pedido: {e}')
        return redirect(url_for('pedidos.allOrders', error=True))
