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

## Refatorando a Estrutura do Projeto com Routers e Annotated

### Routers

- Permite organizar e agrupar diferentes rotas na aplicação
- Organizar por domínios
- Um "subaplicativo" FastAPI que pode ser montado em uma aplicação principal


### FAST na Análise Estática do Ruff

Podemos adicionar os padrões de boas práticas de código do FastAPI ao Ruff:

```toml
# pyproject.toml
[tool.ruff.lint]
preview = true
select = ['I', 'F', 'E', 'W', 'PL', 'PT', 'FAST']
```

### Annotated

É um recurso que o FastAPI suporta vindo da biblioteca nativa `typing`.
Ao definir uma anotação de tipo, seguimos o seguinte formato:

```python
session: Session = Depends(get_session)
```

Como o FastAPI recomenda usar:

```python
from typing import Annotated 

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
```

## Tornando o Projeto Assíncrono (asyncIO)

A aplicação fica `idle` quando fazemos acessos ao banco de dados e coisas do tipo. Chamamos isso de chamada bloqueante

O servidor (**uvicorn**) não bloqueia. Por padrão 2048 requisições podem aguardar no backlog

O servidor pode "copiar" a aplicação. Com isso, conseguimos distribuir as requisições de forma paralela

```bash
uvicorn api.app:app --workers 3
```

Com o código acima, criamos 3 cópias do servidor para permitir 3 acessos ao mesmo tempo na aplicação

**Essas cópias são processos.**

### Aplicação não Bloqueante

#### Corrotinas

Uma corrotina assíncrona basicamente é uma função em python que pode ser **escalonada** durante o bloqueio de I/O.

São criadas pela palavra `async` e o escalonamento é feito pela palavra `await`.

Uma das características de uma corrotina (coroutine) é o fato dela não ser executada quando chamada diretamente.

Ela precisa ser executada por um agente externo. Um **loop de eventos (`event loop`)**.

Dentro da biblioteca `asyncio` temos o método `get_event_loop()` e o `run_until_complete()`

#### Cooperatividade e Escalonamento

- Cooperatividade: habilidade de "passar a vez" para que outra corrotina seja executada.
- Escalonamento: é o que o loop faz ao trocar entre corrotinas durante a cooperação.

O `event loop` usando pelo **uvicorn** é o `uvloop`

### Banco de Dados e Bloqueios

#### Instalando o suporte a asyncio no sqlalchemy

```bash
poetry add "sqlalchemy[asyncio]"
```

#### Instalando o suporte a asyncio no sqlite

```bash
poetry add aiosqlite
```

Precisamos alterar nosso .env:

```.env
DATABASE_URL=sqlite+aiosqlite:...
```

#### Pytest com asyncio

```bash
poetry add --group dev pytest-asyncio
```


#### Coverage não suporta asyncio

Precisamos passar para o coverage.run:

```toml
[tool.coverage.run]
concurrency = ["thread", "greenlet"]
```

## Tornando o Sistema de Autenticação Robusto

### Criando Modelos Users sob Demanda

Podemos criar `users` de forma mais intuitiva e sem a preocupação de valores repetidos, podemos usar uma "fábrica" de `users`

Vamos utilizar a biblioteca `factory-boy`

```bash
poetry add --group dev factory-boy
```

> Fábrica é um padrão de projeto de construção de objetos (GoF)

### Tempo de expiração do Token

Para validar e poder testar se o tempo de expiração do Token está funcionando, podemos adicionar a biblioteca `freezegun` que ajuda a pausa o tempo durantes os testes

```bash
poetry add --group dev freezegun
```

## Rotas CRUD para Gerenciamento de Tarefas

- Criar um novo router
- Criar uma nova tabela no banco
- Criar novos schemas para tarefas
- Criar novos endpoints para tarefas


Introduzindo FuzzyChoice:

```python
import factory.fuzzy

state = factory.fuzzy.FuzzyChoice(TodoState) # por exemplo
```

É uma forma de escolher randomicamente algo

## Dockerizando a Aplicação e Introdução ao PostgreSQL

### Docker

- Ferramenta para criar containers

