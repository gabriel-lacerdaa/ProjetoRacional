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
    form.id_produto.choices = montarListaDeProdutos()
    return render_template('novo_pedido.html', form=form)


@pedidos_blueprint.route('/pedidos/novo/salvar', methods=['post'])
def saveOrder():

    try:
        form = FormularioPedido(request.form)
        newOrder = Pedidos(id_produto=form.id_produto.data, numero_nfe=form.numero_nfe.data, data_do_pedido=form.data_pedido.data,
                        quantidade=form.quantidade.data)
        
        db.session.add(newOrder)
        db.session.commit()

        return redirect(url_for('pedidos.allOrders'))    
    except:
        flash('Erro ao salvar pedido!')
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