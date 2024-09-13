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
    nome TEXT NOT NULL, 
    descricao TEXT NOT NULL, 
    categoria TEXT NOT NULL, 
    quantidade_produto INTEGER NOT NULL , 
    preco_venda REAL NOT NULL DEFAULT 0
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


-- Table for Pedido (Order)
CREATE TABLE IF NOT EXISTS pedido ( 
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, 
    valor REAL NOT NULL,
    data DATE NOT NULL,
    status TEXT NOT NULL DEFAULT Aberto,
    id_cliente INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
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



    -- triggers


    -- Criação do trigger para atualizar o estoque ao inserir uma compra

    CREATE TRIGGER IF NOT EXISTS atualiza_estoque_venda
    AFTER INSERT ON pedido_produto
    BEGIN
        UPDATE produto
        SET quantidade_produto = quantidade_produto - NEW.quantidade_vendas
        WHERE id_produto = NEW.id_produto;
    END;



    -- Criação do trigger para calcular o valor total do pedido
    
    CREATE TRIGGER IF NOT EXISTS calcula_valor_pedido
    AFTER INSERT ON pedido
    BEGIN
        UPDATE pedido
        SET valor = (
            SELECT SUM(pd.quantidade_vendas * p.preco_venda)
            FROM pedido_produto pd
            JOIN produto p ON pd.id_produto = p.id_produto
            WHERE pd.id_pedido = NEW.id_pedido
        )
        WHERE id_pedido = NEW.id_pedido;
    END;
    

    -- Criação do trigger para atualizar o estoque ao vender um produto
    
    CREATE TRIGGER IF NOT EXISTS atualiza_estoque_pedido
    AFTER INSERT ON pedido
    BEGIN
        UPDATE produto
        SET quantidade_produto = quantidade_produto - (
            SELECT SUM(pd.quantidade_vendas)
            FROM pedido_produto pd
            WHERE pd.id_produto = produto.id_produto
            AND pd.id_pedido = NEW.id_pedido
        )
        WHERE id_produto IN (
            SELECT id_produto
            FROM pedido_produto
            WHERE id_pedido = NEW.id_pedido
        );
    END;


    -- Criação do trigger para verificar se o CPF é válido

    CREATE TRIGGER IF NOT EXISTS verifica_cpf_valido
    BEFORE INSERT ON pessoa
    BEGIN
        SELECT CASE
            WHEN NEW.cpf NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
            THEN RAISE(ABORT, 'CPF inválido')
        END;
    END;


    -- Criação do trigger para verificar a quantidade de vendas
    CREATE TRIGGER IF NOT EXISTS verifica_quantidade_vendas
    AFTER INSERT ON pedido_produto
    BEGIN
        DECLARE quantidade_vendas INTEGER;
        SELECT quantidade_vendas INTO quantidade_vendas
        FROM pedido_produto
        WHERE id_pedido = NEW.id_pedido
        AND id_produto = NEW.id_produto;
        
        IF quantidade_vendas < 5 THEN
            PRINT 'Atenção: A quantidade de vendas é menor que 5.';
        END IF;
    END;