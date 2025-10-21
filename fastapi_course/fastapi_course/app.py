from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .schemas import Message

app = FastAPI(title='Curso FastAPI')


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
async def root():
    return {'message': 'Hello World'}
