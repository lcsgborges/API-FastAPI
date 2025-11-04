from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi_course.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

    # model_config recebe uma configuração adicional com ConfigDict.
    # dizemos para tentar encontrar os atributos de UserPublic no objeto
    # passado em model_validate


class UserList(BaseModel):
    users: list[UserPublic]


class TokenJWT(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: Optional[str] = None  # Optional[str] == str | None
    description: Optional[str] = None
    state: Optional[str] = None


class TodoFilter(FilterPage):
    title: Optional[str] = Field(default=None, min_length=3, max_length=30)
    description: Optional[str] = Field(default=None, min_length=3)
    state: Optional[str] = None
