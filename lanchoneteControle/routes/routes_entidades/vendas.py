# routes/vendas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.vendaForm import VendaForm

vendas_bp = Blueprint('vendas', __name__)

@vendas_bp.route('/vendas/adicionarVenda', methods=('GET', 'POST'))
def adiciona_venda():
    form = VendaForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            id_produto = form.id_produto.data
            preco = form.preco.data
            data_inicio = form.data_inicio.data
            data_fim = form.data_fim.data

            conn.execute('''
                INSERT INTO venda (id_produto, preco, data_inicio, data_fim)
                VALUES (?, ?, ?, ?)
            ''', (id_produto, preco, data_inicio, data_fim))
            conn.commit()
            conn.close()

            flash('Venda adicionada com sucesso!', 'success')
            return redirect(url_for('vendas.adiciona_venda'))
    
    return render_template('adiciona_venda.html', form=form)


@vendas_bp.route('/vendas')
def lista_vendas():
    conn = get_db_connection()
    vendas = conn.execute('''
        SELECT v.*, p.nome AS nome_produto
        FROM venda v
        JOIN produto p ON v.id_produto = p.id_produto
    ''').fetchall()
    conn.close()
    return render_template('lista_vendas.html', vendas=vendas)
