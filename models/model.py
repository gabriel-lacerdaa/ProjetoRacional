from extensions import db


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Usuario('{self.nome}')"


class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)


class Frascos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    frasco_imagem = db.Column(db.LargeBinary, nullable=True)