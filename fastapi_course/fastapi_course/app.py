from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi_course.routers import auth, todos, users
from fastapi_course.schemas import Message

app = FastAPI(title='Curso FastAPI')
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
async def root():
    return {'message': 'Hello World'}


# ========================= EXERCICIO COM HTML =========================


@app.get(
    '/exercicio-html', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
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
