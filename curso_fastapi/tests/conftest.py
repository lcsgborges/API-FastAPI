"""
Arquivo de configuração do pytest reconhecido automaticamente pelo framework
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from curso_fastapi.app import app
from curso_fastapi.models import table_registry


# usado para evitar repetir client = TestClient(app) nos arquivos de teste toda hora
@pytest.fixture
def client():
    return TestClient(app)  # Cria um cliente de teste reutilizável


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
