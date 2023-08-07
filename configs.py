SECRET_KEY = 'senhamuitoultasecreta'

infos_de_conexao = {
    'SGBD': 'mysql+mysqlconnector',
    'usuario': 'root',
    'senha': '123456789',
    'servidor': 'localhost',
    'database': 'empresa'
}

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = infos_de_conexao["SGBD"],
    usuario = infos_de_conexao["usuario"],
    senha = infos_de_conexao["senha"],
    servidor = infos_de_conexao["servidor"],
    database = infos_de_conexao["database"],
    )