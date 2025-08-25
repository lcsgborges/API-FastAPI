from http import HTTPStatus

from fastapi.testclient import TestClient

from src.fastapi_zero.app import app


def test_read_root_return_hello_world():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK
