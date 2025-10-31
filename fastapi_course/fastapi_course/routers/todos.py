from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_course.database import get_session
from fastapi_course.models import Todo, User
from fastapi_course.schemas import (
    Message,
    TodoFilter,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fastapi_course.security import get_current_user

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_session)]
T_TodoFilter = Annotated[TodoFilter, Query()]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_class=JSONResponse,
    response_model=TodoPublic,
)
async def create_todo(
    todo: TodoSchema, session: Session, current_user: CurrentUser
):
    new_todo = Todo(
        user_id=current_user.id,
        title=todo.title,
        description=todo.description,
        state=todo.state,
    )

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)

    return new_todo


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=TodoList,
)
async def read_todos(
    session: Session, current_user: CurrentUser, todo_filter: T_TodoFilter
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.limit(todo_filter.limit).offset(todo_filter.offset)
    )

    # all(): Return all scalar values in a sequence
    return {'todos': todos.all()}


@router.delete(
    '/{todo_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
async def delete_todo(
    todo_id: int, session: Session, current_user: CurrentUser
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    await session.delete(db_todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully'}


@router.patch(
    '/{todo_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=TodoPublic,
)
async def update_todo(
    todo_id: int, todo: TodoUpdate, session: Session, current_user: CurrentUser
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo
