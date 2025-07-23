"""
Arquivo de configuração do pytest reconhecido automaticamente pelo framework
"""

import pytest
from fastapi.testclient import TestClient

from curso_fastapi.app import app


# usado para evitar repetir client = TestClient(app) nos arquivos de teste toda hora
@pytest.fixture
def client():
    return TestClient(app)  # Cria um cliente de teste reutilizável
