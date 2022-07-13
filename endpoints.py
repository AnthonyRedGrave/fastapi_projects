from schemas import UserIn
from fastapi import APIRouter, Depends
from repositories import UserRepository

router = APIRouter()

def get_user_repository() -> UserRepository:
    return UserRepository()

@router.post("/register")
async def register(user: UserIn, users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)