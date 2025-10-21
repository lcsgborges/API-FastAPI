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

fastapi_course/
├── fastapi_course
│   └── __init__.py
├── pyproject.toml
├── README.md
└── tests
    └── __init__.py

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


