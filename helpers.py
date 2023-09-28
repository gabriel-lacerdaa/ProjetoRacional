from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, IntegerField, FloatField, SelectField

class FormularioFrasco(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    cor = StringField('Cor', [validators.DataRequired(), validators.Length(min=5, max=50)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioFita(FlaskForm):
    codigo_interno = StringField('Cód Interno',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    descricao = StringField('Descrição',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    tamanho_corte_mm = FloatField('Tamanho/Corte',  [validators.DataRequired(), validators.NumberRange(min=0.1, max=10000.0)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioCliche(FlaskForm):
    codigo_interno = StringField('Cód Interno',  [validators.DataRequired(), validators.Length(min=5, max=50)], render_kw={'autocomplete': 'off'})
    descricao = StringField('Descrição',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioProdutoFinal(FlaskForm):
    codigo = StringField('Codigo',  [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'autocomplete': 'off'})
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    # "coerce=int" para garantir que o valor seja um número inteiro
    frasco_id = SelectField('Frasco', [validators.DataRequired()], coerce=int)  
    # Campo de seleção para fita_id
    fita_id = SelectField('Fita', [validators.DataRequired()], coerce=int)
    # Campo de seleção para cliche_id
    cliche_id = SelectField('Clichê', [validators.DataRequired()], coerce=int)
