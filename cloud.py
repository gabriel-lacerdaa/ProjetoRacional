import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
import MySQLdb
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = MySQLdb.connect(
    host= os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd= os.getenv("DB_PASSWORD"),
    db= os.getenv("DB_NAME"),
    autocommit = True,
    ssl_mode = "VERIFY_IDENTITY",
    ssl      = {
        "ca": "cert.pem"
    }
    )
except:
    print("Não foi possivel fazer a conexão")

cursor = conn.cursor()

cursor.execute('USE racionaldb')

cursor.execute("""
               CREATE TABLE if not EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL, 
                senha VARCHAR(100) NOT NULL)
               """)

cursor.execute("""
               CREATE TABLE if not EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cod_produto  varchar(20) NOT NULL, 
                descricao VARCHAR(200) NOT NULL)
               """)

cursor.execute("""
               CREATE TABLE if not EXISTS fitas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo_interno VARCHAR(255) not null,
                descricao VARCHAR(255) not null,
                tamanho_corte_mm FLOAT);
               """)

cursor.execute("""                 
    CREATE TABLE if not EXISTS frascos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cor VARCHAR(50),
    frasco_imagem BLOB
)
""")

cursor.execute("""                 
    CREATE TABLE if not EXISTS cliches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    codigo_interno VARCHAR(255) NOT NULL
)
""")

# frascos = [
#     ("Frasco exemplo 1", "preto"),
#     ("Frasco exemplo 2", "rosa"),
#     ("Frasco exemplo 3", "vermelho")
# ]

# for frasco in frascos:
#     sql_insert = "INSERT INTO frascos (nome, cor) values (%s, %s)"
#     cursor.execute(sql_insert, frasco)


usuario = ("admin", generate_password_hash("admin").decode('utf-8'))
sql_insert = "INSERT INTO usuarios (nome, senha) values (%s,  %s)"
cursor.execute(sql_insert, usuario)

# produtos = [
#     ("produto1", '001', "descricao do produto1"),
#     ("produto2", '002', "descricao do produto2"),
#     ("produto3", '003', "descricao do produto3"),
#     ("produto4", '004', "descricao do produto4"),
#     ("produto5", '005', "descricao do produto5")
# ]

# for produto in produtos:
#     sql_insert = "INSERT INTO produtos (nome, cod_produto, descricao) values (%s, %s, %s)"
#     cursor.execute(sql_insert, produto)


cursor.execute("SELECT * FROM racionaldb.usuarios")
print("-"*10+' Usuarios '+'-'*10)
for user in cursor.fetchall():
    print(user[1])

cursor.execute("SELECT * FROM racionaldb.produtos")
print("-"*10+' Produtos '+'-'*10)
for produto in cursor.fetchall():
    print(produto[1], produto[2])

cursor.execute("SELECT * FROM racionaldb.cliches")
print("-"*10+' Cliches '+'-'*10)
for produto in cursor.fetchall():
    print(produto[1], produto[2])


cursor.close()
conn.commit()
conn.close()