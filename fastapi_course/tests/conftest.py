import pytest
from fastapi.testclient import TestClient

from fastapi_course.app import app

# o arquivo conftest.py é um arquivo de configuração de testes do pytest

# esse decorator permite reutilizar esse bloco de código de teste em
# outros arquivos, é uma forma de de centralizar recursos comuns de teste


@pytest.fixture
def client():
    return TestClient(app)
