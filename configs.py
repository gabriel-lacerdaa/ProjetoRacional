import os
SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = os.getenv('MYSQL_USER'),
    senha = os.getenv('MYSQL_PASSWORD'),
    servidor = os.getenv('MYSQL_SERVER'),
    database = os.getenv('MYSQL_DB'),
    )