- Containers são formas de **isolar as dependências**. Da mesma forma que fazemos com o ambiente virtual, que isolam dependências python.

- No caso de containers Docker, estamos falando de isolamento de ferramentas do sistema operacional. Isolamos programas e ambientes de forma completa.

### PostgreSQL

- Escalabilidade: projetado para lidar com uma grande quantidade de dados e requisições

- Concorrência: permite múltiplas operações simultâneas.

- Funcionalidades avançadas: possui várias extensões e funcionalidades.

Subindo uma aplicação postgreSQL no Docker:

```bash
docker run --name app_database -e POSTGRES_USER=app_user -e POSTGRES_DB=app_db -e POSTGRES_PASSWORD=app_password -p 5432:5432 postgres
```

Podemos passar com a flag `-d` também.

Para listar os containers:

```bash
docker ps
```

A porta `5432:5430` significa que **MEU PC NA PORTA 5432** se comunica com a porta **5430 DO CONTAINER**

Listar imagens instaladas na minha máquina:

```bash
docker image ls
```

Listar containers na minha máquina:

```bash
docker container ls

# com mais detalhes:
docker container ls -a

# podemos usar outro comando:
docker ps

docker ps -a
```

Para iniciar um container parado:

```bash
docker start <nome_container>
```

Para remover um container:

```bash
docker rm <nome_container>

# ou

docker rm -f <nome_container>
```

Para remover uma imagem:

```bash
docker rmi <id_imagem>
```

Para limpar tudo de uma vez, podemos usar:

```bash
docker system prune -a
```

### Conectando nossa aplicação ao postgres

```bash
poetry add "psycopg[binary]"
```

Além disso, precisamos alterar a URL do banco de dados:

```.env
DATABASE_URL="postgresql+psycopg://app_user:app_password@127.0.0.1:5432/app_db"
```

Agora precisamos subir as migrações pro nosso container:

```bash
alembic upgrade head
```

No Windows, não funciona muito bem o async do psycopg, para isso podemos adicionar isso no início do nosso app.py:

```python
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

app = FastAPI()
```

### Banco de Dados nos Testes

Agora, vamos utilizar nosso banco de dados nos testes (retirando o sqlite:///:memory:)

Entretanto, se pararmos o banco de dados, não conseguimos rodar os testes

### Testando com Docker

Existe uma biblioteca que gerencia as dependências de containers externos para que a aplicação seja executada. O `TestContainers`

```bash
poetry add --group dev testcontainers
```

Ela cria um container pro teste, baixa a imagem e faz os testes, mas isso demora muito, dependendo do escopo da fixture.

### Escopo da Fixture

- function: executada em todas as funções de teste
- class: executada uma vez por classe de teste
- module: executada uma vez por módulo
- package: executada uma vez por pacote
- session: executada uma vez por execução de testes

A fixture do pytest tem diferentes escopos, por padrão, ela é do escopo de `function`, ou seja, executa uma função de teste, carrega outra fixture, faz o teste da função, carrega a fixture, ... 

Para resolver o problema com a lentidão de testes, iremos criar uma fixture para iniciar o container de banco de dados com o escopo `session`

### Criando a Imagem do Projeto

- Criar o arquivo `Dockerfile` na raiz do projeto

Para criar a imagem:

```bash
docker build -t "nome_imagem" .
```

Para iniciar a imagem:

```bash
docker run -it --name <nome_imagem> -p 8000:8000 <nome_imagem>:latest
```

### Docker Compose

A ideia do `docker compose` é criar um único arquivo `yaml` que reúna todos os containers necessários para executar a aplicação

Dessa forma, podemos gerenciar todos os containers com um único comando: `docker compose up`

Fazendo o build:

```bash
docker compose build
```

### Refazendo o container

```bash
docker compose up --build
```

### Para parar o container

```bash
docker compose down

# se quisermos remover o volume junto, usamos:
docker compose down -v
```

### Parar rodar o container em background

```bash
docker compose up -d
```

### Remover arquivos não utilizados

Como não estamos mais usando sqlite, podemos remover o aiosqlite:

```bash
poetry remove aiosqlite
```
