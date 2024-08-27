# forms/vendaForm.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class VendaForm(FlaskForm):
    id_produto = IntegerField('ID do Produto', validators=[DataRequired()])
    preco = FloatField('Preço', validators=[DataRequired()])
    data_inicio = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    data_fim = DateField('Data de Fim (opcional)', format='%Y-%m-%d', validators=[])
    submit = SubmitField('Adicionar Venda')
