from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from frascos.frascos import frascos_blueprint
from produtos_final.produtos_final import produtos_blueprint
from login.login import login_blueprint
from cliches.cliches import cliches_blueprint
from genericas.routesGenerics import rotasGenericas_blueprint
from funcionarios.funcionarios import funcionarios_blueprint
from fitas.fitas import fitas_blueprint
from folha_de_ponto.folha_de_ponto import folha_de_ponto_blueprint
from configuracoes.configuracoes import configuracoes_blueprint
from pedidos.pedidos import pedidos_blueprint
from extensions import db
import locale

app = Flask(__name__)
app.config.from_pyfile('configs.py')
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
db.init_app(app)
app.register_blueprint(frascos_blueprint)
app.register_blueprint(produtos_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(rotasGenericas_blueprint)
app.register_blueprint(fitas_blueprint)
app.register_blueprint(cliches_blueprint)
app.register_blueprint(funcionarios_blueprint)
app.register_blueprint(folha_de_ponto_blueprint)
app.register_blueprint(configuracoes_blueprint)
app.register_blueprint(pedidos_blueprint)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

@app.template_filter('format_number')
def format_number(value):
    return locale.format_string("%d", value, grouping=True)

@app.template_filter('format_currency')
def format_currency(value):
    return locale.currency(value, grouping=True)

if __name__ == "__main__":
    app.run(debug=True)
