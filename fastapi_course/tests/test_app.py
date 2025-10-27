from http import HTTPStatus

from fastapi_course.schemas import UserPublic
from fastapi_course.security import create_access_token


def test_root_must_return_hello_world(client):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}
    assert response.status_code == HTTPStatus.OK


def test_exercicio_html(client):
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


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_read_user_with_valid_id(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json() == user_schema


def test_read_user_with_invalid_id(client, user, token):
    response = client.get(
        '/users/1000', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        json={
            'username': 'sofia',
            'email': 'sofia@example.com',
            'password': 'sofia123',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == user_schema


def test_update_another_user(client, user, token):
    response = client.put(
        '/users/1000',
        json={
            'username': 'teste',
            'email': 'teste@example.com',
            'password': 'teste',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
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
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code == HTTPStatus.CONFLICT
    response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_another_user(client, user, token):
    response = client.delete(
        '/users/1000', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_login_access_token(client, user):
    response = client.post(
        '/login',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_invalid_user(client):
    response = client.post(
        '/login',
        data={'username': 'invalid-username', 'password': 'invalid-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_invalid_password(client, user):
    response = client.post(
        '/login',
        data={'username': user.username, 'password': 'invalid-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_with_invalid_sub(client):
    data = {'test': 'test'}
    token = create_access_token(data)

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_with_invalid_user_in_db(client, user):
    data = {'sub': 'invalid-user'}
    token = create_access_token(data)

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
