from http import HTTPStatus

from fastapi.testclient import TestClient

from src.curso_fastapi.app import app


def test_root_deve_retornar_ok_e_hello_world():
    client = TestClient(app)  # arrange (organizar)

    response = client.get('/')  # act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (verificação)
    assert response.json() == {'message': 'Hello World'}  # assert
