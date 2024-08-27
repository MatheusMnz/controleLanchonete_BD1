from flask import Blueprint, flash, render_template, request, redirect, url_for
from db_utils import get_db_connection
from forms.dados_vendaForm import produtoPreco_Venda


# Mapeando BluePrint para dados de venda
dados_venda_bp = Blueprint('dados_venda', __name__)


@dados_venda_bp.route('/estoque/<int:id>/dados_venda')
def lista_dados_venda(id):
    conn = get_db_connection()
    dados_venda = conn.execute('''
        SELECT v.*, p.nome AS nome_produto
        FROM venda v
        INNER JOIN produto p ON v.id_produto = p.id_produto
        WHERE v.id_produto = ?
    ''', (id,)).fetchall()
    conn.close()
    if not dados_venda:
        return 'Nenhum dado de venda encontrado!', 404
    return render_template('lista_dados_venda.html', dados_venda=dados_venda)


@dados_venda_bp.route('/estoque/<int:id>/dados_venda/edit', methods=('GET', 'POST'))
def atualiza_dados_venda(id):
    conn = get_db_connection()
    dados_venda = conn.execute('SELECT * FROM venda WHERE id_produto = ?', (id,)).fetchone()
    form = produtoPreco_Venda()
    
    if dados_venda is None:
        conn.close()
        return 'Dados de venda não encontrados!', 404
    
    if request.method == 'POST':
        if form.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
            preco_venda_novo = form.preco_venda.data

            try:
                # Tentativa de conversão para float
                preco_venda_novo_float = float(preco_venda_novo)
                if preco_venda_novo_float <= 0:
                    flash('O preço de venda deve ser um número positivo.', 'error')
                    return render_template('atualiza_dados_venda.html', form=form, dados_venda=dados_venda)
            except ValueError:
                flash('O preço de venda deve ser um número válido.', 'error')
                return render_template('atualiza_dados_venda.html', form=form, dados_venda=dados_venda)

            # Atualização
            conn.execute('UPDATE venda SET preco = ? WHERE id_produto = ?', (preco_venda_novo_float, id))
            conn.commit()
            conn.close()
            flash('Preço de venda atualizado com sucesso!', 'success')
            return redirect(url_for('dados_venda.lista_dados_venda', id=id))

    conn.close()
    return render_template('atualiza_dados_venda.html', form=form, dados_venda=dados_venda)
