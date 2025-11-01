from http import HTTPStatus

import pytest
from sqlalchemy.exc import DataError

from fastapi_course.models import Todo, TodoState, User
from tests.conftest import TodoFactory


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as time:
        response = client.post(
            '/todos/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'test',
                'description': 'test description',
                'state': 'draft',
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            'id': 1,
            'title': 'test',
            'description': 'test description',
            'state': 'draft',
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        }


@pytest.mark.asyncio
async def test_read_todos(mock_db_time, session, user, client, token):
    with mock_db_time(model=Todo) as time:
        todo = TodoFactory(user_id=user.id)

        session.add(todo)
        await session.commit()
        await session.refresh(todo)

        response = client.get(
            '/todos/', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['todos'] == [
            {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'state': todo.state,
                'created_at': time.isoformat(),
                'updated_at': time.isoformat(),
            }
        ]


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    await session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_should_return_2_todos(session, client, user, token):
    expected_todos = 2

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Todo Title')
    )

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    await session.commit()

    response = client.get(
        '/todos?title=Test%20Todo%20Title',  # %20 pra representar espaço
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(
            5, user_id=user.id, description='Test Todo Description Test'
        )
    )

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))

    await session.commit()

    response = client.get(
        '/todos?description=Test%20Todo%20Description%20Test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )

    await session.commit()

    response = client.get(
        '/todos?state=draft', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_delete_todo_(client, token, todo):
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/100', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(session, client, token, other_user):
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()

    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo_error(client, token, todo):
    response = client.patch(
        f'/todos/{todo.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo_alter_title(client, todo, token):
    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'New Title Test'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'New Title Test'


@pytest.mark.asyncio
async def test_create_todo_error(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='test',
        user_id=user.id,
    )

    session.add(todo)

    with pytest.raises(DataError):
        await session.commit()


def test_list_todos_title_min_lenght_error(client, token):
    tiny_string = 'a'

    response = client.get(
        f'/todos/?title={tiny_string}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_list_todos_title_max_lenght_error(client, token):
    large_string = 'a' * 31

    response = client.get(
        f'/todos/?title={large_string}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
