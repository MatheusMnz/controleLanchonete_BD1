# app.py
from flask import Flask
from db_utils import get_db_connection, close_db_connection
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'menezes'
csrf = CSRFProtect(app)

# Registra os blueprints
from routes import estoque_bp, dados_compra_bp, dados_venda_bp, clientes_bp, home_bp
from routes import fornecedores_bp, pedidos_bp, produto_fornecedor_bp
app.register_blueprint(estoque_bp)
app.register_blueprint(dados_venda_bp)
app.register_blueprint(dados_compra_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(fornecedores_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(produto_fornecedor_bp)
app.register_blueprint(home_bp)

# Fecha a conexão com o banco de dados ao final da requisição
app.teardown_appcontext(close_db_connection)

def init_db():
    db = get_db_connection()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
