"""
Arquivo de testes para testar o app construido com fastapi
"""

from http import HTTPStatus


def test_root_deve_retornar_ok_e_hello_world(client):  # arrange (organizar)
    response = client.get('/')  # act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (verificação)
    assert response.json() == {'message': 'Hello World'}


def test_root_html_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/exercicio-html/')

    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user(client):
    response = client.post(  # envio UserSchema
        '/users/', json={'username': 'test', 'email': 'test@test.com', 'password': 'password'}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'username': 'test', 'email': 'test@test.com'}  # UserPublic


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'username': 'test', 'email': 'test@test.com', 'id': 1}]}


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'test', 'email': 'test@test.com', 'id': 1}


def test_read_user_id_nao_existe(client):
    response = client.get('/users/42')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1', json={'password': 'password', 'username': 'test2', 'email': 'test@test.com'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'test2', 'email': 'test@test.com', 'id': 1}


def test_update_user_id_nao_existe(client):
    response = client.put(
        '/users/42', json={'password': 'password', 'username': 'test2', 'email': 'test@test.com'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_id_nao_existe(client):
    response = client.delete('/users/42')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
