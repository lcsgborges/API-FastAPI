from contextlib import contextmanager
from datetime import datetime

import factory
import factory.fuzzy
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fastapi_course.app import app
from fastapi_course.database import get_session
from fastapi_course.models import Todo, TodoState, User, table_registry
from fastapi_course.security import get_password_hash
from fastapi_course.settings import Settings

# o arquivo conftest.py é um arquivo de configuração de testes do pytest

# esse decorator permite reutilizar esse bloco de código de teste em
# outros arquivos, é uma forma de de centralizar recursos comuns de teste


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}#12345')


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.fixture
def client(session: AsyncSession):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# essa fixture vai criar um banco de dados pra sessão inteira pra executar
# todos os testes
@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:18', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    # cria todas as tabelas que estão no table_registry
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    # entrega uma sessão (canal de comunicação com o DB) com yield
    # o yield entrega algo e espera
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    # exclui as tabelas criadas para teste
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


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


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'Test@123'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


@pytest_asyncio.fixture
async def other_user(session: AsyncSession):
    password = 'test123'

    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


# o @contextmanager torna aquela minha função um with ...
# dessa forma, ela vai executar tudo o que tiver antes e para no yield
# o yield vai retornar um time = tempo para a aplicação
# depois volta a executar o que tem abaixo dele depois que quem pediu
# a funcao ja usou o valor do time que o yield entregou


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/login/',
        data={'username': user.username, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    s = Settings()
    # AQUI PODERIA MANIPULAR 's'
    return s


@pytest_asyncio.fixture
async def todo(session: AsyncSession, user):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    return todo
