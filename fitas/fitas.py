from flask import Blueprint, render_template, url_for, flash, redirect, request
from helpers import FormularioFita
from models.model import Fitas
from extensions import db

fitas_blueprint = Blueprint("fitas", __name__, template_folder="templates")

@fitas_blueprint.route('/fitas')
def allFitas():
    fitas = Fitas.query.order_by(Fitas.id)
    return render_template('fitas.html', fitas=fitas, titulo = "Fitas")

@fitas_blueprint.route('/fitas/nova_fita')
def newFita():
    form = FormularioFita()
    return render_template('nova_fita.html', form=form, titulo='Cadastrar Nova Fita')

@fitas_blueprint.route('/fitas/nova_fita/salvar', methods=['POST'])
def salvarFita():
    fita = Fitas.query.filter_by(codigo_interno=request.form['codigo_interno']).first()
    if fita:
        flash('Essa fita ja esta cadastrada!')
        return redirect(url_for('fitas.allFitas'))
    form = FormularioFita(request.form)
    if not form.validate_on_submit():
        flash('Dados invalidos')
        return redirect(url_for('fitas.newFita'))
    fita = Fitas(codigo_interno=form['codigo_interno'].data, descricao=form['descricao'].data, tamanho_corte_mm=form['tamanho_corte'].data)
    db.session.add(fita)
    db.session.commit()
    flash('Fita cadastrada com sucesso!')
    return redirect(url_for('fitas.allFitas'))