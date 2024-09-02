# forms/pedidoForm.py
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateField, SubmitField, SelectField, FieldList, FormField, StringField, HiddenField
from wtforms.validators import DataRequired, NumberRange


# class ProdutoForm(FlaskForm):
#     id_produto = IntegerField('ID do Produto', validators=[DataRequired()])
#     quantidade = IntegerField('Quantidade', validators=[DataRequired()])

class PedidoForm(FlaskForm):
    id_cliente = IntegerField('ID do Cliente', validators=[DataRequired()])
    id_funcionario = IntegerField('ID do Funcionário', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    # produtos = FieldList(FormField(ProdutoForm), min_entries=1)
    produtos_data = HiddenField()
    submit = SubmitField('Adicionar Produto')

