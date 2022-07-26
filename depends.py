from fastapi import Request
from auth_handler import signJWT
from schemas import UserLogin
from repositories import ChatRepository, UserRepository
from fastapi import HTTPException, status
from auth_handler import decodeJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from core.security import JWTBearer, verify_password
from db import User

from ormar.exceptions import NoMatch


async def get_current_user(request: Request):
    credentials: HTTPAuthorizationCredentials = await HTTPBearer().__call__(request)
    payload = decodeJWT(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth error!")
    user = await User.objects.filter(email = payload['user_id']).get()
    return user


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_chat_repository() -> ChatRepository:
    return ChatRepository()


async def check_user(data: UserLogin):
    try:
        user = await User.objects.get(email=data.email)
    except NoMatch:
        raise ValidationError("User with this email does not exist!")
    
    if not verify_password(data.password, user.hashed_password):
        return {
            "error": "wrong password!"
        }
    response = signJWT(user.email)
    response.update({'username': user.name})
    return response 


