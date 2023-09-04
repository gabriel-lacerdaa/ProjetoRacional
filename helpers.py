from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, IntegerField, FloatField


class FormularioFrasco(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    cor = StringField('Cor', [validators.DataRequired(), validators.Length(min=5, max=50)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioFita(FlaskForm):
    codigo_interno = StringField('Cód Interno',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    descricao = StringField('Descrição',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    tamanho_corte_mm = FloatField('Tamanho/Corte',  [validators.DataRequired(), validators.NumberRange(min=0.1, max=10000.0)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')
