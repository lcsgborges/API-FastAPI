from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


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
