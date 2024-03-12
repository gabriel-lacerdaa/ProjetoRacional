import mysql.connector
from flask_bcrypt import generate_password_hash
import os

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='soft1973824650',
        port= 3306
    )
except:
    print("Não foi possivel fazer a conexão")

cursor = conn.cursor()

cursor.execute('DROP DATABASE IF EXISTS `Racional`;')

cursor.execute('CREATE DATABASE `Racional`')

cursor.execute('USE `Racional`')

cursor.execute("""
               CREATE TABLE funcionarios (
                id INT AUTO_INCREMENT,
                nome VARCHAR(100) NOT NULL, 
                senha VARCHAR(100) NOT NULL,
                admin tinyint(1) not null,
                vt float NOT NULL,
                CPF varchar(14) NOT NULL,
                status char(1) NOT NULL,
                constraint pk_funcionario primary key(id)
               )
               """)

cursor.execute("""
               CREATE TABLE produtos_finais (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50),
                nome VARCHAR(100) NOT NULL,
                frasco_id INT NOT NULL,
                fita_id INT NOT NULL,
                cliche_id INT NOT NULL)
               """)

cursor.execute("""
               CREATE TABLE fitas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo_interno VARCHAR(255) not null,
                descricao VARCHAR(255) not null,
                tamanho_corte_mm FLOAT);
               """)

cursor.execute("""                 
    CREATE TABLE frascos (
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


cursor.execute("""
    CREATE TABLE if not EXISTS folha_de_ponto(
	id integer auto_increment,
	id_funcionario integer not null,
	data date not null,
	horas integer not null,
	constraint pk_folha_de_ponto primary KEY(id),
	constraint fk_funcionario foreign KEY(id_funcionario) references funcionarios(id)
)
""")

cursor.execute("""
    CREATE TABLE if not EXISTS configuracoes(
	id integer auto_increment,
	descricao varchar(255) not null,
	valor_salario_dia float,
	constraint pk_configuracoes primary key(id))
""")



usuario = ("gabriel", generate_password_hash("senha").decode('utf-8'), 0, 10, 22222222222, 'A')
sql_insert = "INSERT INTO funcionarios (nome, senha, admin, vt, CPF, status) values (%s,  %s, %s, %s, %s, %s)"
cursor.execute(sql_insert, usuario)
usuario = ("admin", generate_password_hash("admin").decode('utf-8'), 1, 8, 11111111111, 'A')
cursor.execute(sql_insert, usuario)


config = ("Valor pago por dia", 75)
sql_insert = "INSERT INTO configuracoes (descricao, valor_salario_dia) values (%s, %s)"
cursor.execute(sql_insert, config)

cursor.execute("SELECT * FROM Racional.funcionarios")
print("-"*10+' Usuarios '+'-'*10)
for user in cursor.fetchall():
    print(user[1])



cursor.close()
conn.commit()
conn.close()