# routes/produto_fornecedor.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.produto_fornecedorForm import ProdutoFornecedorForm

produto_fornecedor_bp = Blueprint('produto_fornecedor', __name__)

@produto_fornecedor_bp.route('/produto_fornecedor/adicionar', methods=('GET', 'POST'))
def adiciona_produto_fornecedor():
    form = ProdutoFornecedorForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            id_produto = form.id_produto.data
            id_fornecedor = form.id_fornecedor.data
            data = form.data.data
            preco_compra = form.preco_compra.data

            conn.execute('''
                INSERT INTO produto_fornecedor (id_produto, id_fornecedor, data, preco_compra)
                VALUES (?, ?, ?, ?)
            ''', (id_produto, id_fornecedor, data, preco_compra))
            conn.commit()
            conn.close()

            flash('Produto-Fornecedor adicionado com sucesso!', 'success')
            return redirect(url_for('produto_fornecedor.adiciona_produto_fornecedor'))
    
    return render_template('adiciona_produto_fornecedor.html', form=form)


# Rota para listar todos os produtos associados a um fornecedor específico
@produto_fornecedor_bp.route('/produto_fornecedor/<int:id_fornecedor>/produtos')
def lista_produtos_fornecedor(id_fornecedor):
    conn = get_db_connection()
    produtos = conn.execute('''
        SELECT p.nome, pf.preco_compra, pf.data
        FROM produto_fornecedor pf
        JOIN produto p ON pf.id_produto = p.id_produto
        WHERE pf.id_fornecedor = ?
    ''', (id_fornecedor,)).fetchall()
    conn.close()
    return render_template('lista_produtos_fornecedor.html', produtos=produtos, id_fornecedor=id_fornecedor)