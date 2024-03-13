from extensions import db

class Funcionarios(db.Model):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    vt = db.Column(db.Float, nullable=False)
    CPF = db.Column(db.String(14), nullable=False)
    status = db.Column(db.String(1), nullable=False)
    folha_de_ponto = db.relationship("FolhaDePonto", back_populates='funcionario')

    def __repr__(self):
        return f"Usuario('{self.nome}')"


class Produtos(db.Model):
    __tablename__ = 'produtos_finais'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50))
    nome = db.Column(db.String(100), nullable=False)
    frasco_id = db.Column(db.Integer, nullable=False)
    fita_id = db.Column(db.Integer, nullable=False)
    cliche_id = db.Column(db.Integer, nullable=False)
    tempo_de_producao = db.Column(db.Integer, nullable=False)



class Frascos(db.Model):
    __tablename__ = 'frascos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    frasco_imagem = db.Column(db.LargeBinary, nullable=True)


class Fitas(db.Model):
    __tablename__ = 'fitas'
    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(255))
    descricao = db.Column(db.String(255))
    tamanho_corte_mm = db.Column(db.Float)


class Cliches(db.Model):
    __tablename__ = 'cliches'
    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.String(50))
    descricao = db.Column(db.String(255))


class FolhaDePonto(db.Model):
    __tablename__= 'folha_de_ponto'
    id = db.Column(db.Integer, primary_key=True)
    horas = db.Column(db.Integer)
    data = db.Column(db.Date)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    funcionario = db.relationship("Funcionarios", back_populates="folha_de_ponto")

class Configuracoes(db.Model):
    __tablename__= 'configuracoes'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor_salario_dia = db.Column(db.Float, nullable=False)

