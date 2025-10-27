from http import HTTPStatus

from fastapi_course.security import create_access_token


def test_login_access_token(client, user):
    response = client.post(
        'auth/login/',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_access_token_invalid_user(client):
    response = client.post(
        'auth/login',
        data={'username': 'invalid-username', 'password': 'invalid-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_access_token_invalid_password(client, user):
    response = client.post(
        'auth/login',
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
