from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.model import Cliches
from helpers import FormularioCliche
from extensions import db
from utils import verificarDependentesCliche, verificarSeEstaLogado

cliches_blueprint = Blueprint("cliches", __name__, template_folder="templates")

# Middleware para verificar se o usuário está logado
@cliches_blueprint.before_request
def verificar_autenticacao():
    if not verificarSeEstaLogado():
        # Redirecionar para a página de login
        return redirect(url_for('login.login', proxima=request.url))



@cliches_blueprint.route('/cliches')
def allCliches():
    if verificarSeEstaLogado():
        cliches = Cliches.query.order_by(Cliches.id) 
        return render_template('cliches.html', titulo="Clichês", cliches=cliches, erro=request.args.get('erro'))
    else:
        return redirect(url_for('login.login', proxima=url_for('cliches.allCliches')))



@cliches_blueprint.route('/cliches/novo')
def newCliche():
    form = FormularioCliche()
    return render_template('novo_cliche.html', titulo="Novo Clichê", form=form)

@cliches_blueprint.route('/cliches/novo/salvar', methods=['POST'])
def salvarCliche():
    cliches = Cliches.query.filter_by(codigo_interno=request.form['codigo_interno']).first()
    if cliches:
        flash('Esse clichê já está cadastrado')
        return redirect(url_for('cliches.allCliches'))
    form = FormularioCliche(request.form)
    if not form.validate_on_submit():
        flash('Dados inválidos!')
        return redirect(url_for('cliches.newCliche'))
    cliche = Cliches(codigo_interno=form['codigo_interno'].data, descricao=form['descricao'].data)
    db.session.add(cliche)
    db.session.commit()
    flash('Clichê adicionado com sucesso!')
    return redirect(url_for('cliches.allCliches'))


@cliches_blueprint.route('/cliches/editar')
def editarCliche():
    cliche_id = request.args.get('id')
    cliche = Cliches.query.filter_by(id=cliche_id).first()
    form = FormularioCliche()
    form.process(obj=cliche)
    return render_template('editar_cliche.html', form=form, titulo='Editar Clichê', id=cliche_id)


@cliches_blueprint.route('/cliches/editar/salvar', methods=['POST'])
def salvarEdicao():
    erro=None
    form = FormularioCliche(request.form)
    cliche_id = request.form.get('id')
    cliche = Cliches.query.filter_by(id=cliche_id).first()
    if not form.validate_on_submit():
        flash('Dados Inválidos')
        erro = True
    else:
        cliche.codigo_interno = form['codigo_interno'].data
        cliche.descricao = form['descricao'].data
        db.session.add(cliche)
        db.session.commit()
    return redirect(url_for('cliches.allCliches', erro=erro))

@cliches_blueprint.route('/cliches/deletar')
def deletarCliche():
    cliche_id = request.args.get('id')
    erro = None
    if verificarDependentesCliche(cliche_id):
        flash('Não é possível excluir esse clichê, pois existem produtos cadastrados que a utilizam como parte de sua composição.')
        erro=True
    else:
        Cliches.query.filter_by(id=cliche_id).delete()
        db.session.commit()
        flash('Clichê deletado com sucesso')
    return redirect(url_for('cliches.allCliches', erro=erro))

