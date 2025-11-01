from http import HTTPStatus


def test_root_must_return_hello_world(client):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_html(client):
    response = client.get('/exercicio-html')
    assert 'olá mundo' in response.text
    assert response.status_code == HTTPStatus.OK
