from http import HTTPStatus

from fastapi_course.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'Alice@123',
            'confirm_password': 'Alice@123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
    }


def test_create_user_with_weak_password(client):
    response = client.post(
        '/users',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': '123bob',
            'confirm_password': '123bob',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': 'Weak password'}


def test_create_passwords_diff(client):
    response = client.post(
        '/users',
        json={
            'username': 'cj',
            'email': 'cj@email.com',
            'password': 'CJ@12345cj',
            'confirm_password': 'CJ@12345',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': 'The passwords must be the same'}


def test_create_user_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.clean_password,
            'confirm_password': user.clean_password,
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


def test_read_user_with_invalid_id(client, user, other_user, token):
    response = client.get(
        f'/users/{other_user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'sofia',
            'email': 'sofia@example.com',
            'password': 'Sofia123@',
            'confirm_password': 'Sofia123@',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK

    assert response.json() == user_schema


def test_update_user_password_diffs(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': 'emailtestemail@example.com',
            'password': user.clean_password,
            'confirm_password': 'Teste99@99',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': 'The passwords must be the same'}


# o token gerado aqui é do user do conftest, logo, vai tem que dar erro ao
# tentar atualizar o other_user
def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        json={
            'username': 'teste',
            'email': 'teste@example.com',
            'password': 'teste@123',
            'confirm_password': 'teste@123',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_weak_password(client, token, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'teste',
            'email': 'teste@example.com',
            'password': 'teste@',
            'confirm_password': 'teste@',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert response.json() == {'detail': 'Weak password'}


def test_update_integrity_error(client, user, token, other_user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': other_user.username,
            'email': other_user.email,
            'password': other_user.clean_password,
            'confirm_password': other_user.clean_password,
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


def test_delete_another_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
