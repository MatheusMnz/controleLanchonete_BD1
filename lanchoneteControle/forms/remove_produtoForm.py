from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class remove_produtoForm(FlaskForm):
    id = StringField('ID do produto', validators=[DataRequired()])

