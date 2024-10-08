# forms/fornecedorForm.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    contato = StringField('Contato', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Adicionar Fornecedor')
