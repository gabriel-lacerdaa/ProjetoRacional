from flask import Blueprint, request, url_for, redirect, render_template
from models.model import Pedidos, Produtos
from extensions import db
from helpers import FormularioPedido
from utils import montarListaDeProdutos

pedidos_blueprint = Blueprint('pedidos', __name__, template_folder='templates')

@pedidos_blueprint.route('/pedidos')
def allOrders():
    pedidos = db.session.query(Pedidos.id, Pedidos.numero,\
                               Produtos.nome, Pedidos.quantidade, Pedidos.data_do_pedido) \
                                .join(Produtos).all()
    print(pedidos)
    return render_template('pedidos.html', pedidos=pedidos, erro=request.args.get('erro'))


@pedidos_blueprint.route('/pedidos/novo')
def newOrder():
    form = FormularioPedido()
    form.id_produto.choices = montarListaDeProdutos()
    return render_template('novo_pedido.html', form=form)