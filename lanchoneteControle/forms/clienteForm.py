# forms/clienteForm.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ClienteForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired(), Length(max=11)])
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(max=200)])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=0, max=120)])
    submit = SubmitField('Adicionar Cliente')
