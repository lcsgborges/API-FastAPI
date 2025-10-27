from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_course.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


# o yield faz uma parada aqui, o return sai da função e
# não volta pra fechar a sessão depois
