from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_course.app import app


def test_root_must_retun_hello_world():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello World'}

    assert response.status_code == HTTPStatus.OK


def test_exercicio_html_return_ola_mundo():
    client = TestClient(app)

    response = client.get('/exercicio-html')

    assert 'olá mundo' in response.text
    assert response.status_code == HTTPStatus.OK
