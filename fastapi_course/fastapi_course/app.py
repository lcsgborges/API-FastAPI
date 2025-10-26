from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_session
from .models import User
from .schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='Curso FastAPI')


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
async def root():
    return {'message': 'Hello World'}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    new_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # dar um refresh nos dados do new_user

    return new_user


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserList,
)
def read_users(
    session: Session = Depends(get_session), limit: int = 10, offset: int = 0
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user:
        return db_user

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found'
    )


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user:
        try:
            db_user.username = user.username
            db_user.email = user.email
            db_user.password = user.password
            session.commit()
            session.refresh(db_user)
            return db_user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username or Email already exists',
            )

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found'
    )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user:
        session.delete(db_user)
        session.commit()

        return {'message': 'User deleted'}

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found'
    )


# ========================= EXERCICIO COM HTML =========================


@app.get('/exercicio-html', response_class=HTMLResponse)
async def exercicio_html():
    return """
    <html>
        <head>
            <title>Exercicio HTML</title>
        </head>
        <body>
            <h1>olá mundo</h1>
            <p>Exercício de HTML da aula: Introdução ao desenvolvimento WEB</p>
        </body>
    </html>
"""
