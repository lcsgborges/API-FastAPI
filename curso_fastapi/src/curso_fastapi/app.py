from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """
    Primeiro código com fastapi para evitar a maldição do Hello World
    """
    return {'message': 'Hello World'}


@app.get('/exercicio-html/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    """
    Exercício proposto na unidade 02 para retornar HTML
    """
    return """
    <html>
        <head>
            <title> Olá Mundo </title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
    </html>
"""


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    """
    Rota para criar um novo usuário
    """
    # o model_dump() transforma o objeto em um dicionario

    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    """
    Rota para obter todos os usuários criados
    """
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublic, status_code=HTTPStatus.OK)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = database[user_id - 1]

    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user: UserSchema, user_id: int):
    """
    Rota para atualizar um usuário já existente a partir do ID
    """
    # se o id não existir no banco de dados:
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserDB(id=user_id, **user.model_dump())  # novo usuário já com as alterações

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}
