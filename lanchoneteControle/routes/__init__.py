# Importa os blueprints para que eles sejam registrados no aplicativo
from .routes_entidades.estoque import estoque_bp
from .routes_entidades.dados_compra import dados_compra_bp
from .routes_entidades.dados_venda import dados_venda_bp
from .routes_entidades.clientes import clientes_bp
from .routes_entidades.fornecedores import fornecedores_bp
from .routes_entidades.pedidos import pedidos_bp
from .routes_entidades.produto_fornecedor import produto_fornecedor_bp
from .routes_entidades.vendas import vendas_bp
from .routes_entidades.home import home_bp


# Lista de todos os blueprints que você deseja registrar
__all__ = [
    'estoque_bp',
    'dados_venda_bp',
    'dados_compra_bp',
    'clientes_bp',
    'fornecedores_bp',
    'pedidos_bp',
    'produto_fornecedor_bp',
    'vendas_bp',
    'home_bp'
]
