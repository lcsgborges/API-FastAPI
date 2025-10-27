from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_course.database import get_session
from fastapi_course.models import User
from fastapi_course.schemas import TokenJWT
from fastapi_course.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/login/',
    status_code=HTTPStatus.OK,
    response_class=JSONResponse,
    response_model=TokenJWT,
)
def login_for_access_token(session: T_Session, form_data: OAuth2Form):
    db_user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    token = create_access_token({'sub': form_data.username})

    return {'access_token': token, 'token_type': 'Bearer'}
