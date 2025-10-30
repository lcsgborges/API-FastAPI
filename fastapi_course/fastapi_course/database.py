from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_course.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# nao faz sentido esse get_session ser testado, pois estamos usando uma fixture
# para criar uma session pro nosso db em memória

# o yield faz uma parada aqui, o return sai da função e
# não volta pra fechar a sessão depois

# expire_on_commit = False, pois não sabemos se todas as corrotinas "liberaram"
# a sessão
