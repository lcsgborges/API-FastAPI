from http import HTTPStatus


def test_root_must_retun_hello_world(client):
    # Arrange -> conftest

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Hello World'}

    assert response.status_code == HTTPStatus.OK


def test_exercicio_html_return_ola_mundo(client):
    response = client.get('/exercicio-html')

    assert 'olá mundo' in response.text
    assert response.status_code == HTTPStatus.OK


def test_create_user_return_user_public(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'alice123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'alice', 'email': 'alice@example.com'},
        ]
    }


def test_read_user_with_id_success(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_read_user_with_id_failed(client):
    response = client.get('/users/1000')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_success(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'sofia',
            'email': 'sofia@example.com',
            'password': 'sofia123',
        },
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'sofia',
        'email': 'sofia@example.com',
    }


def test_update_user_failed(client):
    response = client.put(
        '/users/1000',
        json={
            'username': 'teste',
            'email': 'teste@example.com',
            'password': 'teste',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_success(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'id': 1,
        'username': 'sofia',
        'email': 'sofia@example.com',
    }


def test_delete_user_failed(client):
    response = client.delete('/users/1000')

    assert response.status_code == HTTPStatus.NOT_FOUND
