from pydantic import BaseModel, ConfigDict, EmailStr


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
