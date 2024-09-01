# forms/produto_fornecedorForm.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired

class ProdutoFornecedorForm(FlaskForm):
    id_produto = SelectField('Produto', choices=[], coerce=int, validators=[DataRequired()])
    id_fornecedor = SelectField('Fornecedor', choices=[], coerce=int, validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    data_compra = DateField('Data da Compra', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Adicionar')   
