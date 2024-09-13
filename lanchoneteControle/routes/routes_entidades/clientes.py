# routes/clientes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_utils import get_db_connection
from forms.clienteForm import ClienteForm, RemoveClienteForm

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes/adicionarCliente', methods=('GET', 'POST'))
def adiciona_cliente():
    form = ClienteForm()
    conn = get_db_connection()

    if request.method == 'POST':
        if form.validate_on_submit():
            cpf = form.cpf.data
            nome = form.nome.data
            endereco = form.endereco.data
            idade = form.idade.data

            conn.execute('''
                INSERT INTO pessoa (cpf, nome, endereco, idade)
                VALUES (?, ?, ?, ?)
            ''', (cpf, nome, endereco, idade))
            id_pessoa = conn.execute('SELECT id_pessoa FROM pessoa WHERE cpf = ?', (cpf,)).fetchone()[0]
            conn.execute('INSERT INTO cliente (id_pessoa) VALUES (?)', (id_pessoa,))
            conn.commit()
            conn.close()

            flash('Cliente adicionado com sucesso!', 'success')
            return redirect(url_for('clientes.adiciona_cliente'))
    
    return render_template('adiciona_cliente.html', form=form)

@clientes_bp.route('/clientes')
def lista_clientes():
    conn = get_db_connection()
    clientes = conn.execute('''
        SELECT p.id_pessoa, p.cpf, p.nome, p.endereco, p.idade
        FROM pessoa p
        INNER JOIN cliente c ON p.id_pessoa = c.id_pessoa
    ''').fetchall()
    conn.close()
    return render_template('lista_clientes.html', clientes=clientes)

@clientes_bp.route('/clientes/removerCliente', methods=('GET', 'POST'))
def remove_cliente_form():
    form = RemoveClienteForm()
    conn = get_db_connection()

    # Preenche o campo SelectField com os clientes disponíveis
    clientes = conn.execute('''
        SELECT p.id_pessoa, p.nome
        FROM pessoa p
        INNER JOIN cliente c ON p.id_pessoa = c.id_pessoa
    ''').fetchall()

    if clientes:
        form.cliente_id.choices = [(c['id_pessoa'], c['nome']) for c in clientes]
    else:
        form.cliente_id.choices = []  # Evitar que choices seja None

    if request.method == 'POST':
        if form.validate_on_submit() and form.cliente_id.data:
            cliente_id = form.cliente_id.data
            conn.execute('DELETE FROM cliente WHERE id_pessoa = ?', (cliente_id,))
            conn.execute('DELETE FROM pessoa WHERE id_pessoa = ?', (cliente_id,))
            conn.commit()
            conn.close()
            flash('Cliente removido com sucesso!', 'success')
            return redirect(url_for('clientes.lista_clientes'))

    conn.close()
    return render_template('remove_cliente.html', form=form)
