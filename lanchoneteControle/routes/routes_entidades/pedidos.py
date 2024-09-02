# routes/pedidos.py
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db_utils import get_db_connection
from forms.pedidoForm import PedidoForm


pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_db_connection()
    produtos = conn.execute(''' SELECT * FROM produto WHERE quantidade_produto > 0''')
    produtos_data = [{
        'id': produto['id_produto'],
        'nome': produto['nome'],
        'preco': produto['preco_venda'],
        'descricao': produto['descricao']
    } for produto in produtos]
    conn.close()
    return jsonify(produtos_data)

@pedidos_bp.route('/pedidos/adicionarPedido', methods=('GET', 'POST'))
def adiciona_pedido():
    form = PedidoForm()

    if request.method == 'POST':
        print("AGGGGGGGGGGGGg")
        if form.validate_on_submit():
            id_cliente = form.id_cliente.data
            id_funcionario = form.id_funcionario.data
            data = form.data.data
           

            # Aqui você pode processar os dados do pedido e salvar no banco de dados
            print('ID Cliente:', id_cliente)
            print('ID Funcionário:', id_funcionario)
            print('Data:', data)
            print('Produtos:')
             # Processar os dados JSON enviados pelo campo oculto
            produtos_data = request.form.get('produtos_data')
            print(str(produtos_data))

            # Verifica se há algum produto selecionado
            if produtos_data :
                produtos = json.loads(produtos_data)  # Decodifica o JSON
                
                # Processar os produtos e criar o pedido no banco de dados
                for produto in produtos:
                    id_produto = produto['id_produto']
                    quantidade = produto['quantidade']
                    print(f"{id_produto} : {quantidade}")

                # Redirecionar ou renderizar uma página de sucesso
                return redirect(url_for('pedidos.lista_pedidos'))

    return render_template('adiciona_pedido.html', form=form)
    # form = PedidoForm()
    # conn = get_db_connection()


    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         quantidade_vendas = form.quantidade_vendas.data
    #         preco_venda = form.preco_venda.data
    #         id_cliente = form.id_cliente.data
    #         id_funcionario = form.id_funcionario.data
    #         id_venda = form.id_venda.data
    #         data = form.data.data

    #         # Valor Calculado no Back-End
    #         valor = 0.0

    #         conn.execute('''
    #             INSERT INTO pedido (quantidade_vendas, preco_venda, id_cliente, id_funcionario, id_venda, data, valor)
    #             VALUES (?, ?, ?, ?, ?, ?, ?)
    #         ''', (quantidade_vendas, preco_venda, id_cliente, id_funcionario, id_venda, data, valor))
    #         conn.commit()
    #         conn.close()

    #         flash('Pedido adicionado com sucesso!', 'success')
    #         return redirect(url_for('pedidos.lista_pedidos'))
    
    # return render_template('adiciona_pedido.html', form=form)


@pedidos_bp.route('/pedidos')
def lista_pedidos():
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido').fetchall()
    conn.close()
    return render_template('lista_pedidos.html', pedidos=pedidos)