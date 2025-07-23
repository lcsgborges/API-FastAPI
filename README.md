# Curso de FastAPI - Eduardo Mendes (https://www.youtube.com/@Dunossauro)

(Link)[https://fastapidozero.dunossauro.com/estavel]

--- 

## Aula 01

> Configurações do ambiente de desenvolvimento

### Instalações: 

* pyenv (gerenciador de versões do python)
* pipx (instalações globais)
* poetry (gerenciador de projetos python)

### Criar uma estrutura simples usando Poetry:

```bash

poetry new <nome_projeto>

pyenv local <versão python>

poetry install # cria o ambiente virtual

poetry add <nome_biblioteca>

poetry add fastapi # adicionar o fastapi (semelhante ao pip install fastapi)

poetry shell # entra no ambiente virtual

fastapi dev <projeto.py> # inicia o servidor da api

```

### Ambiente para desenvolvimento:

``` bash

poetry add --group dev ruff # linter e formatador

poetry add --group dev pytest pytest-cov # testes

poetry add --group dev taskipy # facilitar comandos

```

## Aula 02

> Fundamentos da WEB

```bash 

# para servir a aplicação local (LAN):

fastapi dev <aplicacao> --host 0.0.0.0

# linux: ip addr

```

Descobrindo o ip com Python:

```python

import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
s.getsockname()[0]
```

> [Verbos/Métodos HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Methods)

> [Status de Respostas HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Status)