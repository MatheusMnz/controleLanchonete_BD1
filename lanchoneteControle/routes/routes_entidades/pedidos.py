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
    conn = get_db_connection()

    
    print("Preenchendo Valores")
    funcionarios = conn.execute('''SELECT pessoa.nome, funcionario.id_funcionario 
                                    FROM pessoa INNER JOIN funcionario ON pessoa.id_pessoa = funcionario.id_pessoa''').fetchall()
    form.id_funcionario.choices = [(funcionario['id_funcionario'],f"{funcionario['id_funcionario']} - {funcionario['nome']}") for funcionario in funcionarios]


    if request.method == 'POST':

        if form.validate_on_submit():
            id_cliente = form.id_cliente.data
            id_funcionario = form.id_funcionario.data
            data = form.data.data
            preco_total = form.preco_total.data

            # Aqui você pode processar os dados do pedido e salvar no banco de dados
            print('ID Cliente:', id_cliente)
            print('ID Funcionário:', id_funcionario)
            print('Data:', data)
            print('Preço Total', preco_total)
            print('Produtos:')
             # Processar os dados JSON enviados pelo campo oculto
            produtos_data = request.form.get('produtos_data')
            print(str(produtos_data))

            # Verifica se há algum produto selecionado
            if produtos_data :
                curs = conn.execute('''
                        INSERT INTO pedido (valor,data,status, id_cliente, id_funcionario)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (preco_total,data,"Aberto", id_cliente, id_funcionario))
                conn.commit()

                produtos = json.loads(produtos_data)  # Decodifica o JSON

                lst_row_id = curs.lastrowid
                print("Pedido ID : ", lst_row_id)
                # Processar os produtos e criar o pedido no banco de dados
                for produto in produtos:
                    id_produto = produto['id_produto']
                    quantidade = produto['quantidade']
                    preco = produto['preco']
                    print(f"{id_produto} : {quantidade} : {preco}")
                    conn.execute('''
                        INSERT INTO pedido_produto (id_pedido,id_produto, quantidade_vendas, preco_venda)
                        VALUES (?, ?, ?, ?) ''', 
                        (lst_row_id,id_produto,quantidade,preco ))
                    conn.commit()
                    
                conn.close()

                # Redirecionar ou renderizar uma página de sucesso
                return redirect(url_for('pedidos.lista_pedidos'))

    return render_template('adiciona_pedido.html', form=form)



@pedidos_bp.route('/pedidos/atualizar_status', methods=['POST'])
def atualizar_status_pedido():
    data = request.get_json()
    print(data)
    id_pedido = data.get('id_pedido')
    novo_status = data.get('novo_status')

    print(id_pedido,novo_status)

    # conn = get_db_connection()
    # query = conn.execute(f"UPDATE pedido SET status={novo_status} WHERE pedido.id_pedido={id_pedido}; ")
    # conn.commit()
    # conn.close()
    # if query:
    #     return jsonify({'success': True}), 200
    # else:
    #     return jsonify({'error': 'Pedido não encontrado'}), 404
    return jsonify({'success': True}), 200

@pedidos_bp.route('/pedidos/itens/<int:id_pedido>', methods=['GET'])
def get_itens_pedido(id_pedido):
    conn = get_db_connection()
    itens = conn.execute('''SELECT * FROM pedido_produto pd INNER JOIN produto p ON p.id_produto = pd.id_produto 
                         WHERE pd.id_pedido = ?''',(int(id_pedido),))

    # Formatar os itens para JSON
    itens_lista = [{'nome_produto': item['nome'], 'quantidade': item['quantidade_vendas']} for item in itens]

    # Retornar os itens como JSON
    return jsonify(itens_lista)

@pedidos_bp.route('/pedidos')
def lista_pedidos():
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido').fetchall()
    conn.close()
    return render_template('lista_pedidos.html', pedidos=pedidos)