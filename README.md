# Curso FastAPI

## Configuração do ambiente de desenvolvimento

```bash
# para instalar pacotes executáveis
sudo apt install pipx
```

```bash
pipx install poetry 
pipx inject poetry poetry-plugin-shell
```

```bash
# criar um novo projeto
poetry new --flat nome_projeto
```

> A flag --flat é para criar o projeto sem a pasta 'src'

Organização da pasta após as configurações acima:

```bash
fastapi_course/
├── fastapi_course
│   └── __init__.py
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py
```

Instalando a versão do python no projeto usando poetry:

```bash
poetry python install 3.13
poetry python list 
poetry env use 3.13 # vai criar um ambiente virtual com a versão usada
```

Instalando dependências de outros projetos:

```bash
poetry install
```

Para instalar o FastAPI:

```bash
poetry add "fastapi[standard]"

# para rodar um servidor local com fastapi
poetry shell
fastapi dev app.py


# ou podemos usar o seguinte comando (não precisa ativar o ambiente virtual):
poetry run fastapi dev app.py
```

Instalando outras ferramentas:

- Ruff: Linter e formatador
- Pytest: Para escrever e rodar testes
- Taskipy: Para resumir comandos (parecido com Makefile)

> Observar a configuração no arquivo `pyproject.toml`

Para gerar um .gitignore:

```bash
pipx run ignr -p python > .gitignore
```

## Fundamentos do Desenvolvimento Web

Para rodar o servidor na rede local e abrir a aplicação para outros PC's na rede, é possível com o seguinte comando:

```bash
# só será preciso saber o IP da sua máquina
# no linux é só usar o seguinte comando:
ifconfig

poetry shell
fastapi dev fastapi_course/app.py --host 0.0.0.0
```

### HTTP - Códigos de Resposta

- 1xx: informativo
- 2xx: sucesso
- 3xx: redirecionamento
- 4xx: erro no **cliente**
- 5xx: erro no **servidor**

> Documentação: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

**Códigos importantes para o curso:**

- 200 OK: solicitação bem-sucedida
- 201 CREATED: solicitação bem-sucedida e novo recurso criado com sucesso
- 404 NOT FOUND: recurso solicitado não pôde ser encontrado
- 422 UNPROCESSABLE ENTITY: requisição está bem-formada, mas há erros semânticos
- 500 INTERNAL SERVER ERROR: erro na aplicação

> Pesquisar *templates* depois para renderizar páginas

### APIs

API é uma interface de comunicação entre aplicações. Frequentemente utilizam JSON por ser leve, fácil de escrever e ler (RPC)

**APIRest** precisa trocar HTML.

### Contratos (Schemas)

É crucial estabelecer um entendimento mútuo sobre as estruturas dos dados que serão trocados

- Pydantic: a ideia é criar uma camada de documentação e de fazer a validação dos modelos de entrada e saída da nossa API.

## Criando Rotas CRUD

- **C**reate: (POST)
- **R**ead: (GET)
- **U**pdate: (PUT)
- **D**elete: (DELETE)

> Payload: é o corpo da mensagem que contém os dados reais sendo transferidos entre um cliente e um servidor


## Banco de Dados com SQLAlchemy e Gerenciando Migrações com Alembic

### SQLAlchemy

O *SQLAlchemy* possui um ORM (Mapeamento Objeto-Relacional) que permite vincular objetos a registros de banco de dados. Isso permite fazer consultas e interagir com o banco de dados como se estivesse trabalhando com objetos Python

**Por que usar ORM:**

- Abstração de banco de dados
- Segurança (escapar de consultas e injeções SQL)
- Eficiência no desenvolvimento

Adicionar sqlalchemy:

```bash
poetry add sqlalchemy
```

#### Engine

É o ponto de contato com o banco de dados, estabelecendo e gerenciando conexões. É instanciada através da função *create_engine()*, que recebe as credenciais do banco de dados, o endereço da conexão (URI) e configura uma pull de conexões.

#### Session

É a principal interface quanto à persistência de dados e consultas ao banco de dados utilizando ORM. Atua como intermediário entre o Python e o banco de dados, mediada pela Engine. A Session é encarregada de todas as transações, fornecendo uma API para conduzi-las.


#### Migrações

É uma forma de controlar e versionar as mudanças no banco de dados de um projeto

É bom pensar nas migrações como um **git** para o banco de dados.

Cada migração é um arquivo que descreve uma alteração feita na estrutura do banco (schema).

**Código para o alembic:**

```bash
# cria uma pasta chamada migrations para trabalhar com o alembic
alembic init migrations

# configurar o arquivo env.py

# iniciar uma migração com revisão
alembic revision --autogenerate -m "mensagem"

# aplicando a migração
alembic upgrade head
```

### Padrões da Sessão

- **1. Repositório:** A sessão atua como um repositório
- **2. Unidade de Trabalho:** Quando a sessão é aberta, todos os dados inseridos, modificados ou removidos não são feitos de imediato no banco de dados. Fazemos todas as modificações que queremos e executamos uma unica ação.
- **3. Mapeamento de Identidade:** É criado cache para entidades que já estão carregadas na sessão para evitar conexões desnecessárias.


### Gerenciamento de Dependências no FastAPI

É uma forma declarativa de dizer ao FastAPI:

"Antes de executar esta função, execute primeiro essa outra função e passe o resultado para o parâmetro"

Isso ocorre por meio do objeto *Depends*

## Autenticação e Autorização com Tokens JWT

### Armazenamento de Senhas

Salvar no banco de dados somente o hash das senhas

```bash
# utilizar o pwdlib2 e argon2
poetry add "pwdlib2[argon2]"
```

- pwdlib: biblioteca criada especialmente para manipular hashs de senhas
- argon2: algoritmo de hash

### Token JWT

O Json Web Token (JWT) é uma forma de assinatura do servidor. Ele diz que o cliente foi autenticado com a assinatura desse servidor. Ele é dividido em 3 partes:

- **Header:** Algoritmo + Tipo de Token
- **Payload:** Dados que serão usados para assinatura
- **Assinatura:** Aplicação do algoritmo + Chave secreta da aplicação

#### Payloads e as claims

- **sub:** identifica o assunto (subject), basicamente uma forma de identificar o cliente (email, uuid, ...)
- **exp:** tempo de expiração do token. O backend vai usar esse dado para validar se o token ainda é válido.

```json
{
    "sub": "test@test.com",
    "exp": 1690258153
}
```

> Site para visualizar: [JSON Web Token Claims](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims)

Geração de tokens JWT com Python:

```python
poetry add pyjwt
```

> Gerar um token aleatório com python

```python
import secrets

secrets.token_hex()
```

### Autorização

A ideia é garantir que somente pessoas autorizadas possam executar determinadas operações.

Agora que temos os tokens, podemos garantir que somente clientes com contas já criadas e logadas possam ter acesso aos endpoints:

- Listar: somente se estiver logado
- Deletar: somente se a conta for sua
- Alterar: somente se a conta for sua

