from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField 


class FormularioFrasco(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    cor = StringField('Cor', [validators.DataRequired(), validators.Length(min=5, max=50)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')