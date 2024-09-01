# routes/estoque.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.produtoForm import ProdutoForm
from forms.remove_produtoForm import remove_produtoForm

estoque_bp = Blueprint('estoque', __name__)

# Busca todos os produtos existentes no Estoque
@estoque_bp.route('/estoque')
def lista_estoque():
    conn = get_db_connection()
    estoque = conn.execute('SELECT * FROM produto').fetchall()
    conn.close()
    return render_template('lista_estoque.html', estoque=estoque)


# Detalha o produto em questão
@estoque_bp.route('/estoque/<int:id>')
def detalhe_estoque(id):
    conn = get_db_connection()
    item_estoque = conn.execute('SELECT * FROM produto WHERE id_produto = ?', (id,)).fetchone()
    conn.close()
    if item_estoque is None:
        return 'Item não encontrado!', 404
    return render_template('detalhe_estoque.html', item_estoque=item_estoque)


# Permite a alteração de dados de um Produto
@estoque_bp.route('/estoque/<int:id>/edit', methods=('GET', 'POST'))
def atualiza_estoque(id):
    conn = get_db_connection()
    item_estoque = conn.execute('SELECT * FROM produto WHERE id_produto = ?', (id,)).fetchone()
    form = ProdutoForm()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        quantidade_produto = request.form['quantidade_produto']

        conn.execute('UPDATE produto SET nome = ?, descricao = ?, categoria = ?, quantidade_produto = ? WHERE id_produto = ?',
                     (nome, descricao, categoria, quantidade_produto, id))
        conn.commit()
        conn.close()
        return redirect(url_for('estoque.detalhe_estoque', id=id))

    conn.close()
    return render_template('atualiza_estoque.html', form=form, item_estoque=item_estoque)


# Adiciona um Produto ao Banco de Dados
@estoque_bp.route('/estoque/adicionarProduto', methods=('GET', 'POST'))
def adiciona_produto():
    form = ProdutoForm()
    conn = get_db_connection()

    form.categoria.choices = ["SALGADOS","DOCES","BEBIDAS"]
    if request.method == 'POST':
        if form.validate_on_submit():  # Verifica se o formulário foi enviado e é válido
            # Extrai os dados do formulário
            nome = form.nome.data
            descricao = form.descricao.data
            categoria = form.categoria.data
            quantidade_produto = form.quantidade_produto.data


            conn.execute('''
                INSERT INTO produto (nome, descricao, categoria, quantidade_produto)
                VALUES (?, ?, ?, ?)
            ''', (nome, descricao, categoria, quantidade_produto))
            conn.commit()
            conn.close()

            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('estoque.lista_estoque'))
    
    return render_template('adiciona_produto.html', form=form)


# Busca um Produto para remoção com base no ID inserido 
@estoque_bp.route('/estoque/removerProduto/', methods=('GET', 'POST'))
def remove_produto():
    form = remove_produtoForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            id_produto = form.id.data

            # Buscar o produto pelo ID (opcional, já que o ID está no form)
            item_estoque = conn.execute('SELECT * FROM produto WHERE id_produto = ?', (id_produto,)).fetchone()

            if item_estoque is None:
                flash('Produto não encontrado!', 'error')
                return redirect(url_for('estoque.lista_estoque'))

            # Redirecionar para a página de confirmação, passando o ID do produto
            return redirect(url_for('estoque.confirma_remocao', form=form, id=id_produto))

    # Renderizar o formulário para usuário inserir o ID do produto a ser removido
    return render_template('remove_produto.html', form=form)


# Confirma remoção do Produto especificado pelo ID.
@estoque_bp.route('/estoque/removerProduto/confirmar/<int:id>', methods=('GET', 'POST'))
def confirma_remocao(id):
    conn = get_db_connection()
    form = remove_produtoForm()


    # Buscar o produto pelo ID
    item_estoque = conn.execute('SELECT * FROM produto WHERE id_produto = ?', (id,)).fetchone()

    if item_estoque is None:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('estoque.lista_estoque'))

    if request.method == 'POST':
        # Excluir o produto
        conn.execute('DELETE FROM produto WHERE id_produto = ?', (id,))
        conn.commit()
        conn.close()

        flash('Produto removido com sucesso!', 'success')
        return redirect(url_for('estoque.lista_estoque'))

    # Renderizar a página de confirmação
    return render_template('confirma_remocao.html', form=form, item_estoque=item_estoque)


