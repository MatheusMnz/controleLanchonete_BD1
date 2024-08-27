# forms/pedidoForm.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class PedidoForm(FlaskForm):
    quantidade_vendas = IntegerField('Quantidade de Vendas', validators=[DataRequired()])
    preco_venda = FloatField('Preço da Venda', validators=[DataRequired()])
    id_cliente = IntegerField('ID do Cliente', validators=[DataRequired()])
    id_funcionario = IntegerField('ID do Funcionário', validators=[DataRequired()])
    id_venda = IntegerField('ID da Venda', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    submit = SubmitField('Adicionar Pedido')
