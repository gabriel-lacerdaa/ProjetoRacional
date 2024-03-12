from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.model import Configuracoes
from helpers import FormularioConfiguracao
from extensions import db

configuracoes_blueprint = Blueprint('configuracoes', __name__, template_folder='templates')


@configuracoes_blueprint.before_request
def verificar_autenticacao():
    if (session["isAdmin"] == 0):
        return redirect(url_for('login.logout'))


@configuracoes_blueprint.route('/configuracoes')
def allConfigs():
    configs = Configuracoes.query.order_by(Configuracoes.id).all()
    return render_template('configuracoes.html', configs=configs, erro=request.args.get('erro'))


@configuracoes_blueprint.route('/configuracoes/editar')
def editConfig():
    id=request.args.get('id')
    config = Configuracoes.query.filter_by(id=id).first()
    form = FormularioConfiguracao()
    form.process(obj=config)
    return render_template('configuracoes_editar.html', form=form, id=id)


@configuracoes_blueprint.route('/configuracoes/editar/salvar', methods=['POST'])
def saveConfig():
    try:
        config = Configuracoes.query.filter_by(id=request.args.get('id')).first()
        form = FormularioConfiguracao(request.form)
        if not form.validate_on_submit():
            flash('Dados inválidos')
        else:
            config.descricao = form['descricao'].data
            config.valor_salario_dia = form['valor_salario_dia'].data   
            db.session.commit() 
    except:
        flash('Erro ao salvar edição')

    return redirect(url_for('configuracoes.allConfigs'))