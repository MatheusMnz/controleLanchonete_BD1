from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    categoria = StringField('Categoria', validators=[DataRequired()])
    quantidade_produto = IntegerField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')
