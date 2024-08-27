# forms/produto_fornecedorForm.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class ProdutoFornecedorForm(FlaskForm):
    id_produto = IntegerField('ID do Produto', validators=[DataRequired()])
    id_fornecedor = IntegerField('ID do Fornecedor', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto-Fornecedor')
