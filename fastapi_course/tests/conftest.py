from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_course.app import app
from fastapi_course.database import get_session
from fastapi_course.models import User, table_registry
from fastapi_course.security import get_password_hash

# o arquivo conftest.py é um arquivo de configuração de testes do pytest

# esse decorator permite reutilizar esse bloco de código de teste em
# outros arquivos, é uma forma de de centralizar recursos comuns de teste


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # inicia uma conexão com o banco de dados sqlite em memória
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # cria todas as tabelas que estão no table_registry
    table_registry.metadata.create_all(engine)

    # entrega uma sessão (canal de comunicação com o DB) com yield
    # o yield entrega algo e espera
    with Session(engine) as session:
        yield session

    # exclui as tabelas criadas para teste
    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime.now()):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    password = 'testtest'

    user = User(
        username='test',
        email='test@test.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


# o @contextmanager torna aquela minha função um with ...
# dessa forma, ela vai executar tudo o que tiver antes e para no yield
# o yield vai retornar um time = tempo para a aplicação
# depois volta a executar o que tem abaixo dele depois que quem pediu
# a funcao ja usou o valor do time que o yield entregou
