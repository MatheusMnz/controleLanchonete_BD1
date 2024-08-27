# routes/fornecedores.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.fornecedorForm import FornecedorForm

fornecedores_bp = Blueprint('fornecedores', __name__)

@fornecedores_bp.route('/fornecedores/adicionarFornecedor', methods=('GET', 'POST'))
def adiciona_fornecedor():
    form = FornecedorForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            nome = form.nome.data
            endereco = form.endereco.data
            contato = form.contato.data

            conn.execute('''
                INSERT INTO fornecedor (nome, endereco, contato)
                VALUES (?, ?, ?)
            ''', (nome, endereco, contato))
            conn.commit()
            conn.close()

            flash('Fornecedor adicionado com sucesso!', 'success')
            return redirect(url_for('fornecedores.adiciona_fornecedor'))
    
    return render_template('adiciona_fornecedor.html', form=form)


@fornecedores_bp.route('/fornecedores')
def lista_fornecedores():
    conn = get_db_connection()
    fornecedores = conn.execute('SELECT * FROM fornecedor').fetchall()
    conn.close()
    return render_template('lista_fornecedores.html', fornecedores=fornecedores)
