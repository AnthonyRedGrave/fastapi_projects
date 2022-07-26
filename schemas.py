from pyexpat.errors import messages
from typing import List
from pydantic import BaseModel, EmailStr, constr, ValidationError, validator
from db import User, Chat
from ormar.exceptions import NoMatch


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str


    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValidationError("passwords are not similar!")
        return v


class MessageSchema(BaseModel):
    id: int
    text: str
    user: UserSchema


class ChatSchema(BaseModel):
    id: int
    messages: List[MessageSchema]
    users: List[UserSchema]
    

class MessageIn(BaseModel):
    text: str
    chat: int

    @validator("chat")
    def chat_exists(cls, v, values, **kwargs):
        try:
            chat = Chat.objects.get(id=v)
            return chat
        except:
            raise ValidationError("Chat with this id doesn't exist!")
  

class ChatIn(BaseModel):
    users: List[str]

    @validator("users")
    def users_exists(cls, v, values, **kwargs):
        # print(v, "v")
        return (User.objects.filter(email__in=v), v)