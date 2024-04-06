from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from models.model import FolhaDePonto, Funcionarios
from utils import verificarSeEstaLogado, montarListaDeFuncionarios, buscarValorDoSalarioPagoPorDia
from helpers import FormularioPonto, FormularioCalcularSalario
from datetime import date, datetime
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
    try:
        mes_ano_str = request.args.get('mes_ano')
        mes_ano = datetime.strptime(mes_ano_str, "%Y-%m") if mes_ano_str else datetime.now()
        mes = mes_ano_str[5:] if mes_ano_str else date.today().month
        ano = mes_ano_str[:4] if mes_ano_str else date.today().year
        #Transformando o int para remover os zeros a esquerda
        mes = int(mes)
        ano = int(ano)
        form_calcular = FormularioCalcularSalario(mes_ano=mes_ano)
        folha_de_ponto = db.session.query(FolhaDePonto, Funcionarios)\
            .join(Funcionarios).filter((func.extract('month', FolhaDePonto.data) == mes), \
                                    (func.extract('year', FolhaDePonto.data) == ano))\
            .order_by(FolhaDePonto.id.desc()).all()
        if len(folha_de_ponto) == 0:
            flash('Nenhum ponto encontrado!')
        return render_template('folha_de_ponto.html', form=form_calcular, folha_de_ponto=folha_de_ponto, erro=request.args.get('erro'))
    except:
        flash('Erro ao buscar pontos')
        return render_template('folha_de_ponto.html', erro=request.args.get('erro'))


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


@folha_de_ponto_blueprint.route('/folha_de_ponto/editar')
def editPonto():
    id_ponto = request.args.get('id')
    ponto = FolhaDePonto.query.filter_by(id=id_ponto).first()
    form = FormularioPonto()
    form.process(obj=ponto)
    form.id_funcionario.choices = montarListaDeFuncionarios(ponto.id_funcionario)
    return render_template("editar_ponto.html", form=form, id=ponto.id)

@folha_de_ponto_blueprint.route('/folha_de_ponto/editar/salvar', methods=['POST'])
def saveEditPonto():
    try:
        form = FormularioPonto(request.form)
        id = request.form['id']
        if (form.data.data > date.today()):
            flash('Não é possível escolher uma data superior a de hoje!!')
            return redirect(url_for('folha_de_ponto.allPontos', erro=True)) 
        
        ponto = FolhaDePonto.query.filter_by(id=id).first()
        ponto.id_funcionario = form.id_funcionario.data
        ponto.data = form.data.data
        ponto.horas = form.horas.data

        db.session.add(ponto)
        db.session.commit()

        return redirect(url_for('folha_de_ponto.allPontos'))    
    except:
        return redirect(url_for('folha_de_ponto.allPontos', erro=True)) 
    