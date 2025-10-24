from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title='Curso FastAPI')

database = []


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
def create_user(user: UserSchema):
    # model_dump() pega o meu model (objeto) e transforma em um dict
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserList,
)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_to_update = UserDB(**user.model_dump(), id=user_id)

    database[user_id - 1] = user_to_update

    return user_to_update


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database.pop(user_id - 1)


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


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
