from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class produtoPreco_Venda(FlaskForm):
    preco_venda = DecimalField('Preço de Venda', validators=[DataRequired(), NumberRange(min=0, message="O preço deve ser um número positivo.")])
    submit = SubmitField('Salvar')
