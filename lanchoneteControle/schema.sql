-- Table for Pessoa (Person)
CREATE TABLE IF NOT EXISTS pessoa(
    id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    idade INTEGER NOT NULL
);

-- Table for Cliente (Client)
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pessoa INTEGER NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa)
);

-- Table for Funcionario (Employee)
CREATE TABLE IF NOT EXISTS funcionario (
    id_funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pessoa INTEGER NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id_pessoa)
);

-- Table for Produto (Product)
CREATE TABLE IF NOT EXISTS produto (
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produto TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade_produto INTEGER NOT NULL
);

-- Table for Fornecedor (Supplier)
CREATE TABLE IF NOT EXISTS fornecedor (
    id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_fornecedor TEXT NOT NULL,
    endereco TEXT NOT NULL,
    contato TEXT NOT NULL
);

-- Table for Produto-Fornecedor Relationship
CREATE TABLE IF NOT EXISTS produto_fornecedor (
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_produto INTEGER NOT NULL,
    id_fornecedor INTEGER NOT NULL,
    data DATE NOT NULL,
    preco_compra REAL NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id_fornecedor)
);


-- Estava errado no diagrama, correção feita pelo Evandrino
-- -- Table for Venda (Sale)
-- CREATE TABLE IF NOT EXISTS venda (
--     id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
--     id_produto INTEGER NOT NULL,
--     preco REAL NOT NULL,
--     data_inicio DATE NOT NULL,
--     data_fim DATE,
--     FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
-- );

-- Table for Pedido (Order)
CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    quantidade_vendas INTEGER NOT NULL,
    preco_venda REAL NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    id_venda INTEGER NOT NULL,
    data DATE NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario),
    FOREIGN KEY (id_venda) REFERENCES venda(id_venda)
);

-- Table for Pedido-Produto Relationship
CREATE TABLE IF NOT EXISTS pedido_produto (
    id_pedido INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade_vendas INTEGER NOT NULL,
    preco_venda REAL NOT NULL,
    PRIMARY KEY (id_pedido, id_produto),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);
