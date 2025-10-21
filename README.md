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
