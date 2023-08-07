from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('configs.py')
db = SQLAlchemy(app)


from rotas import *

if __name__ == "__main__":
    app.run(host="localhost", debug=True)