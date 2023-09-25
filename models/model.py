from extensions import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Usuario('{self.nome}')"


class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)


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