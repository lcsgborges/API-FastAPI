from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_course.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


# o yield faz uma parada aqui, o return sai da função e
# não volta pra fechar a sessão depois

# expire_on_commit = False, pois não sabemos se todas as corrotinas "liberaram"
# a sessão
