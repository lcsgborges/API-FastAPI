from http import HTTPStatus

from fastapi_course.schemas import UserPublic


def test_root_must_return_hello_world(client):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_html_return_ola_mundo(client):
    response = client.get('/exercicio-html')
    assert 'olá mundo' in response.text
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
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


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_read_users_without_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_read_user_with_valid_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == user_schema


def test_read_user_with_invalid_id(client, user):
    response = client.get('/users/1000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user_with_valid_id(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'sofia',
            'email': 'sofia@example.com',
            'password': 'sofia123',
        },
    )

    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == user_schema


def test_update_user_with_invalid_id(client, user):
    response = client.put(
        '/users/1000',
        json={
            'username': 'teste',
            'email': 'teste@example.com',
            'password': 'teste',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'test2',
            'email': 'test2@test.com',
            'password': 'test2test2',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test2',
            'email': user.email,
            'password': user.password,
        },
    )

    response.status_code == HTTPStatus.CONFLICT
    response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user_with_valid_id(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_with_invalid_id(client, user):
    response = client.delete('/users/1000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_login_access_token(client, user):
    response = client.post(
        '/login',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
