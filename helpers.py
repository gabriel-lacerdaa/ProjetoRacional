from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, FloatField, SelectField, PasswordField, BooleanField, IntegerField, MonthField


class FormularioLogin(FlaskForm):
    usuario = StringField('Usuário', [validators.DataRequired(), validators.Length(min=5, max=30)], render_kw={'autocomplete': 'off'})
    senha = PasswordField('Senha', [validators.DataRequired()])
    enviar = SubmitField('Enviar')

class FormularioFrasco(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    cor = StringField('Cor', [validators.DataRequired(), validators.Length(min=4, max=50)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioFita(FlaskForm):
    codigo_interno = StringField('Cód Interno',  [validators.DataRequired(), validators.Length(min=5, max=255)], render_kw={'autocomplete': 'off'})
    descricao = StringField('Descrição',  [validators.DataRequired(), validators.Length(min=4, max=255)], render_kw={'autocomplete': 'off'})
    tamanho_corte_mm = FloatField('Tamanho/Corte(mm)',  [validators.DataRequired(), validators.NumberRange(min=0.1, max=10000.0)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioCliche(FlaskForm):
    codigo_interno = StringField('Cód Interno',  [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={'autocomplete': 'off'})
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
    tempo_de_producao = IntegerField('Tempo de produção', [validators.DataRequired(), validators.NumberRange(min=1, max=20)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')

class FormularioFuncionarios(FlaskForm):
    nome = StringField('Nome',  [validators.DataRequired(), validators.Length(min=4, max=50)], render_kw={'autocomplete': 'off'})
    vt = FloatField('VT(Diario)',  [validators.DataRequired(), validators.NumberRange(min=0.1, max=10000.0)], render_kw={'autocomplete': 'off'})
    CPF = StringField('CPF',  [validators.DataRequired(), validators.Length(min=11, max=14)], render_kw={'autocomplete': 'off'})
    admin = BooleanField('Admin', render_kw={'autocomplete': 'off'})
    status = BooleanField('Ativo', render_kw={'autocomplete': 'off'})
    # senha = PasswordField('Senha', [validators.DataRequired()])
    salvar = SubmitField('Salvar')

class FormularioPonto(FlaskForm):
    id_funcionario = SelectField('Funcionario', [validators.DataRequired()], coerce=int)
    horas = IntegerField('Horas trabalhadas', [validators.DataRequired(), validators.NumberRange(min=1, max=9)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')


class FormularioCalcularSalario(FlaskForm):
    mes_ano = MonthField('Mês para calcular: ')
    calcular = SubmitField('Calcular salário')


class FormularioConfiguracao(FlaskForm):
    descricao = StringField('Descrição',  [validators.DataRequired(), validators.Length(min=8, max=255)], render_kw={'autocomplete': 'off'})
    valor_salario_dia = FloatField('Valor salario diário', [validators.DataRequired(), validators.NumberRange(min=50, max=150)], render_kw={'autocomplete': 'off'})
    salvar = SubmitField('Salvar')