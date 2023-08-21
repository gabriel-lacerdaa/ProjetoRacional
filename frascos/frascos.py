from flask import render_template, redirect, flash, request, url_for, Blueprint
from models.model import Frascos
from helpers import FormularioFrasco
import base64
from extensions import db

frascos_blueprint = Blueprint("frascos", __name__, template_folder="templates")



#POr enquanto essa é a raiz
@frascos_blueprint.route('/')
def allFrascos():
    frascos = Frascos.query.order_by(Frascos.id)
    return render_template("frascos.html", frascos=frascos, titulo='Frascos')

#Rota para carregar formulario para cadastrar novo Frasco
@frascos_blueprint.route('/frascos/novo')
def newFrasco():
    formFrasco = FormularioFrasco()
    return render_template('novo_frasco.html', titulo="Novo Frasco", form=formFrasco)


#Rota para salvar novo frasco
@frascos_blueprint.route('/frasco/novo/salvar', methods=['POST'])
def salvarFrasco():
    frasco = Frascos.query.filter_by(nome=request.form["nome"]).first()
    if frasco:
        flash('Esse Frasco já esta cadastrado!')
        return redirect(url_for('frascos.allFrascos'))
    else:
        form = FormularioFrasco(request.form)
        if not form.validate_on_submit():
            return redirect(url_for('newFrasco'))
        
        frasco_imagem = request.files['arquivo']
        if frasco_imagem.filename != 'img_padrao.jpg' and frasco_imagem.filename != '':
            imagem_binaria = frasco_imagem.read()
            if len(imagem_binaria) > 65000:
                flash('Por favor, envie imagens com tamanho inferior a 64 KB. A imagem atual é muito grande.')
                return redirect(url_for('frascos.allFrascos'))
            novo_frasco = Frascos(nome=form.nome.data, cor=form.cor.data, frasco_imagem=imagem_binaria)
        else:
            novo_frasco = Frascos(nome=form.nome.data, cor=form.cor.data) 
        db.session.add(novo_frasco)
        db.session.commit()
        return redirect(url_for('frascos.allFrascos'))


#Rota para mostrar formulario para editar o cadastro do frasco
@frascos_blueprint.route('/frascos/editar')
def editarFrasco():
    id = request.args.get("id")
    frasco = Frascos.query.filter_by(id=id).first()
    form = FormularioFrasco()
    form.process(obj=frasco)
    if frasco.frasco_imagem:
        img = base64.b64encode(frasco.frasco_imagem).decode('utf-8')
    else:
        img = None
    
    return render_template('editar_frasco.html', titulo='Editar Frasco', form=form, id=frasco.id, imagem=img, img_padrao=url_for('genericas.imagemPadrao'))

#rota para salvar frasco editado
@frascos_blueprint.route('/frascos/editar/salvar', methods=['POST'])
def salvarEdicaoFrasco():
    frasco = Frascos.query.filter_by(id=request.form['id']).first()
    frasco.nome = request.form['nome']
    frasco.cor = request.form['cor']
    frasco_imagem = request.files['arquivo']
    if frasco_imagem.filename != 'img_padrao.jpg' and frasco_imagem.filename != '':
        imagem_binaria = frasco_imagem.read()
        if len(imagem_binaria) > 65000:
            flash('Por favor, envie imagens com tamanho inferior a 64 KB. A imagem atual é muito grande.')
            return redirect(url_for('frascos.allFrascos'))
        frasco.frasco_imagem = imagem_binaria
    db.session.add(frasco)
    db.session.commit()
    return redirect(url_for('frascos.allFrascos'))

@frascos_blueprint.route('/frascos/deletar')
def deletarFrasco():
    id = request.args.get("id")
    Frascos.query.filter_by(id=id).delete()
    flash(f'Frasco deletado com sucesso!')
    db.session.commit()
    return redirect(url_for('frascos.allFrascos'))