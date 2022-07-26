from core.security import JWTBearer
from auth_handler import signJWT
from depends import check_user, get_user_repository, get_chat_repository, get_current_user
from schemas import ChatIn, ChatSchema, MessageIn, MessageSchema, UserIn, UserLogin, UserSchema
from fastapi import APIRouter, Depends
from repositories import ChatRepository, UserRepository
from typing import List

router = APIRouter()


#все чаты
# один чат
# отправить сообщение


@router.post("/register")
async def register(user: UserIn, users: UserRepository = Depends(get_user_repository)):
    await users.create(u=user)
    return signJWT(user.name)


@router.post("/login")
async def login(checked_user = Depends(check_user)):
    return checked_user


@router.get("/users", response_model=List[UserSchema], dependencies=[Depends(JWTBearer())])
async def users(username: str, users: UserRepository = Depends(get_user_repository)):
    return await users.search(username=username)


@router.get("/messages", response_model=List[MessageSchema])
async def messages(chats: ChatRepository = Depends(get_chat_repository)):
    return await chats.messages()


# @router.post("/messages_create", response_model=MessageSchema)
@router.post("/messages_create")
async def create_message(message: MessageIn, chats: ChatRepository = Depends(get_chat_repository), current_user = Depends(get_current_user)):
    # print(await current_user)
    return await chats.create_message(m = message, current_user = current_user)


@router.get("/chats", response_model=List[ChatSchema], dependencies=[Depends(JWTBearer())])
async def chats(chats: ChatRepository = Depends(get_chat_repository)):
    return await chats.read_all()


@router.post("/chats_create", response_model=ChatSchema)
async def create_chat(chat: ChatIn, chats: ChatRepository = Depends(get_chat_repository)):
    return await chats.create(c=chat)
