# routes/precos_compra.py
from flask import Blueprint, flash, render_template, request, redirect, url_for
from db_utils import get_db_connection
from forms.dados_compraForm import produtoPreco_Compra

# Mapeando BluePrint
dados_compra_bp = Blueprint('dados_compra', __name__)


@dados_compra_bp.route('/estoque/historico_compras/')
def lista_hist_compras():
    conn = get_db_connection()
        # Gera uma consulta que contem todos os produtos
    query = '''SELECT * FROM produto_fornecedor'''
    historico_compras = conn.execute(query).fetchall()
    conn.close()
    # Renderiza a pagina de históricos
    return render_template('historico_compras.html',historico_compras=historico_compras)

@dados_compra_bp.route('/estoque/<int:id>/dados_compra')
def lista_dados_compra(id):
    conn = get_db_connection()
    dados_produto = conn.execute('''
        SELECT pf.*, f.nome AS nome_fornecedor
        FROM produto_fornecedor pf
        INNER JOIN fornecedor f ON pf.id_fornecedor = f.id_fornecedor
        WHERE pf.id_produto = ?
    ''', (id,)).fetchall()
    conn.close()
    if dados_produto is None:
        return 'Preço não encontrado!', 404
    return render_template('lista_dados_compra.html', dados_produto=dados_produto)


@dados_compra_bp.route('/estoque/<int:id>/dados_compra/edit', methods=('GET', 'POST'))
def atualiza_dados_compra(id):
    conn = get_db_connection()
    dados_produto = conn.execute('SELECT * FROM produto_fornecedor WHERE id_produto = ?', (id,)).fetchone()
    form = produtoPreco_Compra()
    
    if dados_produto is None:
        conn.close()
        return 'Preço não encontrado!', 404
    
    if request.method == 'POST':
        # Verifica se o formulário foi enviado e é válido
        if form.validate_on_submit():  
            # Extrai os dados do formulário
            preco_compra_novo = form.preco_compra.data

            try:
                # Tentativa de conversão para float
                preco_compra_novo_float = float(preco_compra_novo)
                if preco_compra_novo_float <= 0:
                    flash('O preço de compra deve ser um número positivo.', 'error')
                    return render_template('atualiza_dados_compra.html', form=form, dados_produto=dados_produto)
            except ValueError:
                flash('O preço de compra deve ser um número válido.', 'error')
                return render_template('atualiza_dados_compra.html', form=form, dados_produto=dados_produto)

            # Atualização
            conn.execute('UPDATE produto_fornecedor SET preco_compra = ? WHERE id_produto = ?', (preco_compra_novo_float, id))
            conn.commit()
            conn.close()
            flash('Preço de compra atualizado com sucesso!', 'success')
            return redirect(url_for('dados_compra.lista_dados_compra', id=id))

    return render_template('atualiza_dados_compra.html', form=form, dados_produto=dados_produto)
