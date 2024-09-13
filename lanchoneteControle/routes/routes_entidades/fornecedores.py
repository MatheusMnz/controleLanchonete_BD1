# routes/fornecedores.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.fornecedorForm import FornecedorForm, RemoveFornecedorForm

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

@fornecedores_bp.route('/fornecedores/removerFornecedor', methods=('GET', 'POST'))
def remove_fornecedor_form():
    form = RemoveFornecedorForm()
    conn = get_db_connection()

    # Preencher o campo SelectField com os fornecedores disponíveis
    fornecedores = conn.execute('SELECT id_fornecedor, nome FROM fornecedor').fetchall()
    form.fornecedor_id.choices = [(f['id_fornecedor'], f['nome']) for f in fornecedores]

    if request.method == 'POST':
        if form.validate_on_submit():
            fornecedor_id = form.fornecedor_id.data
            conn.execute('DELETE FROM fornecedor WHERE id_fornecedor = ?', (fornecedor_id,))
            conn.commit()
            conn.close()
            flash('Fornecedor removido com sucesso!', 'success')
            return redirect(url_for('fornecedores.lista_fornecedores'))
    
    conn.close()
    return render_template('remove_fornecedor.html', form=form)
