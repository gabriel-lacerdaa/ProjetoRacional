from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.model import Cliches
from helpers import FormularioCliche
from extensions import db

cliches_blueprint = Blueprint("cliches", __name__, template_folder="templates")


@cliches_blueprint.route('/cliches')
def allCliches():
    cliches = Cliches.query.order_by(Cliches.id) 
    return render_template('cliches.html', titulo="Clichês", cliches=cliches)

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