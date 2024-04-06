from flask import session
from models.model import Produtos
from models.model import Frascos, Fitas, Cliches, Funcionarios, Configuracoes
from extensions import db

def listaDeFrascoParaSelect(label_incial, value=0):
    listaDeOpcoes = [(value, label_incial)]
    frascos = Frascos.query.order_by(Frascos.id)
    for frasco in frascos:
        if frasco.id != listaDeOpcoes[0][0]:
            listaDeOpcoes.append((frasco.id, f'{frasco.nome} / {frasco.cor}'))
    return listaDeOpcoes

def listaDeFitasParaSelect(label_inicial, value=0):
    listaDeOpcoes = [(value, label_inicial)]
    fitas = Fitas.query.order_by(Fitas.id)
    for fita in fitas:
        if fita.id != listaDeOpcoes[0][0]:
            listaDeOpcoes.append((fita.id, f'{fita.descricao} / {fita.tamanho_corte_mm}(mm)'))
    return listaDeOpcoes


def listaDeClichesParaSelect(label_inicial, value=0):
    listaDeOpcoes = [(value, label_inicial)]
    cliches = Cliches.query.order_by(Cliches.id)
    for cliche in cliches:
        if cliche.id != listaDeOpcoes[0][0]:
            listaDeOpcoes.append((cliche.id, f'{cliche.codigo_interno} / {cliche.descricao}'))
    return listaDeOpcoes


def verificarDependentesFita(fita_id):
    produtos = Produtos.query.filter_by(fita_id=fita_id).first()
    if produtos:
        return True
    else:
        return False


def montarListaDeFuncionarios(id_funcionario=0):
    if id_funcionario:
        f = Funcionarios.query.filter_by(id=id_funcionario).first()
        listaFuncionarios = [(id_funcionario, f'{f.nome} / {f.CPF}')]
        funcionarios = db.session.query(Funcionarios).filter(Funcionarios.status == 'A', \
                     Funcionarios.id != id_funcionario).order_by(Funcionarios.id).all()
    else:
        listaFuncionarios = [(0, '--Escolha um funcionario--')]
        funcionarios = db.session.query(Funcionarios).filter(Funcionarios.status == 'A').order_by(Funcionarios.id).all()

    
    for funcionario in funcionarios:
        listaFuncionarios.append((funcionario.id, f'{funcionario.nome} / {funcionario.CPF}'))
    return listaFuncionarios


def montarListaDeProdutos():
    produtos = Produtos.query.order_by(Produtos.id).all()
    lista_produtos = [(0, '--Escolha um Produto--')]
    for p in produtos:
        lista_produtos.append((p.id, f'{p.nome} / {p.codigo}' ))
    return lista_produtos

def verificarDependentesFrasco(frasco_id):
    produtos = Produtos.query.filter_by(frasco_id=frasco_id).first()
    if produtos:
        return True
    else:
        return False


def verificarDependentesCliche(cliche_id):
    produtos = Produtos.query.filter_by(cliche_id=cliche_id).first()
    if produtos:
        return True
    else:
        return False
    

def verificarSeEstaLogado():
    if ("user" in session) and (session["user"] is not None):
        return True
    return False


def buscarValorDoSalarioPagoPorDia():
    config = Configuracoes.query.filter_by(id=1).first()
    return config.valor_salario_dia