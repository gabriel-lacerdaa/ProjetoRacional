from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from models.model import FolhaDePonto, Funcionarios
from utils import verificarSeEstaLogado, montarListaDeFuncionarios, buscarValorDoSalarioPagoPorDia
from helpers import FormularioPonto, FormularioCalcularSalario
from datetime import date
from extensions import db
from sqlalchemy import func

folha_de_ponto_blueprint = Blueprint('folha_de_ponto', __name__, template_folder='templates')


@folha_de_ponto_blueprint.before_request
def verificar_autenticacao():
    if (session["isAdmin"] == 0):
        return redirect(url_for('login.logout'))

    if not verificarSeEstaLogado():
        # Redirecionar para a página de login
        return redirect(url_for('login.login', proxima=request.url))



@folha_de_ponto_blueprint.route('/folha_de_ponto')
def allPontos():

    mes_ano = request.args.get('mes_ano')
    mes = mes_ano[5:] if mes_ano else date.today().month
    #Transformando o int para remover os zeros a esquerda
    mes = int(mes)
    form_calcular = FormularioCalcularSalario()
    folha_de_ponto = db.session.query(FolhaDePonto, Funcionarios)\
        .join(Funcionarios).filter(func.extract('month', FolhaDePonto.data) == mes)\
        .order_by(FolhaDePonto.id.desc()).all()
    return render_template('folha_de_ponto.html', form=form_calcular, folha_de_ponto=folha_de_ponto, erro=request.args.get('erro'))


@folha_de_ponto_blueprint.route('/folha_de_ponto/novo')
def newPonto():
    form = FormularioPonto()
    form.id_funcionario.choices = montarListaDeFuncionarios()
    return render_template('novo_folha_de_ponto.html', form=form)


@folha_de_ponto_blueprint.route('/folha_de_ponto/novo/salvar', methods=['POST'])
def saveNewPonto():
    try:
        form = FormularioPonto(request.form)
        ponto = FolhaDePonto(horas=form.horas.data,id_funcionario=form.id_funcionario.data, data=date.today())
        db.session.add(ponto)
        db.session.commit()
    except:
        flash('Erro ao criar novo ponto')
    return redirect(url_for('folha_de_ponto.allPontos'))

@folha_de_ponto_blueprint.route('/folha_de_ponto/calcular', methods=['POST', 'GET'])
def calcularSalario():
    try:
        valor_salario_dia = buscarValorDoSalarioPagoPorDia()
        valor_salario_hora = valor_salario_dia / 9
        mes_ano = request.form['mes_ano']
        mes = mes_ano[5:]
        ano = mes_ano[:4]
        if (mes_ano == ''):
            flash('Necessário escolher o mês e ano')
            return redirect(url_for('folha_de_ponto.allPontos', erro=True))
        if (int(mes) > date.today().month) or (int(ano) > date.today().year):
            flash('Mês ou ano escolhido superior ao mês e ano atual!') 
            return redirect(url_for('folha_de_ponto.allPontos', erro=True))
        
        salarios = db.session.query(Funcionarios.nome, Funcionarios.vt, 
                        func.round((func.sum(FolhaDePonto.horas) * valor_salario_hora), 2).label('salario'),
                        (func.sum(FolhaDePonto.horas).label('horas_trabalhadas')), 
                        (func.count().label('dias_trabalhados'))) \
        .join(FolhaDePonto) \
        .filter(func.extract('month', FolhaDePonto.data) == mes) \
        .filter(func.extract('year', FolhaDePonto.data) == ano) \
        .group_by(Funcionarios.id) \
        .all()
        return render_template('salario_calculado.html', salarios=salarios, valor_salario_dia=valor_salario_dia)
    except Exception as e:
        flash(f'Erro ao calcular salário: {str(e)}')
        return redirect(url_for('folha_de_ponto.allPontos', erro=True))

    

@folha_de_ponto_blueprint.route('/folha_de_ponto/deletar')
def deletePonto():
    FolhaDePonto.query.filter_by(id=request.args.get('id')).delete()
    db.session.commit()
    return redirect(url_for('folha_de_ponto.allPontos'))