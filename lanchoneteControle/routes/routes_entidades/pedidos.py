# routes/pedidos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.pedidoForm import PedidoForm

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos/adicionarPedido', methods=('GET', 'POST'))
def adiciona_pedido():
    form = PedidoForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            quantidade_vendas = form.quantidade_vendas.data
            preco_venda = form.preco_venda.data
            id_cliente = form.id_cliente.data
            id_funcionario = form.id_funcionario.data
            id_venda = form.id_venda.data
            data = form.data.data
            valor = form.valor.data

            conn.execute('''
                INSERT INTO pedido (quantidade_vendas, preco_venda, id_cliente, id_funcionario, id_venda, data, valor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (quantidade_vendas, preco_venda, id_cliente, id_funcionario, id_venda, data, valor))
            conn.commit()
            conn.close()

            flash('Pedido adicionado com sucesso!', 'success')
            return redirect(url_for('pedidos.adiciona_pedido'))
    
    return render_template('adiciona_pedido.html', form=form)


@pedidos_bp.route('/pedidos')
def lista_pedidos():
    conn = get_db_connection()
    pedidos = conn.execute('SELECT * FROM pedido').fetchall()
    conn.close()
    return render_template('lista_pedidos.html', pedidos=pedidos)