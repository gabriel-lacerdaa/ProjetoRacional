from models.model import Produtos

def listaParaSelectPelaDescricao(Opcoes, labelIncial):
    listaDeOpcoes = [(0, labelIncial)]
    for opcao in Opcoes:
        listaDeOpcoes.append((opcao.id, opcao.descricao))
    return listaDeOpcoes

def listaParaSelectPeloNome(Opcoes, labelIncial):
    listaDeOpcoes = [(0, labelIncial)]
    for opcao in Opcoes:
        listaDeOpcoes.append((opcao.id, opcao.nome))
    return listaDeOpcoes


def verificarDependentesFita(fita_id):
    produtos = Produtos.query.filter_by(fita_id=fita_id).first()
    if produtos:
        return True
    else:
        return False


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