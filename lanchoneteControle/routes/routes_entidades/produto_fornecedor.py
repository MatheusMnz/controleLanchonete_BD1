# routes/produto_fornecedor.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.produto_fornecedorForm import ProdutoFornecedorForm

produto_fornecedor_bp = Blueprint('produto_fornecedor', __name__)

@produto_fornecedor_bp.route('/produto_fornecedor/adicionar', methods=('GET', 'POST'))
def adiciona_produto_fornecedor():
    form = ProdutoFornecedorForm()
    conn = get_db_connection()

   
    # Populando o campo 'id_produto' com os produtos do banco de dados
    produtos = conn.execute('SELECT id_produto, nome FROM produto').fetchall()
    form.id_produto.choices = [(produto['id_produto'],f"{produto['id_produto']} - {produto['nome']}") for produto in produtos]

    # Populando o campo 'id_fornecedor' com os fornecedores do banco de dados
    fornecedores = conn.execute('SELECT id_fornecedor, nome FROM fornecedor').fetchall()
    form.id_fornecedor.choices = [(fornecedor['id_fornecedor'], f"{fornecedor['id_fornecedor']} - {fornecedor['nome']}") for fornecedor in fornecedores]

    if(request.method == 'POST'):
        print(f"Preenche {form}")
        if form.validate_on_submit(): 
            print("Valido")
            # Captura os dados do formulário    
            id_produto = form.id_produto.data
            id_fornecedor = form.id_fornecedor.data
            preco_compra = form.preco_compra.data
            quantidade = form.quantidade.data
            data = form.data_compra.data

            # Insere os dados na tabela produto_fornecedor
            conn.execute('''
                INSERT INTO produto_fornecedor (id_produto, id_fornecedor, data, preco_compra, quantidade)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_produto, id_fornecedor, data, preco_compra, quantidade))
            conn.commit()
            conn.close()

            flash('Produto e Fornecedor adicionados com sucesso!', 'success')
            return redirect(url_for('dados_compra.lista_hist_compras'))

    conn.close()
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