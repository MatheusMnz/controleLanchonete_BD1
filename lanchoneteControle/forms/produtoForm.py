from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    categoria = SelectField('Categoria',choices=["SALGADOS","DOCES","BEBIDAS"], validators=[DataRequired()])
    preco_venda = FloatField('Preço',validators=[DataRequired()])
    quantidade_produto = IntegerField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')
