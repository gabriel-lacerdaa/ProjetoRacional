from flask import send_from_directory, Blueprint

rotasGenericas_blueprint = Blueprint('genericas', __name__)

@rotasGenericas_blueprint.route('/imagem/padrao')
def imagemPadrao():
    return send_from_directory('IMGs', 'img_padrao.jpg')