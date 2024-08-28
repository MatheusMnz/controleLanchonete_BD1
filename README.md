# Sistema de Controle de Lanchonete para Disciplina de Banco de Dados 1

Este projeto implementa um sistema de controle de lanchonete desenvolvido como parte da disciplina de Banco de Dados 1.

## Como Inicializar o Projeto

Siga os passos abaixo para configurar e iniciar o projeto:

### 1. Instalar Dependências

Na raiz do projeto, execute os seguintes comandos individualmente caso nao tenha os requisitos:

```bash
pip install virtualenv

pip install Flask

pip install Flask-WTF
```


Na pasta controleLanchonete_BD1:

```bash
cd controleLanchonete_BD1
```


### 2. Criacao do Ambiente Virtual:

```bash
python3 -m venv env
```

Em caso de erro na criacao do env:

```bash
sudo apt install python3.10-venv
```

e rode novamente o comando:

```bash
python3 -m venv env
```


### 3. Para inicializacao:

```bash
source env/bin/activate

cd lanchoneteControle/
 
python3 app.py  
```

caso de algum erro durante a inicializacao, rode os comandos de instalacao dos requisitos que forem apresentados no erro novamente