from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from flask_bcrypt import generate_password_hash
from models.model import Funcionarios
from utils import verificarSeEstaLogado
from helpers import FormularioFuncionarios
from extensions import db

funcionarios_blueprint = Blueprint('funcionarios', __name__, template_folder='templates')

@funcionarios_blueprint.before_request
def verificar_autenticacao():
    if (session["isAdmin"] == 0):
        return redirect(url_for('login.logout'))

    if not verificarSeEstaLogado():
        # Redirecionar para a página de login
        return redirect(url_for('login.login', proxima=request.url))


@funcionarios_blueprint.route('/funcionarios')
def allFuncionarios():
    try:
        funcionarios =  Funcionarios.query.order_by(Funcionarios.id)   
        # db.session.query(Funcionarios).filter(Funcionarios.admin != 1).order_by(Funcionarios.id).all()
        return render_template('funcionarios.html', funcionarios=funcionarios, erro=request.args.get('erro'))
    except:
        flash('Erro ao buscar funcionarioos!')
        return render_template('funcionarios.html', erro=True)


@funcionarios_blueprint.route('/funcionarios/novo')
def newFuncionario():
    form = FormularioFuncionarios()
    return render_template('novo_funcionario.html', form=form, erro=request.args.get('erro'))


@funcionarios_blueprint.route('/funcionarios/novo/salvar', methods=['POST'])
def saveFuncionario():
    try:
        form = FormularioFuncionarios(request.form)
        funcionario = Funcionarios.query.filter_by(CPF=form["CPF"].data).first()
        if funcionario:
            flash('Esse funcionário já está cadastrado!')
            return redirect(url_for('funcionarios.newFuncionario', erro=True))

        #deixar  como senha padrão 1234
        senha = '1234'
        senha = generate_password_hash(senha)
        status = 'A' if form['status'].data else 'I'
       

        funcionario = Funcionarios(nome=form['nome'].data, vt=form['vt'].data, 
                                senha=senha, CPF= form['CPF'].data, admin=0, status=status)
        db.session.add(funcionario)
        db.session.commit()

        return redirect(url_for('funcionarios.allFuncionarios'))
    except:
        flash('Erro ao salvar novo funcionario!')
        return redirect(url_for('funcionarios.allFuncionarios', erro=True))
        
    
    

@funcionarios_blueprint.route('/funcionarios/inativar')
def inativarFuncionario():
    try:
        id = request.args.get("id")
        funcionarios = Funcionarios.query.filter_by(id=id).first()
        funcionarios.status = 'I'
        db.session.commit()
        return redirect(url_for('funcionarios.allFuncionarios'))
    except:
        flash('Erro ao inativar funcionario!')
        return redirect(url_for('funcionarios.allFuncionarios', erro=True))
