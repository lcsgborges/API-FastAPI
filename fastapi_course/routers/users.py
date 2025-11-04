from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_course.database import get_session
from fastapi_course.models import User
from fastapi_course.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_course.security import get_current_user, get_password_hash
from fastapi_course.services import validate_password

router = APIRouter(prefix='/users', tags=['users'])

CurrentUser = Annotated[User, Depends(get_current_user)]
T_FilterPage = Annotated[FilterPage, Query()]
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_class=JSONResponse,
    response_model=UserPublic,
)
async def create_user(user: UserSchema, session: Session):
    if not validate_password(user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            detail='Weak password',
        )

    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            detail='The passwords must be the same',
        )

    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)  # dar um refresh nos dados do new_user

    return new_user


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserList,
)
async def read_users(
    session: Session, current_user: CurrentUser, filters: T_FilterPage
):
    users = await session.scalars(
        select(User).limit(filters.limit).offset(filters.offset)
    )

    return {'users': users}


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
async def read_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if db_user:
        return db_user

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail='User not found'
    )


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=UserPublic,
)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    if not validate_password(user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            detail='Weak password',
        )

    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_CONTENT,
            detail='The passwords must be the same',
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=Message,
)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
