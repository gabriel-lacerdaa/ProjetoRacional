import mysql.connector
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456789'
    )
except:
    print("Não foi possivel fazer a conexão")

cursor = conn.cursor()

cursor.execute('DROP DATABASE IF EXISTS `EMPRESA`;')

cursor.execute('CREATE DATABASE `EMPRESA`')

cursor.execute('USE `EMPRESA`')

cursor.execute("""
               CREATE TABLE usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL, 
                senha VARCHAR(100) NOT NULL)
               """)

cursor.execute("""
               CREATE TABLE produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cod_produto  varchar(20) NOT NULL, 
                descricao VARCHAR(200) NOT NULL)
               """)

cursor.execute("""                 
    CREATE TABLE frascos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cor VARCHAR(50),
    frasco_imagem BLOB
)
""")

frascos = [
    ("Frasco exemplo 1", "preto"),
    ("Frasco exemplo 2", "rosa"),
    ("Frasco exemplo 3", "vermelho")
]

for frasco in frascos:
    sql_insert = "INSERT INTO frascos (nome, cor) values (%s, %s)"
    cursor.execute(sql_insert, frasco)


usuario = ("gabriel", generate_password_hash("senha").decode('utf-8'))
sql_insert = "INSERT INTO usuarios (nome, senha) values (%s,  %s)"
cursor.execute(sql_insert, usuario)

produtos = [
    ("produto1", '001', "descricao do produto1"),
    ("produto2", '002', "descricao do produto2"),
    ("produto3", '003', "descricao do produto3"),
    ("produto4", '004', "descricao do produto4"),
    ("produto5", '005', "descricao do produto5")
]

for produto in produtos:
    sql_insert = "INSERT INTO produtos (nome, cod_produto, descricao) values (%s, %s, %s)"
    cursor.execute(sql_insert, produto)


cursor.execute("SELECT * FROM EMPRESA.usuarios")
print("-"*10+' Usuarios '+'-'*10)
for user in cursor.fetchall():
    print(user[1])

cursor.execute("SELECT * FROM EMPRESA.produtos")
print("-"*10+' Produtos '+'-'*10)
for produto in cursor.fetchall():
    print(produto[1], produto[2])


cursor.close()
conn.commit()
conn.close()